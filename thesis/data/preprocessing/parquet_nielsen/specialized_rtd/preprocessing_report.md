# Nielsen RTD Preprocessing Report
> Generated: 2026-05-01 20:28:46
> Category: RTD
> Market scope: DVH EXCL. HD
> Min periods filter: 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 42 |
| Total rows | 1,554 |
| Periods per brand | 37 |
| Features engineered | 18 |
| Peak RAM (preprocessing) | 1022.6 MB |
| Elapsed time | 5.8 s |

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

| brand                |   n_periods |   n_nonzero |      total_units |   train_periods |   val_periods |   test_periods |
|:---------------------|------------:|------------:|-----------------:|----------------:|--------------:|---------------:|
| BREEZER              |          37 |          37 |      3.23256e+07 |              24 |             6 |              7 |
| SHAKER               |          37 |          37 |      2.37127e+07 |              24 |             6 |              7 |
| SMIRNOFF ICE/TWISTED |          37 |          37 |      2.20622e+07 |              24 |             6 |              7 |
| SOMERSBY             |          37 |          37 |      9.14362e+06 |              24 |             6 |              7 |
| MOKAÏ                |          37 |          37 |      3.81625e+06 |              24 |             6 |              7 |
| READY TO DRINK       |          37 |          37 |      2.20702e+06 |              24 |             6 |              7 |
| IMPRESS              |          37 |          37 | 715624           |              24 |             6 |              7 |
| TANQUERAY            |          37 |          37 | 649637           |              24 |             6 |              7 |
| PUNCH! CLUB          |          37 |          34 | 459857           |              24 |             6 |              7 |
| NOHRLUND             |          37 |          37 | 370477           |              24 |             6 |              7 |
| BUZZBALLZ            |          37 |          37 | 274371           |              24 |             6 |              7 |
| MIKROPOLIS COCKTAILS |          37 |          37 | 258477           |              24 |             6 |              7 |
| THE COCKTAIL FACTORY |          37 |          37 | 227556           |              24 |             6 |              7 |
| SPRITZ               |          37 |          37 | 217218           |              24 |             6 |              7 |
| MAGNERS              |          37 |          37 | 171567           |              24 |             6 |              7 |
| REKORDERLIG          |          37 |          37 | 165209           |              24 |             6 |              7 |
| MOJITO               |          37 |          37 | 138592           |              24 |             6 |              7 |
| SIR. JAMES 101       |          37 |          37 | 110131           |              24 |             6 |              7 |
| G&T                  |          37 |          37 | 109655           |              24 |             6 |              7 |
| MALFY                |          37 |          33 | 103739           |              24 |             6 |              7 |
