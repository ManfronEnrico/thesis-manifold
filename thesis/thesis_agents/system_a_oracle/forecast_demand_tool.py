"""
System A — `forecast_demand` tool (the thesis's dedicated-model alternative to
Prometheus's code-as-action).

This is the ONE novel component. Where Prometheus would have its coder write and
run forecasting code in the E2B sandbox, System A's agent calls this tool, which
returns a pre-trained XGBoost forecast (point + split-conformal 90% interval +
confidence tier) from the committed forecast service (scripts/forecast_service.py
→ thesis/data/_07_forecast_service/forecasts.csv).

To deploy into the Graph Engine: drop this project under
`graph-engine/data_agents/projects/oracle/` and register the tool name in the
project's ProjectDeps.tool_names. The decorator below mirrors the engine's tool
API (`@data_agent.tool` / system_prompt injection); imports resolve only inside
the engine, so this file is engine-coupled by design.
"""
from __future__ import annotations

from pathlib import Path

# Inside the engine these resolve; here they document the integration surface.
try:
    from pydantic_ai import RunContext
    from data_agents.agents.base_agents import data_agent
    from data_agents.types.agent_deps_types import CodeExecutorDeps
    from data_agents.types.base_agents_types import ProjectDeps
    _ENGINE = True
except Exception:  # running outside the engine (e.g. unit test)
    _ENGINE = False

# The dedicated-model layer (thesis-owned, runs anywhere).
import importlib.util

_svc_path = Path(__file__).resolve().parents[3] / "scripts" / "forecast_service.py"
_spec = importlib.util.spec_from_file_location("forecast_service", _svc_path)
forecast_service = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(forecast_service)


def _format(result: dict) -> str:
    """Render the structured forecast as a short, agent-friendly text block."""
    if result.get("status") != "ok":
        return result.get("message", "No forecast available for that entity.")
    lo, hi = result["interval_90"]
    chain = f" · chain {result['chain']}" if result.get("chain") else ""
    return (
        f"Forecast ({result['horizon']}) for {result['brand']} in {result['category']}{chain}: "
        f"{result['forecast_units']:,.0f} units "
        f"(90% interval {lo:,.0f}–{hi:,.0f}). "
        f"Confidence {result['confidence']:.0f}/100 ({result['tier']}). "
        f"Source: dedicated {result['model']} model (not generated code)."
    )


if _ENGINE:

    @data_agent.tool
    async def forecast_demand(
        ctx: RunContext[CodeExecutorDeps],
        category: str,
        brand: str,
        chain: str | None = None,
    ) -> str:
        """Return a demand forecast for a brand from the dedicated forecasting model.

        Use this for ANY forward-looking / "next month" / "predict" / "expected
        sales" question. Do NOT write forecasting code — this tool calls a
        pre-trained, validated model and returns a point forecast, a 90% interval,
        and a confidence tier.

        Args:
            category: one of csd | danskvand | energidrikke | rtd.
            brand: brand name (e.g. HARBOE); case-insensitive.
            chain: optional retail chain (only danskvand is modelled per chain).
        """
        result = forecast_service.forecast_demand(category, brand, chain)
        return _format(result)

    @data_agent.system_prompt
    def add_forecast_context(ctx: "RunContext[ProjectDeps]") -> str:
        if getattr(ctx.deps, "agent_name", "") != "Oracle":
            return ""
        return (
            "\nYou have a `forecast_demand` tool backed by a dedicated, pre-trained "
            "forecasting model. **Use it for every predictive / forward-looking "
            "request** (next-month demand, expected sales). Never write or run "
            "forecasting code yourself — delegate to the tool, then explain its "
            "point forecast, interval, and confidence tier in plain commercial "
            "language. For purely descriptive questions (what happened), use the "
            "normal analysis path."
        )
