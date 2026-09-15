---
name: 2026-09-15_BRANCH_A_ai-declaration-variant-D-final
description: FINAL - Variant D of the AI Use Declaration, reworded against the CBS GenAI guidelines. Uses the four permitted-use categories as its structure, places the writing-process declaration in the Methodology as CBS requires, and states the GDPR position. Paste-ready.
category: workflow
applies-to: [ai-use-declaration, ch3_methodology, submission preparation]
triggers: [AI declaration, GenAI, academic integrity statement, front matter, submission]
created: 2026_09_15-00_45
updated: 2026_09_15-10_35
snapshot: 2026-09-15_10-29_post-sku-abstract
status: prose ready to paste
---

# AI Use Declaration — Variant D, reworded to the CBS guidelines

Verified at `37a04f0`, fetch clean. Snapshot `2026-09-15_10-29_post-sku-abstract`
(46,667 words, 28 comments in 22 threads). Zotero: 92 items. Threads **298** and
**299**.

**This replaces the version written at 00:45.** Same disclosure level — Variant D
— but restructured so it answers the CBS guidelines point by point.

---

# What the CBS guidelines change

**The guidelines are more permissive than the earlier drafting assumed, and more
specific about placement.** Reading them changes three things.

| CBS says | Consequence for the declaration |
|---|---|
| Four uses are **acceptable**: language assistant, search engine, idea generation and conceptualisation, and generating content **with a specific reference** | ⚠ **The declaration should name the guidelines' own categories.** An assessor checking compliance is checking against this list, so matching its vocabulary makes compliance visible rather than inferred |
| Declare idea-generation and writing-process use **in the Methods section**, or the Introduction if there is none | ⚠ **A front-matter declaration alone does not satisfy this.** The thesis has a Methodology chapter, so a short declaration belongs in **Chapter 3** — see F2 below |
| Spell-check and search-engine use need **no** declaration | Nothing to add; declaring more than required is not penalised |
| Generated content in the final product needs a **specific reference** | ⚠ **This is the one to be careful about** — see the note at the end |
| Never input personal, confidential or proprietary data | ⚠ **This thesis uses licensed commercial data under an NDA.** Stating the boundary is a strength, and the repository enforces it |
| Readers must be able to distinguish own contributions from GenAI contributions | The verification paragraph does this work |

✅ **"Editorial support" survives the guidelines comfortably.** It sits inside
"language assistant", which CBS compares to Word's spell-check and Grammarly and
which needs no declaration at all. Declaring it anyway is the safer side of the
line.

---

# The declaration

### Anchor

**The whole section**, from the heading *"# AI Use Declaration"* through the end
of *"## Outstanding Notes"*, inclusive. That is: the CBS-requirement line, the
*"Draft text (bullet form - NOT prose yet)"* heading, all four bullet blocks, the
placement table, and the exogenous-variables footnote.

### Action

REPLACE.

#### Replace with

> ## Use of Artificial Intelligence in This Thesis
>
> This declaration follows the CBS guidelines on the use of generative AI in
> final projects.
>
> **As an object of study.** Large language models are the subject of this
> thesis's fourth research question and are invoked programmatically throughout
> its evaluation. The scenario comparison reported in Chapter 8 issues requests to
> OpenAI's `gpt-5.5-2026-04-23` across seven scenarios, three brands and three
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
> **As a development assistant.** Claude Code was used as a software development
> assistant across the project: the data pipeline, the modelling and evaluation
> code, and the scripts that generate this thesis's tables and figures. Every
> figure and table in this document is produced by a script the authors wrote and
> reviewed, and the project's conventions require that any figure appearing in a
> table or caption be computed from an input consumed on that run rather than
> transcribed.
>
> **As a language assistant, and for structuring and conceptualisation.**
> Generative AI was used in the writing process for editorial support on the
> manuscript and to discuss the organisation of arguments and the structure of
> chapters. Its role in the writing process is described further in Section 3.8.
>
> **How the work was verified.** The authors treated assistance as a first draft
> requiring verification rather than as output to be accepted. Every empirical
> claim in this document was checked against the artefact that produces it. That
> discipline caught errors during the work, including figures that had gone stale
> after a re-run and a prediction-interval scheme that did not survive an honest
> test on held-out data. Both are reported in this thesis rather than quietly
> corrected.
>
> **Confidentiality.** The commercial scanner panel underlying this thesis is
> licensed data held under a non-disclosure agreement. No proprietary, personal or
> confidential data was entered into any externally hosted generative AI tool
> outside the controlled experimental calls described in Chapter 8, whose inputs
> are the brand-level aggregates reproduced in the appendix. The raw panel never
> leaves the local environment, and the project repository enforces this.
>
> **What the authors did independently.** The research questions, the design of
> the artefact and of its evaluation, the selection and reading of the literature,
> the interpretation of the results, and the conclusions drawn from them are the
> authors' own. Responsibility for every claim in this thesis, including any claim
> informed by AI-assisted drafting, rests with the authors.

---

# F2 — the Methodology declaration CBS explicitly requires

⚠ **This is the part the earlier draft was missing, and it is the one CBS names
as a requirement rather than a courtesy:**

> *"You must declare the use of GenAI tools as part of the Methods section in your
> document, i.e., describe how you have used GenAI in the writing process."*

**A front-matter declaration does not satisfy a rule that names the Methods
section.** Adding it costs one short subsection and closes the requirement
explicitly.

### Anchor

**Chapter 3, as a new final subsection**, after §3.7 (the limitations section,
which ends the chapter). Number it **3.8**.

⚠ **Check the current final section number in Word before numbering.** §3.7 was
the last as of this snapshot.

### Action

APPEND — a new subsection at the end of Chapter 3.

#### Replace with

> ### 3.8 Use of generative AI in the research process
>
> Generative AI was used in this project in three ways, declared here in
> accordance with the CBS guidelines for final projects.
>
> It was used as a software development assistant. The data pipeline, the
> modelling and evaluation code, and the scripts producing this thesis's tables
> and figures were written with AI assistance and reviewed by the authors. Because
> the artefact is itself the object of assessment, the project adopted a
> convention that every number appearing in a generated table, caption or report
> is computed from an input consumed on that run rather than written by hand, so
> that a result cannot silently survive a change to the data that produced it.
>
> It was used as a language assistant and for conceptual discussion during
> writing: editorial support on the manuscript, and dialogue about how to organise
> an argument or sequence a chapter. Decisions about what to claim, which evidence
> supports a claim, and how a result should be interpreted were taken by the
> authors.
>
> It was not used for the literature search or for the selection and reading of
> sources, which were conducted by the authors, and no source is cited in this
> thesis that the authors have not read. Every reference was verified against the
> project's reference library before citation.
>
> The commercial panel underlying the empirical work is licensed under a
> non-disclosure agreement and was never submitted to an externally hosted AI
> tool, with the exception of the brand-level aggregates that form the documented
> inputs to the Chapter 8 experiment, which are reproduced in full in the
> appendix.

### Note — the cross-reference

**Both directions are wired:** the front-matter declaration points forward to
§3.8, and §3.8 stands alone for a reader who starts at Chapter 3. ⚠ **If you
renumber, fix the forward reference in the declaration too** — it names "Section
3.8" explicitly.

---

# Placement

| | |
|---|---|
| **Front matter, before the abstract** | the declaration above — maximum visibility |
| **Chapter 3, §3.8** | the writing-process description — **because CBS requires it there** |

Decided; no supervisor confirmation, per your instruction.

---

# What is deleted along with the old section

| Deleted | Why |
|---|---|
| "CBS requirement: Autumn 2025 rules... Status: DRAFT... Last updated: 2026-03-15" | metacomment; threads 298, 299 |
| "Draft text (bullet form - NOT prose yet)" | same |
| The placement table (Options A/B/C) | reasoning is sound, but it belongs in this note |
| The exogenous-variables footnote | Chapter 4 §4.1.3 and §4.3 already carry this content |
| "Temperature: 0 (deterministic outputs)" | ⚠ **false** — not settable on this model |
| "Claude claude-sonnet-4-6 ... Synthesis Agent" | ⚠ **false** — wrong vendor, wrong model, an architecture never built |

---

# ⚠ One clause I want you to read twice

> *"Using GenAI to generate text, images, or other content as part of the final
> product is only acceptable if a specific reference is provided."*

**This is the clause with teeth, and neither variant fully satisfies it in the
strictest reading.** A strict reading asks for a reference at each generated
passage, the way a quotation is referenced. Nobody does this for editorial
assistance, and the guidelines' own framing — comparing language-assistant use to
Grammarly, which needs no declaration — makes the strict reading implausible for
prose that has been reviewed, revised and verified by the authors.

**Where the line actually sits:** CBS distinguishes *assistance in producing your
own product* from *generated content as a component of the final product*. A
figure generated wholesale by AI, or a passage inserted verbatim, is the second.
Drafting reviewed and rewritten by the authors is the first.

✅ **The declaration above places the use in the first category and says so
plainly.** That is defensible and it is what the guidelines describe. But it is
an interpretation, and you should be able to say it out loud in a defence.

→ **Recorded in `anticipated-assessor-questions.md`** as a defence item, with the
answer: the assistance was drafting and editorial support on the authors'
arguments and evidence, declared in the front matter and in §3.8, and every
empirical claim was verified against its artefact.

---

# What the guidelines let you stop worrying about

✅ **Using AI to search for literature would have been fine** (search-engine use,
no declaration needed). The declaration says the authors did the searching, which
is true and stronger.

✅ **Idea generation and structuring are explicitly acceptable**, compared by CBS
to *"asking a parent, fellow student, or mentor"*. The §3.8 text names this
directly rather than avoiding it.

✅ **Spell-check and language-assistant use need no declaration at all.** Everything
declared above is therefore declared by choice, which is the right side of the
line to be on.

---

# The defence

⚠ **CBS requires that you inform your supervisor and censor if GenAI was used in
preparing for the oral defence, and forbids using it during the defence itself.**

**Not an action for today**, but it belongs in the defence preparation note —
recorded in `anticipated-assessor-questions.md`.
