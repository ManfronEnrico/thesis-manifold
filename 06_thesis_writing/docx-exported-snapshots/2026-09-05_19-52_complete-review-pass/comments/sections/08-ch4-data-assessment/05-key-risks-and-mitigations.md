# Comments -- Key Risks and Mitigations

> Objections on **Data Assessment > Key Risks and Mitigations**
>
> Prose: `chapters/sections/08-ch4-data-assessment/05-key-risks-and-mitigations.md`
>
> 2 comment(s) in 2 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
2 comment(s) in 2 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [193](#c193) | Key Risks and Mitigations | VERIFY, PROSE |  | VERIFY & PROSE... |
| [194](#c194) | Key Risks and Mitigations | SOURCE |  | SOURCE: So far only one singular source in chapter 4. Needs more as can be seen ... |

---

<a id="c193"></a>

## [193] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > Key Risks and Mitigations
- **Date:** 2026-09-03T17:34:00
- **On:** “Figures verified (resolved). All structural, data-quality, and EDA figures in this chapter are recomputed locally from the data/raw parquets under the DVH EXCL. HD scope (2026-06-27), superseding the earlier P0023 audit values; no placeholders remain. Residual dependence is only on Brian’s final harmonised pipeline, against which the local figures are expected to reconcile.Market scope (resolved). Confirmed locally that the inherited “All Markets” aggregation double-counts (6.16× inflation for CSD; 14–17× for the other three categories, which expose 86 market levels). Resolved by scoping all four categories to the single DVH EXCL. HD market level; feature matrices regenerated accordingly (2026-06-23) under DVH EXCL. HD + MIN_PERIODS=30.Per-category EDA (resolved). All four categories now have a dedicated EDA recomputed under DVH EXCL. HD (§4.3.6): stationarity (three of four series I(1), RTD stationary in level), short-horizon autocorrelation (lag-1 +0.55…+0.82), seasonality, and promo correlation. MIN_PERIODS and LAGS transfer reasonably across categories; PEAK_MONTHS is derived per category rather than inherited, since the four seasonal profiles differ materially. Per-brand lag optimisation remains a stated scope bound.Thin training windows (danskvand, RTD). Both have only 23 training months, marginally below the ~24-period ARIMA rule of thumb, and danskvand has just 24 retained brands. Mitigation: these three categories are framed as parallel proofs of concept rather than primary evidence; CSD (42 periods, 77 brands) is the worked category carrying the main claims, and t […791 more characters — see the chapter file…] cibility is limited to processed features, code, and protocol.Generalisability bound. Findings are bounded to the DVH EXCL. HD scope, the available period window, and the fully observed series filter; applicability to other markets, intermittent series, or non-beverage categories is future research.”

VERIFY & PROSE

<a id="c194"></a>

## [194] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Key Risks and Mitigations
- **Date:** 2026-09-03T17:35:00
- **On:** “research”

SOURCE: So far only one singular source in chapter 4. Needs more as can be seen in the previous comments
