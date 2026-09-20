#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deck_snapshot.py -- Snapshot the oral-defence .pptx into this repo, diffably.

The sibling of thesis_snapshot.py, and for the same reason. The deck lives in
OneDrive so both authors can edit it; a .pptx is a zip of compressed XML, so
git can neither diff it nor merge it, and two people editing slides is exactly
where silent drift happens.

What the drift looks like here, concretely: the slide plan
(06_thesis_writing/defence/slide-plan.md) carries speaker notes and the thesis
section grounding each claim. The deck carries the slides actually being
presented. Nothing connects them. A number corrected on a slide and not in the
plan -- or the reverse -- is invisible until someone reads both side by side.

So: copy the .pptx in as a dated artifact, AND extract slide text and speaker
notes to markdown, so `diff` answers "what changed since last time".

Output, per snapshot:

    <stamp>_<label>/
        deck.pptx            verbatim copy of the source
        deck.md              every slide, in presentation order, one document
        slides/NN-kw-title.md  one per slide -- this is what diffs cleanly
        notes.md             speaker notes only, for rehearsal
        MANIFEST.md          provenance, counts, and the missing-alt-text audit

Slide files are named from the deck's own "KEYWORD | Title" header convention,
so `11-the_gap-extending_ai_agents_with_dedicated_ml_models.md` is findable
without opening it and a directory listing reads as an outline.

What is extracted, and why each was needed: bullet structure with nesting depth
(flattening a list loses the distinction between a heading and its items),
table header rows (PowerPoint flags these on tblPr/@firstRow, not on the row),
and image alt text (cNvPr/@descr), which is where a figure's provenance lives --
which 05_thesis_results/ artefact it came from. The manifest lists every image
still missing alt text, so the gap is a worklist rather than a silence.

Usage:
    python utility_scripts/scripts/deck_snapshot.py --label "first-full-draft"
    python utility_scripts/scripts/deck_snapshot.py --source "C:/path/to.pptx"
    python utility_scripts/scripts/deck_snapshot.py --diff      # vs previous

A .pptx open in PowerPoint is LOCKED on Windows: opening it raises
PermissionError. The file is therefore copied to a temporary path first and
read from the copy, so a snapshot never requires closing the deck. That is not
a nicety -- the common case is snapshotting while editing.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from pathlib import Path

# Resolve every repo path through PATHS.py. Anchored on a repo marker rather
# than a hop-count, which breaks whenever this file moves (path-handling.md).
for _cand in (Path(__file__).resolve().parent, *Path(__file__).resolve().parents):
    if any((_cand / _a).exists() for _a in (".env.example", ".env", "PATHS.py")):
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break
from PATHS import THESIS_DECK_SNAPSHOTS_DIR  # noqa: E402

SNAP_ROOT = THESIS_DECK_SNAPSHOTS_DIR

DEFAULT_SOURCE = (
    r"C:\Users\brian\OneDrive\Documents\02-Areas\MSc. Data Science"
    r"\2026-03 - CBS Master Thesis\Drafts"
    r"\MSc. Data Science - 175888 and 176171 - Oral Defence - Master Thesis.pptx"
)

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
# "Modern comments" (PowerPoint 2018+) and the anchor markers they use. These
# are Microsoft extension namespaces, not ECMA-376 -- comments moved out of the
# slide part into ppt/comments/ and are not in the base standard.
P188 = "{http://schemas.microsoft.com/office/powerpoint/2018/8/main}"
AC = "{http://schemas.microsoft.com/office/drawing/2013/main/command}"
# "Add Section" lives in a 2010 extension list on the presentation part.
P14 = "{http://schemas.microsoft.com/office/powerpoint/2010/main}"


# ---------------------------------------------------------------- extraction

def _para_text(para: ET.Element) -> str:
    """All runs in one paragraph, joined, with no formatting. A <a:br/> is \\n.

    This is the plain-text form, used for comment-offset resolution and table
    cells. `_para_runs` is the formatted form used for rendering.
    """
    out = []
    for node in para.iter():
        if node.tag == f"{A}t":
            out.append(node.text or "")
        elif node.tag == f"{A}br":
            out.append("\n")
    return "".join(out).strip()


def _run_style(rPr: ET.Element | None) -> dict:
    """Character formatting from a run's <a:rPr>.

    Formatting is a property of the RUN, not the paragraph: one line can mix
    bold and plain, which is exactly what the deck does in its "KEYWORD |
    Title" headers. Reading it at paragraph level would lose the distinction.

    `sz` is in hundredths of a point (sz="3200" is 32pt). A run with no `sz`
    inherits from the placeholder or theme, and that inherited value is NOT
    resolved here -- following the inheritance chain through layout and master
    would be a lot of machinery to report a number nobody set deliberately.
    Absent means "inherited", and that is reported as such rather than guessed.
    """
    if rPr is None:
        return {"b": False, "i": False, "u": False, "sz": None, "font": None}
    latin = rPr.find(f"{A}latin")
    font = latin.get("typeface") if latin is not None else None
    # +mn-lt / +mj-lt are theme references, not real typefaces.
    if font and font.startswith("+"):
        font = None
    sz = rPr.get("sz")
    return {
        "b": rPr.get("b") == "1",
        "i": rPr.get("i") == "1",
        "u": (rPr.get("u") or "none") not in ("none", "None"),
        "sz": int(sz) / 100 if sz and sz.isdigit() else None,
        "font": font,
    }


def _para_runs(para: ET.Element) -> list[dict]:
    """Runs of one paragraph, each with its text and character formatting."""
    runs = []
    for node in para:
        if node.tag == f"{A}r":
            t = node.find(f"{A}t")
            text = (t.text or "") if t is not None else ""
            if text:
                runs.append({"text": text, **_run_style(node.find(f"{A}rPr"))})
        elif node.tag == f"{A}br":
            runs.append({"text": "\n", "b": False, "i": False, "u": False,
                         "sz": None, "font": None})
    return runs


def _md_runs(runs: list[dict]) -> str:
    """Runs as markdown, merging adjacent runs that share a style.

    PowerPoint splits a run on every edit, so `**bold**` can arrive as four
    consecutive bold runs. Emitting each separately gives `**b****o****ld**`,
    which renders wrong -- so identical adjacent styles are merged first.

    Underline has no markdown equivalent; <u> is used, which renders in the
    editors this repo's markdown is read in.
    """
    merged: list[dict] = []
    for r in runs:
        key = (r["b"], r["i"], r["u"])
        if merged and (merged[-1]["b"], merged[-1]["i"], merged[-1]["u"]) == key:
            merged[-1]["text"] += r["text"]
        else:
            merged.append(dict(r))

    out = []
    for r in merged:
        text = r["text"]
        stripped = text.strip()
        if not stripped:
            out.append(text)
            continue
        lead = text[:len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]
        # Markers must hug the text -- "** bold **" does not render.
        if r["u"]:
            stripped = f"<u>{stripped}</u>"
        if r["b"]:
            stripped = f"**{stripped}**"
        if r["i"]:
            stripped = f"*{stripped}*"
        out.append(f"{lead}{stripped}{trail}")
    return "".join(out)


def _para(para: ET.Element) -> dict | None:
    """One paragraph with its bullet state and indent depth.

    PowerPoint marks a bullet with <a:buChar>/<a:buAutoNum> inside <a:pPr>, and
    suppresses one with <a:buNone>. Depth is pPr/@lvl, zero-based. A paragraph
    with neither marker is body text and is emitted as a plain line, because
    rendering every paragraph as a bullet is what flattened the earlier export
    and lost the distinction between a heading and its list.

    `marL` is deliberately NOT used as evidence of a bullet: it is set on
    plenty of non-bulleted paragraphs for pure indentation.
    """
    text = _para_text(para)
    if not text:
        return None
    pPr = para.find(f"{A}pPr")
    bullet, kind = False, ""
    if pPr is not None:
        if pPr.find(f"{A}buNone") is not None:
            bullet = False
        elif pPr.find(f"{A}buChar") is not None:
            bullet, kind = True, (pPr.find(f"{A}buChar").get("char") or "•")
        elif pPr.find(f"{A}buAutoNum") is not None:
            bullet, kind = True, "1."
    lvl = int((pPr.get("lvl") if pPr is not None else None) or 0)
    runs = _para_runs(para)
    return {"text": text, "md": _md_runs(runs) or text, "runs": runs,
            "bullet": bullet, "lvl": lvl, "char": kind}


def _shape_meta(sp: ET.Element) -> dict:
    """Where a shape sits, how big its text is, and whether it is a placeholder.

    These three together are what identify a title. XML order does not: shapes
    are stored in z-order, so a 10pt image caption at the foot of the slide can
    precede the 32pt headline. That is exactly how slide 4's caption ("* AI
    generated image, based on real article") was once picked as its title.
    """
    nv = sp.find(f"{P}nvSpPr/{P}cNvPr")
    ph = sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
    off = sp.find(f"{P}spPr/{A}xfrm/{A}off")
    sizes = [int(r.get("sz")) / 100 for r in sp.iter(f"{A}rPr")
             if r.get("sz") and r.get("sz").isdigit()]
    return {
        "id": nv.get("id") if nv is not None else None,
        "name": nv.get("name") if nv is not None else "",
        "ph": ph.get("type") if ph is not None else None,
        "is_ph": ph is not None,
        # EMU -> inches. None where the shape inherits its position.
        "y": int(off.get("y")) / 914400 if off is not None and off.get("y") else None,
        "max_sz": max(sizes) if sizes else None,
    }


def _shape_blocks(root: ET.Element, note: list | None = None) -> list[list[dict]]:
    """One block of paragraphs per text-bearing shape, in document order.

    Kept per shape rather than flattened, because a slide's title and its
    bullet list are different shapes and collapsing them loses the structure
    that makes a diff readable. Each block carries its shape metadata under a
    leading `_meta` key so the title heuristic can use it.
    """
    tree = root.find(f"{P}cSld/{P}spTree")
    return _walk_tree(tree if tree is not None else root, note)


def _shape_box(node: ET.Element) -> tuple[float, float, float]:
    """(top, left, bottom) of a shape or group, in inches.

    The bottom edge is what makes column detection possible: two shapes belong
    to the same horizontal band when their vertical extents overlap, and that
    cannot be decided from the top edge alone.
    """
    for pfx in (f"{P}spPr/{A}xfrm", f"{P}grpSpPr/{A}xfrm"):
        xfrm = node.find(pfx)
        if xfrm is None:
            continue
        off, ext = xfrm.find(f"{A}off"), xfrm.find(f"{A}ext")
        if off is not None and off.get("x") and off.get("y"):
            top = int(off.get("y")) / 914400
            left = int(off.get("x")) / 914400
            cy = int(ext.get("cy")) / 914400 if ext is not None and ext.get("cy") else 0.0
            return top, left, top + cy
    return float("inf"), float("inf"), float("inf")


def _shape_pos(node: ET.Element) -> tuple[float, float]:
    """Top-left of a shape or group, in inches. (inf, inf) when it inherits."""
    for path in (f"{P}spPr/{A}xfrm/{A}off", f"{P}grpSpPr/{A}xfrm/{A}off"):
        off = node.find(path)
        if off is not None and off.get("x") and off.get("y"):
            return int(off.get("y")) / 914400, int(off.get("x")) / 914400
    return float("inf"), float("inf")


def _walk_tree(node: ET.Element, note: list | None = None) -> list[list[dict]]:
    """Text blocks in READING order: top-to-bottom, left-to-right, groups kept
    whole and recursed into.

    Three things make raw XML order wrong, and all three bit this deck:

    1. **It is z-order, not reading order.** Slide 5's three boxes are stored
       bottom-to-top (Goal at y=5.79 before Offering at y=1.56).
    2. **`root.iter()` flattens groups.** A group is one visual unit -- a
       heading and its bullets -- and flattening interleaves it with whatever
       else the document order happens to contain.
    3. **Inside a group the order is arbitrary too.** Slide 5's groups store
       their bullets textbox BEFORE their title textbox, which is why "Goal"
       printed after its own bullets and appeared to belong to the box above.

    PowerPoint's own Reading Order pane reorders only TOP-LEVEL shapes, so it
    cannot fix (3) -- which is why Brian's change did not move that heading.
    Sorting by position does, and it needs no manual upkeep.

    Shapes with no explicit position (they inherit from a placeholder) sort
    last within their level rather than being dropped.
    """
    items: list[tuple[tuple[float, float], list[list[dict]]]] = []
    for ch in node:
        tag = ch.tag
        if tag == f"{P}grpSp":
            inner = _walk_tree(ch)
            if inner:
                items.append((_shape_box(ch), inner))
        elif tag == f"{P}sp":
            meta = _shape_meta(ch)
            # Slide-number, date and footer placeholders are chrome: they
            # render a field, carry no authored content, and leak a bare "5"
            # into the export as diff noise on every renumber.
            if meta.get("ph") in ("sldNum", "dt", "ftr"):
                continue
            paras = [p for p in (_para(x) for x in ch.iter(f"{A}p")) if p]
            if paras:
                paras[0] = dict(paras[0], _meta=meta)
                items.append((_shape_box(ch), [paras]))

    return _band_sort(items, note)


def _band_sort(items: list[tuple[tuple[float, float, float], list]],
               note: list | None = None) -> list:
    """Reading order for a possibly multi-COLUMN layout.

    Sorting strictly by (top, left) is right for a stacked layout and wrong for
    a side-by-side one. Slide 15 is three columns -- RESEARCH / FORECASTING /
    DESIGN SCIENCE, each a heading box at y=1.53 above its own bullets at
    y=2.6. Strict top-to-bottom emits all three headings, then all three bullet
    lists, so every bullet appears to belong to the last heading printed.

    Instead group shapes into horizontal BANDS: a shape opens a band, and any
    later shape whose vertical extent overlaps that band joins it. Within a
    band, read left-to-right; bands themselves run top-to-bottom. A single
    column collapses to one shape per band, which is the stacked case
    unchanged.

    Overlap is required to exceed a small fraction of the shape's own height,
    so a caption that merely grazes the box above it does not get absorbed.
    """
    if not items:
        return []
    placed = [it for it in items if it[0][0] != float("inf")]
    floating = [it for it in items if it[0][0] == float("inf")]

    placed.sort(key=lambda it: (it[0][0], it[0][1]))
    bands: list[list] = []
    for it in placed:
        top, left, bottom = it[0]
        height = max(bottom - top, 0.01)
        for band in bands:
            b_top = min(x[0][0] for x in band)
            b_bottom = max(x[0][2] for x in band)
            overlap = min(bottom, b_bottom) - max(top, b_top)
            if overlap > 0.5 * min(height, b_bottom - b_top or height):
                band.append(it)
                break
        else:
            bands.append([it])

    for band in bands:
        band.sort(key=lambda it: it[0][1])          # left to right

    # A layout can be columnar ACROSS bands too: slide 25 puts both headings in
    # one band (y=0.18) and both bullet lists in the next (y=0.80), so
    # band-by-band reading still emits heading, heading, bullets, bullets.
    #
    # The signal that distinguishes this from a genuine stack is that the same
    # left edges recur in band after band. Where every band shares the same
    # column positions, read COLUMN-major: all of column 1 top-to-bottom, then
    # column 2. Otherwise read band-major, which is the ordinary case.
    out = []
    lefts = [tuple(round(it[0][1], 1) for it in band) for band in bands]
    columnar = (len(bands) > 1 and len(lefts[0]) > 1
                and all(l == lefts[0] for l in lefts))
    if note is not None:
        if columnar:
            note.append(f"{len(lefts[0])} columns x {len(bands)} bands "
                        "(read column-major)")
        elif any(len(b) > 1 for b in bands):
            note.append(f"{max(len(b) for b in bands)} columns "
                        "(read left-to-right within each row)")
    if columnar:
        for col in range(len(lefts[0])):
            for band in bands:
                out.extend(blk for blk in band[col][1])
    else:
        for band in bands:
            for _, blocks in band:
                out.extend(blocks)

    for _, blocks in floating:                      # inherited position: last
        out.extend(blocks)
    return out


def _table_rows(root: ET.Element) -> list[dict]:
    """Every table as {header, rows}.

    A PowerPoint table marks its header row on <a:tblPr firstRow="1">, not on
    the row itself. Where that flag is set the first row becomes the markdown
    header so the exported table renders as a table rather than as a wall of
    pipes; where it is not, no header is invented.
    """
    tables = []
    for tbl in root.iter(f"{A}tbl"):
        pr = tbl.find(f"{A}tblPr")
        first_is_header = bool(pr is not None and pr.get("firstRow") == "1")
        rows = []
        # Runs are kept flat alongside the rendered rows so the typography
        # audit sees table text too -- a font used only inside tables is
        # exactly the kind of inconsistency that hides from a per-slide read.
        cell_runs: list[dict] = []
        for tr in tbl.iter(f"{A}tr"):
            cells = []
            for tc in tr.iter(f"{A}tc"):
                # Multi-paragraph cells are joined with <br> so the row stays
                # on one markdown line; a raw newline would break the table.
                parts = []
                for p in tc.iter(f"{A}p"):
                    rr = _para_runs(p)
                    cell_runs.extend(rr)
                    md = _md_runs(rr).strip() or _para_text(p)
                    # A pipe inside a cell would end the column early.
                    if md:
                        parts.append(md.replace("|", "\\|"))
                cells.append(" <br> ".join(parts))
            if any(c.strip() for c in cells):
                rows.append(cells)
        if rows:
            tables.append({"header": rows[0] if first_is_header else None,
                           "rows": rows[1:] if first_is_header else rows,
                           "runs": cell_runs})
    return tables


def _images(root: ET.Element, rels: dict[str, str] | None = None) -> list[dict]:
    """Pictures with their alt text.

    PowerPoint stores alt text on cNvPr/@descr (the "Description" field in the
    Alt Text pane); @title is the rarely-used "Title" field. Capturing both
    means a figure's provenance -- which 05_thesis_results/ SVG it came from --
    travels into the snapshot and can be diffed like anything else.
    """
    out = []
    # Collected BEFORE the walk: a set built mid-iteration only suppresses
    # children encountered after their group, which is why the first attempt
    # double-counted and reported 93 visuals where there are 72.
    inside_group: set[int] = set()
    for grp in root.iter(f"{P}grpSp"):
        nv = grp.find(f"{P}nvGrpSpPr/{P}cNvPr")
        if nv is not None and (nv.get("descr") or "").strip():
            for child in grp.iter(f"{P}pic"):
                inside_group.add(id(child))
    # A visual is not always a <p:pic>. Alt text is equally valid on a GROUP
    # (several shapes described as one figure) and on a GRAPHIC FRAME (a chart
    # or SmartArt). Reading only p:pic reported 28 of 68 here and looked like
    # the author had not written the text -- when in fact 17 group and 4 frame
    # descriptions were simply never looked at.
    for tag, nv_path in ((f"{P}pic", f"{P}nvPicPr/{P}cNvPr"),
                         (f"{P}grpSp", f"{P}nvGrpSpPr/{P}cNvPr"),
                         (f"{P}graphicFrame", f"{P}nvGraphicFramePr/{P}cNvPr")):
        for node in root.iter(tag):
            nv = node.find(nv_path)
            if nv is None:
                continue
            # A picture inside a DESCRIBED group is reported once, by the
            # group -- the group's alt text describes the whole figure.
            if id(node) in inside_group:
                continue
            # An undescribed group is a layout container, not a figure; its
            # children are reported individually instead.
            if tag == f"{P}grpSp" and not (nv.get("descr") or "").strip():
                continue
            # The media file is the stable identity. Shape NAMES are not:
            # the same logo is "Picture 15" on one slide and "Picture 43" on
            # the next, so name-matching cannot recognise a repeated asset.
            blip = node.find(f"{P}blipFill/{A}blip")
            embed = blip.get(f"{R}embed") if blip is not None else None
            media = (rels or {}).get(embed or "", "").split("/")[-1]
            out.append({
                "name": nv.get("name") or "",
                "descr": (nv.get("descr") or "").strip(),
                "title": (nv.get("title") or "").strip(),
                "media": media,
                "kind": {f"{P}pic": "image", f"{P}grpSp": "group"}.get(tag, "graphic"),
            })
    return out


def _authors(z: zipfile.ZipFile) -> dict[str, str]:
    """authorId -> display name, from ppt/authors.xml."""
    if "ppt/authors.xml" not in z.namelist():
        return {}
    root = ET.fromstring(z.read("ppt/authors.xml"))
    out = {}
    for a in root.iter(f"{P188}author"):
        out[a.get("id", "")] = a.get("name") or a.get("initials") or "unknown"
    return out


def _shape_plaintext(sp: ET.Element) -> str:
    """A shape's text as PowerPoint counts it for comment offsets.

    Paragraphs are joined with a single newline, because that is the unit the
    `cp` character offset in <ac:txMk> is measured against. Getting this wrong
    silently shifts every anchor on the slide.
    """
    paras = []
    for p in sp.iter(f"{A}p"):
        paras.append("".join(t.text or "" for t in p.iter(f"{A}t")))
    return "\n".join(paras)


def _comments_for(z: zipfile.ZipFile, slide_part: str,
                  authors: dict[str, str]) -> list[dict]:
    """Comments on one slide, each resolved back to the text it anchors to.

    PowerPoint 2018+ stores these as "modern comments" in ppt/comments/, linked
    from the slide's .rels. The anchor is a character range -- <ac:spMk id=…>
    names the shape and <ac:txMk cp=… len=…> the offset and length within it --
    so the quoted text can be reconstructed rather than guessed at.

    That reconstruction is the whole point: a comment saying "not sure of the
    numbers" is unusable without knowing which number it sits on.

    The older <p:cmLst> format is not handled. This deck does not use it, and
    inventing an untested code path for a format we may never see is worse than
    not having one -- it would look supported and quietly produce nothing.
    """
    rel = f"ppt/slides/_rels/{slide_part.split('/')[-1]}.rels"
    if rel not in z.namelist():
        return []
    parts = [r.get("Target") for r in ET.fromstring(z.read(rel))
             if "comment" in (r.get("Type") or "").lower()]
    if not parts:
        return []

    # Shape id -> its plain text, for offset resolution.
    slide = ET.fromstring(z.read(slide_part))
    shapes = {}
    for sp in slide.iter(f"{P}sp"):
        nv = sp.find(f"{P}nvSpPr/{P}cNvPr")
        if nv is not None and nv.get("id"):
            shapes[nv.get("id")] = _shape_plaintext(sp)

    out = []
    for tgt in parts:
        part = "ppt/" + (tgt or "").replace("../", "")
        if part not in z.namelist():
            continue
        for cm in ET.fromstring(z.read(part)).iter(f"{P188}cm"):
            body = cm.find(f"{P188}txBody")
            text = "\n".join(
                t for t in ((_para_text(p) for p in body.iter(f"{A}p")) if body is not None else [])
                if t)
            sp_mk = next(cm.iter(f"{AC}spMk"), None)
            tx_mk = next(cm.iter(f"{AC}txMk"), None)
            anchor, context = "", ""
            if sp_mk is not None and tx_mk is not None:
                full = shapes.get(sp_mk.get("id") or "", "")
                try:
                    cp, ln = int(tx_mk.get("cp") or 0), int(tx_mk.get("len") or 0)
                except ValueError:
                    cp = ln = 0
                if full and 0 <= cp <= len(full):
                    anchor = full[cp:cp + ln].strip()
                    lo, hi = max(0, cp - 60), min(len(full), cp + ln + 60)
                    context = full[lo:hi].replace("\n", " ").strip()
            out.append({
                "author": authors.get(cm.get("authorId", ""), "unknown"),
                "created": (cm.get("created") or "")[:16].replace("T", " "),
                "text": text,
                "anchor": anchor,
                "context": context,
            })
    return out


def _sections(z: zipfile.ZipFile) -> dict[int, str]:
    """Slide number (1-based) -> the "Add Section" name it belongs to.

    Sections live in an extension list on the presentation, under the 2010
    p14 namespace, as a list of section names each holding slide IDs. They are
    the author's own structure -- this deck's are already numbered
    ("01_Background & Motivation") -- so prefixing a filename with the section
    makes a directory listing sort into presentation order AND read as the
    outline the author built.

    Slides in no section, or a deck with no sections at all, simply get no
    prefix rather than an invented one.
    """
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    lst = pres.find(f"{P}sldIdLst")
    if lst is None:
        return {}
    pos = {s.get("id"): i for i, s in enumerate(lst, 1)}
    out: dict[int, str] = {}
    for sec in pres.iter(f"{P14}section"):
        name = sec.get("name") or ""
        for sid in sec.iter(f"{P14}sldId"):
            n = pos.get(sid.get("id"))
            if n:
                out[n] = name
    return out


def _ordered_slides(z: zipfile.ZipFile) -> list[str]:
    """Slide parts in PRESENTATION order, not filename order.

    slide12.xml sorts before slide2.xml lexically, and PowerPoint reorders
    slides without renaming their parts -- so the sldIdLst is the only
    authority on what order the deck is actually in.
    """
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    rels = ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
    rmap = {r.get("Id"): r.get("Target") for r in rels}
    order = []
    lst = pres.find(f"{P}sldIdLst")
    if lst is None:
        return sorted(n for n in z.namelist()
                      if n.startswith("ppt/slides/slide") and n.endswith(".xml"))
    for sid in lst:
        tgt = rmap.get(sid.get(f"{R}id"))
        if tgt:
            order.append("ppt/" + tgt.replace("../", ""))
    return order


def _notes_for(z: zipfile.ZipFile, slide_part: str) -> str:
    """Speaker notes for one slide, or ''. Drops the slide-number placeholder."""
    rel = f"ppt/slides/_rels/{slide_part.split('/')[-1]}.rels"
    if rel not in z.namelist():
        return ""
    for r in ET.fromstring(z.read(rel)):
        tgt = r.get("Target") or ""
        if "notesSlide" in tgt:
            part = "ppt/notesSlides/" + tgt.split("/")[-1]
            if part not in z.namelist():
                return ""
            root = ET.fromstring(z.read(part))
            lines = [t for t in (_para_text(p) for p in root.iter(f"{A}p"))
                     if t and not t.isdigit()]
            return "\n\n".join(lines)
    return ""


def read_pptx(path: Path) -> dict:
    """Parse a .pptx into ordered slides with text, tables, notes and counts."""
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        authors = _authors(z)
        sections = _sections(z)
        slides = []
        for i, part in enumerate(_ordered_slides(z), 1):
            if part not in names:
                continue
            root = ET.fromstring(z.read(part))
            srel = f"ppt/slides/_rels/{part.split('/')[-1]}.rels"
            rmap = ({r.get("Id"): r.get("Target")
                     for r in ET.fromstring(z.read(srel))}
                    if srel in names else {})
            layout_note: list[str] = []
            imgs = _images(root, rmap)
            slides.append({
                "index": i,
                "part": part.split("/")[-1],
                "blocks": _shape_blocks(root, layout_note),
                "tables": _table_rows(root),
                "images": imgs,
                "notes": _notes_for(z, part),
                "comments": _comments_for(z, part, authors),
                "section": sections.get(i, ""),
                "layout_note": "; ".join(layout_note),
                "pics": len(imgs),
                "charts": len(list(root.iter(f"{P}graphicFrame"))),
            })
        media = sorted(n.split("/")[-1] for n in names if n.startswith("ppt/media/"))
    return {"slides": slides, "media": media, "authors": authors,
            "sections": sections}


# ------------------------------------------------------------------- writing

def _title_of(slide: dict) -> str:
    """The slide's headline, by placeholder if it has one, else by typography.

    Shapes are stored in z-order, not reading order, so "first shape with text"
    is not the title -- on slide 4 it picked a 10pt image caption sitting at the
    foot of the slide over the 32pt headline at the top.

    Two passes, in order of authority:

    1. **A real title placeholder** (`ph type="title"` / `ctrTitle`). Where
       PowerPoint has been told what the title is, that is the answer.
    2. **Typography and position.** Largest text wins; ties break upward. This
       matches how a reader identifies a headline, and it is what the free-form
       text boxes in this deck require -- most carry no placeholder at all.

    A shape with no explicit size is skipped in pass 2 rather than assumed
    small: it inherits, and inherited text is rarely the headline.
    """
    metas = []
    for blk in slide["blocks"]:
        meta = blk[0].get("_meta") or {}
        text = next((p["text"].strip() for p in blk if p["text"].strip()), "")
        if text:
            metas.append((meta, text))

    for meta, text in metas:
        if meta.get("ph") in ("title", "ctrTitle"):
            return text

    sized = [(m, t) for m, t in metas if m.get("max_sz")]
    if sized:
        biggest = max(m["max_sz"] for m, _ in sized)
        top = [(m, t) for m, t in sized if m["max_sz"] == biggest]
        # A clear winner on size is the title. A TIE is not evidence -- six
        # agenda items all at 24pt are a list, not six candidate headlines --
        # so a tie falls through to position, where an inherited-size shape
        # above them all can still win.
        if len(top) == 1:
            return top[0][1]

    # Position decides when size cannot: nothing carries an explicit size
    # (every shape inherits), or the largest size is tied across shapes.
    # Highest on the slide wins, which is where a headline sits.
    placed = [(m, t) for m, t in metas if m.get("y") is not None]
    if placed:
        placed.sort(key=lambda mt: mt[0]["y"])
        return placed[0][1]

    return metas[0][1] if metas else f"(untitled slide {slide['index']})"


def _split_title(title: str) -> tuple[str, str]:
    """Split the deck's "KEYWORD | Title" convention into its two halves.

    The deck titles slides as `THE GAP | Extending AI Agents with dedicated ML
    Models`. Both halves matter and they matter differently: the keyword is the
    section, the remainder is the claim. Splitting them here is what lets the
    filename carry both, so a directory listing reads as an outline.

    Only the FIRST pipe splits -- a title containing further pipes keeps them in
    the second half rather than being chopped into three.
    """
    if "|" not in title:
        return title.strip(), ""
    head, _, tail = title.partition("|")
    return head.strip(), tail.strip()


def _slug(text: str, limit: int = 48, sep: str = "_") -> str:
    s = re.sub(r"[^a-z0-9]+", sep, text.lower()).strip(sep)
    return s[:limit].rstrip(sep) or "slide"


def _slide_filename(slide: dict) -> str:
    """`NN-section-keyword-title.md`, from the deck's own structure.

    Three segments, each from something the author set rather than something
    inferred: the slide number, the "Add Section" it belongs to, and the
    "KEYWORD | Title" header. A directory listing then sorts in presentation
    order and reads as the outline.

    Each segment degrades independently -- no section, or no pipe in the title,
    drops that segment rather than inventing an empty one.
    """
    kw, rest = _split_title(_title_of(slide))
    sec = slide.get("section") or ""
    # "Default Section" is PowerPoint's name for slides the author never
    # sectioned -- it is the absence of a choice, so it earns no prefix.
    sec_slug = ""
    if sec and sec.strip().lower() != "default section":
        sec_slug = _slug(sec, 24)

    # The section is bracketed and upper-cased so a directory listing groups
    # visually at a glance. Square brackets are legal on Windows -- only
    # < > : " / \ | ? * are reserved -- and sort before alphanumerics, which
    # keeps the numeric prefix doing the ordering.
    prefix = f"{slide['index']:02d}"
    parts = [f"{prefix}-[{sec_slug.upper()}]" if sec_slug else prefix]

    # A section title repeated as the slide title ("03_Methodology" ->
    # "METHODOLOGY") would stutter in the filename, so the duplicate is dropped.
    head = _slug(kw, 24) if rest else _slug(kw, 40)
    if sec_slug and head and head in sec_slug:
        head = ""
    if head:
        parts.append(head)
    if rest:
        parts.append(_slug(rest, 40))
    return "-".join(parts) + ".md"


def _render_paras(paras: list[dict]) -> list[str]:
    """Paragraphs as markdown: bullets indented by level, body text plain."""
    out = []
    for p in paras:
        text = p.get("md", p["text"]).replace("\n", " ")
        if p["bullet"]:
            out.append(f"{'  ' * p['lvl']}- {text}")
        else:
            if out and out[-1].lstrip().startswith("-"):
                out.append("")
            out.append(text)
    return out


def _render_table(tbl: dict) -> list[str]:
    """A markdown table, with a header row only where PowerPoint marks one."""
    out = []
    header, rows = tbl["header"], tbl["rows"]
    width = max([len(header)] if header else [0] + [len(r) for r in rows] or [0])

    def row(cells: list[str]) -> str:
        padded = list(cells) + [""] * (width - len(cells))
        return "| " + " | ".join(c.strip() or " " for c in padded) + " |"

    if header:
        out.append(row(header))
        out.append("|" + "---|" * width)
    for r in rows:
        out.append(row(r))
    return out


def _render_slide(slide: dict) -> str:
    """One slide as markdown. Shapes separated so a diff localises a change."""
    title = _title_of(slide)
    kw, rest = _split_title(title)
    heading = f"{kw} — {rest}" if rest else kw
    out = [f"## Slide {slide['index']:02d} — {heading}", ""]

    meta_line = []
    if slide.get("section"):
        meta_line.append(f"*Section:* **{slide['section']}**")
    if rest:
        meta_line.append(f"*Keyword:* **{kw}**")
    if meta_line:
        out += [" · ".join(meta_line), ""]

    for blk in slide["blocks"]:
        out += _render_paras(blk)
        out.append("")

    for tbl in slide["tables"]:
        out += _render_table(tbl)
        out.append("")

    if slide["images"]:
        out += ["### Images", ""]
        for img in slide["images"]:
            if img["descr"]:
                out.append(f"- **{img['name']}** — {img['descr']}")
            else:
                out.append(f"- **{img['name']}** — ⚠ *no alt text*")
        out.append("")

    out += ["### Speaker notes", "",
            slide["notes"] if slide["notes"] else "*(none)*", ""]

    if slide["comments"]:
        out += ["### Comments", ""]
        for c in slide["comments"]:
            head = f"**{c['author']}**"
            if c["created"]:
                head += f" · {c['created']}"
            out.append(head)
            if c["anchor"]:
                out += ["", f"> On: *“{c['anchor']}”*"]
            elif c["context"]:
                out += ["", f"> Near: *“{c['context']}”*"]
            out += ["", c["text"] or "*(empty comment)*", ""]
    return "\n".join(out)


def _write(d: dict, out_dir: Path, src: Path, sha: str) -> None:
    (out_dir / "slides").mkdir(parents=True, exist_ok=True)

    full = ["# Oral defence deck", "",
            f"> Generated by `deck_snapshot.py` from `{src.name}`.",
            "> **Read-only.** Edit the OneDrive .pptx, then re-snapshot.", ""]
    notes_doc = ["# Speaker notes", "",
                 "> Notes only, in presentation order — for rehearsal.", ""]

    for s in d["slides"]:
        body = _render_slide(s)
        full.append(body)
        (out_dir / "slides" / _slide_filename(s)).write_text(body, encoding="utf-8")
        if s["notes"]:
            notes_doc += [f"## Slide {s['index']:02d} — {_title_of(s)}", "",
                          s["notes"], ""]

    (out_dir / "deck.md").write_text("\n".join(full), encoding="utf-8")
    (out_dir / "notes.md").write_text("\n".join(notes_doc), encoding="utf-8")

    # Comments get their own file: they are a worklist, and hunting them across
    # 40 slide files is exactly the friction that leaves them unactioned.
    all_comments = [(s, c) for s in d["slides"] for c in s["comments"]]
    cdoc = ["# Comments", "",
            "> Every comment in the deck, in slide order, with the text it is "
            "anchored to.", ""]
    if all_comments:
        cdoc += [f"**{len(all_comments)}** comment(s) across "
                 f"{len({s['index'] for s, _ in all_comments})} slide(s).", ""]
        for s, c in all_comments:
            cdoc += [f"## Slide {s['index']:02d} — {_title_of(s)}", "",
                     f"**{c['author']}**"
                     + (f" · {c['created']}" if c["created"] else ""), ""]
            if c["anchor"]:
                cdoc += [f"> On: *“{c['anchor']}”*", ""]
            if c["context"] and c["context"] != c["anchor"]:
                cdoc += [f"Context: …{c['context']}…", ""]
            cdoc += [c["text"] or "*(empty comment)*", ""]
    else:
        cdoc += ["*No comments in this version of the deck.*", ""]
    (out_dir / "comments.md").write_text("\n".join(cdoc), encoding="utf-8")

    with_notes = sum(1 for s in d["slides"] if s["notes"])
    words = sum(len(s["notes"].split()) for s in d["slides"])
    _n = Counter(i.get("media") or i["name"]
                 for s in d["slides"] for i in s["images"])
    _chrome = {n for n, c in _n.items() if c >= len(d["slides"]) * 0.5}
    imgs = [i for s in d["slides"] for i in s["images"]
            if (i.get("media") or i["name"]) not in _chrome]
    with_alt = [i for i in imgs if i["descr"]]
    bullets = sum(1 for s in d["slides"] for b in s["blocks"]
                  for p in b if p["bullet"])

    man = [
        "# Deck snapshot manifest", "",
        "| | |", "|---|---|",
        f"| Source | `{src.name}` |",
        f"| Source SHA-256 | `{sha[:16]}…` |",
        f"| Snapshotted | {datetime.now():%Y-%m-%d %H:%M:%S} |",
        f"| Slides | **{len(d['slides'])}** |",
        f"| Slides with notes | **{with_notes}** of {len(d['slides'])} |",
        f"| Words of notes | **{words:,}** |",
        f"| Bullet paragraphs | {bullets} |",
        f"| Tables | {sum(len(s['tables']) for s in d['slides'])} |",
        f"| Images with alt text | **{len(with_alt)}** of {len(imgs)} |",
        f"| Comments | **{sum(len(s['comments']) for s in d['slides'])}** |",
        f"| Sections | {len({s.get('section') for s in d['slides'] if s.get('section')})} |",
        f"| Media files | {len(d['media'])} |",
        "",
        "## Slides", "",
    ]
    # Grouped by section, because that is the structure the author built and a
    # flat 40-row table hides it.
    HDR = ["| # | Keyword | Title | Img | Alt | Tbl | Notes | Cmt |",
           "|---:|---|---|---:|---:|---:|---:|---:|"]
    current = object()
    for s in d["slides"]:
        if s.get("section", "") != current:
            current = s.get("section", "")
            man += ["", f"### {current or '(no section)'}", ""] + HDR
        kw, rest = _split_title(_title_of(s))
        alt = sum(1 for i in s["images"] if i["descr"])
        man.append(
            f"| {s['index']} | {kw[:28]} | {rest[:48]} | {s['pics']} | "
            f"{alt} | {len(s['tables'])} | "
            f"{len(s['notes'].split()) if s['notes'] else 0} | "
            f"{len(s['comments']) or ''} |")

    # --- typography audit -------------------------------------------------
    # The point is consistency, not inventory: a font used twice against one
    # used 264 times is a slip, and it is invisible slide by slide.
    fonts: Counter = Counter()
    sizes: Counter = Counter()
    font_slides: dict[str, set] = {}
    emph = Counter()
    for s in d["slides"]:
        runs_here = [r for blk in s["blocks"] for para in blk
                     for r in para.get("runs", [])]
        runs_here += [r for tbl in s["tables"] for r in tbl.get("runs", [])]
        for r in runs_here:
            if not r["text"].strip():
                continue
            if r["font"]:
                fonts[r["font"]] += 1
                font_slides.setdefault(r["font"], set()).add(s["index"])
            if r["sz"]:
                sizes[r["sz"]] += 1
            for k in ("b", "i", "u"):
                if r[k]:
                    emph[k] += 1

    man += ["", "## Typography", "",
            f"**Emphasis:** {emph['b']} bold · {emph['i']} italic · "
            f"{emph['u']} underline runs.", ""]
    if fonts:
        man += ["| Typeface | Runs | Slides |", "|---|---:|---|"]
        for f, n in fonts.most_common():
            sl = sorted(font_slides[f])
            shown = ", ".join(str(x) for x in sl[:8]) + ("…" if len(sl) > 8 else "")
            man.append(f"| `{f}` | {n} | {shown} |")
        if len(fonts) > 1:
            odd = [f for f, n in fonts.items() if n < max(fonts.values()) * 0.25]
            if odd:
                man += ["", f"⚠ **{len(odd)} minority typeface(s)** against "
                        f"`{fonts.most_common(1)[0][0]}` — likely pasted-in "
                        "formatting rather than a deliberate choice: "
                        + ", ".join(f"`{f}`" for f in odd) + ".", ""]
    if sizes:
        man += ["", "| Size (pt) | Runs |", "|---:|---:|"]
        for szv, n in sorted(sizes.items()):
            man.append(f"| {szv:g} | {n} |")
        man += ["", "*Runs with no explicit size inherit from the layout and "
                "are not counted.*", ""]

    # A visual that repeats on nearly every slide is template chrome -- a logo
    # or a placeholder -- not a figure. Listing it 38 times buries the handful
    # of real gaps, so it is counted once and named rather than enumerated.
    name_slides = Counter(i.get("media") or i["name"]
                          for s in d["slides"] for i in s["images"]
                          if not i["descr"])
    chrome = {n for n, c in name_slides.items() if c >= len(d["slides"]) * 0.5}
    # --- layout audit ---------------------------------------------------
    # Reading order is INFERRED from geometry, so it can be wrong on a layout
    # nobody anticipated. This reports the slides where the inference had to
    # work hardest, so they get looked at rather than trusted silently.
    tricky = [s for s in d["slides"] if s.get("layout_note")]
    if tricky:
        man += ["", "## Layout — slides whose reading order was inferred", "",
                "These carry a multi-column or banded layout, so the order "
                "below was derived from shape geometry rather than read off "
                "the file. **Check these when the deck changes.**", "",
                "| Slide | Title | Layout |", "|---:|---|---|"]
        for s in tricky:
            man.append(f"| {s['index']} | {_title_of(s)[:52]} | "
                       f"{s['layout_note']} |")
        man.append("")

    missing = [(s["index"], i["name"]) for s in d["slides"]
               for i in s["images"]
               if not i["descr"] and (i.get("media") or i["name"]) not in chrome]
    if missing:
        man += ["", "## Images still without alt text", "",
                "Alt text is where a figure's provenance lives — which "
                "`05_thesis_results/` artefact it came from. Without it the "
                "snapshot records that an image exists and nothing about what "
                "it shows.", "",
                "| Slide | Shape |", "|---:|---|"]
        man += [f"| {n} | {nm} |" for n, nm in missing]
    if chrome:
        man += ["", f"*Excluded as template chrome (present on most slides): "
                + ", ".join(f"`{n}`" for n in sorted(chrome)) + ".*", ""]

    (out_dir / "MANIFEST.md").write_text("\n".join(man), encoding="utf-8")


# ---------------------------------------------------------------------- diff

def _diff(prev: Path, new: Path) -> None:
    """Which slides were added, removed or edited since the previous snapshot."""
    import difflib

    def load(d: Path) -> dict:
        # Keyed on slide NUMBER, not filename. Renaming a section rewrites
        # every filename in it, and a filename-keyed diff then reports the
        # whole deck as removed-and-re-added -- burying the one slide that
        # actually changed.
        out = {}
        for f in sorted((d / "slides").glob("*.md")):
            num = f.name.split("-", 1)[0]
            out[num] = (f.name, f.read_text(encoding="utf-8"))
        return out

    a, b = load(prev), load(new)
    added = [k for k in b if k not in a]
    removed = [k for k in a if k not in b]
    changed = [k for k in a if k in b and a[k][1] != b[k][1]]
    renamed = [k for k in a if k in b and a[k][0] != b[k][0]
               and a[k][1] == b[k][1]]

    print(f"\n  vs {prev.name}")
    if not (added or removed or changed or renamed):
        print("  no change")
        return
    for k in added:
        print(f"  + added    {b[k][0][:-3]}")
    for k in removed:
        print(f"  - removed  {a[k][0][:-3]}")
    for k in sorted(changed):
        n = sum(1 for ln in difflib.unified_diff(
            a[k][1].splitlines(), b[k][1].splitlines(), n=0) if ln[:1] in "+-")
        note = "  (also renamed)" if a[k][0] != b[k][0] else ""
        print(f"  ~ edited   {b[k][0][:-3]}  ({n} line(s)){note}")
    for k in sorted(renamed):
        print(f"  » renamed  {a[k][0][:-3]}\n             -> {b[k][0][:-3]}")


# ---------------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Snapshot the oral-defence .pptx into a diffable mirror.")
    ap.add_argument("--source", type=Path, default=Path(DEFAULT_SOURCE))
    ap.add_argument("--label", default="deck",
                    help="short slug appended to the timestamped folder name")
    ap.add_argument("--diff", action="store_true",
                    help="also diff against the previous snapshot")
    args = ap.parse_args()

    if not args.source.is_file():
        sys.exit(f"No such file: {args.source}")

    # A deck open in PowerPoint is locked. Copy first, always -- the common
    # case is snapshotting mid-edit, and failing there would make the tool
    # something you have to plan around instead of something you just run.
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "deck.pptx"
        try:
            shutil.copy2(args.source, work)
        except PermissionError:
            sys.exit("Could not read the .pptx even to copy it. Close it and retry.")

        sha = hashlib.sha256(work.read_bytes()).hexdigest()
        data = read_pptx(work)

        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        out_dir = SNAP_ROOT / f"{stamp}_{_slug(args.label)}"
        out_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(work, out_dir / "deck.pptx")
        _write(data, out_dir, args.source, sha)

    rel = out_dir.relative_to(SNAP_ROOT.parents[2])
    with_notes = sum(1 for s in data["slides"] if s["notes"])
    print(f"snapshot -> {rel}")
    print(f"  slides   : {len(data['slides'])}")
    print(f"  notes    : {with_notes} slide(s), "
          f"{sum(len(s['notes'].split()) for s in data['slides']):,} words")
    print(f"  media    : {len(data['media'])}")
    print(f"  wrote    : deck.md, notes.md, slides/, MANIFEST.md")

    if args.diff:
        prev = sorted((p for p in SNAP_ROOT.iterdir()
                       if p.is_dir() and p != out_dir), reverse=True)
        if prev:
            _diff(prev[0], out_dir)
        else:
            print("\n  no previous snapshot to diff against")

    print("\ndone. Snapshot is read-only; edit the OneDrive .pptx.")


if __name__ == "__main__":
    main()
