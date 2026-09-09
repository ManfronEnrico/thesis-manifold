#!/usr/bin/env python3
"""
SRQ1 forecasting benchmark — Optuna-tuned LightGBM + XGBoost.

For each (dataset, category): tune on the validation split (objective = WMAPE),
refit the best config on train+val, evaluate once on test. Reports tuned
WMAPE / mean-MAPE / median-MAPE and saves best params for the thesis appendix.
Compares against the untuned run (scripts/srq1_benchmark.py).

Self-contained, seed=42, reproducible. No Prometheus/Nika dependency.
Usage:  .venv/bin/python scripts/srq1_benchmark_tuned.py [--trials 30]
Output: 04_thesis_results/srq1/{tuned_metrics.csv, tuned_params.json, tuned_summary.md}
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import optuna

# Repo root located by searching upward for PATHS.py rather than by a fixed
# parents[N] index: the index silently breaks whenever a script moves a
# directory deeper, which is exactly what happened in the 2026-08-19
# reorganisation (ModuleNotFoundError: No module named 'PATHS').
_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, THESIS_DATA_ENGINEERED_BYMONTH_DIR

warnings.filterwarnings("ignore")
# The active horizon, and the paths that follow from it. ONE source, so the
# matrix read and the results written can never describe different horizons
# (P0049 F24). Set SRQ1_HORIZON=1 to run the secondary horizon.
from _horizon import HORIZON, matrix_path, results_root, banner  # noqa: E402,F401
from _features import FEATURES as _FEATURES, resolve as _resolve_feats, describe as _describe_feats  # noqa: E402,F401
optuna.logging.set_verbosity(optuna.logging.WARNING)

class _SRQ1Out:
    """Routes `OUT / "file.ext"` into figures/, tables/ or models/ by role.

    Added 2026-09-06 (P0046 Phase 3b). The results tier is the tree humans browse
    to pick thesis artefacts, so every SRQ folder has the same three-way shape.
    This preserves each existing call site while filing the output correctly, and
    it resolves READS too, so scripts reading a sibling's output keep working.

    Splitting by role rather than by extension keeps a `.csv` and its rendered
    `.md` twin together -- they are one artefact in two formats.
    """

    _MODELS = {"cv_params.json", "pooled_params.json", "tuned_params.json"}
    _FIGURES = {".png", ".svg", ".pdf"}

    def __init__(self, base):
        self._base = base

    def _sub(self, name):
        if name in self._MODELS:
            return self._base / "models"
        if Path(name).suffix.lower() in self._FIGURES:
            return self._base / "figures"
        return self._base / "tables"

    _PASSTHROUGH = {"figures", "tables", "models"}

    def __truediv__(self, name):
        # A bare subfolder name is already the destination -- pass it straight
        # through, or `RES / "figures"` would be filed as if it were a table.
        if str(name) in self._PASSTHROUGH:
            d = self._base / str(name)
            d.mkdir(parents=True, exist_ok=True)
            return d
        d = self._sub(str(name))
        d.mkdir(parents=True, exist_ok=True)
        return d / str(name)

    def __getattr__(self, attr):
        return getattr(self._base, attr)

    def __fspath__(self):
        return str(self._base)

    def __str__(self):
        return str(self._base)


OUT = _SRQ1Out(results_root())
SEED = 42


# ---------------------------------------------------------------------------
# XGB_N_JOBS: reproducibility, not performance. READ BEFORE CHANGING.
#
# XGBoost's histogram builder sums gradient statistics per thread and reduces
# them in completion order. Floating-point addition is not associative, so a
# different THREAD COUNT gives a different sum, a different split, and a
# different tree -- with the seed, the data and every hyperparameter identical.
# `random_state` fixes the subsample/colsample draw; it does NOT fix the order
# of a parallel reduction.
#
# Measured on danskvand brand-month, seed 42, all else held constant
# (2026-09-06):
#     n_jobs=1  -> WMAPE 34.648708   (repeatable across runs)
#     n_jobs=2  -> WMAPE 34.946778
#     n_jobs=4  -> WMAPE 35.397904
#     n_jobs=8  -> WMAPE 37.297544   (== n_jobs=-1 on this 8-core machine)
#
# A 2.65pp spread from thread count alone. That is larger than most of the
# holiday-enrichment effects reported in appendix table 94, so with n_jobs=-1
# a reader on a different machine could not reproduce the sign of a finding.
# This is what caused the XGBoost-only drift when srq1_benchmark.py was re-run
# on 2026-09-06 against matrices whose new holiday columns no models read
# (P0047 F18).
#
# Fixed to 1 for every ACCURACY number. The cost is wall-clock on a
# single fit, which is seconds here and is not a reported quantity.
#
# DELIBERATELY NOT APPLIED to srq1_profiling.py: that script measures memory
# and latency under realistic multi-core execution, where n_jobs=-1 is the
# thing being measured. It records the core count with its results and says so
# in its output table.
# ---------------------------------------------------------------------------
XGB_N_JOBS = 1
CATS = {"CSD": "csd", "danskvand": "danskvand", "energidrikke": "energidrikke", "RTD": "rtd"}
# Grain: brand x month only, per DEC-GRAIN (2026-07-12). The "bychain" entry was
# removed by P0035 (2026-08-01) along with its deleted data directory.
# NOTE: the tag is "brand" (not "bymonth") because the existing
# 04_thesis_results/srq1/tuned_params.json keys are prefixed "brand/". Renaming
# it here would orphan those recorded results.
DATASETS = {
    "brand":   THESIS_DATA_ENGINEERED_BYMONTH_DIR,
}
# weighted_distribution / weighted_dist is deliberately ABSENT (P0036 task 7,
# 2026-08-19).
#
# Note these scripts previously named "weighted_distribution", a column that does
# not exist in the matrix (it is "weighted_dist" after step 1's RENAMES). They
# were therefore already training without it -- silently, since
# available_features() drops unknown names. This makes that state deliberate and
# documented rather than accidental.
#
# It was tested for leakage and CLEARED: never lagged, but structural and nearly
# static -- corr(wd[t], wd[t-1]) = 0.976, corr(wd[t], wd[t+3]) = 0.946, median
# month-on-month change 0.00114 on a 0-1 scale.
#
# It is absent because it does not improve out-of-sample accuracy. LightGBM, 300
# trees, seeds 42/7/2024 (identical -- deterministic):
#
#     category        without    with     lagged
#     CSD              17.20%   18.24%   18.32%
#     Danskvand        33.39%   34.36%   32.89%
#     Energidrikke     17.40%   16.94%   16.86%
#     RTD              31.83%   32.54%   31.26%
#
# Worse in 3 of 4. The column REMAINS in the feature matrix for EDA; this removes
# it only from model inputs. If reintroduced, use the LAGGED form.
# The modelling feature set, defined once in srq1/_features.py. Eleven copies of
# this literal existed and had already drifted -- srq1_pooled.py was missing
# promo_intensity, silently confounding the pooled-vs-per-category comparison
# (P0049 F31). Holiday and intermittency columns are conditional; resolve()
# intersects against the matrix, so a category lacking one simply omits it.
FEATURES = list(_FEATURES)

def available_features(fm, wanted=None):
	"""Return the wanted features that this matrix actually contains.

	DEC-DISCOVER-COLUMNS: categories differ in capability, not just in values.
	Danskvand and RTD carry no `promo_units` (Nielsen does not report promotion
	for them), so the pipeline omits `promo_intensity` for those categories
	rather than zero-filling -- a constant-zero column would assert "no
	promotion ran", which the data does not support.

	Indexing by a fixed list therefore raises KeyError on exactly the categories
	whose capability differs. Selecting by intersection trains each category on
	what it has, and picks up new columns without a code change.

	The order of `wanted` is preserved so feature-importance output stays
	comparable across runs.
	"""
	wanted = FEATURES if wanted is None else wanted
	return [c for c in wanted if c in fm.columns]



def _wmape(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    return float(np.abs(y - yhat).sum() / max(y.sum(), 1e-9) * 100)


def _all_metrics(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    ae = np.abs(y - yhat); ape = ae / np.maximum(y, 1e-9)
    return float(np.mean(ape) * 100), float(np.median(ape) * 100), float(ae.sum() / max(y.sum(), 1e-9) * 100)


def _load(ds, cat, slug):
    """Return the split parts AND the feature list this matrix supports.

    The feature list must travel with the parts: available_features() needs the
    matrix to intersect against (DEC-DISCOVER-COLUMNS), and previously `tune()`
    referenced a global `fm` that did not exist there -- the script raised
    NameError on its first call and could not run at all."""
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(matrix_path(cat, slug, base=DATASETS[ds]))
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    parts = {s: d[d.split == s] for s in ("train", "val", "test")}
    return parts, available_features(fm)


def _make(model, params):
    if model == "LightGBM":
        from lightgbm import LGBMRegressor
        return LGBMRegressor(random_state=SEED, verbose=-1, **params)
    from xgboost import XGBRegressor
    return XGBRegressor(random_state=SEED, verbosity=0, n_jobs=XGB_N_JOBS, **params)


def _space(trial, model):
    if model == "LightGBM":
        return dict(
            n_estimators=trial.suggest_int("n_estimators", 200, 1200),
            learning_rate=trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
            num_leaves=trial.suggest_int("num_leaves", 15, 128),
            min_child_samples=trial.suggest_int("min_child_samples", 5, 60),
            subsample=trial.suggest_float("subsample", 0.6, 1.0),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
        )
    return dict(
        n_estimators=trial.suggest_int("n_estimators", 200, 1200),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
        max_depth=trial.suggest_int("max_depth", 3, 10),
        min_child_weight=trial.suggest_float("min_child_weight", 1.0, 8.0),
        subsample=trial.suggest_float("subsample", 0.6, 1.0),
        colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
    )


def tune(model, parts, feats, trials):
    tr, va = parts["train"], parts["val"]
    Xtr, ytr = tr[feats].fillna(0.0), tr["log_sales_units"].values
    Xva, yva = va[feats].fillna(0.0), np.expm1(va["log_sales_units"].values)

    def objective(trial):
        m = _make(model, _space(trial, model))
        m.fit(Xtr, ytr)
        return _wmape(yva, np.expm1(m.predict(Xva)))

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=SEED))
    study.optimize(objective, n_trials=trials, show_progress_bar=False)

    # refit best on train+val, eval on test
    trval = pd.concat([tr, va])
    m = _make(model, study.best_params)
    m.fit(trval[feats].fillna(0.0), trval["log_sales_units"].values)
    te = parts["test"]
    pred = np.expm1(m.predict(te[feats].fillna(0.0)))
    mp, md, wm = _all_metrics(np.expm1(te["log_sales_units"].values), pred)
    return dict(val_wmape=study.best_value, test_wmape=wm, test_mape=mp, test_median=md), study.best_params


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--trials", type=int, default=30)
    trials = ap.parse_args().trials
    OUT.mkdir(parents=True, exist_ok=True)
    rows, params = [], {}
    for ds in DATASETS:
        print(f"\n########## {ds} (trials={trials}) ##########")
        for cat, slug in CATS.items():
            parts, feats = _load(ds, cat, slug)
            if len(parts["train"]) < 30 or len(parts["test"]) == 0:
                continue
            for model in ("LightGBM", "XGBoost"):
                res, best = tune(model, parts, feats, trials)
                rows.append(dict(dataset=ds, category=cat, model=model, **res))
                params[f"{ds}/{cat}/{model}"] = best
                print(f"  {cat:13s} {model:9s} test WMAPE={res['test_wmape']:5.1f}% "
                      f"medMAPE={res['test_median']:5.1f}% (val {res['val_wmape']:5.1f}%)")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "tuned_metrics.csv", index=False)
    (OUT / "tuned_params.json").write_text(json.dumps(params, indent=2), encoding="utf-8", newline="\n")

    lines = ["# SRQ1 benchmark — Optuna-tuned (TPE, seed=42)", "",
             f"Trials per model: {trials}. Tuned on validation (WMAPE), refit on "
             "train+val, evaluated once on test.", ""]
    for ds in DATASETS:
        lines += [f"## Dataset: {ds}", "",
                  "| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |",
                  "|---|---|---|---|---|---|"]
        for _, x in df[df.dataset == ds].iterrows():
            lines.append(f"| {x['category']} | {x['model']} | {x['test_wmape']:.1f}% | "
                         f"{x['test_mape']:.1f}% | {x['test_median']:.1f}% | {x['val_wmape']:.1f}% |")
        lines.append("")
    (OUT / "tuned_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\nSaved tuned_metrics.csv + tuned_params.json + tuned_summary.md in {OUT}")


if __name__ == "__main__":
    main()
