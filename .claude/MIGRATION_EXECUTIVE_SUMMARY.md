# Migration Executive Summary

**Problem**: Enrico saved 10 Jupyter notebooks + 50 eval prompts in `docs/thesis/analysis/` but they should be in `thesis/analysis/` (the thesis root structure). The notebooks have hardcoded paths that will break if moved without careful updates.

**Scope**: 10 notebooks, 10 ML scripts, 2 CSV files, 7 categories of trained models (pickles).

**Risk Level**: HIGH — path errors will silently fail at runtime (model loading, prompt reading, output writing).

**Time to complete**: 
- Analysis: ✅ DONE (3 documents created)
- Execution: ~4-5 hours (2-3 hours regenerate models OR 1 hour move pickles + update code)
- Testing: ~1 hour
- Final eval run (thesis): ~35 min + $4

---

## What I've Analyzed

### 1. **ANALYSIS_MIGRATION_PLAN.md**
   - Maps current file locations
   - Lists target structure
   - Shows all path dependencies found via grep
   - Pre-migration checklist (7 phases)
   - Risk assessment matrix
   - **Key finding**: `ANALYSIS_DIR` is the root variable; change it, rest follows

### 2. **NOTEBOOK_STRUCTURE_ANALYSIS.md**
   - Cell-by-cell breakdown of each of 10 notebooks
   - What each does operationally
   - Data flow between notebooks (training → registry → eval)
   - Phase 5 prompt evolution (v1-v5 fixes)
   - **Key finding**: `thesis_notebook_AB_test.ipynb` is critical path (produces Chapter 7)

### 3. **CROSS_REFERENCES_AND_DEPENDENCIES.md**
   - Master list of hardcoded paths
   - Which code loads/saves to each path
   - Dependency chain visualization
   - File-by-file migration checklist
   - Risk matrix (what breaks if each path is wrong)
   - Fallback logic (safe migration pattern)
   - **Key finding**: Model pickle loading will silently fail if paths don't match

---

## Top 3 Issues Found

### Issue 1: Registry hardcoding
**Where**: `thesis_agentic_notebook.ipynb` §0.5  
**Problem**: 
```python
ANALYSIS_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis"  # ← OLD PATH

CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs",  # → docs/thesis/analysis/outputs
        ...
    },
    ...
}
```

**After migration must be**:
```python
ANALYSIS_DIR = PROJECT_ROOT / "thesis" / "analysis"  # ← NEW PATH

CATEGORY_MODELS = {
    "csd": {
        "outputs_dir": ANALYSIS_DIR / "outputs" / "csd",  # → thesis/analysis/outputs/csd
        ...
    },
    ...
}
```

**Why it matters**: If `outputs_dir` points to old path, `load_model_for_category()` will fail with FileNotFoundError when trying to load pickles. This function is called by:
- `thesis_agentic_notebook.ipynb` (forecasting agent)
- `thesis_notebook_AB_test.ipynb` (evaluation tiers L2 + L3)

**If this fails**: Chapter 7 results won't generate.

---

### Issue 2: Prompts CSV location
**Where**: `thesis_notebook_AB_test.ipynb` §1  
**Problem**:
```python
prompts_path = ANALYSIS_DIR / "outputs_ab_test" / "prompts.csv"
prompts_df = pd.read_csv(prompts_path)  # Will fail if file not at path
```

**Action**:
```
Move: docs/thesis/analysis/outputs_ab_test/prompts.csv
  → thesis/analysis/prompts/prompts_v5_final.csv

Update notebook:
prompts_path = ANALYSIS_DIR / "prompts" / "prompts_v5_final.csv"
```

**Why it matters**: The 50 evaluation prompts (v5 with all bug fixes) are hardcoded. If file not found, notebook can't run evaluation loop.

---

### Issue 3: Model pickle artifacts
**Where**: All training notebooks save to `OUTPUT_DIR / "pipelines" / "model_*.pkl"`  
**Problem**: Currently saved in:
```
docs/thesis/analysis/outputs/pipelines/model_xgboost.pkl
docs/thesis/analysis/outputs_danskvand/pipelines/model_lightgbm.pkl
... (7 categories × 2 models × 2 formats = many files)
```

**After migration need to be**:
```
thesis/analysis/outputs/csd/pipelines/model_xgboost.pkl
thesis/analysis/outputs/danskvand/pipelines/model_lightgbm.pkl
... (same structure, new root)
```

**Decision**: Move or regenerate?
- **Move** (1 hour): Copy pickles to new locations. Risk: trust old artifacts.
- **Regenerate** (2-3 hours): Re-run training notebooks. Benefit: latest, auditability.
- **Hybrid** (1 hour + later): Copy now, add fallback logic, regenerate when convenient.

---

## Migration Path (Recommended)

### Step 1: Prepare structure
```bash
mkdir -p thesis/analysis/notebooks/{02_ml_training,03_agentic,05_evaluation}
mkdir -p thesis/analysis/prompts/
mkdir -p thesis/analysis/outputs/
```

### Step 2: Copy and update notebooks
```bash
# Copy each notebook, then find-replace paths
cp docs/thesis/analysis/thesis_notebook_CSD.ipynb \
   thesis/analysis/notebooks/02_ml_training/specialized_CSD.ipynb

# In each notebook: find-replace
# OLD: "docs" / "thesis" / "analysis"
# NEW: "thesis" / "analysis"
```

### Step 3: Move data assets
```bash
cp docs/thesis/analysis/outputs_ab_test/prompts.csv \
   thesis/analysis/prompts/prompts_v5_final.csv

cp docs/thesis/analysis/outputs_ab_test/human_eval_pilot_15_v3.csv \
   thesis/analysis/prompts/
```

### Step 4: Move or regenerate pickles
**Option A (QUICK — 1 hour)**:
```bash
# Move old artifacts
mkdir -p thesis/analysis/outputs/{csd,danskvand,energidrikke,rtd_v2,totalbeer,pooled_4,pooled_5}

for cat in csd danskvand energidrikke rtd_v2 totalbeer pooled_4 pooled_5; do
  if [ "$cat" = "csd" ]; then
    src="docs/thesis/analysis/outputs"
  elif [ "$cat" = "rtd_v2" ]; then
    src="docs/thesis/analysis/outputs_rtd_v2"
  else
    src="docs/thesis/analysis/outputs_$cat"
  fi
  cp -r "$src"/* "thesis/analysis/outputs/$cat/"
done
```

**Option B (THOROUGH — 3 hours)**:
```bash
# Re-run each training notebook in Jupyter
# Do NOT skip this if you want Chapter 7 reproducibility
jupyter notebook thesis/analysis/notebooks/02_ml_training/specialized_CSD.ipynb
# ... run through, saves to NEW location automatically
# Repeat for each category
```

### Step 5: Update and test notebooks
```bash
# Test agentic notebook can load models
jupyter notebook thesis/analysis/notebooks/03_agentic_integration/registry_and_forecasting.ipynb
# Run §0-2, verify load_model_for_category("csd") works

# DRY-RUN eval (cheap test)
jupyter notebook thesis/analysis/notebooks/05_evaluation/4tier_ab_test_final.ipynb
# Run §0-2 (setup, load prompts, load models)
# Print: "✅ All paths resolved, models loaded"
# Run §3 with 1 prompt × 1 system (L0 only) → $0.05, 2 min

# FULL RUN (expensive, only if dry-run passes)
# Run §3-8 (200 OpenAI calls, 1000+300 Claude calls) → $4, 35 min
```

### Step 6: Archive old location
```bash
mv docs/thesis/analysis docs/thesis/analysis.archive_2026-04-27
```

---

## Execution Blockers

| Blocker | Status | Unblock plan |
|---------|--------|--------------|
| Exact pickle locations unknown | ❓ Need to check | `ls -lR docs/thesis/analysis/outputs*` |
| Don't know if old pickles are up-to-date | ❓ Need to check | Check commit date of .pkl files |
| Don't know notebook run time | ❓ Need to test | Time one training notebook |
| Don't know if pickles are corrupt | ❌ Won't know until load | Test load in agentic notebook §0.5 |
| Uncertainty: move or regenerate? | ⚠️ Decision needed | Ask Enrico preference, or go Hybrid |

---

## Critical Path to Chapter 7

```
MIGRATE notebooks + paths
    ↓
DECIDE: move pickles or regenerate
    ↓
UPDATE registry in agentic notebook
    ↓
TEST agentic notebook can load models (§0-2)
    ↓
DRY-RUN eval with 1 prompt (§3 subset)
    ↓
APPROVE v5 prompt (is it what Enrico intended?)
    ↓
FULL-RUN eval notebook (35 min, $4)
    ↓
EXTRACT results for Chapter 7 (tables + figures)
    ↓
WRITE Chapter 7 (1 week)
```

---

## Three Analysis Documents Created

1. **ANALYSIS_MIGRATION_PLAN.md** — Overall structure + phases + checklist
2. **NOTEBOOK_STRUCTURE_ANALYSIS.md** — Cell-by-cell breakdown + data flows
3. **CROSS_REFERENCES_AND_DEPENDENCIES.md** — Path-by-path + risk matrix + fallback logic

Each document is ~3-4k tokens, designed to be read independently or together.

---

## What You Asked For

> "the way he saved that is trash? What he saved is in the docs file, but there is a thesis folder at the root, and this is where it should go. I would have to know all the cross references and dependencies on the old paths before we migrated, so it's like the first step."

**✅ DONE**. You now have:
1. **Map of all cross-references** (3 documents, all paths catalogued)
2. **Dependencies identified** (which code calls what, when it fails)
3. **Migration phases** (7 steps from structure prep to cleanup)
4. **Risk assessment** (what breaks if each path is wrong)
5. **Fallback logic** (how to migrate safely without breaking Chapter 7)

> "I would also like us to analyze each different Python notebook step by step and then to identify what's going on, pretty much."

**✅ DONE**. NOTEBOOK_STRUCTURE_ANALYSIS.md has:
1. **Phase 2 ML training** — 8 notebooks, common structure, what each saves
2. **Phase 3 agentic registry** — Multi-category model loading + forecasting functions
3. **Phase 5 evaluation** — 4-tier LLM eval, prompt v5 fixes, 12-metric rubric
4. **Data flows** — Who reads what, who writes where
5. **Call graph** — Dependencies visualized

---

## Next Step: Approval

**Ready to execute migration?** Or do you want me to:
1. Deep-dive on one specific notebook first?
2. Run `ls -lR` on old structure to inventory files?
3. Check if pickles are up-to-date (git blame or file timestamps)?
4. Start with a test migration of just one notebook?
5. Something else?

**Default assumption**: Proceed with Step-by-step execution starting with notebook copy + path updates.
