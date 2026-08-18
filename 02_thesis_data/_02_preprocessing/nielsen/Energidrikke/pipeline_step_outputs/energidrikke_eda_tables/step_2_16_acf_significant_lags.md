## Significant ACF Lags per Brand

- Lags whose autocorrelation exceeds the 95% band (+/-1.96/sqrt(n)) under the null of no autocorrelation -- the standard Box-Jenkins reading of an ACF plot (Box & Jenkins, 1970).
- Lags significant in at least half of the top 5 brands: [1, 2, 3, 6, 9, 10, 12, 15, 18]. A lag clearing the band for one brand is noise; one clearing it across the majority is structure worth a feature.
- A spike at lag 12 indicates annual seasonality; spikes at 1-3 indicate short-run momentum. Both are what the lag features exist to capture.
- Computed on log1p(target) so these lags describe the series the model is actually fitted to.
- Evidence only -- LAGS is derived in step 3 (DEC-EDA-SPLIT). This figure is the justification for whatever that step selects.

| brand              |   n_periods |   conf_band | significant_lags                                    |
|:-------------------|------------:|------------:|:----------------------------------------------------|
| RED BULL           |          43 |      0.2989 | [3, 6, 9, 12, 15, 18]                               |
| MONSTER ENERGY     |          43 |      0.2989 | [1, 2, 3, 6, 9, 10, 12, 15, 18]                     |
| FAXE KONDI BOOSTER |          43 |      0.2989 | [1, 2, 3, 4, 6, 9, 10, 11, 12, 15, 18]              |
| CULT               |          43 |      0.2989 | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] |
| STATE              |          43 |      0.2989 | [1, 2, 3, 6, 9, 12, 18]                             |
