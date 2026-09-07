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
| CSD | XGBoost | wmape | 16.6% | 33.7% | 16.1 | 0 |
| CSD | XGBoost | medmape | 19.2% | 28.8% | 29.3 | 59 |
| danskvand | LightGBM | wmape | 20.5% | 38.6% | 17.9 | 10 |
| danskvand | LightGBM | medmape | 23.8% | 36.5% | 32.2 | 12 |
| danskvand | XGBoost | wmape | 21.7% | 33.2% | 17.7 | 13 |
| danskvand | XGBoost | medmape | 21.7% | 32.9% | 29.0 | 69 |
| energidrikke | LightGBM | wmape | 16.5% | 34.7% | 10.6 | 3 |
| energidrikke | LightGBM | medmape | 29.8% | 39.1% | 34.2 | 70 |
| energidrikke | XGBoost | wmape | 14.1% | 35.6% | 10.7 | 36 |
| energidrikke | XGBoost | medmape | 15.0% | 30.5% | 32.7 | 25 |
| RTD | LightGBM | wmape | 31.8% | 38.1% | 27.9 | 69 |
| RTD | LightGBM | medmape | 40.1% | 34.6% | 32.7 | 44 |
| RTD | XGBoost | wmape | 34.9% | 33.9% | 28.4 | 3 |
| RTD | XGBoost | medmape | 39.4% | 31.2% | 31.6 | 13 |

## Does the objective change the answer?

| Category | Model | WMAPE when tuned for WMAPE | ... for medMAPE | delta |
|---|---|---|---|---|
| CSD | LightGBM | 14.5% | 22.8% | +8.3pp |
| CSD | XGBoost | 16.6% | 19.2% | +2.6pp |
| danskvand | LightGBM | 20.5% | 23.8% | +3.2pp |
| danskvand | XGBoost | 21.7% | 21.7% | -0.1pp |
| energidrikke | LightGBM | 16.5% | 29.8% | +13.3pp |
| energidrikke | XGBoost | 14.1% | 15.0% | +0.8pp |
| RTD | LightGBM | 31.8% | 40.1% | +8.2pp |
| RTD | XGBoost | 34.9% | 39.4% | +4.6pp |

