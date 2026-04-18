#!/usr/bin/env python3
"""
NotebookLM Ingestion Pipeline — Google Drive as source of truth.

Uses Google Drive as the authoritative paper repository. Both collaborators
can run this script without needing local PDF copies.

Papers organized in Google Drive by chapter:
  /Thesis Papers/
    ├── ch2-literature/
    ├── ch3-methodology/
    ├── ch4-models/
    ├── ch5-synthesis/
    ├── ch6-evaluation/
    └── thesis-defense/
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

# Import NotebookLM and Google Drive
try:
    from notebooklm import NotebookLMClient
except ImportError:
    logger.error("notebooklm-py not installed. Run: pip install notebooklm-py")
    exit(1)


class GoogleDriveNotebookLMIngestion:
    """
    Manage paper ingestion to NotebookLM using Google Drive as source of truth.

    Papers are stored in a shared Google Drive folder and referenced by ID.
    Manifest tracks which Google Drive files have been ingested to which notebooks.
    """

    # Chapter-to-notebook mapping
    CHAPTER_NOTEBOOKS = {
        "ch2-literature": None,  # Will be populated from manifest
        "ch3-methodology": None,
        "ch4-models": None,
        "ch5-synthesis": None,
        "ch6-evaluation": None,
        "thesis-defense": None,
    }

    # Google Drive folder structure
    # Update these with your actual shared folder IDs
    GDRIVE_ROOT_FOLDER_ID = None  # Set via environment or config
    GDRIVE_CHAPTER_FOLDERS = {
        "ch2-literature": None,
        "ch3-methodology": None,
        "ch4-models": None,
        "ch5-synthesis": None,
        "ch6-evaluation": None,
        "thesis-defense": None,
    }

    def __init__(self, repo_root: Path = Path("."), manifest_path: Optional[str] = None):
        """
        Initialize ingestion manager.

        Args:
            repo_root: Repository root path
            manifest_path: Path to ingestion_manifest.json
        """
        self.repo_root = repo_root
        self.manifest_path = Path(manifest_path or repo_root / "papers" / "ingestion_manifest.json")
        self.client = None
        self.manifest = None
        self.drive_service = None

    async def initialize(self) -> None:
        """Initialize NotebookLM client and load manifest."""
        logger.info("Initializing NotebookLM client...")
        self.client = await NotebookLMClient.from_storage()

        logger.info("Initializing Google Drive service...")
        self._init_drive_service()

        logger.info(f"Loading manifest from {self.manifest_path}...")
        if self.manifest_path.exists():
            with open(self.manifest_path) as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {
                "notebooks": {},
                "sources": {},
                "gdrive_root_folder_id": self.GDRIVE_ROOT_FOLDER_ID,
                "gdrive_chapter_folders": self.GDRIVE_CHAPTER_FOLDERS,
                "_last_updated": None,
            }

    def _init_drive_service(self) -> None:
        """Initialize Google Drive service (requires authentication)."""
        try:
            from google.colab import auth
            from googleapiclient.discovery import build

            auth.authenticate_user()
            self.drive_service = build("drive", "v3")
            logger.info("Google Drive service initialized (Colab auth)")
        except ImportError:
            try:
                from google.auth.transport.requests import Request
                from google.oauth2.service_account import Credentials
                from googleapiclient.discovery import build
                import os

                # Try service account (if running on server)
                credentials_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
                if credentials_file:
                    creds = Credentials.from_service_account_file(
                        credentials_file,
                        scopes=["https://www.googleapis.com/auth/drive.readonly"],
                    )
                    self.drive_service = build("drive", "v3", credentials=creds)
                    logger.info("Google Drive service initialized (service account)")
                else:
                    logger.warning("No Google Drive credentials found. Ingestion may fail.")
                    logger.info("Set GOOGLE_APPLICATION_CREDENTIALS or authenticate via Colab.")
            except Exception as e:
                logger.warning(f"Could not initialize Google Drive service: {e}")
                logger.info("You can still query existing NotebookLM notebooks directly.")

    async def ensure_notebooks(self) -> None:
        """Ensure all chapter notebooks exist; create if needed."""
        logger.info("Ensuring chapter notebooks exist...")

        for chapter in self.CHAPTER_NOTEBOOKS.keys():
            notebook_id = self.manifest["notebooks"].get(chapter)

            if notebook_id:
                logger.info(f"  {chapter}: Using existing notebook {notebook_id}")
                self.CHAPTER_NOTEBOOKS[chapter] = notebook_id
            else:
                # Create new notebook
                logger.info(f"  {chapter}: Creating new notebook...")
                notebook = await self.client.notebooks.create(
                    title=f"thesis-{chapter}",
                    description=f"Thesis chapter: {chapter}",
                )
                notebook_id = notebook.notebook_id
                self.CHAPTER_NOTEBOOKS[chapter] = notebook_id
                self.manifest["notebooks"][chapter] = notebook_id

                logger.info(f"  {chapter}: Created with ID {notebook_id}")

    def _list_gdrive_papers(self, folder_id: str, chapter: str) -> List[Dict]:
        """
        List all PDFs in a Google Drive folder.

        Args:
            folder_id: Google Drive folder ID
            chapter: Chapter name (for logging)

        Returns:
            List of {file_id, file_name, drive_path}
        """
        if not self.drive_service or not folder_id:
            logger.warning(f"  {chapter}: No Drive service or folder ID. Skipping.")
            return []

        try:
            query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                spaces="drive",
                fields="files(id, name, webViewLink)",
                pageSize=100,
            ).execute()

            papers = [
                {
                    "file_id": f["id"],
                    "file_name": f["name"],
                    "drive_link": f.get("webViewLink", ""),
                }
                for f in results.get("files", [])
            ]

            logger.info(f"  {chapter}: Found {len(papers)} PDFs on Google Drive")
            return papers

        except Exception as e:
            logger.error(f"  {chapter}: Failed to list Drive papers: {e}")
            return []

    async def ingest_paper_from_drive(
        self,
        file_id: str,
        file_name: str,
        drive_link: str,
        chapter: str,
    ) -> Optional[str]:
        """
        Ingest a paper from Google Drive to NotebookLM.

        Args:
            file_id: Google Drive file ID
            file_name: File name (for reference)
            drive_link: Google Drive web link
            chapter: Chapter name

        Returns:
            NotebookLM source ID if successful, None otherwise
        """
        try:
            notebook_id = self.CHAPTER_NOTEBOOKS.get(chapter)
            if not notebook_id:
                logger.error(f"No notebook for chapter {chapter}")
                return None

            paper_slug = file_id  # Use Drive file ID as unique slug

            # Check if already ingested
            if paper_slug in self.manifest["sources"]:
                logger.info(f"  Skipping {file_name} (already ingested, ID: {paper_slug})")
                return None

            logger.info(f"  Ingesting {file_name} from Google Drive to {chapter}...")

            # Add file via Google Drive ID to NotebookLM
            # NotebookLM supports adding files by Drive ID
            source = await self.client.sources.add_drive(
                notebook_id=notebook_id,
                file_id=file_id,
            )

            source_id = source.source_id

            # Record in manifest
            self.manifest["sources"][paper_slug] = {
                "file_name": file_name,
                "gdrive_file_id": file_id,
                "gdrive_link": drive_link,
                "notebook": chapter,
                "notebooklm_source_id": source_id,
                "added_at": datetime.now().isoformat(),
                "verified": False,  # Always requires human verification
            }

            logger.info(f"  Successfully ingested {file_name} (NotebookLM ID: {source_id})")
            return source_id

        except Exception as e:
            logger.error(f"  Failed to ingest {file_name}: {e}")
            return None

    async def ingest_all_papers_from_drive(self) -> int:
        """
        Ingest all papers from Google Drive.

        Returns:
            Number of papers successfully ingested
        """
        if not self.drive_service:
            logger.error("Google Drive service not initialized. Cannot ingest from Drive.")
            logger.info("You can still query existing NotebookLM notebooks directly.")
            return 0

        success_count = 0

        for chapter, folder_id in self.GDRIVE_CHAPTER_FOLDERS.items():
            if not folder_id:
                logger.warning(f"Skipping {chapter}: No Drive folder ID configured")
                continue

            papers = self._list_gdrive_papers(folder_id, chapter)

            for paper in papers:
                source_id = await self.ingest_paper_from_drive(
                    file_id=paper["file_id"],
                    file_name=paper["file_name"],
                    drive_link=paper["drive_link"],
                    chapter=chapter,
                )
                if source_id:
                    success_count += 1

        return success_count

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

        Compares manifest sources against actual sources in each notebook.

        Returns:
            True if integrity check passes, False otherwise
        """
        logger.info("Verifying manifest integrity...")

        issues = []

        for chapter, notebook_id in self.CHAPTER_NOTEBOOKS.items():
            if not notebook_id:
                continue

            # Get actual sources in notebook
            actual_sources = await self.client.sources.list(notebook_id=notebook_id)
            actual_ids = {s.source_id for s in actual_sources}

            # Check manifest sources for this chapter
            for paper_slug, record in self.manifest["sources"].items():
                if record["notebook"] != chapter:
                    continue

                manifest_id = record.get("notebooklm_source_id")
                if manifest_id not in actual_ids:
                    issues.append(
                        f"  {record.get('file_name', paper_slug)}: "
                        f"manifest ID {manifest_id} not in {chapter} notebook"
                    )

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
        logger.info("=== NotebookLM Ingestion Pipeline (Google Drive Source) ===")

        await self.initialize()
        await self.ensure_notebooks()

        ingested = await self.ingest_all_papers_from_drive()
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
        manager = GoogleDriveNotebookLMIngestion()
        await manager.run()
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
