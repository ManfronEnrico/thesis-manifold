## Correlation with sales_units

- Pearson and Spearman correlation of each measure with the forecast target. Pearson quantifies linear association; Spearman quantifies monotone association between ranks.
- A large absolute difference between the two coefficients indicates a relationship that is monotone but not linear, identifying measures for which a transformation is more appropriate than inclusion in raw form.
- The rank-based coefficient is the more robust of the two for this data, since the target is right-skewed and the product-moment correlation is sensitive to the resulting extreme values.
- These correlations are contemporaneous. The measures are observed in the same month as the target, so a high coefficient does not establish predictive value at a one-month forecast horizon.
- Association reported here is descriptive and does not identify a causal relationship between any measure and sales.

| column                                       |   pearson_r |   spearman_r |   abs_delta | non_linear   |
|:---------------------------------------------|------------:|-------------:|------------:|:-------------|
| sales_value                                  |      0.9967 |       0.9927 |      0.0041 | False        |
| baseline_sales_units                         |      0.9918 |       0.9847 |      0.0071 | False        |
| promo_units                                  |      0.9890 |       0.9688 |      0.0202 | False        |
| sales_value_any_promo                        |      0.9876 |       0.9642 |      0.0235 | False        |
| baseline_sales_units_any_promo               |      0.9837 |       0.9605 |      0.0232 | False        |
| baseline_sales_value_any_promo               |      0.9820 |       0.9575 |      0.0245 | False        |
| sales_units_any_tpr                          |      0.9706 |       0.9388 |      0.0318 | False        |
| sales_liters                                 |      0.9688 |       0.9953 |      0.0264 | False        |
| sales_in_liters_any_promo                    |      0.9680 |       0.9665 |      0.0015 | False        |
| baseline_sales_in_liters_any_promo           |      0.9541 |       0.9582 |      0.0041 | False        |
| baseline_sales_in_liters                     |      0.9466 |       0.9808 |      0.0343 | False        |
| weighted_distribution_feat_without_disp      |      0.6613 |       0.5865 |      0.0748 | False        |
| weighted_distribution_total_feat             |      0.6349 |       0.5716 |      0.0633 | False        |
| baseline_sales_value                         |      0.5387 |       0.9833 |      0.4446 | True         |
| weighted_distribution_any_tpr                |      0.4997 |       0.7550 |      0.2553 | True         |
| weighted_distribution_any_promo              |      0.4646 |       0.7992 |      0.3345 | True         |
| numeric_distribution                         |      0.4597 |       0.9214 |      0.4617 | True         |
| weighted_distribution_disp_and_feat          |      0.4533 |       0.4209 |      0.0324 | False        |
| weighted_dist                                |      0.4206 |       0.8852 |      0.4645 | True         |
| number_of_items_reach                        |      0.3903 |       0.8983 |      0.5080 | True         |
| avg_number_of_stores_selling_reach           |      0.3900 |       0.8983 |      0.5083 | True         |
| numeric_distribution_reach                   |      0.3896 |       0.8983 |      0.5087 | True         |
| total_weighted_distribution_points_tdp_reach |      0.3592 |       0.8552 |      0.4961 | True         |
| weighted_distribution_reach                  |      0.3592 |       0.8552 |      0.4961 | True         |
| weighted_distribution_any_disp               |      0.3289 |       0.7139 |      0.3850 | True         |
| weighted_distribution_disp_without_feat      |      0.2631 |       0.6856 |      0.4225 | True         |
| avg_no_of_items_per_store_reach              |     -0.0080 |       0.5429 |      0.5509 | True         |
| universe_number_of_stores                    |      0.0018 |      -0.0890 |      0.0907 | False        |
