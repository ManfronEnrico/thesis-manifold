## Missing Value Analysis

- Unreported values per measure. In this panel an unreported value denotes a measure Nielsen did not supply for an observed brand-month, which is distinct from a brand-month that does not appear at all.
- The distinction matters for time-series construction: lagged and rolling features computed across an unreported value propagate it into every window spanning the gap.

| Column                              |   Missing |   Missing % |
|:------------------------------------|----------:|------------:|
| weighted_distribution_any_promo     |      1236 |     29.4000 |
| weighted_distribution_disp_feat     |      3432 |     81.5000 |
| weighted_distribution_disp_w_o_feat |      1705 |     40.5000 |
| weighted_distribution_feat_w_o_disp |      3310 |     78.6000 |
| weighted_distribution_total_feat    |      3309 |     78.6000 |
| weighted_distribution_any_disp      |      1703 |     40.5000 |
| weighted_distribution_any_tpr       |      1436 |     34.1000 |
