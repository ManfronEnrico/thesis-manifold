# Nielsen CSD Preprocessing Report (bymonth)

**Generated:** 2026-07-13 13:03:25
**Category:** CSD
**Grain:** bymonth (group keys: brand)
**Market Scope:** All Market Types (aggregated across all 28 outlet channels)
**Min Periods Filter:** 40

---

## Executive Summary

| Metric | Value |
|---|---|
| Series in feature matrix | 58 |
| Total rows | 2,552 |
| Rows per series (avg) | 44 |
| Features engineered | 18 |
| Total pipeline time | 6.2s |

---

## Output Files

| Artifact | File | Description |
|---|---|---|
| Feature Matrix | `csd_feature_matrix.parquet` | Final feature matrix for modeling |
| Series Index | `csd_series_index.csv` | Series-level metadata with sales units |
| Split Dates | `csd_split_dates.json` | Train/val/test split date boundaries (JSON) |
| Report | `csd_preprocessing_report.md` | This preprocessing summary report |

**Location:** `Z:\_dev-ssd\thesis-manifold\02_thesis_data\_03_engineered\bymonth\CSD`

---

## Split Boundaries

| Split | Start | End | Rows |
|---|---|---|---|
| Train | 2022-10 | 2024-10-01 | 1,450 |
| Val | 2024-11-01 | 2025-04-01 | 348 |
| Test | 2025-05-01 | 2026-05 | 754 |

---

## Top 20 Series by Total Sales Units

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
- **weighted_distribution:** ~16.7% NULL in source data. Averaged during aggregation; NaN for missing series-months.
- **Engineered features:** NaN propagates where source is NaN. Lag/rolling operations do NOT forward-fill gaps.
- **log_sales_units:** NaN for non-positive or missing values (log-safe transformation).

### Filtering Criteria
- Only series with >=40 non-zero observations retained
- NaN pattern from earlier steps preserved through final matrix

### Train/Val/Test Notes
- Split based on **date, not random sampling** (time-series integrity required)

---

## Configuration & Parameters (CSD EDA-Driven)

| Parameter | Value |
|---|---|
| Grain | bymonth |
| Group Keys | brand |
| Market Scope | All Market Types (aggregated across 28 retail outlet channels) |
| Min Periods Filter | 40 |
| Lag Windows | 1, 2, 3, 4, 8, 13 months (autocorrelation-based) |
| Rolling Windows | 4-month, 13-month (Nielsen calendar + quarterly) |
| Holiday Months | 3 (Mar), 6 (Jun), 12 (Dec) — **Empirical CSD peaks** (not default {1,4,6,10,12}) |
| Split Method | Locked date-based (time-series) |

---

## Processing Summary

- **Total series processed:** 58
- **Total rows in final matrix:** 2,552
- **Features engineered:** 18
- **Pipeline execution time:** 6.2s
- **Generated:** 2026-07-13 13:03:25
