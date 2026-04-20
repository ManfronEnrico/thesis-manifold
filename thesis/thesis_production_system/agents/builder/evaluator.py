"""
Builder Agent — Evaluator Sub-agent
--------------------------------------
Assesses the full set of trial results accumulated so far and decides whether
the Builder loop should stop or continue.

Stopping conditions (any one triggers stop):
- CONVERGED: last 5 consecutive successful trials show < 0.5% absolute MAPE
  improvement over the current best MAPE
- BUDGET: trials_run >= max_trials
- RAM_VIOLATION: any trial exceeded 7.5 GB peak RAM (0.5 GB buffer below 8 GB)

In addition, the Evaluator calls the Claude API (claude-sonnet-4-6, temperature=0)
to produce a short judgment (max 3 sentences) summarising: what pattern is
emerging across trials, and what configuration to try next.
"""

from __future__ import annotations

import os
from typing import List, Optional, Tuple

import anthropic

from .experiment_registry import BuilderState, TrialResult

# ── Constants ─────────────────────────────────────────────────────────────────

CONVERGENCE_WINDOW = 5          # Number of consecutive trials to inspect
CONVERGENCE_THRESHOLD = 0.005   # 0.5% absolute MAPE improvement threshold
RAM_LIMIT_MB = 7_680.0          # 7.5 GB Builder hard cap

LLM_MODEL = "claude-sonnet-4-6"
LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS = 256            # 3-sentence judgment fits easily in 256 tokens


class Evaluator:
    """
    Evaluates stopping conditions and produces a human-readable judgment.

    Usage
    -----
    >>> evaluator = Evaluator()
    >>> should_stop, reason, judgment = evaluator.evaluate(state)
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ["ANTHROPIC_API_KEY"]
        )

    # ── Main entry point ──────────────────────────────────────────────────────

    def evaluate(
        self, state: BuilderState
    ) -> Tuple[bool, Optional[str], str]:
        """
        Check all stopping conditions and produce an Evaluator judgment.

        Parameters
        ----------
        state : BuilderState
            Current builder state including all trials_run and results so far.

        Returns
        -------
        should_stop : bool
            True if the Builder loop should halt.
        stop_reason : str or None
            One of "budget_exhausted", "converged", "ram_violation", or None.
        judgment : str
            Max 3-sentence LLM judgment — pattern observed + suggested next step.
        """
        results = state.get("results", [])
        trials_run = state.get("trials_run", [])
        max_trials = state.get("max_trials", 30)

        # ── Stopping condition 1: budget exhausted ────────────────────────────
        if len(trials_run) >= max_trials:
            judgment = self._get_judgment(state, stop_reason="budget_exhausted")
            return True, "budget_exhausted", judgment

        # ── Stopping condition 2: RAM violation ───────────────────────────────
        if self._ram_violation(results):
            judgment = self._get_judgment(state, stop_reason="ram_violation")
            return True, "ram_violation", judgment

        # ── Stopping condition 3: convergence ─────────────────────────────────
        if self._converged(results):
            judgment = self._get_judgment(state, stop_reason="converged")
            return True, "converged", judgment

        # ── Continue ──────────────────────────────────────────────────────────
        judgment = self._get_judgment(state, stop_reason=None)
        return False, None, judgment

    # ── Stopping condition checks ─────────────────────────────────────────────

    @staticmethod
    def _ram_violation(results: List[TrialResult]) -> bool:
        """Return True if any trial exceeded the 7.5 GB RAM limit."""
        return any(r.get("peak_RAM_MB", 0.0) > RAM_LIMIT_MB for r in results)

    @staticmethod
    def _converged(results: List[TrialResult]) -> bool:
        """
        Return True if the last CONVERGENCE_WINDOW successful trials all show
        less than CONVERGENCE_THRESHOLD absolute improvement over the running best.

        'Successful' means error is None and MAPE > 0.
        """
        successful = [
            r for r in results
            if r.get("error") is None and r.get("MAPE", 0.0) > 0.0
        ]
        if len(successful) < CONVERGENCE_WINDOW:
            return False

        # MAPE values of the last N successful trials
        recent = [r["MAPE"] for r in successful[-CONVERGENCE_WINDOW:]]
        best_so_far = min(r["MAPE"] for r in successful[:-CONVERGENCE_WINDOW + 1] or successful)

        # All recent trials show < CONVERGENCE_THRESHOLD improvement over historical best
        return all(
            abs(best_so_far - mape) < CONVERGENCE_THRESHOLD for mape in recent
        )

    # ── LLM judgment ──────────────────────────────────────────────────────────

    def _get_judgment(
        self,
        state: BuilderState,
        stop_reason: Optional[str],
    ) -> str:
        """
        Call Claude API to produce a 3-sentence evaluation judgment.

        Parameters
        ----------
        state : BuilderState
            Full builder state for context.
        stop_reason : str or None
            Why we are stopping, or None if continuing.

        Returns
        -------
        str
            Judgment text (max 3 sentences).
        """
        results = state.get("results", [])
        successful = [r for r in results if r.get("error") is None and r.get("MAPE", 0.0) > 0.0]
        failed = [r for r in results if r.get("error") is not None]

        best_mape = min((r["MAPE"] for r in successful), default=None)
        best_trial_id = state.get("best_trial_id", "none")

        # Build a compact summary of results for the prompt
        result_lines = []
        for r in results[-10:]:  # Last 10 trials to stay within token budget
            status = "OK" if r.get("error") is None else "FAIL"
            result_lines.append(
                f"  {r['trial_id']}: MAPE={r.get('MAPE', 0):.2f}% "
                f"RAM={r.get('peak_RAM_MB', 0):.0f}MB "
                f"latency={r.get('latency_sec', 0):.1f}s [{status}]"
            )
        results_summary = "\n".join(result_lines) if result_lines else "  (no trials yet)"

        stop_line = (
            f"The loop is STOPPING. Reason: {stop_reason}."
            if stop_reason
            else "The loop is CONTINUING — propose what to try next."
        )

        user_prompt = f"""\
Goal: {state.get('goal', '(no goal set)')}
Trials completed: {len(results)} total ({len(successful)} successful, {len(failed)} failed)
Best MAPE so far: {f'{best_mape:.2f}%' if best_mape is not None else 'N/A'} (trial {best_trial_id})

Recent trial results (last ≤10):
{results_summary}

{stop_line}

Produce a judgment in exactly 3 sentences:
1. What pattern is emerging from the results?
2. Which model combination or configuration setting is driving the best results?
3. What should be tried next (or what is the final recommendation if stopping)?"""

        try:
            response = self.client.messages.create(
                model=LLM_MODEL,
                max_tokens=LLM_MAX_TOKENS,
                temperature=LLM_TEMPERATURE,
                system=(
                    "You are an ML experiment analyst evaluating a systematic search "
                    "over forecasting model configurations for retail demand prediction. "
                    "Be concise, specific, and data-driven. Max 3 sentences."
                ),
                messages=[{"role": "user", "content": user_prompt}],
            )
            return response.content[0].text.strip()
        except Exception as exc:  # noqa: BLE001
            return f"[Evaluator judgment unavailable: {exc}]"
