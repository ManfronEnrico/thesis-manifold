**Composition of the modelling matrix - part 5 of 6.** Rows 37 to 45 of 54. Every column of the CSD feature matrix at a 3-month forecast horizon, with the role it plays in training. The matrix holds 4,370 brand-months across 95 brands in 54 columns, of which 34 are model inputs.

| Column                                  | Role                       | Type    | Populated   |
|:----------------------------------------|:---------------------------|:--------|:------------|
| weighted_distribution_feat_without_disp | Feature - promotional      | float64 | 20%         |
| weighted_distribution_total_feat        | Feature - promotional      | float64 | 20%         |
| zero_run_flag                           | Feature - series quality   | float64 | 93%         |
| zero_run_length                         | Feature - series quality   | float64 | 93%         |
| period_month                            | Raw date part, superseded  | int32   | 100%        |
| period_year                             | Raw date part, superseded  | int32   | 100%        |
| baseline_sales_in_liters                | Excluded - contemporaneous | float64 | 87%         |
| baseline_sales_in_liters_any_promo      | Excluded - contemporaneous | float64 | 87%         |
| baseline_sales_units                    | Excluded - contemporaneous | float64 | 87%         |

*Note.* The target is sales_units, modelled as log1p and inverted for reporting. Splits are chronological: training 2022-10 to 2025-05, validation 2025-06 to 2025-12, test 2026-01 to 2026-07. The 12 columns marked excluded are same-period sales and baseline measures, retained so a prediction can be traced back to the observation it was made from; they are not available to the model, which would otherwise observe the quantity it is asked to predict. Populated is the share of rows with a value: autoregressive features are empty for a brand's earliest months by construction. Columns are ordered by role, so the grouping continues across parts.
