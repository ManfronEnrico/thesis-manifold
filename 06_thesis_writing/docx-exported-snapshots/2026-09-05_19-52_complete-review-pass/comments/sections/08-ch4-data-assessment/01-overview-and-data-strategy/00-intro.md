# Comments -- Overview and Data Strategy

> Objections on **Data Assessment > Overview and Data Strategy**
>
> Prose: `chapters/sections/08-ch4-data-assessment/01-overview-and-data-strategy/00-intro.md`
>
> 5 comment(s) in 5 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
5 comment(s) in 5 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [133](#c133) | Overview and Data Strategy | ACADEMIC |  | ACADEMIC: Reading through the thesis from front to back i noticed that we kind o... |
| [134](#c134) | Overview and Data Strategy | INCORRECT |  | INCORRECT: This is not the reason it was scoped out. The fact table did exist, b... |
| [135](#c135) | Overview and Data Strategy | CONTEXT |  | CONTEXT: CSD is true, but the other categories were assessed for the pooled vs. ... |
| [136](#c136) | Overview and Data Strategy | VERIFY |  | VERIFY: The survey-type claim is a bit dodgy to me. This MUST be grounded in the... |
| [137](#c137) | Overview and Data Strategy | OUTDATED |  | OUTDATED: Not really true. We changed it to a proportial split, which is thus no... |

---

<a id="c133"></a>

## [133] Brian Rohde -- Data Assessment  `ACADEMIC`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:07:00
- **On:** “This thesis draws on one secondary data source in the sense of Saunders et al. (2023): data”

ACADEMIC: Reading through the thesis from front to back i noticed that we kind of repeat the same or similar information multiple times in different chapters.


I am not 100% positive if that is proper academic rigour, and supposed to be like that (e.g. allowing a reader to have some context in each chapter, while having the deep dive in the dedicated chapter), or if that is AI slop, a point for optimization. 


We might want to look at the thesis of my friend Max for reference (Graded 12/12). To see if they wrote in a similar fashion

<a id="c134"></a>

## [134] Brian Rohde -- Data Assessment  `INCORRECT`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:09:00
- **On:** “A fifth category, beer (totalbeer), was scoped out because its facts table is absent from the source data (the data do not exist at source, not a size or memory constraint); this is recorded as a data limitation rather than an analytical choice”

INCORRECT: This is not the reason it was scoped out.  The fact table did exist, but it was way too large for our laptops and internet connections to fetch, so we excluded it. So ist not a data limitation but an analytical choice, directly in conflict with your claim

<a id="c135"></a>

## [135] Brian Rohde -- Data Assessment  `CONTEXT`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:10:00
- **On:** “CSD is the worked category, assessed in full (Section 4.3); the other three are processed through the identical pipeline as parallel proofs of concept.”

CONTEXT: CSD is true, but the other categories were assessed for  the pooled vs. Specialized and potentially also the overall model performance (SRQ1 i believe). 


So just a bit more to-verify context neceassry

<a id="c136"></a>

## [136] Brian Rohde -- Data Assessment  `VERIFY`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:12:00
- **On:** “survey-type, structured, commercial secondary data”

VERIFY: The survey-type claim is a bit dodgy to me. This MUST be grounded in the metadata provided by nielsen. If not we cant claim it. I hardly believe it would be exclusively survey data, maybe not even at all, or more realistically a mix. But we cant outright claim with no evidence.

<a id="c137"></a>

## [137] Brian Rohde -- Data Assessment  `OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy
- **Date:** 2026-09-03T13:13:00
- **On:** “The train, validation, and test split is then specified as a locked, pre-registered design decision applied identically across the forecasting models”

OUTDATED: Not really true. We changed it to a proportial split, which is thus not locked in and will move upon dataset update relatively speaking in absolute cutoff points.
