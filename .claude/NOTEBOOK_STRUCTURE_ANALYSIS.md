# Notebook Structure Analysis — Step-by-Step Breakdown

**Scope**: Analyze each notebook's sections, dependencies, and outputs  
**Date**: 2026-04-27

---

## Overview: 10 Notebooks, 3 Distinct Purposes

| **Phase** | **Notebook** | **Purpose** | **Size** | **Status** |
|-----------|--------------|-----------|---------|-----------|
| 2 | thesis_notebook_CSD.ipynb | Train XGBoost/LightGBM for CSD category | Large | ✅ Complete |
| 2 | thesis_notebook_danskvand.ipynb | Train models for danskvand | Large | ✅ Complete |
| 2 | thesis_notebook_energidrikke.ipynb | Train models for energidrikke | Large | ✅ Complete |
| 2 | thesis_notebook_rtd.ipynb | Train models for RTD (V2 regularized) | Large | ✅ Complete |
| 2 | thesis_notebook_totalbeer.ipynb | Train models for totalbeer | Large | ✅ Complete |
| 2 | thesis_notebook_pooled_4.ipynb | Pooled model (4 categories) | Large | ✅ Complete |
| 2 | thesis_notebook_pooled_5.ipynb | Pooled model (all 5 categories) | Large | ✅ Complete |
| 2 | thesis_notebook_final_comparison.ipynb | Aggregate metrics across all 7 models | ~1k tokens | ✅ Complete |
| 3 | thesis_agentic_notebook.ipynb | Multi-category registry + forecasting agent | ~2929 tokens | ✅ Active |
| 5 | thesis_notebook_AB_test.ipynb | 4-tier LLM eval (L0/L1/L2/L3) v5 prompts | ~31k tokens | ⏳ Awaiting final run |

---

## Phase 2: ML Training Notebooks (8 notebooks)

### Common Structure (all training notebooks follow same pattern)

```
1. Setup (§0)
   - Find PROJECT_ROOT via CLAUDE.md
   - Import libraries (sklearn, xgboost, lightgbm, optuna, numpy, pandas)
   - Set random seeds (SEED=42)
   
2. Paths (§0.2)
   - OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_{category}"
   - FIGURE_DIR = OUTPUT_DIR / "figures"
   - SRQ1_DATA = PROJECT_ROOT / "thesis" / "data" / "nielsen" / ...
   
3. Load raw data (§1)
   - Read Nielsen sales + feature matrix
   - Define: brand, channel, date, category, sales_units
   - Time split: train ≤ Feb 2025, val Mar-Aug 2025, test Sep 2025+
   
4. Walk-forward CV setup (§2)
   - 5 folds, 3-month horizon, expanding window
   - Report: per-fold MAPE, per-brand MAPE, per-channel MAPE
   
5. Baseline models (§3)
   - Ridge, LinearRegression, DummyRegressor
   
6. Hyperparameter tuning (§4)
   - Optuna: 50 trials for XGBoost
   - Optuna: 50 trials for LightGBM
   - Evaluate on val set
   
7. Training + test evaluation (§5)
   - Train on full train+val
   - Predict on test
   - Compute: MAPE, MAE, RMSE, sMAPE
   - Save per-brand + per-channel metrics
   
8. Feature importance (§6)
   - Permutation importance or SHAP
   
9. Save artifacts (§7)
   - model_xgboost.pkl → OUTPUT_DIR / "pipelines"
   - model_lightgbm.pkl → OUTPUT_DIR / "pipelines"
   - pipe_tree.pkl (preprocessing pipeline)
   - feature_matrix_split.parquet (for agentic notebook)
   - metrics.csv (MAPE by brand, channel, etc.)
   
10. Visualizations (§8)
    - Boxplot: MAPE across brands
    - Time series: actual vs predicted
    - Feature importance: top 20
```

### Key Finding: All save to parallel structure
```
docs/thesis/analysis/outputs/                    (CSD)
docs/thesis/analysis/outputs_danskvand/          (danskvand)
docs/thesis/analysis/outputs_energidrikke/       (energidrikke)
docs/thesis/analysis/outputs_rtd_v2/             (RTD, V2)
docs/thesis/analysis/outputs_totalbeer/          (totalbeer)
docs/thesis/analysis/outputs_pooled_4/           (pooled_4)
docs/thesis/analysis/outputs_pooled_5/           (pooled_5)
```

**After migration, this becomes**:
```
thesis/analysis/outputs/
├── csd/
│   ├── pipelines/
│   │   ├── model_xgboost.pkl
│   │   ├── model_lightgbm.pkl
│   │   └── pipe_tree.pkl
│   ├── feature_matrix_split.parquet
│   ├── metrics.csv
│   └── figures/
├── danskvand/
│   └── [same structure]
├── energidrikke/
├── rtd_v2/
├── totalbeer/
├── pooled_4/
└── pooled_5/
```

### Data flow: Training notebook outputs → Agentic notebook inputs

**Training notebook saves**:
```python
# In each training notebook (§7 Save artifacts)
(OUTPUT_DIR / "pipelines" / "model_xgboost.pkl").write_bytes(...)
(OUTPUT_DIR / "pipelines" / "pipe_tree.pkl").write_bytes(...)
(OUTPUT_DIR / "feature_matrix_split.parquet").write_text(...)
```

**Agentic notebook loads**:
```python
# In thesis_agentic_notebook.ipynb §0.5
CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs",
        "fm_filename": "feature_matrix_split.parquet",
    },
    ...
}

# §2.5 load_model_for_category()
with open(out_dir / "pipelines" / f"model_{chosen}.pkl", "rb") as f:
    model = pickle.load(f)
```

**After migration**: Paths must align exactly, or model loading will fail.

---

## Phase 3: Agentic Registry Notebook

### `thesis_agentic_notebook.ipynb` Structure

**Size**: ~2929 tokens (manageable)

**Sections**:
```
§0: Setup
  - Find PROJECT_ROOT
  - Load .env (OpenAI + Anthropic keys)
  
§0.5: CATEGORY_MODELS registry (CRITICAL)
  - Dict mapping: category → (outputs_dir, primary_model, MAPE metrics, fm_filename)
  - 5 specialized models (CSD, danskvand, energidrikke, RTD, totalbeer)
  - 2 pooled models (pooled_4, pooled_5)
  - Functions:
    - load_model_for_category(category, model_type) → {model, pipe_tree, fm, ...}
    - predict_for_category(brand, channel, date, category) → {prediction, actual, error, ...}
  
§1: Data loading
  - Load Nielsen sales (raw)
  - Load Indeks features
  - Merge on date + brand + channel
  
§2: Feature engineering agent
  - Call data_assessment_agent (from thesis_agents/)
  - Engineer: causal lags, rolling stats, calendar, promo intensity
  
§2.5: Forecasting agent (multi-category)
  - Takes brand + channel + date → routes to load_model_for_category()
  - Calls LLM with: historical data + forecasted sales from per-category model
  - Returns: LLM forecast + confidence
  
§3+: Visualization and export
  - Plot: actual vs forecasted
  - Export: CSV with all predictions
```

### Key Issue: Registry is hardcoded to OLD paths

**Current**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"

CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs",  # → docs/thesis/analysis/outputs
        ...
    },
    "danskvand": {
        "outputs_dir": ANALYSIS_DIR / "outputs_danskvand",  # → docs/thesis/analysis/outputs_danskvand
        ...
    },
    ...
}
```

**After migration**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"

CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "csd",  # → thesis/analysis/outputs/csd
        ...
    },
    "danskvand": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "danskvand",  # → thesis/analysis/outputs/danskvand
        ...
    },
    ...
}
```

### Backwards compatibility question

If the old pickles are still in `docs/thesis/analysis/outputs*`, should we:
1. **Keep both paths** during transition (load from old if new doesn't exist)?
2. **Copy the pickles** to new location?
3. **Force regeneration** (cost: 2-3 hours local compute, no cloud $)?

**Recommendation**: Option 1 (fallback) + Option 2 (migrate pickles) = safest. Then Option 3 later if needed.

---

## Phase 5: Evaluation Notebook (CRITICAL PATH)

### `thesis_notebook_AB_test.ipynb` Structure

**Size**: ~31k tokens (very large, multiple sections)  
**Status**: Ready to run, waiting for final approval  
**Cost to run**: ~$4 + 35 min  
**Importance**: Produces Chapter 7 thesis results

**Sections**:
```
§0: Setup & paths
  - Find PROJECT_ROOT
  - ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"  ← MUST UPDATE
  - Load .env
  
§1: Load evaluation prompts
  - Read CSV: outputs_ab_test/prompts.csv  ← MUST MOVE
  - 50 final prompts, v5 (fixes brand-routing, channel mapping, fallback logic)
  
§2: Load models
  - Call load_model_for_category() for each of: L2 (untuned), L3 (tuned)
  - ← Will fail if paths don't match!
  
§3: Run 4-tier eval (MAIN LOOP)
  - For each of 50 prompts, call:
    - L0: gpt-4o-mini (no tools, LLM-only)
    - L1: gpt-4o-mini + raw data tool (no ML)
    - L2: gpt-4o-mini + untuned ML (LightGBM n_est=200, no Optuna)
    - L3: gpt-4o-mini + tuned ML (XGBoost/LGB Optuna-50 tuned)
  - Each prompt → 4 LLM calls = 200 calls total (~$1.50)
  
§4: Quantitative metrics (FREE)
  - MAPE, MAE, RMSE, sMAPE
  - Hallucination detection
  - Latency tracking
  - Cost tracking
  
§5: LLM-as-judge (EXPENSIVE)
  - 50 prompts × 4 systems × 5 metrics = 1000 Claude calls (~$2)
  - Metrics: groundedness, actionability, specificity, coherence, business_relevance
  - Each call: send L0/L1/L2/L3 outputs + rubric, get score 1-5
  
§6: Pairwise comparison (CHEAPER)
  - 6 pairwise comparisons (L0v1, L0v2, L0v3, L1v2, L1v3, L2v3)
  - 50 prompts × 6 pairs = 300 Claude calls (~$0.50)
  
§7: Aggregate metrics & stats
  - MAPE filtered (drop outliers)
  - Hallucination rate
  - Win rates (pairwise)
  - Composite quality score
  
§8: Figures & tables (FREE)
  - Boxplot: sMAPE by tier
  - Heatmap: judge metrics
  - Radar chart: 4-tier comparison
  - Win-rate matrix
  - Cost vs quality scatter
  
§9: Ready-to-paste markdown
  - Tables for Chapter 7
```

### Critical data flow

```
thesis_notebook_AB_test.ipynb
├── Loads: outputs_ab_test/prompts.csv (50 prompts v5)
├── Loads: Category models via load_model_for_category()
├── Calls: OpenAI API (L0/L1 via gpt-4o-mini)
├── Calls: Anthropic API (judge, pairwise)
└── Outputs:
    ├── outputs_ab_test/ab_raw_outputs.csv (all recommendations)
    ├── outputs_ab_test/ab_metrics.csv (per-query metrics)
    ├── outputs_ab_test/ab_summary.csv (L0 v L1 v L2 v L3 aggregates)
    ├── figures_ab_test/*.png (5 figures)
    └── Markdown table (ready for Chapter 7)
```

### Path migration impact

**MUST UPDATE** (will break if not):
```diff
- prompts_path = ANALYSIS_DIR / "outputs_ab_test" / "prompts.csv"
+ prompts_path = ANALYSIS_DIR / "prompts" / "prompts_v5_final.csv"

- OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_ab_test"
+ OUTPUT_DIR = ANALYSIS_DIR / "outputs" / "ab_test_v5"
```

**MUST VERIFY**:
```python
# In load_model_for_category() call (from agentic notebook import or inline)
# If registry paths are wrong, this will fail before spending $4
```

---

## Phase 5 Prompt Versions: What Changed?

From `MESSAGE_TO_BRIAN.md` § Phase 5:

| **Version** | **Change** | **Result** |
|-----------|-----------|----------|
| v1 | Base prompt (4k tokens) | MAPE 27%, hallucination 0% |
| v2 | +actionability layer (10k tokens) | MAPE ↓ (worse), actionability flat → ROLLED BACK |
| v3 | Category hint in prompt ("MORENA (totalbeer brand)") | Helps routing, but discovers bugs |
| v4 | Permissive brand mapping + 18 valid channels | Fixes brand/channel confound |
| v5 | v4 + fallback channel logic + strict JSON schema + max_tokens=6000 | **FINAL, READY** |

**v5 prompt changes** (from MESSAGE_TO_BRIAN.md line 82):
```
- Permissive brand mapping ("examples non-exhaustive")
- Explicit 18-channel list
- Fallback logic: try 2 alternates before abstaining
- Strict JSON schema: predicted_sales_units MUST be scalar (never dict/list)
- max_tokens=6000
- Up to 5 tool calls per multi-brand archetypes
```

**Status**: All fixes in place, ready to run. No known issues.

---

## Notebook Call Graph (Dependencies)

```
thesis_notebook_CSD.ipynb (and parallel: danskvand, energidrikke, rtd, totalbeer, pooled_4, pooled_5)
    ↓ (saves pickles + feature matrices)
thesis_agentic_notebook.ipynb (loads via load_model_for_category())
    ↓ (exports CSV with forecasts)
thesis_notebook_final_comparison.ipynb (aggregates metrics across all 7)
    ↓ (reads outputs from each + compares)
thesis_notebook_AB_test.ipynb (uses load_model_for_category() for L2 + L3 tier)
    ↓ (final eval, produces Chapter 7 results)
```

---

## What Each Notebook Does (Operational View)

### For Brian to RUN (in order):

1. **Regenerate training** (optional, if you want latest):
   ```bash
   jupyter notebook thesis/analysis/notebooks/02_ml_training/specialized_CSD.ipynb
   # ... run through to completion
   # Repeat for each: danskvand, energidrikke, rtd, totalbeer, pooled_4, pooled_5
   # Time: ~2-3 hours, all local, no cloud cost
   # Output: pickles + metrics
   ```

2. **Run agentic notebook** (optional, just to test):
   ```bash
   jupyter notebook thesis/analysis/notebooks/03_agentic_integration/registry_and_forecasting.ipynb
   # Run through to completion
   # Time: ~5 min
   # Output: CSV with forecast + LLM confidence
   ```

3. **Run AB test notebook** (CRITICAL for thesis):
   ```bash
   jupyter notebook thesis/analysis/notebooks/05_evaluation/4tier_ab_test_final.ipynb
   # Run §0-1 (setup, load prompts)
   # Review CATEGORY_MODELS registry print
   # Review v5 prompt (§1)
   # Then run §3-8 (MAIN LOOP)
   # Time: 35 min + $4
   # Output: Chapter 7 metrics + figures
   ```

---

## Summary: What to Watch For

| **Notebook** | **Risk** | **Mitigation** |
|-------------|----------|---------------|
| All training (8) | Pickle paths don't match registry | Update OUTPUT_DIR path before running |
| Agentic | load_model_for_category() fails | Verify registry outputs_dir matches actual pickle location |
| AB_test | Prompts CSV not found | Move prompts.csv to thesis/analysis/prompts/ |
| AB_test | $4 wasted if model loading fails | Test load_model_for_category() in §0.5 before main loop |
| AB_test | v5 prompt not applied | Verify prompts.csv is loaded, not hardcoded v3 |

---

## Next: Detailed Cell-by-Cell Analysis?

Ready to dive into:
1. **Agentic notebook registry** (§0.5 functions)?
2. **AB test eval loop** (§3-8 metric calculations)?
3. **Training notebook v5 prompts** (where exactly they're used)?

Or proceed directly to **migration execution**?
