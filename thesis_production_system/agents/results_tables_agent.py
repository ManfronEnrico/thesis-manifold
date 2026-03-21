"""
Results Tables Agent — Thesis Production System (System B)
-----------------------------------------------------------
Reads experiment data from the registry and generates formatted Markdown
tables for direct inclusion in thesis sections.

All tables are reproducible — regenerated from experiment_registry.json.
Tables are appended to the relevant chapter section files or written to
standalone files in docs/thesis/tables/.

Output: docs/thesis/tables/table_*.md
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .experiment_tracking_agent import ExperimentTrackingAgent


TABLES_DIR = Path("docs/thesis/tables")


class ResultsTablesAgent:
    """
    Generates Markdown tables from experiment registry data.

    Tables produced:
    - table_model_benchmark      → Ch.6 model comparison table
    - table_srq3_ablation        → Ch.6/8 consumer signal contribution table
    - table_evaluation_level1    → Ch.8 Level 1 evaluation results
    - table_evaluation_level3    → Ch.8 Level 3 agent behaviour results
    - table_experiment_log       → Appendix experiment registry overview
    """

    def __init__(
        self,
        tracker: Optional[ExperimentTrackingAgent] = None,
        output_dir: Path = TABLES_DIR,
    ) -> None:
        self.tracker = tracker or ExperimentTrackingAgent()
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Main entry point ──────────────────────────────────────────────────────

    def run(self, table_ids: Optional[List[str]] = None) -> Dict[str, Path]:
        """
        Generate tables. If table_ids is None, generate all available.
        Returns dict of table_id → output_path.
        """
        experiments = self.tracker.get_all_experiments()
        latest = self.tracker.get_latest_experiment()

        generators = {
            "table_model_benchmark":   lambda: self.model_benchmark_table(latest),
            "table_srq3_ablation":     lambda: self.srq3_ablation_table(experiments),
            "table_evaluation_level1": lambda: self.evaluation_level1_table(latest),
            "table_evaluation_level3": lambda: self.evaluation_level3_table(latest),
            "table_experiment_log":    lambda: self.experiment_log_table(experiments),
        }

        target_ids = table_ids or list(generators.keys())
        outputs: Dict[str, Path] = {}

        for table_id in target_ids:
            generator = generators.get(table_id)
            if generator is None:
                continue
            if not experiments:
                self._write_placeholder(table_id)
                continue
            try:
                path = generator()
                outputs[table_id] = path
                print(f"[ResultsTablesAgent] Generated: {table_id} → {path}")
            except Exception as exc:
                print(f"[ResultsTablesAgent] Failed {table_id}: {exc}")

        return outputs

    # ── Table generators ───────────────────────────────────────────────────────

    def model_benchmark_table(
        self, experiment: Optional[Dict[str, Any]]
    ) -> Path:
        """
        Ch.6 Table 6.1 — Full model benchmark comparison.
        Columns: Model | MAPE (%) | RMSE | MAE | Dir. Acc. | Calib. Coverage | Peak RAM (MB) | Runtime (s)
        Best model row highlighted with **bold**.
        """
        if not experiment:
            raise ValueError("No experiment data.")

        metrics = experiment.get("metrics", {})
        runtime = experiment.get("runtime", {})
        best_model = experiment.get("best_model_by_mape", "")

        header = (
            "| Model | MAPE (%) | RMSE | MAE | Dir. Acc. | Calib. Coverage | Peak RAM (MB) | Runtime (s) |\n"
            "|---|---|---|---|---|---|---|---|\n"
        )

        rows = []
        for model in sorted(metrics.keys()):
            m = metrics[model]
            r = runtime.get(model, {})
            mape = f"{m['MAPE']*100:.2f}" if m.get("MAPE") is not None else "—"
            rmse = f"{m['RMSE']:.2f}" if m.get("RMSE") is not None else "—"
            mae = f"{m['MAE']:.2f}" if m.get("MAE") is not None else "—"
            dir_acc = f"{m['directional_accuracy']:.1%}" if m.get("directional_accuracy") is not None else "—"
            calib = f"{m['calibration_coverage']:.1%}" if m.get("calibration_coverage") is not None else "—"
            ram = f"{r['peak_ram_mb']:.0f}" if r.get("peak_ram_mb") is not None else "—"
            rt = f"{r['runtime_seconds']:.1f}" if r.get("runtime_seconds") is not None else "—"

            row = f"| {model} | {mape} | {rmse} | {mae} | {dir_acc} | {calib} | {ram} | {rt} |"
            if model == best_model:
                row = f"| **{model}** | **{mape}** | **{rmse}** | **{mae}** | **{dir_acc}** | **{calib}** | **{ram}** | **{rt}** |"
            rows.append(row)

        content = self._table_header(
            "Table 6.1 — Model Benchmark Results",
            f"Experiment: `{experiment.get('experiment_id', '—')}` | "
            f"Dataset: {experiment.get('dataset_version', '—')} | "
            f"Consumer signals: {'Yes' if experiment.get('consumer_signals_included') else 'No'}",
        )
        content += header + "\n".join(rows) + "\n\n"
        content += f"> **Bold** = best model ({best_model}). MAPE target: ≤ 15%. "
        content += "Calibration coverage target: ≥ 85% (Kuleshov et al., 2018 method).\n"

        return self._write(content, "table_model_benchmark")

    def srq3_ablation_table(
        self, experiments: List[Dict[str, Any]]
    ) -> Path:
        """
        SRQ3 ablation table: MAPE with vs. without Indeks Danmark consumer signals.
        Columns: Model | MAPE without (%) | MAPE with (%) | Improvement (pp) | Improvement (%)
        """
        without = {
            e.get("experiment_id"): e
            for e in experiments
            if not e.get("consumer_signals_included", True)
        }
        with_sig = {
            e.get("experiment_id"): e
            for e in experiments
            if e.get("consumer_signals_included", False)
        }

        content = self._table_header(
            "Table 6.2 — SRQ3 Ablation: Consumer Signal Contribution",
            "Comparison of MAPE with vs. without Indeks Danmark consumer demand indices.",
        )

        if not without or not with_sig:
            content += (
                "_Table pending: run experiments with `consumer_signals_included = False` "
                "and `consumer_signals_included = True` to populate this table._\n"
            )
            return self._write(content, "table_srq3_ablation")

        # Best MAPE per model per condition
        def best_mape_per_model(exp_dict: Dict) -> Dict[str, float]:
            best: Dict[str, float] = {}
            for exp in exp_dict.values():
                for model, m in exp.get("metrics", {}).items():
                    mape = m.get("MAPE")
                    if mape is not None and (model not in best or mape < best[model]):
                        best[model] = mape * 100
            return best

        mape_wo = best_mape_per_model(without)
        mape_wi = best_mape_per_model(with_sig)
        all_models = sorted(set(mape_wo) | set(mape_wi))

        header = "| Model | MAPE w/o signals (%) | MAPE w/ signals (%) | Δ (pp) | Δ (%) |\n|---|---|---|---|---|\n"
        rows = []
        for model in all_models:
            wo = mape_wo.get(model)
            wi = mape_wi.get(model)
            if wo is not None and wi is not None:
                delta_pp = wo - wi
                delta_pct = (delta_pp / wo) * 100
                rows.append(
                    f"| {model} | {wo:.2f} | {wi:.2f} | "
                    f"{'+'if delta_pp>0 else ''}{delta_pp:.2f} | "
                    f"{'+'if delta_pct>0 else ''}{delta_pct:.1f}% |"
                )
            else:
                rows.append(f"| {model} | {'—' if wo is None else f'{wo:.2f}'} | {'—' if wi is None else f'{wi:.2f}'} | — | — |")

        content += header + "\n".join(rows) + "\n\n"
        content += "> Positive Δ values indicate improvement from consumer signal enrichment (lower MAPE).\n"
        content += "> Cite: Customer Segmentation + Sales Prediction (2023); Xu et al. (2024).\n"

        return self._write(content, "table_srq3_ablation")

    def evaluation_level1_table(
        self, experiment: Optional[Dict[str, Any]]
    ) -> Path:
        """
        Ch.8 Table 8.1 — Level 1 evaluation results.
        Formatted for direct inclusion in the evaluation chapter.
        """
        if not experiment:
            raise ValueError("No experiment data.")

        content = self._table_header(
            "Table 8.1 — Level 1 Evaluation: ML Accuracy",
            f"Experiment: `{experiment.get('experiment_id', '—')}` | "
            f"Target MAPE: ≤ 15% | Calibration coverage target: ≥ 85%.",
        )

        metrics = experiment.get("metrics", {})
        best = experiment.get("best_model_by_mape", "")

        header = "| Model | MAPE (%) | RMSE | MAE | Dir. Acc. | Calib. Coverage | Within target? |\n|---|---|---|---|---|---|---|\n"
        rows = []
        for model, m in sorted(metrics.items()):
            mape_val = m.get("MAPE")
            mape_str = f"{mape_val*100:.2f}" if mape_val is not None else "—"
            within = "✅" if (mape_val is not None and mape_val * 100 <= 15) else ("❌" if mape_val is not None else "—")
            calib = m.get("calibration_coverage")
            calib_str = f"{calib:.1%}" if calib is not None else "—"
            rows.append(
                f"| {'**' + model + '**' if model == best else model} | {mape_str} | "
                f"{m.get('RMSE', '—') or '—'} | {m.get('MAE', '—') or '—'} | "
                f"{('{:.1%}'.format(m['directional_accuracy'])) if m.get('directional_accuracy') else '—'} | "
                f"{calib_str} | {within} |"
            )

        content += header + "\n".join(rows) + "\n"
        return self._write(content, "table_evaluation_level1")

    def evaluation_level3_table(
        self, experiment: Optional[Dict[str, Any]]
    ) -> Path:
        """
        Ch.8 Table 8.3 — Level 3 evaluation: agent behaviour (RAM + latency).
        """
        if not experiment:
            raise ValueError("No experiment data.")

        content = self._table_header(
            "Table 8.3 — Level 3 Evaluation: Agent Behaviour",
            f"Experiment: `{experiment.get('experiment_id', '—')}` | "
            f"RAM budget: ≤ 8,192 MB total | Per-model budget: ≤ 512 MB.",
        )

        runtime = experiment.get("runtime", {})
        peak_total = experiment.get("peak_ram_total_mb")
        within_budget = experiment.get("within_total_ram_budget", True)

        header = "| Model | Peak RAM (MB) | Within budget? | Runtime (s) | Inference latency (s) |\n|---|---|---|---|---|\n"
        rows = []
        for model, r in sorted(runtime.items()):
            ram = r.get("peak_ram_mb")
            ram_str = f"{ram:.0f}" if ram is not None else "—"
            ok = "✅" if r.get("within_ram_budget", True) else "❌"
            rt = r.get("runtime_seconds")
            rt_str = f"{rt:.1f}" if rt is not None else "—"
            rows.append(f"| {model} | {ram_str} | {ok} | {rt_str} | — |")

        total_row = (
            f"| **Pipeline total** | "
            f"**{peak_total:.0f}** | "
            f"{'✅' if within_budget else '❌'} | — | — |"
            if peak_total is not None else ""
        )

        content += header + "\n".join(rows)
        if total_row:
            content += "\n" + total_row
        content += "\n\n> Sequential model execution protocol ensures only one model is in RAM at a time.\n"

        return self._write(content, "table_evaluation_level3")

    def experiment_log_table(
        self, experiments: List[Dict[str, Any]]
    ) -> Path:
        """
        Appendix table: full experiment log for reproducibility.
        One row per experiment run.
        """
        content = self._table_header(
            "Appendix — Experiment Registry Log",
            f"Full record of all {len(experiments)} experiment(s) for reproducibility. "
            "Generated from `docs/experiments/experiment_registry.json`.",
        )

        header = "| Experiment ID | Timestamp | Dataset | Models | Consumer signals | Best model | Peak RAM (MB) | Within budget? |\n|---|---|---|---|---|---|---|---|\n"
        rows = []
        for exp in experiments:
            exp_id = exp.get("experiment_id", "—")
            ts = exp.get("timestamp", "—")[:10]
            dataset = exp.get("dataset_version", "—")
            models = ", ".join(exp.get("models_executed", []))
            signals = "Yes" if exp.get("consumer_signals_included") else "No"
            best = exp.get("best_model_by_mape", "—")
            ram = exp.get("peak_ram_total_mb")
            ram_str = f"{ram:.0f}" if ram is not None else "—"
            within = "✅" if exp.get("within_total_ram_budget", True) else "❌"
            rows.append(f"| `{exp_id}` | {ts} | {dataset} | {models} | {signals} | {best} | {ram_str} | {within} |")

        content += header + "\n".join(rows) + "\n"
        return self._write(content, "table_experiment_log")

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _table_header(self, title: str, subtitle: str = "") -> str:
        lines = [
            f"# {title}",
            f"> Auto-generated by ResultsTablesAgent — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"> Source: `docs/experiments/experiment_registry.json`",
        ]
        if subtitle:
            lines.append(f"> {subtitle}")
        lines += ["", "---", ""]
        return "\n".join(lines)

    def _write(self, content: str, table_id: str) -> Path:
        path = self.output_dir / f"{table_id}.md"
        path.write_text(content)
        return path

    def _write_placeholder(self, table_id: str) -> Path:
        content = self._table_header(
            f"{table_id.replace('_', ' ').title()}",
            "Pending: no experiments have been run yet.",
        )
        content += "_This table will be auto-generated once forecasting experiments are complete._\n"
        return self._write(content, table_id)
