"""Editorial notes for generated tables and figures, filed by chapter.

WHY THIS EXISTS
---------------
Generated tables under `05_thesis_results/` used to carry two audiences in one
file: submission-ready caption and table above an `<!-- INTERNAL REVIEW -->`
marker, notes for Brian and Enrico below it. The reasoning was that a note
belongs beside the table it describes, and that a screenshot cropped to the
table cannot capture what sits below a horizontal rule.

That reasoning covers screenshots and misses the repository. Tiers 01-05 are
read by assessors, so every internal note in them travels with the thesis --
staleness flags, plan IDs, "an earlier draft claimed", and our own arguments
with ourselves about what a number means.

The rule is about CONTENT, not about which tree an export happens to delete:
**nothing student-facing appears anywhere in tiers 01-05**, marked or unmarked.
A marker is a symptom of internal content, not its definition -- searching for
one finds the notes that were honest about being notes, and misses a sentence
that reads as ordinary prose and happens to cite a plan file.

So the split is by FILE. The table is submission-ready in full; the note lives
under `06_thesis_writing/writing-notes/`, and names its table so the two are
findable from each other.

WHY NOTES ARE FILED BY CHAPTER
------------------------------
A note exists to help finish a CHAPTER, so it belongs beside the other notes for
that chapter rather than in a directory grouped by which script wrote it.
Grouping by producer serves the producer; grouping by chapter serves the person
writing.

The chapter is derived from the artefact's own output path (see chapter_of), not
passed in, so a producer cannot file a table in one chapter and its note in
another, and a re-routed table takes its note with it.

Notes land in a `generated/` subfolder of the chapter's note folder, so a
regenerated note can never overwrite something a human wrote.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    for cand in (start, *start.parents):
        if any((cand / a).exists() for a in (".env.example", ".env", "PATHS.py")):
            return cand
    raise FileNotFoundError(f"Could not find project root above {start}")


sys.path.insert(0, str(_find_repo_root(Path(__file__).resolve().parent)))
from PATHS import (  # noqa: E402
    CHAPTER_ORDER,
    ROOT_DIR,
    THESIS_RESULTS_DIR,
    get_chapter_generated_notes_dir,
)

_HEADER = (
    "<!-- GENERATED -- do not hand-edit; rewritten by the artefact's producer. -->\n"
    "<!-- NOT FOR SUBMISSION. Editorial notes for Brian and Enrico. Tiers 01-05 "
    "carry only what a thesis reader should see, which is why this lives here "
    "and not beside the artefact it describes. -->\n"
)


def chapter_of(artefact_path: Path) -> str:
    """The chapter slug owning an artefact, read from its own output path.

    Every generated artefact lands under `05_thesis_results/{NN}_{slug}/`, so
    the path already states which chapter it belongs to. Deriving the note's
    destination from it means a producer cannot file a table in one chapter and
    its note in another, and a re-routed table takes its note along.

    Raises rather than guessing: a note whose chapter cannot be established is a
    note nobody will find.
    """
    p = Path(artefact_path)
    if not p.is_absolute():
        p = ROOT_DIR / p
    try:
        parts = p.resolve().relative_to(THESIS_RESULTS_DIR.resolve()).parts
    except ValueError:
        raise ValueError(
            f"{artefact_path} is not under {THESIS_RESULTS_DIR}, so its chapter "
            "cannot be derived. Generated artefacts belong in the results tree."
        ) from None

    # "{NN}_{slug}" -- strip the derived number prefix and keep the subject.
    head = parts[0] if parts else ""
    slug = head.split("_", 1)[1] if "_" in head else head
    if slug not in CHAPTER_ORDER:
        raise ValueError(
            f"{artefact_path} sits under {head!r}, which is not a chapter "
            "folder. Expected 05_thesis_results/{NN}_{chapter-slug}/...")
    return slug


def write_review_note(slug: str, table_path: Path, title: str,
                      review: str, producer: str) -> Path | None:
    """Write one table's editorial note, or clear a stale one.

    The note is filed under the chapter that owns the table, derived from
    `table_path` -- see chapter_of.

    Returns the note path when written, None when the table has no review text
    (in which case any previous note for that slug is removed, so a note cannot
    outlive the reasoning that produced it).
    """
    dst_dir = get_chapter_generated_notes_dir(chapter_of(table_path))
    dst = dst_dir / f"{slug}.md"

    if not review or not review.strip():
        if dst.exists():
            dst.unlink()
        return None

    dst_dir.mkdir(parents=True, exist_ok=True)

    try:
        rel = table_path.relative_to(ROOT_DIR).as_posix()
    except ValueError:
        rel = table_path.as_posix()

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = (
        f"{_HEADER}\n"
        f"# {title}\n\n"
        f"| | |\n|---|---|\n"
        f"| Table | `{rel}` |\n"
        f"| Producer | `{producer}` |\n"
        f"| Written | {stamp} |\n\n"
        f"---\n\n"
        f"{review.strip()}\n"
    )
    dst.write_text(body, encoding="utf-8", newline="\n")
    return dst


def clear_review_notes(slug_to_chapter) -> int:
    """Remove notes for a producer's tables before a regeneration run.

    Takes the producer's own slug -> chapter-slug mapping, so it looks in the
    chapter folder each note was filed under and matches on slug. It therefore
    cannot reach a note another producer owns, and cannot touch a hand-written
    note, which never lives in the `generated/` subfolder.
    """
    removed = 0
    for slug, chapter in dict(slug_to_chapter).items():
        f = get_chapter_generated_notes_dir(chapter) / f"{slug}.md"
        if f.exists():
            try:
                f.unlink()
                removed += 1
            except OSError:
                continue
    return removed
