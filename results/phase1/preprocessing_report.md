# Nielsen Preprocessing Report
> Generated: 2026-04-13
> Market scope: DVH EXCL. HD
> Min periods filter: 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 77 |
| Total rows | 3,234 |
| Periods per brand | 42 |
| Features engineered | 17 |
| Peak RAM (preprocessing) | 8.0 MB |
| Elapsed time | 11.6 s |

## Split Boundaries

| Split | Start | End | Periods |
|---|---|---|---|
| Train | 2022-10-01 | 2025-02-01 | 29 |
| Val | 2025-03-01 | 2025-08-01 | 6 |
| Test | 2025-09-01 | 2026-03-01 | 7 |

## Feature List

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
| HARBOE            |          42 |          42 |   2.08436e+08 |              29 |             6 |              7 |
| COCA COLA         |          42 |          42 |   1.99549e+08 |              29 |             6 |              7 |
| PEPSI             |          42 |          42 |   1.70583e+08 |              29 |             6 |              7 |
| FAXE KONDI        |          42 |          42 |   1.28057e+08 |              29 |             6 |              7 |
| FANTA             |          42 |          42 |   3.42968e+07 |              29 |             6 |              7 |
| JOLLY             |          42 |          42 |   1.92736e+07 |              29 |             6 |              7 |
| TUBORG SQUASH     |          42 |          42 |   1.70469e+07 |              29 |             6 |              7 |
| SCHWEPPES         |          42 |          42 |   1.39655e+07 |              29 |             6 |              7 |
| HANCOCK           |          42 |          42 |   9.68664e+06 |              29 |             6 |              7 |
| FEVER TREE        |          42 |          42 |   8.13824e+06 |              29 |             6 |              7 |
| SAN PELLEGRINO    |          42 |          42 |   8.07717e+06 |              29 |             6 |              7 |
| HARBOE OTHER      |          42 |          42 |   4.60843e+06 |              29 |             6 |              7 |
| EGO               |          42 |          42 |   3.74373e+06 |              29 |             6 |              7 |
| ULUDAG            |          42 |          42 |   3.03555e+06 |              29 |             6 |              7 |
| SPRITE            |          42 |          42 |   2.99003e+06 |              29 |             6 |              7 |
| CARIBIA           |          42 |          42 |   2.82e+06    |              29 |             6 |              7 |
| THE PERFECT MIXER |          42 |          42 |   2.34077e+06 |              29 |             6 |              7 |
| FREM              |          42 |          42 |   2.30141e+06 |              29 |             6 |              7 |
| MIRINDA           |          42 |          42 |   1.78967e+06 |              29 |             6 |              7 |
| FRESH             |          42 |          30 |   1.51854e+06 |              29 |             6 |              7 |
