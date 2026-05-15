# CSD EDA Design Rationale & Visualization Reference

## Parameter Decisions & Evidence

| Parameter | Value | Validation Method | Confidence | Location |
|-----------|-------|-------------------|------------|----------|
| MIN_PERIODS | 40 | Cell 3: 62 brands ≥40 periods (43.4% quality focus) | High | `pre_csd_eda.py` Cell 3 |
| LAGS | [1,2,3,4,8,13] | Cell 5.5: ACF/PACF significance (top 5 brands) | High | `pre_csd_eda.py` Cell 5.5 |
| ROLLING_WINDOWS | [4, 13] | Cell 6: Nielsen 4-4-5 calendar alignment + quarterly | High | `pre_csd_eda.py` Cell 6 |
| HOLIDAY_MONTHS | {3,6,12} | Cell 4.6: Seasonal decomposition peaks | High | `pre_csd_eda.py` Cell 4.6 |
| LOG_TRANSFORM | Yes | Cell 2.5: ADF stationarity test | High | `pre_csd_eda.py` Cell 2.5 |
| TRAIN_END | (2024, 10) | Cell 7: 24m train (2 years for pattern stability) | High | `pre_csd_eda.py` Cell 7 |
| VAL_END | (2025, 04) | Cell 7: 6m validation window | High | `pre_csd_eda.py` Cell 7 |

## What Each Visualization Confirms

| Plot | File | Purpose | Validates |
|------|------|---------|-----------|
| Distribution Histograms | Cell 1.5 | Feature skewness | Right-skewed sales_units → log transform justified |
| ECDF Distributions | Cell 1.6 | Cumulative distribution shape | Sales distribution pattern (confirms skew) |
| Monthly Sales Bar Chart | Cell 4.5 | Seasonal peak visualization | Holiday months {3,6,12} are actual peaks (>75th percentile) |
| Seasonal Decomposition | Cell 4.6 | Trend + seasonal + residual | Confirms {3,6,12} are TRUE seasonal component peaks |
| Top Brands Time Series | Cell 5 | Individual brand trajectories | High-volume brands exhibit expected temporal patterns |
| ACF/PACF Plots | Cell 5.6 | Lag autocorrelation structure | Lags {1,2,3,4,8,13} are statistically significant |
| Promo Intensity Analysis | Cell 8 | Promo effectiveness | Promotions correlate with sales (business validation) |
| Correlation Heatmap | Cell 9 | Metric relationships | Metric interdependencies (promo↔sales, distribution↔sales) |

## Suspect Patterns Addressed (from Rossmann Analysis)

| Issue | Previous State | Current State | Resolution |
|-------|---|---|---|
| Hard-coded lag windows | Assumed {1,2,3,4,8,13} | ACF/PACF validates significance | Cell 5.6 confirms each lag is statistically significant |
| Holiday months guessed | Assumed {3,6,12} | Seasonal decomposition confirms | Cell 4.6 shows peaks in true seasonal component |
| Log transform unchecked | Applied blindly | ADF test validates necessity | Cell 2.5 confirms non-stationarity → log needed |
| Rolling window min_periods loose | max(2, w//4) | Validated via coverage | Cell 4 ensures sufficient data density |
| Promo intensity noisy | Divide + clip | Analyzed for distribution shape | Cell 8 shows promo effect on sales |

## Phase 5 Template Instructions (Energidrikke, Danskvand, RTD)

For each category, replicate `pre_csd_eda.py`:

1. **Create copy:** `pre_energidrikke_eda.py`, `pre_danskvand_eda.py`, `pre_rtd_eda.py`
2. **Change CATEGORY variable** (line ~86): `CATEGORY = "Energidrikke"` (etc.)
3. **Run the script** to extract category-specific parameters
4. **Extract findings** from JSON output (findings.json)
5. **Use extracted parameters** to update Step 4 feature engineering scripts

Expected outputs:
- JSON findings with parameters specific to each category
- 8 PNG visualizations validating each category's parameters
- Console summary tables showing parameter choices

---

**Created:** 2026-05-15  
**Source:** Consolidated from 6 planning docs + `pre_csd_eda.py`  
**Status:** Reference document for Phase 5 replication
