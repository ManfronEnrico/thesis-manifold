# Repository Map — CMT_Codebase

> Fast session orientation. Read this after CLAUDE.md at the start of every session.
> Last updated: 2026-04-19

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
│   ├── generate_figures.py            ← Generates thesis diagrams → thesis/writing/figures/
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
│   ├── ai_research_framework/         ← SYSTEM A: research computation (thesis subject)
│   │   ├── .system_a_frozen.md        ← FROZEN: no modifications allowed
│   │   ├── config.py                  ← 8GB RAM constraint, model list, LLM config
│   │   ├── agents/                    ← 4 research agents (blocked on Nielsen data)
│   │   ├── core/coordinator.py        ← LangGraph StateGraph orchestrator
│   │   └── state/research_state.py    ← LangGraph TypedDict (ResearchState)
│   │
│   ├── thesis_production_system/      ← SYSTEM B: thesis writing tooling
│   │   ├── .system_b_active.md        ← ACTIVE: safe to extend with toggles
│   │   ├── agents/                    ← 10 production agents
│   │   ├── core/coordinator.py        ← Plan→Execute→Critic orchestrator
│   │   └── state/thesis_state.py      ← Pydantic ThesisState
│   │
│   ├── writing/                       ← Thesis document content
│   │   ├── sections/                  ← 10 chapter .md files (bullet skeletons)
│   │   ├── figures/                   ← Thesis diagrams (SVG + PNG)
│   │   ├── prose/                     ← Word + PDF drafts of approved sections
│   │   ├── analysis/                  ← Jupyter notebooks & outputs
│   │   ├── outline.md                 ← Chapter structure & page budgets
│   │   └── references.md             ← APA 7 bibliography (living doc)
│   │
│   ├── literature/                    ← Paper corpus & citation management
│   │   ├── bibtex.bib                 ← BibTeX database (48+ entries)
│   │   ├── citations.json             ← Zotero export
│   │   ├── ingestion_manifest.json    ← NotebookLM ingestion state
│   │   ├── gap_analysis.md            ← Literature gaps identified
│   │   ├── scraping_log.md            ← Paper confirmation log
│   │   └── obisdian_paper_analysis/   ← 50+ annotated paper summaries
│   │
│   ├── compliance/                    ← CBS formal requirements
│   │   ├── cbs_guidelines_notes.md    ← CBS guidelines extracted
│   │   └── compliance_checks/         ← Compliance audit reports
│   │
│   ├── data/                          ← Data sources & pipelines
│   │   ├── nielsen/                   ← Nielsen SQL connector & scripts
│   │   │   ├── scripts/               ← connector, loader, exploration scripts
│   │   │   └── description/           ← nielsen-prometheus_data_model.md
│   │   ├── indeksdanmark/             ← SPSS/CSV loader & data
│   │   │   ├── scripts/               ← spss_indeksdanmark_loader.py
│   │   │   ├── description/           ← spss_indeksdanmark_data_model.md
│   │   │   └── .csv/                  ← 254MB CSV data files (gitignored)
│   │   ├── preprocessing/             ← Combined preprocessing pipeline
│   │   └── assessment/                ← Data notes, ML use cases, migration docs
│   │
│   └── thesis-docs/                   ← Thesis reference docs
│       ├── PROJECT_OVERVIEW.md        ← Problem statement, RQs, gaps, timeline
│       ├── research-questions.md      ← Main RQ + 4 SRQs (v2)
│       ├── project-state.md           ← Frozen decisions, constraints, risks
│       └── CITATION_VERIFICATION_SOP.md ← Citation trust levels & workflow
│
└── docs/                              ← CODEBASE & TOOLING DOCS
    ├── codebase/                      ← System architecture documents
    │   ├── architecture.md            ← System A/B design overview
    │   ├── system_architecture_report.md ← Comprehensive technical report
    │   ├── thesis_production_architecture.md ← Production system design
    │   └── experiment_tracking_agent.md ← Experiment registry agent spec
    ├── tooling/                       ← Environment & tooling docs
    │   └── tooling-issues.md          ← Solved Windows/OneDrive issues (living log)
    ├── integrations/                  ← Integration setup & architecture docs
    │   ├── NOTEBOOKLM_*.md            ← NotebookLM integration (7 files)
    │   ├── ZOTERO_INTEGRATION_SETUP.md ← Zotero full setup guide
    │   ├── GOOGLE_DRIVE_*.md          ← Google Drive setup docs
    │   ├── ENRICO_*.md                ← Enrico-specific setup guides
    ├── planning/                      ← Implementation plans (time-bound)
    │   └── 2026_04_18-indeks_integration_plan.md ← Indeks Danmark integration plan
    ├── reference/                     ← Quick-reference cards (daily use)
    │   ├── CHEATSHEET.md              ← CLI commands, workflow triggers
    │   ├── ZOTERO_QUICK_REFERENCE.md  ← Zotero API quick commands
    │   ├── ZOTERO_SETUP_GUIDE.md      ← Zotero config reference
    │   ├── TESTING_QUICK_REFERENCE.md ← System A test quick card
    │   └── INTEGRATION_QUICK_REFERENCE.md ← All integrations status table
    ├── claude-tooling/                ← Claude Code skill/workflow docs
    │   ├── SKILL_ACTIVATION_SUMMARY.md
    │   └── SKILL_CREATION_SUMMARY.md
    ├── project-management/            ← Project state & planning docs
    │   ├── IMPLEMENTATION_CHECKLIST.md
    │   └── context.md                 ← Session log & package installs
    ├── codebase-testing/              ← Codebase test plans & results
    │   ├── TEST_SUMMARY_2026-04-15.md
    │   ├── TEST_GROUP_SCRIPT_README.md
    │   ├── agent_system_test_scenarios.md
    │   ├── PRE_SYNC_TEST_GUIDE.md
    │   ├── TEST_EXECUTION_CHECKLIST.md
    │   └── VALIDATION_COMPLETE_2026-04-15.md
    ├── sessions/                      ← Dated session artifacts (YYYY-MM-DD_HH-MM_slug.md)
    │   ├── 2026-04-15_19-58_zotero-sync-report.md
    │   ├── 2026-04-18_17-58_integration-audit-and-handover.md
    │   ├── 2026-04-18_18-44_notebook-quality-audit.md
    │   ├── 2026-04-18_18-45_gitignore-strategy.md
    │   ├── 2026-04-18_18-46_action-items.md
    │   └── 2026-04-18_21-10_handover-summary.md
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
| Research questions | `thesis/thesis-docs/research-questions.md` |
| Project state & constraints | `thesis/thesis-docs/project-state.md` |
| CBS compliance requirements | `thesis/compliance/cbs_guidelines_notes.md` |
| System A/B architecture | `docs/codebase/architecture.md` |
| Tooling issues (living log) | `docs/tooling/tooling-issues.md` |
| Thesis chapter sections | `thesis/writing/sections/` |
| Paper corpus | `thesis/literature/obisdian_paper_analysis/` |
| BibTeX bibliography | `thesis/literature/bibtex.bib` |
| Experiment outputs | `results/phase1/` |
| Nielsen data scripts | `thesis/data/nielsen/scripts/` |
| Indeks Danmark scripts | `thesis/data/indeksdanmark/scripts/` |
| CLI quick reference | `docs/reference/CHEATSHEET.md` |
| Zotero quick reference | `docs/reference/ZOTERO_QUICK_REFERENCE.md` |
| Integration status | `docs/reference/INTEGRATION_QUICK_REFERENCE.md` |

---

## System A vs System B

| | System A | System B |
|--|----------|----------|
| **Location** | `thesis/ai_research_framework/` | `thesis/thesis_production_system/` |
| **Status** | FROZEN (research artefact) | ACTIVE (thesis tooling) |
| **Purpose** | The thing being evaluated in the thesis | Tooling that helps write the thesis |
| **Modify?** | No — would invalidate results | Yes — toggle-gated features |
| **Marker** | `.system_a_frozen.md` | `.system_b_active.md` |
