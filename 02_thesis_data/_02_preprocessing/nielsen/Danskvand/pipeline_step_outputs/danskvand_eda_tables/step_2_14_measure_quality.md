## Measure-Column Quality Scan

- Per-column scan for the two defects that silently corrupt aggregation: impossible negatives, and rate columns mistakenly treated as additive.
- Negative counts and negative shares are impossible by definition, so any listed here are delivery defects. Reported and left uncorrected (F42): clipping would manufacture a plausible-looking value and hide the problem, and none of the affected columns is the target.
- The in_0_100 flag answers F39. A column bounded within [0, 100] behaves as a rate and must be averaged when aggregating -- summing two 70% distribution figures into 140% is the specific error this check exists to prevent.
- The additive/intensive split it implies is what step 1's aggregation already applies; this table is the evidence that the classification matches the data.

| column                                       |       min |           max |         mean |   nulls |   zeros |   negatives |   neg_pct | in_0_100   |
|:---------------------------------------------|----------:|--------------:|-------------:|--------:|--------:|------------:|----------:|:-----------|
| sales_value                                  |    1.0000 | 18913269.3412 | 1061231.1442 |       0 |       0 |           0 |    0.0000 | False      |
| sales_liters                                 |    0.2000 |  4621587.5811 |  153831.6410 |       0 |       0 |           0 |    0.0000 | False      |
| sales_units                                  |    1.0000 |  3852225.7843 |  130651.0808 |       0 |       0 |           0 |    0.0000 | False      |
| numeric_distribution                         |    0.0001 |        0.2894 |       0.0334 |       0 |       0 |           0 |    0.0000 | True       |
| numeric_distribution_reach                   |    0.0004 |        0.3166 |       0.0436 |       0 |       0 |           0 |    0.0000 | True       |
| weighted_dist                                |    0.0000 |        0.3191 |       0.0442 |       0 |       0 |           0 |    0.0000 | True       |
| weighted_distribution_reach                  |    0.0000 |        0.3421 |       0.0557 |       0 |       0 |           0 |    0.0000 | True       |
| total_weighted_distribution_points_tdp_reach |    0.0000 |        0.3421 |       0.0557 |       0 |       0 |           0 |    0.0000 | True       |
| number_of_items_reach                        |    1.0000 |      809.8765 |     110.2634 |       0 |       0 |           0 |    0.0000 | False      |
| avg_number_of_stores_selling_reach           |    1.0000 |      809.1665 |     110.0309 |       0 |       0 |           0 |    0.0000 | False      |
| universe_number_of_stores                    | 2468.0000 |     2556.0000 |    2521.4432 |       0 |       0 |           0 |    0.0000 | False      |
| avg_no_of_items_per_store_reach              |    0.9954 |        1.3750 |       1.0016 |       0 |       0 |           0 |    0.0000 | True       |
