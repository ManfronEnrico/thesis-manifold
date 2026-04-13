# CLAUDE.md — Manifold AI Thesis: Predictive Analytics Framework
> This file is automatically read by Claude Code at every session.
> Navigation hub only — full specs live in `.claude/rules/`. Do not bloat this file.

---

## NAVIGATION

**Read at session start (in order):**
1. This file (CLAUDE.md) — project context + constraints
2. [dev/repository_map.md](dev/repository_map.md) — file locations + agent status
3. [docs/tooling-issues.md](docs/tooling-issues.md) — known env problems (mandatory before any plan)

**Key references:**
- [docs/decisions/ADR-001-template-strategy.md](docs/decisions/ADR-001-template-strategy.md) — LaTeX template (OPEN)
- [docs/decisions/ADR-002-build-pipeline.md](docs/decisions/ADR-002-build-pipeline.md) — PDF pipeline (OPEN)
- [docs/decisions/ADR-003-builder-agent-fate.md](docs/decisions/ADR-003-builder-agent-fate.md) — Builder agent (OPEN)
- [docs/compliance/cbs_guidelines_notes.md](docs/compliance/cbs_guidelines_notes.md) — CBS requirements
- [CHEATSHEET.md](CHEATSHEET.md) — quick-reference commands

**Claude workflows (in `.claude/rules/`):**
- Standup: `/log_standup` → `/prep_standup` → `/finalize_standup` → `/init_standup`
- Commit: `/draft_commit`
- Docs: `/update_all_docs`
- Plans: `/update_plan`

---

## TOOLING RULE

**OneDrive safety**: This repo is on an OneDrive path. **Never** use Edit/Write directly on `.py` files.
Use the safe patching pattern (temp script → CRLF normalize → write_bytes). See [docs/tooling-issues.md](docs/tooling-issues.md).
The PreToolUse hook (`.claude/hooks/check_file_edit.py`) enforces this automatically.

---

## BUILD COMMANDS (Phase 3 — not yet set up)

Once the LaTeX pipeline is built (Phase 3):
```bash
make pdf      # Markdown → LaTeX → PDF (build/thesis.pdf)
make check    # Run integrity gates (scripts/check_integrity.py)
make figures  # Regenerate all figures (generate_figures.py)
```

---

## INTEGRITY GATES (Phase 4 — not yet set up)

| Gate | When | Checks |
|------|------|--------|
| Gate 1 (Pre-Draft) | Before prose expansion | Section completeness, page budget (120p), skeleton approved |
| Gate 2 (Post-Draft) | After first full draft | APA7 citations, figure references, NotebookLM cross-check |
| Gate 3 (Pre-Submission) | Before final PDF | 7-mode AI failure checklist, CBS compliance, AI disclosure, 49-citation validation |

Run Gate 3 with `make check`. Run Gate 1/2 manually using [docs/compliance/integrity_checklist.md](docs/compliance/integrity_checklist.md) (TODO Phase 4).

---

## KNOWN TODOs / FROZEN DECISIONS

> These are deliberate choices. **Do not "fix" these without Brian's explicit instruction.**

- **Measurement model**: DSR (Design Science Research) methodology confirmed — do not suggest alternatives
- **RAM constraint**: 8GB hard limit on all System A models — no exceptions, no suggestions to "just use more RAM"
- **Writing Agent**: produces ONLY bullet points — never full prose. Prose requires human sign-off
- **Phase transitions**: every phase requires explicit human approval before proceeding
- **Nielsen access**: SQL modality not yet confirmed — do not assume CSV or SQL until clarified
- **RQs v2**: currently the canonical version — do not modify without Brian flagging a change
- **System A vs System B**: these are separate systems. Never modify System A logic from System B agents
- **ADR-001/002/003**: open decisions — do not implement Phase 3 before these are resolved

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

### Blocked 🔴
- [ ] **BLOCKED**: Nielsen database access — not yet obtained, must request from Manifold + sign confidentiality agreement
- [ ] **BLOCKED**: Indeks Danmark CSVs — must download from Google Drive to Thesis/ folder

### Pending (can proceed without data)
- [ ] **NotebookLM Phase 0**: Run `notebooklm login`, create 6 chapter notebooks, add one test PDF, generate one study guide — gate decision before Phase 1
- [ ] Literature Scraping Run 2 (trigger at next session)
- [ ] Generate architecture figures (requires: pip install graphviz matplotlib)
- [ ] CBS compliance checks on chapter skeletons
- [ ] Tier B paper confirmations (10 papers — user decision pending)

### Data-dependent (blocked)
- [ ] Phase 1: Data Assessment (actual implementation)
- [ ] Phase 4: Model Benchmark (SRQ1)
- [ ] Phase 5: Synthesis Module (SRQ2)
- [ ] Phase 6: Evaluation (SRQ3/SRQ4)

> Last updated: 2026-03-15

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
    guides/                     # NotebookLM-generated study guides (cached Markdown, auto-generated)
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

papers/                         # PDF source files for NotebookLM ingestion
  ch2-literature/               # All 16+ confirmed papers (cross-corpus QA)
  ch3-methodology/              # Tier A ML methodology papers
  ch4-models/                   # Forecasting model papers
  ch5-synthesis/                # Consumer signal / sentiment papers
  ch6-evaluation/               # Calibration + evaluation papers
  ingestion_manifest.json       # Maps paper slugs → NotebookLM source IDs + notebook IDs

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

## NOTEBOOKLM INTEGRATION

**Status**: Phase 0 PASSED (2026-04-13) — auth, source add, and grounded Q&A confirmed working. Ready for Phase 1 (create 6 chapter notebooks, populate with 16 confirmed papers).

**Library**: `notebooklm-py==0.3.4` (pinned) — unofficial API, fragile by design. Manual UI fallback always available at notebooklm.google.com.

**Auth**: Run once per session expiry — `notebooklm login` (opens Chromium browser). Cookies stored at `~/.notebooklm/storage_state.json`.

**Ownership model**: Brian's Google account owns all notebooks. Enrico gets shared access via NotebookLM web UI (`notebooklm.google.com`). Only Brian runs `notebooklm-py` scripts — the API only sees notebooks owned by the authenticated account. `ingestion_manifest.json` holds Brian's notebook IDs as the single source of truth.

### Notebook Map (populate after `notebooklm login` + `notebooklm create`)

| Notebook | NotebookLM ID | Chapter focus |
|---|---|---|
| `thesis-ch2-literature` | *(pending login)* | All 16+ confirmed papers — cross-corpus QA |
| `thesis-ch3-methodology` | *(pending login)* | ML methodology papers (Tier A) |
| `thesis-ch4-models` | *(pending login)* | Forecasting + benchmark comparison papers |
| `thesis-ch5-synthesis` | *(pending login)* | Consumer signal / sentiment papers |
| `thesis-ch6-evaluation` | *(pending login)* | Calibration + evaluation methodology |
| `thesis-defense` | *(pending login)* | All papers — defense Q&A |

### Mandatory Rules (Non-Negotiable)

1. **Never pass NotebookLM output directly to WritingAgent** without `verified: False` flag cleared by a human.
2. **All quotes** from NotebookLM must be cross-checked against the actual PDF before entering any draft.
3. **Study guides / briefing docs** = orientation only. Not citable. They inform the analyst, not the draft.
4. **Never use NotebookLM output as evidence** in the SRQ3/SRQ4 evaluation sections (quantitative results only).
5. **If notebooklm-py breaks** → fall back to manual UI. All notebooks remain accessible there. Zero production capability lost.

### Citation Format (when NotebookLM-sourced)

```
[Claim] (Author, Year, p. X — verified via NotebookLM citation, PDF confirmed)
```
`PDF confirmed` tag is mandatory before final submission.

### Approved Workflow Patterns

- **Pattern A** (Literature QA): Ask → get answer + citation passage → flag as `[NOTEBOOKLM — VERIFY]` → human confirms against PDF
- **Pattern B** (Study Guide): Generate → cache to `docs/literature/guides/` → flag as `[SUMMARY — NOT VERBATIM]`
- **Pattern C** (Quote Verification): Writing Agent flags claim → NotebookLM locates passage → human confirms
- **Pattern D** (Defense Prep): Ask defense questions → get grounded answers + challenges → human reviews

### Source Ingestion

Papers live in `papers/<chapter>/`. Run `scripts/notebooklm_ingestion.py` to sync new PDFs to notebooks.
Manifest at `papers/ingestion_manifest.json` — check before adding (idempotency).

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

## LAST UPDATED

2026-04-13 — Added navigation hub, tooling rule, build commands, integrity gates, Known TODOs. Bootstrapped .claude/ infrastructure (Pre-Phase complete).
2026-04-13 — NotebookLM integration: installed notebooklm-py==0.3.4, created papers/ directory structure, added NOTEBOOKLM section to CLAUDE.md, updated requirements.txt and .env.example. Phase 0 smoke test pending (requires `notebooklm login`).
