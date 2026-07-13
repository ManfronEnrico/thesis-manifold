# Testing Guide: Preprocessing Scripts with Data Previews

**Date**: 2026-05-01  
**Update**: All scripts now include intermediate data previews  
**Status**: Ready to test

---

## What's New

All 5 preprocessing scripts now display **intermediate data previews** at each step of the pipeline. You'll see exactly what the data looks like after each transformation.

---

## Preview Outputs Per Step

### Step 1: Load Raw Data
**What you'll see**:
```
✓ Aggregated data (first 10 rows):
brand  period_year  period_month  sales_units  sales_value  sales_liters  promo_units  weighted_dist
COCA COLA        2019            1      [values...]
PEPSI            2019            1      [values...]
...
```

**What it shows**: Raw aggregated data (brand × month), before any preprocessing

---

### Step 2: Build Calendar (Fill Missing Months)
**What you'll see**:
```
Rows after calendar fill: 5,712
Date range: 2019-01-01 to 2025-08-31
✓ Calendar-filled data (first 10 rows):
brand  date          sales_units  sales_value  sales_liters  promo_units  weighted_dist
COCA COLA  2019-01-01      [values...]
COCA COLA  2019-02-01      [values...]
HARBOE     2019-01-01      0            0           0            0            [values...]
```

**What it shows**: Every brand now has every month (no gaps), zeros filled for missing months

---

### Step 3: Filter Short Series (Drop Sparse Brands)
**What you'll see**:
```
Series kept after filter (>= 30 non-zero periods): 77 brands
✓ Filtered data (first 10 rows):
brand  date          sales_units  ...
COCA COLA  2019-01-01      [values...]
COCA COLA  2019-02-01      [values...]
```

**What it shows**: Only brands with ≥30 non-zero months remain (sparse brands dropped)

---

### Step 4: Engineer Features (Create Lags, Rolling Stats, Calendar)
**What you'll see**:
```
Feature engineering complete
Columns: 25
✓ Feature-engineered data (first 5 rows, selected columns):
brand  date          sales_units  log_sales_units  lag_1  rolling_mean_4  month  holiday_month
COCA COLA  2019-01-01      [values...]  [values...]  NaN    NaN            1      1
COCA COLA  2019-02-01      [values...]  [values...]  [val]  NaN            2      0
COCA COLA  2019-03-01      [values...]  [values...]  [val]  [value]        3      0
```

**What it shows**: 
- All 25 columns now present (17 features + base columns)
- Lags populated (earliest rows have NaN since no prior data)
- Rolling mean populated (needs 4+ prior rows)
- Calendar features (month, holiday_month) filled

---

### Step 5: Apply Split Labels
**What you'll see**:
```
Split labels applied
Split distribution: {'train': 2233, 'val': 546, 'test': 455}
✓ Final feature matrix (first 5 rows):
brand  date          sales_units  split
COCA COLA  2019-01-01      [values...]  train
COCA COLA  2019-02-01      [values...]  train
COCA COLA  2025-02-01      [values...]  train
COCA COLA  2025-03-01      [values...]  val
COCA COLA  2025-09-01      [values...]  test
```

**What it shows**: 
- Split column added (train/val/test)
- Train/val/test distribution shown
- Final feature matrix ready for models

---

## How to Test All 5 Scripts

```bash
# Run from project root
cd C:\dev\thesis-manifold

# Test all in sequence
python thesis/data/preprocessing/preprocessing_csd.py
python thesis/data/preprocessing/preprocessing_danskvand.py
python thesis/data/preprocessing/preprocessing_energidrikke.py
python thesis/data/preprocessing/preprocessing_rtd.py
python thesis/data/preprocessing/preprocessing_totalbeer.py
```

Each script will print:
1. Project root found: `Project root found at: C:\dev\thesis-manifold`
2. Input/output dirs: `Input directory: ...` and `Output directory: ...`
3. All 5 steps with previews
4. Final summary with elapsed time and RAM usage

---

## Expected Total Output

**Per script**: ~150–200 lines of output (with previews)
- Header (title, category, market scope)
- Input validation (✓ 4 files found)
- Step 1: aggregated data preview (10 rows)
- Step 2: calendar-filled data preview (10 rows, with date range)
- Step 3: filtered data preview (10 rows)
- Step 4: feature-engineered data preview (5 key columns)
- Step 5: final feature matrix preview (5 rows with split labels)
- Summary: brand count, elapsed time, peak RAM
- Preprocessing report (markdown table + top 20 brands)
- Output location confirmation

**Total for all 5**: ~15–20 minutes execution time (depends on data size)

---

## Verifying Success

After each script completes, look for:

✅ **No errors** (exit code 0)  
✅ **All 5 steps completed** (Step 1/5 through Step 5/5)  
✅ **Data previews show reasonable values**
  - First brand should be a recognizable brand (e.g., COCA COLA, PEPSI)
  - Sales units should be positive numbers (not NaN until sufficient history)
  - Lags should be populated after row 13 (lag_13 needs 13 prior months)
  - Split distribution should match expected: train ~60%, val ~15%, test ~15%

✅ **Output files created**
  - `parquet_nielsen/specialized_{CATEGORY}/specialized_{CATEGORY}_feature_matrix.parquet`
  - `parquet_nielsen/specialized_{CATEGORY}/series_index.csv`
  - `parquet_nielsen/specialized_{CATEGORY}/split_dates.json`
  - `parquet_nielsen/specialized_{CATEGORY}/preprocessing_report.md`

✅ **Performance reasonable**
  - Elapsed time: 3–10 seconds per category
  - Peak RAM: 200–500 MB

---

## If Something Goes Wrong

### "Missing required Nielsen CSV files"
→ Nielsen raw data not downloaded. Run:
```bash
python thesis/data/raw_nielsen/scripts/save_all_datasets.py
```

### Script hangs or times out
→ Check RAM and disk space. Previews should print within 1–2 minutes per script.

### Data preview shows all NaN
→ Usually early in the pipeline (lags need history). Check subsequent steps to verify data fills in.

### Output files not created
→ Check error message for permission issues or missing directories. Script should auto-create `parquet_nielsen/specialized_{CATEGORY}/`.

---

## Next Steps After Testing

Once all 5 scripts pass:

1. ✅ Verify output files exist in each category subfolder
2. ✅ Spot-check the data previews (sanity check on values)
3. ✅ Test loading from Jupyter notebooks (update notebook paths)
4. 📝 Document any differences between categories in P0017 outcome

All scripts are ready for execution!
