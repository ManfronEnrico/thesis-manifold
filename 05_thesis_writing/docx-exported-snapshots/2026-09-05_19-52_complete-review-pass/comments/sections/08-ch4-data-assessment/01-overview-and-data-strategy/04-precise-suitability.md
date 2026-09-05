# Comments -- Precise Suitability

> Objections on **Data Assessment > Overview and Data Strategy > Precise Suitability**
>
> Prose: `chapters/sections/08-ch4-data-assessment/01-overview-and-data-strategy/04-precise-suitability.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [151](#c151) | Precise Suitability | SOURCE |  | SOURCE... |
| [152](#c152) | Precise Suitability | OUTDATED, CONTEXT |  | CONTEXT & OUTDATED & VERIFICATION: Justification WHY as zero rather than null. A... |
| [153](#c153) | Precise Suitability | OUTDATED |  | OUTDATED & VERIFICATION... |
| [154](#c154) | Precise Suitability | VERIFY, OUTDATED |  | OUTDATED & VERIFY: I believe here we said that we cant be sure about it, or whet... |

---

<a id="c151"></a>

## [151] Brian Rohde -- Data Assessment  `SOURCE`

- **Section:** Data Assessment > Overview and Data Strategy > Precise Suitability
- **Date:** 2026-09-03T13:33:00
- **On:** “Nielsen is an established commercial panel provider whose continued operation depends on data credibility; its scanner data are therefore treated as reliable, while recognising that, as with any provider, definitions and collection conventions are fixed by Nielsen rather than by the researcher.”

SOURCE

<a id="c152"></a>

## [152] Brian Rohde -- Data Assessment  `OUTDATED * CONTEXT`

- **Section:** Data Assessment > Overview and Data Strategy > Precise Suitability
- **Date:** 2026-09-03T13:35:00
- **On:** “it is fully populated (0.00% null), with the absence of promotional activity encoded as a zero rather than a null”

CONTEXT & OUTDATED & VERIFICATION: Justification WHY as zero rather than null. Actually I believe our current code does the exact opposite, where we assigned zero meaning, and null genuinely absent (e.g. unrecorded). Please verify

<a id="c153"></a>

## [153] Brian Rohde -- Data Assessment  `OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Precise Suitability
- **Date:** 2026-09-03T13:35:00
- **On:** “Weighted-distribution nulls: negligible across all categories - 0.019% (CSD), 0.016% (danskvand), 0.093% (energidrikke), 0.000% (RTD).”

OUTDATED & VERIFICATION

<a id="c154"></a>

## [154] Brian Rohde -- Data Assessment  `VERIFY * OUTDATED`

- **Section:** Data Assessment > Overview and Data Strategy > Precise Suitability
- **Date:** 2026-09-03T13:36:00
- **On:** “Negative and zero values: negatives are return/correction adjustments standard in scanner data and are clipped to zero - they are rare (CSD 58 rows, 0.031%; danskvand 14, 0.057%; energidrikke 16, 0.032%; RTD 10, 0.022%).”

OUTDATED & VERIFY: I believe here we said that we cant be sure about it, or whether negative numbers are a measurement error or actually returns, so we floored negative numbers to 0.
