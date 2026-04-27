# Thesis Manifold Repository Index

**Last Updated:** 2026-04-27  
**Project:** CBS Master's Thesis 2026 (Manifold AI - Prometheus Integration)  
**Team:** Brian Rohde + Enrico Manfron  
**Deadline:** 2026-05-15

---

## Quick Start

**First time here?** Read in this order:

1. [CLAUDE.md](CLAUDE.md) — How Claude Code works in this project
2. [docs/codebase/architecture.md](docs/codebase/architecture.md) — System A/B design
3. [thesis/thesis-context/research-questions/research-questions.md](thesis/thesis-context/research-questions/research-questions.md) — What we're researching
4. [thesis/thesis-context/thesis-topic/project-state.md](thesis/thesis-context/thesis-topic/project-state.md) — Frozen decisions
5. [docs/dev/repository_map.md](docs/dev/repository_map.md) — File locations

---

## Folder Structure Overview

```
thesis-manifold/
├── CLAUDE.md                    ← Project instructions & workflows
├── README.md                    ← Project overview & setup
├── INDEX.md                     ← This file
├── config.py                    ← Root configuration
│
├── thesis/                      ← All thesis content & research code
│   ├── INDEX.md                 ← Thesis folder guide
│   │
│   ├── thesis_agents/           ← Research & production agents
│   │   ├── ai_research_framework/     # System A: Multi-agent forecasting
│   │   │   ├── agents/                # 4 research agents
│   │   │   ├── core/coordinator.py    # LangGraph orchestrator
│   │   │   ├── state/research_state.py # State management
│   │   │   ├── config.py              # RAM budget, model config
│   │   │   └── requirements.txt
│   │   │
│   │   └── thesis_production_system/  # System B: Thesis writing tooling
│   │       ├── agents/                # 10 production agents
│   │       ├── core/coordinator.py    # Plan→Execute→Critic loop
│   │       ├── state/thesis_state.py  # State management
│   │       └── requirements.txt
│   │
│   ├── thesis-context/          ← Thesis metadata & requirements
│   │   ├── research-questions/  # RQs v2 & evolution
│   │   ├── thesis-topic/        # Project state & frozen decisions
│   │   ├── formal-requirements/ # CBS guidelines & compliance
│   │   ├── chapters/            # Chapter metadata (mappings, TOC)
│   │   └── prometheus-integration/ # Prometheus integration plan
│   │
│   ├── thesis-writing/          ← Draft chapters & final prose
│   │   ├── sections-drafts/     # Bullet skeletons (all chapters)
│   │   ├── sections-final/      # Final prose versions
│   │   ├── figures/             # Diagrams, graphs, charts
│   │   ├── analysis/            # Thesis-specific analysis
│   │   └── [outline, references, etc.]
│   │
│   ├── data/                    ← Datasets (local, not in git)
│   │   ├── nielsen/             # Nielsen Fabric API data
│   │   │   ├── README.md        # Data access guide
│   │   │   ├── description/SCHEMA_SNAPSHOT.md  # Auto-generated schema
│   │   │   └── [52 CSV exports, 1.9 GB]
│   │   ├── spss_indeksdanmark/  # Indeks Danmark survey data
│   │   │   └── [20K respondents × 6.3K variables]
│   │   ├── preprocessing/       # Data pipeline & transformations
│   │   └── assessment/          # Data quality reports
│   │
│   ├── literature/              ← 49 papers & gap analysis
│   │   ├── obisdian_paper_analysis/ # Annotated papers
│   │   └── [gap_analysis.md, rq_evolution.md in docs/]
│   │
│   └── analysis/                ← Experiment outputs & notebooks
│       ├── notebooks/           # Jupyter notebooks for analysis
│       ├── outputs/             # Model predictions, metrics, plots
│       └── prompts/             # LLM prompts for agents
│
├── docs/                        ← Technical documentation
│   ├── codebase/                # Architecture & design decisions
│   ├── dev/                     # Developer guides, repository_map.md
│   ├── reference/               # Git strategy, cheatsheet, etc.
│   ├── integrations/            # Zotero, MCP, etc.
│   ├── project-management/      # Context, session logs
│   ├── tooling/                 # Known issues, environment notes
│   ├── analyses/                # Analysis reports & findings
│   ├── guides/                  # Setup, how-to docs
│   ├── tasks/                   # Task-specific docs
│   ├── experiments/             # Experiment tracking & results
│   ├── decisions/               # Architecture & approach decisions
│   ├── codebase-testing/        # Testing strategy docs
│   └── 00_archive/              # Archived/deprecated docs
│
├── scripts/                     ← CLI tools & utilities
│   ├── ml_retraining/           # Model retraining pipelines
│   └── [data_pipeline.py, etc.]
│
├── tests/                       ← Test suite
│   └── [unit & integration tests]
│
├── integrations/                ← External integrations
│   └── [Zotero, MCP, etc.]
│
├── project_updates/             ← Standup & session logs
│   └── standup_draft.md         ← Current session entries
│
├── plans/                       ← Session plans & outcomes
│   ├── plan_files/              # Active plans with timestamps
│   └── outcome_files/           # Completed plans with results
│
├── .claude/                     ← Claude Code configuration
│   ├── settings.json            # Project settings
│   ├── memory/                  # Auto-memories from sessions
│   ├── rules/                   # Workflow automation rules
│   ├── skills/                  # Project-specific skills
│   ├── hooks/                   # Custom hook scripts
│   ├── logs/                    # Tooling issues, errors (JSONL)
│   ├── agents/                  # Custom agents
│   ├── commands/                # Custom commands
│   └── docs/                    # Internal skill documentation
│
└── .archive/                    ← Old versions, backups
    ├── memory_legacy/           # Archived memory files
    └── Thesis_obsidian_backup/  # Obsidian vault backup
```

---

## Key Directories Explained

### `thesis/thesis_agents/` — Research & Production Code
**What:** System A (research framework) and System B (thesis production) agent implementations  
**Structure:**
- **System A** (`ai_research_framework/`) — 4-agent multi-model forecasting pipeline
  - DataAssessmentAgent → ForecastingAgent → SynthesisAgent → ValidationAgent
  - Models: ARIMA, Prophet, LightGBM, XGBoost, Ridge
  - RAM constraint: ≤ 8 GB total
  
- **System B** (`thesis_production_system/`) — 10-agent thesis writing system
  - ThesisCoordinator, PlannerAgent, WritingAgent, ComplianceAgent, etc.
  - **Rule:** WritingAgent produces only bullet points (never prose without approval)

### `thesis/thesis-context/` — Thesis Metadata
**What:** Research questions, compliance requirements, project state, integration plans  
**Key files:**
- `research-questions/research-questions.md` — RQs v2 (frozen)
- `thesis-topic/project-state.md` — Architecture decisions (frozen)
- `formal-requirements/compliance.md` — CBS guidelines
- `prometheus-integration/` — Deployment architecture (NEW, 2026-04-27)

### `thesis/thesis-writing/` — Thesis Content
**What:** Draft chapters, final prose, figures, references  
**Workflow:**
- `sections-drafts/` — Bullet-only skeletons (13 chapters)
- `sections-final/` — Final approved prose versions
- `figures/` — Graphviz + Matplotlib diagrams

### `thesis/data/` — Datasets
**What:** Nielsen Fabric API exports + Indeks Danmark survey data  
**Status:** Both local & accessible (2026-04-22)
- **Nielsen:** 52 Fabric objects, 29 CSV exports, 2.5M rows, 1.9 GB
- **Indeks Danmark:** 20K respondents × 6.3K variables
- **See:** [thesis/data/nielsen/README.md](thesis/data/nielsen/README.md) for access guide

### `thesis/analysis/` — Experiments & Outputs
**What:** Model training, predictions, metrics, notebooks  
- `notebooks/` — Jupyter analysis notebooks
- `outputs/` — Model predictions, performance metrics, plots
- `prompts/` — LLM prompts for agents

### `docs/` — Technical Documentation
**What:** Architecture, design decisions, developer guides  
**Key files:**
- `codebase/architecture.md` — System A/B design
- `dev/repository_map.md` — Module inventory & responsibilities
- `reference/cheatsheet.md` — CLI commands & skill triggers
- `project-management/context.md` — Session logs
- `tooling/tooling-issues.md` — Known Windows/OneDrive issues (6 documented)

### `scripts/` — CLI Tools
**What:** Data processing, model training, utilities  
- `ml_retraining/` — Retraining pipeline
- Other ETL & analysis scripts

### `plans/` — Session Planning
**What:** Session plans & completion outcomes  
- `plan_files/` — Active plans (YYYY-MM-DD_slug.md)
- `outcome_files/` — Completed plans with results

**Rule:** No outcome file = plan not completed (instant visual check)

### `.claude/` — Claude Code Configuration
**What:** Project-specific settings, rules, skills, hooks  
- `rules/` — Workflow automation (branch strategy, docs, git commit)
- `skills/` — Custom skills for this project
- `hooks/` — Custom hooks (branch guard, etc.)
- `logs/tooling-issues.jsonl` — Structured error log
- `memory/` — Session memories (auto-persists across sessions)

---

## Important Files

| File | Purpose | Status |
|------|---------|--------|
| [CLAUDE.md](CLAUDE.md) | Project instructions & workflows | ✅ Active |
| [README.md](README.md) | Project overview & setup | ✅ Current |
| [docs/codebase/architecture.md](docs/codebase/architecture.md) | System A/B design | ✅ Frozen |
| [thesis/thesis-context/research-questions/research-questions.md](thesis/thesis-context/research-questions/research-questions.md) | Research questions v2 | ✅ Frozen |
| [thesis/thesis-context/thesis-topic/project-state.md](thesis/thesis-context/thesis-topic/project-state.md) | Frozen decisions | ✅ Frozen |
| [thesis/thesis-context/formal-requirements/compliance.md](thesis/thesis-context/formal-requirements/compliance.md) | CBS requirements | ✅ Locked |
| [thesis/thesis-context/prometheus-integration/PROMETHEUS_INTEGRATION_OVERVIEW.md](thesis/thesis-context/prometheus-integration/PROMETHEUS_INTEGRATION_OVERVIEW.md) | Prometheus integration plan | 🆕 NEW (2026-04-27) |
| [docs/dev/repository_map.md](docs/dev/repository_map.md) | File → purpose mapping | ✅ Current |
| [docs/reference/cheatsheet.md](docs/reference/cheatsheet.md) | CLI commands & skills | ✅ Current |
| [docs/tooling/tooling-issues.md](docs/tooling/tooling-issues.md) | Known environment issues | ✅ Updated |
| [thesis/data/nielsen/README.md](thesis/data/nielsen/README.md) | Nielsen data access guide | ✅ Current |
| [thesis/data/nielsen/description/SCHEMA_SNAPSHOT.md](thesis/data/nielsen/description/SCHEMA_SNAPSHOT.md) | Auto-generated schema reference | ✅ Current |

---

## Workflows & Commands

### Common Tasks

| Task | Command |
|------|---------|
| Start new session | Use your branch (or create with worktree) |
| Draft a git commit | `/git-draft-commit` |
| Write a thesis section | `/write-section <id>` (after bullet approval) |
| Add a citation | `/cite` |
| Update project docs | `/docs-update-all` |
| Log standup entry | `/standup-log` |
| Test codebase | Run pytest or use skill |
| Check branch strategy | See [docs/reference/GIT_BRANCH_STRATEGY.md](docs/reference/GIT_BRANCH_STRATEGY.md) |

### Key Rules

1. **Every session gets its own branch** — never commit directly to `main`
2. **Bullets only for thesis** — WritingAgent never produces prose without explicit approval
3. **One-off execution by default** — `/loop` only if interval is explicitly specified
4. **Outcome files prove completion** — no outcome file = plan not done
5. **Python files:** Edit via temp script, not directly (hook enforces)

See [CLAUDE.md](CLAUDE.md) for full workflow details.

---

## Current Status (as of 2026-04-27)

| Component | Status | Notes |
|-----------|--------|-------|
| **Data Access** | ✅ Complete | Nielsen + Indeks Danmark local (2026-04-22) |
| **Literature Review** | 📋 In Progress | 49 papers catalogued |
| **Research Questions** | ✅ Frozen | RQs v2 finalized |
| **Project State** | ✅ Frozen | All architecture decisions locked |
| **Compliance** | ✅ Confirmed | CBS requirements met |
| **Prometheus Integration** | 🆕 Planning | New architecture doc (2026-04-27) |
| **Thesis Chapters** | 📝 Drafted | Bullet skeletons, awaiting approval |
| **Model Training** | 🚀 Next Phase | 5-model benchmark (Nielsen data) |
| **API Deployment** | 🚀 Next Phase | Expose models for Prometheus integration |
| **Submission Deadline** | ⏰ 2026-05-15 | 18 days away |

---

## Critical Dates & Deadlines

- **Today:** 2026-04-27 (Saturday)
- **Prometheus integration clarified:** 2026-04-27 ← 👈 You are here
- **Model training phase:** Next (1 week estimated)
- **API deployment:** Follow-up (3-5 days estimated)
- **Nika integration & sandbox testing:** Parallel (~1 week estimated)
- **Final testing & analysis:** ~1 week
- **Thesis submission:** 2026-05-15 (18 days away)

**Timeline is tight.** Parallel work with Nika is essential.

---

## Getting Help

- **Project questions:** Check [CLAUDE.md](CLAUDE.md)
- **File locations:** See [docs/dev/repository_map.md](docs/dev/repository_map.md)
- **Git workflows:** See [docs/reference/GIT_BRANCH_STRATEGY.md](docs/reference/GIT_BRANCH_STRATEGY.md)
- **Claude Code help:** Type `/help` in Claude Code
- **Tooling issues:** See [docs/tooling/tooling-issues.md](docs/tooling/tooling-issues.md)
- **Thesis structure:** See [thesis/INDEX.md](thesis/INDEX.md)

---

## What's New (2026-04-27)

- ✅ **Restructured INDEX.md** — Now reflects actual repo structure (thesis_agents, data, etc.)
- ✅ **Prometheus Integration Overview** — New doc clarifying architecture, meeting strategy, and deployment plan
- ✅ **Data Access Verified** — Nielsen + Indeks Danmark both local & accessible

---

## Next Steps

1. **Read** [thesis/thesis-context/prometheus-integration/PROMETHEUS_INTEGRATION_OVERVIEW.md](thesis/thesis-context/prometheus-integration/PROMETHEUS_INTEGRATION_OVERVIEW.md) before meeting with Nika
2. **Schedule meeting** with Nika (after 11 CET per her email)
3. **Clarify** deployment format, API contract, sandbox access
4. **Begin model training** (parallel with Nika's prep work)
5. **Document** model interface once agreed with Nika
6. **Deploy & iterate** (fast cycle required)

---

## Repository Stats

- **Lines of Code:** ~5000+ (agents, forecasting, feature engineering)
- **Test Coverage:** Integration tests for System A/B + forecasting
- **Papers:** 49 analyzed
- **Datasets:** Nielsen (52 objects, 29 CSVs, 2.5M rows) + Indeks Danmark (20K × 6.3K)
- **Thesis Chapters:** 13 (drafted, bullet skeletons)
- **Git Commits:** 150+ (session/thesis/chore/data branches)
