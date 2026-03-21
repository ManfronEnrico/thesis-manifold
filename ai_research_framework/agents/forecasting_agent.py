"""
Forecasting Agent — AI Research Framework (System A)
------------------------------------------------------
Trains and evaluates 5 lightweight ML models sequentially.
Sequential execution is the core RAM management strategy:
  load → fit → predict → calibrate → unload → gc.collect()

SRQs addressed: SRQ1 (model accuracy + RAM footprint).
RAM budget per model: ≤512 MB (one model in memory at a time).
"""

from __future__ import annotations

import gc
import tracemalloc
from typing import Dict, List

from ..config import FORECASTING_MODELS, RAM_BUDGET_MB, MAPE_TARGET_PERCENT
from ..state.research_state import ModelForecast, ResearchState


class ForecastingAgent:
    """
    Trains each model sequentially, profiles RAM, and applies post-hoc
    calibration to prediction intervals (Kuleshov et al., ICML 2018).
    """

    def __init__(self, models: List[str] = FORECASTING_MODELS) -> None:
        self.models = models

    # ── Main entry point ──────────────────────────────────────────────────────

    def run(self, state: ResearchState) -> ResearchState:
        """LangGraph node — iterates over all models sequentially."""
        feature_matrix = state.get("feature_matrix")
        if feature_matrix is None:
            return {
                "errors": state.get("errors", [])
                + ["ForecastingAgent: feature_matrix is None. Run DataAssessmentAgent first."],
            }

        forecasts: Dict[str, ModelForecast] = {}
        errors: list[str] = []
        peak_observed = state.get("peak_ram_observed_mb", 0.0)

        for model_name in self.models:
            try:
                forecast, peak_mb = self._run_single_model(model_name, feature_matrix)
                forecasts[model_name] = forecast
                peak_observed = max(peak_observed, peak_mb)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"ForecastingAgent [{model_name}]: {exc}")

        return {
            "current_phase": "synthesis" if not errors else "model_benchmarking",
            "model_forecasts": forecasts,
            "current_model_loading": None,
            "peak_ram_observed_mb": peak_observed,
            "errors": state.get("errors", []) + errors,
            "requires_human_approval": True,  # Pause after benchmarking for review
        }

    # ── Sequential model execution ────────────────────────────────────────────

    def _run_single_model(
        self, model_name: str, feature_matrix
    ) -> tuple[ModelForecast, float]:
        """
        Load → Fit → Predict → Calibrate → Unload.
        Returns the ModelForecast and peak RAM (MB).
        """
        tracemalloc.start()

        try:
            model = self._load_model(model_name)
            forecast = self._fit_and_predict(model_name, model, feature_matrix)
            forecast = self._calibrate_intervals(model_name, forecast, feature_matrix)
        finally:
            # Always unload to free RAM, even on failure
            del model  # type: ignore[possibly-undefined]
            gc.collect()

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return forecast, peak / 1_048_576

    def _load_model(self, model_name: str):
        """Instantiate the model object (does not load data)."""
        if model_name == "arima":
            from pmdarima import AutoARIMA
            return AutoARIMA(max_p=5, max_q=5, seasonal=True, information_criterion="aic")
        elif model_name == "prophet":
            from prophet import Prophet
            return Prophet(
                changepoint_prior_scale=0.05,
                seasonality_mode="multiplicative",
            )
        elif model_name == "lightgbm":
            from lightgbm import LGBMRegressor
            return LGBMRegressor(n_estimators=500, learning_rate=0.05, n_jobs=1)
        elif model_name == "xgboost":
            from xgboost import XGBRegressor
            return XGBRegressor(n_estimators=500, learning_rate=0.05, n_jobs=1)
        elif model_name == "ridge":
            from sklearn.linear_model import Ridge
            return Ridge(alpha=1.0)
        else:
            raise ValueError(f"Unknown model: {model_name}")

    def _fit_and_predict(self, model_name: str, model, feature_matrix) -> ModelForecast:
        """Fit the model and generate point forecasts + prediction intervals."""
        # Implementation depends on feature_matrix structure — populated in Phase 4
        raise NotImplementedError(
            f"Fit + predict for {model_name}: pending data access and feature engineering."
        )

    def _calibrate_intervals(
        self, model_name: str, forecast: ModelForecast, feature_matrix
    ) -> ModelForecast:
        """
        Apply post-hoc isotonic regression calibration to prediction intervals.
        Method: Kuleshov et al. (2018) ICML — 'Accurate Uncertainties for Deep Learning'.
        Calibration set: validation period actuals vs. stated intervals.
        """
        # Implementation: fit IsotonicRegression on validation coverage data
        # forecast.calibrated = True once applied
        raise NotImplementedError(
            f"Calibration for {model_name}: pending validation set availability."
        )
