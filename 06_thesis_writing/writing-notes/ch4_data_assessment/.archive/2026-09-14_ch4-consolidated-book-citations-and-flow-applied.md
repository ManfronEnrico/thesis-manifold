---
name: 2026-09-14_BRANCH_A_ch4-consolidated-book-citations-and-flow
description: NOTE - Chapter 4 consolidated pass. Three Hyndman findings folded in with the cross-chapter flow items that land in this chapter. Section 13.7 flips from threat to free citation; the 2.3 "cyclic" audit is struck as a non-issue; the 7.5 weighted-distribution citation is rerouted here from Ch5.
category: workflow
applies-to: [ch4_data_assessment]
triggers: [ch4 prose pass, defending the log transform, justifying the retention threshold, book citations]
created: 2026_09_14-09_30
updated: 2026_09_14-09_30
snapshot: 2026-09-13_21-30_book-citations-pass
status: prose ready to paste, awaiting human review
---

# Chapter 4 — consolidated pass

Verified against snapshot `2026-09-13_21-30_book-citations-pass` (Ch4 at 5,314
words), repository at `9746b44`, fetch clean, origin and HEAD level. Zotero:
**89 items**. Hyndman & Athanasopoulos (2021) is key `5NFQRRXS`, already in the
library and already cited three times in this chapter.

**Notes swept:** `2026-09-13_21-15_BRANCH_A_book-transformation-and-sample-size.md`
(not applied — **superseded by this file**, and archived with it). Its three
findings are carried forward below, two of them **materially corrected** by
verification against the current chapter text.

**This note folds two streams into one**, because both land in the same three
sections and applying them separately means reading the chapter twice:

1. the Hyndman findings from the P0055 book scan, and
2. the cross-chapter flow items routed to Ch4.

---

# Two corrections to the note this supersedes

Read these before the fixes. Both change what you were told to do.

## Correction 1 — Section 13.7 is a FREE CITATION, not a threat

The superseded note flagged 13.7 as *"the one that may undercut existing prose"*
and asked whether `MIN_PERIODS` is a rule of thumb. **It is not, and the chapter
already says so in as many words.** Section 4.6, final paragraph:

> "The minimum-history requirement is the exception: it follows from the feature
> specification and the forecast horizon by construction, and is not free to
> choose."

That is the book's own criterion restated: *"The only theoretical limit is that
we need more observations than there are parameters."* The code agrees —
`MIN_PERIODS = warmup + horizon + 1`, and `engineer_features.py:51` records that
a hardcoded `DEFAULT_MIN_PERIODS = 30` was **removed** in August precisely
because it was not derived.

**So 13.7 flips from a threat into the strongest free citation in this note.**
The check this needed is done — it was a question about what the repo already
does, answered by reading it, with no run required. Fix 3 below claims it.

⚠ The book explicitly rejects *"the magic number of 30"* — and this repo deleted
a hardcoded 30 for the same reason, independently. That is worth one clause.

## Correction 2 — the "cyclic" audit item is STRUCK

The superseded note asked you to *"audit the chapter for the word"* cyclic,
because at 39–46 months a cycle claim is unsupportable.

**The word does not appear in Chapter 4. Not once, case-insensitive, in 5,314
words.** I checked the whole chapter against this snapshot. The chapter already
says "seasonality" and "annual cycles" where it means them, both of which are
claimable on three-plus years of data.

**No action. Do not go looking for it.** The item is recorded here only so it is
not re-raised by the next pass.

---

# The fixes

## Fix 1 — 4.3, the log transform's defence is incomplete in one specific way

This is the superseded note's finding 1, unchanged and confirmed.

### Anchor

**Section 4.3.** The paragraph beginning *"A logarithmic transformation is
applied uniformly to the target and to the volume-valued inputs rather than
selected per brand."*

It ends: *"...a transformation applied unevenly across brands would make the
feature semantics inconsistent within the panel."*

### Action

INSERT AFTER — one sentence, appended to the end of that paragraph.

#### Replace with

> Stating the transform in these terms also states what it assumes: a
> multiplicative relationship between the seasonal component and the level,
> since a logarithmic transformation converts a multiplicative decomposition
> into an additive one, and multiplicative decompositions are the common case
> for economic series (Hyndman & Athanasopoulos, 2021).

### Note — why this is worth a sentence

The chapter currently justifies the log on **variance stabilisation** and
**skewness**, both correct and both evidenced. What it never says is that the
transform is simultaneously a **structural commitment**: it asserts that
seasonal variation scales with the level rather than sitting on top of it.

That commitment is almost certainly right for retail beverage demand, which is
why this is an addition rather than a correction. But an examiner who knows the
decomposition identity will notice the thesis made the assumption without
naming it, and naming it costs one clause.

---

## Fix 2 — 4.3, the low-power defence answers an objection nobody raised

### Anchor

**Section 4.3**, the final clause of the same paragraph as Fix 1:

> "Uniform treatment is preferred to per-series selection because the tests that
> would drive such a selection have limited power at forty-six observations"

### Action

REWORD.

#### Replace with

> Uniform treatment is preferred to per-series selection because per-brand
> estimation of a transformation parameter is not supportable at forty-six
> observations, and because a transformation applied unevenly across brands
> would make the feature semantics inconsistent within the panel.

### Note — why the current wording does not land

The chapter defends the uniform transform by saying the **tests** that would
drive per-series selection *"have limited power"*. That is a true statement
about hypothesis tests and an **irrelevant** one here, because the standard
instrument for choosing a transformation is not a test at all. The Guerrero
method (Guerrero, 1993, given in Hyndman & Athanasopoulos §3.1) is an
**estimator**: it picks the lambda that most nearly equalises seasonal variation
across the series. Low power is a property of tests. It says nothing about
whether an estimator is usable.

So the chapter defends a correct decision with an argument that does not support
it — which is worse than no argument, because a reader who knows the method sees
the gap.

**The reword removes the wrong argument and replaces it with a true one.**
Per-brand estimation of a transformation parameter genuinely is not supportable
at forty-six observations — that is a statement about estimation, which is what
is actually at issue, and it needs no new measurement to stand behind it.

### Note — why no diagnostic should be run to support this

⚠ **Do not run a per-brand Guerrero estimation to strengthen this sentence.**
The decision to leave it unmeasured is deliberate and it is the safer choice.

The reasoning is asymmetric. If lambda came back near zero the chapter gains
very little, because the log is already evidenced on skewness — 4.1 to 5.1 raw,
none above 0.25 transformed, which is not a marginal case. If lambda came back
far from zero, or dispersed, the diagnostic **contradicts a transform that is
already baked into every trained model and every experimental result**, and
nothing could be done about it within Branch A.

A thesis cannot report evidence against its own design choice and then proceed
as though it had not. So the realistic outcomes are "negligible gain" or
"unfixable damage", and a measurement with that payoff structure should not be
taken. **This is a decision recorded, not an omission.**

---

## Fix 3 — 4.6, the minimum-history rule has a source and does not use it

This is **Correction 1** above, turned into prose. It is the highest-value free
citation in the chapter.

### Anchor

**Section 4.6**, the third numbered limitation, the paragraph beginning *"The
third is that the pipeline parameters are empirical rather than theory-first."*

It ends: *"...it follows from the feature specification and the forecast horizon
by construction, and is not free to choose."*

### Action

INSERT AFTER — one sentence, appended to that paragraph.

#### Replace with

> That distinction matters more than it may appear, because minimum-sample rules
> of thumb are rejected in the forecasting literature as unsubstantiated, with
> the only defensible limit being that a series must carry more observations
> than the specification has parameters (Hyndman & Athanasopoulos, 2021) — which
> is precisely the form the requirement takes here.

### Note — what this buys, and the one thing not to claim

The retention rule is the single most consequential preprocessing decision in
the chapter: it removes roughly a third of the brands in every category. A
reader is entitled to ask where the threshold came from, and *"it follows from
the feature specification"* is a good answer that currently stands alone.

This citation converts it from the thesis's own reasoning into an alignment with
the standard reference's explicit position — and the book's position is
unusually strong, naming rules of thumb *"misleading and unsubstantiated in
theory or practice"*.

⚠ **Do not cite the AICc half of 13.7.** The book recommends AICc as the
instrument for short series, and this repo computes no information criterion
anywhere. Claiming the parameter-count half while silently holding the AICc half
is honest; claiming both is not.

That gap is **not** something to close now. Adding an information criterion means
re-selecting features, which means retraining, which means re-running the funded
experiment. It is future work, and Chapter 9 is where it belongs if it is named
at all.

---

## Fix 4 — 4.3, the weighted-distribution rejection is unsourced and should not be

**Rerouted from the Ch5 note, which sent it to the wrong chapter.** Ch5 never
mentions the weighted-distribution feature; the rejection prose is here in Ch4,
in two places.

### Anchor

**Section 4.3**, the paragraph beginning *"Two of the column groups in the table
warrant further comment."* The relevant sentences are at its end:

> "The weighted-distribution measure was tested as an input and not adopted. It
> is known in advance and moves slowly, so it was a genuine candidate rather
> than a leakage risk; fitting the benchmark with and without it raised the
> error in three of the four categories, and it is excluded on that measurement
> rather than on principle."

### Action

REWORD — the final clause only. Everything before *"and it is excluded"* stands.

**Before:**
> "...and it is excluded on that measurement rather than on principle."

**After:**
> "...and it is excluded on that measurement rather than on principle, which is
> the criterion the forecasting literature endorses for admitting or rejecting a
> predictor: selection on measured predictive performance rather than on
> in-sample significance (Hyndman & Athanasopoulos, 2021)."

### Note — why this is a better citation than it looks

Section 7.5 names two selection procedures **invalid** in so many words:
dropping a predictor by eyeballing a scatterplot, and dropping it because
*p > 0.05*. It recommends instead criteria *"which have forecasting as their
objective"*.

This repo rejected the feature because **measured error rose in three of four
categories** — a held-out predictive criterion, which is exactly what the source
sanctions. The chapter's own sentence already draws the distinction (*"on that
measurement rather than on principle"*); it simply does not know it has backing.

⚠ **Do not claim the other half of 7.5.** It recommends AICc/AIC/CV specifically,
and the repo computes none of them. Same boundary as Fix 3 — the free half rests
on a measurement you already have, and the other half would require work that
cannot be done without retraining.

---

# Cross-chapter flow items landing in Chapter 4

From `2026-09-13_18-40_BRANCH_A_cross-chapter-flow-and-connectedness.md`.
**Chapter 4 comes out of the flow read exceptionally well** — it is named in that
note as a counter-example twice, for its cross-reference discipline and for its
honesty about the 6.16x double-count and the thirteen lumpy brands.

Only one flow item touches this chapter, and it is not a Ch4 defect:

| Item | What it needs | Where |
|---|---|---|
| **S30** — Ch3 §3.4 duplicates Ch4 §4.1.1 | **Cut Ch3's version**, not Ch4's. Ch4 is the fuller and better one | a Ch3 fix |

**Nothing in Chapter 4 should be cut or changed to accommodate it.** Recorded
here so that whoever applies S30 does not "resolve the duplication" in the wrong
direction.

---

# Citations register rows

Both rows are the same source, already in Zotero, so neither carries
verification debt. Add to `citations-added-register.md`:

| | |
|---|---|
| Source | Hyndman & Athanasopoulos (2021), *Forecasting: Principles and Practice*, 3rd ed. |
| Zotero key | `5NFQRRXS` |
| Status | **IN-ZOTERO** ✓ — verified against the 89-item pull |

| Fix | Lands in | Supports the sentence |
|---|---|---|
| Fix 1 | 4.3 | "...a multiplicative relationship between the seasonal component and the level, since a logarithmic transformation converts a multiplicative decomposition into an additive one" |
| Fix 3 | 4.6 | "...minimum-sample rules of thumb are rejected in the forecasting literature as unsubstantiated, with the only defensible limit being that a series must carry more observations than the specification has parameters" |
| Fix 4 | 4.3 | "...selection on measured predictive performance rather than on in-sample significance" |

**NLM-CONFIRMED is not required for any of the three.** Each cites a section of
a source already cited in this chapter for adjacent claims, and each of the three
statements is a direct restatement of a quoted passage recorded in the P0055
scan. The quotations are in the archived note.

---

# What this note deliberately does not do

**It does not touch 4.4's seasonal-stability gap.** The superseded note raised
§2.4/§2.5: seasonal stability across years is never checked, yet `peak_month` is
computed from pooled means. That is **real and it is a measurement, not a
citation** — it needs a run to say anything about, and the chapter cannot claim
stability it has not tested.

⚠ **Leave it unmeasured, for the same reason as Fix 2's Guerrero note.**
`peak_month` is a live model feature. A diagnostic showing the seasonal peak
moves between years would undercut a feature already trained into every model and
already carried through the funded experiment, with no way to act on it. The
chapter does not currently claim stability, so there is nothing false to correct
— only an untested assumption, which is the ordinary condition of a feature and
not a defect to go looking for.

**It does not name the panel's hierarchical structure.** §11.1 observes the panel
is exactly a mixed hierarchical/grouped structure, (category/brand) x market, and
the thesis never names it. Naming it costs a sentence, but the right place is
**Ch9's limitations**, where the non-reconciliation is already discussed — not
Ch4, which would raise it and then not use it. It is in the Ch9 note.
