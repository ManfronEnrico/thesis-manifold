"""
Data Assessment Agent — AI Research Framework (System A)
---------------------------------------------------------
Analyses Nielsen CSD and Indeks Danmark datasets.
Produces a structured data quality report and engineered feature matrix.

SRQs addressed: precondition for all SRQs.
RAM budget: ~1,024 MB (dominated by Indeks Danmark: ~970 MB).
"""

from __future__ import annotations

import gc
import tracemalloc
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from ..config import NielsenConfig, IndeksDanmarkConfig, RAM_BUDGET_MB
from ..features.engineer_features import (
    aggregate_brand_month_from_csvs,
    FeatureEngineer,
    build_series_index,
    save_feature_matrix,
)
from ..state.research_state import ResearchState


class DataAssessmentAgent:
    """
    Loads, validates, and profiles the Nielsen and Indeks Danmark datasets.
    Outputs a quality report (Markdown string) and engineered feature matrix.
    """

    def __init__(
        self,
        nielsen_cfg: NielsenConfig,
        indeks_cfg: IndeksDanmarkConfig,
        output_path: Path = Path("docs/data"),
    ) -> None:
        self.nielsen_cfg = nielsen_cfg
        self.indeks_cfg = indeks_cfg
        self.output_path = output_path

    # ── Main entry point (LangGraph node function) ────────────────────────────

    def run(self, state: ResearchState) -> ResearchState:
        """
        LangGraph node. Called by the Coordinator when phase == 'data_assessment'.
        Returns an updated state dict (LangGraph merges partial updates).
        """
        tracemalloc.start()
        errors: list[str] = []

        feature_matrix_path: Optional[str] = None
        series_index_path: Optional[str] = None
        consumer_signals: Optional[Dict[str, float]] = None
        quality_report: Optional[str] = None

        try:
            _nielsen_df, nielsen_report = self._assess_nielsen()
            _indeks_df, indeks_report = self._assess_indeks_danmark()
            feature_matrix_path, series_index_path, consumer_signals = (
                self._engineer_features(_nielsen_df, _indeks_df)
            )
            quality_report = self._format_report(nielsen_report, indeks_report)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"DataAssessmentAgent failed: {exc}")

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = peak / 1_048_576

        return {
            "current_phase": "feature_engineering" if not errors else "data_assessment",
            # DataFrames are not propagated through state (msgpack-unfriendly);
            # downstream agents read parquet from feature_matrix_path.
            "nielsen_data": None,
            "indeks_data": None,
            "feature_matrix": None,
            "feature_matrix_path": feature_matrix_path,
            "series_index_path": series_index_path,
            "consumer_signals": consumer_signals,
            "data_quality_report": quality_report,
            "peak_ram_observed_mb": max(
                state.get("peak_ram_observed_mb", 0.0), peak_mb
            ),
            "errors": state.get("errors", []) + errors,
            "requires_human_approval": True,  # Always pause after data assessment
        }

    # ── Internal steps ────────────────────────────────────────────────────────

    def _assess_nielsen(self) -> Tuple[Any, Dict]:
        """Load Nielsen data and run quality checks."""
        import pandas as pd

        csv_files = list(self.nielsen_cfg.csv_dir.glob("csd_clean_facts_v.csv"))

        if not csv_files:
            raise FileNotFoundError(
                f"Nielsen data not found at {self.nielsen_cfg.csv_dir.resolve()}\n"
                f"Expected files: csd_clean_*.csv\n"
                f"Place Nielsen CSV exports in: thesis/data/nielsen/.csv/"
            )

        df = pd.read_csv(csv_files[0])
        report = {
            "source": "CSV export",
            "file": str(csv_files[0]),
            "rows": len(df),
            "columns": len(df.columns),
        }
        return df, report

    def _assess_indeks_danmark(self) -> Tuple[Any, Dict]:
        """Load Indeks Danmark CSVs and run quality checks."""
        import pandas as pd

        csv_files = list(self.indeks_cfg.csv_dir.glob("indeksdanmark_data.csv"))

        if not csv_files:
            raise FileNotFoundError(
                f"Indeks Danmark data not found at {self.indeks_cfg.csv_dir.resolve()}\n"
                f"Expected files: indeksdanmark_data.csv, indeksdanmark_metadata.csv, official_codebook.csv\n"
                f"Place files in: thesis/data/spss_indeksdanmark/.csv/"
            )

        df = pd.read_csv(csv_files[0])
        report = {
            "source": "SPSS Indeks Danmark export",
            "file": str(csv_files[0]),
            "rows": len(df),
            "columns": len(df.columns),
        }
        return df, report

    def _engineer_features(
        self, nielsen_df: Any, indeks_df: Any
    ) -> Tuple[str, str, Dict[str, float]]:
        """
        Build feature matrix for ML models via the shared feature module.
        Aggregates Nielsen facts to brand × month, applies the leakage-safe
        pipeline (lags, rolling stats, calendar, promo, log target, split),
        and persists the result to thesis/analysis/outputs/phase1/.

        Returns paths (not DataFrames) so downstream LangGraph nodes can
        checkpoint state via msgpack. Indeks-Danmark-derived consumer signals
        (PCA + k-means) are currently out of scope and returned as an empty
        dict; they will be integrated in a follow-up workstream once SRQ4
        methodology is locked.
        """
        brand_month = aggregate_brand_month_from_csvs(self.nielsen_cfg.csv_dir)
        fe = FeatureEngineer()
        features = fe.fit_transform(brand_month)

        output_dir = Path("results") / "phase1"
        series_idx = build_series_index(features)
        paths = save_feature_matrix(features, output_dir, series_idx)

        consumer_signals: Dict[str, float] = {}
        return (
            str(paths["feature_matrix"]),
            str(paths.get("series_index", "")),
            consumer_signals,
        )

    def _format_report(
        self, nielsen_report: Dict, indeks_report: Dict
    ) -> str:
        """Format data quality findings as a Markdown string."""
        return (
            "# Data Assessment Report\n\n"
            "## Nielsen CSD\n"
            f"- Source: `{nielsen_report.get('source', 'N/A')}`\n"
            f"- File: `{nielsen_report.get('file', 'N/A')}`\n"
            f"- Rows: {nielsen_report.get('rows', 'N/A'):,}\n"
            f"- Columns: {nielsen_report.get('columns', 'N/A')}\n\n"
            "## Indeks Danmark\n"
            f"- Source: `{indeks_report.get('source', 'N/A')}`\n"
            f"- File: `{indeks_report.get('file', 'N/A')}`\n"
            f"- Rows: {indeks_report.get('rows', 'N/A'):,}\n"
            f"- Columns: {indeks_report.get('columns', 'N/A')}\n"
        )

    # ── Cleanup ───────────────────────────────────────────────────────────────

    @staticmethod
    def unload(state: ResearchState) -> ResearchState:
        """
        Explicitly release dataset references from state to free RAM
        before loading the Forecasting Agent's models.
        Call this after feature_matrix is written to disk.
        """
        gc.collect()
        return {
            "nielsen_data": None,
            "indeks_data": None,
        }
