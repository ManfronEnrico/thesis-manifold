---
pid: P0023
created: 2026-06-30 12:38:00
updated: 2026-06-30 12:38:00
---

# P0023 — EDA Critique: Findings

## Source

- `thesis/data/_02_preprocessing/nielsen/CSD/pre_csd_1.5_eda.py` (~940 lines, 16 cells)
- Input: `step_1_aggregate.parquet` — CSD brand × month Nielsen panel data

---

## Structured Critique

### CRITICAL (P0 — Must fix before feature engineering proceeds)

---

#### C1 — Target Variable Is Never Defined

**What the EDA does**: Analyses `sales_units` as a distribution and time series.  
**What it doesn't do**: Never asks "what are we predicting, at what horizon, for which brands?"

**Why this matters for ML**:
- Lightweight models (LightGBM, Ridge) need a clearly defined Y. Is it:
  - `sales_units` at t+1 (1-month ahead)?
  - `log(sales_units)` at t+1?
  - % change month-over-month?
- The choice of Y determines which lags are valid, which features are legal (no leakage), and how to evaluate the model.
- Without defining the forecast horizon, the entire lag/rolling window analysis in Cells 10–12 may be wrong.

**Fix**: Add a dedicated cell that explicitly states:  
`Y = log1p(sales_units_{t+1})` (or whatever the thesis specifies), forecast horizon H=1 month, per brand. All subsequent feature engineering should be framed relative to this Y.

---

#### C2 — Train/Val/Test Split Has Data Leakage Risk

**What the EDA does** (Cell 13): Hardcodes `train_periods = 24`, `val_periods = 6`, computes split dates arithmetically from the earliest date.

**Problems**:
1. **Global split applied uniformly** — but brands may have different start dates. A brand that starts at period 10 gets only 14 months of training data, not 24.
2. **No temporal ordering check** — the code doesn't verify data is sorted before computing cutoffs.
3. **No buffer zone** — features like 13-period rolling windows require a warmup period before the first valid prediction. Without a buffer, the first 13 rows of each brand in the training set produce NaN features that silently corrupt training.
4. **The val/test boundary is not validated** — code computes dates arithmetically using modular arithmetic (`% 12`) which is correct but produces dates that may not exist in the data (e.g., if the data ends mid-year).
5. **Hardcoded 24/6 is not justified empirically** — why 24 months train? What's the minimum needed for stable feature computation given LAGS=(1,2,3,4,8,13) and ROLLING_WINDOWS=(4,13)?

**Fix**: 
- Check per-brand data availability before applying the global split.
- Add a warmup buffer of at least `max(LAGS + ROLLING_WINDOWS) = max(13, 13) = 13` periods before the first training observation used for prediction.
- Validate split dates against actual data range.

---

#### C3 — Stationarity Test Is Aggregated, Not Per-Brand

**What the EDA does** (Cell 4): Runs ADF on `df.groupby(['period_year','period_month'])['sales_units'].sum()` — the total CSD category sales.

**Why this is wrong for ML**:
- Models are trained per-brand (or with brand as a categorical feature). The stationarity of the total does not imply stationarity of individual brands.
- A brand entering/exiting distribution will show a structural break that's invisible in aggregated data.
- The log transform decision (`log_necessary = True/False`) is a single global flag applied to all brands — but some may be stationary raw, others may need differencing.

**Fix**:
- Run ADF per brand (at minimum for top 20 by volume).
- Report: % of brands stationary raw vs. after log vs. needing differencing.
- Use the per-brand result to decide feature construction strategy, not a single flag.

---

### HIGH PRIORITY (P1 — Fix before modelling)

---

#### H1 — Lag Analysis Is Done on One Brand Only (Cell 10)

**What the EDA does**: Computes lag correlations only for `top_brands[0]` — the single highest-volume brand.

**Why this matters**:
- FMCG CSD brands have very different sales profiles (national vs. private label vs. niche).
- Lag structure for Coca-Cola is likely not representative of a small regional brand.
- The recommendation `LAGS = (1, 2, 3, 4, 8, 13)` is derived from one brand but applied to all.

**Fix**:
- Compute lag correlations for all brands (or a stratified sample: top, mid, low volume).
- Report median + IQR of lag correlations across brands.
- Only include lags that are significant for ≥ 50% of brands.

---

#### H2 — ACF/PACF Plots Are Brand-Specific But Not Used to Validate Lags

**What the EDA does** (Cell 11): Plots ACF/PACF for top 5 brands. Correctly uses `plot_acf` / `plot_pacf`.

**Gap**: The visual output is not programmatically analysed. The recommendation `LAGS = (1,2,3,4,8,13)` was decided before Cell 11 ran (it's in Cell 10) and Cell 11 just "validates" it visually. This is circular.

**Fix**:
- Extract statistically significant lags from ACF/PACF (spikes outside the ±1.96/√n band) for each of the top brands.
- Use these to _derive_ the LAGS parameter, not retroactively validate it.
- Specifically: lag 8 is included but is likely not significant for most CSD brands (no clear bi-monthly business cycle). Lag 12 (annual) is a more natural candidate that's missing.

---

#### H3 — Cross-Brand Heterogeneity Not Analysed

**What the EDA does**: Looks at top 5 brands by volume. All other analysis is aggregate.

**Why this is critical for lightweight ML**:
- If you train a single model across all brands (panel model), you need to know whether the relationship between features and sales is consistent across brands.
- If the heterogeneity is high, a single model will underfit most brands.
- Lightweight models handle this via brand fixed effects / embeddings — but the EDA should quantify whether this is needed.

**What's missing**:
- Coefficient of variation of sales across brands
- Whether seasonal patterns differ by brand (some brands may peak in winter, others in summer)
- Distribution of promo intensity across brands (not just aggregate)

---

#### H4 — Zero-Sales Handling Is Not Analysed

**What the EDA does**: Cell 5 counts brands with `sales_units > 0` per period. That's it.

**Why this matters for ML**:
- Zero sales periods for a brand could mean: (a) brand not in distribution, (b) data gap, (c) genuine zero sales.
- These cases require different feature engineering (e.g., a distribution indicator feature).
- Rolling means computed over zeros will underestimate true sales trend when a brand relaunches.
- The lag correlation in Cell 10 uses `fillna(0)` for zeros — this artificially deflates autocorrelation.

**What's missing**:
- Distribution of zero-sales periods per brand
- Whether zeros cluster (brand entry/exit) or are scattered (data gaps)
- Decision rule: impute zeros? Exclude them from rolling calculations? Use a missingness indicator?

---

#### H5 — Rolling Window Rationale Is Business Logic, Not Data-Driven (Cell 12)

**What the EDA does**: Justifies windows 4 and 13 based on "Nielsen 4-4-5 calendar" and "quarterly cycles".

**Why this is weak for a thesis**:
- A thesis needs empirical justification. The Nielsen calendar argument is a domain heuristic, not a statistical finding.
- The EDA never tests whether a 4-period rolling mean is more predictive than a 3-period or 6-period mean.
- Window 8 is dismissed as "redundant" without evidence.

**Fix**:
- Compute rolling mean with windows {2, 3, 4, 6, 8, 12, 13} for a sample of brands.
- Correlate each rolling feature with t+1 sales.
- Pick the windows with highest predictive correlation and lowest cross-correlation (to avoid redundancy).

---

### MEDIUM PRIORITY (P2 — Improve before thesis submission)

---

#### M1 — Skewness Threshold Logic Has a Bug (Cell 2)

**Code issue**:
```python
if skewness > 2:
    interp = "Highly right-skewed..."
elif skewness > 0.5:
    interp = "Right-skewed..."
elif skewness < -0.5:
    interp = "Left-skewed..."
elif skewness < -2:    # ← DEAD CODE: unreachable
    interp = "Highly left-skewed..."
```
The `skewness < -2` branch is never reached because `skewness < -0.5` catches it first.

**Fix**: Reorder conditions:
```python
if skewness > 2:    ...
elif skewness > 0.5: ...
elif skewness < -2:  ...   # check extreme first
elif skewness < -0.5: ...
else: ...
```

---

#### M2 — Promo Intensity Metric Is Flawed (Cell 14)

**Code**: `df['promo_intensity'] = df['promo_units'] / (df['sales_units'] + 1)`

**Problems**:
- Adding 1 to the denominator (`+1`) avoids division by zero but introduces systematic downward bias for low-sales brands (if `sales_units = 0`, intensity = `promo_units / 1`, which overestimates intensity).
- `promo_units` in Nielsen data typically refers to units sold on promotion — it's already a subset of `sales_units`, so values > 1.0 indicate a data problem.
- The distribution histogram shows whether this is the case but the code doesn't assert `promo_intensity <= 1.0`.

**Fix**:
- Use `promo_intensity = promo_units / sales_units.clip(lower=1)` (clip, not add 1).
- Assert `0 <= promo_intensity <= 1.0` for all rows where `sales_units > 0`.
- Separate analysis for zero-sales rows.

---

#### M3 — Seasonal Decomposition Uses Additive Model Without Justification (Cell 8)

**Code**: `seasonal_decompose(ts_monthly, model='additive', period=12)`

**Problem**: For FMCG sales data:
- Seasonal amplitude typically _scales_ with the trend (larger absolute swings in peak months as volume grows) → multiplicative model is more appropriate.
- The EDA never compares additive vs. multiplicative decomposition.
- An incorrect additive model will understate seasonal amplitude in high-volume periods.

**Fix**:
- Run both `model='additive'` and `model='multiplicative'`.
- Compare residual variance: lower residual variance → better model.
- Or use STL decomposition (more robust) via `statsmodels.tsa.seasonal.STL`.

---

#### M4 — Correlation Heatmap Uses Pearson Only (Cell 15)

**Problem**: `df[corr_cols].corr()` uses Pearson, which assumes linearity.

**FMCG reality**:
- `sales_units` vs `weighted_dist` is likely non-linear (distribution threshold effects).
- `sales_units` vs `promo_units` may have a threshold effect (small promos do nothing).

**Fix**: Add Spearman rank correlation alongside Pearson. Flag pairs where Pearson ≠ Spearman (non-linear relationship).

---

#### M5 — No Distribution Shift / Concept Drift Check

**What's missing**: No analysis of whether the feature-to-sales relationship is stable across the training window.

**Why this matters**:
- COVID-19 likely caused a structural break in CSD sales (lockdowns, on-trade closure).
- If the data spans 2018–2024, the pre/post-COVID periods are effectively different datasets.
- Training a lightweight model on pooled pre/post data without accounting for the break will produce biased coefficients.

**Fix**:
- Split the time series at the likely break point (e.g., 2020-03).
- Compare mean, variance, and autocorrelation structure pre vs. post.
- Report whether a structural break is present and flag it as a modelling decision.

---

## Recommendations Summary

| Priority | ID | Issue | Action |
|----------|----|-------|--------|
| P0 | C1 | Target variable never defined | Add Y-definition cell; validate horizon |
| P0 | C2 | Data leakage risk in split | Per-brand split validation + warmup buffer |
| P0 | C3 | ADF on aggregate only | Run ADF per brand; report % needing transforms |
| P1 | H1 | Lag analysis single brand | Extend to all brands; use median significance |
| P1 | H2 | ACF/PACF not used to derive lags | Extract significant lags programmatically |
| P1 | H3 | Cross-brand heterogeneity ignored | CV analysis; seasonal pattern by brand |
| P1 | H4 | Zero-sales not analysed | Characterise zeros; decide imputation strategy |
| P1 | H5 | Rolling windows business-justified only | Empirical correlation test across window sizes |
| P2 | M1 | Skewness branch dead code | Fix elif order |
| P2 | M2 | Promo intensity metric bias | Use clip(lower=1) not +1 |
| P2 | M3 | Additive decomposition unjustified | Compare additive vs multiplicative |
| P2 | M4 | Pearson correlation only | Add Spearman; flag non-linear pairs |
| P2 | M5 | No concept drift check | Check pre/post structural break |

---

## Phase 5 — Further Improvements (Post-P0023)

See full assessment: `thesis/data/_02_preprocessing/nielsen/docs/eda-improvement-candidates.md`

| # | Improvement | Literature | Add to Zotero first? |
|---|-------------|-----------|----------------------|
| 1 | Walk-forward CV feasibility check | Hyndman 2021, Bergmeir 2012 | Yes |
| 2 | Lagged scatter plots | Tukey 1977 (weak) | No — appendix only |
| 3 | Per-volume-tier distribution analysis | Pesaran & Smith 1995 | Yes |
| 4 | Weighted distribution threshold (empirical) | Ataman et al. 2010 | Yes |
| 5 | Fourier / spectral multi-frequency analysis | Cleveland 1990, Taylor 2018 | Yes |
| 6 | Train-size adequacy curve (MIN_PERIODS sensitivity) | Cerqueira et al. 2020 | Yes |

**Zotero status (2026-06-30)**: None of these 6 canonical references are in the library. Must be added via `/cite` before thesis chapter justification can be written.

---

## What the EDA Does Well (Strengths)

- ACF/PACF analysis (Cell 11) is methodologically correct and multi-brand.
- Brand stability threshold analysis (Cell 5) is well-reasoned for thesis scope.
- JSON findings export (Cell 16) is good for reproducibility.
- Seasonal decomposition (Cell 8) is visually informative even if model choice is unvalidated.
- Modular cell structure makes it easy to extend.
- The visualisation philosophy is consistent and thesis-ready.
