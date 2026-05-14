# Nielsen Energidrikke Preprocessing Report
> Generated: 2026-05-14 13:27:56
> Category: Energidrikke
> Market scope: DVH EXCL. HD
> Min periods filter: 30

## Summary

| Metric | Value |
|---|---|
| Brands in feature matrix | 28 |
| Total rows | 1,120 |
| Periods per brand | 40 |
| Features engineered | 17 |
| Peak RAM (preprocessing) | 270.7 MB |
| Elapsed time | 3.2 s |

## Split Boundaries

| Split | Start | End | Periods |
|---|---|---|---|
| Train | 2023-01-01 | 2025-02-01 | 26 |
| Val | 2025-03-01 | 2025-08-01 | 6 |
| Test | 2025-09-01 | 2026-04-01 | 8 |

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
| RED BULL           |          40 |          40 |      8.68681e+07 |              26 |             6 |              8 |
| MONSTER ENERGY     |          40 |          40 |      8.62317e+07 |              26 |             6 |              8 |
| FAXE KONDI BOOSTER |          40 |          40 |      7.56818e+07 |              26 |             6 |              8 |
| CULT               |          40 |          40 |      1.20478e+07 |              26 |             6 |              8 |
| STATE              |          40 |          40 |      1.07291e+07 |              26 |             6 |              8 |
| X-RAY              |          40 |          40 |      9.25912e+06 |              26 |             6 |              8 |
| VITAMIN WELL       |          40 |          40 |      7.87149e+06 |              26 |             6 |              8 |
| POWERADE           |          40 |          40 |      5.48094e+06 |              26 |             6 |              8 |
| PRIME              |          40 |          36 |      3.96599e+06 |              26 |             6 |              8 |
| ROCKSTAR           |          40 |          40 |      2.38755e+06 |              26 |             6 |              8 |
| NOCCO              |          40 |          40 |      2.28063e+06 |              26 |             6 |              8 |
| STATE VITAMIN      |          40 |          40 | 856807           |              26 |             6 |              8 |
| POWERKING          |          40 |          40 | 820127           |              26 |             6 |              8 |
| GATORADE           |          40 |          40 | 755134           |              26 |             6 |              8 |
| SMAG               |          40 |          40 | 680017           |              26 |             6 |              8 |
| LINUSPRO           |          40 |          31 | 515261           |              26 |             6 |              8 |
| AQUA D'OR          |          40 |          31 | 500073           |              26 |             6 |              8 |
| 4MOVE              |          40 |          40 | 404296           |              26 |             6 |              8 |
| BUTTERFLY          |          40 |          32 | 358688           |              26 |             6 |              8 |
| EASIS              |          40 |          38 | 334233           |              26 |             6 |              8 |
