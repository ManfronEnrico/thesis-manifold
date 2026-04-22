# Skill Groups

This file is the source of truth for which skills belong to which group.
Skills live flat in `skills/<name>/` -- this file is purely a logical grouping.
A skill may appear in multiple groups (rare).

## foundational

The "install everywhere" set. Git workflow + plan/docs hygiene + workspace auditing + error tracking. Install these in any new Claude Code project.

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

## standup

Standup / supervisor-meeting workflow. Install in projects with a recurring stakeholder update cadence.

- standup-init
- standup-log
- standup-prep
- standup-finalize

## thesis-writing

Academic paper writing, research, and literature management. Core thesis production skills.

- academic-paper
- academic-paper-reviewer
- academic-pipeline
- citation-apa
- literature-review
- research-deep
- scientific-writing
- thesis-structuring

## data-science

Data analysis, machine learning, statistical modeling, EDA, and feature engineering.

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

## visualization

Plotting, visual analysis, and publication-ready figures.

- matplotlib
- networkx
- scientific-visualization
- seaborn

## research-methods

Research evaluation, critical thinking, hypothesis generation, and grant writing.

- ml-audit-repo
- research-grants
- research-scholar-evaluation
- scientific-critical-thinking

## How to extend

To add a new group, append a `## <group-name>` section here with a bulleted list of skill names.
To add a skill to an existing group, just append it to the group's bullet list.
