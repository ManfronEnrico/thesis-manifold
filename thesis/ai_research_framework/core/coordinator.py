"""
Research Framework Coordinator — AI Research Framework (System A)
------------------------------------------------------------------
LangGraph StateGraph that orchestrates the four research agents.
The Coordinator is the sole node that decides phase transitions.

Every phase transition that requires human approval calls interrupt()
which halts the graph and yields control back to the user.
"""

from __future__ import annotations

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from ..agents import (
    DataAssessmentAgent,
    ForecastingAgent,
    SynthesisAgent,
    ValidationAgent,
)
from ..config import NielsenConfig, IndeksDanmarkConfig
from ..state.research_state import ResearchState


def _should_continue_after_data(state: ResearchState) -> str:
    """Route after data assessment: error → stop, else → forecasting."""
    if state.get("errors"):
        return "end"
    if state.get("requires_human_approval"):
        return "await_approval"   # Human-in-the-loop interrupt
    return "forecasting"


def _should_continue_after_forecasting(state: ResearchState) -> str:
    """Route after benchmarking: error → stop, else → synthesis."""
    if state.get("errors"):
        return "end"
    return "synthesis"


def _should_continue_after_synthesis(state: ResearchState) -> str:
    if state.get("errors"):
        return "end"
    return "validation"


def _should_continue_after_validation(state: ResearchState) -> str:
    if state.get("requires_human_approval"):
        return "await_approval"
    return "end"


def build_research_graph() -> StateGraph:
    """
    Assembles the LangGraph StateGraph for the AI Research Framework.
    Returns a compiled graph ready for invocation.

    Usage:
        graph = build_research_graph()
        result = graph.invoke(initial_state, config={"configurable": {"thread_id": "run-1"}})
    """
    nielsen_cfg = NielsenConfig()
    indeks_cfg = IndeksDanmarkConfig()

    data_agent = DataAssessmentAgent(nielsen_cfg, indeks_cfg)
    forecast_agent = ForecastingAgent()
    synthesis_agent = SynthesisAgent()
    validation_agent = ValidationAgent()

    graph = StateGraph(ResearchState)

    # ── Nodes ──────────────────────────────────────────────────────────────────
    graph.add_node("data_assessment", data_agent.run)
    graph.add_node("forecasting", forecast_agent.run)
    graph.add_node("synthesis", synthesis_agent.run)
    graph.add_node("validation", validation_agent.run)

    # ── Edges ──────────────────────────────────────────────────────────────────
    graph.set_entry_point("data_assessment")

    graph.add_conditional_edges(
        "data_assessment",
        _should_continue_after_data,
        {"forecasting": "forecasting", "end": END, "await_approval": END},
    )
    graph.add_conditional_edges(
        "forecasting",
        _should_continue_after_forecasting,
        {"synthesis": "synthesis", "end": END},
    )
    graph.add_conditional_edges(
        "synthesis",
        _should_continue_after_synthesis,
        {"validation": "validation", "end": END},
    )
    graph.add_conditional_edges(
        "validation",
        _should_continue_after_validation,
        {"await_approval": END, "end": END},
    )

    # Persist state across invocations (human-in-the-loop checkpointing)
    memory = MemorySaver()
    return graph.compile(checkpointer=memory, interrupt_before=["forecasting", "validation"])
