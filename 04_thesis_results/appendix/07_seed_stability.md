**Sensitivity of the substrate to random seed.** Variation in fitted accuracy across repeated fits that differ only in the random seed supplied to the training procedure, over 5 seeds per model and category. The more stable model in each row is shown in bold italic.

| Measure                                       | Category     | LightGBM    | XGBoost     |
|:----------------------------------------------|:-------------|:------------|:------------|
| Median coefficient of variation (%)           | CSD          | ***11.24*** | 12.31       |
| Median coefficient of variation (%)           | danskvand    | ***11.94*** | 12.42       |
| Median coefficient of variation (%)           | energidrikke | ***17.38*** | 17.42       |
| Median coefficient of variation (%)           | RTD          | 12.52       | ***10.44*** |
| Standard deviation of WMAPE across seeds (pp) | CSD          | 0.65        | ***0.59***  |
| Standard deviation of WMAPE across seeds (pp) | danskvand    | ***0.69***  | 1.04        |
| Standard deviation of WMAPE across seeds (pp) | energidrikke | 1.18        | ***0.79***  |
| Standard deviation of WMAPE across seeds (pp) | RTD          | 1.64        | ***0.92***  |
| Mean WMAPE across seeds (%)                   | CSD          | 15.44       | ***15.06*** |
| Mean WMAPE across seeds (%)                   | danskvand    | ***20.79*** | 21.83       |
| Mean WMAPE across seeds (%)                   | energidrikke | 14.14       | ***13.93*** |
| Mean WMAPE across seeds (%)                   | RTD          | ***33.51*** | 35.14       |

*Note.* Models with a stochastic fitting procedure, which includes gradient-boosted trees, can return different parameters from identical data. Seed sensitivity is therefore measured rather than assumed, following the stability criterion of Klee and Xia (2025). The coefficient of variation measures dispersion of the forecasts themselves; the standard deviation of WMAPE measures how far the resulting accuracy moves, and is the quantity against which any difference between models should be judged material.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

THIS IS THE 3.97pp NUMBER'S HOME. wmape_std here is why we must not claim re-tuning is less accurate -- seed noise swamps the ~0.3pp between refit and re-tune. Cross-ref retraining_cost.
