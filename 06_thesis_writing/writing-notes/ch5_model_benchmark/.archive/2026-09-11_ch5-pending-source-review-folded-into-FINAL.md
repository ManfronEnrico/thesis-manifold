---
name: ch5-pending-source-review
description: NOTE - A source review of Chapter 5 against Forecasting Principles and Practice is in progress. It raises four substantive problems the prose pass did not, and no chapter-5 section should be marked finished until its verdicts land.
category: workflow
applies-to: [chapter 5]
created: 2026_09_10-20_40
updated: 2026_09_10-20_40
status: open
---

# Do not close Chapter 5 before the source review lands

**There is a second review of this chapter in flight**, and it is not in this
folder. It lives at:

`06_thesis_writing/notebookLM/03-Modelling_Review/forecasting-book-sections-for-citation-verification.md`

It maps Chapter 5's claims onto specific sections of *Forecasting: Principles and
Practice* and defines what NotebookLM must verify for each. Brian is working
through the book chapter by chapter, printing the sections and feeding them in.

**The prose pass in this folder does not supersede it and is not superseded by
it.** They answer different questions. The pass asks *does the chapter match the
repository*; the review asks *does the chapter match the literature it cites*.
A section can pass one and fail the other.

---

# Four problems it raises that the prose pass did not

These are not citation-formatting issues. Each one is a claim in the chapter that
may need to change, and none was caught by verifying against the codebase.

## 1. The ARIMA baseline is non-seasonal, on strongly seasonal data

The chapter treats annual seasonality as the defining property of monthly
beverage demand - it is the whole justification for including seasonal naive -
and then implements ARIMA at a fixed order with **no seasonal term at all**.

That makes the ARIMA-versus-seasonal-naive comparison structurally uneven in a
way the chapter does not acknowledge. The current limitation says ARIMA is "not
order-optimised", which is true but understates it: the model has no mechanism
for the seasonality the chapter says dominates the data.

**Likely outcome:** label it explicitly as a fixed **non-seasonal** ARIMA(1,1,1),
and say the comparison disadvantages it. Possibly rerun with a seasonal order.

## 2. ETS is missing from a claimed spectrum of inductive biases

Section 5.1 claims the five families "span the inductive-bias spectrum".
Exponential smoothing is one of the two dominant classical families and it is
absent. A reader who knows the field will notice.

**Likely outcome:** narrow the claim, or acknowledge the omission explicitly.
Either is cheap; the current unqualified wording is the risk.

## 3. "Prophet is applied outside its design regime" may overstate the source

This is the chapter's explanation for Prophet's extreme figures, and it is
attributed to Taylor and Letham. **They do not say it.** The mechanical argument
is available and stronger, but the chapter must present the interpretation as its
own inference rather than as something the authors documented.

## 4. Clipping the Ridge forecasts needs methodological support

The chapter reports clipped Ridge figures and mentions the unclipped ones. What
it does not do is justify clipping as a method or state the bounds. The book
covers constrained forecasting, and it may recommend a transformation-based
constraint rather than post-hoc clipping - in which case the chapter is doing the
less defensible of two available things without saying so.

---

# A first pass has been read, and it found two more

`notebookLM/03-Modelling_Review/fpp3-first-pass-findings.md` records a direct
read of six of the forty section PDFs, with page-located quotations. It confirms
problems 1, 3 and 4 above and adds two that are **defects rather than citation
gaps**:

| # | What | Section |
|---|---|---|
| **5** | Ridge forecasts are clipped post-hoc; the book handles bounding **through the transformation** and calls an artificial constraint "unrealistic" | 13.3 |
| **6** | Back-transformed log forecasts are **medians, not means**, so brand forecasts do not aggregate additively to a category total | 5.6 |

Finding 6 reaches beyond this chapter: the forecast tool serves per-brand
forecasts and nothing currently warns a consumer against summing them.

Finding 3 improves: the book states the Prophet design-regime point **in its own
voice**, which is a better citation than Taylor and Letham, who do not make it.

---

# What this means for sequencing

**Do not treat a Chapter 5 section as finished when its prose-pass block is
applied.** Sections 5.1, 5.2.2, 5.2.3, 5.5.2 and 5.5.8 all carry claims the
review is examining, and its verdicts may change wording the pass declares
settled.

| Section | Prose pass | Source review also touches it |
|---|---|---|
| 5.1 | rewritten | ⚠ the inductive-bias claim (problem 2) |
| 5.2.2 ARIMA | rewritten | ⚠ the seasonality gap (problem 1) |
| 5.2.3 Prophet | rewritten | ⚠ the design-regime claim (problem 3) |
| 5.5.2 | table and three paragraphs replaced | ⚠ problems 1, 3 and 4 |
| 5.5.8 | rewritten | ⚠ the ARIMA limitation may need strengthening |

Everything else in the chapter is unaffected and can be applied and considered
done.

---

# One thing the review found that is already fixed

Its section 6 flags that the chapter's internal cross-references point at Chapter
6. **That is correct and it is handled** - the prose pass rewrites those
references as part of each section's prose rather than repairing them in place.
No separate action needed.

---

# Citation practice, settled 2026-09-10

**Cite the whole book.** The Zotero entry is now a single correct book record and
the authors present the work as one book, so the bibliography carries one entry.

Add a section locator in text only where a passage is quoted directly:

> (Hyndman & Athanasopoulos, 2021, Section 5.2)

**Never a page number.** The online edition is revised continuously and does not
share pagination with the print version.

Feeding individual chapters to NotebookLM is a verification-input decision and
does not change how the source is cited.
