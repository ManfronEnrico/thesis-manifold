## Correlation with sales_units

- Pearson and Spearman correlation of each measure with the forecast target. Pearson quantifies linear association; Spearman quantifies monotone association between ranks.
- A large absolute difference between the two coefficients indicates a relationship that is monotone but not linear, identifying measures for which a transformation is more appropriate than inclusion in raw form.
- The rank-based coefficient is the more robust of the two for this data, since the target is right-skewed and the product-moment correlation is sensitive to the resulting extreme values.
- These correlations are contemporaneous. The measures are observed in the same month as the target, so a high coefficient does not establish predictive value at a one-month forecast horizon.
- Association reported here is descriptive and does not identify a causal relationship between any measure and sales.

| column                                       |   pearson_r |   spearman_r |   abs_delta | non_linear   |
|:---------------------------------------------|------------:|-------------:|------------:|:-------------|
| sales_liters                                 |      0.9799 |       0.9894 |      0.0095 | False        |
| sales_value                                  |      0.9162 |       0.9811 |      0.0649 | False        |
| numeric_distribution                         |      0.8042 |       0.9088 |      0.1045 | True         |
| weighted_dist                                |      0.7722 |       0.8911 |      0.1189 | True         |
| number_of_items_reach                        |      0.7634 |       0.8911 |      0.1276 | True         |
| avg_number_of_stores_selling_reach           |      0.7632 |       0.8910 |      0.1278 | True         |
| numeric_distribution_reach                   |      0.7623 |       0.8903 |      0.1279 | True         |
| total_weighted_distribution_points_tdp_reach |      0.7316 |       0.8704 |      0.1389 | True         |
| weighted_distribution_reach                  |      0.7316 |       0.8704 |      0.1389 | True         |
| universe_number_of_stores                    |      0.0313 |       0.0360 |      0.0047 | False        |
| avg_no_of_items_per_store_reach              |      0.0080 |       0.6442 |      0.6362 | True         |
