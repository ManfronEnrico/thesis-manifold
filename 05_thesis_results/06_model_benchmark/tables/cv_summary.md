# SRQ1 — CV-tuned benchmark

Expanding-window time-series CV (4 folds), 100 Optuna
TPE trials per configuration, seed 42. Each configuration is tuned
twice — once for WMAPE, once for median MAPE — to show whether the
objective changes which model is selected.

`plateau_trial` = the trial after which the best CV score improved by
<0.1% relative. This is the empirical justification for the trial
budget; there is no citable convention for a trial count.

| Category | Model | Tuned for | test WMAPE | test medMAPE | CV score | plateau |
|---|---|---|---|---|---|---|
| CSD | LightGBM | wmape | 17.8% | 41.2% | 20.2 | 11 |
| CSD | LightGBM | medmape | 27.4% | 39.9% | 44.6 | 19 |
| CSD | XGBoost | wmape | 17.8% | 42.1% | 19.6 | 30 |
| CSD | XGBoost | medmape | 26.4% | 38.7% | 42.6 | 53 |
| danskvand | LightGBM | wmape | 30.5% | 42.0% | 28.5 | 69 |
| danskvand | LightGBM | medmape | 33.9% | 43.6% | 37.9 | 94 |
| danskvand | XGBoost | wmape | 24.7% | 41.3% | 25.1 | 65 |
| danskvand | XGBoost | medmape | 26.8% | 45.3% | 37.1 | 6 |
| energidrikke | LightGBM | wmape | 17.1% | 55.4% | 11.6 | 22 |
| energidrikke | LightGBM | medmape | 26.4% | 51.6% | 43.4 | 93 |
| energidrikke | XGBoost | wmape | 15.9% | 52.6% | 12.5 | 10 |
| energidrikke | XGBoost | medmape | 23.6% | 53.3% | 41.4 | 57 |
| RTD | LightGBM | wmape | 33.1% | 46.1% | 36.3 | 55 |
| RTD | LightGBM | medmape | 33.3% | 46.4% | 46.9 | 75 |
| RTD | XGBoost | wmape | 33.2% | 44.7% | 34.3 | 70 |
| RTD | XGBoost | medmape | 45.1% | 50.0% | 46.4 | 71 |

## Does the objective change the answer?

| Category | Model | WMAPE when tuned for WMAPE | ... for medMAPE | delta |
|---|---|---|---|---|
| CSD | LightGBM | 17.8% | 27.4% | +9.6pp |
| CSD | XGBoost | 17.8% | 26.4% | +8.6pp |
| danskvand | LightGBM | 30.5% | 33.9% | +3.4pp |
| danskvand | XGBoost | 24.7% | 26.8% | +2.1pp |
| energidrikke | LightGBM | 17.1% | 26.4% | +9.3pp |
| energidrikke | XGBoost | 15.9% | 23.6% | +7.6pp |
| RTD | LightGBM | 33.1% | 33.3% | +0.3pp |
| RTD | XGBoost | 33.2% | 45.1% | +11.9pp |

