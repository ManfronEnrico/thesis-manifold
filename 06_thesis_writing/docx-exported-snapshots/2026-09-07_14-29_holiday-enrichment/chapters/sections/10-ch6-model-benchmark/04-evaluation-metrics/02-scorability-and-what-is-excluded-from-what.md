# Scorability, and what is excluded from what

> Section of **Model Benchmark & Selection > Evaluation metrics > Scorability, and what is excluded from what**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, TABLE-REFERENCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/04-evaluation-metrics/02-scorability-and-what-is-excluded-from-what.md`

---

Between 14% and 29% of test rows per category have a zero actual, where APE is undefined. Two distinct decisions follow, and they are **not** the same rule:
| Rule | Applies to | Basis |
|---|---|---|
| Exclude zero-actual rows | Median APE and MAPE only | Mathematical - APE is undefined there |
| *(nothing else)* | - | - |
**Table** **9** - Exclud Zero-Actual Rows Decision
**WMAPE and MASE are computed on every row.** Both are defined at zero actuals, so neither requires an exclusion, and none is applied.
Irregular series are handled by **categorisation rather than removal**  - see §6.4.4.
