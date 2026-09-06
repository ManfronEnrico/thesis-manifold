# Comments -- Demand-pattern categorisation

> Objections on **Model Benchmark & Selection > Evaluation metrics > Demand-pattern categorisation**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/04-evaluation-metrics/04-demand-pattern-categorisation.md`
>
> 2 comment(s) in 2 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
2 comment(s) in 2 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [272](#c272) | Demand-pattern categorisation | VERIFY, SOURCE, TABLE-REFERENCE, PROSE |  | VERIFY, SOURCES, PROSE, TABLE REFERENCE... |
| [274](#c274) | Demand-pattern categorisation | NAMING |  | NAMING... |

---

<a id="c272"></a>

## [272] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * TABLE-REFERENCE * PROSE`

- **Section:** Model Benchmark & Selection > Evaluation metrics > Demand-pattern categorisation
- **Date:** 2026-09-05T15:29:00
- **On:** “Demand-pattern categorisationBrand-level demand on this panel ranges from steady weekly sellers to series with long gaps and highly variable order sizes. Reporting a single pooled accuracy figure across that range obscures more than it conveys, and thresholding the difficult series away would reproduce exactly the practice the metric literature objects to.Each brand is therefore classified using the scheme of Syntetos, Boylan and Croston (2005, p. 495), on two measured quantities with derived cut-offs:p - average inter-demand interval (periods per non-zero demand)CV² - squared coefficient of variation of non-zero demand sizes | CV² ≤ 0.49 | CV² > 0.49 || p ≤ 1.32 | smooth | erratic || p > 1.32 | intermittent | lumpy || Table 10 - NO IDEAThe thresholds are not tuned to this data: they mark where the relative accuracy ordering of Croston’s method, the Syntetos–Boylan Approximation and simple exponential smoothing changes. Classification uses train and validation periods only - deriving classes from test rows and then reporting test accuracy per class would leak.Category | smooth | erratic | intermittent | lumpy || CSD | 44 | 32 | 5 | 14 || RTD | 32 | 20 | 2 | 8 || energidrikke | 16 | 18 | 2 | 8 || danskvand | 16 | 9 | 3 | 1 || Table 11 - Category Resulting Distribution (230 brands)This categorises; it does not exclude. Accuracy is reported per class, so weak performance on lumpy series appears as a stated limitation rather than as an absence. That is the response Syntetos and Boylan’s own work recommends - their contribution is estimators for such series, not advice to discard them.”

VERIFY, SOURCES, PROSE, TABLE REFERENCE

<a id="c274"></a>

## [274] Brian Rohde -- Model Benchmark & Selection  `NAMING`

- **Section:** Model Benchmark & Selection > Evaluation metrics > Demand-pattern categorisation
- **Date:** 2026-09-05T16:08:00
- **On:** “Table 10 - NO IDEA”

NAMING
