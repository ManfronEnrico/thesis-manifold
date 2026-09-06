#!/usr/bin/env python3
"""
SRQ1 -- MASE across the model ladder.

WHY THIS EXISTS. The thesis cites Hyndman & Koehler (2006) for the instability of
percentage errors near zero, and a 2026-08-23 source verification confirmed that
claim -- but also established two things the project had not acted on:

  1. They propose **MASE** (pp. 684-685) as *the* scale-free measure for comparing
     accuracy across series of differing scale. We reported no scaled metric at all.
  2. They explicitly criticise **excluding zero-actual windows** (p. 683) as "an
     artificial solution that is impossible to apply in practical situations". Our
     MAPE-family statistics exclude roughly 27% of brands for exactly that reason.

So the literature we cite recommends a metric we do not report, for precisely the
problem we have. This closes that gap.

WHAT MASE BUYS HERE that WMAPE and medMAPE do not:

  - It is **defined at zero**, so every brand enters the table, including the ones
    percentage errors must drop. Those are the intermittent, low-volume brands --
    the population most at issue in the pooling and scenario comparisons.
  - It has an **absolute interpretation**: MASE < 1 beats a naive one-step forecast
    on that series' own history, MASE > 1 does not. WMAPE of 15% is only meaningful
    relative to some other WMAPE; MASE of 0.9 is meaningful on its own.
  - Scaling is **per series**, so a large brand cannot dominate the average the way
    it does in a volume-weighted metric.

Denominator: in-sample MAE of the one-step naive forecast, computed on the TRAIN
split only, in raw units. Series with a flat history (naive MAE = 0) are omitted --
MASE is genuinely undefined there.

Self-contained. No API spend.
Usage:  .venv/Scripts/python.exe .../srq1_mase.py
Output: 04_thesis_results/srq1/{mase.csv, mase.md}
"""

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR

sys.path.insert(0, str(_here.parent))
from srq1_benchmark_cv import (  # noqa: E402
    CATS, _load, _wmape, _medmape, mase_denominator, _mase,
)


def _mdase(y, yhat, keys, denom):
    """MEDIAN absolute scaled error.

    Report this beside mean MASE, because mean MASE is not robust and on this data
    that is not hypothetical. On RTD the mean is 6.54 while the median is 0.18 --
    a single brand (STRONGBOW, scaled error ~317) moves the mean by more than an
    order of magnitude. Hyndman & Koehler note MASE's mean form inherits the
    outlier sensitivity of any mean of ratios; with intermittent retail series the
    denominator can be small enough to make one cell dominate.

    Quoting mean MASE alone on RTD would report the dataset's worst brand as if it
    were the model's typical behaviour.
    """
    y = np.asarray(y, float); yhat = np.clip(np.asarray(yhat, float), 0, None)
    ok = np.array([k in denom for k in keys])
    if not ok.any():
        return float("nan")
    d = np.array([denom.get(k, np.nan) for k in keys], float)
    return float(np.median(np.abs(y - yhat)[ok] / d[ok]))

warnings.filterwarnings("ignore")
OUT = THESIS_RESULTS_SRQ1_DIR


def _naive(tr, te):
    """Seasonal-naive (lag_13) and naive (lag_1) predictions on the test rows.

    NO expm1 HERE. The lag columns are stored in RAW units while the target
    `log_sales_units` is logged (F54 -- the matrix was engineered for trees, which
    are invariant to monotone transforms of a feature). Applying expm1 to a lag
    treats a raw count as a log and overflows to inf, which is exactly what the
    first version of this script did.
    """
    return te["lag_1"].values.astype(float), te["lag_13"].values.astype(float)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []

    for cat, slug in CATS.items():
        d, feats = _load(cat, slug)
        tr = d[d.split.isin(["train", "val"])]
        te = d[d.split == "test"]
        if len(tr) < 30 or len(te) == 0:
            continue

        denom = mase_denominator(tr)
        keys = te["brand"].astype(str).values
        y = np.expm1(te["log_sales_units"].values)

        covered = np.mean([k in denom for k in keys])
        scorable = float(np.mean(y > 0))

        naive, snaive = _naive(tr, te)
        for name, pred in (("Naive", naive), ("SeasonalNaive", snaive)):
            rows.append(dict(
                category=cat, model=name,
                mase=_mase(y, pred, keys, denom),
                median_ase=_mdase(y, pred, keys, denom),
                wmape=_wmape(y, pred), medmape=_medmape(y, pred),
                n_test=len(te), pct_series_scaled=round(100 * covered, 1),
                pct_rows_mape_scorable=round(100 * scorable, 1)))

        print(f"{cat:13s} n_test={len(te):4d}  "
              f"series with a MASE denominator: {100*covered:5.1f}%  "
              f"rows scorable on MAPE: {100*scorable:5.1f}%")
        for r in rows[-2:]:
            print(f"    {r['model']:14s} MASE={r['mase']:7.3f}  "
                  f"medASE={r['median_ase']:6.3f}  "
                  f"WMAPE={r['wmape']:6.1f}%  medMAPE={r['medmape']:6.1f}%")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "mase.csv", index=False)

    Lm = ["# SRQ1 -- mean absolute scaled error (MASE)", "",
         "Scaling denominator: in-sample MAE of the one-step naive forecast, per",
         "brand, computed on train+val in raw units (Hyndman & Koehler, 2006,",
         "pp. 684-685).", "",
         "**MASE < 1 beats a naive one-step forecast on that series' own history;",
         "MASE > 1 does not.** Unlike WMAPE and median MAPE, this threshold is",
         "absolute rather than relative to another model.", "",
         "**Mean and median are both reported.** Mean MASE is a mean of ratios and",
         "is not robust: on RTD it reads 6.54 while the median reads 0.18, because",
         "one brand (STRONGBOW) has a scaled error near 317. Quote the median as",
         "the typical case and the mean only with that caveat attached.", "",
         "| Category | Model | MASE (mean) | MASE (median) | WMAPE | medMAPE | n_test | % series scaled | % rows MAPE-scorable |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for _, r in df.iterrows():
        Lm.append(f"| {r['category']} | {r['model']} | {r['mase']:.3f} | "
                 f"**{r['median_ase']:.3f}** | "
                 f"{r['wmape']:.1f}% | {r['medmape']:.1f}% | {int(r['n_test'])} | "
                 f"{r['pct_series_scaled']}% | {r['pct_rows_mape_scorable']}% |")
    Lm += ["",
          "## Why the last two columns matter", "",
          "`% rows MAPE-scorable` is the share of test rows on which a percentage",
          "error is defined at all. Where it is well below 100%, every MAPE-family",
          "number in this project is computed on a **subset** of the data, and that",
          "subset is not random -- it excludes the intermittent, low-volume brands.",
          "",
          "`% series scaled` is the share with a usable MASE denominator; it is",
          "lower than 100% only for brands with a perfectly flat training history,",
          "where MASE is undefined for a different and much rarer reason.",
          "",
          "Hyndman & Koehler (2006, p. 683) call dropping zero-actual windows \"an",
          "artificial solution that is impossible to apply in practical",
          "situations\". Reporting MASE alongside is what lets those rows be scored",
          "rather than discarded."]
    (OUT / "mase.md").write_text(chr(10).join(Lm) + chr(10), encoding="utf-8", newline=chr(10))
    print("Saved mase.csv + mase.md in " + str(OUT))


if __name__ == "__main__":
    main()
