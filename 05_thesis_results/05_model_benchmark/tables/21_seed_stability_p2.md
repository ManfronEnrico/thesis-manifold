**Sensitivity of the substrate to random seed - part 2 of 2.** Rows 10 to 12 of 12. Variation in fitted accuracy across repeated fits that differ only in the random seed supplied to the training procedure, over 5 seeds per model and category. The more stable model in each row is shown in bold italic.

| Measure    | Category     |   LightGBM |   XGBoost |
|:-----------|:-------------|-----------:|----------:|
| mWMAPE (%) | Danskvand    |      27.01 |     25.8  |
| mWMAPE (%) | Energidrikke |      16.24 |     16.95 |
| mWMAPE (%) | RTD          |      30.5  |     30.08 |

*Note.* Models with a stochastic fitting procedure, which includes gradient-boosted trees, can return different parameters from identical data. Seed sensitivity is therefore measured rather than assumed, following the stability criterion of Klee and Xia (2025). The coefficient of variation measures dispersion of the forecasts themselves; the standard deviation of WMAPE measures how far the resulting accuracy moves. mWMAPE (%) = mean WMAPE across seeds; sdWMAPE (pp) = its standard deviation; medCV (%) = median coefficient of variation of the forecasts.
