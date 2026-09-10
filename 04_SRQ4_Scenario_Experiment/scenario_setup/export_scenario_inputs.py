#!/usr/bin/env python3
"""
Materialise the per-brand series each scenario is given, as shipped CSV files.

WHY THIS EXISTS
---------------
Scenarios B and D are handed one brand's monthly history and asked to forecast a
held-out month. Today that series is built at run time from
`_03_engineered/*.parquet` via `_brand_history()`.

An assessor reading the results has no way to see what Scenario B was actually
given. The series is built at run time and pasted into a prompt; it exists in the
logs, in a form nobody wants to read, and nowhere else.

DEC-SHARE-CSV (Brian, 2026-09-10) permits shipping it: what Scenario B receives
is already filtered to one brand and aggregated to monthly -- not live warehouse
access, and not the dataset -- so it discloses no more than the thesis tables do.

WHAT THESE FILES ARE, AND ARE NOT
---------------------------------
They are **evidence, not a dependency**. The harness reads
`_03_engineered/bymonth/*.parquet` and never reads this directory; the
engineered matrices are tracked and ship with the submission, so scenarios A-C
run with or without these CSVs.

What they add is inspection without execution: an assessor can see the exact
bytes Scenario B was handed, and `index.csv` carries the held-out actual, which
is what lets a scored run be verified. An earlier version of this docstring
claimed the CSVs were what kept A-C runnable -- that was written against an
assumption that the matrices would be stripped, and it is not true of the
repository that actually ships.

WHAT IS WRITTEN, AND WHY IT IS EXACTLY WHAT THE HARNESS USES
------------------------------------------------------------
The rows come from `_brand_history()` itself, not from a reimplementation. That
matters: the function withholds the test window, asserts no leakage, and pins the
scored month to the horizon. A second code path would be free to drift from all
three -- silently, which is this project's dominant failure mode (F21/F25/F31/F32).

Per brand:
  * `<category>__<brand>.csv`  -- the fit series: period_year, period_month,
    sales_units, promo_intensity. Byte-identical to the CSV pasted into Scenario
    B's prompt.
  * a row in `index.csv` -- category, brand, stratum, rows, span, the scored
    month, and the held-out actual.

The held-out actual IS included, deliberately. It is the ground truth the thesis
reports and an assessor needs it to verify a scored run. It is not in the CSV the
model sees.

STRATIFICATION
--------------
Three brands per category by default -- highest / median / lowest volume, via
`_stratified_brands()`. That is the sample the funded design uses, so an assessor
can answer the generalisability question on sparse brands as well as strong ones.
`--all-scorable` writes every scorable brand instead (168 at H=3).

USAGE
    python export_scenario_inputs.py                # 3 per category, the funded sample
    python export_scenario_inputs.py --all-scorable
    python export_scenario_inputs.py --dry-run      # list what would be written
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_root = next((p for p in HERE.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {HERE}")
sys.path.insert(0, str(_root))
sys.path.insert(0, str(HERE))

import pandas as pd  # noqa: E402

import srq4_experiment as E  # noqa: E402

# The stratum labels, in the order _stratified_brands() returns them. Named here
# rather than inferred, so a reader of index.csv knows what "median" meant.
_STRATA = ("max_volume", "median_volume", "min_volume")


def _out_dir() -> Path:
    """Beside the runs the scenarios produce, inside the SRQ4 results tier.

    Not in `_03_engineered`: that tree is deleted by the export, which is the
    whole reason this script exists.
    """
    d = Path(E.THESIS_RESULTS_SRQ4_DIR) / "scenario_inputs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _safe(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in str(name))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--all-scorable", action="store_true",
                    help="every scorable brand, not just the stratified 3 per category")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    out = _out_dir()
    print(f"  horizon H={E.HORIZON}   ->  {out}\n")

    rows, written = [], 0
    for cat in E.CAT_FILE:
        brands = (E._scorable_brands(cat) if a.all_scorable
                  else E._stratified_brands(cat))
        for i, brand in enumerate(brands):
            # Straight from the harness. Withholds the test window, asserts no
            # leakage, and pins the scored month to HORIZON -- all three would be
            # at risk in a reimplementation.
            fit, actual, target = E._brand_history(cat, brand)
            if fit is None or not len(fit) or actual is None:
                print(f"  skip {cat}/{brand}: no scorable history")
                continue

            stratum = _STRATA[i] if not a.all_scorable and i < len(_STRATA) else "all"
            fname = f"{_safe(cat)}__{_safe(brand)}.csv"
            span = (f"{int(fit.period_year.min())}-"
                    f"{int(fit[fit.period_year == fit.period_year.min()].period_month.min()):02d}"
                    f"..{int(fit.period_year.max())}-"
                    f"{int(fit[fit.period_year == fit.period_year.max()].period_month.max()):02d}")

            if not a.dry_run:
                # index=False and the harness's own column order, so this file is
                # byte-identical to the CSV pasted into Scenario B's prompt.
                fit.to_csv(out / fname, index=False, lineterminator="\n")
            written += 1
            rows.append({"category": cat, "brand": brand, "stratum": stratum,
                         "file": fname, "rows": len(fit), "history_span": span,
                         "scored_month": target, "held_out_actual": actual})
            print(f"  {cat:14s} {brand:16s} {stratum:14s} "
                  f"{len(fit):3d} rows  {span}  -> {target}")

    if a.dry_run:
        print(f"\n  [dry] {written} file(s) would be written")
        return 0

    idx = pd.DataFrame(rows)
    idx.to_csv(out / "index.csv", index=False, lineterminator="\n")

    readme = out / "README.md"
    readme.write_text(
        "# Scenario inputs\n\n"
        "One CSV per brand: the monthly sales history a scenario is given, and\n"
        "nothing else. This is exactly what Scenario B receives in its prompt and\n"
        "what Scenario D is handed, so the two arms differ only in the\n"
        "orchestrator around them.\n\n"
        f"Forecast horizon: **H={E.HORIZON}** (months ahead).\n\n"
        "## Columns\n\n"
        "| Column | Meaning |\n|---|---|\n"
        "| `period_year`, `period_month` | the observation month |\n"
        "| `sales_units` | units sold, that brand, that month |\n"
        "| `promo_intensity` | share of units sold on promotion, lagged; absent "
        "where Nielsen reports no promotion for the category |\n\n"
        "## What is deliberately NOT here\n\n"
        "The **held-out months are withheld** from every CSV. Each series stops at\n"
        "the training cutoff; the month being forecast is not in the file a model\n"
        "sees. `index.csv` records `scored_month` and `held_out_actual` so a run\n"
        "can be verified, but a scenario is never shown them.\n\n"
        "## Selection\n\n"
        "Three brands per category: highest, median and lowest volume among those\n"
        "with a complete non-zero held-out window. The spread is deliberate, so\n"
        "results can be read for sparse brands as well as strong ones.\n\n"
        "## Provenance\n\n"
        "Written by `04_SRQ4_Scenario_Experiment/scenario_setup/"
        "export_scenario_inputs.py`, which calls the experiment harness's own\n"
        "`_brand_history()` rather than rebuilding the series -- so these files\n"
        "cannot drift from what the scenarios actually run on.\n",
        encoding="utf-8", newline="\n")

    print(f"\n  {written} series + index.csv + README.md written to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
