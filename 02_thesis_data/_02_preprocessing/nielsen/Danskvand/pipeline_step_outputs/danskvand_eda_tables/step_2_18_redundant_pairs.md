## Near-Duplicate Column Pairs (|r| > 0.9)

- Column pairs correlating above 0.9 carry substantially the same information; keeping both adds collinearity without adding signal.
- The 0.9 threshold is conventional for near-duplicate detection and is deliberately stricter than the 0.756 weighted_dist correlation P0036 F7 tracks -- pairs listed here are a stronger claim than that one.
- Collinearity inflates coefficient variance in linear models. Tree ensembles tolerate it but split their importance across the duplicates, which makes the resulting importance ranking misleading.
- Listed for step 3 to act on, not pruned here.

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
