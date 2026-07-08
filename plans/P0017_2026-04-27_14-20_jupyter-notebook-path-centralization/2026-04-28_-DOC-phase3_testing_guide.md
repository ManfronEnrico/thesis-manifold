# Phase 3: Testing & Validation — Quick Guide

**Status**: Ready to start  
**Estimated time**: 15-30 minutes (quick test) or 2-3 hours (full validation)  
**What you'll do**: Verify notebooks can import from config.py without errors

---

## Quick Test (< 15 minutes)

### Test Setup Cell (§0) in Each Notebook

1. **Open Jupyter**:
   ```bash
   jupyter notebook
   ```

2. **Open first training notebook**:
   - Navigate to: `thesis/analysis/notebooks/SRQ_1/specialized_danskvand.ipynb`

3. **Run cell §0** (config import):
   - Click cell §0
   - Press `Shift+Enter` to run
   - **Expected output**:
     ```
     ✓ Project root: C:\dev\thesis-manifold
     ✓ Thesis outputs: C:\dev\thesis-manifold\thesis\analysis\outputs
     ```
   - **If error**: Check if PROJECT_ROOT discovery works (CLAUDE.md exists in parent dirs)

4. **Run cell §3** (category setup for training notebook):
   - Click cell §3
   - Press `Shift+Enter` to run
   - **Expected output**:
     ```
     ✓ DANSKVAND outputs: C:\dev\thesis-manifold\thesis\analysis\outputs\danskvand
     ✓ DANSKVAND figures: C:\dev\thesis-manifold\thesis\analysis\outputs\danskvand\figures
     ```

5. **Repeat for 2-3 other notebooks** to spot-check:
   - `specialized_CSD.ipynb`
   - `specialized_energidrikke.ipynb`
   - One pooled notebook

---

## Special Cases

### Agentic Notebook (`registry_and_forecasting.ipynb`)

**After running §0, check cells §1-§2:**

1. Look for a cell containing `CATEGORY_MODELS` dictionary
2. Check if model paths are hardcoded (e.g., `"docs/thesis/analysis/outputs/csd"`)
3. If found, they should be replaced with config variables:

**Before**:
```python
CATEGORY_MODELS = {
    "csd": {"outputs_dir": "C:/dev/thesis-manifold/docs/thesis/analysis/outputs_csd"},
    "danskvand": {"outputs_dir": "..."},  # more hardcoded paths
}
```

**After**:
```python
CATEGORY_MODELS = {
    "csd": {"outputs_dir": CSD_OUTPUTS_DIR},
    "danskvand": {"outputs_dir": DANSKVAND_OUTPUTS_DIR},
    # ... continue for all 7 categories
}
```

**Testing**: Run cells §0-§2 to verify model registry loads without errors.

### Evaluation Notebook (`4tier_ab_test_final.ipynb`)

**After running §0, check cells §1-§3:**

1. Look for lines with hardcoded prompt file paths (e.g., `"docs/thesis/analysis/outputs_ab_test/prompts.csv"`)
2. Should be replaced with config paths:

**Before**:
```python
prompts_path = Path("C:/dev/thesis-manifold/docs/thesis/analysis/outputs_ab_test/prompts.csv")
```

**After**:
```python
prompts_path = THESIS_ANALYSIS_DIR / "prompts" / "prompts_v5_final.csv"
```

**Testing**: Run cells §0-§2 to verify prompts load successfully.

---

## Full Validation (if quick test passes)

### Dry-Run Evaluation

Once §0 setup works for all notebooks, you can test the full pipeline:

1. **Open**: `thesis/analysis/notebooks/SRQ_2_and_3/4tier_ab_test_final.ipynb`
2. **Run cells §0-§3** (setup + prompt loading)
3. **Find the cell that runs the evaluation** (usually cell §4 or later)
4. **Modify to run only 1 prompt** from the lowest tier (L0):
   ```python
   # In the eval loop, add:
   prompts_to_eval = [prompts[0]]  # Just the first prompt
   # Or:
   for i, prompt in enumerate(prompts[:1]):  # Just run 1
       # ... evaluation code
   ```
5. **Run it**:
   - Should take ~2 minutes
   - Should cost ~$0.05
   - Should print results without errors

---

## Troubleshooting

### Error: `FileNotFoundError: Could not find project root (CLAUDE.md)`

**Cause**: Notebook can't find CLAUDE.md above its current directory  
**Fix**: Check that you're running Jupyter from within the project folder:
```bash
# Wrong:
cd thesis/analysis/notebooks
jupyter notebook

# Right:
cd C:/dev/thesis-manifold
jupyter notebook
```

### Error: `{CATEGORY}_OUTPUTS_DIR does not exist`

**Cause**: Category output directory missing  
**Fix**: Check that the directory exists:
```bash
ls -la thesis/analysis/outputs/csd  # Example for CSD
# Should see: pipelines/, figures/, etc.
```

### Error: `ModuleNotFoundError: No module named 'config'`

**Cause**: sys.path doesn't include project root  
**Fix**: Make sure cell §0 runs successfully before cell §3:
- Run cell §0 first
- Check console output for "✓ Project root" message
- Then run cell §3

### Kernel Stuck/Slow After Running Setup

**Cause**: Jupyter kernel cache not cleared after config.py changes  
**Fix**: Restart the kernel:
- Menu: `Kernel → Restart Kernel`
- Or: Press `Ctrl+Shift+P`, type "restart kernel"

---

## Verification Checklist

### Quick Test (§0-§3)
- [ ] Cell §0 runs without FileNotFoundError
- [ ] Cell §0 prints paths successfully (✓ symbols appear)
- [ ] Cell §3 runs without FileNotFoundError
- [ ] Cell §3 prints category paths (✓ symbols appear)

### Special Notebooks
- [ ] Agentic notebook (§0-§2) loads CATEGORY_MODELS without errors
- [ ] Evaluation notebook (§0-§3) loads prompts without errors

### Full Validation (if quick test passes)
- [ ] Dry-run evaluation runs for 1 prompt
- [ ] Dry-run completes without errors
- [ ] Dry-run costs ~$0.05 and takes ~2 minutes

---

## Expected Output Examples

### Training Notebook (§0 + §3)

```
✓ Project root: C:\dev\thesis-manifold
✓ Thesis outputs: C:\dev\thesis-manifold\thesis\analysis\outputs
✓ DANSKVAND outputs: C:\dev\thesis-manifold\thesis\analysis\outputs\danskvand
✓ DANSKVAND figures: C:\dev\thesis-manifold\thesis\analysis\outputs\danskvand\figures
```

### Agentic Notebook (§0-§2)

```
✓ Project root: C:\dev\thesis-manifold
✓ Thesis outputs: C:\dev\thesis-manifold\thesis\analysis\outputs

Loading models from registry...
✓ CSD model loaded: csd_pipeline.pkl
✓ DANSKVAND model loaded: danskvand_pipeline.pkl
... (all 7 categories loaded)
```

### Evaluation Notebook (§0-§3)

```
✓ Project root: C:\dev\thesis-manifold
✓ Thesis outputs: C:\dev\thesis-manifold\thesis\analysis\outputs

Loading prompts...
✓ Loaded 15 prompts from: thesis/analysis/prompts/prompts_v5_final.csv
Ready for evaluation.
```

---

## When to Create Outcome File

Create `plans/03-outcome_plans/2026-04-28_JUPYTER_PATH_CENTRALIZATION_PHASE3_COMPLETE.md` after:
- ✅ All notebooks pass quick test (§0-§3 run without errors)
- ✅ Agentic notebook verified (§0-§2 works)
- ✅ Evaluation notebook verified (§0-§3 works)
- ✅ Dry-run passes (optional but recommended)

---

## Next Actions After Phase 3

If all tests pass:

1. **Pickles Decision**:
   - [ ] Move old pickles from `docs/thesis/analysis/outputs_{category}` to new locations
   - [ ] OR: Regenerate pickles by running training notebooks

2. **Full Evaluation**:
   - [ ] Run full evaluation (all prompts, all tiers)
   - [ ] Extract results for thesis

3. **Cleanup** (separate branch):
   - [ ] Notebook renaming (descriptive names instead of `pooled_4.ipynb`)
   - [ ] Folder reorganization (rename `02_ml_training/` to descriptive name)
   - [ ] Archive old `docs/thesis/analysis/` structure

---

## Reference

- **Phase 2 Outcome**: `plans/03-outcome_plans/2026-04-28_JUPYTER_PATH_CENTRALIZATION_PHASE2_COMPLETE.md`
- **Config File**: `config.py` (root)
- **Notebooks**: `thesis/analysis/notebooks/{SRQ_1,SRQ_2_and_3}/`

