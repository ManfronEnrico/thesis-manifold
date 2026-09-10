#!/usr/bin/env python
"""
Appendix tables documenting the DK public-holiday enrichment.

WHY THIS EXISTS AS A GENERATOR
------------------------------
Per DEC-P0046-PATHS every artefact that could enter the thesis must be produced
by a script under version control, resolving its output through PATHS.py. A
hand-pasted table of holiday counts would be exactly the undefendable artefact
P0046 exists to eliminate: nobody could say which fetch produced it.

ROUTING (DEC-P0046-ROUTING)
---------------------------
This lives beside its producer -- the holiday fetch, in SRQ1's raw tier, since
the enrichment feeds SRQ1's models -- and writes into the results tier, which
per DEC-P0046-SINGLE-HOME is where artefacts live exactly once. Tier 06
(writing) receives nothing.

CONVENTIONS (F7, matching export_appendix.py)
---------------------------------------------
  - .md and .csv twins from the same DataFrame, so they cannot disagree
  - no hard-coded numbers: every value derives from the cache on disk
  - units in the column headers
  - an <!-- INTERNAL REVIEW --> separator below which nothing is for submission
  - the filename carries the sequence number; the content carries none, because
    numbering inside the document is Word's job

USAGE
    python export_holiday_appendix.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


def _find_repo_root() -> Path:
    """Anchor on .env.example per DEC-P0046-ANCHOR -- never CLAUDE.md, never
    cwd, never a parents[N] hop (hop counts encode folder depth, which the
    2026-09-06 restructure changed)."""
    start = Path(__file__).resolve().parent
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


_REPO_ROOT = _find_repo_root()
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from PATHS import get_chapter_tables_dir  # noqa: E402

sys.path.insert(0, str(_REPO_ROOT / "05_thesis_results"))
from review_notes import write_review_note  # noqa: E402
from check_reader_facing import warn_after_run  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_holidays import CACHE_DIR, MANIFEST_PATH, load_manifest  # noqa: E402

# Ch4: these describe the calendar SOURCE -- how the holiday data was obtained
# and shaped. The ablation RESULTS that use it are Ch5, and are written by
# srq1_export_enrichment_appendix.py. Same subject, two chapters, on purpose.
OUT = get_chapter_tables_dir("data_assessment")
# Review notes go BESIDE the table, not INSIDE it: 05_thesis_results/ ships to
# assessors, so an internal note appended below a table travelled with the
# thesis. They are written to 06_thesis_writing/writing-notes/, which the
# submission export removes.
_PRODUCER = "01_SRQ1_Model_Training/01_thesis_data/_00_raw/holidays/export_holiday_appendix.py"

# Continues export_appendix.py's sequence. Holiday tables are appendix material
# for SRQ1's feature set, so they sort after the SRQ4 run tables rather than
# renumbering them.
SEQ_START = 90


def _emit(seq: int, slug: str, title: str, caption: str, df: pd.DataFrame,
          note: str = "", review: str = "") -> None:
    """Write one table as .md + .csv twins. Mirrors export_appendix.py._emit."""
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{seq:02d}_{slug}"
    df.to_csv(OUT / f"{stem}.csv", index=False, encoding="utf-8")

    lines = [f"**{title}.** {caption}", "", df.to_markdown(index=False)]
    if note:
        lines += ["", f"*Note.* {note}"]
    (OUT / f"{stem}.md").write_text("\n".join(lines) + "\n",
                                    encoding="utf-8", newline="\n")
    write_review_note(slug, OUT / f"{stem}.md", title, review, _PRODUCER)
    print(f"  {stem:42s} {len(df):>4d} rows  {title}")


def _load_all_holidays() -> pd.DataFrame:
    """Every cached holiday as one long frame."""
    rows = []
    for path in sorted(CACHE_DIR.glob("dk_*.json")):
        for h in json.loads(path.read_text(encoding="utf-8")):
            rows.append({
                "date": h["date"],
                "local_name": h.get("localName"),
                "name": h.get("name"),
                "fixed": h.get("fixed"),
                "global": h.get("global"),
            })
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df.sort_values("date").reset_index(drop=True)


def table_provenance(manifest: dict) -> None:
    """The source record. This is what makes the enrichment citable."""
    df = pd.DataFrame([
        {"Field": "Source", "Value": manifest["source"]},
        {"Field": "Endpoint", "Value": manifest["url_template"]},
        {"Field": "Country code", "Value": manifest["country"]},
        {"Field": "Retrieved (UTC)", "Value": manifest["fetched_utc"]},
        {"Field": "Years covered", "Value":
            f"{min(manifest['years_covered'])}-{max(manifest['years_covered'])}"},
        {"Field": "Holiday-days retrieved (n)", "Value":
            str(sum(y["n_holidays"] for y in manifest["years"].values()))},
        {"Field": "Access", "Value": "Public tier, no API key"},
    ])
    _emit(
        SEQ_START, "holiday_source_provenance",
        "DK public-holiday data source",
        "Provenance of the calendar used to construct the holiday features.",
        df,
        note=("Retrieved from the free public tier. The commercial "
              "nagerholidays.com/api/pro/ paths require a key and return HTTP 401 "
              "without one."),
        review=(f"Cache: `{CACHE_DIR}`\nManifest: `{MANIFEST_PATH}`\n\n"
                "Per-year sha256 digests in the manifest detect an upstream "
                "revision on re-pull. Regenerate with `fetch_holidays.py --force`."),
    )


def table_annual_counts(hol: pd.DataFrame) -> None:
    """The Store Bededag break, which is the case for the feature."""
    df = (hol.groupby("year").size().reset_index(name="Holiday-days (n)")
             .rename(columns={"year": "Year"}))
    _emit(
        SEQ_START + 1, "holiday_annual_counts",
        "Danish public holiday-days per year",
        "Annual count of public holiday-days, showing the 2024 structural break.",
        df,
        note=("The count falls from 15 to 14 in 2024 when Store Bededag (Great "
              "Prayer Day) was abolished. A month-of-year encoding cannot "
              "represent a one-off permanent change, which is the primary "
              "motivation for the count feature."),
        review=("Verify against Danish legislation: Store Bededag abolished "
                "effective 2024 (L 13, adopted 2023-02-28)."),
    )


def table_monthly_matrix(hol: pd.DataFrame) -> None:
    """Month x year, which makes the Easter movement visible at a glance."""
    pivot = (hol.pivot_table(index="month", columns="year", values="date",
                             aggfunc="count", fill_value=0)
                .astype(int).reset_index().rename(columns={"month": "Month"}))
    pivot.columns = [str(c) for c in pivot.columns]
    _emit(
        SEQ_START + 2, "holiday_monthly_matrix",
        "Public holiday-days by calendar month and year",
        "Holiday-days per month, demonstrating within-month variation across years.",
        pivot,
        note=("March and April vary inversely as Easter moves between them; "
              "May falls by one from 2024. Because the same calendar month "
              "takes different values in different years, this variation is not "
              "expressible by the month, quarter or peak_month features."),
        review=("This table is the evidence that n_holidays is not a "
                "re-encoding of month-of-year. Cite it wherever the enrichment "
                "is defended against that objection."),
    )


def table_feature_definitions() -> None:
    """What was actually built, in the words the code uses."""
    df = pd.DataFrame([
        {"Feature": "days_in_month", "Definition": "Calendar days in the month",
         "Unit": "days", "Source": "Calendar"},
        {"Feature": "n_holidays",
         "Definition": "Public holiday-days falling in the month",
         "Unit": "days", "Source": "Nager.Date"},
        {"Feature": "non_holiday_days",
         "Definition": "days_in_month minus n_holidays",
         "Unit": "days", "Source": "Derived"},
    ])
    _emit(
        SEQ_START + 3, "holiday_feature_definitions",
        "Holiday-derived features",
        "Definitions of the three calendar features added to the feature matrix.",
        df,
        note=("`non_holiday_days` is named for what it computes and asserts "
              "nothing about trading. Danish retail is open at weekends "
              "(Lukkeloven liberalised 2012) and many stores open on public "
              "holidays with reduced hours, so the column is a proxy for "
              "trading exposure, not a measurement of it."),
        review=("Naming follows the 2026-08-18 holiday_months -> peak_months "
                "precedent: a feature name must not assert a cause the "
                "computation never established. Earlier drafts of this work "
                "used `selling_days` and `trading_days`; both were rejected.\n\n"
                "Missing-value rule: a panel month inside the fetched range "
                "with no holidays is 0 (a measurement); a month outside it is "
                "NaN (unknown), never 0."),
    )


def main() -> int:
    manifest = load_manifest()
    if manifest is None:
        print("No holiday cache. Run fetch_holidays.py first.")
        return 1

    hol = _load_all_holidays()
    print(f"Writing holiday appendix tables -> {OUT}")

    table_provenance(manifest)
    table_annual_counts(hol)
    table_monthly_matrix(hol)
    table_feature_definitions()

    print(f"\n4 tables written ({len(hol)} holiday-days, "
          f"{hol['year'].nunique()} years).")
    warn_after_run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
