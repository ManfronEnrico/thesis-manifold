"""
Experiment Tracking Agent — Thesis Production System (System B)
----------------------------------------------------------------
Captures metadata from every forecasting experiment and persists it to a
structured JSON registry so that thesis results are fully reproducible.

Runs automatically after the Forecasting Agent and before the Validation Agent.
Visualization and Tables agents read experiment data from the registry.

Registry location : docs/experiments/experiment_registry.json
Summary location  : docs/experiments/experiment_summary.md
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ── Registry paths ─────────────────────────────────────────────────────────────

EXPERIMENTS_DIR = Path("docs/experiments")
REGISTRY_FILE = EXPERIMENTS_DIR / "experiment_registry.json"
SUMMARY_FILE = EXPERIMENTS_DIR / "experiment_summary.md"


# ── Experiment data models ─────────────────────────────────────────────────────

class ModelMetrics(BaseModel):
    """Evaluation metrics for a single model within one experiment."""
    MAPE: Optional[float] = None             # Mean Absolute Percentage Error (%)
    RMSE: Optional[float] = None             # Root Mean Squared Error
    MAE: Optional[float] = None              # Mean Absolute Error
    directional_accuracy: Optional[float] = None  # % of weeks with correct direction
    calibration_coverage: Optional[float] = None  # Empirical 90% PI coverage


class ModelRuntime(BaseModel):
    """Compute and memory profile for a single model."""
    runtime_seconds: float
    peak_ram_mb: float
    within_ram_budget: bool = True   # peak_ram_mb ≤ 512 MB per model (research constraint)


class ModelHyperparameters(BaseModel):
    """Hyperparameters used during fitting (model-specific)."""
    params: Dict[str, Any] = Field(default_factory=dict)


class ExperimentRecord(BaseModel):
    """
    Complete metadata record for one forecasting experiment.
    Stored as a JSON object in the registry.
    """
    experiment_id: str
    timestamp: str                              # ISO 8601 UTC
    dataset_version: str                        # e.g., "nielsen_v1", "synthetic_v1"
    dataset_split: Dict[str, str] = Field(     # train/val/test date ranges
        default_factory=lambda: {
            "train_start": "TBD",
            "train_end": "TBD",
            "validation_end": "TBD",
            "test_end": "TBD",
        }
    )
    models_executed: List[str]
    hyperparameters: Dict[str, ModelHyperparameters] = Field(default_factory=dict)
    metrics: Dict[str, ModelMetrics] = Field(default_factory=dict)
    runtime: Dict[str, ModelRuntime] = Field(default_factory=dict)
    peak_ram_total_mb: float = 0.0
    within_total_ram_budget: bool = True        # peak_ram_total ≤ 8192 MB
    notes: str = ""
    consumer_signals_included: bool = False     # Whether Indeks Danmark features were used
    best_model_by_mape: Optional[str] = None    # Populated by ExperimentTrackingAgent


# ── Registry ───────────────────────────────────────────────────────────────────

class ExperimentRegistry:
    """
    Reads and writes the JSON experiment registry.
    Acts as a thin persistence layer — no business logic here.
    """

    def __init__(self, registry_path: Path = REGISTRY_FILE) -> None:
        self.registry_path = registry_path
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        if not registry_path.exists():
            registry_path.write_text(json.dumps({"experiments": []}, indent=2))

    def load(self) -> List[Dict[str, Any]]:
        data = json.loads(self.registry_path.read_text())
        return data.get("experiments", [])

    def append(self, record: ExperimentRecord) -> None:
        experiments = self.load()
        experiments.append(json.loads(record.model_dump_json()))
        self.registry_path.write_text(
            json.dumps({"experiments": experiments}, indent=2)
        )

    def get_by_id(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        return next(
            (e for e in self.load() if e["experiment_id"] == experiment_id),
            None,
        )

    def get_latest(self) -> Optional[Dict[str, Any]]:
        experiments = self.load()
        return experiments[-1] if experiments else None

    def count(self) -> int:
        return len(self.load())


# ── Experiment Tracking Agent ──────────────────────────────────────────────────

class ExperimentTrackingAgent:
    """
    Captures forecasting experiment metadata from the research framework's state
    and persists it to the experiment registry.

    Workflow position:
        Forecasting Agent → ExperimentTrackingAgent → Validation Agent
                                       ↓
                               experiment_registry.json
                                       ↓
                        Visualization Agent / Tables Agent

    The agent operates on data produced by System A (ResearchState model forecasts)
    but lives in System B as a production tracking tool. It does NOT modify any
    forecasting or synthesis logic.
    """

    def __init__(
        self,
        registry: Optional[ExperimentRegistry] = None,
        summary_path: Path = SUMMARY_FILE,
    ) -> None:
        self.registry = registry or ExperimentRegistry()
        self.summary_path = summary_path

    # ── Main entry point ───────────────────────────────────────────────────────

    def track(
        self,
        model_forecasts: Dict[str, Any],          # Dict[str, ModelForecast] from ResearchState
        dataset_version: str = "nielsen_v1",
        dataset_split: Optional[Dict[str, str]] = None,
        consumer_signals_included: bool = False,
        notes: str = "",
    ) -> ExperimentRecord:
        """
        Build an ExperimentRecord from the Forecasting Agent's output and persist it.

        Parameters
        ----------
        model_forecasts : dict
            Maps model_name → ModelForecast (from thesis.ai_research_framework.state.research_state).
        dataset_version : str
            Identifies the dataset snapshot used (e.g., "nielsen_v1", "synthetic_v1").
        dataset_split : dict, optional
            Train/val/test date boundaries.
        consumer_signals_included : bool
            Whether Indeks Danmark features were included (SRQ3 ablation flag).
        notes : str
            Free-text notes for this experiment.

        Returns
        -------
        ExperimentRecord
            The persisted record.
        """
        experiment_id = self._generate_id()
        timestamp = datetime.now(timezone.utc).isoformat()

        record = ExperimentRecord(
            experiment_id=experiment_id,
            timestamp=timestamp,
            dataset_version=dataset_version,
            dataset_split=dataset_split or {},
            models_executed=list(model_forecasts.keys()),
            consumer_signals_included=consumer_signals_included,
            notes=notes,
        )

        # Extract metrics, runtime, hyperparameters from each ModelForecast
        for model_name, forecast in model_forecasts.items():
            record.metrics[model_name] = self._extract_metrics(forecast)
            record.runtime[model_name] = self._extract_runtime(forecast)
            record.hyperparameters[model_name] = ModelHyperparameters(
                params=getattr(forecast, "hyperparameters", {})
            )

        # Aggregate RAM
        if record.runtime:
            record.peak_ram_total_mb = max(
                r.peak_ram_mb for r in record.runtime.values()
            )
            record.within_total_ram_budget = record.peak_ram_total_mb <= 8_192

        # Identify best model
        record.best_model_by_mape = self._best_model(record.metrics)

        # Persist
        self.registry.append(record)
        self._update_summary()

        return record

    # ── Extraction helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _extract_metrics(forecast: Any) -> ModelMetrics:
        """
        Extract ModelMetrics from a ModelForecast dataclass.
        Uses getattr with defaults so the tracker is robust to partial results.
        """
        return ModelMetrics(
            MAPE=getattr(forecast, "mape_validation", None),
            RMSE=getattr(forecast, "rmse_validation", None),
            MAE=getattr(forecast, "mae_validation", None),
            directional_accuracy=getattr(forecast, "directional_accuracy", None),
            calibration_coverage=getattr(forecast, "calibration_coverage", None),
        )

    @staticmethod
    def _extract_runtime(forecast: Any) -> ModelRuntime:
        peak_ram = getattr(forecast, "peak_ram_mb", 0.0)
        return ModelRuntime(
            runtime_seconds=(
                getattr(forecast, "training_latency_s", 0.0)
                + getattr(forecast, "inference_latency_s", 0.0)
            ),
            peak_ram_mb=peak_ram,
            within_ram_budget=peak_ram <= 512,  # per-model budget from architecture
        )

    @staticmethod
    def _best_model(metrics: Dict[str, ModelMetrics]) -> Optional[str]:
        """Return the model name with the lowest MAPE. Returns None if no MAPE data."""
        candidates = {
            name: m.MAPE
            for name, m in metrics.items()
            if m.MAPE is not None
        }
        if not candidates:
            return None
        return min(candidates, key=lambda k: candidates[k])

    @staticmethod
    def _generate_id() -> str:
        """Generate a short, human-readable experiment ID: exp_YYYYMMDD_HHMMSS."""
        return "exp_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── Summary generator ──────────────────────────────────────────────────────

    def _update_summary(self) -> None:
        """
        Regenerate docs/experiments/experiment_summary.md from the full registry.
        Called automatically after every new experiment is tracked.
        """
        experiments = self.registry.load()
        if not experiments:
            return

        latest = experiments[-1]
        total = len(experiments)

        # ── Best model across all experiments ─────────────────────────────────
        all_mape: Dict[str, list] = {}
        for exp in experiments:
            for model, metrics in exp.get("metrics", {}).items():
                mape = metrics.get("MAPE")
                if mape is not None:
                    all_mape.setdefault(model, []).append(mape)

        avg_mape = {
            model: sum(vals) / len(vals)
            for model, vals in all_mape.items()
        }
        overall_best = min(avg_mape, key=lambda k: avg_mape[k]) if avg_mape else "N/A"

        # ── Latest experiment metrics table ───────────────────────────────────
        metrics_rows = []
        for model, m in latest.get("metrics", {}).items():
            mape = m.get("MAPE")
            rmse = m.get("RMSE")
            ram_row = latest.get("runtime", {}).get(model, {})
            ram = ram_row.get("peak_ram_mb", "—")
            rt = ram_row.get("runtime_seconds", "—")
            mape_str = f"{mape:.1%}" if mape is not None else "—"
            rmse_str = f"{rmse:.2f}" if rmse is not None else "—"
            ram_str = f"{ram:.0f} MB" if isinstance(ram, (int, float)) else "—"
            rt_str = f"{rt:.1f}s" if isinstance(rt, (int, float)) else "—"
            metrics_rows.append(
                f"| {model} | {mape_str} | {rmse_str} | {ram_str} | {rt_str} |"
            )

        metrics_table = (
            "| Model | MAPE | RMSE | Peak RAM | Runtime |\n"
            "|---|---|---|---|---|\n"
            + "\n".join(metrics_rows)
            if metrics_rows
            else "_No metrics recorded yet._"
        )

        # ── All-time best table ────────────────────────────────────────────────
        best_rows = "\n".join(
            f"| {model} | {avg:.1%} |"
            for model, avg in sorted(avg_mape.items(), key=lambda x: x[1])
        )
        best_table = (
            "| Model | Avg MAPE (all experiments) |\n|---|---|\n" + best_rows
            if best_rows
            else "_No experiments completed yet._"
        )

        # ── RAM compliance ─────────────────────────────────────────────────────
        ram_ok = latest.get("within_total_ram_budget", True)
        ram_total = latest.get("peak_ram_total_mb", 0)
        ram_status = (
            f"✅ {ram_total:.0f} MB — within 8 GB budget"
            if ram_ok
            else f"🔴 {ram_total:.0f} MB — OVER 8 GB budget"
        )

        content = f"""\
# Experiment Summary
> Auto-generated by ExperimentTrackingAgent
> Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Registry overview

| | |
|---|---|
| Total experiments | {total} |
| Latest experiment | `{latest.get("experiment_id", "—")}` |
| Timestamp | {latest.get("timestamp", "—")[:19].replace("T", " ")} UTC |
| Dataset | {latest.get("dataset_version", "—")} |
| Consumer signals included | {"Yes" if latest.get("consumer_signals_included") else "No"} |
| RAM status (latest) | {ram_status} |

---

## Latest experiment — results

**Experiment ID**: `{latest.get("experiment_id", "—")}`
**Best model**: {latest.get("best_model_by_mape", "—")}

{metrics_table}

---

## All-time best model (by avg MAPE)

**Overall best**: {overall_best}

{best_table}

---

## Notes

{latest.get("notes", "_No notes recorded._")}

---

_Registry file_: `docs/experiments/experiment_registry.json`
_Registry entries_: {total}
"""

        self.summary_path.parent.mkdir(parents=True, exist_ok=True)
        self.summary_path.write_text(content)

    # ── Utility: load for downstream agents ───────────────────────────────────

    def get_latest_experiment(self) -> Optional[Dict[str, Any]]:
        """Return the most recent experiment record (for Visualization/Tables agents)."""
        return self.registry.get_latest()

    def get_all_experiments(self) -> List[Dict[str, Any]]:
        """Return all experiment records (for cross-experiment comparisons)."""
        return self.registry.load()

    def get_best_model_across_experiments(self) -> Optional[str]:
        """Return the model with the lowest average MAPE across all experiments."""
        all_mape: Dict[str, list] = {}
        for exp in self.registry.load():
            for model, metrics in exp.get("metrics", {}).items():
                mape = metrics.get("MAPE")
                if mape is not None:
                    all_mape.setdefault(model, []).append(mape)
        if not all_mape:
            return None
        avg = {m: sum(v) / len(v) for m, v in all_mape.items()}
        return min(avg, key=lambda k: avg[k])
