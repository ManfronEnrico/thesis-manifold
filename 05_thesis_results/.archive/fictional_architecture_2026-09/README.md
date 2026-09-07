# The v1 architecture diagrams — archived 2026-09-06 (P0046 F18)

`system_architecture_v1`, `agent_workflow_v1`, `data_flow_v1`,
`confidence_score_v1`, `project_overview_v1`, plus the generator that made them.

## Why archived rather than corrected

They depicted a system that does not exist. Verified against the live tree:

| Depicted | Reality |
|---|---|
| LangGraph / StateGraph orchestration | **not a dependency**; imported by no live module. The only mention is an aspirational docstring line in `engineer_features.py` |
| "Coordinator", "Agent Layer", 4 named Agents | no such objects anywhere in live code |
| Phase 1→2→3→4 human approval gates | no approval mechanism exists |
| "Consumer Signals: PCA → k-means → segments" | **no PCA or KMeans call anywhere in the repo** |
| ARIMA + Prophet in the model ladder | statistical *baselines* (`srq1_baselines_stat.py`), never ladder members |
| Ridge 15 / ARIMA 20 / Prophet 200 / LightGBM 300 / XGBoost 400 MB | invented. Measured: Ridge 5.4, XGBoost 29.2, LightGBM 38.1 |
| Indeks Danmark as a data source | never used; archived 2026-09-06 |
| LLM-as-Judge validation level | design decided against |
| "System B" thesis-writing agents | abandoned; archived separately |
| 8 GB envelope | 4096 MB (confirmed by Brian) |

Two rounds of label-patching were applied before this call. That was the wrong
approach: **the frame itself was the error**, so correcting labels inside it kept
producing a diagram of a system nobody built. Rebuilt from the code instead.

## What replaced them

`ch4_preprocessing_pipeline_v2`, `ch6_model_selection_v2`, `ch7_scenarios_v2`, `ch6_resource_profile_v2` — three
sequential stages plus a measured resource chart, matching what the repo does:
preprocessing (`run_preprocessing.py`, steps 0-6) → independent model fitting and
persistence → the three-scenario SRQ4 comparison (A plain / B data+code /
C trained model). No orchestrator, because there isn't one.

Every number in the new set is read from an artefact at render time. The
generator exits rather than drawing if a source table is missing.

## If you need one of these back

The old generator is preserved here as
`generate_architecture_diagrams_OLD.py`. It still runs. Do not cite its output
without first checking each claim against the code — that is what this README
exists to warn about.
