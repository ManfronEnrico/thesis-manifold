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

**Verdict: AUTOCORRELATION REMAINS -- structure is left unmodelled.**
