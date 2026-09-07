# Comments -- 4.3 Feature Engineering (forecasting substrate)

> Objections on **Chapter 4 | Data Assessment > 4.3 Feature Engineering (forecasting substrate)**
>
> Prose: `chapters/sections/08-ch4-data-assessment/03-4-3-feature-engineering-forecasting-substrate.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-07 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [185](#c185) | 4.3 Feature Engineering (forecasting substrat | VERIFY, UPDATE |  | VERIFY & UPDATE: As we are thinking about including exogenous features (holiday ... |
| [187](#c187) | 4.3 Feature Engineering (forecasting substrat |  |  | VERIFICATION... |
| [188](#c188) | 4.3 Feature Engineering (forecasting substrat | VERIFY, SOURCE |  | VERIFY & SOURCE... |
| [189](#c189) | 4.3 Feature Engineering (forecasting substrat | SOURCE |  | SOURCE... |

---

<a id="c185"></a>

## [185] Brian Rohde -- Chapter 4 | Data Assessment  `VERIFY * UPDATE`

- **Section:** Chapter 4 | Data Assessment > 4.3 Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:13:00
- **On:** “The feature matrix contains 22 columns: 17 modelling features per observation”

VERIFY & UPDATE: As we are thinking about including exogenous features (holiday calendar)

<a id="c187"></a>

## [187] Brian Rohde -- Chapter 4 | Data Assessment

- **Section:** Chapter 4 | Data Assessment > 4.3 Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:23:00
- **On:** “Table 4 - Feature Engineering Overview”

VERIFICATION

<a id="c188"></a>

## [188] Brian Rohde -- Chapter 4 | Data Assessment  `VERIFY * SOURCE`

- **Section:** Chapter 4 | Data Assessment > 4.3 Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:23:00
- **On:** “log_sales_units is the modelling target (the models predict log sales and exponentiate back), not an input feature - using it as a predictor would be trivial leakage; and weighted_distribution is the fourteenth input feature, while the raw promo_units column is carried through the matrix but is not itself a model input (only its derived “promo_intensity” is)”

VERIFY & SOURCE

<a id="c189"></a>

## [189] Brian Rohde -- Chapter 4 | Data Assessment  `SOURCE`

- **Section:** Chapter 4 | Data Assessment > 4.3 Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:26:00
- **On:** “so the tree models handle NaN natively and the linear model receives a zero-fill at fit time.”

SOURCE
