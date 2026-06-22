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

---

## Detailed Comparison

### 1. Data Loading & Preprocessing
| Aspect | Rossmann | CSD | Gap? |
|--------|----------|-----|------|
| Load CSV | ✓ | ✓ | None |
| Date parsing | ✓ (robust) | ✓ | None |
| Type conversion | ✓ | ✓ | None |
| Missing value check | ✓ | ✓ | None |

### 2. Exploratory Data Analysis
| Aspect | Rossmann | CSD | Gap? |
|--------|----------|-----|------|
| Descriptive stats | ✓ | ✓ | None |
| Data shape/info | ✓ | ✓ | None |
| Correlation matrix | ✓ | ✗ | **HIGH** |
| Distribution plots | ✓ (extensive) | ✗ | **HIGH** |
| Time series plots | ✓ | ✗ | **HIGH** |

### 3. Time Series Decomposition
| Aspect | Rossmann | CSD | Gap? |
|--------|----------|-----|------|
| Seasonal decomposition | ✓ | ✗ | **CRITICAL** |
| Trend extraction | ✓ | ✗ | **CRITICAL** |
| Residual analysis | ✓ | ✗ | **CRITICAL** |
| Stationarity tests (ADF) | ✓ | ✗ | **CRITICAL** |

### 4. Autocorrelation Analysis
| Aspect | Rossmann | CSD | Gap? |
|--------|----------|-----|------|
| ACF plots | ✓ | ✗ | **HIGH** |
| PACF plots | ✓ | ✗ | **HIGH** |
| Lag interpretation | ✓ | ✗ | **HIGH** |

### 5. Feature Engineering Validation
| Aspect | Rossmann | CSD | Gap? |
|--------|----------|-----|------|
| Parameter sensitivity | ✓ | ✓ | None |
| Visualization of results | ✓ | ✗ | **MEDIUM** |

---

## Recommended Actions

### Priority 1: Add Visualizations (1–2 days)
```python
# Add to pre_csd_eda.py:
# - matplotlib.pyplot for distribution, time series, correlation heatmap
# - sns.histplot for multi-column distributions
# - plt.plot for time series trends
```

### Priority 2: Seasonal Decomposition (1 day)
```python
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(df['sales'], model='additive', period=52)  # weekly seasonality
```

### Priority 3: Stationarity Testing (1 day)
```python
from statsmodels.tsa.stattools import adfuller
adf_result = adfuller(df['sales'])
print(f"ADF p-value: {adf_result[1]}")  # if p < 0.05, series is stationary
```

### Priority 4: ACF/PACF (1 day)
```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf(df['sales'], lags=40)
plot_pacf(df['sales'], lags=40)
```

---

## Timeline

- **Week of 2026-05-14:** Implement visualizations + seasonal decomposition
- **Week of 2026-05-21:** Add stationarity + ACF/PACF analysis
- **By 2026-05-28:** Full Rossmann parity achieved

---

## Related Documents

- [CSD EDA Reference](./2026-05-14_DOC-vps-ready-eda-code-reference.md)
- [Feature Engineering & EDA Analysis](./2026-05-14_DOC-feature-engineering-eda-analysis-and-insights.md)
