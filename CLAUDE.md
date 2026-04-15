# CLAUDE.md — Manifold AI Thesis: Predictive Analytics Framework
> This file is automatically read by Claude Code at every session.
> Navigation hub only — full specs live in `.claude/rules/`. Do not bloat this file.

---

## NAVIGATION

**Read at session start (in order):**
1. This file (CLAUDE.md) — project context + constraints
2. [docs/architecture.md](docs/architecture.md) — System A/B separation, agent roles, design patterns
3. [docs/research-questions.md](docs/research-questions.md) — main RQ + 4 SRQs (v2), evolution history
4. [docs/project-state.md](docs/project-state.md) — frozen decisions, TODOs, constraints
5. [docs/compliance.md](docs/compliance.md) — CBS requirements, integrity gates, ADR status
6. [docs/tooling-issues.md](docs/tooling-issues.md) — known environment problems (mandatory before any plan)
7. [dev/repository_map.md](dev/repository_map.md) — file locations + agent status

**Key references:**
- [CHEATSHEET.md](CHEATSHEET.md) — quick-reference commands
- [docs/context.md](docs/context.md) — session log + package install documentation

**Claude workflows (in `.claude/rules/`):**
- Standup: `/log_standup` → `/prep_standup` → `/finalize_standup` → `/init_standup`
- Commit: `/draft_commit`
- Docs: `/update_all_docs`
- Plans: Write to `~/.claude/plans/` (auto-mirrored to `.claude/plans/plan_files/` with timestamps)

**Plan files organization**: See [.claude/rules/trigger-plan-workflow.md](.claude/rules/trigger-plan-workflow.md) for naming, mirroring, and outcome documentation.

---

## Model Override Convention

**Default**: Haiku across all agents (cost-optimized for thesis writing & analysis)

**Three ways to override:**

1. **`/model <tier>` command** — Session-wide override
   ```
   /model sonnet    # upgrade rest of session (complex analyses)
   /model haiku     # back to default
   /model opus      # for major architecture decisions
   ```

2. **Voice/inline phrase** — Per-request override (voice-friendly)
   ```
   "use sonnet for this analysis"     # detected and upgraded for this request
   "switch to opus"                   # recognized pattern
   "back to haiku" / "use default"    # resets to Haiku
   ```
   Particularly useful for voice input; phrase matching is case-insensitive.

3. **Automatic `/model` parsing** — Built into settings
   Commands like `/model sonnet` work session-wide without needing to restart.

**Rules**:
- Default = Haiku (cost-optimized for thesis writing + analysis)
- Inline phrases override for single request only
- `/model` command overrides for the entire session until you switch again
- When both `/model` and inline phrase present, inline takes precedence

**When to escalate to Sonnet**:
- Multi-file refactors (5+ files across System A and System B)
- Architecture decisions or major design changes
- Complex literature synthesis requiring deep reasoning
- Thesis writing at chapter boundaries when decisions intersect

---

## TOOLING RULE

**OneDrive safety**: This repo is on an OneDrive path. **Never** use Edit/Write directly on `.py` files.
Use the safe patching pattern (temp script → CRLF normalize → write_bytes). See [docs/tooling-issues.md](docs/tooling-issues.md).
The PreToolUse hook (`.claude/hooks/check_file_edit.py`) enforces this automatically.

> **macOS / Desktop path note**: The hook only fires on OneDrive-rooted paths. Enrico's Desktop path (`/Users/enricomanfron/Desktop/Thesis Maniflod/`) is NOT an OneDrive path — Edit/Write on `.py` files work normally here.

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

**See [docs/project-state.md](docs/project-state.md) for frozen decisions, constraints, risks, and TODOs.**

---

## PROJECT

**Description**: Master's thesis (Business Administration & Data Science) at Copenhagen Business School (CBS), in collaboration with Manifold AI. The project designs, implements, and evaluates a multi-agent framework that transitions Manifold's AI Colleagues system from descriptive analytics to predictive decision-support.

**Objective**: Answer the main research question — *How can an AI agent transition from descriptive analytics to predictive decision-support in a resource-constrained cloud environment (8GB RAM)?* — through an original framework integrating LLM orchestration, lightweight machine learning, and multi-criteria decision synthesis.

**Target users**: Manifold AI internal analysts and their business clients (Danish retailers and consumer goods manufacturers).

**Deadline**: 15 May 2026 — 120-page thesis (group, 2 students).

**Hard constraint**: 8GB total RAM. Every architectural decision must be justified against this constraint.

---

**See [docs/research-questions.md](docs/research-questions.md) for main RQ, SRQs (v2), and evolution history.**

---

## STACK

| Layer | Technology |
|---|---|
| Runtime | Local Python + Google Colab |
| Agent framework | PydanticAI + LangGraph |
| Orchestration | LangGraph (multi-agent coordination) |
| ML/Forecasting | LightGBM (global, Tweedie loss), XGBoost, Ridge (log-transform), ARIMA, Prophet, Seasonal Naive — **CONFIRMED** |
| Primary data | Nielsen/Prometheus CSD — SQL via Microsoft Fabric (pyodbc + azure-identity) — **CONFIRMED** |
| Secondary data | Indeks Danmark consumer survey — CSV, 20,134 rows, 6,364 variables — **CONFIRMED (downloaded)** |
| Data format | SQL (Microsoft Fabric) + CSV (Indeks Danmark) |
| Packages | See docs/context.md for install log |
| Frontend | None for now |
| Deployment | Local / Google Colab |

**Nielsen Dataset (primary)**:
- Star schema: `csd_clean_dim_market_v`, `csd_clean_dim_period_v`, `csd_clean_dim_product_v`, `csd_clean_facts_v`
- Access: SQL via Microsoft Fabric — Service Principal auth (pyodbc + azure-identity) — **live and returning data**
- Scope: Carbonated Soft Drinks (CSD), DVH EXCL. HD market (primary), 28 Danish retailers total
- History: 42 periods (full calendar 2022–2026), 77 brands after MIN_PERIODS filter
- Metrics: `sales_value`, `sales_in_liters`, `sales_units`, promo variants, `weighted_distribution`

**Indeks Danmark (secondary)**:
- Location: `Thesis/indeksdanmark/` — three CSVs (main 254 MB, codebook 1.8 MB, metadata 1.0 MB)
- CSD brand variables (K_564/K_565/K_700), retailer shopping frequency (FORR*), attitudinal variables
- Row-level survey weight: `VEJ_HH24`

---

## CURRENT STATUS

### Completed ✅
- [x] Indeks Danmark dataset documented + **CSVs downloaded** (2026-04-13) — located at `Thesis/indeksdanmark/`
- [x] Nielsen/Prometheus data model documented + **DB connection confirmed** (2026-04-12) — all 4 views returning data
- [x] `ai_research_framework/data/nielsen_connector.py` — Service Principal auth via pyodbc + azure-identity
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
- [x] **Phase 1 Data Assessment complete** — preprocessing pipeline, 77 brands, DVH EXCL. HD, 42 periods, feature matrix at `results/phase1/feature_matrix.parquet`
- [x] **SRQ1 Benchmark complete** — 6 models + ensemble benchmarked with walk-forward CV + held-out test evaluation
  - Validation metrics: LightGBM 31%, XGBoost 33%, Ensemble 32% median MAPE (see `benchmark_summary_v2.md`)
  - **Test set metrics (authoritative)**: XGBoost 45.5%, LightGBM 46.7%, Ridge 48.4% median MAPE (Sep 2025–Mar 2026)
  - SeasonalNaive baseline: 66.9% median MAPE on test
  - Analysis: See `docs/tasks/srq1_verification_report.md` for validation→test discrepancy analysis
- [x] NotebookLM Phase 0 PASSED (2026-04-13) — auth, source add, and grounded Q&A confirmed working

### Blocked 🔴
- [ ] **PENDING REVIEW**: Ch.1, Ch.2, Ch.3, Ch.4 prose in `docs/thesis/writing/` — requires human review before `prose_approved`
- [ ] **PENDING**: DSR supervisor confirmation (OI-03) — required for Ch.3 compliance sign-off

### Pending (can proceed now)
- [ ] Ch.4 Data Assessment writing — data assessment complete, can begin section writing
- [ ] Ch.5 Framework Design (14pp) — no additional data required
- [ ] Ch.9 Discussion (8pp) — no data required
- [ ] Ch.10 Conclusion (6pp) — no data required
- [ ] NotebookLM Phase 1: create 6 chapter notebooks, populate with 16+ confirmed papers
- [ ] Literature Scraping Run 2
- [ ] NotebookLM verification of 25 Ch.2 citations (pending)
- [ ] CBS compliance checks on chapter skeletons

### Data-dependent (now unblocked)
- [ ] Phase 5: Synthesis Module (SRQ2) — can begin (Phase 4 benchmark complete)
- [ ] Phase 6: Evaluation (SRQ3/SRQ4) — requires Phase 5 complete
- [ ] Indeks Danmark integration as external consumer signal (SRQ3)

> Last updated: 2026-04-13

---

**See [docs/compliance.md](docs/compliance.md) for definition of done criteria per phase.**

---

**See [docs/architecture.md](docs/architecture.md) for full System A/B agent architecture and design.**

Full system documentation: [docs/system_architecture_report.md](docs/system_architecture_report.md)

---

### SYSTEM A — AI Research Framework (`/ai_research_framework/`) — SUMMARY
*The experimental architecture being evaluated in the thesis. Appears in Chapters 5–8.*

| Agent | File | SRQ | Status |
|---|---|---|---|
| **Research Coordinator** | `core/coordinator.py` | Orchestrator | ✅ LangGraph StateGraph |
| **Data Assessment Agent** | `agents/data_assessment_agent.py` | SRQ1–4 precondition | ✅ Complete — Phase 1 done (77 brands, 42 periods, DVH EXCL. HD) |
| **Forecasting Agent** | `agents/forecasting_agent.py` | SRQ1 | ✅ Complete — 6 models + ensemble; test baseline: XGBoost 45.5%, LightGBM 46.7% median MAPE |
| **Synthesis Agent** | `agents/synthesis_agent.py` | SRQ2 | ⬜ Partial (API implemented — Phase 5 pending) |
| **Validation Agent** | `agents/validation_agent.py` | SRQ1–4 | ⬜ Pending (Phase 6 — requires Phase 5 complete) |

**Key model files (standalone runners, not class-based):**
- `agents/forecasting_agent.py` — per-brand benchmark (Ridge, LightGBM, XGBoost, ARIMA, Prophet + Ensemble)
- `agents/global_model.py` — Global LightGBM v1 (28.2% validation MAPE)
- `agents/global_model_v2.py` — Global LightGBM v2 + Tweedie + ensemble (validation: 22–26% MAPE; test: see test_evaluation.py)
- `agents/test_evaluation.py` — held-out test set evaluation (Sep 2025–Mar 2026); XGBoost 45.5%, LightGBM 46.7% median MAPE
- `data/preprocessing.py` — Nielsen preprocessing pipeline (feature engineering, train/val/test split)

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
  agents/                       # Research agents (benchmark runners)
    forecasting_agent.py        # Per-brand benchmark — 6 models + ensemble
    global_model.py             # Global LGB v1 (28.2% MAPE)
    global_model_v2.py          # Global LGB v2, Tweedie (22.5% MAPE) ← best
    test_evaluation.py          # Held-out test set evaluation
    data_assessment_agent.py    # Phase 1 complete
    synthesis_agent.py          # SRQ2 (partial)
    validation_agent.py         # SRQ1–4 (pending)
  data/
    nielsen_connector.py        # Microsoft Fabric auth (pyodbc + azure-identity)
    preprocessing.py            # Feature engineering + train/val/test split
  state/research_state.py       # LangGraph TypedDict (ResearchState)
  core/coordinator.py           # LangGraph StateGraph

thesis_production_system/       # SYSTEM B — thesis writing tooling (not research contribution)
  agents/                       # 10 production agents (all implemented)
  state/thesis_state.py         # Pydantic ThesisState
  core/coordinator.py           # Plan→Execute→Critic loop

results/
  phase1/                       # Phase 1 outputs (CSV/parquet gitignored)
    feature_matrix.parquet      # Full feature matrix, all brands — LOCAL ONLY
    series_index.csv            # Brand-level index — LOCAL ONLY
    split_dates.json            # Locked train/val/test boundaries
    preprocessing_report.md     # Data quality summary
    benchmark_summary.md        # Per-brand model benchmark (v1)
    benchmark_summary_v2.md     # Per-brand model benchmark (v2, lag_12 added)
    global_summary.md           # Global LGB v1 results
    global_v2_summary.md        # Global LGB v2 results (Tweedie, 22.5% MAPE)
    test_summary.md             # Held-out test set evaluation results

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
    guides/                     # NotebookLM-generated study guides (cached Markdown)
  data/
    nielsen_assessment.md       # Nielsen data model + access status
    indeksdanmark_notes.md      # Indeks Danmark structure + memory estimate
  tasks/
    data_assessment.md          # Phase 1 plan
    model_benchmark.md          # SRQ1 results (empty — use results/phase1/ instead)
    synthesis_module.md         # SRQ2 design (pending Phase 5)
    validation_report.md        # Validation results (pending Phase 6)
    thesis_state.json           # ThesisState persistence (System B state)
  experiments/
    experiment_registry.json    # All experiment records (append-only)
    experiment_summary.md       # Auto-generated summary
  thesis/
    outline.md                  # 10-chapter approved structure
    figures/                    # Diagram Agent outputs (SVG + PNG)
    tables/                     # Results Tables Agent outputs
    sections/                   # 11 chapter bullet skeletons (all complete)
    writing/                    # Prose drafts (Ch.1–3 written, pending review)
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
  indeksdanmark/                # Indeks Danmark CSVs (indeksdanmark_data.csv, codebook, metadata)
  prometheus_data_model-1.md   # Nielsen star schema
  indeksdanmark_data_model-1.md # Indeks Danmark structure
```

---

## CBS GUIDELINES

The CBS thesis guidelines PDF files are in `Thesis/Thesis Guidelines/`.
The CBS Compliance Agent must read them at session start and verify every Thesis Writing Agent output against:
- Citation format (APA 7 / CBS standard)
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

PHASE 1 — Data Assessment  ✅ COMPLETE
  → Data Assessment Agent analyses Nielsen + Indeks Danmark
  → Produced: results/phase1/ (feature matrix, preprocessing report, series index)
  → Nielsen: 77 brands, 42 periods, DVH EXCL. HD market

PHASE 2 — Literature Review & Gap Analysis  ✅ COMPLETE
  → Literature Review Agent researches papers, identifies gaps, proposes novelty
  → Produced: docs/literature/gap_analysis.md + rq_evolution.md
  → 40 papers, 6 Tier A confirmed

PHASE 3 — Framework Design  ✅ COMPLETE
  → Coordinator (architect persona) designed architecture
  → Produced: docs/architecture.md, docs/system_architecture_report.md

PHASE 4 — SRQ1: Model Selection & Benchmark  ✅ COMPLETE
  → Forecasting Agent tested 6 models + ensemble with walk-forward CV
  → Best: Global LightGBM v2 (Tweedie) — 22.5% median MAPE
  → Results: results/phase1/global_v2_summary.md

PHASE 5 — SRQ2: Synthesis Module  ← NEXT
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
- `docs/thesis/references.md` is owned exclusively by the APA Citation Skill (`/cite`). No agent writes to it directly.
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
- 🔴 **Tight timeline**: 15 May — ~1 month remaining for SRQ2–4 implementation + thesis writing
- 🟡 **High uncertainty**: RQs still evolving, novelty to be finalised, Indeks Danmark integration for SRQ3 not yet implemented
- 🟡 **External dependency**: Manifold AI feedback on framework design pending
- 🔒 **Security critical**: Nielsen dataset must not leave the local environment; Indeks Danmark contains survey weights
- 💥 **Context overflow risk**: Literature Review Agent over many papers, Thesis Writing Agent over 120 pages — use `/compact` aggressively

---

## NOTEBOOKLM INTEGRATION

**Status**: Phase 0 PASSED (2026-04-13) — auth, source add, and grounded Q&A confirmed working. Ready for Phase 1 (create 6 chapter notebooks, populate with 16 confirmed papers).

**Library**: `notebooklm-py==0.3.4` (pinned) — unofficial API, fragile by design. Manual UI fallback always available at notebooklm.google.com.

**Auth**: Run once per session expiry — `notebooklm login` (opens Chromium browser). Cookies stored at `~/.notebooklm/storage_state.json`.

**Notebook ID (Enrico's primary)**: `48697de0-f0a5-4e66-918e-531abea82c20`

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
[ ] docs/ structure verified (context.md, architecture.md, tasks/, literature/, data/, thesis/, compliance/)
[ ] CBS guidelines PDF present in Thesis/Thesis Guidelines/
[ ] CBS Compliance Agent has read the guidelines
[ ] Nielsen access confirmed (SQL via Microsoft Fabric — pyodbc + azure-identity)
[ ] Indeks Danmark CSVs confirmed at Thesis/indeksdanmark/
[ ] Current RQs documented in docs/literature/rq_evolution.md
[ ] Human confirmation received before starting any new phase
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
- NEVER claim Nielsen/Indeks Danmark results unless Phase 1 confirmed complete ✅ (Phase 1 IS complete)

---

## LAST UPDATED

2026-04-13 — Added navigation hub, tooling rule, build commands, integrity gates, Known TODOs. Bootstrapped .claude/ infrastructure (Pre-Phase complete).
2026-04-13 — NotebookLM integration: installed notebooklm-py==0.3.4, created papers/ directory structure, added NOTEBOOKLM section to CLAUDE.md, updated requirements.txt and .env.example. Phase 0 smoke test PASSED.
2026-04-13 — **Major status update (Enrico)**: Nielsen DB confirmed + live (pyodbc + azure-identity), Indeks Danmark CSVs downloaded, Phase 1 Data Assessment complete (77 brands, 42 periods), SRQ1 benchmark complete (Global LightGBM v2 Tweedie = 22.5% median MAPE), Ch.1–3 prose written. STACK and AGENT ARCHITECTURE updated to reflect real project state.
