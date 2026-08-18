## Missing Value Analysis

- Unreported values per measure. In this panel an unreported value denotes a measure Nielsen did not supply for an observed brand-month, which is distinct from a brand-month that does not appear at all.
- The distinction matters for time-series construction: lagged and rolling features computed across an unreported value propagate it into every window spanning the gap.

| Column                             |   Missing |   Missing % |
|:-----------------------------------|----------:|------------:|
| weighted_distribution_any_promo    |       332 |     19.5000 |
| weighted_distribution_disp_feat    |      1190 |     69.9000 |
| weighted_distribution_disp_wo_feat |       503 |     29.6000 |
| weighted_distribution_feat_wo_disp |      1141 |     67.0000 |
| weighted_distribution_total_feat   |      1139 |     66.9000 |
| weighted_distribution_any_disp     |       503 |     29.6000 |
| weighted_distribution_any_tpr      |       380 |     22.3000 |
