# Nielsen Energidrikke Preprocessing Report
> Generated: 2026-05-01 20:28:37
> Category: Energidrikke
> Market scope: DVH EXCL. HD
> Min periods filter: 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 27 |
| Total rows | 1,053 |
| Periods per brand | 39 |
| Features engineered | 17 |
| Peak RAM (preprocessing) | 1519.8 MB |
| Elapsed time | 7.6 s |

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

| brand              |   n_periods |   n_nonzero |      total_units |   train_periods |   val_periods |   test_periods |
|:-------------------|------------:|------------:|-----------------:|----------------:|--------------:|---------------:|
| RED BULL           |          39 |          39 |      8.4207e+07  |              26 |             6 |              7 |
| MONSTER ENERGY     |          39 |          39 |      8.36007e+07 |              26 |             6 |              7 |
| FAXE KONDI BOOSTER |          39 |          39 |      7.35104e+07 |              26 |             6 |              7 |
| CULT               |          39 |          39 |      1.19637e+07 |              26 |             6 |              7 |
| STATE              |          39 |          39 |      1.04848e+07 |              26 |             6 |              7 |
| X-RAY              |          39 |          39 |      8.96123e+06 |              26 |             6 |              7 |
| VITAMIN WELL       |          39 |          39 |      7.69134e+06 |              26 |             6 |              7 |
| POWERADE           |          39 |          39 |      5.35002e+06 |              26 |             6 |              7 |
| PRIME              |          39 |          35 |      3.96598e+06 |              26 |             6 |              7 |
| NOCCO              |          39 |          39 |      2.21261e+06 |              26 |             6 |              7 |
| ROCKSTAR           |          39 |          39 |      2.14719e+06 |              26 |             6 |              7 |
| STATE VITAMIN      |          39 |          39 | 830230           |              26 |             6 |              7 |
| POWERKING          |          39 |          39 | 751059           |              26 |             6 |              7 |
| GATORADE           |          39 |          39 | 746791           |              26 |             6 |              7 |
| SMAG               |          39 |          39 | 672181           |              26 |             6 |              7 |
| LINUSPRO           |          39 |          30 | 515260           |              26 |             6 |              7 |
| AQUA D'OR          |          39 |          30 | 498211           |              26 |             6 |              7 |
| 4MOVE              |          39 |          39 | 396249           |              26 |             6 |              7 |
| BUTTERFLY          |          39 |          32 | 358688           |              26 |             6 |              7 |
| EASIS              |          39 |          38 | 334233           |              26 |             6 |              7 |
