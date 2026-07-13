---
pid: P0029
created: 2026-07-13 13:26:00
updated: 2026-07-13 13:35:00
status: in_progress
focus_detail: "Phases 1-3 complete. Dominant finding: pre_csd_1.5_eda.py is currently non-functional (reads a filename that no longer exists after P0027's Phase 4a-ii Step 1 rewrite). Most of ChatGPT's dramatic grain-corruption claims resolve automatically once that one-line path fix lands, since the correct-grain file already exists. Several independent, grain-unrelated methodological gaps also confirmed (model-selection leakage, missing-period audit, decomposition model-selection stat error, and smaller items). Full claim-by-claim table in findings.md. No code changed yet — awaiting Brian's direction on which fixes to apply and whether/how this feeds back into P0027's paused Phase 5 decision."
---

# P0029 — ChatGPT EDA Gap Analysis Reconciliation

## Goal

Brian had ChatGPT independently analyze `02_thesis_data/_02_preprocessing/nielsen/CSD/pipeline_step_scripts/pre_csd_1.5_eda.py` for gaps/issues, with **only that single script as input** — no access to the dataset, the rest of the pipeline (Steps 0-6), `PATHS.py`, or the extensive prior verification work already done in P0027 (CSD EDA Reconciliation + Academic Rigor Pass).

This plan's job is to take that raw analysis and reconcile it claim-by-claim against ground truth:
1. What does the analysis get right?
2. What does it get wrong or mischaracterize, because it lacked context (dataset stats, pipeline architecture, prior fixes already shipped in P0027)?
3. What does it surface that's genuinely new and not yet covered by P0027's existing findings?
4. Only once verified — what, if anything, should change in the EDA script or methodology?

**Explicitly NOT in scope**: applying any fix before verification. Every claim gets checked against code/data first (per [[plan-verification-discipline]] and Brian's explicit instruction this session — "take this with a grain of salt and verify at each step").

**Relationship to P0027**: P0027 ("CSD EDA Reconciliation + Academic Rigor Pass") is the long-running plan that already did deep rigor work on this exact script and pipeline, and is currently **paused** specifically waiting on the outcome of this ChatGPT analysis before deciding whether/how to proceed to Phase 5 (extend to 3 more categories). This plan (P0029) is scoped narrowly to processing the new external analysis; if verified findings here imply changes to P0027's phases or should feed back into extending the pipeline, that gets handed back to P0027 explicitly rather than duplicated here.

## Context

- Source script under review: `02_thesis_data/_02_preprocessing/nielsen/CSD/pipeline_step_scripts/pre_csd_1.5_eda.py`
- The ChatGPT analysis was generated blind: single-file input, no dataset, no repo access, no awareness of P0027's already-verified/already-fixed items (e.g. the pooled-ACF defect already fixed via `compute_acf_per_brand.py`, the MIN_PERIODS re-derivation already done in Phase 4a-ii, the ADF p-value discrepancy already reconciled in Task 13, the row-level MNAR/MAR/MCAR test already done in Task 14).
- High prior probability that some fraction of the ChatGPT analysis will re-discover things P0027 already fixed, or will flag things as gaps that are actually handled elsewhere in the pipeline (e.g. in Steps 1-6, not visible from the EDA script alone).
- Analysis text has not yet been provided — Brian will paste it in this session.

## Phases

### Phase 1 — Ingest and Triage the ChatGPT Analysis
**Status**: complete

- [x] Received full analysis text from Brian at `2026_07_13-13_27 - ChatGPT Analysis Text`, saved to `findings.md`
- [x] Extracted discrete claims — analysis's own numbered sections (1-19 + priority list) served as the natural item breakdown
- [x] Triaged Section 1 (grain, P0-priority) directly myself: script cannot currently run at all (input file doesn't exist); the file that WOULD load is already correct grain. Dispatched two parallel forked agents for the remaining sections (2-3, 4-9, 10-12), each cross-referencing P0027's task_plan.md/findings.md for already-resolved items.

### Phase 2 — Verify Each Claim
**Status**: complete

- [x] Section 1 (grain) verified directly: confirmed via filesystem check + `pd.read_parquet` that `step_1_aggregate.parquet` doesn't exist, only `step_1_aggregate_bymonth.parquet` does, and that file is already true brand×month grain (140 brands, max 44 rows/brand, no market_id/chain_id column)
- [x] Sections 4, 5, 6, 8, 9 verified via forked agent — results: lag threshold (confirmed, grain-independent), rolling window leakage/collinearity/partial-window (confirmed, mixed mechanism accuracy), ADF n=396 (false as stated, stale-artifact-based), decomposition model selection (confirmed, textbook stat error), MIN_PERIODS (already fixed in P0027, notebook itself never updated)
- [x] Sections 2, 3, 10, 11, 12 verified via forked agent — results: missing-period audit (confirmed new gap), model-selection leakage (confirmed, distinct from P0027's prior leakage fix), train/val/test split (confirmed, grain-independent), promo analysis (partially valid, Cell 15 unguarded), weighted_dist leakage (out of scope for this script)
- [x] Full verification method + evidence documented per claim in `findings.md`

### Phase 3 — Reconcile and Report
**Status**: complete

- [x] Consolidated table built in `findings.md` (claim → verdict → recommended action) covering all 11 distinct findings
- [x] Executive summary written identifying the dominant finding (script is non-functional due to a stale input path) and what remains genuinely open after that fix
- [x] Handoff note written for P0027: don't extend the EDA methodology to 3 more categories until the notebook is fixed and re-run — the template P0027's Phase 5 would copy is currently broken
- [x] No code changes made — all fixes pending Brian's explicit direction

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| New P-ID (P0029) rather than resuming P0027 | Brian explicitly requested a new plan for this endeavor |
| Verification-first, no fixes until confirmed | ChatGPT analysis had no dataset/repo access — must not be trusted at face value (Brian's explicit instruction) |
| Cross-reference against P0027 findings before treating anything as new | P0027 already did an extensive rigor pass on this exact script; avoid re-doing work or contradicting already-verified conclusions without cause |

## Errors Encountered

(none yet)
