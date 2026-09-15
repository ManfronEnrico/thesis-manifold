---
name: 2026-09-15_NLM_ch5-citation-verification-pass
description: PASS - NotebookLM's twenty Chapter 5 citation checks. Eighteen confirmed, two real typographic fixes, and two FALSE verdicts corrected to NOT-ADDRESSED because the sources are in the library and were simply not loaded into the notebook.
category: workflow
applies-to: [ch5_model_benchmark]
triggers: [ch5 citations, notebooklm, citation verification, ch5 prose pass]
created: 2026_09_15-12_50
updated: 2026_09_15-12_50
snapshot: 2026-09-15_10-49_final-comment-sweep
status: prose ready to paste, awaiting human review
---

# Chapter 5 — NotebookLM citation pass, verified

Verified at `37a04f0`, fetch clean. Snapshot `2026-09-15_10-49_final-comment-sweep`.
Zotero re-pulled **2026-09-15 10:49:34, 92 items**.

**Notes swept:** `ch5_model_benchmark/` holds one live note,
`2026-09-14_appendix-citations-ch5.md` (recommendations only, no anchors). Its
`.archive/` carries nineteen applied notes. **Nothing dropped.**

✅ **This is the cleanest of the four blocks.** Chapter 5's citations are in good
order: eighteen of twenty confirmed, and the two edits are typographic.

---

# Summary

| | |
|---|---|
| **Real edits** | **2** — F1 and F2, the same missing space, twice |
| **Verdicts corrected** | 2 — CIT-006 and CIT-007 are not FALSE |
| **Confirmed** | 18 |

---

# F1 and F2 — a missing space in two citations

**Both copies flag it and both are right.** `Hyndman and Athanasopoulos(2021)`
appears twice with no space before the parenthesis. ✅ **Verified: exactly two
instances in Ch5**, at snapshot lines 227 and 235. Nowhere else in the chapter.

## F1 — §5.5.2, the benchmark-rung paragraph

### Anchor

**Chapter 5, Section 5.5.2 "The simple benchmarks, and where they win"** — the
paragraph immediately after the **Prohpet** bolded lead-in. Searchable, verbatim:

> "This is precisely the outcome the benchmark rung exists to detect. Hyndman and Athanasopoulos(2021) recommend the simple methods as a standard against which any new method must justify itself"

### Action

REWORD — insert one space: `Athanasopoulos(2021)` → `Athanasopoulos (2021)`.

#### Replace with

> "This is precisely the outcome the benchmark rung exists to detect. Hyndman and Athanasopoulos (2021) recommend the simple methods as a standard against which any new method must justify itself"

### ⚠ Note — do not paste NotebookLM's version of this one

Its "verbatim replacement" column silently **changes the end of the sentence**,
from *"...here they are not a formality but a live constraint, and reporting a
headline ML number without them would have concealed that the thesis's approach
is beaten outright on half the categories"* to *"...and that standard is met on
three of the four categories."*

⚠ **That is a different claim, and it contradicts the chapter.** §5.5.2 reports
seasonal naive beating the tuned models on **RTD** and Prophet beating them on
**danskvand** — two of four, which is why the existing sentence says *"beaten
outright on half the categories"*. **Pasting NotebookLM's text would state the
opposite of the chapter's own result table.**

→ **Change only the space.**

---

## F2 — §5.5.2, the Ridge bounding paragraph

### Anchor

**Chapter 5, Section 5.5.2**, under the **Ridge** bolded lead-in — the paragraph
beginning *"The bound is stated as a forecasting constraint rather than a
numerical convenience"*. Searchable, verbatim:

> "Hyndman and Athanasopoulos(2021) prefer bounds imposed through the transformation itself over constraints applied to a finished forecast"

### Action

REWORD — insert one space.

#### Replace with

> "Hyndman and Athanasopoulos (2021) prefer bounds imposed through the transformation itself over constraints applied to a finished forecast"

✅ **The rest of the sentence stands.** NotebookLM's replacement keeps it intact
here, unlike F1.

---

# Two FALSE verdicts that are not FALSE

**CIT-006 (Ke et al., 2017) and CIT-007 (Chen & Guestrin, 2016) are both marked
`FALSE`.** Reading its own evidence column: *"Source PDF not in selected sources
corpus (indexed in Zotero library, key 8RUJXQ45 / KKR3U38C)."*

⚠ **NotebookLM is reporting that it could not open the PDF, not that the claim is
wrong.** That is `NOT-ADDRESSED`, and the distinction matters — a source silent
on a claim is not evidence against it.

✅ **Both are in the library, exactly at the keys it names:**

```
[8RUJXQ45] conferencePaper  LightGBM: A Highly Efficient Gradient Boosting Decision Tree
[KKR3U38C] conferencePaper  XGBoost: A Scalable Tree Boosting System
```

✅ **And both claims are textbook-accurate**: LightGBM's histogram-based split
finding and leaf-wise growth, XGBoost's level-wise growth and L1/L2 leaf-weight
penalties. These are the defining contributions of each paper.

→ **No action.** Recorded so the FALSE marks are not carried into a register as
though they were findings.

⚠ **Same pattern as Ch1's CIT-010 (González-Potes).** When a block says FALSE,
read the evidence column before believing it — three of the four FALSE verdicts
across all four blocks turned out to be unopened PDFs.

---

# Confirmed, no action — eighteen items

| ID | Citation | Library |
|---|---|---|
| CIT-001 | Hyndman & Athanasopoulos (2021), benchmark standard | ✅ `5NFQRRXS` |
| CIT-002 | Makridakis et al. (2018), M4 pure-ML entries | ✅ `EXNY7D4X` |
| CIT-003 | Hyndman & Athanasopoulos (2021), four simple methods | ✅ |
| CIT-004 | Hyndman & Athanasopoulos (2021), seasonal order for monthly | ✅ |
| CIT-005 | Taylor & Letham (2018), Prophet decomposition | ✅ `KN4IEBZN` |
| CIT-008 | Hastie et al. (2009), ridge regression | ✅ `94VFSWKI` ⚠ see below |
| CIT-009 | Hyndman & Koehler (2006), percentage errors undefined at zero | ✅ `RTYN3Z8Q` |
| CIT-010 | Gneiting (2011), scoring functions and functionals | ✅ `D8JBHU9S` |
| CIT-011 | Hyndman & Athanasopoulos (2021), RMSE recommendation | ✅ |
| CIT-012 | Syntetos et al. (2005), demand categorisation, p=1.32 / CV²=0.49 | ✅ `8ZMMZXDG` |
| CIT-013 | Syntetos & Boylan (2005), estimators not exclusion | ✅ `PBAHP5BH` |
| CIT-014 | Hyndman & Athanasopoulos (2021), information criteria within-class only | ✅ |
| CIT-015 | Cawley & Talbot (2010), optimistic bias in model selection | ✅ `5G55UDSP` |
| CIT-017 | Taylor & Letham (2018), daily series design regime | ✅ |
| CIT-019 | Hyndman & Athanasopoulos (2021), quantiles under monotone transforms | ✅ |
| CIT-020 | Lei et al. (2018), Algorithm 2 quantile correction | ✅ `UHZWB269` |

✅ **CIT-002 is worth noting as a positive.** Ch5 §5.1 cites **Makridakis et al.
(2018)** for the M4 pure-ML result — which is the correct paper of the two, and
the Ch1 note's F5 does not disturb it.

⚠ **CIT-008, Hastie — the duplicate problem lands here.** The library holds *six*
Hastie-related records: one book (`94VFSWKI`), **three identical webpages**
(`4TVC5APJ`, `SPW7NXHT`, `Q4IIBE2Z` — the thread-277 triplication), and two book
sections. **Cite the book, and merge the three webpages in Zotero before
generating the bibliography**, or Ch5's ridge citation may resolve to a
year-less webpage rendering as "n.d.".

---

# Chapter rename — ⚠ one worth considering

**Current:** *"Chapter 5 | Model Benchmark & Selection"*, standfirst *"Selecting a
Forecasting Substrate Under Memory and Data Constraints"*.

⚠ **The chapter's own conclusion is that it does not select a model.** §5.6 states
plainly: *"The choice between LightGBM and XGBoost is not supported by this
data... Naming a winner per category would report one seed's outcome as a
finding."* The title promises a selection the chapter deliberately declines to
make.

**This is a real, if minor, mismatch** — and an assessor reading the title, then
§5.6, may read the chapter as having failed at its stated task rather than as
having produced a careful negative result.

| Option | |
|---|---|
| **Leave it** | ✅ defensible — the chapter *does* select a substrate *family* (gradient boosting over ARIMA/Ridge/Prophet), which is a selection |
| **"Model Benchmark & Substrate Selection"** | narrows the promise to what §5.6 delivers |
| **"Model Benchmark and Selection Under Seed Instability"** | ⚠ too long, and leads with the limitation |

**NEEDS-BRIAN. My recommendation: leave the title, and let the standfirst carry
it** — *"Selecting a Forecasting Substrate"* is already accurate at the family
level, which is exactly the distinction §5.6 draws. A rename this late also
touches the TOC, the chapter map in Ch1 §1.5, and every cross-reference.

→ Recorded in `deferred-structural-decisions.md` rather than decided here.

---

# For the registers

## `citations-added-register.md`

**No citations added.** Both fixes are whitespace.

## Deferred / structural

| ID | Item | Recommendation |
|---|---|---|
| **new** | Ch5 title promises a selection §5.6 declines to make | **Leave the title.** The standfirst is accurate at the family level. Revisit only if an examiner comment raises it |

## Zotero hygiene

⚠ **`Hastie` resolves to six records, three of them identical year-less
webpages.** Highest-priority merge before the dynamic list, because Ch5 §5.2.6
depends on it.
