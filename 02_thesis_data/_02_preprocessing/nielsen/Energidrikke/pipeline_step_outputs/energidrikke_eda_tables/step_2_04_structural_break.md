## Top 3 Break Candidates by Chow F-statistic

- Chow test for a structural break in the aggregate series: the null is that the same relationship holds before and after the candidate date (Chow, 1960).
- A low p-value indicates the series mean/variance shifts at that point. That matters for the split, because a break inside the test window means the test period is not drawn from the training regime.
- Reported as the three strongest candidates rather than one verdict: with a single series and many candidate dates this is exploratory, and the multiple-comparisons problem is real.

| date    |   chow_f |   chow_p |   mean_ratio |   std_ratio |
|:--------|---------:|---------:|-------------:|------------:|
| 2025-03 |  19.8040 |   0.0001 |       1.2360 |      1.2310 |
| 2025-05 |  17.1780 |   0.0002 |       1.2280 |      1.2230 |
| 2025-06 |  16.7410 |   0.0002 |       1.2290 |      1.2610 |
