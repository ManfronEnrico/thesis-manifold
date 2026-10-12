---
pid: P0056
created: 2026-09-15 17:36:00
updated: 2026-09-19 12:00:00
status: in_progress
focus_detail: "Oral defence preparation. Thesis was HANDED IN 2026-09-15 14:00 - nothing here edits the thesis. CURRENT WORK: Phase 2b - restructure both decks onto the seven-section spine Brian chose (Background & Motivation / Literature Review / Methodology / Architecture & Experiment / Most Relevant Findings / Limitations & Conclusion / Discussion), modelled on a top-grade reference deck from Max's group. The structural move that matters is section 07: a single 'Let's discuss' slide followed by a WALL of reserve slides never presented, reached only when an examiner asks. Reference deck ran 13 presented to 22 reserve. See findings.md F11 for the measurement and task_plan.md Phase 2b for the slide-to-artefact mapping. Section 02 (Literature Review) is the only section with NO existing slide - it must be authored. Deliverables already complete: both deck variants (old 10-slide structure), NotebookLM corpus (4 files), qa-drill.md. Do not rebuild anticipated-assessor-questions.md (4,544 words) - extend it."
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

## Defence date

**Wednesday 21 October 2026, 13:15–14:30** (75 min, matching the CBS format below).
Confirmed by Brian 2026-10-12. Nine days from that confirmation.

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
| 0.1 | Notify supervisor **and** censor that GenAI was used in defence preparation | **pending — Brian/Enrico action.** Distinct from the thesis's methodology-section declaration, which covers the *writing*; this rule covers *defence prep*, which happened after submission. An email suffices — no slide required. Draft in R-1012-03. Verbatim CBS source: "You need to inform your supervisor and censor if you have used GenAI when preparing for your oral defense." |
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

#### 2b — RESTRUCTURE to the seven-section spine (decided 2026-09-19)

Brian supplied a reference deck: a **printed handout with speaker notes from
Max's group, who took the top grade**, on a different topic (participatory
governance on decentralised social media). Read at
`~/OneDrive/Documents/02-Areas/MSc. Data Science/2026-03 - CBS Master Thesis/Documents/Max - Oral Defense Presentation_with_notes_OCR.pdf`,
35 pages. See **F11** for what its shape actually is, measured.

**The new section order, Brian's decision:**

| # | Section | Maps to what we already have |
|---|---|---|
| 01 | Background & Motivation | current slide 2 (the gap) |
| 02 | Literature Review | **new — we have no such slide today** |
| 03 | Methodology | current slide 3 (RQ + four layers), plus DSR |
| 04 | Architecture & Experiment | current slides 4 and 6 |
| 05 | Most Relevant Findings | current slides 5 and 7 |
| 06 | Limitations & Conclusion | current slides 8, 9, 10 |
| 07 | Discussion | **new — the "Let's discuss!" wall** |

**The load-bearing structural change is section 07.** Max's deck puts a single
slide reading *"Let's discuss!"* at page 13, then carries **22 further slides
behind it** (pages 14–35) that are never presented — interview tables, ethics,
construct definitions, architecture comparisons, framework diagrams. They are
reached only when an examiner asks something they answer.

That ratio is the point: **13 slides presented, 22 held in reserve.** The
backup set is roughly twice the size of the deck itself.

**What this buys us, stated concretely.** F6 lists six questions askable from
the submitted text that we cannot currently answer with a picture. F9 is a
two-table memory discrepancy that needs a side-by-side. We have **87 generated
SVGs and cite about two of them in the thesis** (F6 item 4) — which is itself a
question an examiner may ask. A reserve wall converts that surplus from a
liability into the answer.

**Allocation rule for the restructure:**

- Sections 01–06 carry **only** the figures and numbers the argument fails
  without. Keep them few. Max's presented slides are visually sparse; the
  density lives behind the discussion slide.
- Section 07 is the wall. Every reserve slide is **one question, one artefact**,
  titled with the question it answers so it can be found under pressure.
- **No new figures are generated.** Every reserve slide references an existing
  SVG in `05_thesis_results/` by path. The artefact rule holds: tier 06 produces
  no artefact, and nothing is copied.

**Reserve slides to build, each mapped to a real file** (verified present
2026-09-19; 87 SVGs on disk):

| Question it answers | Artefact |
|---|---|
| What does the whole ladder look like? | `08_experimental_evaluation/tables/22_scenario_comparison.svg` |
| How did runs fail, not just how badly? | `08_experimental_evaluation/tables/23_outcome_taxonomy.svg` |
| Show me an actual run | `.../25_per_run_record_p1.svg` … `30_per_run_record_p6.svg` |
| Were the prompts really controlled? | `.../prompt_schema_composition.svg`, `31_run_configuration.svg` |
| What does the memory profile show? | `05_model_benchmark/tables/15_substrate_resource_profile.svg` (**the F9 answer**) |
| Sandbox side of the same measurement | `08_experimental_evaluation/tables/17_sandbox_resource_profile.svg` |
| Which baselines beat you? | `05_model_benchmark/tables/19_statistical_baselines.svg` |
| Why won't you name a winner? | `.../20_seed_stability_p1.svg`, `21_seed_stability_p2.svg` |
| What does retraining cost? | `.../16_retraining_cost.svg` |
| Do the parameters drift? | `.../18_parameter_drift.svg` |
| What drives the model? | `05_model_benchmark/figures/shap_importance.svg` |
| Does it actually track the series? | `.../fig3_forecast_overlay.svg` |
| How was the model chosen? | `.../ch5_model_selection_v2.svg` |
| How is the interval communicated? | `07_decision_synthesis/tables/24_interval_communication.svg` |
| What is the tool contract? | `06_architecture/figures/ch6_tool_interface_v1.svg` |
| What is the data pipeline? | `04_data_assessment/figures/ch4_preprocessing_pipeline_v2.svg` |
| What is in the feature matrix? | `.../08_feature_matrix_p1.svg` … `13_feature_matrix_p6.svg` |
| Is there annual seasonality? | `04_data_assessment/figures/*/06_acf_pacf_plots.svg` (**the lag-12 evidence**) |
| What is the literature gap? | `02_literature_review/figures/ch2_gap_diagram_v2.svg` |
| What is the DSR design? | `03_methodology/figures/ch3_methodology_design_v1.svg` |

⚠ **Section 02 (Literature Review) has no current slide and needs writing from
scratch.** `ch2_gap_diagram_v2.svg` exists and is the natural anchor. This is
the only section where content must be authored rather than rearranged.

⚠ **Timing is unchanged at ~15 minutes.** Adding a seventh section does not add
time — section 07 is one slide (*"Let's discuss"*) plus a silent reserve. The
presented body must still fit the same budget, so sections 01–06 are *tighter*
than the current 10-slide deck, not longer.

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
