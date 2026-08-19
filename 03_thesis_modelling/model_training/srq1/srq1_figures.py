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
RES = THESIS_RESULTS_SRQ1_DIR
FIG = RES / "figures"
FIG.mkdir(parents=True, exist_ok=True)
SEED = 42
CATS = ["CSD", "danskvand", "energidrikke", "RTD"]

m = pd.read_csv(RES / "metrics.csv")
# NOTE (P0035): tuned_metrics.csv is no longer read here — its only consumer was
# the removed Fig 2 granularity comparison. Left documented rather than deleted so
# a future grain comparison knows where the tuned table lives.
# t = pd.read_csv(RES / "tuned_metrics.csv")

# ---- Fig 1: model ladder (brand×month), WMAPE ----
# P0035: was m.dataset == "bychain"; repointed to the brand×month grain, which is
# the only grain the thesis now claims. Tag is "brand" to match metrics.csv.
mb = m[m.dataset == "brand"]
ladder = ["SeasonalNaive", "Ridge", "LightGBM", "XGBoost"]
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(CATS)); w = 0.2
for i, mdl in enumerate(ladder):
    vals = [mb[(mb.category == c) & (mb.model == mdl)]["wmape"].mean() for c in CATS]
    ax.bar(x + (i - 1.5) * w, vals, w, label=mdl)
ax.set_xticks(x); ax.set_xticklabels(CATS); ax.set_ylabel("Test WMAPE (%)")
ax.set_title("SRQ1 model ladder (brand×month, untuned) — every model beats SeasonalNaive")
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
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "peak_month", "promo_intensity"]

def available_features(fm, wanted=None):
	"""Return the wanted features that this matrix actually contains.

	DEC-OPEN-WORLD: categories differ in capability, not just in values.
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

fm = pd.read_parquet(get_category_engineered_bymonth_dir("CSD") / "csd_feature_matrix_h3.parquet")
d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
top = d.groupby("brand")["sales_units"].sum().idxmax()
db = d[d.brand == top].sort_values("period_index")
tr = d[d.split.isin(["train", "val"])]
m3 = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6, subsample=0.8,
                  colsample_bytree=0.8, random_state=SEED, verbosity=0)
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
