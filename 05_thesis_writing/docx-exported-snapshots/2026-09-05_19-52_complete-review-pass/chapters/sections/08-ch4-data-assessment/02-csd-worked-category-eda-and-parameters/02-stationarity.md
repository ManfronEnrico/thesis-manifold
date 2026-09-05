# Stationarity

> Section of **Data Assessment > CSD - Worked Category (EDA and Parameters) > Stationarity**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/08-ch4-data-assessment/02-csd-worked-category-eda-and-parameters/02-stationarity.md`

---

**ADF test (aggregate monthly total, n = 42, DVH EXCL. HD)**: the level series is non-stationary in both raw (p = 0.360) and log form (p = 0.421); it becomes stationary only after first differencing (p < 0.001) - i.e. the series is difference-stationary, I(1). This **revises** Brian’s all-markets finding that the log level was stationary (p = 0.028): that does not hold at the corrected scope. (ADF power is limited at n = 42.)
**Treatment**: a natural-log transform is applied to “sales_units” to stabilise variance; non-stationarity in the mean is handled by **differencing** for ARIMA and by **lagged/rolling features** for the tree models (which do not require a stationary level). NaN is preserved for non-positive/missing values rather than imputed.
