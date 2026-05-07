# Implementation Summary: Nielsen Data Organization & Preprocessing Pipeline

**Date:** 2026-05-05  
**Status:** Complete  
**Branch:** chore/folder-cleanup

---

## What Was Implemented

### 1. **PATHS.py — Category & Type-Specific Helpers** ✅

**File:** `C:\dev\thesis-manifold\PATHS.py`

Added 5 new helper functions for accessing Nielsen data by category and type:

```python
def get_category_parquet_dir(category: str) -> Path
def get_category_raw_dir(category: str) -> Path
def get_category_views_dir(category: str) -> Path
def get_category_metadata_dir(category: str) -> Path
def get_category_engineered_dir(category: str) -> Path
```

**Usage:**
```python
from PATHS import get_category_engineered_dir
eng_dir = get_category_engineered_dir("CSD")
df = pd.read_parquet(eng_dir / "csd_feature_matrix.parquet")
```

**Benefits:**
- Clean, discoverable API
- Consistent naming across all 5 categories
- Type-safe (no string concatenation)

---

### 2. **save_all_datasets.py — Reorganized CSV Output** ✅

**File:** `C:\dev\thesis-manifold\thesis\data\raw_nielsen\scripts\save_all_datasets.py`

**Changed:** Flat CSV structure → Organized by category and type

**Before:**
```
data_csv/
  csd_clean_facts_v.csv
  csd_clean_facts.csv
  metadata_csd_columns.csv
  danskvand_clean_facts_v.csv
  ... (all mixed together)
```

**After:**
```
data_csv/
  CSD/
    ├─ views/              (csd_clean_facts_v.csv, etc.)
    ├─ raw/                (csd_clean_facts.csv, etc.)
    └─ metadata/           (metadata_csd_*.csv, etc.)
  Danskvand/
    ├─ views/
    ├─ raw/
    └─ metadata/
  Energidrikke/
    ...
```

**Implementation:**
- Refactored `main()` to iterate categories and types
- Creates directories: `category / (views | raw | metadata)`
- Maintains original filename convention from Nielsen
- Manifest still generated at output root

---

### 3. **preprocessing_csd.py — Load Raw, Save All Three Types** ✅

**File:** `C:\dev\thesis-manifold\thesis\data\preprocessing\preprocessing_csd.py`

**Major changes:**

#### a) Input paths now use new structure
```python
# Before:
INPUT_DIR = THESIS_DATA_NIELSEN_CSV_DIR

# After:
INPUT_RAW_DIR = THESIS_DATA_NIELSEN_CSV_DIR / CATEGORY / "raw"
INPUT_VIEWS_DIR = THESIS_DATA_NIELSEN_CSV_DIR / CATEGORY / "views"
INPUT_METADATA_DIR = THESIS_DATA_NIELSEN_CSV_DIR / CATEGORY / "metadata"
```

#### b) Load from raw tables (not views)
```python
# Before: load_raw() used csd_clean_facts_v.csv (views)
# After: load_raw() uses csd_clean_facts.csv (raw)
```

**Rationale:** Raw tables preserve all columns for statistical feature reduction and correlation analysis.

#### c) Output organized by type
```python
OUT_RAW = get_category_raw_dir(CATEGORY)
OUT_VIEWS = get_category_views_dir(CATEGORY)
OUT_METADATA = get_category_metadata_dir(CATEGORY)
OUT_ENGINEERED = get_category_engineered_dir(CATEGORY)
```

**Directory structure:**
```
preprocessing/parquet_nielsen/
  CSD/
    ├─ raw/              (csd_clean_facts.parquet, etc.)
    ├─ views/            (csd_clean_facts_v.parquet, etc.)
    ├─ metadata/         (metadata_csd_*.parquet, etc.)
    └─ engineered/       (csd_feature_matrix.parquet, csd_series_index.csv, etc.)
```

#### d) New output naming (simplified)

| Type | Old | New |
|------|-----|-----|
| **Feature matrix** | `specialized_CSD_feature_matrix.parquet` | `csd_feature_matrix.parquet` |
| **Series index** | (in root) | `csd_series_index.csv` |
| **Split dates** | (in root) | `csd_split_dates.json` |
| **Report** | (in root) | `csd_preprocessing_report.md` |

#### e) New function: save_dimension_tables()

Caches raw/views/metadata as parquet (one-time setup during preprocessing):

```python
def save_dimension_tables(input_raw_dir, input_views_dir, input_metadata_dir):
    """Save Nielsen dimensions as parquet for caching and reference."""
    # Saves 4 raw tables, 4 view tables, 5 metadata tables
```

Called as **Step 0** in pipeline (before feature engineering).

#### f) Renamed save_outputs() → save_engineered_outputs()

New function explicitly saves to `engineered/` subdirectory with simplified naming.

#### g) Updated pipeline steps

**Before:** 5 steps  
**After:** 6 steps

```
0. Cache Nielsen data (raw/views/metadata) as parquet
1. Load raw data
2. Build calendar index
3. Filter short series
4. Engineer features
5. Apply split labels
6. Save engineered outputs
```

---

## File Changes Summary

| File | Changes | Impact |
|------|---------|--------|
| **PATHS.py** | +91 lines (5 helpers) | Import-friendly API |
| **save_all_datasets.py** | Refactored main() | New CSV folder structure |
| **preprocessing_csd.py** | Refactored paths, added 2 new functions | Raw table loading, organized output |

---

## Directory Structure (After Implementation)

```
C:\dev\thesis-manifold\
  thesis/
    data/
      raw_nielsen/
        data_csv/
          CSD/
            ├─ raw/           ← Nielsen base tables (CSV)
            ├─ views/         ← Nielsen cleaned views (CSV)
            └─ metadata/      ← Nielsen schema documentation (CSV)
          Danskvand/
            ├─ raw/
            ├─ views/
            └─ metadata/
          ... (3 more categories)
        
      preprocessing/
        parquet_nielsen/
          CSD/
            ├─ raw/           ← Cached Nielsen raw tables (Parquet)
            ├─ views/         ← Cached Nielsen views (Parquet)
            ├─ metadata/      ← Cached schema documentation (Parquet)
            └─ engineered/    ← Preprocessed features (Parquet, CSV, JSON, MD)
          Danskvand/
            ├─ raw/
            ├─ views/
            ├─ metadata/
            └─ engineered/
          ... (3 more categories)
```

---

## Data Usage & Rationale

### Raw Tables (Base Tables)
- **Source:** Nielsen Fabric base tables (no `_v` suffix)
- **Columns:** Full set (39+ columns)
- **Use case:** Feature engineering (load raw → apply statistical filtering)
- **Preserved:** Audit metadata (last_server_update, pipeline_run_id, etc.)

### Views (Cleaned Data)
- **Source:** Nielsen Fabric views (`_v` suffix)
- **Columns:** Reduced set (10 columns)
- **Use case:** Reference, validation, quick analysis
- **Dropped:** Audit metadata (views are pre-filtered)

### Metadata
- **Source:** Nielsen metadata tables
- **Contents:** Column descriptions, types, null semantics
- **Use case:** Schema documentation, reproducibility

### Engineered Features
- **Source:** Preprocessing pipeline output
- **Columns:** Selected features after statistical analysis
- **Use case:** Model training
- **Naming:** Simplified (`csd_*` instead of `specialized_CSD_*`)

---

## Next Steps

### For Other Categories (Danskvand, Energidrikke, RTD, Totalbeer)

Apply the same pattern to remaining preprocessing scripts:
- `preprocessing_danskvand.py`
- `preprocessing_energidrikke.py`
- `preprocessing_rtd.py`
- `preprocessing_totalbeer.py`

Changes needed:
1. Update imports (add PATHS helpers)
2. Update input paths (use category-specific paths)
3. Update load_raw() to load from raw tables
4. Add save_dimension_tables() call in main()
5. Rename save_outputs() → save_engineered_outputs()
6. Update pipeline steps (0–6)

### For Notebooks

Update specialized_CSD.ipynb (and others) to load dimensions from new paths:

```python
from PATHS import get_category_views_dir

views_dir = get_category_views_dir("CSD")
dim_period = pd.read_parquet(views_dir / "csd_clean_dim_period_v.parquet")
dim_market = pd.read_parquet(views_dir / "csd_clean_dim_market_v.parquet")
dim_product = pd.read_parquet(views_dir / "csd_clean_dim_product_v.parquet")
facts = pd.read_parquet(views_dir / "csd_clean_facts_v.parquet")
```

---

## Verification

✅ PATHS helpers imported and working:
```
CSD raw: C:\dev\thesis-manifold\thesis\data\preprocessing\parquet_nielsen\CSD\raw
CSD engineered: C:\dev\thesis-manifold\thesis\data\preprocessing\parquet_nielsen\CSD\engineered
```

✅ preprocessing_csd.py syntax verified (no import errors)

✅ save_all_datasets.py refactored (awaiting Nielsen data download to test)

---

## See Also

- `docs/integration/NIELSEN_DATA_ARCHITECTURE.md` — Design rationale
- `PATHS.py` — Path centralization and helpers
- `thesis/data/raw_nielsen/description/SCHEMA_SNAPSHOT.md` — Nielsen schema reference
