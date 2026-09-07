# SRQ1 benchmark — corrected DVH EXCL. HD matrices

Test-set accuracy. WMAPE = volume-weighted (business metric); medMAPE = median per-row APE. Models trained in log space, seed=42.

## Dataset: bymonth

| Category | Model | WMAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 26.8% | 73.0% | 1615 | 665 | 95 |
| CSD | Ridge | 41.5% | 53.6% | 1615 | 665 | 95 |
| CSD | LightGBM | 20.4% | 56.8% | 1615 | 665 | 95 |
| CSD | XGBoost | 20.7% | 50.1% | 1615 | 665 | 95 |
| danskvand | SeasonalNaive | 50.5% | 70.1% | 406 | 174 | 29 |
| danskvand | Ridge | 30.4% | 51.2% | 406 | 174 | 29 |
| danskvand | LightGBM | 34.3% | 57.6% | 406 | 174 | 29 |
| danskvand | XGBoost | 34.9% | 51.2% | 406 | 174 | 29 |
| energidrikke | SeasonalNaive | 31.3% | 100.0% | 660 | 308 | 44 |
| energidrikke | Ridge | 48.6% | 96.4% | 660 | 308 | 44 |
| energidrikke | LightGBM | 17.3% | 84.5% | 660 | 308 | 44 |
| energidrikke | XGBoost | 18.8% | 79.0% | 660 | 308 | 44 |
| RTD | SeasonalNaive | 78.1% | 100.0% | 868 | 372 | 62 |
| RTD | Ridge | 72.4% | 71.2% | 868 | 372 | 62 |
| RTD | LightGBM | 28.4% | 58.8% | 868 | 372 | 62 |
| RTD | XGBoost | 29.4% | 57.4% | 868 | 372 | 62 |

