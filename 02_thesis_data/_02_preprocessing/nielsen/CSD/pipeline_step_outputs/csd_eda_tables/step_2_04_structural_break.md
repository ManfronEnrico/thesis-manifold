## Top 3 Break Candidates by Chow F-statistic

- Chow test for a structural break in the aggregate series: the null is that the same relationship holds before and after the candidate date (Chow, 1960).
- A low p-value indicates the series mean/variance shifts at that point. That matters for the split, because a break inside the test window means the test period is not drawn from the training regime.
- Reported as the three strongest candidates rather than one verdict: with a single series and many candidate dates this is exploratory, and the multiple-comparisons problem is real.

| date    |   chow_f |   chow_p |   mean_ratio |   std_ratio |
|:--------|---------:|---------:|-------------:|------------:|
| 2025-03 |   9.0310 |   0.0044 |       1.1860 |      0.8230 |
| 2025-05 |   8.8100 |   0.0048 |       1.1880 |      0.8740 |
| 2024-12 |   8.1910 |   0.0064 |       1.1750 |      1.0570 |
