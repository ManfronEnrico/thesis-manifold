# SRQ1 benchmark — Optuna-tuned (TPE, seed=42)

Trials per model: 30. Tuned on validation (WMAPE), refit on train+val, evaluated once on test.

## Dataset: brand

| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |
|---|---|---|---|---|---|
| CSD | LightGBM | 15.6% | 93251057354.0% | 34.0% | 16.1% |
| CSD | XGBoost | 14.9% | 103874660089.8% | 37.7% | 14.8% |
| danskvand | LightGBM | 21.1% | 358868231444.5% | 37.8% | 26.8% |
| danskvand | XGBoost | 20.0% | 521658843758.1% | 38.1% | 25.3% |
| energidrikke | LightGBM | 14.3% | 2101461815684.4% | 48.3% | 7.9% |
| energidrikke | XGBoost | 14.3% | 1143461529994.0% | 47.0% | 7.7% |
| RTD | LightGBM | 33.9% | 58904604752.6% | 37.9% | 22.3% |
| RTD | XGBoost | 33.6% | 37293676641.2% | 36.6% | 24.6% |

