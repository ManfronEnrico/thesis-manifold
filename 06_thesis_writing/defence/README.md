---
name: defence-readme
description: REFERENCE - What lives in the defence folder, what each file is for, and the order to use them in.
category: reference
applies-to: [oral defence]
triggers: [preparing for the defence, what is in this folder]
created: 2026_09_15-18_30
updated: 2026_09_15-18_30
---

# Defence preparation

Created 2026-09-15, after submission, under **P0056**.

**Nothing in this folder edits the thesis.** The thesis was submitted
2026-09-15 14:00 and is closed. These are preparation artefacts for the oral
defence.

## Why this sits in tier 06

Tier 06 holds writing-side prose and notes. The artefact rule — *tier 06 holds
no figures, tables or diagrams* — is respected: no artefact is produced here.
The decks **reference** SVGs in `05_thesis_results/` by path and do not copy
them, so there is no second copy of any figure.

## Files

| File | What it is | When to use it |
|---|---|---|
| `deck-variant-T-transparent.html` | 15-min deck, 10 content slides. **Includes** a slide foregrounding the lag-12/13 provenance defect. | if you want to own the defect first |
| `deck-variant-S-silent.html` | Same deck, 9 content slides. **No defect slide**; the 90 seconds go to the ladder and the closing. | if you would rather spend the time on contribution |
| `qa-drill.md` | Every likely question in a 20-second-answer format. Printable. | the morning of, and in the room |
| `notebooklm/01_thesis-in-brief.md` | The whole thesis restated in ~1,200 words | NotebookLM audio overview |
| `notebooklm/02_the-ladder.md` | The SRQ4 design and why it has seven rungs | NotebookLM quiz — the most examinable methodology |
| `notebooklm/03_every-number.md` | Every figure, read from `05_thesis_results/` | NotebookLM multiple-choice generation |
| `notebooklm/04_known-flaws.md` | 12 defects, each with cause and answer | NotebookLM quiz; also read before the drill |

## The deck choice

The two variants differ in **one slide**. Read the note at the top of
Variant S before choosing, because the choice is not what it first appears:

**The lag-12/13 defect is already stated in the submitted thesis**, in Chapter 9
§9.4, as a provenance failure between the analytical and engineering layers. So
Variant S conceals nothing — it omits a slide about text the examiners can read.
What it forgoes is the credit CBS explicitly signals for using the presentation
to correct flaws, and the chance to raise the topic on your terms.

Either way, **the answer must be ready**. `qa-drill.md` prepares it identically
for both.

## Order to work in

1. Read `notebooklm/04_known-flaws.md` — it is the shortest route to knowing where the thesis is soft.
2. Read both decks, pick one, and rehearse it aloud with a timer.
3. Feed the four `notebooklm/` files to NotebookLM. Generate an audio overview first, then a quiz.
4. Read `06_thesis_writing/writing-notes/anticipated-assessor-questions.md` in full — it is the evidence base behind the drill.
5. Drill from `qa-drill.md` until the 20-second answers are fluent without the page.

## ⚠ Two rules that are easy to break

**Never upload thesis chapters to NotebookLM.** It returns our own wording as a
"source", which reads as independent confirmation and is not. The four files
here are restatements written from the results artefacts for exactly this
reason.

**Inform supervisor and censor that GenAI was used in preparation.** This is a
CBS requirement, not a courtesy, and it has an outside party — it cannot be done
from this repository. No GenAI tool may be used during the defence itself.

## Where the evidence lives

| Kind | Location |
|---|---|
| Any measured number | `05_thesis_results/`, by chapter |
| The 25-question evidence base | `06_thesis_writing/writing-notes/anticipated-assessor-questions.md` |
| 22 line-numbered forecasting defects | `plans/P0055_*/findings.md` |
| This session's reconnaissance | `plans/P0056_*/findings.md` |
| The submitted text, greppable | `06_thesis_writing/docx-exported-snapshots/2026-09-15_17-43_oral-exam-prep/` |
