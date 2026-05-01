# Nielsen Total Beer Preprocessing Report
> Generated: 2026-05-01 20:35:09
> Category: Total Beer
> Market scope: DVH EXCL. HD
> Min periods filter: 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 173 |
| Total rows | 6,747 |
| Periods per brand | 39 |
| Features engineered | 17 |
| Peak RAM (preprocessing) | 2964.0 MB |
| Elapsed time | 17.5 s |

## Split Boundaries

| Split | Start | End | Periods |
|---|---|---|---|
| Train | 2023-01-01 | 2025-02-01 | 26 |
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

| brand                  |   n_periods |   n_nonzero |   total_units |   train_periods |   val_periods |   test_periods |
|:-----------------------|------------:|------------:|--------------:|----------------:|--------------:|---------------:|
| TUBORG GRØN            |          39 |          39 |   2.94889e+07 |              26 |             6 |              7 |
| TUBORG CLASSIC         |          39 |          39 |   2.06928e+07 |              26 |             6 |              7 |
| CARLSBERG PILSNER      |          39 |          39 |   9.29074e+06 |              26 |             6 |              7 |
| HARBOE PREMIUM         |          39 |          38 |   7.29576e+06 |              26 |             6 |              7 |
| ROYAL EXPORT           |          39 |          37 |   4.47482e+06 |              26 |             6 |              7 |
| JACOBSEN               |          39 |          39 |   4.22858e+06 |              26 |             6 |              7 |
| GRIMBERGEN             |          39 |          39 |   3.91987e+06 |              26 |             6 |              7 |
| SKOVLYST               |          39 |          39 |   3.69699e+06 |              26 |             6 |              7 |
| KRONENBOURG 1664 BLANC |          39 |          39 |   3.44084e+06 |              26 |             6 |              7 |
| HEINEKEN ORIGINAL      |          39 |          39 |   3.19849e+06 |              26 |             6 |              7 |
| ODENSE PILSNER         |          39 |          39 |   2.77346e+06 |              26 |             6 |              7 |
| HANCOCK HØKER BAJER    |          39 |          30 |   2.55429e+06 |              26 |             6 |              7 |
| ROYAL CLASSIC          |          39 |          39 |   2.21409e+06 |              26 |             6 |              7 |
| ODENSE CLASSIC         |          39 |          38 |   2.11505e+06 |              26 |             6 |              7 |
| TO ØL                  |          39 |          39 |   1.94404e+06 |              26 |             6 |              7 |
| CARLSBERG NORDIC       |          39 |          39 |   1.72385e+06 |              26 |             6 |              7 |
| ANARKIST               |          39 |          39 |   1.68475e+06 |              26 |             6 |              7 |
| TUBORG GULD            |          39 |          38 |   1.67727e+06 |              26 |             6 |              7 |
| WILLEMOES              |          39 |          39 |   1.61075e+06 |              26 |             6 |              7 |
| CORONA EXTRA           |          39 |          38 |   1.54888e+06 |              26 |             6 |              7 |
