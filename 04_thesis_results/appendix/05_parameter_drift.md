**Effect of holding hyperparameters fixed as data accrues.** Forecast error using stored hyperparameters against error after repeating the hyperparameter search, at successive monthly forecast origins. A positive difference indicates that the stored parameters performed worse. The lower error in each row is shown in bold italic.

| Forecast origin   |   Training rows | WMAPE, stored parameters (%)   | WMAPE, re-tuned (%)   |   Difference (pp) |
|:------------------|----------------:|:-------------------------------|:----------------------|------------------:|
| 2026-02-01        |           2,660 | ***14.26***                    | 14.82                 |             -0.56 |
| 2026-03-01        |           2,755 | 15.58                          | ***10.95***           |              4.63 |
| 2026-04-01        |           2,850 | 13.49                          | ***11.44***           |              2.05 |
| 2026-05-01        |           2,945 | ***11.69***                    | 14.49                 |             -2.8  |
| 2026-06-01        |           3,040 | ***12.57***                    | 14.49                 |             -1.92 |

*Note.* The mean difference across origins is +0.28 percentage points, and individual origins fall on both sides of zero. Over the period observed there is therefore no detectable penalty from holding hyperparameters fixed. The window is short and the number of origins small, so this should be read as an absence of evidence at this horizon rather than as evidence that no drift occurs over longer ones.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

INCONCLUSIVE -- do not cite the +0.414 pp/month slope. Carried by two opposite outliers (month 4: -3.74, month 7: +3.60) on n=7, and three months are exactly 0.00 because re-tuning rediscovered the frozen num_leaves=93. Recommend refit-per-query + SCHEDULED re-tune, cadence not optimised. F31.

Kept SEPARATE from the merged resource table: unit is pp of forecast error across origins, not time/memory.
