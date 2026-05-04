# Preprocessing Pipeline Analysis

**Date:** 2026-05-04  
**Plan:** P0019 Preprocessing Unification  
**Status:** Analysis phase

---

## Executive Summary

The thesis project has **5 independent preprocessing scripts** + **2 superseded variants**:

| Script | Data Source | Path Pattern | Status | Notes |
|--------|-------------|--------------|--------|-------|
| `preprocessing_csd.py` | CSV (local) | ✅ centralized (paths.py) | **ACTIVE** | Modern, validated |
| `preprocessing_energidrikke.py` | CSV (local) | ✅ centralized (paths.py) | **ACTIVE** | Modern, validated |
| `preprocessing_danskvand.py` | CSV (local) | ✅ centralized (paths.py) | **ACTIVE** | Modern, validated |
| `preprocessing_rtd.py` | CSV (local) | ✅ centralized (paths.py) | **ACTIVE** | Modern, validated |
| `preprocessing_totalbeer.py` | CSV (local) | ✅ centralized (paths.py) | **ACTIVE** | Modern, validated |
| `preprocessing.py` | SQL (Fabric) | ❌ hardcoded parents[4] | **OBSOLETE** | Old database variant, unused |
| `preprocessing_csd_old.py` | SQL (Fabric) | ❌ hardcoded parents[4] | **OBSOLETE** | Duplicate of preprocessing.py |

**Key Finding:** All **active scripts use centralized paths.py** (CLAUDE.md discovery pattern). No fallback SQL query exists in modern scripts — they assume CSV data pre-downloaded via `save_all_datasets.py`.

---

## Key Findings

### Path Centralization Status ✅

**Modern Scripts (CSV-based):**
- Dynamic CLAUDE.md discovery: **YES** (lines 38-50 in preprocessing_csd.py)
- Centralized paths.py imports: **YES** (lines 55-60)
- Use THESIS_DATA_NIELSEN_CSV_DIR: **YES** (line 77)
- Use THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR: **YES** (line 80)
- Output path validation: **YES** (explicit mkdir at line 81)

**Obsolete Scripts (SQL-based):**
- Dynamic root discovery: NO (hardcoded `parents[4]`)
- Centralized paths.py imports: NO (use raw SQL)
- Output paths: Hardcoded to `results/phase1/` (not in paths.py)

### Data Access Pipeline

```
Nielsen Fabric Warehouse (RU_* .env credentials)
    ↓
save_all_datasets.py (thesis/data/raw_nielsen/data_csv/)
    ↓
Preprocessing Scripts (CSD, energidrikke, danskvand, RTD, totalbeer)
    ↓
thesis/data/preprocessing/parquet_nielsen/ (feature matrices)
```

### Path Fixes Applied

**save_all_datasets.py output path mismatch:**
- **Before:** `OUTPUT_DIR = Path(__file__).resolve().parents[2] / ".csv"` → thesis/data/.csv
- **After:** `OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data_csv"` → thesis/data/raw_nielsen/data_csv ✓

**Now aligns with:** `THESIS_DATA_NIELSEN_CSV_DIR` in paths.py ✓

---

## Architecture Decisions

1. **CSV-first approach:** Scripts assume CSV data pre-downloaded via save_all_datasets.py
2. **No SQL fallback:** Decouples preprocessing from database credentials
3. **Dynamic root discovery:** Works from any directory using CLAUDE.md pattern
4. **Centralized path imports:** All 5 scripts use same paths.py definitions

---

## Deleted Files

- `preprocessing.py` — Old SQL variant (obsolete)
- `preprocessing_csd_old.py` — Duplicate of above (obsolete)

---

## Created/Modified Files

**New:**
- `run_all_preprocessing.py` — Unified runner (orchestrates 5 categories)

**Modified (all use centralized paths.py + dynamic root discovery):**
- `preprocessing_csd.py`
- `preprocessing_energidrikke.py`
- `preprocessing_danskvand.py`
- `preprocessing_rtd.py`
- `preprocessing_totalbeer.py`
- `thesis/data/raw_nielsen/scripts/save_all_datasets.py` (path fix)

---

## Summary

✅ **All 5 active scripts now use centralized paths**  
✅ **Unified runner successfully orchestrates all categories**  
✅ **Path mismatch in save_all_datasets.py fixed**  
✅ **obsolete SQL variants deleted**  

Ready for production use.

