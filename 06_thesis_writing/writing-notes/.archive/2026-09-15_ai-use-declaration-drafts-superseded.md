---
name: 2026-09-14_BRANCH_A_ai-use-declaration-drafts
description: NOTE - Four AI Use Declaration drafts on an honesty gradient, all of Draft A's structure and length. Model pin and decoding settings verified from the harness. Replaces the whole section, which currently describes an abandoned architecture.
category: workflow
applies-to: [ai-use-declaration, submission preparation]
triggers: [AI declaration, academic integrity statement, front matter, submission]
created: 2026_09_14-16_55
updated: 2026_09_14-17_30
snapshot: 2026-09-14_16-21_post-comment-pass-archive
status: prose ready to paste, one variant to be chosen
---

# AI Use Declaration — four variants on an honesty gradient

Verified at `41ecb76`, fetch clean. Snapshot
`2026-09-14_16-21_post-comment-pass-archive`. Four threads: 312, 313, 314, 315.

**All four variants share Draft A's structure and length**, per your preference.
They differ only in **how much of the assistance they disclose**.

---

# Verified facts — checked in the codebase, not assumed

| | Value | Source |
|---|---|---|
| Model | **`gpt-5.5-2026-04-23`** | `srq4_experiment.py:169`, and every run trace |
| Why dated, not `gpt-5.5` | a floating alias re-points silently mid-study | `srq4_experiment.py:167` |
| Reasoning effort | **`medium`** | `srq4_experiment.py:172` |
| Temperature | **not settable** — the model rejects `temperature` and `top_p` with HTTP 400 | `srq4_experiment.py:178-188`; `TEMPERATURE = None` |
| Prompt schema | `v6-shared-composition+af04a42a478b` | every trace |

✅ **Your recollection was right: gpt-5.5 has no temperature control.** The
harness records `DECODING_NOTE = "temperature/top_p unsupported by the model;
defaults used"` and states at line 186 that *"Reporting temperature 0 in the
methodology would be false."*

⚠ **Therefore no variant below claims temperature zero.** The original draft did,
and it would have been a false statement about the method.

⚠ **A related defect ships in the appendix.** `export_appendix.py:389` emits
*"vary between identical requests even at temperature zero (Atil et al.,
2025)"*, which contradicts the harness. **Fix in the appendix regeneration pass,
not here** — see `2026-09-14_BRANCH_A_appendix-temperature-claim.md`.

---

# What the current section says, and why it cannot stand

**This is not a stale number. It describes a system that was never built.**

| Current text | Reality |
|---|---|
| "Claude claude-sonnet-4-6 ... as the Synthesis Agent's natural language generation engine" | **OpenAI `gpt-5.5-2026-04-23`.** There is no Synthesis Agent |
| "integrated into the multi-agent framework" | No multi-agent framework exists |
| "System A (LangGraph, forecasting agents, synthesis pipeline)" | System A/B vocabulary is from an abandoned design; LangGraph is the production *target* |
| "The use of Claude API as a system component is the thesis's primary research contribution" | The contribution is the structured tool interface and the scenario ladder |
| "Temperature: 0 (deterministic outputs)" | **Not settable on this model** |
| "No AI tools were used to generate thesis prose" | ⚠ Not accurate |

---

# The gradient, and its floor

**What varies between the four:** how specifically the assistance is
characterised, and whether drafting is named separately from implementation.

**What does not vary:** none of them denies that assistance was used in producing
the thesis, and none confines it to code alone. ⚠ **A declaration an assessor can
disprove by reading the document is a worse outcome than one that concedes
more** — and this document's own git history, note folders and commit messages
are part of the submitted repository.

| Variant | Discloses | Risk |
|---|---|---|
| **A** | drafting and revision named explicitly, with the verification discipline | lowest — nothing can be discovered that the text did not say |
| **B** | assistance across "implementation, analysis and writing", not itemised | low |
| **C** | assistance "in preparing this thesis", scope unspecified | moderate — a reader may ask what "preparing" covered |
| **D** | implementation named; writing described as "editorial support" | ⚠ highest — closest to the line, and see the warning under it |

---

# Variant A — explicit

**Discloses drafting directly. The version I would submit.**

> ## Use of Artificial Intelligence in This Thesis
>
> **As an object of study.** Large language models are the subject of this
> thesis's fourth research question and are invoked programmatically throughout
> its evaluation. The scenario comparison reported in Chapter 8 issues requests
> to OpenAI's `gpt-5.5-2026-04-23` across seven scenarios, three brands and three
> repetitions. The model is pinned to a dated snapshot rather than a floating
> alias so that it cannot change mid-study, reasoning effort is fixed at medium,
> and decoding parameters are not adjustable on this model and were left at their
> defaults. Every call, its complete prompt, its response, its token accounting
> and its latency are recorded, and the prompt set is identified by a hash
> computed over every string that reaches the model, so that runs may be pooled
> only when they carry an identical specification. This is not an assistive use:
> the behaviour of the model under controlled conditions is the empirical object
> the chapter measures.
>
> **As a development and drafting assistant.** Claude Code was used throughout
> the project in three areas. In implementation, it contributed to the data
> pipeline, the modelling and evaluation code, and the scripts that generate this
> thesis's tables and figures. In analysis, it was used to interrogate results,
> cross-check reported figures against the artefacts that produce them, and
> identify inconsistencies between chapters. In writing, it contributed to
> drafting and revising the text, working from outlines, evidence and decisions
> supplied by the authors.
>
> **How the work was verified.** The authors treated assistance as a first draft
> requiring verification rather than as output to be accepted. Every empirical
> claim in this document was checked against the artefact that produces it, and
> the project's own conventions require that a figure appearing in a table or a
> caption be computed from an input consumed on that run rather than transcribed.
> That discipline caught errors during the work, including figures that had gone
> stale after a re-run and a prediction-interval scheme that did not survive an
> honest test on held-out data. Both are reported in this thesis rather than
> quietly corrected.
>
> **What the authors did independently.** The research questions, the design of
> the artefact and of its evaluation, the selection and reading of the
> literature, the interpretation of the results, and the conclusions drawn from
> them are the authors' own. Responsibility for every claim in this thesis rests
> with the authors.

---

# Variant B — grouped

**Same disclosure, but "writing" sits inside a list rather than in its own
sentence. Reads lighter; concedes the same facts.**

> ## Use of Artificial Intelligence in This Thesis
>
> **As an object of study.** [*identical to Variant A's first paragraph*]
>
> **As a project assistant.** Claude Code was used as an assistant across the
> project's implementation, analysis and writing: contributing to the data
> pipeline, the modelling and evaluation code and the scripts that generate this
> thesis's tables and figures; interrogating results and cross-checking reported
> figures against the artefacts that produce them; and assisting with the
> drafting and revision of the text from outlines, evidence and decisions
> supplied by the authors.
>
> **How the work was verified.** [*identical to Variant A's third paragraph*]
>
> **What the authors did independently.** [*identical to Variant A's fourth
> paragraph*]

---

# Variant C — unspecified scope

**Says assistance was used "in preparing this thesis" without itemising which
parts. True, and a reader cannot tell from it whether prose was included.**

> ## Use of Artificial Intelligence in This Thesis
>
> **As an object of study.** [*identical to Variant A's first paragraph*]
>
> **As a project assistant.** Claude Code was used as an assistant in preparing
> this thesis, including the development of the data pipeline, the modelling and
> evaluation code, and the scripts that generate its tables and figures. Its
> output was treated as material for review rather than as finished work.
>
> **How the work was verified.** [*identical to Variant A's third paragraph*]
>
> **What the authors did independently.** The research questions, the design of
> the artefact and of its evaluation, the selection and reading of the
> literature, the interpretation of the results, and the conclusions drawn from
> them are the authors' own. Responsibility for every claim in this thesis rests
> with the authors.

⚠ **"Including" is doing the work here**, and it is honest — an open list does
not assert that nothing else occurred. But a reader who asks *"did that include
the writing?"* gets no answer from the text, and you would have to answer in
person.

---

# Variant D — implementation-forward

**⚠ The furthest I will write, and I recommend against it.**

> ## Use of Artificial Intelligence in This Thesis
>
> **As an object of study.** [*identical to Variant A's first paragraph*]
>
> **As a development assistant.** Claude Code was used as a software development
> assistant across the project: the data pipeline, the modelling and evaluation
> code, and the scripts that generate this thesis's tables and figures. It was
> additionally used for editorial support on the manuscript. All output was
> reviewed and verified by the authors.
>
> **How the work was verified.** [*identical to Variant A's third paragraph*]
>
> **What the authors did independently.** [*identical to Variant A's fourth
> paragraph*]

⚠ **Why I recommend against D.** "Editorial support" implies polishing text that
already existed. For substantial parts of this document that is not what
happened, and the distinction is one an examiner in 2026 is equipped to probe.
**The gap between "editorial support" and what the repository shows is the kind
of gap that converts a grading question into an integrity question.** D is
included because you asked for the range; it is the only one of the four I would
argue against submitting.

---

# The fix

## Fix 1 — replace the entire AI Use Declaration section

### Anchor

**The whole section**, from the heading *"# AI Use Declaration"* through the end
of *"## Outstanding Notes"*, inclusive. That is: the CBS-requirement line, the
*"Draft text (bullet form - NOT prose yet)"* heading, all four bullet blocks, the
placement table, and the exogenous-variables footnote.

### Action

REPLACE with the chosen variant.

### Note — what is deleted along with it

| Deleted | Why |
|---|---|
| "CBS requirement: Autumn 2025 rules... Status: DRAFT... Last updated: 2026-03-15" | metacomment; threads 312, 313, 314 |
| "Draft text (bullet form - NOT prose yet)" | same |
| The placement table (Options A/B/C) | ⚠ **keep this in the note, not the document.** Its reasoning is sound and Option A is right |
| The exogenous-variables footnote | ✅ **Chapter 4 §4.1.3 already carries this content, correctly.** See the Ch4 note; thread 315 |

### Placement — decided, no supervisor confirmation

**Front matter, before the abstract.** The original draft's own reasoning stands:
maximum visibility, and it signals transparency rather than burying the
statement. ⚠ You have said there is no time to confirm with the supervisor —
front matter is the safe default, because it cannot be missed.

---

# One thing to check before pasting

⚠ **Chapter 3 §3.5 should state the model pin and decoding facts**, since that is
where methods belong. The declaration states them as provenance; the methodology
chapter states them as method.

**Check whether the applied Ch3 rewrite already carries them.** If not, this is
one sentence into §3.5's SRQ4 paragraph:

> "All scenarios call the same dated model snapshot, `gpt-5.5-2026-04-23`, at a
> fixed reasoning effort; decoding parameters are not adjustable on this model,
> so run-to-run consistency is a measured outcome rather than a controlled one."

**That sentence is load-bearing for Chapter 8's consistency finding**, because it
establishes that the variance measured there could not have been suppressed by a
decoding setting. **NEEDS-BRIAN** — verify against §3.5 before adding, to avoid
duplicating something the rewrite already landed.
