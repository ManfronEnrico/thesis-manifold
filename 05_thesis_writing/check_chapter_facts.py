#!/usr/bin/env python3
"""
Check thesis chapters against the results actually on disk.

WHY: the drafts were written 2026-03-21 and last substantively touched
2026-06-24. Everything measured since then -- the category scope, the panel
depth, the model benchmark, the split geometry, the SRQ4 experiment -- postdates
them. A chapter that quotes a superseded number reads exactly like one that
quotes a correct number, which is why this is a script and not a proofread.

It does NOT judge prose. It finds claims that contradict
`04_thesis_results/` and the feature matrices, and prints them with the current
value so a human can decide what the sentence should say.

Usage:
    python 05_thesis_writing/check_chapter_facts.py
    python 05_thesis_writing/check_chapter_facts.py --chapter ch6
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

_here = Path(__file__).resolve()
_root = next((p for p in _here.parents if (p / "PATHS.py").is_file()), None)
if _root is None:
    raise RuntimeError(f"PATHS.py not found above {_here}")
sys.path.insert(0, str(_root))
from PATHS import THESIS_RESULTS_SRQ1_DIR, get_category_engineered_bymonth_dir

DRAFTS = _root / "05_thesis_writing" / "sections-drafts"
CATEGORIES = {"CSD": "csd", "danskvand": "danskvand",
              "energidrikke": "energidrikke", "RTD": "rtd"}


def ground_truth() -> dict:
    """Read the facts a chapter could contradict, from the artefacts."""
    g = {"categories": sorted(CATEGORIES), "n_categories": len(CATEGORIES),
         "panel": {}, "brands": {}, "splits": {}, "wmape": {}}

    for cat, slug in CATEGORIES.items():
        f = get_category_engineered_bymonth_dir(cat) / f"{slug}_feature_matrix_h3.parquet"
        if not f.is_file():
            continue
        fm = pd.read_parquet(f)
        ym = (fm.period_year.astype(int) * 100 + fm.period_month.astype(int))
        g["panel"][cat] = {"months": int(ym.nunique()),
                           "first": int(ym.min()), "last": int(ym.max())}
        g["brands"][cat] = int(fm.brand.nunique())
        d = fm.dropna(subset=["log_sales_units", "lag_1", "lag_13"])
        g["splits"][cat] = {s: int(d[d.split == s].period_index.nunique())
                            for s in ("train", "val", "test")}

    # ACCURACY GROUND TRUTH: cv_metrics.csv, NOT tuned_metrics.csv.
    #
    # Corrected 2026-08-23. The checker previously read tuned_metrics.csv, which was
    # SUPERSEDED by the 100-trial expanding-window-CV run. Consequence: the tool was
    # validating chapters against a stale artefact and reporting stale figures as the
    # correction -- it flagged RTD 31.8% (the CURRENT best) as an error, telling the
    # author to write 33.6% (the OLD value). A fact-checker anchored to the wrong file
    # is worse than none, because its output carries authority.
    #
    # cv_metrics.csv holds two rows per model (tuned_for = wmape | medmape). Compare
    # like with like: take the WMAPE-tuned rows when ranking on WMAPE. Mixing regimes
    # would rank a medMAPE-tuned model on a metric it was not optimised for.
    cv = THESIS_RESULTS_SRQ1_DIR / "cv_metrics.csv"
    tm = THESIS_RESULTS_SRQ1_DIR / "tuned_metrics.csv"
    src = cv if cv.is_file() else tm
    if src.is_file():
        df = pd.read_csv(src)
        if "tuned_for" in df.columns:
            df = df[df.tuned_for == "wmape"]
        for cat in CATEGORIES:
            s = df[(df.category == cat) & df.test_wmape.notna()]
            if len(s):
                r = s.sort_values("test_wmape").iloc[0]
                g["wmape"][cat] = {"model": r["model"],
                                   "wmape": round(float(r.test_wmape), 1)}
        g["wmape_source"] = src.name
    return g


def build_checks(g: dict) -> list[tuple]:
    """(regex, severity, message) — each names what the text claims and what is true."""
    months = ", ".join(f"{c} {v['months']}" for c, v in sorted(g["panel"].items()))
    lo = min((v["months"] for v in g["panel"].values()), default=0)
    hi = max((v["months"] for v in g["panel"].values()), default=0)
    last = max((v["last"] for v in g["panel"].values()), default=0)

    checks = [
        # Scope. The single most repeated error: beer was dropped, but Ch1/Ch3/Ch5
        # still describe a five-category study.
        (r"\bfive (?:Nielsen )?(?:product )?categor",
         "ERROR",
         f"claims FIVE categories; the thesis runs {g['n_categories']} "
         f"({', '.join(g['categories'])}). Beer/totalbeer was scoped out."),
        (r"\btotalbeer\b|beer \(totalbeer\)",
         "CHECK",
         "mentions beer/totalbeer -- correct only where explaining why it was "
         "EXCLUDED, wrong wherever it is counted as a study category."),

        # Panel depth. Every category has grown since the drafts were written.
        (r"between 37 and 42 monthly|37 to 42 month",
         "ERROR",
         f"claims 37-42 months; current panel is {lo}-{hi} ({months})."),
        (r"March 2026|to 2026-03",
         "ERROR",
         f"claims the panel ends March 2026; it now ends "
         f"{str(last)[:4]}-{str(last)[4:]}."),

        # Superseded naming.
        (r"\bholiday_month\b",
         "ERROR",
         "uses holiday_month; renamed peak_month -- it flags above-average "
         "months and never consulted a holiday calendar."),
        (r"\bbychain\b|chain grain|chain-level grain",
         "ERROR",
         "refers to the chain grain; DEC-GRAIN locked the thesis to brand x "
         "month and the chain artefacts were deleted."),
        (r"\bopen-world\b",
         "CHECK",
         "uses 'open-world'; renamed DEC-DISCOVER-COLUMNS."),

        # Vendor.
        # Skipped in ai-declaration.md, where naming Claude is the POINT: it
        # discloses the tools used to write the thesis, which is a different
        # claim from which model the experiment runs on.
        (r"claude-sonnet|Claude Sonnet",
         "ERROR",
         "names Claude as the experiment's model; DEC-LLM and B-DEC-1 pin all "
         "SRQ4 scenarios to gpt-5.5-2026-04-23."),
        (r"\bE2B\b",
         "ERROR",
         "names E2B; Scenario B now runs in OpenAI's hosted Code Interpreter."),
        (r"System A|System B(?!\w)",
         "CHECK",
         "uses System A/B; the design is now three SCENARIOS -- A_plain, "
         "B_data, C_model -- and the lettering is reversed."),
        (r"LLM-as-[Jj]udge|GPT-4o",
         "ERROR",
         "describes an LLM judge; dropped (B-DEC-2). Every SRQ4 metric is "
         "programmatic."),
    ]

    # Benchmark figures: flag any stale WMAPE still in the prose.
    # Numbers that appear in chapter prose and are NO LONGER current. Keep this list
    # in sync with cv_metrics.csv -- an entry here that matches the current value
    # would flag correct text as an error (which is exactly what happened with RTD
    # 31.8% before 2026-08-23).
    stale = {"17.1": "CSD", "32.6": "danskvand", "16.5": "CSD",
             "23.8": "danskvand", "11.4": "energidrikke", "31.0": "RTD"}
    # The number alone is ambiguous: the same digits legitimately appear as another
    # category's figure, or in a different column (CV score vs test WMAPE). Require
    # the line to name the category the value is stale FOR, so a stale figure in its
    # own row still trips while a coincidental match elsewhere does not.
    for num, cat in stale.items():
        cur = g["wmape"].get(cat, {})
        if cur and abs(cur["wmape"] - float(num)) > 0.05:
            checks.append(
                (rf"(?i)\b{cat}\b.*\b{num}\s*%|\b{num}\s*%.*(?i:\b{cat}\b)",
                 "ERROR",
                 f"quotes {num}% on a line naming {cat}; re-tuning on the post-EDA "
                 f"matrices gives {cur['wmape']}% ({cur['model']})."))
    return checks


def scan(path: Path, checks) -> list[tuple]:
    hits = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for pat, sev, msg in checks:
            if re.search(pat, line):
                hits.append((i, sev, msg, line.strip()[:110]))
    return hits


def main():
    ap = argparse.ArgumentParser(description="Check chapters against results on disk")
    ap.add_argument("--chapter", default=None, help="e.g. ch6 (default: all)")
    ap.add_argument("--errors-only", action="store_true")
    a = ap.parse_args()

    g = ground_truth()
    checks = build_checks(g)

    print("=" * 78)
    print("GROUND TRUTH (read from disk just now)")
    print("=" * 78)
    print(f"  categories : {g['n_categories']} -- {', '.join(g['categories'])}")
    for cat, v in sorted(g["panel"].items()):
        sp = g["splits"].get(cat, {})
        w = g["wmape"].get(cat, {})
        print(f"  {cat:13s} {v['months']:2d} months "
              f"({str(v['first'])[:4]}-{str(v['first'])[4:]} to "
              f"{str(v['last'])[:4]}-{str(v['last'])[4:]}), "
              f"{g['brands'].get(cat, 0):3d} brands, "
              f"split {sp.get('train')}/{sp.get('val')}/{sp.get('test')}, "
              f"best {w.get('model','?')} {w.get('wmape','?')}%")

    files = sorted(DRAFTS.glob(f"{a.chapter}*.md" if a.chapter else "*.md"))
    # The AI declaration names tools deliberately; vendor checks do not apply.
    vendor_pats = {"claude-sonnet|Claude Sonnet"}
    total_e = total_c = 0
    for f in files:
        active = ([c for c in checks if c[0] not in vendor_pats]
                  if f.name == "ai-declaration.md" else checks)
        hits = scan(f, active)
        if a.errors_only:
            hits = [h for h in hits if h[1] == "ERROR"]
        if not hits:
            continue
        print("\n" + "=" * 78)
        print(f"{f.name}  --  {len(hits)} item(s)")
        print("=" * 78)
        for ln, sev, msg, txt in hits:
            total_e += sev == "ERROR"
            total_c += sev == "CHECK"
            print(f"\n  [{sev}] line {ln}: {msg}")
            print(f"         > {txt}")

    print("\n" + "=" * 78)
    print(f"{total_e} ERROR (contradicts the artefacts), "
          f"{total_c} CHECK (may be correct in context)")
    print("Nothing here judges prose quality -- only whether a claim matches the data.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
