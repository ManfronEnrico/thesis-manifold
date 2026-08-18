## Feature matrix construction (Danskvand, horizon 1 month(s))

- Row counts at each stage of matrix construction. The calendar fill completes each brand's month grid so that a lag refers to a fixed interval rather than to the previous observed month.
- Brands below the minimum series length are excluded before feature construction. The threshold is not a quality judgement: a shorter series yields no observation whose lag features are defined under this specification.
- Every parameter above is read from the step 3 contract for this category and horizon. This step derives none of them, so the matrix and the recorded parameters cannot disagree.

| quantity                 | value        |
|:-------------------------|:-------------|
| rows_in                  | 1225         |
| brands_in                | 55           |
| rows_after_calendar_fill | 2255         |
| brands_after_min_periods | 30           |
| rows_after_min_periods   | 1230         |
| rows_engineered          | 1230         |
| columns_engineered       | 31           |
| min_periods_applied      | 15           |
| peak_months_applied      | [6, 7, 8, 9] |
