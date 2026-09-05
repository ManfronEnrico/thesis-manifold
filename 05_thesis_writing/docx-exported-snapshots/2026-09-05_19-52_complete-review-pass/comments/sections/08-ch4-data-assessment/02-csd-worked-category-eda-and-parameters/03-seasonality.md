# Comments -- Seasonality

> Objections on **Data Assessment > CSD - Worked Category (EDA and Parameters) > Seasonality**
>
> Prose: `chapters/sections/08-ch4-data-assessment/02-csd-worked-category-eda-and-parameters/03-seasonality.md`
>
> 1 comment(s) in 1 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
1 comment(s) in 1 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [165](#c165) | Seasonality | VERIFY, PROSE |  | VERIFY & PROSE & METADATA... |

---

<a id="c165"></a>

## [165] Brian Rohde -- Data Assessment  `VERIFY * PROSE`

- **Section:** Data Assessment > CSD - Worked Category (EDA and Parameters) > Seasonality
- **Date:** 2026-09-03T13:40:00
- **On:** “SeasonalityPeak months (share of annual units, DVH EXCL. HD): December (12.8%), March (10.9%), June (8.9%); September is next at 8.5%.Peak-month indicator: PEAK_MONTHS - months whose mean “sales_units” exceeds the category’s overall mean by more than 10%, measured per category. For CSD this gives {3, 6, 9, 12}. Renamed from HOLIDAY_MONTHS (2026-08-18). No holiday calendar is an input to the pipeline, so the former name asserted a cause the computation never established. The evidence often contradicts it: CSD’s peaks are the quarter-end months, consistent with retail trade loading rather than holidays.Now verified per category, resolving the open question: CSD {3, 6, 9, 12}; Danskvand {6, 7, 8, 9} (summer - bottled water); Energidrikke {3, 6, 9} (quarter-ends, no December peak); RTD {5, 6, 12}. Four distinct seasonal profiles, each commercially plausible for its category.The earlier {3, 6, 12} came from a top-quartile rule on monthly totals, which is confounded by how many brands were active in a month. The current rule uses means, which is not - the panel is unbalanced by construction. September enters CSD’s set under the corrected rule.”

VERIFY & PROSE & METADATA
