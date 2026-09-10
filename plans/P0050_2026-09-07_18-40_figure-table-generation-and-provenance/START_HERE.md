# START HERE — P0050, figure & table generation

**Written 2026-09-07 to survive an account switch that loses session history.**
Everything needed to resume is on disk. Read this page, then `task_plan.md`.

---

## What this plan owns

Every figure, table, graph and diagram in the thesis: making each one
**regenerable from current data by a live script**, centrally located,
consistently styled, and provably data-driven rather than asserted.

It absorbs the figure/table threads that were scattered across
`P0046_..._figure-table-provenance-centralisation` (the predecessor, now
superseded by this plan) and the styling decisions made on 2026-09-07.

**It does not own**: prose insertion (P0048), the funded experiment sequence
(P0049), or the holiday-enrichment decision (P0047).

---

## The state in one paragraph

Twelve diagrams and twenty-five appendix tables regenerate from **nine** producer
scripts, in any order, with no duplicate filenames and no leaked internal
references. Every number is read from an artefact at render time; a generator
exits rather than drawing when a source table is missing. The preprocessing
pipeline logs both its execution and its content, and the appendix consumes
both. `PATHS.py` resolves.

**Updated 2026-09-10** after a provenance audit prompted by the cluster re-run
(F26-F31), then corrected the same day (F32-F33). What holds now:

| | |
|---|---|
| Everything in tier 05 is **SVG**, never PNG | DEC-SVG-ONLY |
| Figures paint a **white** ground, never transparent | DEC-WHITE-GROUND |
| Tier 05 output carries **only what a thesis reader should see** | DEC-READER-FACING-ONLY |
| Editorial notes live in the **chapter folder** they serve | DEC-NOTES-BY-CHAPTER |

The audit found three stale literals, three figures showing a superseded model
selection, and three orphan SVGs. All fixed at the producer.

## The invariant, and how it is now held

Tiers 01-05 are read by assessors, so **nothing student-facing appears in them**,
marked or unmarked. Producer scripts may live anywhere (Brian: "I don't mind
honestly"); only emitted content is governed.

Two passes each caught the class they were looking for and missed the next one --
the first searched for an `INTERNAL REVIEW` marker, the second for a plan-ID
shape, and a bare `F17` reading as ordinary prose survived both (F32, F34). So
the rule is no longer something a person checks:

```powershell
python 05_thesis_results/check_reader_facing.py     # exit 1 on any hit
```

Every appendix producer also calls `warn_after_run()` at the end of its own run,
so a new leak is reported by the run that writes it.

**Editorial notes** live at
`06_thesis_writing/writing-notes/ch{N}_{chapter}/generated/<slug>.md`, filed by
the chapter that discusses the artefact. The chapter is derived from the
artefact's own output path, so a table and its note cannot diverge.

**Phase 8 is complete.** Nothing is committed.

---

## Run everything (the nine producers)

```powershell
$env:PATH += ";C:\Program Files\Graphviz\bin"   # winget installed it, but not on PATH

python 05_thesis_results/generate_architecture_diagrams.py          # 12 diagrams
python 05_thesis_results/generate_methodology_diagram.py            # ch3 figure
python 05_thesis_results/generate_literature_table.py               # table 89
python 04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py # tables 01-15
python 01_SRQ1_Model_Training/01_thesis_data/_00_raw/holidays/export_holiday_appendix.py       # 90-93
python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py  # 94-99
python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/training_report.py
python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_generate_performance_figures.py
python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_generate_shap_figures.py
```

The **EDA plots** are not in that list: they are written by pipeline step 2 and
copied into tier 05 by `promote_eda_artifacts()`. To refresh them:

```powershell
python 01_SRQ1_Model_Training/01_thesis_data/_02_preprocessing/nielsen/_shared_modules/run_preprocessing.py --category CSD --horizon 3 --from-step 2 --to-step 2
```

`generate_methodology_diagram.py` reads the **newest docx snapshot**, so run
`thesis_snapshot.py` first if the methodology chapter was edited in Word.

To regenerate the underlying pipeline data (~2 min, all four categories):

```powershell
python 01_SRQ1_Model_Training/01_thesis_data/_02_preprocessing/nielsen/_shared_modules/run_preprocessing.py --all-categories --horizons 1,3 --no-log
```

---

## Read these two things before touching a figure

1. **`.claude/rules/figure-generation-standards.md`** — the style contract.
   Horizontal layouts, bold box headers, no step numbers, greyscale contrast
   tiers, **white** background, submission-ready captions, every value read
   from an artefact, and no internal content anywhere in tiers 01-05.
2. **`findings.md` in this folder** — F1-F14, the things that were wrong and how
   they were found. F5 and F6 in particular are traps that will recur.

---

## ⚠ One blocking caveat inherited from elsewhere

**The forecast horizon is never applied to feature construction.**
`engineer_features()` takes no horizon argument (verified directly:
`_shared_modules/engineer_features.py:444`). The `h1` and `h3` matrices encode
the **same one-month task** and differ only in their split dates.

Found by P0048 (F1), carried by P0049 (F22). It is upstream of the funded runs.

**Consequence for this plan**: the appendix's data-reduction table carries a
"Horizon (months)" column. The row counts are real; the *label* asserts a horizon
the pipeline never applied. A DO-NOT-PUBLISH warning is in that table's review
notes. **Re-run the table after the horizon fix lands** and remove the warning.

No other figure in this plan depends on the horizon.

---

## Where things live

| What | Where |
|------|-------|
| Diagrams (11) | `05_thesis_results/diagrams/` |
| Appendix tables (25) | `05_thesis_results/appendix/` |
| EDA artefacts (149) | `05_thesis_results/eda/{category}/` |
| SRQ1 results | `05_thesis_results/srq1_model_performance/{figures,tables,models}/` |
| Superseded hand-drawn figures | `05_thesis_results/diagrams/orphan_conceptual/` (do not paste) |

**Appendix filename block allocation** — keep this in step when adding a
producer, or one script will delete another's output (F6):

```
01-49   export_appendix.py              <- clears its own block on each run
89      generate_literature_table.py
90-93   export_holiday_appendix.py
94-99   srq1_export_enrichment_appendix.py
```

---

## Next action

**Phase 5** -- publish the regenerable inventory FIRST, then choose citations.
Never the reverse (F2). Phases 3b, 6 and 7 are also open; Phase 8 sits above them
in `task_plan.md` only because it was added last.

Nothing from the last three sessions is committed. Review the working tree and
stage **by explicit path** -- never `git add -A`, which sweeps in another
session's files.

One open item is inherited rather than owned here: the horizon blocker above.
When the horizon fix lands, re-run the data-reduction table and drop the warning
from its chapter note.
