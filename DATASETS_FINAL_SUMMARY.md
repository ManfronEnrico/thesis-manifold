# Datasets Reorganization — Final Setup Complete

**Date**: 2026-04-18  
**Status**: ✅ COMPLETE

---

## Overview

Your datasets folder has been reorganized into a clean, importable structure:

```
datasets/
├── data_nielsen/
│   ├── __init__.py
│   ├── .csv/                      ← Nielsen data output (gitignored)
│   ├── description/
│   │   └── nielsen-prometheus_data_model.md
│   └── scripts/
│       ├── __init__.py
│       ├── nielsen_connector.py       (Get SQL connection)
│       ├── nielsen_data_assessment.py (Data quality report)
│       ├── nielsen_data_exploration.py (Initial exploration)
│       └── nielsen_load_and_cache.py  (Fetch + cache to CSV)
│
├── data_spss_indeksdanmark/
│   ├── __init__.py
│   ├── .csv/                      ← SPSS CSVs (gitignored)
│   ├── description/
│   │   └── spss_indeksdanmark_data_model.md
│   └── scripts/
│       └── __init__.py
│
└── combined_scripts/
    ├── __init__.py
    └── preprocessing.py
```

---

## Scripts — Naming & Purpose

| Script | Purpose |
|--------|---------|
| `nielsen_connector.py` | Returns pyodbc connection to Nielsen SQL |
| `nielsen_data_assessment.py` | Comprehensive data quality checks |
| `nielsen_data_exploration.py` | First-look at tables, rows, columns |
| `nielsen_load_and_cache.py` | Fetch Nielsen data → save to CSV |

---

## What Changed

### Renamed Scripts (Underscore Format)

Old → New (underscores for Python imports):
```
nielsen-connector.py          → nielsen_connector.py
nielsen-data_assessment.py    → nielsen_data_assessment.py
nielsen-data_exploration.py   → nielsen_data_exploration.py
```

Why: Python modules cannot contain hyphens. Underscores allow both importability and readability.

### Fixed All Import Paths

Updated scripts to use correct paths:
```python
# OLD
from ai_research_framework.data.nielsen_connector import get_connection

# NEW
from datasets.data_nielsen.scripts.nielsen_connector import get_connection
```

### Fixed .env Path Resolution

All scripts now correctly find .env at project root.

### Created Python Module Markers

Added __init__.py files:
```
datasets/data_nielsen/__init__.py
datasets/data_nielsen/scripts/__init__.py
datasets/data_spss_indeksdanmark/__init__.py
datasets/data_spss_indeksdanmark/scripts/__init__.py
```

### Created Nielsen Loader Script

New: `nielsen_load_and_cache.py`
- Connects to Nielsen SQL
- Fetches csd_clean_facts_v table
- Saves to datasets/data_nielsen/.csv/nielsen_data.csv
- Reuses cache on next run (unless --force-refresh)

---

## How to Use

### Command Line

Fetch + cache Nielsen data:
```bash
cd CMT_Codebase
python -m datasets.data_nielsen.scripts.nielsen_load_and_cache
```

Force refresh from SQL:
```bash
python -m datasets.data_nielsen.scripts.nielsen_load_and_cache --force-refresh
```

Run data assessment:
```bash
python -m datasets.data_nielsen.scripts.nielsen_data_assessment
```

### In Python Code

Load Nielsen data:
```python
from datasets.data_nielsen.scripts.nielsen_load_and_cache import load_nielsen_data

df = load_nielsen_data()
print(f"Loaded {len(df)} rows")
```

Use connector directly:
```python
from datasets.data_nielsen.scripts.nielsen_connector import get_connection
import pandas as pd

conn = get_connection()
df = pd.read_sql("SELECT TOP 100 * FROM dbo.csd_clean_facts_v", conn)
conn.close()
```

---

## For Enrico

1. Old location (ai_research_framework/data/) is no longer used
2. New location: everything is in datasets/data_*/scripts/
3. Import paths: Updated throughout
4. SPSS data: Place 3 CSVs in:
   ```
   datasets/data_spss_indeksdanmark/.csv/
   ```

---

## Files Changed

- `nielsen_connector.py` — Renamed + fixed imports
- `nielsen_data_assessment.py` — Renamed + fixed imports
- `nielsen_data_exploration.py` — Renamed + fixed imports
- `nielsen_load_and_cache.py` — CREATED (new loader script)
- `datasets/data_nielsen/__init__.py` — CREATED (module marker)
- `datasets/data_nielsen/scripts/__init__.py` — CREATED (module marker)
- `datasets/data_spss_indeksdanmark/__init__.py` — CREATED (module marker)
- `datasets/data_spss_indeksdanmark/scripts/__init__.py` — CREATED (module marker)

---

## Ready to Test

```bash
cd CMT_Codebase
python -m datasets.data_nielsen.scripts.nielsen_load_and_cache
```

This will connect to Nielsen SQL, fetch the facts table, save to .csv/nielsen_data.csv, and print success message.

On next run, it will load from cache unless you use --force-refresh.
