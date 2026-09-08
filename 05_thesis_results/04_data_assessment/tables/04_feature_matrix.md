**Composition of the modelling matrix.** Every column of the CSD feature matrix at a 3-month forecast horizon, with the role it plays in training. The matrix holds 4,370 brand-months across 95 brands in 54 columns, of which 34 are model inputs.

| Column                                       | Role                       | Type           | Populated   |
|:---------------------------------------------|:---------------------------|:---------------|:------------|
| brand                                        | Identifier                 | object         | 100%        |
| date                                         | Identifier                 | datetime64[us] | 100%        |
| sales_units                                  | Target                     | float64        | 100%        |
| log_sales_units                              | Target, transformed        | float64        | 100%        |
| split                                        | Split label                | object         | 100%        |
| period_index                                 | Ordering                   | int32          | 100%        |
| lag_1                                        | Feature - autoregressive   | float64        | 93%         |
| lag_13                                       | Feature - autoregressive   | float64        | 67%         |
| lag_2                                        | Feature - autoregressive   | float64        | 91%         |
| lag_3                                        | Feature - autoregressive   | float64        | 89%         |
| lag_4                                        | Feature - autoregressive   | float64        | 87%         |
| lag_8                                        | Feature - autoregressive   | float64        | 78%         |
| rolling_mean_13                              | Feature - autoregressive   | float64        | 100%        |
| rolling_mean_4                               | Feature - autoregressive   | float64        | 96%         |
| rolling_std_4                                | Feature - autoregressive   | float64        | 100%        |
| days_in_month                                | Feature - calendar         | int32          | 100%        |
| month                                        | Feature - calendar         | int32          | 100%        |
| n_holidays                                   | Feature - calendar         | float64        | 100%        |
| non_holiday_days                             | Feature - calendar         | float64        | 100%        |
| peak_month                                   | Feature - calendar         | int64          | 100%        |
| quarter                                      | Feature - calendar         | int32          | 100%        |
| avg_no_of_items_per_store_reach              | Feature - distribution     | float64        | 87%         |
| avg_number_of_stores_selling_reach           | Feature - distribution     | float64        | 87%         |
| number_of_items_reach                        | Feature - distribution     | float64        | 87%         |
| numeric_distribution                         | Feature - distribution     | float64        | 87%         |
| numeric_distribution_reach                   | Feature - distribution     | float64        | 87%         |
| total_weighted_distribution_points_tdp_reach | Feature - distribution     | float64        | 87%         |
| universe_number_of_stores                    | Feature - distribution     | float64        | 87%         |
| weighted_dist                                | Feature - distribution     | float64        | 100%        |
| weighted_distribution_reach                  | Feature - distribution     | float64        | 87%         |
| promo_intensity                              | Feature - promotional      | float64        | 93%         |
| weighted_distribution_any_disp               | Feature - promotional      | float64        | 54%         |
| weighted_distribution_any_promo              | Feature - promotional      | float64        | 63%         |
| weighted_distribution_any_tpr                | Feature - promotional      | float64        | 60%         |
| weighted_distribution_disp_and_feat          | Feature - promotional      | float64        | 18%         |
| weighted_distribution_disp_without_feat      | Feature - promotional      | float64        | 54%         |
| weighted_distribution_feat_without_disp      | Feature - promotional      | float64        | 20%         |
| weighted_distribution_total_feat             | Feature - promotional      | float64        | 20%         |
| zero_run_flag                                | Feature - series quality   | float64        | 93%         |
| zero_run_length                              | Feature - series quality   | float64        | 93%         |
| period_month                                 | Raw date part, superseded  | int32          | 100%        |
| period_year                                  | Raw date part, superseded  | int32          | 100%        |
| baseline_sales_in_liters                     | Excluded - contemporaneous | float64        | 87%         |
| baseline_sales_in_liters_any_promo           | Excluded - contemporaneous | float64        | 87%         |
| baseline_sales_units                         | Excluded - contemporaneous | float64        | 87%         |
| baseline_sales_units_any_promo               | Excluded - contemporaneous | float64        | 87%         |
| baseline_sales_value                         | Excluded - contemporaneous | float64        | 87%         |
| baseline_sales_value_any_promo               | Excluded - contemporaneous | float64        | 87%         |
| promo_units                                  | Excluded - contemporaneous | float64        | 100%        |
| sales_in_liters_any_promo                    | Excluded - contemporaneous | float64        | 87%         |
| sales_liters                                 | Excluded - contemporaneous | float64        | 100%        |
| sales_units_any_tpr                          | Excluded - contemporaneous | float64        | 87%         |
| sales_value                                  | Excluded - contemporaneous | float64        | 100%        |
| sales_value_any_promo                        | Excluded - contemporaneous | float64        | 87%         |

*Note.* The target is sales_units, modelled as log1p and inverted for reporting. Splits are chronological: training 2022-10 to 2025-05, validation 2025-06 to 2025-12, test 2026-01 to 2026-07. The 12 columns marked excluded are same-period sales and baseline measures, retained so a prediction can be traced back to the observation it was made from; they are not available to the model, which would otherwise observe the quantity it is asked to predict. Populated is the share of rows with a value: autoregressive features are empty for a brand's earliest months by construction.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Read from csd_feature_matrix_h3.parquet and csd_manifest_h3.json at render time; the feature list is the manifest's own, not a copy. Role assignment is BY RULE (_fm_role) and asserts that no column falls through -- a column added upstream fails the export rather than appearing unclassified. Counts here supersede the 13/14/16-feature figures in earlier drafts (P0048 F3, F10): the current matrix carries 34 features after the holiday enrichment. CSD is shown as the worked category; the other three differ in the promotional block, which is absent at source for the promo-zero categories.
