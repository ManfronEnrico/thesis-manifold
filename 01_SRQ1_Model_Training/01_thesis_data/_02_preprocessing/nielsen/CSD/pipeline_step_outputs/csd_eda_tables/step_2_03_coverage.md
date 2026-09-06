## Coverage

- Observed temporal span of the panel. The count of distinct months bounds every window-based feature: a twelve-month rolling statistic is undefined in a series shorter than twelve months.
- The span also bounds the train-validation-test partition, since each split must retain enough history for the lag structure to be computable within it.

| Metric         | Value              |
|:---------------|:-------------------|
| Date Range     | 2022-10 to 2026-07 |
| Total Months   | 46                 |
| Total Rows     | 4,209              |
| Unique Brands  | 142                |
| Avg Rows/Brand | 29.6               |
