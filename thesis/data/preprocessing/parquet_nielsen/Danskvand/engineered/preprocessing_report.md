# Nielsen Danskvand Preprocessing Report
> Generated: 2026-05-09 11:53:10
> Category: Danskvand
> Market scope: DVH EXCL. HD
> Min periods filter: 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 24 |
| Total rows | 912 |
| Periods per brand | 38 |
| Features engineered | 18 |
| Peak RAM (preprocessing) | 6571.3 MB |
| Elapsed time | 205.8 s |

## Split Boundaries

| Split | Start | End | Periods |
|---|---|---|---|
| Train | 2023-03-01 | 2025-02-01 | 24 |
| Val | 2025-03-01 | 2025-08-01 | 6 |
| Test | 2025-09-01 | 2026-04-01 | 8 |

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
| HARBOE            |          38 |          38 |      6.40511e+07 |              24 |             6 |              8 |
| BLUE KELD         |          38 |          38 |      2.33721e+07 |              24 |             6 |              8 |
| FIRST PRICE       |          38 |          38 |      1.40836e+07 |              24 |             6 |              8 |
| AQUA D'OR         |          38 |          38 |      1.26705e+07 |              24 |             6 |              8 |
| KILDEVÆLD         |          38 |          38 |      7.45454e+06 |              24 |             6 |              8 |
| EGEKILDE          |          38 |          38 |      6.60664e+06 |              24 |             6 |              8 |
| RAMLOESA          |          38 |          38 |      5.84417e+06 |              24 |             6 |              8 |
| SAN PELLEGRINO    |          38 |          38 |      5.2091e+06  |              24 |             6 |              8 |
| OTHER BRAND       |          38 |          38 | 713316           |              24 |             6 |              8 |
| ACTIVE 02         |          38 |          38 | 586470           |              24 |             6 |              8 |
| HANCOCK           |          38 |          38 | 422478           |              24 |             6 |              8 |
| CARLSBERG KURVAND |          38 |          38 | 232646           |              24 |             6 |              8 |
| PERRIER           |          38 |          38 | 208513           |              24 |             6 |              8 |
| OK PLUS           |          38 |          37 | 149698           |              24 |             6 |              8 |
| KIRVI             |          38 |          38 | 123805           |              24 |             6 |              8 |
| EVIAN             |          38 |          38 |  77418.6         |              24 |             6 |              8 |
| FREM              |          38 |          38 |  70335.2         |              24 |             6 |              8 |
| DENICE            |          38 |          36 |  48856           |              24 |             6 |              8 |
| SAN BENEDETTO     |          38 |          38 |  26915.7         |              24 |             6 |              8 |
| SALTUM            |          38 |          38 |  26569.1         |              24 |             6 |              8 |
