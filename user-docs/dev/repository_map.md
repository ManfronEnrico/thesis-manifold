# Repository Map — CMT_Codebase

> Fast session orientation. Read this after CLAUDE.md at the start of every session.
> Last updated: 2026-04-20

---

## Top-Level Structure

```
CMT_Codebase/
├── CLAUDE.md                          ← Session entry point & navigation hub
├── README.md                          ← Project overview
├── pyproject.toml / uv.lock           ← Python project config & locked deps
├── .env / .env.example                ← Environment variables (Nielsen, Zotero, GDrive)
│
├── .archive/                          ← Archived legacy materials (not version controlled)
├── .claude/                           ← Claude Code operating environment
│   ├── hooks/                         ← OneDrive .py safety enforcer
│   ├── rules/                         ← Auto-loaded workflow rules
│   ├── skills/                        ← Academic research skills
│   ├── agents/                        ← literature-researcher, thesis-writer agents
│   ├── commands/                      ← REV, REV-brian, cite, find-papers commands
│   ├── plans/                         ← Dated plan files + outcome files
│   ├── memory/                        ← Session memory (single source of truth)
│   └── SKILLS_INVENTORY.md            ← Complete skills reference
│
├── scripts/                           ← Utility scripts (run from repo root)
│   ├── generate_figures.py            ← Generates thesis diagrams → thesis/thesis-writing/figures/
│   ├── generate_systemB_diagram.py    ← System B architecture diagram
│   ├── notebooklm_ingestion.py        ← Batch ingest papers → NotebookLM notebooks
│   ├── zotero_client.py               ← Zotero API client
│   ├── zotero_sync_phase1.py          ← Zotero sync → thesis/literature/papers/
│   └── test_group.py                  ← Test Zotero group library connection
│
├── src/                               ← Integration layer
│   └── google_drive_integration.py    ← Google Drive API (used by notebooklm_ingestion.py)
│
├── tests/                             ← Unit tests for codebase
│
├── results/                           ← Experiment outputs by phase
│   ├── phase1/                        ← Preprocessing, feature matrix, benchmarks
│   ├── audit_logs/                    ← Experiment metadata & EDA audit trails
│   └── seaborn_exploratory/           ← EDA figures + sample Nielsen CSV
│
├── project_updates/                   ← Standup drafts & session logs (hardcoded in skills)
│   ├── standup_draft.md               ← Active standup draft
│   └── standup_draft_archive.md       ← Archived standup entries
│
├── thesis/                            ← ALL THESIS-FACING WORK
│   ├── thesis_agents/                 ← Python agent packages (importable)
│   │   ├── ai_research_framework/     ← SYSTEM A: research computation (thesis subject)
│   │   │   ├── .system_a_frozen.md    ← FROZEN: no modifications allowed
│   │   │   ├── config.py              ← 8GB RAM constraint, model list, LLM config
│   │   │   ├── agents/                ← 4 research agents (blocked on Nielsen data)
│   │   │   ├── core/coordinator.py    ← LangGraph StateGraph orchestrator
│   │   │   └── state/research_state.py ← LangGraph TypedDict (ResearchState)
│   │   │
│   │   └── thesis_production_system/  ← SYSTEM B: thesis writing tooling
│   │       ├── .system_b_active.md    ← ACTIVE: safe to extend with toggles
│   │       ├── agents/                ← 10 production agents
│   │       ├── core/coordinator.py    ← Plan→Execute→Critic orchestrator
│   │       └── state/thesis_state.py  ← Pydantic ThesisState
│   │
│   ├── thesis-writing/                ← Thesis document content
│   │   ├── sections-drafts/           ← 11 chapter .md files (kebab-case, bullet skeletons)
│   │   ├── sections-final/            ← Approved Word .docx exports (kebab-case)
│   │   ├── figures/                   ← Thesis diagrams (SVG + PNG)
│   │   ├── analysis/                  ← Jupyter notebooks & outputs
│   │   ├── outline.md                 ← Chapter structure & page budgets
│   │   └── references.md              ← APA 7 bibliography (living doc)
│   │
│   ├── thesis-context/                ← Thesis scope & formal requirements
│   │   ├── research-questions/        ← Main RQ + 4 SRQs (v2)
│   │   ├── thesis-topic/              ← Project state, overview, defense notes
│   │   ├── formal-requirements/       ← CBS guidelines, compliance reports
│   │   └── chapters/                  ← Ch2 literature review draft (context stub)
│   │
│   ├── literature/                    ← Paper corpus & citation management
│   │   ├── bibtex.bib                 ← BibTeX database (48+ entries)
│   │   ├── citations.json             ← Zotero export
│   │   ├── ingestion_manifest.json    ← NotebookLM ingestion state
│   │   ├── gap_analysis.md            ← Literature gaps identified
│   │   ├── scraping_log.md            ← Paper confirmation log
│   │   └── obisdian_paper_analysis/   ← 50+ annotated paper summaries
│   │
│   └── data/                          ← Data sources & pipelines
│       ├── nielsen/                   ← Nielsen SQL connector & scripts
│       │   ├── scripts/               ← Production scripts (audit, export, connection)
│       │   │   ├── nielsen_connector.py ← Power BI/Fabric API connection (fixed)
│       │   │   ├── audit_datasets.py ← Discover all 52 Fabric objects
│       │   │   ├── save_all_datasets.py ← Batch export to CSV + manifest
│       │   │   └── exploration scripts ← Data profiling utilities
│       │   ├── exported/              ← CSV backups (29 files, 1.9 GB, manifest.json)
│       │   ├── README.md              ← Colleague onboarding guide
│       │   └── description/           ← nielsen-prometheus_data_model.md
│       ├── indeksdanmark/             ← SPSS/CSV loader & data
│       │   ├── scripts/               ← spss_indeksdanmark_loader.py
│       │   └── description/           ← spss_indeksdanmark_data_model.md
│       ├── preprocessing/             ← Combined preprocessing pipeline
│       └── assessment/                ← Data notes, ML use cases, migration docs
│
└── docs/                              ← CODEBASE & TOOLING DOCS
    ├── codebase/                      ← System architecture documents
    │   ├── architecture.md            ← System A/B design overview
    │   ├── system-architecture-report.md ← Comprehensive technical report
    │   ├── thesis_production_architecture.md ← Production system design
    │   └── experiment-tracking-agent.md ← Experiment registry agent spec
    ├── tooling/                       ← Environment & tooling docs
    │   └── tooling-issues.md          ← Solved Windows/OneDrive issues (living log)
    ├── integrations/                  ← Integration setup & architecture docs
    │   ├── notebooklm-*.md            ← NotebookLM integration (7 files)
    │   ├── zotero-integration-setup.md ← Zotero full setup guide (canonical)
    │   ├── google-drive-*.md          ← Google Drive setup docs
    │   ├── enrico-*.md                ← Enrico-specific setup guides
    ├── planning/                      ← Implementation plans (time-bound)
    │   └── 2026_04_18-indeks_integration_plan.md ← Indeks Danmark integration plan
    ├── reference/                     ← Quick-reference cards (daily use)
    │   ├── cheatsheet.md              ← CLI commands, workflow triggers
    │   ├── zotero-quick-reference.md  ← Zotero API quick commands
    │   ├── testing-quick-reference.md ← System A test quick card
    │   ├── integration-quick-reference.md ← All integrations status table
    │   └── git-branch-strategy.md    ← Git branching conventions
    ├── claude-tooling/                ← Claude Code skill/workflow docs
    │   ├── skill-activation-summary.md
    │   └── skill-creation-summary.md
    ├── project-management/            ← Project state & planning docs
    │   ├── implementation-checklist.md
    │   └── context.md                 ← Session log & package installs
    ├── codebase-testing/              ← Codebase test plans & results
    │   ├── test-summary-2026-04-15.md
    │   ├── test-group-script-readme.md
    │   ├── agent-system-test-scenarios.md
    │   ├── pre-sync-test-guide.md
    │   ├── test-execution-checklist.md
    │   └── validation-complete-2026-04-15.md
    ├── notes/                         ← Dated session notes (YYYY_MM_DD-slug.md)
    │   ├── 2026_04_15-zotero_sync_report.md
    │   ├── 2026_04_18-notebook_quality_audit.md
    │   ├── 2026_04_18-gitignore_strategy.md
    │   └── 2026_04_18-action_items.md
    ├── handover/                      ← Dated handover docs (YYYY_MM_DD-slug.md)
    │   ├── 2026_04_18-integration_audit_handover.md
    │   └── 2026_04_18-handover_summary.md
    ├── memory/                        ← Legacy memory (live memory is in .claude/memory/)
    ├── dev/                           ← Development reference
    │   └── repository_map.md          ← THIS FILE
    ├── decisions/                     ← Architecture Decision Records (ADRs)
    ├── experiments/                   ← Experiment registry & summaries
    └── tasks/                         ← Phase-specific work items & thesis_state.json
```

---

## Key File Locations

| What | Where |
|------|-------|
| Session start (read first) | `CLAUDE.md` |
| Research questions | `thesis/thesis-context/research-questions/research-questions.md` |
| Project state & constraints | `thesis/thesis-context/thesis-topic/project-state.md` |
| CBS compliance requirements | `thesis/thesis-context/formal-requirements/cbs_guidelines_notes.md` |
| System A/B architecture | `docs/codebase/architecture.md` |
| Tooling issues (living log) | `docs/tooling/tooling-issues.md` |
| Thesis chapter sections | `thesis/thesis-writing/sections-drafts/` |
| Paper corpus | `thesis/literature/obisdian_paper_analysis/` |
| BibTeX bibliography | `thesis/literature/bibtex.bib` |
| Experiment outputs | `results/phase1/` |
| Nielsen data scripts | `thesis/data/nielsen/scripts/` |
| Indeks Danmark scripts | `thesis/data/indeksdanmark/scripts/` |
| CLI quick reference | `docs/reference/cheatsheet.md` |
| Zotero quick reference | `docs/reference/zotero-quick-reference.md` |
| Integration status | `docs/reference/integration-quick-reference.md` |

---

## System A vs System B

| | System A | System B |
|--|----------|----------|
| **Location** | `thesis/thesis_agents/ai_research_framework/` | `thesis/thesis_agents/thesis_production_system/` |
| **Status** | FROZEN (research artefact) | ACTIVE (thesis tooling) |
| **Purpose** | The thing being evaluated in the thesis | Tooling that helps write the thesis |
| **Modify?** | No — would invalidate results | Yes — toggle-gated features |
| **Marker** | `.system_a_frozen.md` | `.system_b_active.md` |
