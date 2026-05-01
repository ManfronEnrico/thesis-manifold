# Preprocessing Pipeline Verification Guide

## Quick Verification Checklist

After running `python preprocessing_csd.py`, verify success by checking:

### 1. **Exit Code**
```
$LASTEXITCODE -eq 0  # PowerShell
echo $?               # Bash
```
✅ **Success**: Exit code `0`
❌ **Failure**: Non-zero exit code + error message

### 2. **Output Files Exist**
Check that all 4 files were created in `thesis/data/preprocessing/parquet_nielsen/`:

```powershell
Get-ChildItem "thesis/data/preprocessing/parquet_nielsen/" | Select-Object Name, Length
```

Expected files:
- ✅ `specialized_CSD_feature_matrix.parquet` (0.3–0.5 MB)
- ✅ `series_index.csv` (5–10 KB)
- ✅ `split_dates.json` (< 1 KB)
- ✅ `preprocessing_report.md` (5–10 KB)

### 3. **Parquet File Content (Quick Check)**
Verify the feature matrix is readable and has expected shape:

```python
import pandas as pd
from pathlib import Path

parquet_path = Path("thesis/data/preprocessing/parquet_nielsen/specialized_CSD_feature_matrix.parquet")
df = pd.read_parquet(parquet_path)

print(f"Shape: {df.shape}")                    # Should be (rows, cols)
print(f"Columns: {df.columns.tolist()}")       # Should include 'brand', 'date', features
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Brands: {df['brand'].nunique()}")      # Should be 77 for CSD
print(f"Splits: {df['split'].value_counts()}")  # Train/val/test counts
```

**Expected output (CSD):**
- Shape: `(3234, 25)` — 3,234 rows (brand × month), 25 columns
- 77 unique brands
- Brands: HARBOE, COCA COLA, PEPSI, FANTA, etc.
- Train/val/test: 2,233/546/455 rows

### 4. **Preprocessing Report**
Open `thesis/data/preprocessing/parquet_nielsen/preprocessing_report.md` and verify:
- ✅ Timestamp (when script ran)
- ✅ Category: CSD
- ✅ Market scope: DVH EXCL. HD
- ✅ Summary table with row counts, feature count, elapsed time
- ✅ Top 20 brands list

### 5. **Run Console Output**
When you run the script, you should see:
```
================================================================================
Nielsen CSD Preprocessing Pipeline
================================================================================
Category: CSD
Market scope: DVH EXCL. HD
Min periods: 30

✓ Input validation: All 4 required files found

Step 1/5 — Loading raw data from CSV files...
  ...
Step 2/5 — Building full calendar index...
  ...
Step 3/5 — Filtering short series...
  Series kept after filter (>= 30 non-zero periods): 77 brands

Step 4/5 — Engineering features...
  Feature engineering complete

Step 5/5 — Applying split labels...
  Split labels applied

Done in 3-5s  |  Peak RAM: 350-400 MB

Outputs written to C:\dev\thesis-manifold\thesis\data\preprocessing\parquet_nielsen/
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'paths'"
**Cause**: Dynamic root finder (CLAUDE.md) not working
**Fix**: Ensure CLAUDE.md exists in project root: `C:/dev/thesis-manifold/CLAUDE.md`

### Error: "Missing required Nielsen CSV files"
**Cause**: raw_nielsen/data_csv/ doesn't have required CSVs
**Fix**: Run Nielsen download script:
```bash
python thesis/data/raw_nielsen/scripts/save_all_datasets.py
```
Requires: .env file + ODBC Driver + credentials

### Error: "ImportError: Unable to find a usable engine"
**Cause**: pyarrow not installed
**Fix**: Install dependencies:
```bash
pip install -r thesis/data/preprocessing/requirements.txt
```

### Error: "Missing optional dependency 'tabulate'"
**Cause**: tabulate library not installed
**Fix**: 
```bash
pip install tabulate
```

## Success Indicators

✅ **Preprocessing is working correctly if:**
1. Script runs without errors (exit code 0)
2. All 4 output files created in parquet_nielsen/
3. Parquet file is readable and has correct shape
4. Report shows 77 brands, 3,234 rows, 17 features
5. Split boundaries correct (train/val/test)

## Next Steps

Once verified:
1. Repeat for other categories (danskvand, energidrikke, rtd, totalbeer)
2. Load feature matrices in Jupyter notebooks:
   ```python
   from paths import THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR
   df = pd.read_parquet(THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR / "specialized_CSD_feature_matrix.parquet")
   ```
3. Run specialized_CSD.ipynb to validate downstream consumption
