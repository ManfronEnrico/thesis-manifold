# Experiment Tracking Agent
> Part of: Thesis Production System (System B)
> Location: `thesis_production_system/agents/experiment_tracking_agent.py`
> Last updated: 2026-03-15

---

## 1. Purpose

The Experiment Tracking Agent automatically captures metadata from every forecasting experiment run by the AI Research Framework (System A) and stores it in a structured, queryable JSON registry.

Its primary goal is **reproducibility**: any thesis result can be traced back to a specific experiment, with a full record of what models were run, which hyperparameters were used, and what metrics were obtained.

**Distinction from research agents**: the Experiment Tracking Agent is a production tool (System B). It does not perform forecasting, synthesis, or evaluation. It only observes and records.

---

## 2. What the agent tracks

For every experiment, the registry stores:

| Field | Description |
|---|---|
| `experiment_id` | Unique ID: `exp_YYYYMMDD_HHMMSS` |
| `timestamp` | ISO 8601 UTC timestamp |
| `dataset_version` | Dataset snapshot identifier (e.g., `nielsen_v1`) |
| `dataset_split` | Train / validation / test date ranges |
| `models_executed` | List of models run (ARIMA, Prophet, LightGBM, XGBoost, Ridge) |
| `hyperparameters` | Per-model hyperparameter dict |
| `metrics.MAPE` | Mean Absolute Percentage Error on test set |
| `metrics.RMSE` | Root Mean Squared Error |
| `metrics.MAE` | Mean Absolute Error |
| `metrics.directional_accuracy` | % of periods with correct direction of change |
| `metrics.calibration_coverage` | Empirical 90% PI coverage (target ≥ 85%) |
| `runtime.runtime_seconds` | Training + inference time per model |
| `runtime.peak_ram_mb` | Peak RAM per model (tracemalloc) |
| `peak_ram_total_mb` | Pipeline-level peak RAM (≤ 8,192 MB hard constraint) |
| `within_total_ram_budget` | Boolean: `peak_ram_total_mb ≤ 8,192` |
| `consumer_signals_included` | Whether Indeks Danmark features were active (SRQ3 ablation flag) |
| `best_model_by_mape` | Model with lowest MAPE in this experiment |
| `notes` | Free-text experiment context |

---

## 3. Storage structure

```
docs/experiments/
  experiment_registry.json    ← Full structured log of all experiments
  experiment_summary.md       ← Auto-generated human-readable summary
```

### Registry JSON structure

```json
{
  "experiments": [
    {
      "experiment_id": "exp_20260401_143022",
      "timestamp": "2026-04-01T14:30:22+00:00",
      "dataset_version": "nielsen_v1",
      "dataset_split": {
        "train_start": "2023-01-01",
        "train_end": "2025-06-30",
        "validation_end": "2025-09-30",
        "test_end": "2025-12-31"
      },
      "models_executed": ["ARIMA", "Prophet", "LightGBM", "XGBoost", "Ridge"],
      "hyperparameters": {
        "LightGBM": {"params": {"n_estimators": 500, "learning_rate": 0.05}}
      },
      "metrics": {
        "ARIMA":    {"MAPE": 0.221, "RMSE": 23.1},
        "LightGBM": {"MAPE": 0.115, "RMSE": 14.8}
      },
      "runtime": {
        "ARIMA":    {"runtime_seconds": 12.4, "peak_ram_mb": 48.2,  "within_ram_budget": true},
        "LightGBM": {"runtime_seconds": 31.7, "peak_ram_mb": 312.5, "within_ram_budget": true}
      },
      "peak_ram_total_mb": 1840.0,
      "within_total_ram_budget": true,
      "consumer_signals_included": false,
      "best_model_by_mape": "LightGBM",
      "notes": "Baseline run — no consumer signals."
    }
  ]
}
```

---

## 4. Integration with the agent workflow

The Experiment Tracking Agent sits between the Forecasting Agent and the Validation Agent:

```
┌──────────────────────────────────────────────────┐
│              AI Research Framework               │
│                   (System A)                     │
│                                                  │
│  Forecasting Agent                               │
│    produces: Dict[str, ModelForecast]            │
│              (in ResearchState)                  │
└───────────────────────┬──────────────────────────┘
                        │  model_forecasts passed to
                        ▼
┌──────────────────────────────────────────────────┐
│           Experiment Tracking Agent              │
│                   (System B)                     │
│                                                  │
│  ExperimentTrackingAgent.track(                  │
│      model_forecasts,                            │
│      dataset_version,                            │
│      consumer_signals_included                   │
│  )                                               │
│  → appends to experiment_registry.json           │
│  → regenerates experiment_summary.md             │
│  → returns ExperimentRecord                      │
└───────────────────────┬──────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────┐
│              AI Research Framework               │
│                                                  │
│  Validation Agent reads ResearchState            │
│  (Experiment Tracking does NOT modify state)     │
└──────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────┐
│           Downstream (System B)                  │
│                                                  │
│  Visualization Agent                             │
│    reads: ExperimentTrackingAgent                │
│              .get_latest_experiment()            │
│                                                  │
│  Tables Agent                                    │
│    reads: ExperimentTrackingAgent                │
│              .get_all_experiments()              │
└──────────────────────────────────────────────────┘
```

### How to call the agent after a forecasting run

```python
from thesis_production_system.agents import ExperimentTrackingAgent

tracker = ExperimentTrackingAgent()

# model_forecasts comes from ResearchState after ForecastingAgent.run()
record = tracker.track(
    model_forecasts=state["model_forecasts"],
    dataset_version="nielsen_v1",
    dataset_split={
        "train_start": "2023-01-01",
        "train_end": "2025-06-30",
        "validation_end": "2025-09-30",
        "test_end": "2025-12-31",
    },
    consumer_signals_included=False,
    notes="SRQ1 baseline — no Indeks Danmark features.",
)

print(f"Tracked experiment: {record.experiment_id}")
print(f"Best model: {record.best_model_by_mape}")
```

### How Visualization / Tables agents read experiment data

```python
tracker = ExperimentTrackingAgent()

# Latest experiment (for current-session figures)
latest = tracker.get_latest_experiment()

# All experiments (for cross-run comparison tables)
all_experiments = tracker.get_all_experiments()

# Best model across all runs
best = tracker.get_best_model_across_experiments()
```

---

## 5. How reproducibility is ensured

| Reproducibility requirement | How it is met |
|---|---|
| Which models were run | `models_executed` list stored per experiment |
| Which hyperparameters were used | `hyperparameters` dict stored per model |
| Which metrics were obtained | `metrics` dict with MAPE, RMSE, MAE, directional accuracy, calibration |
| Which data was used | `dataset_version` + `dataset_split` date ranges |
| What the compute footprint was | `runtime` dict with seconds and peak RAM per model |
| Whether RAM constraint was met | `within_total_ram_budget` boolean (8 GB check) |
| Whether consumer signals were active | `consumer_signals_included` flag (SRQ3 ablation) |
| When the experiment ran | ISO 8601 UTC `timestamp` |

Given the experiment ID, any result in the thesis can be traced to a specific registry entry. The combination of dataset version + split + hyperparameters is sufficient to fully reconstruct any experiment.

---

## 6. SRQ3 ablation support

The `consumer_signals_included` flag enables the SRQ3 ablation comparison:

| Experiment | `consumer_signals_included` | Purpose |
|---|---|---|
| `exp_baseline` | `false` | SRQ1 baseline — pure ML models |
| `exp_with_indeks` | `true` | SRQ3 — models + Indeks Danmark features |

The difference in MAPE between these two experiment types directly answers SRQ3.

---

## 7. Summary auto-update

After every `tracker.track()` call, `experiment_summary.md` is regenerated. It always reflects the current state of the registry. Content includes:

- Registry statistics (total experiments, latest ID)
- Per-model metrics table for the most recent experiment
- All-time best model ranking (sorted by avg MAPE)
- RAM compliance status for the latest run
- Experiment notes
