#!/usr/bin/env python3
"""
SRQ1 statistical baselines — ARIMA + Prophet (univariate, per brand series).

Completes the model ladder for the SRQ4 "ML vs traditional forecasting" comparison.
Per category (brand×month _03), for each retained brand: fit on train+val months,
forecast the test horizon, score WMAPE (volume-weighted) and median per-series MAPE.
Comparable to the tabular-model results in 04_thesis_results/srq1/tuned_summary.md.

ARIMA  = statsmodels SARIMAX(log y, order=(1,1,1)) — no pmdarima available.
Prophet= additive, yearly seasonality, on raw monthly y.

Self-contained, seed-free (deterministic fits). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_baselines_stat.py
Output: 04_thesis_results/srq1/{stat_baselines.csv, stat_baselines.md}
"""
import sys
import warnings, logging
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir

warnings.filterwarnings("ignore")
logging.getLogger("prophet").setLevel(logging.CRITICAL)
logging.getLogger("cmdstanpy").setLevel(logging.CRITICAL)

RES = THESIS_RESULTS_SRQ1_DIR
RES.mkdir(parents=True, exist_ok=True)
CATS = {"CSD": "csd", "danskvand": "danskvand", "energidrikke": "energidrikke", "RTD": "rtd"}


def _wmape_parts(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    return np.abs(y - yhat).sum(), y.sum(), float(np.median(np.abs(y - yhat) / np.maximum(y, 1e-9)) * 100)


def _date(yr, mo):
    return pd.Timestamp(int(yr), int(mo), 1)


def run_arima(series):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    fit = series["fit"]; h = series["h"]
    y = np.log(np.maximum(fit, 1.0))
    m = SARIMAX(y, order=(1, 1, 1), enforce_stationarity=False, enforce_invertibility=False)
    r = m.fit(disp=False)
    return np.expm1(r.forecast(h))


def run_prophet(series):
    from prophet import Prophet
    df = pd.DataFrame({"ds": series["fit_ds"], "y": np.log(np.maximum(series["fit"], 1.0))})
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(df)
    fut = pd.DataFrame({"ds": series["test_ds"]})
    return np.expm1(m.predict(fut)["yhat"].values)


def main():
    rows = []
    for cat, slug in CATS.items():
        sub = "CSD" if cat == "CSD" else cat
        fm = pd.read_parquet(get_category_engineered_bymonth_dir(sub) / f"{slug}_feature_matrix.parquet")
        d = fm.dropna(subset=["sales_units"]).copy()
        d["ds"] = [_date(y, m) for y, m in zip(d.period_year, d.period_month)]
        acc = {"ARIMA": [0.0, 0.0, []], "Prophet": [0.0, 0.0, []]}
        nfit = {"ARIMA": 0, "Prophet": 0}
        for brand, g in d.groupby("brand"):
            g = g.sort_values("period_index")
            fit = g[g.split.isin(["train", "val"])]
            test = g[g.split == "test"]
            if len(fit) < 12 or len(test) == 0:
                continue
            series = {"fit": fit.sales_units.values, "h": len(test),
                      "fit_ds": fit.ds.values, "test_ds": test.ds.values}
            ytrue = test.sales_units.values
            for name, fn in [("ARIMA", run_arima), ("Prophet", run_prophet)]:
                try:
                    pred = fn(series)
                    if len(pred) != len(ytrue):
                        continue
                    ae, sy, _ = _wmape_parts(ytrue, pred)
                    acc[name][0] += ae; acc[name][1] += sy
                    acc[name][2].extend(list(np.abs(ytrue - np.clip(pred, 0, None)) / np.maximum(ytrue, 1e-9)))
                    nfit[name] += 1
                except Exception:
                    continue
        for name in ("ARIMA", "Prophet"):
            ae, sy, apes = acc[name]
            wm = (ae / sy * 100) if sy > 0 else float("nan")
            md = float(np.median(apes) * 100) if apes else float("nan")
            rows.append(dict(category=cat, model=name, wmape=wm, median_mape=md, n_series=nfit[name]))
            print(f"  {cat:13s} {name:8s} WMAPE={wm:5.1f}% medMAPE={md:5.1f}% (n_series={nfit[name]})")

    df = pd.DataFrame(rows)
    df.to_csv(RES / "stat_baselines.csv", index=False)
    lines = ["# SRQ1 statistical baselines — ARIMA + Prophet (brand×month, per-brand)", "",
             "WMAPE = volume-weighted across brands; medMAPE = median per-series. "
             "For SRQ4 comparison vs the tabular models (tuned_summary.md).", "",
             "| Category | Model | WMAPE | median MAPE | n_series |",
             "|---|---|---|---|---|"]
    for _, x in df.iterrows():
        lines.append(f"| {x['category']} | {x['model']} | {x['wmape']:.1f}% | {x['median_mape']:.1f}% | {int(x['n_series'])} |")
    (RES / "stat_baselines.md").write_text("\n".join(lines) + "\n")
    print("Saved stat_baselines.csv + stat_baselines.md")


if __name__ == "__main__":
    main()
