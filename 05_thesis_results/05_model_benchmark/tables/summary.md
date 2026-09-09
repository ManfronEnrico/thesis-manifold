# SRQ1 benchmark — corrected DVH EXCL. HD matrices

Test-set accuracy. WMAPE = volume-weighted (business metric); medMAPE = median per-row APE. Models trained in log space, seed=42.

## Dataset: bymonth

| Category | Model | WMAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 26.8% | 73.0% | 1615 | 665 | 95 |
| CSD | Ridge | 19.1% | 48.9% | 1615 | 665 | 95 |
| CSD | LightGBM | 21.4% | 52.8% | 1615 | 665 | 95 |
| CSD | XGBoost | 21.4% | 48.6% | 1615 | 665 | 95 |
| Danskvand | SeasonalNaive | 50.5% | 70.1% | 406 | 174 | 29 |
| Danskvand | Ridge | 30.2% | 50.4% | 406 | 174 | 29 |
| Danskvand | LightGBM | 34.7% | 55.9% | 406 | 174 | 29 |
| Danskvand | XGBoost | 35.0% | 55.4% | 406 | 174 | 29 |
| Energidrikke | SeasonalNaive | 31.3% | 100.0% | 660 | 308 | 44 |
| Energidrikke | Ridge | 23.9% | 83.1% | 660 | 308 | 44 |
| Energidrikke | LightGBM | 17.8% | 85.2% | 660 | 308 | 44 |
| Energidrikke | XGBoost | 20.0% | 76.8% | 660 | 308 | 44 |
| RTD | SeasonalNaive | 78.1% | 100.0% | 868 | 372 | 62 |
| RTD | Ridge | 71.5% | 68.4% | 868 | 372 | 62 |
| RTD | LightGBM | 27.7% | 57.8% | 868 | 372 | 62 |
| RTD | XGBoost | 28.3% | 56.7% | 868 | 372 | 62 |

