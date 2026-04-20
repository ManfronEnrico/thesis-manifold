"""
NotebookLM Access Layer — Unified interface with hybrid API + fallback.

Provides dual-stack access:
- Primary: Direct API (notebooklm-py) for speed
- Fallback: Browser automation (skill-based) for robustness

All queries auto-retry on API failure with fallback.
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

import notebooklm
from notebooklm import NotebookLMClient
from notebooklm.types import AskResult, Artifact

logger = logging.getLogger(__name__)


@dataclass
class Citation:
    """A single citation with source reference."""
    source_id: str
    source_name: str
    passage: str
    page_number: Optional[int] = None


@dataclass
class QuestionResult:
    """Result from NotebookLM question query."""
    answer: str
    citations: List[Citation]
    timestamp: str
    source: str  # "api" or "skill_fallback"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answer": self.answer,
            "citations": [
                {
                    "source_id": c.source_id,
                    "source_name": c.source_name,
                    "passage": c.passage,
                    "page_number": c.page_number,
                }
                for c in self.citations
            ],
            "timestamp": self.timestamp,
            "source": self.source,
        }


@dataclass
class ResearchResult:
    """Result from NotebookLM research (gap-filling) query."""
    query: str
    papers_found: List[Dict[str, Any]]  # [{title, relevance_score, url, summary}, ...]
    timestamp: str
    source: str  # "api" or "skill_fallback"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "papers_found": self.papers_found,
            "timestamp": self.timestamp,
            "source": self.source,
        }


class NotebookLMAccess:
    """
    Unified NotebookLM interface with automatic fallback.

    Primary path: Direct API (notebooklm-py async client)
    Fallback path: Browser automation via skill (if API fails)
    """

    def __init__(self, client: Optional[NotebookLMClient] = None):
        """
        Initialize access layer.

        Args:
            client: Optional NotebookLMClient. If None, will be created from storage.
        """
        self.client = client
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the NotebookLM client from stored auth."""
        if self._initialized:
            return

        try:
            if self.client is None:
                self.client = await NotebookLMClient.from_storage()
            self._initialized = True
            logger.info("NotebookLM client initialized from storage")
        except Exception as e:
            logger.error(f"Failed to initialize NotebookLM client: {e}")
            self._initialized = False
            raise

    async def ask(
        self,
        notebook_id: str,
        question: str,
        use_fallback: bool = True,
    ) -> QuestionResult:
        """
        Query a NotebookLM notebook with a question.

        Args:
            notebook_id: ID of the notebook to query
            question: The question to ask
            use_fallback: If True, fall back to skill if API fails

        Returns:
            QuestionResult with answer and citations

        Raises:
            NotebookLMError: If both API and fallback fail (if use_fallback=True)
            RuntimeError: If use_fallback=False and API fails
        """
        try:
            await self.initialize()
            logger.info(f"Querying notebook {notebook_id}: {question[:50]}...")

            result = await self.client.chat.ask(
                notebook_id=notebook_id,
                question=question,
            )

            # Parse result (notebooklm-py returns AskResult)
            citations = self._parse_citations(result)

            return QuestionResult(
                answer=result.answer,
                citations=citations,
                timestamp=datetime.now().isoformat(),
                source="api",
            )

        except Exception as e:
            logger.warning(f"Direct API failed: {e}. Attempting fallback...")

            if use_fallback:
                return await self._ask_via_skill(notebook_id, question)
            else:
                raise RuntimeError(f"NotebookLM API failed: {e}") from e

    async def research(
        self,
        notebook_id: str,
        query: str,
        use_fallback: bool = True,
    ) -> ResearchResult:
        """
        Search for papers addressing a research query.

        Uses NotebookLM's research tool (web search + relevance ranking).

        Args:
            notebook_id: ID of the notebook context
            query: Research question or gap description
            use_fallback: If True, fall back to skill if API fails

        Returns:
            ResearchResult with candidate papers
        """
        try:
            await self.initialize()
            logger.info(f"Researching: {query[:50]}...")

            # NotebookLM research mode
            result = await self.client.research.start(
                notebook_id=notebook_id,
                query=query,
            )

            # Parse papers from result
            papers = self._parse_research_papers(result)

            return ResearchResult(
                query=query,
                papers_found=papers,
                timestamp=datetime.now().isoformat(),
                source="api",
            )

        except Exception as e:
            logger.warning(f"Direct API research failed: {e}. Attempting fallback...")

            if use_fallback:
                return await self._research_via_skill(notebook_id, query)
            else:
                raise RuntimeError(f"NotebookLM research failed: {e}") from e

    async def get_fulltext(
        self,
        source_id: str,
        notebook_id: str,
    ) -> str:
        """
        Extract full text of an indexed source for verification.

        Args:
            source_id: ID of the source (from citations)
            notebook_id: ID of the notebook containing the source

        Returns:
            Full text of the source
        """
        try:
            await self.initialize()
            logger.info(f"Extracting fulltext for source {source_id}...")

            fulltext = await self.client.sources.get_fulltext(
                notebook_id=notebook_id,
                source_id=source_id,
            )

            return fulltext

        except Exception as e:
            logger.error(f"Failed to extract fulltext: {e}")
            raise

    # --- Private fallback methods ---

    async def _ask_via_skill(self, notebook_id: str, question: str) -> QuestionResult:
        """
        Fallback: Query NotebookLM via browser automation skill.

        This is slower (10-30s) but robust to API changes.
        """
        import subprocess
        from pathlib import Path

        logger.info("Using skill-based browser automation fallback...")

        # Build command to run skill
        skill_dir = Path(".agents/skills/notebooklm")
        cmd = [
            "python",
            str(skill_dir / "scripts" / "run.py"),
            "ask_question.py",
            "--question", question,
            "--notebook-id", notebook_id,
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                # Parse skill output (assumes JSON format)
                output = json.loads(result.stdout)

                citations = [
                    Citation(
                        source_id=c.get("source_id", "unknown"),
                        source_name=c.get("source_name", "unknown"),
                        passage=c.get("passage", ""),
                        page_number=c.get("page_number"),
                    )
                    for c in output.get("citations", [])
                ]

                return QuestionResult(
                    answer=output.get("answer", ""),
                    citations=citations,
                    timestamp=datetime.now().isoformat(),
                    source="skill_fallback",
                )
            else:
                raise RuntimeError(f"Skill command failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            raise RuntimeError("Skill query timed out after 120s")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse skill output: {e}")

    async def _research_via_skill(self, notebook_id: str, query: str) -> ResearchResult:
        """
        Fallback: Research via browser automation skill.

        Returns placeholder result (skill doesn't support research mode yet).
        """
        logger.warning("Research mode not yet supported via skill fallback")

        return ResearchResult(
            query=query,
            papers_found=[],
            timestamp=datetime.now().isoformat(),
            source="skill_fallback_unavailable",
        )

    # --- Private parsing methods ---

    def _parse_citations(self, result: AskResult) -> List[Citation]:
        """Parse citations from NotebookLM AskResult."""
        citations = []

        if hasattr(result, "citations") and result.citations:
            for cite in result.citations:
                citations.append(
                    Citation(
                        source_id=getattr(cite, "source_id", "unknown"),
                        source_name=getattr(cite, "source_name", "unknown"),
                        passage=getattr(cite, "text_passage", ""),
                        page_number=getattr(cite, "page_number", None),
                    )
                )

        return citations

    def _parse_research_papers(self, result: Any) -> List[Dict[str, Any]]:
        """Parse papers from NotebookLM research result."""
        papers = []

        if hasattr(result, "papers") and result.papers:
            for paper in result.papers:
                papers.append({
                    "title": getattr(paper, "title", ""),
                    "relevance_score": getattr(paper, "relevance_score", 0.0),
                    "url": getattr(paper, "url", ""),
                    "summary": getattr(paper, "summary", ""),
                })

        return papers
