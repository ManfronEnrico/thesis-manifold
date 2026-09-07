<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 4 — Data Assessment

> ⚠ **THE STATUS LINE BELOW IS STALE (flagged 2026-09-07, not rewritten).**
> It claims COMPLETE / all figures recomputed 2026-06-27 / no placeholders remain.
> Since then the pipeline was re-run (feature matrices regenerated 2026-09-07 15:59,
> now horizon-correct and carrying the holiday features), and the SRQ1 result tables
> are older still (2026-09-06 22:55) — so they are pre-fix. Treat every figure in this
> file as unverified until the benchmark re-runs. Left in place because it is unclear
> what "COMPLETE" was originally scoped to; see `writing-notes/ch4-comment-pass.md`.

> Status: COMPLETE — ALL FIGURES RECOMPUTED LOCALLY (2026-06-27) — RQs v4 (four beverage categories; SRQ3 = integration readiness; Nielsen scanner panel only). The cleaned Nielsen parquets are local (`data/raw/nielsen_<cat>_clean_*.parquet`); structural figures, data-quality figures (null rates, negative/zero counts, in-scope SKU and series counts), and the detailed time-series EDA (ADF stationarity, ACF/PACF, seasonality, promo correlation) are computed directly from them under the DVH EXCL. HD market scope for all four categories. No `[regenerate]` placeholders remain. Awaiting human review only.
> Author: Claude Code — requires human review before finalisation
> Convention: all figures are local, recomputed under DVH EXCL. HD unless explicitly attributed to Brian's superseded all-markets audit.
> ✅ RESOLVED — MARKET SCOPE (verified locally, 2026-06-23): The 28 CSD market values are **hierarchical** (grand totals + group aggregates + individual chains). Brian's pipeline sums across all of them, which inflates CSD sales **6.16×** (168.6B units summed across all 28 levels vs 27.4B units at the single DVH EXCL. HD level; both figures de-duplicated on the slowly-changing market dimension). This thesis therefore scopes to the single market `market_description = "DVH EXCL. HD"` (Nielsen's recommended default; one `market_id`, no summing → double-counting impossible by construction). All CSD figures below are **recomputed locally under this scope** and supersede Brian's all-markets figures; they remain provisional only against Brian's final harmonised pipeline.

---

## 4.1 Overview and Data Strategy

> Claims settled in the 2026-09-07 comment pass (threads 133-137).
> Prose staged in `writing-notes/ch4-comment-pass.md` blocks C1-C4.

**Claims this section must make**

- One secondary data source: the Nielsen/Prometheus beverage scanner panel, four Danish
  categories (CSD, danskvand, energidrikke, RTD).
- **Beer (`totalbeer`) was available at source and deliberately excluded** on compute and
  bandwidth grounds -- an analytical scoping choice, NOT a gap in the data.
  Evidence: `save_all_datasets.py` registers `totalbeer_clean_facts_v`;
  `_00_raw/nielsen/data_jsonl/Totalbeer/metadata/` exists. Ch1 §1.4 and Ch3 §3.4 must
  agree. (thread 134)
- **The data are point-of-sale scanner records, not survey data.** Nielsen metadata
  describes the monetary measures as consumer retail price captured at point of sale;
  "survey" appears nowhere in any category's metadata. Coverage is bounded by which
  retailers report, not by sampling error. (thread 136)
- CSD is the worked category (**§4.2**, not §4.3 -- numbering corrected 2026-09-07).
- **The other three categories are load-bearing, not replications**: they carry the
  pooled-vs-per-category comparison, whose answer differs by category scale.
  Evidence: `srq1_model_performance/tables/pooled_summary.md`. (thread 135)
- **The split is proportional and derived, not locked or pre-registered** -- cut-offs are
  recomputed from each category's period count and move when the panel extends.
  Evidence: `_03_engineered/bymonth/CSD/csd_split_dates_h3.json` (test ends 2026-07).
  (thread 137; same fact as threads 183/185/187/191 in §4.4)
- Assessment follows the three-stage Saunders et al. (2023) secondary-data evaluation.
  Name the framework here; do not re-explain it -- Ch3 owns the explanation. (thread 133)

**Open**

- Chapter subtitle undecided; the literal placeholder `COULD USE A SUBTITLE` is still in
  the Word document and must be removed. (thread 131)
- Cross-thesis repetition question (thread 133) is a whole-document judgement, not a §4.1
  edit.

---

## 4.2 The Nielsen Scanner Panel (core forecasting input)

### 4.2.1 Source, Type, and Access

> Threads 139-140 settled 2026-09-07. Prose: `writing-notes/ch4-pass.md` §4.1.1.

- Provided by Manifold AI via the Prometheus platform; commercial, restricted access.
- **Documentary secondary data (scanner panel), NOT survey data** -- same correction as
  thread 136. The bolded phrase in Word was the error itself. (thread 139)
- **No NDA exists.** Access is restricted by understanding, not contract; raw extracts
  stay local and are not redistributed. Do not assert a legal instrument we cannot
  produce. ⚠ confirm against what was actually agreed. (thread 140)

**Open**
- Bolding has no convention chapter-wide; proposal is headers and table labels only.


### 4.2.2 Schema and Structure

> Threads 142-146 settled 2026-09-07. Prose: `writing-notes/ch4-pass.md` §4.1.2.

- Star schema verified: market/period/product dimensions, facts at market x product x
  period. Product dimension carries brand, manufacturer, pack format, flavour, price
  tier, corporate attribution. (thread 142)
- Period identifiers are not monotonic with calendar time; sort by
  (period_year, period_month).
- **Retention threshold is DERIVED, not chosen**: `min_periods = warmup + horizon + 1`
  = 15 at H1, 17 at H3. The >=30 / >=40 thresholds are gone -- three competing fixed
  values were removed 2026-08-18. This retracts a limitation rather than restating one.
  Evidence: `_shared_modules/engineer_features.py`. (thread 146)
- **Brands retained: 95 / 29 / 44 / 62** (CSD / danskvand / energidrikke / RTD),
  superseding 77 / 24 / 27 / 42. Evidence: `*_manifest_h3.json`. (thread 143)

**Open**
- Data-model diagram does not exist -- P0050 owes it. (thread 142)
- Table 4.1's long caption should move to an appendix. (thread 143)
- Periods and SKU columns not re-verified since 2026-06-27.


| Category | Periods (max) | Brands (in scope) | retained ≥40 | retained ≥30 | Catalog SKUs | In-scope SKUs | Brand-month rows | In-scope fact rows |
|---|---|---|---|---|---|---|---|---|
| CSD | 42 | 136 | 57 | **77** | 8,608 | 7,668 | 3,789 | 187,907 |
| danskvand | 37 | 49 | 0 ⚠️ | **24** | 565 | 453 | 1,090 | 24,796 |
| energidrikke | 39 | 64 | 0 ⚠️ | **27** | 747 | 577 | 1,520 | 49,345 |
| RTD | 37 | 93 | 0 ⚠️ | **42** | 589 | 511 | 2,193 | 44,449 |

### 4.2.3 Overall Suitability

> Threads 148-149 settled 2026-09-07. Prose: `writing-notes/ch4-pass.md` §4.1.3.

- Market scope is the single `DVH EXCL. HD` level; summing the 28 hierarchical market
  values inflates CSD volume 6.16x.
- **Exogenous predictors now include the holiday calendar** (`days_in_month`,
  `n_holidays`, `non_holiday_days`) -- present in the regenerated matrices. (thread 148)
- **Promo is unavailable for danskvand and RTD** (`has_promo: false`), so the predictor
  set is narrower there -- not zero-filled, absent. (thread 148)
- **Counts are extract-dependent, not fixed.** Monthly re-pull lengthens the panel and
  admits brands previously below the minimum. Report the extract date, not frozen
  numbers. (thread 149)


### 4.2.4 Precise Suitability

> Threads 151-154 settled 2026-09-07. Prose: `writing-notes/ch4-pass.md` §4.1.4.

- **Zero is a measurement; null is an unobserved month.** The thesis had this inverted.
  Zero-fill applies to sales measures in months absent from a brand's calendar because
  the brand sold nothing, not an unknown amount. Evidence: `engineer_features.py` --
  "That is a measurement, not a gap to be imputed." (thread 152)
- **Weighted-distribution gaps are forward-filled within brand, never backward.** The
  claimed brand-and-market median imputation DOES NOT EXIST in the code. bfill was
  removed as leakage: it contaminated 1,176 rows (19.1% of the calendar) across 51
  brands. Leading gaps fill zero. (thread 153)
- **Negatives are floored to zero without asserting a cause.** The extract cannot
  distinguish returns/corrections from recording errors, so claim the treatment, not the
  explanation. Evidence: `full[c] = full[c].clip(lower=0)`. (thread 154)

**Open**
- Reliability currently rests on Nielsen's reputation with no source -- register row 5.
  Either cite a panel-data methodology source or argue from the completeness figures.
  (thread 151)
- Null-rate percentages and negative-row counts predate the regeneration.


- *Promotional values*: where the promotional metric exists (CSD and energidrikke) it is fully populated (0.00% null), with the absence of promotional activity encoded as a zero rather than a null; for **danskvand** and **RTD** the promotional column is absent entirely, collapsing to the promo-zero case above.
- *Weighted-distribution nulls*: negligible across all categories — 0.019% (CSD), 0.016% (danskvand), 0.093% (energidrikke), 0.000% (RTD). These reflect products Nielsen does not track for distribution in a given period; they are imputed using a brand-and-market median, which preserves central tendency but ignores within-period time variation (a moderate limitation for niche brands, immaterial at these null rates).
- *Negative and zero values*: negatives are return/correction adjustments standard in scanner data and are clipped to zero — they are rare (CSD 58 rows, 0.031%; danskvand 14, 0.057%; energidrikke 16, 0.032%; RTD 10, 0.022%). True zero-sales rows are likewise rare (CSD 12, danskvand 1, energidrikke 28, RTD 17) and are retained and flagged as genuine zeros, distinct from corrections.

### 4.2.5 Forecasting Suitability

> Threads 156-157 settled 2026-09-07. Prose: `writing-notes/ch4-pass.md` §4.1.5.

- **Adequacy rests on three-plus complete annual cycles**, verifiable from the panel --
  NOT on an ARIMA minimum period count, which had no source in the 86-entry library.
  Register row 6. (thread 156)
- Benchmarking uses the brands meeting the derived minimum length: 95 / 29 / 44 / 62.
  (thread 157)
- A fully-observed subset (present in every period) is a stricter alternative; the
  57/22/18/37 figures predate regeneration and need re-deriving if cited.


---

## 4.3 CSD — Worked Category (EDA and Parameters)

> Threads 159-175 settled 2026-09-07. Prose: `writing-notes/ch4-pass.md` §4.2.
> NOTE: this is §4.2 in the Word document under the corrected numbering.

**Claims this section must make**

- **CSD is the worked category because it is the largest and longest-running**: most
  brands, longest unbroken history, and it has the promo measures two others lack -- so
  it exercises every stage of the pipeline. State the justification; do not assert the
  status. (thread 159)
- Panel: **142 brands, 4,209 brand-month rows**, full-history series **46 periods**
  (thesis says 136 / 3,789 / 42). Retained after the derived minimum: **95 brands**.
  Evidence: `csd_eda_tables/step_2_01_shape.md`. (thread 161)
- **Stationarity is per-brand, not aggregate.** Difference-stationarity dominates; a
  minority are stationary in log level; a few need no transform. ADF power is limited at
  n=46, so treat as indicative of the transform, not a classification.
  Evidence: `step_2_05_adf_per_brand.md`. (thread 163)
- **Peak months verified exactly as stated** -- CSD {3,6,9,12}, danskvand {6,7,8,9},
  energidrikke {3,6,9}, RTD {5,6,12}. Four measured profiles, each commercially
  plausible. This is a real result and should stay prominent.
  Evidence: all four `step_3_contract_h3.md`. (thread 165)
- The indicator is named for what it measures (an elevated month), not a presumed cause.
  Peaks are quarter-ends -- trade loading, not holidays. (thread 165)
- Mean-based rule, not totals: the panel is unbalanced, so a month's total reflects how
  many brands were active. (thread 165)
- **Two ACF estimates differ by construction** -- single-brand keeps the brand's level,
  pooled demeans first and isolates common dynamics, so pooled is larger. Conclusion is
  unaffected. (thread 167)
- **All 142 CSD brands have no zero-sales months**, so intermittent demand does not arise
  for this category. Evidence: `step_2_07_zero_types.md`. Cites Hyndman & Koehler (2006),
  which IS in the library.

**Open**

- **Table 3 (per-category EDA) is NOT verified.** Promo correlations (r=0.937/0.988), ADF
  p-values and ACF figures all predate regeneration and could not be reproduced from
  current outputs -- `step_2_13_promo_intensity` gives a distribution, not a correlation.
  Needs a regeneration pass. (thread 173)
- Table 2 (parameters) has two wrong rows: MIN_PERIODS 30 and the 24/6/12 split.
- Both tables are appendix candidates -- P0050. (threads 169, 173)
- Remove revision narration throughout ("supersedes Brian's...", "revises...",
  "renamed from..."). Six threads flag this as METADATA.
- "§4.6" cross-reference is residue; no such section exists. (thread 172)


### 4.3.1 Scope and Filtering

- **Market scope**: `DVH EXCL. HD` (single Nielsen market level; see header). 187,907 facts rows fall in scope.
- **Span**: 42 monthly periods (Oct 2022–Mar 2026) on Nielsen's 4-4-5 week calendar. (Period identifiers are not calendar-monotonic, so the span is taken from the documented window, not raw min/max.)
- **Brands**: 136 total; the adopted filter `MIN_PERIODS ≥ 30` (≥30 non-zero monthly observations) retains **77 brands** and **3,077** brand-month rows (of 3,789 total). A ≥40 filter would retain only 57 and is infeasible for the other three categories (37–39 periods → zero brands), so ≥30 is applied globally (Table 4.1). These figures are recomputed locally under DVH EXCL. HD and **supersede** Brian's all-markets values (143 → 62 brands; 4,040 rows), inflated by the market double-count.
- **Aggregation grain**: brand × month, positive sales only; weighted distribution averaged rather than summed (correct for an ACV metric).

### 4.3.2 Stationarity

- **ADF test (aggregate monthly total, n = 42, DVH EXCL. HD)**: the level series is non-stationary in both raw (p = 0.360) and log form (p = 0.421); it becomes stationary only after first differencing (p < 0.001) — i.e. the series is difference-stationary, I(1). This **revises** Brian's all-markets finding that the log level was stationary (p = 0.028): that does not hold at the corrected scope. (ADF power is limited at n = 42.)
- **Treatment**: a natural-log transform is applied to `sales_units` to stabilise variance; non-stationarity in the mean is handled by **differencing** for ARIMA and by **lagged/rolling features** for the tree models (which do not require a stationary level). NaN is preserved for non-positive/missing values rather than imputed.

### 4.3.3 Seasonality

- **Peak months (share of annual units, DVH EXCL. HD)**: December (12.8%), March (10.9%), June (8.9%); September is next at 8.5%.
- **Peak-month indicator**: `PEAK_MONTHS` — months whose mean `sales_units` exceeds the category's overall mean by more than 10%, measured per category. For CSD this gives {3, 6, 9, 12}.
  - Renamed from `HOLIDAY_MONTHS` (2026-08-18). No holiday calendar is an input to the pipeline, so the former name asserted a cause the computation never established. The evidence often contradicts it: CSD's peaks are the quarter-end months, consistent with retail trade loading rather than holidays.
  - **Now verified per category**, resolving the open question: CSD {3, 6, 9, 12}; Danskvand {6, 7, 8, 9} (summer — bottled water); Energidrikke {3, 6, 9} (quarter-ends, **no December peak**); RTD {5, 6, 12}. Four distinct seasonal profiles, each commercially plausible for its category.
  - The earlier `{3, 6, 12}` came from a top-quartile rule on monthly *totals*, which is confounded by how many brands were active in a month. The current rule uses means, which is not — the panel is unbalanced by construction. September enters CSD's set under the corrected rule.

### 4.3.4 Autocorrelation and Lag Structure

- **Lag set**: `LAGS = (1, 2, 3, 4, 8, 13)` and `ROLLING_WINDOWS = (4, 13)` (4-month and ~annual cycles on the Nielsen calendar).
- **Autocorrelation (recomputed, DVH EXCL. HD)**: for the top brand by units (HARBOE, n = 42) the log-series ACF is +0.26 (lag 1), +0.47 (lag 3), and ≈0 (lag 13) — a strong quarterly (lag-3) signal but a weak annual (lag-13) one for this brand. Lag structure is clearly brand-dependent, so a single global lag set is a simplification; per-brand optimisation is out of scope. This **revises** Brian's Coca-Cola example (lag-1 = −0.399), which was computed on the inflated all-markets series. *Method note*: the per-category figures in §4.3.6 (CSD lag-1 +0.78) use a pooled, brand-demeaned log series across all retained brands, whereas the HARBOE figures here are a single-brand series; the pooled estimate is larger because demeaning removes between-brand level differences and leaves the common short-horizon dynamics. Both are reported; the qualitative conclusion (positive short-horizon, near-zero annual carry) is robust to the method.
- **Promotional intensity**: strongly correlated with sales units, confirmed under DVH EXCL. HD at r = 0.937 (n = 2,442 promo-bearing brand-month rows), closely matching Brian's all-markets value (r = 0.941); the relationship is robust to market scope. For energidrikke the promotional signal is even stronger (r = 0.988); danskvand and RTD carry no promotional data (promo-zero).

### 4.3.5 Parameter Summary

| Parameter | Value (CSD) | Basis | Status |
|---|---|---|---|
| `MIN_PERIODS` | 30 (global) | feasibility (other cats have 37–39 periods) + quality | adopted |
| `LAGS` | 1, 2, 3, 4, 8, 13 | ACF/PACF inspection | empirical; needs prose justification |
| `ROLLING_WINDOWS` | 4, 13 | 4-month + annual cycle | empirical |
| `PEAK_MONTHS` | per category: CSD 3,6,9,12; Danskvand 6,7,8,9; Energidrikke 3,6,9; RTD 5,6,12 | mean monthly units >10% above the category mean | derived per category (renamed from `HOLIDAY_MONTHS`) |
| log transform | applied to `sales_units` | variance stabilisation; series is I(1), diff-stationary (ADF p<0.001) | confirmed |
| Train / Val / Test | 24 / 6 / 12 months | forward-chaining (Section 4.5) | confirmed |

### 4.3.6 Per-category EDA — danskvand, energidrikke, RTD

<!-- Approved by Enrico 2026-06-24. Numbers factual, recomputed locally under

| Category | Promo correlation | Peak month | Top brand | ADF (log level) | Verdict | ACF lag1 / lag3 |
|---|---|---|---|---|---|---|
| CSD | r = 0.937 | December | HARBOE | p = 0.421 | non-stationary, I(1) | +0.78 / +0.55 |
| danskvand | none (promo-zero) | June | HARBOE | p = 0.998 | non-stationary, I(1) | +0.55 / +0.25 |
| energidrikke | r = 0.988 | March | RED BULL | p = 0.901 | non-stationary, I(1) | +0.71 / +0.39 |
| RTD | none (promo-zero) | December | BREEZER | p = 0.000 | stationary in level | +0.82 / +0.58 |

---

## 4.4 Feature Engineering (forecasting substrate)

> Threads 177-181 settled 2026-09-07. Prose: `writing-notes/ch4-pass.md` §4.3.
> NOTE: this is §4.3 in the Word document.

**Claims this section must make**

- **The holiday enrichment is IN the data**: `days_in_month`, `n_holidays`,
  `non_holiday_days` are present in the regenerated matrices. (thread 177)
- Model inputs: six lags, three rolling statistics, three calendar features, three
  holiday features, promo_intensity where available.
- `log_sales_units` is the TARGET, not an input -- using it would be trivial leakage.
  (thread 180)
- **Tree models take NaN natively (default branch direction per split); the linear model
  gets a zero-fill at fit time.** Deferring to the model keeps both treatments visible
  instead of hiding one imputation in the shared substrate. No citation needed -- this is
  a property of the implementations. (thread 181)

**Open**

- ⚠ **Four competing counts exist and none matches the thesis's "22 columns / 17
  features"**: parquet 54 columns, manifest 34 features, `srq1_benchmark.py` 13 trained,
  pooled comparison 12. Best reconstruction is 13 + 3 holiday = **16**. Read the benchmark
  script before finalising. (threads 177, 179)
- **`weighted_distribution` as "the fourteenth input feature" is doubtful** -- it is not in
  the FEATURES list; it is a raw Nielsen measure in the matrix, which is different from
  being a model input. (thread 180)


| Feature | Description | Models |
|---|---|---|
| `lag_1`, `lag_2`, `lag_3`, `lag_4`, `lag_8`, `lag_13` | Lagged `sales_units` (short, medium, seasonal) | LightGBM, XGBoost, Ridge |
| `rolling_mean_4`, `rolling_std_4` | 4-month rolling mean and standard deviation | LightGBM, XGBoost, Ridge |
| `rolling_mean_13` | Trailing annual average | LightGBM, XGBoost, Ridge |
| `month`, `quarter`, `peak_month` | Calendar features (`peak_month` = month in the category's derived `PEAK_MONTHS`) | LightGBM, XGBoost, Ridge |
| `promo_intensity` | Promotional share of units (clipped 0–1) | LightGBM, XGBoost, Ridge |
| `weighted_distribution` | Nielsen weighted-distribution availability proxy | LightGBM, XGBoost, Ridge |

---

## 4.5 Train, Validation, and Test Split

| Category | Periods | Train | Validation | Test | Train window | Validation window | Test window |
|---|---|---|---|---|---|---|---|
| CSD | 42 | 24 | 6 | 12 | 2022-10 → 2024-09 | 2024-10 → 2025-03 | 2025-04 → 2026-03 |
| danskvand | 37 | 23 | 6 | 8 | 2023-03 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |
| energidrikke | 39 | 25 | 6 | 8 | 2023-01 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |
| RTD | 37 | 23 | 6 | 8 | 2023-03 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |

---

## 4.6 Key Risks and Mitigations

> Threads 193-194 settled 2026-09-07. Prose: `writing-notes/ch4-pass.md` §4.5.
> NOTE: this is §4.5 in the Word document.

**Claims this section must make**

- Figures are pipeline-generated and regenerate on refresh; report the extract date rather
  than framing figures as "verified (resolved)". A risk register states standing
  limitations, not project history. (thread 193)
- **The weighted-distribution median imputation DOES NOT EXIST** -- it is a within-brand
  forward fill with an explicit no-backfill guard. The current text concedes a limitation
  the pipeline does not have. Residual risk is a stale value persisting through a long
  gap. (thread 193)
- Thin panels: danskvand and RTD retain 29 and 62 brands against CSD's 95. Statistical
  baselines are most exposed since they estimate from a single series. Report panel
  lengths so the reader can weight the results. (thread 193)
- Promo-zero categories (danskvand, RTD) lack the signal entirely -- unmeasured-variable
  limitation.
- Generalisability bounded to DVH EXCL. HD, the observed window, and the retained series.

**Open**

- **Chapter 4 cites exactly one source (Saunders et al. 2023).** Most claims are
  measurements of this dataset and are correctly uncited, but three places genuinely need
  one: Hyndman & Koehler 2006 (in library, usable now), Box & Jenkins 1970 (NOT in
  library -- register row 8), and a commercial-panel reliability source (register row 6).
  (thread 194)
- Stale numbers to correct here: MIN_PERIODS=30, "CSD (42 periods, 77 brands)" -> 46 and 95.


- **Figures verified (resolved).** All structural, data-quality, and EDA figures in this chapter are recomputed locally from the `data/raw` parquets under the DVH EXCL. HD scope (2026-06-27), superseding the earlier P0023 audit values; no placeholders remain. Residual dependence is only on Brian's final harmonised pipeline, against which the local figures are expected to reconcile.
- **Market scope (resolved).** Confirmed locally that the inherited "All Markets" aggregation double-counts (6.16× inflation for CSD; 14–17× for the other three categories, which expose 86 market levels). Resolved by scoping all four categories to the single `DVH EXCL. HD` market level; feature matrices regenerated accordingly (2026-06-23) under DVH EXCL. HD + MIN_PERIODS=30.
- **Per-category EDA (resolved).** All four categories now have a dedicated EDA recomputed under DVH EXCL. HD (§4.3.6): stationarity (three of four series I(1), RTD stationary in level), short-horizon autocorrelation (lag-1 +0.55…+0.82), seasonality, and promo correlation. `MIN_PERIODS` and `LAGS` transfer reasonably across categories; `PEAK_MONTHS` is derived per category rather than inherited, since the four seasonal profiles differ materially. Per-brand lag optimisation remains a stated scope bound.
- **Thin training windows (danskvand, RTD).** Both have only 23 training months, marginally below the ~24-period ARIMA rule of thumb, and danskvand has just 24 retained brands. Mitigation: these three categories are framed as parallel proofs of concept rather than primary evidence; CSD (42 periods, 77 brands) is the worked category carrying the main claims, and the short-window caveat is restated in the discussion.
- **Empirical parameters.** `MIN_PERIODS`, `LAGS`, `ROLLING_WINDOWS`, and `PEAK_MONTHS` are EDA-driven, not theory-first. Mitigation: justified post hoc in the modelling chapter and stated as a limitation.
- **Promotional coverage (danskvand, RTD).** Promo-zero categories lack the promotional signal (an unmeasured-variable limitation). Mitigation: promotional features are disabled for these categories and the limitation is stated in the discussion.
- **Weighted-distribution imputation.** Median imputation ignores within-period time variation (moderate risk for niche brands, low for high-coverage brands). Mitigation: documented; sensitivity noted.
- **Commercial access / confidentiality.** Raw data cannot be redistributed and must stay local; full external reproducibility is limited to processed features, code, and protocol.
- **Generalisability bound.** Findings are bounded to the DVH EXCL. HD scope, the available period window, and the fully observed series filter; applicability to other markets, intermittent series, or non-beverage categories is future research.

---

## References cited in this chapter

- Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). *Research Methods for Business Students* (9th ed.). Pearson.
