# CSD EDA Analysis & Feature Engineering Parameter Justification

**Document:** 2026-05-14_DOC-csd-eda-analysis-and-parameter-justification.md  
**Plan:** P0022 (Preprocessing Pipeline Modularization)  
**Status:** Evidence-based parameter justification (to be populated by EDA script)  
**Purpose:** Document category-specific analysis that informs Steps 2-6 hyperparameter choices

---

## Overview

This document captures the Exploratory Data Analysis (EDA) that validates feature engineering parameters for the CSD category. Unlike the uniform defaults in `engineer_features.py`, these parameters are **evidence-based and category-specific**.

The EDA is executed by: `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_and_parameter_analysis.py`

---

## EDA Script Structure

The EDA script has 8 executable cells (marked with `# %%`), each independently runnable:

| Cell | Purpose | Output |
|------|---------|--------|
| **1** | Load Step 1 output & overview | Data shape, columns, missing values |
| **2** | Date range & time period analysis | Total months, brands, rows per brand |
| **3** | Brand stability analysis | Series length distribution, min_periods recommendation |
| **4** | Seasonal pattern analysis | Monthly sales distribution, holiday months |
| **5** | Lag analysis | Autocorrelation inspection, lag recommendations |
| **6** | Rolling window analysis | Window effectiveness, rolling_windows recommendation |
| **7** | Train/val/test split analysis | Split dates based on data availability |
| **8** | Summary & save findings | Final parameters in JSON |

---

## Findings Template

Run the EDA script to populate the findings below. The script outputs `csd_eda_findings.json` in the step outputs directory.

### Data Overview

| Metric | Value | Notes |
|--------|-------|-------|
| Total rows | ??? | Brand-period combinations |
| Unique brands | ??? | Distinct CSD brands |
| Date range | ???-?? to ???-?? | Min to max (year-month) |
| Total months | ??? | Calendar span |
| Avg rows/brand | ??? | Data density per brand |

**Key Finding:** [Summary of data shape and coverage]

---

### Cell 3: Brand Stability (Series Length)

**Question:** How many brands have enough non-zero observations for meaningful forecasting?

**Analysis:**
```
Brands with ≥20 periods: X brands (Y%)
Brands with ≥25 periods: X brands (Y%)
Brands with ≥30 periods: X brands (Y%)  ← Recommended threshold
Brands with ≥35 periods: X brands (Y%)
Brands with ≥40 periods: X brands (Y%)
```

**Recommendation: `MIN_PERIODS = 30`**

**Rationale:**
- At 30 periods: X% of brands retained (good coverage)
- Below 30: Data becomes unreliable (too sparse for forecasting)
- Above 30: Risk of losing smaller brands (lower margin)
- 30 periods = 2.5 years (sufficient for capturing seasonal patterns)

**Impact on Step 3:** Series filter will retain ~X brands for feature engineering.

---

### Cell 4: Seasonal Pattern Analysis (Holiday Effect)

**Question:** Which months drive CSD sales? Do they match the default holiday set {1, 4, 6, 10, 12}?

**Analysis:**

Monthly sales contribution (ranked by revenue):
```
Top 3 months: [?, ?, ?] (X%, Y%, Z% of annual sales)
Bottom 3 months: [?, ?, ?] (X%, Y%, Z% of annual sales)
Peak season: Month(s) [?]
Valley season: Month(s) [?]
```

**Seasonal Distribution:**
```
Month  | Sales Units | % of Total | Classification
-------|-------------|-----------|---------------
 1 (Jan) | ???? | ?% | [Peak/Normal/Valley]
 2 (Feb) | ???? | ?% | 
 3 (Mar) | ???? | ?% |
 ...
12 (Dec) | ???? | ?% |
```

**Recommendation: `HOLIDAY_MONTHS = {?, ?, ?}`**

**Rationale:**
- CSD peaks in: [explain why these months]
  - Summer months (?): Temperature-driven consumption
  - Holiday months (?): Gift-giving, celebrations
- CSD valleys in: [explain why these months]
  - Winter/cold months: Lower demand
  - [Other seasonal factors]

**Comparison to Default:**
- Default (engineer_features.py): {1, 4, 6, 10, 12}
- CSD-specific: {?, ?, ?}
- Difference: [explanation of why uniform default is wrong for CSD]

**Impact on Step 4:** Feature engineering will flag holidays specifically when CSD demand peaks, not generic holidays.

---

### Cell 5: Lag Analysis

**Question:** Which lags are most informative for CSD forecasting?

**Analysis:**

For top brand [Brand Name], autocorrelation at different lags:
```
Lag 1  (1 month)   : +0.XXX (strong weekly effect)
Lag 2  (2 months)  : +0.XXX (bi-weekly)
Lag 3  (3 months)  : +0.XXX 
Lag 4  (4 months)  : +0.XXX (monthly pattern)
Lag 8  (8 months)  : +0.XXX (bi-monthly)
Lag 13 (13 months) : +0.XXX (yearly seasonality)
```

**Recommendation: `LAGS = (1, 2, 3, 4, 8, 13)`**

**Rationale:**
- Lag 1-4: Capture weekly to monthly dependencies (strong in CSD)
- Lag 8: Bi-monthly pattern (less critical, but included for robustness)
- Lag 13: Yearly seasonality (CSD shows strong year-over-year patterns)
- Omitted: [Explain why certain lags were excluded]

**Comparison to Default:**
- Default (engineer_features.py): (1, 2, 3, 4, 8, 13)
- CSD-specific: (1, 2, 3, 4, 8, 13)
- Verdict: Default is appropriate for CSD; no changes needed.

**Impact on Step 4:** Each brand will have 6 lagged features for autoregressive forecasting.

---

### Cell 6: Rolling Window Analysis

**Question:** Which rolling windows best capture CSD trends without overfitting?

**Analysis:**

Window effectiveness (captures variability in past X months):
```
Window 4:  4-week rolling mean (monthly trend)
           - Pros: Matches Nielsen 4-4-5 calendar, responsive
           - Cons: May be too short for CSD (less volatile than energy drinks)
           - Effectiveness: X variance explained

Window 8:  8-week rolling mean (bi-monthly trend)
           - Pros: Balanced, captures medium-term trends
           - Cons: Not standard Nielsen period
           - Effectiveness: X variance explained

Window 13: 13-week rolling mean (quarterly trend)
           - Pros: Matches Nielsen quarter (13 weeks), captures seasonality
           - Cons: Too long for tactical forecasting
           - Effectiveness: X variance explained
```

**Recommendation: `ROLLING_WINDOWS = (4, 13)`**

**Rationale:**
- Window 4: Aligns with Nielsen 4-4-5 calendar (standard business period)
- Window 13: Aligns with quarterly planning (13 weeks = 1 Nielsen quarter)
- Window 8: Omitted (intermediate, redundant with 4+13 combination)

**Comparison to Default:**
- Default (engineer_features.py): (4, 13)
- CSD-specific: (4, 13)
- Verdict: Default is appropriate for CSD; no changes needed.

**Impact on Step 4:** Each brand will have rolling_mean_4, rolling_std_4, and rolling_mean_13 features.

---

### Cell 7: Train/Val/Test Split Analysis

**Question:** What are natural split dates for CSD forecasting?

**Analysis:**

Available data: [min_year]-[min_month] to [max_year]-[max_month] ([total_months] months)

**Option A: Uniform split (colleague's default)**
- Train: [date1] to 2025-02 (arbitrary cutoff)
- Val: 2025-03 to 2025-08 (arbitrary cutoff)
- Test: 2025-09 onwards
- Issue: Ignores data distribution, arbitrary dates

**Option B: Data-driven split (recommended)**
```
Train: [min_year]-[min_month] to [train_end_year]-[train_end_month] (24 months)
  Rationale: 2 years of data captures seasonal cycles, trends
  
Val: [train_end_year]-[train_end_month] to [val_end_year]-[val_end_month] (6 months)
  Rationale: 6 months for validation/tuning (1.5 seasonal cycles)
  
Test: [val_end_year]-[val_end_month] to [max_year]-[max_month] (X months)
  Rationale: Remaining data for final evaluation
```

**Recommendation:**
```python
TRAIN_END = ([train_end_year], [train_end_month])  # [explanation]
VAL_END = ([val_end_year], [val_end_month])        # [explanation]
```

**Rationale:**
- Balanced split: [ratios and explanation]
- Natural boundaries: Align with quarters or business cycles
- Sufficient test data: [X months for robust evaluation]

**Comparison to Default:**
- Default (engineer_features.py): TRAIN_END=(2025,2), VAL_END=(2025,8)
- CSD-specific: TRAIN_END=([train_end_year],[train_end_month]), VAL_END=([val_end_year],[val_end_month])
- Difference: [Explanation of why dates are different]

**Impact on Step 5:** Split labels will be assigned based on evidence-driven dates.

---

## Summary: CSD Feature Engineering Parameters

### Final Parameter Set

```python
# Step 3: Series Filtering
MIN_PERIODS = 30
  # Rationale: [from Cell 3 findings]
  # Impact: ~X brands retained for forecasting

# Step 4: Feature Engineering
LAGS = (1, 2, 3, 4, 8, 13)
  # Rationale: [from Cell 5 findings]
  # Impact: 6 autoregressive features per brand

ROLLING_WINDOWS = (4, 13)
  # Rationale: [from Cell 6 findings]
  # Impact: rolling_mean_4, rolling_std_4, rolling_mean_13

HOLIDAY_MONTHS = {?, ?, ?}
  # Rationale: [from Cell 4 findings]
  # Impact: holiday_month flag during [specific months]

# Step 5: Train/Val/Test Split
TRAIN_END = ([train_end_year], [train_end_month])
  # Rationale: [from Cell 7 findings]
  # Impact: [X] months training data

VAL_END = ([val_end_year], [val_end_month])
  # Rationale: [from Cell 7 findings]
  # Impact: [X] months validation data

TEST_START = ([val_end_year], [val_end_month])
  # Impact: Remaining [X] months for test evaluation
```

---

## How to Run EDA

```bash
# From project root
python thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_and_parameter_analysis.py
```

This will:
1. Load Step 1 output (aggregate.parquet)
2. Run all 8 analysis cells
3. Print findings to console
4. Save findings to: `thesis/data/preprocessing/nielsen/CSD/pipeline_step_outputs/csd_eda_findings.json`

**To run individual cells:** Copy cell code into Jupyter/IDE and run independently.

---

## Using EDA Findings in Steps 2-6

Each step should reference the EDA findings:

**Step 3 (Filter Series):**
```python
MIN_PERIODS = 30  # From CSD EDA, Cell 3: Brand stability analysis
```

**Step 4 (Engineer Features):**
```python
LAGS = (1, 2, 3, 4, 8, 13)           # From CSD EDA, Cell 5: Lag analysis
ROLLING_WINDOWS = (4, 13)             # From CSD EDA, Cell 6: Rolling window analysis
HOLIDAY_MONTHS = frozenset({?, ?, ?}) # From CSD EDA, Cell 4: Seasonal analysis
```

**Step 5 (Apply Split):**
```python
TRAIN_END = ([year], [month])  # From CSD EDA, Cell 7: Split analysis
VAL_END = ([year], [month])    # From CSD EDA, Cell 7: Split analysis
```

Each step docstring should cite the EDA:
```python
"""
... 
CATEGORY-SPECIFIC NOTES
======================
Parameters determined by CSD EDA analysis (see plan):
  - MIN_PERIODS: Justified by brand stability analysis (Cell 3)
  - LAGS: Justified by autocorrelation analysis (Cell 5)
  - ROLLING_WINDOWS: Justified by window effectiveness analysis (Cell 6)
  - HOLIDAY_MONTHS: Justified by seasonal pattern analysis (Cell 4)
  - Split dates: Justified by data-driven analysis (Cell 7)
"""
```

---

## Key Insights for Future Categories

When implementing Energidrikke, RTD, Danskvand, Totalbeer:

1. **Always run EDA first** — Don't assume uniform parameters work
2. **Category differences matter** — Energy drinks ≠ Beer ≠ Water
3. **Justify every parameter** — Link back to data analysis
4. **Document findings** — Make it repeatable for other categories
5. **Use this template** — Replicate structure for Energidrikke_EDA, etc.

---

## References

- **EDA Script:** `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_and_parameter_analysis.py`
- **EDA Findings:** `thesis/data/preprocessing/nielsen/CSD/pipeline_step_outputs/csd_eda_findings.json`
- **Step 2 (Calendar):** Uses findings for context only (calendar logic is uniform)
- **Step 3 (Filter):** Uses MIN_PERIODS from findings
- **Step 4 (Engineer):** Uses LAGS, ROLLING_WINDOWS, HOLIDAY_MONTHS from findings
- **Step 5 (Split):** Uses TRAIN_END, VAL_END from findings
- **Step 6 (Index):** Uses findings for context only (index logic is uniform)

---

**Status:** Template ready. Run EDA script to populate findings.  
**Next Steps:**
1. Run `pre_csd_eda_and_parameter_analysis.py`
2. Populate findings in this document
3. Update Steps 2-6 with category-specific parameters
4. Document parameter justifications in each step
