# SRQ1 benchmark — Optuna-tuned (TPE, seed=42)

Trials per model: 30. Tuned on validation (WMAPE), refit on train+val, evaluated once on test.

## Dataset: bychain

| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |
|---|---|---|---|---|---|
| CSD | LightGBM | 21.2% | 55.2% | 22.1% | 22.6% |
| CSD | XGBoost | 20.8% | 54.5% | 22.0% | 21.9% |
| danskvand | LightGBM | 24.1% | 7438153885.4% | 23.4% | 16.6% |
| danskvand | XGBoost | 22.0% | 7984019094.5% | 21.8% | 16.3% |
| energidrikke | LightGBM | 14.4% | 11431678131.8% | 21.2% | 14.6% |
| energidrikke | XGBoost | 13.9% | 16142103812.7% | 21.0% | 14.5% |
| RTD | LightGBM | 40.8% | 5019414818.6% | 30.2% | 40.0% |
| RTD | XGBoost | 38.8% | 5346112824.9% | 29.1% | 38.9% |

## Dataset: brand

| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |
|---|---|---|---|---|---|
| CSD | LightGBM | 17.4% | 46.9% | 24.5% | 15.3% |
| CSD | XGBoost | 16.5% | 45.5% | 24.4% | 15.2% |
| danskvand | LightGBM | 26.2% | 827797946.8% | 31.1% | 14.9% |
| danskvand | XGBoost | 23.8% | 1629493165.4% | 25.5% | 14.2% |
| energidrikke | LightGBM | 14.3% | 49298452761.5% | 37.0% | 11.0% |
| energidrikke | XGBoost | 11.4% | 9449126792.3% | 41.2% | 11.1% |
| RTD | LightGBM | 33.4% | 7791027559.2% | 31.1% | 28.8% |
| RTD | XGBoost | 31.0% | 2565595403.3% | 29.5% | 30.3% |

