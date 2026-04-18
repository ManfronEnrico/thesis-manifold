#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zotero_client.py — Shared Zotero citation client for CMT thesis.

Always makes a live API call to the group library (6479832).
Returns citation items only — attachments and notes are excluded.
Auto-syncs citations + BibTeX to docs/literature/ on every call.
"""

import os
import json
from pathlib import Path

from pyzotero import Zotero
from dotenv import load_dotenv

_SCHOLARLY_TYPES = {
    "journalArticle", "preprint", "book", "bookSection",
    "conferencePaper", "report", "document", "thesis",
    "magazineArticle", "newspaperArticle", "webpage",
}

SCHOLARLY_ITEM_TYPES = _SCHOLARLY_TYPES


def _load_env() -> dict:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    api_key = os.environ.get("ZOTERO_API_KEY")
    group_id = os.environ.get("ZOTERO_GROUP_ID", "6479832")
    if not api_key:
        raise ValueError("Missing ZOTERO_API_KEY in .env")
    return {"api_key": api_key, "group_id": group_id}


def _extract_year(item_data: dict) -> str | None:
    date_str = item_data.get("date", "") or ""
    return date_str[:4] if date_str else None


def _normalize(item: dict) -> dict:
    data = item["data"]
    creators = data.get("creators", [])
    authors = ", ".join(
        f"{c.get('lastName', '')} {c.get('firstName', '')}".strip()
        for c in creators
        if c.get("creatorType") == "author"
    )
    return {
        "key": item.get("key") or data.get("key"),
        "itemType": data.get("itemType"),
        "title": data.get("title"),
        "authors": authors or None,
        "year": _extract_year(data),
        "venue": data.get("publicationTitle") or data.get("publisher") or data.get("university"),
        "url": data.get("url"),
        "doi": data.get("DOI"),
        "abstract": data.get("abstractNote"),
        "tags": [t["tag"] for t in data.get("tags", [])],
    }


def get_citations(group_id: str | None = None, sync_files: bool = True) -> list[dict]:
    """Fetch all citation items from the Zotero group library (live call).

    Excludes attachments and notes. Returns normalized dicts.
    If sync_files=True (default), also writes citations.json and bibtex.bib to docs/literature/.
    """
    env = _load_env()
    gid = group_id or env["group_id"]

    zot = Zotero(
        library_id=gid,
        library_type="group",
        api_key=env["api_key"],
    )

    raw = zot.everything(zot.top(itemType="-attachment"))
    citations = [
        _normalize(item)
        for item in raw
        if item["data"].get("itemType") in _SCHOLARLY_TYPES
    ]

    if sync_files:
        _write_citation_files(citations, zot)

    return citations


def _write_citation_files(citations: list[dict], zot: Zotero) -> None:
    """Write citations.json and bibtex.bib to docs/literature/."""
    lit_dir = Path(__file__).resolve().parents[1] / "docs" / "literature"
    lit_dir.mkdir(parents=True, exist_ok=True)

    json_file = lit_dir / "citations.json"
    json_file.write_bytes(
        json.dumps(citations, indent=2, ensure_ascii=False).encode("utf-8")
    )
    print(f"  [OK] Synced citations to {json_file.relative_to(Path.cwd())}")

    bibtex_file = lit_dir / "bibtex.bib"
    bibtex_lines = []
    for c in citations:
        key = c.get("key", "unknown")
        title = c.get("title", "")
        authors = c.get("authors", "")
        year = c.get("year", "")
        venue = c.get("venue", "")
        doi = c.get("doi", "")
        url = c.get("url", "")
        itype = c.get("itemType", "misc")

        bibtex_lines.append(f"@{itype}{{{key},")
        if title:
            bibtex_lines.append(f'  title = "{{{title}}},')
        if authors:
            bibtex_lines.append(f'  author = {{{authors}}},')
        if year:
            bibtex_lines.append(f'  year = {{{year}}},')
        if venue:
            bibtex_lines.append(f'  journal = {{{venue}}},')
        if doi:
            bibtex_lines.append(f'  doi = {{{doi}}},')
        if url:
            bibtex_lines.append(f'  url = {{{url}}},')
        bibtex_lines[-1] = bibtex_lines[-1].rstrip(",")
        bibtex_lines.append("}")
        bibtex_lines.append("")

    bibtex_file.write_bytes("\n".join(bibtex_lines).encode("utf-8"))
    print(f"  [OK] Synced BibTeX to {bibtex_file.relative_to(Path.cwd())}")


if __name__ == "__main__":
    print("Fetching citations from Zotero group library...")
    items = get_citations()
    print(f"\nFetched {len(items)} citation items")
    print("\nSample citations:")
    for item in items[:5]:
        year = item["year"] or "?"
        print(f"  [{item['itemType']}] ({year}) {item['title']}")
