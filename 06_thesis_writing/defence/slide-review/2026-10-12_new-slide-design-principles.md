---
name: 2026-10-12_new-slide-design-principles
description: REFERENCE - Build spec for the one new slide the deck needs, the five design principles, with on-screen text, layout, speaker notes and thesis grounding.
category: reference
applies-to: [oral defence, slide deck]
triggers: [design principles slide, closing slide, what transfers]
created: 2026_10_12-11_00
updated: 2026_10_13-13_45
snapshot_thesis: 2026-10-10_16-42_deck-finalisation
answers: pass-02 §3.4
---

# New slide — the five design principles

## 1 Why this slide, and where

| # | Point |
|---|---|
| 1.1 | **What it fixes.** The abstract names three contributions: an artefact, *"five design principles"*, and an evaluation design. The deck shows the first and third. Slide 14 tells the examiners that design science is judged on an artefact **and** transferable knowledge. Without this slide, the knowledge is never shown. |
| 1.2 | **Where.** After slide 24 (Limitations), before the Reference List. Section 06 then ends on what the thesis *contributes* rather than on what it couldn't do, which suits the don't-volunteer approach (R-1012-01). |
| 1.3 | **Title.** `WHAT TRANSFERS \| Five Design Principles` |
| 1.4 | **Origin.** Planned in September as slide 06.2 in `slide-plan.md`, never built. This spec supersedes that one: it uses "~50×" instead of "51×" and has been re-checked against the 2026-10-10 snapshot. |

---

## 2 On screen

**Layout:** a five-row table across the top two-thirds; the closing sentence below
it, in the largest text on the slide. Two columns only.

| # | Principle | Because we measured |
|---|---|---|
| 2.1 | **Delegation over generation** | tool-backed answers identical on every repeat; code-written answers differed almost every time |
| 2.2 | **Explicit refusal over silent fallback** | a fallback asserts something was found, and an agent cannot tell the difference |
| 2.3 | **Carry the track record, not only the interval** | the interval spans 8–34× the forecast; the measured error is what carries reliability |
| 2.4 | **Budget memory at selection time, report it at run time** | 4 GB excluded transformers up front; realised peak ~231 MB |
| 2.5 | **Report cost and latency beside accuracy** | ~50× cost difference at comparable accuracy |

> **2.6** A forecast becomes usable not when it is accompanied by an interval, but
> when it is accompanied by **evidence of how far the model producing it has been
> right before.**

*(The `#` column is for this document only. Leave it off the slide.)*

### 2.7 Design suggestions

- Bold only the principle names. Right column regular weight, 12–14 pt, matching slide 20's table.
- No icons. Five rows of text already fill the space.

---

## 3 Speaker notes

*Paste into the notes field. Bullets to speak from, not a script.*

- Design science says an artefact only becomes a contribution when the knowledge
  inside it is stated separately. These five are that knowledge. *(Ch10 §10.2;
  Hevner et al. 2004)*
- Each is stated for a **kind of problem**, not for our system, so someone
  building something similar can use them. And each is backed by a measurement:
  if the principle were wrong, our results would have come out differently.
  *(Ch9 §9.2.2)*
- Pick **one** to explain, not all five. The best is the first: when a number has
  to be the same every time you ask, let the language model *ask* a model for it
  rather than calculate it itself.
- Close on the sentence at the bottom. It's the thesis's final statement, nearly
  word for word. *(Ch10 §10.6)*
- Then stop and hand over to questions. *(Plan: 55% of the slot is dialogue.)*

### 3.1 The five in plain English (for you, not the slide)

The external examiner isn't from a statistics background. If asked "what does
that mean?", use these:

| # | Principle | Plain English |
|---|---|---|
| 3.1.1 | Delegation over generation | Don't let the chatbot invent the number. Let it fetch the number from a model built for the job. |
| 3.1.2 | Explicit refusal over silent fallback | If the tool can't answer, it should say "I can't" rather than quietly give a substitute. The chatbot would pass the substitute on as if it were real. |
| 3.1.3 | Carry the track record | A forecast should come with "here's how accurate this model has been before", because a range like "between 100 and 3,000" doesn't help anyone. |
| 3.1.4 | Budget memory at selection time | Use the memory limit to rule out heavy models before building anything, then report what you actually used. |
| 3.1.5 | Report cost and latency | Two approaches can be equally accurate and differ fifty-fold in price. If you only measure accuracy, you'd never see that. |

---

## 4 Grounding, verified 2026-10-12

| # | Claim on the slide | Source | Checked |
|---|---|---|---|
| 4.1 | Names of all five principles | Ch10 §10.2, verbatim | ✓ |
| 4.2 | identical on every repeat / different almost every time | Ch9 §9.2.2 DP1; `22_scenario_comparison.csv`: C and E 100% identical, B and D 0% | ✓ |
| 4.3 | refusal instead of fallback | Ch7: three refusal conditions (unknown category, brand with no held-out data, month outside the test split); `forecast_tool.py` | ✓ |
| 4.4 | 8–34× | Ch7; Ch9 §9.2.2 DP3 | ✓ |
| 4.5 | 4 GB excluded transformers; ~231 MB | Ch1 §1.4; Ch6 memory table ("End-to-end peak ~231 MB"); Ch9 DP4 | ✓ |
| 4.6 | ~50× cost | Ch10 §10.2 "a factor of roughly fifty"; CSV 0.4667 / 0.0091 = 51.3 | ✓ |
| 4.7 | closing sentence | Ch10 §10.6, verbatim apart from punctuation | ✓ |

### 4.8 One honest caveat, only if asked

Ch10 §10.4 says *"the design principles are derived rather than validated across
contexts"*: one design cycle, one company. If an examiner asks how general these
are, that is the answer. It's already in the thesis, so it's safe to say.
