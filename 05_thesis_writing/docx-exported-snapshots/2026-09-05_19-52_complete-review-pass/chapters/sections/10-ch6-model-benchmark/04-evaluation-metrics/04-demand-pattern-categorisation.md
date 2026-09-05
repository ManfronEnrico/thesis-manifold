# Demand-pattern categorisation

> Section of **Model Benchmark & Selection > Evaluation metrics > Demand-pattern categorisation**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, SOURCE, TABLE-REFERENCE, PROSE, NAMING. Detail: `comments/sections/10-ch6-model-benchmark/04-evaluation-metrics/04-demand-pattern-categorisation.md`

---

Brand-level demand on this panel ranges from steady weekly sellers to series with long gaps and highly variable order sizes. Reporting a single pooled accuracy figure across that range obscures more than it conveys, and thresholding the difficult series away would reproduce exactly the practice the metric literature objects to.
Each brand is therefore classified using the scheme of Syntetos, Boylan and Croston (2005, p. 495), on two measured quantities with **derived** cut-offs:
**p**  - average inter-demand interval (periods per non-zero demand)
**CV²**  - squared coefficient of variation of **non-zero** demand sizes
|  | CV² ≤ 0.49 | CV² > 0.49 |
|---|---|---|
| p ≤ 1.32 | smooth | erratic |
| p > 1.32 | intermittent | lumpy |
**Table** **10** - NO IDEA
The thresholds are not tuned to this data: they mark where the relative accuracy ordering of Croston’s method, the Syntetos–Boylan Approximation and simple exponential smoothing changes. Classification uses **train and validation periods only**  - deriving classes from test rows and then reporting test accuracy per class would leak.
| Category | smooth | erratic | intermittent | lumpy |
|---|---|---|---|---|
| CSD | 44 | 32 | 5 | 14 |
| RTD | 32 | 20 | 2 | 8 |
| energidrikke | 16 | 18 | 2 | 8 |
| danskvand | 16 | 9 | 3 | 1 |
**Table** **11** - Category Resulting Distribution (230 brands)
**This categorises; it does not exclude.** Accuracy is reported per class, so weak performance on lumpy series appears as a stated limitation rather than as an absence. That is the response Syntetos and Boylan’s own work recommends - their contribution is estimators for such series, not advice to discard them.
