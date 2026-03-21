"""
Builder Agent — Architect Sub-agent
--------------------------------------
Designs the next System A configuration to test based on the Builder goal and
all previous trial results.

Rules:
- First trial: always the full 5-model baseline (equal weights, no consumer signal)
- Subsequent trials: calls Claude API to propose the next config
- Never proposes a config whose hash already appears in the registry (deduplication)
- Never proposes a config that would exceed 7.5 GB RAM (rejects per-model RAM > 512 MB)
- On first trial: models = all 5, equal weights (0.20 each)
"""

from __future__ import annotations

import json
import os
import uuid
from typing import Any, Dict, List, Optional

import anthropic

from .experiment_registry import BuilderRegistry, BuilderState, TrialConfig

# ── Constants ─────────────────────────────────────────────────────────────────

AVAILABLE_MODELS: List[str] = ["ridge", "arima", "prophet", "lightgbm", "xgboost"]
DEFAULT_MAX_RAM_PER_MODEL_MB: int = 512

LLM_MODEL = "claude-sonnet-4-6"
LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS = 512

# Approximate peak RAM per model (MB) — used to gate obviously unsafe configs
MODEL_RAM_ESTIMATES_MB: Dict[str, int] = {
    "ridge": 15,
    "arima": 20,
    "prophet": 200,
    "lightgbm": 300,
    "xgboost": 400,
}
# Total RAM headroom for models: 7680 MB - ~900 MB (runtime + feature matrix)
AVAILABLE_RAM_FOR_MODELS_MB = 6_780


class Architect:
    """
    Designs the next TrialConfig to test.

    Usage
    -----
    >>> architect = Architect(registry=BuilderRegistry())
    >>> config = architect.propose(state)
    """

    def __init__(
        self,
        registry: Optional[BuilderRegistry] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.registry = registry or BuilderRegistry()
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ["ANTHROPIC_API_KEY"]
        )

    # ── Main entry point ──────────────────────────────────────────────────────

    def propose(self, state: BuilderState) -> TrialConfig:
        """
        Return the next TrialConfig to execute.

        On the first trial, always returns the full 5-model baseline.
        On subsequent trials, uses Claude API to propose the next config, then
        validates it (deduplication + RAM check) before returning.

        Parameters
        ----------
        state : BuilderState
            Current builder state.

        Returns
        -------
        TrialConfig
            A validated configuration not yet tried.

        Raises
        ------
        RuntimeError
            If the LLM proposes only duplicate or invalid configs after 5 attempts.
        """
        trials_run = state.get("trials_run", [])

        # First trial: full baseline
        if not trials_run:
            return self._baseline_config()

        # Subsequent trials: LLM-proposed
        existing_hashes = self._existing_hashes()
        for attempt in range(1, 6):  # Up to 5 attempts to get a valid novel config
            candidate = self._llm_propose(state)
            candidate_hash = BuilderRegistry._hash_config(candidate)
            if candidate_hash not in existing_hashes and self._ram_safe(candidate):
                return candidate
            # Tell the LLM it proposed a duplicate/unsafe config on the next attempt
            state = {**state, "evaluator_judgment": (
                f"[Attempt {attempt}: proposed config was a duplicate or exceeded RAM limit. "
                "Propose a meaningfully different configuration.]"
            )}

        raise RuntimeError(
            "Architect failed to propose a novel, RAM-safe configuration after 5 attempts. "
            "Consider increasing max_trials budget or re-specifying the goal."
        )

    # ── Config construction ───────────────────────────────────────────────────

    def _baseline_config(self) -> TrialConfig:
        """Full 5-model baseline with equal ensemble weights."""
        n = len(AVAILABLE_MODELS)
        return {
            "trial_id": self._new_trial_id(),
            "models": list(AVAILABLE_MODELS),
            "ensemble_weights": {m: round(1.0 / n, 4) for m in AVAILABLE_MODELS},
            "use_consumer_signal": False,
            "apply_calibration": True,
            "max_ram_mb": DEFAULT_MAX_RAM_PER_MODEL_MB,
        }

    def _llm_propose(self, state: BuilderState) -> TrialConfig:
        """
        Call Claude API to propose the next TrialConfig as JSON.

        The prompt includes:
        - The Builder goal
        - All tried configs and their MAPE results (compact summary)
        - Hard constraints (RAM, sequential execution, available models)
        - The JSON schema to return
        """
        summary = self._build_summary(state)

        system_prompt = (
            "You are an ML experiment architect designing configurations for a retail "
            "demand forecasting system. You propose the next configuration to test in a "
            "systematic search over model combinations and ensemble weights.\n\n"
            "Hard constraints:\n"
            f"- Available models (pick any subset): {AVAILABLE_MODELS}\n"
            "- Models run SEQUENTIALLY — no parallelism\n"
            "- ensemble_weights must sum exactly to 1.0 (rounded to 4 decimal places)\n"
            "- max_ram_mb per model must not exceed 512\n"
            "- Do not repeat configurations that have already been tried\n\n"
            "Return ONLY a valid JSON object matching this schema — no prose:\n"
            "{\n"
            '  "models": ["ridge", "arima"],\n'
            '  "ensemble_weights": {"ridge": 0.5, "arima": 0.5},\n'
            '  "use_consumer_signal": false,\n'
            '  "apply_calibration": true,\n'
            '  "max_ram_mb": 512\n'
            "}"
        )

        user_prompt = f"""\
Goal: {state.get('goal', '(no goal set)')}

Trials completed so far:
{summary}

Latest evaluator judgment: {state.get('evaluator_judgment', '(none yet)')}

Propose the next configuration to try. Return only JSON."""

        response = self.client.messages.create(
            model=LLM_MODEL,
            max_tokens=LLM_MAX_TOKENS,
            temperature=LLM_TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw = response.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Architect received invalid JSON from Claude API: {exc}\nRaw: {raw}"
            ) from exc

        return self._build_config(data)

    def _build_config(self, data: Dict[str, Any]) -> TrialConfig:
        """Validate and normalise a raw dict from the LLM into a TrialConfig."""
        models = data.get("models", AVAILABLE_MODELS)
        weights_raw: Dict[str, float] = data.get("ensemble_weights", {})

        # Normalise weights so they sum exactly to 1.0
        if not weights_raw:
            n = len(models)
            weights = {m: round(1.0 / n, 4) for m in models}
        else:
            total = sum(weights_raw.values())
            weights = (
                {m: round(w / total, 4) for m, w in weights_raw.items()}
                if total > 0
                else {m: round(1.0 / len(models), 4) for m in models}
            )

        # Ensure weights cover exactly the selected models
        weights = {m: weights.get(m, 0.0) for m in models}

        return {
            "trial_id": self._new_trial_id(),
            "models": models,
            "ensemble_weights": weights,
            "use_consumer_signal": bool(data.get("use_consumer_signal", False)),
            "apply_calibration": bool(data.get("apply_calibration", True)),
            "max_ram_mb": int(data.get("max_ram_mb", DEFAULT_MAX_RAM_PER_MODEL_MB)),
        }

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _existing_hashes(self) -> set:
        """Return the set of config hashes already in the registry."""
        return {e.get("config_hash") for e in self.registry.load()}

    @staticmethod
    def _ram_safe(config: TrialConfig) -> bool:
        """
        Rough RAM safety check based on known model memory footprints.
        Maximum single-model RAM must not exceed config["max_ram_mb"].
        """
        max_model_ram = max(
            (MODEL_RAM_ESTIMATES_MB.get(m, 512) for m in config["models"]),
            default=0,
        )
        return max_model_ram <= config.get("max_ram_mb", DEFAULT_MAX_RAM_PER_MODEL_MB)

    @staticmethod
    def _build_summary(state: BuilderState) -> str:
        """Compact MAPE summary of all trials for the LLM prompt."""
        results = state.get("results", [])
        trials = state.get("trials_run", [])
        if not results:
            return "  (no trials yet)"

        lines = []
        for config, result in zip(trials, results):
            mape = result.get("MAPE", 0.0)
            err = result.get("error")
            models_str = ",".join(config.get("models", []))
            status = f"MAPE={mape:.2f}%" if not err else f"FAIL ({err[:60]})"
            lines.append(f"  {config.get('trial_id', '?')}: [{models_str}] {status}")
        return "\n".join(lines)

    @staticmethod
    def _new_trial_id() -> str:
        """Generate a short unique trial ID."""
        return f"t_{uuid.uuid4().hex[:6]}"
