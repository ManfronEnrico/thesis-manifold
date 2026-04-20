# Project Overview — Manifold AI Thesis
> *A Multi-Agent AI Framework for Predictive Decision-Support in FMCG Retail*
> CBS Master's Thesis · Business Administration & Data Science · Deadline 15 May 2026
> Last updated: 2026-03-15

---

## 1. Thesis Topic

### 1.1 The Problem

Business Intelligence systems in SME retail and consumer goods contexts operate at a **descriptive analytics level**: they tell category managers and analysts what *happened* — sales volumes, promotional uplifts, distribution gaps — but not what *will* happen or what to *do*.

**Manifold AI** builds "AI Colleagues" — conversational AI assistants embedded in BI workflows for Danish retailers and consumer goods manufacturers. The current system is descriptive only: it can retrieve and explain historical data, but it cannot forecast, cannot recommend, and cannot communicate uncertainty to the user.

The transition from descriptive to predictive decision-support requires:

1. **Reliable forecasting models** that fit within realistic cloud deployment budgets
2. **Integration of multiple data signals** — sales history and consumer behaviour
3. **Synthesis into actionable, confidence-qualified recommendations**

The core constraint: SME cloud deployments realistically budget **≤ 8 GB RAM** — ruling out large language models used as direct forecasters or deep learning architectures like LSTM.

---

### 1.2 The Research Gap

A review of 26 confirmed academic papers across five research angles identifies **five gaps**, none of which are individually new, but whose intersection has not been addressed:

| # | Gap | Evidence from corpus |
|---|---|---|
| G1 | No multi-agent AI framework combining LLM orchestration + ML ensemble + MCDM synthesis within ≤ 8 GB RAM | All 5 SRQ1 forecasting papers omit RAM as a design variable |
| G2 | No head-to-head benchmark of ARIMA / Prophet / LightGBM / XGBoost / Ridge under an explicit RAM budget in retail CPG | Each paper tests one model family; none enforce a memory ceiling |
| G3 | Consumer survey data (behavioural / attitudinal) has not been used as a demand forecasting enrichment signal in multi-agent systems | Customer segmentation papers exist; multi-agent integration is absent |
| G4 | The descriptive-to-predictive BI transition is discussed conceptually but never empirically evaluated against a defined baseline in real retail CPG | AI-enhanced BI 2025 is survey-based; Design Principles ADR 2024 is a design study |
| G5 | No replicable RAM profiling methodology exists for multi-component AI pipelines combining ML + LLM synthesis | Absent from all 26 confirmed papers |

**Closest paper in the literature**: Bürger & Pauli (2024, EAAI) — *Hybrid AI and LLM-Enabled Agent for Industrial Batch Processes* — an architecturally analogous system applied to dairy CIP process control. The thesis is the retail CPG transposition of this blueprint, under explicit RAM constraints and with consumer survey enrichment.

---

### 1.3 Research Questions

**Main RQ**
> *How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?*

| SRQ | Question | Addressed in |
|---|---|---|
| **SRQ1** | Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints? | Ch. 4 (data), Ch. 6 (benchmark) |
| **SRQ2** | How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations? | Ch. 5 (design), Ch. 7 (synthesis) |
| **SRQ3** | To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems? | Ch. 7 (consumer signals), Ch. 8 (ablation) |
| **SRQ4** | How does the proposed predictive AI system compare to traditional descriptive analytics approaches used in business intelligence systems? | Ch. 8 (evaluation), Ch. 9 (discussion) |

**Methodology**: Design Science Research (Hevner et al., 2004; Peffers et al., 2007) — the thesis produces both an **instantiation** (a working multi-agent system) and a **method-level contribution** (5 generalised design principles reusable beyond this specific retail context).

**Data**:
- *Primary*: Nielsen / Prometheus CSD star schema SQL — 28 Danish retailers, ~36 monthly periods, Carbonated Soft Drinks category
- *Secondary*: Indeks Danmark consumer survey — 20,134 respondents × 6,364 variables — provides consumer demand signals for SRQ3

---

## 2. Agent Framework

The project uses **two completely separate multi-agent systems** with distinct purposes:

| | **System A** | **System B** |
|---|---|---|
| **Purpose** | The research contribution — evaluated in the thesis | The writing scaffolding — invisible to thesis readers |
| **What it is** | A multi-agent predictive analytics framework | A thesis production pipeline |
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
                           → [Phase 3] Synthesis Agent    (ensemble + LLM)
                           → [Phase 4] Validation Agent   (3-level evaluation)
                           → Decision Output
```

**Agents:**

| Agent | Role | Key output |
|---|---|---|
| **Coordinator** | LangGraph StateGraph orchestrator; phase routing; human approval gates | Phase transitions + state management |
| **Data Assessment Agent** | Loads Nielsen + Indeks Danmark; validates quality; engineers feature matrix; runs PCA + k-means for consumer segments | Feature matrix (~200–300 MB) + consumer demand indices |
| **Forecasting Agent** | Runs 5 models **sequentially** (load → fit → predict → del → gc.collect()); profiles RAM with tracemalloc | 5 × ModelForecast {point, lower_90, upper_90, MAPE, RMSE, peak_RAM_MB} |
| **Synthesis Agent** | 5-step pipeline: ensemble weighting → interval calibration → consumer signal adjustment → confidence score → Claude API recommendation | SynthesisOutput {forecast, calibrated interval, confidence 0–100, recommendation text} |
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
Score (0–100) = 0.40 × interval_width_score
              + 0.30 × inter_model_agreement
              + 0.30 × consumer_signal_alignment
```

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
| **Results Visualization Agent** | MAPE comparison charts, RAM profile, calibration curve, SRQ3 ablation chart (data-dependent) |
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
| Confidence score | `confidence_score_v1.svg` | Three-card composition of the 0–100 score |

The combined System A + System B overview figure is at `docs/thesis/figures/project_overview_v1.svg` (see below — generated alongside this document).

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

**SRQ2 — Multi-agent synthesis** *(7 papers)*
| Paper | Key finding |
|---|---|
| Toolformer (NeurIPS 2023) | LLMs learn tool use; tool delegation substitutes for raw parameter scale |
| ART: Multi-Step Reasoning + Tool Use (2023) | Automated multi-step tool calling; structured decomposition |
| LangGraph (LangChain, 2024) | Stateful multi-agent orchestration — the thesis's orchestration framework |
| LLMs in Supply Chain (2025, IFAC) | LLM as interpreter of ML outputs; 78% recommendation actionability |
| Kuleshov et al. — Calibrated Regression (ICML 2018) | Isotonic regression post-hoc calibration; foundational method for confidence intervals |
| Evaluating Calibration in Regression (2023, MDPI Sensors) | Isotonic regression validated as best method across tree ensemble model families |
| ANAH: LLM Hallucination Evaluation (ACL 2024) | Framework for evaluating LLM factual reliability; motivates LLM-as-Judge protocol |

**SRQ3 — Consumer signal enrichment** *(4 papers)*
| Paper | Key finding |
|---|---|
| Customer Segmentation + Sales Prediction (2023, Springer) | Segment-level demand indices improve sales prediction; validates Indeks Danmark approach |
| Consumer Behavior in Supermarket Analytics (2025, C&IE) | ML on consumer attributes measurably improves retail forecasting accuracy |
| Prediction Intervals improve Planning (2010, EJOR) | Interval-expressed forecasts reduce planning cost by 14.2% vs. point-only; justifies calibrated interval output |
| Hybrid AI + LLM Industrial (2024, EAAI) | Closest architectural blueprint; hybrid ML + LLM for CIP process control — the thesis is its retail transposition |

**SRQ4 — Comparison with descriptive BI** *(3 papers)*
| Paper | Key finding |
|---|---|
| AI-Enhanced BI for Decision-Making (2025, Procedia) | 34% higher decision confidence for AI-enhanced vs. descriptive BI |
| Design Principles for AI-augmented Decision Making (2024, EJIS) | DSR study deriving design principles; "uncertainty communication builds trust" |
| Humans vs. LLMs: Judgmental Forecasting (2024, IJF) | LLMs match professional forecasters in structured tasks; thesis frames AI as complement not replacement |

**Reliability + resource constraints** *(3 papers — cross-cutting)*
| Paper | Key finding |
|---|---|
| AgentNoiseBench (2026, arXiv — not peer-reviewed) | Noise robustness in tool-using agents; informs failure mode analysis |
| Edge Intelligence Survey (2024, JEC) | INT8 quantization + knowledge distillation achieves 94–97% accuracy at 3–5× speedup |
| Neuro-Symbolic AI Survey (2025, arXiv) | Classifies the thesis as a data-driven + symbolic reasoning hybrid |

---

### 3.2 Coverage map — gaps vs papers

| Gap | Papers that confirm it | Papers that partially address it |
|---|---|---|
| G1 (RAM-constrained multi-agent) | All 26 papers — none address this intersection | Hybrid AI + LLM Industrial (Bürger 2024) — no RAM budget |
| G2 (Head-to-head model benchmark under RAM) | FMCG ML 2024, Demand Methods 2023, Retail MDPI 2024 | — each tests ≤ 2 model families |
| G3 (Consumer survey enrichment in agents) | Customer Segmentation 2023, Consumer Behavior 2025 | Hybrid CNN-LSTM 2024 uses exogenous variables — not survey data |
| G4 (Descriptive-to-predictive BI transition empirically tested) | AI-enhanced BI 2025 (survey-based, not CPG), Design Principles ADR 2024 (design study) | — no empirical CPG evaluation |
| G5 (RAM profiling methodology) | Absent from all papers | Edge AI Survey provides component-level benchmarks — not pipeline |

---

## 4. Quick Reference

| Item | Value |
|---|---|
| Thesis deadline | 15 May 2026 |
| Page limit | 120 standard pages (2 students; 2,275 chars incl. spaces / page) |
| Primary data | Nielsen CSD SQL — 28 retailers, ~36 months (access pending) |
| Secondary data | Indeks Danmark — 20,134 respondents, 6,364 variables (download pending) |
| RAM hard limit | 8 GB total |
| MAPE target | ≤ 15% (LightGBM expected best; CNN-LSTM SOTA = 4.16% — unconstrained) |
| Calibration target | ≥ 85% empirical coverage of stated 90% prediction intervals |
| LLM used | claude-sonnet-4-6 via API, temperature = 0, ~0 MB local RAM |
| Chapters | 10 + abstract + frontpage — all bullet skeletons complete |
| Papers in corpus | 26 confirmed (Runs 1 + 2); ~20 remaining Tier 1 papers pending Run 3 |
| CBS methodology | Design Science Research (Hevner 2004 + Peffers 2007) — confirm acceptance with supervisor |

---

*For full technical detail: see `docs/system-architecture-report.md`*
*For CBS compliance status: see `docs/compliance/compliance_checks/compliance_report_20260315.md`*
*For literature details: see `docs/literature/gap_analysis.md` and `docs/literature/papers/`*
