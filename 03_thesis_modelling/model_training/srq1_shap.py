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
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "holiday_month", "promo_intensity", "weighted_distribution"]

params = json.loads((RES / "tuned_params.json").read_text())
rows = []
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, (cat, slug) in zip(axes.ravel(), CATS.items()):
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(get_category_engineered_bymonth_dir(sub) / f"{slug}_feature_matrix.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    trval = d[d.split.isin(["train", "val"])]
    te = d[d.split == "test"]
    p = params.get(f"brand/{cat}/XGBoost", {})
    m = XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **p)
    m.fit(trval[FEATURES].fillna(0.0), trval["log_sales_units"].values)
    expl = shap.TreeExplainer(m)
    sv = expl.shap_values(te[FEATURES].fillna(0.0))
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
