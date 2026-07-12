# Step 07 — Baselines Summary (VAL set)
_Generated 2026-04-16T20:26:56_

Evaluation window: VAL (Mar 2025 – Aug 2025, 6 months, 77 brands).
Metric convention: median MAPE across brands (robust to outliers).

## Ranking

| model | n_brands | median_mape | mean_mape | median_wape | mean_rmse | mean_mae |
|---|---|---|---|---|---|---|
| SeasonalNaive | 77 | 49.37 | 1155.44 | 46.82 | 70580.77 | 57632.96 |
| NaiveMean | 77 | 57.51 | 6619.94 | 53.86 | 77066.40 | 67863.87 |
| ARIMA_top10 | 10 | 71.86 | 125.91 | 70.49 | 1828062.98 | 1587215.26 |
| Ridge_global | 77 | 73.12 | 271.71 | 70.43 | 123721.53 | 104312.70 |
| OLS_global | 77 | 73.42 | 270.55 | 72.14 | 122469.98 | 102762.84 |

## Reference (Phase-1 benchmark, per-brand best-of)

| Model         | Median MAPE |
|---|---:|
| LightGBM      | 31.03 |
| Ensemble      | 31.59 |
| XGBoost       | 32.84 |
| Ridge (local) | 39.90 |
| SeasonalNaive | 49.37 |
| ARIMA         | 49.60 |
| Prophet       | 58.61 |