**Computational cost of the forecasting substrate.** Time and memory required to fit, to serve, and to retrain each candidate model, measured on the largest category (CSD) at brand-by-month granularity, and expressed against the memory available in the production deployment environment. Resident set size is sampled every 5 ms by a monitoring thread, in a separate process per model. The lowest value in each row is shown in bold italic.

| Measure                                        | Ridge       |   LightGBM |   XGBoost |   ARIMA(per-series) |
|:-----------------------------------------------|:------------|-----------:|----------:|--------------------:|
| Fit time (s)                                   | ***0.027*** |      2.147 |     1.942 |                0.09 |
| Prediction time (ms)                           | ***3.0***   |      7.7   |    15.8   |                5.9  |
| Peak fit memory, RSS (MB)                      | ***1.6***   |     14.9   |    31.9   |                2    |
| Peak prediction memory, RSS (MB)               | ***0.03***  |      0.14  |     0.47  |                0.17 |
| Peak fit memory, Python heap (MB)              | 0.8         |      4.9   |     0.1   |                0.3  |
| Serialised model size (MB)                     | ***0.00***  |      1.59  |     3.9   |                     |
| Training rows                                  | 2280        |   2280     |  2280     |               24    |
| Features                                       | 18          |     18     |    18     |                1    |
| Peak fit memory as share of 4096 MB budget (%) | ***0.04***  |      0.36  |     0.78  |                0.05 |

*Note.* Resident set size and Python-heap allocation are reported side by side because they measure different quantities. Python-heap accounting observes only allocations made through the interpreter, whereas gradient-boosted ensembles are constructed by native libraries; the serialised model size provides an independent check on which of the two reflects the memory a deployment must provision. Fit time is the cost of a single fit given hyperparameters; the cost of retraining in service is reported separately below.
