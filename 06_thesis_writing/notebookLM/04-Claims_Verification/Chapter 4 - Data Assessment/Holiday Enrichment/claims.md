---
name: ch4-holiday-enrichment-claims
description: Unverified claims appearing in Ch4 §4.3 holiday-enrichment prose. Feeds the NotebookLM factual-claims notebook (Notebook B).
chapter: 4
section: "4.3 Feature Engineering (forecasting substrate)"
topic: Holiday Enrichment
prose_source: writing-notes/srq1-holiday-enrichment-result-and-limitations.md §2.1
created: 2026_09_07-15_10
updated: 2026_09_07-15_10
---

# Ch4 §4.3 — Holiday Enrichment: claims to verify

**Status of the prose:** §2.1 is written so that **no unverified claim is asserted**. The
paragraphs below are safe to paste today. Verification would let them be *sharpened* —
it is not a precondition for using them.

---

## CV-03 — Danish shop-opening law

**Appears in prose as (safe wording, currently used):**
> "...shops trade at weekends, and many open on public holidays with reduced hours."

**The stronger wording that is NOT used, pending verification:**
> "...because Lukkeloven was liberalised in 2012."

| Part | Status |
|---|---|
| Danish retail trades weekends and often public holidays | **Confirmed by researcher** (domain knowledge). The feature design rests on this. |
| Statute named *Lukkeloven*, liberalised **2012** | **Unverified** — name and year both originated with Claude |

**To determine:**
1. Correct name of the Danish shop-opening-hours statute.
2. Date(s) of liberalisation — a staged process would make a single year wrong.
3. Does it treat public holidays differently from Sundays?

**Why it matters:** justifies naming the feature `non_holiday_days` rather than
`trading_days` — a Danish public holiday is not a closed day. The reasoning survives
without the statute; only the specifics need a source.

**If unverifiable:** keep the current wording. No edit needed.

---

## CV-05 — Store Bededag abolition

**Appears in prose as (safe wording, currently used):**
> "...the abolition of Store Bededag reduced the Danish public-holiday count from
> fifteen to fourteen partway through the panel"

This is asserted as **observed in the fetched calendar data** (appendix table 91), not as
a legislative fact — which is why it is safe as written.

**Unverified:** the bill number, the parliamentary process, the exact effective date.

**To determine:**
1. Correct legislative reference for the abolition.
2. Exact effective date.
3. Any transitional provision affecting 2023.

**Why it matters:** this is the strongest substantive argument for the whole enrichment —
a permanent mid-panel structural break that a month index cannot represent. A precise
citation would strengthen it.

**If unverifiable:** keep citing the observed data. The argument does not depend on the
bill number.

---

## Notebook routing

Both belong to **Notebook B (factual)** — they are answered by specific documents, not by
a body of literature. Sources to place in `../../Candidate Sources/`:

- Danish shop-opening-hours legislation (retsinformation.dk)
- The Store Bededag abolition act

Do **not** put these in the same notebook as CV-01/CV-02 (statistical thresholds); see
`../../Claims_Verification-01-HOW-TO-RUN.md` §1.
