"""
Builder Agent — Experiment Registry
------------------------------------
Append-only registry for Builder Agent trial results.

Separate from the ExperimentTrackingAgent registry
(docs/experiments/experiment_registry.json) which tracks full forecasting
experiments. This registry tracks Builder trials where each trial tests one
System A configuration and records accuracy + RAM metrics.

Registry location: results/experiment_registry.json
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False


# ── Registry path ──────────────────────────────────────────────────────────────

RESULTS_DIR = Path("results")
REGISTRY_FILE = RESULTS_DIR / "experiment_registry.json"


# ── Data structures ───────────────────────────────────────────────────────────

class TrialConfig(TypedDict):
    """
    Configuration that the Architect sub-agent proposes for one trial.
    The trial_id is set by the Architect before execution begins.
    """
    trial_id: str
    models: List[str]           # subset of ["ridge", "arima", "prophet", "lgbm", "xgboost"]
    ensemble_weights: Dict[str, float]  # model_name → weight; must sum to 1.0
    use_consumer_signal: bool   # Include Indeks Danmark features (SRQ3 flag)
    apply_calibration: bool     # Apply Kuleshov isotonic regression post-hoc
    max_ram_mb: int             # Hard limit per model (default 512 MB)


class TrialResult(TypedDict):
    """
    Outcome produced by the Executor sub-agent after running one trial.
    All numeric fields are 0.0 when the trial fails; check `error` field first.
    """
    trial_id: str
    MAPE: float                 # Best single-model MAPE (%) on validation set
    RMSE: float                 # Best single-model RMSE
    peak_RAM_MB: float          # Maximum RAM observed across all models in the trial
    latency_sec: float          # Wall-clock seconds for Phase 2 + Phase 3
    confidence_score: float     # Composite 0–100 from Synthesis Agent (0.0 if failed)
    error: Optional[str]        # None if successful; stderr string if failed


class BuilderState(TypedDict):
    """
    Shared state threaded through the Builder LangGraph StateGraph.
    One instance per Builder session; updated by each sub-agent node.
    """
    goal: str                           # High-level goal from Thesis Coordinator
    max_trials: int                     # Stopping budget (default 30)
    trials_run: List[TrialConfig]       # All configs attempted so far
    results: List[TrialResult]          # Corresponding results (parallel list)
    best_trial_id: Optional[str]        # trial_id of current best by MAPE
    stop_reason: Optional[str]          # "budget_exhausted" | "converged" | "human_stop"
    generated_code: Optional[str]       # Last Python script produced by Coder
    evaluator_judgment: Optional[str]   # Latest Evaluator sub-agent verdict (≤3 sentences)


# ── Registry entry ────────────────────────────────────────────────────────────

class TrialEntry(TypedDict):
    """One row in the JSON registry. Written once, never updated."""
    trial_id: str
    timestamp: str                  # ISO 8601 UTC
    goal: str
    config: TrialConfig
    config_hash: str                # SHA-256 of canonical JSON(config) for deduplication
    result: TrialResult
    evaluator_judgment: str         # Free-text from Evaluator sub-agent


# ── Registry class ────────────────────────────────────────────────────────────

class BuilderRegistry:
    """
    Append-only persistence layer for Builder Agent trial results.

    Rules enforced:
    - Never overwrite or delete existing entries.
    - Duplicate configs (same hash) are recorded but flagged in evaluator_judgment.
    - File is initialised to {"trials": []} if it does not exist.

    Usage
    -----
    >>> reg = BuilderRegistry()
    >>> entry = reg.append(goal, config, result, judgment)
    >>> best = reg.get_best_trial(metric="MAPE")
    >>> df = reg.get_all_results_as_dataframe()
    """

    RAM_LIMIT_MB: float = 7_680.0   # 7.5 GB — 0.5 GB buffer below the 8 GB constraint

    def __init__(self, registry_path: Path = REGISTRY_FILE) -> None:
        self.registry_path = registry_path
        self._ensure_file()

    # ── I/O ───────────────────────────────────────────────────────────────────

    def _ensure_file(self) -> None:
        """Create the registry file and parent directory if they do not exist."""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            self.registry_path.write_text(json.dumps({"trials": []}, indent=2))

    def _load_raw(self) -> List[Dict[str, Any]]:
        data = json.loads(self.registry_path.read_text())
        return data.get("trials", [])

    def _write_raw(self, trials: List[Dict[str, Any]]) -> None:
        self.registry_path.write_text(
            json.dumps({"trials": trials}, indent=2)
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def append(
        self,
        goal: str,
        config: TrialConfig,
        result: TrialResult,
        evaluator_judgment: str,
    ) -> TrialEntry:
        """
        Persist a completed trial. Returns the TrialEntry that was written.

        Parameters
        ----------
        goal : str
            Human-readable description of what this trial was testing.
        config : TrialConfig
            The System A configuration that was executed.
        result : TrialResult
            Metrics produced by the Executor sub-agent.
        evaluator_judgment : str
            Evaluator sub-agent verdict (max 3 sentences).

        Returns
        -------
        TrialEntry
            The entry that was written to the registry.
        """
        trials = self._load_raw()
        config_hash = self._hash_config(config)

        # Flag duplicate configs
        existing_hashes = {t.get("config_hash") for t in trials}
        judgment = evaluator_judgment
        if config_hash in existing_hashes:
            judgment = (
                f"[DUPLICATE CONFIG — hash {config_hash[:8]} already in registry] "
                + evaluator_judgment
            )

        entry: TrialEntry = {
            "trial_id": config["trial_id"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "goal": goal,
            "config": config,
            "config_hash": config_hash,
            "result": result,
            "evaluator_judgment": judgment,
        }

        trials.append(entry)
        self._write_raw(trials)
        return entry

    def load(self) -> List[TrialEntry]:
        """Return all trial entries (read-only view)."""
        return self._load_raw()  # type: ignore[return-value]

    def get_by_id(self, trial_id: str) -> Optional[TrialEntry]:
        """Return a single entry by trial_id, or None if not found."""
        return next(
            (t for t in self._load_raw() if t["trial_id"] == trial_id),
            None,
        )

    def count(self) -> int:
        """Return the total number of trials recorded."""
        return len(self._load_raw())

    # ── Analysis helpers ──────────────────────────────────────────────────────

    def get_best_trial(self, metric: str = "MAPE") -> Optional[TrialEntry]:
        """
        Return the TrialEntry with the best value for `metric` among
        successful trials (where result["error"] is None or absent).

        Parameters
        ----------
        metric : str
            Metric name as it appears in TrialResult. Supported values:
            "MAPE", "RMSE", "peak_RAM_MB", "latency_sec", "confidence_score".
            For "confidence_score" higher is better; all others lower is better.

        Returns
        -------
        TrialEntry or None if no successful trials have been recorded.
        """
        _HIGHER_IS_BETTER = {"confidence_score"}

        trials = self._load_raw()
        successful = [
            t for t in trials
            if t.get("result", {}).get("error") is None
        ]
        if not successful:
            return None

        def _value(t: Dict[str, Any]) -> Optional[float]:
            return t.get("result", {}).get(metric)

        candidates = [(t, _value(t)) for t in successful if _value(t) is not None]
        if not candidates:
            return None

        if metric in _HIGHER_IS_BETTER:
            best = max(candidates, key=lambda x: x[1])
        else:
            best = min(candidates, key=lambda x: x[1])

        return best[0]  # type: ignore[return-value]

    def get_all_results_as_dataframe(self) -> Any:
        """
        Return a pandas DataFrame with one row per trial.

        Columns: trial_id, timestamp, goal, evaluator_judgment,
                 MAPE, RMSE, peak_RAM_MB, latency_sec, confidence_score,
                 error, config_hash, models (comma-separated).

        Raises
        ------
        ImportError
            If pandas is not installed in the current environment.
        """
        if not _PANDAS_AVAILABLE:
            raise ImportError(
                "pandas is required for get_all_results_as_dataframe(). "
                "Install with: pip install pandas"
            )

        import pandas as pd  # noqa: PLC0415

        trials = self._load_raw()
        if not trials:
            return pd.DataFrame()

        rows = []
        for t in trials:
            result = t.get("result", {})
            config = t.get("config", {})
            rows.append({
                "trial_id": t.get("trial_id"),
                "timestamp": t.get("timestamp"),
                "goal": t.get("goal"),
                "evaluator_judgment": t.get("evaluator_judgment"),
                "MAPE": result.get("MAPE"),
                "RMSE": result.get("RMSE"),
                "peak_RAM_MB": result.get("peak_RAM_MB"),
                "latency_sec": result.get("latency_sec"),
                "confidence_score": result.get("confidence_score"),
                "error": result.get("error"),
                "config_hash": t.get("config_hash"),
                "models": ",".join(config.get("models", [])),
                "use_consumer_signal": config.get("use_consumer_signal"),
                "apply_calibration": config.get("apply_calibration"),
            })

        return pd.DataFrame(rows)

    # ── Internal ──────────────────────────────────────────────────────────────

    @staticmethod
    def _hash_config(config: TrialConfig) -> str:
        """
        Deterministic SHA-256 hash of a TrialConfig (excluding trial_id).
        Two configs with the same settings but different trial_ids hash identically,
        enabling deduplication of re-proposed configurations.
        """
        hashable = {k: v for k, v in config.items() if k != "trial_id"}
        canonical = json.dumps(hashable, sort_keys=True, default=str)
        return hashlib.sha256(canonical.encode()).hexdigest()
