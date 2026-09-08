# 5.4.2 Scorability, and what is excluded from what

> Section of **Chapter 5 | Model Benchmark & Selection > 5.4 Evaluation metrics > 5.4.2 Scorability, and what is excluded from what**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, TABLE-REFERENCE, PROSE. Detail: `comments/sections/09-ch5-framework-design/04-5-4-evaluation-metrics/02-5-4-2-scorability-and-what-is-excluded-from-what.md`

---

Between 14% and 29% of test rows per category have a zero actual, where APE is undefined. Two distinct decisions follow, and they are **not** the same rule:
| Rule | Applies to | Basis |
|---|---|---|
| Exclude zero-actual rows | Median APE and MAPE only | Mathematical - APE is undefined there |
| *(nothing else)* | - | - |
**Table** **9** - Exclud Zero-Actual Rows Decision
**WMAPE and MASE are computed on every row.** Both are defined at zero actuals, so neither requires an exclusion, and none is applied.
Irregular series are handled by **categorisation rather than removal**  - see §6.4.4.
