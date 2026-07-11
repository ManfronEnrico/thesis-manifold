"""
Research Framework — Shared LangGraph State
--------------------------------------------
TypedDict used for LangGraph StateGraph compatibility.
All agents read from and write to this state object.
The Coordinator is the sole node that transitions between phases.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict
from dataclasses import dataclass, field


# ── Sub-state dataclasses ─────────────────────────────────────────────────────

@dataclass
class ModelForecast:
    """Output produced by the Forecasting Agent for a single model."""
    model_name: str
    point_forecast: float
    lower_90: float
    upper_90: float
    mape_validation: float          # MAPE on held-out validation set
    rmse_validation: float
    peak_ram_mb: float              # Peak RAM during model.fit() + predict()
    training_latency_s: float
    inference_latency_s: float
    calibrated: bool = False        # True after Kuleshov isotonic calibration


@dataclass
class SynthesisOutput:
    """Output produced by the Synthesis Agent."""
    point_forecast_ensemble: float
    lower_90_calibrated: float
    upper_90_calibrated: float
    confidence_score: float         # 0–100 composite score
    confidence_tier: Literal["High", "Moderate", "Low"]
    inter_model_spread: float       # Relative disagreement across models
    consumer_signal_direction: str  # "aligned" | "divergent" | "neutral"
    recommendation_text: str        # Natural language output from LLM
    llm_tokens_used: int


@dataclass
class ValidationReport:
    """Output produced by the Validation Agent."""
    # Level 1 — ML accuracy
    mape_per_model: Dict[str, float] = field(default_factory=dict)
    best_model: str = ""
    mape_with_consumer_signals: float = 0.0
    mape_without_consumer_signals: float = 0.0
    # Level 2 — Recommendation quality
    llm_judge_scores: Dict[str, float] = field(default_factory=dict)   # dimension → score
    calibration_coverage: float = 0.0
    # Level 3 — Agent behaviour
    peak_ram_total_mb: float = 0.0
    pipeline_latency_s: float = 0.0
    within_ram_budget: bool = False


# ── Main LangGraph state ───────────────────────────────────────────────────────

class ResearchState(TypedDict):
    """
    Shared state for the AI Research Framework LangGraph StateGraph.
    Coordinator reads and writes this state at each node transition.
    """

    # ── Control flow ──────────────────────────────────────────────────────────
    current_phase: Literal[
        "data_assessment",
        "feature_engineering",
        "model_benchmarking",
        "synthesis",
        "validation",
        "complete",
    ]
    errors: List[str]
    requires_human_approval: bool   # Halts the graph until user confirms

    # ── Data inputs ───────────────────────────────────────────────────────────
    # DataFrames are NOT stored in state (LangGraph msgpack serializer cannot
    # handle pd.DataFrame). Agents persist parquet to disk and share paths.
    nielsen_data: Optional[Any]         # Reserved — kept None; read from CSV dir per config
    indeks_data: Optional[Any]          # Reserved — kept None; read from CSV dir per config
    feature_matrix: Optional[Any]       # Reserved — kept None; load via feature_matrix_path
    feature_matrix_path: Optional[str]  # Filesystem path to results/phase1/feature_matrix.parquet
    series_index_path: Optional[str]    # Filesystem path to results/phase1/series_index.csv
    consumer_signals: Optional[Dict[str, float]]  # Retailer-level demand indices

    # ── Data quality report ───────────────────────────────────────────────────
    data_quality_report: Optional[str]  # Markdown string output by Data Assessment Agent

    # ── Forecasting outputs ───────────────────────────────────────────────────
    model_forecasts: Dict[str, ModelForecast]   # model_name → forecast
    current_model_loading: Optional[str]         # Tracks which model is in RAM

    # ── Synthesis output ──────────────────────────────────────────────────────
    synthesis_output: Optional[SynthesisOutput]

    # ── Validation output ─────────────────────────────────────────────────────
    validation_report: Optional[ValidationReport]

    # ── RAM tracking ──────────────────────────────────────────────────────────
    ram_budget_mb: int               # Always 8192 — set from config
    peak_ram_observed_mb: float      # Running maximum across all phases
