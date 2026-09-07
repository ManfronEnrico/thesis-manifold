## Significant ACF Lags per Brand

- Lags at which the sample autocorrelation exceeds the 95 per cent confidence band of plus or minus 1.96 divided by the square root of the sample size, the standard criterion for identifying significant autocorrelation (Box and Jenkins, 1970).
- Lags significant across a majority of the leading brands indicate category-level temporal structure, whereas a lag significant for a single brand is more plausibly sampling variation.
- Significance at lag 12 indicates annual seasonality; significance at lags 1 to 3 indicates short-run persistence. Both motivate the inclusion of lagged sales as predictors.
- Autocorrelations are computed on the logarithmic transformation of the target, so the reported lags describe the series in the form in which it is modelled.
- The confidence band assumes a stationary series; where the stationarity tests are inconclusive, significance at long lags may reflect trend rather than genuine seasonal dependence.

| brand       |   n_periods |   conf_band | significant_lags                                      |
|:------------|------------:|------------:|:------------------------------------------------------|
| HARBOE      |          41 |      0.3061 | [1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 15]                |
| BLUE KELD   |          41 |      0.3061 | [3, 12, 15]                                           |
| FIRST PRICE |          41 |      0.3061 | [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 16, 17, 18, 19] |
| AQUA D'OR   |          41 |      0.3061 | [1, 2, 7, 11, 12, 13, 14, 15, 19]                     |
| KILDEVÆLD   |          41 |      0.3061 | [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18] |
