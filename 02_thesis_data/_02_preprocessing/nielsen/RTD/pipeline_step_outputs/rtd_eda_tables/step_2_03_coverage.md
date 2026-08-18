## Coverage

- Observed temporal span of the panel. The count of distinct months bounds every window-based feature: a twelve-month rolling statistic is undefined in a series shorter than twelve months.
- The span also bounds the train-validation-test partition, since each split must retain enough history for the lag structure to be computable within it.

| Metric         | Value              |
|:---------------|:-------------------|
| Date Range     | 2023-03 to 2026-07 |
| Total Months   | 41                 |
| Total Rows     | 2,509              |
| Unique Brands  | 101                |
| Avg Rows/Brand | 24.8               |
