# SRQ1 benchmark — Optuna-tuned (TPE, seed=42)

Trials per model: 30. Tuned on validation (WMAPE), refit on train+val, evaluated once on test.


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

> **Grain note (P0035, 2026-08-01):** the `bychain` (brand x chain) table was
> removed from this file. DEC-GRAIN (2026-07-12) locked the thesis grain to
> brand x month, so chain-grain numbers are no longer a claimed result. The
> original table is preserved verbatim at
> `plans/P0035_2026-08-01_grain-artifact-removal/preserved_chain_grain_results/`.
