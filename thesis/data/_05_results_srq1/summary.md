# SRQ1 benchmark — corrected DVH EXCL. HD matrices

Test-set accuracy. WMAPE = volume-weighted (business metric); medMAPE = median per-row APE. Models trained in log space, seed=42.

## Dataset: bychain

| Category | Model | WMAPE | mean MAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 39.9% | 1955.7% | 44.2% | 3822 | 4305 | 390 |
| CSD | Ridge | 45356.2% | 2245.5% | 89.5% | 3822 | 4305 | 390 |
| CSD | LightGBM | 24.2% | 64.5% | 25.3% | 3822 | 4305 | 390 |
| CSD | XGBoost | 23.3% | 65.2% | 25.1% | 3822 | 4305 | 390 |
| danskvand | SeasonalNaive | 37.7% | 97308488780.5% | 38.5% | 1213 | 966 | 125 |
| danskvand | Ridge | 24577.9% | 493529084890.8% | 82.2% | 1213 | 966 | 125 |
| danskvand | LightGBM | 27.6% | 8780526532.1% | 24.1% | 1213 | 966 | 125 |
| danskvand | XGBoost | 22.9% | 4846033915.4% | 22.4% | 1213 | 966 | 125 |
| energidrikke | SeasonalNaive | 31.9% | 6218276771549.4% | 40.6% | 1814 | 1149 | 159 |
| energidrikke | Ridge | 498.0% | 813855069999.6% | 76.4% | 1814 | 1149 | 159 |
| energidrikke | LightGBM | 16.5% | 13077433484.8% | 22.9% | 1814 | 1149 | 159 |
| energidrikke | XGBoost | 16.0% | 20944068538.8% | 21.7% | 1814 | 1149 | 159 |
| RTD | SeasonalNaive | 58.8% | 151162791750.3% | 67.8% | 2056 | 1505 | 215 |
| RTD | Ridge | 3889.6% | 239616902074.2% | 95.4% | 2056 | 1505 | 215 |
| RTD | LightGBM | 45.2% | 4912813197.1% | 31.1% | 2056 | 1505 | 215 |
| RTD | XGBoost | 41.2% | 7871636645.5% | 30.3% | 2056 | 1505 | 215 |

## Dataset: brand

| Category | Model | WMAPE | mean MAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 32.6% | 4437.2% | 56.3% | 750 | 845 | 77 |
| CSD | Ridge | 163.3% | 1119.7% | 89.4% | 750 | 845 | 77 |
| CSD | LightGBM | 19.6% | 57.0% | 27.7% | 750 | 845 | 77 |
| CSD | XGBoost | 19.0% | 54.6% | 26.6% | 750 | 845 | 77 |
| danskvand | SeasonalNaive | 36.7% | 64736843214.2% | 43.8% | 238 | 190 | 24 |
| danskvand | Ridge | 483.6% | 424940583973.6% | 84.6% | 238 | 190 | 24 |
| danskvand | LightGBM | 42.3% | 14912360973.6% | 41.4% | 238 | 190 | 24 |
| danskvand | XGBoost | 31.8% | 3990000982.2% | 31.3% | 238 | 190 | 24 |
| energidrikke | SeasonalNaive | 27.5% | 4052930708385.4% | 73.4% | 288 | 205 | 27 |
| energidrikke | Ridge | 120.0% | 3643603033637.2% | 91.2% | 288 | 205 | 27 |
| energidrikke | LightGBM | 16.3% | 158919434156.3% | 42.8% | 288 | 205 | 27 |
| energidrikke | XGBoost | 15.6% | 37408172815.4% | 35.8% | 288 | 205 | 27 |
| RTD | SeasonalNaive | 41.6% | 93209890711.2% | 70.5% | 416 | 324 | 42 |
| RTD | Ridge | 345.9% | 436625453575.7% | 131.8% | 416 | 324 | 42 |
| RTD | LightGBM | 36.4% | 12641869462.9% | 29.8% | 416 | 324 | 42 |
| RTD | XGBoost | 38.4% | 6567621145.3% | 27.1% | 416 | 324 | 42 |

