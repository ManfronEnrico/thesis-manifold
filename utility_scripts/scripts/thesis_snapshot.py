#!/usr/bin/env python3
"""
Snapshot the shared thesis .docx into this repo, as a diffable record.

WHY THIS EXISTS
---------------
The authoritative thesis prose lives in a Word document in OneDrive, shared with
Enrico. This repo lives on an external SSD. Neither can move:

  - The .docx must stay in OneDrive or it stops being shared.
  - A git repo must NOT be hosted inside OneDrive. Tooling issue #1 in
    .claude/logs/tooling-issues.jsonl documents sync races corrupting files
    mid-write on this very project; a .git directory is that failure mode with
    worse consequences, and two machines syncing one .git produce conflicts git
    cannot resolve.

And committing the .docx alone would not help: it is a zip of compressed XML, so
every save rewrites the bytes wholesale and git reports only "binary files
differ". You would get history, never a readable diff.

So: copy the .docx in as a dated artifact (history), AND extract its text to
markdown beside it (the diff). Splitting on Heading 1 gives per-chapter files,
which is the granularity that makes drift locatable -- "ch2 lost 1,316 words" is
actionable, "the thesis differs" is not.

WHAT IT WRITES
--------------
    05_thesis_writing/snapshots/YYYY-MM-DD/
        thesis_full.docx          verbatim copy of the source
        thesis_full.md            whole-document text
        chapters/ch3-methodology.md   one file per Heading 1
        comments.md               every Word comment + the text it is anchored to
        MANIFEST.md               what was captured, and the drift table

THE SNAPSHOT IS READ-ONLY. Never edit a file under snapshots/ and never convert
one back. Editing them creates a fourth version of the thesis and reintroduces
exactly the ambiguity the snapshot exists to remove. The working surfaces are
05_thesis_writing/sections-drafts/*.md (live) and the OneDrive .docx (prose).

Usage:
    python utility_scripts/scripts/thesis_snapshot.py
    python utility_scripts/scripts/thesis_snapshot.py --source "C:/path/to.docx"
    python utility_scripts/scripts/thesis_snapshot.py --no-drift
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
W15 = "{http://schemas.microsoft.com/office/word/2012/wordml}"
W14 = "{http://schemas.microsoft.com/office/word/2010/wordml}"

# The shared review copy. Overridable with --source; kept here so the common
# case is a bare invocation.
DEFAULT_SOURCE = (
    r"C:\Users\brian\OneDrive\Documents\02-Areas\MSc. Data Science"
    r"\2026-03 - CBS Master Thesis\Drafts"
    r"\MSc. Data Science - 175888 and 176171 - Master Thesis.docx"
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SNAP_ROOT = REPO_ROOT / "05_thesis_writing" / "snapshots"
DRAFTS = REPO_ROOT / "05_thesis_writing" / "sections-drafts"

# Heading 1 text -> the sections-drafts basename it should be compared against.
# An explicit map, not string-similarity guessing: a wrong pairing would report
# drift between two unrelated chapters, which is worse than reporting none.
CHAPTER_MAP = {
    "chapter 1": "ch1-introduction",
    "chapter 2": "ch2-literature-review",
    "chapter 3": "ch3-methodology",
    "chapter 4": "ch4-data-assessment",
    "chapter 5": "ch5-framework-design",
    "chapter 6": "ch6-model-benchmark",
    "chapter 7": "ch7-decision-synthesis",
    "chapter 8": "ch8-experimental-evaluation",
    "chapter 9": "ch9-discussion",
    "chapter 10": "ch10-conclusion",
    "abstract": "abstract",
}

# Styles that mark a chapter break. Word's built-in Heading 1 is `Heading1`;
# a document using custom styles or outline levels would need this extended,
# which is why _split reports what it found and refuses to emit one giant file.
H1_STYLES = {"Heading1", "heading1", "Heading 1"}
HEADING_STYLES = {"Heading1": 1, "Heading2": 2, "Heading3": 3,
                  "Heading4": 4, "Heading5": 5}


def _style(para) -> str | None:
    pr = para.find(f"{W}pPr")
    if pr is None:
        return None
    s = pr.find(f"{W}pStyle")
    return s.get(f"{W}val") if s is not None else None


def _text(el) -> str:
    """All w:t descendants, with tabs and breaks rendered as whitespace."""
    out = []
    for n in el.iter():
        if n.tag == f"{W}t":
            out.append(n.text or "")
        elif n.tag == f"{W}tab":
            out.append("\t")
        elif n.tag in (f"{W}br", f"{W}cr"):
            out.append("\n")
    return "".join(out)


def _slug(title: str) -> str:
    """Map a Heading 1 to a draft basename via CHAPTER_MAP, else a safe slug.

    Longest key first, and the match must end at a non-digit. Both guards are
    needed: plain `startswith` maps "Chapter 10 - Conclusion" to `ch1-...`
    because "chapter 1" is a prefix of "chapter 10", which silently overwrites
    ch1's file with ch10's text and reports a nonsense -2,733 word drift.
    """
    low = title.lower().strip()
    for key in sorted(CHAPTER_MAP, key=len, reverse=True):
        if low.startswith(key):
            rest = low[len(key):]
            if rest[:1].isdigit():      # "chapter 1" vs "chapter 10"
                continue
            return CHAPTER_MAP[key]
    s = re.sub(r"[^a-z0-9]+", "-", low).strip("-")
    return s[:60] or "untitled"


def read_docx(path: Path) -> dict:
    """Parse a .docx into paragraphs, chapters and comments. Stdlib only.

    python-docx is deliberately not used: it has no comment API at all, so the
    XML would have to be read directly regardless -- through a heavier dep.
    """
    z = zipfile.ZipFile(path)
    names = set(z.namelist())

    # --- comments -------------------------------------------------------
    comments: dict[str, dict] = {}
    if "word/comments.xml" in names:
        for c in ET.fromstring(z.read("word/comments.xml")).findall(f"{W}comment"):
            cid = c.get(f"{W}id")
            para_ids = [p.get(f"{W14}paraId") for p in c.iter(f"{W}p")
                        if p.get(f"{W14}paraId")]
            comments[cid] = {
                "id": cid,
                "author": c.get(f"{W}author") or "",
                "date": (c.get(f"{W}date") or "")[:19],
                "text": _text(c).strip(),
                "para_ids": para_ids,
                "anchor": "", "chapter": "", "heading_path": "",
                "resolved": False, "is_reply": False,
            }

    # Resolved status and reply threading live in a separate part that only
    # Word writes -- generator-produced .docx lack it entirely.
    if "word/commentsExtended.xml" in names:
        done_by_para, parent_by_para = {}, {}
        for ce in ET.fromstring(z.read("word/commentsExtended.xml")).iter(f"{W15}commentEx"):
            pid = ce.get(f"{W15}paraId")
            if pid is None:
                continue
            done_by_para[pid] = (ce.get(f"{W15}done") in ("1", "true"))
            if ce.get(f"{W15}paraIdParent"):
                parent_by_para[pid] = ce.get(f"{W15}paraIdParent")
        for c in comments.values():
            for pid in c["para_ids"]:
                if pid in done_by_para:
                    c["resolved"] = done_by_para[pid]
                if pid in parent_by_para:
                    c["is_reply"] = True

    # --- body walk ------------------------------------------------------
    doc = ET.fromstring(z.read("word/document.xml"))
    body = doc.find(f"{W}body")

    paragraphs: list[dict] = []
    chapters: list[dict] = []          # {title, slug, paras: [str]}
    current: dict | None = None
    open_ids: set[str] = set()
    anchored: dict[str, list[str]] = {cid: [] for cid in comments}
    heading_stack: dict[int, str] = {}
    h1_seen = 0

    for para in body.iter(f"{W}p"):
        st = _style(para)
        text = _text(para).strip()

        if st in H1_STYLES:
            h1_seen += 1
            current = {"title": text, "slug": _slug(text), "paras": []}
            chapters.append(current)
            heading_stack = {1: text}
        elif st in HEADING_STYLES:
            lvl = HEADING_STYLES[st]
            heading_stack = {k: v for k, v in heading_stack.items() if k < lvl}
            heading_stack[lvl] = text

        hpath = " > ".join(heading_stack[k] for k in sorted(heading_stack))

        # Comment ranges are tracked in document order: a start opens an id, an
        # end closes it, and every w:t seen while an id is open belongs to it.
        for node in para.iter():
            if node.tag == f"{W}commentRangeStart":
                cid = node.get(f"{W}id")
                open_ids.add(cid)
                if cid in comments and not comments[cid]["chapter"]:
                    comments[cid]["chapter"] = current["title"] if current else "(front matter)"
                    comments[cid]["heading_path"] = hpath
            elif node.tag == f"{W}commentRangeEnd":
                open_ids.discard(node.get(f"{W}id"))
            elif node.tag == f"{W}t" and open_ids:
                for cid in open_ids:
                    if cid in anchored:
                        anchored[cid].append(node.text or "")

        if text:
            paragraphs.append({"text": text, "style": st, "heading_path": hpath})
            if current is not None:
                prefix = "#" * HEADING_STYLES[st] + " " if st in HEADING_STYLES else ""
                current["paras"].append(prefix + text)

    for cid, parts in anchored.items():
        comments[cid]["anchor"] = "".join(parts).strip()

    return {
        "paragraphs": paragraphs,
        "chapters": chapters,
        "comments": sorted(comments.values(), key=lambda c: int(c["id"])),
        "h1_count": h1_seen,
        "has_commentsExtended": "word/commentsExtended.xml" in names,
    }


def _words(s: str) -> int:
    return len(s.split())


def write_snapshot(src: Path, out_dir: Path, do_drift: bool) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    chap_dir = out_dir / "chapters"
    chap_dir.mkdir(exist_ok=True)

    # Copy FIRST, then read the copy. Word holds an exclusive lock on an open
    # document -- zipfile raises PermissionError on the original, while a plain
    # copy succeeds. Reading the copy also guarantees the parsed text and the
    # archived .docx are the same bytes.
    dst_docx = out_dir / "thesis_full.docx"
    shutil.copy2(src, dst_docx)
    print(f"  copied  {dst_docx.name}  ({dst_docx.stat().st_size:,} bytes)")

    d = read_docx(dst_docx)

    if d["h1_count"] == 0:
        raise SystemExit(
            "ABORT: no Heading 1 paragraphs found. The document may use custom\n"
            "styles or outline levels rather than the built-in Heading 1.\n"
            "Extend H1_STYLES rather than accepting a single undivided file."
        )

    full = "\n\n".join(p["text"] for p in d["paragraphs"])
    (out_dir / "thesis_full.md").write_text(full, encoding="utf-8")
    print(f"  wrote   thesis_full.md  ({_words(full):,} words)")

    for ch in d["chapters"]:
        body = "\n\n".join(ch["paras"])
        (chap_dir / f"{ch['slug']}.md").write_text(
            f"# {ch['title']}\n\n{body}\n", encoding="utf-8")
    print(f"  wrote   chapters/  ({len(d['chapters'])} files)")

    # --- comments -------------------------------------------------------
    cm = ["# Word comments", "",
          f"Extracted {_dt.date.today()} from `{src.name}`.",
          f"{len(d['comments'])} comment(s). "
          f"Resolved status {'available' if d['has_commentsExtended'] else 'UNAVAILABLE'}.",
          "", "> Read-only extract. Reply in Word, not here.", ""]
    for c in d["comments"]:
        flags = []
        if c["resolved"]:
            flags.append("RESOLVED")
        if c["is_reply"]:
            flags.append("reply")
        cm.append(f"## [{c['id']}] {c['author']} — {c['chapter'] or '(unanchored)'}"
                  + (f"  `{' · '.join(flags)}`" if flags else ""))
        cm.append("")
        if c["heading_path"]:
            cm.append(f"- **Section:** {c['heading_path']}")
        cm.append(f"- **Date:** {c['date']}")
        if c["anchor"]:
            cm.append(f"- **On:** \u201c{c['anchor'][:400]}\u201d")
        cm += ["", c["text"], ""]
    (out_dir / "comments.md").write_text("\n".join(cm), encoding="utf-8")
    print(f"  wrote   comments.md  ({len(d['comments'])} comments)")

    # --- manifest + drift ----------------------------------------------
    man = ["# Snapshot manifest", "",
           f"- **Source:** `{src}`",
           f"- **Captured:** {_dt.datetime.now():%Y-%m-%d %H:%M:%S}",
           f"- **Source modified:** {_dt.datetime.fromtimestamp(src.stat().st_mtime):%Y-%m-%d %H:%M:%S}",
           f"- **Size:** {src.stat().st_size:,} bytes",
           f"- **Words:** {_words(full):,}",
           f"- **Chapters (Heading 1):** {d['h1_count']}",
           f"- **Comments:** {len(d['comments'])}",
           "",
           "> **Read-only.** Never edit these files and never convert them back.",
           "> Working surfaces are `sections-drafts/*.md` (live) and the OneDrive",
           "> `.docx` (prose as submitted).",
           "", "## Chapters", "",
           "| Heading 1 | file | words |", "|---|---|---:|"]
    for ch in d["chapters"]:
        man.append(f"| {ch['title'][:60]} | `chapters/{ch['slug']}.md` "
                   f"| {_words(' '.join(ch['paras'])):,} |")

    if do_drift and DRAFTS.is_dir():
        man += ["", "## Drift vs. `sections-drafts/`", "",
                "Word counts only -- a weak signal, since markdown syntax and",
                "bullet scaffolding do not survive conversion. Use it to rank",
                "chapters for inspection, not as a verdict.", "",
                "| chapter | draft .md | snapshot | delta |", "|---|---:|---:|---:|"]
        for ch in d["chapters"]:
            draft = DRAFTS / f"{ch['slug']}.md"
            if not draft.is_file():
                continue
            dw = _words(draft.read_text(encoding="utf-8", errors="replace"))
            sw = _words(" ".join(ch["paras"]))
            man.append(f"| {ch['slug']} | {dw:,} | {sw:,} | {sw - dw:+,} |")

    (out_dir / "MANIFEST.md").write_text("\n".join(man) + "\n", encoding="utf-8")
    print("  wrote   MANIFEST.md")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="path to the shared .docx (default: the OneDrive copy)")
    ap.add_argument("--date", default=None,
                    help="snapshot folder name (default: today, YYYY-MM-DD)")
    ap.add_argument("--no-drift", action="store_true",
                    help="skip the drift table against sections-drafts/")
    a = ap.parse_args()

    src = Path(a.source)
    if not src.is_file():
        print(f"ERROR: source not found:\n  {src}", file=sys.stderr)
        return 2

    out = SNAP_ROOT / (a.date or _dt.date.today().isoformat())
    print(f"snapshot -> {out.relative_to(REPO_ROOT)}")
    write_snapshot(src, out, not a.no_drift)
    print("\ndone. Snapshot is read-only; edit the OneDrive .docx or the drafts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
