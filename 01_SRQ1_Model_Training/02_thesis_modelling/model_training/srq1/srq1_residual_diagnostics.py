#!/usr/bin/env python3
"""
SRQ1 residual diagnostics -- the Ljung-Box portmanteau test on ARIMA residuals.

Answers one question, and it is a gate rather than a result: **do the residuals of
the reported ARIMA baseline still contain autocorrelation?** If they do, the model
has left structure unmodelled and richer seasonal features are justified. If they
do not, the residuals are white noise and no feature addition can recover anything
further from the univariate signal -- which is itself a reportable finding.

WHY THIS TEST, AND WHY ON ARIMA
-------------------------------
Hyndman & Athanasopoulos (*Forecasting: Principles and Practice*, 3rd ed.) make the
residual check part of the modelling loop rather than an afterthought: ch 9.7 step 6
says that if the residuals "do not look like white noise, try a modified model".
Ch 5.4 defines the portmanteau tests themselves.

The test is run on ARIMA and not on the gradient-boosted models deliberately. The
degrees-of-freedom correction below is defined in terms of ARIMA orders; a boosted
tree has no p and no q, so the correction has no meaning there and the test would
report unadjusted -- that is, overstated -- significance.

THE DEGREES-OF-FREEDOM CORRECTION
---------------------------------
Ch 9.7 specifies that a portmanteau test applied to the residuals of a fitted ARIMA
uses **l - K** degrees of freedom, where K = p + q is the number of fitted ARMA
parameters. The book's own worked example passes dof explicitly for this reason.

Omitting it is not a minor inaccuracy: it inflates the apparent significance, so the
test reports remaining autocorrelation that is partly an artefact of the unadjusted
statistic. For a gate whose job is to decide whether MORE work is warranted, that
bias points in the self-serving direction, so it is corrected here.

The baseline in srq1_baselines_stat.py fits SARIMAX(order=(1,1,1)), giving
p = 1, q = 1 and therefore DOF = 2. Both are derived from ARIMA_ORDER below rather
than written as a literal, so the two cannot drift apart.

WHAT IT READS AND WRITES
------------------------
Reads the same engineered brand x month matrices as the baselines, and applies the
same brand-retention rule, so the panel it describes is the panel the reported
baseline table describes. It loads no persisted model and writes no model: the
SARIMAX fits are recomputed here, which takes seconds per category.

Usage:  python srq1_residual_diagnostics.py
Output: <results>/tables/residual_diagnostics.{csv,md}
"""
import sys
import warnings
import logging
from pathlib import Path

import numpy as np
import pandas as pd

# Repo root located by searching upward for PATHS.py rather than by a fixed
# parents[N] index, which breaks silently whenever a script moves a directory
# deeper. Same pattern as the sibling srq1_* scripts.
_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))

warnings.filterwarnings("ignore")
logging.getLogger("statsmodels").setLevel(logging.CRITICAL)

# The active horizon, and the paths that follow from it. ONE source, so the
# matrix read and the results written can never describe different horizons.
from _horizon import HORIZON, matrix_path, results_root, banner  # noqa: E402,F401

CATS = {"CSD": "csd", "Danskvand": "danskvand",
        "Energidrikke": "energidrikke", "RTD": "rtd"}

# The order fitted by the reported baseline (srq1_baselines_stat.py::run_arima).
# DOF is derived from it, never typed: ch 9.7 requires K = p + q, and deriving it
# means changing the order here cannot leave a stale correction behind.
ARIMA_ORDER = (1, 1, 1)
P, D, Q = ARIMA_ORDER
DOF = P + Q

# Two full seasonal cycles. Ch 5.4 recommends l = 2m for seasonal data, and m = 12
# for a monthly panel. The test needs l > dof to have any degrees of freedom left.
SEASONAL_PERIOD = 12
LB_LAG = 2 * SEASONAL_PERIOD

ALPHA = 0.05

# Brand-retention rule, copied from srq1_baselines_stat.py::main so this gate
# describes the same series set as the reported baseline table.
MIN_FIT_MONTHS = 12


def _date(yr, mo):
    return pd.Timestamp(int(yr), int(mo), 1)


def fit_arima_residuals(y_units):
    """Fit the reported ARIMA and return its in-sample residuals, or None.

    The log1p/expm1 pair matches run_arima exactly: log1p handles the genuine
    zeros in this panel without a max(y, 1.0) floor that would rewrite a real
    zero as a one. Residuals are taken in LOG space, which is the space the
    model's own error assumptions live in -- back-transforming them first would
    reintroduce the multiplicative skew the log was applied to remove.
    """
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    y = np.log1p(np.maximum(np.asarray(y_units, float), 0.0))
    m = SARIMAX(y, order=ARIMA_ORDER,
                enforce_stationarity=False, enforce_invertibility=False)
    r = m.fit(disp=False)
    resid = np.asarray(r.resid, float)

    # The differencing order consumes the first d residuals, which are not
    # model errors but initialisation artefacts of the state-space filter.
    # Including them would inject a spurious spike at the lowest lags.
    if D > 0:
        resid = resid[D:]
    resid = resid[np.isfinite(resid)]
    return resid if len(resid) else None


def ljung_box(resid, lag, dof):
    """Ljung-Box Q at a single lag, with the ch 9.7 degrees-of-freedom correction.

    Returns (statistic, p_value), or None when the series is too short for the
    test to be defined -- which needs strictly more usable lags than parameters
    consumed, plus enough observations for the autocorrelations to be estimable.
    """
    from statsmodels.stats.diagnostic import acorr_ljungbox

    # Need lag < len(resid) for the autocorrelations, and lag > dof for the
    # chi-squared to retain at least one degree of freedom.
    usable_lag = min(lag, len(resid) - 1)
    if usable_lag <= dof:
        return None

    out = acorr_ljungbox(resid, lags=[usable_lag], model_df=dof,
                         return_df=True)
    stat = float(out["lb_stat"].iloc[0])
    pval = float(out["lb_pvalue"].iloc[0])
    if not np.isfinite(pval):
        return None
    return stat, pval, usable_lag


def seasonal_acf(resid, period=SEASONAL_PERIOD):
    """Residual autocorrelation at the seasonal lag.

    Reported alongside the portmanteau result because it localises the failure.
    A significant Q tells you structure remains; a large ACF at lag 12 tells you
    it is ANNUAL structure -- which is the specific evidence for fitting a
    seasonal order rather than adding features.
    """
    if len(resid) <= period + 1:
        return float("nan")
    from statsmodels.tsa.stattools import acf
    a = acf(resid, nlags=period, fft=False)
    return float(a[period]) if np.isfinite(a[period]) else float("nan")


def main():
    banner()
    print(f"Ljung-Box on ARIMA{ARIMA_ORDER} residuals "
          f"(lag={LB_LAG}, dof={DOF}, alpha={ALPHA})")
    print(f"dof = p + q = {P} + {Q} = {DOF}  [Hyndman & Athanasopoulos ch 9.7]")
    print()

    per_brand = []

    for cat, slug in CATS.items():
        fm = pd.read_parquet(matrix_path(cat, slug))
        d = fm.dropna(subset=["sales_units"]).copy()
        d["ds"] = [_date(y, m) for y, m in zip(d.period_year, d.period_month)]

        for brand, g in d.groupby("brand"):
            g = g.sort_values("period_index")
            fit = g[g.split.isin(["train", "val"])]
            test = g[g.split == "test"]
            # Same retention rule as the reported baselines.
            if len(fit) < MIN_FIT_MONTHS or len(test) == 0:
                continue

            try:
                resid = fit_arima_residuals(fit.sales_units.values)
            except Exception:
                resid = None
            if resid is None:
                continue

            lb = ljung_box(resid, LB_LAG, DOF)
            if lb is None:
                continue
            stat, pval, used_lag = lb

            per_brand.append(dict(
                category=cat, brand=brand,
                n_resid=len(resid), lag=used_lag, dof=DOF,
                lb_stat=stat, lb_pvalue=pval,
                rejects=bool(pval < ALPHA),
                acf_seasonal=seasonal_acf(resid),
            ))

    if not per_brand:
        raise SystemExit("No series produced a testable ARIMA fit -- "
                         "check the matrices and the retention rule.")

    pb = pd.DataFrame(per_brand)

    # Per-category summary. The rejection RATE is the gate's readout: a single
    # brand's p-value says little, but the share of brands whose residuals retain
    # autocorrelation is the panel-level verdict.
    rows = []
    for cat in CATS:
        s = pb[pb.category == cat]
        if s.empty:
            continue
        rows.append(dict(
            category=cat,
            n_series=len(s),
            n_reject=int(s.rejects.sum()),
            reject_rate=float(s.rejects.mean() * 100),
            median_p=float(s.lb_pvalue.median()),
            median_acf12=float(np.nanmedian(s.acf_seasonal)),
        ))
    summ = pd.DataFrame(rows)

    overall_n = int(len(pb))
    overall_rej = int(pb.rejects.sum())
    overall_rate = overall_rej / overall_n * 100
    overall_acf12 = float(np.nanmedian(pb.acf_seasonal))

    for _, x in summ.iterrows():
        print(f"  {x.category:13s} reject {x.n_reject:3d}/{x.n_series:3d} "
              f"({x.reject_rate:5.1f}%)  median p={x.median_p:.4f}  "
              f"median ACF(12)={x.median_acf12:+.3f}")
    print()
    print(f"  {'OVERALL':13s} reject {overall_rej:3d}/{overall_n:3d} "
          f"({overall_rate:5.1f}%)  median ACF(12)={overall_acf12:+.3f}")
    print()

    # The gate verdict. Stated by the script rather than left to a reader, because
    # the whole point of a gate is that it decides something. The threshold is the
    # ordinary one: at alpha=0.05 a white-noise panel rejects ~5% of the time by
    # construction, so a rate materially above that is remaining structure.
    white_noise = overall_rate <= (ALPHA * 100) * 2
    verdict = ("WHITE NOISE -- no remaining autocorrelation to exploit"
               if white_noise else
               "AUTOCORRELATION REMAINS -- structure is left unmodelled")
    print(f"  GATE G1: {verdict}")

    out_dir = results_root() / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)

    pb.to_csv(out_dir / "residual_diagnostics_per_brand.csv", index=False)
    summ.to_csv(out_dir / "residual_diagnostics.csv", index=False)

    # Every figure below is interpolated from a value computed this run. Nothing
    # is transcribed -- a hardcoded result is true when typed and wrong after the
    # next re-run.
    lines = [
        "# SRQ1 residual diagnostics -- Ljung-Box on ARIMA residuals",
        "",
        f"Portmanteau test applied to the in-sample residuals of "
        f"ARIMA{ARIMA_ORDER}, the statistical baseline reported in "
        f"`stat_baselines.md`. Tested at lag {LB_LAG} (two seasonal cycles, "
        f"m = {SEASONAL_PERIOD}) against a chi-squared with "
        f"`lag - {DOF}` degrees of freedom.",
        "",
        f"**The degrees-of-freedom correction matters.** Hyndman & "
        f"Athanasopoulos (3rd ed., ch 9.7) specify that a portmanteau test on "
        f"the residuals of a fitted ARIMA consumes one degree of freedom per "
        f"fitted ARMA parameter, so `K = p + q = {P} + {Q} = {DOF}` here. "
        f"Omitting it overstates significance, reporting autocorrelation that "
        f"is partly an artefact of the unadjusted statistic.",
        "",
        f"The test is applied to ARIMA rather than to the gradient-boosted "
        f"models because the correction is defined in terms of ARIMA orders; a "
        f"boosted tree has no `p` and no `q`, so the same test there would be "
        f"uncorrectable and its significance overstated by construction.",
        "",
        f"Residuals are taken in log space, matching the `log1p` transform the "
        f"baseline fits on. The first {D} residual(s) per series are dropped as "
        f"differencing initialisation rather than model error.",
        "",
        "| Category | n series | rejects H0 | rejection rate | median p | median ACF(12) |",
        "|---|---|---|---|---|---|",
    ]
    for _, x in summ.iterrows():
        lines.append(f"| {x.category} | {int(x.n_series)} | {int(x.n_reject)} | "
                     f"{x.reject_rate:.1f}% | {x.median_p:.4f} | "
                     f"{x.median_acf12:+.3f} |")
    lines.append(f"| **Overall** | **{overall_n}** | **{overall_rej}** | "
                 f"**{overall_rate:.1f}%** | | **{overall_acf12:+.3f}** |")
    lines += [
        "",
        f"`ACF(12)` is the residual autocorrelation at the seasonal lag. It "
        f"localises the failure: a significant Q says structure remains, while "
        f"a large ACF at lag {SEASONAL_PERIOD} says that structure is annual.",
        "",
        f"**Reading the rejection rate.** At alpha = {ALPHA}, a panel of genuine "
        f"white noise rejects about {ALPHA * 100:.0f}% of the time by "
        f"construction. A rate materially above that is remaining structure, "
        f"not test noise.",
        "",
        f"**Verdict: {verdict}.**",
        "",
    ]
    (out_dir / "residual_diagnostics.md").write_text(
        "\n".join(lines), encoding="utf-8")

    print(f"  wrote {out_dir / 'residual_diagnostics.md'}")
    print(f"  wrote {out_dir / 'residual_diagnostics.csv'}")
    print(f"  wrote {out_dir / 'residual_diagnostics_per_brand.csv'}")


if __name__ == "__main__":
    main()
