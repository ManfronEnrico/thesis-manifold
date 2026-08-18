## Measure-Column Quality Scan

- Per-measure scan for two data-quality conditions: values that are impossible given the measure's definition, and rate measures that would be corrupted by summation.
- Counts and shares cannot be negative by definition, so any negative values reported here indicate defects in the delivered data. They are reported rather than adjusted, since imputing a substitute value would present a fabricated figure as an observation.
- Measures observed entirely within the interval [0, 100] behave as rates rather than counts and must be averaged when aggregating across records. Summing two distribution figures of 70 per cent into 140 per cent is the specific error this check identifies.
- The resulting classification of measures as additive or intensive determines the aggregation function applied to each when constructing the brand-month panel.

| column                                       |        min |            max |         mean |   nulls |   zeros |   negatives |   neg_pct | in_0_100   |
|:---------------------------------------------|-----------:|---------------:|-------------:|--------:|--------:|------------:|----------:|:-----------|
| sales_value                                  |     1.0000 | 128733406.7997 | 3572722.6117 |       0 |       0 |           0 |    0.0000 | False      |
| sales_liters                                 |     0.2000 |  14028289.1484 |  347681.9543 |       0 |       0 |           0 |    0.0000 | False      |
| sales_units                                  |     1.0000 |   8270379.6905 |  227554.8107 |       0 |       0 |           0 |    0.0000 | False      |
| sales_value_any_promo                        |  -276.2766 | 100548736.5201 | 2284618.2457 |       0 |    1236 |           1 |    0.0240 | False      |
| sales_in_liters_any_promo                    | -1201.3435 |  12741297.3502 |  243085.0691 |       0 |    1236 |           1 |    0.0240 | False      |
| promo_units                                  | -3640.4349 |   6429767.9379 |  132885.6094 |       0 |    1236 |           1 |    0.0240 | False      |
| sales_units_any_tpr                          | -5603.9253 |   5669329.8359 |  100793.3269 |       0 |    1436 |           1 |    0.0240 | False      |
| baseline_sales_value                         |     0.0000 |  92034765.3944 | 2496605.1607 |       0 |       1 |           0 |    0.0000 | False      |
| baseline_sales_in_liters                     |     0.0000 |   6787012.0042 |  209380.5608 |       0 |       1 |           0 |    0.0000 | False      |
| baseline_sales_units                         |     0.0000 |   6345477.7946 |  166067.3126 |       0 |       1 |           0 |    0.0000 | False      |
| baseline_sales_value_any_promo               |     0.0000 |  46778307.2664 | 1098983.0190 |       0 |    1281 |           0 |    0.0000 | False      |
| baseline_sales_in_liters_any_promo           |     0.0000 |   3826475.8028 |   90567.2896 |       0 |    1281 |           0 |    0.0000 | False      |
| baseline_sales_units_any_promo               |     0.0000 |   2192334.0501 |   57834.1418 |       0 |    1281 |           0 |    0.0000 | False      |
| numeric_distribution                         |     0.0001 |         0.5190 |       0.0456 |       0 |       0 |           0 |    0.0000 | True       |
| numeric_distribution_reach                   |     0.0002 |         0.6457 |       0.0631 |       0 |       0 |           0 |    0.0000 | True       |
| weighted_dist                                |     0.0000 |         0.6422 |       0.0610 |       0 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_reach                  |     0.0000 |         0.7402 |       0.0803 |       0 |       0 |           0 |    0.0000 | True       |
| total_weighted_distribution_points_tdp_reach |     0.0000 |         0.7402 |       0.0803 |       0 |       0 |           0 |    0.0000 | True       |
| number_of_items_reach                        |     1.0000 |      1639.0513 |     159.6478 |       0 |       0 |           0 |    0.0000 | False      |
| avg_number_of_stores_selling_reach           |     0.5000 |      1635.3681 |     159.3466 |       0 |       0 |           0 |    0.0000 | False      |
| universe_number_of_stores                    |  2468.0000 |      2556.0000 |    2522.5998 |       0 |       0 |           0 |    0.0000 | False      |
| avg_no_of_items_per_store_reach              |     0.9441 |         2.0000 |       1.0022 |       0 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_any_promo              |     0.0000 |         0.5612 |       0.0423 |    1236 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_disp_and_feat          |     0.0002 |         0.2052 |       0.0230 |    3432 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_disp_without_feat      |     0.0000 |         0.2783 |       0.0193 |    1705 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_feat_without_disp      |     0.0004 |         0.1285 |       0.0369 |    3310 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_total_feat             |     0.0004 |         0.3219 |       0.0529 |    3309 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_any_disp               |     0.0000 |         0.3848 |       0.0230 |    1703 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_any_tpr                |     0.0000 |         0.4545 |       0.0323 |    1436 |       0 |           0 |    0.0000 | True       |
