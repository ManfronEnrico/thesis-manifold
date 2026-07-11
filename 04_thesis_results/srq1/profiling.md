# SRQ1 operational profiling (CSD brand×chain; tuned configs)

Peak RAM (tracemalloc, Python-object allocations) and wall-clock per model. Supports the ≤8 GB sequential-execution constraint. ARIMA is per-series (univariate); tabular models train on the full matrix in one fit.

| Model | fit (s) | predict (ms) | peak RAM fit (MB) | peak RAM predict (MB) | n_train | n_features |
|---|---|---|---|---|---|---|
| Ridge | 0.011 | 2.5 | 1.5 | 0.98 | 6045 | 14 |
| LightGBM | 7.714 | 166.9 | 18.7 | 0.53 | 6045 | 14 |
| XGBoost | 1.746 | 16.3 | 0.2 | 0.12 | 6045 | 14 |
| ARIMA(per-series) | 0.058 | 55.7 | 0.5 | 0.17 | 174 | 1 |

All models fit comfortably within the ≤8 GB budget (peak RAM in the tens-of-MB range). Note tracemalloc captures Python-level allocations; native library buffers (LightGBM/XGBoost C++) are additional but small at this data scale.
