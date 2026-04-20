---
name: Complete Skills Inventory
description: Reference guide for all skills by category and use case
version: 2.0
date: 2026-04-20
---

# Complete Skills Inventory

Quick reference organized by category with chapter alignment and use cases.

---

## Table of Contents

1. [ML & Time Series Forecasting](#ml--time-series-forecasting)
2. [Data Analysis & Exploration](#data-analysis--exploration)
3. [Explainability & Interpretation](#explainability--interpretation)
4. [Visualization & Figures](#visualization--figures)
5. [Research Quality & Writing](#research-quality--writing)
6. [Advanced Research Pipelines](#advanced-research-pipelines)
7. [Standup & Project Management](#standup--project-management)
8. [Literature & Reference Management](#literature--reference-management)
9. [Utilities & Tools](#utilities--tools)

---

## ML & Time Series Forecasting

**Category**: Core research (SRQ1, Chapter 6)
**Priority**: Tier 1 (Critical)

### /aeon
**Time Series Machine Learning**
- **Description**: Deep learning & ensemble forecasting for time series classification, regression, forecasting, anomaly detection
- **Use for**: Ch. 6 — Multiple forecasting methods comparison (System A vs. baselines)
- **Key features**: AutoML pipelines, ensemble methods, neural networks
- **Chapter alignment**: SRQ1, Chapter 6
- **Demo**: `aeon.forecasting.ensemble.AutoEnsemble` on Nielsen 7-day forecast
- **Read first**: `.claude/skills/aeon/SKILL.md`

### /scikit-learn
**Machine Learning Library**
- **Description**: Classical ML with supervised learning (classification, regression, clustering)
- **Use for**: Ch. 6-7 — Baseline comparison (logistic regression, random forest, SVM)
- **Key features**: Pipeline API, preprocessing, model selection, metrics
- **Chapter alignment**: SRQ4 ("How does System A compare to traditional ML?")
- **Demo**: Train logistic regression on aggregated Nielsen data
- **Read first**: `.claude/skills/scikit-learn/SKILL.md`

### /pymc
**Bayesian Modeling**
- **Description**: Probabilistic programming with MCMC, variational inference, posterior predictive
- **Use for**: Ch. 6-8 — Uncertainty quantification, posterior distributions
- **Key features**: Hierarchical models, NUTS sampler, LOO cross-validation
- **Chapter alignment**: SRQ2 (multi-agent coordination under uncertainty)
- **Demo**: Hierarchical regression with confidence bands
- **Read first**: `.claude/skills/pymc/SKILL.md`

### /statsmodels
**Statistical Models**
- **Description**: Classical statistical models (OLS, GLM, ARIMA, GARCH, time series)
- **Use for**: Ch. 6 — Statistical baselines (ARIMA, seasonal decomposition)
- **Key features**: ARIMA, GARCH, mixed effects, hypothesis testing
- **Chapter alignment**: SRQ1 (statistical forecasting baseline)
- **Demo**: ARIMA(1,1,1) on Nielsen demand series
- **Read first**: `.claude/skills/statsmodels/SKILL.md`

---

## Data Analysis & Exploration

**Category**: Data preparation (Chapter 4)
**Priority**: Tier 1 (Critical)

### /data-eda
**Automated Data Profiling**
- **Description**: Comprehensive EDA on 200+ file formats (CSV, Excel, Parquet, etc.)
- **Use for**: Ch. 4 — Nielsen data quality assessment, missing values, outliers
- **Key features**: Auto-profiling, missing value analysis, distribution visualization
- **Chapter alignment**: Chapter 4 ("Data Characteristics")
- **Demo**: Profile 120K SKU dataset in ~30 seconds
- **Read first**: `.claude/skills/data-eda/SKILL.md`

### /polars
**High-Performance Data Wrangling**
- **Description**: Lazy-execution DataFrame library (5-10x faster than pandas)
- **Use for**: Ch. 4-6 — Aggregate Nielsen to thesis-relevant dimensions
- **Key features**: Lazy evaluation, streaming, partitioning, aggregation
- **Chapter alignment**: "8GB RAM constraint optimization"
- **Demo**: Aggregate 2M rows to 1K summary rows
- **Read first**: `.claude/skills/polars/SKILL.md`

### /stats-analysis
**Statistical Test Selection**
- **Description**: Guided statistics with automatic test selection (ANOVA, t-test, Kruskal-Wallis)
- **Use for**: Ch. 6-8 — Compare forecasting methods statistically
- **Key features**: Test selection guide, reporting, effect sizes
- **Chapter alignment**: SRQ4 (statistical comparison protocols)
- **Demo**: Run Wilcoxon signed-rank test on method A vs. B
- **Read first**: `.claude/skills/stats-analysis/SKILL.md`

---

## Explainability & Interpretation

**Category**: Model explanation (SRQ2, Chapter 8)
**Priority**: Tier 1 (Critical)

### /shap
**Model Explainability (SHAP Values)**
- **Description**: Feature importance, decision explanation, interaction effects
- **Use for**: Ch. 8 — Why does System A make specific predictions?
- **Key features**: Force plots, dependence plots, SHAP values, interaction effects
- **Chapter alignment**: SRQ2 ("How can multi-agent systems explain their decisions?")
- **Demo**: Explain 3 System A predictions with SHAP force plots
- **Read first**: `.claude/skills/shap/SKILL.md`

### /networkx
**Network Analysis & Visualization**
- **Description**: Graph analysis, network topology, shortest paths, centrality
- **Use for**: Ch. 5 — Visualize agent coordination architecture
- **Key features**: Network metrics, community detection, layout algorithms
- **Chapter alignment**: Chapter 5 (System A architecture)
- **Demo**: Draw agent dependency graph with communication flow
- **Read first**: `.claude/skills/networkx/SKILL.md`

### /scientific-critical-thinking
**Scientific Claim Evaluation**
- **Description**: Assess experimental design, evidence quality, logical validity
- **Use for**: Ch. 2-3 — Evaluate paper claims, prevent hallucinated conclusions
- **Key features**: Design validity checks, evidence grading, bias detection
- **Chapter alignment**: Chapter 2 (Literature quality)
- **Demo**: Evaluate 5 claims from sample papers
- **Read first**: `.claude/skills/scientific-critical-thinking/SKILL.md`

---

## Visualization & Figures

**Category**: Publication-ready figures (Chapters 1-10)
**Priority**: Tier 1 (Critical)

### /matplotlib
**Low-Level Plot Control**
- **Description**: Fine-grained control over every plot element (color, size, style)
- **Use for**: Multi-panel figures, custom layouts, non-standard plots
- **Key features**: OO interface, subplots, 3D, animation, export (PNG/PDF/SVG)
- **Chapter alignment**: All chapters (1-10) for publication figures
- **Demo**: Create 2×2 subplot panel with shared axis labels
- **Read first**: `.claude/skills/matplotlib/SKILL.md`

### /seaborn
**Statistical Visualization**
- **Description**: High-level plots built on matplotlib (distributions, relationships, categorical)
- **Use for**: Ch. 4 — Quick exploratory plots (histograms, violin, pairplot)
- **Key features**: Theme integration, categorical plots, heatmaps, aesthetics
- **Chapter alignment**: Chapter 4 (Exploratory analysis)
- **Demo**: Create violin plot + heatmap of Nielsen correlations
- **Read first**: `.claude/skills/seaborn/SKILL.md`

### /scientific-visualization
**Meta-Skill: Journal-Ready Figures**
- **Description**: Publication-quality figure standards (multi-panel, styling, sizing)
- **Use for**: Final figures destined for journal submission
- **Key features**: Journal templates, style guides, sizing conventions
- **Chapter alignment**: All chapters (required for submission quality)
- **Demo**: Format Figure 1 (System A architecture) to Science journal specs
- **Read first**: `.claude/skills/scientific-visualization/SKILL.md`

---

## Research Quality & Writing

**Category**: Literature, writing, quality assurance (Chapters 2, 9-10)
**Priority**: Tier 1-2 (High-Value)

### /literature-review
**Systematic Literature Review**
- **Description**: Comprehensive search across PubMed, arXiv, Google Scholar, etc.
- **Use for**: Ch. 2 — Deepen literature coverage beyond current Zotero corpus
- **Key features**: Multi-source search, deduplication, relevance ranking
- **Chapter alignment**: Chapter 2 (Literature Review)
- **Demo**: Search for "deep learning + retail forecasting" across all databases
- **Read first**: `.claude/skills/literature-review/SKILL.md`

### /research-scholar-evaluation
**Literature Quality Assessment**
- **Description**: Systematically rank papers by relevance, impact, citation network
- **Use for**: Ch. 2 — Assess which papers are truly essential
- **Key features**: ScholarEval framework, citation analysis, venue rankings
- **Chapter alignment**: Chapter 2 (Literature curation)
- **Demo**: Rank current 37 papers by relevance to thesis
- **Read first**: `.claude/skills/research-scholar-evaluation/SKILL.md`

### /scientific-writing
**Full Manuscript Writing**
- **Description**: Write scientific paragraphs in full prose (alternative to bullet points)
- **Use for**: Ch. 9-10 — Discussion & Conclusion (if exploring full writing)
- **Key features**: Academic tone, paragraph structure, citation integration
- **Chapter alignment**: Chapters 9-10 (Discussion, Conclusion)
- **Demo**: Draft paragraph on System A limitations
- **Read first**: `.claude/skills/scientific-writing/SKILL.md`

### /research-grants
**Grant Proposal Writing**
- **Description**: Write competitive research proposals (NSF, NIH, DOE, DARPA)
- **Use for**: Future work section / funding implications
- **Key features**: Agency-specific templates, budget justification, impact statements
- **Chapter alignment**: Chapter 10 (Future research)
- **Demo**: Draft NSF proposal on "Retail Forecasting with 8GB RAM"
- **Read first**: `.claude/skills/research-grants/SKILL.md`

### /citation-apa
**APA 7 Citation Formatting**
- **Description**: Format, verify, and insert APA 7 citations
- **Use for**: All chapters — Ensure citation compliance
- **Key features**: Format conversion, DOI lookup, plagiarism check
- **Chapter alignment**: Compliance (CBS requirement)
- **Demo**: Format and insert citation from DOI
- **Read first**: `.claude/skills/citation-apa/SKILL.md`

---

## Advanced Research Pipelines

**Category**: Orchestrated multi-agent workflows
**Priority**: Tier 2-3 (Specialized)

### /research-deep
**13-Agent Research Orchestration**
- **Description**: Universal deep research team for rigorous academic investigation
- **Use for**: Deep dives on specific topics (e.g., "retail forecasting with constraints")
- **Key features**: Parallel agent research, synthesis, novelty detection
- **Chapter alignment**: Extended literature work (if time permits)
- **Demo**: Research "time series with memory constraints" across 13 perspectives
- **Read first**: `.claude/skills/research-deep/SKILL.md`

### /research-hypothesis-generation
**Data-Driven Hypothesis Synthesis**
- **Description**: Automatically generate hypotheses from observed data patterns
- **Use for**: Ch. 5-7 — Discover unexpected findings, structure research
- **Key features**: Pattern detection, hypothesis formulation, novelty assessment
- **Chapter alignment**: Chapter 5 (System A coordination)
- **Demo**: Generate 5 hypotheses from Nielsen + forecast mismatch analysis
- **Read first**: `.claude/skills/research-hypothesis-generation/SKILL.md`

### /academic-pipeline
**10-Stage Research Validation Pipeline**
- **Description**: End-to-end workflow: research → write → review → integrity → publish
- **Use for**: Comprehensive quality gates before submission
- **Key features**: Stage orchestration, gate enforcement, quality metrics
- **Chapter alignment**: Final submission workflow (2 weeks before deadline)
- **Demo**: Run 10-stage validation on Chapter 6 draft
- **Read first**: `.claude/skills/academic-pipeline/SKILL.md`

### /academic-paper-reviewer
**5-Perspective Peer Review**
- **Description**: Simulate peer review from 5 independent perspectives
- **Use for**: Pre-submission review (catch issues before supervisor sees them)
- **Key features**: Role-based reviewers, structured feedback, severity ranking
- **Chapter alignment**: Final review (1 week before deadline)
- **Demo**: Run peer review on complete Chapter 6 draft
- **Read first**: `.claude/skills/academic-paper-reviewer/SKILL.md`

### /academic-paper
**12-Agent Academic Paper Writing**
- **Description**: Full paper writing pipeline with 10 modes (full draft, outline, revision, etc.)
- **Use for**: Systematic paragraph generation if moving away from "bullets only"
- **Key features**: Mode selection, multi-agent writing, coherence checking
- **Chapter alignment**: Chapters 9-10 (if exploring full prose)
- **Demo**: Generate outline for Chapter 6
- **Read first**: `.claude/skills/academic-paper/SKILL.md`

---

## Standup & Project Management

**Category**: Session tracking and documentation
**Priority**: Tier 1 (Required)

### /standup-init
**Initialize Standup Draft**
- **Description**: Create new standup draft for next supervisor meeting
- **Use for**: Start of multi-session work block
- **Key features**: Auto-carry forward unchecked tasks, backlog items
- **Trigger**: "init standup", "initialize standup"
- **Read first**: `.claude/skills/standup-init/SKILL.md`

### /standup-log
**Log Session to Standup**
- **Description**: Append current session entry to standup_draft.md
- **Use for**: End of every session to track progress
- **Key features**: Auto-timestamp, work summary, blockers
- **Trigger**: "log standup" (auto-fires at session end if changes detected)
- **Read first**: `.claude/skills/standup-log/SKILL.md`

### /standup-prep
**Prepare Standup for Meeting**
- **Description**: Draft non-technical summary and create meeting-ready copy
- **Use for**: 1 day before supervisor meeting
- **Key features**: Summary generation, formatting, clean copy
- **Trigger**: "prep standup", "prepare standup"
- **Read first**: `.claude/skills/standup-prep/SKILL.md`

### /standup-finalize
**Finalize Standup**
- **Description**: Overwrite meeting file with final version, archive draft
- **Use for**: Right before supervisor meeting
- **Key features**: Archive previous version, update CLAUDE.md
- **Trigger**: "finalize standup"
- **Read first**: `.claude/skills/standup-finalize/SKILL.md`

---

## Literature & Reference Management

**Category**: Zotero integration and academic sources
**Priority**: Tier 1 (In Progress)

### /pyzotero
**Zotero API Integration**
- **Description**: Interact with Zotero libraries (read, create, update, delete items)
- **Use for**: Sync group library (6479832) with thesis
- **Key features**: Item retrieval, collection management, attachment handling
- **Status**: Phase 1 complete (39 items, 11 papers)
- **Read first**: `.claude/skills/pyzotero/SKILL.md`

### /notebooklm
**Google NotebookLM Query**
- **Description**: Source-grounded answers from NotebookLM notebooks
- **Use for**: Literature synthesis with citation backs
- **Key features**: Browser automation, notebook selection, question answering
- **Status**: Active (set up with thesis notebooks)
- **Read first**: `.claude/skills/notebooklm/SKILL.md`

---

## Utilities & Tools

**Category**: Infrastructure and meta-skills
**Priority**: Tier 1 (Required)

### /git-draft-commit
**Generate Git Commit Message**
- **Description**: Create ready-to-paste commit message from session changes; delegates worktree setup to /git-worktrees
- **Use for**: End of work session — generate and review the message
- **Key features**: Conventional commits, trailers, branch/worktree check
- **Trigger**: "draft commit", "git commit message", "prepare commit"
- **Read first**: `.claude/skills/git-draft-commit/SKILL.md`

### /git-commit
**Execute Git Commit**
- **Description**: Stage files and submit an approved commit message (PowerShell-safe)
- **Use for**: After /git-draft-commit message is approved
- **Key features**: Staging choices, confirmation gate, post-commit checklist
- **Trigger**: "commit this", "run the commit", "submit the commit"
- **Read first**: `.claude/skills/git-commit/SKILL.md`

### /git-worktrees
**Git Worktree Session Setup**
- **Description**: Create isolated `.cc/worktrees/<slug>` workspace with project branch conventions
- **Use for**: Start of any session needing isolation
- **Key features**: Gitignore check, branch naming, mismatch detection
- **Trigger**: "set up worktree", "create worktree", "isolate session"
- **Read first**: `.claude/skills/git-worktrees/SKILL.md`

### /docs-update-all
**Update Living Documentation**
- **Description**: Sync all project docs in order (sections → compliance → CLAUDE.md → plans)
- **Use for**: End of phase to keep docs current
- **Key features**: Phase-aware updates, change tracking
- **Trigger**: "update all docs"
- **Read first**: `.claude/skills/docs-update-all/SKILL.md`

### /plan-update
**Log Plan Outcome**
- **Description**: Finalize plan by documenting completed/adjusted/dropped items
- **Use for**: After plan execution
- **Key features**: Outcome file creation, auto-relocation to proper directory
- **Trigger**: "update plan [name]"
- **Read first**: `.claude/skills/plan-update/SKILL.md`

### /errors-log
**Log Tooling Issues**
- **Description**: Scan conversation for error→solution sequences, append to JSONL
- **Use for**: Capture Windows/OneDrive/tooling issues for future reference
- **Key features**: Deduplication, JSONL schema, markdown rebuild
- **Trigger**: "log errors", "update tooling"
- **Read first**: `.claude/skills/errors-log/SKILL.md`

### /skill-creator
**Create Custom Skills**
- **Description**: Define new skills, modify existing skills, run evals (community skill)
- **Use for**: If extending thesis capabilities
- **Key features**: Skill definition templates, eval framework
- **Read first**: `.claude/skills/skill-creator/SKILL.md`

### /test-codebase-integrity
**Integration Testing (10 tests)**
- **Description**: Test entire System A+B codebase (agents, LangGraph, models)
- **Use for**: Verify system stability after changes
- **Status**: All 10 tests passing
- **Read first**: `.claude/skills/test-codebase-integrity/SKILL.md`

### /ml-audit-repo
**Evidence-Driven ML Repository Verification**
- **Description**: Treats every Claude Code claim as a hypothesis to test. Staged audits across code executability, data reality, training authenticity, and metric validity.
- **Use for**: Before model releases, after heavy Claude Code sessions, pre-merge gate for ML workflows
- **Key features**: Claim verdicts, hallucination detection (12 checks), 100-point scoring rubric
- **Levels**: `quick` (15–30 min) | `standard` (2–6h) | `forensic` (1–3 days)
- **Trigger**: "audit ml repo", "quick audit", "verify training"
- **Read first**: `.claude/skills/ml-audit-repo/SKILL.md`

### /thesis-structuring
**Outline Evolution**
- **Description**: Maintain thesis outline in pattern-aware, disciplined way
- **Use for**: Evolve chapter structure, add sections
- **Key features**: Bullet-to-prose conversion tracking
- **Read first**: `.claude/skills/thesis-structuring/SKILL.md`

### /workspace-audit
**Repository Health Audit (read-only)**
- **Read first**: `.claude/skills/workspace-audit/SKILL.md`

### /workspace-cleanup
**Repository Fixer**
- **Read first**: `.claude/skills/workspace-cleanup/SKILL.md`

### /workspace-enforce
**CI Gate for Workspace Health**
- **Read first**: `.claude/skills/workspace-enforce/SKILL.md`

### /repo-hygiene
**Repository Root & Markdown Hygiene**
- **Read first**: `.claude/skills/repo-hygiene/SKILL.md`

---

## Quick Activation Reference

**"I need to explore Nielsen data"**
→ `/data-eda`, then `/seaborn`

**"I need to compare forecasting methods"**
→ `/scikit-learn`, `/aeon`, then `/statsmodels`

**"I need to understand why System A made a prediction"**
→ `/shap`, then `/scientific-critical-thinking`

**"I need to create publication figures"**
→ `/matplotlib` or `/seaborn`, then `/scientific-visualization`

**"I need to review my literature"**
→ `/literature-review`, then `/research-scholar-evaluation`

**"I need to simulate peer review"**
→ `/academic-paper-reviewer`

**"I need deep research on a topic"**
→ `/research-deep` (13-agent orchestration)

**"I need to commit my work"**
→ `/git-draft-commit` → approve → `/git-commit`

---

**Updated**: 2026-04-20 — skills renamed for domain grouping
