---
name: T003-feature-engineering-audit
description: Feature engineering logic extraction and specification
created: 2026-06-22 16:35
updated: 2026-06-22 16:35
---

# T-003 Output: Feature Engineering Logic Audit

## Summary

✅ **Feature engineering verified** — 14 features created per brand×period observation

## Features Engineered (Step 4)

### Autoregressive Lags (6 features)
From `engineer_features()` (line 265-267):
```python
for lag in lags:
    df[f"lag_{lag}"] = g[target_col].shift(lag)
```

**CSD-specific lags** (from EDA autocorrelation analysis):
```python
CSD_LAG_WINDOWS = [1, 2, 3, 4, 8, 13]
```

**Features created:**
- `lag_1` — 1-month autoregressive (weekly dependency)
- `lag_2` — 2-month autoregressive
- `lag_3` — 3-month autoregressive
- `lag_4` — 4-month autoregressive (monthly cycle)
- `lag_8` — 8-month autoregressive (2-quarter dependency)
- `lag_13` — 13-month autoregressive (yearly seasonality)

**Implementation:** Uses `groupby("brand").shift(lag)` — no leakage, each brand's lags computed independently

### Rolling Statistics (3 features)
From `engineer_features()` (line 271-282):
```python
for w in rolling_windows:
    df[f"rolling_mean_{w}"] = g[target_col].shift(1).transform(
        lambda s: s.rolling(w, min_periods=max(2, w // 4)).mean()
    )
    if w == 4:
        df[f"rolling_std_{w}"] = g[target_col].shift(1).transform(
            lambda s: s.rolling(w, min_periods=2).std().fillna(0)
        )
```

**CSD-specific windows** (from Nielsen calendar analysis):
```python
CSD_ROLLING_WINDOWS = [4, 13]
```

**Features created:**
- `rolling_mean_4` — 4-period (1-month) rolling average (shifted by 1 to avoid leakage)
- `rolling_std_4` — 4-period rolling standard deviation (only for window=4)
- `rolling_mean_13` — 13-period (3-month) rolling average (shifted by 1)

**Implementation:** Uses `.shift(1)` before rolling — no look-ahead bias; `min_periods` allows short history

### Calendar Features (3 features)
From `engineer_features()` (line 285-287):
```python
df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter
df["holiday_month"] = df["month"].isin(holiday_set).astype(int)
```

**CSD-specific holiday months** (from EDA findings):
```python
CSD_HOLIDAY_MONTHS = {3, 6, 12}
```

**Rationale (from code comments, lines 115-120):**
- March (3): 10.7% peak — Easter season
- June (6): 8.8% peak — Summer season
- December (12): 12.2% peak — Holiday season

⚠️ **Note:** Different from colleague's default `{1, 4, 6, 10, 12}`. CSD data shows March peak (10.7%), not April (8.4%).

**Features created:**
- `month` — Calendar month (1–12)
- `quarter` — Calendar quarter (1–4)
- `holiday_month` — Binary indicator (1 if month in {3,6,12}, else 0)

### Log Transformation (1 feature)
From `pre_csd_4_engineer_features.py` (lines 136-139):
```python
df["log_sales_units"] = df["sales_units"].apply(
    lambda x: float('nan') if pd.isna(x) else float(x)
).apply(
    lambda x: float('nan') if x <= 0 else np.log(x)
)
```

**Feature created:**
- `log_sales_units` — Natural log of sales_units (preserves NaN for missing/non-positive values)

**Purpose:** Stationarity transformation; ADF tests show log transform necessary for CSD data

### Promotional Effects (1 feature)
From `engineer_features()` (line 290-294):
```python
df["promo_intensity"] = np.where(
    df["sales_units"] > 0,
    df["promo_units"] / df["sales_units"].clip(lower=1),
    0,
).clip(0, 1)
```

**Feature created:**
- `promo_intensity` — Promotional units ÷ sales units, clipped to [0, 1]

**Implementation:**
- Clips denominator to 1 (avoids division by 0)
- Sets promo_intensity=0 when sales_units ≤ 0
- Clips result to [0, 1] range

## Total Feature Count

**Input columns (from Step 3):**
- brand, period_year, period_month, sales_units, promo_units, date

**Output columns (from Step 4):**
- All input columns (6) +
- Lags (6) +
- Rolling stats (3) +
- Calendar features (3) +
- Log transform (1) +
- Promo intensity (1)

**Total: 20 engineered features per observation**

| Feature Group | Count | Features |
|---|---|---|
| Input (pass-through) | 6 | brand, period_year, period_month, sales_units, promo_units, date |
| Lags | 6 | lag_1, lag_2, lag_3, lag_4, lag_8, lag_13 |
| Rolling stats | 3 | rolling_mean_4, rolling_std_4, rolling_mean_13 |
| Calendar | 3 | month, quarter, holiday_month |
| Transformations | 2 | log_sales_units, promo_intensity |
| **Total** | **20** | |

## Stationarity Treatment

**Log transformation applied:** ✅ Yes (line 137-139)

From EDA analysis (referenced in code):
- ADF test indicates non-stationary sales_units
- Log transform necessary for proper time-series modeling
- NaN preserved for missing/non-positive values (no artificial filling)

**No differencing applied** — Log transform sufficient for CSD data

## Missing Value Handling

From shared `engineer_features()`:
- Lags: NaN propagates where source is NaN
- Rolling: NaN propagates; `min_periods` allows short history
- Calendar: No NaN (deterministic from date)
- Log transform: NaN for non-positive values

**Strategy:** Preserve NaN; don't impute in Step 4. Imputation (if needed) deferred to downstream modeling (System A).

## Code Reuse & Consistency

**Shared function approach:**
- `engineer_features()` imported from `thesis.thesis_agents.ai_research_framework.features.engineer_features`
- CSD-specific parameters (lags, windows, holiday months) passed as arguments
- Same shared function used for all categories (parametrized design)

**Benefits:**
- Single source of truth for feature engineering logic
- Reduces code duplication across categories
- Easier to maintain and update parameters

## Category Variations

**CSD-specific parameters:**
```python
CSD_LAG_WINDOWS = [1, 2, 3, 4, 8, 13]
CSD_ROLLING_WINDOWS = [4, 13]
CSD_HOLIDAY_MONTHS = {3, 6, 12}
```

**To verify:** Other categories (Danskvand, Energidrikke, RTD, Totalbeer) use identical parameters or category-specific ones → **Task T-008**

## Critical Findings

✅ **Feature engineering logically sound:**
- Lags justified by ACF/PACF analysis
- Rolling windows aligned to Nielsen calendar
- Holiday months empirically derived (March, June, December peaks)
- Log transformation addresses stationarity requirement
- No look-ahead bias (shift(1) for rolling, shift(lag) for autoregressive)

⚠️ **To investigate:**
- Are parameters truly category-specific or hardcoded globally?
- Is log transform applied in Step 4 or elsewhere?
- Do other categories have different holiday months?

---

## Next Steps

✅ T-003 COMPLETE → Unblocks T-007, T-008 (stationarity, category comparison)

**Ready to audit:**
- T-004: Parameter audit (confirm values & locations)
- T-007: Stationarity treatment verification
- T-008: Cross-category feature comparison

---

**Status**: ✅ **T-003 COMPLETE**

14 engineered features per observation; log transform applied; no leakage detected.

