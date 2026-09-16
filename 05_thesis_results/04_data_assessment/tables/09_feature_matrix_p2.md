**Composition of the modelling matrix - part 2 of 6.** Rows 10 to 18 of 54. Every column of the CSD feature matrix at a 3-month forecast horizon, with the role it plays in training. The matrix holds 4,370 brand-months across 95 brands in 54 columns, of which 34 are model inputs.

| Column          | Role                     | Type    | Populated   |
|:----------------|:-------------------------|:--------|:------------|
| lag_3           | Feature - autoregressive | float64 | 89%         |
| lag_4           | Feature - autoregressive | float64 | 87%         |
| lag_8           | Feature - autoregressive | float64 | 78%         |
| rolling_mean_13 | Feature - autoregressive | float64 | 100%        |
| rolling_mean_4  | Feature - autoregressive | float64 | 96%         |
| rolling_std_4   | Feature - autoregressive | float64 | 100%        |
| days_in_month   | Feature - calendar       | int32   | 100%        |
| month           | Feature - calendar       | int32   | 100%        |
| n_holidays      | Feature - calendar       | float64 | 100%        |

*Note.* The target is sales_units, modelled as log1p and inverted for reporting. Splits are chronological: training 2022-10 to 2025-05, validation 2025-06 to 2025-12, test 2026-01 to 2026-07. The 12 columns marked excluded are same-period sales and baseline measures, retained so a prediction can be traced back to the observation it was made from; they are not available to the model, which would otherwise observe the quantity it is asked to predict. Populated is the share of rows with a value: autoregressive features are empty for a brand's earliest months by construction. Columns are ordered by role, so the grouping continues across parts.
