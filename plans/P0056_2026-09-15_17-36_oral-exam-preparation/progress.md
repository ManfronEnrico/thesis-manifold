---
name: p0056-progress
description: LOG - Session log for oral defence preparation.
pid: P0056
created: 2026_09_15-17_36
updated: 2026_09_15-18_05
---

# P0056 — Progress

## Session 1 — 2026-09-15, from 17:36

### `/re-snap` — 3 of 4 steps run, 1 skipped with reason

| Step | Result |
|---|---|
| 1. `git fetch` | clean. `83689d3`, 6 ahead of `origin/main`, nothing incoming |
| 2. snapshot | `2026-09-15_17-43_oral-exam-prep` — 47,299 words, 17 chapters, 1 comment, 143 leaf sections |
| 3. diff vs previous | **skipped deliberately** — thesis is submitted, no pending pass to check landings for |
| 4. Zotero re-pull | 88 items; `bibtex.bib` + `citations.json` written, then a cosmetic crash (see task_plan errors) |

Snapshot warned: 2 chapters not in `CHAPTER_SUBJECTS` (Table of Appendices,
Chapter 7). Known — P0052's concern, harmless here.

### Read

Submitted: abstract, Ch1, Ch8, Ch9, Ch10, the Ch8 comment thread, MANIFEST.
Repo: `PLANS_INDEX.md`, P0055 `task_plan.md` + `findings.md`,
`anticipated-assessor-questions.md`, `deferred-structural-decisions.md`,
canonical research questions, `22_scenario_comparison.csv`, the 87-SVG inventory,
submission-repo tier comparison.

### Decisions

| | |
|---|---|
| Deck before NotebookLM corpus before drill | Brian's choice; the deck forces the emphasis decisions the others inherit |
| Two deck variants, not one strategy | Brian declined both flaw options and asked for a transparent and a silent version |
| Deck reuses existing SVGs | 87 already generated and consistent with the submitted numbers (F7) |
| Numbers come from `05_thesis_results/`, never from the prose | Correctness-tier rule; also caught that "roughly fifty" is 51.3× (F3) |

### Phase 2 + 3 delivered (Session 1, 18:05–18:35)

All under `06_thesis_writing/defence/` — a new folder, with a README stating why
it sits in tier 06 and confirming no artefact is produced there (the decks
reference `05_thesis_results/` SVGs by path, never copy them).

| File | Lines of substance |
|---|---|
| `deck-variant-T-transparent.html` | 10 content slides, per-slide timings, speaker split, say-this text, reserve answers in notes |
| `deck-variant-S-silent.html` | 9 content slides; defect slide removed, 90 s returned to slides 6 and 10, both marked |
| `qa-drill.md` | 21 drilled questions + 8 one-liners, 20-second answer format, printable |
| `notebooklm/01_thesis-in-brief.md` | whole thesis in ~1,200 words |
| `notebooklm/02_the-ladder.md` | SRQ4 design, controls, the audit that caught drifted prompts |
| `notebooklm/03_every-number.md` | every figure, sourced from artefacts |
| `notebooklm/04_known-flaws.md` | 12 defects with cause + answer, plus 6 things NOT to concede |
| `README.md` | what to use when, and the two easy-to-break rules |

**Phase 4 is effectively delivered inside `qa-drill.md`** rather than as a
separate pass — it extends `anticipated-assessor-questions.md` (Part 2 carries
the six F6 gaps plus F9) instead of rebuilding it. Phase 5 (rehearsal support)
is partly inside the decks: timings, speaker split, handover notes. A separate
timing script was not written.

### Open for Brian

1. **Phase 0 compliance** — CBS requires informing supervisor *and* censor of GenAI use in defence preparation. Outside party; cannot be done from here.
2. **F5** — the lag-13 defect is already in the submitted Ch9 §9.4, so "transparent vs silent" is not confess-vs-conceal. Changes the choice.
3. **F8** — was Ch8's Table 24 regenerated before submission (comment 279)?
4. Defence date/time — not yet known; available on Digital Exam ≤8 days prior.
