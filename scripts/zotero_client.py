#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zotero_client.py — Shared Zotero citation client for CMT thesis.

Always makes a live API call to the group library (6479832).
Returns citation items only — attachments and notes are excluded.
BibTeX is the source of truth. JSON is derived from BibTeX for programmatic access.
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


def _extract_month(item_data: dict) -> str | None:
    """Extract month from date field. Returns abbreviated month name."""
    date_str = item_data.get("date", "") or ""
    if not date_str:
        return None
    try:
        if len(date_str) >= 7 and date_str[4] == "-":
            month_num = int(date_str[5:7])
            months = ["", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
            return months[month_num] if 1 <= month_num <= 12 else None
    except (ValueError, IndexError):
        pass
    return None


def _extract_publisher(item_data: dict) -> str | None:
    """Extract publisher from publisher field or extra field (for preprints)."""
    pub = item_data.get("publisher", "").strip()
    if pub:
        return pub

    # For preprints, publisher may be in extra field (e.g., "arXiv:2502.04306 [cs]")
    extra = item_data.get("extra", "").strip()
    if extra and item_data.get("itemType") == "preprint":
        if extra.lower().startswith("arxiv"):
            return "arXiv"

    return None



def generate_citation_key(creators: list, title: str, year: str) -> str:
    """Generate citation key in Zotero format: firstname_firstword_year (all lowercase).

    Args:
        creators: List of creator dicts with 'lastName' field
        title: Paper title
        year: Year as string

    Returns:
        Citation key like 'avramova_overview_2025'
    """
    # Get first author's last name
    if creators and isinstance(creators, list) and len(creators) > 0:
        first_author = creators[0].get('lastName', '').lower()
    else:
        first_author = 'unknown'

    # Get first word of title
    if title:
        title_words = str(title).split()
        first_word = title_words[0].lower() if title_words else 'unknown'
    else:
        first_word = 'unknown'

    # Get year
    year_str = str(year).strip() if year else 'unknown'

    return f"{first_author}_{first_word}_{year_str}"



def _normalize_author_name(name: str) -> str:
    """Normalize author name by replacing hyphens and spaces with underscores.

    Examples:
        'al-karkhi' -> 'al_karkhi'
        'Al Karkhi' -> 'Al_Karkhi'
    """
    if not name:
        return 'unknown'
    normalized = name.replace('-', '_').replace(' ', '_')
    return normalized


def generate_gdrive_filename(item_data: dict) -> str:
    """Generate standardized Google Drive filename from Zotero item data.

    Pattern: FirstAuthor-SecondAuthor_or_et_al-Year-Title_with_underscores.pdf

    Rules:
    - 2 authors or fewer: list both separated by hyphen
    - 3+ authors: FirstAuthor-et_al
    - Within author names: replace hyphens/spaces with underscores
    - Within title: replace spaces with underscores
    - Separators between blocks (authors, year, title): hyphen

    Args:
        item_data: Zotero item data dict with creators, title, date fields

    Returns:
        Filename string like 'Avramova-et_al-2025-Overview_of_Existing_Multi_Criteria.pdf'
    """
    creators = item_data.get('creators', [])
    title = item_data.get('title', '')
    date_str = item_data.get('date', '')

    year = date_str[:4] if date_str else 'unknown'

    if len(creators) == 0:
        author_part = 'Unknown'
    elif len(creators) == 1:
        author_part = _normalize_author_name(creators[0].get('lastName', 'Unknown'))
    elif len(creators) == 2:
        author1 = _normalize_author_name(creators[0].get('lastName', 'Unknown'))
        author2 = _normalize_author_name(creators[1].get('lastName', 'Unknown'))
        author_part = f"{author1}-{author2}"
    else:
        first_author = _normalize_author_name(creators[0].get('lastName', 'Unknown'))
        author_part = f"{first_author}-et_al"

    if title:
        title_clean = str(title)[:60].replace(' ', '_').replace('-', '_')
    else:
        title_clean = 'Unknown'

    filename = f"{author_part}-{year}-{title_clean}.pdf"
    return filename

def _to_bibtex_value(val: str | list | None) -> str:
    """Format a value for BibTeX output."""
    if val is None or val == "":
        return ""
    if isinstance(val, list):
        val = ", ".join(str(v) for v in val)
    return str(val)


def get_citations(group_id: str | None = None, sync_files: bool = True) -> list[dict]:
    """Fetch all citation items from the Zotero group library (live call).

    Excludes attachments and notes. Returns list of dicts with all available fields.
    If sync_files=True (default), writes bibtex.bib and derives citations.json.
    """
    env = _load_env()
    gid = group_id or env["group_id"]

    zot = Zotero(
        library_id=gid,
        library_type="group",
        api_key=env["api_key"],
    )

    raw = zot.everything(zot.top(itemType="-attachment"))
    entries = []

    for item in raw:
        if item["data"].get("itemType") not in _SCHOLARLY_TYPES:
            continue

        data = item["data"]
        creators = data.get("creators", [])
        authors = ", ".join(
            f"{c.get('lastName', '')} {c.get('firstName', '')}".strip()
            for c in creators
            if c.get("creatorType") == "author"
        )

        # Build entry with all available fields (except note and file)
        entry = {
            "key": data.get("citationKey") or item.get("key"),
            "itemType": data.get("itemType"),
            "title": data.get("title"),
            "shorttitle": data.get("shortTitle"),
            "volume": data.get("volume"),
            "numberOfVolumes": data.get("numberOfVolumes"),
            "copyright": data.get("rights"),
            "issn": data.get("ISSN"),
            "isbn": data.get("ISBN"),
            "url": data.get("url"),
            "doi": data.get("DOI"),
            "abstract": data.get("abstractNote"),
            "language": data.get("language"),
            "number": data.get("issue"),
            "urldate": data.get("accessDate"),
            "journal": data.get("publicationTitle") or data.get("university"),
            "journalAbbreviation": data.get("journalAbbreviation"),
            "publisher": _extract_publisher(data),
            "author": authors,
            "month": _extract_month(data),
            "year": _extract_year(data),
            "pages": data.get("pages"),
            "numPages": data.get("numPages"),
            "keywords": [t["tag"] for t in data.get("tags", [])],
            "series": data.get("series"),
            "seriesNumber": data.get("seriesNumber"),
            "seriesTitle": data.get("seriesTitle"),
            "seriesText": data.get("seriesText"),
            "section": data.get("section"),
            "partNumber": data.get("partNumber"),
            "partTitle": data.get("partTitle"),
            "archive": data.get("archive"),
            "archiveID": data.get("archiveID"),
            "archiveLocation": data.get("archiveLocation"),
            "repository": data.get("repository"),
            "genre": data.get("genre"),
            "format": data.get("format"),
            "place": data.get("place"),
            "libraryCatalog": data.get("libraryCatalog"),
            "callNumber": data.get("callNumber"),
            "citationKey": data.get("citationKey"),
            "edition": data.get("edition"),
            "originalDate": data.get("originalDate"),
            "originalPlace": data.get("originalPlace"),
            "originalPublisher": data.get("originalPublisher"),
            "conferenceName": data.get("conferenceName"),
            "proceedingsTitle": data.get("proceedingsTitle"),
            "eventPlace": data.get("eventPlace"),
            "extra": data.get("extra"),
        }

        # Remove None/empty values to keep output clean
        entry = {k: v for k, v in entry.items() if v not in (None, "", [])}

        entries.append(entry)

    if sync_files:
        _write_citation_files(entries)

    return entries


def _write_citation_files(entries: list[dict]) -> None:
    """Write bibtex.bib as source of truth, then derive citations.json."""
    lit_dir = Path(__file__).resolve().parents[1] / "docs" / "literature"
    lit_dir.mkdir(parents=True, exist_ok=True)

    # Write BibTeX as source of truth
    bibtex_file = lit_dir / "bibtex.bib"
    bibtex_lines = []

    # Field order matching Zotero export convention
    field_order = [
        "title", "shorttitle", "volume", "numberOfVolumes", "copyright", "issn", "isbn",
        "url", "doi", "abstract", "language", "number", "urldate", "journal",
        "journalAbbreviation", "publisher", "author", "month", "year", "pages", "numPages",
        "keywords", "series", "seriesNumber", "seriesTitle", "seriesText",
        "section", "partNumber", "partTitle", "archive", "archiveID", "archiveLocation",
        "repository", "genre", "format", "place", "libraryCatalog", "callNumber",
        "citationKey", "edition", "originalDate", "originalPlace", "originalPublisher",
        "conferenceName", "proceedingsTitle", "eventPlace", "extra"
    ]

    for entry in entries:
        key = entry.get("key", "unknown")
        itype = entry.get("itemType", "misc")

        bibtex_lines.append(f"@{itype}{{{key},")

        for field in field_order:
            val = entry.get(field)
            if val:
                if isinstance(val, list):
                    val = ", ".join(str(v) for v in val)
                bibtex_lines.append(f'  {field} = {{{val}}},')

        # Remove trailing comma from last field
        bibtex_lines[-1] = bibtex_lines[-1].rstrip(",")
        bibtex_lines.append("}")
        bibtex_lines.append("")

    bibtex_file.write_bytes("\n".join(bibtex_lines).encode("utf-8"))
    print(f"  [OK] Synced BibTeX to {bibtex_file.relative_to(Path.cwd())}")

    # Derive JSON from BibTeX entries (programmatic access only)
    json_file = lit_dir / "citations.json"
    json_file.write_bytes(
        json.dumps(entries, indent=2, ensure_ascii=False, default=str).encode("utf-8")
    )
    print(f"  [OK] Derived citations.json from BibTeX")


if __name__ == "__main__":
    print("Fetching citations from Zotero group library...")
    items = get_citations()
    print(f"\nFetched {len(items)} citation items")
    print("\nSample citations:")
    for item in items[:5]:
        year = item["year"] or "?"
        print(f"  [{item['itemType']}] ({year}) {item['title']}")
