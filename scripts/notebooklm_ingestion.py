#!/usr/bin/env python3
"""
NotebookLM Ingestion Pipeline — Idempotent paper ingestion.

Scans papers/ directory, ingests new PDFs to NotebookLM notebooks,
and maintains ingestion_manifest.json as source of truth.
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

# Import NotebookLM
try:
    from notebooklm import NotebookLMClient
except ImportError:
    logger.error("notebooklm-py not installed. Run: pip install notebooklm-py")
    exit(1)


class NotebookLMIngestionManager:
    """Manage paper ingestion to NotebookLM notebooks."""

    # Chapter-to-notebook mapping
    CHAPTER_NOTEBOOKS = {
        "ch2-literature": None,  # Will be populated from manifest
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
        self.papers_dir = repo_root / "papers"
        self.manifest_path = Path(manifest_path or repo_root / "papers" / "ingestion_manifest.json")
        self.client = None
        self.manifest = None

    async def initialize(self) -> None:
        """Initialize NotebookLM client and load manifest."""
        logger.info("Initializing NotebookLM client...")
        self.client = await NotebookLMClient.from_storage()

        logger.info(f"Loading manifest from {self.manifest_path}...")
        if self.manifest_path.exists():
            with open(self.manifest_path) as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {
                "notebooks": {},
                "sources": {},
                "_last_updated": None,
            }

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

    async def find_uningesteda_papers(self) -> Dict[str, Path]:
        """
        Find papers not yet in the manifest.

        Returns:
            {paper_slug: paper_path} for papers to ingest
        """
        uningesteda = {}

        for chapter_dir in self.papers_dir.iterdir():
            if not chapter_dir.is_dir():
                continue

            for pdf_file in chapter_dir.glob("*.pdf"):
                paper_slug = pdf_file.stem
                chapter = chapter_dir.name

                # Check if already in manifest
                if paper_slug in self.manifest["sources"]:
                    logger.debug(f"  Skipping {paper_slug} (already ingested)")
                    continue

                uningesteda[f"{chapter}/{paper_slug}"] = pdf_file

        return uningesteda

    async def ingest_paper(self, paper_slug: str, paper_path: Path, chapter: str) -> Optional[str]:
        """
        Ingest a single paper to NotebookLM.

        Args:
            paper_slug: Paper identifier (filename without .pdf)
            paper_path: Full path to PDF file
            chapter: Chapter directory name

        Returns:
            NotebookLM source ID if successful, None otherwise
        """
        try:
            notebook_id = self.CHAPTER_NOTEBOOKS.get(chapter)
            if not notebook_id:
                logger.error(f"No notebook for chapter {chapter}")
                return None

            logger.info(f"  Ingesting {paper_slug} to {chapter}...")

            # Upload file to NotebookLM
            source = await self.client.sources.add_file(
                notebook_id=notebook_id,
                file_path=str(paper_path),
            )

            source_id = source.source_id

            # Record in manifest
            self.manifest["sources"][paper_slug] = {
                "local_path": str(paper_path.relative_to(self.repo_root)),
                "notebook": chapter,
                "notebooklm_source_id": source_id,
                "added_at": datetime.now().isoformat(),
                "verified": False,  # Always requires human verification
            }

            logger.info(f"  Successfully ingested {paper_slug} (ID: {source_id})")
            return source_id

        except Exception as e:
            logger.error(f"  Failed to ingest {paper_slug}: {e}")
            return None

    async def ingest_all_papers(self) -> int:
        """
        Ingest all uningesteda papers.

        Returns:
            Number of papers successfully ingested
        """
        uningesteda = await self.find_uningesteda_papers()

        if not uningesteda:
            logger.info("No uningesteda papers found.")
            return 0

        logger.info(f"Found {len(uningesteda)} papers to ingest.")

        success_count = 0
        for paper_key, paper_path in uningesteda.items():
            chapter, paper_slug = paper_key.split("/", 1)
            source_id = await self.ingest_paper(paper_slug, paper_path, chapter)
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
                        f"  {paper_slug}: manifest ID {manifest_id} not in {chapter} notebook"
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
        logger.info("=== NotebookLM Ingestion Pipeline ===")

        await self.initialize()
        await self.ensure_notebooks()

        ingested = await self.ingest_all_papers()
        logger.info(f"Ingested {ingested} papers.")

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
        manager = NotebookLMIngestionManager()
        await manager.run()
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
