---
pid: P0025
created: 2026-06-30 14:50:00
updated: 2026-06-30 14:50:00
status: in_progress
focus_detail: "Re-fetch full Nielsen history from Fabric warehouse and rebuild all 5 preprocessing pipelines"
---

# P0025 — Nielsen Full Re-Fetch + Pipeline Rebuild

## Problem

Local JSONL/parquet cache only has ~11 months of data (2025-07 to 2026-05).
Warehouse has 39–44 months per category. Step 3 (filter_series, requires ≥40 non-zero periods)
eliminates all brands → 0 rows output.

## Warehouse Coverage (confirmed via diagnostic)

| Category | Rows | Periods | Range |
|---|---|---|---|
| CSD | 9,824,601 | 44 | 2022-10 → 2026-05 |
| Energidrikke | 3,290,631 | 41 | 2023-01 → 2026-05 |
| Totalbeer | 16,292,742 | 41 | 2023-01 → 2026-05 |
| Danskvand | 1,315,542 | 39 | 2023-03 → 2026-05 |
| RTD | 2,299,796 | 39 | 2023-03 → 2026-05 |

## Tasks (IDs 7–10, sequential)

### T-7 — Re-fetch JSONL ← START HERE
```
python thesis/data/_00_raw/nielsen/scripts/save_all_datasets.py
```
- Views + metadata only (~10 min)
- Verify: MANIFEST.json shows CSD facts ~9.8M rows

### T-8 — Convert JSONL → parquet
```
python thesis/data/_01_converted/nielsen/jsonl_to_parquet/run_all_conversions.py --force
```
- --force bypasses skip-if-newer check
- Verify: parquet files updated, CSD facts parquet substantially larger

### T-9 — Review MIN_PERIODS thresholds (before pipeline run)
- Files: `thesis/data/_02_preprocessing/nielsen/{Danskvand,RTD}/pre_*_3_filter_series.py`
- Danskvand + RTD only have 39 periods → may need threshold lowered from 40 to 36
- Energidrikke + Totalbeer have 41 periods → may be fine at 40
- CSD has 44 → fine

### T-10 — Run full preprocessing pipeline
```
python thesis/data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py
python thesis/data/_02_preprocessing/nielsen/Danskvand/preprocessing_danskvand.py
python thesis/data/_02_preprocessing/nielsen/Energidrikke/preprocessing_energidrikke.py
python thesis/data/_02_preprocessing/nielsen/RTD/preprocessing_rtd.py
python thesis/data/_02_preprocessing/nielsen/Totalbeer/preprocessing_totalbeer.py
```
- Verify: non-zero feature matrices in `thesis/data/_03_engineered/nielsen/{CATEGORY}/`

## Dependency Chain

T-7 → T-8 → T-9 → T-10  (strictly sequential)
