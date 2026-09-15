**Deployed model configuration by category.** The estimator serving each category, with the data it was fitted on and the cost of fitting it. Read from each model's own metadata record rather than from the benchmark, so it describes what answers a forecast call rather than what was evaluated.

| Category     | Deployed model   |   Inputs |   Train rows | Trained through   |   Test rows |   Brands |   Interval q90 (log) |   Fit (s) |   Peak fit RAM (MB) |
|:-------------|:-----------------|---------:|-------------:|:------------------|------------:|---------:|---------------------:|----------:|--------------------:|
| CSD          | XGBoost(tuned)   |       18 |        2,280 | 2025-12           |         665 |       95 |                2.027 |      4.8  |                47.5 |
| Danskvand    | XGBoost(tuned)   |       17 |          580 | 2026-01           |         174 |       29 |                2.04  |      1.82 |                 0.2 |
| Energidrikke | LightGBM(tuned)  |       18 |          924 | 2025-12           |         308 |       44 |                2.691 |      4.96 |                43.7 |
| Rtd          | LightGBM(tuned)  |       17 |        1,240 | 2026-01           |         372 |       62 |                1.89  |      1.23 |                 8.2 |

*Note.* One model is served per category, selected on cross-validated score. `Interval q90 (log)` is the split-conformal quantile of the validation residuals in log space, which is what sets the width of the 90% prediction interval the tool returns. Input counts differ because promotional measures are absent for two categories, where the column is omitted rather than zero-filled.
