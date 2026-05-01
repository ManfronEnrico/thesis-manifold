# Testing Plan: All 5 Preprocessing Scripts

**Date**: 2026-05-01  
**Status**: Ready to Test  
**Prerequisites**: Nielsen raw CSV files must exist in `thesis/data/raw_nielsen/data_csv/`

---

## Test Matrix

| Category | Script | Input Path | Output Path | Status |
|----------|--------|-----------|-------------|--------|
| CSD | `preprocessing_csd.py` | `raw_nielsen/data_csv/csd_clean_*.csv` | `parquet_nielsen/specialized_CSD/` | Ready |
| Danskvand | `preprocessing_danskvand.py` | `raw_nielsen/data_csv/danskvand_clean_*.csv` | `parquet_nielsen/specialized_danskvand/` | Ready |
| Energidrikke | `preprocessing_energidrikke.py` | `raw_nielsen/data_csv/energidrikke_clean_*.csv` | `parquet_nielsen/specialized_energidrikke/` | Ready |
| RTD | `preprocessing_rtd.py` | `raw_nielsen/data_csv/rtd_clean_*.csv` | `parquet_nielsen/specialized_rtd/` | Ready |
| Total Beer | `preprocessing_totalbeer.py` | `raw_nielsen/data_csv/totalbeer_clean_*.csv` | `parquet_nielsen/specialized_totalbeer/` | Ready |

---

## How to Test

### Option 1: Test All 5 Scripts (Sequential)
```bash
cd C:/dev/thesis-manifold

python thesis/data/preprocessing/preprocessing_csd.py
python thesis/data/preprocessing/preprocessing_danskvand.py
python thesis/data/preprocessing/preprocessing_energidrikke.py
python thesis/data/preprocessing/preprocessing_rtd.py
python thesis/data/preprocessing/preprocessing_totalbeer.py
```

**Expected output** (per script):
```
================================================================================
Nielsen {Category} Preprocessing Pipeline
================================================================================
Category: {category}
Market scope: DVH EXCL. HD
Min periods: 30

✓ Input validation: All 4 required files found

Step 1/5 — Loading raw data from CSV files...
  [CSV shapes printed]

Step 2/5 — Building full calendar index...
  Rows after calendar fill: [number]

Step 3/5 — Filtering short series...
  Series kept after filter (>= 30 non-zero periods): [number] brands

Step 4/5 — Engineering features...
  Feature engineering complete

Step 5/5 — Applying split labels...
  Split labels applied

Done in [elapsed]s  | Peak RAM: [peak_mb] MB

[Preprocessing report with summary tables]

Outputs written to C:\dev\thesis-manifold\thesis\data\preprocessing\parquet_nielsen\specialized_{CATEGORY}/
```

### Option 2: Test One Script at a Time
```bash
# Test just CSD
python thesis/data/preprocessing/preprocessing_csd.py

# If successful, test next
python thesis/data/preprocessing/preprocessing_danskvand.py
```

---

## Success Criteria

### Per Script
✅ **Script completes without errors**
- Exit code 0 (no exceptions)
- All 5 steps complete (1/5 through 5/5)

✅ **Input validation passes**
- Message: "✓ Input validation: All 4 required files found"
- If fails: Script prints helpful error message with download instructions

✅ **Output files created**
- `parquet_nielsen/specialized_{CATEGORY}/specialized_{CATEGORY}_feature_matrix.parquet`
- `parquet_nielsen/specialized_{CATEGORY}/series_index.csv`
- `parquet_nielsen/specialized_{CATEGORY}/split_dates.json`
- `parquet_nielsen/specialized_{CATEGORY}/preprocessing_report.md`

✅ **Performance reasonable**
- Elapsed time: 3–10 seconds per category
- Peak RAM: 200–500 MB per category
- No timeouts

### Data Validation
✅ **Parquet file is readable**
```python
import pandas as pd
df = pd.read_parquet("thesis/data/preprocessing/parquet_nielsen/specialized_CSD/specialized_CSD_feature_matrix.parquet")
print(df.shape)          # Should show (rows, 25) for CSD
print(df.columns.tolist())  # Should include brand, date, features, split
```

✅ **Series index is consistent**
```python
import pandas as pd
si = pd.read_csv("thesis/data/preprocessing/parquet_nielsen/specialized_CSD/series_index.csv")
print(len(si))  # Should show brand count (77 for CSD)
print(si.columns.tolist())  # Should include n_periods, total_units, train/val/test periods
```

✅ **Split dates are valid**
```python
import json
with open("thesis/data/preprocessing/parquet_nielsen/specialized_CSD/split_dates.json") as f:
    dates = json.load(f)
print(dates)  # Should have train_start, train_end, val_start, val_end, test_start, test_end
```

---

## Failure Scenarios & Solutions

### Error: "ModuleNotFoundError: No module named 'paths'"
**Cause**: Dynamic root finder (CLAUDE.md) not working  
**Solution**: Verify CLAUDE.md exists at project root

### Error: "Missing required Nielsen CSV files"
**Cause**: CSVs not downloaded or in wrong location  
**Solution**: Run Nielsen download script:
```bash
python thesis/data/raw_nielsen/scripts/save_all_datasets.py
```

### Error: "Unable to find a usable engine for Parquet"
**Cause**: pyarrow not installed  
**Solution**: 
```bash
pip install -r thesis/data/preprocessing/requirements.txt
```

### Error: "Missing optional dependency 'tabulate'"
**Cause**: tabulate library not installed  
**Solution**:
```bash
pip install tabulate
```

---

## Verification Checklist (Post-Test)

After all 5 scripts run successfully:

- [ ] `specialized_CSD/` contains 4 output files (391 KB parquet, CSVs, JSON, markdown)
- [ ] `specialized_danskvand/` contains 4 output files
- [ ] `specialized_energidrikke/` contains 4 output files
- [ ] `specialized_rtd/` contains 4 output files
- [ ] `specialized_totalbeer/` contains 4 output files
- [ ] Each parquet file is readable with pandas
- [ ] Each series_index.csv lists brands (column 'brand' exists)
- [ ] Each split_dates.json has 6 date fields
- [ ] Each preprocessing_report.md displays properly (markdown format)

---

## Next Steps (After Testing)

1. **If all pass**: Update notebooks to load from per-category folders
2. **If any fail**: Debug using error message + verify CSV files exist
3. **Document results**: Update P0017 plan with test outcomes

---

## Important Notes

- **CSD already tested**: preprocessing_csd.py has been tested end-to-end; output files exist in `specialized_CSD/`
- **Other categories untested**: preprocessing_danskvand.py, etc. are ready but haven't been run yet
- **Data requirements**: All 5 scripts require Nielsen raw CSVs to be present. If they're not downloaded, validation will fail gracefully with helpful instructions
