## Missing Value Analysis

- Unreported values per measure. In this panel an unreported value denotes a measure Nielsen did not supply for an observed brand-month, which is distinct from a brand-month that does not appear at all.
- The distinction matters for time-series construction: lagged and rolling features computed across an unreported value propagate it into every window spanning the gap.

| Column                                  |   Missing |   Missing % |
|:----------------------------------------|----------:|------------:|
| weighted_distribution_any_promo         |       854 |     34.0000 |
| weighted_distribution_disp_and_feat     |      2088 |     83.2000 |
| weighted_distribution_disp_without_feat |      1246 |     49.7000 |
| weighted_distribution_feat_without_disp |      2055 |     81.9000 |
| weighted_distribution_total_feat        |      2052 |     81.8000 |
| weighted_distribution_any_disp          |      1239 |     49.4000 |
| weighted_distribution_any_tpr           |       957 |     38.1000 |
