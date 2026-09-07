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
| weighted_dist                                | weighted_distribution_reach                  |      0.9883 |
| weighted_dist                                | total_weighted_distribution_points_tdp_reach |      0.9883 |
| numeric_distribution                         | numeric_distribution_reach                   |      0.9856 |
| numeric_distribution                         | number_of_items_reach                        |      0.9855 |
| numeric_distribution                         | avg_number_of_stores_selling_reach           |      0.9854 |
| numeric_distribution_reach                   | weighted_distribution_reach                  |      0.9851 |
| numeric_distribution_reach                   | total_weighted_distribution_points_tdp_reach |      0.9851 |
| numeric_distribution                         | weighted_dist                                |      0.9850 |
| total_weighted_distribution_points_tdp_reach | avg_number_of_stores_selling_reach           |      0.9846 |
| total_weighted_distribution_points_tdp_reach | number_of_items_reach                        |      0.9846 |
| weighted_distribution_reach                  | avg_number_of_stores_selling_reach           |      0.9846 |
| weighted_distribution_reach                  | number_of_items_reach                        |      0.9846 |
| numeric_distribution_reach                   | weighted_dist                                |      0.9809 |
| weighted_dist                                | number_of_items_reach                        |      0.9805 |
| weighted_dist                                | avg_number_of_stores_selling_reach           |      0.9804 |
| sales_liters                                 | sales_units                                  |      0.9799 |
| numeric_distribution                         | total_weighted_distribution_points_tdp_reach |      0.9640 |
| numeric_distribution                         | weighted_distribution_reach                  |      0.9640 |
| sales_value                                  | sales_units                                  |      0.9162 |
| sales_value                                  | sales_liters                                 |      0.9074 |
