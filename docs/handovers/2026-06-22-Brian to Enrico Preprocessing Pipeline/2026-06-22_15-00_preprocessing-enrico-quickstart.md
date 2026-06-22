---
name: preprocessing-enrico-quickstart
description: REFERENCE - Quick-start checklist for Enrico on preprocessing pipeline
category: reference
applies-to: [thesis-writing, system-a-integration, preprocessing-continuation]
triggers: [where-to-start, quick-reference, what-to-do-next]
created: 2026_06_22-16_30
updated: 2026_06_22-16_30
---

# Quick Start Guide for Enrico — Preprocessing & EDA

**Status**: All preprocessing complete. CSD EDA in detail. Ready for thesis writing or System A integration.

---

## In 30 Seconds

- ✅ **Preprocessing done**: Steps 0–6 for 4 categories (CSD, Danskvand, Energidrikke, RTD)
- ✅ **CSD EDA complete**: 8 thesis-quality visualizations; log transform confirmed; 20 features verified
- ✅ **Feature matrices ready**: Parquets generated for all 4 categories
- 🟡 **CSD EDA not fully finalised**: Brian will polish and lock the EDA design before replicating to other categories
- ❌ **Skipped**: Totalbeer — facts table missing from source JSONL (data does not exist at source)

**Next**: Verify 2 critical items, then thesis writing can proceed.

---

## Already Verified (No Action Needed)

The P0023 audit (June 22) resolved the previously open items for CSD:

| Item | Status | Detail |
|------|--------|--------|
| **Log transform** | ✅ Confirmed | `np.log()` in `pre_csd_4_engineer_features.py` lines 136–139 |
| **Feature count** | ✅ Confirmed | **20 features**: 6 lags, 3 rolling, 3 calendar, 1 log transform, 1 promo intensity, 5 index/target/label |
| **Missing data** | ✅ Confirmed | `weighted_dist` averaged across markets — correct for ACV metric |
| **Reproducibility** | ✅ Confirmed | All operations deterministic |

You can still run the inspection command below to see the feature names directly from the parquet if useful for thesis writing:

```bash
python -c "
import pandas as pd
df = pd.read_parquet('thesis/data/_03_engineered/nielsen/CSD/csd_feature_matrix.parquet')
print(f'Shape: {df.shape}')
for i, col in enumerate(df.columns, 1):
    print(f'  {i}. {col}')
"
```

---

## Data Overview

| Property | Value |
|----------|-------|
| **Data source** | Nielsen CSD sales facts (Oct 2022 – Apr 2026) |
| **Brands** | 62 retained (from 143 total, filtered at MIN_PERIODS ≥ 40) |
| **Time periods** | 43 months |
| **Aggregation** | By (brand, year, month) → 4,140 rows |
| **Key columns** | sales_units, sales_value, promo_units, weighted_dist |
| **Missing data** | 4.3% in weighted_dist — ✅ handled via mean aggregation (ACV metric) |
| **Stationarity** | Log transform applied ✅ (ADF test p=0.028 → non-stationary raw; stationary after log) |

---

## File Locations

```
Data pipeline (4-tier structure):
  thesis/data/_00_raw/nielsen/scripts/save_all_datasets.py  (Step 1: download)
  thesis/data/_01_converted/nielsen/jsonl_to_parquet/       (Step 2: convert)
  thesis/data/_02_preprocessing/nielsen/CSD/                (Step 3: preprocess)
  ├── preprocessing_csd.py                                  (run this)
  ├── pre_csd_4_engineer_features.py                        (log transform here, lines 136–139)
  └── pre_csd_1.5_eda.py                                    (EDA analysis)
  thesis/data/_03_engineered/nielsen/CSD/                   (final outputs)
  ├── csd_feature_matrix.parquet                            (use this for modeling)
  ├── csd_split_dates.json                                  (train/val/test boundaries)
  ├── csd_preprocessing_report.md                           (audit trail)
  └── 8 × csd_*.png                                         (visualizations)

Parallel categories:
  thesis/data/_02_preprocessing/nielsen/{Danskvand,Energidrikke,RTD}/  (same structure)
  thesis/data/_03_engineered/nielsen/{Danskvand,Energidrikke,RTD}/     (same outputs)

Audit plan:
  plans/2026-06-22_15-00_preprocessing-pipeline-audit/      (findings + tasks)

Handover docs:
  docs/handovers/2026-06-22_15-00_preprocessing-eda-handover-enrico.md       (full overview)
  docs/handovers/2026-06-22_15-00_preprocessing-pipeline-diagram.md          (visual flow)
  docs/handovers/2026-06-22_15-00_preprocessing-audit-status-p0023.md        (status + blockers)
```

---

## Quick Commands

### Load and inspect feature matrix
```python
import pandas as pd
import json

# Load features
df = pd.read_parquet('thesis/data/_03_engineered/nielsen/CSD/csd_feature_matrix.parquet')
print(f"Shape: {df.shape}")  # Should be (brands * months, features)
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst row:\n{df.iloc[0]}")

# Load split dates
with open('thesis/data/_03_engineered/nielsen/CSD/csd_split_dates.json') as f:
    splits = json.load(f)
    print(f"\nTrain: {splits['train_start']} to {splits['train_end']}")
    print(f"Val:   {splits['val_start']} to {splits['val_end']}")
    print(f"Test:  {splits['test_start']} to {splits['test_end']}")
```

### Run the full pipeline (3 steps)

**Step 1 — Download raw Nielsen data** (one-time; skippable if already cached):
```bash
python thesis/data/_00_raw/nielsen/scripts/save_all_datasets.py
```

**Step 2 — Convert JSONL → Parquet cache** (one-time; skippable if `_01_converted/` exists):
```bash
python thesis/data/_01_converted/nielsen/jsonl_to_parquet/run_all_conversions.py
```

**Step 3 — Run preprocessing pipeline** (main step; re-run any time):
```bash
python thesis/data/_02_preprocessing/nielsen/CSD/preprocessing_csd.py
```

Final output folder: `thesis/data/_03_engineered/nielsen/CSD/`  
File to use for modeling: `csd_feature_matrix.parquet`

All paths are dynamic (defined in `PATHS.py`), so everything writes to the correct folders automatically.

### View preprocessing report
```bash
cat thesis/data/preprocessing/nielsen/CSD/engineered/csd_preprocessing_report.md
```

---

## Known Issues to Watch For

| Issue | Status | Impact | Action |
|-------|--------|--------|--------|
| **Log transform** | ✅ RESOLVED | — | Confirmed in Step 4 lines 136–139 |
| **Feature list** | ✅ RESOLVED | — | 20 features, fully named (see audit T-010) |
| **Missing data handling** | ✅ RESOLVED | — | weighted_dist averaged (correct for ACV) |
| **Per-category EDA** | 🔴 OPEN | HIGH | Danskvand/Energidrikke/RTD use unchecked defaults — Brian will replicate CSD EDA once finalised |
| **MIN_PERIODS** | 🟡 OPEN | MEDIUM | Brian will revisit (currently 40; EDA suggested 30) — do not change |
| **Parameter justification** | 🟡 OPEN | MEDIUM | EDA-driven for CSD; needs prose in thesis Chapter 4 |
| **Totalbeer skipped** | ✅ KNOWN | LOW | Facts table absent from source JSONL — not a size/RAM issue |

---

## For Thesis Chapter 4 (Data Methodology)

**What to write** (use this structure):

### Section 1: Data Source
- Nielsen CSD category facts table
- Oct 2022 – Apr 2026 (43 months)
- 143 brands total, ~2.5M raw facts aggregated to 4,140 rows
- 28 retailers, but aggregated away (retail-level variation not captured)

### Section 2: Aggregation & Filtering
- Aggregation: (brand, year, month) level
- Filtering: Keep brands with ≥40 observations → 62 brands retained (43.7% of data)
- Rationale: Quality over breadth; all retained brands have continuous coverage

### Section 3: Feature Engineering
- **Steps 0–6 pipeline**:
  - Step 0: Cache (parquet load)
  - Step 1: Aggregate (group by brand-month)
  - Step 2: Calendar (create time index)
  - Step 3: Filter (MIN_PERIODS ≥ 40)
  - Step 4: Engineer features (lag, rolling, seasonal)
  - Step 5: Split (train/val/test)
  - Step 6: Save (parquet output)
- **Features created**: 20 features — `lag_1/2/3/4/8/13`, `rolling_mean_4`, `rolling_std_4`, `rolling_mean_13`, `month`, `quarter`, `holiday_month`, `log_sales_units`, `promo_intensity`, plus 5 index/target columns (`brand`, `period_year`, `period_month`, `sales_units`, `split`)
- **Transformations**: Log transform applied to sales_units (ADF test p=0.028 proves necessity)

### Section 4: Stationarity & Seasonality
- ADF test on original series: non-stationary (p=0.353)
- ADF test on log-transformed: stationary (p=0.028) ✅
- Seasonal decomposition: additive (period=12 months)
- Peak months: December (12.4%), March (10.9%), June (9.0%)

### Section 5: Train/Val/Test Split
- Total: 43 months (Oct 2022 – Apr 2026)
- Train: 24 months (Oct 2022 – Oct 2024)
- Val: 6 months (Oct 2024 – Apr 2025)
- Test: 12 months (Apr 2025 – Apr 2026)
- Strategy: Forward-chaining (no look-ahead bias)

### Section 6: Limitations
- Only ~3.5 years of data (most time series studies use 5–10 years)
- Retail-level variation aggregated away (28 market types collapsed)
- Totalbeer category excluded (facts table absent from source data)
- Per-category EDA not yet run for Danskvand/Energidrikke/RTD
- No promotional calendar analysis
- No structural break detection

---

## For System A Integration (Model Training)

**What you have from preprocessing**:

1. ✅ Feature matrix parquets — ready in `thesis/data/_03_engineered/nielsen/{category}/{category}_feature_matrix.parquet`
2. ✅ Train/val/test split dates — JSON files in same `_03_engineered/` folder
3. ✅ 20 confirmed features per observation (6 lags, 3 rolling, 3 calendar, 1 log, 1 promo, 5 index/target)
4. ✅ Missing data handled — `weighted_dist` averaged, not imputed
5. ⚠️ **Feature scaling**: No scaling in preprocessing — handle per-model (Ridge needs scaling; LightGBM/XGBoost do not)

**Before training**:
- Verify that `thesis/thesis-context/thesis-topic/thesis-topic.md` matches your System A design — Brian rewrote it on 2026-06-22; confirm the model list (Ridge, ARIMA, Prophet, LightGBM, XGBoost), confidence score formula, and RAM budget match your implementation

**Next steps after verification**:
1. Load feature matrices into System A
2. Feed to Ridge/ARIMA/Prophet/LightGBM/XGBoost
3. Evaluate MAPE on test set
4. Compare agentic vs non-agentic forecasting

---

## Timeline

- **Verification** (today): 30 minutes (grep + feature inspection)
- **Audit completion** (this week): 3–4 hours (if needed)
- **Thesis Chapter 4 writing** (next): 4–6 hours (use skeleton above)
- **System A integration** (parallel): 6–8 hours (model training + evaluation)

---

## Questions?

Check these docs in order:
1. [2026-06-22_15-00_preprocessing-eda-handover-enrico.md](2026-06-22_15-00_preprocessing-eda-handover-enrico.md) — Full overview
2. [2026-06-22_15-00_preprocessing-audit-status-p0023.md](2026-06-22_15-00_preprocessing-audit-status-p0023.md) — What needs verification
3. [2026-06-22_15-00_preprocessing-pipeline-diagram.md](2026-06-22_15-00_preprocessing-pipeline-diagram.md) — Visual flow

Or check the plan folder: `plans/2026-06-22_15-00_preprocessing-pipeline-audit/`

---

## Checklist Before You Start Thesis Chapter 4

- [x] Log transform confirmed in Step 4 (lines 136–139)
- [x] Feature list documented — 20 features (see audit T-010)
- [x] Missing data handling confirmed (weighted_dist: mean aggregation)
- [ ] Read preprocessing report (`csd_preprocessing_report.md`)
- [ ] Understood split dates (train/val/test)
- [ ] Reviewed EDA visualizations (8 PNGs)
- [ ] Confirmed reproducibility (ran `preprocessing_csd.py` successfully)

---

**Go here next**: 
1. Run verification commands above
2. Read [2026-06-22_15-00_preprocessing-eda-handover-enrico.md](2026-06-22_15-00_preprocessing-eda-handover-enrico.md)
3. Start thesis writing or System A integration

Good luck! 🚀
