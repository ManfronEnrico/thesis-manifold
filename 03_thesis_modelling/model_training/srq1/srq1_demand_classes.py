#!/usr/bin/env python3
"""
SRQ1 -- Syntetos-Boylan-Croston demand categorisation.

WHY THIS EXISTS. Per-brand accuracy comparisons on this panel were previously guarded
by a **volume floor of 1 unit/month** -- a threshold chosen by judgement to keep
near-empty series from producing WMAPE deltas in the thousands of percentage points.
It worked, but it was arbitrary, and the literature offers a principled replacement.

Syntetos, Boylan & Croston (2005), *JORS* 56(5), 495-503, derive a categorisation of
demand patterns from two measurable quantities, with **non-arbitrary cut-offs**:

    p    = average inter-demand interval        (periods per non-zero demand)
    CV^2 = squared coefficient of variation of NON-ZERO demand sizes

                    CV^2 <= 0.49        CV^2 > 0.49
    p <= 1.32       smooth              erratic
    p  > 1.32       intermittent        lumpy

The thresholds are derived, not tuned: they are the points at which the relative
accuracy ordering of Croston's method, the Syntetos-Boylan Approximation and simple
exponential smoothing changes (alpha = 0.15, lead time 1).

WHY IT IS BETTER THAN THE FLOOR IT REPLACES. Measured on this panel, the volume floor
was a poor proxy for the thing it was trying to exclude:

  - it removed **8 smooth brands** -- well-behaved series that happen to be small,
    which is exactly the population a forecasting study should keep;
  - it left **21 lumpy/intermittent brands** above the line, the very series whose
    erratic behaviour motivated the floor.

Volume and regularity are different properties. The SBC scheme measures the one that
matters.

WHAT THIS BUYS THE WRITE-UP. Accuracy can be reported **per demand pattern** instead
of pooled behind a threshold. "The model reaches X% on smooth series and Y% on lumpy
ones" is a more informative and more honest result than a single number computed after
dropping the hard cases -- and it answers the objection that both Hyndman & Koehler
(2006, p. 683) and Syntetos & Boylan (2005) raise, that difficult series should be
**modelled or categorised**, not discarded.

IMPORTANT -- THIS IS A CATEGORISATION, NOT AN EXCLUSION RULE. Nothing here drops a
brand. Every series is classified and reported. Whether any quadrant is excluded from a
particular table is a separate, explicit decision.

Classification uses TRAIN+VAL only. Using test rows to categorise and then reporting
test accuracy per category would leak.

Self-contained. No API spend.
Usage:  .venv/Scripts/python.exe .../srq1_demand_classes.py
Output: 04_thesis_results/srq1/{demand_classes.csv, demand_classes.md}
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
from srq1_benchmark_cv import CATS, _load  # noqa: E402

warnings.filterwarnings("ignore")
OUT = THESIS_RESULTS_SRQ1_DIR

P_CUT = 1.32      # Syntetos, Boylan & Croston (2005), p. 495
CV2_CUT = 0.49    # same
MIN_PERIODS = 4   # below this, p and CV^2 are not estimable with any confidence


def classify(p, cv2):
    """The four SBC quadrants. Boundaries follow the paper: <= is the lower class."""
    if p > P_CUT:
        return "lumpy" if cv2 > CV2_CUT else "intermittent"
    return "erratic" if cv2 > CV2_CUT else "smooth"


def series_stats(y):
    """p and CV^2 for one series, from RAW units.

    p is periods-per-non-zero-demand: total periods divided by the number of periods
    with non-zero demand. CV^2 is computed on the NON-ZERO sizes only -- including the
    zeros would conflate the two dimensions the scheme deliberately separates.
    """
    y = np.asarray(y, float)
    n = len(y)
    nz = y[y > 0]
    if n < MIN_PERIODS or len(nz) == 0:
        return None
    p = n / len(nz)
    cv2 = ((nz.std(ddof=1) / nz.mean()) ** 2
           if len(nz) > 1 and nz.mean() > 0 else 0.0)
    return p, float(cv2), n, len(nz)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []

    for cat, slug in CATS.items():
        d, _ = _load(cat, slug)
        tr = d[d.split.isin(["train", "val"])]
        te = d[d.split == "test"]
        sort_col = "period_index" if "period_index" in tr.columns else None

        test_mean = {b: float(np.expm1(g["log_sales_units"].values).mean())
                     for b, g in te.groupby("brand")}

        for b, g in tr.groupby("brand"):
            gg = g.sort_values(sort_col) if sort_col else g
            st = series_stats(np.expm1(gg["log_sales_units"].values))
            if st is None:
                continue
            p, cv2, n, nnz = st
            rows.append(dict(
                category=cat, brand=str(b), p=round(p, 3), cv2=round(cv2, 3),
                demand_class=classify(p, cv2), n_periods=n, n_nonzero=nnz,
                mean_test_units=round(test_mean.get(b, np.nan), 2)))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "demand_classes.csv", index=False)

    order = ["smooth", "erratic", "intermittent", "lumpy"]
    piv = (df.pivot_table(index="category", columns="demand_class",
                          values="brand", aggfunc="count")
             .reindex(columns=order).fillna(0).astype(int))

    L = ["# SRQ1 -- demand-pattern categorisation (Syntetos-Boylan-Croston)", "",
         "Every brand is classified on two measured quantities, using the derived",
         "cut-offs of Syntetos, Boylan & Croston (2005, *JORS* 56(5), 495-503, p. 495):",
         "",
         "- **p** -- average inter-demand interval (periods per non-zero demand)",
         "- **CV^2** -- squared coefficient of variation of **non-zero** demand sizes",
         "",
         f"| | CV^2 <= {CV2_CUT} | CV^2 > {CV2_CUT} |",
         "|---|---|---|",
         f"| **p <= {P_CUT}** | smooth | erratic |",
         f"| **p > {P_CUT}** | intermittent | lumpy |", "",
         "The thresholds are **derived, not tuned** -- they mark where the relative",
         "accuracy ordering of Croston's method, the SBA and simple exponential",
         "smoothing changes. Classification uses **train+val only**; using test rows to",
         "categorise and then reporting test accuracy per class would leak.", "",
         "## Brands per class", "",
         "| Category | " + " | ".join(order) + " | total |",
         "|---|" + "---|" * (len(order) + 1)]
    for cat, r in piv.iterrows():
        L.append(f"| {cat} | " + " | ".join(str(r[c]) for c in order)
                 + f" | {int(r.sum())} |")
    tot = piv.sum()
    L.append("| **all** | " + " | ".join(f"**{int(tot[c])}**" for c in order)
             + f" | **{int(tot.sum())}** |")

    # The comparison that justifies the replacement.
    have = df.mean_test_units.notna()
    below = df[have & (df.mean_test_units < 1.0)]
    above_hard = df[have & (df.mean_test_units >= 1.0)
                    & df.demand_class.isin(["lumpy", "intermittent"])]
    L += ["", "## Why this replaces the 1 unit/month volume floor", "",
          "The floor was a judgement call standing in for 'series too irregular to",
          "inform a comparison'. Volume is a poor proxy for regularity, and the",
          "measured overlap shows how poor:", "",
          "| | brands |",
          "|---|---:|",
          f"| Below the old floor (<1 unit/month) | {len(below)} |",
          f"| — of which **smooth** (well-behaved, merely small) | **{int((below.demand_class == 'smooth').sum())}** |",
          f"| — of which lumpy or intermittent | {int(below.demand_class.isin(['lumpy', 'intermittent']).sum())} |",
          f"| **Above** the floor yet lumpy/intermittent (the floor missed them) | **{len(above_hard)}** |", "",
          "So the floor **removed well-behaved small brands** -- exactly the series a",
          "forecasting study should keep -- while **leaving irregular ones in**. The SBC",
          "scheme measures the property that actually matters.", "",
          "## How to use this", "",
          "**This categorises; it does not exclude.** Report accuracy **per demand",
          "class**, so that a weak result on lumpy series is visible as a stated",
          "limitation rather than absorbed into a pooled average or hidden behind a",
          "threshold. Both Hyndman & Koehler (2006, p. 683) and Syntetos & Boylan",
          "(2005) object to discarding difficult series; categorising them is the",
          "response their own work recommends.", "",
          "**A caveat to state.** The cut-offs were derived for Croston-type estimators",
          "under specific assumptions (alpha = 0.15, lead time 1), not for gradient",
          "boosting on a brand-month panel. They are used here as a **principled,",
          "citable partition of demand patterns**, not as a claim that the same",
          "accuracy ordering holds for these models -- which is itself a question the",
          "per-class results can answer."]
    (OUT / "demand_classes.md").write_text("\n".join(L) + "\n",
                                           encoding="utf-8", newline="\n")

    print(piv.to_string())
    print(f"\nBelow old floor: {len(below)} brands "
          f"({int((below.demand_class == 'smooth').sum())} of them SMOOTH)")
    print(f"Above floor but lumpy/intermittent: {len(above_hard)}")
    print(f"\nSaved demand_classes.csv + demand_classes.md in {OUT}")


if __name__ == "__main__":
    main()
