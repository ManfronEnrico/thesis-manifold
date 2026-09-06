# Comments -- Stationarity

> Objections on **Data Assessment > CSD - Worked Category (EDA and Parameters) > Stationarity**
>
> Prose: `chapters/sections/08-ch4-data-assessment/02-csd-worked-category-eda-and-parameters/02-stationarity.md`
>
> 1 comment(s) in 1 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
1 comment(s) in 1 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [163](#c163) | Stationarity | VERIFY, PROSE |  | VERIFY & PROSE & METADATA... |

---

<a id="c163"></a>

## [163] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Stationarity
- **Date:** 2026-09-03T13:40:00
- **On:** “StationarityADF test (aggregate monthly total, n = 42, DVH EXCL. HD): the level series is non-stationary in both raw (p = 0.360) and log form (p = 0.421); it becomes stationary only after first differencing (p < 0.001) - i.e. the series is difference-stationary, I(1). This revises Brian’s all-markets finding that the log level was stationary (p = 0.028): that does not hold at the corrected scope. (ADF power is limited at n = 42.)Treatment: a natural-log transform is applied to “sales_units” to stabilise variance; non-stationarity in the mean is handled by differencing for ARIMA and by lagged/rolling features for the tree models (which do not require a stationary level). NaN is preserved for non-positive/missing values rather than imputed.”

VERIFY & PROSE & METADATA
