## Missing Value Analysis

- Nulls per column. In this panel a null is an unreported measure for an observed brand-month, which is distinct from a brand-month that does not appear at all.
- Matters for feature engineering because a lag or rolling window computed across a null propagates it forward into every window that spans the gap.

| Column                              |   Missing |   Missing % |
|:------------------------------------|----------:|------------:|
| weighted_distribution_any_promo     |      1236 |     29.4000 |
| weighted_distribution_disp_feat     |      3432 |     81.5000 |
| weighted_distribution_disp_w_o_feat |      1705 |     40.5000 |
| weighted_distribution_feat_w_o_disp |      3310 |     78.6000 |
| weighted_distribution_total_feat    |      3309 |     78.6000 |
| weighted_distribution_any_disp      |      1703 |     40.5000 |
| weighted_distribution_any_tpr       |      1436 |     34.1000 |
