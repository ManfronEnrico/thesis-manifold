# Comments -- Feature engineering

> Objections on **Model Benchmark & Selection > Experimental setup > Feature engineering**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/03-experimental-setup/02-feature-engineering.md`
>
> 1 comment(s) in 1 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
1 comment(s) in 1 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [254](#c254) | Feature engineering | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCES, PROSE... |

---

<a id="c254"></a>

## [254] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Experimental setup > Feature engineering
- **Date:** 2026-09-05T15:25:00
- **On:** “Feature engineeringLags: t−1, t−2, t−3, t−4, t−8, t−13 monthsRolling statistics: 4-month and 13-month mean; 4-month standard deviationCalendar: month, quarter, and a binary peak_month flag derived from the category’s own seasonal profile (months whose mean units exceed the category mean by more than 10%). No holiday calendar is used - the flag is measured from the sales distribution, not from calendar datesPromotional: “promo_intensity” (promotional share of units, clipped to [0,1], lagged one period). Available for CSD and energidrikke only - Nielsen reports no promotional measure for danskvand or RTD, so the feature is omitted rather than zero-filled, since a constant zero would assert that no promotion ranMissing lag values for short histories are left as NaN (handled natively by the tree models); Ridge receives a zero-fill at fit time”

VERIFY, SOURCES, PROSE
