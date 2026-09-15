**Composition of the modelling matrix - part 3 of 6.** Rows 19 to 27 of 54. Every column of the CSD feature matrix at a 3-month forecast horizon, with the role it plays in training. The matrix holds 4,370 brand-months across 95 brands in 54 columns, of which 34 are model inputs.

| Column                                       | Role                   | Type    | Populated   |
|:---------------------------------------------|:-----------------------|:--------|:------------|
| non_holiday_days                             | Feature - calendar     | float64 | 100%        |
| peak_month                                   | Feature - calendar     | int64   | 100%        |
| quarter                                      | Feature - calendar     | int32   | 100%        |
| avg_no_of_items_per_store_reach              | Feature - distribution | float64 | 87%         |
| avg_number_of_stores_selling_reach           | Feature - distribution | float64 | 87%         |
| number_of_items_reach                        | Feature - distribution | float64 | 87%         |
| numeric_distribution                         | Feature - distribution | float64 | 87%         |
| numeric_distribution_reach                   | Feature - distribution | float64 | 87%         |
| total_weighted_distribution_points_tdp_reach | Feature - distribution | float64 | 87%         |

*Note.* The target is sales_units, modelled as log1p and inverted for reporting. Splits are chronological: training 2022-10 to 2025-05, validation 2025-06 to 2025-12, test 2026-01 to 2026-07. The 12 columns marked excluded are same-period sales and baseline measures, retained so a prediction can be traced back to the observation it was made from; they are not available to the model, which would otherwise observe the quantity it is asked to predict. Populated is the share of rows with a value: autoregressive features are empty for a brand's earliest months by construction. Columns are ordered by role, so the grouping continues across parts.
