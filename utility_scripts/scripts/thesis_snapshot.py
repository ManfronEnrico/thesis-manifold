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
    05_thesis_writing/docx-exported-snapshots/YYYY-MM-DD_HH-mm/
        thesis_full.docx          verbatim copy of the source
        thesis_full.md            whole-document text
        chapters/ch3-methodology.md   one file per Heading 1
        comments.md               every Word comment + the text it is anchored to
        comments/ch1-introduction.md  the same comments, split per chapter
        MANIFEST.md               what was captured, sha256, and the drift table

THE SNAPSHOT IS READ-ONLY. Never edit a file under docx-exported-snapshots/ and never convert
one back. Editing them creates a fourth version of the thesis and reintroduces
exactly the ambiguity the snapshot exists to remove. The working surfaces are
05_thesis_writing/sections-drafts/*.md (live) and the OneDrive .docx (prose).

Usage:
    python utility_scripts/scripts/thesis_snapshot.py
    python utility_scripts/scripts/thesis_snapshot.py --source "C:/path/to.docx"
    python utility_scripts/scripts/thesis_snapshot.py --no-drift

See docx-exported-snapshots/README.md for copy-paste commands and the workflow.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
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
SNAP_ROOT = REPO_ROOT / "05_thesis_writing" / "docx-exported-snapshots"
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
    # Ch1-6 headings dropped their "Chapter N -" prefix (seen 2026-09-05) and
    # read as a bare title, so match on the title too. Keys are matched as
    # substrings of the lowercased heading; keep them long enough to be unique.
    "introduction": "ch1-introduction",
    "literature review": "ch2-literature-review",
    "methodology": "ch3-methodology",
    "data assessment": "ch4-data-assessment",
    "predictive-extension architecture": "ch5-framework-design",
    "model benchmark": "ch6-model-benchmark",
    "context-aware decision synthesis": "ch7-decision-synthesis",
    "experimental evaluation": "ch8-experimental-evaluation",
    "discussion": "ch9-discussion",
    "conclusion": "ch10-conclusion",
    # Front matter: no sections-drafts counterpart by design. Registered so the
    # "not in CHAPTER_MAP" warning stays meaningful -- otherwise 6 expected
    # entries drown out the one that signals a genuinely new chapter.
    "table of contents": "table-of-contents",
    "table of figures": "table-of-figures",
    "table of tables": "table-of-tables",
    "reference list": "reference-list",
    "ai use declaration": "ai-use-declaration",
    "appendix": "appendix",
}

# Heading levels are NOT hardcoded. They are resolved per-document from
# word/styles.xml by _heading_levels(), because keying on style *names* is what
# broke on 2026-09-05: chapters 1-6 switched to a custom "H1-Chapter" style,
# the name was not in the list, and six chapters silently merged into Abstract
# instead of erroring. A .docx states each style's level itself; ask it.
#
# These remain only as a last-resort floor if styles.xml is unreadable.
FALLBACK_HEADING_STYLES = {"Heading1": 1, "Heading2": 2, "Heading3": 3,
                           "Heading4": 4, "Heading5": 5,
                           "Heading6": 6, "Heading7": 7,
                           "Heading8": 8, "Heading9": 9}

# outlineLvl=9 is Word's "body text" sentinel: TOCHeading is basedOn Heading1
# but sets 9 to opt out of the outline. Treat it as "not a heading".
_NO_OUTLINE = 9


def _heading_levels(z: zipfile.ZipFile) -> dict[str, int]:
    """Map every styleId in the document to a heading level (1-9), or absent.

    Three sources, most authoritative first:
      1. an explicit w:outlineLvl on the style (0-based; 9 means "not a heading")
      2. the w:basedOn chain -- "H1-Chapter" is basedOn "Heading1", which is
         how a custom style declares it is a heading without restating the level
      3. the style name/id as a last resort ("heading 3", "H3-Something")

    Resolving from the file means a renamed or newly-invented custom style is
    picked up automatically, with no edit to this script.
    """
    try:
        root = ET.fromstring(z.read("word/styles.xml"))
    except (KeyError, ET.ParseError):
        return dict(FALLBACK_HEADING_STYLES)

    explicit: dict[str, int] = {}     # styleId -> level, from outlineLvl
    based_on: dict[str, str] = {}     # styleId -> parent styleId
    names: dict[str, str] = {}        # styleId -> human name
    para_styles: set[str] = set()

    for st in root.iter(f"{W}style"):
        sid = st.get(f"{W}styleId")
        if not sid:
            continue
        if st.get(f"{W}type") in (None, "paragraph"):
            para_styles.add(sid)
        nm = st.find(f"{W}name")
        if nm is not None:
            names[sid] = (nm.get(f"{W}val") or "")
        bo = st.find(f"{W}basedOn")
        if bo is not None and bo.get(f"{W}val"):
            based_on[sid] = bo.get(f"{W}val")
        pr = st.find(f"{W}pPr")
        ol = pr.find(f"{W}outlineLvl") if pr is not None else None
        if ol is not None and (ol.get(f"{W}val") or "").isdigit():
            explicit[sid] = int(ol.get(f"{W}val"))

    def from_name(sid: str) -> int | None:
        # "heading 3" / "Heading3" / "H3 - Chapter" -> 3. Requires the digit to
        # follow the h-word so "Header" and "Hyperlink" do not match.
        for cand in (names.get(sid, ""), sid):
            m = re.match(r"^\s*h(?:eading)?\s*[-_ ]?([1-9])\b", cand, re.I)
            if m:
                return int(m.group(1))
        return None

    def resolve(sid: str, seen: frozenset[str] = frozenset()) -> int | None:
        if sid in seen:                       # cyclic basedOn; give up
            return None
        if sid in explicit:                   # 1. explicit wins, including 9
            lvl = explicit[sid]
            return None if lvl >= _NO_OUTLINE else lvl + 1
        parent = based_on.get(sid)
        if parent:                            # 2. inherit from the chain
            lvl = resolve(parent, seen | {sid})
            if lvl is not None:
                return lvl
        return from_name(sid)                 # 3. name, last

    out: dict[str, int] = {}
    for sid in para_styles:
        lvl = resolve(sid)
        if lvl is not None and 1 <= lvl <= 9:
            out[sid] = lvl
    return out or dict(FALLBACK_HEADING_STYLES)


def _style(para) -> str | None:
    pr = para.find(f"{W}pPr")
    if pr is None:
        return None
    s = pr.find(f"{W}pStyle")
    return s.get(f"{W}val") if s is not None else None


# Brian's review vocabulary, applied by hand across the 2026-09-05 whole-thesis
# pass (195 of 268 comments carry at least one). Parsing it turns a prose comment
# into a typed, routable action -- "every OUTDATED claim in ch6" becomes a query
# rather than a re-read. Canonical spelling on the left, accepted variants right.
KEYWORDS = {
    "VERIFY": ("VERIFY", "VALIDATE"),
    "SOURCE": ("SOURCES", "SOURCE"),
    "METACOMMENT": ("METACOMMMENT", "METACOMMENT"),   # sic: typo present in the doc
    "TABLE-REFERENCE": ("TABLE REFERENCE", "TABLE-REFERENCE"),
    "PROSE": ("PROSE",),
    "NAMING": ("NAMING",),
    "FORMATTING": ("FORMATTING",),
    "MATH": ("MATH",),
    "WATERMARK": ("WATERMARK",),
    "ACADEMIC": ("ACADEMIC",),
    "OUTDATED": ("OUTDATED",),
    "INCORRECT": ("INCORRECT",),
    "APPENDIX": ("APPENDIX",),
    "INTERNALREFERENCES": ("INTERNALREFERENCES", "INTERNAL REFERENCES"),
    "MISSING": ("MISSING",),
    "UPDATE": ("UPDATE",),
    "CONTEXT": ("CONTEXT",),
}


def _keywords(text: str) -> list[str]:
    """Canonical review keywords found in a comment.

    Matched only in the leading portion: these are written as a prefix
    ("VERIFY & APPENDIX: ..."), and the same words occur naturally in prose
    further down, where they are not tags.
    """
    head = text[:120].upper()
    found = []
    for canon, variants in KEYWORDS.items():
        for v in sorted(variants, key=len, reverse=True):
            if re.search(r"\b" + re.escape(v) + r"\b", head):
                found.append(canon)
                break
    return found

def _on(rpr, tag: str) -> bool:
    """True when a run property is present AND not explicitly switched off.

    Word writes <w:b/> for on and <w:b w:val="0"/> for off; inherited bold is
    cancelled with the latter, so presence alone is not enough.
    """
    if rpr is None:
        return False
    e = rpr.find(f"{W}{tag}")
    return e is not None and (e.get(f"{W}val") not in ("0", "false", "none"))


# Character styles whose runs are TERMS -- model names, metrics, identifiers --
# rather than emphasis. Rendered as `code` so a reader (and NotebookLM) can tell
# "italic because it is a term" from "italic because it is a quotation", a
# distinction direct italic formatting throws away permanently.
TERM_STYLES = {"Term", "TermChar"}


def _text(el, emphasis: bool = False) -> str:
    """All w:t descendants, with tabs and breaks rendered as whitespace.

    With emphasis=True, bold and italic runs are wrapped in markdown markers.
    Off by default: slugs, word counts and drift comparison want plain text,
    and marker characters would corrupt all three.

    ElementTree has no parent pointers, so runs are walked explicitly rather
    than flattening with .iter() and asking each w:t what it belongs to.
    """
    if not emphasis:
        out = []
        for n in el.iter():
            if n.tag == f"{W}t":
                out.append(n.text or "")
            elif n.tag == f"{W}tab":
                out.append("\t")
            elif n.tag in (f"{W}br", f"{W}cr"):
                out.append("\n")
        return "".join(out)

    out: list[str] = []
    for node in el.iter():
        if node.tag != f"{W}r":
            continue
        rpr = node.find(f"{W}rPr")
        bold, ital = _on(rpr, "b"), _on(rpr, "i")
        # A run carrying the Term character style is a term, not emphasis. The
        # style supplies the italic, so the run itself has no <w:i> -- reading
        # direct formatting alone misses it entirely.
        rs = rpr.find(f"{W}rStyle") if rpr is not None else None
        term = rs is not None and rs.get(f"{W}val") in TERM_STYLES
        # A bold superscript footnote marker sitting inside an italic quotation
        # splits it into "...text.**1* *more..." -- correct per run, unreadable
        # as prose. Superscripts carry no emphasis of their own.
        va = rpr.find(f"{W}vertAlign") if rpr is not None else None
        if va is not None and va.get(f"{W}val") in ("superscript", "subscript"):
            bold = ital = False
        chunk = []
        for n in node.iter():
            if n.tag == f"{W}t":
                chunk.append(n.text or "")
            elif n.tag == f"{W}tab":
                chunk.append("\t")
            elif n.tag in (f"{W}br", f"{W}cr"):
                chunk.append("\n")
        txt = "".join(chunk)
        if not txt:
            continue
        # Markers must hug the text: "** bold **" is not emphasis in markdown,
        # so leading/trailing space is moved outside the markers.
        lead = txt[:len(txt) - len(txt.lstrip())]
        trail = txt[len(txt.rstrip()):]
        core = txt.strip()
        if core and term:
            # Backticks, not italics: unambiguous, and never confused with a
            # quotation. Nested markers would be meaningless inside code.
            core = f"`{core}`"
        elif core and (bold or ital):
            mark = "**" if bold else "*"
            if ital and bold:
                mark = "***"
            core = f"{mark}{core}{mark}"
        out.append(lead + core + trail)

    # Adjacent runs with identical formatting produce "**a****b**"; collapse the
    # seam so the result is valid markdown rather than four literal asterisks.
    joined = "".join(out)
    # Adjacent runs with identical formatting produce "**a****b**"; close the
    # seam so the result is valid markdown rather than four literal asterisks.
    # Anchored on a run of 4+ asterisks: a naive replace("*"*2, "") would also
    # eat the halves of a legitimate "**bold**" pair.
    joined = re.sub(r"(?<!\*)\*{4}(?!\*)", "", joined)
    joined = re.sub(r"\*{6}", "", joined)
    return joined

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


# Cell/row boundaries in anchor text use ASCII unit/record separators, not
# "|": table cells legitimately contain pipes (the WMAPE formula is
# "S|y-y^| / S|y|"), and a pipe separator split that maths into fragments.
_CELL_SEP = chr(31)
_ROW_SEP = chr(30)


def _tidy_anchor(text: str) -> str:
    r"""Normalise anchor text and render table cell/row separators.

    Order matters. The sentinels become placeholders BEFORE whitespace is
    collapsed (chr(30)/chr(31) are matched by \s and would be eaten), and are
    rendered as pipes only at the very end. Trimming is done on the
    placeholders, not on pipes, so a pipe that is part of the content -- the
    WMAPE formula is S|y-y^| / S|y| -- is never mistaken for a separator.
    """
    ph_row, ph_cell = "\u0001R\u0001", "\u0001C\u0001"
    t = text.replace(_ROW_SEP, ph_row).replace(_CELL_SEP, ph_cell)
    t = re.sub(r"\s+", " ", t)
    # drop empty leading/trailing cells and any cell-break that merely abuts
    # a row-break, while both are still unambiguous placeholders
    t = re.sub("(?:" + ph_cell + "| )+(?=" + ph_row + ")", "", t)
    t = re.sub("^(?:" + ph_cell + "|" + ph_row + "| )+", "", t)
    t = re.sub("(?:" + ph_cell + "|" + ph_row + "| )+$", "", t)
    t = t.replace(ph_row, " || ").replace(ph_cell, " | ")
    return re.sub(r" {2,}", " ", t).strip()

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
                "text": _text(c, emphasis=True).strip(),
                "para_ids": para_ids,
                "anchor": "", "chapter": "", "heading_path": "",
                "resolved": False, "is_reply": False,
                "keywords": _keywords(_text(c)),
                # w:id is a POSITION -- Word renumbers every comment when one
                # is inserted earlier (F33: 120 of 122 shared ids pointed at a
                # different comment 20 minutes later). para_id is the identity
                # that survives, and is what any cross-snapshot record keys on.
                "para_id": para_ids[0] if para_ids else None,
                "thread_para_id": para_ids[0] if para_ids else None,
                "parent_id": None, "thread_id": cid, "reply_count": 0,
                "thread_pos": 0,
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
        # paraId -> comment id, so a paraIdParent can be resolved to the
        # comment it answers. A comment can hold several paragraphs; any of
        # them may be the one another comment points at.
        cid_by_para = {pid: c["id"] for c in comments.values()
                       for pid in c["para_ids"]}

        for c in comments.values():
            for pid in c["para_ids"]:
                if pid in done_by_para:
                    c["resolved"] = done_by_para[pid]
                if pid in parent_by_para:
                    c["is_reply"] = True
                    # Keep the parent COMMENT id, not just the boolean. Without
                    # it the extract can say a comment is a reply but not what
                    # it answers, so ~190 threads read as 217 unrelated items
                    # and a thread's conclusion is filed away from its question.
                    parent = cid_by_para.get(parent_by_para[pid])
                    if parent is not None and parent != c["id"]:
                        c["parent_id"] = parent

        # Walk each chain to its root. Guarded against cycles and orphans: a
        # deleted parent leaves a dangling id, and the comment then roots itself
        # rather than vanishing from the output.
        for c in comments.values():
            seen = {c["id"]}
            node = c
            while node["parent_id"] and node["parent_id"] in comments:
                node = comments[node["parent_id"]]
                if node["id"] in seen:
                    break
                seen.add(node["id"])
            c["thread_id"] = node["id"]
            c["thread_para_id"] = node["para_id"]

        # reply_count is carried on every member so a row can be read on its
        # own; thread_pos orders replies under their root by document order.
        for tid in {c["thread_id"] for c in comments.values()}:
            members = sorted((c for c in comments.values() if c["thread_id"] == tid),
                             key=lambda c: int(c["id"]))
            for i, c in enumerate(members):
                c["thread_pos"] = i
                c["reply_count"] = len(members) - 1

    # --- body walk ------------------------------------------------------
    # Levels come from the document's own style definitions, so custom styles
    # (H1-Chapter, or anything invented later) are picked up without a code edit.
    levels = _heading_levels(z)
    styles_used: dict[str, int] = {}
    doc = ET.fromstring(z.read("word/document.xml"))
    body = doc.find(f"{W}body")

    paragraphs: list[dict] = []
    chapters: list[dict] = []          # {title, slug, paras: [str]}
    current: dict | None = None
    open_ids: set[str] = set()
    anchored: dict[str, list[str]] = {cid: [] for cid in comments}
    heading_stack: dict[int, str] = {}
    h1_seen = 0
    n_tables = [0]

    def _scan_ranges(el, hpath: str) -> None:
        """Track comment ranges in document order and collect anchor text.

        Must be called for every paragraph -- including those inside tables --
        or a comment anchored in a table silently loses its quoted text.

        Cell and row boundaries emit separators. Without them a comment on a
        table row quotes back as "RTD37930 @425895112,19344,449" -- every value
        run together, with no way to tell which number is which column, which
        is what made the four table-anchored comments unactionable (2026-09-05).
        """
        def walk(node) -> None:
            for child in node:
                tag = child.tag
                if tag == f"{W}commentRangeStart":
                    cid = child.get(f"{W}id")
                    open_ids.add(cid)
                    if cid in comments and not comments[cid]["chapter"]:
                        comments[cid]["chapter"] = current["title"] if current else "(front matter)"
                        comments[cid]["heading_path"] = hpath
                elif tag == f"{W}commentRangeEnd":
                    open_ids.discard(child.get(f"{W}id"))
                elif tag == f"{W}t" and open_ids:
                    for cid in open_ids:
                        if cid in anchored:
                            anchored[cid].append(child.text or "")
                else:
                    walk(child)
                    # Closing a cell/row separates values that are otherwise
                    # concatenated. Emitted only while a range is open.
                    if open_ids and tag in (f"{W}tc", f"{W}tr"):
                        sep = _CELL_SEP if tag == f"{W}tc" else _ROW_SEP
                        for cid in open_ids:
                            if cid in anchored:
                                anchored[cid].append(sep)
        walk(el)

    def _cell_text(tc) -> str:
        """A cell's paragraphs joined with <br>, so a multi-line cell stays in
        one markdown row. Pipes are escaped or they would split the column."""
        parts = [_text(q, emphasis=True).strip() for q in tc.iter(f"{W}p")]
        parts = [x for x in parts if x]
        return "<br>".join(parts).replace("|", "\\|")

    def _render_table(tbl, hpath: str) -> str:
        """Render w:tbl as a markdown pipe table.

        Word has no notion of a header row, so the first row is used as one:
        markdown requires a header, and every table in this document does in
        fact lead with one. Merged cells (w:gridSpan / w:vMerge) are NOT
        reconstructed -- the text is kept, the span is lost.
        """
        rows: list[list[str]] = []
        for tr in tbl.findall(f"{W}tr"):
            cells = tr.findall(f"{W}tc")
            if not cells:
                continue
            row = []
            for tc in cells:
                span = 1
                pr = tc.find(f"{W}tcPr")
                if pr is not None:
                    gs = pr.find(f"{W}gridSpan")
                    if gs is not None and (gs.get(f"{W}val") or "").isdigit():
                        span = int(gs.get(f"{W}val"))
                row.append(_cell_text(tc))
                row += [""] * (span - 1)      # keep columns aligned
            rows.append(row)
        if not rows:
            return ""
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        head, body_rows = rows[0], rows[1:]
        out = ["| " + " | ".join(head) + " |",
               "|" + "|".join(["---"] * width) + "|"]
        for r in body_rows:
            out.append("| " + " | ".join(r) + " |")
        return "\n".join(out)

    def _handle_para(para) -> None:
        nonlocal current, h1_seen, heading_stack, hpath
        st = _style(para)
        text = _text(para).strip()
        lvl = levels.get(st) if st else None
        # Headings are bold by style definition (Heading1, H2-Chapter, ...), so
        # emphasis inside one would render "## **Title**" -- 13 heading runs in
        # this document carry an explicit <w:b> that would do exactly that.
        rich = text if lvl else _text(para, emphasis=True).strip()
        if lvl and text:
            styles_used[st] = styles_used.get(st, 0) + 1
        if lvl == 1 and text:
            h1_seen += 1
            # `blocks` keeps the level alongside the text so the heading tree
            # can be rebuilt for sections/; `paras` stays a flat list of
            # rendered markdown for chapters/, unchanged.
            current = {"title": text, "slug": _slug(text), "paras": [],
                       "blocks": []}
            chapters.append(current)
            heading_stack = {1: text}
        elif lvl and text:
            heading_stack = {k: v for k, v in heading_stack.items() if k < lvl}
            heading_stack[lvl] = text

        hpath = " > ".join(heading_stack[k] for k in sorted(heading_stack))
        _scan_ranges(para, hpath)

        if text:
            paragraphs.append({"text": rich, "style": st, "heading_path": hpath})
            if current is not None:
                prefix = ("#" * levels[st] + " ") if st in levels else ""
                current["paras"].append(prefix + rich)
                current["blocks"].append({"lvl": lvl, "text": rich,
                                          "md": prefix + rich})

    # Walk direct children, not body.iter(w:p): iterating paragraphs recurses
    # INTO tables, which is how 28 tables were flattened into loose cell values
    # with the row/column structure lost (seen 2026-09-05). Tables are handled
    # as a unit here, in document order so comment ranges stay correct.
    hpath = ""
    for child in body:
        if child.tag == f"{W}p":
            _handle_para(child)
        elif child.tag == f"{W}tbl":
            _scan_ranges(child, hpath)          # anchors first, in order
            md = _render_table(child, hpath)
            if md:
                n_tables[0] += 1
                paragraphs.append({"text": md, "style": "__table__",
                                   "heading_path": hpath})
                if current is not None:
                    current["paras"].append(md)
                    current["blocks"].append({"lvl": None, "text": md,
                                              "md": md})

    for cid, parts in anchored.items():
        comments[cid]["anchor"] = _tidy_anchor("".join(parts))

    return {
        "paragraphs": paragraphs,
        "chapters": chapters,
        "comments": sorted(comments.values(), key=lambda c: int(c["id"])),
        "h1_count": h1_seen,
        "levels": levels,
        "styles_used": styles_used,
        "n_tables": n_tables[0],
        "has_commentsExtended": "word/commentsExtended.xml" in names,
        "src_name": path.name,
    }


def _folder_slug(label: str) -> str:
    """Turn a human label into a filesystem-safe folder suffix.

    "First Complete Audit" -> "first-complete-audit". Kept short so the folder
    name stays readable next to the timestamp, and restricted to characters
    that survive Windows, git and OneDrive alike.
    """
    s = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    return s[:48] or "labelled"


def _sha256(path: Path) -> str:
    """Provenance for the snapshot: the .docx itself is gitignored (a large
    binary git cannot diff), so this hash is what proves which source file the
    tracked .md files came from."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _plain(s: str) -> str:
    """Strip markdown emphasis markers.

    Truncating rich text at a fixed width can cut through "**", leaving a
    dangling marker that italicises the rest of a table row. Index gists and
    one-line summaries therefore use plain text.
    """
    return re.sub(r"\*{1,3}", "", s)


def _words(s: str) -> int:
    return len(s.split())


def _group_threads(rows: list[dict]) -> list[tuple[dict, list[dict]]]:
    """[(root, [replies...])] in document order, from a flat comment list.

    A reply whose root is in a different chapter file still renders with its
    root; grouping is by thread_id, which is chapter-independent by design.
    """
    by_id = {c["id"]: c for c in rows}
    threads: dict[str, list[dict]] = {}
    for c in rows:
        threads.setdefault(c["thread_id"], []).append(c)
    out = []
    for tid, members in threads.items():
        members.sort(key=lambda c: c["thread_pos"])
        root = by_id.get(tid) or members[0]
        replies = [c for c in members if c["id"] != root["id"]]
        out.append((root, replies))
    out.sort(key=lambda t: int(t[0]["id"]))
    return out


def _n_threads(rows: list[dict]) -> int:
    return len({c["thread_id"] for c in rows})


ANCHOR_LIMIT = 2000


def _anchor_excerpt(a: str) -> str:
    """The quoted passage, generously capped and honestly marked when cut.

    For a PROSE or VERIFY thread the anchored text *is* the work item -- the
    passage to rewrite or fact-check. The old 400-char cap truncated 78 of 268
    anchors mid-sentence, removing the very thing the thread is about. Long
    anchors are real: one spans 56k characters (a whole section selected).

    Keeps head and tail rather than a prefix, so a selection's start and end are
    both visible; the middle is where a long selection is least informative.
    """
    if len(a) <= ANCHOR_LIMIT:
        return a
    head, tail = a[:ANCHOR_LIMIT - 400], a[-300:]
    return (f"{head} […{len(a) - ANCHOR_LIMIT + 100:,} more characters — "
            f"see the chapter file…] {tail}")


def _thread_keywords(root: dict, replies: list[dict]) -> list[str]:
    """Keywords for a whole thread: the root's, plus any a reply introduces.

    A reply can add a type the root did not name -- Enrico answering a VERIFY
    with a SOURCE. Union, de-duplicated, root's order first.
    """
    out = list(root["keywords"])
    for r in replies:
        for k in r["keywords"]:
            if k not in out:
                out.append(k)
    return out


def _render_comments(rows: list[dict], title: str, src_name: str,
                     has_ext: bool, scoped: bool) -> str:
    """One comments file: index table, then a section per THREAD.

    Threads, not comments, are the unit of triage: a thread is one decision,
    and its conclusion lives in its last message. Rendering 217 flat sections
    files every answer away from its question -- and would hand Enrico 17 open
    items that are in fact his replies to Brian.

    Every comment keeps its own stable `<a id="cNN">` anchor, including
    replies, so existing links from drafts and plans stay valid.
    """
    out = [f"# {title}", "",
           f"Extracted {_dt.date.today()} from `{src_name}`.",
           f"{len(rows)} comment(s) in {_n_threads(rows)} thread(s). "
           f"Resolved status {'available' if has_ext else 'UNAVAILABLE'}.",
           "",
           "> **Read-only extract.** Reply in Word, not here -- this file is "
           "regenerated on every snapshot and any edit is lost.", ""]

    if not rows:
        out += ["*(no comments in this chapter)*", ""]
        return "\n".join(out)

    threads = _group_threads(rows)

    out += ["## Index", "",
            "| # | " + ("section" if scoped else "chapter") + " | tags | replies | opens with |",
            "|---|---|---|---:|---|"]
    for root, replies in threads:
        where = (root["heading_path"].split(" > ")[-1] if scoped
                 else root["chapter"] or "(unanchored)")
        first = _plain(" ".join(root["text"].split()))[:80]
        flag = " ✔" if root["resolved"] else ""
        n = str(len(replies)) if replies else ""
        tags = ", ".join(_thread_keywords(root, replies))
        out.append(f"| [{root['id']}](#c{root['id']}) | {where[:45]}{flag} "
                   f"| {tags} | {n} | {first}... |")
    out += ["", "---", ""]

    for root, replies in threads:
        flags = []
        if root["resolved"]:
            flags.append("RESOLVED")
        if replies:
            flags.append(f"thread of {len(replies) + 1}")
        flags += _thread_keywords(root, replies)
        out.append(f'<a id="c{root["id"]}"></a>')
        out.append("")
        out.append(f"## [{root['id']}] {root['author']} -- "
                   f"{root['chapter'] or '(unanchored)'}"
                   + (f"  `{' * '.join(flags)}`" if flags else ""))
        out.append("")
        if root["heading_path"]:
            out.append(f"- **Section:** {root['heading_path']}")
        out.append(f"- **Date:** {root['date']}")
        if root["anchor"]:
            out.append(f"- **On:** “{_anchor_excerpt(root['anchor'])}”")
        out += ["", root["text"], ""]

        # Replies are nested under the root, not promoted to siblings, so the
        # thread reads as the one conversation it is.
        for r in replies:
            out.append(f'<a id="c{r["id"]}"></a>')
            out.append("")
            out.append(f"### [{r['id']}] {r['author']} -- reply"
                       + ("  `RESOLVED`" if r["resolved"] else ""))
            out.append("")
            out.append(f"- **Date:** {r['date']}")
            if r["anchor"] and r["anchor"] != root["anchor"]:
                out.append(f"- **On:** “{_anchor_excerpt(r['anchor'])}”")
            out += ["", r["text"], ""]
    return "\n".join(out)


def _num_prefix(i: int) -> str:
    """Zero-padded ordinal so a directory listing sorts in document order.

    Without it "10-conclusion" sorts before "2-literature-review", and the
    tree stops matching the thesis it mirrors.
    """
    return f"{i:02d}"


def _section_tree(d: dict) -> list[dict]:
    """Flatten the heading tree into leaf sections, once, for both writers.

    Returns [{rel, chapter, heading_path, body}] where `rel` is the relative
    path without extension. chapters/sections/<rel>.md holds the prose and
    comments/sections/<rel>.md the objections, so the two trees are addressable
    by the same key.
    """
    leaves: list[dict] = []
    for ci, ch in enumerate(d["chapters"], 1):
        blocks = ch.get("blocks") or []
        if not blocks:
            continue
        cdir = f"{_num_prefix(ci)}-{ch['slug']}"

        units: list[dict] = []
        pre: list[str] = []
        for blk in blocks:
            if blk["lvl"] == 2:
                units.append({"title": blk["text"], "body": [], "subs": []})
            elif blk["lvl"] == 3 and units:
                units[-1]["subs"].append({"title": blk["text"], "body": []})
            else:
                if units and units[-1]["subs"]:
                    units[-1]["subs"][-1]["body"].append(blk["md"])
                elif units:
                    units[-1]["body"].append(blk["md"])
                else:
                    pre.append(blk["md"])

        if any(x.strip() for x in pre):
            leaves.append({"rel": f"{cdir}/00-preamble", "chapter": ch["title"],
                           "heading_path": "", "body": pre})
        for ui, u in enumerate(units, 1):
            slug = f"{_num_prefix(ui)}-{_slug_plain(u['title'])}"
            if u["subs"]:
                if any(x.strip() for x in u["body"]):
                    leaves.append({"rel": f"{cdir}/{slug}/00-intro",
                                   "chapter": ch["title"],
                                   "heading_path": u["title"],
                                   "body": u["body"]})
                for si, sub in enumerate(u["subs"], 1):
                    nm = f"{_num_prefix(si)}-{_slug_plain(sub['title'])}"
                    leaves.append({
                        "rel": f"{cdir}/{slug}/{nm}",
                        "chapter": ch["title"],
                        "heading_path": f"{u['title']} > {sub['title']}",
                        "body": sub["body"]})
            else:
                leaves.append({"rel": f"{cdir}/{slug}", "chapter": ch["title"],
                               "heading_path": u["title"], "body": u["body"]})
    return leaves


def _section_comments(leaf: dict, d: dict) -> list[dict]:
    """Comments anchored in this leaf section.

    Matched on the full heading path, not the last heading alone: "Results"
    occurs under several chapters, and a loose match would file a ch6 objection
    under ch8.
    """
    want = (f"{leaf['chapter']} > {leaf['heading_path']}"
            if leaf["heading_path"] else leaf["chapter"])
    return [c for c in d["comments"] if c["heading_path"] == want]


def _sect_head(leaf: dict) -> tuple[str, str]:
    """(short title, full heading path) for a leaf section."""
    title = (leaf["heading_path"].split(" > ")[-1]
             if leaf["heading_path"] else leaf["chapter"])
    full = (f"{leaf['chapter']} > {leaf['heading_path']}"
            if leaf["heading_path"] else leaf["chapter"])
    return title, full


def _write_sections(d: dict, out_dir: Path) -> None:
    """chapters/sections/ -- prose, one file per leaf section.

    A chapter file is 3-6k words, so a diff between two snapshots is unreadable
    and an agent must load a whole chapter to reason about one subsection. A
    leaf section is ~100 words (median H3), which makes "how did 4.1.1 change
    between these snapshots" a small, precise question.

    Lives UNDER chapters/ because it is chapter content divided by section
    (Brian, 2026-09-05); comments/sections/ mirrors it key-for-key.
    """
    root = out_dir / "chapters" / "sections"
    n = 0
    for leaf in _section_tree(d):
        path = root / f"{leaf['rel']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        hits = _section_comments(leaf, d)
        title, full = _sect_head(leaf)
        out = [f"# {title}", "", f"> Section of **{full}**", ">",
               "> Generated from the Word document -- **do not edit.** Edit the "
               "OneDrive `.docx`; this file is rewritten on every snapshot.", ""]
        if hits:
            # Tags and counts, never comment ids: w:id is renumbered on every
            # insertion (F33), so ids here would make every section file differ
            # on every snapshot even when the prose is untouched.
            tags: list[str] = []
            for c in hits:
                for k in c["keywords"]:
                    if k not in tags:
                        tags.append(k)
            out += [f"**{len(hits)} comment(s) on this section**"
                    + (f" -- {', '.join(tags)}" if tags else "")
                    + f". Detail: `comments/sections/{leaf['rel']}.md`", ""]
        out += ["---", ""]
        out += leaf["body"] or ["*(no body text under this heading)*"]
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        n += 1
    print(f"  wrote   chapters/sections/  ({n} leaf section files)")


def _write_comment_sections(d: dict, out_dir: Path) -> None:
    """comments/sections/ -- the same tree, carrying objections not prose.

    Mirrors chapters/sections/ key-for-key, so a section and the objections
    against it can be held side by side without loading either chapter file.
    Only sections that actually carry comments get a file: 154 mostly-empty
    placeholders would bury the ones that matter.
    """
    root = out_dir / "comments" / "sections"
    n = 0
    for leaf in _section_tree(d):
        hits = _section_comments(leaf, d)
        if not hits:
            continue
        path = root / f"{leaf['rel']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        title, full = _sect_head(leaf)
        threads = _group_threads(hits)
        rendered = _render_comments(hits, f"Comments -- {title}",
                                    d.get("src_name", "the source document"),
                                    d["has_commentsExtended"], scoped=True)
        head = ("\n".join([
            f"> Objections on **{full}**", ">",
            f"> Prose: `chapters/sections/{leaf['rel']}.md`", ">",
            f"> {len(hits)} comment(s) in {len(threads)} thread(s).", ""]))
        first, rest = rendered.split("\n", 1)
        path.write_text(first + "\n\n" + head + rest, encoding="utf-8")
        n += 1
    print(f"  wrote   comments/sections/  ({n} sections carrying comments)")


def _slug_plain(t: str) -> str:
    """Filesystem slug for a heading, with emphasis markers stripped first."""
    x = re.sub(r"[*`]", "", t).lower()
    x = re.sub(r"[^a-z0-9]+", "-", x).strip("-")
    return x[:52] or "section"



def _write_thread_index(d: dict, out_dir: Path) -> None:
    """comments/INDEX.md -- one row per THREAD across the whole document.

    This is the tabular view (F27): derived, never hand-edited, and carrying
    keys/status/gist only. Resolution prose stays in the ledger, because a
    decision worded in two places diverges -- the drift
    `writing-surface-authority.md` exists to prevent.
    """
    rows = d["comments"]
    threads = _group_threads(rows)
    by_ch: dict[str, int] = {}
    for root, _ in threads:
        key = root["chapter"] or "(unanchored)"
        by_ch[key] = by_ch.get(key, 0) + 1

    out = ["# Thread index", "",
           f"Generated {_dt.date.today()} -- **derived, do not edit.** "
           f"Regenerated on every snapshot.", "",
           f"{len(rows)} comment(s) in **{len(threads)} thread(s)** "
           f"across {len(by_ch)} chapter(s).", "",
           "> Status and resolution live in the ledger, not here. This table "
           "carries keys, counts and a gist so a thread can be found; the "
           "reasoning behind a decision belongs in one place only.", "",
           "## Threads per chapter", "",
           "| chapter | threads |", "|---|---:|"]
    for ch, n in sorted(by_ch.items(), key=lambda kv: -kv[1]):
        out.append(f"| {ch} | {n} |")

    # Work-type roll-up: the taxonomy answers "how much of what kind of work is
    # left, and where", which a per-thread list cannot show at 241 threads.
    kw_ch: dict[str, dict[str, int]] = {}
    for root, replies in threads:
        ch = root["chapter"] or "(unanchored)"
        for k in _thread_keywords(root, replies):
            kw_ch.setdefault(k, {})[ch] = kw_ch.setdefault(k, {}).get(ch, 0) + 1
    if kw_ch:
        chaps = [c for c, _ in sorted(by_ch.items(), key=lambda kv: -kv[1])]
        out += ["", "## Work type by chapter", "",
                "Keyword tags Brian applied during the review pass. A thread "
                "counts once per tag.", "",
                "| tag | total | " + " | ".join(c[:18] for c in chaps) + " |",
                "|---|---:|" + "---:|" * len(chaps)]
        for k in sorted(kw_ch, key=lambda k: -sum(kw_ch[k].values())):
            cells = " | ".join(str(kw_ch[k].get(c, "") or "") for c in chaps)
            out.append(f"| **{k}** | {sum(kw_ch[k].values())} | {cells} |")
        untagged = sum(1 for r, rp in threads if not _thread_keywords(r, rp))
        out += ["", f"*{untagged} thread(s) carry no tag.*"]

    out += ["", "## All threads", "",
            "| thread | chapter | section | tags | opened by | replies | last voice | gist |",
            "|---|---|---|---|---|---:|---|---|"]
    for root, replies in threads:
        sec = (root["heading_path"].split(" > ")[-1]
               if root["heading_path"] else "")
        last = replies[-1]["author"] if replies else root["author"]
        gist = _plain(" ".join(root["text"].split()))[:70]
        slug = _slug(root["chapter"]) if root["chapter"] else "unanchored"
        flag = " RESOLVED" if root["resolved"] else ""
        out.append(f"| [{root['id']}]({slug}.md#c{root['id']}) "
                   f"| {(root['chapter'] or '')[:28]} | {sec[:32]} "
                   f"| {', '.join(_thread_keywords(root, replies))} "
                   f"| {root['author'][:16]} | {len(replies)} "
                   f"| {last[:16]}{flag} | {gist}... |")

    (out_dir / "comments" / "INDEX.md").write_text("\n".join(out),
                                                   encoding="utf-8")
    print(f"  wrote   comments/INDEX.md  ({len(threads)} threads)")


def _chapter_label(group: list[dict], slug: str) -> str:
    """Name a comments file after a thread ROOT's chapter, not whichever member
    happens to sort first -- a reply can carry a different chapter."""
    for c in group:
        if c["thread_id"] == c["id"] and c["chapter"]:
            return c["chapter"]
    return next((c["chapter"] for c in group if c["chapter"]), slug)


def _write_comments(d: dict, src: Path, out_dir: Path) -> None:
    """Write the combined comments file plus one per chapter.

    Per-chapter files are the point (F16): they put a chapter's prose and the
    objections raised against it one directory apart, so either can be handed
    to NotebookLM as a single scoped source. NotebookLM ingests text, not
    .xlsx, which is why this export is markdown rather than a spreadsheet.
    """
    rows = d["comments"]
    has_ext = d["has_commentsExtended"]

    (out_dir / "comments.md").write_text(
        _render_comments(rows, "Word comments — all chapters", src.name,
                         has_ext, scoped=False), encoding="utf-8")

    # Group by the chapter each comment is anchored in, reusing the same slug
    # map the chapter split uses so comments/chN.md pairs with chapters/chN.md.
    # A thread is filed by its ROOT's chapter, so a reply anchored elsewhere
    # travels with the conversation it belongs to instead of being orphaned
    # into another file where it reads as an unexplained fragment.
    slug_by_thread: dict[str, str] = {}
    for c in rows:
        if c["thread_id"] == c["id"]:
            slug_by_thread[c["thread_id"]] = (
                _slug(c["chapter"]) if c["chapter"] else "unanchored")

    by_slug: dict[str, list[dict]] = {}
    for c in rows:
        slug = slug_by_thread.get(
            c["thread_id"],
            _slug(c["chapter"]) if c["chapter"] else "unanchored")
        by_slug.setdefault(slug, []).append(c)

    cdir = out_dir / "comments"
    cdir.mkdir(exist_ok=True)
    for slug, group in sorted(by_slug.items()):
        (cdir / f"{slug}.md").write_text(
            _render_comments(group, f"Comments — {_chapter_label(group, slug)}",
                             src.name, has_ext, scoped=True), encoding="utf-8")

    print(f"  wrote   comments.md + comments/  "
          f"({len(rows)} comments over {len(by_slug)} chapter file(s))")
    _write_thread_index(d, out_dir)
    _write_sections(d, out_dir)
    _write_comment_sections(d, out_dir)


def _sanity_warnings(d: dict) -> list[str]:
    """Fail loudly on a structurally implausible parse.

    The 2026-09-05 breakage passed every check the script had: chapters 1-6
    used an unrecognised custom style, so they merged into Abstract and the run
    reported success with 11 chapters and a 22,885-word "Abstract". Nothing was
    zero, so nothing tripped. These checks target that shape -- a parse that is
    non-empty but wrong -- rather than only the empty case.
    """
    chapters = d["chapters"]
    if not chapters:
        raise SystemExit(
            "ABORT: no headings resolved to level 1.\n"
            "Levels are read from word/styles.xml, so this means the document\n"
            "has no level-1 style at all -- check it is the right file."
        )

    words = {c["title"]: _words(" ".join(c["paras"])) for c in chapters}
    total = sum(words.values()) or 1
    biggest, big_n = max(words.items(), key=lambda kv: kv[1])
    warn: list[str] = []

    # Structural checks first: they are exact, while the ratio checks
    # below are heuristics that a very short document can trip.
    slugs = [c["slug"] for c in chapters]
    dupes = {x for x in slugs if slugs.count(x) > 1}
    if dupes:
        raise SystemExit(
            f"ABORT: two chapters share a filename: {', '.join(sorted(dupes))}.\n"
            "The later one would overwrite the earlier. Add distinguishing\n"
            "entries to CHAPTER_MAP."
        )

    # One section holding most of the document = neighbours merged into it.
    if len(chapters) >= 5 and big_n / total > 0.40:
        raise SystemExit(
            f"ABORT: '{biggest}' holds {big_n:,} of {total:,} words "
            f"({big_n / total:.0%}).\n"
            "That usually means following chapters merged into it because their\n"
            "heading style did not resolve to a level. Compare the style ids in\n"
            "word/styles.xml against _heading_levels()."
        )

    # A front-matter section that outgrew a real chapter is the same symptom,
    # caught earlier: Abstract at 22,885 words was the 2026-09-05 tell.
    for name in ("abstract", "table of contents", "table of figures",
                 "table of tables", "ai use declaration"):
        for title, n in words.items():
            if title.lower().startswith(name) and n > 2000:
                warn.append(
                    f"  WARN    '{title}' is {n:,} words -- front matter this "
                    f"long usually means a following section merged into it."
                )

    empties = [t for t, n in words.items() if n == 0]
    if empties:
        warn.append(f"  WARN    {len(empties)} empty chapter(s): "
                    f"{', '.join(empties[:5])}")


    unmapped = [c["title"] for c in chapters if c["slug"] not in CHAPTER_MAP.values()]
    if unmapped:
        warn.append(f"  WARN    {len(unmapped)} chapter(s) not in CHAPTER_MAP, "
                    f"named from their title: {', '.join(unmapped[:4])}")
    return warn


def write_snapshot(src: Path, out_dir: Path, do_drift: bool,
                   label: str | None = None) -> None:
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

    for line in _sanity_warnings(d):
        print(line)

    full = "\n\n".join(p["text"] for p in d["paragraphs"])
    (out_dir / "thesis_full.md").write_text(full, encoding="utf-8")
    print(f"  wrote   thesis_full.md  ({_words(full):,} words)")

    for ch in d["chapters"]:
        body = "\n\n".join(ch["paras"])
        # The header is not decoration: editing a snapshot instead of the
        # source is how a fourth version of the thesis appears (F10).
        (chap_dir / f"{ch['slug']}.md").write_text(
            "<!-- DO NOT EDIT. Regenerated by thesis_snapshot.py from the"
            " OneDrive .docx. Edit the .docx or sections-drafts/*.md"
            " instead. -->\n\n"
            f"# {ch['title']}\n\n{body}\n", encoding="utf-8")
    print(f"  wrote   chapters/  ({len(d['chapters'])} files)")

    # --- comments -------------------------------------------------------
    _write_comments(d, src, out_dir)


    # --- manifest + drift ----------------------------------------------
    man = ["# Snapshot manifest", "",
           *( [f"- **Label:** **{label}**"] if label else [] ),
           f"- **Source:** `{src}`",
           f"- **Captured:** {_dt.datetime.now():%Y-%m-%d %H:%M:%S}",
           f"- **Source modified:** {_dt.datetime.fromtimestamp(src.stat().st_mtime):%Y-%m-%d %H:%M:%S}",
           f"- **Size:** {src.stat().st_size:,} bytes",
           f"- **SHA-256:** `{_sha256(dst_docx)}`",
           f"- **Words:** {_words(full):,}",
           f"- **Chapters (level 1):** {d['h1_count']}",
           f"- **Comments:** {len(d['comments'])}",
           f"- **Tables:** {d['n_tables']} (rendered as markdown pipe tables)",
           "",
           "> **Read-only.** Never edit these files and never convert them back.",
           "> Working surfaces are `sections-drafts/*.md` (live) and the OneDrive",
           "> `.docx` (prose as submitted).",
           "", "## Chapters", "",
           "| Heading 1 | file | words |", "|---|---|---:|"]
    for ch in d["chapters"]:
        man.append(f"| {ch['title'][:60]} | `chapters/{ch['slug']}.md` "
                   f"| {_words(' '.join(ch['paras'])):,} |")

    # Recorded so a future break is visible as a diff: if a style disappears
    # from this table between two snapshots, the document was restyled.
    man += ["", "## Heading styles resolved", "",
            "Levels are read from `word/styles.xml` (outlineLvl, then basedOn,",
            "then name), not hardcoded -- custom styles are picked up on their own.",
            "", "| style id | level | paragraphs |", "|---|---:|---:|"]
    for sid, n in sorted(d["styles_used"].items(),
                         key=lambda kv: (d["levels"].get(kv[0], 9), -kv[1])):
        man.append(f"| `{sid}` | {d['levels'].get(sid, '?')} | {n} |")

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
    ap.add_argument("--stamp", "--date", dest="stamp", default=None,
                    help="snapshot folder name (default: now, YYYY-MM-DD_HH-mm)")
    ap.add_argument("--label", "--slug", dest="label", default=None,
                    help="name this snapshot, appended to the timestamp "
                         "(e.g. --label \"First Complete Audit\" -> "
                         "2026-09-05_18-10_first-complete-audit). Use it to "
                         "mark a milestone so it is not mistaken for a "
                         "routine or test run.")
    ap.add_argument("--no-drift", action="store_true",
                    help="skip the drift table against sections-drafts/")
    a = ap.parse_args()

    src = Path(a.source)
    if not src.is_file():
        print(f"ERROR: source not found:\n  {src}", file=sys.stderr)
        return 2

    stamp = a.stamp or _dt.datetime.now().strftime("%Y-%m-%d_%H-%M")
    if a.label:
        stamp = f"{stamp}_{_folder_slug(a.label)}"
    out = SNAP_ROOT / stamp
    print(f"snapshot -> {out.relative_to(REPO_ROOT)}")
    write_snapshot(src, out, not a.no_drift, label=a.label)
    print("\ndone. Snapshot is read-only; edit the OneDrive .docx or the drafts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
