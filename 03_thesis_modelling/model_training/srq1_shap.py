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

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir

warnings.filterwarnings("ignore")
RES = THESIS_RESULTS_SRQ1_DIR
FIG = RES / "figures"; FIG.mkdir(parents=True, exist_ok=True)
SEED = 42
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


params = json.loads((RES / "tuned_params.json").read_text())
rows = []
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, (cat, slug) in zip(axes.ravel(), CATS.items()):
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(get_category_engineered_bymonth_dir(sub) / f"{slug}_feature_matrix_h3.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    trval = d[d.split.isin(["train", "val"])]
    te = d[d.split == "test"]
    p = params.get(f"brand/{cat}/XGBoost", {})
    m = XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **p)
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
