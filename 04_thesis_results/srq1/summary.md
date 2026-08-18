# SRQ1 benchmark — corrected DVH EXCL. HD matrices

Test-set accuracy. WMAPE = volume-weighted (business metric); medMAPE = median per-row APE. Models trained in log space, seed=42.

## Dataset: bymonth

| Category | Model | WMAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 34.9% | 76.5% | 1805 | 665 | 95 |
| CSD | Ridge | 446.7% | 97.9% | 1805 | 665 | 95 |
| CSD | LightGBM | 18.5% | 38.9% | 1805 | 665 | 95 |
| CSD | XGBoost | 17.1% | 36.3% | 1805 | 665 | 95 |
| danskvand | SeasonalNaive | 44.0% | 59.4% | 464 | 174 | 29 |
| danskvand | Ridge | 7392.6% | 96.5% | 464 | 174 | 29 |
| danskvand | LightGBM | 33.1% | 56.9% | 464 | 174 | 29 |
| danskvand | XGBoost | 32.6% | 46.2% | 464 | 174 | 29 |
| energidrikke | SeasonalNaive | 30.6% | 98.8% | 748 | 308 | 44 |
| energidrikke | Ridge | 2669.4% | 398.8% | 748 | 308 | 44 |
| energidrikke | LightGBM | 17.8% | 47.0% | 748 | 308 | 44 |
| energidrikke | XGBoost | 14.9% | 43.9% | 748 | 308 | 44 |
| RTD | SeasonalNaive | 54.8% | 94.8% | 992 | 372 | 62 |
| RTD | Ridge | 1121.4% | 272.3% | 992 | 372 | 62 |
| RTD | LightGBM | 32.2% | 33.0% | 992 | 372 | 62 |
| RTD | XGBoost | 31.8% | 28.6% | 992 | 372 | 62 |

