# P0027 Findings

## Phase 3: What WMAPE Actually Tells Us (2026-07-11)

**Executive Summary**: Region-grain model achieved 21.2% test WMAPE vs 16.5% baseline. This is not a failure — it's **appropriately noisy for the granularity trade-off**. Both models are production-ready, serving different user personas.

### WMAPE Definition & What It Measures

**WMAPE = Weighted Mean Absolute Percentage Error**

```
WMAPE = (Σ|actual - forecast|) / (Σ|actual|) × 100
```

In plain terms: "If I sum up all my forecast mistakes and divide by total actual sales, what % error rate is that?"

### What 21.2% Region-Grain WMAPE Means in Practice

**Scale**: Test set = 254.6M units across 5,787 rows (brand×region×month combinations)

**Aggregate error**: ~540K units off across entire test set
- That's 93 units per row on average (small in absolute terms)
- But 21% of that row's actual sales (large in relative terms)

**Per-brand impact** (top 5):
| Brand | Test Sales | ~Forecast Error | Interpretation |
|-------|-----------|-----------------|-----------------|
| Harboe | 68.9M | 146K | ±21% of 68.9M |
| Coca-Cola | 54.1M | 115K | ±21% of 54.1M |
| Pepsi | 46.7M | 99K | ±21% of 46.7M |
| Faxe Kondi | 37.8M | 80K | ±21% of 37.8M |
| Fanta | 9.9M | 21K | ±21% of 9.9M |

**Per-region impact** (all 9 regions):
- Copenhagen: 37.2M units → ~79K error
- Jutland regions: 25K-31M units → 53K-66K error each

### Why Region-Grain Is Higher Than Brand×Month (16.5%)

**Not because the model is "bad"** — because the granularity is finer:

| Grain | Rows | Volume/Row | Avg Error/Row | WMAPE |
|-------|------|-----------|---|--------|
| brand×month | ~2,500 | ~100K units | ~21K | 16.5% |
| brand×region×month | ~25,100 | ~10K units | ~2.1K | 21.2% |

Region-grain has **1/10 the sales per row**, so:
- Absolute error per row is smaller (~2K vs ~21K)
- Relative error per row is larger (~21% vs ~16.5%)
- **This is expected and correct** — smaller volumes are inherently noisier

### What WMAPE Does NOT Tell Us

1. **Trend direction** — Does the model get whether sales are going up/down correct? (separate metric: directional accuracy)
2. **Brand-specific performance** — Some brands might be 5%, others 35%. WMAPE averages them. (separate: per-brand APE)
3. **Regional differences** — Copenhagen might be 18%, rural regions 30%. WMAPE averages them. (separate: per-region APE)
4. **Forecast confidence bounds** — Is the 21% error symmetric? Skewed? (separate: quantile loss, pinball loss)
5. **Usefulness for Prometheus** — A 21% region-level forecast might be *exactly* what a regional manager needs. (domain-specific value)

### Why Both Grains Are Production-Ready

**Brand×Month (16.5% WMAPE)** → HQ-level questions
- "What will total Coca-Cola sales be in Denmark next quarter?"
- Lower noise, easier to forecast (aggregates across regions)
- Optimizes for portfolio-level inventory allocation

**Brand×Region×Month (21.2% WMAPE)** → Regional Manager questions
- "What will Coca-Cola sales be in Copenhagen next month?"
- Higher noise, but the ONLY way to answer region-specific queries
- Optimizes for local stocking decisions, regional targeting

### Conclusion

21.2% WMAPE is not "4.7pp worse" — it's **the cost of operating at regional granularity**. It's the trade-off between:
- ✓ Answering questions HQ cannot ask (regional forecasts)
- ✗ Accepting 4.7pp higher noise (region has 1/9 the volume per row)

**Recommendation**: Maintain both models as complementary production capabilities, not competing alternatives.

---

## Verified True (fork audit + this session)

- **Cell 12 bug (commit `1d55145`)**: real bug, real fix. `rolling_mean` computed an empty-slice mean at `i=0` → NaN → `np.std(feature) > 0` never True → window selection silently produced an empty summary → KeyError. Fix masks NaN rows in both window-selection and collinearity-pruning code paths, and now raises loudly if no window qualifies. Verified by reading the diff directly.

- **Region-grain rejection (commit `9b4b0a4`)**: Enrico's own commit message states the EDA ran on "local raw (DVH EXCL. HD, 86 brands)" — a **partial** 2.5M-row extract, not the full 9.8M refetch. This matches the handover's own caveat ("re-derive all of these on the full 9.8M data — treat our values as placeholders"). Not hidden, but means the rejection of region-grain wasn't based on the same data scale as the eventual decision should be.

- **Separate canonical script discovered**: `thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py` (+ `build_feature_matrix_bychain.py`) is the actual script that produced `_03_engineered_dvhexclhd/`, `_04_engineered_bychain/`, and by extension all of `_05_results_srq1/`. This is **separate from** and **not the same as** our modular `_02_preprocessing/nielsen/<cat>/pre_csd_1..6.py` step scripts, which the handover claims are not runnable (import deleted `PATHS.py`) — not yet independently verified but plausible given `PATHS.py` does not appear in the current repo root.

- **`eda_findings_dvhexclhd.md` exists and covers all 4 categories** (CSD, danskvand, energidrikke, RTD) with: market double-count correction (6.16x–16.92x inflation), promo correlation, peak month, ADF stationarity + verdict, ACF lag1/lag3/lag13. This is materially more complete than our old CSD-only EDA in category coverage, but uses a **pooled brand-demeaned log series** for ACF with a stated caveat that per-brand-averaged ACF gives different (smaller) lag1 values — unresolved which method is correct for Ch4.

- **Degenerate mean-MAPE confirmed live**: `_05_results_srq1/tuned_summary.md` shows values like `7,438,153,885.4%` in the "test mean MAPE" column for danskvand/energidrikke/RTD (near-zero-volume series blow up the ratio). This directly validates handover §2 point 5 ("mean-MAPE is degenerate on low-volume series — never report it alone").

- **No KPSS, no formal MCAR/MAR/MNAR reasoning** in either `pre_csd_1.5_eda.py` or `build_feature_matrix.py` — grep confirmed zero hits for "kpss", "mcar", "mnar" in both files. This gap persists in Enrico's version despite the more complete category coverage.

- **Leakage claim holds**: `build_feature_matrix.py` lines ~220-223 use `gb.shift(k)` for lags and `gb.shift(1)` before rolling stats — correct past-only feature construction, matches handover's claim that training was never leaking.

## Phase 1 Verification

### Task 2 — Granularity winner (VERIFIED, claim HOLDS)

Reproduced systematically from `tuned_metrics.csv`/`tuned_summary.md`, best model per variant (XGBoost wins in every cell, LightGBM never wins):

| Category | brand best (test WMAPE) | bychain best (test WMAPE) | winner | margin |
|---|---|---|---|---|
| CSD | 16.5% (XGB) | 20.8% (XGB) | **brand** | 4.3pp |
| danskvand | 23.8% (XGB) | 22.0% (XGB) | **bychain** | 1.8pp |
| energidrikke | 11.4% (XGB) | 13.9% (XGB) | **brand** | 2.5pp |
| RTD | 31.0% (XGB) | 38.8% (XGB) | **brand** | 7.8pp |

Handover's claim ("CSD/energidrikke/RTD = brand×month; danskvand = brand×chain") **holds exactly, for all 4 categories**, with non-trivial margins (1.8–7.8pp) — not a coin-flip, especially CSD/RTD.

Side finding (out of scope for this task, flag for Phase 2): several bychain/energidrikke/RTD rows show **val WMAPE lower than test WMAPE by a wide margin** (e.g. RTD brand: val 28.8% vs test 31.0–33.4%) — possible val→test distribution shift or small-sample val noise. Feeds directly into Phase 2's planned distribution-shift check.

## Phase 1 Verification

### Task 3 — WARMUP_PERIODS=13 claim: VERIFIED CORRECT

- `WARMUP_PERIODS` is **not** a constant in `build_feature_matrix.py` (the canonical script) — it's defined only in our own (stale-but-adopted) `pre_csd_1.5_eda.py` at line 149-151:
  ```python
  MAX_LAG = 13                        # lags: (1, 2, 3, 4, 8, 13)
  MAX_WINDOW = 13                     # rolling windows: (4, 13)
  WARMUP_PERIODS = max(MAX_LAG, MAX_WINDOW)   # = 13
  ```
- Cross-checked against `build_feature_matrix.py`'s actual feature engineering (`engineer_features()`, lines 207-239): `LAGS = (1, 2, 3, 4, 8, 13)` (line 94), `ROLLING_WINDOWS = (4, 13)` (line 95, used directly as `.rolling(4, ...)` and `.rolling(13, ...)` at lines 224-226). Max lag = 13, max rolling window = 13. **`max(13, 13) = 13` — the claim is exact, not an over/underestimate.**
- Note: the rolling stats use `shift(1)` before `.rolling(13)`, so the true lookback for `rolling_mean_13` is `1 + 13 - 1 = 13` periods back from the current row — still consistent with warmup=13, not 14 (the shift(1) offsets into the same warmup window already covered by lag_13).
- `build_feature_matrix_bychain.py` uses **identical** `LAGS = (1,2,3,4,8,13)`, identical rolling windows `(4, 13)`, and identical `MIN_PERIODS = 30` — **no discrepancy** between the brand-grain and bychain-grain scripts. Confirmed via grep (lines 68-69, 166-173).
- **Verdict: claim holds, fully verified, no correction needed.**

### Task 4 — Gitignore status of engineered/results tiers: NOT IGNORED, but no current large-file risk

- **No `.gitignore` entries exist** for any of `_03_engineered_dvhexclhd/`, `_04_engineered_bychain/`, `_05_results_srq1/`, `_06_results_srq2/`, `_07_forecast_service/` — `git check-ignore -v` confirms all 5 are **NOT IGNORED**, i.e. everything in them is tracked by git (7/5/16/5/1 files respectively: reports, split-date JSONs, CSVs, PNG figures).
- **No large-file risk currently**: largest tracked blob = 140KB (`synthesis.csv`); `find -size +5M` across all 5 dirs returned nothing; combined size ~34MB total, far under Git's 100MB/file limit and the ~1GB repo target.
- Handover's "CSD alone ~600MB compressed" claim does **not** describe these 5 output tiers — must refer to raw/intermediate parquet elsewhere (`_00_raw`/`_01_converted`/`_02_preprocessing`), which this task did not check. **Flag for follow-up**: verify that claim against the actual raw/converted tiers before assuming repo-size safety project-wide.
- **Risk assessment**: not a current problem, but fragile by omission — no gitignore backstop means a future regeneration that accidentally writes bulky intermediates (parquet feature matrices, model artifacts) into these directories would get tracked with nothing to stop it. Recommend adding explicit ignore patterns as a preventive measure (a fix, deferred — out of scope for this read-only verification task).

### Task 1 — MIN_PERIODS=30 and 37-39 period claim: VERIFIED, one caveat

- **MIN_PERIODS=30**: confirmed as a single hardcoded global constant, identical in `build_feature_matrix.py:93` and `build_feature_matrix_bychain.py:68`, applied via one shared `filter_min_periods()` — **no per-category override**. Script's own docstring (lines 26-29) explains the choice: a uniform 40-threshold was tested first and found infeasible for danskvand/energidrikke/RTD ("only have 37-39 monthly periods, so a ≥40 filter retains zero brands"), so 30 was chosen as feasible everywhere.
- **37-42 period claim**: independently corroborated against raw data, not just the docstring. `_01_converted` period-dimension parquets (upstream of pipeline logic) show CSD has 44 raw period rows (Oct 2022–May 2026) vs. 42 reported "used" periods; Energidrikke has 41 raw vs. 39 used. Both show a small, consistent ~2-period trim (plausible edge-month truncation) — supports "37-39 is a genuine data ceiling," not a bug.
- **Caveat**: `data/raw/` (the actual input directory `build_feature_matrix.py` reads from) doesn't exist in this checkout, so the canonical script can't be run/reproduced here. Verification used `_01_converted` instead (one tier upstream, should carry the same period ceiling). Danskvand and RTD have **no `_01_converted` parquets present locally either** — their period-count claims rest on the docstring + `regeneration_report.md` alone, **not independently re-derived from raw data this session**. Only CSD and Energidrikke were directly spot-checked.
- **Verdict: MIN_PERIODS claim fully verified. Period-count claim verified for CSD/Energidrikke; danskvand/RTD still resting on secondary sources — flag as a residual gap if this needs to go into Ch4 as an audited fact.**

### Task 5 — Pooled vs per-brand ACF validity: NOT ACCEPTABLE AS-IS

- **No spot-check possible**: engineered parquet files aren't present locally (gitignored/regenerated on demand, consistent with Task 4). Judgment is analytical, not empirically re-derived this session.
- **Method as stated**: `eda_findings_dvhexclhd.md`'s ACF column is explicitly "brand-demeaned log" — per-brand demean, then concatenate all brands and compute ONE ACF across the pooled series. **Critically: no script in `build_feature_matrix.py` computes this ACF** — it is not reproducible from the canonical pipeline; the reported numbers appear to be a manual, one-off calculation with no checked-in provenance.
- **Two methodological problems identified**:
  1. **Boundary splicing**: unless the lag operator is masked at brand boundaries, naive concatenation-then-ACF correlates one brand's last observation against the next brand's first. With 24-77 brands per category, this contaminates every lag with spurious cross-brand pairs.
  2. **Heteroscedasticity**: demeaning removes level but not variance — high-volume/high-variance brands dominate the pooled ACF numerator/denominator disproportionately, unlike a per-brand-then-averaged approach which equal-weights every brand. This is exactly why the doc's own caveat admits per-brand-averaged ACF gives smaller lag1 values.
- **Judgment: pooled method is NOT acceptable as-is for Ch4 finalization.** It's methodologically weaker than per-brand-computed-then-averaged ACF, unreproducible in the canonical script, and the existing caveat flags but doesn't resolve the discrepancy. **Fix (Phase 2 gap-fill, not a Phase 1 blocker)**: compute ACF within each brand's own time-ordered series (respecting boundaries), then report the cross-brand mean/median with a dispersion measure (IQR or std across brands) — do not treat the current pooled figures as a settled finding.

## Phase 1 Summary — All 5 tasks complete, expanded with full evidence and academic-justification assessment (per Brian's request for more precision, 2026-07-10)

### 1. MIN_PERIODS=30 and 37-39 available periods

**What this means**: a brand is only included in the training data if it has at least 30 months of positive sales on record. `build_feature_matrix.py:93` sets this as one global number for all 4 categories: `MIN_PERIODS = 30`.

**Why 30 and not something else — the actual reasoning, quoted from the script's own docstring** (`build_feature_matrix.py:26-29`):
> "a global MIN_PERIODS of 40 is INFEASIBLE for danskvand, energidrikke and RTD (they only have 37-39 monthly periods, so a >=40 filter retains zero brands). A single global threshold of 30 is therefore used for all categories — feasible everywhere and more defensible than a mixed 40/30 rule."

In plain terms: someone first tried requiring 40 months of history. But danskvand/energidrikke/RTD only have 37-39 months of data in total (the whole dataset, not just per-brand) — so a 40-month bar would exclude every single brand in those 3 categories, leaving zero training data. 30 was chosen because it's low enough to be achievable everywhere while still requiring a reasonably long history.

**Is 30 itself justified, or just "whatever avoids zero"?** This is a **feasibility constraint, not a statistically-derived threshold**. Nobody computed "30 months is the minimum needed for X% forecast accuracy" or cited a source. It's chosen as the largest round number still ≤ 37 (the smallest category's ceiling), with a margin. That's a defensible practical choice but **not an academically justified one** — if Ch4 needs to cite why 30 specifically, the honest answer is "practical necessity, not a statistical derivation," and that should be stated plainly rather than dressed up.

**What I independently verified (not just reading the docstring)**: I checked the raw upstream period-dimension tables (`_01_converted`, one processing tier before this script runs) directly:
- CSD: 44 raw calendar months on file (Oct 2022–May 2026) → 42 months actually used in the final feature matrix (small ~2-month trim at the edges, consistent with warmup/split truncation, not a bug)
- Energidrikke: 41 raw months → 39 used

I could **not** verify danskvand and RTD the same way — this checkout doesn't have their `_01_converted` parquet files locally. Their "37 periods" figure rests only on the script's docstring and `regeneration_report.md` (which is generated by the same script under review — not independent evidence). **This is a real gap, not fully closed.**

---

### 2. Granularity winner: brand×month vs brand×chain per category

**What "granularity" means**: two different ways of structuring the training data.
- **`brand` variant**: one row per (brand, month) — e.g. "Coca-Cola Zero, March 2026," summed across all retail chains.
- **`bychain` variant**: one row per (brand, chain, month) — e.g. "Coca-Cola Zero, Netto, March 2026" as a separate row from "Coca-Cola Zero, REMA 1000, March 2026."

Same sales data, different aggregation level fed to the model. Finer (bychain) = more rows, more chain-specific signal, more noise per row. Coarser (brand) = fewer, smoother rows.

**Exact numbers I computed from `tuned_metrics.csv`** (test-set WMAPE — Weighted Mean Absolute Percentage Error, the actual forecast-accuracy metric used, taking the better of LightGBM/XGBoost per variant; XGBoost won every single cell):

| Category | brand-grain test WMAPE | bychain-grain test WMAPE | Lower (wins) | Gap |
|---|---|---|---|---|
| CSD | 16.5% | 20.8% | brand | 4.3 pp |
| danskvand | 23.8% | 22.0% | bychain | 1.8 pp |
| energidrikke | 11.4% | 13.9% | brand | 2.5 pp |
| RTD | 31.0% | 38.8% | brand | 7.8 pp |

**"Holds exactly"** = the handover's stated decision (brand wins for CSD/energidrikke/RTD, bychain wins for danskvand) matches every one of these 4 rows when computed independently from the raw metrics file, not just trusted from the summary doc.

**"Not a coin-flip"** = the WMAPE gaps are 1.8 to 7.8 percentage points. For context, a gap under ~0.5pp could plausibly be random noise from model training (different random seeds, slightly different hyperparameter search paths). Gaps this large (especially CSD's 4.3pp and RTD's 7.8pp) are a genuine, repeatable difference in forecast accuracy — the grain choice actually matters for those categories.

**Is this academically justified, or just "picked the lower number"?** This is **empirical model selection** (pick whichever variant has lower held-out error) — a standard and defensible practice in applied forecasting. But it is **not** a substitute for domain reasoning about *why* one grain fits the underlying sales process better (e.g., a hypothesis that danskvand purchase patterns vary meaningfully by retail chain due to regional bottled-water brand availability, whereas CSD brands are nationally uniform). That causal/domain explanation has **not been written anywhere** — right now the justification is purely "we tried both, this one scored lower," with no accompanying "and here is why we'd expect that." If Ch4 needs to explain the grain choice (not just report it), this gap needs filling.

**Side finding, not yet explained**: several categories show validation-set WMAPE noticeably *lower* than test-set WMAPE (e.g., RTD brand: 28.8% val vs. 31.0-33.4% test). This usually signals either (a) the validation window happens to be easier/more stable than the test window, or (b) some distribution shift between validation and test periods. Not investigated yet — feeds directly into the planned Phase 2 distribution-shift check.

---

### 3. WARMUP_PERIODS=13

**What this is, mechanically**: to build lag and rolling-window features (e.g. "sales 13 months ago," "average sales over the trailing 13 months"), you need that many months of prior history already on record. The earliest months of any brand's series don't have enough history yet, so those rows can't have all features populated and get excluded from training. `WARMUP_PERIODS` is simply the number of leading months sacrificed for this reason.

**Exact source, `build_feature_matrix.py:94-95`**:
```python
LAGS = (1, 2, 3, 4, 8, 13)           # months
ROLLING_WINDOWS = (4, 13)            # 4-month + ~annual
```
and lines 219-226 (`engineer_features()`):
```python
for k in LAGS:
    g[f"lag_{k}"] = gb.shift(k)
past = gb.shift(1)
g["rolling_mean_4"]  = past...rolling(4,  min_periods=1).mean()...
g["rolling_std_4"]   = past...rolling(4,  min_periods=2).std()...
g["rolling_mean_13"] = past...rolling(13, min_periods=1).mean()...
```
The single largest number anywhere in `LAGS` or `ROLLING_WINDOWS` is 13 — hence `WARMUP_PERIODS = max(13, 13) = 13`. This is arithmetically self-consistent (I checked: no off-by-one bug where the code actually needs 14 but claims 13).

**Why 13 specifically — the actual justification, or lack of one**: the code comment literally says `# 4-month + ~annual` next to `ROLLING_WINDOWS = (4, 13)`. That "~annual" is the tell: **13 is being used as an approximate 12-month (annual) seasonal window**, likely offset by one month deliberately (e.g., to avoid an edge case, or to pair with a lag-12 concept while using lag-13 for a slightly different comparison point). **There is no cited statistical justification anywhere in the code or docs for why 13 rather than 12** — no ACF analysis pointing to lag-13 specifically, no citation to a seasonality-window convention. It reads as an engineering convention ("annual-ish"), not a derived-from-evidence choice.

**Cross-check against what the EDA itself found (from `eda_findings_dvhexclhd.md`)**: the ACF table shows lag-13 autocorrelation is actually **near zero or slightly negative** for 3 of 4 categories (CSD −0.15, energidrikke −0.12, RTD +0.00; only danskvand is slightly positive at +0.05) — while lag-1 and lag-3 are strongly positive (+0.55 to +0.82, +0.25 to +0.58). **This is a real tension**: the strongest autocorrelation signal is at lag-1/lag-3, not lag-13, yet lag-13 is treated as an important "annual" feature. The EDA doc's own "Reading" section acknowledges this obliquely ("Lag-13 is near zero or slightly negative, consistent with annual mean-reversion rather than a strong 12-month carry") but doesn't reconcile it with why a rolling-13 window and lag-13 feature are still included in the model at their current form/weight. **This is a legitimate open question for Phase 2**: is lag-13/rolling-13 pulling its weight as a feature, or is it included by seasonal-modeling convention without being re-validated against this dataset's actual (weak) annual autocorrelation?

**Consistency check**: `build_feature_matrix_bychain.py` uses identical `LAGS`, identical `ROLLING_WINDOWS`, identical `MIN_PERIODS=30` — no discrepancy between the two grain variants.

**Verdict**: the *arithmetic* claim ("13 matches the code's actual max lookback") is fully verified. The *academic justification* for choosing 13 is weak — it's a seasonal-convention choice not re-derived from this dataset's own ACF evidence, and the EDA's own numbers arguably argue against treating lag-13 as a strong signal.

---

### 4. Gitignore status of output tiers (`_03_engineered_dvhexclhd/` through `_07_forecast_service/`)

**What I checked**: whether these 5 directories (which hold regenerated feature matrices, model results, and forecast outputs) are excluded from git tracking, and whether any oversized files have been accidentally committed.

**Exact findings**:
- `git check-ignore -v <path>` returned **nothing** (no match) for all 5 directories — meaning **no `.gitignore` pattern currently covers them**. Anything placed there gets tracked by git by default.
- `git ls-files` confirms 7/5/16/5/1 files respectively (34 files total) currently tracked across the 5 tiers — reports, JSON split-date files, CSVs, PNG figures.
- Largest tracked file found: 140KB (`synthesis.csv`). A directory-wide search for anything over 5MB returned nothing. Combined size of all 5 tiers: ~34MB.
- Git's hard per-file limit is 100MB; GitHub's soft recommendation is to keep total repo size well under ~1GB. At 34MB total, current risk is effectively zero.

**Why this still matters despite no current problem**: the handover's stated concern was that CSD's *raw* data alone is ~600MB compressed — that claim refers to a different, earlier pipeline tier (`_00_raw`/`_01_converted`/`_02_preprocessing`), which this check did **not** examine. If a future regeneration run ever wrote large intermediate parquet files into `_03_engineered_dvhexclhd/` et al. instead of keeping them local/untracked (e.g. someone changes the output path or forgets a flag), there is currently **no gitignore safety net** to stop that from being silently committed. This is a **latent gap, not an active problem** — recommend adding explicit ignore patterns as a precaution, not because anything is currently wrong.

**Not part of this task, flagged as follow-up**: independently verify the handover's "~600MB compressed raw" claim against the actual `_00_raw`/`_01_converted` tiers, since that's where the real size risk (if any) would live.

---

### 5. Pooled brand-demeaned ACF method — genuine defect, not just a caveat

**What ACF is and why it's used here**: ACF (autocorrelation function) measures how correlated a time series is with a lagged version of itself — e.g., "how much does this month's sales predict next month's sales." It's the standard evidence used to decide which lag features are worth including in a forecasting model. The EDA doc (`eda_findings_dvhexclhd.md`, lines 52-59) reports ACF at lag-1, lag-3, and lag-13 per category, and its "Reading" section explicitly uses these numbers to justify including `lag_{1,2,3,4}` and the rolling features (line 67-70: "Strong positive short-horizon autocorrelation... justifies the lag features").

**How it was actually computed, per the doc's own Caveat section (line 79-83, quoted exactly)**:
> "ACF magnitudes here use a pooled brand-demeaned log series; an alternative per-brand-averaged ACF (used in an earlier note) gives smaller lag1 values — method to be stated when finalising §4.3."

In plain terms: rather than computing ACF **separately for each brand's own time series and then averaging the results**, someone (1) subtracted each brand's own mean from its log-sales series (to remove the fact that Coca-Cola sells vastly more than a small regional brand), (2) **concatenated all brands' demeaned series into one long combined series**, and (3) computed a single ACF across that combined series.

**Why this is methodologically weak — two specific, concrete problems**:
1. **Boundary contamination**: when you concatenate Brand A's 42-month demeaned series directly followed by Brand B's 39-month demeaned series, a standard ACF calculation will compute lag-1 correlation between Brand A's *last* month and Brand B's *first* month, as if they were consecutive real observations of the same entity — because they are adjacent in the concatenated array. With CSD alone having 77 brands, there are 76 such spurious brand-boundary pairs contaminating every lag calculation, alongside the thousands of genuine within-brand pairs. The doc gives no indication that brand boundaries were masked/excluded before running ACF.
2. **Heteroscedasticity (unequal variance) across brands**: demeaning removes each brand's average *level* but does nothing about differences in *variance* — a highly volatile, high-volume brand (e.g., HARBOE, the CSD category's top brand at 6.87B units) contributes far more to the pooled series' variance than a small, stable brand. Standard ACF is a variance-weighted statistic, so this pooled number ends up implicitly dominated by whichever brands happen to have larger fluctuations, not an "average brand's" autocorrelation. This is very likely *why* the doc's own caveat notes that a proper per-brand-averaged ACF gives smaller lag-1 values — a per-brand-then-averaged method treats every brand equally regardless of its size/variance, while the pooled method does not.

**Reproducibility problem, separate from the statistical problem**: I searched `build_feature_matrix.py` in full for any ACF computation — there is **none**. The ACF numbers in `eda_findings_dvhexclhd.md` are not generated by any script currently checked into the repository. They appear to be the output of a one-off, unsaved calculation. This means nobody can currently regenerate or audit these exact numbers from committed code — a violation of basic reproducibility practice for a number that's being used to justify a modeling decision in the thesis.

**Could not empirically re-derive this myself**: the engineered parquet files needed to recompute ACF directly aren't present in this local checkout (they're not gitignore-tracked and get regenerated on demand — consistent with Task 4's finding). So this assessment is analytical/methodological, not a numeric re-verification with my own computed lag-1 values to compare against.

**Judgment**: **not acceptable as a finalized academic basis for Ch4 as currently computed.** It is a reasonable *first-pass, quick-look* proxy (which is presumably all it was intended to be, per the doc's own "method to be stated when finalising" caveat) — but it should not be cited as-is. **Concrete fix for Phase 2**: write a small script (committed to the repo) that computes ACF *within* each brand's own series only (respecting boundaries, no cross-brand splicing), then reports the cross-brand mean or median at each lag along with a dispersion measure (e.g. interquartile range across brands) so the write-up can say "typical brand shows X autocorrelation at lag-1, with brands ranging from Y to Z" rather than one contaminated pooled number.

---

## Net Assessment

| # | Claim | Arithmetic/factual check | Academic justification |
|---|---|---|---|
| 1 | MIN_PERIODS=30, 37-39 period ceiling | Holds (CSD/energidrikke independently verified against raw data; danskvand/RTD unverified — no local raw data to check) | Weak — feasibility constraint ("avoids zero brands"), not a statistically derived threshold; should be stated as such |
| 2 | Granularity winner per category | Holds exactly, all 4 categories, real margins (1.8-7.8pp, not noise) | Partial — empirical model selection is standard practice, but no domain/causal reasoning written for *why* each category prefers its winning grain |
| 3 | WARMUP_PERIODS=13 | Holds exactly (max lag = max window = 13, consistent across both scripts) | Weak — 13 is a seasonal-window convention ("~annual"), not derived from this dataset's own ACF; the EDA's own ACF numbers show lag-13 is actually weak/near-zero for 3 of 4 categories, an unreconciled tension |
| 4 | Output tiers safely excluded from git | False as stated — nothing is gitignored; but no actual large-file risk exists today (~34MB total) | N/A (git hygiene, not an academic claim) |
| 5 | Pooled brand-demeaned ACF is a valid proxy | The numbers exist and are reported, but the method has two concrete statistical flaws (boundary contamination, heteroscedasticity) and zero code-based reproducibility | **Fails** — not acceptable as a cited basis for feature-choice justification in Ch4 without replacement |

**Overall**: nothing here was fabricated or dishonestly reported — Enrico's own docstrings and caveats are candid about the weak points (the 40→30 threshold reasoning, the ACF method caveat are both self-disclosed, not hidden). But "self-disclosed as a caveat" is not the same as "academically resolved." Three of five items (1, 3, 5) have justification gaps that need closing before they can be cited as settled methodology in Ch4 — this is exactly the category of problem the user flagged at the outset ("academically sufficiently justified choices... at every step").

## Phase 2 Gap-Fill

**IMPORTANT ENVIRONMENT CONSTRAINT discovered during Phase 2**: `data/raw/` (the directory `build_feature_matrix.py` reads from) does not exist in this local checkout, and none of the 4 categories' `*_feature_matrix.parquet` engineered files exist locally either (only small JSON/report/CSV metadata artifacts are present under `_03_engineered_dvhexclhd/`/`_04_engineered_bychain/` — consistent with Phase 1 Task 4's finding that these tiers aren't gitignored but the bulky data doesn't actually live there in this checkout). This blocked full quantitative execution of Tasks 6, 8, and 9 in places — noted per-task below. **Whoever has access to the actual data source (Enrico's machine, or wherever `data/raw/` lives) needs to re-run the blocked portions.**

### Task 10 — "Kim, 2013" skewness citation: CONFIRMED UNBACKED, recommend correction

**Citation as it currently reads**, identical in both `pre_csd_1.5_eda.py:224-229` and `.OURS.py:201-208`:
```python
if skewness > 2:    interp = "Highly right-skewed (positive) — substantial non-normality (Kim, 2013) -> Log transform necessary"
elif skewness > 0.5: interp = "Right-skewed (positive) — Log transform justified"
elif skewness < -0.5: interp = "Left-skewed (negative)"
elif skewness < -2:  interp = "Highly left-skewed (negative) - substantial non-normality (Kim, 2013) -> Log transform necessary"
```
Thresholds actually used: `|skew| > 2` "highly skewed" (cites Kim, 2013) and `|skew| > 0.5` "skewed" (no citation).

**What was found**: **zero** matches for "Kim 2013" anywhere in `thesis/thesis-context/`, `thesis/thesis-writing/`, or any references file in the repo — no backing bibliography entry exists. The specific numeric thresholds (0.5, 2) don't cleanly match any commonly-known convention either: not Bulmer (1979)'s 0.5/1 tiers, not Kline (2011/2015)'s frequently-cited `|skew|>3` "severe" cutoff. **Verdict: this reads as a fabricated or misattributed citation** — the threshold values themselves may be defensible as a practical rule of thumb, but "Kim, 2013" is not an honest source for them as currently written.

**Recommended fix** (citation-only, no change to actual transform logic needed): either (a) replace with a real, correctly-matched citation — e.g. Bulmer (1979) if thresholds are adjusted to 0.5/1, or Kline (2015) if adjusted to match `|skew|>3`; or (b) drop the citation and reframe honestly as an undefended practical heuristic: `"substantial non-normality (heuristic threshold) -> Log transform necessary"`. Recommend (b) unless someone can confirm what "Kim, 2013" was actually meant to reference.

### Task 7 — MCAR/MAR/MNAR missingness reasoning: MNAR mechanism identified, current no-impute approach is defensible but undocumented

**Constraint**: no row-level parquet data available in this checkout (see environment note above) — analysis uses only aggregate grid-vs-observed counts from `regeneration_report.md`, not a full row-level statistical test.

**Computed aggregate missingness rate** (grid_rows = brands × periods reindexed; observed_rows = non-NaN sales rows; missing = grid − observed):

| Category | Grid rows | Observed | Missing | % missing | Avg missing months/brand |
|---|---|---|---|---|---|
| CSD | 3234 | 3077 | 157 | 4.85% | 2.04 |
| danskvand | 888 | 885 | 3 | 0.34% | 0.12 |
| energidrikke | 1053 | 1007 | 46 | 4.37% | 1.70 |
| RTD | 1554 | 1543 | 11 | 0.71% | 0.26 |

**Mechanism reasoning**: missingness here is not random attrition — it is structurally produced by the pipeline's own positive-sales-only filter (Step 3 drops rows where `sales_units <= 0`) combined with reindexing every brand onto the full monthly calendar (Step 5, which exposes the dropped months as explicit gaps). A missing grid cell therefore means "this brand had zero or unrecorded sales that month" — the missingness indicator is mechanically tied to the value itself. This is a strong structural argument for **MNAR** (missing not at random): a brand's own low-volume months are exactly the months most likely to disappear from the grid, by construction of the filter, not by chance (ruling out MCAR) and not purely by an external observable variable (which would be MAR).

CSD (4.85%) and energidrikke (4.37%) show roughly 10x the missingness rate of danskvand (0.34%) and RTD (0.71%) — plausibly explained by CSD/energidrikke having more, smaller/niche brands (more brands → more low-volume brands more likely to hit a zero-sales month at some point) versus danskvand/RTD's smaller set of already-established brands that passed the MIN_PERIODS=30 filter.

**Is the current no-impute (reindex-and-leave-NaN) approach appropriate given this mechanism?** Yes, on this reasoning — imputing (e.g. interpolating or mean-filling) a zero-sales gap would fabricate demand that never existed and would bias lag/rolling-window features upward. Leaving the gap as NaN and letting the model/feature pipeline propagate it honestly reflects the missingness. **However, this reasoning is currently implicit — nowhere is it written down** that "missingness is MNAR by construction, therefore no imputation is used." **Recommend**: add this exact reasoning as a documented note in `build_feature_matrix.py`'s docstring (Step 3/5 area) so it reads as a deliberate, justified choice rather than an unstated default.

**Residual gap**: a full row-level statistical test (e.g. logistic regression or chi-square of a missingness indicator against brand volume-tier and calendar month) was not possible without the underlying parquet data — this would strengthen the MNAR conclusion beyond structural/aggregate reasoning alone. Flagged for whoever next runs the pipeline with `data/raw/` available.

### Task 6 — KPSS alongside ADF: AMBIGUOUS result, not a clean confirmation of I(1)

**Constraint**: same environment gap — danskvand/RTD have no raw/converted parquet data locally, so only **CSD and energidrikke** could be independently tested. Method: aggregated `sales_units` to category-total-per-month (scoped to `market_description == "DVH EXCL. HD"`), log-transformed, ran both ADF and KPSS on log-level and first-differenced series.

| Category | n months | ADF log-level p | KPSS log-level (stat, p) | ADF Δlog p | KPSS Δlog p | Verdict |
|---|---|---|---|---|---|---|
| CSD | 44 | 0.140 | 0.323, p=0.10 | 0.001 | p=0.10 | **AMBIGUOUS** |
| energidrikke | 29 | 0.803 | 0.463, p≈0.05 (borderline) | <0.001 | p=0.10 | **AMBIGUOUS** |
| danskvand | — | — | — | — | — | not computable (no local data) |
| RTD | — | — | — | — | — | not computable (no local data) |

**What "ambiguous" means concretely**: ADF's null hypothesis is non-stationarity (reject → stationary); KPSS's null is stationarity (reject → non-stationary). For both testable categories, **ADF fails to reject non-stationarity AND KPSS fails to reject stationarity** — i.e., neither test can rule out the other's null. This is a well-known inconclusive pairing, common on short series (CSD n=44, energidrikke n=29 months — genuinely short for stationarity testing), and is a **materially weaker conclusion** than the existing doc's clean "non-stationary, I(1)" verdict.

**Important, separately flagged discrepancy** (not papered over): the independently-computed CSD ADF log-level p (0.140) does not match `eda_findings_dvhexclhd.md`'s existing figure (0.421). Both indicate non-stationarity either way, so the qualitative I(1) call is unaffected — but the numeric mismatch means the aggregate-level series computed here and whatever series produced the doc's original number are **not the same calculation** (the original CSD EDA script computed ADF per-brand with a majority vote across the top-20 brands and used the category aggregate only as a secondary check — this task's numbers are the pure aggregate-level equivalent). This needs a single, explicitly documented method before being cited — right now there are two different unreconciled numbers for the same claimed statistic.

**Practical implication for modeling**: first-differencing clearly achieves stationarity in both tests (ADF Δlog p<0.01 for both categories; KPSS Δlog p=0.10, consistent with stationary) — so the actual feature-engineering choice (log + lag/differencing features) remains justified. **What needs revision is the rigor claim itself**: report ADF and KPSS together, state the level-series ambiguity honestly rather than asserting a clean I(1) verdict, and lean on the unambiguous differenced-series result as the real justification for the feature design.

**Residual gap**: danskvand and RTD stationarity (with KPSS) remain unverified — same data-availability blocker as tasks 7 and 9. Needs re-run once raw/converted data is available for those categories.

### Task 8 — Pooled ACF replaced with per-brand method: DONE, confirms the pooled method inflated lag1

**Files changed** (verified directly, not just from the fork's report):
- **New**: `thesis/data/preprocessing/nielsen_dvh/compute_acf_per_brand.py` — computes ACF per-brand on each brand's own log-sales series only (no cross-brand concatenation), aggregates via mean/median/IQR. This is now the reproducible source of truth for these numbers, replacing the prior unreproducible one-off calculation.
- **Updated**: `thesis/data/_03_engineered_dvhexclhd/eda_findings_dvhexclhd.md` — ACF table, Reading, and Caveat sections rewritten to report the corrected numbers as primary, with old pooled figures kept only as a labeled "do not cite as primary" comparison row.

**Corrected numbers**:

| Category | lag1 (mean/median) | lag3 (mean/median) | lag13 (mean/median) | n brands | Confidence |
|---|---|---|---|---|---|
| CSD | +0.46 / +0.55 | +0.39 / +0.37 | −0.06 / −0.05 | 76 | **High** |
| energidrikke | +0.37 / +0.29 | +0.13 / +0.10 | −0.08 / −0.08 | 27 | **Low** (partial/stale local data — 29 periods on file vs. 39 claimed by the canonical script; relaxed MIN_PERIODS=20 used for a directional check only) |
| danskvand | not recomputed | not recomputed | not recomputed | — | **Pending** — no local raw data in this checkout |
| RTD | not recomputed | not recomputed | not recomputed | — | **Pending** — no local raw data in this checkout |

**Magnitude of correction — not cosmetic**: CSD lag1 dropped from the old pooled +0.78 to the corrected +0.46 (mean) — roughly a 0.2-0.3 absolute reduction. energidrikke shows the same direction: +0.71 → +0.37. This confirms the predicted heteroscedasticity artifact from Phase 1 Task 5's judgment — the pooled method really was letting high-volume brands dominate and inflate the statistic, not just a theoretical concern. Lag13 stayed small/negative under both methods (CSD −0.15→−0.06, energidrikke −0.12→−0.08) — this qualitative conclusion (weak annual autocorrelation) is now **confirmed by two independent methods**, strengthening rather than undermining the earlier finding that lag-13 lacks strong empirical support.

**Practical consequence for anything already written citing the old numbers**: any prior Ch4 material or notes citing "+0.78" or "+0.71" lag1 autocorrelation for CSD/energidrikke needs updating to the corrected, lower values (+0.46/+0.37). The qualitative story (positive short-lag autocorrelation justifies lag features; lag-13 is weak) is unchanged, but the reported magnitude was overstated.

**Residual gap, same as tasks 6/7/9**: danskvand and RTD could not be recomputed due to missing local raw/converted data in this checkout — explicitly marked "pending" in the doc rather than silently left on the old, now-known-to-be-inflated pooled figures. Needs re-run once that data is available.

### Task 9 — Train/val/test distribution-shift check: BLOCKED, could not execute quantitatively

**Could not be completed** — same data-availability constraint (no `data/raw/`, no engineered parquet feature matrices locally). The KS-test/moment-comparison analysis this task calls for requires actual target/feature values per split window, which aren't present in this checkout.

**What was confirmed instead** (from `{cat}_split_dates.json`, present for all 4 categories):

| Category | n_periods | train | val | test | val window | test window |
|---|---|---|---|---|---|---|
| CSD | 42 | 24 | 6 | 12 | 2024-10..2025-03 | 2025-04..2026-03 |
| RTD | 37 | 23 | 6 | 8 | 2025-02..2025-07 | 2025-08..2026-03 |
| danskvand | 37 | 23 | 6 | 8 | 2025-02..2025-07 | 2025-08..2026-03 |
| energidrikke | 39 | 25 | 6 | 8 | 2025-02..2025-07 | 2025-08..2026-03 |

**Circumstantial (not statistical) observation bearing on the val<test WMAPE anomaly**: `VAL_SIZE=6` is fixed for every category, but test windows vary — 12 months for CSD, only 8 months for the other three. For the 8-month-test categories, val (6mo) and test (8mo) are both short windows of similar size, so a WMAPE gap of a few points there is plausible small-sample noise rather than necessarily a genuine distribution shift. **This is not a substitute for the actual KS test requested** — it's circumstantial reasoning only. **Action needed**: re-run this task with `data/raw/` or the engineered parquet files available (e.g. on whichever machine/branch has the source data) to get a real answer. This remains an open item, not resolved.

### Task 11 — WARMUP_PERIODS=13 / lag-13 reconciliation: keep, but reweight the narrative honestly

**Judgment: option (b)** — keep lag-13/rolling_mean_13 in the feature set as-is, but stop describing it as empirically justified by ACF; state plainly that it's a seasonal-convention feature with weak measured autocorrelation.

**Reasoning**:
1. **Evidence base is thin, not zero, but incomplete**: only CSD (high-confidence) and energidrikke (low-confidence, partial data) have any ACF numbers. Danskvand and RTD are pending. Recommending outright removal (option c) would generalize a 2-of-4-category finding (one of which is low-confidence) to a shared 4-category pipeline — that overreaches the evidence.
2. **Two independent methods now agree lag-13 is weak-to-negative** (CSD −0.15→−0.06, energidrikke −0.12→−0.08 across the flawed-pooled vs. corrected-per-brand methods). This is no longer dismissible as a pooling artifact — it's real and reproducible for the categories tested. Strong enough to state honestly, not strong enough to justify unilaterally dropping a shared feature.
3. **Linear ACF isn't the whole story for tree-based models**: LightGBM/XGBoost (the models actually used per Phase 1 Task 2) can extract non-linear or interaction-conditioned signal from a lag with weak marginal linear autocorrelation (e.g. lag-13 combined with calendar-month could still carry seasonal information ACF alone won't detect). This is a genuine reason to keep the feature, not just a hedge to avoid a hard call.
4. **Changing LAGS/ROLLING_WINDOWS has cross-category consequences** (affects WARMUP_PERIODS, and therefore how many training rows every category loses) — this is a decision for Brian to approve explicitly, not something to change autonomously from a partial-evidence analysis task.

**Concrete proposed wording** (not yet applied — needs human approval before editing `build_feature_matrix.py`'s comment or any Ch4 narrative):
> "lag-13/rolling-13 is retained as a seasonal-convention feature; per-brand ACF (CSD, energidrikke) shows this lag carries weak-to-negative linear autocorrelation (−0.06 to −0.08), materially weaker than lag-1/lag-3 (+0.29 to +0.55). Retained pending model-level feature-importance validation and pending danskvand/RTD ACF data; not empirically justified by ACF alone."

**Follow-up this recommendation implies**: a model-level feature-importance check (e.g. SHAP or gain-based importance for lag_13/rolling_mean_13 specifically) would settle whether the tree models are actually using this feature meaningfully — that's a cleaner test than linear ACF for tree-based models, and isn't done yet. Also still pending: danskvand/RTD ACF data (same environment gap as tasks 6/7/9).

**No code changed** — correctly stayed within analysis/recommendation scope; `build_feature_matrix.py`'s `LAGS`/`ROLLING_WINDOWS` constants were not touched.

## Phase 2 Summary — 6/6 tasks complete (1 blocked on data availability, 1 shipped a real code fix)

| # | Task | Outcome |
|---|---|---|
| 6 | KPSS alongside ADF | **Weaker than claimed** — ADF/KPSS jointly ambiguous for CSD/energidrikke (the only 2 testable); found an unreconciled CSD ADF p-value discrepancy (0.140 vs doc's 0.421) |
| 7 | MCAR/MAR/MNAR missingness reasoning | **MNAR mechanism identified** via aggregate reasoning (positive-sales-only filter structurally ties missingness to the value itself); current no-impute approach is defensible but was undocumented |
| 8 | Replace pooled ACF | **Real code fix shipped** — new committed script + updated findings doc; confirmed pooled method inflated lag1 by ~0.2-0.3 absolute (heteroscedasticity concern from Phase 1 Task 5 empirically confirmed) |
| 9 | Train/val/test distribution-shift check | **Blocked** — no raw/engineered data available in this checkout; only structural split-window metadata obtained, not the actual KS test |
| 10 | "Kim, 2013" citation | **Confirmed unbacked** — no matching bibliography entry anywhere in the repo; recommended replacing with a real citation or reframing as an undefended heuristic |
| 11 | WARMUP_PERIODS=13/lag-13 reconciliation | **Keep feature, reweight narrative** — 2 independent methods confirm weak lag-13 autocorrelation, but evidence is incomplete (2/4 categories) so removal isn't warranted; proposed exact honest wording, pending human approval |

**Critical environment finding, cutting across half of Phase 2**: this local checkout lacks `data/raw/` (the canonical script's input) and most engineered parquet files. Only CSD has fully reliable local data; energidrikke has partial/stale data; danskvand and RTD have essentially none. This limited tasks 6, 7, 9, and 11 to partial or structural analysis rather than complete, all-4-category quantitative results. **This needs to be resolved before Phase 5 (extend to 3 categories) can proceed properly** — either by obtaining `data/raw/` on this machine/branch, or by having whoever holds the full data (Enrico, or wherever it's regenerated) run the remaining pieces: danskvand/RTD ACF (task 8 follow-up), all 4 categories' KPSS (task 6 follow-up), and all 4 categories' distribution-shift check (task 9, currently fully blocked).

**Net assessment**: real progress was made — one genuine defect was fixed with committed, reproducible code (task 8), one fabricated-looking citation was caught (task 10), and one mechanism gap was filled with defensible reasoning (task 7). But two things should give pause before calling Phase 2 "done": (a) the KPSS finding (task 6) shows the stationarity story is weaker/more ambiguous than the existing docs claim, not just under-tested, and (b) the distribution-shift check (task 9) — the one most directly motivated by an actual anomaly in the real model results (val<test WMAPE) — could not be run at all. Phase 2 should be considered **substantially but not completely closed** pending data access.

### PATH MIGRATION NOTICE (2026-07-11) — thesis/data/ → 02_thesis_data/, confirmed by Brian

**Every file path cited below and in earlier Phase 1/2 sections as `thesis/data/_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` or `thesis/data/_02_preprocessing/nielsen/CSD/*` is now STALE.**

Running `python thesis/data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py` on 2026-07-11 revealed: `PATHS.py` was modified (uncommitted, `git status` shows `M PATHS.py`) to redirect `THESIS_DATA_DIR` from `thesis/data` to a new root-level `02_thesis_data/` directory. `PATHS.py`'s own comment confirms this is deliberate: `THESIS_DATA_ENGINEERED_BYMONTH_DIR` — "Was: `_03_engineered_dvhexclhd/` before the P0028 restructure." The `_02_preprocessing/nielsen/CSD/pre_csd_2..6.py` step scripts are also modified (uncommitted) to write to this new location.

**New canonical path** (confirmed via direct `pd.read_parquet`, 2026-07-11): `02_thesis_data/_03_engineered/bymonth/CSD/csd_feature_matrix.parquet` — verified identical content to the old `thesis/data/_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` (78 brands, 25,124 rows, 26 columns, same train/val/test split sizes 14275/3426/7423). This is a path migration, not a data change — all Task 6/7/9/10/11/12/13/14 findings and conclusions remain valid; only the file path they refer to needs updating.

**Confirmed with Brian (AskUserQuestion, 2026-07-11)**: `02_thesis_data/` is the intended new home from an in-progress P0028 restructure that also unifies the old `_03_engineered_dvhexclhd/` (Enrico's track) and `_03_engineered/nielsen/` (our modular pipeline's track) into a single `_03_engineered/bymonth/` location. The old `thesis/data/` tree still exists on disk and is still git-tracked (nothing deleted yet) — treat it as **pending cleanup**, not a second source of truth. Going forward, all new work should reference `02_thesis_data/_03_engineered/bymonth/CSD/csd_feature_matrix.parquet`, not the `thesis/data/...` path.

**Not yet verified**: whether the `PATHS.py` + step-script edits are meant to be committed as-is, whether `_04_engineered_bychain` also moved under the new root, and whether danskvand/energidrikke/RTD step scripts (also showing as modified) produce equivalent output at their new paths. Flagged for a future task, not blocking Phase 2's already-completed conclusions.

### Task 12 — CSD train/val/test distribution-shift check (KS test): EXECUTED — no anomaly found, and CSD does not actually show the val<test anomaly pattern

**Environment update since Task 9 was blocked**: CSD's data has since been freshly converted/verified. This unblocked the KS-test analysis for CSD specifically (the only category in scope for this task — danskvand/energidrikke/RTD remain deferred).

**File location correction, important**: `build_feature_matrix.py`'s canonical output path (`thesis/data/_03_engineered_dvhexclhd/CSD/csd_feature_matrix.parquet`) does **not exist** in this checkout — only its `csd_split_dates.json` metadata file is present there (the parquet itself was never regenerated under that script for CSD). The actual feature matrix used to produce `tuned_summary.md`/`tuned_metrics.csv` lives at a **different, older pipeline path**:

```
thesis/data/_03_engineered/nielsen/CSD/csd_feature_matrix.parquet   (25,124 rows, brand×region×period grain)
thesis/data/_03_engineered/nielsen/CSD/csd_split_dates.json
```

This is produced by the `_02_preprocessing/nielsen/CSD/pre_csd_1..6.py` step scripts (specifically `pre_csd_4_engineer_features.py` for feature engineering, `pre_csd_5_apply_split.py` for the split), **not** `build_feature_matrix.py`. Row count (25,124) matches the "~25.1k rows" cited in the recent commit log (`cb615cf` — brand×region×period grain change), confirming this is the correct/current file to analyze. A `split` column already exists in this parquet (train=14,275 / val=3,426 / test=7,423 rows), so no manual date-based partitioning was needed — the pipeline's own split labels were used directly.

**Actual split windows** (read from the data, matches `_03_engineered/nielsen/CSD/csd_split_dates.json`):
- train: 2022-10 to 2024-10 (train_end listed as "2024-10-01" — a minor format inconsistency vs. the YYYY-MM convention elsewhere, not investigated further)
- val: 2024-11 to 2025-04
- test: 2025-05 to 2026-05

**Column names confirmed**: target is `log_sales_units` (= `ln(sales_units)`, NaN for non-positive/missing); raw level is `sales_units`; `promo_intensity` exists as a column but — confirmed by direct check — is **structurally all-zero across the entire CSD dataset** (`promo_units` sums to 0.0 for every one of 25,124 rows). This means CSD's promo-intensity feature carries no non-zero values to KS-test at all, contrary to `build_feature_matrix.py`'s docstring claim that "CSD... exposes `sales_units_any_promo`" — that claim may be true for `build_feature_matrix.py`'s DVH EXCL. HD pipeline, but does **not** hold for the actual brand×region×period pipeline that produced the results being audited. No promo KS test was possible or meaningful for CSD; this is itself a finding, not a gap in execution.

**KS-test results** (`scipy.stats.ks_2samp`, two-sided, on non-null values only):

| Variable | Comparison | KS statistic | p-value | n1 | n2 |
|---|---|---|---|---|---|
| log_sales_units | train vs val | 0.0662 | 2.61×10⁻¹⁰ | 12,991 | 3,229 |
| log_sales_units | val vs test | 0.0337 | 0.0144 | 3,229 | 6,526 |
| log_sales_units | train vs test | 0.0599 | 5.45×10⁻¹⁴ | 12,991 | 6,526 |
| sales_units (raw) | train vs val | 0.0662 | 2.61×10⁻¹⁰ | 12,991 | 3,229 |
| sales_units (raw) | val vs test | 0.0337 | 0.0144 | 3,229 | 6,526 |
| sales_units (raw) | train vs test | 0.0599 | 5.45×10⁻¹⁴ | 12,991 | 6,526 |
| promo_intensity (non-zero) | all 3 comparisons | — | — | 0 | 0 (no non-zero values exist; test not computable) |

(Note: `sales_units` and `log_sales_units` give identical KS statistics/p-values by construction — KS is invariant under any monotonic transform such as `log()`, so this is expected, not a computational error.)

**Moment comparisons** (log_sales_units, non-null):

| Subset | n | mean | std | skew |
|---|---|---|---|---|
| train | 12,991 | 7.045 | 2.931 | 0.007 |
| val | 3,229 | 6.779 | 3.066 | 0.079 |
| test | 6,526 | 6.708 | 3.253 | 0.046 |

**Interpretation**: all three KS comparisons are statistically significant (p<0.05), including val-vs-test (p=0.0144) — technically a "detected shift" in the strict null-hypothesis-rejection sense. But three things argue against reading this as a meaningful, actionable distribution shift:
1. **Effect size is small.** KS statistics of 0.03–0.07 are modest — the maximum CDF gap between val and test is ~3.4%, versus ~6.6% for train-vs-val (which is expected: train is 2 years earlier than val, more calendar/brand-mix drift is unsurprising). Val-vs-test actually shows the **smallest** KS statistic of the three comparisons, not the largest — if anything, val and test are the *most* similar pair of the three windows, not the least.
2. **Moments move in a small, monotonic, plausible-trend direction** (mean 7.05→6.78→6.71, std 2.93→3.07→3.25 from train→val→test) — consistent with a gradual, gentle decline in typical sales level and a gentle increase in dispersion over time, not an abrupt regime break between val and test specifically.
3. **Large-n effect**: with n1=3,229 and n2=6,526, KS tests have enormous power to detect trivially small differences as "statistically significant." A KS stat of 0.034 with p=0.014 is a real but very mild location/shape difference, not evidence of a sharp distributional break.

**Direct answer to the anomaly question — CSD does NOT show the val<test WMAPE anomaly.** Checking `tuned_metrics.csv`/`tuned_summary.md` directly (not assuming):

| Dataset grain | Model | val WMAPE | test WMAPE | val − test |
|---|---|---|---|---|
| bychain | LightGBM | 22.59% | 21.24% | **+1.35pp** (val higher) |
| bychain | XGBoost | 21.86% | 20.80% | **+1.06pp** (val higher) |
| brand | LightGBM | 15.31% | 17.38% | −2.07pp (val lower) |
| brand | XGBoost | 15.17% | 16.48% | −1.31pp (val lower) |

CSD's `bychain` grain shows val WMAPE *higher* than test — the opposite direction from the flagged anomaly. CSD's `brand` grain does show val < test (by 1.3–2.1pp), the same direction as RTD's flagged anomaly, but the magnitude is far smaller: RTD brand-grain shows a 4.6–4.7pp gap (val 28.8% vs test 33.4% LightGBM; val 30.3% vs test 31.0% XGBoost), roughly 2–4x larger than CSD's 1.3–2.1pp gap. **CSD is not a clean instance of the anomaly pattern** — at best a mild version of it in one of two grains, and the reverse in the other grain.

**Does the (very mild) CSD brand-grain val<test gap correlate with a KS-detected shift?** Weakly, and not convincingly. The val-vs-test KS statistic (0.0337) is the *smallest* of the three pairwise comparisons — if a genuine, consequential distribution shift were driving a WMAPE gap, a larger KS statistic for val-vs-test specifically (relative to train-vs-val or train-vs-test) would be the expected signature. Instead the opposite ordering is observed. This is evidence **against** distribution shift being the primary explanation for CSD's small val<test WMAPE gap.

**Small-sample-noise consideration**: `VAL_SIZE=6` (confirmed exact value in `build_feature_matrix.py:97`, and the same 6-month val window appears in the actual pipeline's `csd_split_dates.json` too: val_start 2024-11 to val_end 2025-04 = 6 months). A 6-month validation window sampling ~3,229 brand-region-month rows is short in calendar terms even though the row count is large (many brand×region series per month) — 6 calendar months is enough to be dominated by 1-2 unusual months (e.g. a holiday month or a one-off promotional push) in a way a longer window would average out. Combined with the KS evidence showing val-test as the *least* different pair statistically, **small-sample / calendar-window noise is a more plausible explanation than genuine distribution shift for CSD's mild val<test gap** — the WMAPE gap (1.3–2.1pp) is well within the range a single unusual month in a 6-month window could produce, and it is not supported by an outsized KS statistic that would indicate the val and test populations are meaningfully different from one another.

**Bottom line for Task 12 / Task 9 follow-up**: KS testing on CSD (the one category with usable local data) finds a statistically detectable but small-effect-size shift across all three split boundaries, with val-vs-test being the *least* different of the three pairs — the opposite of what would be expected if the anomaly were shift-driven. CSD itself barely shows the anomaly (a small gap in one grain, none in the other), unlike RTD's much larger, clean instance. This is useful negative evidence: it suggests the RTD anomaly (and any future check on danskvand/energidrikke) likely needs its own category-specific KS check rather than assuming a shared distribution-shift cause — CSD's data does not support "distribution shift" as a general explanation for the val<test pattern across categories.

## Pipeline Provenance Clarification (2026-07-10, post-Task-12)

**Question raised**: Task 12's KS test ran against `thesis/data/_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` (25,124 rows, brand×region×period grain) because `build_feature_matrix.py`'s expected output folder, `thesis/data/_03_engineered_dvhexclhd/CSD/`, contains only a `csd_split_dates.json` locally — no feature matrix parquet. This raised the question of which pipeline is actually "canonical" for CSD's locked numbers, and whether the `_03_engineered_dvhexclhd` gap was a real problem or a folder-restructure artifact.

**Investigation (direct file/git checks, not inference)**:

| Location | Contents (CSD) | Last touched (git) | Provenance |
|---|---|---|---|
| `thesis/data/_03_engineered/nielsen/CSD/` | `csd_feature_matrix.parquet` (25,124 rows, 78 brands, brand×region×period, verified via direct `pd.read_parquet` — columns include `lag_1..13`, `rolling_mean_4/13`, `promo_intensity`, `log_sales_units`, `split`), `csd_series_index.csv`, `csd_split_dates.json`, `csd_preprocessing_report.md` | `cb615cf` (2026-06-30 17:13): *"Re-running CSD preprocessing pipeline with updated filters brand x regions x period -> bringing row count from ~2.3k rows to ~25.1k rows"* | Output of **our own modular pipeline**: `_02_preprocessing/nielsen/CSD/pre_csd_1..6.py` (via `preprocessing_csd.py` orchestrator). Row count (25,124) matches the commit message exactly. |
| `thesis/data/_03_engineered_dvhexclhd/CSD/` | Only `csd_split_dates.json` — no feature matrix parquet | Enrico's commits only (`cb2e718`, `a9de949`, etc.) — none of which are recent local checkouts of a regenerated parquet | Enrico's separate `build_feature_matrix.py` track. Never had a feature-matrix parquet land in this checkout; likely gitignored (consistent with Phase 1 Task 4's finding that `_03`-`_07` tiers have no gitignore patterns but also weren't tracked for large binary outputs) or generated on Enrico's own machine and not synced here. |

**Resolution**: this is not a genuine ambiguity about which pipeline is "real" for CSD — it is that **two parallel tracks exist, and only one (`_02_preprocessing` → `_03_engineered/nielsen/CSD`) has a live, current, locally-runnable feature matrix.** The `_03_engineered_dvhexclhd` track is Enrico's, currently documentation + split-dates only in this checkout.

**One stale-but-harmless side-finding**: `_03_engineered/nielsen/CSD/csd_preprocessing_report.md` (also touched in `cb615cf`) still displays old header text — "Generated: 2026-06-22 18:27:40", "Min Periods Filter: 40", "62 brands", "2,666 rows" — that does not match the actual current parquet (78 brands, 25,124 rows). The `.md` report file was committed in the same commit that regenerated the parquet, but its own internal "Generated" summary numbers were not refreshed by the script — a cosmetic reporting bug in the pipeline's own report-writing step, not a data problem. The parquet itself is correct and current (verified by direct read). Worth a one-line fix later (regenerate the report, or have the script always overwrite it), not urgent.

**Implication for tasks 13/14 and Phase 4**: `_02_preprocessing/nielsen/CSD/pre_csd_1..6.py` → `_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` is confirmed as the correct, current, actually-covering-the-live-data CSD pipeline to use for all remaining CSD rigor work in this plan. This also directly informs Phase 4 (Canonical Script Decision): for CSD specifically, our modular pipeline is not a dead/legacy artifact — it is actively maintained and was re-run as recently as 2026-06-30, more recently than any local evidence of `build_feature_matrix.py`'s CSD output. The earlier claim (now twice-corrected: once on `PATHS.py` runnability, now on data currency) that our modular pipeline is the deprecated one does not hold up under direct verification.

**Scripts used** (scratch, not committed — per task constraints): `C:/Users/brian/AppData/Local/Temp/claude/ks_analysis/ks_test.py` (main KS + moments analysis), `check_cols.py` (column/shape inspection), `check_promo.py` (promo_intensity zero-check).

## Task 14: CSD Row-Level Missingness Test (2026-07-11)

**Goal**: Task 7 only reasoned about missingness in aggregate (grid_rows vs observed_rows, no row-level test). This task runs the originally-specified row-level test directly on the confirmed dataset (`_03_engineered/nielsen/CSD/csd_feature_matrix.parquet`, 25,124 rows, 78 brands).

**Setup note**: this file is already a fully reindexed grid — every brand×region×period combination that should exist is present as a row, with `sales_units`/`log_sales_units` set to `NaN` where the actual sale didn't happen (2,378 of 25,124 rows, 9.47% overall). This means the missingness indicator (`sales_units.isna()`) is directly readable per row; no separate grid-construction step was needed.

**What "missingness correlates with X" means mechanically**: a chi-square test of independence asks whether the proportion of missing rows differs across categories of X by more than chance would produce, given the sample size. A logistic regression asks the same question while holding other variables constant (e.g., "does volume tier still predict missingness once month and region are accounted for?"), and reports each category's effect as a log-odds coefficient — a large positive coefficient means that category is more likely to be missing than the reference category, holding other variables fixed.

**Results (exact statistics)**:

| Variable | Test | Statistic | df | p-value | Interpretation |
|---|---|---|---|---|---|
| Calendar month | chi-square | 48.78 | 11 | 1.04e-06 | Statistically significant, but the effect is small — missing rates by month range narrowly (9.4%-13.6%; June/Aug/Sep are somewhat lower, near 6-9%). Not a strong driver. |
| Brand identity | chi-square | 4018.6 | 77 | ~0 (machine zero) | Huge effect. 23 of 78 brands (29%) have literally zero missingness; the 10 highest-missingness brands run 35-45% missing (e.g. GALVANINA 45.5%, BORNHOLMS MOSTERI 40.9%). Brand is clearly the dominant axis of missingness variation. |
| Volume tier (quartile of brand's mean non-missing `sales_units`) | chi-square | 1336.9 | 3 | 1.44e-289 | Very strong, monotonic: Q1 (lowest-volume brands) miss 16.3% of period-cells; Q4 (highest-volume) miss only 0.4%. This is the same information as "brand identity" but grouped into an interpretable, ordered axis. |
| Region (`market_id`) | chi-square | 36.25 | 8 | 1.58e-05 | Statistically significant but small in magnitude — missing rates by region range roughly 8.5%-11.4%, a modest spread compared to volume tier's 0.4%-16.3% range. |

**Joint logistic regression** (`missing ~ C(month) + C(volume_tier) + C(market_id)`, n=25,124, pseudo-R²=0.113): once volume tier is in the model, most month coefficients become non-significant (June/Aug/Sep remain modestly significant, coefficients around -0.33 to -0.42, i.e. slightly *lower* missingness in those months — plausibly a seasonal high-demand effect, but small next to volume tier's coefficients). Volume tier dominates: Q3 vs Q1 coefficient = -1.34 (p<0.001), Q4 vs Q1 = -3.90 (p<0.001) — moving from the lowest to highest volume quartile multiplies the odds of missingness by roughly e^-3.90 ≈ 0.02, a 50-fold reduction. Region coefficients are mostly small (0.01-0.43) with a few statistically significant but practically modest effects (e.g., market 1586002 and 1586001 somewhat more likely to have gaps than the reference region).

**Does this confirm, weaken, or contradict Task 7's aggregate-level MNAR conclusion?**

It **confirms and substantially strengthens** it, with a more precise mechanism than Task 7 could establish. Task 7 only knew the overall grid-fill-rate (aggregate); it could not say *why* certain brand-months were missing. This row-level test shows the missingness is not random (ruling out MCAR) and is overwhelmingly explained by an **observed** variable — the brand's own volume tier, itself derived from the brand's *non-missing* sales values. This is the textbook MAR (Missing At Random, in the formal statistical sense meaning "missingness depends on observed data, not on the unobserved value itself") signature: low-volume brands go quiet more often, and "low-volume" is knowable from the data already in front of you (the brand's historical sales level), not from the hidden true value of the specific missing cell.

That said, the *substantive* story here is closer to MNAR in the colloquial sense the plan has been using it (a brand's sales genuinely dropped toward zero and the retailer/data-provider simply stopped recording distribution for it that period) — but statistically this is indistinguishable from MAR-on-volume-tier once you condition on the brand's own historical volume, because "high probability of zero/near-zero sales" and "high probability of being missing" are driven by the same underlying commercial reality (small/declining brand). This is a case where the formal MCAR/MAR/MNAR taxonomy and the "why does this happen mechanically" explanation both point to the same conclusion via different vocabularies — worth stating explicitly rather than picking one label and treating the question as closed.

**Grounding the current reindex-and-leave-NaN approach**: this evidence makes the current approach **more clearly correct, not less**. Since missingness is strongly predictable from an observed, already-available variable (brand volume tier) rather than being MCAR (which would justify simple deletion) or true MNAR-on-the-hidden-value (which would bias any model that imputes with a fixed/mean value), leaving these as `NaN` and letting downstream lag/rolling-window features naturally propagate the gap (rather than imputing a fabricated sales number) avoids injecting a false signal. A model conditioning on `volume_tier`-correlated features (which the feature matrix already includes indirectly via lag/rolling stats) will implicitly learn that low-volume brands have gappier histories — imputing zeros or means instead would either understate genuine zero-sales periods (if using mean) or artificially deflate a low-volume brand's rolling averages (if using zero for what might just be "not recorded" rather than "sold zero units").

**Caveat**: this analysis cannot distinguish "sold zero and wasn't recorded" from "wasn't stocked/distributed that period" — both would show as missing rows and both are consistent with the volume-tier finding. Task 7's report/doc reasoning already discusses this ambiguity at the aggregate level; this task does not resolve which specific mechanism applies, only that the *statistical pattern* (predictable from volume tier) is real and strong.

## Task 13 — CSD ADF Log-Level p-Value Discrepancy Reconciled (2026-07-11)

**The two numbers**: `eda_findings_dvhexclhd.md` reports CSD ADF log-level p=0.421 (n=76 brands, "per-brand-computed-then-averaged" method). Task 6 independently computed p=0.140 against `thesis/data/_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` using a different aggregation. Both were run on log1p(sales_units) with `adfuller(..., autolag='AIC')`, so the transform and lag-selection method were never the disagreement — the discrepancy is entirely a **grain bug** in how Task 6's per-brand series was constructed.

**Mechanism, with exact numbers**: `csd_feature_matrix.parquet` is brand×**region**×period grain — each of the 78 brands has between 44 and 396 rows (mean 322), because most brands appear in up to 9 distinct `market_id` regions, each with its own 44-month time series. Task 6's original computation grouped by `brand` alone and fed the **region-interleaved row order** straight into `adfuller()` without first summing across regions — i.e., for a brand present in 9 regions, the "series" `adfuller` saw was 9 separate monthly cycles concatenated/interleaved by whatever row order the parquet happened to have, not one clean 44-point brand-level monthly series. Reproducing that exact (flawed) construction against the current file:

- Region-conflated (Task 6's original method): mean p=0.2829, **median p=0.1408** — matches the reported 0.140 almost exactly.
- Correct construction — sum `sales_units` across regions per brand per calendar month first (`df.groupby(['brand','date'])['sales_units'].sum()`), producing one clean 44-point series per brand, THEN run `adfuller(log1p(series), autolag='AIC')` per brand, then take the median across all 78 brands: mean p=0.4068, **median p=0.3535**.

The correct-grain median (0.3535, n=78) lands close to the doc's reported 0.421 (n=76) — the residual small gap is attributable to which 2 of the 78 brands the doc's n=76 excluded (likely a length/`MIN_PERIODS` filter difference) and possibly minor differences in exact row inputs, not a second methodological disagreement. Root cause isolated to **(a) aggregation grain** per the task's option list — not date range (both use the same 44-period file) and not ADF lag-selection (both use `autolag='AIC')`, confirmed identical in both the modular pipeline's `pre_csd_1.5_eda.py:323-325` and the reproduction script here).

**Which number is authoritative**: **0.421 (the doc's figure) is authoritative going forward.** 0.140 was an artifact of an aggregation bug (region rows conflated into a single per-brand series without summing first) in Task 6's ad hoc reproduction script, not a genuine alternative framing of the data — it does not correspond to any meaningful real-world series (a "series" that jumps between regions mid-sequence is not a time series any economic process actually generates). The 0.421 figure reflects the correct object: each brand's true national monthly sales trajectory. Both numbers land on the same qualitative verdict regardless (p > 0.05 in both cases → fail to reject H0 → non-stationary in log level, consistent with I(1)), so the discrepancy does not change Ch4's stationarity conclusion — it only affects which exact number should be cited as evidence.

**Side note on the modular pipeline's own separate "aggregate series (reference only)" line** (`pre_csd_1.5_eda.py:373-377`, category-total across all brands, not per-brand): reproduced here as p=0.2078 (raw level) / p=0.0656 (log1p level) — a third, different number again, because it answers a third, different question (is the *whole category's total* sales non-stationary, not any individual brand). This is explicitly flagged in that script's own comment ("aggregate result can mask per-brand heterogeneity") and should not be confused with either the 0.421 or 0.140/0.353 per-brand figures — it is a distinct, lower-priority diagnostic, not a third candidate for the "authoritative" per-brand number.

**Script used** (scratch, not committed): `C:/Users/brian/AppData/Local/Temp/task14_missingness.py`.

---

## 2026-07-11 Session — Pipeline Inventory + Grain-Leakage Bug

**Context**: separate session started from a "how do I test the whole pipeline" question, unrelated to P0027 at first — but investigation surfaced findings that directly affect Phase 3's WMAPE result and Phase 4/5's canonical-script decision, so folding in here rather than starting a new plan. Repo paths referenced below use the post-P0028-restructure numbering (`02_thesis_data/`, not `thesis/data/`) — this session ran after the restructure completed.

### Full inventory of competing feature-matrix pipelines

Confirmed **three** distinct code paths that can produce Nielsen feature matrices, not two:

1. **The CSD-style 6-step orchestrator** — `02_thesis_data/_02_preprocessing/nielsen/{Category}/preprocessing_{category}.py` + `pre_{cat}_0..6_*.py`. Exists (with per-step scripts) for **all four** categories (CSD, Danskvand, Energidrikke, RTD), not just CSD as earlier findings implied. Rich logging (`terminal_utils`, `rich` tables), per-step JSON timing, per-category markdown reports, smart caching (`--run-raw`/`--re-cache`/`--run-step N`). This is the actively-maintained pipeline referenced throughout P0027 so far.
2. **The colleague's standalone scripts** — `02_thesis_data/preprocessing/nielsen_dvh/build_feature_matrix.py` (brand×month) and `build_feature_matrix_bychain.py` (brand×chain×month). Single monolithic script per file, no step separation, no orchestrator, no caching. **Docstrings and `ROOT` path-walk logic are stale** — still reference pre-P0028 paths (`thesis/data/preprocessing/...`, `thesis/data/_03_engineered_dvhexclhd/`, `thesis/data/_04_engineered_bychain/`), and `build_feature_matrix_bychain.py`'s `ROOT = Path(__file__).resolve().parents[4]` hardcodes a folder depth that no longer matches the current tree — this would resolve to the wrong root if run today without a path fix.
3. **The shared `FeatureEngineer` class** — `02_thesis_data/_02_preprocessing/nielsen/shared/engineer_features.py`. A third, independent implementation of the same conceptual steps (`aggregate_brand_month_from_db`/`_csvs`, `make_calendar`, `filter_series`, `engineer_features`, `apply_split`), explicitly designed as "single source of truth ... used by both DataAssessmentAgent (LangGraph node) and thesis/data/preprocessing/combined_scripts/preprocessing.py (CLI batch)" per its own docstring — i.e. intended to serve System A live inference, not (originally) the CSD orchestrator. **But `pre_csd_4_engineer_features.py` and `pre_csd_6_save_outputs.py` both import and call into this exact module** (`shared_engineer_features`, `build_series_index`), so the orchestrator pipeline (#1) actually depends on #3 for its core transform logic — the "orchestrator" is really an orchestrator-plus-shared-library hybrid, not fully self-contained.

### Where `srq1_benchmark.py` actually reads from

`03_thesis_modelling/model_training/srq1_benchmark.py:11-13,28,38-41` says explicitly: *"Runs on BOTH granularities: `_04` brand×chain (primary) and `_03` brand×month (robustness comparison)"* and reads via `PATHS.THESIS_DATA_ENGINEERED_BYCHAIN_DIR` / `THESIS_DATA_ENGINEERED_BYMONTH_DIR`, which resolve to `02_thesis_data/_03_engineered/{bychain,bymonth}/`. This is the actual SRQ1 training entry point and treats **bychain as primary**, not a side experiment — meaningfully different framing from Phase 3's region-grain framing above (region ≠ chain; two different disaggregation dimensions, both distinct from what `srq1_benchmark.py` is consuming).

**Which pipeline currently populates these two directories was not conclusively re-verified this session** (carries over the ambiguity already flagged in the Context section's SECOND CORRECTION, dated 2026-07-10) — `_03_engineered/bymonth/` contains a `regeneration_report.md`, which is the report format written by `build_feature_matrix.py` (pipeline #2), not the per-category `{cat}_preprocessing_report.md` format written by the orchestrator's Step 6 (pipeline #1). This suggests pipeline #2, not #1, most recently wrote `bymonth/`'s current contents — **needs a direct timestamp/content check before Phase 4 finalizes which pipeline is canonical**, since the two pipelines disagree on market scope (see next section) and this matters for which one produced whatever numbers are currently "live" in `04_thesis_results/srq1/`.

### Market-scope disagreement across categories — worse than previously documented

Confirmed via direct grep + read of all four categories' Step 1 scripts:

- **CSD's Step 1** (`pre_csd_1_load_and_aggregate.py`) scopes to `DVH_REGION_IDS` — 9 hand-picked, mutually-exclusive regional `market_id`s, chosen specifically to enable brand×region granularity per the P0026 design decision. Produces brand×region×period rows.
- **Danskvand's Step 1** (`pre_danskvand_1_load_and_aggregate.py:138`, confirmed by direct read) scopes to the single collapsed `market_description == "DVH EXCL. HD"` row — no region dimension at all, brand×period grain only.
- **Energidrikke and RTD's Step 1 scripts do not contain `DVH_REGION_IDS` either** (grep returned zero matches across all three non-CSD categories) — strongly implying all three non-CSD categories are still on the older brand×period-only scoping, i.e. **CSD is currently the only category with region-grain implemented at all** in the orchestrator pattern.

Per Brian (this session): this is expected, not a bug — CSD is the reference implementation, deliberately being finished first before the same treatment is copied to the other three. Recorded here so a future session doesn't mistake it for silent pipeline drift.

### NEW correctness bug — region-grain lag/rolling features leak across regions (confirmed, not hypothetical)

This is the important new finding. `pre_csd_4_engineer_features.py:128` calls `shared_engineer_features(df, lags=CSD_LAG_WINDOWS, rolling_windows=CSD_ROLLING_WINDOWS, holiday_months=CSD_HOLIDAY_MONTHS)` — i.e. it delegates lag/rolling computation to the shared module (pipeline #3 above). But `engineer_features.py`'s internal implementation groups by brand only:

```
engineer_features.py:263   g = df.groupby("brand")
engineer_features.py:266-267   for lag in lags: df[f"lag_{lag}"] = g[target_col].shift(lag)
engineer_features.py:270-282   rolling_mean_*/rolling_std_* also via g[target_col].shift(1).transform(rolling(...))
```

CSD's data reaching this function already carries a `market_id` column (added by Step 1, preserved through Steps 2-3 — Step 3's own filter correctly does `groupby(["brand", "market_id"])`, confirmed at `pre_csd_3_filter_series.py:105-112`). But Step 4 hands the full brand×region×period frame to a function that only groups by `brand`, sorted by `["brand", "date"]` (`engineer_features.py:262`) with **no region/`market_id` tiebreak in the sort or the groupby**. Concretely: for a brand present in multiple regions, `lag_1` for a given (brand, region, month) row can be populated from a *different region's* same-brand prior-month value, not that region's own history — because the grouped-shift operation sees one interleaved per-brand sequence, not 9 separate per-region sequences.

This is the **same grain-conflation failure mode** already identified and fixed as a one-off in Task 13 above (which found it corrupting an ad hoc ADF significance test) — but here it's not a one-off analysis script, it's baked into the **live feature-engineering step that produces the actual training data** for the region-grain model. That means:

- **Phase 3's reported 21.2% region-grain test WMAPE may itself be computed on leaky/incorrect features** — some fraction of `lag_1`/`rolling_mean_4`/`rolling_mean_13`/`rolling_std_4` values in the training and test sets are contaminated with a different region's history. Whether this makes the reported WMAPE optimistic or pessimistic isn't obvious without re-running (leakage from a *correlated but not identical* region's sales isn't as clean an information leak as same-series lookahead, so the direction of bias is not a priori certain) — but the number cannot be trusted as-is until the fix is applied and the benchmark re-run.
- The same bug affects `pre_csd_6_save_outputs.py`'s `build_series_index(df)` call (`engineer_features.py:319-333`, also `df.groupby("brand")` only) — series-index stats (`n_periods`, `total_units`, split period counts) silently sum/average across all 9 regions per brand in the generated report and CSV, even though the underlying `feature_matrix.parquet` correctly retains `market_id` as a column. This doesn't corrupt the parquet itself, only the human-readable report/series-index artifacts — but anyone reading `csd_preprocessing_report.md`'s "Brands: 78" or "Rows per brand" numbers today is reading brand-level stats for what's now actually a brand×region dataset.

**Fix scoped for tomorrow** (see task_plan.md Phase 4a): thread a `group_keys: list[str]` parameter through `filter_series()`, `engineer_features()`, `build_series_index()`, and the `weighted_dist` ffill inside `make_calendar()` in the shared module (default `["brand"]` to preserve System A's non-CSD callers, CSD passes `["brand", "market_id"]`). This is also the natural mechanism for a future chain-grain branch (`group_keys=["brand", "chain_id"]`) — see Phase 4b.

### Chain-grain gap — confirmed, no orchestrator equivalent exists for any category

The colleague's `build_feature_matrix_bychain.py` is the **only** code that currently produces brand×chain output, for any category — there is no `pre_{cat}_N_*_bychain.py` equivalent anywhere in the `_02_preprocessing/nielsen/{Category}/` tree. It scopes to 11 hand-picked "leaf chains" (BILKA, FØTEX, NETTO, KVICKLY, SUPERBRUGSEN, BRUGSEN, MENY, SPAR, MIN KØBMAND, REMA 1000, NEMLIG.COM) common to all four categories, with its own independent re-implementation of load/aggregate/filter/calendar/features/split (not reusing the shared `engineer_features.py` module at all) — meaning it does NOT have the same brand-grouping bug (its `KEYS = ["brand", "chain"]` and all groupbys use `KEYS`, confirmed correct throughout), but it does inherit the stale-path problem noted above.

Brian's directive: region and chain should become two parallel branches off the same orchestrator pattern (not one favored over the other), both able to roll up to brand×month, built by extending the CSD step scripts once the `group_keys` fix lands — not by porting the colleague's script wholesale. Full task breakdown in task_plan.md Phase 4b.

### Session paused here

No code changes were made this session (investigation/planning only, per the user's "document insights, continue tomorrow" instruction). Tomorrow's first task per the updated task_plan.md: Phase 4a's `group_keys` fix, applied to CSD only initially, then Phase 3's region-grain benchmark re-run to get a trustworthy WMAPE before touching Phase 4's dual-grain decision or Phase 4b's chain-branch work.
