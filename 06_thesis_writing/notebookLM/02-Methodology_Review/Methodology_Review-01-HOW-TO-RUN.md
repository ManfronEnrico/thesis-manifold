---
name: methodology-review-how-to-run
description: Operating procedure for the Ch3/Ch4 methodology verification run — what to upload, in what order to ask, how to handle each verdict class, and what NOT to paste back.
created: 2026_08_25-14_00
updated: 2026_08_25-14_00
---

# How to run the methodology review

Companion to `Methodology_Review-00-MASTER-verification-brief.md`. That file is **what to
check**; this file is **how to run it and what to do with the answers**.

Read this once before starting. The two things most likely to cost you a rerun are in
§1 (what goes in the notebook) and §5 (what not to paste back).

---

## 1. Notebook setup — keep it clean

**Upload exactly this, and nothing else:**

| # | What | From |
|---|---|---|
| 1 | 14 Saunders chapter PDFs | `Methdology Book Chapters/` |
| 2 | `ch3-methodology.md` | `05_thesis_writing/sections-drafts/` |
| 3 | `ch4-data-assessment.md` | `05_thesis_writing/sections-drafts/` |
| 4 | `Methodology_Review-00-MASTER-verification-brief.md` | this folder |

**Do not add to this notebook:**

- **Max's Grade 12 thesis.** It is not a source — it is a worked example of Saunders
  applied to a different design. If its prose is in the retrieval pool, a question like
  *"what does Saunders say about embedded case studies?"* can return **Max's reading of
  Saunders** presented as Saunders. That is precisely the failure class this whole
  exercise exists to catch. Separate notebook, different questions, later.
- **The literature-review or modelling PDFs.** Different corpus, different run. Mixing
  them dilutes retrieval on the Saunders chapters.
- **Other thesis chapters.** Ch3 and Ch4 are the Saunders-dependent ones. Adding Ch6 or
  Ch8 gives the model more prose to search and no more evidence.

**Why all 14 Saunders chapters and not just the obviously relevant ones.** Several claims
route to chapters you would not guess: MR-04/05/06 need Ch 3 (reviewing the literature),
MR-10 needs Ch 6 (ethics), MR-12–19 need Ch 8 (secondary data). Uploading the whole book
costs nothing and prevents a "Not Addressed" verdict that only means *you did not upload
the chapter that addresses it*.

---

## 2. Ask in this order

Do **not** paste the whole brief and ask for everything at once. The completed runs show
quality degrades across a long batch — later claims get thinner quotes. Work in blocks,
one message each.

| Order | Block | Why here |
|---|---|---|
| 1 | **MR-01, MR-02, MR-03** (Part 1) | The three structural labels. If any is wrong, the fix is architectural. Everything downstream is cheaper to interpret once these are settled |
| 2 | **Part 4 — the coherence read** | Highest-value single output of the run. Needs Part 1's answers to be meaningful |
| 3 | **MR-12, MR-13, MR-14** | Ch4's framework spine — the three-stage evaluation the whole chapter is built on |
| 4 | **MR-15 – MR-19** | Rest of Ch4 |
| 5 | **MR-04 – MR-11** | Ch3 remainder, including the two missing onion layers |

For each block, paste the relevant section of the brief verbatim, including the **YOUR
TASK** format block and the four rules. Repeating the rules per message is deliberate —
they are what keeps the verdicts disciplined.

---

## 3. What a good answer looks like

Every claim must come back with all five fields:

```
### MR-02 — single-case embedded study
**Verdict:** Contradicted
**Source location:** Ch 5, "Case study", p. NNN
**Verbatim quote:** "<exact words>"
**Analysis:** <where the thesis diverges>
**Safest thesis-ready wording:** <replacement>
```

**Push back and re-ask if you see any of these:**

| Symptom | What it means | What to say |
|---|---|---|
| Paraphrase where a quote belongs | It has not located the passage | "Quote the passage verbatim, with page number, or answer Cannot Verify" |
| A page number with no quote | Same | Same |
| Confident verdict, vague location | It is reasoning from general knowledge of Saunders, not from the PDF | "Which uploaded chapter and page? Quote it." |
| It cites Ch3/Ch4 (your own draft) as evidence | Circular — your draft cannot verify your draft | "Evidence must come from the Saunders PDFs only" |
| Every verdict is Supported | Almost certainly not reading critically | Re-ask MR-01 and MR-02 specifically; those two have real problems |

The last one deserves emphasis. The literature run returned **five Contradicted** out of
37. A methodology run that returns zero problems across 19 claims is not good news — it
is a signal the run did not work.

---

## 4. Handling each verdict

| Verdict | What it means here | Action |
|---|---|---|
| **Supported** | Saunders says it, the thesis uses the term as he defines it | Nothing. Optionally tighten wording using his phrasing |
| **Partially Supported / Qualified** | Right idea, imprecise term or overstated scope | Narrow the sentence to what the quote supports |
| **Contradicted** | The thesis uses a term Saunders defines differently | **Stop and assess blast radius before editing.** See below |
| **Not Addressed** | Saunders does not cover it | Legitimate and expected — DSR, CBS taxonomy, pre-registration. Reattribute to the correct source or state it as the thesis's own choice |
| **Cannot Verify** | Could not locate it | Check the chapter is uploaded, then re-ask once. If still unresolved, record as unverified rather than assuming either way |

### Contradicted on MR-01/02/03 — assess before editing

These three are not sentence-level. Before touching prose, answer:

1. **Where else does the wrong term appear?** `grep -rn "explanatory\|embedded\|pragmat"
   05_thesis_writing/sections-drafts/` — the label may be repeated in Ch1, Ch9 or the
   abstract.
2. **Does anything downstream depend on it?** If the design is evaluative rather than
   explanatory, does §3.6's validity discussion still fit?
3. **Is it one edit or a section rewrite?** Decide, then do it once.

The Ceran finding is the precedent: one Contradicted verdict removed a criterion that
Ch6, Ch9 and Ch10 all measured against. Cascades are normal here — check for them first.

---

## 5. What to do with "Safest thesis-ready wording" — read this before pasting

**Take the facts verbatim. Rewrite the argument yourself.**

The suggested-wording blocks are useful, and they are also the single place where this
workflow can quietly damage the chapter. Three rules:

**Do take the facts.** Definitions, page-anchored terminology, the exact distinction
between Saunders' categories. These are the source's and you have no licence to vary
them.

**Do not paste the paragraph.** The blocks come back as standalone LaTeX in a heavier
register than your chapters, and — this is the real problem — **they cannot see what the
surrounding sentences need the corrected sentence to do.**

The precedent is Goodwin (LR-13) in the literature run. NotebookLM's suggestion reported
the negative finding accurately and stopped. But that sentence was load-bearing: it was
the evidence that communicating uncertainty pays off, which motivated the entire
interval-serving design. Pasting the suggestion would have left a correct sentence
sitting in a hole where an argument used to be. The applied correction reported the
finding **and** added the paragraph turning it into an argument *for* the interpretive
layer — which is a stronger position than the thesis had before.

**Do not adopt its hedging as a default.** "Defensive academic hedging" applied
indiscriminately makes a chapter read as though it is unsure of itself. Hedge where the
evidence is genuinely thin; state plainly where it is not.

### The claim this workflow cannot support

You will see the phrase *"pre-defended against critique"* used about this process. It
overstates what verification does. Verification makes claims **accurate**. It does not
make an argument **good**, and an examiner attacks the argument. A chapter can be
flawlessly sourced and still fail on coherence — which is exactly why Part 4 of the brief
exists and why it is second in the running order rather than last.

---

## 6. Filing the output

Match the naming convention the completed runs use, so all three reviews stay browsable
together:

```
02-Methodology_Review/NLM Review/Methodology_Review-Section_A-<topic>.md
```

Suggested split, following how the literature run divided:

| File | Covers |
|---|---|
| `Section_A-research_design_labels.md` | MR-01, MR-02, MR-03 |
| `Section_B-onion_coherence.md` | Part 4 |
| `Section_C-secondary_data_framework.md` | MR-12 – MR-19 |
| `Section_D-ch3_remainder.md` | MR-04 – MR-11 |

---

## 7. What this run does not cover

State these as out of scope rather than working around them:

- **The 10 repo fixes (S1–S10 in the brief) need no PDF.** They are known now, and none
  is actioned. S5 (Ch3 still *specifies* the dropped LLM judge) and S9 (brand × retailer
  grain, contradicting DEC-GRAIN) are the two that would actively mislead an examiner.
  **Fold them into the same edit as this run's findings** — one pass over Ch3, not two.
- **Claims with no citation at all.** A claim register is built from claims that *have*
  sources; a factual sentence with nothing behind it never enters one. Closing that gap
  is the improvement round's job — see
  `../00-REVIEW-METHOD-and-improvement-questions.md`.
- **Whether DSR is acceptable to the supervisor** (open item OI-03) and anything
  attributed to "the CBS taxonomy" or "CBS case study guidelines." Saunders cannot settle
  institutional questions. Flag for separate checking.

---

## 8. Done when

- [ ] All 19 MR claims have a verdict with a verbatim quote and page reference
- [ ] Part 4 coherence read returned, with the three missing onion layers filled in
- [ ] Any Contradicted verdict on MR-01/02/03 has had its blast radius checked by grep
- [ ] Reports filed under `NLM Review/` using the naming convention above
- [ ] Ch3 and Ch4 edited in **one** pass combining this run's findings with S1–S10
- [ ] `python 05_thesis_writing/check_chapter_facts.py` re-run; Ch3's 10 items reduced
- [ ] Findings summarised at the top of the master brief, as the literature brief records
      its own outcome

---

## Related

- `Methodology_Review-00-MASTER-verification-brief.md` — the claims themselves
- `../00-REVIEW-METHOD-and-improvement-questions.md` — what verification structurally cannot find, and the improvement round that follows
- `../01-Literature_Review/NLM Review/` — completed run; the precedent for format and for what a Contradicted cascade looks like
- `plans/P0042_.../task_plan.md` — where this sits in the funded-phase sequence (workstream A, task A1)
