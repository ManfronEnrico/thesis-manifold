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

NOMINAL = [0.80, 0.90]

params = json.loads((RES / "tuned_params.json").read_text())
rows = []
for cat, slug in CATS.items():
    sub = "CSD" if cat == "CSD" else cat
    fm = pd.read_parquet(get_category_engineered_bymonth_dir(sub) / f"{slug}_feature_matrix_h3.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr, va, te = (d[d.split == s] for s in ("train", "val", "test"))
    if len(tr) < 30 or len(va) == 0 or len(te) == 0:
        continue
    m = XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1, **params.get(f"brand/{cat}/XGBoost", {}))
    m.fit(tr[available_features(fm)].fillna(0.0), tr["log_sales_units"].values)
    # calibration residuals on validation (log space)
    res = np.abs(va["log_sales_units"].values - m.predict(va[available_features(fm)].fillna(0.0)))
    pred_te = m.predict(te[available_features(fm)].fillna(0.0))
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
(RES / "calibration.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
print("Saved calibration.csv + calibration.md")
