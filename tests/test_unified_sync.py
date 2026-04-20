#!/usr/bin/env python3
"""End-to-end tests for unified sync check."""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from scripts.zotero_client import get_citations, generate_gdrive_filename
from scripts.unified_sync_check import _compute_sync_status, _load_manifest, unified_sync_check

class TestFilenameGeneration:
    def test_single_author(self):
        result = generate_gdrive_filename({
            'creators': [{'lastName': 'Smith', 'firstName': 'John'}],
            'title': 'Machine Learning',
            'date': '2024-01-15'
        })
        assert result == 'Smith-2024-Machine_Learning.pdf'

class TestSyncStatus:
    def test_complete_status(self):
        entry = {'zotero_status': 'active', 'gdrive_status': 'found', 'notebooklm_status': 'ingested'}
        assert _compute_sync_status(entry) == 'COMPLETE'
    
    def test_partial_status(self):
        entry = {'zotero_status': 'active', 'gdrive_status': 'found', 'notebooklm_status': 'pending'}
        assert _compute_sync_status(entry) == 'PARTIAL'

class TestEnd2End:
    @pytest.fixture(scope="class", autouse=True)
    def setup(self):
        load_dotenv()
    
    def test_sync_check_summary(self):
        summary = unified_sync_check(check_only=True, verbose=False)
        assert isinstance(summary, dict)
        assert summary['total_zotero'] > 0
        assert summary['total_gdrive'] > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
