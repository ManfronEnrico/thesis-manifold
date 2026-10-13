---
name: defence-readme
description: REFERENCE - Start here. What to open, in what order, and how to work through the deck finalisation before the 21 October defence.
category: reference
applies-to: [oral defence]
triggers: [preparing for the defence, what is in this folder, what do I work on next]
created: 2026_09_15-18_30
updated: 2026_10_13-13_45
---

# Defence preparation — start here

**Defence: Wednesday 21 October 2026, 13:15–14:30.** 75 minutes: about 15 presented,
the rest dialogue, deliberation and grading.

**Nothing in this folder edits the thesis.** It was submitted 2026-09-15 and is closed.
The authoritative deck is the **OneDrive `.pptx`**; everything here helps you edit it.

---

## 1 The three files to work through, in order

| # | File | What it is | Time |
|---|---|---|---|
| 1.1 | `slide-review/2026-10-10_deck-review-pass-02.md` | **The main worklist.** §1 open fixes · §2 your slide comments answered · §3 new findings · §4 speaker notes for every presented slide · §5 design suggestions | most of it |
| 1.2 | `slide-review/2026-10-12_new-slide-design-principles.md` | Build spec for the **one new slide** (Five Design Principles, after slide 24) | ~30 min |
| 1.3 | `qa-drill.md` | 22 likely questions, each with a 20-second answer. **Rehearsal, not editing.** | the last days |

Background only, no action needed: `slide-review/2026-09-20_deck-review-pass-01.md`
(the first review; pass 02 §1 lists which of its fixes are still open) and
`slide-plan.md` (the September plan the deck grew from).

---

## 2 How to work through them

### 2.1 Set up

Open the `.pptx` and pass 02 side by side. Every item names the **slide number**, quotes
the **current text**, and gives the **replacement**, so you never have to search.

### 2.2 Work in this order

| # | Step | Where | Why this order |
|---|---|---|---|
| 2.2.1 | Fix factual errors | pass 02 **§1**, top to bottom; tick each ☐ | these cost marks; everything else is polish |
| 2.2.2 | Act on your slide comments | pass 02 **§2** (~~delete 13~~ ✅ done; split slide 24 item 5) | structural changes before wording |
| 2.2.3 | Build the new slide | file **1.2** | changes the deck's last section |
| 2.2.4 | Replace the speaker notes | pass 02 **§4**: on each slide, delete the pasted *"Original Figure Description"* and paste the bullets, then reword them in your own voice | notes should match the final slides |
| 2.2.5 | Design | pass 02 **§5.1** first (slide 14 overflow, slide 9 font); §5.2 optional | last, because content changes move layout |

### 2.3 Splitting it between two people

Divide by **slide range** rather than by step, so you never edit the same slide at
the same time in OneDrive. One natural split: slides 1–15 / 16–26 plus the new slide.
Each person does steps 2.2.1–2.2.5 for their range.

### 2.4 Checking your work

Whenever you want a check, ask Claude to **"re-snap the deck"**. It snapshots the
`.pptx`, diffs it against the last snapshot, and reports which fixes landed, which
didn't, and any new comments.

**Questions for Claude can go straight into PowerPoint comments.** The snapshot
exports each comment with the exact text it's anchored to; that's how your slide
13/23/25 comments were picked up.

---

## 3 Rules that are easy to break

| # | Rule | Why |
|---|---|---|
| 3.1 | **Don't volunteer weaknesses; never deny them if asked.** | Decided 2026-10-12. The prepared "only if asked" answers are pass 02 §4.16 and drill Q22. |
| 3.2 | **Never say "off by one month"** about the lags | at the three-month horizon it's three months (findings F16) |
| 3.3 | **No GenAI during the defence itself** | CBS rule |
| 3.4 | GenAI used in *preparing* the defence | CBS asks students to inform supervisor and censor; whether the slide-4 disclosure and §3.8 suffice is your call (R-1012-04 §1) |
| 3.5 | Never upload thesis chapters to NotebookLM | it returns your own wording as a "source" |

---

## 4 Where the evidence lives

| Kind | Location |
|---|---|
| Every finding, in plain English **and** technical detail | `plans/P0056_*/findings.md`. F14/F16 = the forecasting method; F15 = deck pass 01; F17 = drill sweep and code cross-check |
| Any measured number | `05_thesis_results/`, by chapter |
| The thesis text, greppable | `06_thesis_writing/docx-exported-snapshots/` (newest folder) |
| Deck snapshots | `pptx-exported-snapshots/` (newest folder; gitignored) |
| The 25-question evidence base behind the drill | `06_thesis_writing/writing-notes/anticipated-assessor-questions.md` |

---

## 5 Superseded

`deck-variant-T-transparent.html` and `deck-variant-S-silent.html` are the September
HTML decks, from before the PowerPoint existed. **Kept for history; don't work from
them.** The `notebooklm/` restatements still stand as study material.
