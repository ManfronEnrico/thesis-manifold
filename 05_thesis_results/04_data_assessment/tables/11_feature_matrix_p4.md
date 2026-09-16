**Composition of the modelling matrix - part 4 of 6.** Rows 28 to 36 of 54. Every column of the CSD feature matrix at a 3-month forecast horizon, with the role it plays in training. The matrix holds 4,370 brand-months across 95 brands in 54 columns, of which 34 are model inputs.

| Column                                  | Role                   | Type    | Populated   |
|:----------------------------------------|:-----------------------|:--------|:------------|
| universe_number_of_stores               | Feature - distribution | float64 | 87%         |
| weighted_dist                           | Feature - distribution | float64 | 100%        |
| weighted_distribution_reach             | Feature - distribution | float64 | 87%         |
| promo_intensity                         | Feature - promotional  | float64 | 93%         |
| weighted_distribution_any_disp          | Feature - promotional  | float64 | 54%         |
| weighted_distribution_any_promo         | Feature - promotional  | float64 | 63%         |
| weighted_distribution_any_tpr           | Feature - promotional  | float64 | 60%         |
| weighted_distribution_disp_and_feat     | Feature - promotional  | float64 | 18%         |
| weighted_distribution_disp_without_feat | Feature - promotional  | float64 | 54%         |

*Note.* The target is sales_units, modelled as log1p and inverted for reporting. Splits are chronological: training 2022-10 to 2025-05, validation 2025-06 to 2025-12, test 2026-01 to 2026-07. The 12 columns marked excluded are same-period sales and baseline measures, retained so a prediction can be traced back to the observation it was made from; they are not available to the model, which would otherwise observe the quantity it is asked to predict. Populated is the share of rows with a value: autoregressive features are empty for a brand's earliest months by construction. Columns are ordered by role, so the grouping continues across parts.
