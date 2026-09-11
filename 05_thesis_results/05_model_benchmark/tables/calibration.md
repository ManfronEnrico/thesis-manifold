# SRQ1 prediction-interval calibration — split conformal (tuned LightGBM / XGBoost, per served model, brand×month)

Half-width calibrated on validation residuals (log space); empirical coverage measured on test. Well-calibrated => empirical ≈ nominal.

**Read coverage and width together.** Coverage alone is not a success criterion: an arbitrarily wide interval attains perfect coverage while carrying no decision-relevant information. `Mean rel. width` is the interval width as a multiple of the actual value, so 3.0 means the interval spans about three times the quantity being forecast.

| Category | Nominal | Empirical coverage | Mean rel. width | n_test |
|---|---|---|---|---|
| CSD | 80% | 80.5% | 3.4 | 665 |
| CSD | 90% | 91.7% | 8.99  **<- too wide to act on** | 665 |
| Danskvand | 80% | 73.6% | 3.03 | 174 |
| Danskvand | 90% | 83.9% | 11.77  **<- too wide to act on** | 174 |
| Energidrikke | 80% | 77.3% | 10.54  **<- too wide to act on** | 308 |
| Energidrikke | 90% | 86.7% | 34.44  **<- too wide to act on** | 308 |
| RTD | 80% | 83.3% | 3.92 | 372 |
| RTD | 90% | 91.4% | 8.52  **<- too wide to act on** | 372 |

Coverage near nominal indicates the conformal interval is a usable confidence signal for the agentic layer (SRQ2); systematic over/under-coverage flags residual heteroskedasticity (interval width is global, not per-series).

## What the guarantee does and does not cover

The half-width is the `ceil((n+1)(1-alpha))/n` empirical quantile of the calibration residuals, i.e. Algorithm 2 of Lei et al. (2018), whose distribution-free finite-sample guarantee is **marginal** coverage `P(Y in C(X)) >= 1-alpha` -- an average over cells, NOT a per-brand or per-month promise (Lei et al., 2018, Remark 3).

**That guarantee assumes exchangeability, which monthly brand demand violates.** Barber et al. (2023) show unweighted split conformal can lose coverage materially under temporal drift, and bound the loss by a weighted sum of total-variation distances rather than eliminating it. So the coverage numbers above are an **empirical measurement**, not a theoretical entitlement -- which is exactly why they are measured on a held-out test period instead of assumed. The danskvand row (73.6% against a nominal 80%) is what that gap looks like in practice.

**Width is the binding constraint here, not coverage.** Danskvand and Energidrikke reach acceptable coverage at 90% only with intervals spanning 12-34x the actual, which no planner can act on. Report those as a limitation rather than averaging into a well-calibrated claim.
