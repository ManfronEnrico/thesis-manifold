# SRQ1 statistical baselines — ARIMA + Prophet (brand×month, per-brand)

**medMAPE (median per-series) is the headline metric here.** WMAPE is volume-weighted and unbounded above, so one diverged series sets the category figure -- CSD Prophet's WMAPE is 60% a single brand (P0038 F72). Both are reported; prefer medMAPE when comparing per-series statistical baselines. For SRQ4 comparison vs the tabular models (tuned_summary.md).

| Category | Model | medMAPE | WMAPE | n_series |
|---|---|---|---|---|
| CSD | ARIMA | 58.5% | 21.8% | 95 |
| CSD | Prophet | 63.1% | 105.7% | 95 |
| danskvand | ARIMA | 48.4% | 33.5% | 29 |
| danskvand | Prophet | 37.1% | 19.5% | 29 |
| energidrikke | ARIMA | 70.1% | 19.4% | 44 |
| energidrikke | Prophet | 112.5% | 975.6% | 44 |
| RTD | ARIMA | 66.0% | 53.3% | 62 |
| RTD | Prophet | 88.8% | 66.8% | 62 |
