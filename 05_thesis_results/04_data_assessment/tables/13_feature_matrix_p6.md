**Composition of the modelling matrix - part 6 of 6.** Rows 46 to 54 of 54. Every column of the CSD feature matrix at a 3-month forecast horizon, with the role it plays in training. The matrix holds 4,370 brand-months across 95 brands in 54 columns, of which 34 are model inputs.

| Column                         | Role                       | Type    | Populated   |
|:-------------------------------|:---------------------------|:--------|:------------|
| baseline_sales_units_any_promo | Excluded - contemporaneous | float64 | 87%         |
| baseline_sales_value           | Excluded - contemporaneous | float64 | 87%         |
| baseline_sales_value_any_promo | Excluded - contemporaneous | float64 | 87%         |
| promo_units                    | Excluded - contemporaneous | float64 | 100%        |
| sales_in_liters_any_promo      | Excluded - contemporaneous | float64 | 87%         |
| sales_liters                   | Excluded - contemporaneous | float64 | 100%        |
| sales_units_any_tpr            | Excluded - contemporaneous | float64 | 87%         |
| sales_value                    | Excluded - contemporaneous | float64 | 100%        |
| sales_value_any_promo          | Excluded - contemporaneous | float64 | 87%         |

*Note.* The target is sales_units, modelled as log1p and inverted for reporting. Splits are chronological: training 2022-10 to 2025-05, validation 2025-06 to 2025-12, test 2026-01 to 2026-07. The 12 columns marked excluded are same-period sales and baseline measures, retained so a prediction can be traced back to the observation it was made from; they are not available to the model, which would otherwise observe the quantity it is asked to predict. Populated is the share of rows with a value: autoregressive features are empty for a brand's earliest months by construction. Columns are ordered by role, so the grouping continues across parts.
