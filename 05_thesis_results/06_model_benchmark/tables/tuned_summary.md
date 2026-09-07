# SRQ1 benchmark — Optuna-tuned (TPE, seed=42)

Trials per model: 30. Tuned on validation (WMAPE), refit on train+val, evaluated once on test.

## Dataset: brand

| Category | Model | test WMAPE | test mean MAPE | test median MAPE | val WMAPE |
|---|---|---|---|---|---|
| CSD | LightGBM | 19.7% | 456147798740.7% | 55.9% | 18.1% |
| CSD | XGBoost | 18.6% | 578829519035.0% | 49.3% | 18.7% |
| danskvand | LightGBM | 24.8% | 200714676755.5% | 59.5% | 29.2% |
| danskvand | XGBoost | 25.3% | 221420452458.4% | 58.3% | 28.2% |
| energidrikke | LightGBM | 22.9% | 22060348811263.7% | 78.9% | 11.3% |
| energidrikke | XGBoost | 17.4% | 24980804491696.9% | 81.3% | 11.2% |
| RTD | LightGBM | 31.7% | 222296342613.2% | 48.0% | 26.1% |
| RTD | XGBoost | 33.4% | 297449371629.2% | 46.8% | 27.0% |

