---
pid: P0056
created: 2026-09-15 17:36:00
updated: 2026-09-15 18:05:00
status: in_progress
focus_detail: "Oral defence preparation. Thesis was HANDED IN 2026-09-15 14:00 - nothing here edits the thesis. Deliverables in order: (1) slide deck in TWO variants per Brian's instruction - one surfacing a known defect, one surfacing none; (2) NotebookLM source corpus for audio/quiz generation; (3) Q&A drill material extending the existing anticipated-assessor-questions.md. Phase 1 (reconnaissance) COMPLETE - see findings.md F1-F6. The single most important inherited asset is 06_thesis_writing/writing-notes/anticipated-assessor-questions.md (4,544 words, ~25 questions with measured answers) - READ IT BEFORE WRITING ANY DRILL MATERIAL; do not rebuild it."
---

# P0056 — Oral defence preparation

> The thesis is **submitted**. This plan produces defence artefacts only.
> **Nothing in this plan edits the thesis, the repo's pipeline code, or any result.**

---

## Goal

Prepare two authors for a 75-minute CBS group defence of a submitted master's
thesis, where the presentation is ~20% of the slot (≈15 min) and examiner
dialogue ≈55%.

Assessment is **overall** — thesis plus defence performance — so the defence can
still move the grade.

## Hard constraints from CBS (source: my.cbs.dk, pasted by Brian 2026-09-15)

| Constraint | Consequence for this plan |
|---|---|
| Group defence, 2 people, **75 min** | presentation ≈15 min total, both speaking |
| Presentation ≈20%, dialogue ≈55%, deliberation ≈15%, grade ≈10% | the drill material matters more than the deck |
| "Correct (significant) flaws" is an explicitly invited use of the presentation | the transparent deck variant is sanctioned, not risky |
| Only references actually used are examinable | no need to revise the wider curriculum |
| Any exam aid permitted (computer, notes) | a printed Q&A drill is usable *in* the room |
| Print slides for the examiners | deck must survive greyscale print |
| **Must inform supervisor + censor of GenAI use in preparation** | ⚠ action item, not optional — see Phase 0 |
| **May NOT use GenAI during the defence itself** | drill material must be memorable, not lookup-dependent |

## Phases

### Phase 0 — Compliance action ⚠ do first, it has an external dependency

| Step | State |
|---|---|
| 0.1 | Notify supervisor **and** censor that GenAI was used in defence preparation | **pending — Brian/Enrico action, cannot be done by this session** |
| 0.2 | Confirm no GenAI tool is used during the defence | noted |

Source: `anticipated-assessor-questions.md`, closing section, quoting the CBS
GenAI guidelines. This was already discovered by an earlier pass; it is
surfaced here as a task because it is the only item with an outside party.

### Phase 1 — Reconnaissance ✅ COMPLETE

`/re-snap` run, repo inspected, submitted document read. Findings F1–F6.

### Phase 2 — Slide deck, two variants ← CURRENT

Same spine; they differ in **one slide**.

| | Variant T (transparent) | Variant S (silent) |
|---|---|---|
| Self-found defect | one slide, foregrounded | absent |
| Everything else | identical | identical |

⚠ **F5 changes what this choice means.** Ch9 §9.4 *already* states the lag-13
defect in the submitted text. So Variant T foregrounds something the thesis
owns; Variant S omits a slide about something the examiner can read. Neither is
concealment. Brian to choose after seeing both.

### Phase 3 — NotebookLM corpus

Source `.md` files for audio overview / quiz / MCQ generation.
⚠ **Never upload thesis chapters themselves** — NotebookLM returns our own
wording as a "source", which reads as independent confirmation and is not.
(Rule inherited from `prose-insertion-discipline.md`.)

### Phase 4 — Q&A drill

Extend, do not rebuild, `anticipated-assessor-questions.md` into a drilled
format. Add the gaps found in F6.

### Phase 5 — Rehearsal support

Timing script, who-speaks-when split, opening 90 seconds written verbatim.

## Errors encountered

| Error | Attempt | Resolution |
|---|---|---|
| `zotero_client.py` `KeyError: 'year'` | 1 | **Cosmetic.** Crash is in the 5-item sample-print loop (line 355), which runs *after* both `write_bytes` calls. `bibtex.bib` + `citations.json` are current at 88 items. One-line fix would be `item.get("year")`. Not fixed here — this plan does not touch tooling. |
| Working directory drifted twice (`cd` inside compound Bash commands) | 2 | Absolute paths only. |
