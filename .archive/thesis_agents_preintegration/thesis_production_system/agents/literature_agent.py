"""
Literature Agent — Thesis Production System (System B)
-------------------------------------------------------
Manages the literature corpus: scraping, annotation, gap analysis, and
RQ refinement. Writes outputs to thesis/literature/.

This agent is a THESIS PRODUCTION tool — it is NOT part of the research
framework evaluated in the thesis.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from ..state.thesis_state import LiteratureState, PaperRecord, ThesisState


PAPERS_DIR = Path("thesis/literature/papers")
SCRAPING_LOG = Path("thesis/literature/scraping_log.md")
GAP_ANALYSIS = Path("thesis/literature/gap_analysis.md")


class LiteratureAgent:
    """
    Manages all literature-related tasks:
    - run_scraping: search for new papers (appends to scraping_log.md)
    - confirm_pending_papers: move confirmed papers to corpus
    - update_gap_analysis: revise gap_analysis.md based on new annotations
    - propose_rq_refinement: flag if new papers suggest RQ changes
    """

    def __init__(self, project_root: Path = Path(".")) -> None:
        self.project_root = project_root

    # ── Actions ────────────────────────────────────────────────────────────────

    def run_scraping(self, state: ThesisState) -> ThesisState:
        """
        Search for new papers across 6 research angles.
        Appends proposed additions to scraping_log.md.
        Does NOT add to corpus — requires human confirmation.
        """
        # Implementation: use web search tools to query arXiv, Semantic Scholar, etc.
        # Angle queries defined in thesis/literature/scraping_log.md
        raise NotImplementedError(
            "Scraping requires web search tool access. "
            "Use Claude Code with web search enabled."
        )

    def confirm_papers(
        self, state: ThesisState, confirmed_titles: list[str]
    ) -> ThesisState:
        """
        Move papers from pending → confirmed in ThesisState.
        Updates scraping_log.md Confirmed Additions table.
        """
        for title in confirmed_titles:
            if title in state.literature_state.papers:
                state.literature_state.papers[title].confirmed = True
        self._update_scraping_log_confirmed(confirmed_titles)
        return state

    def update_gap_analysis(self, state: ThesisState) -> ThesisState:
        """
        Revise thesis/literature/gap_analysis.md based on newly confirmed papers.
        Outputs to the same file (incremental update).
        """
        confirmed = [
            p for p in state.literature_state.papers.values() if p.confirmed
        ]
        # Implementation: synthesise confirmed papers → update gap analysis
        raise NotImplementedError("Gap analysis update: implement with annotation synthesis.")

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _update_scraping_log_confirmed(self, confirmed_titles: list[str]) -> None:
        """Append confirmed papers to the 'Confirmed Additions' table in scraping_log.md."""
        from datetime import date
        log_path = self.project_root / SCRAPING_LOG
        if not log_path.exists():
            return

        today = date.today().isoformat()
        additions = "\n".join(
            f"| — | {title} | {today} | Confirmed |"
            for title in confirmed_titles
        )

        content = log_path.read_text()
        # Replace the pending placeholder
        updated = content.replace(
            "| — | Pending confirmation | — | — |",
            additions,
        )
        log_path.write_text(updated)
