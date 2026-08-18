---
pid: P0031
created: 2026-07-13 18:29:00
updated: 2026-08-19 10:00:00
status: complete
completed: 2026-08-19 10:00:00
outcome_summary: "Delivered by the P0038 pipeline rather than by patching the notebook. Tasks 1, 2, 4 are satisfied by the step 3 contract (lags with provenance, has_promo capability, CONTEMPORANEOUS_COLS). Task 5 is moot (notebook retired). Task 3 (heterogeneity forwarding) is the one genuine gap and is recorded as a known limitation rather than left open."
focus_detail: "Delivered by the P0038 pipeline rather than by patching the notebook. Tasks 1, 2, 4 are satisfied by the step 3 contract (lags with provenance, has_promo capability, CONTEMPORANEOUS_COLS). Task 5 is moot (notebook retired). Task 3 (heterogeneity forwarding) is the one genuine gap and is recorded as a known limitation rather than left open."
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

---

## Closed 2026-08-19

**Complete — delivered by the pipeline, not by the patches this plan proposed.**

The plan listed six fixes to the CSD EDA notebook. That notebook is retired; the
equivalent work landed in the shared pipeline. Task by task:

| # | Task | Outcome |
|---|------|---------|
| 1 | Wire ACF/PACF lag consensus into LAGS | **Delivered** — contract carries `lags: [1,2,3,4,8,13]` with a `provenance` entry stating why lag-13 is retained |
| 2 | Flag CSD's zero promo signal | **Delivered differently, and better** — the zero-promo signal was a market-scope artifact (DEC-SCOPE), not a property of CSD. Capability is now recorded per category as `has_promo`, and a degenerate-feature guard fails loudly on any all-zero column (F76) |
| 3 | Forward heterogeneity verdict into findings JSON | **NOT delivered** — see limitation below |
| 4 | Resolve sales_value/sales_liters redundancy | **Delivered** — F79: they are contemporaneous measures of the target, now excluded from the manifest's feature list via `CONTEMPORANEOUS_COLS` |
| 5 | Fix stale CELL-N print headers | **Moot** — notebook retired |
| 6 | End-to-end re-verification | **Delivered** — 8/8 clean runs, 4 categories x 2 horizons, plus the F68 parity gate |

### Known limitation carried forward (task 3)

The contract records `peak_months` but **not** a per-category heterogeneity verdict
(coefficient of variation across brands, concentration of volume in peak months).

Consequence: the pipeline treats every category's brand panel as equally poolable. If
one category's brands are far more heterogeneous than another's, a pooled model is a
weaker fit there and nothing in the artifacts says so.

**Not fixed, deliberately.** It is a reporting gap rather than a correctness one — no
number is wrong because of it — and with under a month to submission the thesis is
better served by writing than by extending the contract schema. It belongs in the
limitations section: *parameters are derived per category, but cross-brand
heterogeneity within a category is not quantified in the artifacts.*
