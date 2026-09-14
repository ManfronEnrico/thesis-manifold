**Sensitivity of the substrate to random seed.** Variation in fitted accuracy across repeated fits that differ only in the random seed supplied to the training procedure, over 5 seeds per model and category. The more stable model in each row is shown in bold italic.

| Measure      | Category     | LightGBM    | XGBoost     |
|:-------------|:-------------|:------------|:------------|
| medCV (%)    | CSD          | 18.16       | ***15.19*** |
| medCV (%)    | Danskvand    | ***13.76*** | 17.39       |
| medCV (%)    | Energidrikke | ***23.92*** | 24.29       |
| medCV (%)    | RTD          | ***9.85***  | 11.35       |
| sdWMAPE (pp) | CSD          | ***0.67***  | 0.83        |
| sdWMAPE (pp) | Danskvand    | 2.81        | ***1.04***  |
| sdWMAPE (pp) | Energidrikke | ***0.59***  | 1.08        |
| sdWMAPE (pp) | RTD          | ***0.30***  | 1.04        |
| mWMAPE (%)   | CSD          | 18.87       | ***18.61*** |
| mWMAPE (%)   | Danskvand    | 27.01       | ***25.80*** |
| mWMAPE (%)   | Energidrikke | ***16.24*** | 16.95       |
| mWMAPE (%)   | RTD          | 30.50       | ***30.08*** |

*Note.* Models with a stochastic fitting procedure, which includes gradient-boosted trees, can return different parameters from identical data. Seed sensitivity is therefore measured rather than assumed, following the stability criterion of Klee and Xia (2025). The coefficient of variation measures dispersion of the forecasts themselves; the standard deviation of WMAPE measures how far the resulting accuracy moves. mWMAPE (%) = mean WMAPE across seeds; sdWMAPE (pp) = its standard deviation; medCV (%) = median coefficient of variation of the forecasts.
