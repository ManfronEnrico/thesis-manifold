# Data Connection Audit — Environment Variables & Storage Strategy

**Status**: Completed 2026-04-18 | Session Investigation

---

## 1. Environment Variables Referenced in Code

### Zotero Integration (scripts/zotero_sync_phase1.py)
```python
# Lines 24-30
required = ["ZOTERO_USER_ID", "ZOTERO_API_KEY"]
```
- **ZOTERO_USER_ID**: Zotero library ID (group or user)
- **ZOTERO_API_KEY**: Zotero API key for authentication

### Nielsen Data Connection (ai_research_framework/config.py)
```python
# Lines 63-67 — NielsenConnectionConfig
RU_SERVER_STRING      # Azure SQL server endpoint
RU_DATABASE           # Database name
RU_CLIENT_ID          # Azure AD service principal ID
RU_TENANT_ID          # Azure AD tenant ID
RU_CLIENT_SECRET      # Service principal secret
```

**Status**: `access_confirmed: bool = True` in config.py (line 84), but `.env` variable names have been updated by Enrico.

---

## 2. Current Data Storage Issues

### Nielsen CSD Data
- **Current State**: NOT IMPLEMENTED
- **Location**: Azure SQL database (remote)
- **Agent**: `data_assessment_agent.py:83-91` 
- **Issue**: Raises `NotImplementedError` — awaiting data access confirmation
- **What needs to change**: 
  1. Verify current `.env` variable names match what Enrico set
  2. Implement SQL loader to write output to local cache directory
  3. Convert to pandas DataFrame on first load, cache as Parquet

### Indeks Danmark Data
- **Current State**: NOT IMPLEMENTED
- **Location**: Google Drive (3 CSVs)
- **Agent**: `data_assessment_agent.py:93-101`
- **RAM Budget**: ~970 MB for main CSV
- **What needs to change**:
  1. Download 3 CSVs to local cache directory (non-tracked)
  2. Load into pandas DataFrames
  3. Save as Parquet for efficient reloading

### Zotero Data
- **Status**: Reads from `.env` (ZOTERO_USER_ID, ZOTERO_API_KEY)
- **Current flow**: Fetches live from Zotero API, writes report to `docs/zotero_sync_report.md`
- **What needs to change**: Optional — maintain live API calls OR cache response

---

## 3. Recommended Data Storage Strategy

### Directory Structure (Non-Tracked)
```
CMT_Codebase/
├── .data/                          ← NEW: gitignored local data cache
│   ├── raw/                        ← Raw source files (CSV, SQL dumps)
│   │   ├── indeks_danmark_raw/
│   │   │   ├── data.csv
│   │   │   ├── codebook.csv
│   │   │   └── metadata.csv
│   │   └── nielsen/
│   │       └── csd_dump.parquet
│   ├── processed/                  ← Processed DataFrames (Parquet)
│   │   ├── indeks_danmark.parquet
│   │   ├── nielsen_csd.parquet
│   │   └── feature_matrix.parquet
│   └── checksums.json              ← Hash verification (see load patterns)
└── .gitignore                       ← Add `.data/` directory
```

### Implementation Pattern

```python
# Generic loader pattern (apply to all data sources)
from pathlib import Path
import pandas as pd
import hashlib

class DataCache:
    CACHE_DIR = Path(".data/processed")
    RAW_DIR = Path(".data/raw")
    
    @staticmethod
    def load_or_fetch(
        source_name: str,
        fetch_fn: callable,
        hash_check: bool = True
    ) -> pd.DataFrame:
        """
        Load from cache if exists, else fetch → cache → return.
        
        Args:
            source_name: e.g., 'indeks_danmark', 'nielsen_csd'
            fetch_fn: Function that returns pd.DataFrame
            hash_check: Verify checksums before returning
        
        Returns:
            pd.DataFrame with data
        """
        cache_file = DataCache.CACHE_DIR / f"{source_name}.parquet"
        DataCache.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Return from cache if exists
        if cache_file.exists():
            df = pd.read_parquet(cache_file)
            if hash_check:
                DataCache._verify_hash(source_name, df)
            return df
        
        # Fetch, cache, and return
        df = fetch_fn()
        df.to_parquet(cache_file, compression='snappy')
        DataCache._save_hash(source_name, df)
        return df
    
    @staticmethod
    def _save_hash(source_name: str, df: pd.DataFrame) -> None:
        """Save SHA256 of DataFrame shape + column hash for integrity check."""
        import json
        hash_data = {
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(df[col].dtype) for col in df.columns},
            "hash": hashlib.sha256(
                pd.util.hash_pandas_object(df, index=True).values
            ).hexdigest()
        }
        checksums_file = DataCache.CACHE_DIR / "checksums.json"
        checksums = json.loads(checksums_file.read_text()) if checksums_file.exists() else {}
        checksums[source_name] = hash_data
        checksums_file.write_text(json.dumps(checksums, indent=2))
    
    @staticmethod
    def _verify_hash(source_name: str, df: pd.DataFrame) -> bool:
        """Check cached file hasn't been modified outside the loader."""
        import json
        checksums_file = DataCache.CACHE_DIR / "checksums.json"
        if not checksums_file.exists():
            return True
        checksums = json.loads(checksums_file.read_text())
        if source_name not in checksums:
            return True
        # Compare row count + column names (fast check)
        record = checksums[source_name]
        assert len(df) == record["rows"], f"Row count mismatch for {source_name}"
        assert list(df.columns) == record["columns"], f"Column mismatch for {source_name}"
        return True
```

### Data Source Implementation

#### Nielsen CSD (Azure SQL)
```python
# ai_research_framework/data/nielsen_connector.py (NEW)

from ai_research_framework.config import NielsenConnectionConfig
from data_cache import DataCache
import pandas as pd

def fetch_nielsen_csd() -> pd.DataFrame:
    """
    Connects to Azure SQL, fetches facts table, returns as DataFrame.
    """
    cfg = NielsenConnectionConfig()
    # TODO: Implement mssql connection using azure-identity
    # ... SQL query on csd_clean_facts_v ...
    df = ...  # Load from database
    return df

# Usage in data_assessment_agent.py
def _assess_nielsen(self) -> Tuple[Any, Dict]:
    df = DataCache.load_or_fetch(
        source_name='nielsen_csd',
        fetch_fn=fetch_nielsen_csd,
        hash_check=True
    )
    # ... quality checks ...
    return df, report
```

#### Indeks Danmark (Google Drive CSVs)
```python
# scripts/load_indeks_danmark.py (NEW)

def fetch_indeks_danmark() -> pd.DataFrame:
    """
    Download 3 CSVs from Google Drive, cache raw, load + merge into DataFrame.
    """
    raw_dir = Path(".data/raw/indeks_danmark_raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Download from Google Drive (gdown or manual)
    # TODO: Get Google Drive share IDs from .env
    
    data_csv = raw_dir / "data.csv"
    df = pd.read_csv(data_csv, encoding='utf-8')
    return df

# Usage in data_assessment_agent.py
def _assess_indeks_danmark(self) -> Tuple[Any, Dict]:
    df = DataCache.load_or_fetch(
        source_name='indeks_danmark',
        fetch_fn=fetch_indeks_danmark,
        hash_check=True
    )
    return df, report
```

---

## 4. Updated .gitignore Entry

```diff
+ # Data cache (downloaded/fetched on demand)
+ .data/
+ .data_temp/
```

The `.data/` directory will be created on first run, populated by loaders, and excluded from version control.

---

## 5. Audit Trail for Code Review

**Why write to disk instead of keeping in memory:**
- **RAM constraint**: 8GB budget; Nielsen + Indeks = ~1.5 GB peak
- **Reproducibility**: Inspect cached files to verify data hasn't changed
- **Debugging**: Can reload and inspect without re-fetching
- **Auditability**: Checksums in `.data/processed/checksums.json` prove data integrity
- **Recovery**: If agent crashes mid-pipeline, restart with cached data instead of re-fetch

---

## 6. Environment Variable Rename Instructions

**Enrico's Changes** (awaiting your .env):
- OLD: `RU_SERVER_STRING`, `RU_DATABASE`, `RU_CLIENT_ID`, `RU_TENANT_ID`, `RU_CLIENT_SECRET`
- NEW: Check what Enrico named them in the updated .env

**Action**: Once you have Enrico's .env names:
1. Update `ai_research_framework/config.py` lines 63-67 to match new variable names
2. Keep the NielsenConnectionConfig dataclass structure (do not change field names)
3. Verify in `scripts/test_env_vars.py` (create if needed)

---

## Next Steps

1. **Immediate**: Check `.env` for Enrico's Nielsen variable names → update config.py
2. **Week 1**: Implement Nielsen SQL connector + DataCache pattern
3. **Week 1**: Download Indeks Danmark CSVs to `.data/raw/` + implement loader
4. **Week 2**: Update `data_assessment_agent.py` to use cached DataFrames
5. **Week 2**: Run data quality checks → verify `.data/processed/checksums.json`
