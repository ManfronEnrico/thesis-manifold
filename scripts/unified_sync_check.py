#!/usr/bin/env python3
"""
Unified sync check (Phase 2): query all 3 systems and populate manifest with sync status.

Scans Zotero (papers), Google Drive (PDFs), and NotebookLM (ingested sources).
Updates ingestion_manifest.json with current state and status.

Phase 2 enhancements:
- Create NotebookLM notebooks (real API, not placeholders)
- Sync context markdown files from thesis/thesis-components/ to each notebook
- Ingest all papers from Google Drive to all NotebookLM notebooks
- Verify ingestion via queries
- Track actual source IDs in manifest

Usage:
  python scripts/unified_sync_check.py              # Report current state + execute NotebookLM Phase 2
  python scripts/unified_sync_check.py --verbose    # Show all matches + confidences
  python scripts/unified_sync_check.py --check-only # No changes, just report
  python scripts/unified_sync_check.py --skip-notebooklm  # Skip NotebookLM phase (testing)
"""

import sys
import json
import os
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
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
        "notebooks": {
            "ch2-literature": None,
            "srq1-models": None,
            "srq2-agents": None,
            "srq3-context": None,
            "srq4-comparison": None,
            "thesis-defense": None,
        },
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


async def _setup_notebooklm_notebooks(manifest: dict, verbose: bool = False) -> Tuple[bool, Dict[str, str], List[str]]:
    """
    Create NotebookLM notebooks if they don't exist.

    Returns:
        (success, notebook_ids_dict, errors)
    """
    try:
        from thesis.thesis_production_system.research import NotebookLMAccess
    except ImportError:
        return False, {}, ["NotebookLMAccess not found"]

    nlm = NotebookLMAccess()
    await nlm.initialize()

    notebook_ids = {}
    errors = []

    for chapter_name in manifest['notebooks'].keys():
        if not chapter_name:
            continue

        existing_id = manifest['notebooks'].get(chapter_name)
        if existing_id:
            notebook_ids[chapter_name] = existing_id
            if verbose:
                print(f"    {chapter_name}: Using existing notebook {existing_id}")
            continue

        try:
            notebook = await nlm.client.notebooks.create(
                title=f"thesis-{chapter_name}",
                description=f"Thesis: {chapter_name}",
            )
            notebook_ids[chapter_name] = notebook.notebook_id
            manifest['notebooks'][chapter_name] = notebook.notebook_id
            if verbose:
                print(f"    {chapter_name}: Created with ID {notebook.notebook_id}")
        except Exception as e:
            error_msg = f"{chapter_name}: {str(e)}"
            errors.append(error_msg)
            print(f"    ERROR creating {chapter_name}: {e}")

    return len(errors) == 0, notebook_ids, errors


async def _sync_context_files(notebook_ids: Dict[str, str], verbose: bool = False) -> Tuple[int, List[str]]:
    """
    Sync context markdown files from thesis/thesis-components/ to NotebookLM notebooks.

    Returns:
        (count_synced, errors)
    """
    try:
        from thesis.thesis_production_system.research import NotebookLMAccess
    except ImportError:
        return 0, ["NotebookLMAccess not found"]

    nlm = NotebookLMAccess()
    await nlm.initialize()

    context_dir = Path("thesis/thesis-components")
    if not context_dir.exists():
        return 0, [f"Context directory not found: {context_dir}"]

    synced_count = 0
    errors = []

    context_mapping = {
        "ch2-literature": "ch2-literature-review.md",
        "srq1-models": "srq1-models-efficiency.md",
        "srq2-agents": "srq2-multi-agent-architecture.md",
        "srq3-context": "srq3-contextual-information.md",
        "srq4-comparison": "srq4-comparison-to-traditional-bi.md",
        "thesis-defense": "thesis-defense.md",
    }

    for chapter_name, notebook_id in notebook_ids.items():
        if not notebook_id:
            continue

        context_file = context_mapping.get(chapter_name)
        if not context_file:
            continue

        context_path = context_dir / context_file
        if not context_path.exists():
            error_msg = f"{chapter_name}: Context file not found: {context_path}"
            errors.append(error_msg)
            if verbose:
                print(f"    ERROR: {error_msg}")
            continue

        try:
            context_content = context_path.read_text(encoding='utf-8')

            await nlm.client.sources.add_text(
                notebook_id=notebook_id,
                text=context_content,
                title="Chapter Context",
            )

            synced_count += 1
            if verbose:
                print(f"    {chapter_name}: Synced context file")
        except Exception as e:
            error_msg = f"{chapter_name}: Failed to sync context: {str(e)}"
            errors.append(error_msg)
            if verbose:
                print(f"    ERROR: {error_msg}")

    return synced_count, errors


async def _ingest_papers_to_notebooklm(
    manifest: dict,
    notebook_ids: Dict[str, str],
    gdrive_file_ids: List[str],
    verbose: bool = False
) -> Tuple[int, int, List[str]]:
    """
    Ingest papers from Google Drive to all NotebookLM notebooks.

    Args:
        manifest: Manifest dict with sources
        notebook_ids: Dict of chapter_name -> notebook_id
        gdrive_file_ids: List of Google Drive file IDs to ingest
        verbose: Print detailed output

    Returns:
        (success_count, failed_count, errors)
    """
    try:
        from thesis.thesis_production_system.research import NotebookLMAccess
    except ImportError:
        return 0, 0, ["NotebookLMAccess not found"]

    nlm = NotebookLMAccess()
    await nlm.initialize()

    success_count = 0
    failed_count = 0
    errors = []

    # Ingest all papers to all notebooks (initial bulk load for curation)
    for chapter_name, notebook_id in notebook_ids.items():
        if not notebook_id:
            continue

        for gdrive_file_id in gdrive_file_ids:
            try:
                source = await nlm.client.sources.add_drive(
                    notebook_id=notebook_id,
                    file_id=gdrive_file_id,
                )

                # Record in manifest
                if gdrive_file_id in manifest['sources']:
                    entry = manifest['sources'][gdrive_file_id]
                    if 'notebooklm_source_ids' not in entry:
                        entry['notebooklm_source_ids'] = {}
                    entry['notebooklm_source_ids'][chapter_name] = source.source_id

                success_count += 1

            except Exception as e:
                failed_count += 1
                error_msg = f"{chapter_name}/{gdrive_file_id}: {str(e)}"
                errors.append(error_msg)
                if verbose:
                    print(f"    ERROR: {error_msg}")

    return success_count, failed_count, errors


async def _verify_notebooklm_ingestion(
    notebook_ids: Dict[str, str],
    verbose: bool = False
) -> Tuple[int, List[str]]:
    """
    Verify papers were ingested by querying each notebook.

    Returns:
        (verified_count, errors)
    """
    try:
        from thesis.thesis_production_system.research import NotebookLMAccess
    except ImportError:
        return 0, ["NotebookLMAccess not found"]

    nlm = NotebookLMAccess()
    await nlm.initialize()

    verified_count = 0
    errors = []

    verification_queries = {
        "ch2-literature": "What are the main topics covered in the papers in this notebook?",
        "srq1-models": "Which predictive modeling approaches are discussed?",
        "srq2-agents": "What multi-agent architectures are mentioned?",
        "srq3-context": "How is contextual information used?",
        "srq4-comparison": "How do these papers compare AI to traditional BI?",
        "thesis-defense": "What are the key papers and their main contributions?",
    }

    for chapter_name, notebook_id in notebook_ids.items():
        if not notebook_id:
            continue

        query = verification_queries.get(chapter_name, "What papers are in this notebook?")

        try:
            result = await nlm.ask(notebook_id, query)

            # Check if we got citations (indicates successful ingestion)
            if result.citations:
                verified_count += 1
                if verbose:
                    print(f"    {chapter_name}: Verified ({len(result.citations)} citations)")
            else:
                error_msg = f"{chapter_name}: No citations returned (possible ingestion issue)"
                errors.append(error_msg)
                if verbose:
                    print(f"    WARNING: {error_msg}")
        except Exception as e:
            error_msg = f"{chapter_name}: Query failed: {str(e)}"
            errors.append(error_msg)
            if verbose:
                print(f"    ERROR: {error_msg}")

    return verified_count, errors


async def _notebooklm_scan(manifest: dict, skip: bool = False, verbose: bool = False) -> Dict:
    """
    Execute full NotebookLM scanning and ingestion workflow.

    Returns:
        Summary dict with counts and errors
    """
    summary = {
        'notebooks_created': 0,
        'context_files_synced': 0,
        'papers_ingested': 0,
        'papers_failed': 0,
        'papers_verified': 0,
        'errors': [],
    }

    if skip:
        print("[3] Scanning NotebookLM... (SKIPPED)")
        return summary

    print("[3] Scanning NotebookLM...")

    # Step 1: Create notebooks
    print("    [3.1] Creating notebooks...")
    success, notebook_ids, errors = await _setup_notebooklm_notebooks(manifest, verbose)
    summary['notebooks_created'] = len([n for n in notebook_ids.values() if n])
    summary['errors'].extend(errors)

    if not success or not notebook_ids:
        print(f"    FAILED to create notebooks. Skipping ingestion.")
        return summary

    # Step 2: Sync context files
    print("    [3.2] Syncing context files...")
    synced, errors = await _sync_context_files(notebook_ids, verbose)
    summary['context_files_synced'] = synced
    summary['errors'].extend(errors)

    # Step 3: Ingest papers
    print("    [3.3] Ingesting papers to NotebookLM...")

    # Collect all Google Drive file IDs from manifest sources
    gdrive_file_ids = [
        entry.get('gdrive_file_id')
        for entry in manifest.get('sources', {}).values()
        if entry.get('gdrive_file_id') and entry.get('gdrive_status') == 'found'
    ]

    success_count, failed_count, errors = await _ingest_papers_to_notebooklm(
        manifest, notebook_ids, gdrive_file_ids, verbose
    )
    summary['papers_ingested'] = success_count
    summary['papers_failed'] = failed_count
    summary['errors'].extend(errors)

    # Step 4: Verify ingestion
    print("    [3.4] Verifying ingestion via queries...")
    verified, errors = await _verify_notebooklm_ingestion(notebook_ids, verbose)
    summary['papers_verified'] = verified
    summary['errors'].extend(errors)

    # Update manifest: mark papers as ingested
    for source_entry in manifest.get('sources', {}).values():
        if source_entry.get('notebooklm_source_ids'):
            source_entry['notebooklm_status'] = 'ingested'
        else:
            source_entry['notebooklm_status'] = 'pending'

    print(f"    Notebooks created: {summary['notebooks_created']}")
    print(f"    Context files synced: {summary['context_files_synced']}")
    print(f"    Papers ingested: {summary['papers_ingested']} (failed: {summary['papers_failed']})")
    print(f"    Papers verified: {summary['papers_verified']}")

    return summary


def unified_sync_check(
    check_only: bool = False,
    verbose: bool = False,
    force: bool = False,
    skip_notebooklm: bool = False
) -> dict:
    """Execute unified sync check across all 3 systems.

    Args:
        check_only: If True, don't update manifest
        verbose: Show detailed match info
        force: Ignore cached timestamps, force re-check
        skip_notebooklm: Skip NotebookLM phase (for testing)

    Returns:
        Summary dict with counts and changes
    """
    print("=" * 80)
    print("UNIFIED SYNC CHECK: Zotero <-> Google Drive <-> NotebookLM (Phase 2)")
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

        author_str = paper.get('author', '')
        creators = []
        if author_str:
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
    gdrive_lookup = {}

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

    # [3] NOTEBOOKLM SCAN (Phase 2)
    nlm_summary = {}
    if not skip_notebooklm:
        nlm_summary = asyncio.run(_notebooklm_scan(manifest, skip=skip_notebooklm, verbose=verbose))
    else:
        print("[3] Scanning NotebookLM... (SKIPPED)")

    # [4] MERGE & MATCH
    print("[4] Matching and merging entries...")
    summary = {
        'total_zotero': len(zotero_entries),
        'total_gdrive': len(gdrive_files),
        'total_notebooklm': len([s for s in manifest.get('sources', {}).values() if s.get('notebooklm_source_ids')]),
        'updated': 0,
        'new_entries': 0,
        'status_breakdown': {},
        'matches': {
            'exact': 0,
            'fuzzy': 0,
            'unmatched_zotero': [],
            'unmatched_gdrive': [],
        },
        'notebooklm': nlm_summary,
    }

    matched_gdrive = set()

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

        expected_filename = z_data['generated_filename']
        gdrive_status = 'missing'
        match_confidence = 0.0
        matched_file_id = None

        if expected_filename in gdrive_lookup:
            gdrive_status = 'found'
            match_confidence = 1.0
            matched_gdrive.add(expected_filename)
            matched_file_id = gdrive_lookup[expected_filename]['id']
            summary['matches']['exact'] += 1
            if verbose:
                print("  [EXACT] {} -> {}".format(citation_key, expected_filename))
        else:
            best_gdrive_match = None
            best_gdrive_confidence = 0.0

            for gdrive_filename in gdrive_files.keys():
                if gdrive_filename in matched_gdrive:
                    continue

                similarity = SequenceMatcher(None, expected_filename.lower(), gdrive_filename.lower()).ratio()

                if similarity > best_gdrive_confidence and similarity >= 0.7:
                    best_gdrive_confidence = similarity
                    best_gdrive_match = gdrive_filename

            if best_gdrive_match:
                gdrive_status = 'found'
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

        entry['sync_status'] = _compute_sync_status(entry)
        summary['updated'] += 1

    for gdrive_filename in gdrive_files.keys():
        if gdrive_filename not in matched_gdrive:
            summary['matches']['unmatched_gdrive'].append(gdrive_filename)

    # [5] OUTPUT
    print("\n[5] Manifest update: {} entries".format(summary['updated']))

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

    if nlm_summary:
        print("\nNOTEBOOKLM SUMMARY:")
        print("  Notebooks created:   {}".format(nlm_summary.get('notebooks_created', 0)))
        print("  Context files synced: {}".format(nlm_summary.get('context_files_synced', 0)))
        print("  Papers ingested:     {}".format(nlm_summary.get('papers_ingested', 0)))
        print("  Papers verified:     {}".format(nlm_summary.get('papers_verified', 0)))
        if nlm_summary.get('errors'):
            print("  Errors: {} (see verbose output)".format(len(nlm_summary['errors'])))

    summary['status_breakdown'] = status_counts

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
    skip_notebooklm = "--skip-notebooklm" in sys.argv

    summary = unified_sync_check(
        check_only=check_only,
        verbose=verbose,
        force=force,
        skip_notebooklm=skip_notebooklm
    )

    if summary:
        print("\nPhase 2 Status: Ready for Phase 3 (Agent integration)")
        print("=" * 80)


if __name__ == "__main__":
    main()
