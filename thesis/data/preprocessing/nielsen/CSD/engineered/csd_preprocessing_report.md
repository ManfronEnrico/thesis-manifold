# Nielsen CSD Preprocessing Report

**Generated:** 2026-05-12 16:07:55
**Category:** CSD
**Market Scope:** DVH EXCL. HD
**Min Periods Filter:** 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 78 |
| Total rows | 3,354 |
| Periods per brand | 43 |
| Features engineered | 17 |
| Peak RAM (preprocessing) | 84.6 MB |
| Elapsed time | 3.3 s |

## Split Boundaries

| Split | Start | End | Periods |
|---|---|---|---|
| Train | 2022-10-01 | 2025-02-01 | 29 |
| Val | 2025-03-01 | 2025-08-01 | 6 |
| Test | 2025-09-01 | 2026-04-01 | 8 |

## Engineered Features

- `sales_value`
- `sales_liters`
- `promo_units`
- `weighted_dist`
- `lag_1`
- `lag_2`
- `lag_3`
- `lag_4`
- `lag_8`
- `lag_13`
- `rolling_mean_4`
- `rolling_std_4`
- `rolling_mean_13`
- `month`
- `quarter`
- `holiday_month`
- `promo_intensity`

## Top 20 Brands by Total Sales Units

| brand             |   n_periods |   n_nonzero |   total_units |   train_periods |   val_periods |   test_periods |
|:------------------|------------:|------------:|--------------:|----------------:|--------------:|---------------:|
| HARBOE            |          43 |          43 |   2.13716e+08 |              29 |             6 |              8 |
| COCA COLA         |          43 |          43 |   2.03639e+08 |              29 |             6 |              8 |
| PEPSI             |          43 |          43 |   1.74064e+08 |              29 |             6 |              8 |
| FAXE KONDI        |          43 |          43 |   1.30886e+08 |              29 |             6 |              8 |
| FANTA             |          43 |          43 |   3.51162e+07 |              29 |             6 |              8 |
| JOLLY             |          43 |          43 |   1.96175e+07 |              29 |             6 |              8 |
| TUBORG SQUASH     |          43 |          43 |   1.75144e+07 |              29 |             6 |              8 |
| SCHWEPPES         |          43 |          43 |   1.41717e+07 |              29 |             6 |              8 |
| HANCOCK           |          43 |          43 |   9.95056e+06 |              29 |             6 |              8 |
| FEVER TREE        |          43 |          43 |   8.29369e+06 |              29 |             6 |              8 |
| SAN PELLEGRINO    |          43 |          43 |   8.25799e+06 |              29 |             6 |              8 |
| HARBOE OTHER      |          43 |          43 |   4.6822e+06  |              29 |             6 |              8 |
| EGO               |          43 |          43 |   3.85312e+06 |              29 |             6 |              8 |
| ULUDAG            |          43 |          43 |   3.06649e+06 |              29 |             6 |              8 |
| SPRITE            |          43 |          43 |   3.05884e+06 |              29 |             6 |              8 |
| CARIBIA           |          43 |          43 |   2.8992e+06  |              29 |             6 |              8 |
| THE PERFECT MIXER |          43 |          43 |   2.34147e+06 |              29 |             6 |              8 |
| FREM              |          43 |          43 |   2.34133e+06 |              29 |             6 |              8 |
| MIRINDA           |          43 |          43 |   1.80574e+06 |              29 |             6 |              8 |
| FRESH             |          43 |          31 |   1.54673e+06 |              29 |             6 |              8 |
