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
  * `<category>__<brand>.csv`  -- the fit series as the WAREHOUSE EXTRACT
    provides it: 32 brand-month columns, byte-identical to the CSV pasted into
    Scenario B's prompt. Verified byte-for-byte against the funded runs'
    logged prompts on 2026-09-14.
  * a row in `index.csv` -- category, brand, stratum, rows, span, the scored
    month, and the held-out actual.

WHICH CATEGORIES CAN BE EXPORTED, AND WHY NOT ALL FOUR
-------------------------------------------------------
`_brand_history()` reads the pre-cleaning warehouse extract built by
`build_agent_inputs.py` (changed 2026-09-12), NOT the engineered matrix. That
extract exists only for the categories the funded experiment actually scored.

Exporting a category with no extract is a hard FileNotFoundError, by design --
`_agent_history()` refuses to fall back to the engineered frame, because a
silent fallback would ship the engineered columns under the name of the raw
ones. So this script exports only categories that have an extract on disk, and
says which it skipped rather than crashing partway and leaving a folder
describing two different brand selections.

To add a category, build its extract first:
    python build_agent_inputs.py --category <Category>

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
    python export_scenario_inputs.py                # 3 per exportable category
    python export_scenario_inputs.py --all-scorable
    python export_scenario_inputs.py --dry-run      # list what would be written
    python export_scenario_inputs.py --categories CSD Danskvand
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


def _exportable(cat: str) -> bool:
    """True when this category's warehouse extract exists on disk.

    Checked BEFORE any brand is read, so a missing category is reported and
    skipped rather than crashing mid-loop -- which previously left the folder
    holding files from two different brand selections with index.csv never
    rewritten, a worse state than the stale one it replaced.
    """
    return (Path(E.SRQ4_AGENT_INPUTS_DIR) / cat).is_dir()


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
    ap.add_argument("--categories", nargs="+", metavar="CAT",
                    help="categories to export; default is every category whose "
                         "warehouse extract exists")
    a = ap.parse_args()

    out = _out_dir()
    print(f"  horizon H={E.HORIZON}   ->  {out}\n")

    asked = a.categories or list(E.CAT_FILE)
    cats = [c for c in asked if _exportable(c)]
    skipped = [c for c in asked if not _exportable(c)]
    for c in skipped:
        print(f"  skip {c}: no warehouse extract "
              f"(build_agent_inputs.py --category {c})")
    if skipped:
        print()
    if not cats:
        print("  nothing to export")
        return 1

    rows, written = [], 0
    for cat in cats:
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
                         "file": fname, "rows": len(fit), "cols": len(fit.columns),
                         "history_span": span,
                         "scored_month": target, "held_out_actual": actual})
            print(f"  {cat:14s} {brand:16s} {stratum:14s} "
                  f"{len(fit):3d} rows  {span}  -> {target}")

    if a.dry_run:
        print(f"\n  [dry] {written} file(s) would be written")
        return 0

    idx = pd.DataFrame(rows)
    idx.to_csv(out / "index.csv", index=False, lineterminator="\n")

    from datetime import date
    ncols = int(idx_ncols) if (idx_ncols := max(rows, key=lambda r: r["cols"])["cols"]) else 0
    covered = ", ".join(sorted({r["category"] for r in rows}))
    brands = ", ".join(f"{r['brand']}" for r in rows)

    readme = out / "README.md"
    readme.write_text(
        "# Scenario inputs\n\n"
        "One CSV per brand: the monthly sales history a scenario is given, and\n"
        "nothing else. This is exactly what Scenario B receives in its prompt and\n"
        "what Scenario D is handed, so the two arms differ only in the\n"
        "orchestrator around them.\n\n"
        f"Forecast horizon: **H={E.HORIZON}** (months ahead).\n\n"
        "## What this export covers\n\n"
        f"- **Exported:** {date.today().isoformat()}\n"
        f"- **Categories:** {covered}\n"
        f"- **Brands:** {brands}\n"
        f"- **Shape:** {ncols} columns per file\n\n"
        "These are the brands the funded experiment scored. Categories whose\n"
        "warehouse extract was never built are not represented here, because the\n"
        "experiment never ran on them -- see *Provenance* below.\n\n"
        "## Columns\n\n"
        "Each file carries the brand-month row **as the sales data warehouse\n"
        "produces it**, after joining the fact and dimension tables and\n"
        "aggregating to brand-month. That is volume, value and litres, their\n"
        "promotion and baseline splits, and the distribution measures -- the\n"
        "columns a production agent would see by querying the star schema.\n\n"
        "Two points a reader should not have to infer:\n\n"
        "- **These are warehouse columns, not engineered features.** No lag,\n"
        "  rolling statistic or ratio built by the modelling pipeline appears\n"
        "  here. Handing those over would give away the work SRQ4 exists to\n"
        "  measure.\n"
        "- **The scenario also receives the warehouse's own column\n"
        "  documentation**, so the columns are not unexplained. Withholding it\n"
        "  would make a poor result unfalsifiable.\n\n"
        "## What is deliberately NOT here\n\n"
        "The **held-out months are withheld** from every CSV. Each series stops at\n"
        "the training cutoff; the month being forecast is not in the file a model\n"
        "sees. `index.csv` records `scored_month` and `held_out_actual` so a run\n"
        "can be verified, but a scenario is never shown them.\n\n"
        "## Selection\n\n"
        "Up to three brands per category: highest, median and lowest volume among\n"
        "those with a complete non-zero held-out window whose scored actual clears\n"
        f"the {E.MIN_SCORED_UNITS:,}-unit floor. The spread is deliberate, so results can\n"
        "be read for sparse brands as well as strong ones; the floor exists\n"
        "because a defined percentage error is not automatically a meaningful\n"
        "one, and on a nine-unit series it measures integer rounding.\n\n"
        "## Provenance\n\n"
        "Written by `04_SRQ4_Scenario_Experiment/scenario_setup/"
        "export_scenario_inputs.py`, which calls the experiment harness's own\n"
        "`_brand_history()` rather than rebuilding the series.\n\n"
        "**This is an export, and an export has a date.** It reflects the brand\n"
        "selection and column shape in force on the date above. It is not\n"
        "self-updating: if the selection rule or the extract changes, this folder\n"
        "is stale until the script is run again. Re-run it rather than editing\n"
        "anything here by hand.\n",
        encoding="utf-8", newline="\n")

    print(f"\n  {written} series + index.csv + README.md written to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
