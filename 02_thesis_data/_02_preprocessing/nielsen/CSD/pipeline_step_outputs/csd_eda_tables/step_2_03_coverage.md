## Coverage

- Observed span and completeness of the panel. Total months is the distinct period count, which bounds every window-based feature: a 12-month rolling mean is undefined in a panel shorter than 12.
- Also bounds the split. Train/validation/test cutoffs are derived proportionally from this span rather than hardcoded, after the hardcoded dates drifted to a 24-27% test share (F25).

| Metric         | Value              |
|:---------------|:-------------------|
| Date Range     | 2022-10 to 2026-07 |
| Total Months   | 46                 |
| Total Rows     | 4,209              |
| Unique Brands  | 142                |
| Avg Rows/Brand | 29.6               |
