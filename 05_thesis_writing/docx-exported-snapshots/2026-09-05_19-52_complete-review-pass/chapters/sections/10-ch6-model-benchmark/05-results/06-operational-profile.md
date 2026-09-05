# Operational profile

> Section of **Model Benchmark & Selection > Results > Operational profile**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY. Detail: `comments/sections/10-ch6-model-benchmark/05-results/06-operational-profile.md`

---

Peak RAM on the largest matrix is in single-digit megabytes for every model - Ridge 5.5, LightGBM 8.0, XGBoost 0.1, ARIMA 0.3 MB - against the 8 GB sequential budget of SRQ1. The memory constraint is non-binding by three orders of magnitude at this data scale, which is a real answer to the research question and not a missing measurement: the constraint that motivated the question does not bite here.
Latency is likewise immaterial: XGBoost fits in 0.97 s and predicts in 9.3 ms; LightGBM fits in 2.04 s and predicts in 15.9 ms. profiling.csv.
