#!/usr/bin/env python
"""Literature review summary table: what each strand established, and what it changed.

WHY THIS IS A SEPARATE GENERATOR
--------------------------------
Every other artefact in this tier is derived from measured data. This one is not,
and pretending otherwise would be the exact failure P0046 exists to prevent. It
has two halves with different provenance, and the table marks the boundary:

  * PARSED from ch2-literature-review.md -- the section titles, their
    `*Maps to ...*` SRQ mapping, and their `**Claims**` bullets. These cannot
    drift: if a section is renamed, re-mapped or re-argued, re-running this
    picks the change up.

  * CURATED here -- the "design consequence" column, i.e. what the strand
    actually changed in the build. That link lives in our heads and in the
    prose; there is no artefact to read it from. It is therefore stated
    explicitly, one entry per section, and each entry names a concrete,
    checkable feature of the repository rather than a generality.

If a curated row cannot name something in the code, it does not belong in the
table -- that is the test applied when writing them.

Output: 05_thesis_results/appendix/, as .md + .csv, matching export_appendix.py's
conventions (no table numbers, review notes below a horizontal rule).
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

for _c in (Path(__file__).resolve().parent, *Path(__file__).resolve().parents):
    if any((_c / a).exists() for a in (".env.example", ".env", "PATHS.py")):
        sys.path.insert(0, str(_c))
        break

from PATHS import (THESIS_WRITING_DRAFTS_DIR,
                   get_chapter_tables_dir)

# Ch2: the map from each strand of the literature to the design decision it
# informed. It is parsed from the literature chapter, and read beside it.
OUT = get_chapter_tables_dir("literature_review")
CH2 = THESIS_WRITING_DRAFTS_DIR / "ch2-literature-review.md"

# The curated half: what each strand changed in the build. Keyed by section
# number so a renamed section still matches, and every value names something
# that can be opened and checked.
DESIGN_CONSEQUENCE = {
    "2.1": "Fixed the model ladder to gradient-boosted trees over engineered "
           "lag/rolling features (srq1_benchmark.py) and the grain to brand x "
           "month; ARIMA and Prophet are carried as statistical baselines, not "
           "ladder members (srq1_baselines_stat.py).",
    "2.2": "Made peak fit RSS a reported metric alongside error, profiled per "
           "model (srq1_profiling.py, profiling.csv), and set the 4096 MB "
           "envelope as a selection constraint. Ruled out locally-hosted LLM "
           "inference: the LLM is called over an API, out of process.",
    "2.3": "Motivated the SRQ4 comparison as open-ended decision support rather "
           "than a tight predict-then-optimise loop: scenarios answer a "
           "managerial question and are scored on correctness, consistency and "
           "replicability (srq4_experiment.py).",
    "2.4": "Shaped the tool as a typed call the agent invokes with an "
           "identifier and a horizon -- feature construction stays server-side "
           "and the LLM never handles feature vectors (forecast_tool.py).",
    "2.5": "Attached a calibrated 90% interval by split conformal prediction "
           "and a confidence tier to every forecast, and logged each call with "
           "its model, training cutoff and calibration rows "
           "(srq1_calibration.py, forecast_log.jsonl).",
    "2.6": "Framed SRQ3 as a readiness assessment grounded in a working "
           "integration rather than a completed deployment: the SRQ2 tool is "
           "registered with and executed inside the production system as part "
           "of the SRQ4 runs.",
    "2.7": "Set the four contributions and their status (designed / built / "
           "assessed), which is what the results tier is organised around.",
    "2.8": "Adopted design science as the frame: build an artefact, then "
           "evaluate it -- the structure of the modelling, tool and scenario "
           "tiers.",
}


def _sections(text: str) -> list[dict]:
    """Parse ch2's numbered sections, their SRQ mapping and their claim bullets."""
    out = []
    # Split on the section headings, keeping the heading with its body.
    parts = re.split(r"^## (2\.\d+)\s+(.+?)$", text, flags=re.M)
    # parts = [preamble, num, title, body, num, title, body, ...]
    for i in range(1, len(parts) - 2, 3):
        num, title, body = parts[i], parts[i + 1].strip(), parts[i + 2]

        mapped = ""
        if (m := re.search(r"^\*Maps to (.+?)\*\s*$", body, flags=re.M)):
            mapped = m.group(1).strip()

        # Claims run from the **Claims** marker to the next bold marker.
        # A claim bullet wraps across lines, so continuation lines (indented,
        # not starting a new bullet) must be joined before the markup is
        # stripped -- otherwise a claim is cut mid-sentence and, worse, a bold
        # span opened on one line and closed on the next survives as a stray
        # "**" in the table.
        claims = []
        if (m := re.search(r"\*\*Claims\*\*(.*?)(?=\n\*\*|\n## |\Z)", body, flags=re.S)):
            buf: list[str] = []
            def _flush():
                if not buf:
                    return
                c = " ".join(buf)
                c = re.sub(r"\*\*(.+?)\*\*", r"\1", c, flags=re.S)
                c = re.sub(r"\*(.+?)\*", r"\1", c, flags=re.S)
                c = re.sub(r"[*_`]", "", c)          # any unpaired leftovers
                c = re.sub(r"\s+", " ", c).strip()
                # A claim followed by an enumerated sub-list absorbs the first
                # ordinal ("... well populated 1"); drop a trailing bare number.
                c = re.sub(r"\s+\d+\.?$", "", c)
                if c:
                    claims.append(c)
                buf.clear()

            for line in m.group(1).splitlines():
                if re.match(r"^\s*-\s", line):       # a new bullet at any depth
                    _flush()
                    buf.append(re.sub(r"^\s*-\s", "", line).strip())
                elif line.strip() and buf:           # continuation of the current one
                    buf.append(line.strip())
                elif not line.strip():
                    _flush()
            _flush()
        out.append({"num": num, "title": title, "maps_to": mapped,
                    "claims": claims})
    return out


def _shorten(s: str, n: int = 210) -> str:
    """Trim to the first sentence(s) that fit, so a cell stays readable."""
    s = s.strip().rstrip(".")
    if len(s) <= n:
        return s
    cut = s[:n]
    if (dot := cut.rfind(". ")) > n * 0.5:
        return cut[:dot]
    return cut[:cut.rfind(" ")] + " ..."


def main() -> None:
    if not CH2.is_file():
        raise SystemExit(f"missing {CH2}")
    # 2.0 and 2.9 are the chapter's own introduction and transition, not
    # literature strands: they have no SRQ mapping and produced no design
    # decision, so they are excluded rather than carried as empty rows.
    SKIP = {"2.0", "2.9"}
    secs = [s for s in _sections(CH2.read_text(encoding="utf-8"))
            if s["num"] not in SKIP and (s["claims"] or s["num"] in DESIGN_CONSEQUENCE)]
    if not secs:
        raise SystemExit("parsed no sections from ch2 -- has its structure changed?")

    rows = []
    for s in secs:
        # The lead claim is the strand's headline finding; the rest are support.
        lead = _shorten(s["claims"][0]) if s["claims"] else ""
        rows.append({
            "Section": s["num"],
            "Literature strand": s["title"],
            "Informs": s["maps_to"] or "--",
            "Principal insight": lead,
            "Consequence for the design": DESIGN_CONSEQUENCE.get(
                s["num"], "[not yet mapped]"),
        })

    OUT.mkdir(parents=True, exist_ok=True)
    stem = "89_literature_design_map"
    with (OUT / f"{stem}.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    hdr = list(rows[0])
    md = ["**Literature review: principal insights and their consequence for the "
          "design.** Each strand of the review, the research question it informs, "
          "its principal insight, and the specific design decision it produced.",
          "",
          "| " + " | ".join(hdr) + " |",
          "|" + "|".join("---" for _ in hdr) + "|"]
    for r in rows:
        md.append("| " + " | ".join(str(r[h]).replace("|", "\\|") for h in hdr) + " |")

    unmapped = [r["Section"] for r in rows
                if r["Consequence for the design"] == "[not yet mapped]"]
    md += ["", "*Note.* The section, its research-question mapping and its "
               "principal insight are read from the literature review itself, so "
               "they cannot fall out of step with the chapter. The final column "
               "is a curated statement of what each strand changed in the build; "
               "each entry names a component that can be inspected in the "
               "repository.",
           "\n---\n\n<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->\n",
           f"Generated by `generate_literature_table.py` from "
           f"`{CH2.name}` ({len(rows)} sections parsed). Re-run after editing "
           "Ch2. The 'Consequence for the design' column is CURATED, not "
           "derived -- it is the one column a chapter edit will not update, so "
           "check it when the design changes."]
    if unmapped:
        md.append(f"\n**{len(unmapped)} section(s) have no design consequence "
                  f"recorded: {', '.join(unmapped)}.** Add them to "
                  "DESIGN_CONSEQUENCE or drop the row.")
    (OUT / f"{stem}.md").write_text("\n".join(md) + "\n", encoding="utf-8",
                                    newline="\n")

    print(f"  {stem:42s} {len(rows):>4d} rows  Literature -> design map")
    for r in rows:
        print(f"      {r['Section']:5s} {r['Informs']:28s} {r['Literature strand'][:44]}")
    if unmapped:
        print(f"\n  WARNING: no design consequence for {unmapped}")
    print(f"\n  -> {OUT / f'{stem}.md'}")


if __name__ == "__main__":
    main()
