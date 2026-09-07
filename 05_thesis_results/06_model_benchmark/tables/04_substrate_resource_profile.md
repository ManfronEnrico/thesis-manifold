**Computational cost of the forecasting substrate.** Time and memory required to fit, to serve, and to retrain each candidate model, measured on the largest category (CSD) at brand-by-month granularity, and expressed against the memory available in the production deployment environment. Resident set size is sampled every 5 ms by a monitoring thread, in a separate process per model. The lowest value in each row is shown in bold italic.

| Measure                                        | Ridge      |   LightGBM |   XGBoost | ARIMA(per-series)   |
|:-----------------------------------------------|:-----------|-----------:|----------:|:--------------------|
| Fit time (s)                                   | 0.114      |      8.017 |      3.6  | ***0.085***         |
| Prediction time (ms)                           | ***3.6***  |     33     |     13.8  | 7.9                 |
| Peak fit memory, RSS (MB)                      | 5.4        |     38.1   |     29.2  | ***1.9***           |
| Peak prediction memory, RSS (MB)               | ***0.02*** |      0.1   |      0.62 | 0.09                |
| Peak fit memory, Python heap (MB)              | 5.5        |     23     |      0.1  | 0.3                 |
| Serialised model size (MB)                     | ***0.00*** |      7.64  |      3.7  |                     |
| Training rows                                  | 2470       |   2470     |   2470    | 26                  |
| Features                                       | 13         |     13     |     13    | 1                   |
| Peak fit memory as share of 4096 MB budget (%) | 0.13       |      0.93  |      0.71 | ***0.05***          |

*Note.* Resident set size and Python-heap allocation are reported side by side because they measure different quantities. Python-heap accounting observes only allocations made through the interpreter, whereas gradient-boosted ensembles are constructed by native libraries; the serialised model size provides an independent check on which of the two reflects the memory a deployment must provision. Fit time is the cost of a single fit given hyperparameters; the cost of retraining in service is reported separately below.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

tracemalloc understates XGBoost by ~266x (0.1 vs 29.2 MB). The 3.7 MB pickle is the third witness -- a 3.7 MB artefact cannot be built in 0.1 MB. Keep both rows so the correction stays auditable, but RSS is the headline. P0044 F1-F2.

MERGED from three tables (profile + budget share + retraining) per Brian 2026-09-03: same unit system, same subject, so the comparison belongs in one screenshot. Drift stays separate -- its unit is pp of error, not time or memory.
