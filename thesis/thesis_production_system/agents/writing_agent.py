"""
Writing Agent — Thesis Production System (System B)
----------------------------------------------------
Produces BULLET POINTS for thesis sections. Never writes prose directly.
Every bullet point output must pass the Critic Agent before state update.

Output location: thesis/writing/sections/{chapter_id}.md
Output format: Markdown bullet points with 'Cite:' placeholders.

MANDATORY RULE: This agent produces bullet points ONLY.
Prose is written by the student after human approval of bullet points.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from ..state.thesis_state import SectionState, ThesisState


SECTIONS_DIR = Path("thesis/writing/sections")


class WritingAgent:
    """
    Generates thesis section bullet point skeletons.
    Reads existing chapter files to avoid re-generating completed sections.
    Requires human approval before marking status as 'bullets_approved'.
    """

    def __init__(self, project_root: Path = Path(".")) -> None:
        self.project_root = project_root

    def draft_section_bullets(
        self, state: ThesisState, chapter_ids: List[str]
    ) -> ThesisState:
        """
        Generate bullet point skeletons for the specified chapters.
        Writes to thesis/writing/sections/{chapter_id}.md.
        Updates SectionState to 'bullets_draft' for each chapter.
        Does NOT set 'bullets_approved' — human approval required.
        """
        for ch_id in chapter_ids:
            path = self.project_root / SECTIONS_DIR / f"{ch_id}.md"
            if path.exists():
                # Already has content — do not overwrite; flag for review instead
                if ch_id not in state.sections:
                    state.sections[ch_id] = SectionState(
                        chapter=ch_id,
                        status="bullets_draft",
                        bullet_file=str(path),
                    )
                continue

            bullets = self._generate_bullets(ch_id, state)
            if bullets:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(bullets)
                state.sections[ch_id] = SectionState(
                    chapter=ch_id,
                    status="bullets_draft",
                    bullet_file=str(path),
                )

        return state

    def _generate_bullets(self, chapter_id: str, state: ThesisState) -> Optional[str]:
        """
        Return bullet point content for a chapter.
        Currently all non-empty chapters already have skeletons —
        this handles any chapter not yet written.
        """
        templates = {
            "ch4_data_assessment": self._ch4_template,
        }
        generator = templates.get(chapter_id)
        if generator:
            return generator(state)
        return None  # No template available — WritingAgent will need human input

    def _ch4_template(self, state: ThesisState) -> str:
        return """\
# Chapter 4 — Data Assessment
> Status: BULLET POINT SKELETON — not prose yet
> Last updated: PENDING

---

## 4.1 Nielsen CSD dataset

- Star schema: 4 tables (dim_market, dim_period, dim_product, facts)
- Scope: 28 Danish retailers, ~36 monthly periods, CSD category
- Key metrics: sales_value, sales_in_liters, sales_units, promo flags, weighted_distribution
- ⚠️ Access status: NOT YET OBTAINED — pending Manifold AI confirmation
- Cite: docs/data/nielsen_assessment.md; Xu et al. 2024 (3PL forecasting)

## 4.2 Indeks Danmark consumer survey

- 20,134 respondents × 6,364 variables
- 3 CSV files: main data (~970MB), codebook, metadata
- ⚠️ Status: CSVs on Google Drive — not yet downloaded locally
- Consumer segmentation: PCA + k-means → retailer-level demand indices
- Cite: docs/data/indeksdanmark_notes.md; Customer Segmentation + Sales Prediction 2023

## 4.3 Data quality checks

- Missing value analysis per column
- Distribution checks (outliers, zero-sales weeks)
- Temporal coverage: are all 36 periods present per retailer×SKU?
- Forecasting suitability: minimum 2 years required; confirm availability

## 4.4 Feature engineering plan

- Lag features: t-1, t-2, t-4, t-8, t-52
- Rolling statistics: 4-, 8-, 13-week rolling mean/std
- Calendar: week-of-year, month, quarter, Danish public holidays
- Promotional: price discount flag, display/feature flag
- Consumer signals: Indeks Danmark-derived demand indices (SRQ3)

## Outstanding
- [ ] Confirm Nielsen access modality (SQL vs CSV export)
- [ ] Download Indeks Danmark 3 CSVs from Google Drive
- [ ] Sign confidentiality agreement with Manifold AI (CBS requirement)
"""
