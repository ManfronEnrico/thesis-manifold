**Holiday enrichment: test WMAPE with and without.** Per category and model, hyperparameters tuned separately for each arm.

| Category     | Model    | WMAPE without (%)   | WMAPE with (%)   | Delta (pp)   | Direction   |
|:-------------|:---------|:--------------------|:-----------------|:-------------|:------------|
| CSD          | LightGBM | 19.74               | 18.78            | -0.95        | improved    |
| CSD          | Ridge    | 20.70               | 20.55            | -0.15        | improved    |
| CSD          | XGBoost  | 17.15               | 18.38            | +1.22        | worsened    |
| Danskvand    | LightGBM | 25.71               | 26.68            | +0.98        | worsened    |
| Danskvand    | XGBoost  | 21.20               | 23.41            | +2.21        | worsened    |
| Energidrikke | LightGBM | 20.98               | 20.34            | -0.64        | improved    |
| Energidrikke | XGBoost  | 17.98               | 17.37            | -0.61        | improved    |
| RTD          | LightGBM | 33.26               | 31.85            | -1.40        | improved    |
| RTD          | XGBoost  | 35.67               | 30.75            | -4.92        | improved    |

*Note.* Negative delta indicates the holiday features improved accuracy. They helped in 6 of 9 category-model combinations. Each arm was tuned independently on the validation split, refit on train+validation, and scored once on the held-out test split.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Do NOT quote the mean of this column. It averages over model families that respond differently, and that difference is itself the finding: Ridge benefits in 1 of 1 categories while the tree models benefit in 5 of 8 cells.

RTD XGBoost is the least stable cell in the study (it swings 2.95pp between the untuned and tuned runs, table 95).
