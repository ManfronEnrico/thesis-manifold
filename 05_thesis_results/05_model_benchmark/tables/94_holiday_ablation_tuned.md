**Holiday enrichment: test WMAPE with and without.** Per category and model, hyperparameters tuned separately for each arm.

| Category     | Model    | WMAPE without (%)   | WMAPE with (%)   | Delta (pp)   | Direction   |
|:-------------|:---------|:--------------------|:-----------------|:-------------|:------------|
| CSD          | LightGBM | 15.80               | 15.90            | +0.10        | worsened    |
| CSD          | Ridge    | 21.25               | 22.20            | +0.95        | worsened    |
| CSD          | XGBoost  | 14.99               | 16.72            | +1.73        | worsened    |
| RTD          | LightGBM | 35.10               | 29.74            | -5.36        | improved    |
| RTD          | Ridge    | 56.30               | 47.33            | -8.97        | improved    |
| RTD          | XGBoost  | 36.02               | 35.88            | -0.14        | improved    |
| danskvand    | LightGBM | 23.65               | 19.95            | -3.70        | improved    |
| danskvand    | Ridge    | 21.70               | 20.96            | -0.74        | improved    |
| danskvand    | XGBoost  | 20.88               | 21.50            | +0.62        | worsened    |
| energidrikke | LightGBM | 14.56               | 13.73            | -0.84        | improved    |
| energidrikke | Ridge    | 20.31               | 19.10            | -1.21        | improved    |
| energidrikke | XGBoost  | 13.12               | 13.63            | +0.51        | worsened    |

*Note.* Negative delta indicates the holiday features improved accuracy. They helped in 7 of 12 category-model combinations. Each arm was tuned independently on the validation split, refit on train+validation, and scored once on the held-out test split.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Do NOT quote the mean of this column. It averages over model families that respond differently, and that difference is itself the finding: Ridge benefits in 3 of 4 categories while the tree models benefit in 4 of 8 cells.

danskvand LightGBM is the least stable cell in the study (it swings 3.81pp between the untuned and tuned runs, table 95).
