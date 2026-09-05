# Per-category EDA - danskvand, energidrikke, RTD

> Section of **Data Assessment > CSD - Worked Category (EDA and Parameters) > Per-category EDA - danskvand, energidrikke, RTD**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**3 comment(s) on this section** -- VERIFY, PROSE, APPENDIX. Detail: `comments/sections/08-ch4-data-assessment/02-csd-worked-category-eda-and-parameters/06-per-category-eda-danskvand-energidrikke-rtd.md`

---

The three proof-of-concept categories were taken through the identical pipeline and their EDA recomputed under the corrected DVH EXCL. HD scope, closing the gap previously flagged in §4.6.
| Category | Promo Correl. | Peak month | Top brand | ADF (log level) | Verdict | ACF lag1 / lag3 |
|---|---|---|---|---|---|---|
| CSD | r = 0.937 | December | HARBOE | p = 0.421 | non-stationary, I(1) | +0.78 / +0.55 |
| danskvand | none (promo-zero) | June | HARBOE | p = 0.998 | non-stationary, I(1) | +0.55 / +0.25 |
| energidrikke | r = 0.988 | March | RED BULL | p = 0.901 | non-stationary, I(1) | +0.71 / +0.39 |
| RTD | none (promo-zero) | December | BREEZER | p = 0.000 | stationary in level | +0.82 / +0.58 |
**Table** **3** - Per Category Correlation & Transformations
Three of the four category-level series are difference-stationary (I(1)); RTD is already stationary in log level. All show strong positive short-horizon autocorrelation (lag-1 +0.55…+0.82), supporting the shared lag/rolling feature set, with near-zero lag-13 carry. Seasonality is category-appropriate (water peaks in summer, the others in autumn/spring). danskvand and RTD carry no promotional signal - the unmeasured-variable limitation already noted. MIN_PERIODS and LAGS transfer reasonably across categories. PEAK_MONTHS does **not** and is no longer treated as a transferable default: it is derived per category, and the four profiles differ materially (water peaks in summer, Energidrikke has no December peak). Per-series lag structure is brand-dependent and not separately optimised (a stated scope bound).
