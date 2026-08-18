## Near-Duplicate Column Pairs (|r| > 0.9)

- Pairs of measures whose absolute Pearson correlation exceeds 0.9, the conventional threshold for treating two variables as carrying substantially equivalent information.
- Retaining both members of such a pair introduces collinearity without adding explanatory content.
- Collinearity inflates the sampling variance of coefficient estimates in linear models. Tree-based ensembles are robust to it in terms of predictive accuracy, but distribute split importance across the correlated measures, which renders variable-importance rankings unreliable.
- High correlation between two measures does not by itself determine which of them to retain; that requires their definitions and their individual association with the target.

| column_a                                     | column_b                                     |   pearson_r |
|:---------------------------------------------|:---------------------------------------------|------------:|
| weighted_distribution_reach                  | total_weighted_distribution_points_tdp_reach |      1.0000 |
| number_of_items_reach                        | avg_number_of_stores_selling_reach           |      1.0000 |
| numeric_distribution_reach                   | number_of_items_reach                        |      0.9999 |
| numeric_distribution_reach                   | avg_number_of_stores_selling_reach           |      0.9999 |
| baseline_sales_value_any_promo               | baseline_sales_units_any_promo               |      0.9954 |
| sales_value                                  | sales_value_any_promo                        |      0.9936 |
| sales_units                                  | sales_in_liters_any_promo                    |      0.9935 |
| sales_liters                                 | sales_in_liters_any_promo                    |      0.9920 |
| sales_liters                                 | sales_units                                  |      0.9909 |
| baseline_sales_value                         | baseline_sales_units                         |      0.9886 |
| sales_units                                  | sales_value_any_promo                        |      0.9860 |
| sales_in_liters_any_promo                    | sales_units_any_tpr                          |      0.9856 |
| sales_liters                                 | sales_value_any_promo                        |      0.9810 |
| sales_value                                  | sales_liters                                 |      0.9777 |
| sales_value                                  | sales_units                                  |      0.9762 |
| sales_value_any_promo                        | sales_in_liters_any_promo                    |      0.9761 |
| weighted_dist                                | total_weighted_distribution_points_tdp_reach |      0.9743 |
| weighted_dist                                | weighted_distribution_reach                  |      0.9743 |
| sales_units                                  | sales_units_any_tpr                          |      0.9736 |
| baseline_sales_units                         | baseline_sales_units_any_promo               |      0.9700 |
| baseline_sales_units                         | baseline_sales_value_any_promo               |      0.9690 |
| numeric_distribution                         | number_of_items_reach                        |      0.9677 |
| numeric_distribution                         | avg_number_of_stores_selling_reach           |      0.9677 |
| numeric_distribution                         | numeric_distribution_reach                   |      0.9674 |
| baseline_sales_value                         | baseline_sales_in_liters_any_promo           |      0.9666 |
| baseline_sales_value                         | baseline_sales_value_any_promo               |      0.9631 |
| baseline_sales_units                         | baseline_sales_in_liters_any_promo           |      0.9620 |
| baseline_sales_value_any_promo               | baseline_sales_in_liters_any_promo           |      0.9620 |
| sales_liters                                 | sales_units_any_tpr                          |      0.9617 |
| sales_value                                  | sales_in_liters_any_promo                    |      0.9596 |
| baseline_sales_value                         | baseline_sales_units_any_promo               |      0.9553 |
| baseline_sales_in_liters_any_promo           | baseline_sales_units_any_promo               |      0.9537 |
| weighted_distribution_disp_without_feat      | weighted_distribution_any_disp               |      0.9413 |
| sales_value_any_promo                        | sales_units_any_tpr                          |      0.9386 |
| numeric_distribution_reach                   | total_weighted_distribution_points_tdp_reach |      0.9370 |
| numeric_distribution_reach                   | weighted_distribution_reach                  |      0.9370 |
| total_weighted_distribution_points_tdp_reach | avg_number_of_stores_selling_reach           |      0.9366 |
| total_weighted_distribution_points_tdp_reach | number_of_items_reach                        |      0.9366 |
| weighted_distribution_reach                  | avg_number_of_stores_selling_reach           |      0.9366 |
| weighted_distribution_reach                  | number_of_items_reach                        |      0.9366 |
| weighted_distribution_feat_without_disp      | weighted_distribution_total_feat             |      0.9362 |
| sales_value                                  | baseline_sales_value_any_promo               |      0.9269 |
| numeric_distribution_reach                   | weighted_dist                                |      0.9251 |
| weighted_dist                                | avg_number_of_stores_selling_reach           |      0.9250 |
| weighted_dist                                | number_of_items_reach                        |      0.9250 |
| sales_value                                  | baseline_sales_value                         |      0.9195 |
| sales_value                                  | baseline_sales_units                         |      0.9193 |
| sales_value                                  | baseline_sales_units_any_promo               |      0.9188 |
| numeric_distribution                         | weighted_dist                                |      0.9148 |
| sales_value                                  | sales_units_any_tpr                          |      0.9102 |
| baseline_sales_value_any_promo               | sales_value_any_promo                        |      0.9061 |
