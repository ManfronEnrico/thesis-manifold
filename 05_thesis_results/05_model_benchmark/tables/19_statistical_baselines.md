**Statistical and linear baselines by category.** Forecast error for each baseline model on the held-out test window, by product category. Weighted MAPE aggregates errors in proportion to volume; median MAPE reports the typical per-series error. Lower is better throughout; n denotes the number of series in each category, and the lowest error in each row is shown in bold italic.

| Metric    | Category     | Naive      | SeasonalNaive   | Drift      |   Ridge | Ridge(unclipped)   |   ARIMA | Prophet    |
|:----------|:-------------|:-----------|:----------------|:-----------|--------:|:-------------------|--------:|:-----------|
| wMAPE (%) | CSD          | 42.9       | ***19.2***      | 47.7       |    23.8 | 84.8               |    21.8 | 105.7      |
| wMAPE (%) | Danskvand    | 32.5       | 35.9            | 32.0       |    74.9 | diverged (~1e25)   |    33.5 | ***19.4*** |
| wMAPE (%) | Energidrikke | 18.9       | 23.8            | ***17.7*** |    23.6 | diverged (~1e13)   |    19.4 | 975.0      |
| wMAPE (%) | RTD          | 89.3       | ***27.3***      | 95.9       |    52.4 | diverged (~1e5)    |    53.3 | 66.8       |
| mMAPE (%) | CSD          | 59.1       | ***54.7***      | 57.0       |    58.1 | 58.1               |    58.5 | 63.1       |
| mMAPE (%) | Danskvand    | ***36.0*** | 45.8            | 43.6       |    40.3 | 40.3               |    48.4 | 37.1       |
| mMAPE (%) | Energidrikke | 38.0       | 95.9            | ***34.2*** |   100   | 100.0              |    70.1 | 112.5      |
| mMAPE (%) | RTD          | ***44.1*** | 89.4            | 52.9       |    75.6 | 76.4               |    66   | 88.8       |

*Note.* Prophet's error is high on three of four categories: monthly observations do not support the weekly-seasonality and holiday-window components it is designed around (Taylor & Letham, 2018). Ridge is reported clipped and unclipped to show the effect of constraining predictions to be non-negative; where the unclipped fit diverges, the entry is given by order of magnitude rather than to a decimal it does not support. wMAPE (%) = weighted MAPE; mMAPE (%) = median MAPE across series.
