---
name: claims-verification-how-to-run
description: Operating procedure for the unsourced-claims verification run - what to upload, why this run is split across two notebooks, how to handle each verdict, and what to write back where.
created: 2026_09_07-10_00
updated: 2026_09_07-10_00
---

# How to run the claims verification

Companion to `Claims_Verification-00-MASTER-verification-brief.md`. That file is **what
to check**; this file is **how to run it and what to do with the answers**.

---

## 1. This run needs TWO notebooks, not one

The other runs in this folder each had one corpus. This one does not, and mixing the
five claims into a single notebook will produce worse answers for all of them.

| Notebook | Claims | Corpus |
|---|---|---|
| **A - Statistical** | CV-01, CV-02 | Statistics / econometrics / feature-selection texts |
| **B - Factual** | CV-03, CV-04, CV-05 | Danish legislation, XGBoost documentation |

**Why the split matters.** CV-01 and CV-02 are answered by *what a discipline
conventionally does*, and need a body of statistical writing to answer honestly.
CV-03 to CV-05 are answered by *a specific document* - a statute, a doc page. A notebook
holding both will answer a statistics question using a Danish shop-hours law in its
retrieval pool, and the failure mode is a confident wrong answer rather than a visible
error.

If you only have appetite for one run, **do Notebook A**. CV-01 and CV-02 are the two
that appear as numbers in a results appendix.

---

## 2. What to upload

**Notebook A - Statistical**

| # | What | Where from |
|---|---|---|
| 1 | Any regression / multivariate statistics texts you hold | Zotero, or `Candidate Sources/` |
| 2 | Feature-selection or dimensionality-reduction papers | Zotero |
| 3 | `Claims_Verification-00-MASTER-verification-brief.md` | this folder |

**Notebook B - Factual**

| # | What | Where from |
|---|---|---|
| 1 | Danish shop-opening-hours legislation (retsinformation.dk) | download to `Candidate Sources/` |
| 2 | Store Bededag abolition act | download to `Candidate Sources/` |
| 3 | XGBoost documentation on determinism / parameters | download to `Candidate Sources/` |
| 4 | `Claims_Verification-00-MASTER-verification-brief.md` | this folder |

**Do not upload:**

- **The thesis chapters.** This is the opposite of the methodology run. There, the
  chapters were the thing being checked. Here, the claim text is already quoted in the
  brief, and adding chapter prose lets the notebook retrieve *our own wording* and
  return it as if it were a source. That is exactly the failure that created CV-01.
- **The Saunders chapters or the literature-review PDFs.** Different corpus, different
  run.
- **The code files.** The relevant comments are quoted in the brief.

---

## 3. Handling each verdict

| Verdict | What to do |
|---|---|
| **Sourced** | Add the reference to Zotero. Update the register row to Verified with the citation. The claim may now enter prose. |
| **Partially Sourced** | The source supports a weaker claim. **Use the weaker claim.** Do not stretch the source to cover the original wording. |
| **No Source Found** | Apply the fallback in the brief summary table. This is a normal outcome, not a failure - three of the five have a workable fallback already written. |
| **Contradicted** | Highest priority. Remove the claim from code comments and notes immediately, then correct anywhere it has spread. |

**A note on CV-04.** Do not let a "No Source Found" verdict here suggest the finding
itself is unsupported. The *effect* is measured in this repository and reproducible on
demand. Only the *explanation* is in question, and the fallback - report the measurement,
hedge the cause - is fully defensible.

---

## 4. Where the answers go

1. **Save the raw NotebookLM output** to `NLM Review/` in this folder, named
   `Claims_Verification-Section_A-statistical_thresholds.md` and
   `Claims_Verification-Section_B-factual_claims.md`, matching the naming used in the
   other two review folders.
2. **Update the register** at `06_thesis_writing/writing-notes/unverified-claims-to-check.md`
   - it stays the single source of truth for what is still open. Change the status
   column; do not delete rows. A resolved row with its resolution recorded is more
   useful than a deleted one, because it shows the claim was checked.
3. **Only then** update the code comments and writing notes that carry the claim.

---

## 5. What NOT to paste back

- **Do not paste NotebookLM prose into thesis prose.** Take the citation and the
  verbatim quote; write the sentence yourself.
- **Do not paste a citation you have not opened.** This entire folder exists because a
  plausible-looking reference was written from memory. A reference from NotebookLM that
  you have not seen the source of is in the same category.
- **Do not record "NotebookLM says X" as a source.** It is a retrieval tool over
  documents you supplied; the source is the document.

---

## 6. Definition of done

Every row in `unverified-claims-to-check.md` shows one of:

- **Verified** with a citation now in Zotero, or
- **No source - reworded**, with the new wording recorded, or
- **Removed**, with a note of where it was removed from.

No row may remain in its original unchecked state when the thesis is submitted.
