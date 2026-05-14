# Nielsen Energidrikke Preprocessing Report

**Generated:** 2026-05-14 16:48:58
**Category:** Energidrikke
**Market Scope:** DVH EXCL. HD
**Min Periods Filter:** 30

---

## Executive Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 31 |
| Total rows | 1,302 |
| Rows per brand (avg) | 42 |
| Features engineered | 18 |
| Total pipeline time | 3.7s |

---

## Output Files

| Artifact | File | Description |
|---|---|---|
| Feature Matrix | `energidrikke_feature_matrix.parquet` | Final feature matrix for modeling (brand × period × features × split) |
| Series Index | `energidrikke_series_index.csv` | Brand-level metadata with sales units |
| Split Dates | `energidrikke_split_dates.json` | Train/val/test split date boundaries (JSON) |
| Report | `energidrikke_preprocessing_report.md` | This preprocessing summary report |

**Location:** `/root/dev/thesis-manifold/thesis/data/preprocessing/nielsen/Energidrikke/engineered`

---

## Pipeline Execution Details

### Step 1: Load and Aggregate
- **Input:** Nielsen view files (Facts, Product, Period, Market dimensions)
- **Output:** Brand × period aggregation
- **Processing:** Loaded 4,040 rows, aggregated by brand and period
- **Output file:** `step_1_aggregate.parquet`

| Step | Input Cols | Output Cols | Elapsed (s) | Output Rows |
|---|---|---|---|---|
| Step 1 | — | 8 | 3.05s | 1,728 |

### Step 2: Build Calendar
- **Input:** Aggregated data (step 1)
- **Output:** Complete brand × month index with NaN for missing periods
- **Date Range:** 2022-10 to 2026-03 (42 monthly periods)
- **Processing:** Created complete calendar grid for all brands
- **Output file:** `step_2_calendar_filled.parquet`
- **Columns:** 8 → 8 | **Elapsed:** 0.12s | **Output rows:** 2,982

### Step 3: Filter Series
- **Input:** Calendar-filled data (step 2)
- **Output:** Filtered to brands with ≥30 non-zero periods
- **Processing:** Removed sparse series (insufficient historical observations)
- **Output file:** `step_3_filtered_series.parquet`
- **Columns:** 8 → 8 | **Elapsed:** 0.09s | **Output rows:** 1,302

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
- **Columns:** 8 → 23 | **Elapsed:** 0.10s | **Output rows:** 1,302

### Step 5: Apply Split
- **Input:** Engineered features (step 4)
- **Output:** Added train/val/test split labels
- **Split method:** Locked date-based (time-series integrity)
- **Processing:** Assigned split based on period_year-period_month
- **Output file:** `step_5_split_applied.parquet`
- **Columns:** 23 → 24 | **Elapsed:** 0.07s | **Output rows:** 1,302

### Step 6: Save Outputs
- **Input:** Split-applied data (step 5)
- **Output:** Feature matrix, series index, split dates, report
- **Processing:** Generated final outputs and documentation
- **Output files:** `energidrikke_feature_matrix.parquet`, `energidrikke_series_index.csv`, `energidrikke_split_dates.json`
- **Columns:** 24 → 24 | **Elapsed:** 0.29s | **Output rows:** 1,302

---

## Split Boundaries

| Split | Start | End | Period Range | Rows | Avg rows/brand |
|---|---|---|---|---|---|
| Train | 2022-10 | 2025-02-01 | ≤2025-02 | 899 | 29 |
| Val | 2025-03-01 | 2025-08-01 | 2025-03 to 2025-08 | 186 | 6 |
| Test | 2025-09-01 | 2026-03 | ≥2025-09 | 217 | 7 |

---

## Top 20 Brands by Total Sales Units

| brand              |   n_periods |   n_nonzero | total_units   |   train_periods |   val_periods |   test_periods |
|:-------------------|------------:|------------:|:--------------|----------------:|--------------:|---------------:|
| RED BULL           |          42 |          39 | 1502.7M       |              29 |             6 |              7 |
| MONSTER ENERGY     |          42 |          39 | 1390.2M       |              29 |             6 |              7 |
| FAXE KONDI BOOSTER |          42 |          39 | 1299.8M       |              29 |             6 |              7 |
| CULT               |          42 |          39 | 181.9M        |              29 |             6 |              7 |
| STATE              |          42 |          39 | 165.7M        |              29 |             6 |              7 |
| VITAMIN WELL       |          42 |          39 | 164.4M        |              29 |             6 |              7 |
| X-RAY              |          42 |          39 | 125.8M        |              29 |             6 |              7 |
| POWERADE           |          42 |          39 | 89.6M         |              29 |             6 |              7 |
| PRIME              |          42 |          35 | 62.1M         |              29 |             6 |              7 |
| KONG STRONG        |          42 |          39 | 47.1M         |              29 |             6 |              7 |
| ROCKSTAR           |          42 |          39 | 36.1M         |              29 |             6 |              7 |
| NOCCO              |          42 |          39 | 34.8M         |              29 |             6 |              7 |
| STATE VITAMIN      |          42 |          39 | 14.1M         |              29 |             6 |              7 |
| LIDL FREEWAY       |          42 |          39 | 11.7M         |              29 |             6 |              7 |
| SMAG               |          42 |          39 | 10.9M         |              29 |             6 |              7 |
| GATORADE           |          42 |          39 | 10.8M         |              29 |             6 |              7 |
| POWERKING          |          42 |          39 | 9.6M          |              29 |             6 |              7 |
| AQUA D'OR          |          42 |          31 | 7.4M          |              29 |             6 |              7 |
| LINUSPRO           |          42 |          30 | 7.1M          |              29 |             6 |              7 |
| 4MOVE              |          42 |          39 | 5.8M          |              29 |             6 |              7 |

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

- **Total brands processed:** 31
- **Total rows in final matrix:** 1,302
- **Features engineered:** 18
- **Pipeline execution time:** 3.7s
- **Generated:** 2026-05-14 16:48:58
