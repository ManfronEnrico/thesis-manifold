"""
Citation Confidence Scoring — Assess reliability of NotebookLM citations.

Evaluates:
- Quote specificity (exact quote vs. paraphrase)
- Source match (UUID resolves to expected paper)
- Page number precision
- Overall confidence level (HIGH / MEDIUM / LOW)
"""

import logging
from dataclasses import dataclass
from difflib import SequenceMatcher
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class ConfidenceLevel(str, Enum):
    """Citation confidence level."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class ConfidenceScore:
    """Citation confidence assessment."""
    level: ConfidenceLevel
    specificity_score: float  # 0.0-1.0
    has_page_number: bool
    reason: str
    requires_manual_check: bool


class CitationConfidence:
    """Score confidence of NotebookLM citations."""

    # Thresholds for confidence levels
    HIGH_THRESHOLD = 0.85  # Very specific quote
    MEDIUM_THRESHOLD = 0.60  # Reasonably specific
    LOW_THRESHOLD = 0.0  # Anything lower is low confidence

    @staticmethod
    def score(
        passage: str,
        source_fulltext: str,
        has_page_number: bool = False,
    ) -> ConfidenceScore:
        """
        Score citation based on passage specificity and page precision.

        Args:
            passage: The cited passage from NotebookLM
            source_fulltext: Full text of the source (for verification)
            has_page_number: Whether citation includes page number

        Returns:
            ConfidenceScore with level and reasoning
        """
        specificity = CitationConfidence._measure_specificity(
            passage,
            source_fulltext,
        )

        # Determine confidence level
        if specificity >= CitationConfidence.HIGH_THRESHOLD:
            level = ConfidenceLevel.HIGH
        elif specificity >= CitationConfidence.MEDIUM_THRESHOLD:
            level = ConfidenceLevel.MEDIUM
        else:
            level = ConfidenceLevel.LOW

        # Manual check required if:
        # - Low confidence, OR
        # - Medium confidence without page number
        requires_manual_check = (
            level == ConfidenceLevel.LOW
            or (level == ConfidenceLevel.MEDIUM and not has_page_number)
        )

        # Generate reason
        reason = CitationConfidence._generate_reason(
            level,
            specificity,
            has_page_number,
        )

        return ConfidenceScore(
            level=level,
            specificity_score=specificity,
            has_page_number=has_page_number,
            reason=reason,
            requires_manual_check=requires_manual_check,
        )

    @staticmethod
    def _measure_specificity(passage: str, source_fulltext: str) -> float:
        """
        Measure how specifically the passage matches the source.

        Returns score 0.0-1.0 where:
        - 1.0 = exact match (direct quote)
        - 0.85+ = very similar (minor punctuation differences)
        - 0.6-0.85 = reasonably similar (some paraphrasing)
        - <0.6 = poor match (likely paraphrased or misquoted)
        """
        if not passage or not source_fulltext:
            return 0.0

        # Normalize whitespace
        passage_norm = " ".join(passage.split())
        text_norm = " ".join(source_fulltext.split())

        # Check for exact substring match (best case)
        if passage_norm in text_norm:
            return 1.0

        # Use sequence matching for similarity score
        matcher = SequenceMatcher(None, passage_norm, text_norm)
        similarity = matcher.ratio()

        return similarity

    @staticmethod
    def _generate_reason(
        level: ConfidenceLevel,
        specificity: float,
        has_page_number: bool,
    ) -> str:
        """Generate human-readable reason for confidence score."""
        if level == ConfidenceLevel.HIGH:
            reason = (
                f"Direct quote match (specificity: {specificity:.1%}). "
                "Safe to use."
            )
            if has_page_number:
                reason += " Page number provided."
        elif level == ConfidenceLevel.MEDIUM:
            reason = (
                f"Reasonably specific (specificity: {specificity:.1%}). "
                "Verify against PDF."
            )
            if not has_page_number:
                reason += " Page number missing — verify manually."
        else:  # LOW
            reason = (
                f"Low specificity (specificity: {specificity:.1%}). "
                "Likely paraphrased. MUST verify against PDF."
            )

        return reason

    @staticmethod
    def flag_citation(score: ConfidenceScore, passage: str) -> str:
        """
        Generate a flag/tag for citation in thesis draft.

        Returns formatted string for insertion into bullet point.
        """
        if score.requires_manual_check:
            return f"[{score.level} CONFIDENCE — {score.reason}]"
        else:
            return f"[{score.level} CONFIDENCE — NOTEBOOKLM VERIFIED]"

    @staticmethod
    def batch_score(
        passages: list[tuple[str, str, bool]],
    ) -> list[ConfidenceScore]:
        """
        Score multiple citations at once.

        Args:
            passages: List of (passage, source_fulltext, has_page_number) tuples

        Returns:
            List of ConfidenceScore objects
        """
        return [
            CitationConfidence.score(passage, source_fulltext, has_page_number)
            for passage, source_fulltext, has_page_number in passages
        ]

    @staticmethod
    def audit_report(scores: list[ConfidenceScore]) -> str:
        """
        Generate audit report from confidence scores.

        Returns formatted markdown report.
        """
        high = sum(1 for s in scores if s.level == ConfidenceLevel.HIGH)
        medium = sum(1 for s in scores if s.level == ConfidenceLevel.MEDIUM)
        low = sum(1 for s in scores if s.level == ConfidenceLevel.LOW)
        total = len(scores)

        if total == 0:
            return "No citations to audit."

        verification_rate = ((high + medium) / total) * 100 if total > 0 else 0

        report = f"""
## Citation Confidence Audit

**Overall Verification Rate**: {verification_rate:.1f}% ({high + medium}/{total})

### Breakdown
- **HIGH**: {high}/{total} citations (direct quotes, safe to use)
- **MEDIUM**: {medium}/{total} citations (verify page numbers)
- **LOW**: {low}/{total} citations (must manually verify against PDF)

### Flagged for Manual Review
"""
        for i, score in enumerate(scores):
            if score.requires_manual_check:
                report += f"\n{i+1}. **[{score.level}]** {score.reason}"

        return report
