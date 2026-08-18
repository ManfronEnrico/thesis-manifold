## Feature matrix construction (Energidrikke, horizon 3 month(s))

- Row counts at each stage of matrix construction. The calendar fill completes each brand's month grid so that a lag refers to a fixed interval rather than to the previous observed month.
- Brands below the minimum series length are excluded before feature construction. The threshold is not a quality judgement: a shorter series yields no observation whose lag features are defined under this specification.
- Every parameter above is read from the step 3 contract for this category and horizon. This step derives none of them, so the matrix and the recorded parameters cannot disagree.

| quantity                 | value     |
|:-------------------------|:----------|
| rows_in                  | 1702      |
| brands_in                | 68        |
| rows_after_calendar_fill | 2924      |
| brands_after_min_periods | 44        |
| rows_after_min_periods   | 1892      |
| rows_engineered          | 1892      |
| columns_engineered       | 47        |
| min_periods_applied      | 17        |
| peak_months_applied      | [3, 6, 9] |
