# SRQ1 prediction-interval calibration — split conformal (tuned XGBoost, brand×month)

Half-width calibrated on validation residuals (log space); empirical coverage measured on test. Well-calibrated => empirical ≈ nominal.

| Category | Nominal | Empirical coverage | Median rel. width | n_test |
|---|---|---|---|---|
| CSD | 80% | 83.3% | 1.67 | 845 |
| CSD | 90% | 90.5% | 2.57 | 845 |
| danskvand | 80% | 74.7% | 1.19 | 190 |
| danskvand | 90% | 85.8% | 1.98 | 190 |
| energidrikke | 80% | 67.3% | 1.84 | 205 |
| energidrikke | 90% | 81.0% | 2.95 | 205 |
| RTD | 80% | 79.3% | 1.55 | 324 |
| RTD | 90% | 88.0% | 2.22 | 324 |

Coverage near nominal indicates the conformal interval is a usable confidence signal for the agentic layer (SRQ2); systematic over/under-coverage flags residual heteroskedasticity (interval width is global, not per-series).
