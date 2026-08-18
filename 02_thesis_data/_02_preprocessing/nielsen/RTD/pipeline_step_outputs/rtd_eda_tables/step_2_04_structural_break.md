## Top 3 Break Candidates by Chow F-statistic

- Chow test for a structural break in the aggregate series: the null is that the same relationship holds before and after the candidate date (Chow, 1960).
- A low p-value indicates the series mean/variance shifts at that point. That matters for the split, because a break inside the test window means the test period is not drawn from the training regime.
- Reported as the three strongest candidates rather than one verdict: with a single series and many candidate dates this is exploratory, and the multiple-comparisons problem is real.

| date    |   chow_f |   chow_p |   mean_ratio |   std_ratio |
|:--------|---------:|---------:|-------------:|------------:|
| 2025-12 |   2.6760 |   0.1099 |       1.3580 |      1.2760 |
| 2025-05 |   1.6630 |   0.2048 |       1.2390 |      1.1090 |
| 2026-01 |   1.5470 |   0.2210 |       1.2850 |      1.3250 |
