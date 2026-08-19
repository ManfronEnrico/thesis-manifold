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
    """Features this matrix actually has (DEC-OPEN-WORLD).

    Categories differ in capability, not only in values: Nielsen reports no
    promotion for danskvand or RTD, so `promo_intensity` is omitted there rather
    than zero-filled. A fixed list would raise KeyError on exactly those."""
    wanted = FEATURES if wanted is None else wanted
    return [c for c in wanted if c in fm.columns]


def _period(row):
    return f"{int(row['period_year'])}-{int(row['period_month']):02d}"


def train_category(cat: str, slug: str) -> dict | None:
    """Fit, calibrate and persist one category. Returns its metadata."""
    from xgboost import XGBRegressor

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

    params = {}
    pf = THESIS_RESULTS_SRQ1_DIR / "tuned_params.json"
    if pf.is_file():
        params = json.loads(pf.read_text(encoding="utf-8")).get(
            f"brand/{cat}/XGBoost", {})

    tracemalloc.start()
    t0 = time.perf_counter()

    # 1. CALIBRATION model: train only, so val residuals are genuinely
    #    out-of-sample. Its predictions are never served.
    m_cal = XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params)
    m_cal.fit(tr[feats].fillna(0.0), tr["log_sales_units"].values)
    if len(va):
        resid = np.abs(va["log_sales_units"].values
                       - m_cal.predict(va[feats].fillna(0.0)))
        q90 = float(np.quantile(resid, 0.90))
        calib_note = "90th percentile of |residual| on held-out validation rows"
    else:
        # Deliberately wide rather than deliberately confident: a marker that no
        # honest calibration was possible, not an estimate.
        q90 = 0.5
        calib_note = "NO validation rows -- q90=0.5 is a placeholder, not calibrated"

    # 2. SERVING model: train+val, because withholding val from the deployed
    #    model wastes data for no gain. Test is never seen by either model.
    m_srv = XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params)
    trval = pd.concat([tr, va]).sort_values("period_index")
    m_srv.fit(trval[feats].fillna(0.0), trval["log_sales_units"].values)

    elapsed = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_file = MODELS_DIR / f"{cat}_xgboost.json"
    m_srv.save_model(str(model_file))

    meta = {
        "category": cat,
        "model": "XGBoost(tuned)",
        "model_file": model_file.name,
        "features": feats,
        "n_features": len(feats),
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

    print(f"  {cat:14s} trained on {len(trval):5d} rows through {meta['trained_through']}"
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
