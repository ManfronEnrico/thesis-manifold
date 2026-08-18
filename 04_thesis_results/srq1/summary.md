# SRQ1 benchmark — corrected DVH EXCL. HD matrices

Test-set accuracy. WMAPE = volume-weighted (business metric); medMAPE = median per-row APE. Models trained in log space, seed=42.

## Dataset: bymonth

| Category | Model | WMAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 34.9% | 76.5% | 1805 | 665 | 95 |
| CSD | Ridge | 375.0% | 96.5% | 1805 | 665 | 95 |
| CSD | LightGBM | 17.5% | 37.1% | 1805 | 665 | 95 |
| CSD | XGBoost | 17.5% | 38.9% | 1805 | 665 | 95 |
| danskvand | SeasonalNaive | 44.0% | 59.4% | 464 | 174 | 29 |
| danskvand | Ridge | 847.9% | 97.0% | 464 | 174 | 29 |
| danskvand | LightGBM | 34.4% | 46.7% | 464 | 174 | 29 |
| danskvand | XGBoost | 34.9% | 44.5% | 464 | 174 | 29 |
| energidrikke | SeasonalNaive | 30.6% | 98.8% | 748 | 308 | 44 |
| energidrikke | Ridge | 344.5% | 341.2% | 748 | 308 | 44 |
| energidrikke | LightGBM | 18.0% | 52.2% | 748 | 308 | 44 |
| energidrikke | XGBoost | 14.8% | 59.4% | 748 | 308 | 44 |
| RTD | SeasonalNaive | 54.8% | 94.8% | 992 | 372 | 62 |
| RTD | Ridge | 323.8% | 126.3% | 992 | 372 | 62 |
| RTD | LightGBM | 33.3% | 45.4% | 992 | 372 | 62 |
| RTD | XGBoost | 33.1% | 41.9% | 992 | 372 | 62 |

