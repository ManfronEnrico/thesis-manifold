## Correlation with sales_units

- Pearson and Spearman correlation of each measure with the forecast target. Pearson quantifies linear association; Spearman quantifies monotone association between ranks.
- A large absolute difference between the two coefficients indicates a relationship that is monotone but not linear, identifying measures for which a transformation is more appropriate than inclusion in raw form.
- The rank-based coefficient is the more robust of the two for this data, since the target is right-skewed and the product-moment correlation is sensitive to the resulting extreme values.
- These correlations are contemporaneous. The measures are observed in the same month as the target, so a high coefficient does not establish predictive value at a one-month forecast horizon.
- Association reported here is descriptive and does not identify a causal relationship between any measure and sales.

| column                                       |   pearson_r |   spearman_r |   abs_delta | non_linear   |
|:---------------------------------------------|------------:|-------------:|------------:|:-------------|
| baseline_sales_in_liters                     |      0.9741 |       0.9839 |      0.0098 | False        |
| baseline_sales_units                         |      0.9600 |       0.9900 |      0.0300 | False        |
| sales_liters                                 |      0.9539 |       0.9903 |      0.0364 | False        |
| promo_units                                  |      0.9410 |       0.9369 |      0.0040 | False        |
| sales_units_any_tpr                          |      0.9273 |       0.9077 |      0.0196 | False        |
| baseline_sales_value                         |      0.9142 |       0.9795 |      0.0653 | False        |
| baseline_sales_units_any_promo               |      0.9132 |       0.9320 |      0.0188 | False        |
| sales_value                                  |      0.8966 |       0.9845 |      0.0878 | False        |
| baseline_sales_in_liters_any_promo           |      0.8564 |       0.9250 |      0.0686 | False        |
| sales_in_liters_any_promo                    |      0.8460 |       0.9286 |      0.0825 | False        |
| sales_value_any_promo                        |      0.8253 |       0.9247 |      0.0994 | False        |
| baseline_sales_value_any_promo               |      0.8232 |       0.9211 |      0.0978 | False        |
| weighted_distribution_total_feat             |      0.4684 |       0.6367 |      0.1683 | True         |
| numeric_distribution                         |      0.4631 |       0.9223 |      0.4591 | True         |
| weighted_distribution_disp_and_feat          |      0.4398 |       0.5103 |      0.0705 | False        |
| weighted_distribution_feat_without_disp      |      0.4392 |       0.6496 |      0.2104 | True         |
| weighted_dist                                |      0.4302 |       0.9076 |      0.4774 | True         |
| numeric_distribution_reach                   |      0.4029 |       0.9050 |      0.5021 | True         |
| number_of_items_reach                        |      0.4028 |       0.9050 |      0.5022 | True         |
| avg_number_of_stores_selling_reach           |      0.4024 |       0.9050 |      0.5026 | True         |
| weighted_distribution_reach                  |      0.3857 |       0.8919 |      0.5062 | True         |
| total_weighted_distribution_points_tdp_reach |      0.3857 |       0.8919 |      0.5062 | True         |
| weighted_distribution_any_promo              |      0.3551 |       0.8085 |      0.4533 | True         |
| weighted_distribution_any_disp               |      0.3191 |       0.7254 |      0.4062 | True         |
| weighted_distribution_any_tpr                |      0.3101 |       0.7775 |      0.4674 | True         |
| weighted_distribution_disp_without_feat      |      0.2332 |       0.7057 |      0.4725 | True         |
| universe_number_of_stores                    |      0.0060 |      -0.0194 |      0.0254 | False        |
| avg_no_of_items_per_store_reach              |     -0.0006 |       0.5964 |      0.5970 | True         |
