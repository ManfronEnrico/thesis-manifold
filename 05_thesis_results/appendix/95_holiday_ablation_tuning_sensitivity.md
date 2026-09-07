**Effect of hyperparameter tuning on the ablation.** The same feature comparison, measured against a fixed-configuration baseline and against a tuned one.

| Category     | Model    | Baseline WMAPE, fixed config (%)   | Baseline WMAPE, tuned (%)   | Baseline gain (pp)   | Holiday delta, fixed (pp)   | Holiday delta, tuned (pp)   |
|:-------------|:---------|:-----------------------------------|:----------------------------|:---------------------|:----------------------------|:----------------------------|
| CSD          | LightGBM | 18.48                              | 15.80                       | +2.68                | +1.55                       | +0.10                       |
| CSD          | Ridge    | 21.93                              | 21.25                       | +0.67                | +0.76                       | +0.95                       |
| CSD          | XGBoost  | 17.09                              | 14.99                       | +2.10                | +2.17                       | +1.73                       |
| RTD          | LightGBM | 32.21                              | 35.10                       | -2.89                | -1.67                       | -5.36                       |
| RTD          | Ridge    | 57.27                              | 56.30                       | +0.97                | -10.15                      | -8.97                       |
| RTD          | XGBoost  | 31.78                              | 36.02                       | -4.24                | -2.88                       | -0.14                       |
| danskvand    | LightGBM | 33.12                              | 23.65                       | +9.47                | +0.11                       | -3.70                       |
| danskvand    | Ridge    | 19.21                              | 21.70                       | -2.49                | +0.32                       | -0.74                       |
| danskvand    | XGBoost  | 32.56                              | 20.88                       | +11.68               | +1.57                       | +0.62                       |
| energidrikke | LightGBM | 17.82                              | 14.56                       | +3.26                | -0.41                       | -0.84                       |
| energidrikke | Ridge    | 20.83                              | 20.31                       | +0.52                | +0.79                       | -1.21                       |
| energidrikke | XGBoost  | 14.94                              | 13.12                       | +1.82                | +1.75                       | +0.51                       |

*Note.* Tuning improved the baseline itself by up to 11.68 percentage points. Where a fixed configuration is badly mis-specified, a feature comparison measured against it reflects that mis-specification rather than the features.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

This table is why the fixed-configuration ablation was not reported. Danskvand's trees were mis-specified by ~12pp, and that category flips from harmful to helpful once the model can fit. An ablation is only interpretable against a properly specified model.

Methodological point worth a sentence in the text: the direction of a feature effect can invert under tuning.
