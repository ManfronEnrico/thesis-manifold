## Skewness Analysis

- Fisher-Pearson skewness per numeric column. Zero is symmetric; positive means a long right tail.
- Thresholds follow Kim (2013): |skew| > 2 indicates substantial departure from normality, 0.5-2 moderate. These bands are the stated basis for the log-transform recommendation, not an eyeball judgement.
- The forecast target's skewness is the empirical case for LOG_TRANSFORM_TARGET; see 3.15 for the same evidence as a distribution curve.
- Skewness is a property of the marginal distribution and says nothing about the time-series structure -- 3.05 and 3.16 cover that.

| feature                                      |   skewness | interpretation                                                                          |
|:---------------------------------------------|-----------:|:----------------------------------------------------------------------------------------|
| sales_value                                  |     5.3550 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| sales_liters                                 |     5.1790 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| sales_units                                  |     5.0000 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| sales_value_any_promo                        |     5.7810 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| sales_in_liters_any_promo                    |     6.0500 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| promo_units                                  |     5.6120 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| sales_units_any_tpr                          |     6.2480 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| baseline_sales_value                         |     5.0830 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| baseline_sales_in_liters                     |     4.7060 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| baseline_sales_units                         |     5.0200 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| baseline_sales_value_any_promo               |     5.5920 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| baseline_sales_in_liters_any_promo           |     5.5180 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| baseline_sales_units_any_promo               |     5.1720 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| numeric_distribution                         |     2.1920 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| numeric_distribution_reach                   |     2.0040 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| weighted_dist                                |     1.9630 | Right-skewed -- log transform justified                                                 |
| weighted_distribution_reach                  |     1.7960 | Right-skewed -- log transform justified                                                 |
| total_weighted_distribution_points_tdp_reach |     1.7960 | Right-skewed -- log transform justified                                                 |
| number_of_items_reach                        |     2.0180 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| avg_number_of_stores_selling_reach           |     2.0200 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| universe_number_of_stores                    |    -0.8640 | Left-skewed (negative)                                                                  |
| avg_no_of_items_per_store_reach              |    37.8920 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| weighted_distribution_any_promo              |     2.4540 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| weighted_distribution_disp_feat              |     1.7720 | Right-skewed -- log transform justified                                                 |
| weighted_distribution_disp_w_o_feat          |     3.5600 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| weighted_distribution_feat_w_o_disp          |     0.7270 | Right-skewed -- log transform justified                                                 |
| weighted_distribution_total_feat             |     0.9730 | Right-skewed -- log transform justified                                                 |
| weighted_distribution_any_disp               |     3.8510 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| weighted_distribution_any_tpr                |     2.3580 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
