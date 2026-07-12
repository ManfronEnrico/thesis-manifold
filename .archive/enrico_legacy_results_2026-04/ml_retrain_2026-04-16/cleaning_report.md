# Step 02 — Data Cleaning Report
_Generated 2026-04-16T19:05:26_

## 1. Baseline feature matrix — audit

- Rows: 3,234
- Cols: 22
- Brands: 77
- Date range: 2022-10-01 00:00:00 → 2026-03-01 00:00:00
- Duplicate (brand, date) keys: 0
- sales_units < 0: 0
- sales_units == 0: 157
- Missing per column:
  - lag_1: 77
  - lag_2: 154
  - lag_3: 231
  - lag_4: 308
  - lag_8: 616
  - lag_13: 1001
  - rolling_mean_4: 2
  - rolling_mean_13: 4

## 2. Nielsen CSD facts — cleaning rules applied

| Rule | Removed | Remaining |
|---|---:|---:|
| drop_exact_duplicates | 0 | 2,535,464 |
| drop_negative_sales | 862 | 2,534,602 |

Final: **2,534,602 rows** → `data/clean/nielsen_csd_clean.parquet`

## 3. Indeks data — dimensionality reduction

- Before: 20,134 rows × **6364** cols
- Dropped cols with >95% missing: **45**
- Dropped zero-variance cols: **2**
- After: 20,134 rows × **6317** cols
- Output: `data/clean/indeks_data_clean.parquet`

## Methodology note for thesis

Cleaning is conservative: we only remove rows/columns that are logically invalid (negative sales, exact duplicates) or uninformative (zero variance, >95% missing). We do NOT impute missing values at this stage — imputation decisions are deferred to Step 06 (preprocessing pipeline) so each model can choose its own strategy.