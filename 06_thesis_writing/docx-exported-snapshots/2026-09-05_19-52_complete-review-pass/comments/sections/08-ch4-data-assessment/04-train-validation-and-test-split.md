# Comments -- Train, Validation, and Test Split

> Objections on **Data Assessment > Train, Validation, and Test Split**
>
> Prose: `chapters/sections/08-ch4-data-assessment/04-train-validation-and-test-split.md`
>
> 8 comment(s) in 8 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
8 comment(s) in 8 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [183](#c183) | Train, Validation, and Test Split | INCORRECT |  | INCORRECT: Dynamic Train/Test/Val sets based on percentage cutoff.... |
| [184](#c184) | Train, Validation, and Test Split | SOURCE |  | SOURCE... |
| [185](#c185) | Train, Validation, and Test Split | INCORRECT |  | INCORRECT: Not locked... |
| [187](#c187) | Train, Validation, and Test Split | INCORRECT |  | INCORRECT... |
| [188](#c188) | Train, Validation, and Test Split | VERIFY |  | VERIFY... |
| [189](#c189) | Train, Validation, and Test Split | SOURCE |  | SOURCE... |
| [190](#c190) | Train, Validation, and Test Split | METACOMMENT |  | METACOMMENT... |
| [191](#c191) | Train, Validation, and Test Split | INCORRECT |  | INCORRECT... |

---

<a id="c183"></a>

## [183] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:27:00
- **On:** “calendar date and locked as a pre-specified design decision, applied identically across the forecasting models and across categories”

INCORRECT: Dynamic Train/Test/Val sets based on percentage cutoff.

<a id="c184"></a>

## [184] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:28:00
- **On:** “ARIMA minimum (~24 periods) and to contain at least two seasonal cycles for Prophet”

SOURCE

<a id="c185"></a>

## [185] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:28:00
- **On:** “The per-category boundaries, taken from the locked split files (<cat>_split_dates.json),”

INCORRECT: Not locked

<a id="c187"></a>

## [187] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:32:00
- **On:** “(locked, pre-registered)”

INCORRECT

<a id="c188"></a>

## [188] Brian Rohde -- Data Assessment  `VERIFY`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:32:00
- **On:** “CSD, the longest series, takes a 12-month test window covering a full annual cycle; the three shorter categories take an 8-month test window (a ≥40-month series would be needed for a 12-month test under the same rule)”

VERIFY

<a id="c189"></a>

## [189] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:33:00
- **On:** “ARIMA minimum (~24 periods; danskvand and RTD at 23 are marginally below”

SOURCE

<a id="c190"></a>

## [190] Brian Rohde -- Data Assessment  `METACOMMENT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:33:00
- **On:** “are flagged as a thin-data caveat in §4.6)”

METACOMMENT

<a id="c191"></a>

## [191] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Train, Validation, and Test Split
- **Date:** 2026-09-03T17:33:00
- **On:** “All test windows end in March 2026”

INCORRECT
