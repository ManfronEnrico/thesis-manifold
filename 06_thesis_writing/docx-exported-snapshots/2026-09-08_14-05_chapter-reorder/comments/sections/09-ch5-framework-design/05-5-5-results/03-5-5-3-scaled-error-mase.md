# Comments -- 5.5.3 Scaled error (MASE)

> Objections on **Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.3 Scaled error (MASE)**
>
> Prose: `chapters/sections/09-ch5-framework-design/05-5-5-results/03-5-5-3-scaled-error-mase.md`
>
> 3 comment(s) in 3 thread(s).

Extracted 2026-09-08 from `thesis_full.docx`.
3 comment(s) in 3 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [268](#c268) | 5.5.3 Scaled error (MASE) | VERIFY, PROSE |  | VERIFY & PROSE... |
| [270](#c270) | 5.5.3 Scaled error (MASE) | NAMING |  | NAMING... |
| [271](#c271) | 5.5.3 Scaled error (MASE) | VERIFY |  | VERIFY... |

---

<a id="c268"></a>

## [268] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `VERIFY * PROSE`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.3 Scaled error (MASE)
- **Date:** 2026-09-05T16:10:00
- **On:** “WMAPE compares models within a category but says nothing about whether a category is forecastable at all. MASE answers that directly: below 1 beats the in-sample naive forecast. mase.csv.Category | Naive MASE | Seasonal-naive MASE | Naive median ASE || CSD | 0.95 | 1.63 | 0.39 || danskvand | 0.99 | 1.60 | 0.52 || energidrikke | 0.67 | 2.02 | 0.05 || RTD | 6.54 | 14.02 | 0.18 || Table 14 - Categories: MASE ComparisonRTD’s mean MASE of 6.54 against a median ASE of 0.18 is a distributional finding, not an accuracy one. The typical RTD series is forecast better than naive; the mean is carried by a small number of cells with very large scaled errors. Reporting only the mean would describe RTD as catastrophically unforecastable, and only the median would conceal that a few series are. Both are reported for this reason.Seasonal naive scores worse than naive on MASE in every category while winning on WMAPE for RTD - the two metrics weight differently (volume versus per-series scale), and the disagreement is surfaced rather than resolved by picking one.Pooled versus per-category trainingWhether one model trained across all four categories beats four category-specific models is SRQ1’s central design question. Both arms use the same 12-feature intersection, the same tuning protocol, and are scored on identical test rows, so they differ only in which rows they were trained on. pooled_summary.md.Category | LightGBM pooled → per-cat | XGBoost pooled → per-cat || CSD | 17.5% → 16.3% (per-cat better by 1.2 pp) | 16.6% → 15.3% (per-cat by 1.3) || danskvand | 21.4% → 23.7% (pooling wins 2.2  […69,497 more characters — see the chapter file…] , and calendar and seasonality signals (month, quarter, and a binary peak-month indicator derived from each category’s own observed seasonal profile); these complement the models’ autoregressive features (lagged sales and rolling statistics) derived from the historical sales series itself.↩︎Appendix”

VERIFY & PROSE

<a id="c270"></a>

## [270] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `NAMING`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.3 Scaled error (MASE)
- **Date:** 2026-09-05T16:10:00
- **On:** “Table 14 - Categories: MASE Comparison”

NAMING

<a id="c271"></a>

## [271] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `VERIFY`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.5 Results > 5.5.3 Scaled error (MASE)
- **Date:** 2026-09-05T16:11:00
- **On:** “RTD’s mean MASE of 6.54 against a median ASE of 0.18 is a distributional finding, not an accuracy one. The typical RTD series is forecast better than naive; the mean is carried by a small number of cells with very large scaled errors. Reporting only the mean would describe RTD as catastrophically unforecastable, and only the median would conceal that a few series are. Both are reported for this reason.Seasonal naive scores worse than naive on MASE in every category while winning on WMAPE for RTD - the two metrics weight differently (volume versus per-series scale), and the disagreement is surfaced rather than resolved by picking one.”

VERIFY
