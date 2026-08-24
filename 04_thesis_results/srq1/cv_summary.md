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
| CSD | LightGBM | wmape | 14.5% | 33.2% | 17.0 | 11 |
| CSD | LightGBM | medmape | 22.8% | 30.4% | 31.0 | 21 |
| CSD | XGBoost | wmape | 15.2% | 31.8% | 16.1 | 15 |
| CSD | XGBoost | medmape | 20.5% | 28.8% | 29.5 | 43 |
| danskvand | LightGBM | wmape | 20.5% | 38.6% | 17.9 | 10 |
| danskvand | LightGBM | medmape | 23.8% | 36.5% | 32.2 | 12 |
| danskvand | XGBoost | wmape | 20.9% | 35.8% | 17.1 | 21 |
| danskvand | XGBoost | medmape | 20.5% | 35.5% | 29.4 | 87 |
| energidrikke | LightGBM | wmape | 16.5% | 34.7% | 10.6 | 3 |
| energidrikke | LightGBM | medmape | 29.8% | 39.1% | 34.2 | 70 |
| energidrikke | XGBoost | wmape | 13.0% | 32.3% | 10.6 | 32 |
| energidrikke | XGBoost | medmape | 15.2% | 31.4% | 32.2 | 42 |
| RTD | LightGBM | wmape | 31.8% | 38.1% | 27.9 | 69 |
| RTD | LightGBM | medmape | 40.1% | 34.6% | 32.7 | 44 |
| RTD | XGBoost | wmape | 36.1% | 32.8% | 28.0 | 16 |
| RTD | XGBoost | medmape | 35.0% | 29.5% | 31.6 | 53 |

## Does the objective change the answer?

| Category | Model | WMAPE when tuned for WMAPE | ... for medMAPE | delta |
|---|---|---|---|---|
| CSD | LightGBM | 14.5% | 22.8% | +8.3pp |
| CSD | XGBoost | 15.2% | 20.5% | +5.2pp |
| danskvand | LightGBM | 20.5% | 23.8% | +3.2pp |
| danskvand | XGBoost | 20.9% | 20.5% | -0.4pp |
| energidrikke | LightGBM | 16.5% | 29.8% | +13.3pp |
| energidrikke | XGBoost | 13.0% | 15.2% | +2.1pp |
| RTD | LightGBM | 31.8% | 40.1% | +8.2pp |
| RTD | XGBoost | 36.1% | 35.0% | -1.0pp |

