---
name: 2026-08-18_DOC-stale-file-inventory
description: DOC - Inventory of stale pipeline artifacts superseded by the P0038 shared pipeline, with disposition and evidence for each group
category: reference
applies-to: [02_thesis_data, 03_thesis_modelling]
triggers: [repo cleanup, task 9, retire notebook, delete stale outputs]
created: 2026_08_18-21_30
updated: 2026_08_18-21_30
---

# Stale File Inventory — P0038

Built while running the pipeline, so the evidence for each call is recorded at
the moment it was observed rather than reconstructed later.

**Scope**: artifacts superseded by the shared pipeline. Deliberate `.archive/`
trees are covered separately at the bottom — they are decision evidence, not
debris, and are a different question.

**Nothing here is deleted yet.** This is the worklist for task 9.

## The rule that separates live from stale

Not every un-suffixed file is stale, and this is the trap:

| Step | Horizon-dependent? | Writes `step_N_log.json`? | Un-suffixed file is |
|------|--------------------|---------------------------|---------------------|
| 0 | no | **yes** (live) | **LIVE** |
| 1 | no | **yes** (live) | **LIVE** |
| 2 | no | no | stale |
| 3-6 | yes | no (writes `_h{N}` variants) | stale |

Steps 0 and 1 legitimately write un-suffixed logs because they do not depend on
the horizon. Steps 2-6 do not write `step_N_log.json` at all any more — that was
the notebook's convention. **Verified in source**, not inferred from dates.

## Groups

### 1. `step_N_log.json` for steps 2-6 — 20 files, all 4 categories

```
{CSD,Danskvand,Energidrikke,RTD}/pipeline_step_outputs/step_{2,3,4,5,6}_log.json
```

Dated 2026-07-11/16. **Evidence**: no current step module writes this filename;
steps 4 and 5 write `step_N_log_h{1,3}.json` instead, which sit alongside them
dated today. All 20 tracked in git.

**Disposition: DELETE.** Superseded by the `_h{N}` variants; contain no decision
evidence.

**Do NOT touch `step_0_log.json` / `step_1_log.json`** — both live, dated today.

### 2. CSD `*_bymonth.parquet` for steps 2-5 — 4 files, 0.8 MB

```
CSD/pipeline_step_outputs/step_{2_calendar_filled,3_filtered_series,4_engineered_features,5_split_applied}_bymonth.parquet
```

Dated 2026-07-13. Notebook-era intermediates: 140/58 brands, pre-re-pull,
pre-DEC-SCOPE. Untracked (0/4 in git).

**Disposition: DELETE.** Actively misleading — they look like current pipeline
output and are not.

**Correction to F68**: that finding called all `*_bymonth.parquet` files stale.
Wrong. **`step_1_aggregate_bymonth.parquet` is LIVE** in all four categories
(dated today) — its suffix comes from `GRAIN`, the brand x month modelling
grain, not from the notebook. Only the four CSD steps 2-5 files are stale.

### 3. `csd_eda_plots_bymonth/` — 7 PNGs, 1.1 MB

Dated 2026-07-13, tracked. Superseded by `csd_eda_plots/`, regenerated today.

**Disposition: DELETE** (regenerable from step 2 in ~43s).

### 4. Un-suffixed EDA findings — 2 files

```
CSD/pipeline_step_outputs/csd_eda_findings.json
CSD/pipeline_step_outputs/csd_eda_findings_bymonth.json
```

Superseded by `csd_eda_findings_h{1,3}.json`. **Disposition: DELETE.**

### 5. Un-suffixed engineered outputs — 7 files, 0.4 MB

```
CSD/csd_feature_matrix.parquet      CSD/csd_series_index.csv
CSD/csd_split_dates.json            CSD/csd_preprocessing_report.md
{Danskvand,Energidrikke,RTD}/*_split_dates.json
```

Dated 2026-07-11/16 in `02_thesis_data/_03_engineered/bymonth/`.

**Disposition: DELETE — but ONLY after the 12 downstream consumers are
repointed.** These are exactly the files F65's scripts still read. Deleting
first breaks the modelling layer.

`csd_feature_matrix.parquet` is also the **parity baseline** for F68. Preserve a
copy under the plan folder before deleting, so the gate stays reproducible.

### 6. The notebook and its export — 2 files, 1.1 MB

```
CSD/pipeline_step_scripts/pre_processing_notebook_csd.ipynb
CSD/pipeline_step_scripts/pre_processing_notebook_csd.py
```

**Disposition: ARCHIVE, do not delete.** This is the artifact P0038 replaced and
the source of the parity baseline. Move to
`CSD/pipeline_step_scripts/.archive/2026-08-18_superseded_by_shared_pipeline/`,
matching the pattern the other three categories already use.

## Summary

| # | Group | Files | MB | Disposition |
|---|-------|------:|---:|-------------|
| 1 | `step_N_log.json` steps 2-6 | 20 | ~0 | delete |
| 2 | CSD `*_bymonth.parquet` steps 2-5 | 4 | 0.8 | delete |
| 3 | `csd_eda_plots_bymonth/` | 7 | 1.1 | delete |
| 4 | un-suffixed EDA findings | 2 | ~0 | delete |
| 5 | un-suffixed engineered outputs | 7 | 0.4 | delete **after** F65 repoint |
| 6 | notebook + export | 2 | 1.1 | **archive** |
| | **total** | **42** | **3.4** | |

Small in bytes; the value is removing files that can be **mistaken for current
output**. Group 2 is the clearest case — a stale feature matrix that looks live
is how a wrong number reaches a thesis table.

## Ordering constraint

```
repoint the 12 F65 consumers  ->  delete group 5  ->  archive group 6
```

Groups 1-4 can go at any time; they have no consumers.

## Already archived — no action

Three categories archived their per-category step scripts on 2026-08-18:

```
{Danskvand,Energidrikke,RTD}/.archive/2026-08-18_superseded_by_shared_pipeline/
```

CSD's older modularised scripts are already at
`CSD/pipeline_step_scripts/.archive/2026_07_13-16_02 - Previous Modularized Step Scripts/`.

`__pycache__` is correctly gitignored (0 tracked) — leave it.

## Deliberate archives — out of scope, flagged for a separate decision

Roughly **400 MB** of tracked `.archive/` trees exist. They are **not** part of
this cleanup: they carry decision evidence, and the repo rules require archiving
rather than deleting such material.

| Path | Size | Tracked |
|------|-----:|--------:|
| `./.archive` | 187 MB | 154 files |
| `plans/.archive` | 168 MB | 167 files |
| `user-docs/.archive` | 24 MB | 23 files |
| `utility_scripts/tests/.archive` | 3 MB | — |

Largest single items: `thesis_agents_preintegration` (90 MB),
`Thesis_obsidian_backup` (39 MB), `enrico_legacy_reports_2026-07` (15 MB).

**Worth a separate conversation**: `Thesis_obsidian_backup` in particular looks
like a backup of a backup, and git already provides history for anything ever
committed. But that is Brian's call, not a pipeline-cleanup decision, and the
size is a repo-weight question rather than a correctness one.
