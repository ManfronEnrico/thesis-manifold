# CLAUDE.md — Manifold AI Thesis: Predictive Analytics Framework
> This file is automatically read by Claude Code at every session.
> Do not edit manually — update only through Claude Code.

---

## PROJECT

**Description**: Master's thesis (Business Administration & Data Science) at Copenhagen Business School (CBS), in collaboration with Manifold AI. The project designs, implements, and evaluates a multi-agent framework that transitions Manifold's AI Colleagues system from descriptive analytics to predictive decision-support.

**Objective**: Answer the main research question — *How can an AI agent transition from descriptive analytics to predictive decision-support in a resource-constrained cloud environment (8GB RAM)?* — through an original framework integrating LLM orchestration, lightweight machine learning, and multi-criteria decision synthesis.

**Target users**: Manifold AI internal analysts and their business clients (Danish retailers and consumer goods manufacturers).

**Deadline**: 15 May 2026 — 120-page thesis (group, 2 students).

**Hard constraint**: 8GB total RAM. Every architectural decision must be justified against this constraint.

---

## RESEARCH QUESTIONS
> v2 — updated 2026-03-14. Full history in docs/literature/rq_evolution.md

**Main RQ**: How can AI systems be designed to provide reliable predictive decision-support in real-world business environments under computational constraints?

- **SRQ1**: Which predictive modelling approaches provide the best balance between forecasting accuracy and computational efficiency under realistic cloud resource constraints?
- **SRQ2**: How can a multi-agent architecture coordinate predictive models and heterogeneous data signals to generate actionable managerial recommendations?
- **SRQ3**: To what extent does additional contextual information improve the predictive and decision-support capabilities of AI systems?
- **SRQ4**: How does the proposed predictive AI system compare to traditional descriptive analytics approaches used in business intelligence systems?

> ⚠️ RQs are still evolving — Literature Review Agent has an explicit mandate to propose refinements. See docs/literature/rq_evolution.md for open questions.

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

### Completed ✅
- [x] Indeks Danmark dataset documented (data model available; CSVs still on Google Drive — download pending)
- [x] Nielsen/Prometheus data model documented (star schema known; actual data access NOT confirmed)
- [x] Literature review: 40 papers + 6 Tier A confirmed + 10 Tier B proposed; gap analysis v3 complete
- [x] Research questions v2 (4 SRQs) — see docs/literature/rq_evolution.md
- [x] CBS guidelines extracted and compliance notes written
- [x] Group thesis confirmed (2 students, 120 pages, deadline 15 May 2026)
- [x] System A code skeleton (`/ai_research_framework/`) — all 4 research agents + LangGraph coordinator
- [x] System B code (`/thesis_production_system/`) — all 10 production agents implemented (B9, B10 implemented 2026-03-15)
- [x] All 11 thesis chapter bullet skeletons complete (Ch.1–10 + frontpage)
- [x] `docs/tasks/thesis_state.json` initialised
- [x] `docs/experiments/experiment_registry.json` initialised (template)
- [x] `docs/thesis_production_architecture.md` — System A/B separation documented
- [x] `docs/system_architecture_report.md` — full 10-section architecture report
- [x] Ch.1 Introduction prose (21,400 chars) — citation corrected 2026-04-12
- [x] Ch.2 Literature Review prose (50,500 chars, 22 pages) — written 2026-04-12
- [x] Ch.3 Methodology prose (27,300 chars, 12 pages) — written 2026-04-12
- [x] **Nielsen DB connection confirmed** — Microsoft Fabric connector implemented 2026-04-12; all 4 views return data
- [x] `ai_research_framework/data/nielsen_connector.py` — Service Principal auth via pyodbc + azure-identity
- [x] **Indeks Danmark CSVs downloaded** — 2026-04-13; located at `Thesis/indeksdanmark/`; CSD brand + retailer variables identified

### Blocked 🔴
- [ ] **PENDING REVIEW**: Ch.1, Ch.2, Ch.3, Ch.4 prose in `docs/thesis/writing/` — requires human review before `prose_approved`
- [ ] **PENDING**: DSR supervisor confirmation (OI-03) — required for Ch.3 compliance sign-off

### Pending (can proceed now)
- [ ] Ch.4 Data Assessment — Nielsen connection confirmed; can begin data quality assessment
- [ ] Ch.5 Framework Design (14pp) — no data required; can begin immediately
- [ ] Ch.9 Discussion (8pp) — no data required
- [ ] Ch.10 Conclusion (6pp) — no data required
- [ ] NotebookLM verification of 25 Ch.2 citations (pending)

### Data-dependent (now unblocked)
- [ ] Phase 1: Data Assessment (SRQ1–4 precondition) — UNBLOCKED 2026-04-12
- [ ] Phase 4: Model Benchmark (SRQ1) — requires data assessment complete
- [ ] Phase 5: Synthesis Module (SRQ2) — requires Phase 4 complete
- [ ] Phase 6: Evaluation (SRQ3/SRQ4) — requires Phase 5 complete

> Last updated: 2026-04-12

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

## AGENT ARCHITECTURE

> ⚠️ TWO SEPARATE SYSTEMS — do not confuse them.
> Full documentation: `docs/system_architecture_report.md`

### SYSTEM A — AI Research Framework (`/ai_research_framework/`)
*The experimental architecture being evaluated in the thesis. Appears in Chapters 5–8.*

| Agent | File | SRQ | Status |
|---|---|---|---|
| **Research Coordinator** | `core/coordinator.py` | Orchestrator | ✅ LangGraph StateGraph |
| **Data Assessment Agent** | `agents/data_assessment_agent.py` | SRQ1–4 precondition | ⬜ Blocked (no data) |
| **Forecasting Agent** | `agents/forecasting_agent.py` | SRQ1 | ⬜ Blocked (no data) |
| **Synthesis Agent** | `agents/synthesis_agent.py` | SRQ2 | ⬜ Partial (API implemented) |
| **Validation Agent** | `agents/validation_agent.py` | SRQ1–4 | ⬜ Blocked (pending A1–A3) |

**Hard constraint**: ≤ 8 GB RAM. Sequential model execution. LangGraph TypedDict state.

### SYSTEM B — Thesis Production System (`/thesis_production_system/`)
*Internal tooling for writing the thesis. NOT the research contribution. NOT described in the thesis.*

| Agent | File | Purpose | Status |
|---|---|---|---|
| **Thesis Coordinator** | `core/coordinator.py` | Plan→Execute→Critic loop | ✅ |
| **Planner Agent** | `agents/planner_agent.py` | TaskPlan (JSON) from state | ✅ |
| **Critic Agent** | `agents/critic_agent.py` | Validate agent outputs | ✅ |
| **Literature Agent** | `agents/literature_agent.py` | Corpus management, scraping | ✅ Partial |
| **Writing Agent** | `agents/writing_agent.py` | Bullet points only (never prose) | ✅ |
| **Compliance Agent** | `agents/compliance_agent.py` | CBS formal checks | ✅ |
| **Diagram Agent** | `agents/diagram_agent.py` | Graphviz + Matplotlib figures | ✅ |
| **Experiment Tracking Agent** | `agents/experiment_tracking_agent.py` | Registry + summary | ✅ |
| **Results Visualization Agent** | `agents/results_visualization_agent.py` | Data-driven charts | ✅ |
| **Results Tables Agent** | `agents/results_tables_agent.py` | Markdown tables for thesis | ✅ |

#### OutlineAgent (via thesis-structuring skill)

**Skill location**: `.claude/skills/thesis-structuring/`
**Slash command**: `/update-outline`
**Triggered by**: User invocation or PlannerAgent P2 pre-check (see below)

**Role**: Sole agent responsible for `docs/thesis/outline.md`. No other agent writes to this file.
Reads thesis state and context → decides whether outline needs updating → writes updated outline.
Never writes prose or bullet content.

**Reads**:
- `docs/thesis/outline.md`
- `docs/tasks/thesis_state.json`
- `docs/thesis/sections/*.md`
- `.claude/agents/thesis-writer.md` lines 154–169 (page budgets)
- `docs/context.md`

**Writes**:
- `docs/thesis/outline.md`
- `docs/thesis/sections/{chapter_id}.md` stubs only (status: `no_bullets`)

#### APA Citation Agent (via apa-citation skill)

**Skill location**: `.claude/skills/apa-citation/`
**Slash command**: `/cite`
**Triggered by**: User invokes `/cite`, pastes a _REV or _REV-brian note, provides a DOI, or says "cite this" / "add this reference" / "format this in APA"

**Role**: Sole agent responsible for `docs/thesis/references.md`. No other agent writes to this file directly.
Formats APA 7 citations from any input source (Obsidian notes, DOIs, raw data), verifies via NotebookLM, checks for duplicates, and appends to the references list.

**Do NOT confuse with `/verify-citations`** — that command performs bulk verification of existing prose. This skill handles new citation insertion.

**Reads**:
- User-provided input (_REV note, DOI, raw metadata)
- `docs/thesis/references.md` (duplicate check)
- `docs/thesis/sections/{chapter_id}.md` (insertion target, if specified)

**Writes**:
- `docs/thesis/references.md` (appends new entry — alphabetical order)
- `docs/thesis/sections/{chapter_id}.md` (inserts in-text citation, if section specified)

**Edge case rules**: `.claude/skills/apa-citation/references/apa7-rules.md`

---

#### PlannerAgent P2 pre-check (scheduling rule amendment)

> **[P2 pre-check]** Before scheduling WritingAgent for a chapter, verify that chapter
> has a structural skeleton approved in `docs/thesis/outline.md`.
> If the chapter has no skeleton entry → run `/update-outline` first.
> WritingAgent must not draft bullets for a structurally undefined chapter.

---

**Core architectural rules**:
- System A = research subject — System B never modifies System A logic
- Coordinator = sole decision-maker on task order in both systems
- **Every phase transition requires explicit human approval**
- Writing Agent produces ONLY bullet points — prose requires human sign-off

---

## FILE SYSTEM MEMORY

```
ai_research_framework/          # SYSTEM A — research framework (thesis object of study)
  config.py                     # 8GB RAM constraint, model list, LLM config
  agents/                       # 4 research agents (skeletons — blocked on data)
  state/research_state.py       # LangGraph TypedDict (ResearchState)
  core/coordinator.py           # LangGraph StateGraph

thesis_production_system/       # SYSTEM B — thesis writing tooling (not research contribution)
  agents/                       # 10 production agents (all implemented)
  state/thesis_state.py         # Pydantic ThesisState
  core/coordinator.py           # Plan→Execute→Critic loop

docs/
  context.md                    # Session log (updated every session)
  architecture.md               # Framework architecture decisions
  system_architecture_report.md # Full 10-section architecture report
  thesis_production_architecture.md # System A/B separation documentation
  experiment_tracking_agent.md  # Experiment Tracking Agent documentation
  literature/
    gap_analysis.md             # Gap identification + novelty claim (v3)
    rq_evolution.md             # RQ version history (v1 → v2)
    scraping_log.md             # Literature Scraping Agent log (Run 1 complete)
    papers/                     # 18 annotated papers (12 Tier 1 + 6 Tier A confirmed)
  data/
    nielsen_assessment.md       # Nielsen data model + access status
    indeksdanmark_notes.md      # Indeks Danmark structure + memory estimate
  tasks/
    data_assessment.md          # Phase 1 plan
    model_benchmark.md          # SRQ1 results (empty — pending data)
    synthesis_module.md         # SRQ2 design (empty — pending Phase 4)
    validation_report.md        # Validation results (empty — pending Phase 5)
    thesis_state.json           # ThesisState persistence (System B state)
  experiments/
    experiment_registry.json    # All experiment records (append-only)
    experiment_summary.md       # Auto-generated summary
  thesis/
    outline.md                  # 10-chapter approved structure
    figures/                    # Diagram Agent outputs (SVG + PNG)
    tables/                     # Results Tables Agent outputs
    sections/                   # 11 chapter bullet skeletons (all complete)
  compliance/
    cbs_guidelines_notes.md     # CBS formal requirements (extracted from 9 PDFs)
    compliance_checks/          # ComplianceAgent section outputs

Thesis/                         # Obsidian vault (human knowledge base)
  Thesis Guidelines/            # 9 CBS guideline PDFs
  prometheus_data_model-1.md   # Nielsen star schema
  indeksdanmark_data_model-1.md # Indeks Danmark structure
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
- **No em dashes (—) in any thesis prose.** Rewrite around them using commas, semicolons, colons, or subordinate clauses. Hyphens in compound adjectives (resource-constrained, data-driven) are permitted.
- Every installed package must be documented in `docs/context.md`
- `docs/thesis/outline.md` is owned exclusively by the thesis-structuring skill. PlannerAgent reads it. WritingAgent reads it. Neither writes to it.
- `docs/thesis/references.md` is owned exclusively by the APA Citation Skill (`/cite`). No agent writes to it directly. Use `/cite` for all new reference insertions.
- Major restructuring proposed by `/update-outline` requires explicit human approval before PlannerAgent may schedule any writing tasks for affected chapters.
- WritingAgent may not draft bullets for a chapter not present in `docs/thesis/outline.md`.

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

## REV AGENT — Inline Activation Rule

**REV (Research Evaluator)** is a dedicated internal agent for transforming academic paper content into structured Obsidian notes.

**Activation**: Any message that begins with `_REV` (underscore + REV, case-sensitive) triggers the REV agent exclusively.

**When `_REV` is detected:**
- Ignore all other instructions and context for that message
- Act as REV: produce only the structured Markdown note using the template defined in `.claude/commands/REV.md`
- Do NOT create files, do NOT add explanations, do NOT save anything
- Output the Markdown block directly in chat so the user can copy it into Obsidian

**Also available as**: `/REV` slash command (loads `.claude/commands/REV.md`)

---

## REV-BRIAN AGENT — Inline Activation Rule

**REV-brian** is Brian's personal variant of REV, using his own Obsidian vault property conventions and template structure.

**Activation**: Any message that begins with `_REV-brian` (case-sensitive) triggers REV-brian exclusively.

**When `_REV-brian` is detected:**
- Ignore all other instructions and context for that message
- Act as REV-brian: produce only the structured Markdown note using the template defined in `.claude/commands/REV-brian.md`
- Do NOT create files, do NOT add explanations, do NOT save anything
- Output the Markdown block directly in chat so Brian can copy it into his Obsidian vault (`Thesis/papers/`)
- Include the `%%FILE NAME: ...%%` comment at the top so Brian knows what to name the file

**Also available as**: `/REV-brian` slash command (loads `.claude/commands/REV-brian.md`)

---

## THESIS WRITER AGENT — Slash Command

**`/write-section <chapter_id>`** converts an approved bullet-point skeleton into CBS-compliant academic prose and writes it to `Thesis/thesis_draft.docx`.

**Activation**: `/write-section ch1_introduction` (or any valid chapter ID)

**Mandatory workflow** (never skip steps):
1. Read bullet file — confirm status is `bullets_approved` (not `bullets_draft`)
2. Generate prose draft — show in chat with character count estimate
3. **Citation verification** — NotebookLM verifies every citation is real and accurate (notebook ID: `48697de0-f0a5-4e66-918e-531abea82c20`)
4. **Compliance check** — CBS Compliance Agent validates: APA 7, structure, page budget, mandatory sections
5. **Human approval gate** — show draft + citation report + compliance report, wait for explicit OK
6. Write to Word — `Thesis/thesis_draft.docx` — update section status

**File**: `.claude/commands/write-section.md` + `.claude/agents/thesis-writer.md`
**Word dependency**: `python-docx` (install if missing, log in `docs/context.md`)
**NotebookLM notebook ID**: `48697de0-f0a5-4e66-918e-531abea82c20` (always run `notebooklm use <id>` at session start)

**Hard rules**:
- NEVER write prose without human approval
- NEVER skip compliance check
- NEVER fabricate citations — use `[CITATION NEEDED]` if source unknown
- NEVER claim Nielsen/Indeks Danmark results unless Phase 1 confirmed complete

---

## LAST UPDATED

2026-04-12 — Added `/write-section` + `/verify-citations` + `/find-papers` commands; `thesis-writer` + `literature-researcher` agents; NotebookLM integration (notebook ID: 48697de0-f0a5-4e66-918e-531abea82c20)
