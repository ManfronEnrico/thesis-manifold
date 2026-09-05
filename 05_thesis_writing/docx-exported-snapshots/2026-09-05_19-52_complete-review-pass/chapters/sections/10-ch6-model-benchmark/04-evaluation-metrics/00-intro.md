# Evaluation metrics

> Section of **Model Benchmark & Selection > Evaluation metrics**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY. Detail: `comments/sections/10-ch6-model-benchmark/04-evaluation-metrics/00-intro.md`

---

| Metric | Definition | Rationale |
|---|---|---|
| WMAPE | Σ\|y−ŷ\| / Σ\|y\| × 100 | Primary. Volume-weighted, defined at zero actuals, and consistent for the median (see below) |
| Median APE | median(\|y−ŷ\|/y) over y > 0 | Robust per-series view; undefined where y = 0 |
| MASE | mean(\|y−ŷ\|) / in-sample MAE of the naive forecast, per series | Scale-free, defined at zero, and absolutely interpretable: < 1 beats a naive forecast |
| Coverage (80 / 90% PI) | share of actuals inside the interval | Calibration signal for SRQ2 |
| Median relative interval width | interval width ÷ actual | Reported beside coverage - see below |
| Peak RAM (MB) | tracemalloc peak | The operational constraint |
| Inference latency (ms) | wall-clock prediction time | Agent responsiveness |
**Plain mean MAPE is not reported.** It is undefined against a zero actual and diverges to meaningless magnitudes near zero - on this panel it reaches 10¹³ - because percentage errors are “infinite or undefined if Yₜ = 0 … and have an extremely skewed distribution when any value of Yₜ is close to zero” (Hyndman & Koehler, 2006, p. 683).
