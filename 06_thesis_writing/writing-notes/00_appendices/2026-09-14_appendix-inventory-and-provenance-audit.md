---
name: 2026-09-14_appendix-inventory-and-provenance-audit
description: NOTE - Full inventory of every generated table, figure and diagram in 05_thesis_results, with the producer that writes it, when it was last regenerated, and whether the thesis can reach it. The master analysis; per-chapter citation recommendations live in each chapter's own folder.
category: reference
applies-to: [appendix, all chapters, 05_thesis_results]
triggers: [which appendices do we have, is this figure stale, what can we cite, appendix placement, regenerating the results tree]
created: 2026_09_14-11_40
updated: 2026_09_14-11_40
snapshot: 2026-09-13_21-30_book-citations-pass
status: findings - citation recommendations routed per chapter
---

# Appendix inventory and provenance audit

Every script that writes into `05_thesis_results/`, when its output was last
regenerated, and what the thesis document can actually reach.

Audited 2026-09-14 against the working tree at `41ecb76`, snapshot
`2026-09-13_21-30_book-citations-pass`, and the funded run of 2026-09-12
(19:18-21:06, 63 runs, schema `v6-shared-composition+af04a42a478b`).

**This file is the analysis.** The recommendations on *where each artefact
should be cited* are split per chapter, under each chapter's own note folder,
because that is where they get applied. See [Where the recommendations
live](#where-the-recommendations-live) at the end.

---

# The verdict first

| | |
|---|---|
| Generated files in the results tree | **242** |
| Scripts writing into it | **36** |
| Appendix tables on disk | **24** |
| Appendix tables the document declares | **1** |
| Figures on disk (excluding EDA) | **15** |
| Figures the document declares | **2** |
| EDA plots on disk | **30** |
| EDA plots referenced anywhere in prose | **0** |

**One artefact is factually wrong.** The scenario figure describes an experiment
that no longer exists. Everything else is either current or stale in a way that
does not yet assert a falsehood.

**The larger finding is reach, not staleness.** The work exists and the document
cannot get to it. Twenty-three of twenty-four appendix tables are reachable only
by opening the repository, and no chapter references a figure by number.

---

# 1. The one artefact that is wrong

## `ch7_scenarios_v2.svg` — draws five scenarios, seven ran

Rendered 2026-09-10 19:27. The experiment was redesigned and run 2026-09-12.

Its generator hardcodes a five-rung ladder and marks D and E dashed. The caption
then explains why, and the explanation is false:

> "Scenarios D and E repeat that final comparison inside the production engine
> and are shown dashed: they are specified but not executed here, since the
> engine is proprietary."

Both were executed, nine times each, in the same funded set as the rest.

| The figure asserts | `runs.csv`, 63 funded runs |
|---|---|
| A, B, C drawn solid | A 9, B 9, C 9 |
| D, E drawn dashed, "not executed" | D 9, E 9 |
| F, G absent entirely | F 9, G 9 |

Chapters 6, 8, 9 and 10 all say "seven scenarios", and Chapter 6 §6.7 carries
the full seven-row table with the correct identifiers. **The prose is right and
the figure is wrong.**

It is also the only one of the twelve architecture diagrams that reads no data
at all. The other eleven pull counts, winners and memory profiles from artefacts
at render time, which is exactly why they survived the re-run and this one did
not.

**Fix:** `fig_scenarios()` in `generate_architecture_diagrams.py` should read the
`SCENARIOS` tuple from `srq4_experiment.py:1291`, which is already the single
source of truth for the harness.

## `ch6_layered_architecture_v2.svg` — the scenario block uses retired vocabulary

Its scenario stack is typed as *"Plain agent / Agent + data & code / Agent +
models"*, the three-scenario vocabulary retired on 2026-09-11. The rest of the
figure is sourced live from `profiling()`, `ladder()` and `served()`, so only
this one block is stale.

This matters more than its size suggests: **Figure 2 is one of only two figures
the document cites at all.**

---

# 2. Generated prose that stopped explaining at C

Two appendix tables carry seven columns of correct data underneath a note that
describes three scenarios. The data regenerated on 2026-09-13; the sentence
above it did not, because it is typed into the exporter.

## `11_scenario_comparison.md`

`export_appendix.py:980`:

> "The scenarios form an information ladder: A has no access to firm data, B may
> execute code against it, and C additionally calls the dedicated forecasting
> model."

Accurate as far as it goes, and it stops four scenarios early. D, E, F and G
appear in the table and go unexplained.

## `13_interval_communication.md` — two naming systems in one header

Its columns read `A - no firm data`, `B - code execution`, `C - dedicated
model`, then switch to `D_prometheus_data`, `E_prometheus_model`,
`F_llm_data_model`, `G_prometheus_data_model`.

**Corrected attribution.** My first pass blamed `export_appendix.py:902`. That
was wrong: `HDR` there is an empty dict and every use is `HDR.get(s, s)`, so the
exporter falls through to the raw identifier and renders faithfully.

The actual cause was a three-entry relabel map at
`score_interval_communication.py:113`, applied **when the CSV was written** —
it rewrote A, B and C and left D through G alone. The exporter never saw seven
consistent names because it was never given them.

Worth recording as a general lesson: **the table is not always written by the
script that formats it.** A defect visible in generated output can live one
stage upstream, and the formatter will reproduce it perfectly.

---

# 3. The producer census

Thirty-six scripts write into the results tree. `P0050/START_HERE.md` lists
**nine**, which is why re-running "everything" has been leaving artefacts behind.

## Figure and diagram producers

| Producer | Script mtime | Output mtime | Provenance |
|---|---|---|---|
| `generate_architecture_diagrams.py` (12 diagrams) | 09-10 19:18 | 09-10 19:27 | 9 read live data, 1 fully typed, 2 conceptual |
| `generate_methodology_diagram.py` | 09-10 19:18 | 09-10 19:27 | parsed from the chapter snapshot |
| `srq1_generate_performance_figures.py` | 09-10 18:12 | 09-10 19:04 | reads `metrics.csv`; model ladder typed |
| `srq1_generate_shap_figures.py` | 09-10 18:12 | 09-10 19:04 | pinned to the tuned XGBoost config |
| `step_2_eda_descriptive.py` (30 plots) | 09-10 18:12 | 09-10 18:13 | computed per category |

## Table and appendix producers

| Producer | Script mtime | Output mtime | Covers |
|---|---|---|---|
| `export_appendix.py` | 09-13 18:37 | 09-13 18:18 | tables 01-15 and the appendix index |
| `srq1_residual_diagnostics.py` | 09-14 11:00 | 09-14 11:00 | Ljung-Box gate — **newest artefact** |
| `srq1_export_enrichment_appendix.py` | 09-10 19:23 | 09-10 19:27 | tables 94-99 |
| `export_holiday_appendix.py` | 09-10 19:23 | 09-10 19:27 | tables 90-93 |
| `generate_literature_table.py` | 09-10 19:23 | 09-10 19:27 | table 89 |
| `training_report.py` | 09-10 19:23 | 09-10 19:27 | `training_report.md` |
| `srq1_baselines_stat.py`, `srq1_ridge_pooled.py`, `srq1_pooled_perbrand.py`, `srq1_benchmark*.py`, `srq1_calibration.py`, `srq1_stability.py` + 12 more | 09-07 → 09-12 | 09-09 → 09-11 | the SRQ1 benchmark table set |
| `score_interval_communication.py`, `export_scenario_inputs.py`, `srq4_experiment.py` | 09-13 18:37 | 09-13 18:18 | SRQ4 scoring and inputs |

**The SRQ1 artefacts predating the funded run is expected, not a defect.** The
models were trained before the experiment that consumes them, and the binaries
are unchanged since 09-09 21:10. What matters is that **no figure was
re-rendered after 2026-09-13**, when six tables changed.

## Figure provenance, in full

Nine of twelve read live data through the `profiling()`, `ladder()`, `served()`
and `panel_shape()` helpers.

| Figure | Reads |
|---|---|
| `ch4_raw_schema_v1` | live (`_rows`) |
| `ch4_data_pipeline_v1` | live |
| `ch4_eda_pipeline_csd_v1` | live |
| `ch4_preprocessing_pipeline_v2` | live via `panel_shape()` |
| `ch5_modelling_pipeline_v1` | live via 4 helpers |
| `ch5_model_selection_v2` | live via `profiling()`, `ladder()`, `served()` |
| `ch5_resource_profile_v2` | live via `profiling()`, `ladder()` |
| `ch6_layered_architecture_v2` | live, **except the typed scenario block** |
| `ch6_tool_interface_v1` | live via `served()` |
| `ch1_research_questions_tree_v2` | fully typed — conceptual, legitimate |
| `ch2_gap_diagram_v2` | fully typed — conceptual, interpolates the RAM envelope |
| `ch7_scenarios_v2` | **fully typed — and wrong** |

---

# 4. EDA — current and in sync

149 files, all SVG, no PNG survivors.

| Category | Tables | Plots | Last regenerated | Pipeline copy |
|---|---|---|---|---|
| CSD | 31 | 8 | 2026-09-10 18:13 | in sync |
| Energidrikke | 31 | 8 | 2026-09-10 18:14 | in sync |
| RTD | 29 | 7 | 2026-09-10 18:14 | in sync |
| Danskvand | 28 | 7 | 2026-09-10 18:14 | in sync |

The tier-05 copies match the pipeline-side originals to the minute, so
`promote_eda_artifacts()` ran at the end of the last pipeline pass as intended.
Nothing downstream of the EDA changed in the funded run, so **these do not need
regenerating.**

Danskvand and RTD have seven plots rather than eight because neither carries
promotional measures, so `07_promo_intensity_analysis.svg` is correctly absent.

---

# 5. The reach gap

| On disk | Declared in the document |
|---|---|
| 24 appendix tables | 1 appendix entry (A1, hand-drawn star schema) |
| 15 figures + 30 EDA plots | 2 figures |
| 149 EDA artefacts | 0 referenced |

- **Fifteen tables are indexed but unreferenced.** `APPENDIX_TABLES.md` lists
  tables 01-15; the Table of Appendices names only A1. They are reachable only
  by opening the repository.
- **Nine more are not even indexed.** Tables 89-99, plus `training_report`,
  `calibration`, `profiling`, `cv_summary`, `stat_baselines`,
  `residual_diagnostics`, `demand_classes`, `mase`, `pooled_summary`,
  `pooled_perbrand_summary`, `ridge_pooled`, `stability`, `summary` and
  `tuned_summary` sit outside the index entirely, because three exporters write
  tables and only one writes the index.
- **Zero figure callouts in body prose.** Across all ten chapters, no sentence
  references a figure by number. Figures 1 and 2 appear in the front matter and
  in captions only.
- **The newest artefact is already orphaned.** `residual_diagnostics.md`, written
  2026-09-14, carries the Ljung-Box gate with the Hyndman & Athanasopoulos
  degrees-of-freedom correction. No chapter mentions Ljung-Box or a portmanteau
  test.

---

# 6. What the audit cleared

Worth stating plainly, because the defects above are concentrated rather than
spread.

- **Chapter 5's benchmark table is current.** Its figures match `cv_summary.md`
  row for row, including the energidrikke 11.5 / 16.2 pair and RTD's n = 372. It
  cites the cross-validated artefact, not the tuned one — two different
  experiments, both live. An earlier reading of mine that called this stale was
  wrong.
- **Chapter 8's numbers match the funded run exactly** — 502.2, 662.1, 26.7, 69.5
  and the rest all reconcile against `11_scenario_comparison.md`.
- **Chapter 4's column counts are right and per-category**: 54 for CSD and
  energidrikke, 52 for RTD, 36 for water, with 18 and 17 model inputs. Verified
  directly against the parquet files.
- **The deployed-model figure reproduces the correct winners**: XGBoost for CSD
  and water, LightGBM for energy drinks and RTD.
- **No internal content leaked.** `check_reader_facing.py` passes across all 242
  files.

## One latent defect, not worth fixing today

`generate_architecture_diagrams.py:362` types `"54 columns"` beside a computed
row count. It is true for CSD, which is the category that figure describes, so it
states nothing false now. But it is the one count in the figure set that will not
follow the data, and three of the four categories do not have 54 columns.

---

# Where the recommendations live

The citation recommendations are grouped by chapter, in each chapter's own note
folder, because that is where they get applied:

| Chapter | Note |
|---|---|
| 1 | `ch1_introduction/2026-09-14_appendix-citations-ch1.md` |
| 2 | `ch2_literature_review/2026-09-14_appendix-citations-ch2.md` |
| 3 | `ch3_methodology/2026-09-14_appendix-citations-ch3.md` |
| 4 | `ch4_data_assessment/2026-09-14_appendix-citations-ch4.md` |
| 5 | `ch5_model_benchmark/2026-09-14_appendix-citations-ch5.md` |
| 6 | `ch6_architecture/2026-09-14_appendix-citations-ch6.md` |
| 7 | `ch7_synthesis/2026-09-14_appendix-citations-ch7.md` |
| 8 | `ch8_experiment/2026-09-14_appendix-citations-ch8.md` |
| 9 | `ch9_discussion/2026-09-14_appendix-citations-ch9.md` |

**Chapter 10 gets no note.** It owns no artefacts and should cite by reference to
earlier chapters rather than introduce an appendix at the conclusion.

## Relationship to `deferred-structural-decisions.md`

That file already carries S1-S4, which decide whether Chapter 4's **existing
body tables** stay, move or are deleted. This audit is the other direction: it
asks which **generated artefacts not yet in the document** should come in.

The two do not overlap, and the per-chapter notes defer to S1-S4 wherever a
table is already under discussion there.
