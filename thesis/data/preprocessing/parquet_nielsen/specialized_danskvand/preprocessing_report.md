# Nielsen Danskvand Preprocessing Report
> Generated: 2026-05-01 20:28:20
> Category: Danskvand
> Market scope: DVH EXCL. HD
> Min periods filter: 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 24 |
| Total rows | 888 |
| Periods per brand | 37 |
| Features engineered | 18 |
| Peak RAM (preprocessing) | 310.8 MB |
| Elapsed time | 1.7 s |

## Split Boundaries

| Split | Start | End | Periods |
|---|---|---|---|
| Train | 2023-03-01 | 2025-02-01 | 24 |
| Val | 2025-03-01 | 2025-08-01 | 6 |
| Test | 2025-09-01 | 2026-03-01 | 7 |

## Feature List

- `sales_value`
- `sales_liters`
- `promo_units`
- `numeric_dist`
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

| brand             |   n_periods |   n_nonzero |      total_units |   train_periods |   val_periods |   test_periods |
|:------------------|------------:|------------:|-----------------:|----------------:|--------------:|---------------:|
| HARBOE            |          37 |          37 |      6.17638e+07 |              24 |             6 |              7 |
| BLUE KELD         |          37 |          37 |      2.29315e+07 |              24 |             6 |              7 |
| FIRST PRICE       |          37 |          37 |      1.37655e+07 |              24 |             6 |              7 |
| AQUA D'OR         |          37 |          37 |      1.24892e+07 |              24 |             6 |              7 |
| KILDEVÆLD         |          37 |          37 |      7.29082e+06 |              24 |             6 |              7 |
| EGEKILDE          |          37 |          37 |      6.45226e+06 |              24 |             6 |              7 |
| RAMLOESA          |          37 |          37 |      5.68806e+06 |              24 |             6 |              7 |
| SAN PELLEGRINO    |          37 |          37 |      5.10643e+06 |              24 |             6 |              7 |
| OTHER BRAND       |          37 |          37 | 652269           |              24 |             6 |              7 |
| ACTIVE 02         |          37 |          37 | 585528           |              24 |             6 |              7 |
| HANCOCK           |          37 |          37 | 410155           |              24 |             6 |              7 |
| CARLSBERG KURVAND |          37 |          37 | 229966           |              24 |             6 |              7 |
| PERRIER           |          37 |          37 | 204195           |              24 |             6 |              7 |
| OK PLUS           |          37 |          36 | 149512           |              24 |             6 |              7 |
| KIRVI             |          37 |          37 | 123239           |              24 |             6 |              7 |
| EVIAN             |          37 |          37 |  74025.6         |              24 |             6 |              7 |
| FREM              |          37 |          37 |  69116.2         |              24 |             6 |              7 |
| DENICE            |          37 |          35 |  48815           |              24 |             6 |              7 |
| SALTUM            |          37 |          37 |  26280           |              24 |             6 |              7 |
| SAN BENEDETTO     |          37 |          37 |  25520.7         |              24 |             6 |              7 |
