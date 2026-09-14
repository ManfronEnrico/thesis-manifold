# SRQ1 operational profiling (CSD brand×month; tuned configs)

Peak **process RSS** and wall-clock per model, each measured in isolation. Supports the ≤4 GB sequential-execution constraint (the measured Prometheus sandbox template). ARIMA and Prophet are per-series (univariate); tabular models train on the full matrix in one fit.

Environment: 8 logical cores, 17.0 GB system RAM, XGBoost `n_jobs=-1`. Native buffers scale with core count, so these figures are machine-dependent and the core count is part of the result.

| Model | fit (s) | predict (ms) | peak RSS fit (MB) | peak RSS predict (MB) | tracemalloc fit (MB) | model size (MB) | n_train | n_features |
|---|---|---|---|---|---|---|---|---|
| Ridge | 0.008 | 2.2 | 1.5 | 0.02 | 0.8 | 0.0 | 2280 | 18 |
| LightGBM | 1.758 | 15.5 | 17.9 | 0.07 | 4.9 | 1.59 | 2280 | 18 |
| XGBoost | 1.679 | 11.8 | 34.5 | 0.65 | 0.1 | 3.9 | 2280 | 18 |
| ARIMA(per-series) | 0.04 | 4.7 | 2.1 | 0.11 | 0.3 | -- | 24 | 1 |
| Prophet(per-series) | 11.373 | 95.3 | 5.2 | 1.73 | 2.3 | 0.01 | 24 | 1 |

**Reading the two memory columns.** RSS is what the operating system charges the process and is the figure the sandbox budget is denominated in. tracemalloc counts Python-object allocations only. The gap between them is native (C/C++) allocation: LightGBM and XGBoost build their ensembles outside the Python heap, so tracemalloc is structurally blind to the dominant term for exactly the two models that allocate most. An earlier version of this table reported tracemalloc alone and put XGBoost at 0.1 MB -- below Ridge, and impossible for a 926-tree depth-7 ensemble. That figure was not small, it was unmeasured. Both columns are kept so the correction is auditable rather than silent.

Model size on disk is a third, independent witness, measured by serialisation rather than by either profiler, and so shares neither one's blind spot.
