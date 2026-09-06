---
name: eda-improvement-candidates
description: REFERENCE - Candidate EDA improvements for Nielsen time series preprocessing, with literature grounding assessment
category: reference
applies-to: [eda, preprocessing, nielsen, time-series]
created: 2026_06_30-14_30
updated: 2026_06_30-14_30
---

# EDA Improvement Candidates — Nielsen Time Series
> Scope: `pre_csd_1.5_eda.py` and Phase 5 category replications  
> Context: Predictive sales ML (LightGBM/XGBoost/Ridge), FMCG Nielsen monthly panel, per-brand

---

## Summary Table

| # | Improvement | Priority | Literature Grounding | Status |
|---|-------------|----------|---------------------|--------|
| 1 | Walk-forward cross-validation feasibility check | High | Strong | Candidate |
| 2 | Lagged scatter plots (feature-target visual) | Medium | Weak (Tukey 1977) | Candidate |
| 3 | Per-volume-tier distribution analysis | Medium | Moderate (Pesaran & Smith 1995) | Candidate |
| 4 | Weighted distribution threshold effect | High | Moderate (Ataman et al. 2010) | Candidate |
| 5 | Fourier / spectral analysis (multi-frequency seasonality) | Medium | Strong | Candidate |
| 6 | Train-size adequacy curve (MIN_PERIODS sensitivity) | Medium | Moderate (Cerqueira et al. 2020) | Candidate |

---

## Detailed Assessments

### 1 — Walk-Forward Cross-Validation Feasibility Check

**What it adds**: Instead of a single 24/6/test split, test how many walk-forward CV folds are viable given each brand's history length. Answers the question: can this dataset support CV, and for how many folds?

**Why it matters for ML**: A single split gives one point estimate of error. Walk-forward CV gives a distribution, which is required for a credible thesis methods section.

**Literature grounding**: **Strong**
- Hyndman & Athanasopoulos (2021) *Forecasting: Principles and Practice* — canonical reference for time series CV
- Bergmeir & Benítez (2012, *Information Sciences*) — specific empirical evidence that random CV is invalid for autocorrelated series; time series CV required
- **Check Zotero**: likely already present; search `hyndman` or `forecasting evaluation`

**Implementation note**: EDA role = feasibility check only (min brand history to support K folds). Model evaluation in preprocessing pipeline, not EDA.

---

### 2 — Lagged Scatter Plots (Feature-Target Visual)

**What it adds**: Scatter plots of `log1p(sales_units[t])` vs `log1p(sales_units[t-k])` for k=1,4,12. Reveals whether the lag relationship is linear (good for Ridge), threshold-shaped, or heteroscedastic.

**Why it matters for ML**: ACF shows *if* a lag correlates; scatter shows *how*. A non-linear lag relationship justifies LightGBM over Ridge — a modelling decision the EDA should inform.

**Literature grounding**: **Weak as a standalone method**
- Tukey (1977) *Exploratory Data Analysis* — general EDA practice
- No single canonical citation for "lagged scatter plots in time series EDA"
- **Recommendation**: frame as exploratory visualization, not a formal test. Do not cite as methodology in the thesis chapter — include in appendix only.

---

### 3 — Per-Volume-Tier Distribution Analysis

**What it adds**: Separate distribution histograms and skewness tests for top/mid/low volume quartile brands. Tests whether the log-transform decision and feature engineering are uniform across brand sizes.

**Why it matters for ML**: If small brands have fundamentally different distributions (more zeros, higher skew), they may need different preprocessing. Pooling them silently violates the panel homogeneity assumption.

**Literature grounding**: **Moderate**
- Pesaran & Smith (1995, *Journal of Econometrics*) — pooling vs. heterogeneous panel estimation; establishes that heterogeneity matters for panel ML
- Ailawadi & Farris (2017) — FMCG brand performance heterogeneity
- **Recommendation**: frame as "panel heterogeneity diagnostic" and cite Pesaran & Smith. Avoid claiming it as a novel method.

---

### 4 — Weighted Distribution Threshold Effect

**What it adds**: Test whether `sales_units` vs `weighted_dist` relationship is non-linear (threshold: sales only respond above ~30% distribution coverage). A quantile-binned plot + Spearman vs Pearson delta would show this empirically from the data.

**Why it matters for ML**: `weighted_dist` is typically the strongest predictor in FMCG Nielsen data. If the relationship is threshold-shaped, the raw feature needs binning or a polynomial term — LightGBM handles this natively, Ridge does not.

**Literature grounding**: **Moderate — needs empirical derivation**
- Ataman, Mela & Van Heerde (2010, *Marketing Science*) — brand growth and distribution relationship in FMCG
- Reibstein & Farris (1995, *Marketing Science*) — distribution-sales relationship
- **Critical note**: the "0.3 threshold" is trade marketing practice, NOT in the literature. Do NOT assert it. Instead: derive the threshold empirically from the data (quantile bins) and cite Ataman et al. as motivation for checking non-linearity.
- **Check Zotero**: search `distribution` or `weighted distribution`

---

### 5 — Fourier / Spectral Analysis (Multi-Frequency Seasonality)

**What it adds**: Periodogram or STL decomposition with multiple seasonal periods. CSD brands may have both a summer peak (period ~6) and a Christmas peak (period ~12) — ACF alone can miss multi-frequency structure.

**Why it matters for ML**: If multi-frequency seasonality exists, a single `is_holiday_month` binary feature is insufficient. Would justify Fourier terms (sin/cos at multiple frequencies) as additional features.

**Literature grounding**: **Strong**
- Cleveland, Cleveland, McRae & Terpenning (1990, *Journal of Official Statistics*) — STL decomposition, canonical reference
- Box, Jenkins, Reinsel & Ljung (2015) *Time Series Analysis* — spectral methods
- Taylor & Letham (2018, *American Statistician*) — Prophet model, motivates multi-period seasonality in business time series
- **Check Zotero**: search `seasonality` or `STL`

---

### 6 — Train-Size Adequacy Curve (MIN_PERIODS Sensitivity)

**What it adds**: Plot retained brands vs MIN_PERIODS threshold (currently fixed at 40) as a sensitivity curve. Shows the empirical trade-off between data quality and brand coverage, making the 40-period choice defensible.

**Why it matters for ML**: The current 40-period justification ("high quality") is qualitative. A curve showing inflection points makes it quantitative.

**Literature grounding**: **Moderate**
- Cerqueira, Torgo & Mozetič (2020, *ECML-PKDD*) — evaluation protocols for time series forecasting; discusses minimum series length requirements
- Learning curve analysis: Mukherjee et al. (2003) — general ML framework
- **Recommendation**: frame as sensitivity analysis, cite Cerqueira et al. for the minimum-length rationale.

---

## Implementation Priority

For the thesis (proof-of-concept scope), recommend implementing in this order:

1. **#1 Walk-forward CV check** — required for any credible evaluation section
2. **#4 Weighted distribution threshold** — strongest ML modelling insight; derive empirically
3. **#5 Fourier/spectral** — if data shows multi-frequency pattern in Cell 8 decomposition
4. **#3 Per-tier distributions** — if heterogeneity analysis (Cell 9b) shows high CV spread
5. **#6 Train-size curve** — quick to implement, makes MIN_PERIODS defensible
6. **#2 Lagged scatter** — appendix only, not thesis chapter

---

## What NOT to claim without a citation

| Claim | Problem | Fix |
|-------|---------|-----|
| "Distribution threshold is ~0.3" | No academic source | Derive from data; cite Ataman et al. for motivation |
| "Window 4 is optimal (Nielsen calendar)" | Domain heuristic only | Already fixed in P0023 — now empirically derived |
| "Lag 8 captures bi-monthly cycles" | No evidence in literature or data | Already flagged in P0023 — include only if ACF significant |
| "40 periods is the quality threshold" | Qualitative only | Add sensitivity curve (#6) |

---

## Zotero Search Terms

Run against group library 6479832:

| Topic | Search terms |
|-------|-------------|
| Walk-forward CV | `hyndman`, `bergmeir`, `time series evaluation`, `cross-validation` |
| Seasonal decomposition | `STL`, `cleveland`, `seasonal decompose` |
| Distribution-sales | `ataman`, `weighted distribution`, `FMCG`, `reibstein` |
| Panel heterogeneity | `pesaran`, `panel`, `heterogeneous` |
| Spectral | `fourier`, `spectral`, `periodogram` |

## Zotero Search Results (queried 2026-06-30, library size: 28 papers)

**Result: 0 of the 6 key references are currently in the library.**

The library is currently focused on AI agents, LLM pipelines, and supply chain ML. None of the canonical time series / FMCG methodology papers are present.

Two incidental hits that ARE in the library (already used in EDA):
- `FPJSJGSM` — Kim (2013) *Restorative Dentistry & Endodontics* — skewness threshold (already cited in Cell 2)
- `NVXZ7V8Z` — Cain, Zhang & Yuan (2017) *Behavior Research Methods* — skewness/kurtosis measurement

### Papers that MUST be added to Zotero before using these improvements in the thesis

| Priority | Paper | Why needed |
|----------|-------|-----------|
| **Must** | Hyndman & Athanasopoulos (2021) *Forecasting: Principles and Practice* | Walk-forward CV (#1) |
| **Must** | Bergmeir & Benítez (2012) *Information Sciences* | Walk-forward CV validity (#1) |
| **Must** | Cleveland et al. (1990) *Journal of Official Statistics* | STL / spectral (#5) |
| **Must** | Ataman, Mela & Van Heerde (2010) *Marketing Science* | Distribution threshold (#4) |
| **Should** | Pesaran & Smith (1995) *Journal of Econometrics* | Panel heterogeneity (#3) |
| **Should** | Cerqueira, Torgo & Mozetič (2020) *ECML-PKDD* | Train-size adequacy (#6) |
| **Should** | Taylor & Letham (2018) *American Statistician* | Multi-frequency seasonality (#5) |
| **Optional** | Reibstein & Farris (1995) *Marketing Science* | Distribution-sales relationship (#4) |

**Action**: Use `/cite` skill to add these to Zotero before implementing the corresponding EDA improvements in the thesis.
