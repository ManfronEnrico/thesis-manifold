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
- ✅ **EDA complete**: 8 thesis-quality visualizations for CSD
- ✅ **Feature matrices ready**: Parquets generated for all 4 categories
- 🟡 **Needs verification**: Log transform implementation, exact feature list (24 features)
- ❌ **Skipped**: Totalbeer (too large for parquet conversion)

**Next**: Verify 2 critical items, then thesis writing can proceed.

---

## Critical Verification (Do This First)

### 1. Verify Log Transform Implementation (10 minutes)

**Why**: EDA proves log transform is statistically necessary. But is Step 4 actually doing it?

**Action**:
```bash
# Search for log() in feature engineering code
grep -n "np.log\|\.log()" thesis/data/preprocessing/nielsen/CSD/pre_csd_4_engineer_features.py
```

**Expected result**: You should find `np.log(sales_units)` or similar before lag features are created.

**If NOT found**: This is a **critical bug**. Need to add it before thesis writing.

---

### 2. Verify Feature List (10 minutes)

**Why**: Need to document the 24 features for thesis methodology chapter.

**Action**:
```bash
python -c "
import pandas as pd
df = pd.read_parquet('thesis/data/preprocessing/nielsen/CSD/engineered/csd_feature_matrix.parquet')
print(f'Shape: {df.shape}')
print(f'Features ({len(df.columns)}):')
for i, col in enumerate(df.columns, 1):
    print(f'  {i}. {col}')
"
```

**Write down**: The exact column names (copy-paste into a note or doc).

---

## Data Overview

| Property | Value |
|----------|-------|
| **Data source** | Nielsen CSD sales facts (Oct 2022 – Mar 2026) |
| **Brands** | 62 (filtered from 142 total) |
| **Time periods** | 42 months |
| **Aggregation** | By (brand, year, month) → 4,040 rows |
| **Key columns** | sales_units, sales_value, promo_units, weighted_dist |
| **Missing data** | 4.3% in weighted_dist (handled?) |
| **Stationarity** | Log transform required (ADF test p=0.028) |

---

## File Locations

```
Preprocessing scripts:
  thesis/data/preprocessing/nielsen/CSD/                    (main category)
  ├── preprocessing_csd.py                                  (run this)
  ├── pre_csd_4_engineer_features.py                        (verify log transform here)
  ├── pre_csd_1.5_eda.py                                    (EDA analysis)
  └── engineered/
      ├── csd_feature_matrix.parquet                        (feature data)
      ├── csd_split_dates.json                              (train/val/test)
      ├── csd_preprocessing_report.md                       (audit trail)
      └── 8 × csd_*.png                                     (visualizations)

Parallel categories:
  thesis/data/preprocessing/nielsen/{Danskvand,Energidrikke,RTD}/  (same structure)

Audit plan:
  plans/2026-06-22_15-00_preprocessing-pipeline-audit/      (findings + tasks)

Handover docs:
  docs/handovers/preprocessing-eda-handover-enrico.md       (full overview)
  docs/handovers/preprocessing-pipeline-diagram.md          (visual flow)
  docs/handovers/preprocessing-audit-status-p0023.md        (status + blockers)
```

---

## Quick Commands

### Load and inspect feature matrix
```python
import pandas as pd
import json

# Load features
df = pd.read_parquet('thesis/data/preprocessing/nielsen/CSD/engineered/csd_feature_matrix.parquet')
print(f"Shape: {df.shape}")  # Should be (brands * months, features)
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst row:\n{df.iloc[0]}")

# Load split dates
with open('thesis/data/preprocessing/nielsen/CSD/engineered/csd_split_dates.json') as f:
    splits = json.load(f)
    print(f"\nTrain: {splits['train_start']} to {splits['train_end']}")
    print(f"Val:   {splits['val_start']} to {splits['val_end']}")
    print(f"Test:  {splits['test_start']} to {splits['test_end']}")
```

### Run preprocessing end-to-end
```bash
cd thesis/data/preprocessing/nielsen/CSD
python preprocessing_csd.py
```

Expected output: New `csd_feature_matrix.parquet` in `engineered/` folder (takes ~2–5 minutes)

### View preprocessing report
```bash
cat thesis/data/preprocessing/nielsen/CSD/engineered/csd_preprocessing_report.md
```

---

## Known Issues to Watch For

| Issue | Status | Impact | Action |
|-------|--------|--------|--------|
| **Log transform missing** | ❓ UNKNOWN | 🔴 HIGH | Verify (see verification checklist) |
| **Feature list unclear** | ❓ UNKNOWN | 🔴 HIGH | Document (see verification checklist) |
| **Missing data handling** | ❓ UNKNOWN | 🟡 MEDIUM | Check Step 1 aggregation code |
| **Parameter justification** | ✅ KNOWN | 🟡 MEDIUM | Document in thesis as empirical |
| **Only 4 years of data** | ✅ KNOWN | 🟡 MEDIUM | Note as limitation in thesis |
| **Totalbeer skipped** | ✅ KNOWN | 🟢 LOW | Defer to future work |

---

## For Thesis Chapter 4 (Data Methodology)

**What to write** (use this structure):

### Section 1: Data Source
- Nielsen CSD category facts table
- Oct 2022 – Mar 2026 (42 months)
- 142 brands, ~2.5M raw facts aggregated to 4,040 rows
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
- **Features created**: [LIST THEM HERE - needs verification]
- **Transformations**: Log transform applied to sales_units (ADF test p=0.028 proves necessity)

### Section 4: Stationarity & Seasonality
- ADF test on original series: non-stationary (p=0.353)
- ADF test on log-transformed: stationary (p=0.028) ✅
- Seasonal decomposition: additive (period=12 months)
- Peak months: December (12.4%), March (10.9%), June (9.0%)

### Section 5: Train/Val/Test Split
- Total: 42 months (Oct 2022 – Mar 2026)
- Train: 24 months (Oct 2022 – Oct 2024)
- Val: 6 months (Oct 2024 – Apr 2025)
- Test: 12 months (Apr 2025 – Mar 2026)
- Strategy: Forward-chaining (no look-ahead bias)

### Section 6: Limitations
- Only 3–4 years of data (most time series studies use 5–10 years)
- Retail-level variation aggregated away
- Totalbeer category excluded (dataset size constraint)
- No promotional calendar analysis
- No structural break detection

---

## For System A Integration

**What you need from preprocessing**:

1. ✅ Feature matrix parquets (ready in `engineered/` folders)
2. ✅ Train/val/test split dates (JSON files present)
3. ❓ **Exact feature list** (need to document from Step 4)
4. ❓ **Feature scaling info** (do they need standardization?)
5. ❓ **Missing data handling** (how were they imputed?)

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
1. [preprocessing-eda-handover-enrico.md](preprocessing-eda-handover-enrico.md) — Full overview
2. [preprocessing-audit-status-p0023.md](preprocessing-audit-status-p0023.md) — What needs verification
3. [preprocessing-pipeline-diagram.md](preprocessing-pipeline-diagram.md) — Visual flow

Or check the plan folder: `plans/2026-06-22_15-00_preprocessing-pipeline-audit/`

---

## Checklist Before You Start Thesis Chapter 4

- [ ] Verified log transform in Step 4 (critical!)
- [ ] Documented exact feature list (24 features)
- [ ] Checked missing data handling (weighted_dist)
- [ ] Read preprocessing report (`csd_preprocessing_report.md`)
- [ ] Understood split dates (train/val/test)
- [ ] Reviewed EDA visualizations (8 PNGs)
- [ ] Confirmed reproducibility (ran `preprocessing_csd.py` successfully)

---

**Go here next**: 
1. Run verification commands above
2. Read [preprocessing-eda-handover-enrico.md](preprocessing-eda-handover-enrico.md)
3. Start thesis writing or System A integration

Good luck! 🚀
