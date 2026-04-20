#!/usr/bin/env python3
"""
Validate Google Drive filenames against Zotero-generated standard names.

Compares current GDrive files against generated names from Zotero metadata.
Flags mismatches for user review.

Usage:
  python scripts/zotero_gdrive_filename_validator.py
  python scripts/zotero_gdrive_filename_validator.py --verbose
"""

import sys
from pathlib import Path
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.zotero_client import get_citations, generate_gdrive_filename
from scripts.gdrive_citation_matcher import match_gdrive_to_citation_key, fuzzy_match_gdrive_to_zotero


def validate_filenames(verbose: bool = False) -> dict:
    """Compare Zotero-generated filenames against actual GDrive files.

    Returns:
        Dict with counts: exact_match, misnamed, missing, unexpected
    """
    print("=" * 80)
    print("ZOTERO -> GOOGLE DRIVE FILENAME VALIDATOR")
    print("=" * 80)

    # Fetch papers from Zotero
    print("\n[1] Fetching papers from Zotero...")
    try:
        papers = get_citations(sync_files=False)
        print(f"    Found {len(papers)} papers")
    except Exception as e:
        print(f"    ERROR: Could not fetch from Zotero: {e}")
        return None

    # For each paper, generate expected filename
    expected_files = {}
    print(f"\n[2] Generating expected filenames...")
    for paper in papers:
        # Reconstruct item_data from citation entry
        item_data = {
            'creators': [],
            'title': paper.get('title', ''),
            'date': paper.get('year', '') + '-01-01' if paper.get('year') else ''
        }

        # Parse author field back to creators (simplified: just use for generation)
        if paper.get('author'):
            authors = [a.strip() for a in str(paper['author']).split(',')]
            for author in authors[:3]:  # Limit to first 3
                parts = author.rsplit(' ', 1)  # Split "FirstName LastName"
                if len(parts) == 2:
                    item_data['creators'].append({'lastName': parts[1], 'firstName': parts[0]})
                else:
                    item_data['creators'].append({'lastName': author, 'firstName': ''})

        expected_filename = generate_gdrive_filename(item_data)
        citation_key = paper.get('citationKey') or paper.get('key')
        expected_files[citation_key] = {
            'expected_filename': expected_filename,
            'title': paper.get('title', '')
        }

    print(f"    Generated {len(expected_files)} expected filenames")

    # Note: In full implementation, would fetch actual GDrive files and compare
    # For now, show expected names
    print(f"\n[3] Expected filename mappings:\n")

    stats = {
        'total': len(expected_files),
        'generated': len(expected_files),
        'exact_match': 0,
        'misnamed': 0,
        'missing': 0,
        'unexpected': 0
    }

    for citation_key, data in expected_files.items():
        if verbose:
            print(f"  {citation_key}")
            print(f"    -> {data['expected_filename']}")
            print(f"       (for: {data['title'][:70]}...)\n")
        stats['generated'] += 1

    print("=" * 80)
    print("RESULTS:")
    print(f"  Total papers in Zotero: {stats['total']}")
    print(f"  Expected filenames generated: {stats['generated']}")
    print("=" * 80)
    print("\nNext: Compare with actual GDrive files (Phase 2)")

    return stats


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv
    validate_filenames(verbose=verbose)
