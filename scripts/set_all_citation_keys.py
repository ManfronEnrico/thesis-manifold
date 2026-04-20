#!/usr/bin/env python3
"""
Bulk set citation keys for all papers in Zotero library.

For each paper, generates citation key (lastname_firstword_year)
and sets the citationKey field in Zotero.

Usage:
  python set_all_citation_keys.py [--dry-run] [--limit N]

Options:
  --dry-run: Show what would be done, don't actually update Zotero
  --limit N: Only process first N papers (default: all)
"""

import os
import sys
from pathlib import Path
from pyzotero import Zotero
from dotenv import load_dotenv

def load_env():
    """Load Zotero API credentials from .env"""
    env_file = Path.cwd() / ".env"
    load_dotenv(env_file)
    api_key = os.getenv("ZOTERO_API_KEY")
    group_id = os.getenv("ZOTERO_GROUP_ID", "6479832")
    if not api_key:
        raise ValueError("ZOTERO_API_KEY not found in .env")
    return api_key, group_id

def generate_citation_key(creators: list, title: str, year: str) -> str:
    """Generate citation key: lastname_firstword_year (all lowercase)."""
    if creators and isinstance(creators, list) and len(creators) > 0:
        first_author = creators[0].get('lastName', '').lower()
    else:
        first_author = 'unknown'

    if title:
        title_words = str(title).split()
        first_word = title_words[0].lower() if title_words else 'unknown'
    else:
        first_word = 'unknown'

    year_str = str(year).strip() if year else 'unknown'

    return f"{first_author}_{first_word}_{year_str}"

def set_all_citation_keys(dry_run=False, limit=None):
    """Set citation keys for all papers in Zotero library."""
    api_key, group_id = load_env()
    zot = Zotero(library_id=group_id, library_type="group", api_key=api_key)

    print("=" * 80)
    print("ZOTERO: BULK SET CITATION KEYS")
    print("=" * 80)

    # Fetch all items (excluding attachments and notes)
    scholarly_types = {
        "journalArticle", "preprint", "book", "bookSection",
        "conferencePaper", "report", "document", "thesis",
        "magazineArticle", "newspaperArticle", "webpage",
    }

    raw_items = zot.everything(zot.top(itemType="-attachment"))
    items = [item for item in raw_items if item["data"].get("itemType") in scholarly_types]

    print(f"\nFound {len(items)} scholarly items")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE UPDATE'}")
    if limit:
        print(f"Processing first {limit} items only\n")
    else:
        print("")

    updated = 0
    skipped = 0
    errors = 0

    for i, item in enumerate(items[:limit] if limit else items, 1):
        data = item["data"]
        creators = data.get("creators", [])
        title = data.get("title", "")
        date_str = data.get("date", "")
        year = date_str[:4] if date_str else "unknown"
        item_key = item.get("key")
        existing_key = data.get("citationKey", "")

        # Generate new citation key
        new_key = generate_citation_key(creators, title, year)

        # Check if already set correctly
        if existing_key == new_key:
            print(f"[{i:3d}] [SKIP] {title[:60]:<60} -> {new_key}")
            skipped += 1
            continue

        print(f"[{i:3d}] [SET]  {title[:60]:<60} -> {new_key}", end="")

        if dry_run:
            print(" (dry-run)")
            updated += 1
            continue

        # Update item with new citation key
        try:
            data['citationKey'] = new_key
            item['data'] = data
            zot.update_item(item)
            print(" [OK]")
            updated += 1
        except Exception as e:
            print(f" [ERROR] {str(e)}")
            errors += 1

    print("\n" + "=" * 80)
    print(f"RESULTS:")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors:  {errors}")
    print(f"  Total:   {updated + skipped + errors}")
    print("=" * 80)

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    limit = None
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            try:
                limit = int(sys.argv[idx + 1])
            except ValueError:
                print("ERROR: --limit requires integer argument")
                sys.exit(1)

    set_all_citation_keys(dry_run=dry_run, limit=limit)
