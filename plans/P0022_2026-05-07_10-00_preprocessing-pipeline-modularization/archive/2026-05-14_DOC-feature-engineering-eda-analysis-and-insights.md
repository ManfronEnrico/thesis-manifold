# Feature Engineering & EDA Analysis: Time Series Best Practices vs. Current Implementation

**Date:** 2026-05-14  
**Context:** Evaluation of Nielsen beverage preprocessing feature engineering against time series EDA best practices  
**Purpose:** Document suspect patterns in current implementation and recommend improvements for P0022 feature engineering pipeline refinement  

---

## Executive Summary

**Key Finding:** Current feature engineering approach is **missing critical EDA validation steps** before feature creation. The implementation creates features without verifying:
- Autocorrelation structure (ACF/PACF)
- Stationarity properties
- Seasonality detection and confirmation
- Feature leakage risks from shifted lags

**High-Risk Issues:**
1. **Rolling window min_periods logic** — currently allows too-small windows (risk of unstable statistics)
2. **Hard-coded lag windows** — not validated against actual autocorrelation in CSD data
3. **No stationarity assessment** — log transformation applied without checking if needed
4. **Missing seasonality decomposition** — holiday_months guessed vs. empirically validated
5. **Promo intensity calculation** — division by clipped sales_units could amplify noise

---

## Part 1: EDA Best Practices from Literature

### IMPORTANT CLARIFICATION ✅

**Your CSD EDA script (`pre_csd_eda_and_parameter_analysis.py`) already validates most parameter choices empirically:**

| Parameter | Your Validation | Status |
|---|---|---|
| `LAG_WINDOWS = {1,2,3,4,8,13}` | Cell 5: Lag correlation on top brands | ✅ VALIDATED |
| `HOLIDAY_MONTHS = {3,6,12}` | Cell 4: Top 25% sales months (≥75th percentile) | ✅ VALIDATED |
| `ROLLING_WINDOWS = {4,13}` | Cell 6: Nielsen calendar alignment | ✅ JUSTIFIED |
| `MIN_PERIODS = 40` | Cell 3: 62 brands with ≥40 periods (high quality) | ✅ JUSTIFIED |
| `TRAIN_END, VAL_END` | Cell 7: 24m train + 6m val + rest test | ✅ CALCULATED |

**What's STILL MISSING (from Rossmann best practices):**
- ACF/PACF plots (validate lags are statistically significant)
- Seasonal decomposition (visually confirm peaks)
- Stationarity testing (justify log transform)
- ECDF distribution analysis (understand sales shape)

See `2026-05-14_DOC-rossmann-vs-csd-eda-comparison.md` for detailed component-by-component comparison.

---

### 1.1 Rossmann Time Series Notebook Key Insights

**ACF/PACF Analysis (Critical First Step):**
```
The Rossmann notebook demonstrates that BEFORE feature engineering:
1. Plot ACF/PACF to identify lag structure
   - Lag-1 correlation reveals need for differencing (d/D)
   - Seasonal spikes (lag-12, lag-4, lag-7) reveal natural windows
   - PACF helps distinguish AR order (true dependencies vs. correlation decay)
2. Use seasonal_decompose() to separate trend, seasonal, residual
3. Test for stationarity (ADF test) before modeling
```

**For Rossmann (retail sales):**
- Store types A & B showed **12-lag seasonality** (monthly calendar)
- Store types C & D showed **complex autocorrelation** (adjacency effects)
- **Conclusion:** Different store types needed different lag structures

**For Nielsen beverages (CSD, RTD, etc.):**
- Your current code assumes same lag windows (1,2,3,4,8,13) for all brands
- **Question:** Has CSD autocorrelation been validated? Different categories may have different seasonal patterns

---

### 1.2 Time Series Preprocessing Best Practices

#### Data Quality Gates (from Rossmann & EDA PDFs)

| Step | Check | Current Implementation | Risk |
|------|-------|------------------------|------|
| **Pre-EDA** | Remove closed stores / zero sales | ✓ In step 3 filter_series | OK |
| **EDA Phase** | ECDF distribution analysis | ✗ Missing | Can't detect bimodal/skew patterns |
| **EDA Phase** | ACF/PACF plots | ✗ Missing | Lag selection is guesswork |
| **EDA Phase** | seasonal_decompose() | ✗ Missing | Holiday months unvalidated |
| **EDA Phase** | Stationarity test (ADF) | ✗ Missing | Log transform applied blindly |
| **Feature Eng** | Lag selection | Hardcoded {1,2,3,4,8,13} | Not data-driven |
| **Feature Eng** | Rolling window validation | min_periods=max(2, w//4) | Too permissive |
| **Feature Eng** | Leakage check | Comments reference shift(1) | Needs explicit validation |

**Suspect Pattern:** Steps marked ✗ are the gaps between current implementation and best-practice EDA workflows.

---

### 1.3 Feature Engineering Leakage in Time Series

**From Rossmann notebook:**
```python
# CORRECT approach (from engineer_features.py lines 269-276):
df[f'rolling_mean_{w}'] = (
    g[target_col]
    .shift(1)  # ← Ensures no look-ahead
    .transform(lambda s: s.rolling(w, min_periods=...).mean())
)
```

**Current code does this correctly BUT:**
1. `min_periods=max(2, w//4)` is **too loose**
   - For w=4: min_periods=2 means 2-point rolling avg (high noise)
   - For w=13: min_periods=3 means 3-point avg (insufficient seasonality signal)
   
2. **Better approach:** Require at least 50% of window
   ```python
   min_periods = max(1, w // 2)  # At least half the window
   ```

---

## Part 2: Suspect Patterns in Current Implementation

### Issue 1: Hard-Coded Lag Windows Without Validation

**Current (pre_csd_4_engineer_features.py, line 86):**
```python
CSD_LAG_WINDOWS = [1, 2, 3, 4, 8, 13]  # Weekly to yearly dependencies
```

**Suspected Problem:**
- Lags are **assumed** but not verified against CSD autocorrelation
- `lag_8` = 8 months is unusual (not aligned to quarterly/annual cycles)
- `lag_13` = 13 months (annual+1) makes sense but needs validation

**What the Rossmann notebook shows:**
- Store type A had clear 12-lag seasonality (monthly calendar)
- Store type B had 7-lag seasonality (weekly promo cycle)
- **Conclusion:** Lag structure is **data-specific**, not universal

**Validation needed:**
```
Q: For CSD data, what does ACF reveal?
   - Is lag-12 (annual) the strongest?
   - Is lag-4 (quarterly) significant?
   - Are there weekly patterns (lags 1-4)?
```

---

### Issue 2: Holiday Months Are Guessed, Not Empirically Justified

**Current (pre_csd_4_engineer_features.py, lines 88-89):**
```python
CSD_HOLIDAY_MONTHS = {3, 6, 12}  # March (Easter), June (Summer), Dec (Holidays)
# ⚠️ Different from default {1, 4, 6, 10, 12}
```

**Code comment claims:**
- March peak: 10.7% (Easter)
- June peak: 8.8% (Summer)  
- December peak: 12.2% (Holidays)

**Suspected Problem:**
1. **Where did these percentages come from?** Not visible in step 0-3 outputs
2. **Are they statistically significant?** No confidence intervals shown
3. **Different from default {1,4,6,10,12}** — why April and October excluded?

**What Rossmann notebook demonstrates:**
```python
# First: visualize monthly sales patterns by store type
sns.factorplot(data=train_store, x='Month', y='Sales', 
               col='StoreType', palette='plasma')
# THEN: seasonal_decompose() confirms visually observed peaks
decomposition = seasonal_decompose(sales, model='additive', freq=365)
decomposition.seasonal.plot()
```

**Better approach:**
1. Plot CSD sales by month across all brands
2. Run seasonal_decompose() for CSD aggregated series
3. Identify peaks statistically (e.g., top 3 months)
4. Confirm with PACF seasonal spikes

---

### Issue 3: Rolling Window min_periods Is Too Permissive

**Current (engineer_features.py, lines 271-276):**
```python
df[f'rolling_mean_{w}'] = (
    g[target_col]
    .shift(1)
    .transform(lambda s: s.rolling(w, min_periods=max(2, w // 4)).mean())
)
```

**Analysis:**
- `w=4` (quarterly): `min_periods=2` (50% of window)
- `w=13` (annual): `min_periods=3` (23% of window!)

**Problem:**
- 23% fill is unreliable for 13-month window
- Rolling std (line 281): `min_periods=2` for ANY window is too loose
- Creates noisy features early in time series

**From Rossmann:**
- Notebook doesn't explicitly show min_periods choice
- But feature importance plot (cell 138) shows `rolling_mean_4` is important
- Suggests stable, reliable rolling stats are needed

**Better approach:**
```python
# Require at least half the window
df[f'rolling_mean_{w}'] = (
    g[target_col]
    .shift(1)
    .transform(lambda s: s.rolling(w, min_periods=w//2).mean())
)
df[f'rolling_std_{w}'] = (
    g[target_col]
    .shift(1)
    .transform(lambda s: s.rolling(w, min_periods=w//2).std())
)
```

---

### Issue 4: Log Transform Applied Without Stationarity Check

**Current (pre_csd_4_engineer_features.py, lines 137-139):**
```python
df["log_sales_units"] = df["sales_units"].apply(lambda x: float('nan') if pd.isna(x) else float(x)).apply(
    lambda x: float('nan') if x <= 0 else np.log(x)
)
```

**Suspected Problem:**
1. **No ADF test** to check if log transform is actually needed
2. **Unnecessary lambda chaining** (should be np.log1p for robustness)
3. **No validation** that log-transformed series is stationary

**From EDA literature:**
```python
# Correct approach:
from statsmodels.tsa.stattools import adfuller

# Test original series
adf_orig = adfuller(df['sales_units'].dropna())
print(f"Original p-value: {adf_orig[1]:.4f}")  # p < 0.05 = stationary

# If p > 0.05 (non-stationary), then apply log transform
if adf_orig[1] > 0.05:
    df['log_sales_units'] = np.log1p(df['sales_units'])
    adf_log = adfuller(df['log_sales_units'].dropna())
    print(f"Log-transformed p-value: {adf_log[1]:.4f}")
```

**From Rossmann notebook (cell 99):**
> "Our data is highly seasonal and not random (dependent). Therefore, before fitting any models we need to "smooth" target variable Sales. The typical preprocessing step is to log transform the data in question."

**BUT:** Seasonality ≠ non-stationarity. Log transform stabilizes *variance*, not *mean*. Differencing (d=1) stabilizes mean.

---

### Issue 5: Promo Intensity Calculation May Amplify Noise

**Current (engineer_features.py, lines 289-294):**
```python
df["promo_intensity"] = np.where(
    df["sales_units"] > 0,
    df["promo_units"] / df["sales_units"].clip(lower=1),
    0,
).clip(0, 1)
```

**Suspected Problem:**
1. **Dividing by clipped sales_units** — `clip(lower=1)` masks true division behavior
2. **No handling of promo_units > sales_units** — both should be valid, but ratio > 1 is clipped away
3. **Zero promo_units becomes 0** — indistinguishable from "no promo running" (both → promo_intensity=0)

**Better approach:**
```python
# Only calculate when both values are positive and non-NaN
df["promo_intensity"] = 0.0
valid = (df["sales_units"] > 0) & (df["promo_units"] > 0)
df.loc[valid, "promo_intensity"] = (
    df.loc[valid, "promo_units"] / df.loc[valid, "sales_units"]
).clip(0, 1)
# This preserves: no sales → NaN, no promo → 0, low promo → 0-0.5, high → 0.5-1
```

---

## Part 3: Current State vs. Best Practices

### What Your CSD EDA Already Does Well ✅

Your `pre_csd_eda_and_parameter_analysis.py` is **data-driven** and **empirically justified**:

- ✅ **Lag windows validated:** Cell 5 checks lag correlation on top brands
- ✅ **Holiday months validated:** Cell 4 identifies top 25% sales months via aggregation
- ✅ **Rolling windows justified:** Cell 6 aligns to Nielsen calendar cycles
- ✅ **Min_periods rationalized:** Cell 3 selects 40 for "thesis quality focus"
- ✅ **Split dates calculated:** Cell 7 derives train/val/test from actual data range
- ✅ **JSON output:** Reproducible findings for downstream scripts
- ✅ **Python cells format:** Git-friendly, automation-ready

### What's Missing (Visualization & Statistical Validation)

Your current approach is **parameter-focused** but lacks **visual confirmation** and **statistical rigor**:

- ✗ **ACF/PACF plots:** Lags not validated as statistically significant
- ✗ **Seasonal decompose:** Peaks {3,6,12} not visually confirmed
- ✗ **ADF stationarity test:** Log transform applied without justification
- ✗ **ECDF distribution:** Sales shape not analyzed
- ✗ **Correlation heatmap:** Metric relationships not checked

These missing components are **not critical for parameter selection** but **are critical for understanding why features work**.

---

## Part 3: Recommended Next Steps for P0022

### Phase 2.5: EDA Enhancement (ADD MISSING VISUALIZATIONS)

**Add visualization & statistical validation to your existing EDA:**

1. **ACF/PACF Plots (NEW Cell 5.5)**
   ```
   Goal: Confirm lags are statistically significant
   - Plot ACF/PACF for top 5 brands
   - Check if lags 1,2,3,4,8,13 exceed confidence bands
   - Verify against your cell 5 correlation analysis
   Expected: Should confirm {1,2,3,4,8,13} lags are meaningful
   ```

2. **Seasonal Decomposition (NEW Cell 4.5)**
   ```
   Goal: Visually confirm {3,6,12} are actual seasonal peaks
   - Run seasonal_decompose() on CSD aggregate
   - Plot trend, seasonal, residual components
   - Verify seasonal peaks match {3,6,12}
   Expected: Monthly seasonal component should peak in March, June, December
   ```

3. **ADF Stationarity Test (NEW Cell 2.5)**
   ```
   Goal: Justify log transform decision
   - Test original sales_units for stationarity (ADF test)
   - Test if log-transformed series is stationary
   - Document: "Log necessary due to non-stationarity" or "Sales already stationary"
   Expected: CSD likely non-stationary → log+diff recommended
   ```

4. **ECDF Distribution (NEW Cell 1.5)**
   ```
   Goal: Understand sales distribution shape
   - Plot ECDF of sales_units (with >0 sales)
   - Check if skewed, bimodal, or normal
   Expected: Likely right-skewed → justifies log transform
   ```

### Phase 3 (Revised): Feature Engineering with Validated Parameters

Replace hardcoded values with data-driven selections:

**Current → Revised:**
```python
# CURRENT: Hardcoded
CSD_LAG_WINDOWS = [1, 2, 3, 4, 8, 13]
CSD_HOLIDAY_MONTHS = {3, 6, 12}

# REVISED: Data-driven (from Phase 2.5 EDA)
CSD_LAG_WINDOWS = [...]  # From ACF analysis
CSD_HOLIDAY_MONTHS = {...}  # From seasonal_decompose + visual inspection
CSD_APPLY_LOG_TRANSFORM = True/False  # From ADF test results
CSD_ROLLING_MIN_PERIODS = ...  # From data coverage analysis
```

---

## Part 4: Summary of Suspect Patterns

| # | Issue | Severity | Current | Recommended | Validation |
|---|-------|----------|---------|-------------|-----------|
| 1 | Lag windows hardcoded | 🔴 HIGH | {1,2,3,4,8,13} | ACF/PACF per brand | Plot ACF, check statistical significance |
| 2 | Holiday months guessed | 🔴 HIGH | {3,6,12} | seasonal_decompose() | Visual + peak detection |
| 3 | Rolling min_periods loose | 🟡 MED | max(2, w//4) | w//2 | Check % non-NaN coverage |
| 4 | Log transform unchecked | 🟡 MED | Automatic | ADF test first | Stationarity test |
| 5 | Promo intensity noisy | 🟡 MED | Divide + clip | Preserve nullability | Separate 0-division from 0-promo cases |
| 6 | No EDA phase before FE | 🔴 HIGH | Skip to features | Add Phase 2.5 EDA | ACF, decompose, stationarity, visualization |

---

## References & Resources

**Analysed:**
- `Example_Notebook-Source_time_series_prophet-Rossmann_Sales.ipynb` — Retail time series EDA template
- `Mastering EDA (Medium, Nayeem Islam)` — General EDA methodology
- `EDA (GeeksforGeeks)` — Python EDA tools and patterns

**Current Implementation:**
- `thesis/thesis_agents/ai_research_framework/features/engineer_features.py` — Shared feature engineering (lines 242-299)
- `thesis/data/preprocessing/nielsen/CSD/pre_csd_4_engineer_features.py` — CSD-specific orchestrator

**Key Insight from Rossmann:**
> Time series are fundamentally different from independent data. ACF/PACF, seasonality, and stationarity must be understood BEFORE any feature engineering. Using data-agnostic templates (like {1,4,6,10,12} holiday defaults) without validation leads to suboptimal or misleading features.

---

## Next Session Action Items

1. ✅ Read this doc before VPS session (context)
2. ⚙️ Run EDA phase on Nielsen CSD data
   - ACF/PACF for top 10 brands
   - Seasonal decomposition
   - ADF stationarity test
   - Rolling window coverage analysis
3. 🔧 Update `CSD_LAG_WINDOWS`, `CSD_HOLIDAY_MONTHS`, `CSD_APPLY_LOG_TRANSFORM` with validated values
4. 🧪 Re-run steps 4-6 with new parameters
5. 📊 Compare feature distributions before/after (should be cleaner, less noisy)

---

**Document Status:** Ready for VPS session reference  
**Last Updated:** 2026-05-14 14:32  
