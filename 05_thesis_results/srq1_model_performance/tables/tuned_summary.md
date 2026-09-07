# SRQ1 benchmark — Optuna-tuned (TPE, seed=42)

Trials per model: 30. Tuned on validation (WMAPE), refit on train+val, evaluated once on test.

## Dataset: brand

| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |
|---|---|---|---|---|---|
| CSD | LightGBM | 15.8% | 82706541072.2% | 38.6% | 15.5% |
| CSD | XGBoost | 15.0% | 109817858230.2% | 36.2% | 14.5% |
| danskvand | LightGBM | 23.7% | 80545745568.7% | 47.4% | 27.2% |
| danskvand | XGBoost | 20.9% | 224752845644.6% | 50.8% | 24.8% |
| energidrikke | LightGBM | 14.6% | 2591193490523.4% | 47.6% | 8.0% |
| energidrikke | XGBoost | 13.1% | 1397269399626.6% | 45.1% | 8.7% |
| RTD | LightGBM | 35.1% | 61391240257.3% | 43.4% | 21.9% |
| RTD | XGBoost | 36.0% | 33758178429.6% | 35.0% | 23.8% |

