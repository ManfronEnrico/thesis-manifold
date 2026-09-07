# Scaled error (MASE)

> Section of **Model Benchmark & Selection > Results > Scaled error (MASE)**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**3 comment(s) on this section** -- VERIFY, PROSE, NAMING. Detail: `comments/sections/10-ch6-model-benchmark/05-results/03-scaled-error-mase.md`

---

WMAPE compares models within a category but says nothing about whether a category is forecastable at all. MASE answers that directly: below 1 beats the in-sample naive forecast. mase.csv.
| Category | Naive MASE | Seasonal-naive MASE | Naive median ASE |
|---|---|---|---|
| CSD | 0.95 | 1.63 | 0.39 |
| danskvand | 0.99 | 1.60 | 0.52 |
| energidrikke | 0.67 | 2.02 | 0.05 |
| RTD | 6.54 | 14.02 | 0.18 |
**Table** **14** - Categories: MASE Comparison
RTD’s mean MASE of 6.54 against a median ASE of 0.18 is a distributional finding, not an accuracy one. The typical RTD series is forecast *better* than naive; the mean is carried by a small number of cells with very large scaled errors. Reporting only the mean would describe RTD as catastrophically unforecastable, and only the median would conceal that a few series are. Both are reported for this reason.
Seasonal naive scores worse than naive on MASE in every category while winning on WMAPE for RTD - the two metrics weight differently (volume versus per-series scale), and the disagreement is surfaced rather than resolved by picking one.
