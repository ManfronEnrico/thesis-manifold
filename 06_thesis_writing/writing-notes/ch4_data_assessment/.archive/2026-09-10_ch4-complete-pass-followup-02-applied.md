---
name: ch4-complete-pass-followup-02
description: NOTE - Second follow-up, against snapshot 15-09 and the 2026-09-10 Zotero pull (87 items). F1 and F3 applied. Two items left, both one edit each.
snapshot: 2026-09-10_15-09_ch4-final
category: workflow
applies-to: [chapter 4]
supersedes: [ch4-complete-pass-followup-01.md]
created: 2026_09_10-17_10
updated: 2026_09_10-17_45
status: ready
---

# Chapter 4 - follow-up 02

Regenerated against `2026-09-10_15-09_ch4-final`. Repository at `5137ed4`, fetch
clean. Zotero re-pulled: **87 items**.

## What you applied

| From follow-up 01 | State |
|---|---|
| F1, the holiday sentence names its ablation | **applied**, verbatim |
| F3, promotional correlation to two decimals | **applied** — Table 2 reads r = 0.94 |
| F2, the redundancy figures | applied, but took the **pre-measurement** wording |

You also added a Nager.Date citation to §4.3 and the matching Zotero entry, and
that entry is why the export needed fixing. See the note at the end.

## What is left

Two items, one edit each.

| # | Item | Why |
|---|---|---|
| [F1](#f1) | The redundancy sentence lost its numbers unnecessarily | the figures were re-measured after that fallback was written |
| [F2](#f2) | The Nager.Date in-text citation form | the source is real; the form is not APA |

---

# F1 - Put the redundancy figures back {#f1}

§4.3 now reads *"It performed worse across the four categories."*

That is the fallback I drafted **before** the numbers were re-measured, and it
is no longer the best available wording. Commits `1b0de33` through `0206402`
replaced table 98's hardcoded pair with a computed one:
`feature_diagnostics.py::evaluate_reduction()` fits the full and reduced sets
per category and model and writes `feature_reduction_eval.csv`.

**Measured on the current 18-feature set, across twelve category-and-model
cells: 29.31 against 32.13.** Read from the CSV this session.

A measured figure is stronger than a bare direction, and this one is computed at
render time rather than transcribed, so it cannot silently go stale.

### Anchor

**Section 4.3 Feature Engineering.** The second paragraph, beginning *"Within
that admissible set, two further questions were put to the data."*

First five words of the sentence: *"It performed worse across the..."*
Last five words: *"...across the four categories."*

### Action

REWORD.

**Before:**

> It performed worse across the four categories.

**After:**

> It performed worse, raising mean test error from 29.3 to 32.1 per cent across
> the twelve category-and-model combinations tested.

### Note - the denominator changed, not just the decimals

The old 26.4 and 28.8 were measured across **four categories** at 16 features.
The new pair spans **twelve cells** — four categories times three model families
— at 17 or 18. That is why the sentence says twelve combinations; quoting the
new figures against the old denominator would misdescribe the experiment.

### Note - do not quote a per-cell number here

Two cells are extreme. Water's LightGBM and Ridge each lose about eleven
percentage points under reduction while its XGBoost gains three. **The mean over
twelve cells is Chapter 4's claim.** The spread is a Chapter 5 observation and is
recorded in that chapter's ablation note.

### Note - the 0.95 threshold is computed now too

The same round made the grouping threshold read from
`feature_proposed_set.csv`'s `rho` column rather than sit as a caption literal.
The chapter still does not name it, which remains right: a project parameter
with no external source, and the argument does not need it.

---

# F2 - The Nager.Date citation form {#f2}

§4.3 reads *"joined onto the monthly grid from the Nager.Date (nager,
2014/2026) service"*.

**The source is in the library** — `computerProgram`, key `3MTF7LGL`, dated
2026, URL `https://github.com/nager/Nager.Date`. Verified against the 87-item
pull this session. Citing it is correct and the entry resolves.

**The in-text form is the problem.** `(nager, 2014/2026)` is not APA on two
counts: the author should be capitalised as the entry records it, and a
slash-separated year pair means a **reprinted work** — an original and a
republication date. Software takes a single version year.

### Anchor

**Section 4.3 Feature Engineering.** The paragraph below the caption **"Table 3
- Feature Engineering Overview"**, its first sentence.

First five words: *"Two of the column groups..."*
The clause to change: *"...from the Nager.Date (nager, 2014/2026) service..."*

### Action

REWORD — the citation only. The rest of the sentence stands.

**Before:**

> The Danish public-holiday calendar is joined onto the monthly grid from the
> Nager.Date (nager, 2014/2026) service, giving the number of days in each
> month, the number of public holidays falling within it, and the difference
> between the two.

**After:**

> The Danish public-holiday calendar is joined onto the monthly grid from the
> Nager.Date public holiday service (Nager.Date, 2026), giving the number of
> days in each month, the number of public holidays falling within it, and the
> difference between the two.

### Note - one sentence worth adding, if you want it

The pipeline caches the calendar with a checksum per year, which is a
reproducibility property an examiner would credit and which no citation conveys.
`_00_raw/holidays/nager_dk_manifest.json` records the retrieval at
2026-09-06T15:06:15Z, coverage of 2018 to 2027, and a SHA-256 per year.

Optional, appended to the same sentence:

> The calendar was retrieved once and cached with a per-year checksum, so the
> enrichment is reproducible from the stored copy rather than from a live
> service call.

### Note - check the Zotero entry has a retrieval date

APA wants an access date on a software entry whose contents can change. The
entry carries a 2026 date; **confirm it also has the URL access date**, since
the bibliography is generated from the library and will carry whatever is there.

---

# ⚠ Why I first reported this citation as missing

**I was wrong, and the cause is worth fixing rather than apologising for.**

I re-pulled Zotero, searched `citations.json`, found no Nager entry, and reported
the citation unresolvable. The re-pull was correct. The file was not.

`zotero_client.py` filtered its export to a hardcoded `_SCHOLARLY_TYPES` set —
journal articles, books, preprints and so on — which **did not include
`computerProgram`**. Your entry was therefore dropped between the API and the
export, and the result was indistinguishable from an entry that was never added.

**Fixed this session.** The set now also admits `computerProgram`, `dataset`,
`software`, `blogPost` and `manuscript`, with a comment recording why. The export
went from 86 items to 87 and Nager.Date now appears.

**And a `/re-snap` skill now exists**, which you asked for. It runs the fetch,
the snapshot, the diff against the previous snapshot, and the Zotero pull in one
step — and it carries this specific trap: *never conclude "not in the library"
from `citations.json` alone; query the API unfiltered, and search whole words.*

---

# Verified this session

**Table 2's promotional correlation** reads r = 0.94, matching §4.2.4. Measured
0.940 on 2,972 promotion-bearing brand-months.

**The holiday sentence** carries the tuned ablation and the six-of-nine count,
which is what Appendix Table 94 supports.

**Everything else** was verified in the complete pass and none of it has changed:
Table 1's structural counts, Table 2's ADF and autocorrelation columns, the
monthly shares, the peak-month sets, the HARBOE autocorrelations, the feature
counts of 18 and 17, and the split table.

---

# After F1 and F2

**Chapter 4 is finished.** Nothing in it is then unverified or unsupported.

Two items stay tracked elsewhere and neither blocks the chapter:

- **S1 and S4** in `deferred-structural-decisions.md` — whether Table 1's two
  SKU columns move to an appendix, and extending Appendix A with the
  per-category feature list.
- **S9**, the cross-chapter repetition pass, where §4.1 and §4.2.1 both
  establishing scope gets resolved.

Ready for Chapter 5.
