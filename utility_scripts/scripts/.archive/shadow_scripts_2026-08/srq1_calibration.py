#!/usr/bin/env python3
"""
SRQ1 prediction-interval calibration — split conformal (SRQ2 confidence signal).

For each category, the tuned XGBoost point model is wrapped in a split-conformal
interval: fit on train, calibrate the interval half-width on the validation
residuals (in log space) at a nominal level, then measure EMPIRICAL coverage on
test (fraction of actuals inside the interval). A well-calibrated interval has
empirical coverage ≈ nominal. Provides the raw confidence signal Ch6/SRQ2 needs.

Self-contained, reproducible (seed=42). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_calibration.py
Output: 04_thesis_results/srq1/{calibration.csv, calibration.md}
"""
import json, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir

warnings.filterwarnings("ignore")
RES = THESIS_RESULTS_SRQ1_DIR
SEED = 42
CATS = {"CSD": "csd", "danskvand": "danskvand", "energidrikke": "energidrikke", "RTD": "rtd"}
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "holiday_month", "promo_intensity", "weighted_distribution"]
NOMINAL = [0.80, 0.90]

params = json.loads((RES / "tuned_params.json").read_text())
rows = []
for cat, slug in CATS.items():
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(get_category_engineered_bymonth_dir(sub) / f"{slug}_feature_matrix.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr, va, te = (d[d.split == s] for s in ("train", "val", "test"))
    if len(tr) < 30 or len(va) == 0 or len(te) == 0:
        continue
    m = XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params.get(f"brand/{cat}/XGBoost", {}))
    m.fit(tr[FEATURES].fillna(0.0), tr["log_sales_units"].values)
    # calibration residuals on validation (log space)
    res = np.abs(va["log_sales_units"].values - m.predict(va[FEATURES].fillna(0.0)))
    pred_te = m.predict(te[FEATURES].fillna(0.0))
    ytrue = np.expm1(te["log_sales_units"].values)
    for nom in NOMINAL:
        q = np.quantile(res, nom)  # symmetric half-width in log space
        lo = np.expm1(pred_te - q); hi = np.expm1(pred_te + q)
        cov = float(np.mean((ytrue >= lo) & (ytrue <= hi)) * 100)
        # median relative interval width (robust; mean explodes on low-volume rows)
        width = float(np.median((hi - lo) / np.maximum(ytrue, 1e-9)))
        rows.append(dict(category=cat, nominal=int(nom * 100), empirical_coverage=round(cov, 1),
                         mean_rel_width=round(width, 2), n_test=len(te)))
        print(f"  {cat:13s} nominal={int(nom*100)}%  empirical={cov:5.1f}%  rel_width={width:.2f}")

df = pd.DataFrame(rows)
df.to_csv(RES / "calibration.csv", index=False)
lines = ["# SRQ1 prediction-interval calibration — split conformal (tuned XGBoost, brand×month)", "",
         "Half-width calibrated on validation residuals (log space); empirical coverage "
         "measured on test. Well-calibrated => empirical ≈ nominal.", "",
         "| Category | Nominal | Empirical coverage | Median rel. width | n_test |",
         "|---|---|---|---|---|"]
for _, x in df.iterrows():
    lines.append(f"| {x['category']} | {x['nominal']}% | {x['empirical_coverage']}% | "
                 f"{x['mean_rel_width']} | {int(x['n_test'])} |")
lines += ["", "Coverage near nominal indicates the conformal interval is a usable confidence "
          "signal for the agentic layer (SRQ2); systematic over/under-coverage flags residual "
          "heteroskedasticity (interval width is global, not per-series)."]
(RES / "calibration.md").write_text("\n".join(lines) + "\n")
print("Saved calibration.csv + calibration.md")
