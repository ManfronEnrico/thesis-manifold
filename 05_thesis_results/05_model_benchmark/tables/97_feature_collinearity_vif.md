**Variance inflation factors by feature and category.** VIF computed on the log-scaled, standardised design matrix.

| Feature          | CSD   | RTD   | danskvand   | energidrikke   |
|:-----------------|:------|:------|:------------|:---------------|
| days_in_month    | inf   | inf   | inf         | inf            |
| n_holidays       | inf   | inf   | inf         | inf            |
| non_holiday_days | inf   | inf   | inf         | inf            |
| rolling_mean_4   | 234.0 | 227.5 | 212.1       | 256.1          |
| month            | 105.0 | 28.7  | 17.2        | 44.8           |
| quarter          | 100.1 | 28.5  | 17.3        | 49.5           |
| rolling_std_4    | 50.9  | 33.2  | 48.8        | 59.2           |
| lag_1            | 39.3  | 40.8  | 25.0        | 40.3           |
| lag_2            | 36.9  | 40.5  | 24.0        | 35.3           |
| lag_3            | 36.2  | 40.3  | 20.1        | 32.6           |
| rolling_mean_13  | 31.8  | 17.5  | 34.7        | 16.0           |
| lag_4            | 27.3  | 26.4  | 15.9        | 20.6           |
| lag_8            | 12.4  | 8.7   | 10.6        | 6.3            |
| lag_13           | 7.4   | 4.4   | 7.8         | 3.5            |
| peak_month       | 4.9   | 3.2   | 1.4         | 2.9            |
| promo_intensity  | 2.0   |       |             | 2.1            |

*Note.* 'inf' marks an exact linear dependency: non_holiday_days is days_in_month minus n_holidays by construction. Higher values indicate a feature more fully determined by the others. The autoregressive lag and rolling-mean features are correlated by construction, since each is computed from the same series.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

12 exact dependencies across all categories.

NO THRESHOLD IS ASSERTED IN THE CAPTION, deliberately. The conventional 5 and 10 cut-offs were attributed in an earlier draft to a source not held in the project library; the attribution was removed. See writing-notes/unverified-claims-to-check.md item 1 before putting any numeric threshold in prose.

Measured consequence: dropping the exact dependency changed test WMAPE by less than 0.01pp in all eight cells tested. Report the collinearity; do not claim it explains accuracy.
