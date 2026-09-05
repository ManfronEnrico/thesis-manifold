# Comments -- Data Sources

> Objections on **Methodology > Data Sources**
>
> Prose: `chapters/sections/07-ch3-methodology/04-data-sources.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [104](#c104) | Data Sources |  |  | We must mention why we removed totalbeer from the training and evaluation... |
| [105](#c105) | Data Sources | APPENDIX |  | APPENDIX: This could use a proper generated star schema image, based on the actu... |
| [106](#c106) | Data Sources | OUTDATED |  | OUTDATED: This is not correct. It provides data up to the past month, and is upd... |
| [107](#c107) | Data Sources | APPENDIX, CONTEXT |  | CONTEXT: This could use some actual feature descriptions from the nielsen metada... |

---

<a id="c104"></a>

## [104] Brian Rohde -- Methodology

- **Section:** Methodology > Data Sources
- **Date:** 2026-09-03T12:10:00
- **On:** “beer (totalbeer).”

We must mention why we removed totalbeer from the training and evaluation

<a id="c105"></a>

## [105] Brian Rohde -- Methodology  `APPENDIX`

- **Section:** Methodology > Data Sources
- **Date:** 2026-09-03T11:42:00
- **On:** “sales value, sales in litres, sales units, and weighted distribution at the brand-times-retailer-times-period level, linked to dimension tables for market, period, and product”

APPENDIX: This could use a proper generated star schema image, based on the actual features of each dataset. We dont have proper database access (e.g. Postgres), so we must AI generate the illustraiton, but based on actual verified facts.

<a id="c106"></a>

## [106] Brian Rohde -- Methodology  `OUTDATED`

- **Section:** Methodology > Data Sources
- **Date:** 2026-09-03T11:42:00
- **On:** “March 2026”

OUTDATED: This is not correct. It provides data up to the past month, and is updated monthly. So in case of our thesis handin date that would include up to august 2026

<a id="c107"></a>

## [107] Brian Rohde -- Methodology  `APPENDIX * CONTEXT`

- **Section:** Methodology > Data Sources
- **Date:** 2026-09-03T11:45:00
- **On:** “The sales metrics include both base and promotional variants, enabling the identification of promotional uplifts as a feature engineering input. The weighted distribution metric provides a proxy for product availability, which is a meaningful predictor of sales volume for categories with intermittent distribution. The Nielsen dataset is used under a confidentiality agreement with Manifold AI.”

CONTEXT: This could use some actual feature descriptions from the nielsen metadata. 


APPENDIX: The data dictionary from the metadata files could use a appendix image of the table. Probably a condensed version that spans all of the analysed categories, so we dont need 4 tables
