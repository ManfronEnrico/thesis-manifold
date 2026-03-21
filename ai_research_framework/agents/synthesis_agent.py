"""
Synthesis Agent — AI Research Framework (System A)
---------------------------------------------------
Aggregates multi-model forecasts + consumer signals into a calibrated,
confidence-scored natural language recommendation via the Claude API.

This is the core SRQ2 contribution — the MCDM-style synthesis layer.
RAM overhead: <50 MB (no local LLM; all LLM calls go to Claude API).
"""

from __future__ import annotations

import os
from typing import Dict, Literal, Optional

import anthropic

from ..config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from ..state.research_state import ModelForecast, SynthesisOutput, ResearchState


# ── Confidence score weights (from docs/thesis/sections/ch7_synthesis.md) ────

WEIGHT_INTERVAL_WIDTH = 0.40        # Narrower calibrated interval → higher confidence
WEIGHT_INTER_MODEL_AGREEMENT = 0.30 # Lower spread across models → higher confidence
WEIGHT_CONSUMER_SIGNAL = 0.30       # Aligned consumer signals → higher confidence


class SynthesisAgent:
    """
    Implements the 5-step synthesis pipeline defined in Ch.7:
    1. Model consensus scoring (inverse-MAPE weighting)
    2. Calibrated interval aggregation
    3. Consumer signal adjustment
    4. Composite confidence score computation
    5. LLM natural language recommendation generation
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ["ANTHROPIC_API_KEY"]
        )

    # ── Main entry point ──────────────────────────────────────────────────────

    def run(self, state: ResearchState) -> ResearchState:
        """LangGraph node — runs the full synthesis pipeline."""
        forecasts = state.get("model_forecasts", {})
        consumer_signals = state.get("consumer_signals", {})

        if not forecasts:
            return {
                "errors": state.get("errors", [])
                + ["SynthesisAgent: no model forecasts in state."],
            }

        try:
            output = self._synthesise(forecasts, consumer_signals)
        except Exception as exc:  # noqa: BLE001
            return {
                "errors": state.get("errors", []) + [f"SynthesisAgent: {exc}"],
            }

        return {
            "current_phase": "validation",
            "synthesis_output": output,
            "requires_human_approval": False,   # Validation runs automatically after synthesis
        }

    # ── Pipeline steps ────────────────────────────────────────────────────────

    def _synthesise(
        self,
        forecasts: Dict[str, ModelForecast],
        consumer_signals: Dict[str, float],
    ) -> SynthesisOutput:
        # Step 1: Inverse-MAPE weighted ensemble forecast
        ensemble_point, ensemble_lower, ensemble_upper = self._ensemble_forecast(forecasts)

        # Step 2: Inter-model spread (relative disagreement)
        spread = self._inter_model_spread(forecasts)

        # Step 3: Consumer signal direction
        signal_direction = self._assess_consumer_signal(ensemble_point, consumer_signals)

        # Step 4: Composite confidence score
        score, tier = self._confidence_score(
            lower=ensemble_lower,
            upper=ensemble_upper,
            point=ensemble_point,
            spread=spread,
            signal_direction=signal_direction,
        )

        # Step 5: LLM recommendation
        recommendation, tokens = self._generate_recommendation(
            point=ensemble_point,
            lower=ensemble_lower,
            upper=ensemble_upper,
            score=score,
            tier=tier,
            signal_direction=signal_direction,
            consumer_signals=consumer_signals,
        )

        return SynthesisOutput(
            point_forecast_ensemble=ensemble_point,
            lower_90_calibrated=ensemble_lower,
            upper_90_calibrated=ensemble_upper,
            confidence_score=score,
            confidence_tier=tier,
            inter_model_spread=spread,
            consumer_signal_direction=signal_direction,
            recommendation_text=recommendation,
            llm_tokens_used=tokens,
        )

    def _ensemble_forecast(
        self, forecasts: Dict[str, ModelForecast]
    ) -> tuple[float, float, float]:
        """Inverse-MAPE weighted ensemble of point forecasts and intervals."""
        total_weight = sum(1.0 / f.mape_validation for f in forecasts.values() if f.mape_validation > 0)
        point = sum(
            (1.0 / f.mape_validation) / total_weight * f.point_forecast
            for f in forecasts.values() if f.mape_validation > 0
        )
        lower = sum(
            (1.0 / f.mape_validation) / total_weight * f.lower_90
            for f in forecasts.values() if f.mape_validation > 0
        )
        upper = sum(
            (1.0 / f.mape_validation) / total_weight * f.upper_90
            for f in forecasts.values() if f.mape_validation > 0
        )
        return point, lower, upper

    def _inter_model_spread(self, forecasts: Dict[str, ModelForecast]) -> float:
        """Relative std of point forecasts across models (lower = more agreement)."""
        points = [f.point_forecast for f in forecasts.values()]
        mean = sum(points) / len(points)
        variance = sum((p - mean) ** 2 for p in points) / len(points)
        return (variance ** 0.5) / mean if mean != 0 else 1.0

    def _assess_consumer_signal(
        self, ensemble_point: float, consumer_signals: Dict[str, float]
    ) -> Literal["aligned", "divergent", "neutral"]:
        """Determine whether consumer demand signals support the model forecast."""
        if not consumer_signals:
            return "neutral"
        # Placeholder: compare demand index trend direction with forecast direction
        # Actual logic depends on Indeks Danmark feature engineering output
        raise NotImplementedError("Consumer signal assessment: pending Indeks Danmark integration.")

    def _confidence_score(
        self,
        lower: float,
        upper: float,
        point: float,
        spread: float,
        signal_direction: str,
    ) -> tuple[float, Literal["High", "Moderate", "Low"]]:
        """
        Composite confidence score (0–100) using 3 weighted components.
        See docs/thesis/sections/ch7_synthesis.md for design rationale.
        """
        # Interval width score: narrower relative interval → higher score
        interval_relative = (upper - lower) / point if point != 0 else 1.0
        interval_score = max(0.0, 100.0 * (1.0 - interval_relative))

        # Agreement score: lower spread → higher score
        agreement_score = max(0.0, 100.0 * (1.0 - spread))

        # Consumer signal score
        signal_score = {"aligned": 100.0, "neutral": 50.0, "divergent": 0.0}.get(
            signal_direction, 50.0
        )

        composite = (
            WEIGHT_INTERVAL_WIDTH * interval_score
            + WEIGHT_INTER_MODEL_AGREEMENT * agreement_score
            + WEIGHT_CONSUMER_SIGNAL * signal_score
        )

        tier: Literal["High", "Moderate", "Low"] = (
            "High" if composite >= 70 else "Moderate" if composite >= 40 else "Low"
        )
        return composite, tier

    def _generate_recommendation(
        self,
        point: float,
        lower: float,
        upper: float,
        score: float,
        tier: str,
        signal_direction: str,
        consumer_signals: Dict[str, float],
    ) -> tuple[str, int]:
        """Call Claude API to generate natural language recommendation."""
        system_prompt = (
            "You are a demand forecasting analyst for FMCG retail. "
            "Given ML model forecasts, a calibrated confidence score, and consumer demand signals, "
            "produce a concise, actionable recommendation for a category manager.\n\n"
            "Rules:\n"
            "- Always state the forecast range (lower to upper bound), not just the point estimate.\n"
            "- Always state the confidence level (High/Moderate/Low) and why.\n"
            "- If models disagree, flag the uncertainty explicitly.\n"
            "- Keep recommendations to 2–3 sentences maximum.\n"
            "- Do not hallucinate data — only use provided inputs."
        )
        user_prompt = (
            f"ENSEMBLE FORECAST: {point:.0f} units "
            f"(90% interval: {lower:.0f} – {upper:.0f})\n"
            f"CONFIDENCE: {score:.0f}/100 ({tier})\n"
            f"CONSUMER SIGNAL: {signal_direction}\n\n"
            "Generate a recommendation."
        )

        response = self.client.messages.create(
            model=LLM_MODEL,
            max_tokens=LLM_MAX_TOKENS,
            temperature=LLM_TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        return text, tokens
