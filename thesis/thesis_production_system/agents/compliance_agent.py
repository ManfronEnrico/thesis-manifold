"""
Compliance Agent — Thesis Production System (System B)
-------------------------------------------------------
Validates thesis content against CBS formal requirements.
Reads guidelines from Thesis/Thesis Guidelines/ PDFs (already extracted
to thesis/compliance/cbs_guidelines_notes.md).

Checks per section:
- Citation format (APA 7)
- Structure (required sections present)
- Character count → standard page estimate
- Mandatory elements (philosophy of science, methods, limitations)
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..state.thesis_state import ComplianceCheck, ComplianceState, ThesisState


# CBS formal constants (from thesis/compliance/cbs_guidelines_notes.md)
CHARS_PER_STANDARD_PAGE = 2_275   # characters excluding spaces
MAX_STANDARD_PAGES = 120
GUIDELINES_NOTES = Path("thesis/compliance/cbs_guidelines_notes.md")


class ComplianceAgent:
    """Runs CBS compliance checks on thesis sections."""

    def __init__(self, project_root: Path = Path(".")) -> None:
        self.project_root = project_root

    def check_section_compliance(
        self, state: ThesisState, chapter_ids: List[str]
    ) -> ThesisState:
        """
        Run CBS compliance checks on the specified chapters.
        Updates ComplianceState and marks sections as compliance_checked.
        """
        for ch_id in chapter_ids:
            section = state.sections.get(ch_id)
            if section is None or section.bullet_file is None:
                continue

            path = self.project_root / section.bullet_file
            if not path.exists():
                continue

            content = path.read_text()
            check = self._run_checks(ch_id, content)
            state.compliance_checks.checks[ch_id] = check
            state.sections[ch_id].compliance_checked = True

        # Update global character count estimate
        state = self._update_total_count(state)
        return state

    def _run_checks(self, chapter_id: str, content: str) -> ComplianceCheck:
        issues: List[str] = []

        # ── APA 7 citation format ──────────────────────────────────────────────
        # Look for citation placeholders — Cite: [Author Year] or (Author, Year)
        if "Cite:" not in content and not re.search(r"\([A-Z][a-z]+,?\s+\d{4}\)", content):
            if chapter_id not in ("frontpage", "ch1_introduction"):
                issues.append(
                    "No citation placeholders found. Add 'Cite: [Author Year]' markers "
                    "or APA-format in-text citations."
                )

        # ── Mandatory structure checks per chapter ─────────────────────────────
        mandatory = self._mandatory_sections(chapter_id)
        for section in mandatory:
            if section.lower() not in content.lower():
                issues.append(f"Missing mandatory sub-section: '{section}'")

        # ── Bullet-only check (no prose yet) ──────────────────────────────────
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        prose_lines = [
            l for l in lines
            if not l.startswith(("-", "*", "#", "|", ">", "[", "!"))
            and len(l) > 150
        ]
        if prose_lines:
            issues.append(
                f"{len(prose_lines)} line(s) appear to be prose (>150 chars). "
                "At bullet-point stage, only bullets are expected."
            )

        return ComplianceCheck(
            section=chapter_id,
            timestamp=datetime.now().isoformat(),
            issues=issues,
            passed=len(issues) == 0,
        )

    def _mandatory_sections(self, chapter_id: str) -> List[str]:
        """Return list of required sub-sections for each chapter."""
        requirements: Dict[str, List[str]] = {
            "ch3_methodology": [
                "philosophy of science",
                "design science",
                "research strategy",
                "validity",
                "limitations",
            ],
            "ch8_evaluation": [
                "threats to validity",
                "baseline",
                "metrics",
            ],
            "ch10_conclusion": [
                "theoretical contribution",
                "practical implications",
                "limitations",
                "future research",
            ],
        }
        return requirements.get(chapter_id, [])

    def _update_total_count(self, state: ThesisState) -> ThesisState:
        """Estimate total character count across all section files."""
        total_chars = 0
        for ch_id, section in state.sections.items():
            if section.bullet_file:
                path = self.project_root / section.bullet_file
                if path.exists():
                    # Count chars excluding spaces (CBS standard page formula)
                    text = path.read_text()
                    chars_no_spaces = len(text.replace(" ", ""))
                    total_chars += chars_no_spaces

        state.compliance_checks.total_character_count = total_chars
        state.compliance_checks.standard_pages_estimate = total_chars / CHARS_PER_STANDARD_PAGE
        state.compliance_checks.within_page_limit = (
            state.compliance_checks.standard_pages_estimate <= MAX_STANDARD_PAGES
        )
        return state
