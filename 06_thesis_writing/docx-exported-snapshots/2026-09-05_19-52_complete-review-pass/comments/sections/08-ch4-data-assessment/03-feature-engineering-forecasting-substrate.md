# Comments -- Feature Engineering (forecasting substrate)

> Objections on **Data Assessment > Feature Engineering (forecasting substrate)**
>
> Prose: `chapters/sections/08-ch4-data-assessment/03-feature-engineering-forecasting-substrate.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [177](#c177) | Feature Engineering (forecasting substrate) | VERIFY, UPDATE |  | VERIFY & UPDATE: As we are thinking about including exogenous features (holiday ... |
| [179](#c179) | Feature Engineering (forecasting substrate) |  |  | VERIFICATION... |
| [180](#c180) | Feature Engineering (forecasting substrate) | VERIFY, SOURCE |  | VERIFY & SOURCE... |
| [181](#c181) | Feature Engineering (forecasting substrate) | SOURCE |  | SOURCE... |

---

<a id="c177"></a>

## [177] Brian Rohde -- Data Assessment  `VERIFY * UPDATE`

- **Section:** Data Assessment > Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:13:00
- **On:** “The feature matrix contains 22 columns: 14 modelling features per observation”

VERIFY & UPDATE: As we are thinking about including exogenous features (holiday calendar)

<a id="c179"></a>

## [179] Brian Rohde -- Data Assessment

- **Section:** Data Assessment > Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:23:00
- **On:** “Table 4 - Feature Engineering Overview”

VERIFICATION

<a id="c180"></a>

## [180] Brian Rohde -- Data Assessment  `VERIFY * SOURCE`

- **Section:** Data Assessment > Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:23:00
- **On:** “log_”sales_units” is the modelling target (the models predict log sales and exponentiate back), not an input feature - using it as a predictor would be trivial leakage; and weighted_distribution is the fourteenth input feature, while the raw promo_units column is carried through the matrix but is not itself a model input (only its derived “promo_intensity” is)”

VERIFY & SOURCE

<a id="c181"></a>

## [181] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Feature Engineering (forecasting substrate)
- **Date:** 2026-09-03T17:26:00
- **On:** “so the tree models handle NaN natively and the linear model receives a zero-fill at fit time.”

SOURCE
