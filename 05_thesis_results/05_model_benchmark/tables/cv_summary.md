# SRQ1 — CV-tuned benchmark

Expanding-window time-series CV (4 folds), 100 Optuna
TPE trials per configuration, seed 42. Each configuration is tuned
twice — once for WMAPE, once for median MAPE — to show whether the
objective changes which model is selected.

`plateau_trial` = the first trial whose best CV score is within
0.5 percentage points of the final score. This is the
empirical justification for the trial budget; there is no citable
convention for a trial count.

| Category | Model | Tuned for | test WMAPE | test medMAPE | CV score | plateau |
|---|---|---|---|---|---|---|
| CSD | LightGBM | wmape | 19.3% | 45.7% | 19.4 | 23 |
| CSD | LightGBM | medmape | 27.9% | 40.4% | 43.0 | 71 |
| CSD | XGBoost | wmape | 18.4% | 41.4% | 18.8 | 0 |
| CSD | XGBoost | medmape | 18.9% | 38.8% | 42.5 | 20 |
| Danskvand | LightGBM | wmape | 27.3% | 37.5% | 28.7 | 51 |
| Danskvand | LightGBM | medmape | 35.7% | 42.6% | 37.0 | 71 |
| Danskvand | XGBoost | wmape | 27.1% | 40.4% | 25.7 | 69 |
| Danskvand | XGBoost | medmape | 24.2% | 45.4% | 35.0 | 58 |
| Energidrikke | LightGBM | wmape | 16.2% | 54.8% | 11.5 | 25 |
| Energidrikke | LightGBM | medmape | 23.8% | 52.3% | 43.5 | 82 |
| Energidrikke | XGBoost | wmape | 15.5% | 56.0% | 12.2 | 79 |
| Energidrikke | XGBoost | medmape | 24.7% | 47.7% | 42.4 | 32 |
| RTD | LightGBM | wmape | 30.3% | 49.8% | 34.2 | 62 |
| RTD | LightGBM | medmape | 31.1% | 48.9% | 47.8 | 83 |
| RTD | XGBoost | wmape | 30.2% | 46.2% | 34.5 | 20 |
| RTD | XGBoost | medmape | 29.4% | 47.2% | 45.6 | 39 |

## Does the objective change the answer?

| Category | Model | WMAPE when tuned for WMAPE | ... for medMAPE | delta |
|---|---|---|---|---|
| CSD | LightGBM | 19.3% | 27.9% | +8.7pp |
| CSD | XGBoost | 18.4% | 18.9% | +0.5pp |
| Danskvand | LightGBM | 27.3% | 35.7% | +8.3pp |
| Danskvand | XGBoost | 27.1% | 24.2% | -2.9pp |
| Energidrikke | LightGBM | 16.2% | 23.8% | +7.6pp |
| Energidrikke | XGBoost | 15.5% | 24.7% | +9.3pp |
| RTD | LightGBM | 30.3% | 31.1% | +0.8pp |
| RTD | XGBoost | 30.2% | 29.4% | -0.8pp |

