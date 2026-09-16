**Composition of the modelling matrix - part 1 of 6.** Rows 1 to 9 of 54. Every column of the CSD feature matrix at a 3-month forecast horizon, with the role it plays in training. The matrix holds 4,370 brand-months across 95 brands in 54 columns, of which 34 are model inputs.

| Column          | Role                     | Type           | Populated   |
|:----------------|:-------------------------|:---------------|:------------|
| brand           | Identifier               | str            | 100%        |
| date            | Identifier               | datetime64[us] | 100%        |
| sales_units     | Target                   | float64        | 100%        |
| log_sales_units | Target, transformed      | float64        | 100%        |
| split           | Split label              | str            | 100%        |
| period_index    | Ordering                 | int32          | 100%        |
| lag_1           | Feature - autoregressive | float64        | 93%         |
| lag_13          | Feature - autoregressive | float64        | 67%         |
| lag_2           | Feature - autoregressive | float64        | 91%         |

*Note.* The target is sales_units, modelled as log1p and inverted for reporting. Splits are chronological: training 2022-10 to 2025-05, validation 2025-06 to 2025-12, test 2026-01 to 2026-07. The 12 columns marked excluded are same-period sales and baseline measures, retained so a prediction can be traced back to the observation it was made from; they are not available to the model, which would otherwise observe the quantity it is asked to predict. Populated is the share of rows with a value: autoregressive features are empty for a brand's earliest months by construction. Columns are ordered by role, so the grouping continues across parts.
