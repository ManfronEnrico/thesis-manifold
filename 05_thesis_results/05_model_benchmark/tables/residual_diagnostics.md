# SRQ1 residual diagnostics -- Ljung-Box on ARIMA residuals

Portmanteau test applied to the in-sample residuals of ARIMA(1, 1, 1), the statistical baseline reported in `stat_baselines.md`. Tested at lag 24 (two seasonal cycles, m = 12) against a chi-squared with `lag - 2` degrees of freedom.

**The degrees-of-freedom correction matters.** Hyndman & Athanasopoulos (3rd ed., ch 9.7) specify that a portmanteau test on the residuals of a fitted ARIMA consumes one degree of freedom per fitted ARMA parameter, so `K = p + q = 1 + 1 = 2` here. Omitting it overstates significance, reporting autocorrelation that is partly an artefact of the unadjusted statistic.

The test is applied to ARIMA rather than to the gradient-boosted models because the correction is defined in terms of ARIMA orders; a boosted tree has no `p` and no `q`, so the same test there would be uncorrectable and its significance overstated by construction.

Residuals are taken in log space, matching the `log1p` transform the baseline fits on. The first 1 residual(s) per series are dropped as differencing initialisation rather than model error.

| Category | n series | rejects H0 | rejection rate | median p | median ACF(12) |
|---|---|---|---|---|---|
| CSD | 95 | 24 | 25.3% | 0.4017 | +0.131 |
| Danskvand | 29 | 6 | 20.7% | 0.7621 | +0.115 |
| Energidrikke | 44 | 5 | 11.4% | 0.7180 | +0.022 |
| RTD | 62 | 16 | 25.8% | 0.6704 | +0.112 |
| **Overall** | **230** | **51** | **22.2%** | | **+0.109** |

`ACF(12)` is the residual autocorrelation at the seasonal lag. It localises the failure: a significant Q says structure remains, while a large ACF at lag 12 says that structure is annual.

**Reading the rejection rate.** At alpha = 0.05, a panel of genuine white noise rejects about 5% of the time by construction. A rate materially above that is remaining structure, not test noise.

**These residuals are in-sample, and that qualifies the rejection rates above.** Hyndman & Athanasopoulos (3rd ed., ch 5.3) distinguish residuals from true forecast errors: fitted values "are often not true forecasts because any parameters involved are estimated using all available observations, including future observations". A residual diagnostic that is to describe forecasting behaviour should therefore be computed on cross-validation residuals. The figures here are computed on the in-sample residuals of a single fit per series.

The direction of that bias is known. In-sample residuals are optimistically clean, because the fitted parameters have already absorbed some of the structure the test is looking for. **The rejection rates in this table are therefore lower bounds**, and the qualitative verdict is the conservative one: structure detected under an optimistic test is structure that is genuinely present. The rates themselves should be read as indicative rather than exact.

**Verdict: AUTOCORRELATION REMAINS -- structure is left unmodelled.**

The seasonal localisation survives this limitation intact, because it is a comparison made under identical conditions rather than an absolute level: among the 51 rejecting series the median ACF at lag 12 is +0.361, against +0.064 among the 179 that do not reject. Both halves of that contrast are computed the same way, so the in-sample optimism applies equally to each and cancels in the comparison. What remains unmodelled is concentrated at the annual lag, which is what a non-seasonal ARIMA on a monthly panel would be expected to leave behind.
