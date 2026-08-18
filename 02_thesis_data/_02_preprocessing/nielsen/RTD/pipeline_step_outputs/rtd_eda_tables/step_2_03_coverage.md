## Coverage

- Observed span and completeness of the panel. Total months is the distinct period count, which bounds every window-based feature: a 12-month rolling mean is undefined in a panel shorter than 12.
- Also bounds the split. Train/validation/test cutoffs are derived proportionally from this span rather than hardcoded, after the hardcoded dates drifted to a 24-27% test share (F25).

| Metric         | Value              |
|:---------------|:-------------------|
| Date Range     | 2023-03 to 2026-07 |
| Total Months   | 41                 |
| Total Rows     | 2,509              |
| Unique Brands  | 101                |
| Avg Rows/Brand | 24.8               |
