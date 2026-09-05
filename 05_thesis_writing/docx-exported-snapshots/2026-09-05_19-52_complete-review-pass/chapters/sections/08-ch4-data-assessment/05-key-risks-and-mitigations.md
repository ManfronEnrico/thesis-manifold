# Key Risks and Mitigations

> Section of **Data Assessment > Key Risks and Mitigations**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, PROSE, SOURCE. Detail: `comments/sections/08-ch4-data-assessment/05-key-risks-and-mitigations.md`

---

**Figures verified (resolved).** All structural, data-quality, and EDA figures in this chapter are recomputed locally from the data/raw parquets under the DVH EXCL. HD scope (2026-06-27), superseding the earlier P0023 audit values; no placeholders remain. Residual dependence is only on Brian’s final harmonised pipeline, against which the local figures are expected to reconcile.
**Market scope (resolved).** Confirmed locally that the inherited “All Markets” aggregation double-counts (6.16× inflation for CSD; 14–17× for the other three categories, which expose 86 market levels). Resolved by scoping all four categories to the single DVH EXCL. HD market level; feature matrices regenerated accordingly (2026-06-23) under DVH EXCL. HD + MIN_PERIODS=30.
**Per-category EDA (resolved).** All four categories now have a dedicated EDA recomputed under DVH EXCL. HD (§4.3.6): stationarity (three of four series I(1), RTD stationary in level), short-horizon autocorrelation (lag-1 +0.55…+0.82), seasonality, and promo correlation. MIN_PERIODS and LAGS transfer reasonably across categories; PEAK_MONTHS is derived per category rather than inherited, since the four seasonal profiles differ materially. Per-brand lag optimisation remains a stated scope bound.
**Thin training windows (danskvand, RTD).** Both have only 23 training months, marginally below the ~24-period ARIMA rule of thumb, and danskvand has just 24 retained brands. Mitigation: these three categories are framed as parallel proofs of concept rather than primary evidence; CSD (42 periods, 77 brands) is the worked category carrying the main claims, and the short-window caveat is restated in the discussion.
**Empirical parameters.**  MIN_PERIODS, LAGS, ROLLING_WINDOWS, and PEAK_MONTHS are EDA-driven, not theory-first. Mitigation: justified post hoc in the modelling chapter and stated as a limitation.
**Promotional coverage (danskvand, RTD).** Promo-zero categories lack the promotional signal (an unmeasured-variable limitation). Mitigation: promotional features are disabled for these categories and the limitation is stated in the discussion.
**Weighted-distribution imputation.** Median imputation ignores within-period time variation (moderate risk for niche brands, low for high-coverage brands). Mitigation: documented; sensitivity noted.
**Commercial access / confidentiality.** Raw data cannot be redistributed and must stay local; full external reproducibility is limited to processed features, code, and protocol.
**Generalisability bound.** Findings are bounded to the DVH EXCL. HD scope, the available period window, and the fully observed series filter; applicability to other markets, intermittent series, or non-beverage categories is future research.
