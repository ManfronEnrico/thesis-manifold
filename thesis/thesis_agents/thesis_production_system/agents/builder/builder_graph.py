"""
Builder Agent — LangGraph StateGraph
---------------------------------------
Assembles the Builder loop as a LangGraph StateGraph:

    architect → coder → executor → logger → evaluator
                                               ↓
                     (stop_reason set?) → END  |  → architect (loop)

Each node is a thin wrapper that calls the corresponding sub-agent class
and updates the BuilderState. The logger node persists the trial result to
the Experiment Registry before the Evaluator decides whether to continue.

Entry point: build_graph() returns a compiled LangGraph app.
"""

from __future__ import annotations

from typing import Optional

from langgraph.graph import END, StateGraph

from .architect import Architect
from .coder import Coder
from .evaluator import Evaluator
from .executor import Executor
from .experiment_registry import BuilderRegistry, BuilderState, TrialConfig, TrialResult


# ── Node functions ────────────────────────────────────────────────────────────

def architect_node(state: BuilderState) -> BuilderState:
    """
    Propose the next TrialConfig.
    Adds to trials_run and sets proposed_config in state.
    """
    registry = BuilderRegistry()
    agent = Architect(registry=registry)

    try:
        config: TrialConfig = agent.propose(state)
    except RuntimeError as exc:
        return {
            **state,
            "stop_reason": "human_stop",
            "evaluator_judgment": str(exc),
        }

    return {
        **state,
        "proposed_config": config,
        "trials_run": state.get("trials_run", []) + [config],
        "current_step": "coder",
    }


def coder_node(state: BuilderState) -> BuilderState:
    """
    Generate the trial script for the proposed config.
    Sets generated_code in state.
    """
    config = state.get("proposed_config")
    if config is None:
        return {
            **state,
            "stop_reason": "human_stop",
            "evaluator_judgment": "Coder node: proposed_config is None — architect did not set a config.",
        }

    agent = Coder()
    try:
        script_path = agent.generate(config)
        return {
            **state,
            "generated_code": script_path,
            "current_step": "executor",
        }
    except Exception as exc:  # noqa: BLE001
        # Record failure as an error result so the loop can continue
        error_result: TrialResult = {
            "trial_id": config["trial_id"],
            "MAPE": 0.0,
            "RMSE": 0.0,
            "peak_RAM_MB": 0.0,
            "latency_sec": 0.0,
            "confidence_score": 0.0,
            "error": f"Coder failed: {exc}",
        }
        return {
            **state,
            "generated_code": None,
            "latest_result": error_result,
            "results": state.get("results", []) + [error_result],
            "current_step": "logger",
        }


def executor_node(state: BuilderState) -> BuilderState:
    """
    Run the generated script as a subprocess and capture the TrialResult.
    """
    config = state.get("proposed_config")
    script_path = state.get("generated_code")

    if config is None or script_path is None:
        error_result: TrialResult = {
            "trial_id": "unknown",
            "MAPE": 0.0,
            "RMSE": 0.0,
            "peak_RAM_MB": 0.0,
            "latency_sec": 0.0,
            "confidence_score": 0.0,
            "error": "Executor: missing config or script_path in state.",
        }
        return {
            **state,
            "latest_result": error_result,
            "results": state.get("results", []) + [error_result],
            "current_step": "logger",
        }

    agent = Executor()
    result = agent.run(script_path=script_path, config=config)

    # Check RAM violation — flag but do not stop here (Evaluator decides)
    ram_error = agent.validate_ram(result)
    if ram_error:
        result["error"] = (result.get("error") or "") + " | " + ram_error

    return {
        **state,
        "latest_result": result,
        "results": state.get("results", []) + [result],
        "current_step": "logger",
    }


def logger_node(state: BuilderState) -> BuilderState:
    """
    Persist the latest trial result to the Experiment Registry.
    Updates best_trial_id if this trial has the best MAPE so far.
    """
    registry = BuilderRegistry()
    config = state.get("proposed_config")
    result = state.get("latest_result")
    judgment = state.get("evaluator_judgment") or ""

    if config and result:
        registry.append(
            goal=state.get("goal", ""),
            config=config,
            result=result,
            evaluator_judgment=judgment,
        )

    # Update best trial
    best_id = state.get("best_trial_id")
    best_mape = state.get("best_mape")

    current_mape = result.get("MAPE", 0.0) if result else 0.0
    if (
        result
        and result.get("error") is None
        and current_mape > 0.0
        and (best_mape is None or current_mape < best_mape)
    ):
        best_id = result["trial_id"]
        best_mape = current_mape

    return {
        **state,
        "best_trial_id": best_id,
        "best_mape": best_mape,
        "current_step": "evaluator",
    }


def evaluator_node(state: BuilderState) -> BuilderState:
    """
    Check stopping conditions and produce the Evaluator judgment.
    Sets stop_reason if the loop should halt.
    """
    agent = Evaluator()
    should_stop, stop_reason, judgment = agent.evaluate(state)

    return {
        **state,
        "stop_reason": stop_reason,
        "evaluator_judgment": judgment,
        "current_step": "done" if should_stop else "architect",
    }


# ── Routing ───────────────────────────────────────────────────────────────────

def _route_evaluator(state: BuilderState) -> str:
    """Route to END if stop_reason is set; otherwise loop back to architect."""
    return "end" if state.get("stop_reason") else "architect"


# ── Graph assembly ────────────────────────────────────────────────────────────

def build_graph():
    """
    Assemble and compile the Builder LangGraph StateGraph.

    Returns
    -------
    CompiledGraph
        A LangGraph compiled app ready to invoke with an initial BuilderState.

    Usage
    -----
    >>> app = build_graph()
    >>> initial_state: BuilderState = {
    ...     "goal": "find the best 3-model ensemble under 512MB RAM",
    ...     "max_trials": 30,
    ...     "trials_run": [],
    ...     "results": [],
    ...     "best_trial_id": None,
    ...     "stop_reason": None,
    ...     "generated_code": None,
    ...     "evaluator_judgment": None,
    ... }
    >>> final_state = app.invoke(initial_state)
    """
    builder = StateGraph(BuilderState)

    builder.add_node("architect", architect_node)
    builder.add_node("coder", coder_node)
    builder.add_node("executor", executor_node)
    builder.add_node("logger", logger_node)
    builder.add_node("evaluator", evaluator_node)

    builder.set_entry_point("architect")
    builder.add_edge("architect", "coder")
    builder.add_edge("coder", "executor")
    builder.add_edge("executor", "logger")
    builder.add_edge("logger", "evaluator")
    builder.add_conditional_edges(
        "evaluator",
        _route_evaluator,
        {"end": END, "architect": "architect"},
    )

    return builder.compile()


def run_builder(
    goal: str,
    max_trials: int = 30,
    feature_matrix_path: str = "results/phase1/feature_matrix.parquet",
    consumer_signals_path: str = "results/phase1/consumer_signals.json",
) -> BuilderState:
    """
    Convenience function to run the full Builder loop from the Thesis Coordinator.

    Parameters
    ----------
    goal : str
        High-level goal string (e.g. "find best 3-model ensemble under 512MB RAM").
    max_trials : int
        Maximum number of trials before stopping. Default 30.
    feature_matrix_path : str
        Path to the Phase 1 feature matrix file.
    consumer_signals_path : str
        Path to the Phase 1 consumer signals JSON.

    Returns
    -------
    BuilderState
        Final state after the loop completes, including best_trial_id and
        the full results list.
    """
    app = build_graph()

    initial_state: BuilderState = {
        "goal": goal,
        "max_trials": max_trials,
        "trials_run": [],
        "results": [],
        "best_trial_id": None,
        "stop_reason": None,
        "generated_code": None,
        "evaluator_judgment": None,
    }

    final_state = app.invoke(initial_state)
    return final_state
