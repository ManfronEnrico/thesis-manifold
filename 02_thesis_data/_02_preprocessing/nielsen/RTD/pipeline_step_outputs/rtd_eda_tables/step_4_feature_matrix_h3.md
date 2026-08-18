## Feature matrix construction (RTD, horizon 3 month(s))

- Row counts at each stage of matrix construction. The calendar fill completes each brand's month grid so that a lag refers to a fixed interval rather than to the previous observed month.
- Brands below the minimum series length are excluded before feature construction. The threshold is not a quality judgement: a shorter series yields no observation whose lag features are defined under this specification.
- Every parameter above is read from the step 3 contract for this category and horizon. This step derives none of them, so the matrix and the recorded parameters cannot disagree.

| quantity                 | value      |
|:-------------------------|:-----------|
| rows_in                  | 2509       |
| brands_in                | 101        |
| rows_after_calendar_fill | 4141       |
| brands_after_min_periods | 62         |
| rows_after_min_periods   | 2542       |
| rows_engineered          | 2542       |
| columns_engineered       | 45         |
| min_periods_applied      | 17         |
| holiday_months_applied   | [5, 6, 12] |
