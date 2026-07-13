---
pid: P0023
created: 2026-06-30 12:38:00
updated: 2026-06-30 14:00:00
status: complete
completed: 2026-06-30 14:00:00
outcome_summary: "All 13 EDA critique findings fixed in pre_csd_1.5_eda.py. 3 new analysis cells added (5b zero-sales, 9b heterogeneity, 15b structural break). Parameters now empirically derived."
---

# P0023 — EDA Critique: CSD Nielsen Time Series for Predictive Sales ML

## Goal

Produce a structured, actionable critique of the existing CSD EDA script (`pre_csd_1.5_eda.py`) from the perspective of:
- **Predictive sales ML** using lightweight models (LightGBM, XGBoost, Ridge, etc.)
- **FMCG Nielsen panel data** as monthly time series per brand

The critique should drive concrete improvements, not just flag issues.

---

## Context

- **Input**: `step_1_aggregate.parquet` — aggregated CSD sales data per brand × month
- **Script**: `pre_csd_1.5_eda.py` (16 analysis cells, ~940 lines)
- **Downstream use**: Feature engineering parameters fed to preprocessing pipeline (P0022)
- **Models in scope**: Lightweight (LightGBM, XGBoost, Ridge regression, ElasticNet)
- **Data grain**: Monthly periods, multiple brands, Nielsen panel
- **Purpose**: Proof-of-concept thesis — not production

---

## Phases

### Phase 1 — Deep Read & Catalogue Existing EDA Steps
**Status**: complete

Map what each cell does and what ML-relevant questions it does/doesn't answer.

| Cell | Topic | ML-Relevant? | Notes |
|------|-------|-------------|-------|
| 1 | Load & overview | Partial | Missing: brand × time completeness matrix |
| 2 | Distribution histograms + skewness | Partial | Skewness thresholds are wrong; only looks at marginal distributions |
| 3 | Date range & time period | Yes | Good baseline — but doesn't detect gaps per brand |
| 4 | ADF stationarity test | Partial | Aggregated total only — not per brand; log transform decision is too simple |
| 5 | Brand stability (MIN_PERIODS) | Yes | Good concept; threshold logic sound |
| 6 | Seasonal pattern (holiday months) | Partial | Uses raw totals not normalized; dominated by high-volume brands |
| 7 | Monthly bar plot | Visual only | Cosmetic; doesn't add analytical content |
| 8 | Seasonal decomposition | Partial | Additive model assumption unchecked; aggregated not per-brand |
| 9 | Top brands time series | Yes | Good; only top 5 by volume |
| 10 | Lag analysis (manual correlation) | Partial | Only top brand; correlation not partial; doesn't test lag significance |
| 11 | ACF/PACF plots | Yes | Best cell — multi-brand, correct method |
| 12 | Rolling window analysis | Weak | Justification is qualitative/business, not data-driven |
| 13 | Train/Val/Test split | Critical gap | Hardcoded arithmetic — no data-driven justification; data leakage risk not addressed |
| 14 | Promo intensity | Partial | Useful but promo_units/(sales_units+1) is a flawed metric |
| 15 | Correlation heatmap | Partial | Pearson only; collinearity not assessed for features |
| 16 | Save findings | Mechanical | JSON output good for reproducibility |

---

### Phase 2 — Critique by Theme
**Status**: complete

See `findings.md` for full structured critique.

Themes:
1. Aggregation mistakes (cross-brand pooling distorts signal)
2. Missing target variable framing (what is Y?)
3. Train/val/test split — data leakage risk
4. Stationarity analysis is insufficient for ML
5. Lag/feature engineering validation gaps
6. Promo feature construction problems
7. Missing: cross-brand heterogeneity analysis
8. Missing: distribution shift / concept drift check
9. Skewness threshold logic error
10. Rolling window rationale is business not data-driven

---

### Phase 3 — Recommendations & Prioritisation
**Status**: complete

See `findings.md` → Recommendations section.

Priority tiers:
- **P0 (Must fix before feature engineering)**: Target variable definition, data leakage in split, per-brand stationarity
- **P1 (High value)**: Per-brand ACF/PACF, cross-brand heterogeneity, zero-sales handling
- **P2 (Nice to have)**: Distribution shift, promo metric fix, rolling window empirical test

---

### Phase 4 — Fix All 13 Issues in pre_csd_1.5_eda.py
**Status**: complete

All 13 fixes applied directly to the EDA script. New cells added: 5b, 9b, 15b. All existing cells updated in-place.

| Task | Fix | Location |
|------|-----|----------|
| C1 | ML_TARGET constants block added | Before Cell 1 |
| C2 | Per-brand split validation + WARMUP_PERIODS | Cell 13 |
| C3 | Per-brand ADF for top 20 brands + majority vote | Cell 4 |
| H1 | Lag corr across all stable brands, 50% threshold | Cell 10 |
| H2 | ACF significant lag extraction per brand | Cell 11 |
| H3 | Cross-brand CV, peak-month dist, promo spread | New Cell 9b |
| H4 | Zero-sales run analysis + imputation decision | New Cell 5b |
| H5 | Predictive corr + collinearity pruning for windows | Cell 12 |
| M1 | Fixed dead-code elif ordering in Cell 2 | Cell 2 |
| M2 | clip(lower=1) + data quality assertion | Cell 14 |
| M3 | Additive vs multiplicative auto-selection | Cell 8 |
| M4 | Pearson + Spearman side-by-side + delta flagging | Cell 15 |
| M5 | Structural break Chow test at 2020-03 | New Cell 15b |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Critique from lightweight ML perspective | Thesis uses LightGBM/XGBoost/Ridge — not ARIMA/LSTM |
| Focus on actionable gaps | Not cosmetic issues (plot colours etc.) |
| Per-brand vs aggregated is the central tension | Most EDA cells aggregate across brands, masking heterogeneity |

---

## Errors Encountered

None so far.
