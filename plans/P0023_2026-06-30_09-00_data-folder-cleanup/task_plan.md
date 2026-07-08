---
pid: P0023
created: 2026-06-30 09:00:00
updated: 2026-06-30 09:00:00
status: complete
completed: 2026-06-30 09:30:00
outcome_summary: "All 8 tasks executed. CSD good data (2666 rows, 62 brands) now in _03_engineered. All stale engineered/ copies deleted from _02_preprocessing. Orphan Energidrikke metadata moved to _01_converted. _02_preprocessing now contains only scripts + pipeline_step_outputs/."
---

# P0023: Data Folder Cleanup

**Objective:** Resolve content-verified file placement issues discovered during the 2026-06-30 audit of `thesis/data/`. Ensure `_03_engineered/` is the single canonical destination for final outputs, and `_02_preprocessing/` contains only scripts + intermediate step caches.

## Context

4-tier data hierarchy is in place and correct in PATHS.py. The problems are stale/misplaced *data files*, not code:

1. **CSD output is split across two locations** — `_02_preprocessing/.../CSD/engineered/` has the good 62-brand feature matrix (372KB); `_03_engineered/CSD/` has a corrupt empty run (10KB, 0 rows). Need to overwrite _03 with _02 content.
2. **Danskvand / Energidrikke / RTD have byte-identical copies** in both `_02_preprocessing/.../engineered/` and `_03_engineered/` — safe to delete the _02 copies.
3. **Stray parquet caches inside `_02_preprocessing/`** — CSD metadata (identical to _01_converted), Energidrikke views/metadata (different column counts — _01_converted is more complete). One Energidrikke metadata file is missing from _01_converted and must be moved.
4. **Branch strategy** — all changes on `chore/data-folder-cleanup` branch before committing.

## Tasks

| ID | Title | Phase | Blocked By |
|----|-------|-------|------------|
| T-001 | Create feature branch | setup | — |
| T-002 | Move good CSD outputs from _02 to _03 | core | T-001 |
| T-003 | Delete stale _02 engineered copies (Danskvand, Energidrikke, RTD) | core | T-001 |
| T-004 | Move orphan Energidrikke metadata to _01_converted | core | T-001 |
| T-005 | Delete stray CSD metadata parquets from _02 | core | T-001 |
| T-006 | Delete stray Energidrikke views+metadata from _02 | core | T-004 |
| T-007 | Verify _03_engineered CSD data is readable and correct | testing | T-002 |
| T-008 | Update P0022 and P0017 plan files with cleanup outcome | docs | T-002–T-006 |

## File Decision Table (content-verified)

| File | _02 | _03 | Action |
|------|-----|-----|--------|
| CSD/engineered/csd_feature_matrix.parquet | 372KB, 62 brands ✅ | 10KB, 0 rows ❌ | Copy _02 → _03, delete _02 |
| CSD/engineered/csd_series_index.csv | 62 brands ✅ | header only ❌ | Copy _02 → _03, delete _02 |
| CSD/engineered/csd_split_dates.json | train_start=2022-10 ✅ | "unknown" ❌ | Copy _02 → _03, delete _02 |
| CSD/engineered/csd_preprocessing_report.md | Full data ✅ | 0 brands ❌ | Copy _02 → _03, delete _02 |
| Danskvand/engineered/* | Identical to _03 | Identical to _02 | Delete _02 copies |
| Energidrikke/engineered/* | Identical to _03 | Identical to _02 | Delete _02 copies |
| RTD/engineered/* | Identical to _03 | Identical to _02 | Delete _02 copies |
| CSD/metadata/*.parquet (4 files) | Identical to _01_converted | — | Delete _02 copies |
| Energidrikke/views/*.parquet (3 files) | Fewer cols than _01 | — | Delete _02 copies (_01 is canonical) |
| Energidrikke/metadata/metadata_energidrikke_columns.parquet | Only copy | — | Move → _01_converted |

## Success Criteria

- `_03_engineered/nielsen/CSD/csd_feature_matrix.parquet` has 2,666 rows, 62 brands
- No `engineered/` subfolders remain inside `_02_preprocessing/`
- No `views/` or `metadata/` parquet files remain inside `_02_preprocessing/`
- `_01_converted/nielsen/parquet_nielsen/Energidrikke/metadata/metadata_energidrikke_columns.parquet` exists
- All pre_*_6_save_outputs.py scripts unchanged (they already write to _03_engineered correctly)
