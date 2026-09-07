## Skewness Analysis

- Fisher-Pearson skewness coefficient per measure. A value of zero indicates a symmetric distribution; positive values indicate a long right tail.
- Interpretation follows Kim (2013): absolute skewness above 2 indicates substantial departure from normality, and values between 0.5 and 2 moderate departure.
- Skewness in the forecast target is the empirical basis for applying a logarithmic transformation before modelling.
- This coefficient describes the marginal distribution only. It carries no information about temporal dependence, which is characterised separately by the stationarity and autocorrelation analyses.

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
