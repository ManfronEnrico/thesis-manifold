# Cross-References & Dependencies Map

**Purpose**: Document all code that depends on the current `docs/thesis/analysis/` structure  
**Date**: 2026-04-27

---

## 1. Hardcoded Path References (Master List)

### 1.1 Notebooks (direct hardcode)

**All training notebooks** (8 files):
- `thesis_notebook_CSD.ipynb`
- `thesis_notebook_danskvand.ipynb`
- `thesis_notebook_energidrikke.ipynb`
- `thesis_notebook_rtd.ipynb`
- `thesis_notebook_totalbeer.ipynb`
- `thesis_notebook_pooled_4.ipynb`
- `thesis_notebook_pooled_5.ipynb`

```python
# Pattern in each:
OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_{CATEGORY}"
FIGURE_DIR = OUTPUT_DIR / "figures"

# Then saves:
pickle files → OUTPUT_DIR / "pipelines" / "model_{xgboost|lightgbm}.pkl"
parquet files → OUTPUT_DIR / "feature_matrix_split.parquet"
```

**Expected after migration**:
```python
OUTPUT_DIR = PROJECT_ROOT / "thesis" / "analysis" / "outputs" / "{category_name}"
```

---

**`thesis_agentic_notebook.ipynb`** (§0.5):
```python
ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"  # ← HARDCODE

CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs",
        ...
    },
    "danskvand": {
        "outputs_dir": ANALYSIS_DIR / "outputs_danskvand",
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

POOLED_MODELS = {
    "pooled_4": {
        "outputs_dir": ANALYSIS_DIR / "outputs_pooled_4",
        ...
    },
    "pooled_5": {
        "outputs_dir": ANALYSIS_DIR / "outputs_pooled_5",
        ...
    },
}
```

**Also in agentic notebook**:
```python
SRQ1_OUTPUTS = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs"
SRQ1_PIPELINES = SRQ1_OUTPUTS / "pipelines"  # ← used in §1 for loading models

lgbm_path = SRQ1_PIPELINES / "model_lightgbm.pkl"
pipe_tree_path = SRQ1_PIPELINES / "pipe_tree.pkl"
```

**Expected after migration**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"

CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "csd",  # NEW
        ...
    },
    "danskvand": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "danskvand",  # NEW
        ...
    },
    # etc.
}

# Remove SRQ1_OUTPUTS + SRQ1_PIPELINES (replaced by per-category outputs_dir)
```

---

**`thesis_notebook_AB_test.ipynb`** (§0, §1):
```python
ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"  # ← HARDCODE

# §0.2: Paths for prompts and outputs
prompts_path = ANALYSIS_DIR / "outputs_ab_test" / "prompts.csv"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_ab_test"
FIGURE_DIR = OUTPUT_DIR / "figures"

# §1: Load prompts
prompts_df = pd.read_csv(prompts_path)  # ← Will fail if path wrong

# §2: Load models via load_model_for_category()
# (imported or called inline)
```

**Expected after migration**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"

prompts_path = ANALYSIS_DIR / "prompts" / "prompts_v5_final.csv"
OUTPUT_DIR = ANALYSIS_DIR / "outputs" / "ab_test_v5"
FIGURE_DIR = OUTPUT_DIR / "figures"
```

---

**`thesis_notebook_final_comparison.ipynb`**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"

def output_dir(name):
    if name == "CSD":
        return ANALYSIS_DIR / "outputs"
    else:
        return ANALYSIS_DIR / f"outputs_{name.lower()}"
```

**Expected after migration**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"

def output_dir(name):
    return ANALYSIS_DIR / "outputs" / name.lower()
```

---

### 1.2 Data Assets (move, don't recompute)

**Prompts CSV**:
```
docs/thesis/analysis/outputs_ab_test/prompts.csv  (50 final eval prompts, v5)
    ↓ MOVE TO
thesis/analysis/prompts/prompts_v5_final.csv
```

**Human eval template**:
```
docs/thesis/analysis/outputs_ab_test/human_eval_pilot_15_v3.csv  (15 prompts × 4 systems)
    ↓ MOVE TO
thesis/analysis/prompts/human_eval_pilot_15_v3.csv
```

---

### 1.3 Model Artifacts (Decision: move or regenerate?)

**Current locations**:
```
docs/thesis/analysis/outputs/pipelines/
├── model_xgboost.pkl
├── model_lightgbm.pkl
└── pipe_tree.pkl

docs/thesis/analysis/outputs/feature_matrix_split.parquet

(and parallel: outputs_danskvand/, outputs_energidrikke/, outputs_rtd_v2/, outputs_totalbeer/, outputs_pooled_4/, outputs_pooled_5/)
```

**Target locations** (after migration):
```
thesis/analysis/outputs/csd/pipelines/
├── model_xgboost.pkl
├── model_lightgbm.pkl
└── pipe_tree.pkl

thesis/analysis/outputs/csd/feature_matrix_split.parquet

(and: outputs/danskvand/, outputs/energidrikke/, outputs/rtd_v2/, outputs/totalbeer/, outputs/pooled_4/, outputs/pooled_5/)
```

**Options**:
1. **Move** (requires file copy): 5 min, no recompute
2. **Regenerate** (requires notebook run): 2-3 hours, no cloud cost, ensures consistency
3. **Hybrid** (move + fallback): Migrate files, but add fallback path loading in registries

**Recommendation**: Hybrid (move files now, add fallback logic so old paths work during transition)

---

## 2. Code That Uses These Paths

### 2.1 Load calls (registry-based)

**In `load_model_for_category(category, model_type)`** (agentic notebook §2.5):
```python
def load_model_for_category(category: str, model_type: str | None = None) -> dict:
    registry = {**CATEGORY_MODELS, **POOLED_MODELS}
    cfg = registry[category]
    out_dir = cfg["outputs_dir"]  # ← CRITICAL: must point to correct location
    
    with open(out_dir / "pipelines" / f"model_{chosen}.pkl", "rb") as f:
        model = pickle.load(f)  # ← Will fail if file not at expected path
    
    with open(out_dir / "pipelines" / "pipe_tree.pkl", "rb") as f:
        pipe = pickle.load(f)
    
    fm = pd.read_parquet(out_dir / cfg["fm_filename"])
    return {...}
```

**Call sites**:
- `thesis_agentic_notebook.ipynb` §2.5: `predict_for_category()` → `load_model_for_category()`
- `thesis_notebook_AB_test.ipynb` §2: `load_model_for_category()` (for L2 + L3 tiers)

**Failure mode**: If `out_dir` points to old path, or pickles aren't at that location:
```
FileNotFoundError: [Errno 2] No such file or directory: 'docs/thesis/analysis/outputs/pipelines/model_xgboost.pkl'
```

---

### 2.2 Save calls (output writers)

**In training notebooks** (each, §7 Save artifacts):
```python
(OUTPUT_DIR / "pipelines").mkdir(parents=True, exist_ok=True)
with open(OUTPUT_DIR / "pipelines" / f"model_{chosen}.pkl", "wb") as f:
    pickle.dump(model, f)

with open(OUTPUT_DIR / "pipelines" / "pipe_tree.pkl", "wb") as f:
    pickle.dump(pipe, f)

pd.to_parquet(feature_matrix, OUTPUT_DIR / cfg["fm_filename"])

# Metrics CSV
metrics_df.to_csv(OUTPUT_DIR / "metrics.csv")

# Figures
fig.savefig(OUTPUT_DIR / "figures" / f"mape_boxplot.png")
```

**If OUTPUT_DIR is wrong**: Pickles + metrics save to wrong location → training looks successful but agentic notebook can't find them.

---

### 2.3 CSV write calls (eval notebook)

**In `thesis_notebook_AB_test.ipynb`** (§5-8 Output):
```python
results_df.to_csv(OUTPUT_DIR / "ab_raw_outputs.csv", index=False)
metrics_df.to_csv(OUTPUT_DIR / "ab_metrics.csv", index=False)
summary.to_csv(OUTPUT_DIR / "ab_summary.csv")

fig.savefig(FIGURE_DIR / "mape_boxplot.png")
# etc. (5 figures)
```

**After migration**: Must ensure `OUTPUT_DIR = ANALYSIS_DIR / "outputs" / "ab_test_v5"` exists and is writable.

---

## 3. Dependency Chain Visualization

```
TRAINING NOTEBOOKS (independent, parallel execution)
├── thesis_notebook_CSD.ipynb
│   INPUT:  PROJECT_ROOT / "thesis" / "data" / "nielsen" / "..."
│   OUTPUT: thesis/analysis/outputs/csd/pipelines/model_{xgb,lgb}.pkl
│            thesis/analysis/outputs/csd/feature_matrix_split.parquet
│
├── thesis_notebook_danskvand.ipynb
│   OUTPUT: thesis/analysis/outputs/danskvand/...
│
├── thesis_notebook_energidrikke.ipynb
│   OUTPUT: thesis/analysis/outputs/energidrikke/...
│
├── thesis_notebook_rtd.ipynb
│   OUTPUT: thesis/analysis/outputs/rtd_v2/...
│
├── thesis_notebook_totalbeer.ipynb
│   OUTPUT: thesis/analysis/outputs/totalbeer/...
│
├── thesis_notebook_pooled_4.ipynb
│   OUTPUT: thesis/analysis/outputs/pooled_4/...
│
└── thesis_notebook_pooled_5.ipynb
    OUTPUT: thesis/analysis/outputs/pooled_5/...

        ↓ (all produce artifacts)

REGISTRY NOTEBOOK (depends on training outputs)
├── thesis_agentic_notebook.ipynb
│   INPUT:  Registry points to each OUTPUT above
│            thesis/analysis/prompts/prompts_v5_final.csv (if used)
│   FUNCTIONS:
│   ├── load_model_for_category(cat) → {model, pipe_tree, fm, ...}
│   └── predict_for_category(brand, channel, date, cat) → {pred, actual, error}
│   OUTPUT: thesis/analysis/outputs/agentic/*.csv
│
└── thesis_notebook_final_comparison.ipynb
    INPUT:  Iterates over all 7 outputs dirs
    OUTPUT: Comparison metrics + aggregated MAPE table

        ↓ (registry + functions available)

EVALUATION NOTEBOOK (critical for Chapter 7)
└── thesis_notebook_AB_test.ipynb
    INPUT:  
    ├── load_model_for_category() [via registry or import]
    ├── thesis/analysis/prompts/prompts_v5_final.csv  (50 prompts)
    └── CATEGORY_MODELS registry
    
    PROCESS:
    ├── §3: 4-tier eval (200 OpenAI calls)
    ├── §5: LLM judge (1000 Claude calls)
    ├── §6: Pairwise (300 Claude calls)
    
    OUTPUT:
    ├── thesis/analysis/outputs/ab_test_v5/ab_raw_outputs.csv
    ├── thesis/analysis/outputs/ab_test_v5/ab_metrics.csv
    ├── thesis/analysis/outputs/ab_test_v5/ab_summary.csv
    └── thesis/analysis/outputs/ab_test_v5/figures/*.png (5 figures)

                ↓ (results used in)

THESIS WRITING
└── Chapter 7: Results + Discussion
    Input: ab_summary.csv + figures
    Output: .docx with tables + figures
```

---

## 4. File-by-File Migration Checklist

### Training notebooks (8)

```
[ ] thesis_notebook_CSD.ipynb
    [ ] Update: OUTPUT_DIR = PROJECT_ROOT / "thesis" / "analysis" / "outputs" / "csd"
    [ ] Test: Can it load raw Nielsen data?
    [ ] Test: Can it save pickles to new location?
    [ ] Verify: (NEW_OUTPUT_DIR / "pipelines" / "model_xgboost.pkl").exists()

[ ] thesis_notebook_danskvand.ipynb
    [ ] UPDATE: OUTPUT_DIR = ... / "danskvand"
    [ ] ... (same verification)

[ ] thesis_notebook_energidrikke.ipynb
    [ ] UPDATE: OUTPUT_DIR = ... / "energidrikke"
    
[ ] thesis_notebook_rtd.ipynb
    [ ] UPDATE: OUTPUT_DIR = ... / "rtd_v2"
    
[ ] thesis_notebook_totalbeer.ipynb
    [ ] UPDATE: OUTPUT_DIR = ... / "totalbeer"
    
[ ] thesis_notebook_pooled_4.ipynb
    [ ] UPDATE: OUTPUT_DIR = ... / "pooled_4"
    
[ ] thesis_notebook_pooled_5.ipynb
    [ ] UPDATE: OUTPUT_DIR = ... / "pooled_5"
    
[ ] thesis_notebook_final_comparison.ipynb
    [ ] UPDATE: output_dir(name) function
    [ ] Test: Can it iterate all 7 outputs dirs?
```

### Registry + Agentic

```
[ ] thesis_agentic_notebook.ipynb
    [ ] UPDATE: ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"
    [ ] UPDATE: CATEGORY_MODELS registry (each outputs_dir)
    [ ] UPDATE: POOLED_MODELS registry (each outputs_dir)
    [ ] DELETE or comment: SRQ1_OUTPUTS, SRQ1_PIPELINES (now redundant)
    [ ] Test §0.5: Print ANALYSIS_DIR + verify registry paths
    [ ] Test §2.5: Call load_model_for_category("csd") → should load without error
    [ ] Test: Verify feature_matrix loads
```

### Evaluation (CRITICAL)

```
[ ] thesis_notebook_AB_test.ipynb
    [ ] UPDATE: ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"
    [ ] UPDATE: prompts_path = ANALYSIS_DIR / "prompts" / "prompts_v5_final.csv"
    [ ] UPDATE: OUTPUT_DIR = ANALYSIS_DIR / "outputs" / "ab_test_v5"
    [ ] Test §0-1: Load ANALYSIS_DIR, print paths, verify file exists (prompts.csv)
    [ ] Test §2: Call load_model_for_category() for L2 + L3 tiers
    [ ] DRY-RUN §3: Run 1 prompt × 1 system (e.g., L0 only) → $0.05, 2 min
    [ ] FULL RUN §3-8: 200 OpenAI + 1000+300 Claude calls → $4, 35 min (only after dry-run passes)
```

### Data assets (move)

```
[ ] Prompts CSV
    FROM: docs/thesis/analysis/outputs_ab_test/prompts.csv
    TO:   thesis/analysis/prompts/prompts_v5_final.csv
    VERIFY: file exists, 50 rows, columns match expected
    
[ ] Human eval template
    FROM: docs/thesis/analysis/outputs_ab_test/human_eval_pilot_15_v3.csv
    TO:   thesis/analysis/prompts/human_eval_pilot_15_v3.csv
    VERIFY: file exists, 15 rows
```

### Model artifacts (decision point)

```
[ ] DECIDE: Move pickles or regenerate?
    Option A: MOVE (faster, but trust old artifacts)
      [ ] Copy docs/thesis/analysis/outputs/pipelines → thesis/analysis/outputs/csd/pipelines
      [ ] Copy docs/thesis/analysis/outputs/feature_matrix* → thesis/analysis/outputs/csd/
      [ ] ... (repeat for all 7 categories)
      RISK: If old artifacts are stale/corrupt, problems hidden until runtime
      
    Option B: REGENERATE (slower, but ensures consistency)
      [ ] Run thesis_notebook_CSD.ipynb (and other 7) in Jupyter
      [ ] Time: 2-3 hours local compute
      [ ] Benefit: Latest data, latest hyperparameters, auditability
      
    Option C: HYBRID (move now, regenerate later if issues)
      [ ] Copy old artifacts as backup
      [ ] Add fallback logic in load_model_for_category(): 
          try new path, if not found try old path + warn
      [ ] Later: Regenerate and remove fallback
      BENEFIT: Unblocks Chapter 7 work now, fixes later

[ ] IF MOVE:
    [ ] Archive old docs/thesis/analysis/ (don't delete, in case needed)
    [ ] Create thesis/analysis/outputs/{csd,danskvand,...}/pipelines/
    [ ] Copy .pkl + .parquet files
    [ ] Verify file counts: 7 categories × (2 pkl + 1 parquet) = 21 files
    
[ ] IF REGENERATE:
    [ ] Open Jupyter
    [ ] Iterate: thesis_notebook_{CSD,danskvand,...}.ipynb
    [ ] Monitor disk space (notebooks save large CSVs + PNGs)
    [ ] Time this session: 2-3 hours
```

---

## 5. Risk Matrix: Path Changes

| **Change** | **Breaks if...** | **Mitigation** | **Severity** |
|-----------|------------------|----------------|------------|
| `ANALYSIS_DIR` | Any code not updated | Systematic find-replace + grep verify | HIGH |
| `OUTPUT_DIR` per-category | Notebooks save to old path | Test save location before main run | HIGH |
| `prompts_path` | File not moved | Manual move + verify file exists | HIGH |
| `load_model_for_category()` | Registry paths wrong or pickles missing | Test load before running eval | HIGH |
| Old `docs/thesis/analysis/outputs*` | Code still references | Fallback logic or force migration | MEDIUM |
| Figures path | `FIGURE_DIR.mkdir()` fails | Ensure parent dir exists | LOW |

---

## 6. Fallback Logic (Safe Migration)

If you want to minimize risk during transition:

```python
# In thesis_agentic_notebook.ipynb §0.5

def load_model_for_category(category: str, model_type: str | None = None) -> dict:
    registry = {**CATEGORY_MODELS, **POOLED_MODELS}
    cfg = registry[category]
    out_dir = cfg["outputs_dir"]
    
    # Try new path first
    model_path = out_dir / "pipelines" / f"model_{chosen}.pkl"
    if not model_path.exists():
        # Fallback to old path (temporary)
        old_dir = PROJECT_ROOT / "docs" / "thesis" / "analysis" / cfg.get("old_outputs_name", "outputs")
        model_path = old_dir / "pipelines" / f"model_{chosen}.pkl"
        if model_path.exists():
            print(f"⚠️  WARNING: Loading from OLD path {model_path}. Please regenerate.")
        else:
            raise FileNotFoundError(f"Model not found at {out_dir / 'pipelines'} or {old_dir / 'pipelines'}")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # ... rest of function
```

This allows:
1. Migration to proceed even if you choose to move pickles later
2. Clear warning when old paths are used
3. Easy to remove fallback once everything is regenerated

---

## Summary

**To migrate without breaking anything**:

1. **Update all `ANALYSIS_DIR` + `OUTPUT_DIR` paths** (find-replace in notebooks)
2. **Move prompts CSV + human eval template** (quick copy)
3. **Decide: move pickles or regenerate**
   - Move if you trust old artifacts + want speed
   - Regenerate if you want latest + consistency
   - Hybrid if you want both
4. **Update registry** (`load_model_for_category` calls)
5. **Test each notebook** (dry-run before full execution)
6. **Run AB test evaluation** ($4, 35 min)
7. **Write Chapter 7** (1 week)

**Critical path bottleneck**: `thesis_notebook_AB_test.ipynb` must work, or Chapter 7 stalls.
