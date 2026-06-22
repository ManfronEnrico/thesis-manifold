# UV Cache Migration to Z: Drive

**Status**: Self-directed execution  
**Goal**: Migrate UV cache from D: to Z: drive, then re-download Nielsen data and regenerate parquet files.

---

## Step 1: Verify PowerShell Profile Update

Your profile at `C:\Users\brian\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1` already has:
```powershell
$env:UV_CACHE_DIR = "Z:\.dev-ssd\.uv"
```

**Verify it's active:**
```powershell
$env:UV_CACHE_DIR
# Should output: Z:\.dev-ssd\.uv
```

---

## Step 2: Sync UV Cache to Z: Drive

**Current cache location**: `D:\.dev-ssd\.uv` (old SSD drive)  
**New cache location**: `Z:\.dev-ssd\.uv` (stable external SSD)

**Copy existing cache (preserves cached wheels):**
```powershell
$env:UV_CACHE_DIR = "Z:\.dev-ssd\.uv"
mkdir -Force "Z:\.dev-ssd\.uv" | Out-Null
Copy-Item "D:\.dev-ssd\.uv\*" "Z:\.dev-ssd\.uv\" -Recurse -Force -ErrorAction SilentlyContinue
uv cache dir  # Verify → should output Z:\.dev-ssd\.uv
```

**OR start fresh (cleaner, slower first run):**
```powershell
$env:UV_CACHE_DIR = "Z:\.dev-ssd\.uv"
mkdir -Force "Z:\.dev-ssd\.uv" | Out-Null
# Skip copy, let UV repopulate on next install
```

---

## Step 3: Install/Sync Project Dependencies

**From project root (`Z:\.dev-ssd\thesis-manifold`):**

```powershell
cd "Z:\.dev-ssd\thesis-manifold"
$env:UV_CACHE_DIR = "Z:\.dev-ssd\.uv"

# Install preprocessing dependencies (pandas, pyarrow, etc.)
uv pip install -r thesis/data/preprocessing/requirements.txt

# Install Nielsen data access dependencies (pyodbc, azure-identity, python-dotenv)
uv pip install -r thesis/data/raw_nielsen/scripts/requirements.txt
```

**Verify UV cache is now on Z::**
```powershell
uv cache dir  # Should show Z:\.dev-ssd\.uv
Get-ChildItem "Z:\.dev-ssd\.uv" | Measure-Object -Sum -Property Length  # Check cache size
```

---

## Step 4: Re-download Nielsen Data

**Prerequisite**: `.env` file in project root with Fabric credentials:
```
RU_SERVER_STRING=<endpoint>
RU_DATABASE=Nielsen_clean
RU_CLIENT_ID=<app-id>
RU_TENANT_ID=<tenant-id>
RU_CLIENT_SECRET=<secret>
```

**Run from project root:**
```powershell
cd "Z:\.dev-ssd\thesis-manifold"
python thesis/data/raw_nielsen/scripts/audit_datasets.py  # Verify connection first (lists 52 objects)
```

**If audit passes, download all data (~5-10 min, ~300 MB):**
```powershell
python thesis/data/raw_nielsen/scripts/save_all_datasets.py
# Output: CSV files to thesis/data/raw_nielsen/data_csv/ + MANIFEST.json
```

---

## Step 5: Regenerate Parquet Feature Matrices

**Run preprocessing pipeline:**
```powershell
cd "Z:\.dev-ssd\thesis-manifold"
python thesis/data/preprocessing/run_all_preprocessing.py
```

**Output:**
- Parquet files: `thesis/data/preprocessing/parquet_nielsen/<category>/` (5 categories: CSD, Totalbeer, Energidrikke, Danskvand, RTD)
- Preprocessing reports: `.../preprocessing_report.md` (one per category)
- Split dates: `split_dates.json` (train/test boundaries)

---

## File Locations Reference

| Component | Path |
|-----------|------|
| **PowerShell Profile** | `C:\Users\brian\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1` |
| **UV Cache** | `Z:\.dev-ssd\.uv` (set via env var) |
| **Nielsen Scripts** | `thesis/data/raw_nielsen/scripts/` |
| **Preprocessing Scripts** | `thesis/data/preprocessing/` |
| **Raw Data (CSV)** | `thesis/data/raw_nielsen/data_csv/` |
| **Parquet Output** | `thesis/data/preprocessing/parquet_nielsen/` |
| **Env File** | `Z:\.dev-ssd\thesis-manifold\.env` |

---

## Troubleshooting

### UV cache not using Z: drive
```powershell
# Ensure profile is loaded
. $PROFILE
# Or explicitly set:
$env:UV_CACHE_DIR = "Z:\.dev-ssd\.uv"
uv cache dir
```

### Nielsen connection fails
- Verify `.env` values (endpoint, client ID, secret)
- Must be on WiFi (not CBS LAN) to access Microsoft Fabric
- Check ODBC Driver 18 installed: `Get-OdbcDriver | Where-Object {$_.Name -like "*18*"}`

### Preprocessing hangs
- Ensure all Nielsen CSV files downloaded first (check `thesis/data/raw_nielsen/data_csv/`)
- Monitor RAM (preprocessing can use 2-4 GB for large categories)

---

## Done When

- ✅ `uv cache dir` returns `Z:\.dev-ssd\.uv`
- ✅ `audit_datasets.py` lists 52 objects
- ✅ Parquet files generated in `thesis/data/preprocessing/parquet_nielsen/`
- ✅ Preprocessing reports show no errors

