---
name: preprocessing-pipeline-diagram
description: REFERENCE - Visual pipeline diagram and data flow for Nielsen preprocessing
category: reference
applies-to: [preprocessing-continuation, system-a-integration]
triggers: [understand-pipeline, data-flow, architecture-overview]
created: 2026_06_22-16_30
updated: 2026_06_22-16_30
---

# Preprocessing Pipeline Architecture — Visual Diagram

## Data Flow: Nielsen → Feature Matrix → System A

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     NIELSEN PROMETHEUS SQL SERVER                            │
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │ csd_clean_facts_v    │  │ csd_clean_dim_*      │  │ 28 Retailers     │  │
│  │ (2.5M rows)          │  │ (product, period,    │  │ (market data)    │  │
│  │                      │  │  market)             │  │                  │  │
│  │ 42 months            │  │                      │  │ Dimensions only  │  │
│  │ 142 brands           │  │ Used in Step 0       │  │ (not in EDA)     │  │
│  │ Oct 2022–Mar 2026    │  │                      │  │                  │  │
│  └──────────────────────┘  └──────────────────────┘  └──────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Step 0: Cache
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                   PARQUET CACHE (converted/ folder)                          │
│                                                                              │
│  thesis/data/converted/nielsen/parquet_nielsen/CSD/views/                   │
│  ├── csd_clean_facts_v.parquet                                              │
│  ├── csd_clean_dim_product_v.parquet                                        │
│  ├── csd_clean_dim_period_v.parquet                                         │
│  └── csd_clean_dim_market_v.parquet                                         │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Step 1: Load & Aggregate
                                    │ (group by brand, year, month)
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                   AGGREGATED MONTHLY SERIES (In-Memory)                      │
│                                                                              │
│  Shape: 4,040 rows × 8 columns                                              │
│  (142 brands × 42 months = 4,040 observations)                              │
│                                                                              │
│  Columns:                                                                   │
│  ├── sales_units          (units sold per brand-month)                      │
│  ├── sales_value          (revenue per brand-month)                         │
│  ├── sales_liters         (volume per brand-month)                          │
│  ├── promo_units          (promotional units, r=0.941 with sales)          │
│  ├── weighted_dist        (4.3% missing — CONCERN)                         │
│  ├── brand_id, date, ... (keys)                                             │
│  └── dimension refs       (product, market — not used in EDA)               │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │ Step 2: Build Calendar         │
                    │ (Create date index, fill gaps) │
                    └───────────────┬────────────────┘
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│              TIME-INDEXED SERIES (Per-Brand Monthly Index)                   │
│                                                                              │
│  Shape per brand: 42 months (Oct 2022–Mar 2026)                             │
│  Index: DatetimeIndex (frequency='MS' — month start)                        │
│  Missing months filled (if any)                                             │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴────────────────────────┐
                    │ Step 3: Filter Series                  │
                    │ (Keep brands with ≥40 observations)    │
                    └───────────────┬────────────────────────┘
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                 FILTERED SERIES (Proof-of-Concept)                           │
│                                                                              │
│  CSD Result: 62 brands retained (from 142 total)                            │
│  Coverage: 43.7% of rows                                                    │
│  Rationale: Quality over breadth; all 62 brands have 40+ months             │
│                                                                              │
│  Each brand is now a separate time series:                                  │
│  ├── Brand 1: 42-month series                                               │
│  ├── Brand 2: 42-month series                                               │
│  └── ... (62 total)                                                         │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴─────────────────────────────────┐
                    │ Step 4: Engineer Features                        │
                    │ (Lag, rolling, seasonal, trend indicators)      │
                    └───────────────┬─────────────────────────────────┘
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      FEATURE ENGINEERING OUTPUTS                             │
│                                                                              │
│  Per-Brand Feature Matrix (Claimed 24 features):                            │
│  ├── Lag features: lags (1,2,3,4,8,13) of sales_units                      │
│  ├── Rolling statistics: 4-month and 13-month rolling mean/std              │
│  ├── Trend: linear regression slope per window                              │
│  ├── Seasonal indicators: Boolean flags for HOLIDAY_MONTHS = {3,6,12}       │
│  ├── Domain features: promo_units, weighted_dist (carried through)          │
│  └── [Other features — EXACT LIST NOT YET VERIFIED]                        │
│                                                                              │
│  ⚠️  CRITICAL: Are features log-transformed? Code audit needed.              │
│  ⚠️  CRITICAL: What are the 24 exactly? Feature list needed.                │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴────────────────────────────────┐
                    │ Step 5: Apply Train/Val/Test Split             │
                    │ (Forward-chaining, no look-ahead bias)         │
                    └───────────────┬────────────────────────────────┘
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                   SPLIT DATA (Temporal Partitioning)                        │
│                                                                              │
│ Total Timeline: Oct 2022 ─────────────────────────────────────── Mar 2026   │
│                                                                              │
│ ┌─────────────────────────┬──────────┬────────────────────────────────────┐ │
│ │   TRAIN (24 months)     │ VAL (6)  │        TEST (12 months)           │ │
│ │  Oct 2022 → Oct 2024    │ Oct 2024 │    Apr 2025 → Mar 2026           │ │
│ │       2 years           │ 6 months │         1 year                    │ │
│ └─────────────────────────┴──────────┴────────────────────────────────────┘ │
│                                                                              │
│ ✅ Forward-chaining: Each model trains on past, validates/tests on future   │
│ ⚠️  Note: Only 3–4 years total data (studies often use 5–10 years)         │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴────────────────────────────┐
                    │ Step 6: Save Outputs                       │
                    │ (Parquet + JSON + Markdown Report)         │
                    └───────────────┬────────────────────────────┘
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│              ENGINEERED OUTPUTS (thesis/data/preprocessing/...)              │
│                                                                              │
│  {category}/engineered/                                                     │
│  ├── {category}_feature_matrix.parquet         (62 brands × 43 months × 24) │
│  ├── {category}_series_index.csv               (brand lookups)              │
│  ├── {category}_split_dates.json               (train/val/test boundaries)  │
│  ├── {category}_preprocessing_report.md        (audit trail)                │
│  └── 8 × {category}_*_plot.png                 (DPI=150, thesis-ready)     │
│                                                                              │
│  CSD Example:                                                               │
│  ├── csd_feature_matrix.parquet                (~370 KB)                   │
│  ├── csd_series_index.csv                      (~2.4 KB)                   │
│  ├── csd_split_dates.json                      (~177 B)                    │
│  ├── csd_preprocessing_report.md                (~9 KB)                    │
│  └── csd_distribution_histogram.png, ...                                   │
└──────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴────────────────────┐
                    │ System A Integration               │
                    │ (Feed to forecasting models)       │
                    └───────────────┬────────────────────┘
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│           SYSTEM A FORECASTING PIPELINE (Next Phase)                         │
│                                                                              │
│  5 Forecasting Models:                                                      │
│  ├── Ridge Regression (baseline, interpretable)                             │
│  ├── ARIMA (statistical, parsimonious)                                      │
│  ├── Prophet (seasonal + trend decomposition)                               │
│  ├── LightGBM (expected best, expected MAPE ≤ 15%)                          │
│  └── XGBoost (ensemble alternative)                                         │
│                                                                              │
│  Evaluation:                                                                │
│  ├── MAPE (Mean Absolute Percentage Error) — target ≤ 15%                   │
│  ├── Per-brand performance across 62 brands                                 │
│  ├── Agentic vs. non-agentic comparison                                     │
│  └── RAM profiling (8 GB hard limit)                                        │
│                                                                              │
│  Output: Thesis Chapter 5 (System A Results & Evaluation)                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Preprocessing Parameters — Current Choices

| Parameter | Value | Category | Justification | Status |
|-----------|-------|----------|---|---|
| **Data source** | Nielsen CSD facts table | All | Thesis specified | ✅ Verified |
| **Aggregation level** | (brand, year, month) | All | Monthly demand typical for FMCG | ✅ Verified |
| **Time span** | Oct 2022 – Mar 2026 | All | Available Nielsen data | ✅ Verified |
| **MIN_PERIODS** | 40 observations | All | Proof-of-concept; 62 brands qualify | ⚠️ Empirical, not theoretical |
| **Log transform** | Applied to sales_units | All | ADF test shows p=0.028 (necessary) | ❓ **NEEDS VERIFICATION** |
| **LAGS** | (1,2,3,4,8,13) | All | Chosen empirically from COCA COLA autocorr | ⚠️ Per-brand variation not tested |
| **ROLLING_WINDOWS** | (4, 13) | All | 4-month + 13-month cycles | ⚠️ Empirical, not theory-justified |
| **HOLIDAY_MONTHS** | {3, 6, 12} | All | >75th percentile sales threshold | ⚠️ Empirical; promo vs seasonality unclear |
| **Train/Val/Test** | 24/6/12 months | All | 2yr train, 6mo val, 1yr test | ✅ Reasonable for monthly data |
| **Forecasting horizon** | Next month (h=1) | All | Problem specified | ✅ Standard |

---

## EDA Quality Checklist

### ✅ Completed (Thesis-Ready)
- [x] Data volume and time span verified
- [x] Stationarity testing (ADF test, log transform necessity proven)
- [x] Seasonal decomposition (peak months identified)
- [x] Autocorrelation analysis (top 5 brands, ACF/PACF plots)
- [x] Promotional intensity analysis (r=0.941 with sales_units)
- [x] Correlation heatmap (5 key features)
- [x] Visualizations (8 PNGs, thesis-quality)

### 🟡 Partial (Need Verification)
- [ ] Log transformation implementation in Step 4
- [ ] Feature engineering verification (24 features exact list)
- [ ] Missing value handling for weighted_dist (4.3%)
- [ ] Per-brand lag structure analysis (global LAGS optimal?)

### ❌ Deferred (Out of Scope)
- [ ] Per-category parameter tuning (CSD vs Danskvand vs RTD)
- [ ] Cross-category EDA comparison
- [ ] Promotional calendar vs. seasonality decomposition
- [ ] Structural break detection (42-month period)
- [ ] Outlier detection (univariate/multivariate)
- [ ] Regional variation (market-level effects)

---

## Category Status — All 4 Active Categories

| Category | Status | Notes |
|---|---|---|
| **CSD** | ✅ Complete (full EDA) | 62 brands, 4,040 rows; main focus |
| **Danskvand** | ✅ Working (parallel pipeline) | Parquet outputs exist; no detailed EDA |
| **Energidrikke** | ✅ Working (parallel pipeline) | Parquet outputs exist; no detailed EDA |
| **RTD** | ✅ Working (parallel pipeline) | Parquet outputs exist; no detailed EDA |
| **Totalbeer** | ❌ Skipped (intentional) | Dataset too large (RAM constraint); deferred to Phase 6 |

---

## Key Uncertainties for System A Integration

### Before Feeding to ML Models

1. **Stationarity verification**: Confirm sales_units are log-transformed before lag features
2. **Feature scaling**: Are features standardized? (Ridge & LightGBM often need it)
3. **Missing data**: How are 4.3% missing weighted_dist handled? (Mean imputation? Dropped?)
4. **Feature count**: Exactly which 24 features? Need interpretable feature importance
5. **Multicollinearity**: Are lag features (1,2,3,4 consecutive) problematic? (Likely, but handled by Ridge)
6. **Categorical features**: Brand_id as one-hot? Or separate models per brand?

### After Model Training

- MAPE ≤ 15% target (LightGBM expected best)
- Agentic vs non-agentic performance delta
- Per-brand variance (some brands easier to forecast than others?)
- Temporal performance (test set later months vs earlier months?)

---

## Reproducibility Checklist

- [ ] Random seeds set in preprocessing scripts
- [ ] Train/val/test split deterministic (verify by re-running)
- [ ] Feature engineering deterministic (verify parquet hashes match)
- [ ] EDA plots reproducible (same random state for sampling/plotting)

---

## Quick Reference — File Paths

```
thesis/data/preprocessing/nielsen/
├── CSD/
│   ├── preprocessing_csd.py                    (orchestrator)
│   ├── pre_csd_0_cache.py                      (load from SQL)
│   ├── pre_csd_1_load_and_aggregate.py         (aggregate facts)
│   ├── pre_csd_2_build_calendar.py             (create time index)
│   ├── pre_csd_3_filter_series.py              (MIN_PERIODS ≥ 40)
│   ├── pre_csd_4_engineer_features.py          (lag/rolling/seasonal) ⚠️
│   ├── pre_csd_5_apply_split.py                (train/val/test)
│   ├── pre_csd_6_save_outputs.py               (parquet + JSON)
│   ├── pre_csd_1.5_eda.py                      (EDA + visualizations)
│   └── engineered/
│       ├── csd_feature_matrix.parquet
│       ├── csd_series_index.csv
│       ├── csd_split_dates.json
│       ├── csd_preprocessing_report.md
│       └── 8 × csd_*.png
├── shared/
│   ├── base_preprocessing.py                   (BasePreprocessor class)
│   ├── timing_utils.py                         (speed profiling)
│   └── terminal_utils.py                       (pretty printing)
├── Danskvand/, Energidrikke/, RTD/            (parallel structure)
└── [Totalbeer/] (skipped)

thesis/data/converted/
└── nielsen/parquet_nielsen/CSD/views/          (parquet cache)
    ├── csd_clean_facts_v.parquet
    ├── csd_clean_dim_product_v.parquet
    ├── csd_clean_dim_period_v.parquet
    └── csd_clean_dim_market_v.parquet

plans/
└── 2026-06-22_15-00_preprocessing-pipeline-audit/
    ├── task_plan.md                            (phases + deliverables)
    ├── findings.md                             (verified discoveries)
    ├── progress.md                             (session log)
    ├── T001_preprocessing_script_inventory.md  (complete script map)
    ├── T002_data_integrity_checklist.md        (to-do verification)
    ├── ... (11 more task files)
    └── tasks/
        └── 1.json through 16.json              (task persistence)
```

---

**Last Updated**: 2026-06-22 16:30  
**For**: Enrico (System A Integration & Thesis Writing)  
**Next**: Verify Step 4 feature engineering, then thesis Chapter 4 writing
