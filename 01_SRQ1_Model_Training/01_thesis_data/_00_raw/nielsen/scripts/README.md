# Nielsen Fabric Data Access

Scripts for accessing Nielsen data from Microsoft Fabric Data Warehouse and saving to local CSV.

## Setup (One-time)

1. **Get credentials from Brian or Nika:**
   - Add to `.env` in project root:
     ```
     RU_SERVER_STRING=<endpoint>
     RU_DATABASE=Nielsen_clean
     RU_CLIENT_ID=<app-id>
     RU_TENANT_ID=<tenant-id>
     RU_CLIENT_SECRET=<your-secret>
     ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.lock
   ```
   (From project root. Dependencies: pyodbc, azure-identity, python-dotenv already in lock file.)

3. **Verify ODBC driver (Windows):**
   ODBC Driver 18 for SQL Server must be installed. Download: https://aka.ms/odbc17

4. **Network note:** Must be on WiFi (not CBS LAN) to access Fabric.

## Quick Start

### 1. Audit available datasets
```bash
cd thesis/data/nielsen/scripts
python audit_datasets.py
```
Output: Lists all 52 objects (20 views, 23 tables, 9 metadata).

### 2. Save all data locally
```bash
python save_all_datasets.py
```
- Saves 18 CSV files to `thesis/data/nielsen/.csv/` (~300 MB)
- Generates `MANIFEST.json` with metadata
- Takes ~5-10 minutes first time (2.5M fact rows)

### 3. Use connection directly (in notebooks)
```python
from thesis.data.nielsen.scripts.nielsen_connector import get_connection
import pandas as pd

conn = get_connection()
df = pd.read_sql("SELECT TOP 100 * FROM dbo.csd_clean_facts_v", conn)
conn.close()
```

## Files

| Script | Purpose |
|--------|---------|
| `nielsen_connector.py` | Core: authenticate to Fabric |
| `audit_datasets.py` | List all tables/views (identify gaps) |
| `save_all_datasets.py` | Download all data to CSV + manifest |

## Data Structure

After running `save_all_datasets.py`:

**CSD (Core Soft Drinks):**
- `csd_clean_dim_*.csv` (market, period, product)
- `csd_clean_facts_v.csv` (2.5M sales records)
- `metadata_csd_*.csv` (column definitions)

**Other Categories:** totalbeer, energidrikke, danskvand, rtd (same structure)

**Metadata:** `metadata_*_columns.csv` (Nielsen column mappings)

## Troubleshooting

**"Login failed" / timeout:**
- Check `.env` values
- Verify on WiFi (not CBS LAN)
- Confirm `ODBC Driver 18` installed

**"Named Pipes: Could not open connection":**
- Port 1433 blocked → use WiFi or VPN

**"Connection OK but no data":**
- Run `audit_datasets.py` to verify tables exist
- Check query spelling (case-sensitive)

## Updating Data

```bash
python save_all_datasets.py
```
Refreshes all local CSVs and updates MANIFEST.json.

## Adding New Datasets

1. Query name must follow `dbo.<table_name>` pattern
2. Add to appropriate list in `save_all_datasets.py`
3. Re-run to include in backup

See also: `docs/notes/2026_04_20-nielsen_data_access_strategy.md`
