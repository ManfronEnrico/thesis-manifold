#!/usr/bin/env python3
"""
SRQ1 forecasting benchmark — corrected DVH EXCL. HD matrices.

Trains, per category, on the regenerated feature matrices and reports test-set
accuracy for a baseline ladder:
    SeasonalNaive (lag_13 -> fallback lag_1) | Ridge | LightGBM | XGBoost
Metrics: median per-series MAPE, mean MAPE, and WMAPE (volume-weighted — the
business metric). Forward-chaining split is already encoded in the `split` column.

Runs on BOTH granularities:
    _04 brand×chain (primary)  and  _03 brand×month (robustness comparison).
Self-contained: reads only local parquet matrices. No Prometheus/Nika dependency.

Usage:  .venv/bin/python scripts/srq1_benchmark.py
Output: 04_thesis_results/srq1/{metrics.csv, summary.md}
"""

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_SRQ1_DIR, THESIS_DATA_ENGINEERED_BYCHAIN_DIR, THESIS_DATA_ENGINEERED_BYMONTH_DIR

warnings.filterwarnings("ignore")

OUT = THESIS_RESULTS_SRQ1_DIR
SEED = 42

CATS = {"CSD": "csd", "danskvand": "danskvand",
        "energidrikke": "energidrikke", "RTD": "rtd"}

DATASETS = {
    "bychain": THESIS_DATA_ENGINEERED_BYCHAIN_DIR,
    "brand":   THESIS_DATA_ENGINEERED_BYMONTH_DIR,
}

FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
            "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
            "month", "quarter", "holiday_month",
            "promo_intensity", "weighted_distribution"]

# series key per dataset
KEYS = {"bychain": ["brand", "chain"], "brand": ["brand"]}


def _load(ds: str, cat: str, slug: str) -> pd.DataFrame:
    sub = "CSD" if (cat == "CSD") else cat
    p = DATASETS[ds] / sub / f"{slug}_feature_matrix.parquet"
    return pd.read_parquet(p)


def _metrics(y, yhat):
    """Return (mean MAPE %, median per-row APE %, WMAPE %)."""
    y = np.asarray(y, float); yhat = np.asarray(yhat, float)
    ae = np.abs(y - yhat)
    ape = ae / np.maximum(y, 1e-9)
    return float(np.mean(ape) * 100), float(np.median(ape) * 100), float(ae.sum() / max(y.sum(), 1e-9) * 100)


def _fit_predict(model_name, Xtr, ytr_log, Xte):
    """Train in log space, return predictions on the original scale."""
    if model_name == "Ridge":
        from sklearn.linear_model import Ridge
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        m = make_pipeline(StandardScaler(), Ridge(alpha=1.0, random_state=SEED))
        m.fit(Xtr, ytr_log)
        return np.expm1(m.predict(Xte))
    if model_name == "LightGBM":
        from lightgbm import LGBMRegressor
        m = LGBMRegressor(n_estimators=400, learning_rate=0.05, num_leaves=31,
                          subsample=0.8, colsample_bytree=0.8, random_state=SEED, verbose=-1)
        m.fit(Xtr, ytr_log)
        return np.expm1(m.predict(Xte))
    if model_name == "XGBoost":
        from xgboost import XGBRegressor
        m = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6,
                         subsample=0.8, colsample_bytree=0.8, random_state=SEED,
                         verbosity=0, n_jobs=-1)
        m.fit(Xtr, ytr_log)
        return np.expm1(m.predict(Xte))
    raise ValueError(model_name)


def run_category(ds: str, cat: str, slug: str) -> list[dict]:
    fm = _load(ds, cat, slug)
    d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"]).copy()
    tr = d[d.split == "train"]
    te = d[d.split == "test"]
    rows = []
    if len(tr) < 30 or len(te) == 0:
        return rows

    Xtr = tr[FEATURES].fillna(0.0); ytr_log = tr["log_sales_units"].values
    Xte = te[FEATURES].fillna(0.0); ytrue = np.expm1(te["log_sales_units"].values)

    # Baseline: seasonal naive (same month last year), fallback last month
    sn = te["lag_13"].fillna(te["lag_1"]).fillna(0.0).values
    for name, pred in [("SeasonalNaive", sn)]:
        mp, md, wm = _metrics(ytrue, pred)
        rows.append(dict(dataset=ds, category=cat, model=name,
                         mape_mean=mp, mape_median=md, wmape=wm,
                         n_train=len(tr), n_test=len(te), n_series=d[KEYS[ds]].drop_duplicates().shape[0]))

    for name in ["Ridge", "LightGBM", "XGBoost"]:
        try:
            pred = _fit_predict(name, Xtr, ytr_log, Xte)
            pred = np.clip(pred, 0, None)
            mp, md, wm = _metrics(ytrue, pred)
            rows.append(dict(dataset=ds, category=cat, model=name,
                             mape_mean=mp, mape_median=md, wmape=wm,
                             n_train=len(tr), n_test=len(te), n_series=d[KEYS[ds]].drop_duplicates().shape[0]))
        except Exception as e:  # noqa
            rows.append(dict(dataset=ds, category=cat, model=name, error=str(e)[:120],
                             mape_mean=np.nan, mape_median=np.nan, wmape=np.nan,
                             n_train=len(tr), n_test=len(te), n_series=np.nan))
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows = []
    for ds in DATASETS:
        print(f"\n########## DATASET = {ds} ##########")
        for cat, slug in CATS.items():
            r = run_category(ds, cat, slug)
            all_rows += r
            best = min([x for x in r if x["model"] != "SeasonalNaive" and not np.isnan(x.get("wmape", np.nan))],
                       key=lambda x: x["wmape"], default=None)
            naive = next((x for x in r if x["model"] == "SeasonalNaive"), None)
            if best and naive:
                print(f"  {cat:13s} best={best['model']:9s} WMAPE={best['wmape']:5.1f}% "
                      f"(naive {naive['wmape']:5.1f}%)  medMAPE={best['mape_median']:5.1f}%")

    df = pd.DataFrame(all_rows)
    df.to_csv(OUT / "metrics.csv", index=False)

    # summary.md
    lines = ["# SRQ1 benchmark — corrected DVH EXCL. HD matrices", "",
             "Test-set accuracy. WMAPE = volume-weighted (business metric); "
             "medMAPE = median per-row APE. Models trained in log space, seed=42.", ""]
    for ds in DATASETS:
        lines += [f"## Dataset: {ds}", "",
                  "| Category | Model | WMAPE | mean MAPE | median MAPE | n_train | n_test | n_series |",
                  "|---|---|---|---|---|---|---|---|"]
        sub = df[df.dataset == ds]
        for cat in CATS:
            for _, x in sub[sub.category == cat].iterrows():
                wm = f"{x['wmape']:.1f}%" if pd.notna(x.get("wmape")) else "ERR"
                mp = f"{x['mape_mean']:.1f}%" if pd.notna(x.get("mape_mean")) else "-"
                md = f"{x['mape_median']:.1f}%" if pd.notna(x.get("mape_median")) else "-"
                lines.append(f"| {cat} | {x['model']} | {wm} | {mp} | {md} | "
                             f"{int(x['n_train'])} | {int(x['n_test'])} | "
                             f"{int(x['n_series']) if pd.notna(x.get('n_series')) else '-'} |")
        lines.append("")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"\nSaved metrics.csv + summary.md in {OUT}")


if __name__ == "__main__":
    main()
