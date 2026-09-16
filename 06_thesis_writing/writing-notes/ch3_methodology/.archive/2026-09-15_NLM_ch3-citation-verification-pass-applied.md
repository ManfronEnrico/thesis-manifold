---
name: 2026-09-15_NLM_ch3-citation-verification-pass
description: PASS - NotebookLM's thirteen Chapter 3 citation checks. Eleven confirmed, one real fix on the Hevner three-cycle attribution, one rejected because its replacement removes a stance the chapter argues deliberately.
category: workflow
applies-to: [ch3_methodology]
triggers: [ch3 citations, notebooklm, citation verification, ch3 prose pass]
created: 2026_09_15-12_45
updated: 2026_09_15-12_45
snapshot: 2026-09-15_10-49_final-comment-sweep
status: prose ready to paste, awaiting human review
---

# Chapter 3 — NotebookLM citation pass, verified

Verified at `37a04f0`, fetch clean. Snapshot `2026-09-15_10-49_final-comment-sweep`.
Zotero re-pulled **2026-09-15 10:49:34, 92 items**.

**Notes swept — four live notes in `ch3_methodology/`:**

| Note | State | Carried |
|---|---|---|
| `2026-09-15_BRANCH_A_ch3-temperature-contradiction.md` | **not applied** — §3.6 still says *"outputs at temperature zero"* | ⚠ **still live, apply it** |
| `srq4-data-input-is-a-constructed-choice.md` | reference, not applied | optional A in the consolidated note |
| `verification-of-the-experimental-harness.md` | reference, not applied | optional B |
| `2026-09-14_appendix-citations-ch3.md` | reference | — |

✅ **Nothing dropped, and nothing below duplicates them.** This pass touches only
citations; the temperature fix is a separate, still-outstanding edit.

---

# Summary — the shortest of the four blocks

| | |
|---|---|
| **Real edits** | **1** — F1, the Hevner three-cycle attribution |
| **Rejected** | 1 — F2, the "modest realism" rewrite |
| **Confirmed** | 11 |

---

# F1 — §3.2, the three cycles are Hevner (2007), not Hevner et al. (2004)

**NotebookLM is right, and this is a real attribution error.**

### The problem

Ch3 §3.2 attributes the **relevance / design / rigor three-cycle view** to Hevner
et al. (2004). The 2004 MIS Quarterly paper establishes the IS research framework
(environment → design science research → knowledge base) and seven guidelines.
**The three-cycle terminology is Hevner's 2007 paper**, *"A Three Cycle View of
Design Science Research"*.

✅ **This is a genuine distinction, not pedantry.** A DSR examiner is likely to
know which paper named the cycles, and §3.2 is the chapter's methodological
foundation.

### Anchor

**Chapter 3, Section 3.2 Research Design: Design Science Research** — the
**opening sentence of the second paragraph**. Searchable, verbatim:

> "Hevner et al. (2004) establish three foundational cycles of DSR activity: the relevance cycle, which connects the research to a real-world problem in a specific application domain; the design cycle, which iterates between construction and evaluation of the artefact; and the rigor cycle, which grounds the design in existing knowledge bases, specifically the academic literature reviewed in Chapter 2."

**The sentence after it reads:**
> "This thesis explicitly engages all three cycles."

### ⚠ Action depends on one library check

**`Hevner (2007)` is NOT in the library.** The only Hevner item is
`hevner_design_2004`. So there are two routes, and the second needs no new source:

#### Option A — add Hevner (2007) to Zotero, then paste

> "Hevner et al. (2004) establish the framework within which design science research operates, connecting the application environment, the research activity and the knowledge base; Hevner (2007) formalises the relationships between them as three cycles. The relevance cycle connects the research to a real-world problem in a specific application domain, the design cycle iterates between construction and evaluation of the artefact, and the rigor cycle grounds the design in existing knowledge bases, specifically the academic literature reviewed in Chapter 2."

#### Option B — ⚠ recommended, no new source needed

Keep the cycles but stop attributing the *terminology* to the 2004 paper:

> "The framework Hevner et al. (2004) establish connects three elements: the application environment that makes the research relevant, the design activity itself, and the knowledge base that grounds it in prior work. This thesis engages all three. Relevance is established through the collaboration with Manifold AI, whose operational need to extend a non-predictive, production-oriented agentic system with forecast-informed decision-support defines the problem that the artefact addresses. The design activity is the iterative development, testing and refinement of the predictive-extension architecture across Chapters 5 through 8. Rigor is grounded in the systematic literature review in Chapter 2."

⚠ **Option B replaces the following three sentences too**, because they open
*"The relevance cycle is established through..."* and must match. The full span
to replace runs from *"Hevner et al. (2004) establish three foundational..."* to
*"...the systematic literature review in Chapter 2, which identifies the
theoretical and empirical foundations on which the framework design is built."*

**My recommendation: Option B.** It is accurate, needs no source we do not have,
and loses nothing — the chapter never depends on the word "cycle".

---

# F2 — §3.1, "modest realism" ❌ REJECTED

**NotebookLM proposes** replacing *"the thesis adopts a modest realism about the
business realities it studies"* with *"the thesis views business realities as
existing independently but accessible only through partial, tool-mediated
measurement instruments (Saunders et al., 2023)"*, on the grounds that Saunders
classifies ontology as Objectivism / Realism / Subjectivism and does not use the
phrase "modest realism".

❌ **Reject, for two reasons.**

**First, the replacement says the same thing at greater length.** The existing
sentence already continues: *"demand patterns, consumer preferences, and
retailer-level sales dynamics are taken to exist independently of the researcher
yet are known only through measurement instruments that carry their own
assumptions and limitations"*. That **is** "existing independently but accessible
only through partial, tool-mediated measurement instruments" — the chapter states
it, then elaborates it, and NotebookLM's version deletes the elaboration to
restate the summary.

**Second, a term not appearing in a source is not an error.** The citation
supports the *position*, which Saunders' realism category covers; "modest" is the
thesis's own qualifier, signalling that it is not committing to full critical
realism. That is a deliberate philosophical hedge and it is defensible.

⚠ **If you want to be safe against a methodology examiner**, the cheaper fix is
to move the citation rather than rewrite the sentence — put `(Saunders et al.,
2023)` after "independently of the researcher" so it attaches to the ontological
claim rather than to the phrase "modest realism". **One citation moved, no prose
lost.** I would do that only if you think it is worth the risk; my view is the
sentence is fine as it stands.

✅ **Saunders is in the library:** `XH475DIR`, *Research Methods for Business
Students*, 9th ed.

---

# Confirmed, no action — eleven items

| ID | Citation | Claim | Library |
|---|---|---|---|
| CIT-001 | Saunders et al. (2023) | pragmatism, knowledge judged by practical consequences | ✅ `XH475DIR` |
| CIT-004 | Peffers et al. (2007) | six-activity DSR process model | ✅ `2MVL956G` |
| CIT-005 | Saunders et al. (2023) | secondary data advantage | ✅ `XH475DIR` |
| CIT-006 | Akiba et al. (2019) | Optuna / TPE | ✅ `8CITVHH2` |
| CIT-007 | Klee and Xia (2025) | CV across runs as stability metric | ✅ `UXPL266D` |
| CIT-008 | Lei et al. (2018) | split conformal on held-out residuals | ✅ `UHZWB269` |
| CIT-009 | Ahrens et al. (2024) | inverse-MAPE weighting "in the spirit of" | ✅ `I86QMNYE` ⚠ see below |
| CIT-010a | Ouyang et al. (2025) | code non-determinism | ✅ |
| CIT-010b | Atıl et al. (2025) | persists at temperature zero | ✅ |
| CIT-011 | Schwartz et al. (2020) | cost as first-class criterion | ✅ |
| CIT-012 | Chen et al. (2024) | inference cost orders of magnitude | ✅ |
| CIT-013 | Mehta (2025) | CLEAR multidimensional frame | ✅ |

⚠ **CIT-009 carries a year inconsistency NotebookLM did not flag.** Ch3 §3.5.2
cites **Ahrens et al. (2024)**; Ch2 §2.1 cites the same paper as **Ahrens et al.
(2025)**, and the library key is `ahrens_model_2025`. **One of the two chapters
is wrong.** Ch2's 2025 matches the library, so **Ch3 §3.5.2 should probably read
2025** — but I have not confirmed the publication year against the journal, so
this is a flag, not a fix.

→ Recorded as a register row below.

---

# ⚠ Still outstanding in this chapter — not from NotebookLM

**The temperature contradiction is unapplied.** §3.6 still reads *"outputs at
temperature zero are highly reproducible"*, ten lines after §3.5.4 correctly says
decoding is not adjustable on this model. The fix is written and ready in
`2026-09-15_BRANCH_A_ch3-temperature-contradiction.md`.

**Also unapplied from the consolidated note:** F6, §3.6's *"all five forecasting
models"* → *"all six"*.

⚠ **Both sit in §3.6, in adjacent paragraphs.** Apply them in one visit.

---

# Chapter rename — not recommended

*"Chapter 3 | Methodology"* with *"How the artefact was built, and how it was
judged"* is exact and needs no change. ✅

---

# For the registers

## `citations-added-register.md`

**No citations added** unless you take F1 Option A, which would add Hevner (2007).
If you do, register it with the claim *"the relevance, design and rigor cycles"*.

## Claims register

| Claim | Where | To verify |
|---|---|---|
| Ahrens model-averaging paper year | Ch3 §3.5.2 says 2024, Ch2 §2.1 says 2025 | **Which is the publication year?** Library key says 2025. Align both |
| The three-cycle attribution | Ch3 §3.2 | **Resolved by F1** — either add Hevner (2007) or take Option B |
