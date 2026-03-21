# System Architecture Report
> Multi-Agent AI Framework — Manifold Thesis Project
> Generated: 2026-03-15
> Status: Living document — update after every architectural change

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Agent Inventory](#2-agent-inventory)
3. [Agent Responsibilities](#3-agent-responsibilities)
4. [Workflow Pipelines](#4-workflow-pipelines)
5. [Data Flow Between Agents](#5-data-flow-between-agents)
6. [Directory Structure](#6-directory-structure)
7. [Architecture Diagrams](#7-architecture-diagrams)
8. [Agent Interaction Graph](#8-agent-interaction-graph)
9. [Implementation Status](#9-implementation-status)
10. [Final Summary](#10-final-summary)

---

## 1. System Overview

This repository contains **two completely separate multi-agent systems** with distinct purposes, technologies, and responsibilities. They must never be confused.

---

### System A — AI Research Framework

**Directory**: `/ai_research_framework/`

**Purpose**: The experimental multi-agent forecasting architecture that is the *object of study* in the thesis. This system is designed, implemented, benchmarked, and evaluated to answer the four research questions (SRQ1–SRQ4).

**What it does**: Takes Nielsen CSD retail sales data and Indeks Danmark consumer survey data, runs five lightweight ML forecasting models sequentially, aggregates their outputs into a calibrated ensemble, and generates a natural language recommendation via the Claude API.

**Hard constraint**: Total pipeline RAM ≤ 8 GB. Every architectural decision in System A is justified against this constraint.

**Technology stack**:
- Orchestration: LangGraph `StateGraph`
- Agent definitions: PydanticAI
- State object: `ResearchState` (LangGraph `TypedDict`)
- LLM: Claude API (`claude-sonnet-4-6`) — no local model
- ML models: ARIMA, Prophet, LightGBM, XGBoost, Ridge

**Appears in thesis**: Yes — Chapters 5 (Framework Design), 6 (Model Benchmark), 7 (Synthesis), 8 (Evaluation) describe and evaluate this system.

---

### System B — Thesis Production System

**Directory**: `/thesis_production_system/`

**Purpose**: Internal tooling that assists in *writing, managing, and validating* the thesis. This system is not the research contribution — it is invisible to thesis readers.

**What it does**: Plans tasks, drafts chapter bullet points, checks CBS compliance, generates figures, tracks experiments, and manages the literature corpus.

**Technology stack**:
- State object: `ThesisState` (Pydantic `BaseModel`)
- Persistence: JSON (`docs/tasks/thesis_state.json`) + Markdown files
- LLM: Claude Code (interactive) + Claude API (when agents call it)
- Figure generation: Graphviz + Matplotlib

**Appears in thesis**: No — this is production scaffolding only.

---

### How the two systems interact

System A produces results (model forecasts, synthesis outputs, validation reports). System B observes those results and captures them:

```
System A                              System B
─────────────────────────────────     ──────────────────────────────
ForecastingAgent  ──────────────────► ExperimentTrackingAgent
  produces: Dict[str, ModelForecast]    captures: metrics, RAM, runtime
                                        writes: experiment_registry.json

ValidationAgent   ──────────────────► WritingAgent
  produces: ValidationReport            uses: results to draft Ch.8 bullets

SynthesisAgent    ──────────────────► DiagramAgent
  produces: SynthesisOutput            uses: architecture to generate figures
```

**Critical rule**: System B agents observe and document System A outputs. They do **not** modify forecasting logic, synthesis logic, or evaluation criteria.

---

## 2. Agent Inventory

### System A — AI Research Framework

| # | Agent | File | Purpose | Inputs | Outputs |
|---|---|---|---|---|---|
| A1 | **Data Assessment Agent** | `agents/data_assessment_agent.py` | Load, validate, and profile Nielsen + Indeks Danmark datasets; engineer feature matrix | Nielsen SQL/CSV, Indeks Danmark CSV | Feature matrix, consumer signals, data quality report (Markdown) |
| A2 | **Forecasting Agent** | `agents/forecasting_agent.py` | Train 5 ML models sequentially; profile RAM and latency; calibrate prediction intervals | Feature matrix from `ResearchState` | 5 × `ModelForecast` (point, lower/upper 90%, MAPE, RAM, latency) |
| A3 | **Synthesis Agent** | `agents/synthesis_agent.py` | Aggregate forecasts + consumer signals into a calibrated confidence score + LLM recommendation | `Dict[str, ModelForecast]`, consumer signals | `SynthesisOutput` (ensemble forecast, confidence score, recommendation text) |
| A4 | **Validation Agent** | `agents/validation_agent.py` | Run 3-level evaluation: ML accuracy, recommendation quality, agent behaviour | All `ResearchState` outputs | `ValidationReport` (MAPE/RMSE/calibration, LLM-as-Judge scores, RAM/latency) |
| A5 | **Research Coordinator** | `core/coordinator.py` | Orchestrate A1–A4 as a LangGraph `StateGraph`; enforce phase transitions and human approval gates | `ResearchState` (initial) | Final `ResearchState` (complete) |

---

### System B — Thesis Production System

| # | Agent | File | Purpose | Inputs | Outputs |
|---|---|---|---|---|---|
| B1 | **Thesis Coordinator** | `core/coordinator.py` | Orchestrate all System B agents using Plan → Execute → Critic loop | `ThesisState` | Updated `ThesisState` + session log |
| B2 | **Planner Agent** | `agents/planner_agent.py` | Read state + context files → produce prioritised `TaskPlan` (JSON) | `ThesisState`, `docs/context.md`, `scraping_log.md` | `TaskPlan` (list of `Task` objects with agent, action, priority, rationale) |
| B3 | **Critic Agent** | `agents/critic_agent.py` | Validate outputs from execution agents before state update | Agent output + context | `CriticResult` (status, issues, confidence, suggestions) |
| B4 | **Literature Agent** | `agents/literature_agent.py` | Manage paper corpus: scraping, annotation, confirmation, gap analysis updates | RQ definitions, current corpus | Updated `scraping_log.md`, `gap_analysis.md`, confirmed `PaperRecord` objects |
| B5 | **Writing Agent** | `agents/writing_agent.py` | Generate bullet-point skeletons for thesis sections (never prose) | Chapter ID, `ThesisState` | `.md` bullet files in `docs/thesis/sections/` |
| B6 | **Compliance Agent** | `agents/compliance_agent.py` | Validate thesis content against CBS formal requirements | Chapter `.md` files | `ComplianceCheck` records; updated `ComplianceState` |
| B7 | **Diagram Agent** | `agents/diagram_agent.py` | Generate reproducible code-based thesis figures (Graphviz + Matplotlib) | Figure IDs, `ThesisState` | SVG + PNG files in `docs/thesis/figures/` |
| B8 | **Experiment Tracking Agent** | `agents/experiment_tracking_agent.py` | Capture forecasting experiment metadata; maintain experiment registry; generate summary | `Dict[str, ModelForecast]` from System A | `experiment_registry.json`, `experiment_summary.md`, `ExperimentRecord` |
| B9 | **Results Visualization Agent** | *(planned)* | Generate figures from experiment registry data | `experiment_registry.json` | Figures in `docs/thesis/figures/` |
| B10 | **Results Tables Agent** | *(planned)* | Generate formatted comparison tables from experiment registry | `experiment_registry.json` | Markdown tables for thesis sections |

> **B9 and B10** are defined in the workflow and referenced in the Experiment Tracking Agent's interface (`get_latest_experiment()`, `get_all_experiments()`), but not yet implemented. Their interface contract is established.

---

## 3. Agent Responsibilities

### A1 — Data Assessment Agent

The entry point of the research pipeline. Responsible for two datasets:

**Nielsen CSD** (primary): Star-schema SQL database with 4 tables (`csd_clean_dim_market_v`, `csd_clean_dim_period_v`, `csd_clean_dim_product_v`, `csd_clean_facts_v`), ~36 monthly periods, 28 Danish retailers, Carbonated Soft Drinks category. Access not yet confirmed — agent raises `RuntimeError` until `NielsenConfig.access_confirmed = True`.

**Indeks Danmark** (secondary): 3 CSV files — main data (20,134 respondents × 6,364 variables, ~970 MB), codebook, metadata. CSVs must be downloaded locally before the agent can run.

Feature engineering output (used by all 5 ML models):
- Lag features: t-1, t-2, t-4, t-8, t-52
- Rolling statistics: 4-, 8-, 13-week rolling mean/std
- Calendar: week-of-year, month, quarter, Danish holidays
- Promotional flags: price discount, display/feature
- Consumer demand indices (SRQ3): PCA + k-means on Indeks Danmark → retailer-level demand index

After running, the agent explicitly releases raw dataset references (`nielsen_data = None`, `indeks_data = None`) via `unload()` to free RAM before the Forecasting Agent loads models.

---

### A2 — Forecasting Agent

Implements the sequential model execution protocol — the core RAM management strategy of the research framework:

```
For each model in [ARIMA, Prophet, LightGBM, XGBoost, Ridge]:
    1. load_model()           ← instantiate model object
    2. fit_and_predict()      ← train on train set, predict on test set
    3. calibrate_intervals()  ← Kuleshov et al. (ICML 2018) isotonic regression
    4. del model              ← explicit release
    5. gc.collect()           ← force garbage collection
    6. record peak_ram_mb     ← tracemalloc measurement
```

Per-model RAM budget: ≤ 512 MB. Models are never loaded concurrently. This keeps peak pipeline RAM within the 8 GB constraint even when the feature matrix is large.

Hyperparameter optimisation: Optuna Bayesian search, ≤ 50 trials per model, to stay within time and RAM budget.

The agent produces `ModelForecast` dataclasses — one per model — which are the primary input to both the Synthesis Agent and the Experiment Tracking Agent.

---

### A3 — Synthesis Agent

Implements a 5-step MCDM-style synthesis pipeline (answers SRQ2):

**Step 1 — Inverse-MAPE weighted ensemble**
Weight each model's forecast by `1/MAPE_validation`. Models with lower validation error contribute more to the ensemble. Produces a single weighted point forecast and weighted lower/upper bounds.

**Step 2 — Calibrated interval**
Apply post-hoc isotonic regression calibration (Kuleshov et al., 2018) to the ensemble prediction interval. Target: ≥ 85% empirical coverage of stated 90% intervals.

**Step 3 — Consumer signal adjustment**
Compare the Indeks Danmark-derived consumer demand index direction with the model forecast direction. Classify as `aligned`, `divergent`, or `neutral`. Aligned signals boost confidence; divergent signals add a penalty and flag uncertainty.

**Step 4 — Composite confidence score**
```
score = 0.40 × interval_width_score
      + 0.30 × inter_model_agreement_score
      + 0.30 × consumer_signal_score
```
Maps to three tiers: High (≥ 70), Moderate (40–69), Low (< 40).

**Step 5 — LLM recommendation**
Calls `claude-sonnet-4-6` via the Anthropic API at `temperature=0` with a structured prompt containing the ensemble forecast, confidence score, and consumer signal summary. Returns a 2–3 sentence natural language recommendation.

RAM footprint: < 50 MB (API call only — no local model loaded).

---

### A4 — Validation Agent

Three-level evaluation framework (the thesis's methodological contribution to AI artefact evaluation):

**Level 1 — ML accuracy** (SRQ1)
- MAPE, RMSE, MAE on hold-out test set per model
- Diebold-Mariano test for statistical significance of pairwise differences
- SRQ3 ablation: MAPE with vs. without Indeks Danmark features
- Directional accuracy: % of periods with correct direction of change

**Level 2 — Recommendation quality** (SRQ2)
- LLM-as-Judge: GPT-4o evaluates N=50 sampled recommendations on 5 Likert-scale dimensions (accuracy, calibration, actionability, relevance, clarity)
- Calibration coverage: empirical vs. stated 90% PI across the test set
- Human baseline comparison (SRQ4): AI recommendation vs. human analyst using current descriptive BI tool

**Level 3 — Agent behaviour** (SRQ1 + SRQ2)
- Peak RAM from tracemalloc measurements collected at each pipeline stage
- End-to-end latency (training vs. inference)
- Failure mode testing: API timeout, memory pressure, missing data

---

### A5 — Research Coordinator

LangGraph `StateGraph` with:
- **4 nodes**: `data_assessment`, `forecasting`, `synthesis`, `validation`
- **Conditional edges**: routing on errors, phase completion, and `requires_human_approval`
- **`interrupt_before`**: `["forecasting", "validation"]` — graph pauses and yields to the user before these phases
- **Checkpointing**: `MemorySaver` persists `ResearchState` across invocations for human-in-the-loop resumption

---

### B1 — Thesis Coordinator

Orchestrates System B using a `Plan → Execute → Critic` loop:

1. Load `ThesisState` from `docs/tasks/thesis_state.json`
2. `PlannerAgent.run(state)` → `TaskPlan`
3. For each `Task` in the plan:
   - Dispatch to the appropriate agent via `_dispatch()`
   - Collect output
   - `CriticAgent.validate(agent, action, output)` → `CriticResult`
   - If valid: update state; if invalid: retry once with critic issues injected into `task.context`
   - If still invalid after retry: log and skip
4. `state.save()` → `docs/tasks/thesis_state.json`

The Coordinator does not implement business logic — it only routes and orchestrates.

---

### B2 — Planner Agent

Analyses `ThesisState` + project context files and applies 5 prioritised rules to generate a `TaskPlan`:

| Priority | Rule | Trigger |
|---|---|---|
| 1 | Confirm pending papers | Papers in corpus with `confirmed = False` |
| 2 | Draft section bullets | Sections with `status = "not_started"` |
| 3 | Run compliance check | Sections with `status = "bullets_approved"` and `compliance_checked = False` |
| 4 | Generate missing figures | Required figure IDs absent from `state.figures` |
| 5 | Run literature scraping | `scraping_runs_completed = 0` |

Output is a `TaskPlan` (JSON-serialisable Pydantic model) — the Planner does not execute anything.

---

### B3 — Critic Agent

Validates agent outputs using per-agent rule sets before `ThesisCoordinator` accepts them. Each agent+action pair has a dedicated validator:

| Evaluated agent | Action | Key checks |
|---|---|---|
| WritingAgent | draft_section_bullets | No prose lines (> 150 chars, not a bullet); citation placeholders present; SRQ reference present |
| LiteratureAgent | update_gap_analysis | Required headers; SRQ references |
| ComplianceAgent | check_section_compliance | Required compliance fields in output |
| DiagramAgent | generate_figures | SVG + PNG files exist on disk for all requested figure IDs |
| LiteratureAgent | run_scraping | TIER A/B tables present; relevance scores present |

Returns `CriticResult` with `status`, `issues`, `confidence` (0–1), and `suggestions` for retry.

---

### B4 — Literature Agent

Manages the complete lifecycle of the literature corpus:
- **`run_scraping`**: queries arXiv, Semantic Scholar, Google Scholar, ACM, ScienceDirect, Springer across 6 research angles (18 queries total per run); appends proposed additions to `scraping_log.md` with relevance scores. Never adds to corpus without human confirmation.
- **`confirm_papers`**: moves papers from pending → confirmed in `ThesisState`; updates `scraping_log.md` Confirmed Additions table.
- **`update_gap_analysis`**: revises `docs/literature/gap_analysis.md` based on newly confirmed paper annotations.

Current status: Run 1 completed (2026-03-14). 6 Tier A papers + 10 Tier B papers proposed. All 6 Tier A papers annotated in `docs/literature/papers/`. Awaiting human confirmation to move to corpus.

---

### B5 — Writing Agent

Produces **bullet points only** — never prose. This is a mandatory rule enforced by both the agent and the Critic.

- Reads existing chapter files to avoid overwriting completed work
- Updates `SectionState.status` to `"bullets_draft"` for each new chapter
- Status `"bullets_approved"` requires explicit human approval (set manually or via Coordinator)
- Prose is written by the student after human approval of bullet points

All 10 thesis chapters (Ch.1–Ch.10 + frontpage) already have skeleton files. Ch.4 (Data Assessment) is the only chapter without a skeleton — the Writing Agent has a template for it.

---

### B6 — Compliance Agent

Validates thesis content against CBS formal requirements:
- **APA 7 citations**: checks for citation placeholders or APA in-text format
- **Mandatory sub-sections**: enforces required sections per chapter (e.g., philosophy of science in Ch.3, threats to validity in Ch.8)
- **Bullet-only check**: flags lines > 150 characters that are not bullet points
- **Page count**: tracks cumulative character count; estimates standard pages (CBS formula: chars excl. spaces ÷ 2,275); warns if approaching 120-page limit

Key CBS constants: 120 standard pages (2-student group), 2,275 chars/page, APA 7, font ≥ 11pt, margins 3 cm top/bottom 2 cm left/right.

---

### B7 — Diagram Agent

Generates all thesis figures as **reproducible, code-generated artefacts** using Graphviz (structural diagrams) and Matplotlib (charts). All figures trace back to a Python function in `diagram_agent.py`.

| Figure ID | Type | Tool | Content |
|---|---|---|---|
| `system_architecture_v1` | Architecture | Graphviz | Full multi-agent framework: Coordinator + 4 agents + ResearchState + RAM constraint |
| `agent_workflow_v1` | Workflow | Graphviz | LangGraph state machine with human approval gates |
| `data_flow_v1` | Data flow | Graphviz | Nielsen + Indeks → features → 5 models → synthesis → recommendation |
| `model_performance_v1` | Bar chart | Matplotlib | MAPE comparison across 5 models (placeholder → real data post-benchmark) |
| `evaluation_plot_v1` | Multi-panel | Matplotlib | 3-level evaluation results: ML accuracy + recommendation quality + RAM |

Output: SVG (vector, for thesis PDF) + PNG (raster, for preview), saved to `docs/thesis/figures/`.

---

### B8 — Experiment Tracking Agent

Captures metadata from every System A forecasting experiment and persists it to `docs/experiments/experiment_registry.json`.

**What it tracks per experiment**:
- `experiment_id`, `timestamp`, `dataset_version`, `dataset_split`
- `models_executed`, `hyperparameters` (per model)
- `metrics`: MAPE, RMSE, MAE, directional accuracy, calibration coverage (per model)
- `runtime`: seconds, peak RAM MB, within-budget flag (per model)
- `peak_ram_total_mb`, `within_total_ram_budget` (8 GB check)
- `consumer_signals_included` (SRQ3 ablation flag)
- `best_model_by_mape` (auto-computed)

After every `track()` call, the agent regenerates `experiment_summary.md` with the latest results, all-time best model ranking, and RAM compliance status.

**Interface for downstream agents**:
```python
tracker = ExperimentTrackingAgent()
latest = tracker.get_latest_experiment()      # → Dict (for Visualization Agent)
all_exp = tracker.get_all_experiments()       # → List[Dict] (for Tables Agent)
best = tracker.get_best_model_across_experiments()  # → str
```

---

### B9 — Results Visualization Agent *(planned)*

Will generate experiment-driven figures from `experiment_registry.json` data. Planned figures:
- MAPE progression across experiments (learning curve)
- RAM usage per model across experiments
- Calibration coverage plot

Interface contract already established via `ExperimentTrackingAgent.get_latest_experiment()`.

---

### B10 — Results Tables Agent *(planned)*

Will generate formatted Markdown tables from `experiment_registry.json` for direct inclusion in thesis sections. Planned outputs:
- Model benchmark comparison table (Ch.6)
- SRQ3 ablation table (with vs. without consumer signals)
- 3-level evaluation results table (Ch.8)

---

## 4. Workflow Pipelines

### 4.1 Research Pipeline (System A)

```
Step 1 — Data Assessment
  Input  : Nielsen SQL/CSV + Indeks Danmark CSV (local)
  Agent  : DataAssessmentAgent
  Actions: load datasets → quality checks → feature engineering → PCA/k-means (consumer signals)
  Output : feature_matrix, consumer_signals in ResearchState
  Gate   : requires_human_approval = True
           ↓ Human reviews data quality report and approves before Phase 2

Step 2 — Model Benchmarking
  Input  : feature_matrix from ResearchState
  Agent  : ForecastingAgent
  Actions: for each model in [ARIMA, Prophet, LightGBM, XGBoost, Ridge]:
             load → fit (train set) → predict (test set) → calibrate intervals
             → record MAPE, RMSE, peak_ram_mb, latency → unload → gc.collect()
  Output : Dict[str, ModelForecast] in ResearchState
  Gate   : requires_human_approval = True
           ↓ Human reviews benchmark results before synthesis

Step 3 — Synthesis
  Input  : model_forecasts + consumer_signals from ResearchState
  Agent  : SynthesisAgent
  Actions: ensemble weighting → interval calibration → consumer signal adjustment
           → confidence score → Claude API recommendation
  Output : SynthesisOutput in ResearchState
  Gate   : No pause (validation runs automatically)

Step 4 — Validation
  Input  : Full ResearchState (all prior outputs)
  Agent  : ValidationAgent
  Actions: Level 1 (ML accuracy) → Level 2 (LLM-as-Judge) → Level 3 (RAM/latency)
  Output : ValidationReport in ResearchState
  Gate   : requires_human_approval = True
           ↓ Human reviews validation report → thesis Ch.8 content
```

---

### 4.2 Thesis Production Pipeline (System B)

```
Step 1 — Session Start
  ThesisCoordinator.run_session()
    → ThesisState.load() from docs/tasks/thesis_state.json

Step 2 — Planning
  PlannerAgent.run(state)
    → reads: docs/context.md, scraping_log.md, gap_analysis.md, outline.md
    → applies 5 priority rules
    → returns: TaskPlan (JSON)

Step 3 — Execution loop
  For each Task in TaskPlan:

    [Literature tasks]
      LiteratureAgent.run_scraping()    → scraping_log.md
      LiteratureAgent.confirm_papers()  → corpus update
      LiteratureAgent.update_gap_analysis() → gap_analysis.md

    [Writing tasks]
      WritingAgent.draft_section_bullets() → docs/thesis/sections/{ch}.md
                                             SectionState.status = "bullets_draft"

    [Compliance tasks]
      ComplianceAgent.check_section_compliance() → ComplianceCheck records
                                                   SectionState.compliance_checked = True

    [Diagram tasks]
      DiagramAgent.run(state, figure_ids) → docs/thesis/figures/{id}.svg + .png
                                            FigureState.generated = True

    After each execution:
      CriticAgent.validate(agent, action, output)
        → status = "valid" : state updated
        → status = "invalid": retry once with critic.suggestions injected
                              → still invalid: log + skip

Step 4 — Experiment tracking (triggered after System A forecasting)
  ExperimentTrackingAgent.track(model_forecasts, ...)
    → appends ExperimentRecord to experiment_registry.json
    → regenerates experiment_summary.md
    → returns ExperimentRecord (read by Visualization + Tables agents)

Step 5 — Persist
  state.save() → docs/tasks/thesis_state.json

Step 6 — Human review
  User reviews session outputs
  User sets SectionState.status = "bullets_approved" when satisfied
  User runs ComplianceAgent check before prose writing
```

---

### 4.3 Human Approval Gates

Every phase transition in System A requires explicit human approval. No agent proceeds autonomously through a gate.

```
[System A gates]
After Data Assessment   → human reviews data quality report
After Model Benchmark   → human reviews MAPE/RAM table
After Validation        → human reviews full evaluation report (thesis Ch.8 input)

[System B gates]
After bullet drafts     → human reviews and approves before compliance check
Before any prose        → MANDATORY human approval (Thesis Writing Agent never writes prose without approval)
Before Tier A/B papers  → human confirms which papers enter corpus
```

---

## 5. Data Flow Between Agents

### 5.1 State objects

**System A — `ResearchState` (LangGraph TypedDict)**

```
ResearchState
├── current_phase: str           "data_assessment" | "forecasting" | ...
├── errors: List[str]            accumulated error messages
├── requires_human_approval: bool  halts the LangGraph graph
│
├── nielsen_data: Any            DataFrame (None after unload)
├── indeks_data: Any             DataFrame (None after unload)
├── feature_matrix: Any          ML-ready feature matrix
├── consumer_signals: Dict       retailer → demand index (from Indeks Danmark)
├── data_quality_report: str     Markdown quality report
│
├── model_forecasts: Dict        model_name → ModelForecast
├── current_model_loading: str   tracks which model is in RAM
│
├── synthesis_output: SynthesisOutput
├── validation_report: ValidationReport
│
├── ram_budget_mb: int           8192 (constant)
└── peak_ram_observed_mb: float  running max across all phases
```

Agents write partial dicts — LangGraph merges them into the shared state.

**System B — `ThesisState` (Pydantic BaseModel)**

```
ThesisState
├── literature_state: LiteratureState
│   ├── papers: Dict[str, PaperRecord]   title → paper metadata + confirmed flag
│   ├── gap_analysis_version: str
│   └── scraping_runs_completed: int
│
├── thesis_outline: Dict                  chapter structure
│
├── sections: Dict[str, SectionState]     chapter_id → {status, bullet_file, compliance_checked}
│
├── figures: Dict[str, FigureState]       figure_id → {output_path, generated, format}
│
├── compliance_checks: ComplianceState
│   ├── checks: Dict[str, ComplianceCheck]
│   ├── total_character_count: int
│   └── standard_pages_estimate: float    chars / 2275
│
├── last_task_plan: Dict                  last PlannerAgent output
├── last_critic_result: Dict              last CriticAgent output
└── session_id: str                       YYYYMMDD-HHMMSS
```

Persisted to `docs/tasks/thesis_state.json` after every session.

---

### 5.2 Markdown file outputs

| File | Written by | Read by |
|---|---|---|
| `docs/context.md` | Human (Claude Code session log) | PlannerAgent, LiteratureAgent |
| `docs/architecture.md` | Human (approved design doc) | WritingAgent (Ch.5 input) |
| `docs/literature/gap_analysis.md` | LiteratureAgent | WritingAgent (Ch.2 input) |
| `docs/literature/scraping_log.md` | LiteratureAgent | PlannerAgent, human reviewer |
| `docs/literature/papers/*.md` | LiteratureAgent | WritingAgent (citation input) |
| `docs/literature/rq_evolution.md` | Human / LiteratureAgent | WritingAgent (Ch.1 input) |
| `docs/data/nielsen_assessment.md` | DataAssessmentAgent | WritingAgent (Ch.4 input) |
| `docs/data/indeksdanmark_notes.md` | DataAssessmentAgent | WritingAgent (Ch.4 input) |
| `docs/thesis/sections/ch*.md` | WritingAgent | ComplianceAgent, human |
| `docs/experiments/experiment_summary.md` | ExperimentTrackingAgent | Human, WritingAgent (Ch.6/8) |
| `docs/compliance/cbs_guidelines_notes.md` | Human (extracted from CBS PDFs) | ComplianceAgent |

---

### 5.3 JSON registry

**`docs/experiments/experiment_registry.json`**

Written by: `ExperimentTrackingAgent.track()`
Read by: `ExperimentTrackingAgent.get_latest_experiment()` / `get_all_experiments()` → Visualization Agent, Tables Agent

Structure:
```json
{
  "experiments": [
    {
      "experiment_id":             "exp_YYYYMMDD_HHMMSS",
      "timestamp":                 "ISO 8601 UTC",
      "dataset_version":           "nielsen_v1",
      "models_executed":           ["ARIMA", "Prophet", "LightGBM", "XGBoost", "Ridge"],
      "hyperparameters":           { "model": {"params": {}} },
      "metrics":                   { "model": {"MAPE": 0.115, "RMSE": 14.8} },
      "runtime":                   { "model": {"runtime_seconds": 31.7, "peak_ram_mb": 312.5} },
      "peak_ram_total_mb":         1840.0,
      "within_total_ram_budget":   true,
      "consumer_signals_included": false,
      "best_model_by_mape":        "LightGBM"
    }
  ]
}
```

---

### 5.4 Persistence layer summary

| Data type | Format | Location | Written by | Read by |
|---|---|---|---|---|
| Research state | In-memory TypedDict | LangGraph MemorySaver | All System A agents | All System A agents |
| Thesis state | JSON | `docs/tasks/thesis_state.json` | ThesisCoordinator | ThesisCoordinator, all System B agents |
| Experiment data | JSON | `docs/experiments/experiment_registry.json` | ExperimentTrackingAgent | Visualization, Tables agents |
| Chapter content | Markdown | `docs/thesis/sections/` | WritingAgent | ComplianceAgent, human |
| Paper annotations | Markdown | `docs/literature/papers/` | Human / LiteratureAgent | WritingAgent |
| Figures | SVG + PNG | `docs/thesis/figures/` | DiagramAgent | Thesis PDF compilation |
| Session log | Markdown | `docs/context.md` | Human (Claude Code) | PlannerAgent |
| CBS compliance notes | Markdown | `docs/compliance/cbs_guidelines_notes.md` | Human (extracted from PDFs) | ComplianceAgent |

---

## 6. Directory Structure

```
Thesis Maniflod/
│
├── CLAUDE.md                         ← Coordinator manifest — read at every session start
│
├── ai_research_framework/            ← SYSTEM A: thesis object of study
│   ├── __init__.py
│   ├── config.py                     ← 8GB RAM constraint, 5 models, LLM config, data configs
│   ├── requirements.txt              ← langgraph, pydantic-ai, anthropic, pmdarima, prophet,
│   │                                    lightgbm, xgboost, scikit-learn, pandas, tracemalloc
│   ├── agents/
│   │   ├── data_assessment_agent.py  ← Phase 1: load, validate, feature engineering
│   │   ├── forecasting_agent.py      ← Phase 2: 5 models sequential + RAM profiling
│   │   ├── synthesis_agent.py        ← Phase 3: ensemble → calibration → LLM
│   │   └── validation_agent.py       ← Phase 4: 3-level evaluation
│   ├── state/
│   │   └── research_state.py         ← ResearchState TypedDict + ModelForecast, SynthesisOutput
│   └── core/
│       └── coordinator.py            ← LangGraph StateGraph: nodes, conditional edges, interrupt
│
├── thesis_production_system/         ← SYSTEM B: thesis writing tooling (not research contribution)
│   ├── __init__.py
│   ├── requirements.txt              ← pydantic, graphviz, matplotlib, anthropic
│   ├── agents/
│   │   ├── planner_agent.py          ← reads state → TaskPlan (JSON)
│   │   ├── critic_agent.py           ← validates agent outputs → CriticResult
│   │   ├── literature_agent.py       ← corpus management, scraping, gap analysis
│   │   ├── writing_agent.py          ← bullet point generation (never prose)
│   │   ├── compliance_agent.py       ← CBS formal requirement checks
│   │   ├── diagram_agent.py          ← graphviz + matplotlib figures
│   │   └── experiment_tracking_agent.py ← experiment registry + summary generation
│   ├── state/
│   │   └── thesis_state.py           ← ThesisState Pydantic model (root shared state)
│   └── core/
│       └── coordinator.py            ← Plan → Execute → Critic loop
│
├── docs/                             ← Agent memory + thesis outputs (persistent)
│   ├── context.md                    ← Session log (updated every session)
│   ├── architecture.md               ← Framework architecture (draft → approved)
│   ├── system_architecture_report.md ← This document
│   ├── experiment_tracking_agent.md  ← Experiment Tracking Agent documentation
│   ├── thesis_production_architecture.md ← System B architecture documentation
│   │
│   ├── experiments/
│   │   ├── experiment_registry.json  ← All experiment records (append-only)
│   │   └── experiment_summary.md     ← Auto-generated summary (latest results)
│   │
│   ├── literature/
│   │   ├── gap_analysis.md           ← Identified gaps + novelty claim (v3)
│   │   ├── rq_evolution.md           ← RQ version history (v1 → v2)
│   │   ├── scraping_log.md           ← Literature scraping runs + proposed additions
│   │   └── papers/                   ← 18 annotated paper .md files (12 Tier 1 + 6 Tier A)
│   │
│   ├── data/
│   │   ├── nielsen_assessment.md     ← Nielsen data model + quality notes + access status
│   │   └── indeksdanmark_notes.md    ← Indeks Danmark structure + memory estimate + status
│   │
│   ├── tasks/
│   │   ├── data_assessment.md        ← Phase 1 plan (partially blocked)
│   │   ├── model_benchmark.md        ← Phase 4 results (empty — pending data access)
│   │   ├── synthesis_module.md       ← Phase 5 results (empty — pending Phase 4)
│   │   ├── validation_report.md      ← Phase 6 results (empty — pending Phase 5)
│   │   └── thesis_state.json         ← ThesisState persistence (created at first run)
│   │
│   ├── thesis/
│   │   ├── outline.md                ← Approved 10-chapter structure + locked decisions
│   │   ├── figures/                  ← Diagram Agent outputs (SVG + PNG)
│   │   └── sections/                 ← Chapter bullet point files
│   │       ├── frontpage.md
│   │       ├── ch1_introduction.md
│   │       ├── ch2_literature_review.md
│   │       ├── ch3_methodology.md
│   │       ├── ch5_framework_design.md
│   │       ├── ch6_model_benchmark.md
│   │       ├── ch7_synthesis.md
│   │       ├── ch8_evaluation.md
│   │       ├── ch9_discussion.md
│   │       └── ch10_conclusion.md
│   │
│   └── compliance/
│       ├── cbs_guidelines_notes.md   ← CBS formal requirements (extracted from 9 PDFs)
│       └── compliance_checks/        ← ComplianceAgent section-level check outputs
│
└── Thesis/                           ← Obsidian vault (human knowledge base)
    ├── prometheus_data_model-1.md    ← Nielsen star schema documentation
    ├── indeksdanmark_data_model-1.md ← Indeks Danmark dataset structure
    └── Thesis Guidelines/            ← 9 CBS guideline PDFs
```

---

## 7. Architecture Diagrams

### 7.1 Research Framework Pipeline (System A)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     AI RESEARCH FRAMEWORK (System A)                   │
│                     Hard constraint: ≤ 8 GB RAM total                  │
└─────────────────────────────────────────────────────────────────────────┘

  INPUTS
  ┌──────────────────┐   ┌──────────────────────────┐
  │  Nielsen CSD     │   │  Indeks Danmark           │
  │  SQL/CSV         │   │  CSV (20,134 × 6,364)     │
  │  ~36 periods     │   │  ~970 MB                  │
  │  28 retailers    │   │                           │
  └────────┬─────────┘   └────────────┬─────────────┘
           │                          │
           └──────────────┬───────────┘
                          ▼
  ┌─────────────────────────────────────────────────┐
  │         DATA ASSESSMENT AGENT               [A1] │
  │  Quality checks • Feature engineering           │
  │  PCA + k-means → consumer demand indices        │
  │  RAM: ~1,024 MB (Indeks Danmark dominates)      │
  │  Output: feature_matrix, consumer_signals       │
  └──────────────────────┬──────────────────────────┘
                         │  ◄── HUMAN APPROVAL GATE
                         ▼
  ┌─────────────────────────────────────────────────┐
  │         FORECASTING AGENT                   [A2] │
  │  Sequential model execution:                    │
  │  ┌──────────────────────────────────────────┐   │
  │  │ ARIMA → [unload] → Prophet → [unload]    │   │
  │  │ → LightGBM → [unload] → XGBoost →        │   │
  │  │ [unload] → Ridge → [unload]              │   │
  │  └──────────────────────────────────────────┘   │
  │  tracemalloc profiling at each step             │
  │  RAM per model: ≤ 512 MB                        │
  │  Output: 5 × ModelForecast                      │
  └──────────────────────┬──────────────────────────┘
                         │  ◄── HUMAN APPROVAL GATE
                         ▼
  ┌─────────────────────────────────────────────────┐
  │         SYNTHESIS AGENT                     [A3] │
  │  Step 1: Inverse-MAPE weighted ensemble         │
  │  Step 2: Kuleshov (2018) interval calibration   │
  │  Step 3: Consumer signal assessment             │
  │  Step 4: Composite confidence score (0–100)     │
  │  Step 5: Claude API recommendation (API only)   │
  │  RAM: < 50 MB (no local model)                  │
  │  Output: SynthesisOutput                        │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────┐
  │         VALIDATION AGENT                    [A4] │
  │  Level 1: MAPE/RMSE/MAE + DM test              │
  │           SRQ3 ablation (±consumer signals)     │
  │  Level 2: LLM-as-Judge (GPT-4o) N=50           │
  │           Calibration coverage check            │
  │  Level 3: RAM/latency profiling                 │
  │  Output: ValidationReport                       │
  └──────────────────────┬──────────────────────────┘
                         │  ◄── HUMAN APPROVAL GATE
                         ▼
                      COMPLETE
                   (thesis Ch.6–8 content)
```

---

### 7.2 Thesis Production Pipeline (System B)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   THESIS PRODUCTION SYSTEM (System B)                  │
│                   Internal tooling — not research contribution          │
└─────────────────────────────────────────────────────────────────────────┘

  SESSION START
       │
       ▼
  ┌─────────────────────────────────────────────────┐
  │  ThesisState.load()                             │
  │  ← docs/tasks/thesis_state.json                 │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────┐
  │         PLANNER AGENT                       [B2] │
  │  Reads: ThesisState + docs/context.md           │
  │  Applies 5 priority rules                       │
  │  Output: TaskPlan (JSON)                        │
  └──────────────────────┬──────────────────────────┘
                         │  TaskPlan
                         ▼
  ┌─────────────────────────────────────────────────┐
  │         THESIS COORDINATOR                  [B1] │
  │  For each Task in TaskPlan:                     │
  └──────────┬──────────────────────────────────────┘
             │ dispatches to
    ┌────────┴──────────────────────────────────┐
    │                                           │
    ▼                                           ▼
  Literature tasks                        Thesis tasks
  ┌──────────────────┐          ┌────────────────────────┐
  │ LiteratureAgent  │          │ WritingAgent           │
  │ • run_scraping   │          │ • draft_section_bullets│
  │ • confirm_papers │          │   (bullets only!)      │
  │ • update_gap_    │          └───────────┬────────────┘
  │   analysis       │                      │
  └──────────────────┘          ┌───────────▼────────────┐
                                │ ComplianceAgent        │
  ┌──────────────────┐          │ • CBS checks           │
  │ DiagramAgent     │          │ • page count           │
  │ • gen figures    │          └────────────────────────┘
  │   (graphviz +    │
  │    matplotlib)   │
  └──────────────────┘
             │
             ▼
  ┌─────────────────────────────────────────────────┐
  │         CRITIC AGENT                        [B3] │
  │  Validates each agent output                    │
  │  status="valid"   → update state                │
  │  status="invalid" → retry (max 1 retry)         │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────┐
  │  ThesisState.save()                             │
  │  → docs/tasks/thesis_state.json                 │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼  ◄── HUMAN REVIEW

  EXPERIMENT TRACKING FLOW (triggered after System A forecasting):

  ForecastingAgent (System A)
       │  model_forecasts
       ▼
  ┌─────────────────────────────────────────────────┐
  │  EXPERIMENT TRACKING AGENT                  [B8] │
  │  → experiment_registry.json (append)            │
  │  → experiment_summary.md (regenerate)           │
  └──────────────┬──────────────────┬───────────────┘
                 │                  │
                 ▼                  ▼
    Results Visualization    Results Tables
    Agent (planned) [B9]     Agent (planned) [B10]
```

---

## 8. Agent Interaction Graph

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  FULL SYSTEM INTERACTION GRAPH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [HUMAN USER]
       │  session start / approval / paper confirmation
       ▼
  ┌────────────────────────────────────────────────────┐
  │               THESIS COORDINATOR [B1]              │
  │  Orchestrates System B Plan→Execute→Critic loop    │
  └──────┬──────────────────────────────────┬──────────┘
         │ triggers                         │ accepts/rejects
         ▼                                  ▼
  ┌──────────────┐                  ┌───────────────────┐
  │ PLANNER [B2] │──── TaskPlan ───►│  CRITIC [B3]      │
  └──────────────┘                  │  validates output  │
                                    └────────┬──────────┘
                                             │ CriticResult
         ┌───────────────────────────────────┼───────────────────┐
         │ dispatches tasks to               │                   │
         ▼                                   ▼                   ▼
  ┌──────────────┐          ┌────────────────────┐   ┌────────────────────┐
  │ LITERATURE   │          │ WRITING AGENT [B5] │   │ COMPLIANCE [B6]    │
  │ AGENT [B4]   │          │ bullets only       │   │ CBS checks         │
  │              │          └────────────────────┘   └────────────────────┘
  │ writes:      │
  │ scraping_log │          ┌────────────────────┐   ┌────────────────────┐
  │ gap_analysis │          │ DIAGRAM AGENT [B7] │   │ EXPERIMENT         │
  │ papers/*.md  │          │ graphviz+matplotlib│   │ TRACKING [B8]      │
  └──────────────┘          └────────────────────┘   │                    │
                                                      │ reads: System A   │
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │ model_forecasts   │
                                                      └────────┬───────────┘
  ┌────────────────────────────────────────────────┐           │
  │           RESEARCH COORDINATOR [A5]            │           │
  │           LangGraph StateGraph                 │           │ registry
  └──────┬─────────────┬───────────┬───────┬───────┘           ▼
         │             │           │       │            ┌───────────────────┐
         ▼             ▼           ▼       ▼            │ Visualization [B9]│
  [A1] DATA    [A2] FORECAST  [A3] SYNTH  [A4] VALID   │ Tables [B10]      │
  ASSESSMENT   AGENT          AGENT       AGENT         │ (planned)         │
                                                        └───────────────────┘
       All agents read/write ResearchState (TypedDict)
       Shared via LangGraph MemorySaver (checkpointed)
```

---

## 9. Implementation Status

| Agent | Status | Notes |
|---|---|---|
| A1 — Data Assessment Agent | ⬜ Skeleton | Blocked: Nielsen access TBD, Indeks Danmark not downloaded |
| A2 — Forecasting Agent | ⬜ Skeleton | Blocked: same as A1 |
| A3 — Synthesis Agent | ⬜ Skeleton | `_assess_consumer_signal` blocked; LLM API call implemented |
| A4 — Validation Agent | ⬜ Skeleton | Blocked: pending A1–A3 |
| A5 — Research Coordinator | ✅ Implemented | LangGraph StateGraph with interrupt nodes |
| B1 — Thesis Coordinator | ✅ Implemented | Plan → Execute → Critic loop |
| B2 — Planner Agent | ✅ Implemented | 5 priority rules; JSON TaskPlan |
| B3 — Critic Agent | ✅ Implemented | Per-agent validators; CriticResult schema |
| B4 — Literature Agent | ⬜ Partial | `run_scraping` requires web tools; `confirm_papers` implemented |
| B5 — Writing Agent | ✅ Implemented | Bullet-only generation; Ch.4 template included |
| B6 — Compliance Agent | ✅ Implemented | CBS rules, APA 7, page count, mandatory sections |
| B7 — Diagram Agent | ✅ Implemented | 5 figures (graphviz × 3, matplotlib × 2) |
| B8 — Experiment Tracking Agent | ✅ Implemented | Registry, summary, SRQ3 ablation flag |
| B9 — Results Visualization Agent | 🔴 Not implemented | Interface contract established via B8 |
| B10 — Results Tables Agent | 🔴 Not implemented | Interface contract established via B8 |

**Chapter skeleton status**:

| Chapter | File | Status |
|---|---|---|
| Front page | `frontpage.md` | ✅ Skeleton |
| Ch.1 Introduction | `ch1_introduction.md` | ✅ Skeleton |
| Ch.2 Literature Review | `ch2_literature_review.md` | ✅ Skeleton |
| Ch.3 Methodology | `ch3_methodology.md` | ✅ Skeleton |
| Ch.4 Data Assessment | *(Writing Agent template)* | ⬜ Pending — blocked on data access |
| Ch.5 Framework Design | `ch5_framework_design.md` | ✅ Skeleton |
| Ch.6 Model Benchmark | `ch6_model_benchmark.md` | ✅ Skeleton |
| Ch.7 Synthesis Module | `ch7_synthesis.md` | ✅ Skeleton |
| Ch.8 Evaluation | `ch8_evaluation.md` | ✅ Skeleton |
| Ch.9 Discussion | `ch9_discussion.md` | ✅ Skeleton |
| Ch.10 Conclusion | `ch10_conclusion.md` | ✅ Skeleton |

---

## 10. Final Summary

### Agent count

| System | Implemented | Planned | Total |
|---|---|---|---|
| System A — AI Research Framework | 5 | 0 | **5** |
| System B — Thesis Production System | 8 | 2 | **10** |
| **Total** | **13** | **2** | **15** |

---

### Pipeline count

| Pipeline | Agents involved | Status |
|---|---|---|
| Research pipeline | A1 → A2 → A3 → A4 (orchestrated by A5) | Skeleton — blocked on data |
| Thesis production pipeline | B2 → B1 → B4/B5/B6/B7 → B3 | Active |
| Experiment tracking pipeline | A2 → B8 → B9/B10 | B8 active; B9/B10 planned |

**Total: 3 pipelines**

---

### How the system operates — executive summary

**Before data arrives** (current state): System B is fully operational. The Thesis Coordinator runs planning sessions, the Writing Agent drafts chapter skeletons, the Literature Agent manages the paper corpus, the Compliance Agent validates CBS requirements, and the Diagram Agent generates reproducible figures. The Experiment Tracking Agent is ready to capture results the moment System A produces them.

**When data arrives**: The two blockers are resolved (Nielsen access confirmed, Indeks Danmark CSVs downloaded). System A activates. The Research Coordinator runs the 4-phase pipeline — Data Assessment → Forecasting → Synthesis → Validation — with human approval gates between phases. Each forecasting run is automatically logged by the Experiment Tracking Agent. Results flow into System B: the Writing Agent fills in Chapter 6, 7, and 8 content; the Diagram Agent regenerates figures with real data; the Tables Agent (when implemented) generates the benchmark comparison tables.

**Thesis writing**: Every section passes through: WritingAgent (bullet draft) → human approval → ComplianceAgent (CBS check) → human approval → student prose. The Thesis Writing Agent never writes prose without explicit approval.

**Key design invariants**:
1. System A is the research subject — never modified by System B
2. System A peak RAM ≤ 8 GB at all times (tracemalloc-verified)
3. Sequential model execution: one model in RAM at a time
4. Every phase transition requires human approval
5. Writing Agent produces bullets only — prose requires human sign-off
6. Every experiment is logged and reproducible via the registry
