---
name: review-method-and-improvement-questions
description: What the NotebookLM verification runs do and do not cover, why, and the per-section improvement questions that close the gap — without adding papers.
created: 2026_08_25-12_30
updated: 2026_08_25-12_30
---

# The review method, and what it deliberately leaves out

## What the runs so far actually did

Both completed runs — **01-Literature_Review** and **03-Modelling_Review** — asked one
question of every claim:

> *Does the cited source say what the thesis says it says?*

This is **verification**, and it is a closed test. Every question has a determinate
answer, the answer comes from a PDF already in the corpus, and no new source can change
it. That is exactly why it worked: 36 papers, 37 claims, five Contradicted findings, and
each finding was actionable the moment it arrived.

**What it structurally cannot do:**

| Not covered | Why not |
|---|---|
| Claims with **no** citation | Nothing to check them against. A wrong-but-uncited sentence passes silently |
| Whether a **better** source exists | The corpus is the universe of the test |
| Whether an argument is **complete** | Verification checks the links present, not the ones missing |
| Whether the **framing** is right | A perfectly-sourced paragraph can be answering the wrong question |

The Kuleshov finding (LR-31) is the proof. NotebookLM was asked whether Kuleshov supports
the calibration claim. Answering that honestly forced it to note Kuleshov is *not*
conformal prediction — which revealed §2.5 had **no conformal literature at all** while
the artefact serves conformal intervals. That gap was found as a *side effect*, not
because it was asked for. Relying on side effects to find gaps is not a method.

## Did the corrections use NotebookLM's suggested wording?

**Partly, and deliberately so.** Each report ends with a "Safest Thesis-Ready Wording"
block. I treated those as *evidence about what the source supports*, not as drop-in prose:

- **Where I followed them closely:** the factual content. Ceran's WRMSSE 0.83/0.81, M4's
  exclusion of intermittent series, Goodwin's 83.8%→44.1%, ANAH's four categories, Levi's
  MLP/DenseNet scope. These are the source's facts and I had no licence to vary them.
- **Where I diverged:** the argumentative work. NotebookLM's suggestions are written as
  standalone LaTeX paragraphs, in a heavier register than the chapter's, and they do not
  know what the surrounding sentences need to do. The Goodwin rewrite is the clearest
  case — NotebookLM's version reports the negative finding correctly and stops. The
  chapter needed the finding to then *do something*, because the original sentence was
  load-bearing for the whole uncertainty-communication design. So the correction reports
  the finding and adds the paragraph turning it into an argument **for** the interpretive
  layer.
- **Where I rejected them:** anything that would have imported a citation the thesis does
  not hold, or that asserted more than the audit verified.

## The gap this leaves, and how to close it without adding papers

You are right that the next round should be **improvement questions per section**, not
more verification. Below is that pack. Every question is designed to be answerable from
**sources already in the corpus** plus the chapter drafts — so the expected output is
*better use of what we have*, not a reading list.

Where a question genuinely cannot be answered from the corpus, the correct output is a
**one-line statement of what is missing**, so you can decide whether it is worth one
targeted download. That keeps new-paper decisions explicit and rare rather than
open-ended.

---

# Improvement questions by section

**How to run these.** Upload the same PDFs as the corresponding verification run, plus
the current chapter draft. Ask for prose answers, not tables — the value is in the
reasoning.

**Standing instruction for every question below:**

> Answer only from the uploaded sources and the chapter draft. Where the corpus cannot
> support an answer, say **"corpus gap: <one line on what kind of source would settle
> it>"** and stop. Do not speculate, and do not recommend literature you cannot see.

---

## §2.1 Forecasting substrate

1. **Is the model set justified, or merely listed?** The chapter names ARIMA, Prophet,
   LightGBM, XGBoost, Ridge as spanning "the accuracy–efficiency trade-off frontier."
   Does the corpus actually support that framing, or is it asserted? Which uploaded
   source most directly justifies *each* inclusion, and is there a model in the set that
   no source justifies?
2. **The pooled-vs-per-category question now rests on M5's cross-learning finding.** Is
   that the strongest support in the corpus, or is there a better one? Does any source
   state the *condition* under which pooling wins — which is what Ch6 actually found
   (data volume)?
3. **Ceran now serves a different purpose** after the correction: the zero-inflation
   metric problem rather than an accuracy target. Is that use fully supported, and does
   any *other* corpus source corroborate the zero-inflation problem in retail panels?
4. **What claim in §2.1 has no citation at all?** List them. For each, say whether the
   corpus can support it or whether it is a corpus gap.

## §2.2 Resource constraints

5. **Ng (2017) is doing heavy lifting alone.** The section distinguishes Ng's raw-data
   constraint from the thesis's deployment-cost constraint — a distinction the thesis
   makes, not Ng. Is that distinction defensible from the source, and is there corpus
   support for the *deployment-cost* half, or does it rest on Liu/Semerikov alone?
6. **The 8GB budget is asserted as the SME envelope.** Does anything in the corpus
   justify that specific figure, or is it a design choice presented as a finding? If the
   latter, how should the sentence be framed so the distinction is honest?

## §2.3 Decision support

7. **The Goodwin correction changed this section's argument.** Read the rewritten §2.3.
   Does the argument now hold together — does the corpus support the claim that an
   *interpretive layer* addresses what bare intervals failed to? Or is that step
   currently unsupported and stated as though it were established?
8. **Elmachtoub/Mandi are tight-coupling; the thesis is loose-coupling.** The chapter
   says the tight-coupling literature "motivates the principle but does not address" the
   loose case. Is there anything in the corpus on loosely-coupled or human-in-the-loop
   forecast-to-decision? If nothing: corpus gap, and say what would fill it.

## §2.4 Agents and tool use

9. **Toolformer is the load-bearing citation for "tool delegation substitutes for
   scale."** Is that claim as strong as the chapter needs? Do SciAgent or CodeAct
   corroborate it, or is the chapter over-reading a single result?
10. **The chapter positions its artefact as a "bounded tool-using AI agent" under
    Sapkota's taxonomy.** Is that self-classification correct given what the artefact
    does? Would Sapkota classify it the same way?

## §2.5 Reliability and evaluation

11. **The conformal strand is newly added.** Does it now sit coherently with the
    recalibration strand, or do the two read as competing? Is the relationship between
    them stated as the sources support it?
12. **§2.5 cites Ouyang, Atıl, Schwartz, Chen with no PDFs in the corpus.** Flag each as
    unverifiable and state what the claim would need. *(These are the known second-round
    downloads.)*
13. **The consistency dimension rests on two preprints.** Is that a material weakness for
    a dimension the evaluation treats as primary, and is there peer-reviewed corpus
    support to lean on instead?

## §2.6–2.7 Production systems and the gap

14. **The gap statement rests on four strands being jointly under-addressed.** Test it
    adversarially: taking the corpus as given, can you construct an argument that the
    gap is *narrower* than claimed — that some uploaded paper covers more of the
    intersection than the thesis credits? This is the examiner's move; better we hear it
    now.
15. **González-Potes is the closest exemplar and its limitations are now stated as the
    thesis's observations, not the authors'.** Is the distinction drawn accurately, and
    is the gap still intact once stated honestly?

## Ch6 modelling (use the 03-Modelling_Review corpus)

16. **Two of four categories are beaten by simple benchmarks.** Does the corpus support
    the chapter's handling of this — reporting it as the headline result rather than
    burying it? Is there source guidance on how to report a negative benchmark result?
17. **The tuning protocol is not nested and the chapter says so.** Does the corpus
    quantify what that costs, or only that it biases? Can the chapter say more than
    "unquantifiable"?
18. **The winner flips across seeds in all four categories.** Is the chapter's conclusion
    — that the models are statistically indistinguishable — the right one under the
    corpus, or is there a stronger/weaker claim the sources support?
19. **The accuracy target was just withdrawn.** With no external target, is the
    simple-benchmark comparison a sufficient accuracy criterion by the corpus's
    standards, or does something else need to fill the gap?

---

# What to do with the answers

Expect three kinds, and route them differently:

| Answer type | Route |
|---|---|
| "The corpus supports a stronger/more precise claim" | Rewrite the sentence — free improvement |
| "This claim has no support in the corpus" | Either soften to a design choice, or accept a targeted download |
| "corpus gap: <X>" | Add to a single consolidated download list; decide in one batch, not one at a time |

The third column is the discipline that keeps this from becoming an open-ended literature
hunt. **One batch decision at the end, not a paper per question.**
