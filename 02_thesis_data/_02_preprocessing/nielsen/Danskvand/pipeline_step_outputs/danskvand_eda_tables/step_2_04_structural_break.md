## Top 3 Break Candidates by Chow F-statistic

- Chow test for a structural break in the aggregate series: the null is that the same relationship holds before and after the candidate date (Chow, 1960).
- A low p-value indicates the series mean/variance shifts at that point. That matters for the split, because a break inside the test window means the test period is not drawn from the training regime.
- Reported as the three strongest candidates rather than one verdict: with a single series and many candidate dates this is exploratory, and the multiple-comparisons problem is real.

| date    |   chow_f |   chow_p |   mean_ratio |   std_ratio |
|:--------|---------:|---------:|-------------:|------------:|
| 2025-06 |  13.8920 |   0.0006 |       1.3270 |      1.2870 |
| 2025-05 |  12.6210 |   0.0010 |       1.3110 |      1.2550 |
| 2025-07 |  10.3890 |   0.0026 |       1.2930 |      1.2570 |
