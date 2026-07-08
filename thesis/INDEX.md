# Thesis Folder Structure & Index

**Last Updated:** 2026-04-27

This document maps the `thesis/` folder and explains what each section contains.

---

## Quick Navigation

| Folder | Purpose | Key Files |
|--------|---------|-----------|
| `data/` | Raw datasets, schemas, assessment | Nielsen CSVs, Indeks Danmark, schema docs |
| `literature/` | Literature review, paper analysis | 49 papers, gap analysis, RQ evolution |
| `thesis-context/` | Research questions, compliance, project state | RQs v2, CBS guidelines, Prometheus integration |
| `thesis-writing/` | Draft chapters, outline, references | All 10 chapters, abstract, introduction |
| `thesis_agents/` | System A & B agent code | Research framework, production system |

---

## Folder Details

### `data/`
**Status:** Finalized  
**Purpose:** Data access, schemas, and assessment documentation

- **`nielsen/`**
  - `description/SCHEMA_SNAPSHOT.md` — Complete Nielsen database schema (52 objects, columns, row counts)
  - `scripts/` — Nielsen data loading/processing scripts
  - `.csv/` — **All Nielsen CSVs** (4 product categories × 4 tables each = 16 CSVs, 2 metadata sets)

- **`spss_indeksdanmark/`**
  - `description/spss_indeksdanmark_data_model.md` — Indeks Danmark schema & description
  - `.csv/` — Indeks Danmark CSVs (data + metadata)

- **`assessment/`**
  - `DATA_ACCESS_SETUP.md` — How to access Nielsen & Indeks Danmark locally
  - `DATASETS_FINAL_SUMMARY.md` — Complete data inventory
  - `ml_usecases.md` — How each dataset applies to thesis (sales prediction, feature engineering, etc.)
  - `SCHEMA_SNAPSHOT.md` — Auto-generated schema reference

**Key Takeaway:** Both Nielsen and Indeks Danmark are **local & accessible** (2026-04-22 unblocked).

---

### `literature/`
**Status:** In Progress (49 papers catalogued)  
**Purpose:** Literature review & paper analysis

- **Root Level**
  - `gap_analysis.md` — Systematic gaps in current literature
  - `rq_evolution.md` — How research questions evolved from lit review
  - `scraping_log.md` — Paper collection history

- **`obisdian_paper_analysis/`** (49 papers)
  - **Agent/AI Papers:** `agent_noise_bench.md`, `ai_agents_vs_agentic_ai.md`, `dynamic_llm_agent_network.md`, `langgraph_2024.md`, `sciagent_tool_augmented_llm.md`, `toolformer.md`, etc.
  - **ML & Forecasting:** `ml_fmcg_demand_forecasting.md`, `retail_ml_tree_ensembles_lstm.md`, `humans_vs_llms_forecasting.md`, etc.
  - **Decision Support & Hybrid AI:** `ai_augmented_decision_making_dsr.md`, `hybrid_ai_llm_industrial.md`, `neuro_symbolic_ai_2024.md`, `mcdm_methods_overview.md`, etc.
  - **Methodology:** `hevner_design_science_2004.md`, `peffers_dsr_methodology_2007.md`, etc.

**Key Takeaway:** Rich foundation of 49 papers supporting methodology, agent architecture, ML forecasting, and hybrid AI approaches.

---

### `thesis-context/`
**Status:** Active  
**Purpose:** Research questions, compliance, project state, integration planning

- **`research-questions/`**
  - `research-questions.md` — **RQs v2** (primary research direction)
  - `srq1-models-efficiency.md` — Sub-RQ: ML model efficiency
  - `srq2-multi-agent-architecture.md` — Sub-RQ: Multi-agent design
  - `srq3-contextual-information.md` — Sub-RQ: Context handling
  - `srq4-comparison-to-traditional-bi.md` — Sub-RQ: BI comparison

- **`formal-requirements/`**
  - `compliance.md` — **CBS thesis requirements** (frozen decision)
  - `cbs_guidelines_notes.md` — CBS formatting, structure, plagiarism, ethical guidelines
  - `CITATION_VERIFICATION_SOP.md` — Citation verification process
  - `compliance_report_*.md` — Compliance audit snapshots

- **`thesis-topic/`**
  - `project-state.md` — **Frozen decisions** (architecture, scope, boundaries)
  - `project-overview.md` — High-level project description
  - `thesis-defense.md` — Defense structure & key arguments

- **`prometheus-integration/`** ← **NEW (2026-04-27)**
  - `PROMETHEUS_INTEGRATION_OVERVIEW.md` — Architecture clarification, meeting notes, deployment strategy

**Key Takeaway:** All frozen decisions are in `project-state.md`. Active planning is in `prometheus-integration/`.

---

### `thesis-writing/`
**Status:** In Progress (10 chapters drafted)  
**Purpose:** Final thesis content (prose + structure)

- **`sections-drafts/`** — Individual chapter files
  - `frontpage.md`, `abstract.md` — Front matter
  - `ch1-introduction.md` through `ch10-conclusion.md` — 10 chapters
  - `ai-declaration.md` — AI tool usage disclosure

- **`outline.md`** — **Master outline** (structure, bullet points, approval status)

- **`references.md`** — **APA 7 formatted bibliography** (updated via `/cite` skill)

- **`analysis/outputs_agentic/`**
  - `FUTURE_WORK.md` — Post-thesis research directions

**Key Takeaway:** Draft chapters exist; most are bullet-point skeletons. `/write-section` skill converts approved bullets to prose.

---

### `thesis_agents/`
**Status:** Frozen (System A) / Active (System B)  
**Purpose:** Agent code & frameworks

- **`ai_research_framework/`** (System A)
  - `.system_a_frozen.md` — Research framework documentation (read-only)

- **`thesis_production_system/`** (System B)
  - `.system_b_active.md` — Thesis writing automation (active)
  - `agents/builder/README.md` — Agent builder utilities

**Key Takeaway:** System A is frozen (reference only). System B is the active scaffolding for thesis production.

---

## Document Hierarchy

```
thesis/
├── data/              (Access & schemas — finalized)
├── literature/        (49 papers & analysis — in progress)
├── thesis-context/    (RQs, compliance, frozen state, integration planning — active)
│   └── prometheus-integration/  (NEW: integration strategy)
├── thesis-writing/    (Chapters, outline, references — in progress)
└── thesis_agents/     (System A frozen, System B active)
```

---

## Workflow: How These Folders Connect

1. **Read** `thesis-context/research-questions/research-questions.md` — know the RQs
2. **Check** `thesis-context/thesis-topic/project-state.md` — frozen decisions
3. **Reference** `literature/` papers — for citations in drafts
4. **Write** `thesis-writing/sections-drafts/*.md` — one chapter per file
5. **Update** `thesis-writing/outline.md` — track structure & approval
6. **Add citations** via `/cite` skill → auto-updates `thesis-writing/references.md`
7. **Convert bullets to prose** via `/write-section` skill → populate chapter drafts

---

## Current Status Summary

| Component | Status | Last Update |
|-----------|--------|-------------|
| Data Access | ✅ Complete | 2026-04-22 |
| Literature Review | 📋 In Progress (49 papers) | Ongoing |
| Research Questions | ✅ Frozen (RQs v2) | 2026-04-23 |
| Compliance | ✅ Confirmed | 2026-03-15 |
| Project State | ✅ Frozen | 2026-04-17 |
| Prometheus Integration | 🆕 Planning | 2026-04-27 |
| Thesis Chapters | 📝 Drafted (skeletons) | Ongoing |
| Chapter Writing | 📋 Pending | Dependent on approval |

---

## Important Notes

- **Frozen Decisions:** See `thesis-context/thesis-topic/project-state.md` — don't change without supervisor approval
- **CBS Compliance:** See `thesis-context/formal-requirements/compliance.md` — non-negotiable
- **Prometheus Integration:** See `thesis-context/prometheus-integration/PROMETHEUS_INTEGRATION_OVERVIEW.md` — new (as of 2026-04-27)
- **Chapter Approval Workflow:** Bullets only → human approval → prose conversion via `/write-section`

---

## Quick Links

- [Research Questions](thesis-context/research-questions/research-questions.md)
- [Project State (Frozen Decisions)](thesis-context/thesis-topic/project-state.md)
- [CBS Compliance](thesis-context/formal-requirements/compliance.md)
- [Thesis Outline](thesis-writing/outline.md)
- [References (APA 7)](thesis-writing/references.md)
- [Prometheus Integration (NEW)](thesis-context/prometheus-integration/PROMETHEUS_INTEGRATION_OVERVIEW.md)
- [Data Access Guide](data/assessment/DATA_ACCESS_SETUP.md)
- [Nielsen Schema](data/nielsen/description/SCHEMA_SNAPSHOT.md)

---

## Adding New Files

When creating new thesis documentation:
1. Place it in the appropriate folder above
2. Update this INDEX.md with a link
3. Cross-reference from related files
4. Use the YAML frontmatter format for all `.md` files

