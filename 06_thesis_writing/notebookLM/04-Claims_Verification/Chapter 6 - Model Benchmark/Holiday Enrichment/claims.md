---
name: ch6-holiday-enrichment-claims
description: Unverified statistical-threshold claims behind the Ch6 feature-diagnostics results (VIF, redundancy clustering). Feeds the NotebookLM statistical notebook (Notebook A).
chapter: 6
section: "6.5 Results (feature diagnostics, appendix tables 97-98)"
topic: Holiday Enrichment / feature diagnostics
prose_source: writing-notes/srq1-holiday-enrichment-result-and-limitations.md; appendix tables 97, 98
created: 2026_09_07-15_10
updated: 2026_09_07-15_10
---

# Ch6 — Feature diagnostics: statistical thresholds to verify

**These two are the highest priority in the whole verification exercise**, because both
are *numeric cut-offs that appear in a results appendix*. A number presented as a
standard, with no standard behind it, is the failure this folder exists to catch.

Neither currently appears in body prose — they live in appendix tables 97 and 98. **Do
not write either into prose before verification.**

---

## CV-01 — VIF thresholds of 5 and 10

**The claim:**
> VIF above 10 indicates serious multicollinearity; above 5 is a stricter cut-off.

**Where it entered:** `srq1_feature_diagnostics.py`, as constants with a comment.

**Its history — this is why the folder exists.** The comment originally attributed these
to **Hair et al. (2019), Multivariate Data Analysis**. That attribution was written
**from memory**. The source is not in the Zotero library, was never opened, and could not
be checked. It has been removed from the code.

**To determine:**
1. Does a citable source state a VIF threshold of 10? Of 5?
2. Rule of thumb, or derived criterion?
3. Does Hair et al. actually contain it — was the attribution wrong as well as
   unverified?
4. Is there a primary source earlier than the textbooks?

**Current state:** appendix table 97 asserts **no threshold at all**, deliberately. If no
source is found, that is permanent and the bands never enter prose.

---

## CV-02 — Spearman |rho| >= 0.95 as a redundancy cluster boundary

**The claim:**
> A Spearman rank correlation of 0.95 or above defines a redundancy cluster.

**Where it entered:** `srq1_feature_diagnostics.py::REDUNDANCY_RHO`.

**Status: never had a source, not even a remembered one.** It was chosen.

**To determine:**
1. Is 0.95 used as a redundancy threshold in the feature-selection literature?
2. Is there a conventional value (0.9? 0.8?) that is actually attested?
3. Is threshold-based redundancy clustering a recognised method, or is the defensible
   framing "an arbitrary reporting parameter"?

**Acceptable fallback, already drafted:** describe it as a chosen reporting parameter and
add a sensitivity check at 0.90 and 0.99. Only displace this if a real convention exists.

---

## Context that makes these lower-stakes than they look

The naive VIF-based reduction was **measured and rejected**: cutting 16 features to 9
raised mean test WMAPE from 26.44 to 28.82 (appendix table 98). So no feature was
dropped on the strength of either threshold — they are *reporting* bands over a
diagnostic, not a selection rule.

That is worth stating in prose regardless of the verdicts, because it means the thesis
does not depend on either number being correct.

---

## Notebook routing

**Notebook A (statistical).** Needs a body of statistics / econometrics /
feature-selection literature, not a single document. Do not mix with CV-03/04/05.

**If you only run one notebook, run this one.**
