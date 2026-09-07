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

Eleven diagrams and twenty-five appendix tables regenerate from five producer
scripts, in any order, with no duplicate filenames and no leaked internal
references. Every number is read from an artefact at render time; a generator
exits rather than drawing when a source table is missing. The preprocessing
pipeline logs both its execution and its content, and the appendix consumes
both. 195 live scripts compile; `PATHS.py` resolves.

---

## Run everything (the five producers)

```powershell
$env:PATH += ";C:\Program Files\Graphviz\bin"   # winget installed it, but not on PATH

python 05_thesis_results/generate_architecture_diagrams.py          # 11 diagrams
python 05_thesis_results/generate_literature_table.py               # table 89
python 04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py # tables 01-14
python 01_SRQ1_Model_Training/01_thesis_data/_00_raw/holidays/export_holiday_appendix.py       # 90-93
python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py  # 94-99
```

To regenerate the underlying pipeline data (~2 min, all four categories):

```powershell
python 01_SRQ1_Model_Training/01_thesis_data/_02_preprocessing/nielsen/_shared_modules/run_preprocessing.py --all-categories --horizons 1,3 --no-log
```

---

## Read these two things before touching a figure

1. **`.claude/rules/figure-generation-standards.md`** — the style contract.
   Horizontal layouts, bold box headers, no step numbers, greyscale contrast
   tiers, transparent background, submission-ready captions, every value read
   from an artefact.
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

`task_plan.md` → Phase 5. Publish the inventory **first**, then choose citations.
Never the reverse — see F2.
