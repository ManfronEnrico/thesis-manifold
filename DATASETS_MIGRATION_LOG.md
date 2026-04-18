# Datasets Folder Reorganization — Migration Log

**Date**: 2026-04-18  
**Status**: Assessment + Action Plan

---

## 1. Folder Structure Assessment ✓

Your new hierarchy makes sense. It provides:
- **Clear separation**: Nielsen data vs. Indeks Danmark/SPSS data
- **Organized by type**: Raw CSVs (`.csv/` subfolder) + scripts + documentation
- **Scalable**: Easy to add more datasets later

**Structure Approved:**
```
datasets/
├── data_nielsen/
│   ├── .csv/                  ← Raw CSV output from SQL (gitignored)
│   ├── description/           ← Data model documentation
│   └── scripts/               ← Connector + assessment/exploration
├── data_spss_indeksdanmark/
│   ├── .csv/                  ← Raw CSVs from Google Drive (gitignored)
│   ├── description/           ← SPSS data model documentation
│   └── scripts/               ← [TO BE CREATED]
└── combined_scripts/          ← Preprocessing scripts
```

---

## 2. Script Naming Assessment ✓

**Your renamings are CORRECT and CLEAR:**

| Old | New | Status |
|-----|-----|--------|
| `nielsen_connector.py` | `nielsen-connector.py` (in `data_nielsen/scripts/`) | ✓ Consistent |
| `nielsen_data_assessment.py` | `nielsen-data_assessment.py` (in `data_nielsen/scripts/`) | ✓ Consistent |
| `explore_nielsen.py` | `nielsen-data_exploration.py` (in `data_nielsen/scripts/`) | ✓ Consistent |
| (none) | `spss_indeksdanmark_connector.py` | [TODO] |
| (none) | `spss_indeksdanmark_loader.py` | [TODO] |

**Naming pattern**: `{datasource}-{operation}.py` → Enrico and Claude will instantly understand what each script does.

---

## 3. Stale Reference Check

### Files with OLD Import Paths (Need Fixing)

**File: `datasets/data_nielsen/scripts/nielsen-connector.py` (line 6)**
```python
# OLD (docstring only, not executed):
    from ai_research_framework.data.nielsen_connector import get_connection

# SHOULD BE:
    from datasets.data_nielsen.scripts.nielsen_connector import get_connection
```

**File: `datasets/data_nielsen/scripts/nielsen-data_assessment.py` (line 7-8)**
```python
# OLD (docstring only):
    python3 -m ai_research_framework.data.nielsen_data_assessment

# SHOULD BE:
    cd CMT_Codebase && python -m datasets.data_nielsen.scripts.nielsen_data_assessment

# Also line 17: OLD import:
from datasets.nielsen_connector import get_connection

# SHOULD BE:
from datasets.data_nielsen.scripts.nielsen_connector import get_connection
```

**File: `datasets/data_nielsen/scripts/nielsen-data_exploration.py` (lines 24-25)**
```python
# Line 24: OLD
from ai_research_framework.config import NielsenConfig

# Line 25: WORKS (correct)
from datasets.nielsen_connector import get_connection
# BUT SHOULD BE:
from datasets.data_nielsen.scripts.nielsen_connector import get_connection
```

### Clean-Up Actions

1. **Fix docstring imports** in both `-data_assessment.py` and `-connector.py`
2. **Fix line 17** in `-data_assessment.py`: update import path
3. **Fix line 25** in `-data_exploration.py`: update import path
4. **Fix line 24** in `-data_exploration.py`: remove dependency on `ai_research_framework.config` OR keep if NielsenConfig is still valid there

---

## 4. Nielsen Data Loading + Caching Script (NEW)

### File: `datasets/data_nielsen/scripts/nielsen_load_and_cache.py`

**Purpose**: Fetch Nielsen data from SQL → cache to `.csv/` folder → return DataFrame

**Features**:
- Connects using updated environment variables (verified OK)
- Fetches `csd_clean_facts_v` table
- Saves to `datasets/data_nielsen/.csv/nielsen_data.csv`
- On re-run: loads from cache if exists
- Integrity check: SHA256 hash of data

**Usage**:
```python
from datasets.data_nielsen.scripts.nielsen_load_and_cache import load_nielsen_data
df = load_nielsen_data(force_refresh=False)
```

---

## 5. Indeks Danmark / SPSS Data (Awaiting CSV Files)

Once you receive the CSV files from Enrico:

1. **Place them here**:
   ```
   datasets/data_spss_indeksdanmark/.csv/
   ├── indeksdanmark_data.csv
   ├── official_codebook.csv
   └── indeksdanmark_metadata.csv
   ```

2. **Create loader script**: `datasets/data_spss_indeksdanmark/scripts/spss_indeksdanmark_loader.py`
   - Similar pattern to Nielsen loader
   - Load 3 CSVs, validate, cache

3. **Update import paths** in any existing exploration/assessment scripts

---

## Migration Checklist

- [ ] Fix import in `nielsen-connector.py` docstring (line 6)
- [ ] Fix import in `nielsen-data_assessment.py` docstring (line 7-8)
- [ ] Fix import in `nielsen-data_assessment.py` actual code (line 17)
- [ ] Fix import in `nielsen-data_exploration.py` (line 24-25)
- [ ] Create `nielsen_load_and_cache.py` script
- [ ] Test: `python datasets/data_nielsen/scripts/nielsen_load_and_cache.py` works
- [ ] Verify `.csv/` folder created and `nielsen_data.csv` written
- [ ] Verify hash file created at `.data/processed/checksums.json` (if using DataCache pattern)
- [ ] Await CSV files from Enrico
- [ ] Place CSVs in `datasets/data_spss_indeksdanmark/.csv/`
- [ ] Create `spss_indeksdanmark_loader.py`

---

## Why This Approach?

**For Enrico**: Clear folder structure → he sees exactly where Nielsen/SPSS data is, how it's accessed.

**For Claude**: Import paths are straightforward: `datasets.data_nielsen.scripts.{script_name}`

**For auditing**: CSVs are in `.csv/` subfolders → gitignored → easy to see which datasets are tracked vs. untracked.

---

## Next Step

Approve the migration plan, then I'll:
1. Fix all stale imports
2. Create `nielsen_load_and_cache.py`
3. Test the full flow
