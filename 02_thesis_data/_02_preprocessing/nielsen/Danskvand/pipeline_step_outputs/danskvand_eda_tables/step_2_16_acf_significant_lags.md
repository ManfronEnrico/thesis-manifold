## Significant ACF Lags per Brand

- Lags whose autocorrelation exceeds the 95% band (+/-1.96/sqrt(n)) under the null of no autocorrelation -- the standard Box-Jenkins reading of an ACF plot (Box & Jenkins, 1970).
- Lags significant in at least half of the top 5 brands: [1, 2, 4, 6, 7, 10, 11, 12, 13, 15]. A lag clearing the band for one brand is noise; one clearing it across the majority is structure worth a feature.
- A spike at lag 12 indicates annual seasonality; spikes at 1-3 indicate short-run momentum. Both are what the lag features exist to capture.
- Computed on log1p(target) so these lags describe the series the model is actually fitted to.
- Evidence only -- LAGS is derived in step 3 (DEC-EDA-SPLIT). This figure is the justification for whatever that step selects.

| brand       |   n_periods |   conf_band | significant_lags                                      |
|:------------|------------:|------------:|:------------------------------------------------------|
| HARBOE      |          41 |      0.3061 | [1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 15]                |
| BLUE KELD   |          41 |      0.3061 | [3, 12, 15]                                           |
| FIRST PRICE |          41 |      0.3061 | [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 16, 17, 18, 19] |
| AQUA D'OR   |          41 |      0.3061 | [1, 2, 7, 11, 12, 13, 14, 15, 19]                     |
| KILDEVÆLD   |          41 |      0.3061 | [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18] |
