# Plans Index

> **Scheme updated 2026-06-22**: Flat folder layout replaces status-bucket folders.
> New plans: `plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/`
> Archived plans: `plans/.archive/`
> Status tracked in plan frontmatter only — no outcome files, no folder movement on status change.
> Next available P-ID: **P0032**

---

## Active Plans

### Focus / In Progress

| P-ID | Folder | Status | Detail |
|------|--------|--------|--------|
| **P0031** | `P0031_2026-07-13_18-29_csd-eda-remaining-gaps/` | in_progress | Post-P0030 EDA review found 5 remaining gaps in the (working, migrated) CSD notebook: ACF/PACF lag-consensus unwired, CSD's zero promo signal undocumented, cross-brand heterogeneity verdict not persisted to findings JSON, sales_value/sales_liters redundancy with sales_units unexamined, stale CELL-N print headers. 6 tasks (5 independent + 1 final re-verification), none started. Priority: Task 4 (redundancy) first per real modeling risk. |
| **P0030** | `P0030_2026-07-13_14-08_csd-notebook-consolidation/` | complete | Migrated CSD's 7-stage preprocessing pipeline + EDA stage into one combined Jupyter notebook (`pre_processing_notebook_csd.ipynb`). All 8 tasks complete; Brian re-ran end-to-end successfully. Original 7 `.py` scripts archived to `.archive/`. Post-migration hardening added: auto-detected structural break scan, zero-run flags, per-category log-transform gate, non-blocking plots. Superseded by P0031 for further EDA-completeness work. |
| **P0029** | `P0029_2026-07-13_13-26_chatgpt-eda-gap-analysis-reconciliation/` | in_progress | Reconcile a ChatGPT-generated gap analysis of `pre_csd_1.5_eda.py` (single-file input, no dataset/repo access) against ground truth — triage each claim as already-resolved-in-P0027 / context-blind-false-positive / needs-verification, then verify before any fix. Feeds back into P0027's paused Phase 5 decision. Waiting on Brian to paste the analysis text. |
| **P0028** | `P0028_2026-07-10_restructure-thesis-enrico-integration/` | in_progress | Full repo-root restructure (grew from thesis/data-only scope): flatten `thesis/` prefix to root, renumber 00_thesis_context→01_thesis_research→02_thesis_data→03_thesis_modelling→04_thesis_results→05_thesis_writing, split utility_scripts/ into real tooling vs. relocated thesis-pipeline code (model_training/model_serving), archive Enrico's stray root results/+reports/, centralize all paths in PATHS.py. 8 phases, ~9.5 hrs total; tree design locked after 4 rounds of critique. |
| **P0027** | `P0027_2026-07-10_15-30_csd-eda-reconciliation/` | in_progress | Verify Enrico's 2026-07-01 merge handover claims (SRQ1-4 track); rigor pass on CSD EDA (KPSS, missingness mechanism, distribution shift); region-grain WMAPE test; then extend to danskvand/energidrikke/RTD. **2026-07-11**: found a real leakage bug (shared `engineer_features.py` groups by `brand` only, not `brand`+`market_id` — region-grain lag/rolling features conflate across regions) that blocks trusting Phase 3's 21.2% WMAPE result; added Phase 4a (fix) and Phase 4b (add chain branch alongside region) before Phase 5 can proceed. **2026-07-12**: compared colleague's standalone `02_thesis_data/preprocessing/` scripts vs. the CSD orchestrator — archived the former to `.archive/enrico_legacy_preprocessing_2026-07/` (branch `chore/archive-colleague-preprocessing`, not yet committed); also found `_03_engineered/{bymonth,bychain}/CSD/` are currently empty, so `srq1_benchmark.py` can't run yet even after the leakage fix — added a regenerate-to-canonical-path step to Phase 4a. Resume with the group_keys fix. |
| **P0026** | `P0026_2026-06-30_16-38_aggregation-grain-analysis/` | complete | Implemented brand×region×period grain (9 DVH geographic regions, MIN_PERIODS=24). CSD pipeline: 25,124 rows / 571 series — 10.6× more data than previous grain. NOTE: since rejected by Enrico pending WMAPE test, see P0027. |
| **P0024** | `P0024_2026-06-30_12-40_market-filter-fix/` | complete | Fix DVH EXCL. HD market filter across all 5 Nielsen category preprocessing pipelines (CSD, Danskvand, Energidrikke, RTD, Totalbeer) |
| **P0023** | `P0023_2026-06-30_12-38_csd-eda-critique/` | in_progress | EDA critique from predictive ML + FMCG perspective; 13 issues across P0/P1/P2; output doc pending |
| **P0022** | `P0022_2026-05-07_10-00_preprocessing-pipeline-modularization/` | in_progress | Phase 5 next: EDA replication for Energidrikke, Danskvand, RTD (data folder now clean) |
| **P0017** | `P0017_2026-04-27_14-20_jupyter-notebook-path-centralization/` | in_progress | Path infra complete; remaining: notebook template (comparison §1-5, 7+ notebooks); data folder cleanup needed first |

### Blocked

| P-ID | Folder | Blocked By |
|------|--------|------------|
| **P0005** | `P0005_2026-04-23_08-00_system-a-feature-eng-integration/` | Decision needed: packaging fix Option A vs B |

### Paused

| P-ID | Folder | Waiting On |
|------|--------|------------|
| **P0019** | `P0019_2026-05-04_14-00_root-documentation-boundary-and-folder-cleanup/` | P0022 + P0017 completion |
| **P0020** | `P0020_2026-05-04_14-30_rule-system-reform/` | P0019 Phase 4 |

### Backlog

| P-ID | Folder | Description |
|------|--------|-------------|
| **P0001** | `P0001_2026-04-13_08-00_cmt-master-upgrade-plan/` | CMT Master Upgrade |
| **P0002** | `P0002_2026-04-13_08-00_notebooklm-integration-plan/` | NotebookLM Integration |
| **P0003** | `P0003_2026-04-13_08-00_pta-best-practices-extraction/` | PTA Best Practices Extraction |
| **P0004** | `P0004_2026-04-13_08-00_thesis-repo-upgrade-plan/` | Thesis Repo Upgrade |

---

## Archived Plans

See `plans/.archive/README.md` for the full list. Archived: P0006, P0007, P0008, P0009, P0010, P0011, P0012, P0013, P0014, P0015, P0016, P0018.

---

## How to Create a New Plan

1. Next P-ID: **P0023**
2. Create folder: `plans/P0023_YYYY-MM-DD_HH-mm_<slug>/`
3. Create files: `task_plan.md`, `findings.md`, `progress.md` (use `/planning-with-files` skill)
4. Add to this index
5. Set frontmatter: `pid`, `created`, `updated`, `status`, `focus_detail` (if applicable)

## How to Archive a Plan

Move entire folder to `plans/.archive/` and update this index.

---

**Last updated**: 2026-06-22 (Scheme migration: bucket folders → flat layout; P0001–P0022 migrated)
