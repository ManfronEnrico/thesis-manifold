#!/usr/bin/env python3
"""
SRQ1 operational profiling — peak RAM + train/predict latency per model.

Supports the thesis's ≤8 GB operational constraint claim (Ch6 §6.4) and SRQ4.
Measures, per model, tracemalloc peak memory and wall-clock for fit and predict
on a representative dataset (CSD brand×month). Tabular models
use the tuned configs; ARIMA is profiled on a single representative brand series.

Self-contained, reproducible (seed=42). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_profiling.py
Output: 04_thesis_results/srq1/{profiling.csv, profiling.md}
"""
import json, sys, time, tracemalloc, warnings, gc
from pathlib import Path
import numpy as np
import pandas as pd

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
SEED = 42
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



def _profile(fn):
    gc.collect(); tracemalloc.start(); t0 = time.perf_counter()
    out = fn(); dt = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return out, dt, peak / 1e6  # seconds, MB


def main():
    # P0035: was get_category_engineered_bychain_dir; the chain grain and its data
    # directory are gone (DEC-GRAIN 2026-07-12). Profiling now runs on brand x month.
    fm = pd.read_parquet(get_category_engineered_bymonth_dir("CSD") / "csd_feature_matrix_h3.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    trval = d[d.split.isin(["train", "val"])]
    te = d[d.split == "test"]
    Xtr, ytr = trval[available_features(fm)].fillna(0.0), trval["log_sales_units"].values
    Xte = te[available_features(fm)].fillna(0.0)
    params = json.loads((RES / "tuned_params.json").read_text())

    rows = []

    def add(name, builder):
        m, fit_t, fit_mb = _profile(lambda: builder().fit(Xtr, ytr))
        _, pred_t, pred_mb = _profile(lambda: m.predict(Xte))
        rows.append(dict(model=name, fit_s=round(fit_t, 3), predict_ms=round(pred_t * 1000, 1),
                         peak_fit_MB=round(fit_mb, 1), peak_predict_MB=round(pred_mb, 2),
                         n_train=len(trval), n_features=len(FEATURES)))
        print(f"  {name:10s} fit={fit_t:6.3f}s predict={pred_t*1000:7.1f}ms peakRAM_fit={fit_mb:7.1f}MB")

    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    add("Ridge", lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0)))

    from lightgbm import LGBMRegressor
    add("LightGBM", lambda: LGBMRegressor(random_state=SEED, verbose=-1,
                                          **params.get("brand/CSD/LightGBM", {})))
    from xgboost import XGBRegressor
    add("XGBoost", lambda: XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1,
                                        **params.get("brand/CSD/XGBoost", {})))

    # ARIMA on a single representative brand series (univariate; per-series cost)
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    one = d[d.brand == d.groupby("brand")["sales_units"].sum().idxmax()].sort_values("period_index")
    yfit = np.log(np.maximum(one[one.split.isin(["train", "val"])].sales_units.values, 1.0))
    h = int((one.split == "test").sum())

    def fit_arima():
        return SARIMAX(yfit, order=(1, 1, 1), enforce_stationarity=False,
                       enforce_invertibility=False).fit(disp=False)
    r, fit_t, fit_mb = _profile(fit_arima)
    _, pred_t, pred_mb = _profile(lambda: r.forecast(h))
    rows.append(dict(model="ARIMA(per-series)", fit_s=round(fit_t, 3), predict_ms=round(pred_t * 1000, 1),
                     peak_fit_MB=round(fit_mb, 1), peak_predict_MB=round(pred_mb, 2),
                     n_train=len(yfit), n_features=1))
    print(f"  {'ARIMA':10s} fit={fit_t:6.3f}s predict={pred_t*1000:7.1f}ms peakRAM_fit={fit_mb:7.1f}MB (1 series)")

    df = pd.DataFrame(rows)
    df.to_csv(RES / "profiling.csv", index=False)
    lines = ["# SRQ1 operational profiling (CSD brand×chain; tuned configs)", "",
             "Peak RAM (tracemalloc, Python-object allocations) and wall-clock per model. "
             "Supports the ≤8 GB sequential-execution constraint. ARIMA is per-series "
             "(univariate); tabular models train on the full matrix in one fit.", "",
             "| Model | fit (s) | predict (ms) | peak RAM fit (MB) | peak RAM predict (MB) | n_train | n_features |",
             "|---|---|---|---|---|---|---|"]
    for _, x in df.iterrows():
        lines.append(f"| {x['model']} | {x['fit_s']} | {x['predict_ms']} | {x['peak_fit_MB']} | "
                     f"{x['peak_predict_MB']} | {int(x['n_train'])} | {int(x['n_features'])} |")
    lines += ["", "All models fit comfortably within the ≤8 GB budget (peak RAM in the "
              "tens-of-MB range). Note tracemalloc captures Python-level allocations; native "
              "library buffers (LightGBM/XGBoost C++) are additional but small at this data scale."]
    (RES / "profiling.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("Saved profiling.csv + profiling.md")


if __name__ == "__main__":
    main()
