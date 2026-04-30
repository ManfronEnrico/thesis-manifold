# Jupyter Path Centralization — Quick Summary for Session

**Goal**: Refactor ~20 Jupyter notebooks to use centralized `config.py` paths instead of hardcoded paths.

**Status**: 
- Phase 1 (config.py) ✅ DONE
- Phase 2 (refactor notebooks) 🔄 START NOW
- Phase 3 (validation) ⏳ After Phase 2

---

## What's the Problem?

Notebooks have hardcoded paths like:
```python
OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs_csd"
```

When paths change, all 20 notebooks must be manually updated. This is a coordination nightmare for 2 developers.

---

## The Solution

**config.py** (already created at project root) defines all paths once:

```python
ROOT_DIR = Path(__file__).parent
THESIS_DIR = ROOT_DIR / "thesis"
THESIS_ANALYSIS_DIR = THESIS_DIR / "analysis"
THESIS_OUTPUTS_DIR = THESIS_ANALYSIS_DIR / "outputs"

# Category outputs
CSD_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "csd"
DANSKVAND_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "danskvand"
# ... (all 7 categories)

# Feature matrices
FEATURE_MATRIX_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "feature_matrices"

# Data
THESIS_NIELSEN_DIR = THESIS_DATA_DIR / "nielsen"
# ... etc
```

**Each notebook imports from config.py** (in cell §0):

```python
# 1. Find PROJECT_ROOT (search for CLAUDE.md)
from pathlib import Path
current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        PROJECT_ROOT = current
        break
    current = current.parent

# 2. Add to sys.path
import sys
sys.path.insert(0, str(PROJECT_ROOT))

# 3. Import all paths from config
from config import *

# 4. Define category-specific local vars (optional)
CSD_OUTPUTS = CSD_OUTPUTS_DIR
CSD_FIGURES = CSD_OUTPUTS_DIR / "figures"
CSD_FIGURES.mkdir(parents=True, exist_ok=True)

# 5. Validate
if not CSD_OUTPUTS.exists():
    raise FileNotFoundError(f"CSD_OUTPUTS does not exist: {CSD_OUTPUTS}")
```

**Result**: Change one path in config.py → all notebooks follow automatically.

---

## Phase 2: What to Do (TODAY)

### 1. Copy notebooks to new structure
```bash
mkdir -p thesis/analysis/notebooks/{02_ml_training,03_agentic,05_evaluation}
mkdir -p thesis/analysis/prompts/
mkdir -p thesis/analysis/outputs/{csd,danskvand,energidrikke,rtd_v2,totalbeer,pooled_4,pooled_5}
```

### 2. Copy all 10 notebooks from old location to new:
```bash
# 8 training notebooks → thesis/analysis/notebooks/02_ml_training/
cp docs/thesis/analysis/thesis_notebook_CSD.ipynb thesis/analysis/notebooks/02_ml_training/specialized_CSD.ipynb
cp docs/thesis/analysis/thesis_notebook_danskvand.ipynb thesis/analysis/notebooks/02_ml_training/specialized_danskvand.ipynb
# ... (repeat for all 8)

# 1 agentic notebook → thesis/analysis/notebooks/03_agentic/
cp docs/thesis/analysis/thesis_agentic_notebook.ipynb thesis/analysis/notebooks/03_agentic/registry_and_forecasting.ipynb

# 1 eval notebook → thesis/analysis/notebooks/05_evaluation/
cp docs/thesis/analysis/thesis_notebook_AB_test.ipynb thesis/analysis/notebooks/05_evaluation/4tier_ab_test_final.ipynb
```

### 3. Copy data assets:
```bash
cp docs/thesis/analysis/outputs_ab_test/prompts.csv thesis/analysis/prompts/prompts_v5_final.csv
cp docs/thesis/analysis/outputs_ab_test/human_eval_pilot_15_v3.csv thesis/analysis/prompts/human_eval_pilot_15_v3.csv
```

### 4. Update each notebook's cell §0 to use config.py pattern (see template above)

### 5. Replace all hardcoded paths:

**For ALL notebooks**:
- `PROJECT_ROOT / "docs" / "thesis" / "analysis"` → `PROJECT_ROOT / "thesis" / "analysis"`

**For training notebooks** (8):
- `OUTPUT_DIR = ... / "outputs_csd"` → `OUTPUT_DIR = CSD_OUTPUTS_DIR`
- `OUTPUT_DIR = ... / "outputs_danskvand"` → `OUTPUT_DIR = DANSKVAND_OUTPUTS_DIR`
- ... (repeat for all 7 categories)

**For agentic notebook**:
- Update `CATEGORY_MODELS` registry to new paths:
  ```python
  CATEGORY_MODELS = {
      "csd": {"outputs_dir": THESIS_OUTPUTS_DIR / "csd"},
      "danskvand": {"outputs_dir": THESIS_OUTPUTS_DIR / "danskvand"},
      # ... etc
  }
  ```

**For eval notebook**:
- `prompts_path = ... / "outputs_ab_test" / "prompts.csv"` → `prompts_path = THESIS_ANALYSIS_DIR / "prompts" / "prompts_v5_final.csv"`
- `OUTPUT_DIR = ... / "outputs_ab_test"` → `OUTPUT_DIR = THESIS_OUTPUTS_DIR / "ab_test_v5"`

---

## Phase 3: Validation

1. Open each notebook in Jupyter
2. Run §0 (setup) — should succeed with no FileNotFoundError
3. Verify paths print correctly
4. For agentic: Run §0-2, verify `load_model_for_category()` works
5. For eval: Run §0-2, verify prompts load

---

## Pickles Decision (PENDING)

**Current state**: Old pickles are in `docs/thesis/analysis/outputs{_category}/`

**Two options**:
- **Option A: MOVE** (1 hr) — Copy old pickles to new locations
  ```bash
  cp docs/thesis/analysis/outputs/pipelines/* thesis/analysis/outputs/csd/pipelines/
  ```
  
- **Option B: REGENERATE** (3 hrs) — Run each training notebook to create new pickles in new locations

**Recommendation**: MOVE (faster, validated models)

---

## Success Criteria

- ✅ All 20 notebooks import from config.py
- ✅ No hardcoded "docs/thesis/analysis" paths remain
- ✅ Agentic notebook loads all models without FileNotFoundError
- ✅ Eval notebook loads prompts without FileNotFoundError
- ✅ Dry run passes (1 prompt, ~$0.05, 2 min)

---

## Reference Docs

- **Detailed step-by-step**: `docs/analyses/2026-04-27_1534_MIGRATION_QUICK_REFERENCE.md`
- **Full plan**: `plans/02-in_progress-plans/2026-04-27_1420_JUPYTER_NOTEBOOK_PATH_CENTRALIZATION.md`
- **config.py**: `C:\dev\thesis-manifold\config.py` (already created)

---

## Important Reminders

1. **Do NOT merge main yet** — finish this work first
2. **Kernel reload**: After config.py changes, restart Jupyter kernel
3. **Create outcome file** when Phase 2+3 complete
4. **Notebook renaming is TBD** — focus on paths first, rename later

---

**Ready to start? Begin with step Phase 2.1 (create directories)**
