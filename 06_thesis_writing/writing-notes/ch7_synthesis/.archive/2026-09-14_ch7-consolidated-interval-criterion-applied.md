---
name: 2026-09-14_BRANCH_A_ch7-consolidated-interval-criterion-citation
description: NOTE - Chapter 7 consolidated pass. One free citation sourcing the interval-communication criterion from the standard reference rather than from the thesis's own preference. Plus the S26 table-numbering status, now resolved.
category: workflow
applies-to: [ch7_synthesis]
triggers: [ch7 prose pass, defending the interval-communication criterion, book citations]
created: 2026_09_14-09_30
updated: 2026_09_14-09_30
snapshot: 2026-09-13_21-30_book-citations-pass
status: prose ready to paste, awaiting human review
---

# Chapter 7 — consolidated pass

Verified against snapshot `2026-09-13_21-30_book-citations-pass`, repository at
`9746b44`, fetch clean. Zotero: **89 items**, Hyndman & Athanasopoulos (2021)
key `5NFQRRXS`.

**Notes swept:**
- `2026-09-13_21-15_BRANCH_A_book-citation-interval-criterion.md` — not applied,
  **superseded by this file** and archived with it.
- `2026-09-13_01-05_BRANCH_A_ch7-branch-a-pass.pdf` and
  `ch7-verification-pass.pdf` — PDFs, left in place. Not swept by this note.

**This is a one-fix note.** Chapter 7 came through both the flow read and the
book scan better than any other chapter: its refusal principle (§7.2.3) is named
in the flow note as transferable design knowledge, and §7.3's decision to let
arithmetic rather than a language model do the judging is the passage Chapter 3
contradicts and Chapter 7 gets right.

---

# The fix

## Fix 1 — 7.1, the interval criterion argues from first principles and has a source

### Anchor

**Section 7.1 What a forecast must carry.** The paragraph beginning *"It is
tempting to suppose that the second failure is met simply by attaching an
interval, but the evidence does not support this."*

It ends: *"Both questions must be answered at the interface, and Section 7.2 sets
out the contract through which they are."*

### Action

INSERT — one sentence at the **start** of that paragraph, before *"It is
tempting..."*.

#### Replace with

> That a forecast must carry its uncertainty at all is not this thesis's own
> premise but a stated requirement of the field, where point forecasts are held
> to be of almost no value without the accompanying prediction intervals
> (Hyndman & Athanasopoulos, 2021).

### Note — what this changes about how the chapter reads

Section 7.1 currently opens the uncertainty argument with Goodwin, Önkal and
Thomson (2010) — which is the **right** source for the subtle half of the claim,
that a bare numeric range does not by itself improve a decision.

But Goodwin is an argument about **how** to communicate an interval. It presumes
the reader already accepts that an interval must be communicated. The thesis
never sources that prior premise, so the criterion rests on an assertion the
chapter makes on its own authority.

**§5.5 supplies it in one line**, in the standard reference, unhedged. The
criterion stops being the thesis's preference and becomes an operationalisation
of a requirement the field already states.

**Placement matters here.** It goes *first*, so the paragraph runs: the field
requires intervals → attaching one is not sufficient (Goodwin) → both questions
must be answered at the interface. That is the argument the chapter is already
making, with its first step no longer missing.

---

# What this note deliberately does not claim

## The Table 5.1 / 5.2 arithmetic

The superseded note offered the book's interval multipliers (80% → 1.28, 95% →
1.96) and the seasonal-naive standard-deviation formula
`sigma * sqrt(k+1)`, `k = floor((h-1)/m)`.

**Chapter 7 needs none of it.** It computes no interval — it *checks* intervals
the tool returned, against the payload, within a five per cent tolerance. The
arithmetic belongs to whatever produces the interval, which is Chapter 5's
conformal wrapper, and that is empirical rather than Gaussian so the multipliers
do not apply to it either.

⚠ **The `sqrt(k+1)` formula is parameterised by m, which is a fourth independent
confirmation that m = 12 for this panel** — and the MASE denominator uses m = 1.
**Do not import that here.** It is a Chapter 5 metric question, it is excluded
from Branch A deliberately (see the Ch5 note's Fix 4), and Chapter 7 computes no
MASE at all, so raising it here would introduce a problem the chapter does not
have.

## Anything about the confidence index

§7.4 establishes at length that the confidence index discriminates nothing, and
the flow note names that as one of the thesis's best negative results. **It needs
no source and should not be given one.** It is a measurement of this artefact,
not a claim about forecasting practice.

---

# Cross-chapter flow items landing in Chapter 7

| Item | Status |
|---|---|
| **S26** — Ch7's table numbers collide with Ch6's | ✅ **RESOLVED** — Ch6 runs 17–19, Ch7 runs 20–21, no overlap. Verified against the 2026-09-13 20:40 snapshot and unchanged since |
| **S28** — Ch7 cites Ch5's calibration table rather than repeating it | ✅ **done**, applied 2026-09-12 |
| **Ch7 → Ch8 on the confidence index** | **One clause, optional.** See below |

## The optional Ch8 clause

The flow note observes that §7.4 establishes the index is degenerate and Chapter
8 never mentions it — while Ch8's interval-communication criteria are scored
partly on a confidence being stated. A reader may wonder whether the degenerate
index is what is being scored.

**It is not**, and one clause in **Chapter 8** closes it: the criterion records
whether a confidence was communicated, not whether the index producing it was
informative.

→ **Routed to Ch8**, not actioned here. Recorded so the connection is not lost.

⚠ **One live caveat on Ch7's two table captions.** They are typed as **plain
text**, not Word field references, so they do **not** renumber automatically the
way Ch5, Ch6 and Ch8 do. If the Ch5 calibration table insertion renumbers the
document, Chapter 7's two captions are the **only manual edits** required. That
is S26's residue and it is the reason the register entry stays open until the
renumbering is applied.

---

# Citations register row

| | |
|---|---|
| Source | Hyndman & Athanasopoulos (2021), *Forecasting: Principles and Practice*, 3rd ed. |
| Zotero key | `5NFQRRXS` |
| Status | **IN-ZOTERO** ✓ — verified against the 89-item pull |
| Lands in | Chapter 7, Section 7.1, opening sentence of the second paragraph |
| Supports | "...point forecasts are held to be of almost no value without the accompanying prediction intervals" |

**NLM-CONFIRMED not required.** The supported sentence is a near-verbatim
restatement of the source's own opening claim in §5.5, recorded with the
quotation in the archived note: *"point forecasts can be of almost no value
without the accompanying prediction intervals"*.

⚠ **This is the first Hyndman citation in Chapter 7.** Check the rendered
bibliography after pasting — the entry already resolves for Ch4 and Ch5, so this
should be free, but a first use in a chapter is where a broken reference shows
up.
