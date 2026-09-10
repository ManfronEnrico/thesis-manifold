**Sensitivity of the substrate to random seed.** Variation in fitted accuracy across repeated fits that differ only in the random seed supplied to the training procedure, over 5 seeds per model and category. The more stable model in each row is shown in bold italic.

| Measure                                       | Category     | LightGBM    | XGBoost     |
|:----------------------------------------------|:-------------|:------------|:------------|
| Median coefficient of variation (%)           | CSD          | 18.16       | ***15.19*** |
| Median coefficient of variation (%)           | Danskvand    | ***13.76*** | 17.39       |
| Median coefficient of variation (%)           | Energidrikke | ***23.92*** | 24.29       |
| Median coefficient of variation (%)           | RTD          | ***9.85***  | 11.35       |
| Standard deviation of WMAPE across seeds (pp) | CSD          | ***0.67***  | 0.83        |
| Standard deviation of WMAPE across seeds (pp) | Danskvand    | 2.81        | ***1.04***  |
| Standard deviation of WMAPE across seeds (pp) | Energidrikke | ***0.59***  | 1.08        |
| Standard deviation of WMAPE across seeds (pp) | RTD          | ***0.30***  | 1.04        |
| Mean WMAPE across seeds (%)                   | CSD          | 18.87       | ***18.61*** |
| Mean WMAPE across seeds (%)                   | Danskvand    | 27.01       | ***25.80*** |
| Mean WMAPE across seeds (%)                   | Energidrikke | ***16.24*** | 16.95       |
| Mean WMAPE across seeds (%)                   | RTD          | 30.50       | ***30.08*** |

*Note.* Models with a stochastic fitting procedure, which includes gradient-boosted trees, can return different parameters from identical data. Seed sensitivity is therefore measured rather than assumed, following the stability criterion of Klee and Xia (2025). The coefficient of variation measures dispersion of the forecasts themselves; the standard deviation of WMAPE measures how far the resulting accuracy moves, and is the quantity against which any difference between models should be judged material.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

The WMAPE-sd column here is the seed-noise magnitude that the retraining_cost table's caveat rests on: it is larger than the refit-vs-retune accuracy gap, which is why that gap cannot be called material. Cross-ref retraining_cost. Read the number off this table, do not transcribe it into prose.
