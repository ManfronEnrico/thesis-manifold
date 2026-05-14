# Nielsen Danskvand Preprocessing Report

**Generated:** 2026-05-14 16:54:04
**Category:** Danskvand
**Market Scope:** DVH EXCL. HD
**Min Periods Filter:** 30

---

## Executive Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 27 |
| Total rows | 1,134 |
| Rows per brand (avg) | 42 |
| Features engineered | 18 |
| Total pipeline time | 1.7s |

---

## Output Files

| Artifact | File | Description |
|---|---|---|
| Feature Matrix | `danskvand_feature_matrix.parquet` | Final feature matrix for modeling (brand Ã— period Ã— features Ã— split) |
| Series Index | `danskvand_series_index.csv` | Brand-level metadata with sales units |
| Split Dates | `danskvand_split_dates.json` | Train/val/test split date boundaries (JSON) |
| Report | `danskvand_preprocessing_report.md` | This preprocessing summary report |

**Location:** `/root/dev/thesis-manifold/thesis/data/preprocessing/nielsen/Danskvand/engineered`

---

## Pipeline Execution Details

### Step 1: Load and Aggregate
- **Input:** Nielsen view files (Facts, Product, Period, Market dimensions)
- **Output:** Brand Ã— period aggregation
- **Processing:** Loaded 4,040 rows, aggregated by brand and period
- **Output file:** `step_1_aggregate.parquet`

| Step | Input Cols | Output Cols | Elapsed (s) | Output Rows |
|---|---|---|---|---|
| Step 1 | â€” | 8 | 0.86s | 1,251 |

### Step 2: Build Calendar
- **Input:** Aggregated data (step 1)
- **Output:** Complete brand Ã— month index with NaN for missing periods
- **Date Range:** 2022-10 to 2026-03 (42 monthly periods)
- **Processing:** Created complete calendar grid for all brands
- **Output file:** `step_2_calendar_filled.parquet`
- **Columns:** 8 â†’ 8 | **Elapsed:** 0.16s | **Output rows:** 2,142

### Step 3: Filter Series
- **Input:** Calendar-filled data (step 2)
- **Output:** Filtered to brands with â‰¥30 non-zero periods
- **Processing:** Removed sparse series (insufficient historical observations)
- **Output file:** `step_3_filtered_series.parquet`
- **Columns:** 8 â†’ 8 | **Elapsed:** 0.13s | **Output rows:** 1,134

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
- **Columns:** 8 â†’ 23 | **Elapsed:** 0.14s | **Output rows:** 1,134

### Step 5: Apply Split
- **Input:** Engineered features (step 4)
- **Output:** Added train/val/test split labels
- **Split method:** Locked date-based (time-series integrity)
- **Processing:** Assigned split based on period_year-period_month
- **Output file:** `step_5_split_applied.parquet`
- **Columns:** 23 â†’ 24 | **Elapsed:** 0.10s | **Output rows:** 1,134

### Step 6: Save Outputs
- **Input:** Split-applied data (step 5)
- **Output:** Feature matrix, series index, split dates, report
- **Processing:** Generated final outputs and documentation
- **Output files:** `Danskvand_feature_matrix.parquet`, `Danskvand_series_index.csv`, `Danskvand_split_dates.json`
- **Columns:** 24 â†’ 24 | **Elapsed:** 0.35s | **Output rows:** 1,134

---

## Split Boundaries

| Split | Start | End | Period Range | Rows | Avg rows/brand |
|---|---|---|---|---|---|
| Train | 2022-10 | 2025-02-01 | â‰¤2025-02 | 783 | 29 |
| Val | 2025-03-01 | 2025-08-01 | 2025-03 to 2025-08 | 162 | 6 |
| Test | 2025-09-01 | 2026-03 | â‰¥2025-09 | 189 | 7 |

---

## Top 20 Brands by Total Sales Units

| brand             |   n_periods |   n_nonzero | total_units   |   train_periods |   val_periods |   test_periods |
|:------------------|------------:|------------:|:--------------|----------------:|--------------:|---------------:|
| HARBOE            |          42 |          37 | 863.6M        |              29 |             6 |              7 |
| BLUE KELD         |          42 |          37 | 312.9M        |              29 |             6 |              7 |
| AQUA D'OR         |          42 |          37 | 196.7M        |              29 |             6 |              7 |
| EGEKILDE          |          42 |          37 | 184.1M        |              29 |             6 |              7 |
| FIRST PRICE       |          42 |          37 | 177.6M        |              29 |             6 |              7 |
| RAMLOESA          |          42 |          37 | 125.3M        |              29 |             6 |              7 |
| KILDEVÆLD         |          42 |          37 | 121.9M        |              29 |             6 |              7 |
| SASKIA            |          42 |          37 | 102.0M        |              29 |             6 |              7 |
| SAN PELLEGRINO    |          42 |          37 | 78.4M         |              29 |             6 |              7 |
| CIRCLE K          |          42 |          37 | 41.5M         |              29 |             6 |              7 |
| ACTIVE 02         |          42 |          37 | 13.5M         |              29 |             6 |              7 |
| OTHER BRAND       |          42 |          37 | 10.2M         |              29 |             6 |              7 |
| DENICE            |          42 |          37 | 6.7M          |              29 |             6 |              7 |
| ACQUA PANNA       |          42 |          37 | 6.1M          |              29 |             6 |              7 |
| NEMLIG BASIC      |          42 |          37 | 6.0M          |              29 |             6 |              7 |
| HANCOCK           |          42 |          37 | 5.5M          |              29 |             6 |              7 |
| OK PLUS           |          42 |          37 | 4.1M          |              29 |             6 |              7 |
| CARLSBERG KURVAND |          42 |          37 | 3.0M          |              29 |             6 |              7 |
| PERRIER           |          42 |          37 | 2.9M          |              29 |             6 |              7 |
| KIRVI             |          42 |          37 | 1.6M          |              29 |             6 |              7 |

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

**Calendar Features (3):** `month` (1â€“12), `quarter` (1â€“4), `holiday_month` (binary)

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
- Only brands with â‰¥30 non-zero observations retained
- All brands have complete calendar coverage (2022-10 to 2026-03)
- NaN pattern from earlier steps preserved through final matrix

### Train/Val/Test Notes
- Split based on **date, not random sampling** (time-series integrity required)
- Locked boundaries per research design:
  - Train: period â‰¤ 2025-02
  - Val: 2025-03 â‰¤ period â‰¤ 2025-08
  - Test: period â‰¥ 2025-09

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

- **Total brands processed:** 27
- **Total rows in final matrix:** 1,134
- **Features engineered:** 18
- **Pipeline execution time:** 1.7s
- **Generated:** 2026-05-14 16:54:04
