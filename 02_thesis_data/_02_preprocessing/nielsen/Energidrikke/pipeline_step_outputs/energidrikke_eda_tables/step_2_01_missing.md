## Missing Value Analysis

- Nulls per column. In this panel a null is an unreported measure for an observed brand-month, which is distinct from a brand-month that does not appear at all.
- Matters for feature engineering because a lag or rolling window computed across a null propagates it forward into every window that spans the gap.

| Column                             |   Missing |   Missing % |
|:-----------------------------------|----------:|------------:|
| weighted_distribution_any_promo    |       332 |     19.5000 |
| weighted_distribution_disp_feat    |      1190 |     69.9000 |
| weighted_distribution_disp_wo_feat |       503 |     29.6000 |
| weighted_distribution_feat_wo_disp |      1141 |     67.0000 |
| weighted_distribution_total_feat   |      1139 |     66.9000 |
| weighted_distribution_any_disp     |       503 |     29.6000 |
| weighted_distribution_any_tpr      |       380 |     22.3000 |
