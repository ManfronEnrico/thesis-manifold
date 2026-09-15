**Computational cost of the forecasting substrate.** Time and memory required to fit, to serve, and to retrain each candidate model, measured on the largest category (CSD) at brand-by-month granularity, and expressed against the memory available in the production deployment environment. Resident set size is sampled every 5 ms by a monitoring thread, in a separate process per model. The lowest value in each row is shown in bold italic.

| Measure                                        |    Ridge |   LightGBM |   XGBoost |   ARIMA(per-series) |   Prophet(per-series) |
|:-----------------------------------------------|---------:|-----------:|----------:|--------------------:|----------------------:|
| Fit time (s)                                   |    0.008 |      1.758 |     1.679 |                0.04 |                11.373 |
| Prediction time (ms)                           |    2.2   |     15.5   |    11.8   |                4.7  |                95.3   |
| Peak fit memory, RSS (MB)                      |    1.5   |     17.9   |    34.5   |                2.1  |                 5.2   |
| Peak prediction memory, RSS (MB)               |    0.02  |      0.07  |     0.65  |                0.11 |                 1.73  |
| Peak fit memory, Python heap (MB)              |    0.8   |      4.9   |     0.1   |                0.3  |                 2.3   |
| Serialised model size (MB)                     |    0     |      1.59  |     3.9   |                     |                 0.01  |
| Training rows                                  | 2280     |   2280     |  2280     |               24    |                24     |
| Features                                       |   18     |     18     |    18     |                1    |                 1     |
| Peak fit memory as share of 4096 MB budget (%) |    0.04  |      0.44  |     0.84  |                0.05 |                 0.13  |

*Note.* Resident set size and Python-heap allocation are reported side by side because they measure different quantities. Python-heap accounting observes only allocations made through the interpreter, whereas gradient-boosted ensembles are constructed by native libraries; the serialised model size provides an independent check on which of the two reflects the memory a deployment must provision. Fit time is the cost of a single fit given hyperparameters; the cost of retraining in service is reported separately below.
