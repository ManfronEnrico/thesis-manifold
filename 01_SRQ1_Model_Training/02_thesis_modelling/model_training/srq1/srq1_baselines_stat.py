#!/usr/bin/env python3
"""
SRQ1 statistical baselines — naive, seasonal-naive, drift, Ridge, ARIMA, Prophet.

Completes the model ladder for the SRQ4 "ML vs traditional forecasting" comparison.
Per category (brand×month _03), for each retained brand: fit on train+val months,
forecast the test horizon, score WMAPE (volume-weighted) and median per-series MAPE.
Comparable to the tabular-model results in 04_thesis_results/srq1/tuned_summary.md.

WHY THESE SIX, ACADEMICALLY
---------------------------
The three simple benchmarks are the conventional floor in the forecasting
literature, not optional extras. Hyndman & Athanasopoulos (*Forecasting: Principles
and Practice*, 3rd ed., ch. 5.2) define naive, seasonal-naive and drift as THE
standard benchmark set, and the M-competitions (Makridakis et al. 2018, 2020) score
every entrant against them. A forecasting result reported without them is
conventionally treated as unbenchmarked: an examiner's first question is "is this
better than assuming next month equals last month?"

  naive           y_hat(t+h) = y(t)          -- last value carried forward
  seasonal_naive  y_hat(t+h) = y(t+h-12)     -- same month last year
  drift           naive + average historical trend
  Ridge           L2-regularised linear model on the same 13 features as the
                  tabular models -- isolates "does the NONLINEARITY buy anything,
                  or just the feature engineering?"
  ARIMA           statsmodels SARIMAX(log1p y, order=(1,1,1)) -- no pmdarima
  Prophet         additive, yearly seasonality, on log1p monthly y

Seasonal-naive matters most here: this panel is monthly beverage demand with strong
annual seasonality, which is exactly the structure it exploits. It is the honest
benchmark for the claim "the model learned seasonality" -- and it is free.

Ridge sits between the classical and tabular arms deliberately. LightGBM/XGBoost
beating ARIMA conflates two advantages: richer features AND nonlinearity. Ridge has
the features but not the nonlinearity, so the Ridge->GBM gap isolates the second.

Self-contained, seed-free (deterministic fits). No Prometheus/Nika dependency.
Usage: .venv/bin/python scripts/srq1_baselines_stat.py
Output: 04_thesis_results/srq1/{stat_baselines.csv, stat_baselines.md}
"""
import sys
import warnings, logging
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
logging.getLogger("prophet").setLevel(logging.CRITICAL)
logging.getLogger("cmdstanpy").setLevel(logging.CRITICAL)

RES = THESIS_RESULTS_SRQ1_DIR
RES.mkdir(parents=True, exist_ok=True)
CATS = {"CSD": "csd", "danskvand": "danskvand", "energidrikke": "energidrikke", "RTD": "rtd"}

# Features for the Ridge arm -- the same 13 the tabular models use, so the
# Ridge->GBM comparison isolates nonlinearity rather than feature access.
# Missing columns are dropped per-category (danskvand/RTD lack promo_intensity),
# matching srq1_benchmark_tuned.py::available_features.
RIDGE_FEATURES = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
                  "rolling_mean_4", "rolling_std_4", "rolling_mean_13",
                  "month", "quarter", "peak_month", "promo_intensity"]

# Volume-valued subset of the above. These are log1p-transformed for Ridge because
# the target is logged; calendar terms and promo_intensity are not volumes and are
# left alone. See run_ridge and P0040 F54.
LAGLIKE_COLS = {"lag_1", "lag_2", "lag_3", "lag_4", "lag_8", "lag_13",
                "rolling_mean_4", "rolling_std_4", "rolling_mean_13"}


def _wmape_parts(y, yhat):
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    return np.abs(y - yhat).sum(), y.sum(), float(np.median(np.abs(y - yhat) / np.maximum(y, 1e-9)) * 100)


def _date(yr, mo):
    return pd.Timestamp(int(yr), int(mo), 1)


def run_naive(series):
    """y_hat(t+h) = last observed value. The canonical minimum benchmark.

    Hyndman & Athanasopoulos ch 5.2. For any series without trend or seasonality
    this is provably optimal, which is precisely why beating it is the first thing
    a forecast must demonstrate."""
    return np.repeat(float(series["fit"][-1]), series["h"])


def run_seasonal_naive(series):
    """y_hat(t+h) = value from the same month one year earlier.

    The right floor for monthly beverage demand: it captures annual seasonality
    exactly, with zero parameters. If a learned model cannot beat it, the model has
    not learned seasonality -- it has learned noise. Falls back to naive when fewer
    than 12 months of history exist."""
    fit, h = series["fit"], series["h"]
    if len(fit) < 12:
        return run_naive(series)
    # Step forward h months, reading each value from 12 months prior. Once the
    # forecast horizon exceeds 12 the prediction re-reads its own earlier output,
    # which is the standard recursive definition.
    hist = list(fit)
    out = []
    for _ in range(h):
        out.append(float(hist[-12]))
        hist.append(out[-1])
    return np.array(out)


def run_drift(series):
    """Naive plus the average per-period change over the fitted history.

    Equivalent to extrapolating the straight line between the first and last
    observation (Hyndman & Athanasopoulos ch 5.2). Distinguishes "flat" from
    "trending" -- without it, a naive benchmark flatters any series with drift."""
    fit, h = series["fit"], series["h"]
    if len(fit) < 2:
        return run_naive(series)
    slope = (float(fit[-1]) - float(fit[0])) / (len(fit) - 1)
    return np.clip(float(fit[-1]) + slope * np.arange(1, h + 1), 0, None)


def run_ridge(series):
    """L2-regularised linear regression on the SAME features as the tabular models.

    Isolates nonlinearity from feature engineering. LightGBM beating ARIMA proves
    little on its own -- ARIMA is univariate, so the gap conflates "has lag/rolling/
    calendar features" with "can model interactions". Ridge has the features and no
    interactions, so Ridge->GBM is the nonlinearity premium and ARIMA->Ridge is the
    feature premium.

    Standardised because L2 penalises coefficients on their raw scale; without
    scaling the penalty would fall almost entirely on the small-magnitude features.
    alpha chosen on the validation split rather than fixed."""
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler

    tr, va, te = series["Xtr"], series["Xva"], series["Xte"]
    if tr is None or len(tr) < 10:
        return None

    # Log the volume-valued features to match the logged target (P0040 F54).
    # Without this the model fits log(y) ~ b*(raw lags) -- additive form for a
    # multiplicative relationship -- and log-space RMSE sits at ~3.9 regardless of
    # alpha. Trees are immune (they split on rank order), which is why the same
    # matrix works for LightGBM/XGBoost and why this went unnoticed.
    # `series["logmask"]` marks which feature columns are volumes.
    mask = series.get("logmask")
    if mask is not None and any(mask):
        import numpy as _np
        idx = [i for i, m in enumerate(mask) if m]
        tr, va, te = tr.copy(), (va.copy() if va is not None else None), te.copy()
        tr[:, idx] = _np.log1p(_np.clip(tr[:, idx], 0, None))
        if va is not None and len(va):
            va[:, idx] = _np.log1p(_np.clip(va[:, idx], 0, None))
        te[:, idx] = _np.log1p(_np.clip(te[:, idx], 0, None))

    sc = StandardScaler().fit(tr)
    best, best_a = None, None
    for a in (0.01, 0.1, 1.0, 10.0, 100.0):
        m = Ridge(alpha=a).fit(sc.transform(tr), series["ytr"])
        if va is not None and len(va):
            err = np.abs(np.expm1(m.predict(sc.transform(va))) -
                         np.expm1(series["yva"])).sum()
        else:
            err = 0.0
        if best is None or err < best:
            best, best_a = err, a
    # Refit on train+val at the chosen alpha, matching the tabular protocol.
    Xall = np.vstack([tr, va]) if va is not None and len(va) else tr
    yall = np.concatenate([series["ytr"], series["yva"]]) if va is not None and len(va) else series["ytr"]
    sc = StandardScaler().fit(Xall)
    m = Ridge(alpha=best_a).fit(sc.transform(Xall), yall)
    pred_log = m.predict(sc.transform(te))

    # CLAMP IN LOG SPACE BEFORE INVERTING. Without this a single extrapolated
    # prediction becomes astronomical after expm1 and destroys the volume-weighted
    # WMAPE for the whole category -- the first run of this arm reported
    # WMAPE = 345,856,990% for energidrikke and inf% for CSD/RTD, which are
    # artifacts of unbounded exponentiation, not accuracy measurements.
    #
    # A per-brand Ridge fits ~24 rows against 13 standardised features, which is
    # close to singular; the L2 penalty shrinks coefficients but does not bound the
    # PREDICTION when a test row sits outside the training envelope.
    #
    # The bound is the observed history of THIS series, widened by a factor of 3.
    # Justified as a forecasting constraint rather than a fudge: a monthly demand
    # forecast three times the largest month ever observed for that brand is not a
    # forecast, it is an extrapolation failure, and a practitioner would reject it.
    # Applied identically to every brand, and the clip rate is reported so the
    # write-up can state how often it bound.
    hi_log = float(np.log1p(np.maximum(np.expm1(yall).max(), 0.0) * 3.0 + 1.0))
    lo_log = 0.0  # log1p(0) -- demand cannot be negative
    n_clipped = int(((pred_log > hi_log) | (pred_log < lo_log)).sum())
    if n_clipped:
        series.setdefault("_ridge_clipped", 0)
        series["_ridge_clipped"] += n_clipped

    # BOTH variants are returned (DEC-RIDGE-BOTH, Brian 2026-08-22).
    #
    # Reporting only the clipped figure would misrepresent the model: "Ridge + a
    # 3x extrapolation bound" is a different estimator from "Ridge", and the bound
    # is an arbitrary constant of ours (P0040 F60). Reporting only the pooled Ridge
    # and omitting this arm entirely would hide a real result -- that a per-brand
    # linear fit on ~24 rows against 13 features is unusable.
    #
    # So both are computed and both are published. The unclipped figure is not a
    # defect to be suppressed; it is the evidence for the claim.
    unclipped = np.clip(np.expm1(pred_log), 0, None)
    series["_ridge_unclipped"] = unclipped
    return np.clip(np.expm1(np.clip(pred_log, lo_log, hi_log)), 0, None)


def run_arima(series):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    fit = series["fit"]; h = series["h"]
    # log1p/expm1 are a matched pair; log/expm1 is not (expm1 inverts log1p).
    # log1p also handles the genuine zeros in this panel without the max(y, 1.0)
    # floor, which would rewrite a real zero as a one.
    y = np.log1p(np.maximum(fit, 0.0))
    m = SARIMAX(y, order=(1, 1, 1), enforce_stationarity=False, enforce_invertibility=False)
    r = m.fit(disp=False)
    return np.expm1(r.forecast(h))


def run_prophet(series):
    from prophet import Prophet
    # See run_arima: log1p pairs with the expm1 used to invert below.
    df = pd.DataFrame({"ds": series["fit_ds"],
                       "y": np.log1p(np.maximum(series["fit"], 0.0))})
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(df)
    fut = pd.DataFrame({"ds": series["test_ds"]})
    return np.expm1(m.predict(fut)["yhat"].values)


# Ordered simplest -> most complex, which is also the order they should be read
# in the results table: each row should justify its additional complexity against
# the row above it.
MODELS = {
    "Naive": run_naive,
    "SeasonalNaive": run_seasonal_naive,
    "Drift": run_drift,
    "Ridge": run_ridge,
    "ARIMA": run_arima,
    "Prophet": run_prophet,
}


def main():
    rows = []
    for cat, slug in CATS.items():
        sub = "CSD" if cat == "CSD" else cat
        fm = pd.read_parquet(get_category_engineered_bymonth_dir(sub) / f"{slug}_feature_matrix_h3.parquet")
        d = fm.dropna(subset=["sales_units"]).copy()
        d["ds"] = [_date(y, m) for y, m in zip(d.period_year, d.period_month)]
        acc = {n: [0.0, 0.0, []] for n in MODELS}
        nfit = {n: 0 for n in MODELS}
        clipped = 0  # how many Ridge predictions hit the extrapolation bound
        acc_unclipped = [0.0, 0.0, []]  # Ridge scored WITHOUT the bound
        for brand, g in d.groupby("brand"):
            g = g.sort_values("period_index")
            fit = g[g.split.isin(["train", "val"])]
            test = g[g.split == "test"]
            if len(fit) < 12 or len(test) == 0:
                continue
            series = {"fit": fit.sales_units.values, "h": len(test),
                      "fit_ds": fit.ds.values, "test_ds": test.ds.values}
            # Feature blocks for Ridge. Present only if the matrix carries the
            # tabular features; None otherwise, and run_ridge skips.
            feats = [c for c in RIDGE_FEATURES if c in g.columns]
            # Which of the selected features are volume-valued (see run_ridge).
            logmask = [c in LAGLIKE_COLS for c in feats]
            if feats and "log_sales_units" in g.columns:
                trn = fit.dropna(subset=feats + ["log_sales_units"])
                tst = test.dropna(subset=feats + ["log_sales_units"])
                if len(trn) >= 10 and len(tst) == len(test):
                    n_va = max(1, int(len(trn) * 0.2))
                    series.update(
                        logmask=logmask,
                        Xtr=trn[feats].values[:-n_va].astype(float),
                        ytr=trn["log_sales_units"].values[:-n_va],
                        Xva=trn[feats].values[-n_va:].astype(float),
                        yva=trn["log_sales_units"].values[-n_va:],
                        Xte=tst[feats].values.astype(float))
                else:
                    series.update(Xtr=None, ytr=None, Xva=None, yva=None, Xte=None)
            else:
                series.update(Xtr=None, ytr=None, Xva=None, yva=None, Xte=None)
            ytrue = test.sales_units.values
            for name, fn in MODELS.items():
                try:
                    pred = fn(series)
                    if name == "Ridge":
                        clipped += series.pop("_ridge_clipped", 0)
                        unc = series.pop("_ridge_unclipped", None)
                        if unc is not None and len(unc) == len(ytrue):
                            ae_u, sy_u, _ = _wmape_parts(ytrue, unc)
                            acc_unclipped[0] += ae_u
                            acc_unclipped[1] += sy_u
                            acc_unclipped[2].extend(list(
                                np.abs(ytrue - np.clip(unc, 0, None)) /
                                np.maximum(ytrue, 1e-9)))
                    if pred is None or len(pred) != len(ytrue):
                        continue
                    ae, sy, _ = _wmape_parts(ytrue, pred)
                    acc[name][0] += ae; acc[name][1] += sy
                    acc[name][2].extend(list(np.abs(ytrue - np.clip(pred, 0, None)) / np.maximum(ytrue, 1e-9)))
                    nfit[name] += 1
                except Exception:
                    continue
        for name in MODELS:
            ae, sy, apes = acc[name]
            wm = (ae / sy * 100) if sy > 0 else float("nan")
            md = float(np.median(apes) * 100) if apes else float("nan")
            rows.append(dict(category=cat, model=name, wmape=wm, median_mape=md,
                             n_series=nfit[name],
                             ridge_clipped=(clipped if name == "Ridge" else 0)))
            if name == "Ridge" and acc_unclipped[1] > 0:
                ae_u, sy_u, apes_u = acc_unclipped
                wm_u = ae_u / sy_u * 100
                md_u = float(np.median(apes_u) * 100) if apes_u else float("nan")
                rows.append(dict(category=cat, model="Ridge(unclipped)",
                                 wmape=wm_u, median_mape=md_u,
                                 n_series=nfit[name], ridge_clipped=0))
                print(f"  {cat:13s} {'Ridge(unclipped)':14s} WMAPE={wm_u:9.1f}% "
                      f"medMAPE={md_u:5.1f}% (n_series={nfit[name]})")
            extra = f" [clipped {clipped}]" if name == "Ridge" and clipped else ""
            print(f"  {cat:13s} {name:14s} WMAPE={wm:7.1f}% medMAPE={md:5.1f}% "
                  f"(n_series={nfit[name]}){extra}")

    df = pd.DataFrame(rows)
    df.to_csv(RES / "stat_baselines.csv", index=False)
    lines = ["# SRQ1 statistical baselines (brand×month, per-brand)", "",
             "Six benchmarks, ordered simplest to most complex. The first three "
             "(naive, seasonal-naive, drift) are the standard forecasting floor "
             "per Hyndman & Athanasopoulos ch 5.2 and the M-competitions; a "
             "learned model that does not beat them is unbenchmarked. Ridge uses "
             "the SAME features as the tabular models, so Ridge→GBM isolates the "
             "nonlinearity premium while ARIMA→Ridge isolates the feature "
             "premium.", "",
             "**Ridge appears twice, deliberately.** `Ridge` applies an "
             "extrapolation bound (that series' observed maximum x 3); "
             "`Ridge(unclipped)` does not. The bound is an arbitrary constant, so "
             "reporting only the bounded figure would describe a different "
             "estimator than 'Ridge'. The unclipped figure is the evidence that a "
             "per-brand linear fit on ~24 rows against 13 features is unusable -- "
             "it is published rather than suppressed. Prefer the POOLED Ridge in "
             "`ridge_pooled.md` for the nonlinearity-premium argument.", "",
             "**medMAPE (median per-series) is the headline metric here.** "
             "WMAPE is volume-weighted and unbounded above, so one diverged "
             "series sets the category figure -- CSD Prophet's WMAPE is 60% a "
             "single brand (P0038 F72). Both are reported; prefer medMAPE when "
             "comparing per-series statistical baselines. "
             "For SRQ4 comparison vs the tabular models (tuned_summary.md).", "",
             "| Category | Model | medMAPE | WMAPE | n_series |",
             "|---|---|---|---|---|"]
    for _, x in df.iterrows():
        lines.append(f"| {x['category']} | {x['model']} | {x['median_mape']:.1f}% | {x['wmape']:.1f}% | {int(x['n_series'])} |")
    (RES / "stat_baselines.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("Saved stat_baselines.csv + stat_baselines.md")


if __name__ == "__main__":
    main()
