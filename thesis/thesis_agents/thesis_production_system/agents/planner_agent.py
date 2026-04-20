"""
Planner Agent — Thesis Production System (System B)
----------------------------------------------------
Reads the current ThesisState and project context, then produces a structured
JSON task plan indicating which agents should run and in what order.

The Planner Agent does NOT execute tasks — it only generates the plan.
The Coordinator reads the plan and dispatches agents accordingly.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel

from ..state.thesis_state import ThesisState


# ── Output schema ─────────────────────────────────────────────────────────────

class Task(BaseModel):
    """A single unit of work for a thesis production agent."""
    agent: Literal[
        "LiteratureAgent",
        "WritingAgent",
        "ComplianceAgent",
        "DiagramAgent",
        "CriticAgent",
    ]
    action: str           # e.g., "update_gap_analysis", "draft_section_bullets"
    priority: int         # Lower = higher priority (1 = run first)
    context: Dict[str, Any] = {}   # Agent-specific parameters
    rationale: str = ""   # Why this task is needed now


class TaskPlan(BaseModel):
    """Complete task plan produced by the Planner Agent."""
    tasks: List[Task]
    planning_rationale: str
    session_id: str
    blocked_tasks: List[str] = []   # Tasks that cannot run yet (e.g., waiting on data)


# ── Planner Agent ──────────────────────────────────────────────────────────────

class PlannerAgent:
    """
    Analyses ThesisState and project context files to determine the
    highest-priority tasks for the current session.

    Reads:
    - ThesisState (from docs/tasks/thesis_state.json)
    - docs/context.md (session log and blockers)
    - thesis/literature/scraping_log.md (pending paper confirmations)
    - thesis/thesis-writing/outline.md (chapter status)

    Produces: TaskPlan (JSON-serialisable)
    """

    CONTEXT_FILES = [
        "docs/context.md",
        "thesis/literature/scraping_log.md",
        "thesis/literature/gap_analysis.md",
        "thesis/thesis-writing/outline.md",
    ]

    def __init__(self, project_root: Path = Path(".")) -> None:
        self.project_root = project_root

    def run(self, state: ThesisState) -> TaskPlan:
        """
        Analyse state and context, then produce a prioritised task plan.
        Returns a TaskPlan — does NOT modify state or invoke any agent.
        """
        context = self._read_context_files()
        tasks: List[Task] = []
        blocked: List[str] = []

        # ── Rule 1: Pending paper confirmations ───────────────────────────────
        pending_papers = [
            title for title, paper in state.literature_state.papers.items()
            if not paper.confirmed
        ]
        if pending_papers:
            tasks.append(Task(
                agent="LiteratureAgent",
                action="confirm_pending_papers",
                priority=1,
                context={"pending_count": len(pending_papers)},
                rationale=f"{len(pending_papers)} Tier A/B papers pending human confirmation.",
            ))

        # ── Rule 2: Sections with no bullet points yet ────────────────────────
        not_started = [
            ch_id for ch_id, sec in state.sections.items()
            if sec.status == "not_started"
        ]
        if not_started:
            tasks.append(Task(
                agent="WritingAgent",
                action="draft_section_bullets",
                priority=2,
                context={"chapters": not_started[:3]},  # Batch max 3 at once
                rationale=f"{len(not_started)} chapters have no bullet points yet.",
            ))

        # ── Rule 3: Sections with approved bullets needing compliance check ───
        bullets_approved_unchecked = [
            ch_id for ch_id, sec in state.sections.items()
            if sec.status == "bullets_approved" and not sec.compliance_checked
        ]
        if bullets_approved_unchecked:
            tasks.append(Task(
                agent="ComplianceAgent",
                action="check_section_compliance",
                priority=3,
                context={"chapters": bullets_approved_unchecked},
                rationale="Approved sections need CBS compliance verification before prose.",
            ))

        # ── Rule 4: Missing architecture diagrams ─────────────────────────────
        required_figures = {
            "system_architecture_v1": "architecture",
            "agent_workflow_v1": "workflow",
            "data_flow_v1": "data_flow",
        }
        missing_figures = [
            fig_id for fig_id in required_figures
            if fig_id not in state.figures or not state.figures[fig_id].generated
        ]
        if missing_figures:
            tasks.append(Task(
                agent="DiagramAgent",
                action="generate_figures",
                priority=4,
                context={"figure_ids": missing_figures},
                rationale="Core thesis figures not yet generated.",
            ))

        # ── Rule 5: Literature scraping (if not run this session) ─────────────
        if state.literature_state.scraping_runs_completed == 0:
            tasks.append(Task(
                agent="LiteratureAgent",
                action="run_scraping",
                priority=5,
                context={},
                rationale="No scraping run has been completed yet.",
            ))

        # ── Sort by priority ──────────────────────────────────────────────────
        tasks.sort(key=lambda t: t.priority)

        return TaskPlan(
            tasks=tasks,
            planning_rationale=self._format_rationale(tasks, blocked, state),
            session_id=state.session_id,
            blocked_tasks=blocked,
        )

    def _read_context_files(self) -> str:
        """Read relevant context files for planning decisions."""
        parts = []
        for rel_path in self.CONTEXT_FILES:
            full_path = self.project_root / rel_path
            if full_path.exists():
                parts.append(f"# {rel_path}\n{full_path.read_text()}")
        return "\n\n".join(parts)

    def _format_rationale(
        self, tasks: List[Task], blocked: List[str], state: ThesisState
    ) -> str:
        lines = [f"Session {state.session_id} — {len(tasks)} task(s) planned."]
        for t in tasks:
            lines.append(f"  [{t.priority}] {t.agent}.{t.action} — {t.rationale}")
        if blocked:
            lines.append(f"Blocked: {', '.join(blocked)}")
        return "\n".join(lines)

    def to_json(self, plan: TaskPlan) -> str:
        """Serialise a TaskPlan to JSON string."""
        return plan.model_dump_json(indent=2)
