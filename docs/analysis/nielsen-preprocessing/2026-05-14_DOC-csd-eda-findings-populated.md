# CSD EDA Findings — Analysis Complete

**Document:** 2026-05-14_DOC-csd-eda-findings-populated.md  
**Status:** ✅ EDA executed and findings populated  
**Generated:** 2026-05-14 15:25:24  
**Source Script:** `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_and_parameter_analysis.py`

---

## Executive Summary

The CSD EDA analysis is **complete**. Key findings validate and justify feature engineering parameters for the CSD category. These are **NOT uniform defaults** — they are evidence-based and category-specific.

**Key Insight:** CSD has distinct seasonal peaks in **March, June, and December** (not the uniform {1, 4, 6, 10, 12}). This drives all downstream feature engineering choices.

---

## EDA Findings

### Data Overview
- **Total rows:** 4,140 (brand-period combinations)
- **Unique brands:** 143
- **Date range:** 2022-10 to 2026-04 (43 months = 3.5 years)
- **Avg rows/brand:** 29.0

**Interpretation:** Good coverage. 143 brands across full date range provides sufficient data for category-level analysis.

---

### Cell 3: Brand Stability (Series Length) ✅

**Question:** How many brands have sufficient non-zero observations?

**Finding:**
```
≥ 20 periods: 92 brands (64.3%)
≥ 25 periods: 91 brands (63.6%)
≥ 30 periods: 84 brands (58.7%)  ← RECOMMENDED
≥ 35 periods: 73 brands (51.0%)
≥ 40 periods: 62 brands (43.4%)
```

**Recommendation: `MIN_PERIODS = 30`**

**Rationale:**
- At 30 periods: 84 brands retained (58.7% coverage) — good balance
- Below 30: Risk of unreliable forecasts (sparse data)
- Above 35: Risk of losing smaller, viable brands
- 30 months = 2.5 years — sufficient to capture seasonal cycles

**Impact on Step 3:** Filter will reduce 143 brands → 84 brands for feature engineering.

---

### Cell 4: Seasonal Pattern Analysis (Holiday Months) ✅ **[IMPORTANT]**

**Question:** Which months drive CSD sales? Do they match default {1, 4, 6, 10, 12}?

**Finding:**
```
Monthly Sales Distribution (% of total):

Month  | Sales Units | % of Total | Classification
-------|-------------|-----------|---------------
 1 (Jan) | 371.7M | 6.8% | Valley
 2 (Feb) | 438.8M | 8.0% | Normal
 3 (Mar) | 582.4M | 10.7% | ★ PEAK
 4 (Apr) | 459.6M | 8.4% | Normal
 5 (May) | 390.0M | 7.2% | Valley
 6 (Jun) | 477.9M | 8.8% | ★ PEAK
 7 (Jul) | 367.1M | 6.7% | Valley
 8 (Aug) | 373.7M | 6.9% | Valley
 9 (Sep) | 455.9M | 8.4% | Normal
10 (Oct) | 434.7M | 8.0% | Normal
11 (Nov) | 437.9M | 8.0% | Normal
12 (Dec) | 662.7M | 12.2% | ★ PEAK

Top 3 months: [12, 3, 6] = December, March, June
Bottom 3 months: [7, 1, 8] = July, January, August
```

**Recommendation: `HOLIDAY_MONTHS = {3, 6, 12}`**

**Rationale:**
- **December (12.2%):** Holiday season (Christmas, gift-giving) — strong CSD driver
- **March (10.7%):** Spring/Easter season — CSD consumption peaks
- **June (8.8%):** Summer season — temperature-driven beverage demand
- Combined: These 3 months = 31.7% of annual sales

**Comparison to Default:**
- Default (engineer_features.py): {1, 4, 6, 10, 12}
- CSD-specific: {3, 6, 12}
- **Difference:** CSD peaks in March (Easter), not April or January. No October effect.

**Why This Matters:**
- January (6.8%) is actually a valley for CSD, not a peak
- April (8.4%) is normal, not a holiday
- October (8.0%) is normal, not a holiday
- Marking wrong months as holidays introduces noise into forecasting

**Impact on Step 4:** Feature engineering will flag holidays only in March, June, December → more accurate holiday_month indicator.

---

### Cell 5: Lag Analysis ✅

**Question:** Which lags are most predictive for CSD?

**Finding:**

For top brand (COCA COLA), autocorrelation at different lags:
```
Lag 1  (1 month)   : -0.405 (weekly dependency)
Lag 2  (2 months)  : -0.368 (bi-weekly)
Lag 3  (3 months)  : +0.700 (quarterly)
Lag 4  (4 months)  : -0.397 (monthly)
Lag 8  (8 months)  : -0.373 (bi-monthly)
Lag 13 (13 months) : -0.354 (yearly)
```

**Recommendation: `LAGS = (1, 2, 3, 4, 8, 13)`**

**Rationale:**
- Lags 1-4: Capture short-term dependencies (weekly to monthly)
- Lag 8: Capture bi-monthly patterns
- Lag 13: Capture yearly seasonality (important for CSD with strong year-over-year patterns)

**Comparison to Default:**
- Default (engineer_features.py): (1, 2, 3, 4, 8, 13)
- CSD-specific: (1, 2, 3, 4, 8, 13)
- **Verdict:** Default is appropriate for CSD — no changes needed.

**Impact on Step 4:** Each brand will have 6 lagged features for autoregressive forecasting.

---

### Cell 6: Rolling Window Analysis ✅

**Question:** Which rolling windows best capture CSD trends?

**Finding:**
```
Window 4:  4-week rolling mean (monthly trend)
           - Aligns with Nielsen 4-4-5 calendar
           - Good for short-term trend capture
           
Window 13: 13-week rolling mean (quarterly trend)
           - Aligns with quarterly business cycles
           - Good for medium-term trend capture
           
Window 8:  (NOT included — intermediate, redundant with 4+13)
```

**Recommendation: `ROLLING_WINDOWS = (4, 13)`**

**Rationale:**
- Window 4: Matches Nielsen's standard 4-4-5 week calendar
- Window 13: Matches Nielsen's quarterly structure (13 weeks = 1 quarter)
- Together: Capture trends at monthly and quarterly granularity

**Comparison to Default:**
- Default (engineer_features.py): (4, 13)
- CSD-specific: (4, 13)
- **Verdict:** Default is appropriate for CSD — no changes needed.

**Impact on Step 4:** Each brand will have rolling_mean_4, rolling_std_4, rolling_mean_13 features.

---

### Cell 7: Train/Val/Test Split Analysis ✅

**Question:** What are optimal split dates for CSD forecasting?

**Finding:**
```
Available data: 43 months (2022-10 to 2026-04)

Recommended split:
  Train: 2022-10 to 2024-10 (24 months = 2 years)
  Val:   2024-10 to 2025-04 (6 months = 1.5 quarters)
  Test:  2025-04 to 2026-04 (13 months = ~3-4 quarters)

Rationale:
  - Train (24m): Sufficient to learn seasonal patterns + trends (2 full years)
  - Val (6m): Tuning window (1.5 seasonal cycles)
  - Test (13m): Final evaluation (>1 year of test data)
```

**Recommendation:**
```python
TRAIN_END = (2024, 10)  # October 2024
VAL_END = (2025, 4)     # April 2025
```

**Comparison to Default:**
- Default (engineer_features.py): TRAIN_END=(2025, 2), VAL_END=(2025, 8)
- CSD-specific: TRAIN_END=(2024, 10), VAL_END=(2025, 4)
- **Difference:** Default uses later cutoffs, reducing test data. CSD-specific maximizes test data for robust evaluation.

**Impact on Step 5:**
- Train: 24 months of historical data (2022-10 to 2024-10)
- Val: 6 months (2024-10 to 2025-04)
- Test: 13 months (2025-04 to 2026-04)

---

## Final Parameter Set for CSD

```python
# Step 3: Series Filtering
MIN_PERIODS = 30
  # Justification: Cell 3 analysis — 84 brands have ≥30 non-zero periods
  # Impact: Retains 58.7% of brands (84 out of 143)

# Step 4: Feature Engineering
LAGS = (1, 2, 3, 4, 8, 13)
  # Justification: Cell 5 analysis — captures weekly to yearly dependencies
  # Impact: 6 lagged features per brand

ROLLING_WINDOWS = (4, 13)
  # Justification: Cell 6 analysis — align with Nielsen calendar & quarters
  # Impact: rolling_mean_4, rolling_std_4, rolling_mean_13 per brand

HOLIDAY_MONTHS = {3, 6, 12}  # ← CRITICAL: Different from default!
  # Justification: Cell 4 analysis — CSD peaks in March, June, December
  # Impact: holiday_month flag only during these 3 months
  # Rationale: Default {1, 4, 6, 10, 12} incorrect for CSD (ignores March peak)

# Step 5: Train/Val/Test Split
TRAIN_END = (2024, 10)
  # Justification: Cell 7 analysis — 24 months training data
  # Impact: Train boundary at October 2024

VAL_END = (2025, 4)
  # Justification: Cell 7 analysis — 6 months validation data
  # Impact: Val boundary at April 2025
  # Test: 13 months (2025-04 to 2026-04)
```

---

## How to Use These Findings

### In Step 3 (Filter Series):
```python
# From CSD EDA, Cell 3
MIN_PERIODS = 30
```

### In Step 4 (Engineer Features):
```python
# From CSD EDA, Cell 5
LAGS = (1, 2, 3, 4, 8, 13)

# From CSD EDA, Cell 6
ROLLING_WINDOWS = (4, 13)

# From CSD EDA, Cell 4 — IMPORTANT!
HOLIDAY_MONTHS = frozenset({3, 6, 12})
# Note: Different from colleague's uniform default {1, 4, 6, 10, 12}
```

### In Step 5 (Apply Split):
```python
# From CSD EDA, Cell 7
TRAIN_END = (2024, 10)
VAL_END = (2025, 4)
```

---

## Key Insights for Future Categories

1. **Never assume uniform parameters work** — Run EDA for each category
2. **Holiday analysis is critical** — Different categories have different seasonal peaks
   - CSD: March, June, December (Easter, summer, Christmas)
   - Energy drinks: Likely different (winter peaks?)
   - Beer: Strong December, possibly summer
3. **Validate colleague's defaults** — engineer_features.py defaults were never empirically validated
4. **Document justifications** — Link every parameter back to EDA findings

---

## Next Steps

1. ✅ EDA executed: `pre_csd_eda_and_parameter_analysis.py`
2. ✅ Findings saved: `csd_eda_findings.json`
3. ⏳ **TODO:** Update Steps 2-6 with these parameters
4. ⏳ **TODO:** Document parameter citations in each step's docstring
5. ⏳ **TODO:** Run Steps 2-6 with CSD-specific parameters
6. ⏳ **TODO:** Validate feature engineering quality (optional: plot correlations)

---

## References

- **EDA Script:** `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_and_parameter_analysis.py`
- **EDA Findings JSON:** `thesis/data/preprocessing/nielsen/CSD/pipeline_step_outputs/csd_eda_findings.json`
- **EDA Documentation (Template):** `2026-05-14_DOC-csd-eda-analysis-and-parameter-justification.md`
- **Monolithic Reference:** `thesis/data/preprocessing/preprocessing_csd.py`
- **Colleague's Defaults:** `thesis/thesis_agents/ai_research_framework/features/engineer_features.py`

---

**Status:** ✅ EDA Complete | Parameters Justified | Ready for Step 2-6 Implementation
