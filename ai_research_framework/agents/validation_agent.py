"""
Validation Agent — AI Research Framework (System A)
----------------------------------------------------
3-level evaluation framework (the thesis's core methodological contribution
to AI artefact evaluation design).

Level 1 — ML accuracy (MAPE, RMSE, MAE, calibration coverage)
Level 2 — Recommendation quality (LLM-as-Judge, calibration coverage)
Level 3 — Agent behaviour (RAM profiling, latency)

SRQs addressed: SRQ1, SRQ2, SRQ3, SRQ4.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import anthropic

from ..config import LLM_MODEL, LLM_TEMPERATURE
from ..state.research_state import ModelForecast, SynthesisOutput, ValidationReport, ResearchState


class ValidationAgent:
    """Runs all 3 validation levels and writes the report to state."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.llm_client = anthropic.Anthropic(api_key=api_key) if api_key else None

    # ── Main entry point ──────────────────────────────────────────────────────

    def run(self, state: ResearchState) -> ResearchState:
        """LangGraph node — runs all 3 validation levels."""
        forecasts = state.get("model_forecasts", {})
        synthesis = state.get("synthesis_output")
        peak_ram = state.get("peak_ram_observed_mb", 0.0)

        report = ValidationReport()

        try:
            report = self._level1_ml_accuracy(report, forecasts)
            report = self._level2_recommendation_quality(report, synthesis)
            report = self._level3_agent_behaviour(report, state)
        except Exception as exc:  # noqa: BLE001
            return {
                "errors": state.get("errors", []) + [f"ValidationAgent: {exc}"],
            }

        return {
            "current_phase": "complete",
            "validation_report": report,
            "requires_human_approval": True,  # Present full report for thesis approval
        }

    # ── Level 1: ML accuracy ──────────────────────────────────────────────────

    def _level1_ml_accuracy(
        self, report: ValidationReport, forecasts: Dict[str, ModelForecast]
    ) -> ValidationReport:
        """
        Computes MAPE, RMSE, MAE per model.
        Runs Diebold-Mariano test for pairwise statistical significance.
        Performs SRQ3 ablation: MAPE with vs. without Indeks Danmark features.
        """
        raise NotImplementedError("Level 1 validation: pending test set actuals.")

    # ── Level 2: Recommendation quality (LLM-as-Judge) ───────────────────────

    def _level2_recommendation_quality(
        self, report: ValidationReport, synthesis: Optional[SynthesisOutput]
    ) -> ValidationReport:
        """
        Uses GPT-4o as an independent judge (not claude-sonnet-4-6 — avoids self-evaluation bias).
        Evaluates N=50 sampled recommendations on 5 Likert-scale dimensions.
        Also checks calibration coverage (empirical vs. stated 90% PI).
        """
        raise NotImplementedError("Level 2 validation: pending synthesis outputs.")

    # ── Level 3: Agent behaviour ──────────────────────────────────────────────

    def _level3_agent_behaviour(
        self, report: ValidationReport, state: ResearchState
    ) -> ValidationReport:
        """
        Reports peak RAM and latency from tracemalloc measurements collected
        across the pipeline. Checks whether peak_ram ≤ RAM_BUDGET_MB.
        """
        from ..config import RAM_BUDGET_MB

        peak_ram = state.get("peak_ram_observed_mb", 0.0)
        report.peak_ram_total_mb = peak_ram
        report.within_ram_budget = peak_ram <= RAM_BUDGET_MB
        return report

    # ── Utility: MAPE ─────────────────────────────────────────────────────────

    @staticmethod
    def mape(actuals: Any, predictions: Any) -> float:
        """Mean Absolute Percentage Error. Requires actuals > 0."""
        import numpy as np
        actuals_arr = np.asarray(actuals, dtype=float)
        preds_arr = np.asarray(predictions, dtype=float)
        return float(np.mean(np.abs((actuals_arr - preds_arr) / actuals_arr)) * 100)
