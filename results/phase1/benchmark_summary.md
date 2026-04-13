# Model Benchmark Report -- SRQ1
> Generated: 2026-04-13
> Market: DVH EXCL. HD  |  Brands benchmarked: 77
> Val set: 6 periods (Mar-Aug 2025)  |  Train: 29 periods (Oct 2022-Feb 2025)

## Model Rankings (Mean MAPE on Validation Set)

| model    |   n_brands |      mean_mape |   median_mape |       mean_rmse |   mean_peak_mb |   total_elapsed_s |
|:---------|-----------:|---------------:|--------------:|----------------:|---------------:|------------------:|
| XGBoost  |         77 |  181.03        |         36.03 | 61180.2         |           0.18 |              90.2 |
| Prophet  |         77 |  470.81        |         58.61 | 75351           |           1.9  |            1587.6 |
| ARIMA    |         77 | 1162.85        |         49.6  | 76110.8         |          10.25 |              60   |
| LightGBM |         77 | 1296.71        |         60.9  | 81028.9         |           1.16 |              12.7 |
| Ridge    |         77 |    3.34747e+07 |         34.2  |     3.49411e+08 |           0.05 |               1.9 |

## Interpretation

- Lower MAPE = better accuracy
- Lower peak_mb = better memory efficiency (constraint: 8GB total)
- MAPE computed only on periods with non-zero actual sales
- Results aggregate across 77 brand series in DVH EXCL. HD

## Raw Results

Full per-brand x per-model results: `results/phase1/benchmark_results.csv`

## Total Runtime

1752.8 seconds (29.2 minutes) for all 77 brands x 5 models
