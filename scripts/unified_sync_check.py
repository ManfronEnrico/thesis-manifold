#!/usr/bin/env python3
"""
Unified sync check: query all 3 systems and populate manifest with sync status.

Scans Zotero (papers), Google Drive (PDFs), and NotebookLM (ingested sources).
Updates ingestion_manifest.json with current state and status.

Usage:
  python scripts/unified_sync_check.py              # Report current state
  python scripts/unified_sync_check.py --verbose    # Show all matches + confidences
  python scripts/unified_sync_check.py --check-only # No changes, just report
  python scripts/unified_sync_check.py --force      # Force re-check, ignore timestamps
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from difflib import SequenceMatcher

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.zotero_client import get_citations, generate_gdrive_filename
from scripts.gdrive_citation_matcher import (
    match_gdrive_to_citation_key,
    fuzzy_match_gdrive_to_zotero
)
from src.google_drive_integration import GoogleDriveAPI
from pyzotero import Zotero
from dotenv import load_dotenv


def _load_env() -> dict:
    """Load environment variables."""
    env_path = Path.cwd() / ".env"
    load_dotenv(env_path)
    return {
        "api_key": os.environ.get("ZOTERO_API_KEY"),
        "group_id": os.environ.get("ZOTERO_GROUP_ID", "6479832"),
        "gdrive_service_account": os.environ.get("GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY"),
    }


def _load_manifest() -> dict:
    """Load manifest from disk or create empty."""
    manifest_path = Path("thesis/literature/ingestion_manifest.json")
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding='utf-8'))
    return {
        "_comment": "Unified sync manifest. Maps papers across Zotero, Google Drive, and NotebookLM with status tracking.",
        "_schema_version": "2.1",
        "_last_updated": datetime.now().isoformat(),
        "notebooks": {},
        "sources": {}
    }


def _save_manifest(manifest: dict) -> None:
    """Save manifest to disk."""
    manifest_path = Path("thesis/literature/ingestion_manifest.json")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )


def _compute_sync_status(entry: dict) -> str:
    """Compute sync status from individual system statuses."""
    z_status = entry.get('zotero_status', 'missing')
    g_status = entry.get('gdrive_status', 'missing')
    n_status = entry.get('notebooklm_status', 'missing')

    active_in = sum([
        z_status == 'active',
        g_status == 'found',
        n_status in ['ingested', 'ingested_partial']
    ])

    if active_in == 3:
        return 'COMPLETE'
    elif active_in == 2:
        return 'PARTIAL'
    elif z_status == 'active' and g_status == 'missing' and n_status == 'pending':
        return 'NEW_ZOTERO'
    elif z_status == 'missing' and g_status == 'found' and n_status == 'pending':
        return 'NEW_GDRIVE'
    elif z_status == 'missing' and g_status == 'missing' and n_status in ['ingested', 'ingested_partial']:
        return 'ORPHAN_NOTEBOOKLM'
    elif z_status == 'active' and g_status == 'misnamed':
        return 'MISNAMED'
    else:
        return 'MIXED'


def _match_gdrive_to_zotero(gdrive_filename: str, zotero_entries: Dict) -> Tuple[str, float]:
    """Match a Google Drive filename to a Zotero citation key.

    Uses multiple strategies:
    1. Exact match by filename
    2. Fuzzy match by authors/title/year
    3. Returns best match with confidence score
    """
    best_match = None
    best_confidence = 0.0

    for citation_key, z_data in zotero_entries.items():
        expected_filename = z_data['generated_filename']

        # Strategy 1: Exact filename match
        if gdrive_filename == expected_filename:
            return citation_key, 1.0

        # Strategy 2: Fuzzy matching on author, title, year
        # Extract year from gdrive filename
        gdrive_year = None
        parts = gdrive_filename.rsplit('-', 2)  # Try to extract last 2 parts (year-title)
        if len(parts) >= 2:
            try:
                gdrive_year = parts[-2]
                if len(gdrive_year) == 4 and gdrive_year.isdigit():
                    pass
                else:
                    gdrive_year = None
            except:
                gdrive_year = None

        z_year = z_data['year']

        # Check year match
        year_match = 1.0 if gdrive_year == z_year else 0.0

        # Extract authors from both filenames
        gdrive_author_part = gdrive_filename.split('-')[0]  # e.g., "Smith" or "Smith-Jones"
        z_author_part = expected_filename.split('-')[0]

        # String similarity on author part
        author_similarity = SequenceMatcher(None, gdrive_author_part.lower(), z_author_part.lower()).ratio()

        # Weighted confidence
        confidence = (author_similarity * 0.5) + (year_match * 0.5)

        if confidence > best_confidence and confidence >= 0.7:
            best_confidence = confidence
            best_match = citation_key

    return best_match, best_confidence


def unified_sync_check(check_only: bool = False, verbose: bool = False, force: bool = False) -> dict:
    """Execute unified sync check across all 3 systems.

    Args:
        check_only: If True, don't update manifest
        verbose: Show detailed match info
        force: Ignore cached timestamps, force re-check

    Returns:
        Summary dict with counts and changes
    """
    print("=" * 80)
    print("UNIFIED SYNC CHECK: Zotero <-> Google Drive <-> NotebookLM")
    print("=" * 80)

    manifest = _load_manifest()
    env = _load_env()

    # [1] ZOTERO SCAN
    print("\n[1] Scanning Zotero...")
    try:
        papers = get_citations(sync_files=False)
        print("    Found {} papers".format(len(papers)))
    except Exception as e:
        print("    ERROR: {}".format(e))
        return None

    zotero_entries = {}
    for paper in papers:
        citation_key = paper.get('citationKey') or paper.get('key')

        # Parse author string into creator list for filename generation
        author_str = paper.get('author', '')
        creators = []
        if author_str:
            # Split "LastName FirstName, LastName FirstName" into creator dicts
            for author in author_str.split(', '):
                parts = author.rsplit(' ', 1)
                if len(parts) == 2:
                    creators.append({'lastName': parts[0], 'firstName': parts[1]})
                else:
                    creators.append({'lastName': author, 'firstName': ''})

        zotero_entries[citation_key] = {
            'title': paper.get('title', ''),
            'creators': author_str,
            'year': paper.get('year', ''),
            'generated_filename': generate_gdrive_filename({
                'creators': creators,
                'title': paper.get('title', ''),
                'date': (paper.get('year', '') + '-01-01') if paper.get('year') else ''
            }),
            'zotero_status': 'active'
        }

    # [2] GOOGLE DRIVE SCAN
    print("[2] Scanning Google Drive...")
    gdrive_files = {}
    gdrive_lookup = {}  # Map of filename -> metadata

    try:
        if env.get('gdrive_service_account'):
            api = GoogleDriveAPI(service_account_key_json=env['gdrive_service_account'])
            papers = api.list_papers_with_metadata()
            print("    Found {} files".format(len(papers)))

            for paper in papers:
                filename = paper.get('name', '')
                gdrive_lookup[filename] = {
                    'id': paper.get('id'),
                    'importance': paper.get('importance'),
                    'modified': paper.get('modifiedTime'),
                    'size': paper.get('size', 0),
                }
                gdrive_files[filename] = paper
        else:
            print("    ERROR: Google Drive service account not configured")
    except Exception as e:
        print("    ERROR: {}".format(e))

    # [3] NOTEBOOKLM SCAN
    print("[3] Scanning NotebookLM...")
    print("    (NotebookLM API integration deferred to Phase 2)")
    notebooklm_sources = {}

    # [4] MERGE & MATCH
    print("[4] Matching and merging entries...")
    summary = {
        'total_zotero': len(zotero_entries),
        'total_gdrive': len(gdrive_files),
        'total_notebooklm': len(notebooklm_sources),
        'updated': 0,
        'new_entries': 0,
        'status_breakdown': {},
        'matches': {
            'exact': 0,
            'fuzzy': 0,
            'unmatched_zotero': [],
            'unmatched_gdrive': [],
        }
    }

    # Track which gdrive files have been matched
    matched_gdrive = set()

    # For each Zotero paper, create/update manifest entry and try to match with GDrive
    for citation_key, z_data in zotero_entries.items():
        if citation_key not in manifest['sources']:
            manifest['sources'][citation_key] = {
                'citation_key': citation_key,
                'srqs': [],
                'notebooks': [],
                'notebooklm_source_ids': {}
            }
            summary['new_entries'] += 1

        entry = manifest['sources'][citation_key]
        entry['title'] = z_data['title']
        entry['zotero_status'] = z_data['zotero_status']
        entry['gdrive_filename'] = z_data['generated_filename']
        entry['last_checked'] = datetime.now().isoformat()

        # Try to match with GDrive file
        expected_filename = z_data['generated_filename']
        gdrive_status = 'missing'
        match_confidence = 0.0
        matched_file_id = None

        if expected_filename in gdrive_lookup:
            # Exact match found
            gdrive_status = 'found'
            match_confidence = 1.0
            matched_gdrive.add(expected_filename)
            matched_file_id = gdrive_lookup[expected_filename]['id']
            summary['matches']['exact'] += 1
            if verbose:
                print("  [EXACT] {} -> {}".format(citation_key, expected_filename))
        else:
            # Try fuzzy match
            best_gdrive_match = None
            best_gdrive_confidence = 0.0

            for gdrive_filename in gdrive_files.keys():
                if gdrive_filename in matched_gdrive:
                    continue

                # Simple fuzzy match: compare expected vs actual filename
                similarity = SequenceMatcher(None, expected_filename.lower(), gdrive_filename.lower()).ratio()

                if similarity > best_gdrive_confidence and similarity >= 0.7:
                    best_gdrive_confidence = similarity
                    best_gdrive_match = gdrive_filename

            if best_gdrive_match:
                gdrive_status = 'found'  # Could be 'misnamed' if we want to be stricter
                match_confidence = best_gdrive_confidence
                matched_gdrive.add(best_gdrive_match)
                matched_file_id = gdrive_lookup[best_gdrive_match]['id']
                summary['matches']['fuzzy'] += 1
                if verbose:
                    print("  [FUZZY {:.2f}] {} -> {} (expected: {})".format(
                        best_gdrive_confidence, citation_key, best_gdrive_match, expected_filename))
            else:
                summary['matches']['unmatched_zotero'].append(citation_key)

        entry['gdrive_status'] = gdrive_status
        entry['gdrive_file_id'] = matched_file_id or ""
        entry['match_confidence'] = match_confidence
        entry['notebooklm_status'] = entry.get('notebooklm_status', 'pending')

        # Compute sync status
        entry['sync_status'] = _compute_sync_status(entry)

        summary['updated'] += 1

    # Record unmatched GDrive files
    for gdrive_filename in gdrive_files.keys():
        if gdrive_filename not in matched_gdrive:
            summary['matches']['unmatched_gdrive'].append(gdrive_filename)

    # [5] OUTPUT
    print("\n[5] Manifest update: {} entries".format(summary['updated']))

    # Count by status
    status_counts = {}
    for entry in manifest['sources'].values():
        if isinstance(entry, dict):
            status = entry.get('sync_status', 'UNKNOWN')
            status_counts[status] = status_counts.get(status, 0) + 1

    print("\nSYNC STATUS SUMMARY:")
    for status, count in sorted(status_counts.items()):
        print("  {:20s}: {:3d} papers".format(status, count))

    print("\nMATCHING SUMMARY:")
    print("  Exact matches:       {}".format(summary['matches']['exact']))
    print("  Fuzzy matches:       {}".format(summary['matches']['fuzzy']))
    print("  Unmatched Zotero:    {}".format(len(summary['matches']['unmatched_zotero'])))
    print("  Unmatched GDrive:    {}".format(len(summary['matches']['unmatched_gdrive'])))

    if verbose and summary['matches']['unmatched_zotero']:
        print("\n  Unmatched Zotero papers:")
        for key in summary['matches']['unmatched_zotero'][:5]:
            print("    - {}".format(key))
        if len(summary['matches']['unmatched_zotero']) > 5:
            print("    ... and {} more".format(len(summary['matches']['unmatched_zotero']) - 5))

    if verbose and summary['matches']['unmatched_gdrive']:
        print("\n  Unmatched GDrive files:")
        for filename in summary['matches']['unmatched_gdrive'][:5]:
            print("    - {}".format(filename))
        if len(summary['matches']['unmatched_gdrive']) > 5:
            print("    ... and {} more".format(len(summary['matches']['unmatched_gdrive']) - 5))

    summary['status_breakdown'] = status_counts

    # Save manifest
    if not check_only:
        _save_manifest(manifest)
        print("\n[SAVED] Manifest updated: thesis/literature/ingestion_manifest.json")
    else:
        print("\n[CHECK-ONLY] Manifest NOT updated (--check-only flag set)")

    print("=" * 80)
    return summary


def main():
    """Command-line entry point."""
    check_only = "--check-only" in sys.argv
    verbose = "--verbose" in sys.argv
    force = "--force" in sys.argv

    summary = unified_sync_check(check_only=check_only, verbose=verbose, force=force)

    if summary:
        print("\nNext: Phase 2 - Manual SRQ tagging in Zotero UI")
        print("=" * 80)


if __name__ == "__main__":
    main()
