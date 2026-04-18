# Data Cache Implementation Guide

**Quick summary**: All datasets load-on-demand → cached as Parquet → integrity checksums → unload after use.

---

## Env Vars to Update (Once You Have Enrico's .env)

**File**: `ai_research_framework/config.py` lines 63-67

Old names (current):
```python
RU_SERVER_STRING, RU_DATABASE, RU_CLIENT_ID, RU_TENANT_ID, RU_CLIENT_SECRET
```

Once you get Enrico's new names, update the `default_factory` lambdas:
```python
@dataclass
class NielsenConnectionConfig:
    server: str = field(default_factory=lambda: os.environ["NEW_SERVER_NAME"])
    database: str = field(default_factory=lambda: os.environ["NEW_DB_NAME"])
    # ... etc
```

**Do NOT** change the field names (`server`, `database`, etc.)—keep NielsenConnectionConfig interface the same.

---

## Where is SPSS Data?

**Not found in codebase.** The "Indeks Danmark" dataset (3 CSVs on Google Drive) is likely the SPSS export you're referring to. Once downloaded:
```
.data/
├── raw/
│   ├── indeks_danmark_raw/
│   │   ├── data.csv              ← Main SPSS export
│   │   ├── codebook.csv
│   │   └── metadata.csv
```

---

## DataFrame Caching Pattern (Ready to Use)

**File**: `ai_research_framework/data_cache.py` (already created)

### Example: Indeks Danmark

```python
from ai_research_framework.data_cache import DataCache
import pandas as pd

def fetch_indeks_danmark() -> pd.DataFrame:
    """Download from Google Drive or load from .data/raw/"""
    csv_path = Path(".data/raw/indeks_danmark_raw/data.csv")
    return pd.read_csv(csv_path)

# In data_assessment_agent.py
def _assess_indeks_danmark(self) -> Tuple[Any, Dict]:
    # First call: fetches + caches, subsequent calls: load from cache
    df = DataCache.load_or_fetch(
        source_name='indeks_danmark',
        fetch_fn=fetch_indeks_danmark,
        hash_check=True  # Verify file hasn't been modified
    )
    # Run quality checks...
    report = {...}
    return df, report
```

### Example: Nielsen CSD (Once SQL Access Works)

```python
from ai_research_framework.config import NielsenConnectionConfig
from ai_research_framework.data_cache import DataCache
import pyodbc
import pandas as pd

def fetch_nielsen_csd() -> pd.DataFrame:
    """Query Azure SQL, return as DataFrame."""
    cfg = NielsenConnectionConfig()
    conn_str = f"""Driver={{ODBC Driver 17 for SQL Server}};
Server={cfg.server};Database={cfg.database};
Authentication=ActiveDirectoryServicePrincipal;
UID={cfg.client_id};PWD={cfg.client_secret};"""
    
    with pyodbc.connect(conn_str) as conn:
        df = pd.read_sql("SELECT * FROM csd_clean_facts_v", conn)
    return df

# In data_assessment_agent.py
def _assess_nielsen(self) -> Tuple[Any, Dict]:
    df = DataCache.load_or_fetch(
        source_name='nielsen_csd',
        fetch_fn=fetch_nielsen_csd,
        hash_check=True
    )
    # Run quality checks...
    report = {...}
    return df, report
```

---

## Cache Inspection Commands

**Check what's cached**:
```python
from ai_research_framework.data_cache import DataCache
status = DataCache.get_cache_status()
print(status)
# Output: {'cached_files': ['indeks_danmark', 'nielsen_csd'], 'total_size_mb': 1200.5, ...}
```

**View checksums** (proof of data integrity):
```bash
cat .data/processed/checksums.json
```

**Force refresh** (re-fetch from source):
```python
df = DataCache.load_or_fetch(
    source_name='indeks_danmark',
    fetch_fn=fetch_indeks_danmark,
    force_refresh=True  # Ignore cache, fetch fresh
)
```

**Clear cache** (careful!):
```python
DataCache.clear_cache('indeks_danmark')  # Clear one dataset
DataCache.clear_cache()  # Clear all
```

---

## Why This Approach?

1. **RAM Efficient**: 8GB budget. Load only what you need, unload when done.
2. **Audit Trail**: Checksums in `.data/processed/checksums.json` prove data hasn't changed.
3. **Reproducible**: Same data on re-run → same results.
4. **Testable**: Inspect cached files without re-fetching (e.g., check row counts, dtypes).
5. **CBS Compliance**: Can show reviewers exact data used for each analysis.

---

## Next Steps

1. Get Enrico's `.env` → update `config.py` Nielsen variable names
2. Download Indeks Danmark CSVs → place in `.data/raw/indeks_danmark_raw/`
3. Implement Nielsen SQL connection using `DataCache` pattern
4. Update `data_assessment_agent.py` to use `DataCache.load_or_fetch()` for both sources
5. Test: Run agent, verify `.data/processed/` files created with checksums
