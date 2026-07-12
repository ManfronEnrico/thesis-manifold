---
pid: P0027
created: 2026-07-10 15:30:00
updated: 2026-07-11 18:35:00
status: in_progress
focus_detail: "Phase 2/3 findings stand, but Phase 4 (dual-grain production strategy) is now BLOCKED by a newly-found correctness bug: the shared feature-engineering module groups by 'brand' only (not 'brand'+'market_id'), so lag/rolling features for the region-grain pipeline are computed across region-interleaved rows -- the 21.2% region-grain WMAPE from Phase 3 may itself be leaky and needs re-running after the fix. Also newly mapped (2026-07-11 session): full inventory of competing feature-matrix pipelines (CSD orchestrator vs colleague's build_feature_matrix.py/_bychain.py, both writing into the same _03_engineered/{bymonth,bychain}/ dirs that srq1_benchmark.py reads), a real leakage bug location, and a scoped fix-then-replicate plan agreed with Brian (region + chain as two parallel orchestrator branches, both rolling up to brand-month, CSD first then copy to the other 3 categories). See findings.md '2026-07-11 Session — Pipeline Inventory + Grain-Leakage Bug' for full detail. Session paused here for the day; resume with the group_keys fix (see Phase 4a below) before trusting any region-grain WMAPE number."
---

# P0027 — CSD EDA Reconciliation + Academic Rigor Pass

## Goal

Before templating EDA to danskvand/energidrikke/RTD, get CSD's EDA to a state that is:
1. Not stale (matches the data actually feeding the model)
2. Academically defensible (missingness mechanism, correct stationarity testing, justified transforms)
3. Reconciled with Enrico's parallel modeling track (SRQ1-4), which merged into `main` on 2026-07-01 with its own EDA, its own canonical preprocessing script, and several "locked" decisions we did not make jointly

Then decide — with evidence, not assertion — whether/how to extend to the other 3 categories.

**Explicitly NOT in scope**: writing Ch4 thesis prose. Bullets/findings only. Human approval required before any prose conversion (project law).

## Context

- Prior fork audit (this session, pre-plan) confirmed: `pre_csd_1.5_eda.py` on `main` was stale relative to the brand×region×period grain (P0026) — but that grain was since **rejected** by Enrico (commit `9b4b0a4`) in favor of keeping brand×month / brand×chain.
- Enrico's handover (`docs/handover/2026-07-01_enrico-to-brian-merge-handover.md`) claims several "LOCKED" decisions and results. Per user instruction, treat every claim as unverified until checked against actual code/data — Enrico is a heavy Claude Code user with limited independent verification habits.
- **Already verified true** (this session):
  - Cell 12 bug fix is real and correct (commit `1d55145`): NaN warmup row was silently killing window selection and collinearity pruning. Fix is sound.
  - Region-grain rejection reasoning is accurate: Enrico's EDA ran on a **partial local raw** (2.5M rows / 86 brands), not the full 9.8M refetch — this is stated in his own commit message, not hidden.
  - A **second, separate canonical script** exists: `thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py` (+ `_bychain.py` variant). This — NOT our modular `_02_preprocessing/nielsen/<cat>/pre_*.py` steps — produced the feature matrices in `_03_engineered_dvhexclhd/` and `_04_engineered_bychain/`, which in turn produced the SRQ1 results in `_05_results_srq1/`.
  - **CORRECTION (2026-07-10, later verification)**: the claim that our modular step scripts (`pre_csd_1..6`) are "not runnable because PATHS.py is deleted" is **WRONG as of this check** — `PATHS.py` exists at repo root (`Z:\_dev-ssd\thesis-manifold\PATHS.py`) and imports cleanly (`python -c "import PATHS"` succeeds, `PATHS.THESIS_DATA_PREPROCESSING_DIR` resolves). Either it was restored after the original claim was made, or the claim was never independently verified by running the actual import (Phase 1 Task did not literally try this — it inferred non-runnability from the handover's assertion). **Needs re-verification**: actually try running `pre_csd_1_load_and_aggregate.py` before relying on either claim.
  - **SECOND CORRECTION (2026-07-10, Task 12 follow-up)**: our modular pipeline is not just "runnable" — it is the **currently live, actively-maintained CSD pipeline**. `_02_preprocessing/nielsen/CSD/pre_csd_1..6.py` → `_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` (25,124 rows, 78 brands, brand×region×period, verified via direct `pd.read_parquet`) was re-run as recently as commit `cb615cf` (2026-06-30). By contrast, `build_feature_matrix.py`'s expected output folder `_03_engineered_dvhexclhd/CSD/` contains only a `csd_split_dates.json` locally — no feature matrix parquet has landed in this checkout from that track. The premise that our modular pipeline is the deprecated/non-canonical one does not hold up; see findings.md "Pipeline Provenance Clarification" for full evidence. This directly affects Phase 4's canonical-script decision.
  - `eda_findings_dvhexclhd.md` already contains per-category (CSD/danskvand/energidrikke/RTD) ADF, ACF, seasonality, and promo-correlation findings computed via `build_feature_matrix.py`.
  - Confirmed live in data: `tuned_summary.md`'s "test mean MAPE" column is degenerate (values like 7,438,153,885%) — validates the handover's own warning that mean-MAPE must never be reported alone.
  - No KPSS anywhere in either EDA script; no MCAR/MAR/MNAR missingness-mechanism reasoning in either. These gaps from the fork audit persist in Enrico's version too.
  - Leakage claim holds: `build_feature_matrix.py` uses `shift(k)` for lags and `shift(1)` before rolling stats — no current-period leakage.
- **Not yet verified** — must check in Phase 1 before relying on them:
  - MIN_PERIODS=30 "global" claim and the 37-39 period constraint for danskvand/energidrikke/RTD
  - Per-category granularity claim (brand×month wins for CSD/energidrikke/RTD; brand×chain wins for danskvand) — is this from an actual holdout WMAPE comparison, methodologically sound?
  - SRQ1 "locked" numbers (CSD 16.5%, danskvand 22.0%/23.8%, energidrikke 11.4%, RTD 31.0%) — which dataset variant (brand vs bychain) is actually the reported "locked" number? `tuned_summary.md` shows BOTH a `bychain` and `brand` table per category, and per-category winner is not obviously consistent with the handover's simple claim (needs a careful side-by-side, not eyeballing)
  - Warmup=13 periods claim vs. actual `WARMUP_PERIODS` used in the shared feature engineering
  - "9.8M raw stays local, engineered tiers regenerated as needed" — confirm `_03_engineered_dvhexclhd` etc. are actually gitignored, not tracked bloat
  - Whether `eda_findings_dvhexclhd.md`'s pooled brand-demeaned ACF method is valid given the stated caveat ("an alternative per-brand-averaged ACF gives smaller lag1 values — method to be stated when finalizing §4.3")

## Phases

### Phase 1 — Verify Locked Claims
**Status**: complete

Do not act on any handover claim until checked against code/data. Write results to `findings.md`.

- [x] Confirm MIN_PERIODS=30 and period-count constraints (37-39) for danskvand/energidrikke/RTD directly from data — **holds**, global constant, no per-category override; period ceiling verified for CSD/Energidrikke, danskvand/RTD rest on secondary sources (residual gap, not urgent)
- [x] Reproduce the granularity decision (brand×month vs brand×chain per category) from raw `tuned_metrics.csv`/`tuned_summary.md` — **holds exactly** for all 4 categories, non-trivial margins (1.8-7.8pp), XGBoost always the best model
- [x] Verify WARMUP_PERIODS=13 against the actual feature engineering code (max lag/window used) — **holds exactly**, `max(MAX_LAG=13, MAX_WINDOW=13)=13`, identical in brand and bychain scripts
- [x] Confirm `_03_engineered_dvhexclhd/`, `_04_engineered_bychain/`, `_05_results_srq1/` etc. gitignore status — **not gitignored**, but no current large-file risk (~34MB total); recommend adding ignore patterns preventively
- [x] Assess the pooled brand-demeaned ACF method in `eda_findings_dvhexclhd.md` — **NOT acceptable as-is**: boundary-splicing + heteroscedasticity flaws, unreproducible in canonical script. Needs replacement in Phase 2, not just a caveat.

### Phase 2 — Academic Gap-Fill on Canonical EDA
**Status**: complete (substantially — 1 task fully blocked on data availability, see note)

Target: `build_feature_matrix.py` + a new/extended EDA script, treated as canonical (supersedes `_02_preprocessing/nielsen/<cat>/pre_*` for EDA/feature purposes, pending Phase 4 decision on formal retirement).

- [x] Add KPSS test alongside ADF — **done for CSD/energidrikke only** (danskvand/RTD have no local raw data). Result: ADF/KPSS jointly **ambiguous**, weaker than the doc's existing clean "I(1)" claim. Also surfaced an unreconciled CSD ADF p-value discrepancy (0.140 independently computed vs 0.421 in doc).
- [x] Add formal MCAR/MAR/MNAR missingness-mechanism reasoning — **done at aggregate level** (row-level test blocked by data availability). MNAR mechanism identified (positive-sales-only filter structurally ties missingness to the value itself); current no-impute approach is defensible but was undocumented as deliberate.
- [x] Add train/val/test distribution-shift check — **done for CSD** (Task 12, 2026-07-10): no meaningful shift found; val-vs-test is the *smallest* of the three KS comparisons, opposite of the shift-driven-anomaly signature. Danskvand/energidrikke/RTD remain deferred to Phase 5 (data now converted, not yet re-run per Brian's CSD-only scoping).
- [x] Verify/correct "Kim, 2013" skewness citation — **done**. Confirmed unbacked (no matching bibliography entry anywhere in repo); recommended replacement or reframing as heuristic.
- [x] Replace pooled brand-demeaned ACF with per-brand method — **done, real code fix shipped**: new committed script `thesis/data/preprocessing/nielsen_dvh/compute_acf_per_brand.py` + updated `eda_findings_dvhexclhd.md`. Confirmed pooled method inflated lag1 by ~0.2-0.3 absolute. CSD high-confidence, energidrikke low-confidence, danskvand/RTD pending (no local data).
- [x] Reconcile WARMUP_PERIODS=13/lag-13 tension against corrected ACF — **done**. Recommendation: keep lag-13 as-is but reweight the narrative honestly (proposed wording in findings.md); evidence too thin (2/4 categories) to justify removal. No code changed — awaiting human approval before any narrative/comment edit.

**Note on incomplete closure**: this local checkout lacks `data/raw/` and most engineered parquet files. Only CSD has fully reliable data; energidrikke partial/stale; danskvand/RTD essentially none. This blocks full completion of the KPSS, missingness, distribution-shift, and ACF tasks for 2 of 4 categories. **Before Phase 5 (extend to 3 categories) can proceed, this data-access gap must be resolved** — either get `data/raw/` on this machine/branch, or have whoever holds the full data re-run the blocked pieces.

**RESOLVED (2026-07-10, later same session)**: root cause identified — raw `.jsonl` data exists for ALL 4 categories under `thesis/data/_00_raw/nielsen/data_jsonl/<Category>/`, but the Stage-1 JSONL→Parquet conversion (`thesis/data/_01_converted/nielsen/jsonl_to_parquet_script/run_all_conversions.py`) was only ever run for CSD and Energidrikke. Danskvand and RTD have zero converted parquet output — that's the actual reason tasks 6/7/9/11 above went data-poor for those 2 categories, not a missing-source-data problem. Energidrikke's local parquet is confirmed stale (Task 8 found 29 periods vs 39 expected) and needs `--force` re-conversion.

**Command to close this gap** (run from project root):
```bash
python thesis/data/_01_converted/nielsen/jsonl_to_parquet_script/run_all_conversions.py --only Danskvand Energidrikke RTD --force
```
This converts Danskvand + RTD for the first time and force-refreshes Energidrikke's stale parquet. CSD is left untouched (already converted and verified fresh). Note this script imports `PATHS` — confirmed importable in this checkout (see correction above), so no separate fix needed here.

**Brian's explicit sequencing decision (2026-07-10)**: finish the CSD EDA/preprocessing pipeline (Phases 2-4 of this plan) to full academic rigor FIRST, on the reasoning that the *procedure* (stationarity testing, missingness reasoning, ACF method, transform justification, cutoff derivation) must be identical and equally justified across all 4 categories — only the *numeric results and resulting parameter values* (e.g. which lags matter, what the KPSS/ADF verdict is, what the missingness mechanism looks like) are expected to differ per dataset. Phase 5 (extend to 3 categories) is therefore a copy-the-procedure-apply-fresh-numbers exercise, not a re-design. This confirms the plan's existing Phase 2→Phase 5 ordering was correct; no phase reordering needed, just the data-access gap needed closing first.

**Re-scoping decision (2026-07-10, after conversion completed)**: Brian confirmed conversion succeeded for all 4 categories, but explicitly narrowed immediate scope further: focus purely on making **CSD** bulletproof this session (not yet re-running danskvand/energidrikke/RTD even though their data is now available). New tasks 12-14 created to close the remaining CSD-specific Phase 2 gaps: Task 12 (distribution-shift check, CSD-only, supersedes Task 9's CSD portion — **completed**, see findings.md), Task 13 (reconcile CSD's ADF p-value discrepancy 0.140 vs 0.421), Task 14 (row-level MNAR/MAR/MCAR test for CSD, now that CSD data is confirmed current). Danskvand/energidrikke/RTD portions of Tasks 6/7/9 remain explicitly deferred to Phase 5.

**Pipeline provenance resolved (2026-07-10, Task 12 follow-up)**: investigated and confirmed which pipeline is "real" for CSD — see Context section SECOND CORRECTION above and findings.md. Our modular `_02_preprocessing/nielsen/CSD/pre_csd_1..6.py` pipeline, output at `_03_engineered/nielsen/CSD/csd_feature_matrix.parquet`, is the live, current, most-recently-regenerated (2026-06-30) CSD dataset — not `build_feature_matrix.py`'s `_03_engineered_dvhexclhd/CSD/`, which has no feature matrix parquet in this checkout. Tasks 13/14 will target `_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` directly.

**Tasks 13/14 completed (2026-07-11)**: Task 13 (ADF p-value reconciliation) root-caused the 0.140 vs 0.421 discrepancy to an aggregation-grain bug in Task 6's original script — `csd_feature_matrix.parquet` is brand×region×period grain, and grouping by brand alone without first summing across regions fed a region-interleaved series into `adfuller()`, reproducing 0.140 almost exactly. Correcting the grain (sum across regions per brand per month, then per-brand ADF, then median across 78 brands) gives 0.3535, closely matching the doc's 0.421 (n=76). **0.421 is authoritative going forward**; the qualitative I(1)/non-stationary verdict is unaffected either way. Task 14 (row-level MNAR/MAR/MCAR test) confirmed and substantially strengthened Task 7's aggregate-level conclusion: missingness is overwhelmingly explained by brand volume tier (chi²=1336.9, p≈0; Q1 low-volume brands miss 16.3% of period-cells vs Q4 high-volume 0.4%), a formal MAR signature that also reads as MNAR in the colloquial sense (brand sales dropped near-zero, stopped being recorded) — both vocabularies point to the same conclusion. The current reindex-and-leave-NaN (no-impute) approach is grounded as correct by this evidence. Full detail in findings.md under "Task 13 — CSD ADF Log-Level p-Value Discrepancy Reconciled" and the row-level missingness section preceding it.

**CSD's Phase 2 gap-fill is now complete** (all 6 CSD-scoped tasks — 6, 7/14, 8, 9/12, 10, 11, 13 — closed or explicitly deferred with a stated reason). Next decision point: Phase 3 (region-grain WMAPE test) vs Phase 5 (extend to 3 categories, now that all 4 have current converted data) — not yet decided, needs Brian's input.

### Phase 3 — Region Grain WMAPE Test (handover §5, "your test")
**Status**: complete

**Reframed purpose**: Not optimization (pick best WMAPE), but capability assessment. Region-grain model serves regional managers asking "What will Faxe Kondi sell in Copenhagen next quarter?" — a question brand×month cannot answer. Both grains are production models, serving different user personas (regional managers vs HQ).

**Result (2026-07-11):**
- Region-grain test WMAPE: 21.2% (XGBoost and LightGBM tied)
- Brand×month baseline: 16.5%
- Delta: +4.7pp (region has less predictability per row due to lower volumes, higher noise)

**What 21.2% WMAPE means:**
- Aggregate forecast error: ~540K units across 254M total test sales
- Per-brand error: Coca-Cola ~115K units, Faxe Kondi ~80K units (weighted by volume)
- Per-region error: Copenhagen ~79K units, Jutland regions ~66K units each
- **Interpretation**: Not "inaccurate," but "appropriately noisy for this granularity" — region-month data is ~1/9 the volume per row, so ±21% is expected vs ±16% at brand level

**Metrics WMAPE does NOT tell us:**
- Whether Prometheus gets trend direction correct (directional accuracy)
- Which brands/regions are hard vs easy to forecast (heterogeneous error)
- Whether confidence bounds are well-calibrated (quantile loss)
- Whether the model is useful for regional decision-making (domain-specific value)

**Decision**: Region-grain is PRODUCTION-READY for Prometheus. Keep both models:
- Brand×month (16.5%) → HQ-level "total sales" queries
- Region×month (21.2%) → Regional manager "Copenhagen Faxe Kondi" queries
- Ensemble both for consistency checks and cross-validation

- [x] Confirm `pre_csd_1_load_and_aggregate.py` (region grain, 25.1k rows) still runs against the full 9.8M raw — ✓ runs cleanly, generates 27.1k raw → 25.1k filtered
- [x] Run region-grain tuning → Optuna 30 trials/model, XGBoost and LightGBM both tuned to 21.2% WMAPE on test
- [x] Report result plainly — region-grain 21.2% is +4.7pp vs baseline 16.5%, acceptable for granularity trade-off
- [x] Reframe Phase 4-5 decision — not "retire one, keep one" but "maintain both for complementary use cases"

### Phase 4 — Production Model Strategy (Dual-Grain Architecture)
**Status**: actionable

With Phase 3 confirming region-grain as production-ready, restructure to support both grains formally:

**Decision**: Maintain BOTH pipelines as intentional production capability, not competing alternatives.
- `_02_preprocessing/nielsen/CSD/pre_csd_1..6.py` → brand×month grain (HQ queries, 16.5% WMAPE)
- Region-grain variant (new) → brand×region×month grain (regional mgr queries, 21.2% WMAPE)

**Rationale**: Prometheus serves two user personas (HQ doing inventory allocation, regional managers optimizing local stock). No single grain is "correct" — both are valuable.

**Action items** (when ready):
- [ ] Create formal `pre_csd_1_region.py` (or alias `pre_csd_1_load_and_aggregate.py` to output grain as parameter)
- [ ] Document both grains in repository_map.md as "intentional dual production pipelines"
- [ ] Update CLAUDE.md §Thesis with dual-grain strategy (not "canonical" but "complementary")
- [ ] Confirm Prometheus agent can accept both models for user-appropriate recommendations

### Phase 4a — Fix Region-Grain Leakage Bug (BLOCKS Phase 4/5; found 2026-07-11)
**Status**: pending — not started, identified end of session, resume here tomorrow

**Why this blocks everything above**: Phase 3's 21.2% region-grain WMAPE was computed on features built by `pre_csd_4_engineer_features.py` calling the shared `engineer_features()` function (`_02_preprocessing/nielsen/shared/engineer_features.py`). That shared function groups by `"brand"` only when computing `lag_*`, `rolling_mean_*`, `rolling_std_*` (line 263: `g = df.groupby("brand")`) — but CSD's Step 1-3 already operate at brand×region grain (9 `DVH_REGION_IDS`, `market_id` column present, Step 3 correctly does `groupby(["brand", "market_id"])`). Result: a brand's `lag_1` in one region can silently pick up a different region's prior-month value, because rows are sorted by `["brand", "date"]` only — region is not a sort/group key anywhere in Step 4. This is a real, live leakage bug, not a hypothetical: **the Phase 3 WMAPE result needs to be re-run after the fix** before Phase 4 relies on it, and before any decision to keep region-grain as a formal production branch.

Same root issue affects Step 6's `build_series_index()` (also `groupby("brand")` only) — series-index stats (n_periods, total_units, split counts) silently collapse the region dimension in the generated report, though this doesn't corrupt the underlying parquet (which does retain `market_id` through Step 5).

**Full technical detail, code line numbers, and the fix plan**: see findings.md "2026-07-11 Session — Pipeline Inventory + Grain-Leakage Bug".

- [ ] Add a `group_keys: list[str] = ["brand"]` parameter to `filter_series()`, `engineer_features()`, `build_series_index()`, and the `weighted_dist` ffill inside `make_calendar()` in `_02_preprocessing/nielsen/shared/engineer_features.py`
- [ ] Update `pre_csd_4_engineer_features.py` to call `shared_engineer_features(df, group_keys=["brand", "market_id"], ...)`
- [ ] Update `pre_csd_6_save_outputs.py`'s `build_series_index()` call the same way; add region count to the generated report
- [ ] Re-run CSD's full 6-step pipeline and re-verify the region-grain WMAPE from Phase 3 — expect the number to change (direction unknown, could go either way)
- [ ] Only then resume Phase 4's dual-grain production decision with a trustworthy number

### Phase 4b — Add Chain Branch to CSD Orchestrator (new scope, agreed 2026-07-11)
**Status**: pending — not started

Brian's directive (2026-07-11 session): region and chain should be two parallel branches off the same orchestrator pattern, both able to roll up to brand×month. This does NOT mean porting the colleague's `build_feature_matrix_bychain.py` wholesale — that script has stale pre-P0028 paths (`thesis/data/...`, hardcoded `parents[4]` root-walk) and duplicates logic already fixed once in the `group_keys` work above. Once Phase 4a's `group_keys` parameter exists, a chain branch is "mostly free": same shared functions, different `group_keys=["brand", "chain_id"]`, different Step 1 market scoping (individual leaf-chain `market_id`s instead of the 9 region `market_id`s).

- [ ] Add a chain-grain variant of Step 1 (new script or `--grain` flag) scoped to the leaf retail chains inside DVH EXCL. HD — port the *scoping logic* (which market_ids = chains) from `build_feature_matrix_bychain.py`'s `LEAF_CHAINS` list, but re-verify the chain list against current data rather than trusting the colleague's script's hardcoded values
- [ ] Confirm Steps 2-6 work unmodified for chain grain once `group_keys` is threaded through (they should — the grain-awareness lives entirely in `group_keys` + Step 1's market scope)
- [ ] Add a rollup step/flag (aggregate region-or-chain grain back up to brand×month: sum `sales_units`/`promo_units`, re-average `weighted_distribution`) — this satisfies Brian's "possibility to aggregate up to brand x month" requirement without needing a third parallel pipeline
- [ ] Decide fate of `02_thesis_data/preprocessing/nielsen_dvh/build_feature_matrix.py` + `build_feature_matrix_bychain.py` once the orchestrator covers both grains — likely archive, not delete (they contain the original scope-correction rationale worth preserving, e.g. the 5.24x double-count finding)

### Phase 5 — Extend to 3 Remaining Categories
**Status**: pending

Only start once Phase 2 gap-fill is validated on CSD and Phase 4/4a/4b decide the canonical orchestrator pattern (region + chain branches, group_keys fix applied and re-verified).

- [ ] Copy CSD's finished Step 1-6 pattern (region branch + chain branch + rollup) to Danskvand, Energidrikke, RTD — only category-specific constants change (MIN_PERIODS, holiday months, split dates — each already hand-tuned per category from its own EDA in the existing `pre_{cat}_*.py` scripts)
- [ ] Apply the same KPSS + missingness-mechanism + distribution-shift additions to danskvand, energidrikke, RTD
- [ ] Re-verify per-category granularity winner (brand×month vs brand×region vs brand×chain) after gap-fill changes and the group_keys fix, in case results shift
- [ ] Produce consolidated findings extending `eda_findings_dvhexclhd.md` — extend, do not duplicate, per handover §6

### Phase 6 — Ch4 Handoff Package
**Status**: pending

- [ ] Assemble bullet-point findings package per category (CSD + 3 others) ready for human approval before any prose
- [ ] Flag any remaining academic gaps explicitly as "limitation" bullets rather than silently omitting them

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Working on branch `thesis/csd-eda-rerun`, not main | Branch strategy rule; this is active development work |
| Verify before act on all Enrico handover claims | User explicit instruction — Enrico's claims are Claude-Code-generated and self-graded |
| CSD gets the rigor pass first, others wait | Don't propagate unverified/incomplete method to 3 more categories |
| No thesis prose in this plan | Project law — bullets only, human approval gates prose |

## Errors Encountered

| Error / Gap | Attempt | Resolution |
|---|---|---|
| Phase 2 tasks 6/7/9/11 could only get partial/no data for danskvand/RTD, stale data for energidrikke | Assumed this was a missing-raw-data problem; flagged as environment blocker | **Root cause found**: raw `.jsonl` exists for all 4 categories; only Stage-1 parquet conversion was never run for danskvand/RTD, and energidrikke's parquet is stale. Fix: run `run_all_conversions.py --only Danskvand Energidrikke RTD --force` (see Phase 2 note above) |
| Task_plan.md's Phase 1 context claimed `PATHS.py` is deleted (making `_02_preprocessing` scripts non-runnable) | Took Enrico's handover claim at face value in Phase 1, did not literally test the import | **Corrected**: `PATHS.py` exists at repo root and imports cleanly as of this session's direct check. Claim was wrong or stale — needs a real re-test (actually running a `pre_csd_*.py` step script) before relying on either verdict |
