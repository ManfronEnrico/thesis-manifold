# P0029 Findings

## Raw ChatGPT Analysis (unverified)

Provided by Brian at `plans/P0029_2026-07-13_13-26_chatgpt-eda-gap-analysis-reconciliation/2026_07_13-13_27 - ChatGPT Analysis Text` (verbatim, not reproduced here — see that file).

---

## Phase 1/2 — Section 1: The Grain Claim (verified directly, not forked)

**ChatGPT's claim**: `pre_csd_1.5_eda.py` analyzes a dataset with ~396 obs/brand (44 months × 9 markets), because it sorts/groups only by `brand`, silently treating brand×region×month rows as one sequential per-brand time series. This corrupts every downstream analysis (ADF, ACF, lags, rolling windows, MIN_PERIODS).

**Verification method**: Read the full EDA script (1413 lines) directly. Checked `INPUT_AGGREGATE = STEP_OUTPUT_DIR / "step_1_aggregate.parquet"` (line 110). Checked `pre_csd_1_load_and_aggregate.py` (Step 1) directly — confirmed it now outputs grain-suffixed files (`step_1_aggregate_{grain}.parquet`) as of P0027 Phase 4a-ii (2026-07-13). Ran a filesystem existence check and a direct `pd.read_parquet` against what's actually on disk in `02_thesis_data/_02_preprocessing/nielsen/CSD/pipeline_step_outputs/`.

**Verdict: CONFIRMED-BUT-STALE / SCRIPT IS ACTUALLY BROKEN (worse than ChatGPT thought)**

Findings:
1. `step_1_aggregate.parquet` (the exact non-suffixed filename the EDA script requests) **does not exist on disk**. Only `step_1_aggregate_bymonth.parquet` exists.
2. Directly running the EDA script today would **crash with `FileNotFoundError` at Cell 1**, before any of ChatGPT's flagged analyses (Cells 4/5/10/11/12/13) ever execute. Confirmed via direct Python path-resolution test using the script's own root-finding + `PATHS` import logic.
3. `step_1_aggregate_bymonth.parquet` — the file that WOULD load if the path were fixed — is **already true brand×month grain**: 140 brands, max 44 rows/brand (=44 calendar months, matches total_months), mean 28.4 rows/brand, **no `market_id` or `chain_id` column present at all**. This is not brand×region×month; region has already been fully aggregated away in Step 1's `groupby(["brand","period_year","period_month"])`.
4. Cross-referencing `pre_csd_1_load_and_aggregate.py`'s own `GRAIN_CONFIG` comment block (lines 142-152): P0027 Phase 4a-ii **already identified and root-caused this exact grain-conflation problem** — in the context of the MIN_PERIODS derivation specifically — and explicitly states the old `step_1_aggregate.parquet` (pre-rewrite) was brand×region grain, pooling all 9 `DVH_REGION_IDS` per brand, and that this was a "grain-mismatched coincidence" for the old MIN_PERIODS=40 figure. P0027 re-derived MIN_PERIODS=40 against the corrected bymonth data (58/140 brands ≥40 non-zero months, independently confirmed as the same threshold for the right reason).

**Reconciliation**: ChatGPT's diagnosis of the underlying disease (brand×region rows being treated as one per-brand sequence) was **real and already independently discovered and partially fixed by P0027** on 2026-07-12/13, in the context of a different pipeline stage (`engineer_features.py`'s `group_keys` default, and Step 1's aggregation rewrite). What ChatGPT could NOT have known (no repo access): that fix was applied to **Step 1 and the shared feature-engineering module**, but **not to the EDA notebook's own input path** — `pre_csd_1.5_eda.py` line 110 was never updated to point at the new `step_1_aggregate_bymonth.parquet` filename. So the EDA script is currently orphaned/dead code relative to the rest of the pipeline: it can't run at all, and if its path were trivially patched to point at the new file, most of ChatGPT's Section-1-driven cascading concerns (ADF n=396, lag-analysis grain corruption, rolling-window grain corruption, MIN_PERIODS misinterpretation) would **already be resolved**, because the input data is already correct grain.

**Action needed (not yet applied, pending Brian's approval per plan-verification-discipline)**: `pre_csd_1.5_eda.py` line 110 should be updated from `"step_1_aggregate.parquet"` to `"step_1_aggregate_bymonth.parquet"` (or grain-parameterized, mirroring Steps 1-6's `--grain` pattern) so the EDA script actually runs and reflects the current grain-aware pipeline. This is a real, previously-undetected drift bug — not something P0027 flagged, because P0027's Phase 4a-ii work focused on Steps 1-6 and never re-ran/re-checked the EDA notebook itself after the rewrite.

**This is the single most consequential finding**: it means ChatGPT's Section 1 (P0-priority, "must fix before continuing") is simultaneously (a) diagnosing a real historical bug that (b) has already been mostly fixed elsewhere in the pipeline, but (c) surfaces a genuinely new, undetected gap — the EDA script itself was never updated to match — that only exists BECAUSE of P0027's own prior fix, not despite it. Every other ChatGPT finding that assumes "the EDA script currently analyzes brand×region×month data" needs to be re-read through this lens: mechanically true of the code's stale path/intent, but not true of what the data would look like if the obvious one-line path fix were applied.

---

## Phase 2 — Verification Results (Sections 2-15, forked verification in progress)

### Section 4 — Lag Selection
**ChatGPT's claim**: `|r|>0.1` in ≥50% of brands is an arbitrary threshold ignoring serial dependence, sample size, multiple testing, collinearity; recommends a fixed theoretical set (1,2,3,6,12) validated via rolling-origin CV.

**Verdict: PARTIALLY-VALID** (grain-independent — holds even on the correct bymonth data)
Cell 10 (lines 802-860) confirmed exactly as described: `pct_significant = np.mean(np.abs(arr) > 0.1)`, `Include = pct_significant >= 0.50`. No multiple-comparison correction across 7 lag candidates, no collinearity check between selected lags (Cell 12's window analysis *does* have collinearity pruning — inconsistent rigor between the two cells). This is a real critique of the decision rule itself, independent of the grain bug. ChatGPT's proposed replacement (fixed lag set 1,2,3,6,12) is a defensible default but is itself unvalidated until backed by real rolling-origin CV — the critique of the *current* method is stronger than the specific proposed fix.

### Section 5 — Rolling Window Selection
**ChatGPT's claims**: (a) leakage via correlating against future validation/test outcomes, (b) collinearity checked using only one reference brand, (c) "partial window problem" — growing windows of size 1,2,3...w rather than fixed-size complete windows.

- **(a) leakage**: PARTIALLY-VALID / mischaracterized mechanism. No train/val/test split exists yet when Cell 12 runs (split isn't computed until Cell 13, after). So it's not "leaking from validation/test" literally — there's no split yet to leak from. But it IS real model-selection leakage in the Section-3 sense: window selection uses the full dataset (including what later becomes val/test rows), not train-only. Mechanism ChatGPT names is imprecise; underlying defect is real.
- **(b) single-reference-brand collinearity**: CONFIRMED-VALID. Lines 1010-1011: `ref_brand = sample_brands[0]` — collinearity pruning uses exactly one brand, unlike Cell 10's lag analysis which aggregates across all stable brands. Real internal inconsistency.
- **(c) partial/growing windows**: CONFIRMED-VALID. Lines 972-975: `series[max(0, i-w):i].mean()` produces a genuinely partial window for `1 <= i < w` (e.g., i=1 gives a 1-observation "mean" for a 13-window). The code's own comment shows awareness of the `i=0` NaN edge case but doesn't fix the still-partial windows for `i` between 1 and w-1. ChatGPT's fix (`shift(1).rolling(w, min_periods=w)`) is the standard correct pattern.

### Section 6 — Stationarity/ADF
**ChatGPT's claim**: ADF at n≈396 is a brand×region concatenation artifact; "70% stationary raw → log transform optional" is methodologically insufficient; recommends KPSS.

- **n=396 framing**: FALSE as currently stated, for a subtler reason than "already fixed." Cell 4 (line 320) drops brands with `len(series) < 10` and runs ADF on `df[df['brand']==brand]` directly — on the CURRENT true-bymonth data (max 44 rows/brand, confirmed) this would give n≤44, not n=396, if the script could load data at all. Since the script can't currently run (file-not-found), ChatGPT's n=396 evidence must have come from an older run/artifact (pre-P0027 Phase 4a-ii, when the file existed and was brand×region grain). Accurate for that older artifact; not true of the current code-as-written.
- **"70% stationary, optional" characterization**: CONFIRMED-VALID as a fair paraphrase of a majority-vote rule (`log_necessary = True if (n_log+n_diff) >= n_raw else False`, lines 364-369) that is indeed a same-flavor unjustified-threshold pattern. The critique that ADF alone can't determine variance-stabilization benefit is statistically correct and grain-independent.
- **KPSS recommendation**: CONFIRMED-BUT-ALREADY-FIXED-IN-P0027, with a twist. P0027 Task 6 already ran KPSS alongside ADF for CSD/Energidrikke and found the result ambiguous (not a clean I(1) verdict) — so the ask itself is already answered. BUT P0027 Task 13 later found that Task 6's own ADF p=0.140 was ITSELF the same region-conflation artifact ChatGPT describes here (corrected value: median p=0.3535/mean 0.4068, after summing across regions per brand first) — meaning P0027 independently rediscovered and root-caused essentially the same underlying bug via a different task. However, that Task 6 KPSS run was on the OLD region-conflated data and has not been re-run on the now-corrected bymonth grain — so KPSS-on-correct-data is still technically outstanding, a genuine residual gap.

### Section 8 — Decomposition Model Selection
**ChatGPT's claim**: comparing additive vs. multiplicative residual variance directly is invalid — different scales (sales units vs. ratios), so multiplicative spuriously "wins."

**Verdict: CONFIRMED-VALID** — a real, self-contained statistical defect, fully confirmable without running code. Cell 8 lines 623-626 confirmed exactly: `resid_var_add = np.nanvar(decomp_add.resid)` vs `resid_var_mult = np.nanvar(decomp_mult.resid)`, direct comparison, no scale normalization. `statsmodels`' multiplicative decomposition residuals are `observed / (trend*seasonal)`, centered near 1.0 with inherently tiny variance by construction vs. additive residuals on the raw sales-units scale (potentially thousands). Multiplicative will near-always "win" this comparison regardless of actual fit quality. Textbook error, independent of grain/data.

### Section 9 — MIN_PERIODS Misinterpretation
**ChatGPT's claim**: MIN_PERIODS=40 was derived from brand×region-conflated data (40 rows ≠ 40 months when 9 markets are pooled), needs recalculation on true per-series monthly counts.

**Verdict: CONFIRMED-BUT-ALREADY-FIXED-IN-P0027** — near-verbatim rediscovery of a documented, already-resolved issue. Direct quote, `pre_csd_1_load_and_aggregate.py` lines 142-152: *"min_periods for 'bymonth' was re-derived (2026-07-12 continuation) directly from the leakage-fixed brand x month rollup ... NOT copied from the CSD EDA notebook's original '40' — that number was computed on brand x region grain (step_1_aggregate.parquet, groupby('brand') pooling all 9 regions), which measures a different quantity than true brand x month non-zero-months ... independently confirms 40 as the entry point into the 'High' quality tier ... retaining 58/140 brands (41.4%)."* This is the exact bug ChatGPT names, already root-caused and re-derived on correct data — the "40" surviving is explicitly documented as coincidental, not laundered. **Residual gap**: Cell 5 of `pre_csd_1.5_eda.py` itself was never edited to reflect this — it's still computing from whatever `INPUT_AGGREGATE` resolves to (currently nonexistent). The notebook's own displayed MIN_PERIODS rationale is stale/orphaned relative to `GRAIN_CONFIG`'s corrected value, even though the correct number now lives authoritatively in Step 1's config. Valid critique of the notebook file specifically, even though the pipeline already has the fix elsewhere — same pattern as Section 1.

---

### Section 2 — Missing Values vs Missing Periods
**ChatGPT's claim**: The notebook checks nulls but never audits calendar completeness (e.g., a silently-absent March with no null row to flag it).

**Verdict: PARTIALLY-VALID** — genuinely new gap for this script, not duplicated by P0027. Cell 1's only missingness check is `df.isnull().sum()` on existing columns; no date-reindexing / expected-vs-observed-months logic anywhere in the file (Cell 5b classifies zero-*sales* runs, not *missing rows*). P0027's Task 7/14 work happened on a downstream, already-reindexed feature matrix (Steps 1-6 output) and answers "why is this reindexed row NaN" — a different question from "does this EDA script audit calendar-completeness on its own input." Real, uncovered gap in this specific script.

### Section 3 — Descriptive vs Model-Selection EDA (Leakage)
**ChatGPT's claim**: Full dataset (not train-only) drives lag/window/seasonal-month/MIN_PERIODS selection — model-selection leakage.

**Verdict: CONFIRMED-VALID**, and distinct from any P0027 fix. Cells 5, 6, 10, 12 all operate on the full `df` loaded in Cell 1; Cell 13 (the split) is defined textually and executionally AFTER all of them. P0027's leakage fix (`group_keys` in `engineer_features.py`) addressed cross-*series* row-conflation, not cross-*split* use of val/test data to pick hyperparameters — a different failure mode P0027 never touched. Real, unaddressed methodological gap.

### Section 10 — Train/Val/Test Split
**ChatGPT's claim**: 24mo train / 6mo val / 14mo test, ~11 usable train rows after 13-period warmup, single validation fold ties model selection to one seasonal segment.

**Verdict: CONFIRMED-VALID**. `train_periods=24`, `val_periods=6`, `WARMUP_PERIODS=13` — arithmetic (24−13=11) checks out exactly. No rolling-origin/fold logic exists anywhere in the script. Holds independent of the grain bug — a design property of Cell 13's code, not data-dependent.

### Section 11 — Promotion Analysis
**ChatGPT's claim**: All-zero `promo_units` → NaN correlation → unsupported "promotions work/harm" language.

**Verdict: PARTIALLY-VALID**. Cell 9b already guards against this (`if sub_promo.empty: print("No promo activity... skipping")`) — but Cell 15 does NOT: `corr_promo = corr_pearson.loc[...]` then unconditionally prints `"promos {'work' if corr_promo>0 else 'harm'} sales"` with no NaN check. If `corr_promo` is NaN, `NaN>0` evaluates `False`, so the script would silently print "Weak positive = promos harm sales" — a meaningless statement stated as fact. ChatGPT's fix applies specifically to Cell 15's unguarded print, not the whole notebook (Cell 9b already has it). The causal-language critique ("work"/"harm" wording) is accurate to the actual text regardless of current promo_units variance.

### Section 12 — Distribution/weighted_dist Leakage
**ChatGPT's claim**: `weighted_dist` may be contemporaneous; using it un-lagged for forecasting risks leakage.

**Verdict: OUT-OF-SCOPE-FOR-THIS-SCRIPT**. The only `weighted_dist` reference (Cell 15) is a purely descriptive Pearson correlation with a "matters"/"irrelevant" label — no lag, no feature-availability discussion, no feature construction at all (this script doesn't build model features; that's Steps 4-6). ChatGPT, lacking repo access, couldn't know the EDA/feature-engineering split exists across separate files and over-scoped a legitimate abstract concern onto the wrong file. The correct place to check this is `pre_csd_4_engineer_features.py` / `_shared_modules/engineer_features.py`.

---

## Phase 3 — Reconciled Report

### Consolidated Table

| # | Section | Claim | Verdict | Recommended Action |
|---|---------|-------|---------|---------------------|
| 1 | Grain (P0) | Script analyzes brand×region×month (396 obs/brand) via `groupby('brand')` only | **Stale/broken, worse than ChatGPT thought** — script can't even run (`step_1_aggregate.parquet` doesn't exist); if it could load `step_1_aggregate_bymonth.parquet`, grain is already correct (no market_id/chain_id, max 44 rows/brand) | **Fix**: update `INPUT_AGGREGATE` (line 110) to `step_1_aggregate_bymonth.parquet` (or `--grain`-parameterize to match Steps 1-6) |
| 2 | Missing periods vs missing values | Notebook checks nulls, never audits calendar-gap completeness | **Confirmed, new gap** — not covered by P0027's row-level MNAR work (different data object) | Add a per-brand expected-vs-observed-months audit to Cell 1 or a new cell |
| 3 | Descriptive vs model-selection EDA (leakage) | Full dataset drives lag/window/seasonal/MIN_PERIODS selection = model-selection leakage | **Confirmed, new gap** — distinct from P0027's group_keys leakage fix (different failure mode) | Requires methodology decision: split before Cell 4, or explicitly document as "descriptive-only, not yet validated" until Phase 2-style rolling-CV work is added |
| 4 | Lag selection threshold | `\|r\|>0.1` in ≥50% brands is arbitrary, no correction for multiple testing/collinearity | **Confirmed, grain-independent** | Consider fixed theoretical candidate set + rolling-origin CV comparison (P2, larger effort) |
| 5a | Rolling window "leakage" | Windows selected via correlation with future val/test outcomes | **Partially valid**, mechanism mischaracterized (no split exists yet at that point) — but real model-selection leakage per #3 | Same fix as #3 |
| 5b | Rolling window single-brand collinearity | Collinearity pruning uses only `sample_brands[0]` | **Confirmed** | Aggregate collinearity check across multiple/all stable brands, mirroring Cell 10's cross-brand approach |
| 5c | Rolling window partial-window bug | Growing windows (i=1,2,3...w) instead of fixed-size w | **Confirmed** | Switch to `shift(1).rolling(w, min_periods=w)` pattern |
| 6a | ADF n=396 | Concatenation artifact invalidates ADF | **False as currently stated** — code already computes per-brand ADF correctly; n=396 evidence is from a stale pre-fix artifact | No action needed on the ADF logic itself; resolves automatically once #1 is fixed |
| 6b | "70% stationary → optional" | ADF-only reasoning insufficient for transform decision | **Confirmed**, grain-independent | Minor — reframe majority-vote language, not urgent |
| 6c | KPSS recommendation | Add KPSS alongside ADF | **Already done in P0027 Task 6** (ambiguous result) — but that run was on old region-conflated data; needs re-run once #1 is fixed | Re-run KPSS+ADF after #1 fix, on correct bymonth grain |
| 7 | Decomposition model selection | Additive vs multiplicative residual variance comparison is scale-invalid | **Confirmed, self-contained statistical error**, grain-independent | Fix Cell 8: compare additive-on-raw vs additive-on-log, not additive-vs-multiplicative variance directly |
| 8 | MIN_PERIODS=40 misinterpretation | Derived from region-conflated data, needs recalculation | **Already fixed in P0027** (Phase 4a-ii) in `GRAIN_CONFIG`, but Cell 5 of the notebook itself was never updated to match — same pattern as #1 | Same fix as #1 — notebook needs to load correct data; MIN_PERIODS=40 conclusion itself does not change |
| 9 | Train/val/test split | 24/6/14 split, ~11 usable train rows after warmup, single val fold | **Confirmed**, grain-independent, real design gap | P2 — rolling-origin CV is a larger methodology change; flag as known limitation for now unless Brian wants to invest here |
| 10 | Promotion analysis | All-zero promo_units → invalid "work/harm" language | **Partially valid** — Cell 9b already guards, Cell 15 does not | Small fix: add NaN/zero-variance guard to Cell 15's promo correlation print, soften causal language |
| 11 | weighted_dist leakage | Contemporaneous feature risks leakage if used un-lagged | **Out of scope for this script** — no feature construction happens here | No action in this file; flag as a check-item for Steps 4-6 (`engineer_features.py`) if not already handled there |

### Executive Summary

**The single dominant finding**: the EDA script (`pre_csd_1.5_eda.py`) is currently **non-functional** — its hardcoded input path (`step_1_aggregate.parquet`) was orphaned when P0027's Phase 4a-ii (2026-07-13, same day as this analysis) rewrote Step 1 to output grain-suffixed files. This is a genuinely new finding neither ChatGPT nor P0027 explicitly caught: ChatGPT couldn't know about the rewrite (no repo access), and P0027's own work never circled back to re-run/re-check the EDA notebook after changing Step 1's output contract.

**Once that one-line path fix is applied**, a large fraction of ChatGPT's most dramatic claims (n=396 concatenation, brand×region grain corruption cascading through ADF/lag/rolling/MIN_PERIODS) resolve automatically, because the underlying data is already correct grain (confirmed: `step_1_aggregate_bymonth.parquet` is genuine brand×month, no market_id/chain_id column).

**What remains genuinely open after the path fix**, roughly by severity:
1. **Model-selection leakage** (#3, #5a) — real, unaddressed, distinct from P0027's already-fixed leakage bug. All of Cells 4-12 use the full dataset, not train-only.
2. **Missing-period audit** (#2) — real gap, not covered by P0027's row-level missingness work (different data object/question).
3. **Decomposition model-selection statistical error** (#7) — self-contained, textbook-level bug, easy fix.
4. **Several smaller methodological softness items** (#4 lag threshold, #5b single-brand collinearity, #5c partial windows, #6b ADF-only transform reasoning, #10 promo NaN guard) — real but lower-severity, mostly easy fixes.
5. **KPSS re-run needed** (#6c) — P0027 already did this work once, just on stale data; needs re-running post-#1-fix, not new work.
6. **Split design** (#9) — real, but a bigger methodology investment (rolling-origin CV); recommend flagging as documented limitation rather than an immediate fix, pending Brian's call.
7. **weighted_dist leakage** (#11) — not this script's concern; worth a quick check in Steps 4-6 but not an EDA-script fix.

**Handoff to P0027**: Since P0027 is paused specifically waiting on this analysis before deciding on Phase 5 (extending to 3 more categories), the key message back to that plan is: **don't extend the EDA methodology to other categories until the notebook itself is fixed and re-run** — right now the "template" P0027's Phase 5 would copy is broken and pointing at nonexistent data. The path fix (#1) should happen first, then a decision on how much of #2-#11 to address before templating, since some (leakage, missing-period audit) are methodology-level and would otherwise get baked into all 4 categories' EDA if copied as-is.

**No code changes have been made in this plan.** All items above are pending Brian's explicit go-ahead per [[plan-verification-discipline]].
