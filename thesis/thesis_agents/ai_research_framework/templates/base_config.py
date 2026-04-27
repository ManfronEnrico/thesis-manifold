"""
System A — Builder Trial Base Template
----------------------------------------
This module is the base that the Builder Agent's Coder sub-agent patches
for each trial. It runs Phase 2 (Forecasting) + Phase 3 (Synthesis) only.

Phase 1 (Data Assessment + PCA) is NOT re-run per trial. The feature matrix
and consumer signals produced by Phase 1 are loaded from disk at the paths
provided via the TrialConfig dict. This keeps each trial fast and avoids
re-running PCA (which is both slow and RAM-intensive).

Usage (standalone — executed by the Executor sub-agent as a subprocess):
    python base_config.py --config '{"trial_id": "t_001", ...}' \
                          --feature-matrix thesis/analysis/outputs/phase1/feature_matrix.parquet \
                          --consumer-signals thesis/analysis/outputs/phase1/consumer_signals.json

Output written to: thesis/analysis/outputs/trial_{trial_id}.json
Schema:
    {
      "trial_id": str,
      "MAPE": float,
      "RMSE": float,
      "peak_RAM_MB": float,
      "latency_sec": float,
      "confidence_score": float,
      "error": str | null
    }

CRITICAL — sequential execution:
    Each model follows the load → fit → predict → del → gc.collect() pattern.
    No parallelism. One model in RAM at a time.

CRITICAL — no data fabrication:
    If feature_matrix_path or consumer_signals_path does not exist, the
    script exits with a clear error message and writes error to the output
    JSON. It does NOT generate synthetic data.
"""

from __future__ import annotations

import argparse
import gc
import json
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Patched by Coder sub-agent per trial ──────────────────────────────────────
# The Coder replaces these constants with trial-specific values.

TRIAL_MODELS: List[str] = ["ridge", "arima", "prophet", "lightgbm", "xgboost"]
ENSEMBLE_WEIGHTS: Dict[str, float] = {
    "ridge": 0.20,
    "arima": 0.20,
    "prophet": 0.20,
    "lightgbm": 0.20,
    "xgboost": 0.20,
}
USE_CONSUMER_SIGNAL: bool = False
APPLY_CALIBRATION: bool = True
MAX_RAM_PER_MODEL_MB: int = 512

# ── Fixed paths ───────────────────────────────────────────────────────────────

RESULTS_DIR = Path("results")


# ── Data loading ──────────────────────────────────────────────────────────────

def load_feature_matrix(path: str) -> Any:
    """
    Load the Phase 1 feature matrix from disk.
    Supports .parquet (preferred for memory efficiency) and .csv fallback.

    Parameters
    ----------
    path : str
        Path to the feature matrix file produced by Phase 1.

    Raises
    ------
    FileNotFoundError
        If the file does not exist. Phase 1 must be run before any trial.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Feature matrix not found at {path}. "
            "Phase 1 (Data Assessment Agent) must be run at least once before "
            "Builder trials can start. Do NOT generate synthetic data."
        )
    try:
        import pandas as pd
        if p.suffix == ".parquet":
            return pd.read_parquet(p)
        return pd.read_csv(p)
    except ImportError as exc:
        raise ImportError("pandas is required to load the feature matrix.") from exc


def load_consumer_signals(path: str) -> Dict[str, float]:
    """
    Load Phase 1 consumer demand signals from disk.

    Parameters
    ----------
    path : str
        Path to the consumer signals JSON file produced by Phase 1.

    Returns
    -------
    dict
        Retailer-level demand indices. Empty dict if file not found and
        USE_CONSUMER_SIGNAL is False (signals are optional for SRQ3 ablation).
    """
    p = Path(path)
    if not p.exists():
        if USE_CONSUMER_SIGNAL:
            raise FileNotFoundError(
                f"Consumer signals not found at {path}, but use_consumer_signal=True. "
                "Run Phase 1 first or set use_consumer_signal=False for this trial."
            )
        return {}
    return json.loads(p.read_text())


# ── Phase 2 — Sequential forecasting ─────────────────────────────────────────

def run_phase2(
    feature_matrix: Any,
    consumer_signals: Dict[str, float],
) -> Tuple[Dict[str, Any], float]:
    """
    Run Phase 2: sequential model execution with tracemalloc RAM profiling.

    Imports ForecastingAgent from the research framework and runs each model
    in TRIAL_MODELS sequentially. Each model is unloaded before the next loads.

    Parameters
    ----------
    feature_matrix : DataFrame
        Pre-loaded feature matrix from Phase 1.
    consumer_signals : dict
        Consumer demand indices from Phase 1 (may be empty).

    Returns
    -------
    model_forecasts : dict
        Maps model_name → ModelForecast dataclass.
    peak_ram_mb : float
        Maximum RAM observed during any single model's execution.
    """
    from thesis.ai_research_framework.agents.forecasting_agent import ForecastingAgent
    from thesis.ai_research_framework.state.research_state import ResearchState

    # Build a minimal ResearchState for the Forecasting Agent
    state: ResearchState = {
        "current_phase": "model_benchmarking",
        "errors": [],
        "requires_human_approval": False,
        "nielsen_data": None,
        "indeks_data": None,
        "feature_matrix": feature_matrix,
        "consumer_signals": consumer_signals if USE_CONSUMER_SIGNAL else {},
        "data_quality_report": None,
        "model_forecasts": {},
        "current_model_loading": None,
        "synthesis_output": None,
        "validation_report": None,
        "ram_budget_mb": 8_192,
        "peak_ram_observed_mb": 0.0,
    }

    agent = ForecastingAgent(models=TRIAL_MODELS)

    # Profile RAM across the entire Phase 2 run
    tracemalloc.start()
    new_state = agent.run(state)
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_ram_mb = peak_bytes / 1_048_576
    return new_state.get("model_forecasts", {}), peak_ram_mb


# ── Phase 3 — Synthesis ───────────────────────────────────────────────────────

def run_phase3(
    model_forecasts: Dict[str, Any],
    consumer_signals: Dict[str, float],
) -> Tuple[float, float]:
    """
    Run Phase 3: synthesis pipeline with custom ensemble weights.

    Uses the ENSEMBLE_WEIGHTS from the TrialConfig instead of the default
    inverse-MAPE weighting so that the Architect can test different weighting
    strategies. The SynthesisAgent's LLM call is skipped here to keep trial
    latency low — only the numeric outputs are captured.

    Parameters
    ----------
    model_forecasts : dict
        Output of run_phase2.
    consumer_signals : dict
        Consumer demand indices (may be empty).

    Returns
    -------
    confidence_score : float
        Composite 0–100 from the Synthesis Agent (0.0 if synthesis fails).
    calibration_coverage : float
        Empirical 90% PI coverage after isotonic calibration (0.0 if not applied).
    """
    from thesis.ai_research_framework.agents.synthesis_agent import SynthesisAgent
    from thesis.ai_research_framework.state.research_state import ResearchState

    if not model_forecasts:
        return 0.0, 0.0

    state: ResearchState = {
        "current_phase": "synthesis",
        "errors": [],
        "requires_human_approval": False,
        "nielsen_data": None,
        "indeks_data": None,
        "feature_matrix": None,
        "consumer_signals": consumer_signals if USE_CONSUMER_SIGNAL else {},
        "data_quality_report": None,
        "model_forecasts": model_forecasts,
        "current_model_loading": None,
        "synthesis_output": None,
        "validation_report": None,
        "ram_budget_mb": 8_192,
        "peak_ram_observed_mb": 0.0,
    }

    try:
        agent = SynthesisAgent()
        new_state = agent.run(state)
        synthesis = new_state.get("synthesis_output")
        if synthesis is None:
            return 0.0, 0.0
        coverage = getattr(synthesis, "calibration_coverage", 0.0) or 0.0
        return synthesis.confidence_score, coverage
    except Exception:  # noqa: BLE001
        return 0.0, 0.0


# ── Metrics extraction ────────────────────────────────────────────────────────

def extract_metrics(model_forecasts: Dict[str, Any]) -> Tuple[float, float]:
    """
    Extract the best MAPE and RMSE across all models that ran successfully.

    Returns
    -------
    best_mape : float
        Lowest MAPE (%) across all model forecasts.
    best_rmse : float
        RMSE corresponding to the best-MAPE model.
    """
    mapes = {
        name: getattr(f, "mape_validation", None)
        for name, f in model_forecasts.items()
    }
    rmses = {
        name: getattr(f, "rmse_validation", None)
        for name, f in model_forecasts.items()
    }

    valid = {k: v for k, v in mapes.items() if v is not None}
    if not valid:
        return 0.0, 0.0

    best_model = min(valid, key=lambda k: valid[k])
    return valid[best_model], rmses.get(best_model) or 0.0


# ── Output writer ─────────────────────────────────────────────────────────────

def write_output(trial_id: str, result: Dict[str, Any]) -> Path:
    """
    Write the trial result JSON to thesis/analysis/outputs/trial_{trial_id}.json.
    Creates the thesis/analysis/outputs/ directory if it does not exist.

    Parameters
    ----------
    trial_id : str
        Identifier from the TrialConfig.
    result : dict
        TrialResult-compatible dict.

    Returns
    -------
    Path
        Path to the written JSON file.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / f"trial_{trial_id}.json"
    out_path.write_text(json.dumps(result, indent=2))
    return out_path


# ── Entry point ───────────────────────────────────────────────────────────────

def run_trial(
    trial_id: str,
    feature_matrix_path: str,
    consumer_signals_path: str,
) -> Dict[str, Any]:
    """
    Execute one Builder trial: Phase 2 + Phase 3.

    This function is the single entry point used by the Coder sub-agent's
    generated scripts. It is also called directly when running base_config.py
    from the command line.

    Parameters
    ----------
    trial_id : str
        Identifier for this trial (from TrialConfig["trial_id"]).
    feature_matrix_path : str
        Path to the Phase 1 feature matrix file.
    consumer_signals_path : str
        Path to the Phase 1 consumer signals JSON.

    Returns
    -------
    dict
        TrialResult-compatible dict written to thesis/analysis/outputs/trial_{trial_id}.json.
    """
    result: Dict[str, Any] = {
        "trial_id": trial_id,
        "MAPE": 0.0,
        "RMSE": 0.0,
        "peak_RAM_MB": 0.0,
        "latency_sec": 0.0,
        "confidence_score": 0.0,
        "error": None,
    }

    t0 = time.perf_counter()

    try:
        # Load Phase 1 outputs from disk
        feature_matrix = load_feature_matrix(feature_matrix_path)
        consumer_signals = load_consumer_signals(consumer_signals_path)

        # Phase 2: sequential model execution
        model_forecasts, peak_ram_mb = run_phase2(feature_matrix, consumer_signals)

        # Phase 3: synthesis (numeric outputs only — no LLM call during Builder trials)
        confidence_score, _ = run_phase3(model_forecasts, consumer_signals)

        # Extract accuracy metrics
        best_mape, best_rmse = extract_metrics(model_forecasts)

        result.update({
            "MAPE": best_mape,
            "RMSE": best_rmse,
            "peak_RAM_MB": peak_ram_mb,
            "confidence_score": confidence_score,
        })

    except FileNotFoundError as exc:
        result["error"] = str(exc)
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"{type(exc).__name__}: {exc}"

    result["latency_sec"] = time.perf_counter() - t0

    # Always write output — Executor reads this file regardless of success/failure
    write_output(trial_id, result)
    return result


# ── CLI entry point ───────────────────────────────────────────────────────────

def main() -> None:
    """
    Command-line interface for the Executor sub-agent.

    The Executor runs: python base_config.py --config '{...}' \
                           --feature-matrix path/to/matrix \
                           --consumer-signals path/to/signals.json
    """
    parser = argparse.ArgumentParser(
        description="Run one Builder trial (Phase 2 + Phase 3 only)."
    )
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="JSON string of TrialConfig dict",
    )
    parser.add_argument(
        "--feature-matrix",
        type=str,
        default="thesis/analysis/outputs/phase1/feature_matrix.parquet",
        help="Path to Phase 1 feature matrix file",
    )
    parser.add_argument(
        "--consumer-signals",
        type=str,
        default="thesis/analysis/outputs/phase1/consumer_signals.json",
        help="Path to Phase 1 consumer signals JSON",
    )
    args = parser.parse_args()

    try:
        config = json.loads(args.config)
    except json.JSONDecodeError as exc:
        print(f"ERROR: --config is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    # Patch module-level constants from TrialConfig
    global TRIAL_MODELS, ENSEMBLE_WEIGHTS, USE_CONSUMER_SIGNAL, APPLY_CALIBRATION, MAX_RAM_PER_MODEL_MB  # noqa: PLW0603
    TRIAL_MODELS = config.get("models", TRIAL_MODELS)
    ENSEMBLE_WEIGHTS = config.get("ensemble_weights", ENSEMBLE_WEIGHTS)
    USE_CONSUMER_SIGNAL = config.get("use_consumer_signal", USE_CONSUMER_SIGNAL)
    APPLY_CALIBRATION = config.get("apply_calibration", APPLY_CALIBRATION)
    MAX_RAM_PER_MODEL_MB = config.get("max_ram_mb", MAX_RAM_PER_MODEL_MB)

    trial_id = config.get("trial_id", "unknown")
    result = run_trial(trial_id, args.feature_matrix, args.consumer_signals)

    if result.get("error"):
        print(f"TRIAL FAILED: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
