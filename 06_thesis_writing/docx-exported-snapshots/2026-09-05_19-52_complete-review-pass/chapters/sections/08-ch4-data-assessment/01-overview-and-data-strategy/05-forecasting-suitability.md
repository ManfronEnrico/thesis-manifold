# Forecasting Suitability

> Section of **Data Assessment > Overview and Data Strategy > Forecasting Suitability**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, SOURCE, OUTDATED. Detail: `comments/sections/08-ch4-data-assessment/01-overview-and-data-strategy/05-forecasting-suitability.md`

---

The panel must support the forecasting models. The 37–42-month span exceeds the ARIMA minimum of roughly 24 periods for stable parameter identification and contains enough annual cycles for seasonality to be learned by both decomposition and gradient-boosted models. Benchmarking (Chapter 6) is conducted on the brand series retained by the ≥30-month filter (77 / 24 / 27 / 42 brands for CSD / danskvand / energidrikke / RTD), so that model comparisons are not confounded by very short series; missing months within a retained series are exposed on the regular monthly grid and handled natively by the models rather than imputed. A stricter, fully observed subset (brands present in every period) comprises 57 / 22 / 18 / 37 brands respectively. Applicability to shorter or intermittent series is a bound on external validity, not a claim of this thesis.
