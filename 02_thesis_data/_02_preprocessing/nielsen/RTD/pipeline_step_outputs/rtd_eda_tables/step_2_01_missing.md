## Missing Value Analysis

- Nulls per column. In this panel a null is an unreported measure for an observed brand-month, which is distinct from a brand-month that does not appear at all.
- Matters for feature engineering because a lag or rolling window computed across a null propagates it forward into every window that spans the gap.

| Column                              |   Missing |   Missing % |
|:------------------------------------|----------:|------------:|
| weighted_distribution_any_promo     |       854 |     34.0000 |
| weighted_distribution_disp_and_feat |      2088 |     83.2000 |
| weighted_distribution_disp_wo_feat  |      1246 |     49.7000 |
| weighted_distribution_feat_wo_disp  |      2055 |     81.9000 |
| weighted_distribution_total_feat    |      2052 |     81.8000 |
| weighted_distribution_any_disp      |      1239 |     49.4000 |
| weighted_distribution_any_tpr       |       957 |     38.1000 |
