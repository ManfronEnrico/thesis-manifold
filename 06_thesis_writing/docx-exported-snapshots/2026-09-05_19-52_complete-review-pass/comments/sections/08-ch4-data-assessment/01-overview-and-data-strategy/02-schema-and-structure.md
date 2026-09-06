# Comments -- Schema and Structure

> Objections on **Data Assessment > Overview and Data Strategy > Schema and Structure**
>
> Prose: `chapters/sections/08-ch4-data-assessment/01-overview-and-data-strategy/02-schema-and-structure.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [142](#c142) | Schema and Structure | APPENDIX |  | VERIFICATION & APPENDIX: Double check claims, and also we need a reference to th... |
| [143](#c143) | Schema and Structure | OUTDATED, APPENDIX |  | OUTDATED & VERIFICATION & APPENDIX: This must be updated. Also this table might ... |
| [145](#c145) | Schema and Structure | VERIFY |  | VERIFY... |
| [146](#c146) | Schema and Structure | OUTDATED |  | OUTDATED: We have an updated reasoning in the code for the period selection, wri... |

---

<a id="c142"></a>

## [142] Brian Rohde -- Data Assessment  `APPENDIX`

- **Section:** Data Assessment > Overview and Data Strategy > Schema and Structure
- **Date:** 2026-09-03T13:26:00
- **On:** “Each category follows a star schema: dimension tables for market, period, and product, linked to a facts table at the grain of market × product × period. The facts table records the core sales metrics (sales value, sales in litres, sales units), their promotional variants (the same metrics under promotion), and a weighted-distribution metric that proxies product availability. The product dimension captures brand, manufacturer, packaging format, flavour or type, price tier, and corporate attribution.”

VERIFICATION & APPENDIX: Double check claims, and also we need a reference to the to-be generated data model.

<a id="c143"></a>

## [143] Brian Rohde -- Data Assessment  `OUTDATED * APPENDIX`

- **Section:** Data Assessment > Overview and Data Strategy > Schema and Structure
- **Date:** 2026-09-03T13:28:00
- **On:** “RTD | 37 | 93 | 0 ⚠️ | 42 | 589 | 511 | 2,193 | 44,449”

OUTDATED & VERIFICATION & APPENDIX: This must be updated. Also this table might be a good candidate to move into the appendix. Or at the least eh lengthy definitions and description.

<a id="c145"></a>

## [145] Brian Rohde -- Data Assessment  `VERIFY`

- **Section:** Data Assessment > Overview and Data Strategy > Schema and Structure
- **Date:** 2026-09-05T16:54:00
- **On:** “Per-category training structure, filtered to DVH EXCL. HD scope (2026-06-27)”

VERIFY

<a id="c146"></a>

## [146] Brian Rohde -- Data Assessment  `OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Schema and Structure
- **Date:** 2026-09-03T13:29:00
- **On:** “RTD have only 37–39 monthly periods, so a ≥40-observation filter retains zero brands for them; a single global threshold of ≥30 is therefore adopted across all categories (CSD 77, danskvand 24, energidrikke 27, RTD 42 brands), which is both feasible and consistent - preferable to the inherited mixed rule (40 for CSD, 30 for the rest). The bold column (≥30) is the retained set used downstream.”

OUTDATED: We have an updated reasoning in the code for the period selection, writing notes, or plans.
