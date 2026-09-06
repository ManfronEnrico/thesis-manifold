---
name: system-a-and-b-agent-design-FROZEN
description: REFERENCE - Frozen v2-era System A / System B multi-agent designs, moved out of project-overview.md 2026-08-11. Historical record only — not the current approach.
category: reference
applies-to: [historical-reference]
triggers: [questions about the original agent architecture, Ch5 design history]
created: 2026_08_11-16_45
updated: 2026_08_11-16_45
---

# System A & System B — Agent Design (FROZEN)

> **Not current.** Moved verbatim out of `00_thesis_context/thesis-topic/project-overview.md`
> on 2026-08-11 (Brian: *"we dont use these agents anymore. Was the old approach"*).
> Preserved rather than deleted because parts may still inform Ch5, and because System A's
> tool-interface and RAM-budget design remain live commitments elsewhere.
>
> **Live sources instead:**
> - Architecture → `user-docs/architecture/architecture.md`
> - Forecast service → `03_thesis_modelling/model_serving/system_a_forecast/`
> - Conversational system → `03_thesis_modelling/model_serving/system_b_conversational/`
> - Canonical RQs → `01_thesis_research/research-questions/research-questions.md`
>
> **Known staleness in this document:** SRQ4 is described against a "non-agentic" baseline,
> which v4 replaced with a code-as-action LLM comparator; the Validation Agent's
> "LLM-as-Judge (GPT-4o, N=50)" predates the correctness/consistency/replicability metric set.

---

## Two separate multi-agent systems

| | **System A** | **System B** |
|---|---|---|
| **Purpose** | The research contribution — evaluated in the thesis | The writing scaffolding — invisible to thesis readers |
| **What it is** | A forecasting extension for a production agentic decision-support system | A thesis production pipeline |
| **Tech stack** | LangGraph + TypedDict state | Pydantic + custom coordinators |
| **Thesis role** | The artefact being designed, built, and evaluated | The tooling that helps write and validate the thesis |
| **Agents** | 5 agents + Coordinator | 10 agents + Coordinator |

---

## System A — Research Framework
*(The thesis artefact — what is evaluated in Ch. 5–8)*

System A is a LangGraph StateGraph with 4 phase nodes. A single `ResearchState` TypedDict
object flows through all agents — no data is copied, only referenced. Every phase transition
triggers a **human approval gate**.

```
Data Sources → Coordinator → [Phase 1] Data Assessment Agent
                           → [Phase 2] Forecasting Agent  (5 models, sequential)
                           → [Phase 3] Synthesis Agent    (ensemble + LLM tool call)
                           → [Phase 4] Validation Agent   (3-level evaluation)
                           → Decision Output
```

**Agents:**

| Agent | Role | Key output |
|---|---|---|
| **Coordinator** | LangGraph StateGraph orchestrator; phase routing; human approval gates | Phase transitions + state management |
| **Data Assessment Agent** | Loads Nielsen CSD data; validates quality; engineers feature matrix; assesses integration readiness criteria | Feature matrix (~200–300 MB) + readiness assessment |
| **Forecasting Agent** | Runs 5 models **sequentially** (load → fit → predict → del → gc.collect()); profiles RAM with tracemalloc | 5 × ModelForecast {point, lower_90, upper_90, MAPE, RMSE, peak_RAM_MB} |
| **Synthesis Agent** | 4-step pipeline: ensemble weighting → interval calibration → confidence score → structured tool output → Claude API recommendation | SynthesisOutput {forecast, calibrated interval, confidence 0–100, tool_schema, recommendation text} |
| **Validation Agent** | Level 1: ML accuracy (MAPE/RMSE/DM-test); Level 2: LLM-as-Judge (GPT-4o, N=50); Level 3: RAM + latency profile | ValidationReport |

**The 5 forecasting models (sequential execution, ≤ 512 MB each):**

| Model | RAM | Role |
|---|---|---|
| Ridge Regression | ~15 MB | Linear baseline |
| ARIMA | ~20 MB | Statistical time-series baseline |
| Prophet | ~200 MB | Seasonal decomposition model |
| LightGBM | ~300 MB | Primary ML model (expected best MAPE) |
| XGBoost | ~400 MB | ML comparator |

**Confidence score formula:**
```
Score (0–100) = 0.50 × interval_width_score
              + 0.50 × inter_model_agreement
```

**The tool/action interface (SRQ2 artefact):**

The Synthesis Agent exposes forecasting outputs to the LLM layer as a **typed, structured
tool call** — not raw model output. The schema enforces:
- Point forecast + calibrated 90% prediction interval
- Confidence score (0–100)
- Source model attribution
- Traceability metadata (model versions, data window, RAM peak)

This interface is the primary design contribution of SRQ2: a reusable pattern for any
agentic system that needs to consume ML forecast outputs reliably.

> **Still live.** Unlike the agent topology, this interface design remains the SRQ2
> contribution. See `05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md` §6
> for the current call flow.

**RAM budget:**

| Phase | Peak RAM |
|---|---|
| Python + LangGraph state | ~600 MB (always on) |
| Data loading (worst case) | ~2.5 GB additional (freed after feature extraction) |
| Active ML model | ≤ 512 MB (one at a time) |
| Synthesis + LLM API | ~250 MB |
| **Total worst-case peak** | **~3.6 GB — well within 8 GB limit** |

> **Still live.** The ≤ 8 GB constraint remains a Main-RQ commitment.

---

## System B — Thesis Production System
*(The writing scaffolding — not in the thesis)*

System B is the tooling that supports thesis writing. It reads System A outputs and produces
structured artefacts (bullet skeletons, compliance reports, figures, tables), but **never
modifies System A code or data**.

```
ThesisState (Pydantic JSON) → Planner Agent → Coordinator
                                             → Writing Agent      → bullet skeletons
                                             → Compliance Agent   → CBS checks
                                             → Diagram Agent      → figures (SVG/PNG)
                                             → Literature Agent   → corpus management
                                             → Experiment Tracker → experiment registry
                                             → Results Viz Agent  → charts (data-dependent)
                                             → Results Tables     → Markdown tables
                                             → Critic Agent       → validates every output
```

**Agents:**

| Agent | Role |
|---|---|
| **Thesis Coordinator** | Plan → Execute → Critic loop; retries once on invalid output |
| **Planner Agent** | Reads `ThesisState`; produces `TaskPlan` (JSON) with 5 priority rules; does NOT execute |
| **Critic Agent** | Validates every agent output before state update; per-agent validators (e.g. no prose lines >150 chars in bullet skeletons) |
| **Literature Agent** | Manages paper corpus; annotation file tracking; scraping log maintenance |
| **Writing Agent** | Produces **bullet points only** — never prose; stops and requests approval before every section |
| **Compliance Agent** | CBS formal requirement checks: page count (2,275 chars incl. spaces / page), APA 7, abstract, front page, AI declaration |
| **Diagram Agent** | Code-generated figures using graphviz + matplotlib; reproducible SVG + PNG |
| **Experiment Tracking Agent** | Append-only JSON registry of all model benchmark runs; tracks MAPE/RMSE/RAM/latency per experiment |
| **Results Visualization Agent** | MAPE comparison charts, RAM profile, calibration curve, SRQ4 agentic vs. non-agentic comparison chart (data-dependent) |
| **Results Tables Agent** | Markdown tables for Ch. 6 model benchmark, Ch. 8 evaluation, appendix experiment log (data-dependent) |

> Several System B behaviours survive as **Claude Code rules and skills** rather than as
> running agents — bullets-before-prose, CBS compliance checks, APA citation handling. See
> `.claude/rules/` and `.claude/skills/`.

---

## Figures generated for this design

| Figure | File | Shows |
|---|---|---|
| System A architecture | `system_architecture_v1.svg` | Full agent topology, data sources, Claude API satellite |
| LangGraph workflow | `agent_workflow_v1.svg` | Execution flow with human approval gates and sequential model sub-cluster |
| Data flow | `data_flow_v1.svg` | ResearchState data transformations across all 4 phases |
| RAM budget | `ram_budget_v1.svg` | Per-component RAM with 8 GB hard-limit line |
| Confidence score | `confidence_score_v1.svg` | Two-component composition of the 0–100 score |
| Tool/action interface | `tool_interface_v1.svg` | Typed schema from Forecasting Agent → LLM synthesis layer |

Figures live under `05_thesis_writing/figures/`. The RAM-budget and tool-interface figures
remain usable; the agent-topology ones depict the frozen design.
