# Chapter 4 — Data Assessment
> Status: COMPLETE — ALL FIGURES RECOMPUTED LOCALLY (2026-06-27) — RQs v4 (four beverage categories; SRQ3 = integration readiness; Nielsen scanner panel only). The cleaned Nielsen parquets are local (`data/raw/nielsen_<cat>_clean_*.parquet`); structural figures, data-quality figures (null rates, negative/zero counts, in-scope SKU and series counts), and the detailed time-series EDA (ADF stationarity, ACF/PACF, seasonality, promo correlation) are computed directly from them under the DVH EXCL. HD market scope for all four categories. No `[regenerate]` placeholders remain. Awaiting human review only.
> Author: Claude Code — requires human review before finalisation
> Convention: all figures are local, recomputed under DVH EXCL. HD unless explicitly attributed to Brian's superseded all-markets audit.
> ✅ RESOLVED — MARKET SCOPE (verified locally, 2026-06-23): The 28 CSD market values are **hierarchical** (grand totals + group aggregates + individual chains). Brian's pipeline sums across all of them, which inflates CSD sales **6.16×** (168.6B units summed across all 28 levels vs 27.4B units at the single DVH EXCL. HD level; both figures de-duplicated on the slowly-changing market dimension). This thesis therefore scopes to the single market `market_description = "DVH EXCL. HD"` (Nielsen's recommended default; one `market_id`, no summing → double-counting impossible by construction). All CSD figures below are **recomputed locally under this scope** and supersede Brian's all-markets figures; they remain provisional only against Brian's final harmonised pipeline.

---

## 4.1 Overview and Data Strategy

This thesis draws on one secondary data source in the sense of Saunders et al. (2023): data originally collected by others for another purpose and reanalysed here. The **Nielsen/Prometheus beverage scanner panel** is the forecasting input, covering four Danish beverage categories: carbonated soft drinks (CSD), still and sparkling water (danskvand), energy drinks (energidrikke), and ready-to-drink beverages (RTD). A fifth category, beer (totalbeer), was scoped out because its facts table is absent from the source data (the data do not exist at source, not a size or memory constraint); this is recorded as a data limitation rather than an analytical choice. CSD is the **worked category**, assessed in full (Section 4.3); the other three are processed through the identical pipeline as parallel proofs of concept.

It is survey-type, structured, commercial secondary data. Consistent with the pragmatist stance of Chapter 3, it is treated as a partial but workable representation of demand realities, shaped by the collecting instrument, rather than as a theory-free objective record.

This chapter assesses the data following the three-stage secondary-data evaluation of Saunders et al. (2023): (i) **overall suitability** (measurement validity and coverage), (ii) **precise suitability** (reliability/dependability, validity/credibility, and measurement bias/trustworthiness), and (iii) **costs, benefits, and ethics**. The assessment is conducted per category, since the four categories differ systematically in scale and promotional structure. The train, validation, and test split is then specified as a locked, pre-registered design decision applied identically across the forecasting models (Chapter 6), and the key data risks are documented to bound the empirical claims of the later chapters.

---

## 4.2 The Nielsen Scanner Panel (core forecasting input)

### 4.2.1 Source, Type, and Access

The Nielsen/Prometheus dataset is provided by Manifold AI through its Prometheus reporting platform. In Saunders et al.'s (2023) taxonomy it is **survey secondary data** (a continuously maintained commercial scanner panel), **structured** (organised in a star schema), and **quantitative**. It is used under a **confidentiality agreement** with Manifold AI: the raw data are not redistributed and do not leave the local research environment. Because access is commercial and restricted, the data could not have been collected independently within the scope of a thesis, which is itself a Saunders-listed advantage of using secondary data.

The four categories are each scoped by Manifold AI from the broader Prometheus platform. The exact extraction interface used by the pipeline is documented in Chapter 5; this chapter concerns the data themselves.

### 4.2.2 Schema and Structure

Each category follows a star schema: dimension tables for market, period, and product, linked to a facts table at the grain of market × product × period. The facts table records the core sales metrics (sales value, sales in litres, sales units), their promotional variants (the same metrics under promotion), and a weighted-distribution metric that proxies product availability. The product dimension captures brand, manufacturer, packaging format, flavour or type, price tier, and corporate attribution.

A technical note carried over from the prior pipeline and to be re-verified in the rebuild: period identifiers are not necessarily monotonic with calendar time, so all time-series operations sort by the composite key `(period_year, period_month)`. The facts table may also contain more distinct products than the active product dimension (discontinued or out-of-scope SKUs), so the join to the product dimension is the correct scoping mechanism.

Per-category structural counts (periods, brands, products/SKUs, brand-month rows, in-scope fact rows) are reported in Table 4.1, all computed locally under the DVH EXCL. HD scope.

| Category | Periods (max) | Brands (in scope) | retained ≥40 | retained ≥30 | Catalog SKUs | In-scope SKUs | Brand-month rows | In-scope fact rows |
|---|---|---|---|---|---|---|---|---|
| CSD | 42 | 136 | 57 | **77** | 8,608 | 7,668 | 3,789 | 187,907 |
| danskvand | 37 | 49 | 0 ⚠️ | **24** | 565 | 453 | 1,090 | 24,796 |
| energidrikke | 39 | 64 | 0 ⚠️ | **27** | 747 | 577 | 1,520 | 49,345 |
| RTD | 37 | 93 | 0 ⚠️ | **42** | 589 | 511 | 2,193 | 44,449 |

*Table 4.1. Per-category structure, all four categories computed locally under the DVH EXCL. HD scope (2026-06-27). CSD figures supersede Brian's all-markets values, inflated 6.16× by summing hierarchical markets; the CSD catalog-SKU count (8,608 distinct `product_id` in the product dimension) likewise supersedes the earlier 2,080.* **Column definitions**: *Catalog SKUs* = distinct `product_id` in `dim_product`; *In-scope SKUs* = distinct `product_id` with positive sales at the DVH EXCL. HD scope; *Brand-month rows* = positive-sales brand × month observations across all in-scope brands (the retained ≥30 subset yields 3,077 / 885 / 1,007 / 1,543 observed rows respectively, per `regeneration_report.md`). **MIN_PERIODS feasibility**: danskvand, energidrikke, and RTD have only 37–39 monthly periods, so a ≥40-observation filter retains **zero** brands for them; a single global threshold of **≥30** is therefore adopted across all categories (CSD 77, danskvand 24, energidrikke 27, RTD 42 brands), which is both feasible and consistent — preferable to the inherited mixed rule (40 for CSD, 30 for the rest). The bold column (≥30) is the retained set used downstream.

### 4.2.3 Overall Suitability

**Measurement validity / appropriateness.** The recorded metrics must measure the forecasting target. Sales units (and, where appropriate, litres) are the demand quantities to be forecast; the promotional variants and the weighted-distribution proxy serve as exogenous predictors. The weighted-distribution metric is an availability *proxy* rather than a direct census of shelf presence, and this proxy status is acknowledged in interpretation. **Market scope (resolved).** The primary market is **DVH EXCL. HD** (Danish grocery retail excluding hard discount), Nielsen's recommended default and the scope on which Manifold AI reports. This choice is not cosmetic: the 28 CSD market values form a hierarchy (individual chains nested within group aggregates such as COOP and SALLING GROUP, nested within grand-total roll-ups such as DVH/CONVENIENCE INCL. HD). A local check confirmed that aggregating sales across all 28 — as the inherited pipeline did — counts the same sales at multiple levels and inflates CSD volume by 6.16× (168.6B units summed across all 28 levels vs 27.4B units at the single DVH EXCL. HD level, a legitimate grand-total comparable to DVH/CONVENIENCE INCL. HD at 32.2B; all figures de-duplicated on the slowly-changing market dimension before aggregation). Scoping to the single `DVH EXCL. HD` market level eliminates this by construction (one market identifier, no cross-market summation) and yields a clean branded-demand signal excluding the structurally different hard-discount channel.

**Coverage.** The panel must cover the right population and period and leave sufficient data after exclusions. All four categories are scoped to the single DVH EXCL. HD market level (one market identifier per category, by design), so coverage is assessed on the temporal span, the brand and SKU counts, and the retained series. The temporal span is 37–42 months (CSD 42, energidrikke 39, danskvand and RTD 37), with complete intermediate calendar years constituting the primary training window. In-scope brand counts are 136 (CSD), 49 (danskvand), 64 (energidrikke), and 93 (RTD); in-scope SKU counts are 7,668, 453, 577, and 511 respectively (Table 4.1). After the ≥30-month retention filter, 77 / 24 / 27 / 42 brands remain for benchmarking, with 3,077 / 885 / 1,007 / 1,543 observed brand-month rows. A category-specific coverage caveat applies to **promotional coverage**: for **danskvand** and **RTD** the promotional variables are effectively absent (promo-zero), so the promotional features are unmeasured for those categories, an unmeasured-variable limitation in Saunders' terms, carried forward to the modelling and discussion.

### 4.2.4 Precise Suitability

**Reliability / dependability.** Nielsen is an established commercial panel provider whose continued operation depends on data credibility; its scanner data are therefore treated as reliable, while recognising that, as with any provider, definitions and collection conventions are fixed by Nielsen rather than by the researcher.

**Validity / credibility.** Credibility rests on how the data were collected and compiled (scanner capture aggregated to the market × product × period grain). Definitions (market aggregates such as DVH EXCL. HD, metric definitions, corporate attribution) are provider-set and are documented rather than altered.

**Measurement bias / trustworthiness.** Three data patterns require explicit treatment; per-category figures, computed locally on the in-scope facts, are reported below:
- *Promotional values*: where the promotional metric exists (CSD and energidrikke) it is fully populated (0.00% null), with the absence of promotional activity encoded as a zero rather than a null; for **danskvand** and **RTD** the promotional column is absent entirely, collapsing to the promo-zero case above.
- *Weighted-distribution nulls*: negligible across all categories — 0.019% (CSD), 0.016% (danskvand), 0.093% (energidrikke), 0.000% (RTD). These reflect products Nielsen does not track for distribution in a given period; they are imputed using a brand-and-market median, which preserves central tendency but ignores within-period time variation (a moderate limitation for niche brands, immaterial at these null rates).
- *Negative and zero values*: negatives are return/correction adjustments standard in scanner data and are clipped to zero — they are rare (CSD 58 rows, 0.031%; danskvand 14, 0.057%; energidrikke 16, 0.032%; RTD 10, 0.022%). True zero-sales rows are likewise rare (CSD 12, danskvand 1, energidrikke 28, RTD 17) and are retained and flagged as genuine zeros, distinct from corrections.
Core sales metrics are complete: `sales_units` has 0.00% nulls in every category, confirmed locally.

### 4.2.5 Forecasting Suitability

The panel must support the forecasting models. The 37–42-month span exceeds the ARIMA minimum of roughly 24 periods for stable parameter identification and contains enough annual cycles for seasonality to be learned by both decomposition and gradient-boosted models. Benchmarking (Chapter 6) is conducted on the brand series retained by the ≥30-month filter (77 / 24 / 27 / 42 brands for CSD / danskvand / energidrikke / RTD), so that model comparisons are not confounded by very short series; missing months within a retained series are exposed on the regular monthly grid and handled natively by the models rather than imputed. A stricter, fully observed subset (brands present in every period) comprises 57 / 22 / 18 / 37 brands respectively. Applicability to shorter or intermittent series is a bound on external validity, not a claim of this thesis.

---

## 4.3 CSD — Worked Category (EDA and Parameters)

CSD is the worked category. The structural counts and the stationarity, seasonality, and autocorrelation statistics below are **recomputed locally under the DVH EXCL. HD scope** (2026-06-23); the few items still taken from Brian's all-markets audit are flagged. The other three categories are processed through the identical pipeline; per-category EDA replication under the corrected scope is pending (Section 4.6).

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
- **Holiday indicator**: `HOLIDAY_MONTHS = {3, 6, 12}` (months above the ~75th sales percentile) — **confirmed** at the corrected scope: December/March/June remain the top three. Recomputed locally, and it matches Brian's all-markets ranking, so seasonality is robust to market scope. Whether the same months peak in the other categories is still to be verified.

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
| `HOLIDAY_MONTHS` | 3, 6, 12 | >75th sales percentile | confirmed under DVH EXCL. HD |
| log transform | applied to `sales_units` | variance stabilisation; series is I(1), diff-stationary (ADF p<0.001) | confirmed |
| Train / Val / Test | 24 / 6 / 12 months | forward-chaining (Section 4.5) | confirmed |

These parameters are EDA-driven rather than theory-first; their academic justification is developed in the modelling chapter, and their empirical (not theoretical) origin is stated honestly as a limitation.

### 4.3.6 Per-category EDA — danskvand, energidrikke, RTD

<!-- Approved by Enrico 2026-06-24. Numbers factual, recomputed locally under
DVH EXCL. HD (source: thesis/data/_03_engineered_dvhexclhd/eda_findings_dvhexclhd.md). -->

The three proof-of-concept categories were taken through the identical pipeline and their EDA recomputed under the corrected DVH EXCL. HD scope, closing the gap previously flagged in §4.6.

| Category | Promo correlation | Peak month | Top brand | ADF (log level) | Verdict | ACF lag1 / lag3 |
|---|---|---|---|---|---|---|
| CSD | r = 0.937 | December | HARBOE | p = 0.421 | non-stationary, I(1) | +0.78 / +0.55 |
| danskvand | none (promo-zero) | June | HARBOE | p = 0.998 | non-stationary, I(1) | +0.55 / +0.25 |
| energidrikke | r = 0.988 | March | RED BULL | p = 0.901 | non-stationary, I(1) | +0.71 / +0.39 |
| RTD | none (promo-zero) | December | BREEZER | p = 0.000 | stationary in level | +0.82 / +0.58 |

Three of the four category-level series are difference-stationary (I(1)); RTD is already stationary in log level. All show strong positive short-horizon autocorrelation (lag-1 +0.55…+0.82), supporting the shared lag/rolling feature set, with near-zero lag-13 carry. Seasonality is category-appropriate (water peaks in summer, the others in autumn/spring). danskvand and RTD carry no promotional signal — the unmeasured-variable limitation already noted. These findings confirm the CSD-derived parameter defaults (`MIN_PERIODS`, `LAGS`, `HOLIDAY_MONTHS`) transfer reasonably across categories; per-series lag structure is brand-dependent and not separately optimised (a stated scope bound).

---

## 4.4 Feature Engineering (forecasting substrate)

The forecasting substrate uses features derived from the Nielsen facts table at the brand × month granularity. The feature matrix contains 22 columns: **14 modelling features** per observation, plus index/key columns, the target, the carried `promo_units`, and the split label (verified against the parquet, `scripts/srq1_benchmark_tuned.py`). These are the exogenous and autoregressive predictors referenced in Chapter 1.

| Feature | Description | Models |
|---|---|---|
| `lag_1`, `lag_2`, `lag_3`, `lag_4`, `lag_8`, `lag_13` | Lagged `sales_units` (short, medium, seasonal) | LightGBM, XGBoost, Ridge |
| `rolling_mean_4`, `rolling_std_4` | 4-month rolling mean and standard deviation | LightGBM, XGBoost, Ridge |
| `rolling_mean_13` | Trailing annual average | LightGBM, XGBoost, Ridge |
| `month`, `quarter`, `holiday_month` | Calendar features (`holiday_month` = month in {3,6,12}) | LightGBM, XGBoost, Ridge |
| `promo_intensity` | Promotional share of units (clipped 0–1) | LightGBM, XGBoost, Ridge |
| `weighted_distribution` | Nielsen weighted-distribution availability proxy | LightGBM, XGBoost, Ridge |

The 14 features comprise six lags, three rolling statistics, three calendar features, `promo_intensity`, and `weighted_distribution`. Two clarifications resolve earlier ambiguity: `log_sales_units` is the **modelling target** (the models predict log sales and exponentiate back), **not** an input feature — using it as a predictor would be trivial leakage; and `weighted_distribution` **is** the fourteenth input feature, while the raw `promo_units` column is carried through the matrix but is not itself a model input (only its derived `promo_intensity` is). Index/target/label columns carried alongside the features: `brand`, `period_index`, `period_year`, `period_month`, `sales_units` (raw target), `log_sales_units` (log target), `promo_units`, `split`. Lag and rolling features carry NaN for short history (expected); no imputation is done in preprocessing, so the tree models handle NaN natively and the linear model receives a zero-fill at fit time.

ARIMA and Prophet are fitted as univariate statistical baselines on the (log) sales series, not on the tabular feature matrix. The promotional feature is **not informative for danskvand and RTD** (promo-zero) and is handled accordingly for those categories.

---

## 4.5 Train, Validation, and Test Split

The split is defined by calendar date and locked as a pre-specified design decision, applied identically across the forecasting models and across categories. No random shuffling is applied: a strict temporal split preserves the autocorrelation structure and prevents leakage of future observations into training or validation.

Because the categories differ in length, the split is expressed as contiguous chronological blocks per category (training → validation → test), with the test window placed in the most recent months relevant to Manifold AI's planning horizon and covering at least one autumn/winter promotional cycle. The training window is required to satisfy the ARIMA minimum (~24 periods) and to contain at least two seasonal cycles for Prophet.

The per-category boundaries, taken from the locked split files (`<cat>_split_dates.json`), are:

| Category | Periods | Train | Validation | Test | Train window | Validation window | Test window |
|---|---|---|---|---|---|---|---|
| CSD | 42 | 24 | 6 | 12 | 2022-10 → 2024-09 | 2024-10 → 2025-03 | 2025-04 → 2026-03 |
| danskvand | 37 | 23 | 6 | 8 | 2023-03 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |
| energidrikke | 39 | 25 | 6 | 8 | 2023-01 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |
| RTD | 37 | 23 | 6 | 8 | 2023-03 → 2025-01 | 2025-02 → 2025-07 | 2025-08 → 2026-03 |

*Table 4.2. Forward-chaining train/validation/test boundaries per category (locked, pre-registered).* CSD, the longest series, takes a 12-month test window covering a full annual cycle; the three shorter categories take an 8-month test window (a ≥40-month series would be needed for a 12-month test under the same rule). Every training window satisfies the ARIMA minimum (~24 periods; danskvand and RTD at 23 are marginally below and are flagged as a thin-data caveat in §4.6) and contains at least two seasonal cycles for Prophet. All test windows end in March 2026 and cover at least one autumn/winter promotional cycle.

---

## 4.6 Key Risks and Mitigations

- **Figures verified (resolved).** All structural, data-quality, and EDA figures in this chapter are recomputed locally from the `data/raw` parquets under the DVH EXCL. HD scope (2026-06-27), superseding the earlier P0023 audit values; no placeholders remain. Residual dependence is only on Brian's final harmonised pipeline, against which the local figures are expected to reconcile.
- **Market scope (resolved).** Confirmed locally that the inherited "All Markets" aggregation double-counts (6.16× inflation for CSD; 14–17× for the other three categories, which expose 86 market levels). Resolved by scoping all four categories to the single `DVH EXCL. HD` market level; feature matrices regenerated accordingly (2026-06-23) under DVH EXCL. HD + MIN_PERIODS=30.
- **Per-category EDA (resolved).** All four categories now have a dedicated EDA recomputed under DVH EXCL. HD (§4.3.6): stationarity (three of four series I(1), RTD stationary in level), short-horizon autocorrelation (lag-1 +0.55…+0.82), seasonality, and promo correlation. The CSD-derived parameter defaults (`MIN_PERIODS`, `LAGS`, `HOLIDAY_MONTHS`) are confirmed to transfer reasonably across categories; per-brand lag optimisation remains a stated scope bound.
- **Thin training windows (danskvand, RTD).** Both have only 23 training months, marginally below the ~24-period ARIMA rule of thumb, and danskvand has just 24 retained brands. Mitigation: these three categories are framed as parallel proofs of concept rather than primary evidence; CSD (42 periods, 77 brands) is the worked category carrying the main claims, and the short-window caveat is restated in the discussion.
- **Empirical parameters.** `MIN_PERIODS`, `LAGS`, `ROLLING_WINDOWS`, and `HOLIDAY_MONTHS` are EDA-driven, not theory-first. Mitigation: justified post hoc in the modelling chapter and stated as a limitation.
- **Promotional coverage (danskvand, RTD).** Promo-zero categories lack the promotional signal (an unmeasured-variable limitation). Mitigation: promotional features are disabled for these categories and the limitation is stated in the discussion.
- **Weighted-distribution imputation.** Median imputation ignores within-period time variation (moderate risk for niche brands, low for high-coverage brands). Mitigation: documented; sensitivity noted.
- **Commercial access / confidentiality.** Raw data cannot be redistributed and must stay local; full external reproducibility is limited to processed features, code, and protocol.
- **Generalisability bound.** Findings are bounded to the DVH EXCL. HD scope, the available period window, and the fully observed series filter; applicability to other markets, intermittent series, or non-beverage categories is future research.

---

## References cited in this chapter

- Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). *Research Methods for Business Students* (9th ed.). Pearson.
