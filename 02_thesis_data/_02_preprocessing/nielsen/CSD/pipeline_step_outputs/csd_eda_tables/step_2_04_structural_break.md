## Top 3 Break Candidates by Chow F-statistic

- Chow test for a structural break in the aggregate series. The null hypothesis is that the same relationship holds before and after the candidate break date (Chow, 1960).
- A low p-value indicates that the mean or variance of the series shifts at that date. This bears directly on the validity of the temporal split, since a break inside the evaluation window means the held-out period is not drawn from the same regime as the training period.
- The three strongest candidates are reported rather than a single verdict. With one series and many candidate dates, the procedure is exploratory and subject to multiple-comparisons inflation, so these p-values are not adjusted significance levels.

| date    |   chow_f |   chow_p |   mean_ratio |   std_ratio |
|:--------|---------:|---------:|-------------:|------------:|
| 2025-03 |   9.0310 |   0.0044 |       1.1860 |      0.8230 |
| 2025-05 |   8.8100 |   0.0048 |       1.1880 |      0.8740 |
| 2024-12 |   8.1910 |   0.0064 |       1.1750 |      1.0570 |
