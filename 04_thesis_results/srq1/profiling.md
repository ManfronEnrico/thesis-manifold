# SRQ1 operational profiling (CSD brand×chain; tuned configs)

Peak RAM (tracemalloc, Python-object allocations) and wall-clock per model. Supports the ≤8 GB sequential-execution constraint. ARIMA is per-series (univariate); tabular models train on the full matrix in one fit.

| Model | fit (s) | predict (ms) | peak RAM fit (MB) | peak RAM predict (MB) | n_train | n_features |
|---|---|---|---|---|---|---|
| Ridge | 0.075 | 2.8 | 5.5 | 0.15 | 2470 | 13 |
| LightGBM | 2.039 | 15.9 | 8.0 | 0.09 | 2470 | 13 |
| XGBoost | 0.968 | 9.3 | 0.1 | 0.06 | 2470 | 13 |
| ARIMA(per-series) | 0.085 | 7.0 | 0.3 | 0.08 | 26 | 1 |

All models fit comfortably within the ≤8 GB budget (peak RAM in the tens-of-MB range). Note tracemalloc captures Python-level allocations; native library buffers (LightGBM/XGBoost C++) are additional but small at this data scale.
