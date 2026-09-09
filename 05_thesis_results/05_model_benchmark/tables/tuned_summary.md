# SRQ1 benchmark — Optuna-tuned (TPE, seed=42)

Trials per model: 30. Tuned on validation (WMAPE), refit on train+val, evaluated once on test.

## Dataset: brand

| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |
|---|---|---|---|---|---|
| CSD | LightGBM | 18.8% | 431185427272.5% | 51.6% | 19.4% |
| CSD | XGBoost | 18.4% | 717982958869.5% | 47.7% | 18.2% |
| Danskvand | LightGBM | 26.7% | 140468358984.5% | 57.6% | 29.2% |
| Danskvand | XGBoost | 23.4% | 288153756385.3% | 56.9% | 27.9% |
| Energidrikke | LightGBM | 20.3% | 15855939046528.6% | 80.3% | 12.2% |
| Energidrikke | XGBoost | 17.4% | 17322766093028.8% | 75.9% | 11.7% |
| RTD | LightGBM | 31.9% | 172838315530.9% | 46.9% | 25.4% |
| RTD | XGBoost | 30.8% | 204314827783.4% | 51.9% | 26.5% |

