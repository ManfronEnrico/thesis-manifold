# Project Overview — Manifold AI Thesis
> *Extending Production Agentic Decision-Support with Lightweight Forecasting for FMCG Retail*
> CBS Master's Thesis · Business Administration & Data Science · Deadline 15 May 2026
> Last updated: 2026-06-22

---

## 1. Thesis Topic

### 1.1 The Problem

**Manifold AI** builds "AI Colleagues" — production-deployed conversational AI assistants embedded in BI workflows for Danish retailers and consumer goods manufacturers. The current system operates at a **descriptive analytics level**: it retrieves and explains historical data, but it has no native predictive capability. It cannot forecast future demand, cannot issue confidence-qualified recommendations, and cannot communicate uncertainty to the user.

This is not a prototype gap — it is a capability gap in a live, deployed product. The thesis treats Manifold AI's existing agentic system as the empirical anchor: a production-oriented agentic decision-support system that needs to be extended, not replaced.

The extension requires solving three coupled problems:

1. **A predictive substrate**: lightweight forecasting models that fit within realistic SME cloud deployment budgets (≤ 8 GB RAM) and perform reliably on FMCG retail demand data
2. **A reliable interface**: a structured tool/action interface that exposes forecasting outputs to the agent layer with uncertainty, confidence bounds, and traceability intact
3. **Integration readiness**: the architectural and operational conditions under which an existing agentic system can absorb forecast-informed decision-support without redesign

The core constraint: SME cloud deployments realistically budget **≤ 8 GB RAM** — ruling out deep learning architectures like LSTM and large language models used as direct forecasters.

---

### 1.2 The Research Gap

A review of confirmed academic papers across five research angles identifies **five gaps**, whose intersection has not been addressed:

| # | Gap | Evidence from corpus |
|---|---|---|
| G1 | No framework for extending an existing production agentic system with forecasting under ≤ 8 GB RAM | All SRQ1 forecasting papers omit RAM as a design variable; no paper treats extension of a live system |
| G2 | No head-to-head benchmark of ARIMA / Prophet / LightGBM / XGBoost / Ridge under an explicit RAM budget in retail FMCG | Each paper tests one model family; none enforce a memory ceiling or category-specific evaluation |
| G3 | No structured tool/action interface design for exposing ML forecasts — with uncertainty and traceability — to LLM-based agents | Tool-use literature (Toolformer, ART) covers general tool calling; none addresses ML forecast output as a typed, calibrated agent tool |
| G4 | Integration readiness criteria for agentic systems adopting predictive capabilities have not been empirically derived or validated | AI-enhanced BI literature is survey-based; no paper derives readiness criteria from a real deployed system |
| G5 | No replicable RAM profiling methodology exists for multi-component AI pipelines combining ML forecasting + LLM synthesis | Absent from all reviewed papers |

**Closest paper in the literature**: Bürger & Pauli (2024, EAAI) — *Hybrid AI and LLM-Enabled Agent for Industrial Batch Processes* — an architecturally analogous system applied to dairy CIP process control. The thesis is the retail FMCG transposition of this blueprint, under explicit RAM constraints and with a production-extension framing rather than greenfield design.

---

### 1.3 Research Questions

**Main RQ**
> *How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed decision-making under computational and deployment constraints?*

| SRQ | Question | Addressed in |
|---|---|---|
| **SRQ1** | Which lightweight forecasting models provide the best trade-off between accuracy, memory efficiency, and category specialisation for FMCG demand forecasting under computational constraints? | Ch. 4 (data), Ch. 6 (benchmark) |
| **SRQ2** | How can forecasting outputs be exposed to an agentic decision-support system through a structured tool/action interface that preserves reliability, uncertainty, and traceability? | Ch. 5 (design), Ch. 7 (interface design) |
| **SRQ3** | What architectural and operational capabilities are required for a production-oriented agentic system to integrate forecast-informed decision-support? | Ch. 5 (design), Ch. 7 (integration readiness) |
| **SRQ4** | To what extent does an agentic layer over classical forecasting models improve the quality, reliability, and actionability of decision-support outputs compared with non-agentic forecast-based baselines? | Ch. 8 (evaluation), Ch. 9 (discussion) |

**Methodology**: Design Science Research (Hevner et al., 2004; Peffers et al., 2007) — the thesis produces both an **instantiation** (a working extension of a production agentic system) and a **method-level contribution** (generalised integration readiness criteria and interface design principles reusable beyond this retail context).

**Data**:
- *Primary*: Nielsen / Prometheus CSD star schema SQL — 28 Danish retailers, ~36 monthly periods, Carbonated Soft Drinks category
- *Empirical baseline*: Manifold AI's production agentic system — documented architecture and current capability baseline for SRQ3 and SRQ4

---

## 2. Agent Framework

The project uses **two completely separate multi-agent systems** with distinct purposes:

| | **System A** | **System B** |
|---|---|---|
| **Purpose** | The research contribution — evaluated in the thesis | The writing scaffolding — invisible to thesis readers |
| **What it is** | A forecasting extension for a production agentic decision-support system | A thesis production pipeline |
| **Tech stack** | LangGraph + TypedDict state | Pydantic + custom coordinators |
| **Thesis role** | The artefact being designed, built, and evaluated | The tooling that helps write and validate the thesis |
| **Agents** | 5 agents + Coordinator | 10 agents + Coordinator |

---

### 2.1 System A — Research Framework
*(The thesis artefact — what is evaluated in Ch. 5–8)*

System A is a LangGraph StateGraph with 4 phase nodes. A single `ResearchState` TypedDict object flows through all agents — no data is copied, only referenced. Every phase transition triggers a **human approval gate**.

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

The Synthesis Agent exposes forecasting outputs to the LLM layer as a **typed, structured tool call** — not raw model output. The schema enforces:
- Point forecast + calibrated 90% prediction interval
- Confidence score (0–100)
- Source model attribution
- Traceability metadata (model versions, data window, RAM peak)

This interface is the primary design contribution of SRQ2: a reusable pattern for any agentic system that needs to consume ML forecast outputs reliably.

**RAM budget:**

| Phase | Peak RAM |
|---|---|
| Python + LangGraph state | ~600 MB (always on) |
| Data loading (worst case) | ~2.5 GB additional (freed after feature extraction) |
| Active ML model | ≤ 512 MB (one at a time) |
| Synthesis + LLM API | ~250 MB |
| **Total worst-case peak** | **~3.6 GB — well within 8 GB limit** |

---

### 2.2 System B — Thesis Production System
*(The writing scaffolding — not in the thesis)*

System B is the tooling that supports thesis writing. It reads System A outputs and produces structured artefacts (bullet skeletons, compliance reports, figures, tables), but **never modifies System A code or data**.

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

---

### 2.3 Graphical Representation

> Figures are generated by `generate_figures.py` and stored in `docs/thesis/figures/`.

**Figure overview:**

| Figure | File | Shows |
|---|---|---|
| System A architecture | `system_architecture_v1.svg` | Full agent topology, data sources, Claude API satellite |
| LangGraph workflow | `agent_workflow_v1.svg` | Execution flow with human approval gates and sequential model sub-cluster |
| Data flow | `data_flow_v1.svg` | ResearchState data transformations across all 4 phases |
| RAM budget | `ram_budget_v1.svg` | Per-component RAM with 8 GB hard-limit line |
| Confidence score | `confidence_score_v1.svg` | Two-component composition of the 0–100 score |
| Tool/action interface | `tool_interface_v1.svg` | Typed schema from Forecasting Agent → LLM synthesis layer |

The combined System A + System B overview figure is at `docs/thesis/figures/project_overview_v1.svg`.

---

## 3. Literature Overview

**Corpus status**: 26 papers confirmed across 2 scraping runs (2026-03-15).

### 3.1 By research angle

**Methodology — DSR foundations** *(4 papers)*
| Paper | Key role |
|---|---|
| Hevner et al. (2004) — MIS Quarterly | Foundational DSR: 7 guidelines for IS artefact research; frames the thesis as utility-driven design science |
| Peffers et al. (2007) — JMIS | DSRM 6-step process model: problem → objectives → design → demo → evaluate → communicate; structures the thesis phases |
| AI-Based DSR Framework (2024, Springer) | Extends DSR for AI artefacts specifically; evaluation dimensions for AI systems |
| Pathways for Design Research on AI (2024, INFORMS ISR) | Authoritative editorial on DSR pathways for AI; establishes the thesis as IS design-science |
| Artifact Types in IS Design Science (2012, LNCS) | Distinguishes instantiation vs. method-level DSR contributions; justifies thesis dual contribution |

**SRQ1 — Forecasting under constraints** *(5 papers)*
| Paper | Key finding |
|---|---|
| ML-Based Demand Forecasting for FMCG Retailer (2024, Springer) | LightGBM best accuracy/RAM tradeoff; MAPE ≤ 15% as industry benchmark |
| Demand Forecasting Methods in FMCG Retail (2023, Springer) | Tree ensembles outperform statistical models on promotional data |
| Retail ML: Tree Ensembles vs LSTM (2024, MDPI) | Tree ensembles competitive at 10–100× lower RAM than deep learning |
| Hybrid CNN-LSTM for retail (2024, PLOS ONE) | 4.16% MAPE — state-of-the-art deep learning; excluded from thesis on RAM grounds |
| Model Averaging + Double ML (2024, JAE) | Stacking / inverse-weighting improves over single learners; supports ensemble weighting design |

**SRQ2 — Tool/action interface design** *(5 papers)*
| Paper | Key finding |
|---|---|
| Toolformer (NeurIPS 2023) | LLMs learn tool use; tool delegation substitutes for raw parameter scale |
| ART: Multi-Step Reasoning + Tool Use (2023) | Automated multi-step tool calling; structured decomposition |
| LangGraph (LangChain, 2024) | Stateful multi-agent orchestration — the thesis's orchestration framework |
| Kuleshov et al. — Calibrated Regression (ICML 2018) | Isotonic regression post-hoc calibration; foundational method for confidence intervals |
| Evaluating Calibration in Regression (2023, MDPI Sensors) | Isotonic regression validated as best method across tree ensemble model families |

**SRQ3 — Integration readiness** *(4 papers)*
| Paper | Key finding |
|---|---|
| LLMs in Supply Chain (2025, IFAC) | LLM as interpreter of ML outputs; 78% recommendation actionability — evidence that agentic systems can absorb forecast signals |
| Hybrid AI + LLM Industrial (2024, EAAI) | Closest architectural blueprint; hybrid ML + LLM for CIP process control — integration design patterns directly applicable |
| ANAH: LLM Hallucination Evaluation (ACL 2024) | Framework for evaluating LLM factual reliability; motivates traceability requirements in the interface design |
| AgentNoiseBench (2026, arXiv) | Noise robustness in tool-using agents; informs integration failure mode analysis |

**SRQ4 — Agentic vs. non-agentic baseline** *(3 papers)*
| Paper | Key finding |
|---|---|
| AI-Enhanced BI for Decision-Making (2025, Procedia) | 34% higher decision confidence for AI-enhanced vs. descriptive BI |
| Design Principles for AI-augmented Decision Making (2024, EJIS) | DSR study deriving design principles; "uncertainty communication builds trust" |
| Humans vs. LLMs: Judgmental Forecasting (2024, IJF) | LLMs match professional forecasters in structured tasks; thesis frames AI as complement not replacement |

**Reliability + resource constraints** *(2 papers — cross-cutting)*
| Paper | Key finding |
|---|---|
| Edge Intelligence Survey (2024, JEC) | INT8 quantization + knowledge distillation achieves 94–97% accuracy at 3–5× speedup |
| Neuro-Symbolic AI Survey (2025, arXiv) | Classifies the thesis as a data-driven + symbolic reasoning hybrid |

---

### 3.2 Coverage map — gaps vs papers

| Gap | Papers that confirm it | Papers that partially address it |
|---|---|---|
| G1 (RAM-constrained extension of production agentic system) | All reviewed papers — none address extension of a live system under RAM budget | Hybrid AI + LLM Industrial (Bürger 2024) — no RAM budget, no extension framing |
| G2 (Head-to-head model benchmark under RAM + category specialisation) | FMCG ML 2024, Demand Methods 2023, Retail MDPI 2024 | Each tests ≤ 2 model families; none enforce RAM ceiling |
| G3 (Typed tool/action interface for ML forecast → LLM agent) | Toolformer 2023, ART 2023 — cover general tool use | Calibration papers address interval reliability, not interface schema |
| G4 (Integration readiness criteria from production system) | LLMs in Supply Chain 2025, Hybrid AI + LLM Industrial 2024 | Neither derives criteria empirically from a deployed system |
| G5 (RAM profiling methodology for ML + LLM pipelines) | Absent from all papers | Edge AI Survey provides component-level benchmarks — not pipeline |

---

## 4. Quick Reference

| Item | Value |
|---|---|
| Thesis deadline | 15 May 2026 |
| Page limit | 120 standard pages (2 students; 2,275 chars incl. spaces / page) |
| Primary data | Nielsen CSD SQL — 28 retailers, ~36 months |
| Empirical baseline | Manifold AI production agentic system (current capability baseline) |
| RAM hard limit | 8 GB total |
| MAPE target | ≤ 15% (LightGBM expected best; CNN-LSTM SOTA = 4.16% — unconstrained) |
| Calibration target | ≥ 85% empirical coverage of stated 90% prediction intervals |
| LLM used | claude-sonnet-4-6 via API, temperature = 0, ~0 MB local RAM |
| Chapters | 10 + abstract + frontpage |
| Papers in corpus | 26 confirmed (Runs 1 + 2); Run 3 pending (tool/action interface + integration readiness literature) |
| CBS methodology | Design Science Research (Hevner 2004 + Peffers 2007) |

---

*For full technical detail: see `docs/system-architecture-report.md`*
*For CBS compliance status: see `docs/compliance/compliance_checks/compliance_report_20260315.md`*
*For literature details: see `docs/literature/gap_analysis.md` and `docs/literature/papers/`*
