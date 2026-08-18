# SRQ1 statistical baselines — ARIMA + Prophet (brand×month, per-brand)

WMAPE = volume-weighted across brands; medMAPE = median per-series. For SRQ4 comparison vs the tabular models (tuned_summary.md).

| Category | Model | WMAPE | median MAPE | n_series |
|---|---|---|---|---|
| CSD | ARIMA | 21.8% | 57.8% | 95 |
| CSD | Prophet | 105.7% | 64.4% | 95 |
| danskvand | ARIMA | 33.5% | 48.3% | 29 |
| danskvand | Prophet | 19.6% | 37.1% | 29 |
| energidrikke | ARIMA | 19.4% | 74.1% | 44 |
| energidrikke | Prophet | 1030.1% | 114.5% | 44 |
| RTD | ARIMA | 53.3% | 59.1% | 62 |
| RTD | Prophet | 67.0% | 86.7% | 62 |
