# Builder Agent — README

The Builder Agent is a sub-system inside System B (Thesis Production System) that
automatically generates, executes, evaluates, and iterates on System A configurations
without manual intervention.

---

## What it does

Given a high-level goal (e.g. "find the best 3-model ensemble under 512 MB RAM"), the
Builder autonomously:

1. **Architect** — designs the next System A configuration (model subset, ensemble
   weights, consumer signal flag)
2. **Coder** — generates a Python trial script by patching the base template
3. **Executor** — runs the script in an isolated subprocess (10-minute timeout)
4. **Logger** — persists the trial result to `results/experiment_registry.json`
5. **Evaluator** — checks stopping conditions (convergence / budget / RAM violation)
   and produces a 3-sentence judgment
6. Loops back to Architect until a stopping condition is met

Results are available to the Writing Agent and Results Viz Agent after the loop ends.

---

## Prerequisites

1. **Phase 1 must have run at least once** — the Builder loads the feature matrix
   and consumer signals from disk (it does not re-run PCA). The expected paths are:
   - `results/phase1/feature_matrix.parquet` (or `.csv`)
   - `results/phase1/consumer_signals.json`

2. **Nielsen data must be available** — the trial scripts import from
   `ai_research_framework.agents.forecasting_agent`. If Nielsen data is not found,
   the Executor returns a clear error and records the failure.

3. **`ANTHROPIC_API_KEY` environment variable** must be set for the Architect,
   Evaluator, and Coder (all use claude-sonnet-4-6 at temperature=0).

---

## Triggering from the Thesis Coordinator

Add a `build_and_experiment` task to the TaskPlan:

```python
from thesis_production_system.core.coordinator import ThesisCoordinator

coordinator = ThesisCoordinator()
coordinator.run_build_experiment(
    goal="find the best ensemble of 3 models that stays under 512MB peak RAM",
    max_trials=30,
)
```

Or add it via the TaskPlan mechanism (the Coordinator's `_dispatch` handles it):

```python
task = Task(
    agent="BuilderAgent",
    action="build_and_experiment",
    priority=1,
    context={
        "goal": "find best 3-model ensemble under 512MB RAM",
        "max_trials": 30,
    },
)
```

---

## Running directly (without the Coordinator)

```python
from thesis_production_system.agents.builder import run_builder

final_state = run_builder(
    goal="find the best ensemble of 3 models that stays under 512MB peak RAM",
    max_trials=10,
    feature_matrix_path="results/phase1/feature_matrix.parquet",
    consumer_signals_path="results/phase1/consumer_signals.json",
)

print("Best trial:", final_state["best_trial_id"])
print("Stop reason:", final_state["stop_reason"])
print("Evaluator:", final_state["evaluator_judgment"])
```

---

## Reading results after the loop

```python
from thesis_production_system.agents.builder import BuilderRegistry

registry = BuilderRegistry()

# Best trial by MAPE
best = registry.get_best_trial(metric="MAPE")
print(best["trial_id"], best["result"]["MAPE"])

# All results as DataFrame (for Results Viz Agent)
df = registry.get_all_results_as_dataframe()
print(df[["trial_id", "MAPE", "peak_RAM_MB", "evaluator_judgment"]])
```

Registry file: `results/experiment_registry.json` (append-only, never deleted).

---

## Stopping conditions

| Condition | Trigger | stop_reason |
|---|---|---|
| Budget exhausted | `trials_run >= max_trials` | `"budget_exhausted"` |
| Convergence | Last 5 successful trials show < 0.5% MAPE improvement | `"converged"` |
| RAM violation | Any trial exceeded 7,680 MB (7.5 GB) | `"ram_violation"` |
| Manual stop | Architect fails to propose a novel config after 5 attempts | `"human_stop"` |

---

## File structure

```
ai_research_framework/
└── templates/
    └── base_config.py          ← Template patched by Coder for each trial

thesis_production_system/
└── agents/
    └── builder/
        ├── __init__.py
        ├── architect.py        ← Designs the next TrialConfig (Claude API)
        ├── coder.py            ← Generates trial script from template (Claude API)
        ├── executor.py         ← Runs trial script as subprocess
        ├── evaluator.py        ← Stopping conditions + judgment (Claude API)
        ├── builder_graph.py    ← LangGraph StateGraph (the loop)
        └── experiment_registry.py ← Append-only JSON registry

results/
├── experiment_registry.json    ← All trial metadata (append-only)
├── scripts/
│   └── trial_{id}.py          ← Generated trial scripts
└── trial_{id}.json             ← Per-trial output JSON

tests/
└── test_builder_integration.py ← Integration tests (3 test classes)
```

---

## Running the tests

```bash
python -m pytest tests/test_builder_integration.py -v
```

Tests do not require `ANTHROPIC_API_KEY` — all LLM calls are mocked.
Tests do not require Nielsen data — Executor tests use synthetic scripts.

---

## Integration with other System B agents

After the Builder loop completes:

- **Writing Agent** receives `best_trial_id` + all `TrialResult` objects
  → produces bullet-point skeleton for Ch.6 (Model Benchmark)
  → follows the standard Writing Agent protocol (bullets only, awaits human approval)

- **Results Viz Agent** calls `registry.get_all_results_as_dataframe()`
  → generates MAPE comparison bar chart, RAM budget chart, model combination heatmap
  → saves to `docs/thesis/figures/` as SVG + PNG

- **Experiment Tracker** (existing System B agent) receives the full registry
  → updates ThesisState with experiment log entries
