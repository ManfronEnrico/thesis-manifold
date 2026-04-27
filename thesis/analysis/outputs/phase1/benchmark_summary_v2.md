# Model Benchmark Report v2 -- SRQ1
> Generated: 2026-04-13
> Market: DVH EXCL. HD  |  Brands: 77
> Val set: 6 periods (Mar-Aug 2025)  |  Train: 29 periods (Oct 2022-Feb 2025)
> v2 improvements: lag_12, price_per_unit, Ridge log-clip, larger grids, Ensemble

## Model Rankings (Median MAPE on Validation Set)

| model         |   n_brands |   mean_mape |   median_mape |   p25_mape |   p75_mape |   mean_rmse |   mean_peak_mb |   total_elapsed_s |
|:--------------|-----------:|------------:|--------------:|-----------:|-----------:|------------:|---------------:|------------------:|
| LightGBM      |         77 |      164.22 |         31.03 |      17.05 |      72.5  |    102106   |          1.548 |             222.4 |
| Ensemble      |         77 |      191.86 |         31.59 |      15.45 |      94.54 |     98334.6 |          0     |               0   |
| XGBoost       |         77 |      170.63 |         32.84 |      18.96 |      82.46 |     99825.6 |          0.456 |             603.9 |
| Ridge         |         77 |      235.99 |         39.9  |      16.8  |     109.57 |    101386   |          0.058 |               2.4 |
| SeasonalNaive |         77 |     1155.44 |         49.37 |      21.21 |     200    |     70580.8 |          0.018 |               0   |
| ARIMA         |         77 |     1162.85 |         49.6  |      24.01 |     100.18 |     76110.8 |         10.249 |              67.3 |
| Prophet       |         77 |      470.81 |         58.61 |      25.01 |     210.92 |     75351   |          1.902 |            1618.2 |

## Best Model Per Brand

| model         |   count |
|:--------------|--------:|
| LightGBM      |      20 |
| Ridge         |      17 |
| XGBoost       |      15 |
| Prophet       |      12 |
| ARIMA         |       8 |
| SeasonalNaive |       5 |

## Notes

- Median MAPE used for ranking (robust to outlier brands)
- SeasonalNaive = academic baseline (same month last year)
- Ensemble = 0.6 x XGBoost + 0.4 x Ridge (Ridge weight = 0 if numerically unstable)
- Intermittent brands (>60% zero periods): 0 of 77
- RAM constraint: 8GB total; all models run sequentially

## Raw Results

`results/phase1/benchmark_results_v2.csv`
