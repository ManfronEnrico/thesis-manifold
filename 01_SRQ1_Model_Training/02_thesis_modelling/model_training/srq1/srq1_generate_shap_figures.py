#!/usr/bin/env python3
"""
SRQ1 explainability — SHAP feature importance for the best model per category.

Uses the tuned XGBoost configuration (04_thesis_results/srq1/tuned_params.json)
on the brand×month matrices (_03), trains on train+val, and computes SHAP values on
the test set. Produces a per-category mean|SHAP| bar plot and a combined figure.

Self-contained, reproducible (seed=42). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_shap.py
Output: 04_thesis_results/srq1/figures/shap_*.png + shap_importance.csv
"""
import json
import sys
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap
from xgboost import XGBRegressor

# Repo root located by searching upward for PATHS.py rather than by a fixed
# parents[N] index: the index silently breaks whenever a script moves a
# directory deeper, which is exactly what happened in the 2026-08-19
# reorganisation (ModuleNotFoundError: No module named 'PATHS').
_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir

warnings.filterwarnings("ignore")
# The active horizon, and the paths that follow from it. ONE source, so the
# matrix read and the results written can never describe different horizons
# (P0049 F24). Set SRQ1_HORIZON=1 to run the secondary horizon.
from _horizon import HORIZON, matrix_path, results_root, banner  # noqa: E402,F401
from _features import FEATURES as _FEATURES, resolve as _resolve_feats, describe as _describe_feats  # noqa: E402,F401
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


RES = _SRQ1Out(results_root())
FIG = RES / "figures"; FIG.mkdir(parents=True, exist_ok=True)
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


params = json.loads((RES / "tuned_params.json").read_text())
rows = []
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, (cat, slug) in zip(axes.ravel(), CATS.items()):
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(matrix_path(cat, slug))
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    trval = d[d.split.isin(["train", "val"])]
    te = d[d.split == "test"]
    p = params.get(f"brand/{cat}/XGBoost", {})
    m = XGBRegressor(random_state=SEED, verbosity=0, n_jobs=XGB_N_JOBS, **p)
    m.fit(trval[available_features(fm)].fillna(0.0), trval["log_sales_units"].values)
    expl = shap.TreeExplainer(m)
    sv = expl.shap_values(te[available_features(fm)].fillna(0.0))
    mean_abs = np.abs(sv).mean(axis=0)
    order = np.argsort(mean_abs)[::-1]
    for f, v in zip(np.array(FEATURES)[order], mean_abs[order]):
        rows.append(dict(category=cat, feature=f, mean_abs_shap=float(v)))
    ax.barh(np.array(FEATURES)[order][::-1], mean_abs[order][::-1], color="#2c7fb8")
    ax.set_title(f"{cat} — mean |SHAP| (XGBoost, test)")
    ax.tick_params(labelsize=8)
fig.suptitle("SRQ1 feature importance (SHAP) — brand×month, tuned XGBoost", fontsize=13)
fig.tight_layout(); fig.savefig(FIG / "shap_importance.png", dpi=150); plt.close(fig)

pd.DataFrame(rows).to_csv(RES / "shap_importance.csv", index=False)
print("Saved shap_importance.png + shap_importance.csv")
# top-3 per category
imp = pd.DataFrame(rows)
for cat in CATS:
    top = imp[imp.category == cat].nlargest(3, "mean_abs_shap")
    print(f"  {cat:13s} top3:", ", ".join(f"{r.feature}({r.mean_abs_shap:.2f})" for _, r in top.iterrows()))
