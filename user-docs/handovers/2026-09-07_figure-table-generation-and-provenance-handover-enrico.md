---
name: 2026-09-07_figure-table-generation-and-provenance-handover-enrico
description: HANDOVER - 05_thesis_results reorganised by thesis chapter; figure generation standardised and enforced in code
category: reference
applies-to: [05_thesis_results, PATHS.py, 01_SRQ1_Model_Training, 04_SRQ4_Scenario_Experiment]
triggers: [looking for a figure or table, adding a producer script, reordering thesis chapters, writing a chapter]
created: 2026_09_07-20_45
updated: 2026_09_07-20_45
---

# Handover — chapter-keyed results, and the figure standard

**For:** Enrico (and any later session)
**From:** Brian (session 2026-09-07, evening)
**Plan:** `plans/P0050_2026-09-07_18-40_figure-table-generation-and-provenance/`

Two things changed that affect anyone looking for an artefact or adding a script
that produces one.

---

## 1. Where things live now

`05_thesis_results/` is organised **by thesis chapter**, not by research
question:

```
05_thesis_results/
    01_introduction/            figures/
    02_literature_review/       figures/ tables/
    04_data_assessment/         figures/ tables/ eda/{CSD,Danskvand,…}/
    05_architecture/            figures/
    06_model_benchmark/         figures/ tables/ models/
    07_decision_synthesis/      figures/ tables/
    08_experimental_evaluation/ tables/
    09_discussion/
    .archive/                   quarantined, do-not-paste figures
    APPENDIX_TABLES.md          index: which table, which chapter
```

**Gone:** `srq1_model_performance/`, `srq2_structured_tool_interface/`,
`srq3_integration_readiness/`, `srq4_scenario_experiments/`, `appendix/`,
`diagrams/`. Nothing was lost — all 247 deletions were verified as moves before
anything was removed.

**Why chapter and not SRQ.** The writing workflow runs chapter by chapter, so
the folder you open should be the chapter you are writing. The two keys also
genuinely disagree: `export_appendix.py` lives under SRQ4 but only 5 of its 15
tables concern the scenario experiment, and the holiday tables split between the
calendar *source* (Ch4) and the ablation *results* (Ch6).

### The numbers are derived, not typed

Folder names are `{NN}_{slug}`, but `NN` comes from position in
`PATHS.CHAPTER_SLUGS` via one private helper. **To reorder the thesis, reorder
that tuple** — the folders renumber on the next run, and nothing else references
a chapter number to build a path.

This matters because a reorder is under active consideration (P0048 phase 8:
swapping the benchmark and architecture chapters). Verified by simulating that
swap: `05_model_benchmark` / `06_architecture`, no other edit.

---

## 2. If you add a script that writes an artefact

**Ask `PATHS.py` for a directory; never build one inline.**

```python
from PATHS import get_chapter_tables_dir, get_chapter_figures_dir
out = get_chapter_tables_dir("model_benchmark")     # creates it if needed
```

This is not style advice. ~30 producers write into the results tier, and the
restructure moved almost all of them **without being edited**, because they
asked `get_srq_*_dir()` for a location rather than naming one. The scripts that
needed manual fixing were exactly the ones that had built paths by hand —
including two inside the diagram generator that reconstructed
`THESIS_RESULTS_DIR / "eda" / "CSD"` and broke the moment the EDA folder moved.

`get_srq_{figures,tables,models}_dir(n)` still works and now resolves to the
right chapter, so existing SRQ-shaped code needs no change.

---

## 3. Figures: the standard is now enforced, not remembered

`.claude/rules/figure-generation-standards.md` is the contract. The parts most
likely to bite:

| Rule | Enforcement |
|------|-------------|
| Every diagram filename starts `ch<N>_` | `_check_stem()` **raises** |
| SVG only, no PNG twin | PNG output removed from the generator |
| Aspect ratio ≤ 3.6 (A4 landscape is 1.54) | measured; 9 of 11 fit either orientation |
| Every value read from an artefact at render time | generator exits if a source table is missing |

**Use `_stack()`, not a cluster, when the order of members matters.** Graphviz
reorders a cluster's members to shorten edges, and seven different ways of
constraining it each failed differently. `_stack()` renders the group as one
node whose label is a table of rows, so the order is text and cannot be
renegotiated. The cost: members are no longer individually addressable as edge
endpoints.

**Never span two clusters with `rank="same"`.** It re-parents the members, and
the cluster box then silently disappears — valid SVG, no error, grouping gone.
Graphviz warns (`"<node> was already in a rankset, deleted from cluster …"`);
that warning is worth reading.

---

## 4. Two near-misses, both about verification

**A folder that looked like leftover was not.** After the move,
`srq1_model_performance/` reappeared with four `cv_*` files. They looked like
stragglers, but were **19 hours newer** than the chapter-folder copies — a
benchmark had run mid-session and written through the old path. The newer
results were merged in. *Compare before deleting; a timestamp is cheap.*

**Repointed links can still be broken.** The draft image references were
repointed to `.../introduction/figures/...` before the numeric prefixes existed,
so they resolved to nothing. Caught only by re-resolving every image path in the
drafts at end of day. That check is now part of the `/eod` procedure.

---

## 5. Open, and not mine to close

- **`ch4_preprocessing_pipeline_v2`** (ratio 4.45) is too wide to place, and is
  superseded in substance by `ch4_data_pipeline_v1`. Retire or fix — a Phase 5
  citation decision, not a layout fix.
- **SRQ2's `synthesis.csv` / `synthesis_summary.md`** are cited by Ch7 §7.2 but
  have no live producer. Restore `srq2_synthesis.py` or withdraw the numbers.
- **The horizon blocker** is unchanged: `engineer_features()` never receives the
  horizon, so h1 and h3 encode the same one-month task (P0048 F1 / P0049 F22).
  The data-reduction table's horizon column carries a DO-NOT-PUBLISH warning
  until that lands.

---

## Related

- `plans/P0050_…/findings.md` — F19–F25, the full reasoning including what was
  tried and rejected
- `.claude/rules/figure-generation-standards.md` — the figure contract
- `PATHS.py` — `CHAPTER_SLUGS`, `CHAPTER_ORDER`, `get_chapter_*_dir()`
- `05_thesis_results/APPENDIX_TABLES.md` — which table sits in which chapter
