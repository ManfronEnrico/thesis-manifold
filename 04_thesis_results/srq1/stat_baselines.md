# SRQ1 statistical baselines — ARIMA + Prophet (brand×month, per-brand)

WMAPE = volume-weighted across brands; medMAPE = median per-series. For SRQ4 comparison vs the tabular models (tuned_summary.md).

| Category | Model | WMAPE | median MAPE | n_series |
|---|---|---|---|---|
| CSD | ARIMA | 24.2% | 43.1% | 77 |
| CSD | Prophet | 1715701549531750912.0% | 65.7% | 77 |
| danskvand | ARIMA | 33.4% | 52.8% | 24 |
| danskvand | Prophet | 16.9% | 36.2% | 24 |
| energidrikke | ARIMA | 15.7% | 47.2% | 27 |
| energidrikke | Prophet | 14858220394.7% | 55.4% | 27 |
| RTD | ARIMA | 48.2% | 68.0% | 42 |
| RTD | Prophet | 45.4% | 49.8% | 42 |
