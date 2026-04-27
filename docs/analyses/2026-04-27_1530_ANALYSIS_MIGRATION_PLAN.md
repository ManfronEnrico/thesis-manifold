# Migration Analysis: docs/thesis/analysis → thesis/analysis

**Status**: Pre-migration analysis  
**Created**: 2026-04-27  
**Scope**: 10 Jupyter notebooks + 10 ML retraining scripts + registry + data pipeline

---

## 1. Current State

### Notebooks in `docs/thesis/analysis/`
```
docs/thesis/analysis/
├── thesis_agentic_notebook.ipynb          (Phase 3: multi-category registry)
├── thesis_notebook_AB_test.ipynb          (Phase 5: 4-tier LLM eval v5)
├── thesis_notebook_CSD.ipynb              (Phase 2: CSD category model)
├── thesis_notebook_danskvand.ipynb        (Phase 2: danskvand category)
├── thesis_notebook_energidrikke.ipynb     (Phase 2: energidrikke category)
├── thesis_notebook_rtd.ipynb              (Phase 2: RTD category)
├── thesis_notebook_totalbeer.ipynb        (Phase 2: totalbeer category)
├── thesis_notebook_pooled_4.ipynb         (Phase 2: pooled 4-category)
├── thesis_notebook_pooled_5.ipynb         (Phase 2: pooled 5-category)
├── thesis_notebook_final_comparison.ipynb (Phase 2: comparison across models)
├── outputs_ab_test/
│   ├── prompts.csv                        (50 final eval prompts, v5)
│   └── human_eval_pilot_15_v3.csv         (human eval template)
└── outputs_agentic/                       (runtime outputs from agentic notebook)
```

### Target Structure in `thesis/`
```
thesis/
├── analysis/                              (NEW)
│   ├── notebooks/                         (NEW)
│   │   ├── 02_ml_training/
│   │   │   ├── specialized_CSD.ipynb
│   │   │   ├── specialized_danskvand.ipynb
│   │   │   ├── ...
│   │   │   └── pooled_5.ipynb
│   │   ├── 03_agentic_integration/
│   │   │   └── registry_and_forecasting.ipynb
│   │   └── 05_evaluation/
│   │       └── 4tier_ab_test_final.ipynb
│   ├── prompts/                           (NEW)
│   │   ├── prompts_v5_final.csv
│   │   └── human_eval_pilot_15_v3.csv
│   ├── outputs/                           (NEW - runtime)
│   └── README.md
├── data/                                  (EXISTING)
├── thesis_agents/                         (EXISTING)
└── thesis-writing/                        (EXISTING)
```

---

## 2. Path Dependencies Found in Notebooks

### 2.1 `PROJECT_ROOT` Pattern (All notebooks)
```python
PROJECT_ROOT = Path.cwd().resolve()
while not (PROJECT_ROOT / "CLAUDE.md").exists() and PROJECT_ROOT != PROJECT_ROOT.parent:
    PROJECT_ROOT = PROJECT_ROOT.parent
```
**Status**: ✅ Works from any directory (CLAUDE.md exists at repo root)

### 2.2 `ANALYSIS_DIR` (Multiple notebooks)
**Current**: 
```python
ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"
```
**After migration**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"
```

### 2.3 Output Directories (Hardcoded in registry)
**In `thesis_agentic_notebook.ipynb` §0.5 — CATEGORY_MODELS registry**:
```python
CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs",           # ← will change path
        "primary_model": "xgboost",
        ...
    },
    "danskvand": {
        "outputs_dir": ANALYSIS_DIR / "outputs_danskvand", # ← will change path
        ...
    },
    "energidrikke": {
        "outputs_dir": ANALYSIS_DIR / "outputs_energidrikke",
        ...
    },
    "rtd": {
        "outputs_dir": ANALYSIS_DIR / "outputs_rtd_v2",
        ...
    },
    "totalbeer": {
        "outputs_dir": ANALYSIS_DIR / "outputs_totalbeer",
        ...
    },
}
```

**Impact**: 
- These paths are **dynamically constructed**, so changing `ANALYSIS_DIR` will automatically propagate ✅
- **BUT**: Old model pickle files (`.pkl`) are saved in the old `docs/thesis/analysis/outputs*` dirs
- **Action needed**: Either move the pickles OR regenerate them

### 2.4 Data Paths (External dependencies)
All notebooks reference:
```python
SRQ1_OUTPUTS = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs"  # ← OLD

# Also in some notebooks:
INDEKS_PATH = PROJECT_ROOT / "data" / "raw" / "indeks_data.parquet"
INDEKS_META = PROJECT_ROOT / "data" / "raw" / "indeks_metadata.parquet"
INDEKS_CODEBOOK = PROJECT_ROOT / "data" / "raw" / "indeks_codebook.parquet"
```

**Status**: 
- `SRQ1_OUTPUTS` hardcoded to old path (needs update)
- Data paths (`INDEKS_*`) use generic paths under `data/raw/` (OK, won't break)

### 2.5 ML Retraining Pipeline Scripts
**Location**: `scripts/ml_retraining/` (10 files)
```
scripts/ml_retraining/
├── 00_setup.py
├── 01_ingest_raw.py
├── 02_data_cleaning.py
├── 03_eda.py
├── 04_feature_engineering.py
├── 05_split.py
├── 06_preprocessing_pipeline.py
├── 07_baselines.py
├── 08_advanced_models.py
├── 09_shap_explain.py
├── 10_publication_figures.py
└── __init__.py
```

**References to find**:
- Do these scripts hardcode output paths to `docs/thesis/analysis/outputs*`?
- Do they import from notebooks (unlikely but check)?
- Where do they write pickles?

---

## 3. Cross-Reference Map (Reverse dependencies)

### 3.1 Which files import or reference these notebooks?

**Search results**:
- ✅ `MESSAGE_TO_BRIAN.md` — references the notebooks, lists them in Phase 2-5 description
- ✅ `README.md` — likely links to analysis notebooks
- ❓ `thesis_agents/` modules — may call functions from agentic notebook
- ❓ `scripts/ml_retraining/` — may reference output paths

### 3.2 Which code calls `load_model_for_category()` or `predict_for_category()`?
**In `thesis_agentic_notebook.ipynb` §2.5**:
```python
def load_model_for_category(category: str, model_type: str | None = None) -> dict:
    """Load trained model + pipeline + feature matrix for a Nielsen category."""
    # Uses registry to find: 
    # out_dir / "pipelines" / f"model_{chosen}.pkl"
    # out_dir / "pipelines" / "pipe_tree.pkl"
    # out_dir / cfg["fm_filename"]  (parquet)
```

**Calls to this function**:
- Internal to agentic notebook in `§2.5 forecasting_agent_multi()`
- May be imported by other scripts → **search for imports**

---

## 4. Notebook-by-Notebook Analysis

### 4.1 `thesis_agentic_notebook.ipynb` (Phase 3)
**Size**: ~2929 tokens (large)  
**Sections**:
- §0: Setup (PROJECT_ROOT, paths, env)
- §0.5: **CRITICAL** — Multi-category model registry + `load_model_for_category()` + `predict_for_category()`
- §1: Data loading (Nielsen sales + Indeks features)
- §2: Feature engineering via `data_assessment_agent`
- §2.5: Forecasting agent multi-category (routes to per-category models)
- §3+: Visualization and export

**Path changes needed**:
```diff
- ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"
+ ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"

- SRQ1_PIPELINES = SRQ1_OUTPUTS / "pipelines"
+ SRQ1_PIPELINES = ANALYSIS_DIR / "outputs" / "pipelines"  (or per-category)
```

**Dependencies**:
- Imports: `pandas`, `numpy`, `openai`, `anthropic`, pickle, etc.
- Calls: `data_assessment_agent` from `thesis_agents/`
- Outputs: `outputs_agentic/` CSVs + figures

---

### 4.2 `thesis_notebook_AB_test.ipynb` (Phase 5 — CRITICAL)
**Size**: ~31k tokens (very large, multiple sections)  
**This is the main eval notebook**

**Sections**:
- §0: Setup, paths, registry (same as agentic)
- §1: Load evaluation prompts (50 final prompts v5)
- §2: Run 4-tier LLM eval (L0/L1/L2/L3)
  - L0: gpt-4o-mini (LLM-only)
  - L1: gpt-4o-mini + raw data tool
  - L2: gpt-4o-mini + untuned ML
  - L3: gpt-4o-mini + tuned ML + confidence
- §3-8: Metrics evaluation
- §5: Main loop (200 OpenAI calls, 1000 Claude calls for judge)
- §7: LLM-as-judge (12-metric rubric)
- §8: Pairwise comparison
- §9+: Figures and tables

**Path changes needed**:
```diff
- ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"
+ ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"

- prompts_path = ANALYSIS_DIR / "outputs_ab_test" / "prompts.csv"
+ prompts_path = ANALYSIS_DIR / "prompts" / "prompts_v5_final.csv"

- OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_ab_test"
+ OUTPUT_DIR = ANALYSIS_DIR / "outputs" / "ab_test_v5"
```

**Critical note**: This notebook **MUST run successfully** to produce Chapter 7 results. Any path error will break the final evaluation.

---

### 4.3 Training Notebooks (8 files)
**Files**: `thesis_notebook_{CSD,danskvand,energidrikke,rtd,totalbeer,pooled_4,pooled_5,final_comparison}.ipynb`

**Common pattern** (each):
```python
PROJECT_ROOT = Path.cwd().resolve()
while not (PROJECT_ROOT / "CLAUDE.md").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent

OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_{category}"
FIGURE_DIR = OUTPUT_DIR / "figures"

# Then save:
model.pkl → OUTPUT_DIR / "pipelines" / f"model_{chosen}.pkl"
pipe.pkl → OUTPUT_DIR / "pipelines" / "pipe_tree.pkl"
feature_matrix.parquet → OUTPUT_DIR / "feature_matrix_split.parquet"
```

**Path changes**:
```diff
- OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_{category}"
+ OUTPUT_DIR = PROJECT_ROOT / "thesis" / "analysis" / "outputs" / "{category}"
```

**Note**: If these were already run, the `.pkl` files are in **old locations**. You either:
1. Copy them to new structure OR
2. Re-run training (cost: time, not money—these use local data only)

---

### 4.4 `thesis_notebook_final_comparison.ipynb`
**Purpose**: Compare all 7 trained models (5 specialized + 2 pooled)

**Key code**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"

SPECIALIZED = ["CSD", "danskvand", "energidrikke", "RTD", "totalbeer"]
POOLED = ["pooled_4", "pooled_5"]
ALL_NOTEBOOKS = SPECIALIZED + POOLED

def output_dir(name):
    return ANALYSIS_DIR / (f"outputs_{name.lower()}" if name != "CSD" else "outputs")
```

**After migration**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"

def output_dir(name):
    category = name.lower()
    return ANALYSIS_DIR / "outputs" / category
```

---

## 5. ML Retraining Scripts (`scripts/ml_retraining/`)

**Quick check needed**: Do these reference `docs/thesis/analysis/`?

```bash
grep -r "docs/thesis" scripts/ml_retraining/
```

**If found**: Update the same way.

---

## 6. Migration Checklist

### Phase 1: Pre-migration (Analysis)
- [ ] Verify all path references in each notebook (done above)
- [ ] Check `scripts/ml_retraining/` for hardcoded paths
- [ ] Inventory `.pkl` and `.parquet` files in current `docs/thesis/analysis/outputs*`
- [ ] Confirm `MESSAGE_TO_BRIAN.md` expectations vs. new structure

### Phase 2: Prepare target structure
- [ ] Create `thesis/analysis/` directory
- [ ] Create `thesis/analysis/notebooks/{02_ml_training,03_agentic,05_evaluation}/`
- [ ] Create `thesis/analysis/prompts/`
- [ ] Create `thesis/analysis/outputs/` (for runtime)

### Phase 3: Copy and update notebooks
- [ ] Copy 10 notebooks to `thesis/analysis/notebooks/` (organized by phase)
- [ ] Update `ANALYSIS_DIR` path in each (find-replace pattern)
- [ ] Update `SRQ1_OUTPUTS` if present
- [ ] Update output directory names if different

### Phase 4: Move data assets
- [ ] Move `outputs_ab_test/prompts.csv` → `thesis/analysis/prompts/prompts_v5_final.csv`
- [ ] Move `outputs_ab_test/human_eval_pilot_15_v3.csv` → `thesis/analysis/prompts/`
- [ ] **Decision**: Copy old `.pkl` files or regenerate?

### Phase 5: Update references
- [ ] Update `MESSAGE_TO_BRIAN.md` file paths (if it references them)
- [ ] Update `README.md` if it links to notebooks
- [ ] Update `scripts/ml_retraining/` if needed
- [ ] Update `.claude/IMPORTED_SKILLS_ANALYSIS.md` or similar doc references

### Phase 6: Validation
- [ ] Run `thesis_agentic_notebook.ipynb` (quick smoke test with 1 category)
- [ ] Run `thesis_notebook_AB_test.ipynb` (full run will cost $4, but dry-run first)
- [ ] Verify pickles load correctly
- [ ] Verify output CSVs write to correct locations

### Phase 7: Cleanup
- [ ] Archive old `docs/thesis/analysis/` (or delete after confirmation)
- [ ] Update git references if any workflows reference old paths
- [ ] Commit migration as single changeset

---

## 7. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Hardcoded paths break model loading | **HIGH** | Systematic find-replace + validation |
| Missing pickles after migration | **MEDIUM** | Inventory before migration or accept rerun cost |
| Notebooks don't run after move | **HIGH** | Test each in Jupyter with print(ANALYSIS_DIR) |
| Old outputs still referenced in prose | **LOW** | Search MESSAGE_TO_BRIAN.md + chapter drafts |
| Prometheus integration conflicts | **MEDIUM** | Plan L4 tier alongside migration |

---

## 8. Prometheus Integration Note

Enrico mentioned L4 (Prometheus integration) will be added later. Make sure:
- New structure accommodates `outputs_prometheus/` or similar
- Registry in agentic notebook is extensible
- Don't hardcode single output structure

Proposed:
```python
TIER_OUTPUTS = {
    "L2": ANALYSIS_DIR / "outputs" / "l2_untuned",
    "L3": ANALYSIS_DIR / "outputs" / "l3_tuned",
    "L4": ANALYSIS_DIR / "outputs" / "l4_prometheus",  # ← future
}
```

---

## Next Steps

1. **This document**: Approved? Proceed to **Step-by-step notebook analysis**
2. **Notebook 1 detail**: Deep dive into `thesis_agentic_notebook.ipynb` (registry, functions, outputs)
3. **Notebook 2 detail**: Deep dive into `thesis_notebook_AB_test.ipynb` (eval flow, v5 prompts, metrics)
4. **Scripts check**: Verify `scripts/ml_retraining/` paths
5. **Execute migration**: Coordinated copy + find-replace + test

**Ready to proceed?**
