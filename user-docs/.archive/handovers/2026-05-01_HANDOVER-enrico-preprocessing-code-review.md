# Handover: Preprocessing Code Review for Enrico

**Date**: 2026-05-01  
**From**: Brian + Claude  
**To**: Enrico  
**Subject**: Questions & Concerns About Feature Engineering Choices in `engineer_features.py`

---

## Executive Summary

We've reviewed the actual Python code in `engineer_features.py` (lines 242–299, `engineer_features()` function). The implementation is **technically sound** (no data leakage, deterministic, reproducible), but **several design choices lack documented justification**. Before scaling to 5+ categories, we need clarity on:

1. **Why these specific lags (1,2,3,4,8,13)?**
2. **Why these specific rolling windows (4, 13)?**
3. **Why min_periods=30?**
4. **Why these holiday months {1,4,6,10,12}?**
5. **Why fixed train/val/test split dates?**
6. **How are category-specific column differences handled?**

This handover documents each concern with **code references** so you can address them directly.

---

## 1. Lag Selection: (1, 2, 3, 4, 8, 13)

### Code Location
`engineer_features.py`, lines 265–267:
```python
# Autoregressive lags
for lag in lags:
    df[f"lag_{lag}"] = g[target_col].shift(lag)
```

Default: `DEFAULT_LAGS = (1, 2, 3, 4, 8, 13)` (line 33)

### Questions
1. **Why these specific values?**
   - 1,2,3,4: Capture recent autocorrelation (2–4 months back)
   - 8: 2 months back? (unclear)
   - 13: 1 year back (for yearly seasonality in monthly data) ✓
   
2. **Is this based on ACF/PACF analysis of Nielsen sales data?**
   - ACF (autocorrelation function) analysis is standard for AR feature selection
   - Did you compute ACF for CSD sales to justify these lags?
   - Or are these empirical defaults from prior experience?

3. **Are these universal across all 5 beverage categories?**
   - CSD seasonality might differ from danskvand (water) or energidrikke (energy drinks)
   - Example: Energidrikke might have quarterly peaks (back-to-school, holidays) rather than monthly
   - Should each category override DEFAULT_LAGS?

### Action Required
**Document**: ACF analysis or justification for lag selection. If category-specific, add override mechanism.

---

## 2. Rolling Windows: (4, 13) + Special Case for rolling_std

### Code Location
`engineer_features.py`, lines 271–282:
```python
for w in rolling_windows:
    df[f"rolling_mean_{w}"] = (
        g[target_col]
        .shift(1)
        .transform(lambda s: s.rolling(w, min_periods=max(2, w // 4)).mean())
    )
    if w == 4:  # match preprocessing.py: only window=4 has std
        df[f"rolling_std_{w}"] = (
            g[target_col]
            .shift(1)
            .transform(lambda s: s.rolling(w, min_periods=2).std().fillna(0))
        )
```

Default: `DEFAULT_ROLLING_WINDOWS = (4, 13)` (line 34)

### Questions
1. **Why windows of 4 and 13 months?**
   - 4 ≈ quarterly (OK for trend detection)
   - 13 ≈ yearly (OK for seasonal trend)
   - But why not 3, 6, 12 (more standard)?

2. **Why only rolling_std for window=4?**
   - Line 277: `if w == 4:` — hardcoded special case
   - Why not rolling_std for w=13 also?
   - Comment says "match preprocessing.py" — did you copy this from original without understanding?

3. **min_periods logic**:
   - Line 275: `min_periods=max(2, w // 4)` — what's the rationale?
   - For w=4: min_periods = max(2, 1) = 2 ✓
   - For w=13: min_periods = max(2, 3) = 3 ✓
   - Why not always min_periods=1? (to capture early observations)

### Action Required
**Document**: Rationale for (4, 13) windows and why rolling_std is only computed for w=4. If unjustified, consider widening to all windows.

---

## 3. Holiday Months: {1, 4, 6, 10, 12}

### Code Location
`engineer_features.py`, lines 284–287:
```python
# Calendar features
df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter
df["holiday_month"] = df["month"].isin(holiday_set).astype(int)
```

Default: `DEFAULT_HOLIDAY_MONTHS = frozenset({1, 4, 6, 10, 12})` (line 35)

### What This Does
Creates a binary indicator: 1 if the month is {Jan, Apr, Jun, Oct, Dec}, else 0.

### Questions
1. **Why these months?**
   - Jan: New Year ✓
   - Apr: Easter (but Easter moves; not fixed to April) ⚠️
   - Jun: Summer start (some countries; vacations begin)
   - Oct: Halloween + autumn
   - Dec: Christmas ✓

2. **What's missing?**
   - Jul–Aug: Peak vacation/summer season (often highest sales for beverages)
   - Why excluded?
   - This seems like a **major gap** for a beverage dataset

3. **Domain-specific?**
   - Does this set apply equally to all 5 categories?
   - Danskvand (water): Different drinking patterns than CSD (soft drinks)?
   - Energidrikke: Linked to school calendar more than holidays?

4. **Fixed dates for moving holidays?**
   - Easter (Apr 9 in 2026) is not the same day every year
   - Your binary {1,4,6,10,12} approach won't capture Easter variance

### Action Required
**Verify**: Inspect specialized_CSD.ipynb for Jul–Aug sales patterns. If they show strong peaks, the holiday_months set is incomplete. Also document whether this is:
- A data-driven choice (analyzed sales patterns)
- A domain assumption (from beverage industry knowledge)
- Or arbitrary

---

## 4. Minimum Periods Filter: min_periods=30

### Code Location
`engineer_features.py`, lines 231–239:
```python
def filter_series(
    df: pd.DataFrame,
    min_periods: int = DEFAULT_MIN_PERIODS,
    target_col: str = DEFAULT_TARGET_COL,
) -> pd.DataFrame:
    """Keep only brands with >= min_periods of non-zero target observations."""
    nonzero = df.groupby("brand")[target_col].apply(lambda s: (s > 0).sum())
    keep = nonzero[nonzero >= min_periods].index
    return df[df["brand"].isin(keep)].copy()
```

Default: `DEFAULT_MIN_PERIODS = 30` (line 37)

### What This Does
Drops all brands with fewer than 30 non-zero sales periods (months). For CSD, this drops ~81% of brands (400 → 77).

### Questions
1. **Why 30 periods?**
   - 30 months ≈ 2.5 years (reasonable for time-series forecasting)
   - But is this based on:
     - Empirical analysis (signal-to-noise ratio)?
     - Rule of thumb (minimum periods for lag-13)?
     - Or arbitrary?

2. **Is this universal?**
   - CSD: Well-established category, brands likely have 30+ periods
   - Danskvand (water): Might be newer, fewer periods?
   - Energidrikke: Highly volatile; some brands might exit/enter frequently
   - Should different categories have different thresholds?

3. **Sensitivity**:
   - What if we used 20 instead of 30? → ~90 brands?
   - What if we used 40? → ~60 brands?
   - Did you test this sensitivity?

### Action Required
**Justify**: Why 30? Is this:
- Data-driven (you tested other thresholds)?
- Or a heuristic rule?
If per-category thresholds needed, create override mechanism.

---

## 5. Train/Val/Test Split Dates

### Code Location
`engineer_features.py`, lines 302–316:
```python
def apply_split(
    df: pd.DataFrame,
    train_end: tuple[int, int] = DEFAULT_TRAIN_END,
    val_end: tuple[int, int] = DEFAULT_VAL_END,
) -> pd.DataFrame:
    """Label rows with split = 'train' | 'val' | 'test' based on date cutoffs."""
    df = df.copy()
    train_cutoff = pd.Timestamp(f"{train_end[0]}-{train_end[1]:02d}-01")
    val_cutoff = pd.Timestamp(f"{val_end[0]}-{val_end[1]:02d}-01")
    conditions = [
        df["date"] <= train_cutoff,
        (df["date"] > train_cutoff) & (df["date"] <= val_cutoff),
    ]
    df["split"] = np.select(conditions, ["train", "val"], default="test")
    return df
```

Defaults:
- `DEFAULT_TRAIN_END = (2025, 2)` — inclusive (line 38)
- `DEFAULT_VAL_END = (2025, 8)` — inclusive (line 39)

### What This Does
```
Train: date <= 2025-02-01   (2019-01 to 2025-02 ≈ 75 months, ~29 per brand)
Val:   2025-02-01 < date <= 2025-08-01  (6 months)
Test:  date > 2025-08-01   (Sep–Dec 2025 ≈ 4 months)
```

### Questions
1. **Why Feb 2025 as train cutoff?**
   - Why not Dec 2024 (natural year boundary)?
   - Why not Jan 2025?
   - Only 2 months of 2025 in training — does the model learn 2025 patterns?

2. **Why Aug 2025 as val cutoff?**
   - Only 4 months in test (Sep–Dec 2025)
   - Is this enough for robust evaluation?
   - Summer (Jun–Aug) is in val; winter (Dec) is in test — seasonality mismatch?

3. **Are these dates correct for all categories?**
   - Assumption: All categories have data through Dec 2025
   - True for CSD? What about newer categories (energidrikke)?
   - If danskvand only has data through Jun 2025, split is broken

4. **No overlap check**:
   - Code doesn't verify all dates are within [2019-01, 2025-12]
   - What if a category's data is [2020-06, 2025-10]?
   - The split would put most data in test (wrong!)

### Action Required
**Verify before scaling**:
1. Check data coverage per category (min/max dates)
2. Confirm all categories have 2019-01 start and 2025-12 end
3. If not, allow per-category split overrides
4. Add validation to ensure split boundaries are within data range

---

## 6. Promo Intensity Calculation

### Code Location
`engineer_features.py`, lines 289–294:
```python
# Promo intensity (clip to [0, 1])
df["promo_intensity"] = np.where(
    df["sales_units"] > 0,
    df["promo_units"] / df["sales_units"].clip(lower=1),
    0,
).clip(0, 1)
```

### Questions
1. **Denominator is clipped to 1, not 0**:
   - Line 292: `.clip(lower=1)` — why?
   - Effect: If sales_units is 0.5, denominator becomes 1, so promo_intensity = promo_units / 1 = promo_units
   - This inflates promo_intensity for low-sales months
   - Was this intentional?

2. **Clip to [0, 1] at the end**:
   - Line 294: `.clip(0, 1)` — prevents values > 1
   - Why can promo_units exceed sales_units?
   - Shouldn't they be mutually exclusive (units with promo ≤ total units)?

3. **What does "units with promo" mean?**
   - Is promo_units a count of units sold under promotion?
   - Or a binary flag for "any promo happened"?
   - The CSV column name is `sales_units_any_promo`, which suggests binary
   - But the aggregation uses `.sum()`, which suggests counts

### Action Required
**Clarify**: 
- What does promo_units represent in the Nielsen data?
- Why is the denominator clipped to lower=1?
- Should this calculation differ per category?

---

## 8. Log Transformation

### Code Location
`engineer_features.py`, lines 296–297:
```python
# Log-transformed target
df["log_sales_units"] = np.log1p(df["sales_units"])
```

### Questions
1. **Why log?**
   - Standard practice for skewed data (sales often follow power-law distributions)
   - Makes the feature more normal; helps some models (linear regression, Gaussian processes)
   - But LightGBM (tree-based) doesn't need log; it handles skew natively

2. **np.log1p vs np.log?**
   - np.log1p(x) = log(1+x), handles zeros gracefully (log(0+1) = 0)
   - np.log(0) = -inf, causes issues
   - Your choice is sensible ✓

3. **Do you also include the original sales_units as a feature?**
   - Yes: Both `sales_units` and `log_sales_units` are in the final matrix
   - If your model is tree-based (LightGBM), log is redundant
   - If your model is linear/ridge/lasso, log is useful

### Action Required
**Document**: Is the original `sales_units` included in the feature matrix? If so, is `log_sales_units` necessary, or redundant?

---

## 9. Data Leakage: Verified ✅

### Analysis
I reviewed lines 262–299 line-by-line. **Conclusion: No data leakage.**

#### Lags (lines 266–267)
```python
df[f"lag_{lag}"] = g[target_col].shift(lag)
```
✅ `shift(lag)` always looks backward; no future information.

#### Rolling Stats (lines 272–275)
```python
.shift(1)  # Shift by 1 BEFORE rolling
.transform(lambda s: s.rolling(w, ...).mean())
```
✅ `.shift(1)` first, then rolling window. Example for w=4:
- At time t: rolling window uses [t-4, t-3, t-2, t-1] (only past)
- At time t: includes t-1, not t (no look-ahead)

#### Calendar/Promo/Log (lines 284–297)
✅ All deterministic; no information leakage from training set.

#### Split Application (lines 302–316)
✅ Split applied AFTER all features are created (on full data). This is correct because:
- Features are leakage-safe by construction
- Splitting before feature engineering would limit data availability
- Standard practice: engineer features on full data, then split for model training

---

## 10. Code Quality: Verified ✅

### Strengths
- ✅ Pure functions (no global state, deterministic)
- ✅ Well-commented (especially leakage analysis)
- ✅ Type hints (except a few missing specs)
- ✅ Robust error handling (e.g., aggregate_brand_month_from_csvs checks market existence)

### Weaknesses
- ⚠️ Several "magic numbers" without justification (lags, windows, holidays, min_periods)
- ⚠️ Comment "match preprocessing.py" (line 277) suggests copy-paste without understanding
- ⚠️ No validation of split date boundaries

---

## Summary: Action Items for Enrico

### Before Scaling (Priority 1)
- [ ] **Justify lag selection (1,2,3,4,8,13)**
  - ACF analysis? Domain knowledge? Arbitrary?
  - Per-category override needed?

- [ ] **Justify rolling windows (4,13)**
  - Why not 3,6,12?
  - Why rolling_std only for w=4?

- [ ] **Revisit holiday months {1,4,6,10,12}**
  - Why exclude Jul–Aug (peak summer)?
  - Per-category override needed?

- [ ] **Justify min_periods=30**
  - Data-driven? Rule of thumb?
  - Sensitivity analysis (20, 30, 40)?

- [ ] **Verify train/val/test split dates**
  - Do all categories have 2019-01 to 2025-12 data?
  - If not, allow per-category splits

### Before Duplicating Scripts (Priority 2)
- [ ] **Clarify promo_units definition**
  - Count of units? Binary flag? Impact on promo_intensity calculation?

- [ ] **Document feature schema per category**
  - Do all 5 categories have sales_units_any_promo?
  - Or only CSD, danskvand? (SQL path already handles this)

---

## Questions for You

1. **Are lags/windows/holidays based on ACF analysis or empirical tuning?**
2. **Are these universal across all 5 categories, or should we tune per-category?**
3. **What's the data coverage per category? (Do they all start 2019-01 and end 2025-12?)**
4. **Is the original `sales_units` column included in the final feature matrix, or only `log_sales_units`?**

---

## Next Steps (Brian)

Once you've answered these questions:
1. Update P0017 plan with findings
2. Restructure parquet_nielsen/ to per-category subfolders (CSD/, danskvand/, etc.)
3. Duplicate preprocessing_csd.py for other categories (with documented overrides where needed)
4. Test all 5 scripts end-to-end
