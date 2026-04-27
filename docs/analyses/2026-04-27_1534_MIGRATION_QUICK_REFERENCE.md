# Migration Quick Reference — Copy-Paste Commands & Path Replacements

**Use this for execution phase.**

---

## 1. Directory Structure Setup

```bash
# Create target directories
mkdir -p thesis/analysis/notebooks/{02_ml_training,03_agentic,05_evaluation}
mkdir -p thesis/analysis/prompts/
mkdir -p thesis/analysis/outputs/
mkdir -p thesis/analysis/outputs/{csd,danskvand,energidrikke,rtd_v2,totalbeer,pooled_4,pooled_5}

# Verify created
ls -d thesis/analysis/notebooks/*
ls -d thesis/analysis/outputs/*
```

---

## 2. Copy Notebooks

```bash
# Phase 2 (ML Training — 8 notebooks)
cp docs/thesis/analysis/thesis_notebook_CSD.ipynb \
   thesis/analysis/notebooks/02_ml_training/specialized_CSD.ipynb

cp docs/thesis/analysis/thesis_notebook_danskvand.ipynb \
   thesis/analysis/notebooks/02_ml_training/specialized_danskvand.ipynb

cp docs/thesis/analysis/thesis_notebook_energidrikke.ipynb \
   thesis/analysis/notebooks/02_ml_training/specialized_energidrikke.ipynb

cp docs/thesis/analysis/thesis_notebook_rtd.ipynb \
   thesis/analysis/notebooks/02_ml_training/specialized_rtd.ipynb

cp docs/thesis/analysis/thesis_notebook_totalbeer.ipynb \
   thesis/analysis/notebooks/02_ml_training/specialized_totalbeer.ipynb

cp docs/thesis/analysis/thesis_notebook_pooled_4.ipynb \
   thesis/analysis/notebooks/02_ml_training/pooled_4.ipynb

cp docs/thesis/analysis/thesis_notebook_pooled_5.ipynb \
   thesis/analysis/notebooks/02_ml_training/pooled_5.ipynb

cp docs/thesis/analysis/thesis_notebook_final_comparison.ipynb \
   thesis/analysis/notebooks/02_ml_training/comparison.ipynb

# Phase 3 (Agentic Registry)
cp docs/thesis/analysis/thesis_agentic_notebook.ipynb \
   thesis/analysis/notebooks/03_agentic_integration/registry_and_forecasting.ipynb

# Phase 5 (Evaluation)
cp docs/thesis/analysis/thesis_notebook_AB_test.ipynb \
   thesis/analysis/notebooks/05_evaluation/4tier_ab_test_final.ipynb
```

---

## 3. Copy Data Assets

```bash
# Prompts (evaluation prompts v5)
cp docs/thesis/analysis/outputs_ab_test/prompts.csv \
   thesis/analysis/prompts/prompts_v5_final.csv

# Human eval template
cp docs/thesis/analysis/outputs_ab_test/human_eval_pilot_15_v3.csv \
   thesis/analysis/prompts/human_eval_pilot_15_v3.csv

# Verify
ls -lh thesis/analysis/prompts/
```

---

## 4. Path Replacements (Find & Replace in each notebook)

### For ALL 10 notebooks:

**Original**:
```python
PROJECT_ROOT / "docs" / "thesis" / "analysis"
```

**Replace with**:
```python
PROJECT_ROOT / "thesis" / "analysis"
```

### For training notebooks (8):

**Original**:
```python
OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_{CATEGORY}"
```

**Replace with**:
```python
OUTPUT_DIR = PROJECT_ROOT / "thesis" / "analysis" / "outputs" / "{category_name}"
```

Example replacements per notebook:
- `specialized_CSD.ipynb`:
  - OLD: `"outputs"` → NEW: `"outputs" / "csd"`
- `specialized_danskvand.ipynb`:
  - OLD: `"outputs_danskvand"` → NEW: `"outputs" / "danskvand"`
- `specialized_energidrikke.ipynb`:
  - OLD: `"outputs_energidrikke"` → NEW: `"outputs" / "energidrikke"`
- `specialized_rtd.ipynb`:
  - OLD: `"outputs_rtd_v2"` → NEW: `"outputs" / "rtd_v2"`
- `specialized_totalbeer.ipynb`:
  - OLD: `"outputs_totalbeer"` → NEW: `"outputs" / "totalbeer"`
- `pooled_4.ipynb`:
  - OLD: `"outputs_pooled_4"` → NEW: `"outputs" / "pooled_4"`
- `pooled_5.ipynb`:
  - OLD: `"outputs_pooled_5"` → NEW: `"outputs" / "pooled_5"`
- `comparison.ipynb`:
  - OLD: `output_dir(name)` function → NEW: see below

### For comparison.ipynb:

**Original function**:
```python
def output_dir(name):
    if name == "CSD":
        return ANALYSIS_DIR / "outputs"
    else:
        return ANALYSIS_DIR / f"outputs_{name.lower()}"
```

**Replace with**:
```python
def output_dir(name):
    return ANALYSIS_DIR / "outputs" / name.lower()
```

### For registry_and_forecasting.ipynb (CRITICAL):

**Original (§0.5)**:
```python
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

**Replace with**:
```python
CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "csd",
        ...
    },
    "danskvand": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "danskvand",
        ...
    },
    "energidrikke": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "energidrikke",
        ...
    },
    "rtd": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "rtd_v2",
        ...
    },
    "totalbeer": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "totalbeer",
        ...
    },
}

POOLED_MODELS = {
    "pooled_4": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "pooled_4",
        ...
    },
    "pooled_5": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "pooled_5",
        ...
    },
}
```

**Also in registry_and_forecasting.ipynb, delete (or comment out)**:
```python
# These are now redundant:
SRQ1_OUTPUTS = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs"
SRQ1_PIPELINES = SRQ1_OUTPUTS / "pipelines"
```

### For 4tier_ab_test_final.ipynb (CRITICAL):

**Original (§0.2)**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"
prompts_path = ANALYSIS_DIR / "outputs_ab_test" / "prompts.csv"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_ab_test"
FIGURE_DIR = OUTPUT_DIR / "figures"
```

**Replace with**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"
prompts_path = ANALYSIS_DIR / "prompts" / "prompts_v5_final.csv"
OUTPUT_DIR = ANALYSIS_DIR / "outputs" / "ab_test_v5"
FIGURE_DIR = OUTPUT_DIR / "figures"
```

---

## 5. Move or Regenerate Pickles (Decision)

### Option A: MOVE (fast, 1 hour)

```bash
# If old structure is:
# docs/thesis/analysis/outputs/pipelines/*.pkl
# docs/thesis/analysis/outputs_danskvand/pipelines/*.pkl
# etc.

# Then copy all:
cp -r docs/thesis/analysis/outputs/pipelines/* \
      thesis/analysis/outputs/csd/pipelines/

cp -r docs/thesis/analysis/outputs/feature_matrix_split.parquet \
      thesis/analysis/outputs/csd/

cp -r docs/thesis/analysis/outputs_danskvand/pipelines/* \
      thesis/analysis/outputs/danskvand/pipelines/

cp -r docs/thesis/analysis/outputs_danskvand/feature_matrix_split.parquet \
      thesis/analysis/outputs/danskvand/

# ... (repeat for energidrikke, rtd_v2, totalbeer, pooled_4, pooled_5)

# Verify counts:
find thesis/analysis/outputs -name "*.pkl" | wc -l  # Should be 14 (7 cats × 2 models)
find thesis/analysis/outputs -name "*.parquet" | wc -l  # Should be 7 (1 per category)
```

### Option B: REGENERATE (thorough, 3 hours)

```bash
# Open Jupyter and run each training notebook:
jupyter notebook thesis/analysis/notebooks/02_ml_training/specialized_CSD.ipynb
# [Run all cells, saves to new location automatically]

# Repeat for:
jupyter notebook thesis/analysis/notebooks/02_ml_training/specialized_danskvand.ipynb
jupyter notebook thesis/analysis/notebooks/02_ml_training/specialized_energidrikke.ipynb
jupyter notebook thesis/analysis/notebooks/02_ml_training/specialized_rtd.ipynb
jupyter notebook thesis/analysis/notebooks/02_ml_training/specialized_totalbeer.ipynb
jupyter notebook thesis/analysis/notebooks/02_ml_training/pooled_4.ipynb
jupyter notebook thesis/analysis/notebooks/02_ml_training/pooled_5.ipynb
jupyter notebook thesis/analysis/notebooks/02_ml_training/comparison.ipynb
```

---

## 6. Validation (Before main run)

```bash
# Check all paths exist:
ls thesis/analysis/prompts/prompts_v5_final.csv  # Should exist
ls thesis/analysis/outputs/csd/pipelines/*.pkl  # Should have model_xgboost.pkl + model_lightgbm.pkl
find thesis/analysis/outputs -name "feature_matrix_split.parquet" | wc -l  # Should be 7

# Quick notebook test (in Jupyter):
# 1. Open thesis/analysis/notebooks/03_agentic_integration/registry_and_forecasting.ipynb
# 2. Run §0-2 (setup, load models)
# 3. Verify no FileNotFoundError
# 4. Print: ANALYSIS_DIR, registry keys, model paths

# 2. Open thesis/analysis/notebooks/05_evaluation/4tier_ab_test_final.ipynb
# 1. Run §0-1 (setup, load prompts)
# 2. Verify prompts_df.shape == (50, N)
# 3. Run §2 (load models)
# 4. Verify no FileNotFoundError

# If all ✅, proceed to main run
```

---

## 7. DRY RUN (cheap test, ~2 min, $0.05)

```bash
# In thesis/analysis/notebooks/05_evaluation/4tier_ab_test_final.ipynb:
# 1. Run §0-1 (setup, load prompts) ✅
# 2. Run §2 (load models) ✅
# 3. In §3, modify main loop to run 1 prompt × 1 system (L0 only):

# BEFORE main loop, add:
n_prompts = 1  # Override: just 1 prompt
systems = ["L0"]  # Override: just L0 (no tools, cheapest)

# Then run §3
# Expected: 1 OpenAI call (~$0.001), 2 min
# If success, proceed to full run
```

---

## 8. FULL RUN (thesis chapter, 35 min, $4)

```bash
# In 4tier_ab_test_final.ipynb:
# Comment out or remove the dry-run overrides:
# n_prompts = 1  # ← REMOVE
# systems = ["L0"]  # ← REMOVE

# Run §3: 50 prompts × 4 systems = 200 OpenAI calls (~$1.50, 12 min)
# Run §5: 50 × 4 × 5 metrics judge = 1000 Claude calls (~$2, 20 min)
# Run §6: 6 pairwise × 50 = 300 Claude calls (~$0.50, 5 min)
# Run §7-9: Free (metrics, figures, tables, 3 min)

# Total: 35 min, $4

# Outputs:
# - thesis/analysis/outputs/ab_test_v5/ab_raw_outputs.csv
# - thesis/analysis/outputs/ab_test_v5/ab_metrics.csv
# - thesis/analysis/outputs/ab_test_v5/ab_summary.csv
# - thesis/analysis/outputs/ab_test_v5/figures/*.png (5 figures)

# Copy figures + tables → Chapter 7 Word doc
```

---

## 9. Cleanup (after validation)

```bash
# Archive old location (don't delete until you're 100% sure)
mv docs/thesis/analysis docs/thesis/analysis.archive_2026-04-27

# Verify new location works
ls thesis/analysis/outputs/csd/pipelines/
ls thesis/analysis/prompts/prompts_v5_final.csv

# Git commit
git add thesis/analysis/
git commit -m "feat: migrate analysis notebooks from docs/thesis to thesis/analysis

- Move 10 Jupyter notebooks to thesis/analysis/notebooks/{02_ml_training,03_agentic,05_evaluation}
- Move evaluation prompts to thesis/analysis/prompts/
- Update all path references (ANALYSIS_DIR, OUTPUT_DIR, prompts_path)
- Update CATEGORY_MODELS registry to new output directory structure
- Consolidate model outputs under thesis/analysis/outputs/{category}/

Fixes issue: notebooks in docs/thesis/ should be in thesis/ root structure"
```

---

## Common Errors & Fixes

| **Error** | **Cause** | **Fix** |
|-----------|----------|--------|
| `FileNotFoundError: ... / outputs / prompts.csv` | Prompts CSV not moved | `cp docs/thesis/analysis/outputs_ab_test/prompts.csv thesis/analysis/prompts/prompts_v5_final.csv` |
| `FileNotFoundError: ... / pipelines / model_xgboost.pkl` | Registry path doesn't match pickle location | Verify `cfg["outputs_dir"]` and actual file location match |
| `ModuleNotFoundError` in notebook | Old paths still hardcoded | `grep -n "docs" thesis/analysis/notebooks/*.ipynb` → find and replace |
| Model loads but predictions wrong | Old stale pickles | Option: regenerate (3 hours) or trust old models |
| Eval notebook prompts wrong | CSV not moved or renamed | Verify `prompts_path` and file match exactly |

---

## Checklist

```
PRE-MIGRATION
[ ] Read MIGRATION_EXECUTIVE_SUMMARY.md (this file)
[ ] Decide: MOVE pickles or REGENERATE? (1 hour vs 3 hours)
[ ] Backup old location? `cp -r docs/thesis/analysis docs/thesis/analysis.bak`

DIRECTORY SETUP
[ ] mkdir -p thesis/analysis/notebooks/{02_ml_training,03_agentic,05_evaluation}
[ ] mkdir -p thesis/analysis/prompts/
[ ] mkdir -p thesis/analysis/outputs/{csd,danskvand,...}

NOTEBOOK COPY
[ ] cp all 10 notebooks to new locations (see §2)

DATA ASSETS
[ ] cp prompts.csv → thesis/analysis/prompts/prompts_v5_final.csv
[ ] cp human_eval_pilot_15_v3.csv → thesis/analysis/prompts/

PATH UPDATES
[ ] Update ANALYSIS_DIR (all 10 notebooks)
[ ] Update OUTPUT_DIR (8 training notebooks)
[ ] Update prompts_path (eval notebook)
[ ] Update CATEGORY_MODELS registry (agentic notebook)

PICKLE MANAGEMENT
[ ] MOVE: cp old pickles to new locations (1 hour)
  OR
[ ] REGENERATE: run training notebooks (3 hours)

VALIDATION
[ ] Verify paths exist: ls thesis/analysis/prompts/prompts_v5_final.csv
[ ] Verify models exist: ls thesis/analysis/outputs/csd/pipelines/*.pkl
[ ] Test agentic notebook §0-2 (load models)
[ ] Test eval notebook §0-2 (load prompts + models)

DRY RUN
[ ] Run eval §3 with 1 prompt × 1 system (~$0.05, 2 min)
[ ] Verify no FileNotFoundError

FULL RUN
[ ] Run eval §3-9 (35 min, $4) → Chapter 7 results

CLEANUP
[ ] Archive old docs/thesis/analysis/ → docs/thesis/analysis.archive_2026-04-27
[ ] Git commit migration

POST-MIGRATION
[ ] Update MESSAGE_TO_BRIAN.md file paths
[ ] Update any docs that reference old paths
[ ] Create thesis/analysis/README.md with new structure
```

---

**Questions?** Check the 3 analysis documents:
1. `ANALYSIS_MIGRATION_PLAN.md` — phases & overall strategy
2. `NOTEBOOK_STRUCTURE_ANALYSIS.md` — what each notebook does
3. `CROSS_REFERENCES_AND_DEPENDENCIES.md` — detailed path mapping
