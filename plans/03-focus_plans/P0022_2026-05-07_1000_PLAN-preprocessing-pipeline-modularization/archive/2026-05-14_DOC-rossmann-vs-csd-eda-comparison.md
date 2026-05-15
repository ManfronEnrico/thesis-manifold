# Rossmann vs. CSD EDA Script Comparison

**Purpose:** Identify missing EDA components from Rossmann best practices that should be added to CSD preprocessing EDA  
**Date:** 2026-05-14  
**Scripts Compared:**
- Reference: `Example_Notebook-Source_time_series_prophet-Rossmann_Sales.py` (946 lines)
- Current: `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_and_parameter_analysis.py` (465 lines)

---

## Executive Summary

Your CSD EDA script is **well-structured for parameter selection** but is **missing visualization components** and **time series decomposition analysis** that Rossmann uses to validate feature engineering decisions.

**Missing Components (HIGH PRIORITY):**
1. ✗ Visualization (ECDF, monthly trends, seasonality plots)
2. ✗ Seasonal decomposition (trend + seasonal + residual)
3. ✗ ACF/PACF plots (autocorrelation structure)
4. ✗ Stationarity testing (ADF test)
5. ✗ Correlation analysis (variable relationships)

**What You Have (GOOD):**
- ✓ Data overview & coverage analysis
- ✓ Brand stability (min_periods threshold)
- ✓ Monthly sales distribution & peak analysis
- ✓ Lag correlation for top brands
- ✓ Rolling window justification
- ✓ Train/val/test split calculation
- ✓ JSON output for reproducibility

---

## Detailed Comparison Table

| EDA Component | Rossmann | Your CSD | Priority | Why Missing |
|---|---|---|---|---|
| **Data Loading & Overview** | ✓ Basic stats | ✓ Extended (quality metrics) | ✓ | You exceed Rossmann |
| **ECDF Distribution** | ✓ Plot sales/customers | ✗ Missing | 🟡 MED | Would show sales distribution skew |
| **Missing Value Analysis** | ✓ Detailed | ✗ Quick check | 🟡 MED | Your step 3 already filters, less critical |
| **Feature Creation** | ✓ Sales/customer ratio | ✗ Not applicable | ⚠️ | Nielsen already has ratio metrics |
| **Categorical Breakdown** | ✓ By store type | ✓ By brand (implicitly) | ✓ | Your approach better (brand-level) |
| **Correlation Heatmap** | ✓ Full correlation matrix | ✗ Missing | 🟡 MED | Would show metric relationships |
| **Monthly/Seasonal Trends** | ✓ Facet plots by store type | ✓ Aggregated monthly | ✓ | You validate holiday months |
| **Seasonal Decompose** | ✓ trend + seasonal + residual | ✗ Missing | 🔴 HIGH | **Critical for confirming peaks** |
| **Time Series Plot (raw)** | ✓ Resample + plot trends | ✗ Missing | 🔴 HIGH | Would show trend visually |
| **ACF/PACF Plots** | ✓ 50-lag ACF + PACF per group | ✗ Missing | 🔴 HIGH | **Essential for lag validation** |
| **Stationarity Test (ADF)** | ✗ Not in script | ✗ Missing | 🔴 HIGH | **Critical before log transform** |
| **Autocorrelation Analysis** | ✓ Manual lag correlation | ✓ Simple correlation on 1 brand | ✓ | Yours is more focused |
| **Train/Val/Test Split** | ✗ Not in EDA | ✓ Calculated | ✓ | You exceed Rossmann |

---

## Missing Component Details

### 1. ECDF (Empirical Cumulative Distribution)

**Rossmann does this (cells ~99-125):**
```python
from statsmodels.distributions.empirical_distribution import ECDF

cdf = ECDF(train['Sales'])
plt.plot(cdf.x, cdf.y)
```

**Why it matters:**
- Shows what % of data is below any sales value
- Reveals if distribution is normal, bimodal, skewed, etc.
- Helps identify outliers and zero-inflation

**For CSD:** Plot ECDF of `sales_units` per brand category
- Would show if CSD sales are skewed vs. RTD/Energidrikke
- Justifies log transform (if distribution is right-skewed)

**Add to CSD (Cell 1.5):**
```python
# %% ECDF Distribution Analysis
from statsmodels.distributions.empirical_distribution import ECDF

for category in ['CSD', 'RTD', 'Energidrikke', 'Danskvand']:
    cat_data = df[df['category'] == category]
    cdf = ECDF(cat_data['sales_units'][cat_data['sales_units'] > 0])
    plt.plot(cdf.x, cdf.y, label=category)
```

---

### 2. Seasonal Decomposition

**Rossmann does this (cells ~432-446):**
```python
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(sales_series, model='additive', freq=365)
decomposition.trend.plot()
decomposition.seasonal.plot()
decomposition.residual.plot()
```

**Why it matters:**
- **Trend:** Shows if sales increasing/decreasing over time
- **Seasonal:** Isolates the repeating pattern (confirms peaks)
- **Residual:** What's left (noise, unexplained variation)

**For CSD:** Decompose aggregated CSD sales
- Confirms your {3, 6, 12} holiday months are actually in seasonal component
- Shows if trend is stable or declining (important for model generalization)
- Reveals hidden patterns in residuals

**Add to CSD (Cell 4.5):**
```python
# %% Seasonal Decomposition
# Aggregate CSD sales by month (all brands combined)
csd_monthly = df.groupby(['period_year', 'period_month'])['sales_units'].sum()
csd_monthly.index = pd.to_datetime(csd_monthly.index.map(lambda x: f"{x[0]}-{x[1]:02d}"))
csd_monthly = csd_monthly.sort_index()

decomposition = seasonal_decompose(csd_monthly, model='additive', period=12)

fig, axes = plt.subplots(4, 1, figsize=(14, 10))
csd_monthly.plot(ax=axes[0], title='Original')
decomposition.trend.plot(ax=axes[1], title='Trend')
decomposition.seasonal.plot(ax=axes[2], title='Seasonal')
decomposition.resid.plot(ax=axes[3], title='Residual')
plt.tight_layout()
```

**Then validate:**
```python
# Extract seasonal component peaks
seasonal_component = decomposition.seasonal
peaks = seasonal_component.groupby(seasonal_component.index.month).mean().nlargest(3)
print(f"Seasonal peaks in months: {sorted(peaks.index.tolist())}")
# Should match {3, 6, 12}
```

---

### 3. ACF/PACF Plots

**Rossmann does this (cells ~461-481):**
```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plt.figure(figsize=(12, 8))
plot_acf(sales_series, lags=50, ax=plt.gca())
plot_pacf(sales_series, lags=50, ax=plt.gca())
```

**Why it matters:**
- **ACF:** Correlation with past values; identifies seasonality (spikes at lag-12, lag-4, etc.)
- **PACF:** Partial correlation; shows true autoregressive order
- Validates lag selection (are lags 1,2,3,4,8,13 actually significant?)

**Your current approach (Cell 5):**
- Simple correlation on 1 brand
- Doesn't show full autocorrelation structure
- Can't see if spikes are significant (>2σ)

**Add to CSD (Cell 5.5):**
```python
# %% ACF/PACF Analysis for Top Brands
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

top_5_brands = df.groupby('brand')['sales_units'].sum().nlargest(5).index

fig, axes = plt.subplots(5, 2, figsize=(14, 15))
for idx, brand in enumerate(top_5_brands):
    brand_series = df[df['brand'] == brand].sort_values(['period_year', 'period_month'])['sales_units'].values
    
    # ACF
    plot_acf(brand_series, lags=30, ax=axes[idx, 0], title=f'{brand} ACF')
    # PACF
    plot_pacf(brand_series, lags=30, ax=axes[idx, 1], title=f'{brand} PACF')

plt.tight_layout()

# Interpretation guide:
print("✓ Look for spikes outside confidence bands (blue shaded area)")
print("✓ Lag-12 spike → annual seasonality")
print("✓ Lag-4 spike → quarterly pattern")
print("✓ Lag-1,2,3,4 together → short-term dependency")
```

**Then validate your lags:**
```python
# Check if your lags {1,2,3,4,8,13} are statistically significant
for brand in top_5_brands:
    brand_series = df[df['brand'] == brand].sort_values(['period_year', 'period_month'])['sales_units'].values
    acf_vals = acf(brand_series, nlags=15)
    
    for lag in [1, 2, 3, 4, 8, 13]:
        if lag < len(acf_vals):
            is_significant = abs(acf_vals[lag]) > 1.96 / np.sqrt(len(brand_series))
            print(f"{brand} lag-{lag}: {acf_vals[lag]:+.3f} {'✓' if is_significant else '✗'}")
```

---

### 4. Stationarity Testing (ADF Test)

**Not in Rossmann** but critical for your implementation  
**Why it matters:**
- Time series models assume stationarity (constant mean, variance, autocorrelation)
- Non-stationary series needs differencing (d parameter)
- Log transform stabilizes *variance*, not *mean*

**Current issue:**
You apply log transform without checking if it's needed.

**Add to CSD (New Cell 2.5):**
```python
# %% Stationarity Testing (ADF Test)
from statsmodels.tsa.stattools import adfuller

def adf_test(timeseries, name=''):
    result = adfuller(timeseries.dropna(), autolag='AIC')
    print(f"\n{name} ADF Test Results:")
    print(f"  ADF Statistic: {result[0]:+.6f}")
    print(f"  p-value: {result[1]:.6f}")
    print(f"  Stationary: {'YES ✓' if result[1] < 0.05 else 'NO ✗ (needs differencing)'}")
    return result[1] < 0.05

# Test CSD aggregated series
csd_agg = df.groupby(['period_year', 'period_month'])['sales_units'].sum()
is_stationary = adf_test(csd_agg, "CSD Sales (Original)")

if not is_stationary:
    # Try differencing
    csd_diff = csd_agg.diff().dropna()
    is_stat_diff = adf_test(csd_diff, "CSD Sales (First Difference)")
    
    # Try log + differencing
    csd_log_diff = np.log1p(csd_agg).diff().dropna()
    is_stat_log_diff = adf_test(csd_log_diff, "CSD Sales (Log-Diff)")

print("\n✓ Recommendation:")
if is_stationary:
    print("  Use original sales_units (no transform needed)")
elif is_stat_diff:
    print("  Use differencing (d=1) in ARIMA")
else:
    print("  Use log transform + differencing (log1p + diff)")
```

---

### 5. Correlation Heatmap

**Rossmann does this (cells ~315-332):**
```python
import seaborn as sns
corr_matrix = df.corr()
sns.heatmap(corr_matrix, ...)
```

**Why it matters:**
- Shows which metrics are correlated (sales ~ promo? sales ~ competition distance?)
- Identifies multicollinearity (redundant features)
- Validates business intuition (e.g., promo should correlate with sales)

**For CSD:**
```python
# %% Correlation Analysis
corr_cols = ['sales_units', 'sales_value', 'sales_liters', 'promo_units', 'weighted_dist']
corr_matrix = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
plt.title('CSD Sales Metrics Correlation')
plt.tight_layout()

print("\nInterpretation:")
print(f"  sales_units ↔ promo_units: {corr_matrix.loc['sales_units', 'promo_units']:.3f}")
print("  → Strong positive = promos work")
print(f"  sales_units ↔ weighted_dist: {corr_matrix.loc['sales_units', 'weighted_dist']:.3f}")
print("  → Strong positive = distribution matters")
```

---

## Missing Visualization Components Summary

| Plot Type | Lines | Purpose | For CSD | Difficulty |
|---|---|---|---|---|
| ECDF | ~20 | Distribution shape | Show sales_units skew | 🟢 Easy |
| Monthly trend facets | ~50 | Seasonal pattern by subgroup | Aggregate view | 🟢 Easy |
| Seasonal decompose | ~40 | Trend + seasonal isolation | Validate holiday months | 🟡 Medium |
| Time series resampled | ~15 | Trend visualization | Downsample monthly→quarterly | 🟢 Easy |
| ACF/PACF subplots | ~35 | Lag significance | Validate lag selection | 🟡 Medium |
| Correlation heatmap | ~15 | Metric relationships | Validate promo/distribution correlations | 🟢 Easy |
| **Total Lines** | **~175** | | | |

---

## Recommendation: Phased Addition

### Phase 1 (IMMEDIATE - High Impact):
1. **Seasonal decomposition** (Cell 4.5)
   - Validates {3,6,12} empirically
   - Shows trend stability
   - ~40 lines of code
   
2. **ACF/PACF plots** (Cell 5.5)
   - Validates lags {1,2,3,4,8,13}
   - Shows statistical significance
   - ~35 lines of code

3. **ADF stationarity test** (Cell 2.5)
   - Justifies log transform decision
   - Determines if differencing needed
   - ~30 lines of code

**Total impact:** 3 cells, ~105 lines, addresses all "HIGH" priority gaps

### Phase 2 (NICE-TO-HAVE):
1. ECDF distribution plots
2. Correlation heatmap
3. Monthly trend facet plots

---

## Code Structure Recommendation

Keep your current structure, insert missing cells in order:

```
CELL 1: Data Overview
CELL 1.5: ECDF Distribution (NEW)
CELL 2: Date Range Analysis
CELL 2.5: Stationarity Testing (NEW)
CELL 3: Brand Stability
CELL 4: Seasonal Analysis (keep, will benefit from decompose)
CELL 4.5: Seasonal Decomposition (NEW)
CELL 5: Lag Analysis (keep)
CELL 5.5: ACF/PACF Validation (NEW)
CELL 6: Rolling Windows (keep)
CELL 7: Train/Val/Test (keep)
CELL 8: Summary & Findings (keep)
```

---

## Comparison Summary Table

| Aspect | Rossmann | CSD | Winner |
|---|---|---|---|
| **Data quality focus** | Count rows/missing | + Distribution quality metrics | CSD ✓ |
| **Parameter validation** | Not really (no parameters) | Full parameter selection | CSD ✓ |
| **Visualization** | Extensive (15+ plots) | Minimal (trend tables) | Rossmann ✓ |
| **Time series decomposition** | Yes | Missing | Rossmann ✓ |
| **ACF/PACF analysis** | Yes | Missing | Rossmann ✓ |
| **Stationarity check** | No | Missing | Neither ✗ |
| **Reproducibility** | Visual only | + JSON output | CSD ✓ |
| **Automation-friendly** | No (notebook) | Yes (Python cells) | CSD ✓ |

---

## Next Steps

1. ✅ **Review this comparison** — understand what's missing and why
2. 🔧 **Add Phase 1 cells** to your CSD EDA script:
   - Seasonal decomposition
   - ACF/PACF plots
   - ADF stationarity test
3. 📊 **Run enhanced EDA** on VPS
4. ✏️ **Update feature engineering doc** with visualization insights

**Estimated time to implement:** 2-3 hours (mostly copy-paste from Rossmann + adapt for CSD)

---

**Document Status:** Ready for implementation  
**Last Updated:** 2026-05-14 14:45
