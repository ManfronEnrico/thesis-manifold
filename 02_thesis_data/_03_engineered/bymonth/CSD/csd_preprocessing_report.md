# Nielsen CSD Preprocessing Report

**Generated:** 2026-07-12 19:34:19
**Category:** CSD
**Market Scope:** All Market Types (aggregated across all 28 outlet channels)
**Min Periods Filter:** 40 (Thesis Quality Focus - 62 brands)

---

## Executive Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 58 |
| Total rows | 2,552 |
| Rows per brand (avg) | 44 |
| Features engineered | 18 |
| Total pipeline time | 10.5s |

---

## Output Files

| Artifact | File | Description |
|---|---|---|
| Feature Matrix | `csd_feature_matrix.parquet` | Final feature matrix for modeling (brand × period × features × split) |
| Series Index | `csd_series_index.csv` | Brand-level metadata with sales units |
| Split Dates | `csd_split_dates.json` | Train/val/test split date boundaries (JSON) |
| Report | `csd_preprocessing_report.md` | This preprocessing summary report |

**Location:** `Z:\_dev-ssd\thesis-manifold\02_thesis_data\_03_engineered\bymonth\CSD`

---

## Pipeline Execution Details

### Step 1: Load and Aggregate
- **Input:** Nielsen view files (Facts, Product, Period, Market dimensions)
- **Output:** Brand × period aggregation
- **Processing:** Loaded 4,040 rows, aggregated by brand and period
- **Output file:** `step_1_aggregate.parquet`

| Step | Input Cols | Output Cols | Elapsed (s) | Output Rows |
|---|---|---|---|---|
| Step 1 | — | 10 | 9.60s | 27,086 |

### Step 2: Build Calendar
- **Input:** Aggregated data (step 1)
- **Output:** Complete brand × month index with NaN for missing periods
- **Date Range:** 2022-10 to 2026-03 (42 monthly periods)
- **Processing:** Created complete calendar grid for all brands
- **Output file:** `step_2_calendar_filled.parquet`
- **Columns:** 8 → 8 | **Elapsed:** 0.16s | **Output rows:** 6,160

### Step 3: Filter Series
- **Input:** Calendar-filled data (step 2)
- **Output:** Filtered to brands with ≥40 non-zero periods
- **Processing:** Removed sparse series (insufficient historical observations)
- **Output file:** `step_3_filtered_series.parquet`
- **Columns:** 8 → 8 | **Elapsed:** 0.08s | **Output rows:** 2,552

### Step 4: Engineer Features
- **Input:** Filtered series (step 3)
- **Output:** Features + lag/rolling/calendar features + log transformation
- **Features added:** 10 new columns
- **Processing:**
  - Lags: 1, 2, 3, 4, 8, 13 months
  - Rolling: mean (4, 13-month windows), std (4-month window)
  - Calendar: month, quarter, holiday_month (Jan/Apr/Jun/Oct/Dec)
  - Transformation: log(sales_units) with NaN preservation
- **Output file:** `step_4_engineered_features.parquet`
- **Columns:** 8 → 23 | **Elapsed:** 0.12s | **Output rows:** 2,552

### Step 5: Apply Split
- **Input:** Engineered features (step 4)
- **Output:** Added train/val/test split labels
- **Split method:** Locked date-based (time-series integrity)
- **Processing:** Assigned split based on period_year-period_month
- **Output file:** `step_5_split_applied.parquet`
- **Columns:** 23 → 24 | **Elapsed:** 0.12s | **Output rows:** 2,552

### Step 6: Save Outputs
- **Input:** Split-applied data (step 5)
- **Output:** Feature matrix, series index, split dates, report
- **Processing:** Generated final outputs and documentation
- **Output files:** `csd_feature_matrix.parquet`, `csd_series_index.csv`, `csd_split_dates.json`
- **Columns:** 26 → 26 | **Elapsed:** 0.38s | **Output rows:** 25,124

---

## Split Boundaries

| Split | Start | End | Period Range | Rows | Avg rows/brand |
|---|---|---|---|---|---|
| Train | 2022-10 | 2024-10-01 | ≤2025-02 | 1,450 | 25 |
| Val | 2024-11-01 | 2025-04-01 | 2025-03 to 2025-08 | 348 | 6 |
| Test | 2025-05-01 | 2026-05 | ≥2025-09 | 754 | 13 |

---

## Top 20 Brands by Total Sales Units

| brand             |   n_periods |   n_nonzero | total_units   |   train_periods |   val_periods |   test_periods |
|:------------------|------------:|------------:|:--------------|----------------:|--------------:|---------------:|
| HARBOE            |          44 |          44 | 203.1M        |              25 |             6 |             13 |
| COCA COLA         |          44 |          44 | 194.8M        |              25 |             6 |             13 |
| PEPSI             |          44 |          44 | 166.0M        |              25 |             6 |             13 |
| FAXE KONDI        |          44 |          44 | 125.2M        |              25 |             6 |             13 |
| FANTA             |          44 |          44 | 33.3M         |              25 |             6 |             13 |
| JOLLY             |          44 |          44 | 18.2M         |              25 |             6 |             13 |
| TUBORG SQUASH     |          44 |          44 | 16.7M         |              25 |             6 |             13 |
| SCHWEPPES         |          44 |          44 | 13.4M         |              25 |             6 |             13 |
| HANCOCK           |          44 |          44 | 9.5M          |              25 |             6 |             13 |
| FEVER TREE        |          44 |          44 | 7.8M          |              25 |             6 |             13 |
| SAN PELLEGRINO    |          44 |          44 | 7.8M          |              25 |             6 |             13 |
| HARBOE OTHER      |          44 |          44 | 4.2M          |              25 |             6 |             13 |
| EGO               |          44 |          44 | 3.6M          |              25 |             6 |             13 |
| SPRITE            |          44 |          44 | 2.9M          |              25 |             6 |             13 |
| ULUDAG            |          44 |          44 | 2.9M          |              25 |             6 |             13 |
| CARIBIA           |          44 |          44 | 2.7M          |              25 |             6 |             13 |
| FREM              |          44 |          44 | 2.2M          |              25 |             6 |             13 |
| THE PERFECT MIXER |          44 |          44 | 2.2M          |              25 |             6 |             13 |
| MIRINDA           |          44 |          44 | 1.7M          |              25 |             6 |             13 |
| 7-UP              |          44 |          44 | 1.4M          |              25 |             6 |             13 |

---

## Feature Engineering Summary

### Column Evolution

| Stage | Count | Columns |
|---|---|---|
| Step 1 (Aggregation) | 8 | brand, period_year, period_month, sales_units, sales_value, sales_liters, promo_units, weighted_dist |
| Step 2-3 (Calendar & Filter) | 8 | _(same as Step 1)_ |
| Step 4 (Feature Engineering) | 23 | _(+15 new features: lags, rolling, calendar, log_sales_units)_ |
| Step 5 (Split) | 24 | _(+1 split column)_ |

### Engineered Features

**Lag Features (6):** `lag_1`, `lag_2`, `lag_3`, `lag_4`, `lag_8`, `lag_13`

**Rolling Features (3):** `rolling_mean_4`, `rolling_mean_13`, `rolling_std_4`

**Calendar Features (3):** `month` (1–12), `quarter` (1–4), `holiday_month` (binary)

**Transformations (1):** `log_sales_units` (ln of sales_units, NaN-safe)

**All Engineered Columns:**
- `date`
- `holiday_month`
- `lag_1`
- `lag_13`
- `lag_2`
- `lag_3`
- `lag_4`
- `lag_8`
- `month`
- `promo_intensity`
- `promo_units`
- `quarter`
- `rolling_mean_13`
- `rolling_mean_4`
- `rolling_std_4`
- `sales_liters`
- `sales_value`
- `weighted_dist`

---

## Data Quality Notes

### Null Handling
- **sales_units:** NaN in calendar-filled step indicates zero or missing observation. Preserved for downstream time-series modeling (NOT imputed).
- **weighted_distribution:** ~16.7% NULL in source data. Averaged during aggregation; NaN for missing brand-months.
- **Engineered features:** NaN propagates where source is NaN. Lag/rolling operations do NOT forward-fill gaps.
- **log_sales_units:** NaN for non-positive or missing values (log-safe transformation).

### Filtering Criteria
- Only brands with ≥40 non-zero observations retained
- All brands have complete calendar coverage (2022-10 to 2026-03)
- NaN pattern from earlier steps preserved through final matrix

### Train/Val/Test Notes
- Split based on **date, not random sampling** (time-series integrity required)
- Locked boundaries per research design:
  - Train: period ≤ 2025-02
  - Val: 2025-03 ≤ period ≤ 2025-08
  - Test: period ≥ 2025-09

---

## Configuration & Parameters (CSD EDA-Driven)

| Parameter | Value |
|---|---|
| Market Scope | All Market Types (aggregated across 28 retail outlet channels) |
| Min Periods Filter | 40 non-zero observations per brand (thesis quality focus) |
| Calendar Range | 2022-10 to 2026-04 (43 monthly periods) |
| Lag Windows | 1, 2, 3, 4, 8, 13 months (autocorrelation-based) |
| Rolling Windows | 4-month, 13-month (Nielsen calendar + quarterly) |
| Holiday Months | 3 (Mar), 6 (Jun), 12 (Dec) — **Empirical CSD peaks** (not default (1, 4, 6, 10, 12)) |
| Split Method | Locked date-based (time-series) |
| Train End | 2025-02 |
| Val End | 2025-08 |

---

## Processing Summary

- **Total brands processed:** 58
- **Total rows in final matrix:** 2,552
- **Features engineered:** 18
- **Pipeline execution time:** 10.5s
- **Generated:** 2026-07-12 19:34:20
