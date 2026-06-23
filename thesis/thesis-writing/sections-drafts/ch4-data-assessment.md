# Chapter 4 — Data Assessment
> Status: CSD RECOMPUTED LOCALLY + PLACEHOLDERS — updated 2026-06-23 to RQs v4 (four beverage categories; SRQ3 = integration readiness; Nielsen scanner panel only). The cleaned Nielsen parquets ARE local (`data/raw/nielsen_<cat>_clean_*.parquet`); structural figures for ALL FOUR categories are recomputed directly from them under the DVH EXCL. HD market scope (2026-06-23, see `thesis/data/_03_engineered_dvhexclhd/regeneration_report.md`). Basic EDA (promo correlation, seasonality peak month, top brand, total volume) is recomputed under DVH EXCL. HD for all four categories. The detailed time-series EDA in §4.3 (ADF stationarity, ACF/PACF) is confirmed for CSD under DVH EXCL. HD but still pending recomputation for danskvand/energidrikke/RTD before finalisation.
> Author: Claude Code — requires human review before finalisation
> Convention: `[regenerate]` marks a figure still to be computed from the local data; figures stated for CSD are local under DVH EXCL. HD unless noted.
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

Per-category structural counts (markets/retailers, periods, products/SKUs, brands, fact rows) are reported in Table 4.1 once regenerated.

| Category | Periods (max) | Brands total | retained ≥40 | retained ≥30 | SKUs (catalog) | brand-month rows |
|---|---|---|---|---|---|---|
| CSD | 42 | 136 | 57 | **77** | 2,080 | 3,789 |
| danskvand | 37 | 49 | 0 ⚠️ | **24** | 568 | 1,090 |
| energidrikke | 39 | 64 | 0 ⚠️ | **27** | 761 | 1,520 |
| RTD | 37 | 93 | 0 ⚠️ | **42** | 590 | 2,193 |

*Table 4.1. Per-category structure, all four categories computed locally under the DVH EXCL. HD scope (2026-06-23). CSD figures supersede Brian's all-markets values, inflated 6.16× by summing hierarchical markets.* **MIN_PERIODS feasibility**: danskvand, energidrikke, and RTD have only 37–39 monthly periods, so a ≥40-observation filter retains **zero** brands for them; a single global threshold of **≥30** is therefore adopted across all categories (CSD 77, danskvand 24, energidrikke 27, RTD 42 brands), which is both feasible and consistent — preferable to the inherited mixed rule (40 for CSD, 30 for the rest). The "bold" column (≥30) is the retained set used downstream. SKUs are catalog (dim_product) sizes; in-scope SKU counts to be added.

### 4.2.3 Overall Suitability

**Measurement validity / appropriateness.** The recorded metrics must measure the forecasting target. Sales units (and, where appropriate, litres) are the demand quantities to be forecast; the promotional variants and the weighted-distribution proxy serve as exogenous predictors. The weighted-distribution metric is an availability *proxy* rather than a direct census of shelf presence, and this proxy status is acknowledged in interpretation. **Market scope (resolved).** The primary market is **DVH EXCL. HD** (Danish grocery retail excluding hard discount), Nielsen's recommended default and the scope on which Manifold AI reports. This choice is not cosmetic: the 28 CSD market values form a hierarchy (individual chains nested within group aggregates such as COOP and SALLING GROUP, nested within grand-total roll-ups such as DVH/CONVENIENCE INCL. HD). A local check confirmed that aggregating sales across all 28 — as the inherited pipeline did — counts the same sales at multiple levels and inflates CSD volume by 6.16× (168.6B units summed across all 28 levels vs 27.4B units at the single DVH EXCL. HD level, a legitimate grand-total comparable to DVH/CONVENIENCE INCL. HD at 32.2B; all figures de-duplicated on the slowly-changing market dimension before aggregation). Scoping to the single `DVH EXCL. HD` market level eliminates this by construction (one market identifier, no cross-market summation) and yields a clean branded-demand signal excluding the structurally different hard-discount channel.

**Coverage.** The panel must cover the right population and period and leave sufficient data after exclusions. Coverage is assessed per category on: the number of retailers/markets; the temporal span (37–42 months, with complete intermediate calendar years constituting the primary training window); the number of brands and SKUs; and the count of fully observed brand × market series available for benchmarking after intermittent or short series are excluded. A category-specific coverage caveat applies to **promotional coverage**: for **danskvand** and **RTD** the promotional variables are effectively absent (promo-zero), so the promotional features are unmeasured for those categories, an unmeasured-variable limitation in Saunders' terms, carried forward to the modelling and discussion. Per-category coverage figures: `[regenerate]`.

### 4.2.4 Precise Suitability

**Reliability / dependability.** Nielsen is an established commercial panel provider whose continued operation depends on data credibility; its scanner data are therefore treated as reliable, while recognising that, as with any provider, definitions and collection conventions are fixed by Nielsen rather than by the researcher.

**Validity / credibility.** Credibility rests on how the data were collected and compiled (scanner capture aggregated to the market × product × period grain). Definitions (market aggregates such as DVH EXCL. HD, metric definitions, corporate attribution) are provider-set and are documented rather than altered.

**Measurement bias / trustworthiness.** Three data patterns require explicit treatment, with per-category figures to be regenerated:
- *Promotional nulls* `[regenerate null rate]`: interpreted as absence of promotional activity (the promotional columns are null for the same rows), imputed as zero; for danskvand and RTD this collapses to the promo-zero case above.
- *Weighted-distribution nulls* `[regenerate null rate]`: reflect products Nielsen does not track for distribution in a given period; imputed using a brand-and-market median, which preserves central tendency but ignores within-period time variation (a moderate limitation for niche brands).
- *Negative and zero values* `[regenerate counts]`: negatives are return/correction adjustments standard in scanner data and are clipped to zero; true zero-sales rows are retained and flagged as genuine zeros, distinct from corrections.
Core sales metrics are expected to be complete (zero nulls); this is re-verified per category in the rebuild.

### 4.2.5 Forecasting Suitability

The panel must support the forecasting models. The 37–42-month span exceeds the ARIMA minimum of roughly 24 periods for stable parameter identification and contains enough annual cycles for seasonality to be learned by both decomposition and gradient-boosted models. Benchmarking (Chapter 6) is conducted on the subset of **fully observed** brand series (at the chosen market scope), so that model comparisons are not confounded by differing series lengths; applicability to shorter or intermittent series is a bound on external validity, not a claim of this thesis. The count of fully observed series per category is `[regenerate]`.

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
- **Autocorrelation (recomputed, DVH EXCL. HD)**: for the top brand by units (HARBOE, n = 42) the log-series ACF is +0.26 (lag 1), +0.47 (lag 3), and ≈0 (lag 13) — a strong quarterly (lag-3) signal but a weak annual (lag-13) one for this brand. Lag structure is clearly brand-dependent, so a single global lag set is a simplification; per-brand optimisation is out of scope. This **revises** Brian's Coca-Cola example (lag-1 = −0.399), which was computed on the inflated all-markets series.
- **Promotional intensity**: strongly correlated with sales units in Brian's all-markets EDA (r = 0.941); to be re-confirmed under DVH EXCL. HD.

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

---

## 4.4 Feature Engineering (forecasting substrate)

The forecasting substrate uses features derived from the Nielsen facts table at the brand × month granularity. The audit confirms **14 modelling features** per observation (plus index, target, and split-label columns, for ≈20 columns total — exact count to confirm against the parquet). These are the exogenous predictors referenced in Chapter 1.

| Feature | Description | Models |
|---|---|---|
| `lag_1`, `lag_2`, `lag_3`, `lag_4`, `lag_8`, `lag_13` | Lagged `sales_units` (short, medium, seasonal) | LightGBM, XGBoost, Ridge |
| `rolling_mean_4`, `rolling_std_4` | 4-month rolling mean and standard deviation | LightGBM, XGBoost, Ridge |
| `rolling_mean_13` | Trailing annual average | LightGBM, XGBoost, Ridge |
| `month`, `quarter`, `holiday_month` | Calendar features (`holiday_month` = month in {3,6,12}) | All |
| `log_sales_units` | Natural log of `sales_units` (stationarity treatment) | LightGBM, XGBoost, Ridge |
| `promo_intensity` | Promotional share of units (clipped 0–1) | LightGBM, XGBoost, Ridge |

Index/target/label columns carried in the matrix: `brand`, `period_year`, `period_month`, `sales_units` (target), `split`. **To confirm**: `weighted_distribution` and raw `promo_sales_units` are present in the aggregated data but are *not* in the audit's confirmed 14-feature list — whether they are used as model inputs or only carried through needs parquet verification. Lag and rolling features carry NaN for short history (expected); no imputation is done in preprocessing, so models handle NaN themselves.

ARIMA and Prophet are fitted as univariate statistical baselines on the (log) sales series, not on the tabular feature matrix. The promotional feature is **not informative for danskvand and RTD** (promo-zero) and is handled accordingly for those categories.

---

## 4.5 Train, Validation, and Test Split

The split is defined by calendar date and locked as a pre-specified design decision, applied identically across the forecasting models and across categories. No random shuffling is applied: a strict temporal split preserves the autocorrelation structure and prevents leakage of future observations into training or validation.

Because the categories differ in length, the split is expressed as contiguous chronological blocks per category (training → validation → test), with the test window placed in the most recent months relevant to Manifold AI's planning horizon and covering at least one autumn/winter promotional cycle. The training window is required to satisfy the ARIMA minimum (~24 periods) and to contain at least two seasonal cycles for Prophet.

For **CSD** the boundaries are: **train 24 months** (Oct 2022 → Oct 2024), **validation 6 months** (Oct 2024 → Apr 2025), **test 12 months** (Apr 2025 → Mar 2026), over the 42-period window confirmed locally. The 24/6/12 proportions are forward-chaining. Per-category boundaries for danskvand/energidrikke/RTD: `[regenerate]`.

---

## 4.6 Key Risks and Mitigations

- **Provisional figures.** CSD figures are documented from the P0023 audit but not yet verified against local parquets (some drift across the handover docs, flagged "(to confirm)"); danskvand/energidrikke/RTD figures are still placeholders. Mitigation: figures are verified/filled from local data before the empirical chapters are finalised.
- **Market scope (resolved).** Confirmed locally that the inherited "All Markets" aggregation double-counts (6.16× inflation for CSD; 14–17× for the other three categories, which expose 86 market levels). Resolved by scoping all four categories to the single `DVH EXCL. HD` market level; feature matrices regenerated accordingly (2026-06-23) under DVH EXCL. HD + MIN_PERIODS=30.
- **Per-category EDA pending.** Only CSD has a dedicated EDA; danskvand/energidrikke/RTD currently run on CSD-derived parameter defaults (`MIN_PERIODS`, `LAGS`, `HOLIDAY_MONTHS`) without per-category validation. Mitigation: replicate the EDA per category (owned by the preprocessing pipeline) before treating their results as confirmed.
- **Empirical parameters.** `MIN_PERIODS`, `LAGS`, `ROLLING_WINDOWS`, and `HOLIDAY_MONTHS` are EDA-driven, not theory-first. Mitigation: justified post hoc in the modelling chapter and stated as a limitation.
- **Promotional coverage (danskvand, RTD).** Promo-zero categories lack the promotional signal (an unmeasured-variable limitation). Mitigation: promotional features are disabled for these categories and the limitation is stated in the discussion.
- **Weighted-distribution imputation.** Median imputation ignores within-period time variation (moderate risk for niche brands, low for high-coverage brands). Mitigation: documented; sensitivity noted.
- **Commercial access / confidentiality.** Raw data cannot be redistributed and must stay local; full external reproducibility is limited to processed features, code, and protocol.
- **Generalisability bound.** Findings are bounded to the DVH EXCL. HD scope, the available period window, and the fully observed series filter; applicability to other markets, intermittent series, or non-beverage categories is future research.

---

## References cited in this chapter

- Saunders, M. N. K., Lewis, P., & Thornhill, A. (2023). *Research Methods for Business Students* (9th ed.). Pearson.
