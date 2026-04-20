"""
Results Visualization Agent — Thesis Production System (System B)
------------------------------------------------------------------
Reads experiment data from the registry and generates figures
for inclusion in the thesis. All figures are reproducible — they
are generated from the experiment_registry.json, not drawn manually.

Complements the Diagram Agent (B7), which generates structural diagrams.
This agent generates data-driven results charts.

Output: thesis/writing/figures/results_*.{svg,png}
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .experiment_tracking_agent import ExperimentTrackingAgent


FIGURES_DIR = Path("thesis/writing/figures")


class ResultsVisualizationAgent:
    """
    Generates data-driven thesis figures from experiment registry data.
    Called by the Thesis Coordinator after experiments have been tracked.

    All methods accept the experiment list from ExperimentTrackingAgent
    so they can be called with either live or fixture data.
    """

    def __init__(
        self,
        tracker: Optional[ExperimentTrackingAgent] = None,
        output_dir: Path = FIGURES_DIR,
    ) -> None:
        self.tracker = tracker or ExperimentTrackingAgent()
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Main entry point ──────────────────────────────────────────────────────

    def run(self, figure_ids: Optional[List[str]] = None) -> Dict[str, List[Path]]:
        """
        Generate results figures. If figure_ids is None, generate all available.
        Returns a dict of figure_id → [svg_path, png_path].
        """
        experiments = self.tracker.get_all_experiments()
        latest = self.tracker.get_latest_experiment()

        generators = {
            "results_mape_comparison":      lambda: self.mape_comparison_chart(latest),
            "results_mape_progression":     lambda: self.mape_progression_chart(experiments),
            "results_ram_profile":          lambda: self.ram_profile_chart(latest),
            "results_calibration_coverage": lambda: self.calibration_coverage_plot(latest),
            "results_srq3_ablation":        lambda: self.srq3_ablation_chart(experiments),
        }

        target_ids = figure_ids or list(generators.keys())
        outputs: Dict[str, List[Path]] = {}

        for fig_id in target_ids:
            generator = generators.get(fig_id)
            if generator is None:
                continue
            if not experiments:
                print(f"[ResultsVisualizationAgent] No experiments yet — skipping {fig_id}")
                continue
            try:
                paths = generator()
                outputs[fig_id] = paths
                print(f"[ResultsVisualizationAgent] Generated: {fig_id}")
            except Exception as exc:
                print(f"[ResultsVisualizationAgent] Failed {fig_id}: {exc}")

        return outputs

    # ── Figure generators ──────────────────────────────────────────────────────

    def mape_comparison_chart(
        self, experiment: Optional[Dict[str, Any]]
    ) -> List[Path]:
        """
        Horizontal bar chart: MAPE per model for the latest experiment.
        Annotates bars with exact MAPE values. Red dashed line at target (15%).
        Corresponds to Ch.6 Table 6.1 visualisation.
        """
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        if not experiment:
            raise ValueError("No experiment data available.")

        metrics = experiment.get("metrics", {})
        models = [m for m, v in metrics.items() if v.get("MAPE") is not None]
        mapes = [metrics[m]["MAPE"] * 100 for m in models]  # convert to %

        if not models:
            raise ValueError("No MAPE values in experiment metrics.")

        # Sort by MAPE ascending (best first)
        paired = sorted(zip(mapes, models))
        mapes_sorted = [p[0] for p in paired]
        models_sorted = [p[1] for p in paired]

        colors = [
            "#4A90D9" if m == experiment.get("best_model_by_mape") else "#cccccc"
            for m in models_sorted
        ]

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.barh(models_sorted, mapes_sorted, color=colors, edgecolor="black", linewidth=0.5)
        ax.axvline(x=15, color="red", linestyle="--", linewidth=1, label="Target MAPE (15%)")

        for bar, val in zip(bars, mapes_sorted):
            ax.text(
                bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=10,
            )

        ax.set_xlabel("MAPE (%)", fontsize=12)
        ax.set_title(
            f"Model Benchmark — MAPE Comparison\n"
            f"Experiment: {experiment.get('experiment_id', '—')} | "
            f"Dataset: {experiment.get('dataset_version', '—')}",
            fontsize=11,
        )
        ax.legend(fontsize=10)
        ax.set_xlim(0, max(mapes_sorted) * 1.2)
        fig.tight_layout()

        return self._save(fig, "results_mape_comparison")

    def mape_progression_chart(
        self, experiments: List[Dict[str, Any]]
    ) -> List[Path]:
        """
        Line chart: MAPE per model across all experiments (x = experiment index).
        Shows learning curve as hyperparameters are tuned across runs.
        """
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        model_series: Dict[str, List[float]] = {}
        exp_ids = []

        for exp in experiments:
            exp_ids.append(exp.get("experiment_id", "—")[-8:])  # short ID
            for model, m in exp.get("metrics", {}).items():
                mape = m.get("MAPE")
                if mape is not None:
                    model_series.setdefault(model, []).append(mape * 100)

        if not model_series:
            raise ValueError("No MAPE data across experiments.")

        fig, ax = plt.subplots(figsize=(10, 5))
        colors = ["#4A90D9", "#7FC97F", "#FDC086", "#BEAED4", "#F0027F"]

        for (model, series), color in zip(model_series.items(), colors):
            x = list(range(1, len(series) + 1))
            ax.plot(x, series, marker="o", label=model, color=color, linewidth=2)

        ax.axhline(y=15, color="red", linestyle="--", linewidth=1, label="Target (15%)")
        ax.set_xlabel("Experiment run", fontsize=12)
        ax.set_ylabel("MAPE (%)", fontsize=12)
        ax.set_title("MAPE Progression Across Experiments", fontsize=12)
        ax.legend(fontsize=9)
        fig.tight_layout()

        return self._save(fig, "results_mape_progression")

    def ram_profile_chart(
        self, experiment: Optional[Dict[str, Any]]
    ) -> List[Path]:
        """
        Grouped bar chart: peak RAM per model + 8GB budget line.
        Demonstrates that each model stays within the 512MB per-model budget.
        Directly supports SRQ1 Level 3 evaluation.
        """
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        if not experiment:
            raise ValueError("No experiment data available.")

        runtime = experiment.get("runtime", {})
        models = [m for m, v in runtime.items() if v.get("peak_ram_mb") is not None]
        ram_vals = [runtime[m]["peak_ram_mb"] for m in models]

        if not models:
            raise ValueError("No RAM data in experiment.")

        colors = [
            "#7FC97F" if runtime[m].get("within_ram_budget", True) else "#FF6B6B"
            for m in models
        ]

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(models, ram_vals, color=colors, edgecolor="black", linewidth=0.5)
        ax.axhline(y=512, color="orange", linestyle="--", linewidth=1, label="Per-model budget (512 MB)")
        ax.axhline(y=8192, color="red", linestyle="--", linewidth=1, label="Total pipeline budget (8 GB)")

        for bar, val in zip(bars, ram_vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                f"{val:.0f}", ha="center", va="bottom", fontsize=10,
            )

        ax.set_ylabel("Peak RAM (MB)", fontsize=12)
        ax.set_title("RAM Profile per Model — Peak Memory Usage", fontsize=12)
        ax.legend(fontsize=9)
        fig.tight_layout()

        return self._save(fig, "results_ram_profile")

    def calibration_coverage_plot(
        self, experiment: Optional[Dict[str, Any]]
    ) -> List[Path]:
        """
        Calibration plot: stated confidence level vs. empirical coverage.
        A perfectly calibrated model lies on the diagonal.
        Supports SRQ2 confidence scoring validation.
        Cite: Kuleshov et al. (ICML 2018).
        """
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        if not experiment:
            raise ValueError("No experiment data available.")

        metrics = experiment.get("metrics", {})
        models_with_coverage = {
            m: v["calibration_coverage"]
            for m, v in metrics.items()
            if v.get("calibration_coverage") is not None
        }

        fig, ax = plt.subplots(figsize=(6, 6))

        # Perfect calibration diagonal
        ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Perfect calibration")

        # Target band (85–95% empirical for stated 90%)
        ax.axhspan(0.85, 0.95, alpha=0.1, color="green", label="Target band (85–95%)")

        if models_with_coverage:
            stated = 0.90  # thesis uses 90% prediction intervals
            colors = ["#4A90D9", "#7FC97F", "#FDC086", "#BEAED4", "#F0027F"]
            for (model, cov), color in zip(models_with_coverage.items(), colors):
                ax.scatter(stated, cov, s=100, label=f"{model} ({cov:.0%})", color=color, zorder=5)
        else:
            ax.text(0.5, 0.5, "No calibration data yet\n(run experiments first)",
                    ha="center", va="center", fontsize=11, color="gray")

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel("Stated confidence level", fontsize=12)
        ax.set_ylabel("Empirical coverage", fontsize=12)
        ax.set_title("Calibration Coverage — Stated vs. Empirical\n(Kuleshov et al. 2018 method)", fontsize=11)
        ax.legend(fontsize=9)
        fig.tight_layout()

        return self._save(fig, "results_calibration_coverage")

    def srq3_ablation_chart(
        self, experiments: List[Dict[str, Any]]
    ) -> List[Path]:
        """
        Side-by-side bar chart: MAPE with vs. without Indeks Danmark consumer signals.
        Directly visualises SRQ3 answer: does contextual enrichment improve accuracy?
        """
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        without = [
            e for e in experiments
            if not e.get("consumer_signals_included", True)
        ]
        with_signals = [
            e for e in experiments
            if e.get("consumer_signals_included", False)
        ]

        if not without or not with_signals:
            # Show placeholder if ablation pair not yet run
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.text(
                0.5, 0.5,
                "SRQ3 ablation requires two experiment runs:\n"
                "• consumer_signals_included = False\n"
                "• consumer_signals_included = True\n\n"
                "Run both experiments to populate this chart.",
                ha="center", va="center", fontsize=11, color="gray",
                transform=ax.transAxes,
            )
            ax.set_title("SRQ3 Ablation — Consumer Signal Contribution (Pending)", fontsize=12)
            fig.tight_layout()
            return self._save(fig, "results_srq3_ablation")

        # Use best MAPE from each group
        def best_mape(exp_list: List[Dict]) -> Dict[str, float]:
            best: Dict[str, float] = {}
            for exp in exp_list:
                for model, m in exp.get("metrics", {}).items():
                    mape = m.get("MAPE")
                    if mape is not None:
                        if model not in best or mape < best[model]:
                            best[model] = mape * 100
            return best

        mape_without = best_mape(without)
        mape_with = best_mape(with_signals)
        models = sorted(set(mape_without) | set(mape_with))

        x = np.arange(len(models))
        width = 0.35

        fig, ax = plt.subplots(figsize=(9, 5))
        bars1 = ax.bar(
            x - width / 2,
            [mape_without.get(m, 0) for m in models],
            width, label="Without Indeks Danmark", color="#cccccc", edgecolor="black", linewidth=0.5,
        )
        bars2 = ax.bar(
            x + width / 2,
            [mape_with.get(m, 0) for m in models],
            width, label="With Indeks Danmark", color="#4A90D9", edgecolor="black", linewidth=0.5,
        )

        ax.axhline(y=15, color="red", linestyle="--", linewidth=1, label="Target MAPE (15%)")
        ax.set_xlabel("Model", fontsize=12)
        ax.set_ylabel("MAPE (%)", fontsize=12)
        ax.set_title("SRQ3 Ablation — Impact of Consumer Signal Enrichment on MAPE", fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(models)
        ax.legend(fontsize=9)
        fig.tight_layout()

        return self._save(fig, "results_srq3_ablation")

    # ── Helper ─────────────────────────────────────────────────────────────────

    def _save(self, fig, fig_id: str) -> List[Path]:
        import matplotlib.pyplot as plt
        svg_path = self.output_dir / f"{fig_id}.svg"
        png_path = self.output_dir / f"{fig_id}.png"
        fig.savefig(str(svg_path), format="svg", bbox_inches="tight")
        fig.savefig(str(png_path), format="png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        return [svg_path, png_path]
