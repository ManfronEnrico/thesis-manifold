---
pid: P0027
created: 2026-07-10 15:30:00
updated: 2026-07-11 00:40:00
status: in_progress
focus_detail: "CSD's Phase 2 academic-rigor gap-fill is complete: Tasks 6/7/8/9/10/11/12/13/14 all closed or explicitly deferred with a stated reason. Task 13 root-caused the ADF 0.140/0.421 discrepancy to an aggregation-grain bug (0.421 is authoritative); Task 14 confirmed missingness is volume-tier-driven (MAR/MNAR-adjacent), grounding the no-impute approach. PATH MIGRATION (2026-07-11, confirmed by Brian): repo underwent an in-progress P0028 restructure -- thesis/data/ -> 02_thesis_data/, and _03_engineered_dvhexclhd/ + _03_engineered/nielsen/ unified into _03_engineered/bymonth/. New canonical CSD path: 02_thesis_data/_03_engineered/bymonth/CSD/csd_feature_matrix.parquet (verified identical content to the old file -- 78 brands, 25,124 rows). Old thesis/data/ tree still exists, still git-tracked, pending cleanup -- not a second source of truth. All Phase 1/2 findings remain valid; only cited paths need updating. Also found: pre_csd_1.5_eda.py fails with ModuleNotFoundError: statsmodels not installed. Next decision needed from Brian: Phase 3 (region-grain WMAPE test) vs Phase 5 (extend to danskvand/energidrikke/RTD, now that all 4 categories have current converted data)."
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
**Status**: pending

Enrico's requested decision procedure: run tuned WMAPE on brand×region×period, re-aggregate to brand-national, compare against brand×month baseline (16.5% for CSD). Region wins → switch. Otherwise → region becomes a documented limitation, not a re-litigated decision.

- [ ] Confirm `pre_csd_1_load_and_aggregate.py` (region grain, 25.1k rows) still runs against the full 9.8M raw
- [ ] Run region-grain aggregation → re-aggregate to brand-national → run through the same tuned XGBoost/LightGBM pipeline used for SRQ1
- [ ] Compare test WMAPE against 16.5% baseline; report result plainly regardless of outcome
- [ ] Update `P0026`'s outcome_summary if the grain decision changes as a result

### Phase 4 — Canonical Script Decision
**Status**: pending

- [ ] Decide, with the Phase 1-3 evidence in hand, whether to formally retire `_02_preprocessing/nielsen/<cat>/pre_*.py` in favor of `build_feature_matrix.py` + `_bychain.py`, or keep both for different purposes (document why if kept)
- [ ] If retiring, update `docs/dev/repository_map.md` and CLAUDE.md references accordingly (not a rewrite — a documented decision)

### Phase 5 — Extend to 3 Remaining Categories
**Status**: pending

Only start once Phase 2 gap-fill is validated on CSD and Phase 4 decides the canonical script.

- [ ] Apply the same KPSS + missingness-mechanism + distribution-shift additions to danskvand, energidrikke, RTD in `build_feature_matrix.py` / `_bychain.py`
- [ ] Re-verify per-category granularity winner (brand×month vs brand×chain) after gap-fill changes, in case feature changes shift WMAPE
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
