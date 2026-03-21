"""
Diagram Agent — Thesis Production System (System B)
----------------------------------------------------
Generates all thesis figures as reproducible, code-generated artifacts.
Every figure is produced by a Python function, not drawn manually.

Output directory: docs/thesis/figures/
Output formats: SVG + PNG (both generated for each figure)

Available figure types:
  - system_architecture   : full multi-agent framework diagram
  - agent_workflow        : LangGraph state machine flow
  - model_performance     : model comparison chart (populated post-benchmark)
  - evaluation_plot       : 3-level validation results
  - data_flow             : data ingestion → feature → model → synthesis flow
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from ..state.thesis_state import FigureState, ThesisState


FIGURES_DIR = Path("docs/thesis/figures")


class DiagramAgent:
    """Generates thesis figures. All figures are reproducible from source code."""

    def __init__(self, output_dir: Path = FIGURES_DIR) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, state: ThesisState, figure_ids: Optional[List[str]] = None) -> ThesisState:
        """
        Generate figures. If figure_ids is None, generate all missing figures.
        Returns updated ThesisState with figure records.
        """
        generators = {
            "system_architecture_v1": self.generate_system_architecture,
            "agent_workflow_v1": self.generate_agent_workflow,
            "data_flow_v1": self.generate_data_flow,
            "model_performance_v1": self.generate_model_performance_chart,
            "evaluation_plot_v1": self.generate_evaluation_plot,
        }

        target_ids = figure_ids or list(generators.keys())

        for fig_id in target_ids:
            generator = generators.get(fig_id)
            if generator is None:
                continue
            try:
                output_paths = generator(fig_id)
                state.figures[fig_id] = FigureState(
                    figure_id=fig_id,
                    figure_type=self._infer_type(fig_id),
                    output_path=str(output_paths[0]),   # primary (SVG)
                    format="svg",
                    generated=True,
                    generation_script=f"thesis_production_system/agents/diagram_agent.py",
                )
            except Exception as exc:
                # Non-fatal: log and continue
                print(f"[DiagramAgent] Failed to generate {fig_id}: {exc}")

        return state

    # ── Figure generators ──────────────────────────────────────────────────────

    def generate_system_architecture(self, fig_id: str) -> List[Path]:
        """
        Generate the full multi-agent framework architecture diagram.
        Shows: Coordinator + 4 research agents + LangGraph flow.
        Tool: graphviz (Digraph)
        """
        try:
            import graphviz
        except ImportError:
            raise ImportError("Install graphviz: pip install graphviz")

        dot = graphviz.Digraph(
            name="AI Research Framework",
            comment="System A — Thesis Research Framework",
            graph_attr={"rankdir": "TB", "fontname": "Helvetica", "splines": "ortho"},
            node_attr={"fontname": "Helvetica", "shape": "box", "style": "rounded,filled"},
            edge_attr={"fontname": "Helvetica", "fontsize": "10"},
        )

        # Nodes
        dot.node("coordinator", "Coordinator\n(LangGraph StateGraph)", fillcolor="#4A90D9", fontcolor="white")
        dot.node("data_agent", "Data Assessment\nAgent", fillcolor="#7FC97F")
        dot.node("forecast_agent", "Forecasting Agent\n(ARIMA | Prophet | LightGBM\nXGBoost | Ridge)", fillcolor="#7FC97F")
        dot.node("synthesis_agent", "Synthesis Agent\n(Claude API)", fillcolor="#FDC086")
        dot.node("validation_agent", "Validation Agent\n(3-level eval)", fillcolor="#BEAED4")
        dot.node("state", "ResearchState\n(LangGraph TypedDict)", fillcolor="#F0F0F0", shape="cylinder")
        dot.node("ram", "≤ 8 GB RAM\nConstraint", fillcolor="#FFCCCC", shape="diamond")

        # Edges
        dot.edge("coordinator", "data_agent", label="phase: data_assessment")
        dot.edge("coordinator", "forecast_agent", label="phase: model_benchmarking")
        dot.edge("coordinator", "synthesis_agent", label="phase: synthesis")
        dot.edge("coordinator", "validation_agent", label="phase: validation")
        dot.edge("data_agent", "state", style="dashed")
        dot.edge("forecast_agent", "state", style="dashed")
        dot.edge("synthesis_agent", "state", style="dashed")
        dot.edge("validation_agent", "state", style="dashed")
        dot.edge("coordinator", "ram", label="monitored", style="dotted")

        return self._render(dot, fig_id)

    def generate_agent_workflow(self, fig_id: str) -> List[Path]:
        """
        Generate the LangGraph state machine workflow diagram.
        Shows conditional edges and human-in-the-loop interrupt points.
        """
        try:
            import graphviz
        except ImportError:
            raise ImportError("Install graphviz: pip install graphviz")

        dot = graphviz.Digraph(
            name="Agent Workflow",
            graph_attr={"rankdir": "LR", "fontname": "Helvetica"},
            node_attr={"fontname": "Helvetica", "shape": "box", "style": "rounded,filled"},
        )

        dot.node("start", "START", shape="circle", fillcolor="#4A90D9", fontcolor="white")
        dot.node("data", "data_assessment", fillcolor="#7FC97F")
        dot.node("approval1", "HUMAN APPROVAL\n(data quality)", shape="diamond", fillcolor="#FFCCCC")
        dot.node("forecast", "model_benchmarking", fillcolor="#7FC97F")
        dot.node("approval2", "HUMAN APPROVAL\n(benchmark results)", shape="diamond", fillcolor="#FFCCCC")
        dot.node("synthesis", "synthesis", fillcolor="#FDC086")
        dot.node("validation", "validation", fillcolor="#BEAED4")
        dot.node("approval3", "HUMAN APPROVAL\n(validation report)", shape="diamond", fillcolor="#FFCCCC")
        dot.node("end", "END", shape="circle", fillcolor="#4A90D9", fontcolor="white")

        dot.edge("start", "data")
        dot.edge("data", "approval1")
        dot.edge("approval1", "forecast", label="✓ approved")
        dot.edge("approval1", "end", label="✗ rejected")
        dot.edge("forecast", "approval2")
        dot.edge("approval2", "synthesis", label="✓ approved")
        dot.edge("approval2", "end", label="✗ rejected")
        dot.edge("synthesis", "validation")
        dot.edge("validation", "approval3")
        dot.edge("approval3", "end")

        return self._render(dot, fig_id)

    def generate_data_flow(self, fig_id: str) -> List[Path]:
        """Generate data ingestion → feature engineering → model → synthesis flow."""
        try:
            import graphviz
        except ImportError:
            raise ImportError("Install graphviz: pip install graphviz")

        dot = graphviz.Digraph(
            name="Data Flow",
            graph_attr={"rankdir": "LR", "fontname": "Helvetica"},
            node_attr={"fontname": "Helvetica", "shape": "box", "style": "rounded,filled"},
        )

        # Data sources
        with dot.subgraph(name="cluster_sources") as s:
            s.attr(label="Data Sources", style="dashed")
            s.node("nielsen", "Nielsen CSD\n(Star schema SQL)", fillcolor="#E8F4FD")
            s.node("indeks", "Indeks Danmark\n(20,134 × 6,364 CSV)", fillcolor="#E8F4FD")

        # Processing
        dot.node("features", "Feature Engineering\n(lags, rolling, calendar,\nconsumer signals)", fillcolor="#7FC97F")
        dot.node("models", "5 ML Models\n(sequential)", fillcolor="#FDC086")
        dot.node("synthesis", "Synthesis Agent\n(ensemble + calibration)", fillcolor="#BEAED4")
        dot.node("output", "Natural Language\nRecommendation\n+ Confidence Score", fillcolor="#4A90D9", fontcolor="white")

        dot.edge("nielsen", "features", label="sales metrics")
        dot.edge("indeks", "features", label="PCA + k-means\nconsumer segments")
        dot.edge("features", "models")
        dot.edge("models", "synthesis", label="5 × forecasts\n+ intervals")
        dot.edge("synthesis", "output")

        return self._render(dot, fig_id)

    def generate_model_performance_chart(self, fig_id: str) -> List[Path]:
        """
        Generate model comparison bar chart.
        Uses placeholder data — replace with actual results post-benchmark.
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("Install matplotlib: pip install matplotlib")

        models = ["ARIMA", "Prophet", "Ridge", "XGBoost", "LightGBM"]
        mape_placeholder = [22.1, 18.4, 19.2, 13.8, 11.5]   # Hypothetical — replace post-benchmark
        colors = ["#cccccc", "#cccccc", "#cccccc", "#7FC97F", "#4A90D9"]

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(models, mape_placeholder, color=colors, edgecolor="black", linewidth=0.5)
        ax.axhline(y=15, color="red", linestyle="--", linewidth=1, label="Target MAPE (15%)")
        ax.set_ylabel("MAPE (%)", fontsize=12)
        ax.set_title("Model Benchmark — MAPE Comparison\n(Placeholder data — replace with actual results)", fontsize=11)
        ax.legend()
        ax.set_ylim(0, 30)

        for bar, val in zip(bars, mape_placeholder):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    f"{val:.1f}%", ha="center", va="bottom", fontsize=10)

        fig.tight_layout()
        return self._save_matplotlib(fig, fig_id)

    def generate_evaluation_plot(self, fig_id: str) -> List[Path]:
        """
        Generate 3-level evaluation results visualisation.
        Placeholder structure — populate post-evaluation.
        """
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("Install matplotlib: pip install matplotlib")

        fig, axes = plt.subplots(1, 3, figsize=(14, 5))
        fig.suptitle("3-Level Evaluation Results (Placeholder)", fontsize=13)

        # Level 1: ML accuracy
        models = ["ARIMA", "Prophet", "Ridge", "XGBoost", "LightGBM"]
        mape = [22.1, 18.4, 19.2, 13.8, 11.5]
        axes[0].barh(models, mape, color="#7FC97F")
        axes[0].axvline(x=15, color="red", linestyle="--")
        axes[0].set_title("Level 1: MAPE (%)", fontsize=11)
        axes[0].set_xlabel("MAPE (%)")

        # Level 2: Recommendation quality
        dimensions = ["Accuracy", "Calibration", "Actionability", "Relevance", "Clarity"]
        scores = [4.1, 3.8, 4.3, 3.9, 4.5]
        axes[1].barh(dimensions, scores, color="#FDC086")
        axes[1].axvline(x=3.5, color="red", linestyle="--", label="Target ≥3.5")
        axes[1].set_xlim(0, 5)
        axes[1].set_title("Level 2: LLM-as-Judge (1–5)", fontsize=11)
        axes[1].set_xlabel("Score")

        # Level 3: RAM usage
        components = ["Data Agent", "Forecasting\n(per model)", "Synthesis\nAgent", "Total\nPipeline"]
        ram = [980, 420, 45, 3800]
        colors_ram = ["#cccccc", "#cccccc", "#cccccc", "#4A90D9"]
        axes[2].bar(components, ram, color=colors_ram, edgecolor="black", linewidth=0.5)
        axes[2].axhline(y=8192, color="red", linestyle="--", label="8GB limit")
        axes[2].set_title("Level 3: Peak RAM (MB)", fontsize=11)
        axes[2].set_ylabel("MB")
        axes[2].legend(fontsize=8)

        fig.tight_layout()
        return self._save_matplotlib(fig, fig_id)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _render(self, dot, fig_id: str) -> List[Path]:
        """Render a graphviz Digraph to SVG and PNG."""
        svg_path = self.output_dir / fig_id
        dot.render(str(svg_path), format="svg", cleanup=True)
        dot.render(str(svg_path), format="png", cleanup=True)
        return [svg_path.with_suffix(".svg"), svg_path.with_suffix(".png")]

    def _save_matplotlib(self, fig, fig_id: str) -> List[Path]:
        """Save a matplotlib figure to SVG and PNG."""
        import matplotlib.pyplot as plt
        svg_path = self.output_dir / f"{fig_id}.svg"
        png_path = self.output_dir / f"{fig_id}.png"
        fig.savefig(str(svg_path), format="svg", bbox_inches="tight")
        fig.savefig(str(png_path), format="png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        return [svg_path, png_path]

    @staticmethod
    def _infer_type(fig_id: str) -> str:
        if "architecture" in fig_id:
            return "architecture"
        if "workflow" in fig_id:
            return "workflow"
        if "performance" in fig_id or "model" in fig_id:
            return "model_performance"
        if "evaluation" in fig_id:
            return "evaluation_plot"
        return "data_flow"
