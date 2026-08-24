# SRQ1 statistical baselines (brand×month, per-brand)

Six benchmarks, ordered simplest to most complex. The first three (naive, seasonal-naive, drift) are the standard forecasting floor per Hyndman & Athanasopoulos ch 5.2 and the M-competitions; a learned model that does not beat them is unbenchmarked. Ridge uses the SAME features as the tabular models, so Ridge→GBM isolates the nonlinearity premium while ARIMA→Ridge isolates the feature premium.

**Ridge appears twice, deliberately.** `Ridge` applies an extrapolation bound (that series' observed maximum x 3); `Ridge(unclipped)` does not. The bound is an arbitrary constant, so reporting only the bounded figure would describe a different estimator than 'Ridge'. The unclipped figure is the evidence that a per-brand linear fit on ~24 rows against 13 features is unusable -- it is published rather than suppressed. Prefer the POOLED Ridge in `ridge_pooled.md` for the nonlinearity-premium argument.

**medMAPE (median per-series) is the headline metric here.** WMAPE is volume-weighted and unbounded above, so one diverged series sets the category figure -- CSD Prophet's WMAPE is 60% a single brand (P0038 F72). Both are reported; prefer medMAPE when comparing per-series statistical baselines. For SRQ4 comparison vs the tabular models (tuned_summary.md).

| Category | Model | medMAPE | WMAPE | n_series |
|---|---|---|---|---|
| CSD | Naive | 59.1% | 42.9% | 95 |
| CSD | SeasonalNaive | 54.7% | 19.2% | 95 |
| CSD | Drift | 57.0% | 47.7% | 95 |
| CSD | Ridge | 43.5% | 19.4% | 95 |
| CSD | Ridge(unclipped) | 43.5% | 19.9% | 95 |
| CSD | ARIMA | 58.5% | 21.8% | 95 |
| CSD | Prophet | 63.1% | 105.7% | 95 |
| danskvand | Naive | 36.0% | 32.5% | 29 |
| danskvand | SeasonalNaive | 45.8% | 35.9% | 29 |
| danskvand | Drift | 43.6% | 32.0% | 29 |
| danskvand | Ridge | 40.6% | 10.9% | 29 |
| danskvand | Ridge(unclipped) | 40.6% | 10.9% | 29 |
| danskvand | ARIMA | 48.4% | 33.5% | 29 |
| danskvand | Prophet | 37.1% | 19.5% | 29 |
| energidrikke | Naive | 38.0% | 18.9% | 44 |
| energidrikke | SeasonalNaive | 95.9% | 23.8% | 44 |
| energidrikke | Drift | 34.2% | 17.7% | 44 |
| energidrikke | Ridge | 81.5% | 18.3% | 44 |
| energidrikke | Ridge(unclipped) | 81.5% | 28261334347674.2% | 44 |
| energidrikke | ARIMA | 70.1% | 19.4% | 44 |
| energidrikke | Prophet | 112.5% | 972.4% | 44 |
| RTD | Naive | 44.1% | 89.3% | 62 |
| RTD | SeasonalNaive | 89.4% | 27.3% | 62 |
| RTD | Drift | 52.9% | 95.9% | 62 |
| RTD | Ridge | 56.1% | 40.5% | 62 |
| RTD | Ridge(unclipped) | 56.8% | 2458.9% | 62 |
| RTD | ARIMA | 66.0% | 53.3% | 62 |
| RTD | Prophet | 88.8% | 66.8% | 62 |
