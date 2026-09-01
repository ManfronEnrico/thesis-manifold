<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 4 — Data Assessment
> Status: COMPLETE — ALL FIGURES RECOMPUTED LOCALLY (2026-06-27) — RQs v4 (four beverage categories; SRQ3 = integration readiness; Nielsen scanner panel only). The cleaned Nielsen parquets are local (`data/raw/nielsen_<cat>_clean_*.parquet`); structural figures, data-quality figures (null rates, negative/zero counts, in-scope SKU and series counts), and the detailed time-series EDA (ADF stationarity, ACF/PACF, seasonality, promo correlation) are computed directly from them under the DVH EXCL. HD market scope for all four categories. No `[regenerate]` placeholders remain. Awaiting human review only.
> Author: Claude Code — requires human review before finalisation
> Convention: all figures are local, recomputed under DVH EXCL. HD unless explicitly attributed to Brian's superseded all-markets audit.
> ✅ RESOLVED — MARKET SCOPE (verified locally, 2026-06-23): The 28 CSD market values are **hierarchical** (grand totals + group aggregates + individual chains). Brian's pipeline sums across all of them, which inflates CSD sales **6.16×** (168.6B units summed across all 28 levels vs 27.4B units at the single DVH EXCL. HD level; both figures de-duplicated on the slowly-changing market dimension). This thesis therefore scopes to the single market `market_description = "DVH EXCL. HD"` (Nielsen's recommended default; one `market_id`, no summing → double-counting impossible by construction). All CSD figures below are **recomputed locally under this scope** and supersede Brian's all-markets figures; they remain provisional only against Brian's final harmonised pipeline.

---

## 4.1 Overview and Data Strategy

---

## 4.2 The Nielsen Scanner Panel (core forecasting input)

### 4.2.1 Source, Type, and Access

### 4.2.2 Schema and Structure

| Category | Periods (max) | Brands (in scope) | retained ≥40 | retained ≥30 | Catalog SKUs | In-scope SKUs | Brand-month rows | In-scope fact rows |
|---|---|---|---|---|---|---|---|---|
| CSD | 42 | 136 | 57 | **77** | 8,608 | 7,668 | 3,789 | 187,907 |
| danskvand | 37 | 49 | 0 ⚠️ | **24** | 565 | 453 | 1,090 | 24,796 |
| energidrikke | 39 | 64 | 0 ⚠️ | **27** | 747 | 577 | 1,520 | 49,345 |
| RTD | 37 | 93 | 0 ⚠️ | **42** | 589 | 511 | 2,193 | 44,449 |

### 4.2.3 Overall Suitability

### 4.2.4 Precise Suitability

- *Promotional values*: where the promotional metric exists (CSD and energidrikke) it is fully populated (0.00% null), with the absence of promotional activity encoded as a zero rather than a null; for **danskvand** and **RTD** the promotional column is absent entirely, collapsing to the promo-zero case above.
- *Weighted-distribution nulls*: negligible across all categories — 0.019% (CSD), 0.016% (danskvand), 0.093% (energidrikke), 0.000% (RTD). These reflect products Nielsen does not track for distribution in a given period; they are imputed using a brand-and-market median, which preserves central tendency but ignores within-period time variation (a moderate limitation for niche brands, immaterial at these null rates).
- *Negative and zero values*: negatives are return/correction adjustments standard in scanner data and are clipped to zero — they are rare (CSD 58 rows, 0.031%; danskvand 14, 0.057%; energidrikke 16, 0.032%; RTD 10, 0.022%). True zero-sales rows are likewise rare (CSD 12, danskvand 1, energidrikke 28, RTD 17) and are retained and flagged as genuine zeros, distinct from corrections.

### 4.2.5 Forecasting Suitability

---

## 4.3 CSD — Worked Category (EDA and Parameters)

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
