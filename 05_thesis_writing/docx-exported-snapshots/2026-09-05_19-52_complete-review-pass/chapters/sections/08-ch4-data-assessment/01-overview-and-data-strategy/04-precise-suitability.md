# Precise Suitability

> Section of **Data Assessment > Overview and Data Strategy > Precise Suitability**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**4 comment(s) on this section** -- SOURCE, OUTDATED, CONTEXT, VERIFY. Detail: `comments/sections/08-ch4-data-assessment/01-overview-and-data-strategy/04-precise-suitability.md`

---

**Reliability / dependability.**  Nielsen is an established commercial panel provider whose continued operation depends on data credibility; its scanner data are therefore treated as reliable, while recognising that, as with any provider, definitions and collection conventions are fixed by Nielsen rather than by the researcher.
**Validity / credibility.** Credibility rests on how the data were collected and compiled (scanner capture aggregated to the market × product × period grain). Definitions (market aggregates such as DVH EXCL. HD, metric definitions, corporate attribution) are provider-set and are documented rather than altered.
**Measurement bias / trustworthiness.** Three data patterns require explicit treatment; per-category figures, computed locally on the in-scope facts, are reported below: - *Promotional values*: where the promotional metric exists (CSD and energidrikke) it is fully populated (0.00% null), with the absence of promotional activity encoded as a zero rather than a null; for **danskvand** and **RTD** the promotional column is absent entirely, collapsing to the promo-zero case above. - *Weighted-distribution nulls*: negligible across all categories - 0.019% (CSD), 0.016% (danskvand), 0.093% (energidrikke), 0.000% (RTD). These reflect products Nielsen does not track for distribution in a given period; they are imputed using a brand-and-market median, which preserves central tendency but ignores within-period time variation (a moderate limitation for niche brands, immaterial at these null rates). - *Negative and zero values*: negatives are return/correction adjustments standard in scanner data and are clipped to zero - they are rare (CSD 58 rows, 0.031%; danskvand 14, 0.057%; energidrikke 16, 0.032%; RTD 10, 0.022%). True zero-sales rows are likewise rare (CSD 12, danskvand 1, energidrikke 28, RTD 17) and are retained and flagged as genuine zeros, distinct from corrections. Core sales metrics are complete: “sales_units” has 0.00% nulls in every category, confirmed locally.
