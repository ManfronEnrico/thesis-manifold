---
name: citations-added-register
description: NOTE - Every citation added to the thesis during a prose or follow-up session, with the exact claim it supports and its NotebookLM verification state. Cumulative. Includes the required NotebookLM return format for machine re-ingestion.
category: reference
applies-to: [chapter 4, chapter 5, citations, verification]
created: 2026_09_09-21_10
updated: 2026_09_09-21_10
status: open
---

# Citations added during prose sessions

Every citation a writing session put into the thesis, with **the claim it is
being used to support** rather than only the reference itself.

**Why the claim and not just the source:** a reference that exists is not a
reference that says what you need it to say. Ng (2017) is unquestionably a real
paper about scanner data; whether it supports *"coverage is bounded by which
retailers report"* is a separate question, and that is the one NotebookLM
answers.

**Cumulative across chapters.** Append; do not replace.

---

# Status values

| Status | Meaning |
|---|---|
| `IN-ZOTERO` | the item exists in the group library, verified against a fresh pull |
| `NLM-PENDING` | in Zotero, but the *claim* has not been checked against the source text |
| `NLM-CONFIRMED` | NotebookLM confirms the source supports the claim as written |
| `NLM-PARTIAL` | the source supports a weaker version; the prose needs adjusting |
| `NLM-REFUTED` | the source does not support the claim. **Remove the citation** |
| `NOT-IN-ZOTERO` | proposed but absent from the library. Must be added before use |

**A citation may be `IN-ZOTERO` and still be wrong for its claim.** The two
checks are independent, and only the second one protects against the failure this
register exists to prevent.

---

# Library state

| | |
|---|---|
| Last Zotero pull | **2026-09-09 21:00** |
| Items in library | 86 |
| Pulled by | `python utility_scripts/scripts/zotero_client.py` |

**Re-pull before every verification pass.** The export that preceded this one was
dated 25 August, two weeks stale, and a citation checked against a stale export
is not checked. The pull is one command and takes seconds.

---

# Chapter 4

All eight were verified against the 2026-09-09 pull. Zotero keys included so a
later session can find the exact item rather than re-matching on title.

## C4-01 — Ng (2017)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-PENDING` |
| **Zotero key** | `Q744EZLB` |
| **Full title** | Opportunities and Challenges: Lessons from Analyzing Terabytes of Scanner Data |
| **Type / year** | preprint (NBER w23673), 2017 |
| **URL** | https://www.nber.org/papers/w23673 |
| **Used in** | §4.1, opening paragraph |
| **Added by** | ch4-prose-pass-followup-01, F3a |

**The claim it must support:**

> Retail scanner panels capture transactions at the point of sale rather than
> responses to a survey instrument, which removes recall error but bounds
> coverage by which retailers report and by how the provider defines its market
> aggregates.

**To verify:** does Ng (2017) characterise scanner data as point-of-sale
transaction capture, and does it discuss coverage limits arising from retailer
participation and from provider-defined market aggregation?

## C4-02 — Doane & Seward (2011)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-PENDING` |
| **Zotero key** | `K4WW8T95` |
| **Full title** | Measuring Skewness: A Forgotten Statistic? |
| **Type / year** | journal article, 2011 |
| **DOI** | 10.1080/10691898.2011.11889611 |
| **Used in** | §4.2.2, first paragraph |
| **Added by** | ch4-prose-pass-followup-01, F3b |

**The claim it must support:**

> Skewness values between 4.1 and 5.1 are well beyond the range at which a
> distribution is conventionally treated as approximately normal.

**To verify:** does the source give a threshold or rule of thumb for when
skewness indicates material departure from normality, and is a value above 4
clearly beyond it?

## C4-03 — Cain, Zhang & Yuan (2017)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-PENDING` |
| **Zotero key** | `NVXZ7V8Z` |
| **Full title** | Univariate and multivariate skewness and kurtosis for measuring nonnormality: Prevalence, influence and estimation |
| **Type / year** | journal article, 2017 |
| **DOI** | 10.3758/s13428-016-0814-1 |
| **Used in** | §4.2.2, alongside C4-02 |
| **Added by** | ch4-prose-pass-followup-01, F3b |

**The claim it must support:** as C4-02.

**To verify:** same question. If both confirm, cite both; if only one does, drop
the other rather than padding.

## C4-04 — Guyon & Elisseeff (2003)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-PENDING` |
| **Zotero key** | `I23PZQ48` |
| **Full title** | An Introduction to Variable and Feature Selection |
| **Type / year** | journal article (JMLR), 2003 |
| **URL** | https://www.jmlr.org/papers/v3/guyon03a.html |
| **Used in** | §4.3, second paragraph |
| **Added by** | ch4-prose-pass-followup-01, F3d |

**The claim it must support:**

> A feature-selection rule is justified only by the performance of the model it
> produces.

**To verify:** does the source argue that selection methods must be validated by
predictive performance rather than adopted on structural grounds alone?

## C4-05 — Hastie, Tibshirani & Friedman (2009)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-PENDING` |
| **Zotero key** | `LR3KF2SX` |
| **Full title** | Linear Methods for Regression (chapter in *The Elements of Statistical Learning*) |
| **Type / year** | book section, 2009 |
| **DOI** | 10.1007/978-0-387-84858-7_3 |
| **Used in** | §4.3, second paragraph |
| **Added by** | ch4-prose-pass-followup-01, F3d |

**The claim it must support:**

> Collinearity is a pathology of linear estimation, where it inflates coefficient
> variance and makes individual coefficients uninterpretable.

**To verify:** does the chapter state that correlated predictors inflate
coefficient variance in least-squares estimation, and that this is a property of
linear estimation specifically?

⚠ **Citation-form note.** The library holds this as a *book section*, and there
is a separate whole-book entry for *Elements of Statistical Learning*. Decide
which the thesis cites and use one consistently, or the reference list carries
both.

## C4-06 — Bergmeir, Hyndman & Koo (2018)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-PENDING` |
| **Zotero key** | `LD4FNLEN` |
| **Full title** | A note on the validity of cross-validation for evaluating autoregressive time series prediction |
| **Type / year** | journal article, 2018 |
| **URL** | https://www.sciencedirect.com/science/article/pii/S0167947317302384 |
| **Used in** | §4.3, first paragraph — **optional**, F3e |
| **Added by** | ch4-prose-pass-followup-01, F3e |

**The claim it must support:**

> Observing the admissibility rule is what allows the evaluation to be read as an
> estimate of forecasting performance rather than of in-sample fit.

**To verify:** does the source establish conditions under which an evaluation
scheme yields a valid estimate of out-of-sample forecasting performance for
autoregressive models?

**Note:** this is the one I am least confident maps cleanly. The paper is about
cross-validation validity, and the chapter's claim is about feature
admissibility. Related, but not identical. **If NotebookLM returns `NLM-PARTIAL`,
drop it** — F3e is marked optional precisely because the argument stands without
it.

## C4-07 — Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*

| | |
|---|---|
| **Status** | `IN-ZOTERO` ⚠ **metadata incomplete** / `NLM-PENDING` |
| **Zotero key** | `5NFQRRXS` |
| **Title as stored** | "5.2 Some simple forecasting methods \| Forecasting: Principles and Practice (3rd ed)" |
| **Type / year** | book, **no year recorded** |
| **Used in** | §4.2.2 twice (F3b, F3c) |
| **Added by** | ch4-prose-pass-followup-01 |

**The claims it must support:**

1. Logarithmic transformation is the standard response to multiplicative
   variance, stabilising variance so a proportional change has the same effect at
   every level.
2. Differencing is the conventional treatment for a series carrying a unit root.

**Both are textbook-standard**, so the verification risk is low. The problem is
metadata, not substance.

⚠ **Three defects in the library entry, all needing a fix in Zotero:**

- **No year.** The prose cites "2021", which is the third edition's date, but the
  entry carries none — so an automated bibliography build produces "n.d.".
- **The title is a single section**, "5.2 Some simple forecasting methods",
  rather than the book. Chapter 5 cites §5.2 of this book for the simple
  benchmarks, which is presumably why. But §4.2.2 cites it for log transforms and
  differencing, which are **not in §5.2** — so as stored, the entry points at the
  wrong part of the book.
- **The URL carries a `?utm_source=chatgpt.com` parameter.** Harmless
  functionally, but it should not appear in a submitted reference list.

**Recommended fix:** add the book as its own entry with full metadata
(Hyndman & Athanasopoulos, 2021, 3rd ed., OTexts, Melbourne), and cite sections
by number in text. **Do this before the bibliography is exported.**

## C4-08 — Kim (2013)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / **not used** |
| **Zotero key** | `FPJSJGSM` |
| **Full title** | Statistical notes for clinical researchers: assessing normal distribution (2) using skewness and kurtosis |
| **Used in** | — |

Available for the same skewness claim as C4-02 and C4-03. **Deliberately not
used** — two sources are sufficient and a third is padding. Recorded so a later
session does not "discover" it and add it.

---

# The NotebookLM return format

NotebookLM output must come back in a form that can be pasted into this register
without re-typing, and read by a later session without interpretation.

**Ask for exactly this, one block per citation:**

````markdown
## <register-id> — <Author> (<Year>)

**VERDICT:** CONFIRMED | PARTIAL | REFUTED | NOT-ADDRESSED

**CLAIM AS WRITTEN:**
> <the sentence from the thesis, verbatim>

**SUPPORTING PASSAGE:**
> <direct quotation from the source, verbatim, with page or section>

**LOCATION:** <page number, section number, or "not locatable in provided text">

**ASSESSMENT:**
<2-3 sentences: does the passage support the claim as written, and if PARTIAL,
exactly which part is unsupported>

**SUGGESTED REWORDING:** <only if PARTIAL; the claim narrowed to what the source
actually supports. Omit this field entirely if CONFIRMED>
````

## Why each field is there

**VERDICT first**, as one of four fixed words, so a later session can filter
without reading prose. `NOT-ADDRESSED` is distinct from `REFUTED`: a source that
is silent on a claim is not evidence against it, but it cannot be cited for it
either.

**CLAIM AS WRITTEN, verbatim**, because the thing being verified is the
thesis sentence, not a paraphrase of it. A summary of a claim can be true when
the claim is false.

**SUPPORTING PASSAGE as a direct quotation.** This is the field that makes the
verification checkable by a human later. A verdict without a quotation is an
assertion, and the whole point of this register is not to accept assertions.

**LOCATION**, so the citation can carry a page number where the claim is
specific.

**SUGGESTED REWORDING only on PARTIAL**, because that is the only verdict where
prose can be rescued. On CONFIRMED there is nothing to change; on REFUTED the
citation goes rather than the sentence being bent to fit.

## Rules for the run itself

**Do not upload thesis chapters to NotebookLM.** It returns our own wording back
as a source, which reads as independent confirmation and is not. Upload the
*source PDFs*; paste the *claims* into the query.

**One notebook per chapter**, or per verification batch. Mixing chapters makes
the returned blocks hard to route back.

**Paste the returned blocks into this file** under the matching register ID,
replacing `NLM-PENDING` with the verdict. The register is the record; the
NotebookLM session is not.

---

# Sources not in Zotero

None currently. Every citation proposed in the Chapter 4 sessions was already in
the library.

**When one is proposed that is not in the library**, it is recorded here with
status `NOT-IN-ZOTERO`, and:

1. It **does not go into the prose** until it is in Zotero. A citation the
   bibliography cannot resolve is worse than no citation, because it looks
   verified.
2. The register row states what it is needed for, so whoever adds it can check
   they are adding the right item rather than a same-titled preprint.
3. After adding, re-pull and move the row to `IN-ZOTERO` / `NLM-PENDING`.

**"If a source is not in the library, it is not a source."** This is the
project rule that exists because a plausible-looking reference was once written
from memory and read as verified.

---

# Relationship to the other registers

| Surface | Holds |
|---|---|
| **this file** | citations we **added**, with the claim each supports |
| `notebookLM/04-Claims_Verification/Chapter <N> - <Name>/<Topic>/claims.md` | claims the thesis makes that **need** a source and do not have one, numbered `CV-NN` |
| `deferred-structural-decisions.md` | layout and cross-reference decisions |
| `post-hpc-validation.md` | claims awaiting a measurement |

The two citation surfaces run in opposite directions: this file starts from a
source and asks whether it supports the claim; the `claims.md` packs start from a
claim and ask whether a source exists. A pass usually feeds both.

**The `CV-NN` packs are the established system** and have their own conventions —
see `04-Claims_Verification/Claims_Verification-00-MASTER-verification-brief.md`
and `-01-HOW-TO-RUN.md`. This register does not replace them. It covers the case
they do not: a citation that *was* added, where the risk is not a missing source
but a real source cited for something it does not say.

**Chapter 4 has an open `CV` item that belongs in a pack, not here**: the ARIMA
24-period minimum, which has no source. The follow-up offers a reworded sentence
that avoids needing one, so it may resolve without verification.
