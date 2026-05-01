# Critical Analysis: Nielsen Data Preprocessing Pipeline

**Date**: 2026-05-01  
**Analyst**: Claude + Brian  
**Context**: Reviewing preprocessing approach before scaling to remaining categories

---

## 1. Current Folder Structure Issue

### What We Have Now
```
thesis/data/preprocessing/parquet_nielsen/
  ├── specialized_CSD_feature_matrix.parquet   (399 KB)
  ├── series_index.csv                         (2.8 KB)
  ├── preprocessing_report.md                  (3.5 KB)
  └── split_dates.json                         (183 B)
```

### The Problem
All 4 outputs from CSD preprocessing are **flat** in one folder. For a multi-category pipeline with 5+ categories, this becomes **unmaintainable**:
- Which category do these files belong to? Must parse filename.
- Cannot easily add per-category metadata or intermediate files
- Harder to track versioning per category
- Mixing outputs from different categories in one folder creates risks of overwrite

### Recommended Structure
```
thesis/data/preprocessing/parquet_nielsen/
  ├── CSD/
  │   ├── specialized_CSD_feature_matrix.parquet
  │   ├── series_index.csv
  │   ├── preprocessing_report.md
  │   └── split_dates.json
  ├── danskvand/
  │   ├── specialized_danskvand_feature_matrix.parquet
  │   ├── series_index.csv
  │   ├── preprocessing_report.md
  │   └── split_dates.json
  ├── energidrikke/
  │   └── ...
  └── ...
```

**Benefit**: Clear ownership, isolated outputs, easy versioning.

---

## 2. Preprocessing Pipeline: What Enrico Did

The pipeline has **6 sequential steps**, all implemented in `engineer_features.py`:

### Step 1: Load Raw Data (CSV → Pandas)
**Source**: `thesis/data/raw_nielsen/data_csv/csd_clean_*.csv` (4 files per category)
- **facts**: 2.5M rows of Nielsen transaction data (product, period, sales_units, promotions, etc.)
- **dim_product**: ~600 rows (product_id → brand mapping)
- **dim_period**: ~300 rows (period_id → year/month mapping)
- **dim_market**: ~50 rows (market_id → market description)

**Operation**: JOIN facts × dims on IDs, filter to one market (e.g., "DVH EXCL. HD"), aggregate by (brand, year, month)

**Output**: ~300–400 rows per category (brand × period) with 5 raw metrics
```
brand | period_year | period_month | sales_units | sales_value | sales_liters | promo_units | weighted_dist
```

**Quality Assessment**:
- ✅ Aggregates across products (good: handles variations in SKU-level data)
- ✅ Filters to target market explicitly (good: avoids mixing channels)
- ✅ Uses `on_bad_lines='skip'` for malformed CSV rows (good: robust)
- ⚠️ **Assumes all categories have the same column names** (may not be true — Enrico's code checks dynamically)

---

### Step 2: Build Calendar (Fill Missing Months)
**Purpose**: Ensure every brand has a complete time series with no gaps

**Operation**:
1. Extract all unique (brand, date) combinations from raw data
2. Create Cartesian product: all_brands × all_dates
3. Left-join raw data into this full calendar
4. Fill **sales metrics** with 0 (brand didn't sell in that month)
5. Fill **distribution** with forward/backward fill (carries last known value)
6. Clip negative sales to 0 (handles returns/corrections)

**Output**: 5,712 rows (77 brands × 74 months, gapless)

**Quality Assessment**:
- ✅ **Leakage-safe**: No look-ahead information
- ✅ **Sensible defaults**: 0 for sales (brand didn't operate), ffill/bfill for distribution (market structure doesn't change month-to-month)
- ⚠️ **Distribution carry-forward assumption**: If a brand's distribution drops to 0, we carry the last known value. This is reasonable BUT assumes distribution is sticky.
- ⚠️ **Negative clipping**: Converting returns/corrections to 0 loses information about returns volume. For forecasting models that don't care about direction, this is fine.

---

### Step 3: Filter Short Series (Drop Sparse Brands)
**Purpose**: Remove brands with insufficient historical data (unreliable for forecasting)

**Operation**: Keep only brands with ≥30 non-zero periods (out of 74)
```python
nonzero_count = (sales_units > 0).sum() per brand
keep if nonzero_count >= 30
```

**Result**: 400 brands → 77 brands (81% drop)

**Quality Assessment**:
- ✅ **Justified**: 30 periods ≈ 2.5 years of sales data. Empirical rule of thumb for time-series models.
- ✅ **Transparent**: Clear why brands are dropped
- ⚠️ **Threshold is fixed** at 30 periods (hardcoded in DEFAULT_MIN_PERIODS). **No per-category tuning** — e.g., danskvand might have different seasonality and need 40 periods, while a fast-moving category like csd might need only 20.

---

### Step 4: Engineer Features (Autoregressive + Temporal + Promotional)
**Purpose**: Transform raw sales into modelling-ready features

**Features created** (17 total):

| Type | Features | Rationale |
|------|----------|-----------|
| **Autoregressive lags** | lag_1, lag_2, lag_3, lag_4, lag_8, lag_13 | Capture recent + seasonal patterns (13 ≈ yearly for monthly data) |
| **Rolling statistics** | rolling_mean_4, rolling_mean_13, rolling_std_4 | Trend + volatility over recent windows |
| **Calendar** | month (1–12), quarter (1–4) | Capture calendar seasonality (e.g., higher sales in Q4) |
| **Holiday indicator** | holiday_month (1/0) | Months with holidays: Jan, Apr, Jun, Oct, Dec (hard-coded set) |
| **Promotion intensity** | promo_units / sales_units (clipped [0,1]) | % of sales under promotion |
| **Log target** | log_sales_units | Reduce skew, stabilize variance (common in forecasting) |

**Leakage Analysis** (critical for valid model evaluation):
```python
# ✅ SAFE: Uses shift(1) — no look-ahead
lag_t = sales_{t-k}                    # Always past data
rolling_mean_t = mean(sales_{t-w} to sales_{t-1})   # Shifted; no t included

# ✅ SAFE: Deterministic, no training-data statistics
calendar = date.month, date.quarter    # Just the calendar
holiday = 1 if month in {1,4,6,10,12} else 0
log = log1p(sales)                     # Monotonic transform
```

**Quality Assessment**:
- ✅ **No data leakage**: All features are either past-looking or deterministic
- ✅ **Well-motivated**: Lags capture autoregression; rolling stats capture trend/volatility; calendar + holiday handle seasonality
- ⚠️ **Lag selection** (1,2,3,4,8,13): Seems reasonable for monthly data (13 = 1 year), but **no category-specific tuning**. Q: Does CSD have the same seasonality pattern as beer? Probably not.
- ⚠️ **Holiday months hard-coded**: {Jan, Apr, Jun, Oct, Dec}. Fine for Denmark, but:
  - Does this apply equally to all beverage categories?
  - What about Easter (moves; not in the set)?
  - What about summer (vacation season, Jun–Aug)?
- ⚠️ **Promo intensity only**:  We have `promo_units / sales_units`, but Enrico doesn't engineer other promotional signals (e.g., promo frequency, promo depth = discount size). These might matter for different categories.

---

### Step 5: Apply Train/Val/Test Split (Temporal Boundaries)
**Purpose**: Lock temporal data split for reproducible cross-validation

**Split boundaries** (hard-coded in DEFAULT_TRAIN_END, DEFAULT_VAL_END):
```
Train: 2019-01 to 2025-02 (2,233 rows = 29 periods/brand avg)
Val:   2025-03 to 2025-08 (546 rows = 6 periods/brand avg)
Test:  2025-09 to 2025-12 (455 rows ≈ 6 periods/brand avg)
```

**Quality Assessment**:
- ✅ **Temporal isolation**: No look-ahead; test is after val, val is after train
- ✅ **Realistic**: Matches time-series eval best practice (train on past, eval on future)
- ⚠️ **Fixed dates for all categories**: CSD split might make sense, but does danskvand have the same data coverage (2019–2025)? If danskvand only has 2020–2025 data, the split is wrong.
- ⚠️ **Recent train cutoff** (Feb 2025): Only 2 months of 2025 in training. If the model trains on 2019–2024 and only 2 months of 2025, it may not learn 2025 patterns. (This depends on the intent: is 2025 seasonality expected to match 2024's?)

---

### Step 6: Save Outputs
**Files generated**:

1. **feature_matrix.parquet** (399 KB for CSD)
   - 3,234 rows (77 brands × 42 months)
   - 25 columns (brand, date, sales metrics, 17 features, split label)
   - Consumed by: specialized_CSD.ipynb, comparison.ipynb

2. **series_index.csv** (2.8 KB)
   - 1 row per brand (77 rows for CSD)
   - Columns: brand, n_periods, n_nonzero, total_units, train_periods, val_periods, test_periods
   - Use: Quick metadata lookup (which brands are in the dataset? which has most sales?)

3. **split_dates.json** (183 B)
   - Date boundaries: train_start, train_end, val_start, val_end, test_start, test_end
   - Use: Notebooks can regenerate the same split without re-running preprocessing

4. **preprocessing_report.md** (3.5 KB)
   - Human-readable summary: timestamp, category, market, feature count, brands, split distribution, elapsed time
   - Use: Manual verification, documentation

---

## 3. Critical Questions for Enrico's Approach

### ❓ **Question 1: Why these specific lags (1,2,3,4,8,13)?**
- Likely motivated by: 1–4 capture short-term autocorrelation, 8 is ~2 months, 13 is ~1 year (seasonality)
- **But**: No justification in code. Is this universal across all 5 beverage categories, or tuned specifically for CSD?
- **Action**: Ask Enrico or check if he did lag selection (e.g., ACF/PACF analysis)

### ❓ **Question 2: Why min_periods=30 (≈2.5 years)?**
- Seems reasonable for a monthly time series, but:
- Some categories might be newer (e.g., energidrikke has different market penetration)
- Dropping 81% of brands might be too aggressive
- **Action**: Consider per-category tuning or a sensitivity analysis (test with 20, 30, 40)

### ❓ **Question 3: Are holiday months {1,4,6,10,12} right?**
- Jan (New Year ✓), Apr (Easter+spring ✓), Jun (summer start ✓), Oct (Halloween/autumn ✓), Dec (Christmas ✓)
- **But**: Missing Jul–Aug (summer vacation), which might boost beer/soft drinks sales
- **Action**: Check sales patterns in specialized_CSD.ipynb — do Jul–Aug show spikes?

### ❓ **Question 4: Distribution imputation (ffill/bfill) — appropriate?**
- Assumes distribution is sticky (once a brand is in a market, it stays roughly at the same level)
- **But**: Distribution can change if a retailer stops stocking a brand
- **Action**: Check if there are sudden drops in distribution in the data; if so, ffill might hide important signals

### ❓ **Question 5: Fixed train/val/test split dates — are they right?**
- Train ends Feb 2025, Val ends Aug 2025, Test is Sep–Dec 2025
- **But**: This assumes all categories have complete data through Dec 2025
- **Action**: Verify data coverage per category before applying the same split

### ❓ **Question 6: Handling of returns/corrections (clipping to 0) — impact?**
- Assumes returns are noise (not signal)
- **But**: High return volume might indicate quality issues or demand shock
- **Action**: Check if any category has significant negative values; if so, model them explicitly

---

## 4. Strengths of Enrico's Approach

✅ **Leakage-safe**: Every feature respects temporal order; no look-ahead.  
✅ **Reproducible**: Hard-coded defaults; can regenerate at will.  
✅ **Automated**: Single script handles all 5+ categories (via imports).  
✅ **Reasonable heuristics**: Lags, rolling stats, calendar features are standard in forecasting.  
✅ **Transparent**: Code is readable; feature engineering is explicit.

---

## 5. Weaknesses & Risks

⚠️ **Fixed hyperparameters** across all categories (lags, min_periods, holiday_months, split dates)  
⚠️ **No category-specific tuning** despite beverages having different seasonality/volatility  
⚠️ **Assumes uniform data coverage** (all categories have same date range 2019–2025)  
⚠️ **Limited feature engineering** (only lags, rolling, calendar; no interaction terms, category-specific metrics)  
⚠️ **No sensitivity analysis** (what if we use 20 periods instead of 30? Different lag selection?)  
⚠️ **Holiday dates hard-coded** without domain validation  

---

## 6. Recommendations Before Scaling

### Phase 1: Validate CSD (Current)
1. ✅ Already done — preprocessing_csd.py works end-to-end
2. Open specialized_CSD.ipynb → inspect lag/rolling/calendar features visually
3. Check: Do holidays (Jan, Apr, Jun, Oct, Dec) actually align with sales spikes?
4. Check: Do Jul–Aug show sales spikes (summer season)?

### Phase 2: Understand Per-Category Differences (Before Duplicating Script)
Before creating preprocessing_danskvand.py, preprocessing_rtd.py, etc., **audit the source data**:
1. Does danskvand have the same date coverage (2019–2025)?
2. Do danskvand brands have similar min_periods distribution, or do they need a different threshold?
3. Does danskvand show different seasonality (e.g., stronger summer peak)?
4. How many brands survive the min_periods=30 filter per category?

**Action**: Add data audit to preprocessing_danskvand.py (before feature engineering).

### Phase 3: Category-Specific Tuning (Optional, but Recommended)
If categories differ significantly:
- Create `preprocessing_csd.py`, `preprocessing_danskvand.py`, etc. with **overridable constants**
- E.g.:
  ```python
  if CATEGORY == "danskvand":
      MIN_PERIODS = 25  # Danskvand has fewer brands, lower threshold
      LAGS = (1, 2, 3, 4, 12)  # No 8, 13 for monthly seasonality
  ```
- Document the rationale in preprocessing_report.md

---

## 7. Folder Restructuring Action Items

### Immediate
- [ ] Create `thesis/data/preprocessing/parquet_nielsen/CSD/` folder
- [ ] Move parquet_nielsen files into CSD/ subfolder
- [ ] Update preprocessing_csd.py to write to `OUT / CATEGORY /`
- [ ] Update paths.py docstrings to reflect new structure

### When Duplicating for Other Categories
- [ ] preprocessing_danskvand.py → outputs to `parquet_nielsen/danskvand/`
- [ ] preprocessing_energidrikke.py → outputs to `parquet_nielsen/energidrikke/`
- [ ] Same for rtd, totalbeer, +1 category

---

## Summary: Is Enrico's Quality Good?

**Grade: B+ (Good foundation, needs category-specific validation)**

- **For CSD**: Likely OK. Default lag selection (1,2,3,4,8,13) is reasonable for monthly data. Holiday months could be validated visually.
- **For other categories**: Unknown. Risk: Fixed parameters might not suit every category's seasonality/volatility.

**Action**: Validate CSD visually first (specialized_CSD.ipynb), then audit source data per category before rolling out scripts.
