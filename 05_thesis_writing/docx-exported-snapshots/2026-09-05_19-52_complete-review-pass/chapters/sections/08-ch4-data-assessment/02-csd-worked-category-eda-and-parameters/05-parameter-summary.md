# Parameter Summary

> Section of **Data Assessment > CSD - Worked Category (EDA and Parameters) > Parameter Summary**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE, APPENDIX. Detail: `comments/sections/08-ch4-data-assessment/02-csd-worked-category-eda-and-parameters/05-parameter-summary.md`

---

| Parameter | Value (CSD) | Basis | Status |
|---|---|---|---|
| MIN_PERIODS | 30 (global) | feasibility (other cats have 37–39 periods) + quality | adopted |
| LAGS | 1, 2, 3, 4, 8, 13 | ACF/PACF inspection | empirical; needs prose justification |
| ROLLING_WINDOWS | 4, 13 | 4-month + annual cycle | empirical |
| PEAK_MONTHS | per category: CSD 3,6,9,12; Danskvand 6,7,8,9; Energidrikke 3,6,9; RTD 5,6,12 | mean monthly units >10% above the category mean | derived per category |
| log transform | applied to “sales_units” | variance stabilisation; series is I(1), diff-stationary (ADF p<0.001) | confirmed |
| Train / Val / Test | 24 / 6 / 12 months | forward-chaining (Section 4.5) | confirmed |
**Table** **2** - EDA Parameter Overview
These parameters are EDA-driven rather than theory-first; their academic justification is developed in the modelling chapter, and their empirical (not theoretical) origin is stated honestly as a limitation.
