---
title: Skills Organization Structure
date: 2026-04-22
description: Logical grouping and categorization for .claude/skills
---

# Skills Organization Structure

## Overview

All 44 skills in `.claude/skills/` are organized **logically** (not as folders) into 6 groups defined in `SKILL_GROUPS.md`:

| Group | Count | Purpose |
|-------|-------|---------|
| **foundational** | 12 | Core infrastructure — copied to all repos |
| **standup** | 4 | Supervisor meeting workflow |
| **thesis-writing** | 8 | Academic writing, research, and literature |
| **data-science** | 12 | ML, statistics, EDA, data manipulation |
| **visualization** | 4 | Plotting and visual analysis |
| **research-methods** | 4 | Research evaluation, critical thinking, grants |

## Flat File Structure

Skills live **flat** in `.claude/skills/` to preserve `/` autocomplete functionality:

```
.claude/skills/
├── academic-paper/
├── academic-paper-reviewer/
├── academic-pipeline/
├── aeon/
├── citation-apa/
├── data-eda/
├── docs-update-all/
├── errors-log/
├── feature-engineering/
├── forecasting-time-series-data/
├── git-commit/
├── git-draft-commit/
├── git-worktree-merge/
├── literature-review/
├── matplotlib/
├── ml-audit-repo/
├── networkx/
├── plan-update/
├── polars/
├── pymc/
├── pyzotero/
├── repo-hygiene/
├── research-deep/
├── research-grants/
├── research-hypothesis-generation/
├── research-scholar-evaluation/
├── scientific-critical-thinking/
├── scientific-visualization/
├── scientific-writing/
├── scikit-learn/
├── seaborn/
├── shap/
├── standup-finalize/
├── standup-init/
├── standup-log/
├── standup-prep/
├── stats-analysis/
├── statsmodels/
├── test-codebase-integrity/
├── thesis-structuring/
├── using-git-worktrees/
├── workspace-audit/
├── workspace-cleanup/
└── workspace-enforce/
```

## Skill Groups (Logical Only)

See `SKILL_GROUPS.md` for the canonical grouping. Skills can be installed by group using external tools/scripts.

### foundational (12)
Git workflows, documentation sync, error tracking, planning, testing/auditing. **Install in every project.**

- git-commit
- git-draft-commit
- using-git-worktrees
- git-worktree-merge
- plan-update
- repo-hygiene
- test-codebase-integrity
- workspace-audit
- workspace-cleanup
- workspace-enforce
- errors-log
- docs-update-all

### standup (4)
Supervisor meeting workflow: initialize, log, prepare, finalize.

- standup-init
- standup-log
- standup-prep
- standup-finalize

### thesis-writing (8)
Academic paper writing, peer review, literature reviews, citation management, research orchestration.

- academic-paper
- academic-paper-reviewer
- academic-pipeline
- citation-apa
- literature-review
- research-deep
- scientific-writing
- thesis-structuring

### data-science (12)
ML models, statistical analysis, EDA, feature engineering, time series forecasting, hypothesis generation.

- aeon
- data-eda
- feature-engineering
- forecasting-time-series-data
- polars
- pymc
- pyzotero
- research-hypothesis-generation
- scikit-learn
- shap
- stats-analysis
- statsmodels

### visualization (4)
Publication-ready plots, graph analysis, scientific figures.

- matplotlib
- networkx
- scientific-visualization
- seaborn

### research-methods (4)
Grant writing, research evaluation, critical thinking, ML auditing.

- ml-audit-repo
- research-grants
- research-scholar-evaluation
- scientific-critical-thinking

## Key Points

### Skill Invocation

- Skills are invoked by **skill name**: `/git-draft-commit`, `/feature-engineering`, etc.
- `/` autocomplete works because skills are at flat level
- Trigger phrases in SKILL.md are unchanged and auto-activate
- Claude Code auto-discovers all skills at `.claude/skills/`

### Design Philosophy

This structure follows the **claude-toolkit pattern**:
- **Flat layout** preserves IDE autocomplete and discovery
- **SKILL_GROUPS.md** provides logical grouping for bulk installation
- **No physical folders** breaking the `/` command interface

### Copying to New Projects

To replicate foundational + standup skills to a new repository:

```bash
# Copy individual foundational skills
for skill in git-commit git-draft-commit using-git-worktrees git-worktree-merge \
            plan-update repo-hygiene test-codebase-integrity workspace-audit \
            workspace-cleanup workspace-enforce errors-log docs-update-all; do
  cp -r /path/to/cmt-codebase/.claude/skills/$skill /path/to/new-repo/.claude/skills/
done

# Copy standup skills
for skill in standup-init standup-log standup-prep standup-finalize; do
  cp -r /path/to/cmt-codebase/.claude/skills/$skill /path/to/new-repo/.claude/skills/
done
```

## Updates

To add a new skill:

1. Create the skill folder: `.claude/skills/<skill-name>/`
2. Add `SKILL.md`, `README.md`, and optional `handler.py`
3. Add the skill to the appropriate group in `SKILL_GROUPS.md`

To move a skill between groups, just update `SKILL_GROUPS.md` — no file moves needed.
