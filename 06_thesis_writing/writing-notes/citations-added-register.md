---
name: citations-added-register
description: NOTE - Every citation added to the thesis during a prose or follow-up session, with the exact claim it supports and its NotebookLM verification state. Cumulative. Includes the required NotebookLM return format for machine re-ingestion.
category: reference
applies-to: [chapter 4, chapter 5, citations, verification]
created: 2026_09_09-21_10
updated: 2026_09_10-17_45
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
| Last Zotero pull | **2026-09-10 19:08** |
| Items in library | 87 |
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
| **Status** | `IN-ZOTERO` **metadata fixed 2026-09-10** / `NLM-PENDING` |
| **Zotero key** | `5NFQRRXS` |
| **Full title** | Forecasting: principles and practice |
| **Type / year** | book, 3rd edition, 2021, OTexts, Melbourne |
| **Authors** | Hyndman, Rob J.; Athanasopoulos, George |
| **Used in** | Ch4 §4.2.2 twice (F3b, F3c); Ch5 §5.1, §5.2.1, §5.5.2 |
| **Added by** | ch4-prose-pass-followup-01 |

**The claims it must support:**

1. Logarithmic transformation is the standard response to multiplicative
   variance, stabilising variance so a proportional change has the same effect at
   every level.
2. Differencing is the conventional treatment for a series carrying a unit root.

**Both are textbook-standard**, so the verification risk is low. The problem is
metadata, not substance.

**RESOLVED 2026-09-10.** All three defects recorded here - the missing year, the
section title standing in for the book, and the `utm_source` parameter - are
fixed, and the entry now carries both authors. Confirmed against a fresh pull.

**The diagnosis in this row was the useful part and is worth keeping:** the entry
was stored as section 5.2 because Chapter 5 cites that section, but Chapter 4
cites the same entry for log transformation and differencing, which are in
different chapters of the book entirely. One entry cannot point at three places.

**Settled as DEC-FPP-WHOLE-BOOK:** cite the whole book. One bibliography entry,
per the authors' own presentation of the work. A section locator appears in text
only where a passage is quoted directly, and **never a page number** - the online
edition is revised continuously and does not share pagination with the print
version.

That resolves the three-places problem: Chapter 4's two citations need no
locator at all, since neither quotes anything, and Chapter 5's carry
"Section 5.2" where they quote.

**Still `NLM-PENDING`.** The metadata is right; whether the source supports the
two Chapter 4 claims is a separate question, and it is covered by the source
review at
`notebookLM/03-Modelling_Review/forecasting-book-sections-for-citation-verification.md`.

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

## C4-09 — Nager.Date (added by Brian, 2026-09-10)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-N/A` |
| **Zotero key** | `3MTF7LGL` |
| **Type / year** | computerProgram, 2026 |
| **URL** | https://github.com/nager/Nager.Date |
| **Used in** | §4.3, the holiday-calendar sentence |
| **Added by** | Brian, directly in Word and Zotero |

**The claim it supports:** that the Danish public-holiday calendar was obtained
from the Nager.Date service.

**No NotebookLM verification applies.** This is a data source, not an argument —
the claim is provenance, and the pipeline's own manifest is the evidence:
`_00_raw/holidays/nager_dk_manifest.json` records the retrieval at
2026-09-06T15:06:15Z, coverage 2018-2027, and a SHA-256 per year.

⚠ **The in-text form needs fixing**, not the entry: `(nager, 2014/2026)` should
read `(Nager.Date, 2026)`. A slash-separated year pair means a reprinted work.
See F2 in `ch4_data_assessment/ch4-complete-pass-followup-02.md`.

### Note - this entry exposed an export bug

`citations.json` is filtered by item type, and `computerProgram` was not in the
allowed set, so this entry was silently dropped from the export while present in
the library. A verification pass reported the citation missing when it was there.

**Fixed 2026-09-10:** the filter now also admits `computerProgram`, `dataset`,
`software`, `blogPost` and `manuscript`. The export went 86 -> 87 items.

**The lesson for this register:** `NOT-IN-ZOTERO` must never be recorded from
`citations.json` alone. Query the API unfiltered — the `/re-snap` skill carries
the snippet.

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

# Chapter 5

Both entries below are added by `ch5_model benchmark/ch5-prose-pass.md`, F16a.
They are the only citations that pass adds; every other source it names was
already cited in the chapter.

They arrived by an unusual route, which is worth recording: both come from an
August reference note that was archived as stale. Its **numbers** were superseded,
but this citation work was not, because it concerns what a source says rather
than what a run measured.

**Every other Chapter 5 citation was audited on 2026-09-10** against the
unfiltered Zotero API - fifteen sources, checked one at a time. **All fifteen are
in the library**, so nothing else needs adding here. Four have metadata defects
that will render wrong in the bibliography, tracked as S16 on the deferred list
rather than as register rows, since they are library problems rather than
questions about whether a source supports a claim.

⚠ **The thirteen pre-existing sources have no rows in this register**, because
this register records citations that were *added*. If the NotebookLM pass is
meant to cover every claim in the chapter rather than only new ones, they need
rows. Worth settling before that run - a source cited since August is no more
verified than one cited today.

## C5-01 - Bergmeir, Hyndman & Koo (2018)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-PENDING` |
| **Zotero key** | `LD4FNLEN` |
| **Full title** | A note on the validity of cross-validation for evaluating autoregressive time series prediction |
| **Type / year** | journal article, 2018 |
| **Used in** | §5.3.4, the paragraph justifying the validation scheme |
| **Added by** | ch5-prose-pass, F16a |

**The claim it must support:**

> Standard K-fold cross-validation is not rejected on principle. It is valid for
> stationary autoregressive processes with uncorrelated residuals, and on such
> series it uses the data more efficiently than a single out-of-sample split
> (Bergmeir et al., 2018).

**To verify:** does the source establish that standard K-fold cross-validation is
valid for autoregressive models with uncorrelated errors, and that it is more
data-efficient than out-of-sample evaluation on stationary series?

**Why the wording is cautious.** The citation is being used to state a
*limitation* of the alternative we rejected, which is the honest direction. The
tempting sentence - that K-fold is invalid for time series - is contradicted by
this very paper, so a misreading here would be visible to any examiner who
follows the reference.

## C5-02 - Cerqueira, Torgo & Mozetic (2020)

| | |
|---|---|
| **Status** | `IN-ZOTERO` / `NLM-PENDING` |
| **Zotero key** | `SZSQ955R` |
| **Full title** | Evaluating time series forecasting models: an empirical study on performance estimation methods |
| **Type / year** | journal article, 2020 |
| **DOI** | 10.1007/s10994-020-05910-7 |
| **Used in** | §5.3.4, same paragraph as C5-01 |
| **Added by** | ch5-prose-pass, F16a |

**The claim it must support:**

> Under non-stationarity, methods that preserve temporal order estimate
> generalisation loss substantially more accurately (Cerqueira et al., 2020).

**To verify:** does the source find empirically that order-preserving evaluation
outperforms cross-validation on non-stationary series, and does it also note the
converse for stationary or small-sample cases?

**The converse matters.** The same paper reportedly finds cross-validation
beneficial when a series is stationary or the sample is small. Our sample *is*
small, so a verification run should establish whether the paper's position is
narrower than the sentence implies. If it is, the sentence narrows to
non-stationarity alone, which is the property we actually rely on.

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

**Chapter 4's open `CV` item is now answered, and the answer is that the claim
must go.** The item was the ARIMA 24-period minimum, recorded as having no
source.

**It has no source because the standard reference rejects the whole class of
claim.** Hyndman & Athanasopoulos, Section 13.7, read directly from the PDF on
2026-09-10:

> "Some textbooks provide rules-of-thumb giving minimum sample sizes for various
> time series models. These are misleading and unsubstantiated in theory or
> practice. Further, they ignore the underlying variability of the data and often
> overlook the number of parameters to be estimated as well. There is, for
> example, no justification for the magic number of 30 often given as a minimum
> for ARIMA modelling."

So a verification run would return `REFUTED`, and citing any source for a minimum
length would be citing something this book calls unsubstantiated. **Remove the
claim rather than sourcing it.** The defensible replacement is the book's own
framing: the requirement depends on the number of parameters estimated and the
noise in the data, not on a fixed count.

Details and the surrounding quotations:
`notebookLM/03-Modelling_Review/fpp3-first-pass-findings.md`, finding 4.

---

## Chapter 6 pass, 2026-09-11 — two citations proposed, both verified present

Verified against the **unfiltered Zotero API** at the 2026-09-11 20:08 pull, 89
items, checked by author and date rather than through the filtered export.

### C6-01 — Ouyang, Zhang & Harman (2025)

| | |
|---|---|
| Zotero key | `AMB2F6T2` |
| Title | An Empirical Study of the Non-Determinism of ChatGPT in Code Generation |
| Date in library | January 22, 2025 |
| Lands in | **Section 6.4**, the JSON function-calling paragraph |
| Status | `IN-ZOTERO` ✅ · `NLM-CONFIRMED` ⬜ |

**The sentence it is being used to support, verbatim:**

> "Non-determinism in language-model code generation is measurable and
> substantial (Ouyang et al., 2025), which is why the property is designed for
> rather than assumed."

**What the citation must establish:** that the same prompt, issued repeatedly to
a language model, yields materially different generated code. It is cited for the
**existence and scale of the problem**, not for any claim that function-calling
is the remedy — that argument is ours and rests on the artefact.

⚠ **Verify the direction before submission.** A paper reporting that
non-determinism is *small* would refute this sentence rather than support it. The
title asserts an empirical study; its magnitude is what must be read.

### C6-02 — Goodwin, Önkal & Thomson (2010)

| | |
|---|---|
| Zotero key | `IJ8UMZ3X` |
| Title | Do forecasts expressed as prediction intervals improve production planning decisions? |
| Date in library | 2010-08-16 |
| Lands in | **Section 6.4**, the Uncertainty paragraph |
| Status | `IN-ZOTERO` ✅ · `NLM-CONFIRMED` ⬜ · **offered as optional** |

**The sentence it is being used to support, verbatim:**

> "**Uncertainty**, by attaching interval information to every forecast, which is
> what allows a planner to act on the forecast's reliability rather than on its
> point value alone (Goodwin et al., 2010)."

**What the citation must establish:** that presenting a forecast as an interval
changes, and preferably improves, a production planning decision relative to a
point forecast.

⚠ **This one carries real risk and must not be pasted unverified.** The title is
a *question*, and papers in this literature sometimes answer it negatively. If
the finding is that intervals did **not** improve decisions, the citation still
belongs in the thesis — but in the limitations, supporting a different sentence.
**Read the finding before the citation goes in.**

### Not added — Dong, Lu & Zhu (2024), AgentOps

| | |
|---|---|
| Zotero key | `DAN2UBT6` |
| Date in library | 2024-11-30 |
| Would land in | Section 6.6, the observability capability |

Verified present and on topic. **Deliberately not added**: Section 6.6 carries no
open comment, and adding citations to sections nobody has questioned is scope
that was not asked for. It would strengthen the thinnest section in the chapter
if wanted.
