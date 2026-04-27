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
.
├── CLAUDE.md                    ← Project instructions & workflows
├── README.md                    ← Project description
├── INDEX.md                     ← This file
│
├── thesis/                      ← Thesis content (data, writing, context)
│   ├── INDEX.md                 ← Thesis folder guide
│   ├── data/                    ← Nielsen & Indeks Danmark datasets
│   ├── literature/              ← 49 papers & gap analysis
│   ├── thesis-context/          ← RQs, compliance, project state, integration
│   └── thesis-writing/          ← Draft chapters, outline, references
│
├── src/                         ← Main Python code
│   ├── agents/                  ← System A & B agent implementations
│   ├── forecasting/             ← Time series forecasting models
│   ├── feature_engineering/     ← Feature extraction & transformation
│   └── utils/                   ← Shared utilities (config, logging, etc.)
│
├── scripts/                     ← CLI tools & data processing
│   ├── data_pipeline.py         ← ETL pipeline
│   └── ...
│
├── docs/                        ← Technical documentation
│   ├── codebase/                ← Architecture, design decisions
│   ├── dev/                     ← Developer guides, repository map
│   ├── reference/               ← Git strategy, cheatsheet, etc.
│   ├── integrations/            ← Zotero, MCP, etc.
│   ├── project-management/      ← Context, session logs
│   └── tooling/                 ← Known issues, environment notes
│
├── tests/                       ← Test suite
│   ├── unit/                    ← Unit tests
│   └── integration/             ← Integration tests
│
├── thesis/analysis/outputs/     ← Experiment outputs, metrics
│   ├── forecasts/               ← Model predictions
│   ├── metrics/                 ← Performance evaluation
│   └── analysis/                ← Statistical analysis
│
├── project_updates/             ← Standup & session logs
│   └── standup_draft.md          ← Current standup entries
│
├── .claude/                     ← Claude Code configuration
│   ├── settings.json            ← Project settings
│   ├── rules/                   ← Workflow automation rules
│   ├── plans/                   ← Session plans & outcomes
│   ├── logs/                    ← Tooling issues, errors
│   └── skills/                  ← Project-specific skills
│
└── .agents/                     ← Remote agent skills (global install)
```

---

## Key Directories Explained

### `thesis/` — Thesis Content
**What:** All thesis-related content (data, literature, writing, context)  
**Status:** Active  
**See:** [thesis/INDEX.md](thesis/INDEX.md) for detailed breakdown

Key subdirectories:
- `data/` — Nielsen + Indeks Danmark datasets (local, accessible)
- `literature/` — 49 papers analyzed for RQs & methodology
- `thesis-context/` — RQs, compliance, frozen decisions, **Prometheus integration** (NEW)
- `thesis-writing/` — Draft chapters (bullet skeletons → prose)

### `src/` — Python Codebase
**What:** Main application code  
**Structure:**
- `agents/` — System A (research framework) & System B (thesis production)
- `forecasting/` — Time series models, ARIMA, ensemble methods
- `feature_engineering/` — Feature extraction from Nielsen data
- `utils/` — Shared config, logging, data loading

### `docs/` — Technical Documentation
**What:** Architecture, design decisions, developer guides  
**Key files:**
- `codebase/architecture.md` — System A/B design & integration
- `dev/repository_map.md` — What each module does
- `reference/cheatsheet.md` — CLI commands & skill triggers
- `integrations/zotero-integration-setup.md` — Bibliography integration

### `scripts/` — CLI Tools
**What:** Executable scripts for data processing, training, experiments  
**Example:** `data_pipeline.py` for ETL

### `tests/` — Test Suite
**What:** Unit & integration tests  
**Run:** `pytest` or use `/test-codebase-integrity` skill

### `thesis/analysis/outputs/` — Experiment Outputs
**What:** Model predictions, metrics, analysis plots  
**Organized by:** Forecast type, metric type, analysis date

### `project_updates/` — Standup & Logs
**What:** Session standup entries, meeting notes, progress tracking  
**Key file:** `standup_draft.md` (active session log)

### `.claude/` — Claude Code Configuration
**What:** Project-specific settings, rules, plans, logs  
**Key files:**
- `settings.json` — Project permissions & configuration
- `rules/` — Automation rules (branch strategy, docs workflow, git commit workflow)
- `plans/plan_files/` — Session plans with timestamps
- `plans/outcome_files/` — Outcome summaries (proves plan was completed)
- `logs/tooling-issues.jsonl` — Windows/OneDrive/tooling problems (source of truth)

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

---

## Workflows & Commands

### Common Tasks

| Task | Command |
|------|---------|
| Start new session | Use your branch (or create one with `/git-using-worktrees`) |
| Draft a git commit | `/git-draft-commit` |
| Write a thesis section | `/write-section <id>` (after bullet approval) |
| Add a citation | `/cite` |
| Update project docs | `/docs-update-all` |
| Prepare standup | `/standup-prep` |
| Test codebase | `/test-codebase-integrity` |
| Check branch strategy | See [docs/reference/GIT_BRANCH_STRATEGY.md](docs/reference/GIT_BRANCH_STRATEGY.md) |

### Key Rules

1. **Every session gets its own branch** — never commit directly to `main`
2. **Bullets only for thesis** — never prose without explicit approval
3. **One-off execution by default** — `/loop` only if interval is specified
4. **Outcome files prove completion** — no outcome file = plan not done
5. **Python files:** Edit via temp script, not directly (hook enforces)

See [CLAUDE.md](CLAUDE.md) for full workflow details.

---

## Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| **Data Access** | ✅ Complete | Nielsen + Indeks Danmark local (2026-04-22) |
| **Literature Review** | 📋 In Progress | 49 papers catalogued |
| **Research Questions** | ✅ Frozen | RQs v2 finalized |
| **Project State** | ✅ Frozen | All architecture decisions locked |
| **Compliance** | ✅ Confirmed | CBS requirements met |
| **Prometheus Integration** | 🆕 Planning | New architecture doc (2026-04-27) |
| **Thesis Chapters** | 📝 Drafted | Bullet skeletons, awaiting approval |
| **Model Training** | 🚀 Next Phase | Sales forecasting models (Nielsen data) |
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

- ✅ **Prometheus Integration Overview** — New doc clarifying architecture, meeting strategy, and deployment plan
- ✅ **Thesis INDEX** — Comprehensive guide to thesis folder structure
- ✅ **Root INDEX** — This file

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
- **Datasets:** Nielsen (4 categories × 16 CSVs) + Indeks Danmark (3 CSVs)
- **Thesis Chapters:** 10 (drafted, bullet skeletons)
- **Git Commits:** 150+ (session/thesis/chore/data branches)

