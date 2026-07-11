---
name: data-pipeline-quickstart
description: Quick guide to running the full data pipeline from Nielsen Fabric to engineered features
---

# Data Pipeline Quickstart

## Overview

The data pipeline has 4 tiers:

| Tier | Location | What | Source |
|------|----------|------|--------|
| **_00_raw** | `thesis/data/_00_raw/nielsen/data_jsonl/` | Raw JSONL from Nielsen Fabric | External (download script) |
| **_01_converted** | `thesis/data/_01_converted/nielsen/parquet_nielsen/` | Stage 1: JSONL → Parquet cache | Conversion script |
| **_02_preprocessing** | `thesis/data/_02_preprocessing/nielsen/CSD/` | Stage 2: Preprocessing scripts + intermediate outputs | Pipeline scripts |
| **_03_engineered** | `thesis/data/_03_engineered/nielsen/CSD/` | **FINAL OUTPUT** — Feature matrix ready for modeling | Pipeline Step 6 |

---

## Scripts to Run (In Order)

### Step 0: Download Nielsen Data (One-time)

**Location:** `thesis/data/_00_raw/nielsen/scripts/`

```bash
python save_all_datasets.py
```

**Output:**
- JSONL files in `_00_raw/nielsen/data_jsonl/{CATEGORY}/views/`
- MANIFEST.json (metadata about download)

---

### Step 1: Convert JSONL to Parquet (One-time)

**Location:** `thesis/data/_01_converted/nielsen/jsonl_to_parquet/`

```bash
python run_all_conversions.py
```

**Output:**
- Parquet cache in `_01_converted/nielsen/parquet_nielsen/{CATEGORY}/views/`
- Used by preprocessing pipeline as fast cache

---

### Step 2: Run Preprocessing Pipeline (Main)

**Location:** `thesis/data/_02_preprocessing/nielsen/CSD/`

```bash
python preprocessing_csd.py
```

**What it does (automatically):**
1. Step 0: Validates parquet cache exists
2. Step 1: Loads and aggregates by brand
3. Step 2: Builds calendar (fills missing months)
4. Step 3: Filters low-volume series (MIN_PERIODS=40)
5. Step 4: Engineers features (lags, rolling windows, seasonality)
6. Step 5: Applies train/val/test split (forward-chaining)
7. Step 6: **Saves final outputs to `_03_engineered/`**

**Output (in `_03_engineered/nielsen/CSD/`):**
- `csd_feature_matrix.parquet` — **USE THIS FOR MODELING**
- `csd_split_dates.json` — Train/val/test boundaries
- `csd_series_index.csv` — Brand metadata
- `csd_preprocessing_report.md` — Summary report

---

## Quick Command Reference

```bash
# Full pipeline (Steps 0-2):
python thesis/data/_00_raw/nielsen/scripts/save_all_datasets.py
python thesis/data/_01_converted/nielsen/jsonl_to_parquet/run_all_conversions.py
python thesis/data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py

# Just preprocess (if cache already exists):
python thesis/data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py

# Re-run specific step (e.g., re-engineer features):
python thesis/data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py --run-step 4

# Full refresh (delete cache and re-convert):
python thesis/data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py --re-cache
```

---

## Key Points

✅ **All paths are dynamic** (defined in `PATHS.py`)  
✅ **Final output folder is always `_03_engineered/`**  
✅ **Feature matrix is `csd_feature_matrix.parquet`**  
✅ **Use `--help` on any script for additional options**

---

## Example: Load Feature Matrix for Modeling

```python
import pandas as pd
from PATHS import get_category_engineered_dir

# Get feature matrix
eng_dir = get_category_engineered_dir("CSD")
features = pd.read_parquet(eng_dir / "csd_feature_matrix.parquet")

# Load split info
import json
split_dates = json.load(open(eng_dir / "csd_split_dates.json"))

print(f"Feature matrix shape: {features.shape}")
print(f"Train end: {split_dates['train_end']}")
```

---

**Questions?** Check the preprocessing scripts' docstrings for detailed algorithm descriptions.
