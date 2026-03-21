"""
Critic Agent — Thesis Production System (System B)
---------------------------------------------------
Validates outputs from other thesis production agents before the Coordinator
accepts them and updates ThesisState.

The Critic Agent does NOT modify state — it returns a CriticResult that the
Coordinator uses to accept the output or return the task to the agent.

Workflow:
  Execution Agent → output → CriticAgent.validate() → CriticResult
  Coordinator: if valid → update state; if invalid → retry with issues
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel


# ── Output schema ─────────────────────────────────────────────────────────────

class CriticResult(BaseModel):
    """Validation result produced by the Critic Agent."""
    status: Literal["valid", "invalid"]
    issues: List[str]                   # Empty if valid
    confidence: float                   # 0.0 – 1.0
    agent_evaluated: str                # Which agent produced the output
    action_evaluated: str               # Which action was evaluated
    suggestions: List[str] = []         # Improvement hints for retry


# ── Critic Agent ───────────────────────────────────────────────────────────────

class CriticAgent:
    """
    Validates outputs from thesis production agents using rule-based checks.
    Each agent type has a dedicated validation method.
    """

    def validate(
        self,
        agent: str,
        action: str,
        output: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> CriticResult:
        """
        Dispatch to the appropriate validation method based on agent + action.
        Returns a CriticResult — does NOT raise exceptions.
        """
        validators = {
            ("LiteratureAgent", "update_gap_analysis"):     self._validate_gap_analysis,
            ("WritingAgent", "draft_section_bullets"):       self._validate_section_bullets,
            ("ComplianceAgent", "check_section_compliance"): self._validate_compliance_check,
            ("DiagramAgent", "generate_figures"):            self._validate_figure_output,
            ("LiteratureAgent", "run_scraping"):             self._validate_scraping_output,
        }
        key = (agent, action)
        validator = validators.get(key, self._validate_generic)
        return validator(output, context or {})

    # ── Per-agent validators ───────────────────────────────────────────────────

    def _validate_gap_analysis(
        self, output: Any, context: Dict[str, Any]
    ) -> CriticResult:
        issues = []
        required_sections = [
            "## Literature Corpus Summary",
            "## Preliminary Gap Identification",
            "## Proposed Novelty",
        ]
        content = str(output)
        for section in required_sections:
            if section not in content:
                issues.append(f"Missing section: '{section}'")

        if "SRQ" not in content:
            issues.append("Gap analysis does not reference any SRQ.")

        return CriticResult(
            status="valid" if not issues else "invalid",
            issues=issues,
            confidence=1.0 - (len(issues) * 0.15),
            agent_evaluated="LiteratureAgent",
            action_evaluated="update_gap_analysis",
            suggestions=[f"Add '{s}' header." for s in required_sections if s not in content],
        )

    def _validate_section_bullets(
        self, output: Any, context: Dict[str, Any]
    ) -> CriticResult:
        issues = []
        content = str(output)
        chapter = context.get("chapter", "unknown")

        # Must be bullet points (not prose)
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        prose_lines = [l for l in lines if not l.startswith(("-", "*", "#", "|")) and len(l) > 120]
        if prose_lines:
            issues.append(
                f"Output contains {len(prose_lines)} line(s) that appear to be prose "
                "(>120 chars, not a bullet). Thesis Writing Agent must produce bullets only."
            )

        # Must have at least one cite
        if "Cite:" not in content and "cite:" not in content:
            issues.append("No citation placeholder found. Every bullet section needs at least one 'Cite:' marker.")

        # Must reference at least one SRQ
        if "SRQ" not in content and chapter not in ("ch1_introduction", "ch3_methodology", "ch9_discussion", "ch10_conclusion"):
            issues.append(f"Section {chapter} does not reference any SRQ.")

        confidence = max(0.0, 1.0 - len(issues) * 0.2)
        return CriticResult(
            status="valid" if not issues else "invalid",
            issues=issues,
            confidence=confidence,
            agent_evaluated="WritingAgent",
            action_evaluated="draft_section_bullets",
            suggestions=["Convert prose to bullet format.", "Add 'Cite: [Author Year]' placeholders."]
            if issues else [],
        )

    def _validate_compliance_check(
        self, output: Any, context: Dict[str, Any]
    ) -> CriticResult:
        issues = []
        content = str(output)

        required_fields = ["Citation format", "Structure", "Word count"]
        for field in required_fields:
            if field not in content:
                issues.append(f"Compliance check missing field: '{field}'")

        return CriticResult(
            status="valid" if not issues else "invalid",
            issues=issues,
            confidence=1.0 - len(issues) * 0.2,
            agent_evaluated="ComplianceAgent",
            action_evaluated="check_section_compliance",
        )

    def _validate_figure_output(
        self, output: Any, context: Dict[str, Any]
    ) -> CriticResult:
        issues = []
        from pathlib import Path

        figure_ids = context.get("figure_ids", [])
        for fig_id in figure_ids:
            for fmt in ("svg", "png"):
                expected = Path(f"docs/thesis/figures/{fig_id}.{fmt}")
                if not expected.exists():
                    issues.append(f"Figure file missing: {expected}")

        return CriticResult(
            status="valid" if not issues else "invalid",
            issues=issues,
            confidence=1.0 if not issues else 0.0,
            agent_evaluated="DiagramAgent",
            action_evaluated="generate_figures",
            suggestions=["Re-run DiagramAgent.generate_figures() for missing figures."] if issues else [],
        )

    def _validate_scraping_output(
        self, output: Any, context: Dict[str, Any]
    ) -> CriticResult:
        issues = []
        content = str(output)

        if "TIER A" not in content and "TIER B" not in content:
            issues.append("Scraping output does not contain TIER A or TIER B paper tables.")
        if "score" not in content.lower():
            issues.append("Scraping output does not include relevance scores.")

        return CriticResult(
            status="valid" if not issues else "invalid",
            issues=issues,
            confidence=1.0 - len(issues) * 0.3,
            agent_evaluated="LiteratureAgent",
            action_evaluated="run_scraping",
        )

    def _validate_generic(
        self, output: Any, context: Dict[str, Any]
    ) -> CriticResult:
        """Fallback validator: check that output is non-empty."""
        is_empty = output is None or str(output).strip() == ""
        return CriticResult(
            status="invalid" if is_empty else "valid",
            issues=["Output is empty."] if is_empty else [],
            confidence=0.5 if not is_empty else 0.0,
            agent_evaluated=context.get("agent", "unknown"),
            action_evaluated=context.get("action", "unknown"),
        )
