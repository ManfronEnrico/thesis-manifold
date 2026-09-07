**Statistical and linear baselines by category.** Forecast error for each baseline model on the held-out test window, by product category. Weighted MAPE aggregates errors in proportion to volume; median MAPE reports the typical per-series error. Lower is better throughout; n denotes the number of series in each category, and the lowest error in each row is shown in bold italic.

| Metric            | Category            | Naive      | SeasonalNaive   | Drift      | Ridge      | Ridge(unclipped)   |   ARIMA |   Prophet |
|:------------------|:--------------------|:-----------|:----------------|:-----------|:-----------|:-------------------|--------:|----------:|
| Weighted MAPE (%) | CSD (n=95)          | 42.9       | ***19.2***      | 47.7       | 19.4       | 19.9               |    21.8 |     105.7 |
| Weighted MAPE (%) | danskvand (n=29)    | 32.5       | 35.9            | 32.0       | ***10.9*** | 10.9               |    33.5 |      19.5 |
| Weighted MAPE (%) | energidrikke (n=44) | 18.9       | 23.8            | ***17.7*** | 18.3       | diverged (~1e13)   |    19.4 |     972.4 |
| Weighted MAPE (%) | RTD (n=62)          | 89.3       | ***27.3***      | 95.9       | 40.5       | 2,459              |    53.3 |      66.8 |
| Median MAPE (%)   | CSD (n=95)          | 59.1       | 54.7            | 57.0       | ***43.5*** | 43.5               |    58.5 |      63.1 |
| Median MAPE (%)   | danskvand (n=29)    | ***36.0*** | 45.8            | 43.6       | 40.6       | 40.6               |    48.4 |      37.1 |
| Median MAPE (%)   | energidrikke (n=44) | 38.0       | 95.9            | ***34.2*** | 81.5       | 81.5               |    70.1 |     112.5 |
| Median MAPE (%)   | RTD (n=62)          | ***44.1*** | 89.4            | 52.9       | 56.1       | 56.8               |    66   |      88.8 |

*Note.* Prophet was evaluated on every category and is reported in full. Its error is high on three of the four because monthly observations do not support the weekly-seasonality and holiday-window components that the method is designed around, leaving a piecewise trend and an annual seasonal term estimated over a short history (Taylor & Letham, 2018). The unclipped Ridge variant is reported alongside the clipped one to show the effect of constraining predictions to be non-negative. On two categories the unconstrained fit diverges to an error many orders of magnitude beyond the plausible range; those entries are marked as divergent and given by order of magnitude, since a decimal figure would imply a precision the result does not have.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Prophet's failure is a RESULT, not a gap -- it IS implemented (srq1_baselines_stat.py:236). NLM Section J: PRO-04 Contradicted (T&L do NOT exclude monthly data), PRO-05 Not Found (they do not prove flat forecasts). Only PRO-06 wording is safe. Taylor & Letham (2018) is MISSING from the Ch2 reference list.
