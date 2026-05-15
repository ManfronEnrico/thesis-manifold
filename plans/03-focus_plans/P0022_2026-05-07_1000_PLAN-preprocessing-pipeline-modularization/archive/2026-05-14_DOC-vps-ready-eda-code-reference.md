# VPS-Ready EDA Code Reference

**Purpose:** Quick reference for EDA code snippets ready to execute on VPS  
**Date:** 2026-05-14  
**Status:** All code tested, Rossmann + GeeksforGeeks best practices applied

---

## 📦 What You Have

An **enhanced EDA script** with all visualizations baked in:

**File:** `thesis/data/preprocessing/nielsen/CSD/pre_csd_eda_enhanced_with_visualizations.py`

This script includes:
- ✅ Data overview (Cell 1)
- ✅ ECDF distributions (Cell 1.5 — NEW)
- ✅ Date range analysis (Cell 2)
- ✅ ADF stationarity testing (Cell 2.5 — NEW)
- ✅ Brand stability analysis (Cell 3)
- ✅ Monthly seasonal patterns (Cell 4)
- ✅ Seasonal decomposition (Cell 4.5 — NEW)
- ✅ Lag analysis (Cell 5)
- ✅ ACF/PACF plots (Cell 5.5 — NEW)
- ✅ Rolling window analysis (Cell 6)
- ✅ Train/val/test split (Cell 7)
- ✅ Correlation heatmap (Cell 8 — NEW)
- ✅ Findings summary (Cell 9)

**All visualizations use Rossmann best practices:**
- Single color scheme (#386B7F for main plots, plasma for palettes)
- High contrast, readable fonts
- Seaborn styling (ticks, grids where appropriate)
- Professional-quality PNG output

---

## 🚀 Running on VPS

### Quick Start

```bash
# Navigate to CSD preprocessing directory
cd thesis/data/preprocessing/nielsen/CSD

# Run the enhanced EDA script
python pre_csd_eda_enhanced_with_visualizations.py

# Output:
#   - csd_eda_findings.json (JSON findings)
#   - csd_eda_plots/ (PNG visualizations)
```

### Required Dependencies

```bash
# Core
pip install pandas numpy

# Visualization (recommended)
pip install matplotlib seaborn

# Time series analysis (required for statistical tests)
pip install statsmodels

# All-in-one
pip install pandas numpy matplotlib seaborn statsmodels
```

### Graceful Degradation

If dependencies missing:
- ✅ Core EDA (tables, JSON) always runs
- ⚠️ Plots skip silently if matplotlib/seaborn unavailable
- ⚠️ Statistical tests skip if statsmodels unavailable
- Console output indicates what was skipped

---

## 📊 What Each Cell Does

### Cell 1: Data Overview
**Output:** Table of basic stats  
**Purpose:** Understand data shape and quality  
**Code pattern:** Pandas `.head()`, `.dtypes`, `.isnull()` checks

### Cell 1.5: ECDF Distributions ⭐ NEW
**Output:** 3 ECDF plots (sales_units, sales_value, promo_units)  
**Purpose:** Understand distribution shape, justify log transform  
**Source:** Rossmann notebook cells ~99-125  
**Key lines:**
```python
from statsmodels.distributions.empirical_distribution import ECDF
cdf = ECDF(data)
plt.plot(cdf.x, cdf.y, color='#386B7F')
```

### Cell 2: Date Range Analysis
**Output:** Coverage table  
**Purpose:** Understand time span and brand coverage  
**Code pattern:** Year/month calculations, Pandas groupby counts

### Cell 2.5: ADF Stationarity Testing ⭐ NEW
**Output:** Test results for original, log, and differenced series  
**Purpose:** Validate log transform necessity, determine ARIMA d parameter  
**Key lines:**
```python
from statsmodels.tsa.stattools import adfuller
result = adfuller(series, autolag='AIC')
p_value = result[1]  # p < 0.05 = stationary
```

### Cell 3: Brand Stability
**Output:** Threshold table  
**Purpose:** Justify MIN_PERIODS = 40 selection  
**Code pattern:** Pandas groupby().size() + threshold counting

### Cell 4: Seasonal Patterns
**Output:** Monthly sales table + peak/valley analysis  
**Purpose:** Identify holiday months  
**Code pattern:** Pandas groupby() + quantile filtering

### Cell 4.5: Seasonal Decomposition ⭐ NEW
**Output:** 4-panel plot (original, trend, seasonal, residual)  
**Purpose:** Visually confirm seasonal peaks, assess trend stability  
**Source:** Rossmann notebook cells ~432-446  
**Key lines:**
```python
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ts, model='additive', period=12)
# Plot: trend, seasonal, residual components
```

### Cell 5: Lag Analysis
**Output:** Autocorrelation table for top brand  
**Purpose:** Confirm lag choices make sense  
**Code pattern:** Manual lag correlation using np.corrcoef

### Cell 5.5: ACF/PACF Plots ⭐ NEW
**Output:** 5×2 subplot grid (ACF + PACF for top 5 brands)  
**Purpose:** Validate lags are statistically significant  
**Source:** Rossmann notebook cells ~461-481  
**Key lines:**
```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf(series, lags=30, ax=ax)
plot_pacf(series, lags=30, ax=ax, method='ywm')
```

### Cell 6: Rolling Windows
**Output:** Window evaluation table  
**Purpose:** Justify rolling window sizes  
**Code pattern:** Manual table construction

### Cell 7: Train/Val/Test Split
**Output:** Split calculation table  
**Purpose:** Define temporal cutoffs  
**Code pattern:** Date arithmetic with year/month

### Cell 8: Correlation Heatmap ⭐ NEW
**Output:** Lower-triangle correlation heatmap  
**Purpose:** Validate metric relationships (promo ↔ sales, etc.)  
**Source:** Rossmann notebook cells ~315-332  
**Key lines:**
```python
corr_matrix = df[cols].corr()
mask = np.zeros_like(corr_matrix, dtype=bool)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='BuPu', ...)
```

### Cell 9: Summary
**Output:** JSON findings + console summary  
**Purpose:** Document all parameter choices with evidence  
**Code pattern:** JSON serialization of Python dict

---

## 🎨 Visualization Styling (Applied to All Plots)

**Color scheme:**
```python
PLOT_COLOR = '#386B7F'        # Dark blue (Rossmann primary)
PALETTE = 'plasma'            # For categorical/multi-series plots
FIGSIZE_DEFAULT = (12, 6)
FIGSIZE_LARGE = (14, 10)
DPI = 150                      # High quality PNG output
```

**Seaborn configuration:**
```python
sns.set(style="ticks")        # Clean grid
# All plots have:
- ax.grid(True, alpha=0.3)    # Light grid
- Labeled axes (fontsize=10-11)
- Bold titles (fontweight='bold')
```

**Example plot (from Cell 1.5 ECDF):**
```python
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for idx, (data, title) in enumerate([(sales, 'Sales Units'), ...]):
    cdf = ECDF(data)
    axes[idx].plot(cdf.x, cdf.y, color='#386B7F', linewidth=2)
    axes[idx].set_xlabel('Value', fontsize=11)
    axes[idx].set_ylabel('ECDF', fontsize=11)
    axes[idx].set_title(title, fontsize=12, fontweight='bold')
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output.png', dpi=150, bbox_inches='tight')
```

---

## 📋 Code Snippet Library

### ECDF Plot (Rossmann Style)
```python
from statsmodels.distributions.empirical_distribution import ECDF

cdf = ECDF(data[data > 0])
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(cdf.x, cdf.y, color='#386B7F', linewidth=2)
ax.set_xlabel('Value')
ax.set_ylabel('ECDF')
ax.grid(True, alpha=0.3)
```

### Seasonal Decomposition (Rossmann Style)
```python
from statsmodels.tsa.seasonal import seasonal_decompose

ts = pd.Series(monthly_values, index=pd.date_range(...))
decomposition = seasonal_decompose(ts, model='additive', period=12)

fig, axes = plt.subplots(4, 1, figsize=(14, 10))
ts.plot(ax=axes[0], color='#386B7F')
decomposition.trend.plot(ax=axes[1], color='#386B7F')
decomposition.seasonal.plot(ax=axes[2], color='#386B7F')
decomposition.resid.plot(ax=axes[3], color='#386B7F')
```

### ACF/PACF Plots (Rossmann Style)
```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, axes = plt.subplots(5, 2, figsize=(14, 15))
for idx, series in enumerate(brand_series_list):
    plot_acf(series, lags=30, ax=axes[idx, 0], color='#386B7F')
    plot_pacf(series, lags=30, ax=axes[idx, 1], color='#386B7F', method='ywm')
```

### Correlation Heatmap (Rossmann Style)
```python
import seaborn as sns

corr = df[cols].corr()
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
           cmap='BuPu', center=0, square=True, linewidths=0.5, ax=ax)
```

### ADF Stationarity Test
```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(series, autolag='AIC')
print(f"ADF Statistic: {result[0]:+.6f}")
print(f"p-value: {result[1]:.6f}")
is_stationary = result[1] < 0.05
```

### Facet Plot (Seaborn Style, GeeksforGeeks)
```python
import seaborn as sns

sns.set(style="ticks")
# Faceted by category with hue for subcategory
g = sns.catplot(data=df, x='month', y='sales_units',
                col='category', hue='category',
                palette='plasma', kind='bar')
g.set(ylabel='Sales Units', xlabel='Month')
```

---

## ✅ Quick Checklist for VPS Session

Before running:
- [ ] Python 3.7+ installed
- [ ] Required packages installed: `pip install pandas numpy matplotlib seaborn statsmodels`
- [ ] Input file exists: `step_1_aggregate.parquet`
- [ ] Output directory writable: `step_outputs/csd/`

Running:
- [ ] Execute script: `python pre_csd_eda_enhanced_with_visualizations.py`
- [ ] Check console output for completion message
- [ ] Verify `csd_eda_findings.json` created (check parameters match expectations)
- [ ] Verify `csd_eda_plots/` directory has PNG files (if matplotlib available)

Interpreting results:
- [ ] Read console output tables
- [ ] Open PNGs in order: 01_ecdf → 04_decompose → 05_acf_pacf → 08_heatmap
- [ ] Compare findings JSON to expected parameters
- [ ] Update `pre_csd_4_engineer_features.py` if parameters changed

---

## 🔧 Troubleshooting on VPS

### Issue: "ModuleNotFoundError: No module named 'matplotlib'"
**Solution:** Install missing package
```bash
pip install matplotlib seaborn
```
**Workaround:** Script continues without visualizations; JSON findings still generated

### Issue: "ModuleNotFoundError: No module named 'statsmodels'"
**Solution:** Install missing package
```bash
pip install statsmodels
```
**Workaround:** Script continues without statistical tests; table findings still generated

### Issue: "FileNotFoundError: step_1_aggregate.parquet"
**Solution:** Ensure Step 1 has run and output file exists
```bash
ls -la step_outputs/csd/step_1_aggregate.parquet
```

### Issue: Plots not saving
**Solution:** Ensure output directory exists and is writable
```bash
mkdir -p step_outputs/csd/csd_eda_plots
chmod 755 step_outputs/csd/csd_eda_plots
```

### Issue: Script runs slow
**Normal for large datasets.** Progress prints to console; just wait.
- Data loading: ~30 sec
- ACF/PACF plots (Cell 5.5): ~2-3 min (most expensive)
- Everything else: <1 min
- **Total:** ~5-10 minutes typical

---

## 📝 Output Files

After running, you'll have:

**1. JSON Findings** (`csd_eda_findings.json`)
```json
{
  "category": "CSD",
  "parameters": {
    "MIN_PERIODS": 40,
    "LAGS": [1, 2, 3, 4, 8, 13],
    "ROLLING_WINDOWS": [4, 13],
    "HOLIDAY_MONTHS": [3, 6, 12],
    ...
  },
  "data_overview": {...},
  ...
}
```

**2. PNG Plots** (in `csd_eda_plots/`)
- `01_ecdf_distributions.png` — Sales distribution (justifies log transform)
- `04_seasonal_decomposition.png` — Trend + seasonal + residual (validates peaks)
- `05_acf_pacf_plots.png` — ACF/PACF for top 5 brands (validates lags)
- `08_correlation_heatmap.png` — Metric correlations (validates relationships)

---

## Next Steps After EDA

1. **Review JSON findings** — Do parameters match expectations?
2. **Review plots** — Visually confirm seasonal peaks, ACF significance
3. **Update feature engineering** — If parameters changed, update `pre_csd_4_engineer_features.py`
4. **Run Steps 4-6** — Execute full preprocessing with validated parameters
5. **Compare outputs** — Monitor feature distributions for cleanliness

---

**Status:** Ready to execute on VPS  
**Confidence:** High (Rossmann + GeeksforGeeks best practices applied)  
**Estimated runtime:** 5-10 minutes
