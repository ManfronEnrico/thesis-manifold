# Autocorrelation and Lag Structure

> Section of **Data Assessment > CSD - Worked Category (EDA and Parameters) > Autocorrelation and Lag Structure**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/08-ch4-data-assessment/02-csd-worked-category-eda-and-parameters/04-autocorrelation-and-lag-structure.md`

---

**Lag set**: LAGS = (1, 2, 3, 4, 8, 13) and ROLLING_WINDOWS = (4, 13) (4-month and ~annual cycles on the Nielsen calendar).
**Autocorrelation (recomputed, DVH EXCL. HD)**: for the top brand by units (HARBOE, n = 42) the log-series ACF is +0.26 (lag 1), +0.47 (lag 3), and ≈0 (lag 13) - a strong quarterly (lag-3) signal but a weak annual (lag-13) one for this brand. Lag structure is clearly brand-dependent, so a single global lag set is a simplification; per-brand optimisation is out of scope. This **revises** Brian’s Coca-Cola example (lag-1 = −0.399), which was computed on the inflated all-markets series. *Method note*: the per-category figures in §4.3.6 (CSD lag-1 +0.78) use a pooled, brand-demeaned log series across all retained brands, whereas the HARBOE figures here are a single-brand series; the pooled estimate is larger because demeaning removes between-brand level differences and leaves the common short-horizon dynamics. Both are reported; the qualitative conclusion (positive short-horizon, near-zero annual carry) is robust to the method.
**Promotional intensity**: strongly correlated with sales units, confirmed under DVH EXCL. HD at r = 0.937 (n = 2,442 promo-bearing brand-month rows), closely matching Brian’s all-markets value (r = 0.941); the relationship is robust to market scope. For energidrikke the promotional signal is even stronger (r = 0.988); danskvand and RTD carry no promotional data (promo-zero).
