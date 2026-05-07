# Nielsen CSD Preprocessing Report

**Generated:** 2026-05-07 12:45:19
**Category:** CSD
**Market Scope:** DVH EXCL. HD
**Min Periods Filter:** 30

---

## Executive Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 84 |
| Total rows | 3,528 |
| Rows per brand (avg) | 42 |
| Features engineered | 18 |
| Total pipeline time | 1.4s |

---

## Output Files

| Artifact | File | Description |
|---|---|---|
| Feature Matrix | `csd_feature_matrix.parquet` | Final feature matrix for modeling (brand × period × features × split) |
| Series Index | `csd_series_index.csv` | Brand-level metadata with sales units |
| Split Dates | `csd_split_dates.json` | Train/val/test split date boundaries (JSON) |
| Report | `csd_preprocessing_report.md` | This preprocessing summary report |

**Location:** `Z:\.dev-ssd\thesis-manifold\thesis\data\preprocessing\nielsen\CSD\engineered`

---

## Pipeline Execution Details

### Step 1: Load and Aggregate
- **Input:** Nielsen view files (Facts, Product, Period, Market dimensions)
- **Output:** Brand × period aggregation
- **Processing:** Loaded 4,040 rows, aggregated by brand and period
- **Output file:** `step_1_aggregate.parquet`

| Step | Input Cols | Output Cols | Elapsed (s) | Output Rows |
|---|---|---|---|---|
| Step 1 | — | 8 | 0.81s | 4,040 |

### Step 2: Build Calendar
- **Input:** Aggregated data (step 1)
- **Output:** Complete brand × month index with NaN for missing periods
- **Date Range:** 2022-10 to 2026-03 (42 monthly periods)
- **Processing:** Created complete calendar grid for all brands
- **Output file:** `step_2_calendar_filled.parquet`
- **Columns:** 8 → 8 | **Elapsed:** 0.10s | **Output rows:** 5,964

### Step 3: Filter Series
- **Input:** Calendar-filled data (step 2)
- **Output:** Filtered to brands with ≥30 non-zero periods
- **Processing:** Removed sparse series (insufficient historical observations)
- **Output file:** `step_3_filtered_series.parquet`
- **Columns:** 8 → 8 | **Elapsed:** 0.07s | **Output rows:** 3,528

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
- **Columns:** 8 → 23 | **Elapsed:** 0.09s | **Output rows:** 3,528

### Step 5: Apply Split
- **Input:** Engineered features (step 4)
- **Output:** Added train/val/test split labels
- **Split method:** Locked date-based (time-series integrity)
- **Processing:** Assigned split based on period_year-period_month
- **Output file:** `step_5_split_applied.parquet`
- **Columns:** 23 → 24 | **Elapsed:** 0.08s | **Output rows:** 3,528

### Step 6: Save Outputs
- **Input:** Split-applied data (step 5)
- **Output:** Feature matrix, series index, split dates, report
- **Processing:** Generated final outputs and documentation
- **Output files:** `csd_feature_matrix.parquet`, `csd_series_index.csv`, `csd_split_dates.json`
- **Columns:** — → — | **Elapsed:** 0.26s | **Output rows:** 3,528

---

## Split Boundaries

| Split | Start | End | Period Range | Rows | Avg rows/brand |
|---|---|---|---|---|---|
| Train | 2022-10 | 2025-02-01 | ≤2025-02 | 2,436 | 29 |
| Val | 2025-03-01 | 2025-08-01 | 2025-03 to 2025-08 | 504 | 6 |
| Test | 2025-09-01 | 2026-03 | ≥2025-09 | 588 | 7 |

---

## Top 20 Brands by Total Sales Units

| brand             |   n_periods |   n_nonzero | total_units   |   train_periods |   val_periods |   test_periods |
|:------------------|------------:|------------:|:--------------|----------------:|--------------:|---------------:|
| COCA COLA         |          42 |          42 | 1291.3M       |              29 |             6 |              7 |
| HARBOE            |          42 |          42 | 1129.7M       |              29 |             6 |              7 |
| PEPSI             |          42 |          42 | 1058.4M       |              29 |             6 |              7 |
| FAXE KONDI        |          42 |          42 | 813.9M        |              29 |             6 |              7 |
| FANTA             |          42 |          42 | 212.3M        |              29 |             6 |              7 |
| JOLLY             |          42 |          42 | 115.9M        |              29 |             6 |              7 |
| TUBORG SQUASH     |          42 |          42 | 113.4M        |              29 |             6 |              7 |
| SCHWEPPES         |          42 |          42 | 84.7M         |              29 |             6 |              7 |
| LIDL FREEWAY      |          42 |          42 | 69.9M         |              29 |             6 |              7 |
| HANCOCK           |          42 |          42 | 55.0M         |              29 |             6 |              7 |
| SAN PELLEGRINO    |          42 |          42 | 49.8M         |              29 |             6 |              7 |
| FEVER TREE        |          42 |          42 | 47.8M         |              29 |             6 |              7 |
| ULUDAG            |          42 |          42 | 30.0M         |              29 |             6 |              7 |
| HARBOE OTHER      |          42 |          42 | 27.6M         |              29 |             6 |              7 |
| EGO               |          42 |          42 | 21.6M         |              29 |             6 |              7 |
| SPRITE            |          42 |          42 | 19.4M         |              29 |             6 |              7 |
| CARIBIA           |          42 |          42 | 14.8M         |              29 |             6 |              7 |
| FREM              |          42 |          42 | 13.5M         |              29 |             6 |              7 |
| THE PERFECT MIXER |          42 |          42 | 12.8M         |              29 |             6 |              7 |
| MOUNTAIN DEW.     |          42 |          42 | 10.8M         |              29 |             6 |              7 |

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
- Only brands with ≥30 non-zero observations retained
- All brands have complete calendar coverage (2022-10 to 2026-03)
- NaN pattern from earlier steps preserved through final matrix

### Train/Val/Test Notes
- Split based on **date, not random sampling** (time-series integrity required)
- Locked boundaries per research design:
  - Train: period ≤ 2025-02
  - Val: 2025-03 ≤ period ≤ 2025-08
  - Test: period ≥ 2025-09

---

## Configuration & Parameters

| Parameter | Value |
|---|---|
| Target Market | DVH EXCL. HD |
| Min Periods Filter | 30 non-zero observations per brand |
| Calendar Range | 2022-10 to 2026-03 (42 monthly periods) |
| Lag Windows | 1, 2, 3, 4, 8, 13 months |
| Rolling Windows | 4-month, 13-month |
| Holiday Months | 1 (Jan), 4 (Apr), 6 (Jun), 10 (Oct), 12 (Dec) |
| Split Method | Locked date-based (time-series) |
| Train End | 2025-02 |
| Val End | 2025-08 |

---

## Processing Summary

- **Total brands processed:** 84
- **Total rows in final matrix:** 3,528
- **Features engineered:** 18
- **Pipeline execution time:** 1.4s
- **Generated:** 2026-05-07 12:45:19
