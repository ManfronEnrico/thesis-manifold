---
pid: P0031
created: 2026-07-13 18:29:00
updated: 2026-07-13 18:29:00
status: in_progress
focus_detail: "6 tasks created from a post-P0030 EDA review. Starting with Task 4 (sales_value/sales_liters redundancy) per Brian's priority ranking -- real modeling risk (multicollinear features silently entering the model) vs. the other tasks' documentation/cosmetic nature."
---

# P0031 — CSD Notebook: Remaining EDA Gaps

## Goal

Address 5 remaining EDA gaps identified during a full top-to-bottom review of `pre_processing_notebook_csd.ipynb` after P0030 (the notebook-consolidation migration) completed. Unlike P0030, these are not migration-correctness issues -- the notebook already runs end-to-end correctly -- these are analysis-completeness gaps: EDA cells that compute an insight but never act on it, plus one cosmetic labeling issue.

## Context

- **Direct continuation of P0030**: same notebook (`02_thesis_data/_02_preprocessing/nielsen/CSD/pipeline_step_scripts/pre_processing_notebook_csd.ipynb`), same "EDA insights must be actioned, not just printed" principle that drove P0030's log-transform-gate/zero-run-flag/structural-break-scan fixes.
- **Why a new plan instead of reopening P0030**: P0030's scope was the migration itself (8 tasks, all complete, notebook validated end-to-end by Brian). These 5 gaps were found via a fresh review *after* that migration was done and working -- distinct scope, own plan.
- **Brian's priority ranking** (given when the gaps were first identified): Task 4 (sales_value/sales_liters redundancy) is the one with real modeling risk -- worth resolving before this notebook becomes the template for Danskvand/Energidrikke/RTD. Tasks 1 and 5 are cheap cleanups. Tasks 2/3 are fine as documentation-only additions.
- **No TaskCreate/TaskList tools available this session** (confirmed via ToolSearch, same as P0030) -- tasks tracked solely via persisted `tasks/N.json` files per the dual-update protocol.

## Tasks (persisted to `tasks/`)

| ID | Title | Phase | Blocked By | Status |
|----|-------|-------|-----------|--------|
| 1 | Decide and wire ACF/PACF lag-consensus into LAGS | core | — | pending |
| 2 | Flag CSD's zero promo signal in findings output | core | — | pending |
| 3 | Forward heterogeneity verdict (CV, peak-month concentration) into findings JSON | core | — | pending |
| 4 | Resolve sales_value/sales_liters redundancy with sales_units target | core | — | pending |
| 5 | Fix stale internal CELL-N print headers to match current Step numbering | cleanup | — | pending |
| 6 | End-to-end re-verification after all P0031 EDA fixes applied | testing | 1,2,3,4,5 | pending |

Full task descriptions (file paths, exact cell references, verification steps) are in `tasks/1.json` through `tasks/6.json`.

**Parallel track**: Tasks 1-5 are independent of each other (different cells, no shared in-memory state that one task's edit would break for another) and can be done in any order — only Task 6 (final re-verification) is blocked on all of them.

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| New plan (P0031) rather than reopening P0030 | P0030's scope (migration) is complete and validated; these are a distinct, later-discovered set of analysis-completeness gaps |
| Task 4 prioritized first | Real modeling risk (multicollinearity) vs. Tasks 1/2/3/5's documentation/cosmetic nature — Brian's explicit ranking |
| Tasks 1-5 marked as independent (no blockedBy chain among them) | Unlike P0030's inherently sequential pipeline-step transfers, these touch different, non-overlapping cells |

## Open Questions (to resolve during Task 1 / Task 4)

- Task 1: should ACF/PACF's lag consensus override, merge with, or stay purely diagnostic against the correlation-based `LAGS`? Not yet decided — flagged as ask-Brian-if-ambiguous in the task description.
- Task 4: is sales_value/sales_liters correlation with sales_units clearly >0.95 (drop), clearly <0.5 (keep, not redundant), or ambiguous 0.7-0.9 (ask Brian)? Not yet computed.

## Errors Encountered

(none yet — plan just created)
