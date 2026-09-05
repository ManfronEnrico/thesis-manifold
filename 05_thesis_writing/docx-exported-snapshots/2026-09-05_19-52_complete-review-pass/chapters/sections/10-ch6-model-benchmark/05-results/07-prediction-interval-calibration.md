# Prediction-interval calibration

> Section of **Model Benchmark & Selection > Results > Prediction-interval calibration**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, PROSE, MATH. Detail: `comments/sections/10-ch6-model-benchmark/05-results/07-prediction-interval-calibration.md`

---

A split-conformal wrapper on the tuned model, calibrated on validation residuals in log space, gives the following on the untouched test split. calibration.csv.
| Category | Nominal | Empirical coverage | Median relative width | n calib |
|---|---|---|---|---|
| CSD | 90% | 89.6% | 3.3× | 665 |
| RTD | 90% | 89.0% | 3.1× | 372 |
| danskvand | 90% | 87.4% | 16.8× | 174 |
| energidrikke | 90% | 93.5% | 8.9× | 264 |
| CSD | 80% | 78.6% | 1.9× | 665 |
| RTD | 80% | 76.1% | 1.7× | 372 |
| danskvand | 80% | 70.7% | 3.5× | 174 |
| energidrikke | 80% | 82.5% | 3.3× | 264 |
The half-width is the ⌈(n+1)(1−α)⌉/n empirical quantile of the calibration residuals - Algorithm 2 of Lei et al. (2018) - not the nominal (1−α) quantile. The finite-sample correction is what supports the distribution-free guarantee at finite *n*.
Coverage alone is the wrong success criterion, and this table shows why. An arbitrarily wide interval attains perfect coverage while carrying no decision-relevant information. danskvand meets its 90% coverage target only with intervals spanning roughly seventeen times the quantity being forecast, which no planner can act on. For danskvand and energidrikke, width - not coverage - is the binding constraint, and both are reported as limitations rather than averaged into a “well-calibrated” claim. At the 80% level danskvand additionally undercovers, at 70.7%.
