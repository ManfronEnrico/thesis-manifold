## Correlation with sales_units

- Pearson measures linear association; Spearman measures monotone association on ranks. Reporting both is what makes the comparison in the next bullet possible.
- abs_delta above 0.1 flags a relationship that is monotone but not linear -- a candidate for transformation rather than a raw feature. 16 column(s) flagged here.
- Spearman is the more trustworthy of the two on this data: the target is right-skewed (see 3.02 and 3.15) and Pearson is sensitive to the resulting outliers.
- These correlations are contemporaneous, not predictive: the columns are measured in the same month as the target, so a high value does not by itself establish forecasting value at t+1.
- Descriptive only. No feature is selected or dropped here; the contract is step 3's output (DEC-EDA-SPLIT).

| column                                       |   pearson_r |   spearman_r |   abs_delta | non_linear   |
|:---------------------------------------------|------------:|-------------:|------------:|:-------------|
| sales_in_liters_any_promo                    |      0.9935 |       0.9208 |      0.0726 | False        |
| sales_liters                                 |      0.9909 |       0.9828 |      0.0082 | False        |
| sales_value_any_promo                        |      0.9860 |       0.9133 |      0.0726 | False        |
| sales_value                                  |      0.9762 |       0.9675 |      0.0087 | False        |
| sales_units_any_tpr                          |      0.9736 |       0.8922 |      0.0814 | False        |
| baseline_sales_value_any_promo               |      0.8732 |       0.9024 |      0.0291 | False        |
| baseline_sales_units_any_promo               |      0.8699 |       0.9142 |      0.0443 | False        |
| baseline_sales_units                         |      0.8663 |       0.9866 |      0.1203 | True         |
| baseline_sales_value                         |      0.8590 |       0.9569 |      0.0979 | False        |
| baseline_sales_in_liters_any_promo           |      0.8351 |       0.9076 |      0.0726 | False        |
| weighted_distribution_any_tpr                |      0.7302 |       0.7764 |      0.0462 | False        |
| weighted_distribution_any_promo              |      0.6421 |       0.8319 |      0.1898 | True         |
| numeric_distribution                         |      0.5623 |       0.9451 |      0.3829 | True         |
| weighted_distribution_any_disp               |      0.5307 |       0.7520 |      0.2214 | True         |
| number_of_items_reach                        |      0.5062 |       0.9284 |      0.4222 | True         |
| avg_number_of_stores_selling_reach           |      0.5060 |       0.9284 |      0.4223 | True         |
| numeric_distribution_reach                   |      0.5051 |       0.9282 |      0.4230 | True         |
| weighted_dist                                |      0.4766 |       0.9205 |      0.4439 | True         |
| weighted_distribution_total_feat             |      0.4552 |       0.6711 |      0.2159 | True         |
| weighted_distribution_feat_wo_disp           |      0.4391 |       0.6563 |      0.2172 | True         |
| weighted_distribution_disp_wo_feat           |      0.4350 |       0.7307 |      0.2957 | True         |
| total_weighted_distribution_points_tdp_reach |      0.4133 |       0.9068 |      0.4935 | True         |
| weighted_distribution_reach                  |      0.4133 |       0.9068 |      0.4935 | True         |
| weighted_distribution_disp_and_feat          |      0.4063 |       0.5902 |      0.1839 | True         |
| baseline_sales_in_liters                     |      0.3287 |       0.9671 |      0.6384 | True         |
| avg_no_of_items_per_store_reach              |     -0.0082 |       0.5313 |      0.5395 | True         |
| universe_number_of_stores                    |      0.0070 |      -0.0079 |      0.0149 | False        |
