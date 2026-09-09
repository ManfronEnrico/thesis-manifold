#!/usr/bin/env python3
"""
SRQ1 publication figures — from corrected DVH EXCL. HD results only.

Reads the committed result tables (metrics.csv untuned ladder, tuned_metrics.csv)
and produces:
  fig1_model_ladder.png    — WMAPE per category across the model ladder (brand×month)
  fig3_forecast_overlay.png— actual vs XGBoost forecast, top CSD brand, test window

GRAIN NOTE (P0035, 2026-08-01): fig2_granularity.png is no longer produced. It
compared brand×month against brand×chain, and DEC-GRAIN (2026-07-12) dropped the
chain grain — there is no second grain left to compare against. Fig 1 previously
plotted the bychain ladder and now plots the brand×month ladder.

Self-contained, reproducible (seed=42). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_figures.py
"""
import sys
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
FIG = RES / "figures"
FIG.mkdir(parents=True, exist_ok=True)
SEED = 42

# Determinism control -- see srq1_benchmark.py for the measured rationale.
# Fixed rather than left to the library default so this figure reproduces.
XGB_N_JOBS = 1

CATS = ["CSD", "Danskvand", "Energidrikke", "RTD"]

m = pd.read_csv(RES / "metrics.csv")
# NOTE (P0035): tuned_metrics.csv is no longer read here — its only consumer was
# the removed Fig 2 granularity comparison. Left documented rather than deleted so
# a future grain comparison knows where the tuned table lives.
# t = pd.read_csv(RES / "tuned_metrics.csv")

# ---- Fig 1: model ladder (brand×month), WMAPE ----
# P0035: was m.dataset == "bychain"; repointed to the brand×month grain, which is
# the only grain the thesis now claims.
# FIXED 2026-09-06 (P0046): the tag was "brand", but metrics.csv writes "bymonth".
# The filter matched zero rows, so every bar height was NaN and the chart rendered
# empty -- axes, ticks and legend, no data. It failed silently because a NaN bar
# is a valid matplotlib call, not an error.
_GRAIN_TAG = "bymonth"
mb = m[m.dataset == _GRAIN_TAG]
if mb.empty:
    raise SystemExit(
        f"metrics.csv has no rows with dataset == {_GRAIN_TAG!r} "
        f"(found: {sorted(m.dataset.unique())}). Refusing to write an empty figure."
    )
ladder = ["SeasonalNaive", "Ridge", "LightGBM", "XGBoost"]
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(CATS)); w = 0.2
for i, mdl in enumerate(ladder):
    vals = [mb[(mb.category == c) & (mb.model == mdl)]["wmape"].mean() for c in CATS]
    ax.bar(x + (i - 1.5) * w, vals, w, label=mdl)
ax.set_xticks(x); ax.set_xticklabels(CATS); ax.set_ylabel("Test WMAPE (%)")
# Title derived from the data, never asserted. The hardcoded claim here was
# "every model beats SeasonalNaive", which the numbers contradict: Ridge loses on
# RTD (57.3 vs 54.8 WMAPE). A caption that argues with its own chart is worse
# than no caption -- and this one had been unfalsifiable while the bars were NaN.
_base = mb[mb.model == "SeasonalNaive"].groupby("category")["wmape"].mean()
_losers = sorted({
    f"{mdl} ({c})"
    for mdl in ladder[1:] for c in CATS
    if mb[(mb.category == c) & (mb.model == mdl)]["wmape"].mean() > _base.get(c, float("inf"))
})
_verdict = ("every model beats SeasonalNaive" if not _losers
            else "beats SeasonalNaive except " + ", ".join(_losers))
ax.set_title(f"SRQ1 model ladder (brand×month, untuned) — {_verdict}")
ax.legend(); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(FIG / "fig1_model_ladder.png", dpi=150); plt.close(fig)

# ---- Fig 2: REMOVED (P0035, 2026-08-01) ----
# Was a brand×month vs brand×chain granularity comparison. DEC-GRAIN (2026-07-12)
# dropped the chain grain, so the comparison has no second term. The historical
# chain-grain numbers are preserved at
# plans/P0035_2026-08-01_grain-artifact-removal/preserved_chain_grain_results/.

# ---- Fig 3: forecast overlay (top CSD brand, brand×month, XGBoost) ----
from xgboost import XGBRegressor
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

fm = pd.read_parquet(matrix_path("CSD", "csd"))
d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
top = d.groupby("brand")["sales_units"].sum().idxmax()
db = d[d.brand == top].sort_values("period_index")
tr = d[d.split.isin(["train", "val"])]
# n_jobs was previously unset here, which is NOT a neutral default: XGBoost
# then uses every core, making this figure's forecast line machine-dependent
# for the same reason the accuracy tables were (P0047 F18).
m3 = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6, subsample=0.8,
                  colsample_bytree=0.8, random_state=SEED, verbosity=0,
                  n_jobs=XGB_N_JOBS)
m3.fit(tr[available_features(fm)].fillna(0.0), tr["log_sales_units"].values)
db = db.assign(pred=np.clip(np.expm1(m3.predict(db[available_features(fm)].fillna(0.0))), 0, None))
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(db.period_index, db.sales_units, "o-", label="actual", color="#1f77b4")
ax.plot(db.period_index, db.pred, "s--", label="XGBoost forecast", color="#d62728")
te0 = d[d.split == "test"].period_index.min()
ax.axvline(te0 - 0.5, color="gray", ls=":", label="test start")
ax.set_xlabel("period index"); ax.set_ylabel("sales units")
ax.set_title(f"Forecast overlay — CSD top brand '{top}' (brand×month, XGBoost)")
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(FIG / "fig3_forecast_overlay.png", dpi=150); plt.close(fig)

print("Saved 3 figures to", FIG)
for p in sorted(FIG.glob("*.png")):
    print("  ", p.name)
