#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zotero_library_index.py — Generate a browsable index of the Zotero group library.

Makes a live API call and writes `06_thesis_writing/citations/library-index.md`:
every citable item, grouped under the collection ("subfolder") path it sits in.

Two facts about Zotero collections drive the whole layout, and both are easy to
get wrong:

  * An item can belong to MORE THAN ONE collection. Summing per-collection
    counts therefore over-counts, and the sum exceeds the library size.
  * An item can belong to NO collection. Grouping only by collection silently
    drops those items, which is the failure mode this file exists to avoid.

So the per-collection counts are labelled as memberships, the unfiled items get
a section of their own, and the reconciliation is printed rather than left for
the reader to attempt.

Companion to `zotero_client.py`, which writes bibtex.bib / citations.json. That
one is the citation source of truth; this one is a human-readable map. Neither
reads the other's output -- both call the API -- so they cannot drift apart.
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from pyzotero import Zotero
from dotenv import load_dotenv

# Anchor on a repo marker rather than a hop-count: parents[N] breaks the moment
# this file moves a level, and it has moved before (see path-handling.md).
for _cand in (Path(__file__).resolve().parent, *Path(__file__).resolve().parents):
    if any((_cand / _a).exists() for _a in (".env.example", ".env", "PATHS.py")):
        _REPO_ROOT = _cand
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        break
else:
    raise FileNotFoundError("Could not find project root above " + str(Path(__file__).resolve()))

from PATHS import THESIS_WRITING_CITATIONS_DIR  # noqa: E402

# Reuse the citable-type filter rather than restating it. A second copy would
# drift, and the consequence of drift is an item that is present in Zotero but
# invisible here -- indistinguishable from one that was never added.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from zotero_client import _SCHOLARLY_TYPES  # noqa: E402

OUTPUT_NAME = "library-index.md"


def _fetch(group_id: str | None = None) -> tuple[dict, list[dict]]:
    """Return (collections_by_key, citable_items). Live call, no cache."""
    load_dotenv(_REPO_ROOT / ".env")
    api_key = os.environ.get("ZOTERO_API_KEY")
    if not api_key:
        raise ValueError("Missing ZOTERO_API_KEY in .env")
    gid = group_id or os.environ.get("ZOTERO_GROUP_ID", "6479832")

    zot = Zotero(library_id=gid, library_type="group", api_key=api_key)

    collections = {
        c["data"]["key"]: {
            "name": c["data"]["name"],
            "parent": c["data"].get("parentCollection") or None,
        }
        for c in zot.everything(zot.collections())
    }

    items = []
    for raw in zot.everything(zot.top(itemType="-attachment")):
        data = raw["data"]
        if data.get("itemType") not in _SCHOLARLY_TYPES:
            continue
        items.append(
            {
                "key": raw["key"],
                "citationKey": data.get("citationKey"),
                "itemType": data.get("itemType"),
                "title": (data.get("title") or "(untitled)").strip(),
                "year": (data.get("date") or "")[:4],
                "authors": [
                    (c.get("lastName") or c.get("name") or "").strip()
                    for c in data.get("creators", [])
                    if c.get("creatorType") == "author"
                ],
                "doi": data.get("DOI"),
                "url": data.get("url"),
                "collections": data.get("collections") or [],
            }
        )
    return collections, items


def _collection_path(key: str, collections: dict) -> str:
    """Full 'Parent / Child' path for a collection key, guarded against cycles."""
    parts: list[str] = []
    seen: set[str] = set()
    while key and key in collections and key not in seen:
        seen.add(key)
        parts.append(collections[key]["name"])
        key = collections[key]["parent"]
    return " / ".join(reversed(parts))


def _depth(key: str, collections: dict) -> int:
    d, seen = 0, set()
    while key and key in collections and key not in seen:
        seen.add(key)
        key = collections[key]["parent"]
        d += 1
    return d


def _author_str(authors: list[str]) -> str:
    named = [a for a in authors if a]
    if not named:
        return "—"
    if len(named) == 1:
        return named[0]
    if len(named) == 2:
        return f"{named[0]} & {named[1]}"
    return f"{named[0]} et al."


def _item_line(item: dict) -> str:
    year = item["year"] or "n.d."
    title = item["title"].replace("|", r"\|")
    link = item["doi"] and f"https://doi.org/{item['doi']}" or item["url"]
    title_cell = f"[{title}]({link})" if link else title
    # Distinguish a real BibTeX citation key from the opaque Zotero item ID we
    # fall back to. Most of the library has no citationKey set, and rendering
    # both in one column without marking them makes an 8-character item ID look
    # like something you could type into a \cite{}.
    cite_key = f"`{item['citationKey']}`" if item["citationKey"] else f"`{item['key']}` ¹"
    return f"| {_author_str(item['authors'])} | {year} | {title_cell} | `{item['itemType']}` | {cite_key} |"


TABLE_HEAD = (
    "| Author | Year | Title | Type | Key |\n"
    "|---|---|---|---|---|"
)


def build_markdown(collections: dict, items: list[dict]) -> str:
    by_collection: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        for ck in it["collections"]:
            if ck in collections:
                by_collection[ck].append(it)

    unfiled = [i for i in items if not [c for c in i["collections"] if c in collections]]
    multi = [i for i in items if len([c for c in i["collections"] if c in collections]) > 1]
    memberships = sum(len(v) for v in by_collection.values())

    # Same work entered twice under two Zotero keys. Detected on a normalised
    # title rather than the key, since duplicate keys would not collide.
    by_title: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        by_title["".join(c.lower() for c in it["title"] if c.isalnum())].append(it)
    dup_groups = [v for v in by_title.values() if len(v) > 1]
    dup_items = sum(len(g) for g in dup_groups)
    distinct = len(items) - (dup_items - len(dup_groups))

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    top_level = [k for k, v in collections.items() if not v["parent"]]

    out: list[str] = []
    out.append("---")
    out.append("name: library-index")
    out.append(
        "description: REFERENCE - Every citable item in the Zotero group library, "
        "grouped by the collection it belongs to. Generated, never hand-edited."
    )
    out.append("category: reference")
    out.append("applies-to: [citations, literature, verification]")
    out.append("triggers: [what is in the library, which collection holds, zotero subfolders]")
    out.append(f"updated: {datetime.now().strftime('%Y_%m_%d-%H_%M')}")
    out.append("---")
    out.append("")
    out.append("# Zotero library index")
    out.append("")
    out.append(
        "Generated by `utility_scripts/scripts/zotero_library_index.py` from a live "
        "call to the group library. **Do not edit by hand** — re-run the script instead."
    )
    out.append("")

    # --- Reconciliation -----------------------------------------------------
    out.append("## Library at a glance")
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append(f"| Pulled | **{now}** |")
    out.append(f"| Citable items | **{len(items)}** |")
    out.append(f"| Collections | **{len(collections)}** ({len(top_level)} top-level) |")
    out.append(f"| Items in no collection | **{len(unfiled)}** |")
    out.append(f"| Items in more than one | **{len(multi)}** |")
    out.append(f"| Collection memberships | **{memberships}** |")
    if dup_groups:
        out.append(f"| Duplicated works | **{len(dup_groups)}** (see below) |")
        out.append(f"| Distinct works | **{distinct}** |")
    out.append("")
    out.append(
        "¹ marks a row keyed by its opaque Zotero item ID because the item has no "
        "citation key set. Those IDs are not usable as BibTeX keys — "
        f"{sum(1 for i in items if not i['citationKey'])} of {len(items)} items are in this state, "
        "and `bibtex.bib` falls back to the same ID for them."
    )
    out.append("")
    out.append(
        f"**The counts below do not partition the library.** {len(multi)} items belong to "
        f"more than one collection and {len(unfiled)} belong to none, so the per-collection "
        f"counts sum to {memberships} memberships across {len(items)} distinct items. "
        "An item appears under every collection that holds it."
    )
    out.append("")

    # --- Tree ---------------------------------------------------------------
    out.append("## Collection tree")
    out.append("")
    ordered = sorted(collections, key=lambda k: _collection_path(k, collections).lower())
    for key in ordered:
        indent = "  " * (_depth(key, collections) - 1)
        name = collections[key]["name"]
        n = len(by_collection.get(key, []))
        out.append(f"{indent}- **{name}** — {n} item{'s' if n != 1 else ''}")
    if unfiled:
        out.append(f"- *(no collection)* — {len(unfiled)} item{'s' if len(unfiled) != 1 else ''}")
    out.append("")

    # --- Items per collection ----------------------------------------------
    out.append("## Items by collection")
    out.append("")
    for key in ordered:
        entries = sorted(
            by_collection.get(key, []),
            key=lambda i: (_author_str(i["authors"]).lower(), i["year"]),
        )
        out.append(f"### {_collection_path(key, collections)}")
        out.append("")
        if not entries:
            out.append("*No items filed directly in this collection.*")
            out.append("")
            continue
        out.append(f"{len(entries)} item{'s' if len(entries) != 1 else ''}.")
        out.append("")
        out.append(TABLE_HEAD)
        out.extend(_item_line(i) for i in entries)
        out.append("")

    # --- Unfiled ------------------------------------------------------------
    out.append("## Items in no collection")
    out.append("")
    if unfiled:
        out.append(
            f"{len(unfiled)} items sit at the library root. They are fully citable — "
            "being unfiled is an organisational state, not a defect — but they are "
            "invisible to anyone browsing by collection, which is why they are listed here."
        )
        out.append("")
        out.append(TABLE_HEAD)
        out.extend(
            _item_line(i)
            for i in sorted(unfiled, key=lambda i: (_author_str(i["authors"]).lower(), i["year"]))
        )
    else:
        out.append("Every item is filed in at least one collection.")
    out.append("")

    # --- Duplicates ---------------------------------------------------------
    if dup_groups:
        out.append("## The same work entered twice")
        out.append("")
        out.append(
            f"{len(dup_groups)} works exist under two Zotero keys, so the library reports "
            f"{len(items)} items but holds {distinct} distinct works. Matched on normalised "
            "title; both copies are listed above under wherever each one sits."
        )
        out.append("")
        out.append(
            "The pattern is consistent and worth reading before merging: in most groups the "
            "**filed** copy is the one with no citation key, and the copy carrying the citation "
            "key is **unfiled**. Merging naively toward either side loses something — the "
            "collection membership, or the key the prose may already cite."
        )
        out.append("")
        out.append("| Title | Zotero key | Citation key | Collections |")
        out.append("|---|---|---|---|")
        for group in sorted(dup_groups, key=lambda g: g[0]["title"].lower()):
            for n, i in enumerate(sorted(group, key=lambda x: x["key"])):
                filed = [c for c in i["collections"] if c in collections]
                paths = "; ".join(sorted(_collection_path(c, collections) for c in filed)) or "*(none)*"
                title = i["title"].replace("|", r"\|") if n == 0 else "↳"
                out.append(f"| {title} | `{i['key']}` | {'`' + i['citationKey'] + '`' if i['citationKey'] else '—'} | {paths} |")
        out.append("")

    # --- Cross-filed --------------------------------------------------------
    if multi:
        out.append("## Items in more than one collection")
        out.append("")
        out.append(
            f"{len(multi)} items are cross-filed. Each appears under every collection "
            "listed, and is counted once per appearance above."
        )
        out.append("")
        out.append("| Author | Year | Title | Collections |")
        out.append("|---|---|---|---|")
        for i in sorted(multi, key=lambda i: (_author_str(i["authors"]).lower(), i["year"])):
            paths = "; ".join(
                sorted(_collection_path(c, collections) for c in i["collections"] if c in collections)
            )
            title = i["title"].replace("|", r"\|")
            out.append(f"| {_author_str(i['authors'])} | {i['year'] or 'n.d.'} | {title} | {paths} |")
        out.append("")

    return "\n".join(out) + "\n"


def main() -> None:
    print("Fetching collections and items from Zotero group library...")
    collections, items = _fetch()
    md = build_markdown(collections, items)

    out_dir = THESIS_WRITING_CITATIONS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / OUTPUT_NAME
    out_file.write_bytes(md.encode("utf-8"))

    unfiled = sum(1 for i in items if not [c for c in i["collections"] if c in collections])
    print(f"  [OK] {len(items)} items across {len(collections)} collections")
    print(f"  [OK] {unfiled} items in no collection")
    print(f"  [OK] Wrote {out_file.relative_to(_REPO_ROOT)}")


if __name__ == "__main__":
    main()
