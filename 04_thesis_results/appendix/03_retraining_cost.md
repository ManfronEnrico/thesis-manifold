**Cost of retraining a model on request.** Elapsed time and peak memory for the two ways of bringing a model up to date at a single forecast origin: refitting coefficients while holding stored hyperparameters fixed, against repeating the hyperparameter search at two search budgets. Measured on CSD with LightGBM.

| Operation                       |   Elapsed time (s) | Relative to refit   |   Peak memory, RSS (MB) |   Share of budget (%) |   Test WMAPE (%) |
|:--------------------------------|-------------------:|:--------------------|------------------------:|----------------------:|-----------------:|
| Refit on stored hyperparameters |               2.93 | 1x                  |                    35   |                  0.85 |            12.57 |
| Re-tune, 30 trials x 4 folds    |             107.85 | 37x                 |                    86.6 |                  2.11 |            15.27 |
| Re-tune, 100 trials x 4 folds   |             417.3  | 142x                |                    65.3 |                  1.59 |            16.77 |

*Note.* Refitting re-estimates model coefficients only. Re-tuning repeats a cross-validated fit for every trial of the search, so its cost is the cost of one fit multiplied by the number of trials and the number of folds. This difference in elapsed time, rather than any difference in accuracy, is the basis on which refitting on request is adopted and re-tuning on request is not: memory remains within budget in every case, and the accuracy figures fall within the range produced by changing only the random seed of the search, so they cannot separate the two strategies.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Do NOT claim re-tuning is less accurate. Optuna seed alone moves test WMAPE by 3.97pp, swamping the ~0.3pp between strategies (F21). 100 trials = 417.3 s vs 2.93 s = 142x (F28). Memory is NOT the constraint -- peak 2.11% of budget. The case is elapsed time alone.
