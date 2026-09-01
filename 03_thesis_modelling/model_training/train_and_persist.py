#!/usr/bin/env python3
"""
Train the forecasting models ONCE and write them to disk.

WHY THIS EXISTS
---------------
Training belongs in model_training/. Serving belongs in
model_serving_interface/. Until now the boundary was violated in both
directions:

  - `forecast_service.build_service()` retrained every category on every call
  - `srq4_experiment._eval_forecast()` retrained on EVERY SINGLE TOOL CALL,
    so a 90-run experiment retrained the model 30 times for identical output
  - `srq2_synthesis.py` retrained on IMPORT

Three copies of the same training logic, which is also how the conformal
calibration bug (intervals 3.9x too narrow) got fixed in one copy and survived
in another.

This script is the single training entry point. It writes, per category:

    04_thesis_results/srq1/models/{cat}_xgboost.json     the fitted booster
    04_thesis_results/srq1/models/{cat}_metadata.json    everything needed to
                                                          serve and to audit it

Serving loads these. Serving never fits.

THE TWO MODELS PER CATEGORY, AND WHY
------------------------------------
  m_cal  fitted on TRAIN only. Its residuals on VAL give the conformal q90.
         Split conformal requires a calibration set the model has never seen.
  m_srv  fitted on TRAIN+VAL. This is what actually produces forecasts, because
         withholding val from the deployed model wastes data for no gain.

Only the CALIBRATION must be out-of-sample. Conflating these two is exactly the
bug that made intervals 3.9x too narrow (P0037 F10).

TEST IS NEVER TOUCHED by either model. It is reserved for measuring accuracy.

Usage:
    python 03_thesis_modelling/model_training/train_and_persist.py
    python 03_thesis_modelling/model_training/train_and_persist.py --category CSD
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import tracemalloc
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir

warnings.filterwarnings("ignore")

SEED = 42
MODELS_DIR = THESIS_RESULTS_SRQ1_DIR / "models"

CATEGORIES = {"CSD": "csd", "danskvand": "danskvand",
              "energidrikke": "energidrikke", "RTD": "rtd"}

# weighted_dist is deliberately absent: tested, cleared for leakage, but worse
# out-of-sample in 3 of 4 categories (P0036 task 7).
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "peak_month", "promo_intensity"]


def available_features(fm, wanted=None):
    """Features this matrix actually has (DEC-DISCOVER-COLUMNS).

    Categories differ in capability, not only in values: Nielsen reports no
    promotion for danskvand or RTD, so `promo_intensity` is omitted there rather
    than zero-filled. A fixed list would raise KeyError on exactly those."""
    wanted = FEATURES if wanted is None else wanted
    return [c for c in wanted if c in fm.columns]


def _period(row):
    return f"{int(row['period_year'])}-{int(row['period_month']):02d}"


def best_model_for(cat: str) -> str:
    """The model SRQ1 selected for this category, read from metrics.csv.

    Hardcoding XGBoost was wrong: after the Ridge log-scaling fix, danskvand's
    best model is Ridge at 19.2% WMAPE against XGBoost's 32.6%. Serving XGBoost
    there would hand Scenario C a model 13 points worse than the one SRQ1
    selected -- and the thesis claim is that the SELECTED model is what the
    agent gets."""
    # Two results files exist and they are NOT comparable:
    #   metrics.csv        train-only, DEFAULT hyperparameters (a ranking ladder)
    #   tuned_metrics.csv  train+val, TUNED hyperparameters (the deployed regime)
    # The served model uses the second regime, so selection must read the second
    # file. Reading metrics.csv would compare a tuned candidate against untuned
    # ones -- on danskvand that picked Ridge at 19.2% (untuned, train-only) over
    # XGBoost at 20.0% (tuned, train+val), which are not the same measurement.
    #
    # Ridge and SeasonalNaive appear only in metrics.csv: Ridge is the untuned
    # linear baseline, SeasonalNaive the floor. Both are candidates ONLY if they
    # beat the best tuned model, and that comparison is unavailable, so they are
    # included from metrics.csv with an explicit margin requirement below.
    cvf = THESIS_RESULTS_SRQ1_DIR / "cv_metrics.csv"
    tf = THESIS_RESULTS_SRQ1_DIR / "tuned_metrics.csv"
    mf = THESIS_RESULTS_SRQ1_DIR / "metrics.csv"
    best, best_wmape = "XGBoost", float("inf")

    # P0044 F27/F29: select from the CV study when available, on its CROSS-
    # VALIDATED score rather than on test_wmape.
    #
    # Two changes, and the second matters more than the first. tuned_metrics.csv
    # ranked candidates by `test_wmape` -- the held-out test set -- so the served
    # model was chosen using the same data the thesis then reports it against.
    # That is selection on the test set, and it optimistically biases every
    # downstream number. cv_metrics.csv carries `cv_score`, the expanding-window
    # validation score, which never touches test. Selecting on it keeps the test
    # set genuinely held out.
    #
    # `tuned_for == "wmape"` filters to the objective the thesis reports.
    if cvf.is_file():
        c = pd.read_csv(cvf)
        c = c[(c.category == cat) & (c.tuned_for == "wmape") & c.cv_score.notna()]
        if len(c):
            r = c.sort_values("cv_score").iloc[0]
            best, best_wmape = r["model"], float(r["cv_score"])

    if best_wmape == float("inf") and tf.is_file():
        t = pd.read_csv(tf)
        t = t[(t.category == cat) & t.test_wmape.notna()]
        if len(t):
            r = t.sort_values("test_wmape").iloc[0]
            best, best_wmape = r["model"], float(r["test_wmape"])

    # An untuned baseline is only preferred if it wins by a clear margin, since
    # it has not had the benefit of tuning and a narrow win is likely noise.
    if mf.is_file():
        m = pd.read_csv(mf)
        m = m[(m.category == cat) & m.wmape.notna() & (m.model == "Ridge")]
        if len(m):
            rw = float(m.iloc[0]["wmape"])
            if rw < best_wmape * 0.9:      # >10% relative improvement
                best, best_wmape = "Ridge", rw

    return best


def _make(model_name: str, params: dict):
    """Build an unfitted estimator. Linear models get the log-scaling pipeline;
    tree models do not need it (they are invariant to monotone transforms of a
    feature, which is why only Ridge broke on raw-unit lags)."""
    if model_name == "Ridge":
        from sklearn.linear_model import Ridge
        from sklearn.preprocessing import StandardScaler, FunctionTransformer
        from sklearn.pipeline import make_pipeline
        # np.log1p by name, not a local function: pickling a locally-defined
        # transformer stores a reference to __main__._log_volume_cols, which does
        # not exist when the model is loaded from anywhere else (AttributeError
        # on unpickle). A numpy ufunc pickles by reference and always resolves.
        #
        # Applied to ALL columns rather than only the volume ones: the remaining
        # features are month (1-12), quarter (1-4), peak_month (0/1) and
        # promo_intensity (0-1), all non-negative and small, so log1p is a
        # monotone rescale that StandardScaler then normalises away. Keeping the
        # transformer column-agnostic is what makes it portable.
        return make_pipeline(
            FunctionTransformer(np.log1p, validate=True),
            StandardScaler(), Ridge(alpha=1.0, random_state=SEED))
    if model_name == "LightGBM":
        from lightgbm import LGBMRegressor
        return LGBMRegressor(random_state=SEED, verbose=-1, n_jobs=-1, **params)
    from xgboost import XGBRegressor
    return XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params)


# Volume-valued columns are in RAW units while the target is LOG. A linear model
# cannot bridge that (it would have to approximate a logarithm with a straight
# line) and extrapolates catastrophically; tree models are unaffected.
LOG_SCALE_FEATURES = ("lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
                      "rolling_mean_4", "rolling_std_4", "rolling_mean_13")


def _persist(model, model_name: str, path_stem: Path) -> str:
    """Save a fitted model. XGBoost has a native JSON format that is portable and
    diffable; everything else falls back to joblib."""
    if model_name == "XGBoost":
        f = path_stem.with_suffix(".json")
        model.save_model(str(f))
    else:
        import joblib
        f = path_stem.with_suffix(".joblib")
        joblib.dump(model, f)
    return f.name


def train_category(cat: str, slug: str) -> dict | None:
    """Fit, calibrate and persist one category. Returns its metadata."""

    eng = get_category_engineered_bymonth_dir(cat)
    f = eng / f"{slug}_feature_matrix_h3.parquet"
    if not f.is_file():
        print(f"  {cat:14s} SKIP -- no feature matrix at {f}")
        return None

    fm = pd.read_parquet(f)
    feats = available_features(fm)
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr = d[d.split == "train"].sort_values("period_index")
    va = d[d.split == "val"].sort_values("period_index")
    te = d[d.split == "test"].sort_values("period_index")

    if len(tr) < 30:
        print(f"  {cat:14s} SKIP -- only {len(tr)} training rows")
        return None

    model_name = best_model_for(cat)
    params = {}
    # P0044 F27: prefer cv_params.json (srq1_benchmark_cv.py -- 100 trials,
    # 4-fold expanding-window CV, dual objective, convergence curve saved) over
    # tuned_params.json (srq1_benchmark_tuned.py -- 30 trials, ONE validation
    # split, wMAPE only).
    #
    # The CV script exists precisely to fix the tuned script's three documented
    # weaknesses, and it produced better held-out numbers: on CSD/LightGBM,
    # test wMAPE 14.54% (CV) against 15.59% (served). Its output was nevertheless
    # consumed by nothing for two weeks, because the two scripts write different
    # filenames and nothing read the newer one -- so no test failed and no error
    # surfaced. The served models were built on the weaker tuning throughout.
    #
    # Key schemas differ: "{cat}/{model}/{objective}" here vs
    # "brand/{cat}/{model}" in the old file. wMAPE is the objective the thesis
    # reports against, so that variant is used. tuned_params.json remains as a
    # fallback so a missing CV entry degrades instead of crashing.
    cvf = THESIS_RESULTS_SRQ1_DIR / "cv_params.json"
    if cvf.is_file():
        params = json.loads(cvf.read_text(encoding="utf-8")).get(
            f"{cat}/{model_name}/wmape", {})
    if not params:
        pf = THESIS_RESULTS_SRQ1_DIR / "tuned_params.json"
        if pf.is_file():
            # Ridge is the untuned baseline and has no entry; it uses its defaults.
            params = json.loads(pf.read_text(encoding="utf-8")).get(
                f"brand/{cat}/{model_name}", {})
            if params:
                print(f"  {cat:14s} NOTE: no CV entry for {model_name}; "
                      f"falling back to tuned_params.json")

    tracemalloc.start()
    t0 = time.perf_counter()

    # 1. CALIBRATION model: train only, so val residuals are genuinely
    #    out-of-sample. Its predictions are never served.
    # log1p is undefined below -1, and the pipeline applies it to every column,
    # so clip once here rather than inside a custom (unpicklable) transformer.
    def _X(df):
        return df[feats].fillna(0.0).clip(lower=0) if model_name == "Ridge"             else df[feats].fillna(0.0)

    m_cal = _make(model_name, params)
    m_cal.fit(_X(tr), tr["log_sales_units"].values)
    if len(va):
        resid = np.abs(va["log_sales_units"].values - m_cal.predict(_X(va)))
        q90 = float(np.quantile(resid, 0.90))
        calib_note = "90th percentile of |residual| on held-out validation rows"
    else:
        # Deliberately wide rather than deliberately confident: a marker that no
        # honest calibration was possible, not an estimate.
        q90 = 0.5
        calib_note = "NO validation rows -- q90=0.5 is a placeholder, not calibrated"

    # 2. SERVING model: train+val, because withholding val from the deployed
    #    model wastes data for no gain. Test is never seen by either model.
    m_srv = _make(model_name, params)
    trval = pd.concat([tr, va]).sort_values("period_index")
    m_srv.fit(_X(trval), trval["log_sales_units"].values)

    elapsed = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_file_name = _persist(m_srv, model_name, MODELS_DIR / f"{cat}_model")

    meta = {
        "category": cat,
        "model": f"{model_name}(tuned)" if params else model_name,
        "model_file": model_file_name,
        "model_selected_by": "lowest test WMAPE in SRQ1 metrics.csv",
        "features": feats,
        "n_features": len(feats),
        "clip_negative_features": model_name == "Ridge",
        "hyperparameters": params,
        "seed": SEED,
        # Provenance: what the served model saw, and what the interval was
        # calibrated against. SRQ2 defines traceability as a recorded mapping
        # from tool call to forecast, so these travel with every forecast.
        "trained_on": "train+val",
        "trained_through": _period(trval.iloc[-1]) if len(trval) else None,
        "n_train_rows": int(len(trval)),
        "calibrated_on": "val",
        "calibrated_through": _period(va.iloc[-1]) if len(va) else None,
        "n_calibration_rows": int(len(va)),
        "calibration_note": calib_note,
        "q90_log": q90,
        "interval_method": "split conformal, 90% quantile of validation residuals",
        # Test boundaries are recorded so a caller can assert that a requested
        # target month is genuinely held out.
        "test_from": _period(te.iloc[0]) if len(te) else None,
        "test_through": _period(te.iloc[-1]) if len(te) else None,
        "test_months": sorted({_period(r) for _, r in te.iterrows()}) if len(te) else [],
        "n_test_rows": int(len(te)),
        "brands": int(d.brand.nunique()),
        # Compute cost, for the ~8 GB constraint claim. tracemalloc sees Python
        # allocations only, so this is a lower bound on the Python side.
        "train_seconds": round(elapsed, 3),
        "train_peak_ram_mb": round(peak / 1e6, 2),
        "trained_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (MODELS_DIR / f"{cat}_metadata.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8", newline="\n")

    print(f"  {cat:14s} {model_name:9s} on {len(trval):5d} rows through {meta['trained_through']}"
          f" | q90={q90:.3f} from {len(va)} val rows"
          f" | {elapsed:.2f}s {peak/1e6:.1f}MB")
    return meta


def main():
    ap = argparse.ArgumentParser(description="Train and persist the forecasting models")
    ap.add_argument("--category", default=None, help="one category (default: all)")
    a = ap.parse_args()

    cats = {a.category: CATEGORIES[a.category]} if a.category else CATEGORIES
    print(f"Training {len(cats)} categor{'y' if len(cats)==1 else 'ies'} "
          f"-> {MODELS_DIR}\n")
    metas = [m for c, s in cats.items() if (m := train_category(c, s))]

    if metas:
        idx = {m["category"]: {k: m[k] for k in
                               ("model_file", "trained_through", "q90_log",
                                "test_from", "test_through", "trained_at_utc")}
               for m in metas}
        (MODELS_DIR / "index.json").write_text(
            json.dumps(idx, indent=2), encoding="utf-8", newline="\n")
        print(f"\nWrote {len(metas)} model(s) + index.json to {MODELS_DIR}")
        print("Serving loads these. Serving never fits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
