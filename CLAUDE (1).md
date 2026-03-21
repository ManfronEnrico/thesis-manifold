# CLAUDE.md — Manifold AI Thesis: Predictive Analytics Framework
> This file is automatically read by Claude Code at every session.
> Do not edit manually — update only through Claude Code.

---

## PROJECT

**Description**: Master's thesis (Business Administration & Data Science) at Copenhagen Business School (CBS), in collaboration with Manifold AI. The project designs, implements, and evaluates a multi-agent framework that transitions Manifold's AI Colleagues system from descriptive analytics to predictive decision-support.

**Objective**: Answer the main research question — *How can an AI agent transition from descriptive analytics to predictive decision-support in a resource-constrained cloud environment (8GB RAM)?* — through an original framework integrating LLM orchestration, lightweight machine learning, and multi-criteria decision synthesis.

**Target users**: Manifold AI internal analysts and their business clients (Danish retailers and consumer goods manufacturers).

**Deadline**: 15 May 2025 — 120-page thesis.

**Hard constraint**: 8GB total RAM. Every architectural decision must be justified against this constraint.

---

## RESEARCH QUESTIONS

**Main RQ**: How can an AI agent transition from descriptive analytics to predictive decision-support in a resource-constrained cloud environment (8GB RAM)?

- **SRQ1**: Which lightweight predictive models can be reliably deployed within an 8GB RAM budget without unacceptable accuracy degradation?
- **SRQ2**: How can a multi-indicator synthesis module aggregate predictions from heterogeneous models into a single, confidence-qualified managerial recommendation?
- **SRQ3**: What performance gains in predictive accuracy and decision quality does the proposed framework deliver relative to the current descriptive baseline? *(pending: Nielsen data access)*

> ⚠️ RQs are still evolving — literature review may lead to refinements. The Literature Review Agent has an explicit mandate to propose adjustments.

---

## STACK

| Layer | Technology |
|---|---|
| Runtime | Local Python + Google Colab |
| Agent framework | PydanticAI + LangGraph |
| Orchestration | LangGraph (multi-agent coordination) |
| ML/Forecasting | TBD (target: ARIMA, Prophet, LightGBM, scikit-learn) |
| Primary data | Nielsen/Prometheus CSD — star schema SQL (access TBD) |
| Secondary data | Indeks Danmark consumer survey (CSV, 20,134 rows, 6,364 variables) |
| Data format | CSV + SQL (connection TBD) |
| Packages | TBD — Claude Code may install autonomously, must document every installation |
| Frontend | None for now |
| Deployment | Local / Google Colab |

**Nielsen Dataset (primary)**:
- Star schema: `csd_clean_dim_market_v`, `csd_clean_dim_period_v`, `csd_clean_dim_product_v`, `csd_clean_facts_v`
- History: ~3 years monthly (~36 periods)
- Scope: Carbonated Soft Drinks (CSD), 28 Danish retailers
- Metrics: `sales_value`, `sales_in_liters`, `sales_units`, promo variants, `weighted_distribution`
- ⚠️ Access modality still to be confirmed with Manifold

---

## CURRENT STATUS

- [x] Indeks Danmark dataset received and documented
- [x] Nielsen/Prometheus dataset documented (data model available)
- [x] Literature review in progress (gap and novelty to be finalised)
- [x] Research questions drafted (to be refined)
- [ ] Nielsen database access (to be confirmed with Manifold)
- [ ] Framework design
- [ ] Agent implementation
- [ ] Validation framework
- [ ] Thesis writing

> Update this section after every working session.

---

## DEFINITION OF DONE

| Task | Completion Criterion |
|---|---|
| Data Assessment | Written report: Nielsen data quality, missing values, forecasting suitability, recommendation on additional data needs |
| Literature Review | Finalised RQs + identified academic gap + novelty documented in `docs/literature/gap_analysis.md` |
| Framework Design | Architecture approved with written brief, agent diagram, justification of choices against 8GB constraint |
| SRQ1 — Model Selection | Benchmark of ≥3 lightweight models with memory profiling, comparative table of accuracy vs memory footprint |
| SRQ2 — Synthesis Module | Working module aggregating outputs from multiple models into a confidence-scored recommendation in natural language |
| SRQ3 — Evaluation | Comparative report: framework vs descriptive baseline on defined metrics (MAPE, decision quality score) |
| Validation Framework | All 3 levels covered: ML accuracy metrics, recommendation quality (LLM-as-judge or human eval), agent behaviour monitoring |
| Thesis Writing | Approved bullet points for every paragraph of every section, before any prose is written |

---

## AGENT ARCHITECTURE (7 agents + Coordinator)

| Agent | Type | SuperClaude Persona | Trigger | Input | Output |
|---|---|---|---|---|---|
| **Coordinator** | Orchestrator | `--persona architect` | Session start / task completion | Other agents' outputs | Next task, instructions, human approval request |
| **Literature Review Agent** | Sub-agent | `--persona analyzer` | Literature review phase / RQ update | PDF papers, current RQs, gap notes | Gap analysis, proposed novelty, updated RQs |
| **Data Assessment Agent** | Sub-agent | `--persona backend-engineer` | Dataset received | CSV/SQL Nielsen, Indeks Danmark | Data quality report, feature engineering suggestions |
| **Forecasting Agent** | Sub-agent | `--persona backend-engineer` | Post data assessment | Clean dataset, candidate model list | Model benchmark, memory profiling, SRQ1 recommendation |
| **Synthesis Agent** | Sub-agent | `--persona architect` | Post forecasting | Multiple model outputs | Managerial recommendation with confidence score (SRQ2) |
| **Validation Agent** | Sub-agent | `--persona analyzer` | Post every implementation phase | All agents' outputs | Validation report across 3 levels: ML accuracy, recommendation quality, agent behaviour |
| **Thesis Writing Agent** | Sub-agent | `--persona documentation-writer` | Phase approval | Approved outputs, CBS guidelines | Bullet points per paragraph (NOT prose — awaits approval before every section) |
| **CBS Compliance Agent** | Sub-agent | `--persona security-engineer` | Thesis content produced | Section drafts, citations, methodology | CBS compliance report: citations, structure, academic methods |

**Core architectural rule**:
- Sub-agents = researchers, planners, analysts — **NEVER direct implementers**
- Coordinator = sole decision-maker on task order
- **Every phase transition requires explicit human approval**

---

## FILE SYSTEM MEMORY

```
docs/
  context.md                    # Updated project context (update after every session)
  architecture.md               # Architectural decisions and justifications
  literature/
    gap_analysis.md             # Identified gaps, proposed novelty
    papers/                     # Annotated relevant papers
    rq_evolution.md             # RQ update history
  data/
    nielsen_assessment.md       # Nielsen data quality report
    indeksdanmark_notes.md      # Notes on Indeks Danmark
  tasks/
    data_assessment.md          # Data assessment plan and output
    model_benchmark.md          # SRQ1 results
    synthesis_module.md         # SRQ2 design and results
    validation_report.md        # SRQ3 and validation framework report
  thesis/
    outline.md                  # Approved thesis structure
    sections/
      [section_name].md         # Approved bullet points per section
  compliance/
    cbs_guidelines_notes.md     # Notes extracted from CBS guidelines
    compliance_checks/          # CBS Compliance Agent reports per section
```

---

## CBS GUIDELINES

The CBS thesis guidelines PDF files are in the project root.
The CBS Compliance Agent must read them at session start and verify every Thesis Writing Agent output against:
- Citation format (APA/CBS standard)
- Chapter and section structure
- Methodological requirements
- Word count and formatting
- Mandatory declarations (plagiarism statement, etc.)

---

## ACTIVE MCP SERVERS

| Server | Function |
|---|---|
| Local file system | Read/write docs/, CSV datasets |
| Python interpreter | ML code execution, data analysis |
| Google Colab (if active) | Notebook execution for heavy benchmarks |

---

## WORKFLOW

```
PHASE 0 — Setup
  → Coordinator reads CLAUDE.md
  → Verifies docs/ structure
  → Shows pre-start checklist
  → Awaits human approval

PHASE 1 — Data Assessment
  → Data Assessment Agent analyses Nielsen + Indeks Danmark
  → Produces: docs/data/nielsen_assessment.md
  → Coordinator presents report → HUMAN APPROVAL

PHASE 2 — Literature Review & Gap Analysis
  → Literature Review Agent researches papers, identifies gaps, proposes novelty
  → Produces: docs/literature/gap_analysis.md + rq_evolution.md
  → CBS Compliance Agent verifies methods and citations
  → Coordinator presents output → HUMAN APPROVAL
  → (Iteration possible until RQs are finalised)

PHASE 3 — Framework Design
  → Coordinator (architect persona) designs architecture
  → Produces: docs/architecture.md
  → Coordinator presents brief → HUMAN APPROVAL

PHASE 4 — SRQ1: Model Selection & Benchmark
  → Forecasting Agent tests lightweight models with memory profiling
  → Produces: docs/tasks/model_benchmark.md
  → Validation Agent validates results (Level 1: ML accuracy)
  → Coordinator presents results → HUMAN APPROVAL

PHASE 5 — SRQ2: Synthesis Module
  → Synthesis Agent designs and implements module
  → Produces: docs/tasks/synthesis_module.md
  → Validation Agent validates (Level 2: recommendation quality)
  → Coordinator presents results → HUMAN APPROVAL

PHASE 6 — SRQ3: Evaluation & Validation Framework
  → Validation Agent runs full evaluation (all 3 levels)
  → Produces: docs/tasks/validation_report.md
  → Coordinator presents report → HUMAN APPROVAL

PHASE 7 — Thesis Writing
  → For every section: Thesis Writing Agent produces BULLET POINTS (not prose)
  → CBS Compliance Agent checks every section
  → HUMAN APPROVAL before every section
  → Only after approval: final prose
```

---

## MANDATORY RULES

- Do not write code before reading this file
- Sub-agents = researchers/planners/analysts ONLY — never direct implementers
- Coordinator = sole decision-maker on task order
- **Every phase transition requires explicit human approval**
- Use `/clear` at every task change
- Use `/compact` when context exceeds 50% of the window
- Use **Opus** for architecture, literature review, and complex decisions
- Use **Sonnet** for standard development, benchmarks, and bullet point writing
- Show a brief before every phase and await approval
- Thesis Writing Agent produces ONLY bullet points — never direct prose
- Stop and request human approval before writing any thesis section
- Every installed package must be documented in `docs/context.md`

---

## EXPLICIT LIMITS

- **DO NOT touch**: Nielsen production database, Indeks Danmark personal data outside the local environment
- **DO NOT export data outside the local environment**: no external uploads of datasets
- **DO NOT install packages without documenting them**: install freely but always log in `docs/context.md`
- **DO NOT proceed autonomously if**:
  - An agent produces output that appears wrong or incomplete → stop, notify, await instructions
  - The Coordinator receives a sub-optimal sub-agent output → return task to agent with more specific instructions, then show result
  - A thesis section is about to be written → STOP, request approval
  - RQs change significantly → STOP, align before proceeding

---

## ERROR PROTOCOL

| Situation | Behaviour |
|---|---|
| Agent produces wrong/non-working output | Notify immediately, show problem with analysis, await instructions |
| Coordinator receives incomplete output from sub-agent | Return task to agent with specific instructions, show result and await confirmation |
| Technical error (code fails, missing dependency) | Notify immediately with error analysis, propose solution, await confirmation before proceeding |
| Nielsen database access fails | Notify, document the problem, propose CSV export workaround |

---

## RISK FLAGS

- 🔴 **High complexity**: 7-agent architecture, multi-indicator synthesis module, 3-level validation framework
- 🔴 **Tight timeline**: 15 May — ~2 months for literature review + implementation + thesis writing
- 🟡 **High uncertainty**: Nielsen database access TBD, RQs still evolving, novelty to be finalised, SQL vs CSV access modality unclear
- 🟡 **External dependency**: Manifold AI must confirm data access and modality
- 🔒 **Security critical**: Nielsen dataset must not leave the local environment; Indeks Danmark contains survey weights
- 💥 **Context overflow risk**: Literature Review Agent over many papers, Thesis Writing Agent over 120 pages — use `/compact` aggressively

---

## PRE-START CHECKLIST

```
[ ] CLAUDE.md read and understood by the Coordinator
[ ] docs/ structure created (context.md, architecture.md, tasks/, literature/, data/, thesis/, compliance/)
[ ] CBS guidelines PDF present in project root
[ ] CBS Compliance Agent has read the guidelines
[ ] Nielsen access modality clarified (direct SQL or CSV export?)
[ ] Current RQs documented in docs/literature/rq_evolution.md
[ ] Human confirmation received before starting Phase 1
```

---

## LAST UPDATED

[Claude Code will populate this field at every session]
