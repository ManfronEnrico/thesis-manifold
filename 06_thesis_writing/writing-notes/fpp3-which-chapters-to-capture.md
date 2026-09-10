---
name: fpp3-which-chapters-to-capture
description: NOTE - Forecasting Principles and Practice is a web book with no page numbers, so each cited chapter needs its own capture. This maps every citation in the thesis to the one chapter that supports it, so only three need capturing rather than thirteen.
category: reference
applies-to: [citations, chapter 4, chapter 5]
triggers: [capturing FPP3 sections, Zotero book entries, NotebookLM source prep]
created: 2026_09_10-20_10
updated: 2026_09_10-20_10
status: ready
---

# Forecasting: Principles and Practice - which chapters actually need capturing

**Three chapters, not thirteen.** And of those three, **two are already
verified** with exact quotations captured, so only one needs new work.

The thesis cites this book five times across two chapters. Every citation traces
to one of three sections.

---

# The answer, in one table

| Priority | Chapter to capture | Sections to expand | Supports | Status |
|---|---|---|---|---|
| **1** | **5 - The forecaster's toolbox** | **5.2 only** | four of the five citations | ⚠ **capture this one** |
| **2** | **3 - Time series decomposition** | 3.1, or skip - see below | the Chapter 4 log-transform claim | **probably avoidable** |
| **3** | **9 - ARIMA models** | 9.1, or skip - see below | the Chapter 4 differencing claim | **probably avoidable** |

**Do chapter 5 first.** If you do nothing else, do that.

---

# Why chapter 5 section 5.2 is the one that matters

Four of the five citations point at it, and it is the only one carrying a direct
quotation in the thesis text:

| Where | The claim it supports |
|---|---|
| Ch5, Section 5.1 | the four simple methods are benchmarks, quoted verbatim |
| Ch5, Section 5.2.1 | the four formulas - mean, naive, seasonal naive, drift |
| Ch5, Section 5.5.2 | that a new method must justify itself against them |
| Ch5, model-ladder argument | the same, restated in the selection decision |

**Section 5.2 has its own page**, at `simple-methods.html` - so this is one page,
not an expanded chapter. The rest of chapter 5 (5.1, and 5.3 through 5.11) is not
cited anywhere in the thesis and can be ignored entirely.

### It is already verified, which saves you the hardest part

`notebookLM/03-Modelling_Review/NLM Review/Modelling_Review-Section_D` records
**BM-01 and BM-02 as Supported**, with the two exact quotations already
extracted:

> "Some forecasting methods are extremely simple and surprisingly effective. We
> will use four simple forecasting methods as benchmarks throughout this book."

> "Sometimes one of these simple methods will be the best forecasting method
> available; but in many cases, these methods will serve as benchmarks rather
> than the method of choice. That is, any forecasting methods we develop will be
> compared to these simple methods to ensure that the new method is better than
> these simple alternatives."

**So the capture is proof-of-content for an already-confirmed claim**, not a
verification run. You are producing the artefact, not discovering whether the
claim holds.

⚠ **One thing to check while you have the page open.** An earlier draft of the
project's own notes quoted this section as saying the simple methods "are the
best we can do" for many series. **That quote is not in 5.2** and the actual text
says nearly the opposite in emphasis. Confirm the two quotations above are what
the page says, and nothing stronger.

---

# The two Chapter 4 citations, and why they may not need a capture at all

Both are **background-convention citations**, not claims resting on a specific
passage. Neither quotes the source, and neither would fail if the citation were
dropped.

### Citation A - logarithmic transformation

> "Logarithmic transformation is the standard response to multiplicative
> variance in forecasting practice, stabilising the variance so that a
> proportional change has the same effect at every level of the series (Hyndman
> & Athanasopoulos, 2021)."

**Chapter 3, section 3.1** covers transformations and adjustments, including the
logarithmic case and the variance-stabilising argument. That is the section to
capture **if you keep the citation**.

### Citation B - differencing a unit-root series

> "Non-stationarity in the mean is handled by differencing for the statistical
> baselines, which is the conventional treatment for a series carrying a unit
> root (Hyndman & Athanasopoulos, 2021)."

**Chapter 9, section 9.1** covers stationarity and differencing. Same condition.

### The cheaper option for both

**These two claims are textbook conventions that the surrounding prose already
supports with measurement.** Citation B in particular sits immediately after an
augmented Dickey-Fuller test result reported in the thesis's own data - the
sentence does not need an authority to say that a unit root is handled by
differencing, because the paragraph has just demonstrated it.

**Three ways to resolve them, cheapest first:**

| Option | Cost | Trade-off |
|---|---|---|
| **Drop both citations** | zero | the claims stand on the thesis's own measurements, which is where their evidence actually is |
| **Re-point to a source already captured** | low | Hyndman & Koehler (2006) is in the library as a journal article with page numbers, and covers scale and transformation issues |
| **Capture chapters 3 and 9** | two more expand-and-print cycles | keeps the current text unchanged |

**Recommendation: drop them.** A citation that adds nothing an examiner would
challenge, and costs a screenshot cycle plus a Zotero entry, is not earning its
place. Chapter 4's own numbers are the better support.

---

# How to structure the Zotero entries

The current single entry is malformed and must be replaced regardless. **One
entry per cited chapter**, since the web edition has no page numbers and a
reference must be resolvable to what the reader can actually open.

For the chapter-5 capture:

| Field | Value |
|---|---|
| Item type | **Book section** |
| Section title | Some simple forecasting methods |
| Book title | Forecasting: Principles and Practice |
| Authors | Hyndman, Rob J.; **Athanasopoulos, George** |
| Edition | 3rd |
| Date | **2021** |
| Publisher | OTexts |
| Place | Melbourne, Australia |
| URL | `https://otexts.com/fpp3/simple-methods.html` |
| Accessed | the date you capture it |

**That URL is section 5.2's own page**, taken from the existing entry with the
tracking parameter removed. Each section of this book has its own page, so the
section is the natural unit for both the capture and the reference - which is
what makes "Section 5.2" the right locator rather than a page number.

⚠ **Strip the `utm_source=chatgpt.com` parameter** from the URL. The current
entry carries it, and it will appear in the bibliography.

⚠ **Cite as "(Hyndman & Athanasopoulos, 2021, Section 5.2)"**, not with a page
number. The web edition has none, and inventing one is worse than omitting it.

---

# What to do, in order

1. **Open `https://otexts.com/fpp3/simple-methods.html`** - that is section 5.2
   on its own page, so there is nothing to expand. Print to PDF.
2. **Confirm the two quotations** in the verification file match what the page
   says.
3. **Fix the Zotero entry** per the table above - or replace it with a new book
   section entry and delete the malformed one.
4. **Decide on the two Chapter 4 citations.** If you drop them, nothing else is
   needed. If you keep them, capture chapter 3 section 3.1 and chapter 9 section
   9.1 the same way.

**Total if you drop the Chapter 4 citations: one capture, one Zotero entry.**

---

# What this does not settle

The capture is proof of content for NotebookLM. **It is not a claim
verification** - that runs after the chapters are prosed, and for this source two
of the claims are already through it.

The remaining question is whether the Chapter 4 citations survive at all, which
is a judgement about whether those two sentences need an authority. My reading is
that they do not.

## Related

- `deferred-structural-decisions.md` - S16, the metadata defects in this entry
- `citations-added-register.md` - the register these captures feed
- `notebookLM/03-Modelling_Review/NLM Review/Modelling_Review-Section_D-benchmark_forecasting_methods.md` - BM-01 and BM-02, already Supported
