"""Extract comments + anchored text from a .docx using only the stdlib.

A .docx is a zip of XML parts. Comments live in word/comments.xml; the text they
attach to is delimited in word/document.xml by commentRangeStart/End markers
carrying the same id. No third-party library is required, which matters here
because the venv has neither python-docx nor pandoc.

Usage:
    python docx_comments.py <file.docx> [--json]
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _text(el) -> str:
    """All w:t descendants joined, with tabs/breaks rendered as whitespace."""
    out = []
    for node in el.iter():
        if node.tag == f"{W}t":
            out.append(node.text or "")
        elif node.tag in (f"{W}tab",):
            out.append("\t")
        elif node.tag in (f"{W}br", f"{W}cr"):
            out.append("\n")
    return "".join(out)


def extract(path: str) -> dict:
    z = zipfile.ZipFile(path)
    names = set(z.namelist())

    comments: dict[str, dict] = {}
    if "word/comments.xml" in names:
        root = ET.fromstring(z.read("word/comments.xml"))
        for c in root.findall(f"{W}comment"):
            cid = c.get(f"{W}id")
            comments[cid] = {
                "id": cid,
                "author": c.get(f"{W}author") or "",
                "initials": c.get(f"{W}initials") or "",
                "date": c.get(f"{W}date") or "",
                "text": _text(c).strip(),
                "anchor": "",
                "para_index": None,
                "para_text": "",
            }

    # Walk the body in document order, tracking which comment ranges are open.
    doc = ET.fromstring(z.read("word/document.xml"))
    body = doc.find(f"{W}body")
    open_ids: set[str] = set()
    anchored: dict[str, list[str]] = {cid: [] for cid in comments}

    para_i = 0
    for para in body.iter(f"{W}p"):
        para_i += 1
        ptext = _text(para).strip()
        for node in para.iter():
            tag = node.tag
            if tag == f"{W}commentRangeStart":
                cid = node.get(f"{W}id")
                open_ids.add(cid)
                if cid in comments and comments[cid]["para_index"] is None:
                    comments[cid]["para_index"] = para_i
                    comments[cid]["para_text"] = ptext
            elif tag == f"{W}commentRangeEnd":
                open_ids.discard(node.get(f"{W}id"))
            elif tag == f"{W}t" and open_ids:
                for cid in open_ids:
                    if cid in anchored:
                        anchored[cid].append(node.text or "")

    for cid, parts in anchored.items():
        comments[cid]["anchor"] = "".join(parts).strip()

    # Full body text, one line per paragraph, for drift comparison.
    paras = [_text(p).strip() for p in body.iter(f"{W}p")]
    paras = [p for p in paras if p]

    return {
        "file": path,
        "n_comments": len(comments),
        "n_paragraphs": len(paras),
        "n_words": sum(len(p.split()) for p in paras),
        "comments": sorted(comments.values(), key=lambda c: (c["para_index"] or 0, int(c["id"]))),
        "paragraphs": paras,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    as_json = "--json" in sys.argv
    d = extract(path)

    if as_json:
        print(json.dumps(d, indent=2, ensure_ascii=False))
        return 0

    print(f"{d['file']}")
    print(f"  paragraphs: {d['n_paragraphs']}   words: {d['n_words']}   comments: {d['n_comments']}")
    if not d["comments"]:
        print("  (no comments in this file)")
        return 0
    print()
    for c in d["comments"]:
        loc = f"para {c['para_index']}" if c["para_index"] else "unanchored"
        print(f"--- [{c['id']}] {c['author']} ({loc}) {c['date'][:10]}")
        if c["anchor"]:
            a = c["anchor"]
            print(f'    on: "{a[:160]}{"..." if len(a) > 160 else ""}"')
        print(f"    says: {c['text']}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
