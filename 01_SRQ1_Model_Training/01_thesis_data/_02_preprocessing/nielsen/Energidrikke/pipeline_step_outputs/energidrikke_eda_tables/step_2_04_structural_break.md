## Top 3 Break Candidates by Chow F-statistic

- Chow test for a structural break in the aggregate series. The null hypothesis is that the same relationship holds before and after the candidate break date (Chow, 1960).
- A low p-value indicates that the mean or variance of the series shifts at that date. This bears directly on the validity of the temporal split, since a break inside the evaluation window means the held-out period is not drawn from the same regime as the training period.
- The three strongest candidates are reported rather than a single verdict. With one series and many candidate dates, the procedure is exploratory and subject to multiple-comparisons inflation, so these p-values are not adjusted significance levels.

| date    |   chow_f |   chow_p |   mean_ratio |   std_ratio |
|:--------|---------:|---------:|-------------:|------------:|
| 2025-03 |  19.8040 |   0.0001 |       1.2360 |      1.2310 |
| 2025-05 |  17.1780 |   0.0002 |       1.2280 |      1.2230 |
| 2025-06 |  16.7410 |   0.0002 |       1.2290 |      1.2610 |
