# SRQ1 Verification Report — Code & Data Quality Audit
> Conducted: 2026-04-14
> Scope: Enrico's Phase 1 (Data Assessment) + Phase 4 (SRQ1 Model Selection Benchmark)
> Reviewer: Brian Rohde

---

## Executive Summary

**Code quality**: ✅ **STRONG** — preprocessing and model training are production-ready  
**Data assessment**: ⚠️ **ADEQUATE BUT INCOMPLETE** — suitable for SRQ1 but lacks depth for thesis discussion  
**Model selection narrative**: 🔴 **MISLEADING** — validation metrics reported as test metrics; inflates apparent performance  

**Recommendation**: Use Enrico's code and test results as-is, but update CLAUDE.md and thesis sections to report test metrics (45% MAPE), not validation metrics (22% MAPE).

---

## 1. Code Quality Assessment

### ✅ Preprocessing Pipeline (`preprocessing.py`)

**Strengths:**
- Well-structured: Clear separation of concerns (pull → calendar → filter → engineer → split → save)
- Proper NULL handling: Forward-fills distribution metrics, clips negatives (captures returns/corrections)
- Memory-efficient: 7.9 MB peak on 77 brands, 3,234 rows — excellent for 8GB constraint
- Smart feature engineering:
  - Lags at 1,2,3,4,8,13 periods — captures weekly/monthly seasonality without overfitting
  - Lag-13 crucial for year-over-year patterns (monthly data)
  - Rolling stats with look-ahead prevention (shifts before windowing)
  - Holiday month encoding acknowledges Danish retail seasonality (Jan, Apr, Jun, Oct, Dec)
  - Log-transformed target (sales_units → log_sales_units) for tree-based models
- Reproducible: Train/val/test boundaries locked in `split_dates.json`
- Data quality: No NULLs in Nielsen dimension tables; all 77 brands have 42 complete periods

**Weaknesses:**
- No stationarity test (ADF, KPSS) — assumes features are suitable for tree models without verification
- No cross-correlation analysis with external signals (Indeks Danmark prices, macro factors)
- Holiday month hardcoded (not domain-validated with retail analyst)

**Verdict**: ✅ **Code is production-ready.**

---

### ✅ Model Training Code (`global_model_v2.py`)

**Strengths:**
- Walk-forward cross-validation correctly implemented:
  - Avoids look-ahead bias (CV cutoff respects temporal ordering)
  - Fold size = max(n_dates/6, 3) — reasonable for 29 training periods
  - Evaluates on multiple folds, reports mean CV error
- Proper train/val/test separation:
  - Trains on train+val, evaluates on test
  - No data leakage visible
- Handles predictions safely:
  - Clips predictions to [0, 3×train_max] to avoid wild extrapolation
  - Converts log predictions back to natural units with exp-1 transform
- Hyperparameter grid is sensible:
  - Tests 2 depth levels (5,7), 2 learning rates (0.02, 0.05)
  - Subsample/colsample=0.8 reduces overfitting
  - min_child_samples=[5,10] prevents 1-sample leaves

**Weaknesses:**
- Tweedie loss tested only on validation, never on test set
- Per-brand best-of routing (MSE vs Tweedie) is incomplete — line 272 comment says "needs val-based routing" but uses simple 50/50 average instead
- No ablation study showing impact of new features (distribution_momentum, yoy_growth, seasonal_index) vs baseline features
- Feature importance uses MSE model only, not Tweedie

**Verdict**: ✅ **Model training is sound, but some experiments are incomplete.**

---

## 2. Data Assessment

### ✅ What Is Verified

| Aspect | Finding | Evidence |
|--------|---------|----------|
| Database connectivity | Live, returning data | `nielsen_assessment.md` confirms all 4 views accessible |
| Schema integrity | 28 markets, 42 periods, 2,057 products | Period range: Oct 2022 – Mar 2026 (verified) |
| Primary market (DVH EXCL. HD) | 77 brands with ≥30 non-zero periods | `preprocessing_report.md`: 77 brands, 42 periods, 3,234 rows |
| Data quality | No NULLs in dimensions | Confirmed in `nielsen_assessment.md` |
| Top brands | Sensible (HARBOE, COCA-COLA, PEPSI, FAXE KONDI) | Match Danish CSD market share expectations |
| Split boundaries | Reasonable train/val/test | 29/6/7 periods, locked and reproducible |

### ⚠️ What Is Missing

| Gap | Impact | Recommendation |
|-----|--------|-----------------|
| No autocorrelation (ACF) analysis | Seasonal patterns not quantified | Add ACF plots for 3 top brands in Ch.4 (Data Assessment) |
| No stationarity testing | Unknown if features need differencing | KPSS test on log_sales_units for Ch.4 |
| Intermittent demand distribution | Claim "0 of 77 >60% zero" but no detail | Show histogram of zero %s per brand in Ch.4 — some may have 40%+ zeros |
| No outlier analysis | Potential data quality issues hidden | Check for brands with sudden drops (rebrands, exits) |
| Indeks Danmark not integrated | Secondary data exists but unused | Acceptable for SRQ1 (univariate) — note as SRQ3 future work |

**Verdict**: ⚠️ **Data assessment is adequate for SRQ1 but lacks academic rigor for the thesis. Recommend adding 2–3 figures in Ch.4 (ACF, zero distribution, outliers).**

---

## 3. Model Selection — Validation vs. Test Discrepancy

### 🔴 Red Flag: Inflated Validation Metrics

**What CLAUDE.md currently claims:**
```
Global LightGBM v2 (Tweedie) — 22.5% median MAPE
```

**What test set shows:**
```
LightGBM test median MAPE: 46.7%
XGBoost test median MAPE: 45.5%
```

**The discrepancy:**
| Evaluation | LightGBM | XGBoost | Source |
|---|---|---|---|
| Validation | 26.2% (MSE) / 23.8% (Tweedie) | 32.8% | `benchmark_summary_v2.md` |
| Test | 46.7% | 45.5% | `test_summary.md` |
| **Delta** | **+20.5pp** | **+12.7pp** | — |

### Why This Happened

1. **Two separate evaluation scripts**:
   - `global_model_v2.py` trains on train set, evaluates on validation set → reports 22–26% MAPE
   - `test_evaluation.py` trains on train+val, evaluates on held-out test → reports 45–47% MAPE
   - Both are correct scripts, but the narrative wasn't harmonized

2. **Tweedie was only tested on validation**:
   - `global_model_v2.py` compares Tweedie vs MSE on validation (23.8% vs 26.2%)
   - `test_evaluation.py` doesn't include Tweedie — only tests LightGBM, XGBoost, Ridge, Ensemble, SeasonalNaive
   - Therefore, **no test result for Tweedie exists**

3. **CLAUDE.md was updated with v2 validation numbers but not re-checked against test**:
   - CLAUDE.md line: "Global LightGBM v2 (Tweedie) — 22.5% median MAPE"
   - This is the **GlobalLGB_v2_Avg** (50/50 ensemble) validation MAPE from `global_v2_summary.md` line 12
   - But the test set shows 49.8% MAPE for the same ensemble

### Performance Degradation Analysis

The **12–20pp validation→test gap** is substantial but partly explainable:

| Factor | Evidence |
|--------|----------|
| **Short training window** | Only 29 training periods (~2.4 years) for monthly data — typical ML needs ≥36 |
| **Small test set** | Only 7 test periods (~7 months) — any outlier month inflates MAPE |
| **Seasonality not fully captured** | Training covers Oct 2022 – Feb 2025; test is Sep 2025 – Mar 2026. Seasonal patterns may have shifted. |
| **Intermittent demand** | While no brand has >60% zeros, many may have 30–40% zeros, causing prediction variance |

**Verdict**: The gap is **suspicious but not disqualifying**. Recommend:
1. Accept test MAPE as the ground truth for the thesis
2. Document the validation→test gap in Ch.3 (Methodology)
3. Explain short training window as a constraint of the Nielsen dataset

---

## 4. Feature Engineering — Unverified Gains

**Claim** (from `global_v2_summary.md`):
> "New features (distribution_momentum, yoy_growth, seasonal_index) add real predictive value"

**Evidence for the claim:**
- v1 baseline: 28.2% median MAPE (validation)
- v2 MSE: 26.2% median MAPE (validation)
- Improvement: ~2pp

**Problem:**
- No ablation study showing which new features contribute
- Improvement could come from hyperparameter tuning, not features
- No test set comparison between v1 and v2

**Verification needed for thesis**:
If citing these features as novel contributions, run ablation on validation set:
1. Train v2 without distribution_momentum → measure MAPE drop
2. Train v2 without yoy_growth → measure MAPE drop
3. Train v2 without seasonal_index → measure MAPE drop

**Recommendation**: For SRQ1, report the features as "engineered for interpretability" rather than "added real predictive value" until ablation is done.

---

## 5. Test Set Evaluation — Strengths

### ✅ Proper Methodology

**What `test_evaluation.py` does correctly:**
1. Locks train/val boundaries (29+6 = 35 periods)
2. Trains 5 models on full train+val set
3. Evaluates on held-out test set (7 periods)
4. Computes per-brand MAPE, RMSE, RAM usage
5. Reports median (robust to outliers), P25, P75

**Results are actionable:**
- XGBoost slightly better than LightGBM on test (45.5% vs 46.7%)
- Both substantially outperform SeasonalNaive (66.9%)
- ML adds ~20pp absolute improvement over baseline
- No single model dominates: XGBoost wins 21/77 brands, Ridge 20/77, LightGBM 18/77

**Verdict**: ✅ **Test evaluation is rigorous. Use these numbers in the thesis.**

---

## 6. Synthesis Module Benchmark (SRQ2) — Implications

When Enrico or a synthesis agent builds the SRQ2 module (combining multiple forecasts with contextual signals), benchmark it against:

**Baseline** (from SRQ1):
- XGBoost: 45.5% median MAPE
- Seasonal Naive: 66.9% median MAPE

**Not against** (would be unfair):
- Validation metrics (26% — too easy to beat)
- Global v2 Tweedie (untested on test set)

**Success criterion**: SRQ2 synthesis module achieves <43% median MAPE on the same test set, demonstrating that multi-agent coordination adds value over single-model baseline.

---

## 7. Actionable Recommendations

### For Thesis Writing (Ch.3 Methodology, Ch.4 Data Assessment)

1. **Ch.3 Methodology**:
   - Document 29-period training window as a constraint (explain why)
   - Explain validation→test degradation (not a failure, expected with short windows)
   - Note: Only 7 test periods = high variance in MAPE

2. **Ch.4 Data Assessment**:
   - Add ACF plot (top 3 brands) to show seasonal lag-13 dominance
   - Add histogram of zero % per brand (verify "0 of 77 >60% zero" claim)
   - Acknowledge Indeks Danmark as future external signal (SRQ3)

3. **Ch.5 Framework Design** (SRQ1 section):
   - Report test metrics: "XGBoost 45.5%, LightGBM 46.7%, SeasonalNaive 66.9% median MAPE"
   - Do NOT report validation metrics (22–26%)
   - Do NOT cite Tweedie loss as "best model" — it's untested on test set

4. **Update CLAUDE.md**:
   - Change: "Global LightGBM v2 (Tweedie) — 22.5% median MAPE"
   - To: "Global models on test set: XGBoost 45.5%, LightGBM 46.7% median MAPE"

### For Code / Future Phases

1. **Test Tweedie on test set** (if claiming it as SRQ1 contribution):
   ```python
   # Re-run test_evaluation.py with Tweedie objective
   # Report Tweedie test MAPE alongside MSE
   ```

2. **Run feature ablation study** (if claiming features as novel):
   - Remove distribution_momentum → measure MAPE impact
   - Remove yoy_growth → measure MAPE impact
   - Remove seasonal_index → measure MAPE impact

3. **Document per-brand model choice**:
   - Use val-based routing: For each brand, pick MSE vs Tweedie based on val MAPE
   - Evaluate ensemble on test (current 49.8% is worse than individual models)

---

## 8. Conclusion

| Dimension | Assessment | Action |
|-----------|-----------|--------|
| **Code** | ✅ Production-ready | Use as-is |
| **Data** | ⚠️ Adequate, lacks depth | Add ACF/zero-distribution plots for thesis |
| **Model selection** | ⚠️ Sound methodology, inflated narrative | Harmonize CLAUDE.md to report test metrics |
| **Feature engineering** | 🔴 Unverified | Run ablation before claiming novelty |
| **Test evaluation** | ✅ Rigorous | Use as ground truth for SRQ2 baseline |

**Overall**: Enrico's work is **solid engineering with a narrative problem**. The code and methodology are sound; the issue is reporting validation numbers as if they were test numbers. Fix the CLAUDE.md and thesis prose, and the work becomes trustworthy.

---

## Appendix: Key Files

- `ai_research_framework/data/preprocessing.py` — 315 lines, clean and correct
- `ai_research_framework/agents/global_model_v2.py` — 356 lines, tests 3 models + ensemble on validation
- `ai_research_framework/agents/test_evaluation.py` — 429 lines, evaluates 5 models on held-out test
- `results/phase1/global_v2_summary.md` — validation results (22–26% MAPE)
- `results/phase1/test_summary.md` — test results (45–67% MAPE)
- `results/phase1/preprocessing_report.md` — data quality summary
