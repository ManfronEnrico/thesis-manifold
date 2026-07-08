# Nielsen RTD Preprocessing Report
> Generated: 2026-05-14 13:32:21
> Category: RTD
> Market scope: DVH EXCL. HD
> Min periods filter: 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 42 |
| Total rows | 1,596 |
| Periods per brand | 38 |
| Features engineered | 18 |
| Peak RAM (preprocessing) | 159.5 MB |
| Elapsed time | 2.5 s |

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

| brand                |   n_periods |   n_nonzero |      total_units |   train_periods |   val_periods |   test_periods |
|:---------------------|------------:|------------:|-----------------:|----------------:|--------------:|---------------:|
| BREEZER              |          38 |          38 |      3.29698e+07 |              24 |             6 |              8 |
| SHAKER               |          38 |          38 |      2.41385e+07 |              24 |             6 |              8 |
| SMIRNOFF ICE/TWISTED |          38 |          38 |      2.24508e+07 |              24 |             6 |              8 |
| SOMERSBY             |          38 |          38 |      9.33666e+06 |              24 |             6 |              8 |
| MOKAÏ                |          38 |          38 |      3.84407e+06 |              24 |             6 |              8 |
| READY TO DRINK       |          38 |          38 |      2.24668e+06 |              24 |             6 |              8 |
| IMPRESS              |          38 |          38 | 715647           |              24 |             6 |              8 |
| TANQUERAY            |          38 |          38 | 653861           |              24 |             6 |              8 |
| PUNCH! CLUB          |          38 |          35 | 465064           |              24 |             6 |              8 |
| NOHRLUND             |          38 |          38 | 370605           |              24 |             6 |              8 |
| BUZZBALLZ            |          38 |          38 | 280367           |              24 |             6 |              8 |
| MIKROPOLIS COCKTAILS |          38 |          38 | 263801           |              24 |             6 |              8 |
| THE COCKTAIL FACTORY |          38 |          38 | 227562           |              24 |             6 |              8 |
| SPRITZ               |          38 |          38 | 222579           |              24 |             6 |              8 |
| MAGNERS              |          38 |          38 | 178992           |              24 |             6 |              8 |
| REKORDERLIG          |          38 |          38 | 165453           |              24 |             6 |              8 |
| MOJITO               |          38 |          38 | 138859           |              24 |             6 |              8 |
| SIR. JAMES 101       |          38 |          38 | 111455           |              24 |             6 |              8 |
| G&T                  |          38 |          38 | 110139           |              24 |             6 |              8 |
| MALFY                |          38 |          34 | 103744           |              24 |             6 |              8 |
