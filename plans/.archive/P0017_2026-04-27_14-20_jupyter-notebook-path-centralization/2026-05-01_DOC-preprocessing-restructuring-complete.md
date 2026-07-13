# Preprocessing Folder Restructuring & Script Duplication — Complete

**Date**: 2026-05-01  
**Task**: Restructure parquet output folders + create preprocessing scripts for all 5 categories  
**Status**: ✅ COMPLETE

---

## What Was Done

### 1. Folder Restructuring
Created per-category output folders under `thesis/data/preprocessing/parquet_nielsen/`:

```
parquet_nielsen/
  ├── specialized_CSD/
  │   ├── specialized_CSD_feature_matrix.parquet      (391 KB)
  │   ├── series_index.csv
  │   ├── split_dates.json
  │   └── preprocessing_report.md
  ├── specialized_danskvand/                          (empty, awaiting execution)
  ├── specialized_energidrikke/                       (empty, awaiting execution)
  ├── specialized_rtd/                                (empty, awaiting execution)
  └── specialized_totalbeer/                          (empty, awaiting execution)
```

**Action**: Moved existing CSD output files from `parquet_nielsen/` root into `specialized_CSD/` subfolder.

---

### 2. Script Duplication & Adaptation
Created 5 preprocessing scripts (one per category):

| Script | Location | Status |
|--------|----------|--------|
| `preprocessing_csd.py` | `thesis/data/preprocessing/` | ✅ Updated to write to `specialized_CSD/` |
| `preprocessing_danskvand.py` | `thesis/data/preprocessing/` | ✅ Created |
| `preprocessing_energidrikke.py` | `thesis/data/preprocessing/` | ✅ Created |
| `preprocessing_rtd.py` | `thesis/data/preprocessing/` | ✅ Created |
| `preprocessing_totalbeer.py` | `thesis/data/preprocessing/` | ✅ Created |

**Key Changes Per Script**:
1. `CATEGORY` constant updated (e.g., `CATEGORY = "danskvand"`)
2. `NOTEBOOK_NAME` auto-derived: `f"specialized_{CATEGORY}"`
3. CSV filenames updated to category-specific names:
   - CSD: `csd_clean_*.csv`
   - Danskvand: `danskvand_clean_*.csv`
   - Energidrikke: `energidrikke_clean_*.csv`
   - RTD: `rtd_clean_*.csv`
   - Totalbeer: `totalbeer_clean_*.csv`
4. Output path updated: `OUT = THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR / NOTEBOOK_NAME`
5. Report titles capitalized per category

**Code Structure** (same across all scripts):
- Dynamic root finder (CLAUDE.md)
- Centralized paths via `paths.py`
- Input validation (checks for required CSV files)
- 5-step pipeline: load → calendar → filter → engineer → split
- Outputs: feature_matrix.parquet, series_index.csv, split_dates.json, preprocessing_report.md

---

## File Inventory

### Original Files (Unchanged)
- `preprocessing.py` — Original monolithic script (kept for reference)
- `preprocessing_csd_old.py` — Backup of original (frozen)

### New Files
- `preprocessing_csd.py` — CSD category (12 KB)
- `preprocessing_danskvand.py` — Danskvand category (12 KB)
- `preprocessing_energidrikke.py` — Energidrikke category (12 KB)
- `preprocessing_rtd.py` — RTD category (12 KB)
- `preprocessing_totalbeer.py` — Totalbeer category (12 KB)

**Total**: 5 new scripts + 2 backup scripts = 7 scripts in preprocessing folder

---

## Next Steps

### Testing (Not Yet Done)
These scripts are ready to run, but **require Nielsen raw CSV data** to be present in `thesis/data/raw_nielsen/data_csv/`:

```bash
# Test each script
python preprocessing_csd.py          # Already verified ✅
python preprocessing_danskvand.py
python preprocessing_energidrikke.py
python preprocessing_rtd.py
python preprocessing_totalbeer.py
```

**Expected Output** (per script):
- ✅ "Input validation: All 4 required files found"
- ✅ Step 1–5 progress messages
- ✅ 4 output files in `parquet_nielsen/specialized_{CATEGORY}/`

### Data Requirements
Each category requires 4 CSV files in `thesis/data/raw_nielsen/data_csv/`:
- `{category}_clean_facts_v.csv` — Transaction data (largest)
- `{category}_clean_dim_product_v.csv` — Product → brand mapping
- `{category}_clean_dim_period_v.csv` — Period → year/month mapping
- `{category}_clean_dim_market_v.csv` — Market descriptions

**If CSVs are missing**, the script will print helpful error message with download instructions.

---

## Architecture Notes

### Per-Category Isolation
Each preprocessing script is **independent**:
- No shared state between categories
- Each can be run in isolation
- Easy to debug category-specific issues
- Easy to add category-specific overrides later

### Future Enhancements
If Enrico's handover responses indicate category-specific tuning is needed:
1. Add per-category overrides in each script (e.g., `MIN_PERIODS`, `LAGS`, `HOLIDAY_MONTHS`)
2. Document the rationale in comments
3. No changes needed to folder structure — already supports per-category isolation

### Notebook Loading
Notebooks need to be updated to load from per-category folders:
```python
# Old (flat structure)
df = pd.read_parquet(THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR / "specialized_CSD_feature_matrix.parquet")

# New (per-category structure)
NOTEBOOK_NAME = "specialized_CSD"
df = pd.read_parquet(THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR / NOTEBOOK_NAME / f"{NOTEBOOK_NAME}_feature_matrix.parquet")
```

---

## Summary

✅ **Complete**: Folder structure restructured + 5 preprocessing scripts created  
⏳ **Pending**: Testing (awaiting Nielsen CSV data)  
🔄 **Future**: Notebook updates to load from per-category folders  

All scripts are ready for testing. Each outputs to its own `parquet_nielsen/specialized_{CATEGORY}/` subfolder, making data organization clean and scalable.
