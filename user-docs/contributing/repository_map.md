# Repository Map — thesis-manifold

> Fast session orientation. Read this after CLAUDE.md at the start of every session.
> Last updated: 2026-07-11 (P0028 restructure — supersedes the pre-restructure `thesis/`-based map)

---

## Top-Level Structure

```
thesis-manifold/
├── CLAUDE.md                          ← Session entry point & navigation hub (Claude Code)
├── AGENTS.md                          ← Same navigation hub, for non-Claude-Code agents
├── README.md                          ← Project overview
├── PATHS.py                           ← Centralized path constants (never hardcode paths)
├── pyproject.toml / uv.lock           ← Python project config & locked deps
├── .env / .env.example                ← Environment variables (Nielsen, Zotero, GDrive)
│
├── .archive/                          ← Archived legacy materials (not deleted, kept for reference)
├── .claude/                           ← Claude Code operating environment
│   ├── rules/                         ← Auto-loaded workflow/governance rules
│   ├── skills/                        ← ~70 task-specific skills (research, ML, git, docs)
│   ├── agents/                        ← literature-researcher, thesis-writer agent defs
│   ├── commands/                      ← Slash commands (cite, find-papers, write-section, ...)
│   ├── hooks/                         ← branch_guard and other session hooks
│   ├── memory/                        ← Auto-memory (see MEMORY.md index)
│   └── logs/                          ← tooling-issues.jsonl (source of truth for tooling log)
│
├── 00_thesis_context/                 ← Thesis topic, scope, formal requirements
│   ├── thesis-topic/                  ← project-state.md (frozen decisions), overview
│   ├── formal-requirements/           ← CBS compliance guidelines & checks
│   ├── methodology/                   ← Research methodology framework (Saunders research onion)
│   └── prometheus-integration/        ← SRQ3 integration-readiness notes
│
├── 01_thesis_research/                ← Research questions + literature
│   ├── research-questions/            ← Main RQ + SRQ1–4 (canonical v4)
│   └── literature/                    ← Paper corpus, bibtex.bib, citations.json
│
├── 02_thesis_data/                    ← Data pipeline (raw → engineered)
│   ├── _00_raw/                       ← TIER 1: source data (Nielsen JSONL, SPSS CSV)
│   ├── _01_converted/                 ← TIER 2: format-converted cache (Parquet)
│   ├── _02_preprocessing/             ← TIER 3 scripts: per-category pipelines (not data)
│   │   └── nielsen/{CSD,Danskvand,Energidrikke,RTD,Totalbeer}/
│   ├── _03_engineered/                ← TIER 4: feature matrices
│   │   ├── bymonth/, bychain/         ← current split-by-granularity outputs
│   │   └── nielsen/                   ← ⚠️ old pre-split shape, real data, left in place —
│   │                                    see .claude/rules/repo-tier-structure.md before touching
│   ├── preprocessing/                 ← top-level legacy preprocessing scripts (pre-dates tiers)
│   ├── nielsen/, spss_indeksdanmark/  ← per-source connector scripts + schema docs
│   ├── assessment/                    ← data access setup notes, migration logs
│   └── METADATA.py                    ← dataset metadata constants
│
├── 03_thesis_modelling/               ← Model training + serving
│   ├── model_training/                ← srq1_*.py, srq2_*.py, srq4_*.py (one-off training/benchmark scripts)
│   ├── model_serving/                 ← code that runs trained models
│   │   ├── system_a_forecast/         ← SYSTEM A: forecast_service.py (research object)
│   │   └── system_b_conversational/   ← SYSTEM B: generate_systemB_diagram.py (thesis tooling)
│   ├── notebooks/                     ← SRQ_1/, SRQ_2_and_3/ Jupyter notebooks
│   └── prompts/                       ← LLM prompt templates
│
├── 04_thesis_results/                 ← Final SRQ outputs (one folder per SRQ)
│   ├── srq1/, srq2/, srq4/
│   └── generate_figures.py            ← Thesis figure generator → 05_thesis_writing/figures/
│
├── 05_thesis_writing/                 ← Thesis prose + figures
│   ├── sections-drafts/               ← Chapter bullet skeletons (kebab-case .md)
│   ├── sections-final/                ← Approved Word .docx exports
│   ├── figures/                       ← SVG + PNG architecture/results diagrams
│   ├── analysis/                      ← Jupyter notebooks & EDA outputs
│   ├── outline.md                     ← Chapter structure & page budgets
│   └── references.md                  ← APA 7 bibliography (living doc)
│
├── utility_scripts/                   ← Tooling-only helper scripts (never thesis content)
│   ├── scripts/                       ← notebooklm_ingestion.py, zotero_client.py, test_group.py, ml_retraining/
│   ├── integrations/                  ← integration helper scripts
│   ├── src/                           ← google_drive_integration.py
│   └── tests/                         ← unit tests for utility scripts
│
├── user-docs/                         ← All non-thesis documentation (see below)
├── plans/                             ← P-ID dated session plan folders (see workflow-planning-with-files.md)
└── worktrees/                         ← Git worktrees for parallel sessions (gitignored)
```

See [.claude/rules/repo-tier-structure.md](../../.claude/rules/repo-tier-structure.md) for the authoritative tier-by-tier rules (what goes where, what NOT to mistake for bloat).

---

## `user-docs/` Structure

```
user-docs/
├── architecture/          ← System A/B design docs, ADRs, feature engineering design
├── contributing/          ← This file, git-branch-strategy.md, worktrees guide, CHEATSHEET.md
├── reference/              ← CHEATSHEET.md, zotero-quick-reference.md, integration-quick-reference.md
├── integration/            ← Zotero setup + tooling-issues.md (living log, source: .claude/logs/tooling-issues.jsonl)
├── integrations/           ← Google Drive / NotebookLM / Nielsen integration docs (distinct from integration/ above)
├── handover/               ← Dated handover docs (YYYY-MM-DD or YYYY_MM_DD prefix)
├── handovers/              ← Cross-person handover docs (note: separate from handover/ — not yet reconciled)
├── analysis/               ← EDA and preprocessing comparison docs
├── literature/             ← Working literature files (bibtex/citations snapshots)
├── notes/                  ← Dated session notes
├── planning/               ← Implementation plans (time-bound)
├── project-management/     ← context.md (session log)
└── .archive/               ← Superseded handovers, tasks, thesis docs
```

> **Known drift, not yet resolved:** `handover/` vs `handovers/` and `integration/` vs `integrations/` are separate folders with different content, not simple duplicates. Flagged for a future consolidation pass — do not assume one supersedes the other without checking contents first.

---

## Key File Locations

| What | Where |
|------|-------|
| Session start (read first) | `CLAUDE.md` (Claude Code) / `AGENTS.md` (other agents) |
| Repo tier structure (authoritative) | `.claude/rules/repo-tier-structure.md` |
| Research questions | `01_thesis_research/research-questions/` |
| Project state & constraints | `00_thesis_context/thesis-topic/project-state.md` |
| CBS compliance requirements | `00_thesis_context/formal-requirements/` |
| System A/B architecture | `user-docs/architecture/architecture.md` |
| Tooling issues (living log) | `user-docs/integration/tooling-issues.md` |
| Thesis chapter sections | `05_thesis_writing/sections-drafts/` |
| Paper corpus | `01_thesis_research/literature/` |
| BibTeX bibliography | `01_thesis_research/literature/bibtex.bib` |
| Experiment/SRQ results | `04_thesis_results/srq{1,2,4}/` |
| Nielsen data scripts | `02_thesis_data/nielsen/scripts/` |
| CLI quick reference | `user-docs/reference/CHEATSHEET.md` |
| Zotero quick reference | `user-docs/reference/zotero-quick-reference.md` |
| Path constants (never hardcode) | `PATHS.py` |

---

## System A vs System B

| | System A | System B |
|--|----------|----------|
| **Location** | `03_thesis_modelling/model_training/` + `model_serving/system_a_forecast/` | `03_thesis_modelling/model_serving/system_b_conversational/` + `.claude/` agents |
| **Status** | Research artefact — the thing being evaluated | Thesis tooling — helps write the thesis |
| **Purpose** | Multi-agent forecasting system (SRQ1/SRQ2) | Internal writing/production scaffolding |
| **Modify?** | Care required — changes affect thesis results | Yes — freely extend |
| **In thesis?** | Yes | No — invisible to reader |
