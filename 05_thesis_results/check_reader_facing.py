"""Fail when generated output carries content only the authors should read.

WHY THIS EXISTS
---------------
Tiers 01-05 are read by assessors. Nothing student-facing may appear in them --
plan IDs, internal decision codes, finding numbers, notes to ourselves about
what a number means, or paths into the parts of the repo that do not ship.

An earlier pass enforced this by searching for an `<!-- INTERNAL REVIEW -->`
marker and moving what sat below it. That found the notes which were honest
about being notes, and missed nine lines of ordinary-looking prose that happened
to cite a plan file -- a marker is a SYMPTOM of internal content, not its
definition.

It also relied on somebody remembering to look, which is exactly what failed. So
this runs as a check instead: `python 05_thesis_results/check_reader_facing.py`,
exit 1 on any hit.

WHAT IT DELIBERATELY DOES NOT COVER
-----------------------------------
Source comments. A plan ID in a `#` comment is a note to a developer reading the
code, which is a different audience and a different question; those are handled
by the comment pass. This checks EMITTED text only -- the .md and .csv files a
reader opens.

`.archive/` folders are skipped: they hold superseded artefacts kept as evidence
of a decision, and their READMEs exist precisely to say which plan retired them.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


sys.path.insert(0, str(_find_repo_root(Path(__file__).resolve().parent)))
from PATHS import ROOT_DIR, THESIS_RESULTS_DIR  # noqa: E402

# Each pattern names the failure it catches, so a hit explains itself.
PATTERNS: list[tuple[str, str]] = [
    (r"\bP\d{4}\b", "plan ID"),
    (r"\bDEC-[A-Z][A-Z0-9-]+", "internal decision code"),
    (r"\bF\d{1,3}\b(?!\s*[-–]?\s*\d)", "finding number"),
    (r"(?i)\bnot for submission\b", "submission marker"),
    (r"(?i)\bdo not publish\b", "submission marker"),
    (r"(?i)\bfor our own review\b", "note to the authors"),
    (r"(?i)\binternal review\b", "internal-review marker"),
    (r"06_thesis_writing/", "path into the non-shipping tree"),
    (r"\bwriting-notes\b", "path into the non-shipping tree"),
    (r"(?i)\bBrian\b|\bEnrico\b", "author name"),
]

# Files a reader opens. Scripts are checked by the comment pass, not here.
SUFFIXES = {".md", ".csv"}


def _iter_files(root: Path):
    for p in sorted(root.rglob("*")):
        if p.suffix.lower() not in SUFFIXES or not p.is_file():
            continue
        if any(part.startswith(".") for part in p.relative_to(root).parts[:-1]):
            continue  # .archive/ and friends -- superseded, kept as evidence
        yield p


def scan(root: Path = THESIS_RESULTS_DIR) -> list[tuple[Path, int, str, str]]:
    """Every (file, line number, what it is, the line) that must not ship."""
    hits: list[tuple[Path, int, str, str]] = []
    for f in _iter_files(root):
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for pat, what in PATTERNS:
                if re.search(pat, line):
                    hits.append((f, n, what, line.strip()))
                    break
    return hits


def warn_after_run(root: Path = THESIS_RESULTS_DIR) -> int:
    """Print a warning for any non-reader-facing line. Returns the hit count.

    Called at the end of a producer so the check runs without being remembered.
    It warns rather than raising: a generator that has just written 15 correct
    tables should not exit non-zero over a sentence, and the run that finds the
    problem is rarely the run that introduced it. The standalone check is the
    one that fails.
    """
    hits = scan(root)
    if hits:
        print(f"\n  WARNING: {len(hits)} line(s) not reader-facing "
              f"(run check_reader_facing.py for the list).")
    return len(hits)


def main() -> int:
    hits = scan()
    if not hits:
        n = sum(1 for _ in _iter_files(THESIS_RESULTS_DIR))
        print(f"OK -- {n} generated files carry only reader-facing content.")
        return 0

    print(f"{len(hits)} line(s) in the results tree are not reader-facing:\n")
    for f, n, what, line in hits:
        rel = f.relative_to(ROOT_DIR).as_posix()
        print(f"  {rel}:{n}")
        print(f"      {what}: {line[:110]}")
    print("\nFix each AT ITS PRODUCER, not in the output file -- the next run "
          "would put it back. Keep the reasoning, drop the citation: a plan ID "
          "points at a file the reader does not have, but the sentence around "
          "it is usually a real methodological point. Where the reasoning is "
          "genuinely internal, move it to the chapter's writing note.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
