# SRQ1 benchmark — corrected DVH EXCL. HD matrices

Test-set accuracy. WMAPE = volume-weighted (business metric); medMAPE = median per-row APE. Models trained in log space, seed=42.

## Dataset: bymonth

| Category | Model | WMAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 34.9% | 79.9% | 2014 | 742 | 106 |
| CSD | Ridge | 23.0% | 30.7% | 2014 | 742 | 106 |
| CSD | LightGBM | 18.3% | 38.4% | 2014 | 742 | 106 |
| CSD | XGBoost | 18.1% | 36.6% | 2014 | 742 | 106 |
| danskvand | SeasonalNaive | 44.0% | 60.5% | 480 | 180 | 30 |
| danskvand | Ridge | 20.0% | 39.9% | 480 | 180 | 30 |
| danskvand | LightGBM | 33.7% | 60.1% | 480 | 180 | 30 |
| danskvand | XGBoost | 36.5% | 47.0% | 480 | 180 | 30 |
| energidrikke | SeasonalNaive | 31.5% | 100.0% | 850 | 350 | 50 |
| energidrikke | Ridge | 21.4% | 44.5% | 850 | 350 | 50 |
| energidrikke | LightGBM | 18.4% | 44.8% | 850 | 350 | 50 |
| energidrikke | XGBoost | 16.2% | 44.1% | 850 | 350 | 50 |
| RTD | SeasonalNaive | 54.9% | 94.8% | 1152 | 432 | 72 |
| RTD | Ridge | 55.0% | 37.9% | 1152 | 432 | 72 |
| RTD | LightGBM | 32.0% | 37.5% | 1152 | 432 | 72 |
| RTD | XGBoost | 31.9% | 31.3% | 1152 | 432 | 72 |

