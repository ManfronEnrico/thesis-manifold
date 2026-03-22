# Manifold AI Thesis — Predictive Analytics Framework

> **Master's Thesis** — Business Administration & Data Science
> Copenhagen Business School (CBS), in collaboration with Manifold AI
> **Group thesis** — 2 students — 120 pages — Deadline: 15 May 2026

---

## Research Question

> *How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?*

**Sub-questions:**
- **SRQ1** — Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints (≤8 GB RAM)?
- **SRQ2** — How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations?
- **SRQ3** — To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems?
- **SRQ4** — How does the proposed predictive AI system compare to traditional descriptive analytics approaches used in business intelligence systems?

---

## What This Repository Contains

This repo contains **two separate systems** that must not be confused:

| System | Folder | Purpose | In Thesis? |
|---|---|---|---|
| **System A** — Research Framework | `ai_research_framework/` | The multi-agent forecasting system being studied and evaluated | ✅ Yes — Chapters 5–8 |
| **System B** — Thesis Production | `thesis_production_system/` | Internal tooling for writing and managing the thesis | ❌ No — invisible to reader |

> ⚠️ **System B never modifies System A logic.** System A is the research object; System B supports the writing process.

---

## System A — AI Research Framework

The core research contribution. A multi-agent LLM-orchestrated pipeline that transitions Manifold's AI Colleagues system from descriptive analytics to predictive decision-support.

**Hard constraint: ≤ 8 GB RAM total** — every architectural decision is justified against this.

### Architecture

```
ResearchCoordinator (LangGraph StateGraph)
│
├── A1 — DataAssessmentAgent      →  Data quality report, forecasting suitability
├── A2 — ForecastingAgent         →  Benchmark 5 lightweight models (sequential, memory-profiled)
├── A3 — SynthesisAgent           →  Ensemble + confidence-scored recommendation
└── A4 — ValidationAgent          →  3-level evaluation (ML accuracy, rec. quality, resource usage)
```

### Models Benchmarked (SRQ1)

| Model | Package | Est. RAM |
|---|---|---|
| AutoARIMA | pmdarima | ~50 MB |
| Prophet | prophet | ~200 MB |
| LightGBM | lightgbm | ~100 MB |
| XGBoost | xgboost | ~150 MB |
| Ridge | scikit-learn | ~10 MB |

> Models execute **sequentially** — never in parallel — to stay within the 8 GB budget.

### Data Sources

| Dataset | Format | Status |
|---|---|---|
| Nielsen/Prometheus CSD | SQL star schema (4 tables, ~36 months, 28 retailers) | 🟡 Credentials received — see [setup guide](docs/DATA_ACCESS_SETUP.md) |
| Indeks Danmark | CSV (20,134 respondents × 6,364 variables) | 🔴 Blocked — download pending |

### RAM Budget

| Component | Allocation |
|---|---|
| DataAssessmentAgent | 1,024 MB |
| ForecastingAgent (per model) | 512 MB |
| SynthesisAgent | 200 MB |
| ValidationAgent | 200 MB |
| Coordinator + overhead | 712 MB |
| **Total headroom** | **~2.6 GB** |

---

## System B — Thesis Production System

Internal scaffolding that runs the thesis writing process. **Not described in the thesis.**

### Agents

| Agent | File | Purpose |
|---|---|---|
| ThesisCoordinator | `core/coordinator.py` | Plan → Execute → Critic loop |
| PlannerAgent | `agents/planner_agent.py` | Generates TaskPlan from ThesisState |
| CriticAgent | `agents/critic_agent.py` | Validates all agent outputs |
| LiteratureAgent | `agents/literature_agent.py` | Corpus management, paper scraping |
| WritingAgent | `agents/writing_agent.py` | **Bullet points only** — never prose |
| ComplianceAgent | `agents/compliance_agent.py` | CBS formal requirements checks |
| DiagramAgent | `agents/diagram_agent.py` | Graphviz + Matplotlib figures |
| ExperimentTrackingAgent | `agents/experiment_tracking_agent.py` | Registry + summary |
| ResultsVisualizationAgent | `agents/results_visualization_agent.py` | Data-driven charts |
| ResultsTablesAgent | `agents/results_tables_agent.py` | Markdown tables for thesis |

> **Rule**: WritingAgent produces ONLY bullet points. All prose requires explicit human sign-off.

---

## Project Structure

```
Thesis Maniflod/
├── ai_research_framework/          # SYSTEM A — research contribution
│   ├── config.py                   # RAM budget, model list, LLM config
│   ├── agents/                     # 4 research agents
│   ├── core/coordinator.py         # LangGraph StateGraph orchestrator
│   ├── state/research_state.py     # ResearchState TypedDict
│   └── requirements.txt
│
├── thesis_production_system/       # SYSTEM B — thesis writing tooling
│   ├── agents/                     # 10 production agents
│   │   └── builder/                # Autonomous trial loop (Builder Agent)
│   ├── core/coordinator.py         # Plan→Execute→Critic loop
│   ├── state/thesis_state.py       # ThesisState Pydantic model
│   └── requirements.txt
│
├── docs/
│   ├── context.md                  # Session log
│   ├── architecture.md             # Framework architecture decisions
│   ├── system_architecture_report.md
│   ├── literature/
│   │   ├── gap_analysis.md         # Research gap + novelty (v3)
│   │   ├── rq_evolution.md         # RQ version history
│   │   ├── scraping_log.md         # Literature scraping log
│   │   └── papers/                 # 37 annotated papers
│   ├── data/
│   │   ├── nielsen_assessment.md
│   │   └── indeksdanmark_notes.md
│   ├── tasks/
│   │   ├── thesis_state.json       # ThesisState persistence
│   │   ├── data_assessment.md
│   │   ├── model_benchmark.md
│   │   ├── synthesis_module.md
│   │   └── validation_report.md
│   ├── thesis/
│   │   ├── outline.md              # 10-chapter structure
│   │   ├── sections/               # 11 chapter bullet skeletons
│   │   └── figures/                # SVG + PNG architecture diagrams
│   ├── experiments/
│   │   ├── experiment_registry.json
│   │   └── experiment_summary.md
│   └── compliance/
│       ├── cbs_guidelines_notes.md
│       └── compliance_checks/
│
├── tests/
│   └── test_builder_integration.py
├── results/                        # Experiment outputs
├── generate_figures.py             # Standalone figure generator
├── CLAUDE.md                       # Master project instructions (read by Claude Code)
├── CHEATSHEET.md                   # Quick reference for common commands
└── .gitignore
```

---

## Setup

### Prerequisites

- Python 3.11+
- An **Anthropic API key** (required for all LLM agent calls)

### 1. Clone the repository

```bash
git clone https://github.com/ManfronEnrico/thesis-manifold.git
cd thesis-manifold
```

### 2. Configure credentials

Copy the `.env` template and fill in values (ask your co-author for the Nielsen credentials):

```bash
cp .env.example .env   # then open .env and fill in all values
```

For full instructions including ODBC driver installation on Windows and macOS:
→ **[docs/DATA_ACCESS_SETUP.md](docs/DATA_ACCESS_SETUP.md)**

### 3. Install dependencies

**System A (Research Framework):**
```bash
pip install -r ai_research_framework/requirements.txt
```

**System B (Thesis Production):**
```bash
pip install -r thesis_production_system/requirements.txt
```

> For Prophet on Apple Silicon: `brew install cmake` may be required first.

### 4. Install Claude Code (for AI-assisted development)

```bash
npm install -g @anthropic-ai/claude-code
claude  # run from project root
```

### 5. Generate architecture figures

```bash
pip install graphviz matplotlib
python generate_figures.py
# Output: docs/thesis/figures/*.svg and *.png
```

---

## Running the Research Framework (System A)

> ⚠️ Currently blocked — Nielsen and Indeks Danmark data access is pending.

```python
from ai_research_framework.core.coordinator import build_coordinator
from ai_research_framework.state.research_state import ResearchState

coordinator = build_coordinator()
initial_state: ResearchState = {
    "current_phase": "data_assessment",
    "ram_budget_mb": 8192,
    "errors": [],
    "requires_human_approval": False,
    # ... data inputs added here once access is confirmed
}
result = coordinator.invoke(initial_state)
```

---

## Running Tests

```bash
# Builder Agent integration tests (no API key or data required)
python -m pytest tests/test_builder_integration.py -v

# Run all tests
python -m pytest tests/ -v
```

---

## Workflow Phases

Every phase transition requires **explicit human approval** before proceeding.

```
Phase 0 — Setup & pre-start checklist
Phase 1 — Data Assessment           [BLOCKED — awaiting data access]
Phase 2 — Literature Review & Gap Analysis
Phase 3 — Framework Design
Phase 4 — SRQ1: Model Selection & Benchmark   [BLOCKED — awaiting data]
Phase 5 — SRQ2: Synthesis Module              [BLOCKED — awaiting Phase 4]
Phase 6 — SRQ3/4: Evaluation & Validation     [BLOCKED — awaiting Phase 5]
Phase 7 — Thesis Writing            [bullets only → human approval → prose]
```

---

## Current Status (as of 2026-03-21)

### Completed ✅
- System A skeleton — all 4 research agents + LangGraph coordinator
- System B — all 10 production agents implemented
- Literature review — 37 confirmed papers, gap analysis v3, RQs v2
- CBS compliance checks — all 11 chapters + abstract
- All thesis chapter bullet skeletons (Ch.1–10 + frontpage + abstract)
- Architecture figures — 5 SVG + PNG pairs
- Experiment registry template initialised
- GitHub repository set up with collaborator access

### Blocked 🔴
- Indeks Danmark CSVs — must download from Google Drive

### In Progress 🟡
- Nielsen database — credentials received, connection verified, data exploration in progress
  → See [docs/DATA_ACCESS_SETUP.md](docs/DATA_ACCESS_SETUP.md) for colleague setup
  → Run `python scripts/explore_nielsen.py` to inspect the data

### Pending
- Phase 1–6 implementation (all data-dependent)
- Tier B paper confirmations (10 papers, user decision pending)
- Literature Scraping Run 4 (optional)

---

## Key Documents

| Document | Location | Purpose |
|---|---|---|
| Master instructions | `CLAUDE.md` | Read by Claude Code at every session |
| Quick reference | `CHEATSHEET.md` | Common commands and workflows |
| Session log | `docs/context.md` | What happened in each session |
| Architecture report | `docs/system_architecture_report.md` | Full 10-section technical report |
| Gap analysis | `docs/literature/gap_analysis.md` | Research gap + novelty claim |
| RQ evolution | `docs/literature/rq_evolution.md` | Version history of research questions |
| Thesis outline | `docs/thesis/outline.md` | 10-chapter structure |
| CBS compliance | `docs/compliance/cbs_guidelines_notes.md` | Formal requirements |

---

## CBS Compliance Notes

- **Page limit**: 120 standard pages (group thesis, 2 students)
- **Standard page**: 2,275 characters including spaces
- **Excluded from count**: appendices, bibliography
- **Citation format**: APA 7th edition
- All sections checked against 9 CBS guideline PDFs (stored in `Thesis/Thesis Guidelines/`)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph (System A) + custom coordinator (System B) |
| Agent definitions | PydanticAI |
| LLM | Claude API (`claude-sonnet-4-6`) |
| ML / Forecasting | pmdarima, Prophet, LightGBM, XGBoost, scikit-learn |
| State management | LangGraph TypedDict (System A) + Pydantic BaseModel (System B) |
| Data | Nielsen SQL star schema + Indeks Danmark CSV |
| Figures | Graphviz + Matplotlib |
| Runtime | Local Python 3.11 / Google Colab |

---

## Security Notes

- **Never commit** actual Nielsen or Indeks Danmark data — `.gitignore` enforces this
- `ANTHROPIC_API_KEY` must be set as an environment variable — never hardcoded
- Nielsen dataset must not leave the local environment (confidentiality agreement)
