"""
Thesis Production Coordinator — Thesis Production System (System B)
--------------------------------------------------------------------
Orchestrates the thesis production agents using the Planner → Execute → Critic workflow.

Execution flow:
  1. PlannerAgent.run(state)       → TaskPlan
  2. For each Task in plan:
       a. Route to appropriate agent
       b. Execute agent action
       c. CriticAgent.validate(output)
       d. If valid → update state → persist
          If invalid → retry once with critic issues → if still invalid → log and skip
  3. Present summary to user → await human approval

The Coordinator does NOT implement logic — it only routes and orchestrates.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from ..agents.planner_agent import PlannerAgent, TaskPlan, Task
from ..agents.critic_agent import CriticAgent, CriticResult
from ..agents.literature_agent import LiteratureAgent
from ..agents.writing_agent import WritingAgent
from ..agents.compliance_agent import ComplianceAgent
from ..agents.diagram_agent import DiagramAgent
from ..agents.builder.builder_graph import run_builder
from ..state.thesis_state import ThesisState


class ThesisCoordinator:
    """
    Sole orchestrator for the thesis production system.
    Dispatches tasks from the TaskPlan to the appropriate agents,
    validates outputs with the Critic, and updates shared state.
    """

    MAX_RETRIES = 1   # Retry failed tasks once with critic feedback

    def __init__(self, project_root: Path = Path(".")) -> None:
        self.project_root = project_root
        self.planner = PlannerAgent(project_root)
        self.critic = CriticAgent()
        self.literature_agent = LiteratureAgent(project_root)
        self.writing_agent = WritingAgent(project_root)
        self.compliance_agent = ComplianceAgent(project_root)
        self.diagram_agent = DiagramAgent(project_root / "docs/thesis/figures")

    # ── Main entry point ──────────────────────────────────────────────────────

    def run_session(self, state: Optional[ThesisState] = None) -> ThesisState:
        """
        Execute one full session cycle:
        Plan → Execute all tasks → Persist state → Return summary.
        """
        if state is None:
            state = ThesisState.load()

        # Step 1: Plan
        task_plan = self.planner.run(state)
        state.last_task_plan = task_plan.model_dump()
        self._log(f"Planned {len(task_plan.tasks)} task(s). Blocked: {task_plan.blocked_tasks}")

        # Step 2: Execute
        for task in task_plan.tasks:
            state = self._execute_task(task, state)

        # Step 3: Persist
        state.save()
        return state

    # ── Task dispatcher ───────────────────────────────────────────────────────

    def _execute_task(self, task: Task, state: ThesisState) -> ThesisState:
        """Execute a single task and validate the output with the Critic."""
        self._log(f"Executing [{task.priority}] {task.agent}.{task.action}")

        for attempt in range(1, self.MAX_RETRIES + 2):
            try:
                output, new_state = self._dispatch(task, state)
            except NotImplementedError as exc:
                self._log(f"  ↳ SKIP (not implemented): {exc}")
                return state
            except Exception as exc:  # noqa: BLE001
                self._log(f"  ↳ ERROR: {exc}")
                return state

            result: CriticResult = self.critic.validate(
                agent=task.agent,
                action=task.action,
                output=output,
                context={**task.context, "state": state},
            )
            state.last_critic_result = result.model_dump()

            if result.status == "valid":
                self._log(f"  ↳ VALID (confidence={result.confidence:.2f})")
                return new_state
            else:
                self._log(f"  ↳ INVALID (attempt {attempt}): {result.issues}")
                if attempt > self.MAX_RETRIES:
                    self._log("  ↳ Max retries reached. Skipping task.")
                    return state
                # Enrich task context with critic issues for retry
                task.context["critic_issues"] = result.issues

        return state

    def _dispatch(
        self, task: Task, state: ThesisState
    ) -> tuple[Any, ThesisState]:
        """Route task to the appropriate agent method."""

        if task.agent == "LiteratureAgent":
            if task.action == "run_scraping":
                new_state = self.literature_agent.run_scraping(state)
                return "scraping_complete", new_state
            elif task.action == "confirm_pending_papers":
                # Requires human to have confirmed which papers to add
                # In practice, this is triggered by the user
                raise NotImplementedError(
                    "Paper confirmation requires explicit human approval — "
                    "user must call confirm_papers() with a list of titles."
                )
            elif task.action == "update_gap_analysis":
                new_state = self.literature_agent.update_gap_analysis(state)
                return "gap_analysis_updated", new_state

        elif task.agent == "WritingAgent":
            if task.action == "draft_section_bullets":
                chapters = task.context.get("chapters", [])
                new_state = self.writing_agent.draft_section_bullets(state, chapters)
                # Read the generated content for Critic validation
                outputs = []
                for ch_id in chapters:
                    sec = new_state.sections.get(ch_id)
                    if sec and sec.bullet_file:
                        p = self.project_root / sec.bullet_file
                        if p.exists():
                            outputs.append(p.read_text())
                return "\n\n---\n\n".join(outputs), new_state

        elif task.agent == "ComplianceAgent":
            if task.action == "check_section_compliance":
                chapters = task.context.get("chapters", [])
                new_state = self.compliance_agent.check_section_compliance(state, chapters)
                report = {ch: new_state.compliance_checks.checks.get(ch) for ch in chapters}
                return str(report), new_state

        elif task.agent == "DiagramAgent":
            if task.action == "generate_figures":
                fig_ids = task.context.get("figure_ids", [])
                new_state = self.diagram_agent.run(state, fig_ids)
                return f"Generated: {fig_ids}", new_state

        elif task.agent == "BuilderAgent":
            if task.action == "build_and_experiment":
                goal = task.context.get("goal", "optimise System A configuration")
                max_trials = task.context.get("max_trials", 30)
                final_builder_state = run_builder(goal=goal, max_trials=max_trials)
                stop_reason = final_builder_state.get("stop_reason", "unknown")
                best_id = final_builder_state.get("best_trial_id")
                return f"Builder done: {stop_reason}, best={best_id}", state

        raise ValueError(f"Unknown task: {task.agent}.{task.action}")

    # ── Builder convenience method ─────────────────────────────────────────────

    def run_build_experiment(
        self,
        goal: str,
        max_trials: int = 30,
        feature_matrix_path: str = "results/phase1/feature_matrix.parquet",
        consumer_signals_path: str = "results/phase1/consumer_signals.json",
    ) -> dict:
        """
        Trigger the Builder Agent loop directly (bypasses the TaskPlan mechanism).
        Use this when you want to run the Builder without a full session cycle.

        Parameters
        ----------
        goal : str
            High-level goal string (e.g. "find best 3-model ensemble under 512MB RAM").
        max_trials : int
            Maximum trials before stopping (default 30).
        feature_matrix_path, consumer_signals_path : str
            Paths to Phase 1 outputs. Phase 1 must have run at least once first.

        Returns
        -------
        dict
            Final BuilderState with best_trial_id, stop_reason, and all results.
        """
        self._log(f"Starting Builder Agent: goal='{goal}', max_trials={max_trials}")
        final_state = run_builder(
            goal=goal,
            max_trials=max_trials,
            feature_matrix_path=feature_matrix_path,
            consumer_signals_path=consumer_signals_path,
        )
        self._log(
            f"Builder done: stop_reason={final_state.get('stop_reason')}, "
            f"best={final_state.get('best_trial_id')}"
        )
        return final_state

    # ── Logging ───────────────────────────────────────────────────────────────

    @staticmethod
    def _log(msg: str) -> None:
        print(f"[ThesisCoordinator] {msg}")
