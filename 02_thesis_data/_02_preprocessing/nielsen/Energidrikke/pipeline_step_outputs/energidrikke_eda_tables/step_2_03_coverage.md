## Coverage

- Observed span and completeness of the panel. Total months is the distinct period count, which bounds every window-based feature: a 12-month rolling mean is undefined in a panel shorter than 12.
- Also bounds the split. Train/validation/test cutoffs are derived proportionally from this span rather than hardcoded, after the hardcoded dates drifted to a 24-27% test share (F25).

| Metric         | Value              |
|:---------------|:-------------------|
| Date Range     | 2023-01 to 2026-07 |
| Total Months   | 43                 |
| Total Rows     | 1,702              |
| Unique Brands  | 68                 |
| Avg Rows/Brand | 25.0               |
