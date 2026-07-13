# SRQ1 benchmark — corrected DVH EXCL. HD matrices

Test-set accuracy. WMAPE = volume-weighted (business metric); medMAPE = median per-row APE. Models trained in log space, seed=42.

## Dataset: bymonth

| Category | Model | WMAPE | mean MAPE | median MAPE | n_train | n_test | n_series |
|---|---|---|---|---|---|---|---|
| CSD | SeasonalNaive | 35.1% | 280851070466.2% | 55.3% | 692 | 752 | 58 |
| CSD | Ridge | 347.5% | 217649442019.8% | 86.9% | 692 | 752 | 58 |
| CSD | LightGBM | 21.2% | 11943870447.6% | 27.2% | 692 | 752 | 58 |
| CSD | XGBoost | 25.2% | 21298654177.9% | 27.9% | 692 | 752 | 58 |

