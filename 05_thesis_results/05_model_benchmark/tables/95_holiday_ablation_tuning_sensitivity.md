**Effect of hyperparameter tuning on the ablation.** The same feature comparison, measured against a fixed-configuration baseline and against a tuned one.

| Category     | Model    | Baseline WMAPE, fixed config (%)   | Baseline WMAPE, tuned (%)   | Baseline gain (pp)   | Holiday delta, fixed (pp)   | Holiday delta, tuned (pp)   |
|:-------------|:---------|:-----------------------------------|:----------------------------|:---------------------|:----------------------------|:----------------------------|
| CSD          | LightGBM | 20.20                              | 19.74                       | +0.46                | +1.23                       | -0.95                       |
| CSD          | Ridge    | 19.73                              | 20.70                       | -0.97                | -0.60                       | -0.15                       |
| CSD          | XGBoost  | 20.53                              | 17.15                       | +3.37                | +0.88                       | +1.22                       |
| Danskvand    | LightGBM | 33.88                              | 25.71                       | +8.18                | +0.86                       | +0.98                       |
| Danskvand    | XGBoost  | 34.19                              | 21.20                       | +12.99               | +1.29                       | +2.21                       |
| Energidrikke | LightGBM | 17.72                              | 20.98                       | -3.26                | +0.12                       | -0.64                       |
| Energidrikke | XGBoost  | 19.17                              | 17.98                       | +1.19                | +0.57                       | -0.61                       |
| RTD          | LightGBM | 29.18                              | 33.26                       | -4.08                | -1.51                       | -1.40                       |
| RTD          | XGBoost  | 30.68                              | 35.67                       | -4.98                | -1.96                       | -4.92                       |

*Note.* Tuning improved the baseline itself by up to 12.99 percentage points. Where a fixed configuration is badly mis-specified, a feature comparison measured against it reflects that mis-specification rather than the features.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

This table is why the fixed-configuration ablation was not reported. Danskvand's trees were mis-specified by ~12pp, and that category flips from harmful to helpful once the model can fit. An ablation is only interpretable against a properly specified model.

Methodological point worth a sentence in the text: the direction of a feature effect can invert under tuning.
