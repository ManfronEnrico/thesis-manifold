---
name: 2026-09-15_NLM_ch2-citation-verification-pass
description: PASS - NotebookLM's Chapter 2 citation checks, delivered twice in contradicting versions and resolved against the library. Two sources are genuinely absent from Zotero, several proposed fixes target a superseded draft, and three small edits are real.
category: workflow
applies-to: [ch2_literature_review]
triggers: [ch2 citations, notebooklm, citation verification, ch2 prose pass]
created: 2026_09_15-12_40
updated: 2026_09_15-12_40
snapshot: 2026-09-15_10-49_final-comment-sweep
status: prose ready to paste, awaiting human review
---

# Chapter 2 — NotebookLM citation pass, verified

Verified at `37a04f0`, fetch clean. Snapshot `2026-09-15_10-49_final-comment-sweep`.
Zotero re-pulled **2026-09-15 10:49:34, 92 items**, cross-read against
`bibtex.bib` (92 entries — the two agree).

**Notes swept:** `ch2_literature_review/` holds `2026-09-14_appendix-citations-ch2.md`
(reference material, nothing to apply) and `generated/literature_design_map.md`.
`.archive/2026-09-14_ch2-pass-applied.md` already archived. **Nothing dropped.**

---

# ⚠ Read this first — the block arrived twice, and the two copies disagree

**You pasted two Chapter 2 tables.** They are not duplicates: they give
**opposite verdicts** on four items.

| ID | Copy A says | Copy B says | **Truth** |
|---|---|---|---|
| CIT-001 Saunders | ❌ FABRICATED | ✅ COHERENT | ✅ **Copy B.** `XH475DIR` is in the library |
| CIT-002 Saunders | ❌ FABRICATED | ✅ COHERENT | ✅ **Copy B.** Same item |
| CIT-011 Liu 2025 | ❌ FABRICATED | ✅ COHERENT | ⚠ **Copy A.** **Not in the library** |
| CIT-012 Semerikov | ❌ FABRICATED | ✅ COHERENT | ⚠ **Copy A.** **Not in the library** |

⚠ **Neither copy is reliable on its own.** Copy A cried fabrication on a book we
own; Copy B waved through two sources we do not. **Each copy is wrong exactly
where the other is right**, which is why every item below was resolved against
the library rather than by choosing a version.

**Do not forward either copy to anyone as a verdict list.**

---

# F1 — ⚠ Two cited sources are not in the Zotero library

**This is the finding of the pass, and it blocks Ch1's F2 as well.**

I searched `citations.json` (92 items, all seven item types present, so the
type-filter trap does not apply) **and** parsed all 92 `bibtex.bib` entries for
any author named Liu and for any title touching quantisation, distillation, edge
deployment, compression or resource constraints.

**Result — the only Liu in the entire library:**

```
[liu_a_2024]  "A Dynamic LLM-Powered Agent Network for
               Task-Oriented Agent Collaboration"   (DyLAN, arXiv:2310.02170)
```

| Cited in Ch2 | In library? |
|---|---|
| **Liu et al. (2025)** — §2.2, quantisation and distillation for edge | ❌ **absent** |
| **Semerikov et al. (2025)** — §2.2, resource-constrained LLM survey | ❌ **absent**, zero hits on any spelling |

### Why this matters more than it looks

⚠ **These two citations carry §2.2's central quantitative claim** — *"even
aggressively compressed LLMs typically require on the order of one to four
gigabytes"*. That number is what justifies calling the API instead of hosting a
model locally, which is a load-bearing architectural decision for the whole
thesis.

⚠ **It also resolves Chapter 1's F2 in the wrong direction.** My Ch1 note
proposed repointing Ch1's `(Liu et al., 2024)` to `Liu et al. (2025)`, on the
reasoning that the edge-AI source was already cited next door. **That fix is now
withdrawn** — there is no such item to point at. See the Ch1 follow-up note.

### ⚠ NEEDS-BRIAN — three options, and I recommend the third

| | Option | Cost |
|---|---|---|
| 1 | **Add both to Zotero** from the real publications | correct, if the papers exist and say this |
| 2 | **Delete both sentences** from §2.2 | loses the 1–4 GB claim and the API-versus-local argument |
| 3 | **Find the real sources**, add them, keep the claims | ⚠ **recommended** — the claims are almost certainly true and well-supported in the literature; they just need a source we have read |

→ **Do not simply write the references from memory.** A plausible-looking
reference written from memory once read as verified in this project, which is why
the rule exists.

---

# F2 — §2.4, the Sapkota year is already correct in the document

**NotebookLM (both copies) wants `Sapkota et al. (2025)` → `(2026)`.**

✅ **No edit needed.** The snapshot already reads `Sapkota et al. (2026)` at
`ch2-literature-review.md:69`. NotebookLM's "current text to replace" quotes
`2025`, which is **not what the document says** — it is describing a superseded
draft.

⚠ **This is the pattern to watch in this block.** Several of its proposed fixes
target text that no longer exists. Each is flagged below rather than pasted.

---

# F3 — §2.1, the Al-Karkhi rename is already done

**NotebookLM wants the reference list corrected from "Nguyen et al. (2025)" to
Al-Karkhi & Rządkowski.**

✅ **Already correct in the document.** `ch2-literature-review.md:25` reads
*"Al-Karkhi and Rządkowski (2025), reviewing over 120 machine learning papers..."*
and cites `(Al-Karkhi & Rządkowski, 2025)`. **"Nguyen" appears nowhere in Ch2 or
in the reference list** — I grepped both.

✅ **The library has it:** `al-karkhi_innovative_2025`, *"Innovative machine
learning approaches for complexity in economic forecasting and SME growth"*.

→ **No action.** Superseded fix.

---

# F4 — §2.1, the Ceran rewrite is aimed at a draft that no longer exists

**NotebookLM wants the "15% MAPE benchmark" sentence rewritten.**

⚠ **That sentence is gone.** The current text reads:

> "Ceran et al. (2024), forecasting daily product-store sales across roughly fourteen million series for a national supermarket chain, select LightGBM with Optuna hyperparameter tuning and reach a weighted root mean squared scaled error of 0.83, improved to 0.81 by ensembling group-specific models."

✅ **The chapter already says the opposite of what NotebookLM is correcting.** It
goes on: *"they explicitly reject MAPE because their panel contains too many
zero-demand observations for a percentage error to be well defined"*.

✅ **This is also the withdrawn accuracy target from Ch5 §5.4.3.** The 15 per cent
figure was traced to this paper, found not to be in it, and withdrawn across the
thesis. **Re-inserting it would undo that correction.**

→ **No action. Do not paste NotebookLM's replacement.**

---

# F5 — §2.1, Ahrens is already reworded exactly as proposed

**NotebookLM proposes:** *"...within a double machine learning framework, showing
that constrained least-squares stacking of diverse candidate learners
consistently reduces mean squared prediction error relative to individual
estimators in econometric settings."*

✅ **The document already reads word for word that.** `ch2-literature-review.md:27`.

⚠ **Its "current text to replace" quotes an `inverse-variance weighting` clause
that is no longer present.** Superseded.

→ **No action.**

⚠ **Two Ahrens records in the library**, `I86QMNYE` and `ahrens_model_2025`, same
title. **Duplicate — merge before generating the bibliography.**

---

# F6 — §2.5, the Gu year ⚠ THE ONE REAL EDIT IN THIS BLOCK

**Both copies agree, and this one checks out.**

### Anchor

**Chapter 2, Section 2.5 Reliability, Traceability, Uncertainty, and Evaluation
of Agentic Outputs** — in the paragraph beginning *"Finally, evaluating whether
an agentic layer improves decision-support outputs..."*. Searchable, verbatim:

> "Gu et al. (2025) survey this design space, concluding that pairwise comparison tends to be more consistent than absolute scoring and that judge reliability depends on consistency, robustness, and alignment with human judgment."

**The sentence after it begins:**
> "Ye et al. (2024) quantify systematic biases in LLM judges..."

### Action

REWORD — `2025` → `2024`. **One character.**

#### Replace with

> "Gu et al. (2024) survey this design space, concluding that pairwise comparison tends to be more consistent than absolute scoring and that judge reliability depends on consistency, robustness, and alignment with human judgment."

### Note

✅ **In the library:** `ZPI97MWE`, *"A Survey on LLM-as-a-Judge"*, arXiv:2411.15594
— the arXiv identifier encodes **November 2024**, which settles the year.

⚠ **Check the reference list entry matches after the change**, and note that
thread 277 regenerates it anyway.

---

# F7 — §2.5 and §2.7, two proposed rewrites I am rejecting

## CIT-030 — Dong et al., the em-dash rewrite

NotebookLM proposes replacing the commas with em dashes and **dropping the final
clause** *"positioning such traceability as relevant to emerging compliance and
auditability expectations."*

❌ **Reject.** The year is already `2024` in the document, so the stated reason
for the edit does not apply. The only real change is deleting a clause that does
useful work — it is what connects traceability to the governance argument §2.6
then builds on.

⚠ **Also note the em dashes.** The watermark sweep
(`2026-09-14_BRANCH_A_watermark-patterns-to-remove.md`, P6) is trying to *reduce*
em-dash density. Adding two would work against a pass you have not yet run.

## CIT-032 — Kuleshov, the "post-hoc parametric" rewrite

❌ **Reject as written — it contains a factual error.** NotebookLM's replacement
calls isotonic recalibration *"this post-hoc **parametric** approach"*.

⚠ **Isotonic regression is non-parametric.** It fits a monotone step function
with no fixed functional form. Calling it parametric and contrasting it with
"non-parametric split conformal prediction" gets the distinction backwards, and
an examiner in this area would notice immediately.

✅ **The existing text is already correct and already draws the distinction** the
edit is reaching for: §2.5 says Kuleshov and Levi do *"post-hoc recalibration of
a model's own predictive distribution"*, then opens the next paragraph with
*"The second family is conformal prediction, which is the approach the present
artefact adopts and which the recalibration literature above does not cover."*

→ **No action.** If you want the neural-network scope made explicit, the chapter
already does that too, one sentence later.

---

# Confirmed, no action

**Thirty-one items verified against the library and the snapshot.** Every source
below exists and is cited for a claim it supports:

CIT-003 Makridakis 2020 · CIT-004 Makridakis 2022 · CIT-006 Ma 2025 ·
CIT-009 Klee & Xia · CIT-010 Ng 2017 · CIT-013 Elmachtoub & Grigas ·
CIT-014 Mandi · CIT-015 Rinaldi · CIT-016 Olszak & Bartuś ·
CIT-017 Pathirannehelage · CIT-018 Goodwin · CIT-019 Schick ·
CIT-020 Ma 2024 SciAgent · CIT-021 Paranjape · CIT-022 Wang 2024 ·
CIT-024 Liu DyLAN · CIT-025 Li AutoFlow · CIT-026 Wang ScoreFlow ·
CIT-027 Ji ANAH · CIT-028 Wang AgentNoiseBench · CIT-029 Kartik ·
CIT-031 Guo · CIT-033 Levi · CIT-035 Ye · CIT-036 Mehta ·
CIT-037 Ouyang · CIT-038 Atıl · CIT-039 Schwartz · CIT-040 Chen FrugalGPT ·
CIT-042 Zheng · CIT-044 Hevner · CIT-045 Peffers

⚠ **CIT-029, a naming trap worth recording:** NotebookLM says the reference list
names "Sapra et al. (2025)" and should say Kartik. **The library key is
`kartik_agentcompass:_2025` and searching "Sapra" returns that same item** — so
Sapra is a co-author, not a wrong entry. The reference list does not contain
"Sapra". **No action.**

---

# CIT-043 — Chen & Bibi, a judgement call for you

**NotebookLM wants the MLAT sentence expanded** to name its SSRN preprint status,
its pricing-tool scope and its small synthetic dataset.

✅ **The source is in the library** (`FKXU4NLX`) and ✅ **the current sentence is
already honest** — it says *"exists only as small, non-peer-reviewed proofs of
concept and does not address forecasting, reliability, or production
constraints."*

**NEEDS-BRIAN.** The proposed version is more specific and slightly stronger for
the gap argument, since naming a *pricing* tool sharpens that nobody has done
*forecasting*. But it is longer, and §2.7 is a tight paragraph.

⚠ **If you take it, drop the phrase "small synthetic datasets"** — I cannot
verify from the library record whether MLAT's data is synthetic, and a
specific unverified claim is worse than the general one already there.

---

# Chapter rename — not recommended

*"Chapter 2 | Literature Review"* with the standfirst *"What is known, and what
is missing"* is accurate and does real work: the standfirst frames the gap
argument §2.7 delivers. ✅ **No change.**

---

# For the registers

## `citations-added-register.md`

**No citations added.** F6 corrects a year on an existing item.

## Claims register — two rows

| Claim | Where | To verify |
|---|---|---|
| *"even aggressively compressed LLMs typically require on the order of one to four gigabytes"* | Ch2 §2.2 | **Which source states this?** Semerikov is not in the library |
| *"quantisation and distillation... substantial accuracy preserved at sharply reduced memory footprints"* | Ch2 §2.2 | **Which source states this?** Liu 2025 is not in the library |

## Zotero hygiene — duplicates found this pass

| Item | Keys |
|---|---|
| Ahrens, *Model Averaging and Double Machine Learning* | `I86QMNYE`, `ahrens_model_2025` |
| Ma, *A data-driven and context-aware approach...* | `YPG7VZSJ`, `BW87Z3JR` |
| González-Potes (from the Ch1 pass) | `69RUBISC`, `gonzález-potes_hybrid_2026` |
| *Elements of Statistical Learning* (thread 277) | `4TVC5APJ`, `SPW7NXHT`, `Q4IIBE2Z` |

⚠ **A data-integrity note:** `liu_a_2024` carries **`2026`** in its bibtex year
field while the reference list renders it as 2024. **Fix the year in Zotero**, or
the generated bibliography will disagree with every in-text citation.

---

# Summary

| | |
|---|---|
| **Real edits** | **1** — F6, the Gu year |
| **Already applied** | 4 — Sapkota, Al-Karkhi, Ceran, Ahrens |
| **Rejected** | 2 — Dong (no-op + clause loss), Kuleshov (parametric error) |
| **⚠ Blocking** | **2 missing sources**, carrying §2.2's 1–4 GB claim |
| **Confirmed** | 31 |
