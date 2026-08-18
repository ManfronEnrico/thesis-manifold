## Skewness Analysis

- Fisher-Pearson skewness per numeric column. Zero is symmetric; positive means a long right tail.
- Thresholds follow Kim (2013): |skew| > 2 indicates substantial departure from normality, 0.5-2 moderate. These bands are the stated basis for the log-transform recommendation, not an eyeball judgement.
- The forecast target's skewness is the empirical case for LOG_TRANSFORM_TARGET; see 3.15 for the same evidence as a distribution curve.
- Skewness is a property of the marginal distribution and says nothing about the time-series structure -- 3.05 and 3.16 cover that.

| feature                                      |   skewness | interpretation                                                                          |
|:---------------------------------------------|-----------:|:----------------------------------------------------------------------------------------|
| sales_value                                  |     2.9660 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| sales_liters                                 |     4.9170 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| sales_units                                  |     4.9400 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| numeric_distribution                         |     2.0200 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
| numeric_distribution_reach                   |     1.7550 | Right-skewed -- log transform justified                                                 |
| weighted_dist                                |     1.8770 | Right-skewed -- log transform justified                                                 |
| weighted_distribution_reach                  |     1.6230 | Right-skewed -- log transform justified                                                 |
| total_weighted_distribution_points_tdp_reach |     1.6230 | Right-skewed -- log transform justified                                                 |
| number_of_items_reach                        |     1.7630 | Right-skewed -- log transform justified                                                 |
| avg_number_of_stores_selling_reach           |     1.7630 | Right-skewed -- log transform justified                                                 |
| universe_number_of_stores                    |    -0.7630 | Left-skewed (negative)                                                                  |
| avg_no_of_items_per_store_reach              |    27.2330 | Highly right-skewed -- substantial non-normality (Kim, 2013) -> log transform necessary |
