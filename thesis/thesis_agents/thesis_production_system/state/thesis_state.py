"""
Thesis Production System — Shared State
----------------------------------------
Pydantic BaseModel for typed shared state.
Agents read/write this model. Markdown files remain the persistence layer
for documentation outputs (e.g., chapter bullet points).

State is serialised to/from docs/tasks/thesis_state.json at each step.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ── Sub-state models ───────────────────────────────────────────────────────────

class PaperRecord(BaseModel):
    title: str
    authors: str
    year: int
    venue: str
    url: str
    tier: Literal["1 — Core Essential", "2 — Recommended"]
    score: int
    srqs: List[str]
    annotation_file: Optional[str] = None     # Path relative to thesis/literature/papers/
    confirmed: bool = False                    # Human-confirmed for corpus inclusion


class LiteratureState(BaseModel):
    """State managed by the Literature Agent."""
    papers: Dict[str, PaperRecord] = Field(default_factory=dict)   # title → record
    gap_analysis_version: str = "v3"
    rq_version: str = "v2"
    open_questions: List[str] = Field(default_factory=list)
    scraping_runs_completed: int = 1
    last_scraped: Optional[str] = None   # ISO date string


class SectionState(BaseModel):
    """State managed by the Writing Agent — one entry per chapter section."""
    chapter: str                            # e.g., "ch6-model-benchmark"
    status: Literal[
        "not_started",
        "bullets_draft",
        "bullets_approved",
        "prose_draft",
        "prose_approved",
    ] = "not_started"
    bullet_file: Optional[str] = None      # Path to .md file
    compliance_checked: bool = False
    word_count_estimate: int = 0


class FigureState(BaseModel):
    """State managed by the Diagram Agent."""
    figure_id: str                          # e.g., "system_architecture_v1"
    figure_type: Literal[
        "architecture",
        "workflow",
        "model_performance",
        "evaluation_plot",
        "data_flow",
    ]
    output_path: str                        # Relative to project root
    format: Literal["svg", "png"]
    generated: bool = False
    generation_script: Optional[str] = None  # Path to the Python script that generated it


class ComplianceCheck(BaseModel):
    """Single compliance check result from the Compliance Agent."""
    section: str
    timestamp: str
    issues: List[str] = Field(default_factory=list)
    passed: bool = True


class ComplianceState(BaseModel):
    """State managed by the Compliance Agent."""
    checks: Dict[str, ComplianceCheck] = Field(default_factory=dict)  # section → check
    total_character_count: int = 0
    standard_pages_estimate: float = 0.0    # total_chars / 2275
    page_limit: int = 120
    within_page_limit: bool = True

    # Feature outputs (Phase 1 toggles)
    citation_verification_report: Dict[str, Any] = Field(default_factory=dict)  # Semantic Scholar API
    integrity_report: Dict[str, Any] = Field(default_factory=dict)  # Integrity Verification Gates


# ── Root state ─────────────────────────────────────────────────────────────────

class ThesisState(BaseModel):
    """
    Root shared state for all thesis production agents.
    Agents receive and return this object.
    Coordinator is responsible for persisting state to JSON after each step.
    """

    literature_state: LiteratureState = Field(default_factory=LiteratureState)
    thesis_outline: Dict[str, Any] = Field(default_factory=dict)
    sections: Dict[str, SectionState] = Field(default_factory=dict)  # chapter_id → state
    figures: Dict[str, FigureState] = Field(default_factory=dict)    # figure_id → state
    compliance_checks: ComplianceState = Field(default_factory=ComplianceState)

    # NotebookLM integration (Phase 0.5+)
    notebooklm_context: Dict[str, Any] = Field(
        default_factory=dict
    )  # {chapter: {summary, sources, verified, timestamp}}
    notebooklm_citations: Dict[str, Any] = Field(
        default_factory=dict
    )  # {claim_id: {passage, source_id, confidence_level}}

    # Feature toggles (Phase 1 — all default OFF, opt-in only)
    toggles: Dict[str, bool] = Field(
        default_factory=lambda: {
            "pipeline_state_machine": False,
            "anti_leakage_protocol": False,
            "semantic_scholar_verification": False,
            "writing_quality_check": False,
            "style_calibration": False,
            "integrity_verification_gates": False,
        }
    )

    # Feature-specific state fields
    material_gaps: List[str] = Field(default_factory=list)  # For anti-leakage protocol
    chapter_states: Dict[str, str] = Field(default_factory=dict)  # For pipeline state machine
    style_profile: Dict[str, Any] = Field(default_factory=dict)  # For style calibration

    # Task tracking
    last_task_plan: Optional[Dict[str, Any]] = None     # Output of the Planner Agent
    last_critic_result: Optional[Dict[str, Any]] = None  # Output of the Critic Agent
    current_agent: Optional[str] = None
    session_id: str = Field(default_factory=lambda: datetime.now().strftime("%Y%m%d-%H%M%S"))

    # Persistence
    state_file: str = "docs/tasks/thesis_state.json"

    def save(self, path: Optional[str] = None) -> None:
        """Persist state to JSON file."""
        target = Path(path or self.state_file)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.model_dump_json(indent=2))

    @classmethod
    def load(cls, path: str = "docs/tasks/thesis_state.json") -> "ThesisState":
        """Load state from JSON file, or return a fresh state if file not found."""
        p = Path(path)
        if p.exists():
            return cls.model_validate_json(p.read_text())
        return cls()
