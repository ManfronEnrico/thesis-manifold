# SRQ1 benchmark — corrected DVH EXCL. HD matrices

Test-set accuracy. WMAPE = volume-weighted (business metric); medMAPE = median per-row APE. Models trained in log space, seed=42.

## Dataset: bymonth

| Category | Model | WMAPE | mean MAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 34.9% | 1843370472044.7% | 76.5% | 1805 | 665 | 95 |
| CSD | Ridge | 375.0% | 773088043673.2% | 96.5% | 1805 | 665 | 95 |
| CSD | LightGBM | 17.5% | 52794785965.0% | 37.1% | 1805 | 665 | 95 |
| CSD | XGBoost | 17.5% | 50512689549.9% | 38.9% | 1805 | 665 | 95 |
| danskvand | SeasonalNaive | 44.0% | 535085230058235.1% | 59.4% | 464 | 174 | 29 |
| danskvand | Ridge | 847.9% | 7204824274302845.0% | 97.0% | 464 | 174 | 29 |
| danskvand | LightGBM | 34.4% | 12835859687927.0% | 46.7% | 464 | 174 | 29 |
| danskvand | XGBoost | 34.9% | 24742038538388.9% | 44.5% | 464 | 174 | 29 |
| energidrikke | SeasonalNaive | 30.6% | 671744389835295.6% | 98.8% | 748 | 308 | 44 |
| energidrikke | Ridge | 344.5% | 2969589811220.5% | 341.2% | 748 | 308 | 44 |
| energidrikke | LightGBM | 18.0% | 6393533247952.7% | 52.2% | 748 | 308 | 44 |
| energidrikke | XGBoost | 14.8% | 13860181076507.3% | 59.4% | 748 | 308 | 44 |
| RTD | SeasonalNaive | 54.8% | 29530194842631.7% | 94.8% | 992 | 372 | 62 |
| RTD | Ridge | 323.8% | 79997721713596.0% | 126.3% | 992 | 372 | 62 |
| RTD | LightGBM | 33.3% | 4437248332384.8% | 45.4% | 992 | 372 | 62 |
| RTD | XGBoost | 33.1% | 5427653287601.5% | 41.9% | 992 | 372 | 62 |

