#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Zotero Group Library Connection
Usage: python test_group.py
"""

import os
import sys
from pathlib import Path
from pyzotero import Zotero
from dotenv import load_dotenv

def main():
    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        print(f"ERROR: .env file not found at {env_path}")
        sys.exit(1)

    load_dotenv(env_path)

    group_id = os.environ.get('ZOTERO_GROUP_ID')
    api_key = os.environ.get('ZOTERO_API_KEY')

    if not group_id:
        print("ERROR: ZOTERO_GROUP_ID not found in .env")
        print("Add this to .env:")
        print("  ZOTERO_GROUP_ID=6479832")
        sys.exit(1)

    if not api_key:
        print("ERROR: ZOTERO_API_KEY not found in .env")
        sys.exit(1)

    print(f"Connecting to Zotero group: {group_id}")
    print()

    try:
        zot = Zotero(
            library_id=group_id,
            library_type='group',
            api_key=api_key
        )

        print("Fetching items...", end="", flush=True)
        items = zot.everything(zot.items(limit=100))
        print(f" OK ({len(items)} items)")
        print()

        print("=" * 70)
        print("GROUP LIBRARY CONTENTS")
        print("=" * 70)
        print()

        for i, item in enumerate(items, 1):
            title = item["data"].get("title", "Untitled")
            item_type = item["data"].get("itemType", "?")
            print(f"{i:2d}. {title}")
            print(f"    Type: {item_type}")
            print()

        print("=" * 70)
        print(f"Total: {len(items)} items")
        print("=" * 70)

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
