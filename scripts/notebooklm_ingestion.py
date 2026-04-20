#!/usr/bin/env python3
"""
NotebookLM Ingestion Pipeline — Integrated with Google Drive API.

Uses the existing GoogleDriveAPI to list papers from shared Drive folder,
then ingests them to NotebookLM notebooks.

Both collaborators run this script — it detects which papers are already
ingested via the manifest and skips them.

Workflow:
  GoogleDriveAPI (src/google_drive_integration.py)
    ↓ (lists papers with metadata)
  NotebookLMAccess (thesis/thesis_agents/thesis_production_system/research/notebooklm_access.py)
    ↓ (adds papers to notebooks)
  Manifest (thesis/literature/ingestion_manifest.json)
    ↓ (persists ingestion state)
  Git
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Import NotebookLM access layer
try:
    from thesis.thesis_agents.thesis_production_system.research import NotebookLMAccess
except ImportError:
    logger.error("NotebookLMAccess not found. Ensure thesis/thesis_agents/thesis_production_system is in PYTHONPATH.")
    exit(1)

# Import Google Drive API
try:
    from src.google_drive_integration import GoogleDriveAPI
except ImportError:
    logger.error("GoogleDriveAPI not found. Ensure src/ is in PYTHONPATH.")
    exit(1)


class NotebookLMIngestFromDrive:
    """
    Ingest papers from Google Drive to NotebookLM using existing integrations.

    Uses:
    - GoogleDriveAPI (src/google_drive_integration.py) to list papers
    - NotebookLMAccess (thesis/thesis_agents/thesis_production_system/research/) to add to notebooks
    """

    # Chapter-to-notebook mapping
    CHAPTER_NOTEBOOKS = {
        "ch2-literature": None,
        "ch3-methodology": None,
        "ch4-models": None,
        "ch5-synthesis": None,
        "ch6-evaluation": None,
        "thesis-defense": None,
    }

    # Google Drive folder structure (inferred from GoogleDriveAPI)
    # GoogleDriveAPI looks in importance folders within the papers folder
    # We map papers to chapters based on their importance level or folder structure
    IMPORTANCE_TO_CHAPTER = {
        "essential": "ch2-literature",      # Core papers
        "high": "ch3-methodology",          # Important methodological papers
        "unsure": "ch4-models",             # Papers under evaluation
        "not_relevant": None,               # Skip these
    }

    def __init__(self, repo_root: Path = Path("."), manifest_path: Optional[str] = None):
        """
        Initialize ingestion manager.

        Args:
            repo_root: Repository root path
            manifest_path: Path to ingestion_manifest.json
        """
        self.repo_root = repo_root
        self.manifest_path = Path(manifest_path or repo_root / "thesis" / "literature" / "ingestion_manifest.json")
        self.nlm_client = None
        self.drive_api = None
        self.manifest = None

    async def initialize(self) -> None:
        """Initialize NotebookLM and Google Drive clients, load manifest."""
        logger.info("Initializing NotebookLM client...")
        self.nlm_client = NotebookLMAccess()
        await self.nlm_client.initialize()

        logger.info("Initializing Google Drive API...")
        try:
            import os
            # Try service account first (for automation)
            service_account_key = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY")
            if service_account_key:
                self.drive_api = GoogleDriveAPI(service_account_key_json=service_account_key)
            else:
                # Fall back to default (assumes already authenticated via MCP)
                self.drive_api = GoogleDriveAPI()
        except Exception as e:
            logger.warning(f"Google Drive initialization: {e}")
            logger.info("Make sure Google Drive credentials are configured.")

        logger.info(f"Loading manifest from {self.manifest_path}...")
        if self.manifest_path.exists():
            with open(self.manifest_path) as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {
                "notebooks": {},
                "sources": {},
                "_last_updated": None,
                "_integration": "GoogleDriveAPI + NotebookLMAccess",
            }

    async def ensure_notebooks(self) -> None:
        """Ensure all chapter notebooks exist; create if needed."""
        logger.info("Ensuring chapter notebooks exist...")

        for chapter in self.CHAPTER_NOTEBOOKS.keys():
            if not chapter:  # Skip None entries
                continue

            notebook_id = self.manifest["notebooks"].get(chapter)

            if notebook_id:
                logger.info(f"  {chapter}: Using existing notebook {notebook_id}")
                self.CHAPTER_NOTEBOOKS[chapter] = notebook_id
            else:
                # Create new notebook
                logger.info(f"  {chapter}: Creating new notebook...")
                try:
                    notebook = await self.nlm_client.client.notebooks.create(
                        title=f"thesis-{chapter}",
                        description=f"Thesis chapter: {chapter}",
                    )
                    notebook_id = notebook.notebook_id
                    self.CHAPTER_NOTEBOOKS[chapter] = notebook_id
                    self.manifest["notebooks"][chapter] = notebook_id
                    logger.info(f"  {chapter}: Created with ID {notebook_id}")
                except Exception as e:
                    logger.error(f"  {chapter}: Failed to create notebook: {e}")

    async def ingest_papers_from_drive(self) -> int:
        """
        List papers from Google Drive and ingest to NotebookLM.

        Returns:
            Number of papers successfully ingested
        """
        if not self.drive_api:
            logger.error("Google Drive API not initialized. Cannot ingest papers.")
            return 0

        success_count = 0

        try:
            # Get all papers from Google Drive (includes metadata and importance)
            logger.info("Listing papers from Google Drive...")
            papers = self.drive_api.list_papers_with_metadata()
            logger.info(f"Found {len(papers)} papers in Google Drive.")

            for paper in papers:
                file_id = paper.get("id")
                file_name = paper.get("name", "Unknown")
                importance = paper.get("importance", "unsure")
                folder_path = paper.get("folder_path", "")

                # Map importance to chapter (can be customized)
                chapter = self.IMPORTANCE_TO_CHAPTER.get(importance)

                if not chapter:
                    logger.debug(f"  Skipping {file_name}: importance '{importance}' not mapped to chapter")
                    continue

                # Check if already ingested
                if file_id in self.manifest["sources"]:
                    logger.info(f"  Skipping {file_name} (already ingested)")
                    continue

                # Ingest to NotebookLM
                notebook_id = self.CHAPTER_NOTEBOOKS.get(chapter)
                if not notebook_id:
                    logger.warning(f"  {file_name}: No notebook for chapter {chapter}")
                    continue

                try:
                    logger.info(f"  Ingesting {file_name} to {chapter}...")

                    # Add via Drive file ID to NotebookLM
                    source = await self.nlm_client.client.sources.add_drive(
                        notebook_id=notebook_id,
                        file_id=file_id,
                    )

                    source_id = source.source_id

                    # Record in manifest
                    self.manifest["sources"][file_id] = {
                        "file_name": file_name,
                        "gdrive_file_id": file_id,
                        "importance": importance,
                        "folder_path": folder_path,
                        "chapter": chapter,
                        "notebooklm_source_id": source_id,
                        "added_at": datetime.now().isoformat(),
                        "verified": False,
                    }

                    logger.info(f"  Successfully ingested {file_name}")
                    success_count += 1

                except Exception as e:
                    logger.error(f"  Failed to ingest {file_name}: {e}")

            return success_count

        except Exception as e:
            logger.error(f"Failed to ingest papers: {e}")
            return 0

    def save_manifest(self) -> None:
        """Save manifest to JSON."""
        self.manifest["_last_updated"] = datetime.now().isoformat()

        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=2)

        logger.info(f"Manifest saved to {self.manifest_path}")

    async def verify_manifest_integrity(self) -> bool:
        """
        Verify manifest matches actual notebook state.

        Returns:
            True if integrity check passes, False otherwise
        """
        logger.info("Verifying manifest integrity...")

        issues = []

        for chapter, notebook_id in self.CHAPTER_NOTEBOOKS.items():
            if not notebook_id or not chapter:
                continue

            try:
                # Get actual sources in notebook
                actual_sources = await self.nlm_client.client.sources.list(notebook_id=notebook_id)
                actual_ids = {s.source_id for s in actual_sources}

                # Check manifest sources for this chapter
                for paper_id, record in self.manifest["sources"].items():
                    if record.get("chapter") != chapter:
                        continue

                    manifest_id = record.get("notebooklm_source_id")
                    if manifest_id not in actual_ids:
                        issues.append(
                            f"  {record.get('file_name', paper_id)}: "
                            f"manifest ID {manifest_id} not in {chapter} notebook"
                        )

            except Exception as e:
                logger.warning(f"  {chapter}: Could not verify: {e}")

        if issues:
            logger.error("Integrity issues found:")
            for issue in issues:
                logger.error(issue)
            return False
        else:
            logger.info("Manifest integrity verified.")
            return True

    async def run(self) -> None:
        """Run full ingestion pipeline."""
        logger.info("=== NotebookLM Ingestion Pipeline (Google Drive Integrated) ===")

        await self.initialize()
        await self.ensure_notebooks()

        ingested = await self.ingest_papers_from_drive()
        logger.info(f"Ingested {ingested} papers from Google Drive.")

        self.save_manifest()

        # Verify integrity
        integrity_ok = await self.verify_manifest_integrity()

        if integrity_ok:
            logger.info("Ingestion complete. All papers verified.")
        else:
            logger.warning("Ingestion complete with integrity warnings. Review manifest.")


async def main():
    """Main entry point."""
    import sys

    try:
        manager = NotebookLMIngestFromDrive()
        await manager.run()
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
