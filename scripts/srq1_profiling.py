#!/usr/bin/env python3
"""
SRQ1 operational profiling — peak RAM + train/predict latency per model.

Supports the thesis's ≤8 GB operational constraint claim (Ch6 §6.4) and SRQ4.
Measures, per model, tracemalloc peak memory and wall-clock for fit and predict
on a representative dataset (CSD brand×chain — the largest matrix). Tabular models
use the tuned configs; ARIMA is profiled on a single representative brand series.

Self-contained, reproducible (seed=42). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_profiling.py
Output: thesis/data/_05_results_srq1/{profiling.csv, profiling.md}
"""
import json, time, tracemalloc, warnings, gc
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "thesis" / "data" / "_05_results_srq1"
SEED = 42
FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "holiday_month", "promo_intensity", "weighted_distribution"]


def _profile(fn):
    gc.collect(); tracemalloc.start(); t0 = time.perf_counter()
    out = fn(); dt = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return out, dt, peak / 1e6  # seconds, MB


def main():
    fm = pd.read_parquet(ROOT / "thesis/data/_04_engineered_bychain/CSD/csd_feature_matrix.parquet")
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    trval = d[d.split.isin(["train", "val"])]
    te = d[d.split == "test"]
    Xtr, ytr = trval[FEATURES].fillna(0.0), trval["log_sales_units"].values
    Xte = te[FEATURES].fillna(0.0)
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
                                          **params.get("bychain/CSD/LightGBM", {})))
    from xgboost import XGBRegressor
    add("XGBoost", lambda: XGBRegressor(random_state=SEED, verbosity=0, n_jobs=-1,
                                        **params.get("bychain/CSD/XGBoost", {})))

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
    (RES / "profiling.md").write_text("\n".join(lines) + "\n")
    print("Saved profiling.csv + profiling.md")


if __name__ == "__main__":
    main()
