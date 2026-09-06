## Coverage

- Observed temporal span of the panel. The count of distinct months bounds every window-based feature: a twelve-month rolling statistic is undefined in a series shorter than twelve months.
- The span also bounds the train-validation-test partition, since each split must retain enough history for the lag structure to be computable within it.

| Metric         | Value              |
|:---------------|:-------------------|
| Date Range     | 2023-01 to 2026-07 |
| Total Months   | 43                 |
| Total Rows     | 1,702              |
| Unique Brands  | 68                 |
| Avg Rows/Brand | 25.0               |
