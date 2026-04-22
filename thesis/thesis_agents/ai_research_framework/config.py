"""
Research Framework Configuration
---------------------------------
All architectural constraints defined here are the subject of the thesis evaluation.
The 8GB RAM budget is a hard constraint, not a preference.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()


# ── Hard constraint (SRQ1 evaluation dimension) ──────────────────────────────

RAM_BUDGET_MB: int = 8_192  # 8 GB total pipeline budget

# Per-component RAM targets (validated against docs/architecture.md)
RAM_TARGETS_MB = {
    "coordinator": 200,
    "data_assessment_agent": 1_024,   # Indeks Danmark main CSV ~970MB
    "forecasting_agent": 512,          # one model loaded at a time (sequential)
    "synthesis_agent": 200,
    "validation_agent": 200,
    "system_overhead": 512,
    # Total: ~2.6GB headroom; peak model load may reach ~4GB with feature matrix
}

# ── Sequential execution protocol ────────────────────────────────────────────
# Each model is loaded, run, then explicitly unloaded before the next is loaded.
# This keeps peak RAM under RAM_BUDGET_MB even with multiple large models.

FORECASTING_MODELS: List[str] = [
    "arima",
    "prophet",
    "lightgbm",
    "xgboost",
    "ridge",
]

# ── LLM configuration ─────────────────────────────────────────────────────────
# Using Claude API (no local model) to avoid RAM overhead.

LLM_MODEL: str = "claude-sonnet-4-6"
LLM_TEMPERATURE: float = 0.0       # Deterministic for reproducibility
LLM_MAX_TOKENS: int = 512          # Synthesis recommendations are short


# ── Evaluation targets (SRQ1) ─────────────────────────────────────────────────

MAPE_TARGET_PERCENT: float = 15.0
CALIBRATION_COVERAGE_TARGET: float = 0.85   # 90% PI should cover ≥85% of actuals


# ── Data configuration ────────────────────────────────────────────────────────

@dataclass
class NielsenConnectionConfig:
    """Azure AD service principal credentials — loaded from .env, never hardcoded."""
    server: str = field(default_factory=lambda: os.environ.get("RU_SERVER_STRING", ""))
    database: str = field(default_factory=lambda: os.environ.get("RU_DATABASE", ""))
    client_id: str = field(default_factory=lambda: os.environ.get("RU_CLIENT_ID", ""))
    tenant_id: str = field(default_factory=lambda: os.environ.get("RU_TENANT_ID", ""))
    client_secret: str = field(default_factory=lambda: os.environ.get("RU_CLIENT_SECRET", ""))


@dataclass
class NielsenConfig:
    """Nielsen dataset configuration with local CSV fallback paths."""
    csv_dir: Path = field(default_factory=lambda: Path("thesis/data/nielsen/.csv"))
    schema_tables: List[str] = field(default_factory=lambda: [
        "csd_clean_dim_market_v",
        "csd_clean_dim_period_v",
        "csd_clean_dim_product_v",
        "csd_clean_facts_v",
    ])
    target_metrics: List[str] = field(default_factory=lambda: [
        "sales_value",
        "sales_in_liters",
        "sales_units",
    ])
    history_periods: int = 36   # ~3 years monthly
    access_confirmed: bool = True  # credentials received via one-time secret

    def __post_init__(self) -> None:
        """Verify that CSV directory exists."""
        if not self.csv_dir.exists():
            raise FileNotFoundError(
                f"Nielsen data directory not found: {self.csv_dir.resolve()}\n"
                f"Expected CSV files in: thesis/data/nielsen/.csv/"
            )


@dataclass
class IndeksDanmarkConfig:
    """Indeks Danmark dataset configuration."""
    csv_dir: Path = field(default_factory=lambda: Path("thesis/data/spss_indeksdanmark/.csv"))
    n_respondents: int = 20_134
    n_variables: int = 6_364
    n_files: int = 3               # data CSV, codebook CSV, metadata CSV
    estimated_ram_mb: int = 970    # main data CSV only

    def __post_init__(self) -> None:
        """Verify that CSV directory exists."""
        if not self.csv_dir.exists():
            raise FileNotFoundError(
                f"Indeks Danmark data directory not found: {self.csv_dir.resolve()}\n"
                f"Expected CSV files in: thesis/data/spss_indeksdanmark/.csv/"
            )
