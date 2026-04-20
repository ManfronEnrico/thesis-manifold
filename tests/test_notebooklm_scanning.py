"""
End-to-end tests for Phase 2: NotebookLM scanning and integration.

Tests verify real NotebookLM API functionality:
- Notebook creation
- Context file syncing
- Paper ingestion from Google Drive
- Query verification with citations
- Manifest updates

These are integration tests that require:
- Valid NotebookLM authentication (via storage)
- Google Drive API credentials
- Real papers in Google Drive

Run with: pytest tests/test_notebooklm_scanning.py -v
"""

import pytest
import asyncio
import json
from pathlib import Path
from datetime import datetime

# Only run if NotebookLM access is available
pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="session")
async def nlm_client():
    """Initialize NotebookLMAccess client."""
    try:
        from thesis.thesis_production_system.research import NotebookLMAccess
        client = NotebookLMAccess()
        await client.initialize()
        return client
    except Exception as e:
        pytest.skip(f"NotebookLM not available: {e}")


@pytest.fixture(scope="session")
def gdrive_api():
    """Initialize Google Drive API."""
    try:
        import os
        from src.google_drive_integration import GoogleDriveAPI
        service_account = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY")
        if not service_account:
            pytest.skip("Google Drive credentials not configured")
        return GoogleDriveAPI(service_account_key_json=service_account)
    except Exception as e:
        pytest.skip(f"Google Drive API not available: {e}")


@pytest.fixture
def manifest_path():
    """Path to ingestion manifest."""
    return Path("thesis/literature/ingestion_manifest.json")


@pytest.fixture
def thesis_components_path():
    """Path to thesis components directory."""
    return Path("thesis/thesis-context/chapters")


# ============================================================================
# Test Suite
# ============================================================================


async def test_notebooklm_client_initialization(nlm_client):
    """
    Verify NotebookLMAccess initializes successfully.

    This test confirms:
    - Client can be created
    - Authentication from storage works
    - Client is ready for operations
    """
    assert nlm_client is not None
    assert nlm_client.client is not None
    assert nlm_client._initialized


async def test_notebooklm_notebook_creation(nlm_client):
    """
    Verify real notebook creation via NotebookLM API.

    This test:
    - Creates a test notebook
    - Verifies notebook ID is returned
    - Notebook is queryable
    """
    # Create test notebook
    notebook = await nlm_client.client.notebooks.create(
        title="test-notebook-phase2",
        description="Test notebook for Phase 2 verification"
    )

    # Verify notebook was created
    assert notebook is not None
    assert notebook.notebook_id is not None
    assert len(notebook.notebook_id) > 0

    # Cleanup: delete test notebook
    try:
        await nlm_client.client.notebooks.delete(notebook.notebook_id)
    except:
        pass


async def test_thesis_components_exist(thesis_components_path):
    """
    Verify thesis components directory and context files exist.

    This test:
    - Checks thesis/thesis-context/chapters/ exists
    - Verifies all required context files exist
    """
    assert thesis_components_path.exists(), f"Thesis components directory not found: {thesis_components_path}"

    # Check for required context files
    required_files = [
        "research-questions.md",
        "ch2-literature-review.md",
        "srq1-models-efficiency.md",
        "srq2-multi-agent-architecture.md",
        "srq3-contextual-information.md",
        "srq4-comparison-to-traditional-bi.md",
        "thesis-defense.md",
    ]

    for filename in required_files:
        filepath = thesis_components_path / filename
        assert filepath.exists(), f"Context file not found: {filepath}"


async def test_thesis_components_content_structure(thesis_components_path):
    """
    Verify context files have proper structure.

    This test:
    - Reads each context file
    - Verifies front matter (YAML)
    - Verifies markdown content
    """
    context_files = [
        "ch2-literature-review.md",
        "srq1-models-efficiency.md",
        "srq2-multi-agent-architecture.md",
        "srq3-contextual-information.md",
        "srq4-comparison-to-traditional-bi.md",
        "thesis-defense.md",
    ]

    for filename in context_files:
        filepath = thesis_components_path / filename
        content = filepath.read_text(encoding='utf-8')

        # Check for YAML front matter
        assert content.startswith("---"), f"{filename}: Missing YAML front matter"
        assert "---" in content[3:], f"{filename}: Incomplete YAML front matter"

        # Check for markdown headers
        assert "# " in content, f"{filename}: No markdown headers found"

        # Check for meaningful content
        assert len(content) > 200, f"{filename}: Content too short"


async def test_context_file_sync_to_notebooklm(nlm_client, thesis_components_path):
    """
    Verify context files can be synced to NotebookLM.

    This test:
    - Creates a test notebook
    - Syncs a context file as text source
    - Verifies source appears in notebook
    """
    # Create test notebook
    notebook = await nlm_client.client.notebooks.create(
        title="test-context-sync",
        description="Test context sync"
    )
    notebook_id = notebook.notebook_id

    try:
        # Read context file
        context_path = thesis_components_path / "ch2-literature-review.md"
        context_content = context_path.read_text(encoding='utf-8')

        # Sync to notebook
        source = await nlm_client.client.sources.add_text(
            notebook_id=notebook_id,
            text=context_content,
            title="Test Context"
        )

        # Verify source was created
        assert source is not None
        assert source.source_id is not None

        # Verify source is in notebook
        sources = await nlm_client.client.sources.list(notebook_id=notebook_id)
        source_ids = {s.source_id for s in sources}
        assert source.source_id in source_ids

    finally:
        # Cleanup
        try:
            await nlm_client.client.notebooks.delete(notebook_id)
        except:
            pass


async def test_google_drive_paper_retrieval(gdrive_api):
    """
    Verify Google Drive API returns papers.

    This test:
    - Lists papers from Google Drive
    - Verifies metadata is present
    - Verifies file IDs are valid
    """
    papers = gdrive_api.list_papers_with_metadata()

    # Should have papers
    assert len(papers) > 0, "No papers found in Google Drive"

    # Check paper structure
    for paper in papers[:5]:  # Check first 5
        assert 'id' in paper, "Paper missing 'id' field"
        assert 'name' in paper, "Paper missing 'name' field"
        assert len(paper['id']) > 0, "Paper ID is empty"


async def test_paper_ingestion_to_notebooklm(nlm_client, gdrive_api):
    """
    Verify papers can be ingested from Google Drive to NotebookLM.

    This test:
    - Creates a test notebook
    - Gets a paper from Google Drive
    - Ingests it to the notebook
    - Verifies source ID is returned
    """
    # Create test notebook
    notebook = await nlm_client.client.notebooks.create(
        title="test-paper-ingestion",
        description="Test paper ingestion"
    )
    notebook_id = notebook.notebook_id

    try:
        # Get first paper from Google Drive
        papers = gdrive_api.list_papers_with_metadata()
        if not papers:
            pytest.skip("No papers in Google Drive to test ingestion")

        first_paper = papers[0]
        gdrive_file_id = first_paper['id']

        # Ingest to notebook
        source = await nlm_client.client.sources.add_drive(
            notebook_id=notebook_id,
            file_id=gdrive_file_id
        )

        # Verify source was created
        assert source is not None
        assert source.source_id is not None
        assert len(source.source_id) > 0

        # Verify source is in notebook
        sources = await nlm_client.client.sources.list(notebook_id=notebook_id)
        source_ids = {s.source_id for s in sources}
        assert source.source_id in source_ids

    finally:
        # Cleanup
        try:
            await nlm_client.client.notebooks.delete(notebook_id)
        except:
            pass


async def test_notebooklm_query_with_citations(nlm_client, gdrive_api):
    """
    Verify NotebookLM can answer questions with citations.

    This test:
    - Creates notebook with paper(s)
    - Queries with a question
    - Verifies answer and citations are returned
    """
    # Create test notebook
    notebook = await nlm_client.client.notebooks.create(
        title="test-query",
        description="Test query"
    )
    notebook_id = notebook.notebook_id

    try:
        # Ingest one paper
        papers = gdrive_api.list_papers_with_metadata()
        if not papers:
            pytest.skip("No papers to test query")

        source = await nlm_client.client.sources.add_drive(
            notebook_id=notebook_id,
            file_id=papers[0]['id']
        )

        # Query the notebook
        result = await nlm_client.ask(notebook_id, "What is discussed in this paper?")

        # Verify result
        assert result is not None
        assert result.answer is not None
        assert len(result.answer) > 0
        assert result.source == "api"  # Should use API, not fallback

        # Verify citations (if available)
        assert isinstance(result.citations, list)

    finally:
        try:
            await nlm_client.client.notebooks.delete(notebook_id)
        except:
            pass


async def test_manifest_notebook_id_persistence(manifest_path, nlm_client):
    """
    Verify notebook IDs are persisted to manifest.

    This test:
    - Creates a notebook
    - Saves ID to manifest
    - Reloads manifest
    - Verifies ID is present
    """
    # Create test notebook
    notebook = await nlm_client.client.notebooks.create(
        title="test-persistence",
        description="Test ID persistence"
    )
    notebook_id = notebook.notebook_id

    try:
        # Load manifest
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

        # Save notebook ID to manifest (simulate what unified_sync_check does)
        manifest['notebooks']['ch2-literature'] = notebook_id

        # Write back
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')

        # Reload and verify
        reloaded = json.loads(manifest_path.read_text(encoding='utf-8'))
        assert reloaded['notebooks']['ch2-literature'] == notebook_id

    finally:
        try:
            await nlm_client.client.notebooks.delete(notebook_id)
        except:
            pass

        # Cleanup: reset manifest
        try:
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            manifest['notebooks']['ch2-literature'] = None
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        except:
            pass


async def test_manifest_source_id_tracking(manifest_path):
    """
    Verify manifest can track NotebookLM source IDs.

    This test:
    - Creates a manifest entry with source IDs
    - Verifies structure is correct
    - Verifies per-notebook tracking works
    """
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

    # Create test entry
    test_entry = {
        'citation_key': 'test_paper_2024',
        'gdrive_file_id': 'test-file-id-123',
        'notebooklm_source_ids': {
            'ch2-literature': 'src-uuid-1',
            'srq1-models': 'src-uuid-2',
            'thesis-defense': 'src-uuid-3',
        },
        'notebooklm_status': 'ingested',
    }

    # Add to manifest
    manifest['sources']['test_paper_2024'] = test_entry
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')

    # Reload and verify
    reloaded = json.loads(manifest_path.read_text(encoding='utf-8'))
    loaded_entry = reloaded['sources']['test_paper_2024']

    assert loaded_entry['notebooklm_source_ids']['ch2-literature'] == 'src-uuid-1'
    assert loaded_entry['notebooklm_source_ids']['srq1-models'] == 'src-uuid-2'
    assert loaded_entry['notebooklm_status'] == 'ingested'

    # Cleanup
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        del manifest['sources']['test_paper_2024']
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    except:
        pass
