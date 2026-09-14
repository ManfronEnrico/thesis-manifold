---
name: 2026-09-15_BRANCH_A_ai-declaration-variant-D-final
description: FINAL - Variant D of the AI Use Declaration, written out in full with no cross-references. Supersedes the four-variant note. Paste-ready, front matter, before the abstract.
category: workflow
applies-to: [ai-use-declaration, submission preparation]
triggers: [AI declaration, academic integrity statement, front matter, submission]
created: 2026_09_15-00_45
updated: 2026_09_15-00_45
snapshot: 2026-09-15_00-30_eod-final-pass
status: prose ready to paste
---

# AI Use Declaration — Variant D, in full

Verified at `2b33025`, fetch clean. Snapshot `2026-09-15_00-30_eod-final-pass`.
Threads **299 and 300** (the other two closed in your pass today).

**You chose Variant D.** It is written out in full below — no *"identical to
Variant A"* placeholders, so you can paste it in one action.

| In `2026-09-14_BRANCH_A_ai-use-declaration-drafts.md` | Status |
|---|---|
| Variants A, B, C | **not chosen** — the file stays as the record of the range |
| Variant D's abbreviated text | **superseded by the full text below** |
| Fix 1's anchor, the deletion table, the placement decision | **stand unchanged** |

✅ **You said the model pin is now in Chapter 3 prose.** That closes the
"one thing to check before pasting" item at the end of the earlier note — no
action left there.

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
> code, and the scripts that generate this thesis's tables and figures. It was
> additionally used for editorial support on the manuscript. All output was
> reviewed and verified by the authors.
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
> the artefact and of its evaluation, the selection and reading of the literature,
> the interpretation of the results, and the conclusions drawn from them are the
> authors' own. Responsibility for every claim in this thesis rests with the
> authors.

---

# Placement

**Front matter, before the abstract.** Decided — no supervisor confirmation, per
your instruction. Maximum visibility, and it cannot be missed.

---

# What is deleted along with the old section

| Deleted | Why |
|---|---|
| "CBS requirement: Autumn 2025 rules... Status: DRAFT... Last updated: 2026-03-15" | metacomment; threads 299, 300 |
| "Draft text (bullet form - NOT prose yet)" | same |
| The placement table (Options A/B/C) | its reasoning is sound, but it belongs in this note, not the document |
| The exogenous-variables footnote | Chapter 4 §4.1.3 and §4.3 already carry this content, correctly |
| "Temperature: 0 (deterministic outputs)" | ⚠ **false** — not settable on this model |
| "Claude claude-sonnet-4-6 ... Synthesis Agent" | ⚠ **false** — wrong vendor, wrong model, describes an architecture that was never built |

---

# One standing caveat, recorded rather than repeated

⚠ I said in the earlier note that I would argue against D, and I am not
relitigating a decision you have made. But the reasoning belongs somewhere you
can find it if it is ever raised:

**"Editorial support" implies polishing text that already existed.** If an
assessor asks directly what that phrase covered, answer plainly rather than
standing on the wording — the submitted repository's git history and note folders
are part of the record. **The declaration is defensible; a denial on top of it
would not be.**

✅ **Nothing in Variant D is false.** Claude Code was used as a development
assistant, it was used for editorial support, and all output was reviewed. That
is why it was writable at all.

→ **Record this in `anticipated-assessor-questions.md`** as a defence item: *"What
did 'editorial support' cover?"* — a short, honest, unrehearsed answer is the
right one.
