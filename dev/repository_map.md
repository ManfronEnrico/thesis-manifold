# Repository Map — CMT_Codebase

> Fast session orientation. Read this after CLAUDE.md at the start of every session.
> Last updated: 2026-04-13

---

## Top-Level Structure

```
CMT_Codebase/
├── .claude/                        ← Claude Code operating environment
│   ├── hooks/check_file_edit.py    ← OneDrive .py corruption + .env safety enforcer
│   ├── rules/                      ← 8 auto-loaded workflow rule files
│   ├── skills/                     ← 7 slash command skills
│   ├── plans/                      ← YYYY-MM-DD dated plan files + Outcomes
│   ├── commands/                   ← REV, REV-brian agents
│   ├── settings.json               ← PreToolUse hook registration
│   └── settings.local.json         ← Machine-local permissions (do not overwrite)
│
├── ai_research_framework/          ← SYSTEM A: research computation (thesis subject)
│   ├── config.py                   ← 8GB RAM constraint, model list, LLM config
│   ├── agents/                     ← 4 research agents (blocked on Nielsen data)
│   ├── core/coordinator.py         ← LangGraph StateGraph orchestrator
│   ├── state/research_state.py     ← LangGraph TypedDict (ResearchState)
│   ├── data/nielsen_connector.py   ← Nielsen SQL connector (access TBD)
│   └── templates/base_config.py   ← Base configuration template
│
├── thesis_production_system/       ← SYSTEM B: thesis writing tooling (not the thesis)
│   ├── agents/                     ← 10 production agents (all implemented)
│   │   ├── builder/                ← 6-file builder subsystem (ADR-003 decision pending)
│   │   ├── writing_agent.py        ← Bullet points ONLY — never prose
│   │   ├── compliance_agent.py     ← CBS formal checks
│   │   ├── literature_agent.py     ← Corpus management, scraping
│   │   └── [7 other agents]
│   ├── core/coordinator.py         ← Plan→Execute→Critic loop
│   └── state/thesis_state.py       ← Pydantic ThesisState
│
├── Thesis/                         ← Obsidian vault (human knowledge base)
│   ├── papers/                     ← 24 annotated Obsidian notes
│   ├── Thesis Guidelines/          ← CBS guideline PDFs (gitignored)
│   ├── prometheus_data_model-1.md  ← Nielsen star schema
│   └── indeksdanmark_data_model-1.md ← Indeks Danmark structure
│
├── docs/
│   ├── thesis/
│   │   ├── sections/               ← 13 Markdown chapter files (all bullet skeletons complete)
│   │   │   ├── ch1_introduction.md
│   │   │   ├── ch2_literature_review.md
│   │   │   ├── ch3_methodology.md
│   │   │   ├── ch4_data_assessment.md
│   │   │   ├── ch5_framework_design.md
│   │   │   ├── ch6_model_benchmark.md
│   │   │   ├── ch7_synthesis.md
│   │   │   ├── ch8_evaluation.md
│   │   │   ├── ch9_discussion.md
│   │   │   ├── ch10_conclusion.md
│   │   │   ├── abstract.md
│   │   │   ├── ai_declaration.md
│   │   │   └── frontpage.md
│   │   ├── figures/                ← 6 diagrams (SVG + PNG): agent_workflow, confidence_score, data_flow, project_overview, ram_budget, system_architecture
│   │   └── outline.md              ← 10-chapter approved structure
│   ├── literature/
│   │   ├── papers/                 ← 49 annotated .md files (authoritative citation count)
│   │   ├── guides/                 ← NotebookLM study guide cache (Markdown, auto-generated, NOT citable)
│   │   ├── gap_analysis.md         ← Gap identification + novelty claim (v3)
│   │   ├── rq_evolution.md         ← RQ version history (v1 → v2)
│   │   └── scraping_log.md         ← Literature Scraping Agent log
│   ├── compliance/
│   │   ├── cbs_guidelines_notes.md ← CBS formal requirements (extracted from 9 PDFs)
│   │   ├── integrity_checklist.md  ← [TODO Phase 4] 7-mode AI failure checklist
│   │   └── compliance_checks/      ← ComplianceAgent section outputs
│   ├── decisions/                  ← ADR files (Architecture Decision Records)
│   │   ├── ADR-001-template-strategy.md   ← CBS LaTeX template decision [OPEN]
│   │   ├── ADR-002-build-pipeline.md      ← Pandoc vs Overleaf decision [OPEN]
│   │   └── ADR-003-builder-agent-fate.md  ← Keep or remove builder agent [OPEN]
│   ├── data/
│   │   ├── nielsen_assessment.md   ← Nielsen data model + access status
│   │   └── indeksdanmark_notes.md  ← Indeks Danmark structure + memory estimate
│   ├── experiments/
│   │   ├── experiment_registry.json ← All experiment records (append-only)
│   │   └── experiment_summary.md   ← Auto-generated summary
│   ├── tasks/
│   │   ├── data_assessment.md      ← Phase 1 plan
│   │   ├── model_benchmark.md      ← SRQ1 results (empty — pending data)
│   │   ├── synthesis_module.md     ← SRQ2 design (empty — pending Phase 4)
│   │   ├── validation_report.md    ← Validation results (empty — pending Phase 5)
│   │   └── thesis_state.json       ← ThesisState persistence (System B state)
│   ├── tooling-issues.md           ← Living registry of env/tooling issues
│   ├── architecture.md             ← Framework architecture decisions
│   ├── context.md                  ← Session log
│   └── system_architecture_report.md ← Full 10-section architecture report
│
├── scripts/
│   ├── explore_nielsen.py          ← Nielsen data exploration (existing)
│   ├── check_integrity.py          ← [TODO Phase 4] Gate 1/2/3 integrity checks
│   └── export_notebooklm.py        ← [TODO Phase 4] Batch Markdown → NotebookLM export
│
├── project_updates/                ← Standup lifecycle + session memory
│   ├── standup_draft.md            ← Live active draft (Meeting 1)
│   ├── standup_draft_archive.md    ← Previous meeting archive (carry-over source)
│   └── standup_draft_formatting.md ← Gold standard template (never overwritten)
│
├── dev/
│   └── repository_map.md           ← This file
│
├── papers/                         ← PDF source files for NotebookLM ingestion
│   ├── ch2-literature/             ← All confirmed papers (cross-corpus QA)
│   ├── ch3-methodology/            ← DSR + ML methodology papers
│   ├── ch4-models/                 ← Forecasting model papers
│   ├── ch5-synthesis/              ← Consumer signal / sentiment papers
│   ├── ch6-evaluation/             ← Calibration + evaluation papers
│   └── ingestion_manifest.json     ← Maps paper slugs → NotebookLM source IDs + notebook IDs
│
├── tests/
│   └── test_builder_integration.py ← Builder integration tests
│
├── generate_figures.py             ← Graphviz + Matplotlib figure generation
├── CLAUDE.md                       ← Navigation hub + thesis rules
├── CHEATSHEET.md                   ← Quick-reference commands and triggers
├── README.md                       ← User-facing project documentation
├── README_builder.md               ← Builder agent documentation
└── .gitignore                      ← Excludes: .env, CSVs, PDFs, LaTeX artifacts, Obsidian ws
```

---

## Agent Quick Reference

### System A — AI Research Framework

| Agent | File | Status | Blocks |
|-------|------|--------|--------|
| Research Coordinator | `ai_research_framework/core/coordinator.py` | ✅ Skeleton | — |
| Data Assessment Agent | `ai_research_framework/agents/data_assessment_agent.py` | ⬜ Blocked | Nielsen data |
| Forecasting Agent | `ai_research_framework/agents/forecasting_agent.py` | ⬜ Blocked | Data + models |
| Synthesis Agent | `ai_research_framework/agents/synthesis_agent.py` | ⬜ Partial | Phase 4 |
| Validation Agent | `ai_research_framework/agents/validation_agent.py` | ⬜ Blocked | A1–A3 |

### System B — Thesis Production System

| Agent | File | Status |
|-------|------|--------|
| Thesis Coordinator | `thesis_production_system/core/coordinator.py` | ✅ |
| Writing Agent | `thesis_production_system/agents/writing_agent.py` | ✅ (bullets only) |
| Literature Agent | `thesis_production_system/agents/literature_agent.py` | ✅ Partial |
| Compliance Agent | `thesis_production_system/agents/compliance_agent.py` | ✅ |
| Diagram Agent | `thesis_production_system/agents/diagram_agent.py` | ✅ |
| Builder (6 files) | `thesis_production_system/agents/builder/` | ⚠️ ADR-003 pending |
| [6 other agents] | `thesis_production_system/agents/` | ✅ |

---

## Key Decision Points (Open)

| Decision | ADR | Status |
|----------|-----|--------|
| CBS LaTeX template (A4, font, margins) | ADR-001 | OPEN — extract from Thesis Guidelines/ PDFs |
| Build pipeline (Pandoc local vs. Overleaf) | ADR-002 | OPEN — confirm Overleaf sync preference |
| Builder agent fate (keep 6 files or remove) | ADR-003 | OPEN — lean toward keep + SKILL.md |

---

## Phase Status

| Phase | Goal | Status |
|-------|------|--------|
| Pre-Phase | .claude/ infrastructure | ✅ Complete (2026-04-13) |
| Phase 1 | Architecture decisions (ADRs) | 🔄 In progress |
| Phase 2 | Quick wins + cleanup | 🔄 Partial (gitignore ✅, CLAUDE.md ✅, CHEATSHEET.md ✅) |
| Phase 3 | LaTeX/PDF pipeline | ⬜ Pending Phase 1 decisions |
| Phase 4 | Integrity gates + validation | ⬜ Pending Phase 3 |
| Phase 5 | Workflow hardening | ⬜ Pending data |
