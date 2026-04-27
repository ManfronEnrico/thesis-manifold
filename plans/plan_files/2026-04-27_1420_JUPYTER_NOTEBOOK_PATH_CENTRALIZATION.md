---
created: 2026-04-27 14:20:00
updated: 2026-04-27 14:20:00
---

# Plan: Jupyter Notebook Path Centralization

**Objective**: Refactor all 10 Jupyter notebooks (Phase 2, 3, 5) to use centralized path management via `config.py` instead of hardcoded paths. This enables team-based collaboration (Brian + Enrico) with single-point-of-truth path updates.

---

## Current State (Problem)

- **10 notebooks** scattered across `thesis/analysis/notebooks/{02_ml_training,03_agentic,05_evaluation}/`
- **Hardcoded paths** in each notebook (e.g., `OUTPUT_DIR = PROJECT_ROOT / "docs" / "thesis" / "analysis" / "outputs"`)
- **Risk**: If paths change, all notebooks must be manually updated → coordination nightmare for 2 developers
- **No validation**: Notebooks silently fail or create wrong directories if paths are misconfigured

---

## Solution: Centralized Config Pattern

### config.py Structure

Single source of truth for all paths:

```python
ROOT_DIR = Path(__file__).parent
THESIS_DIR = ROOT_DIR / "thesis"
THESIS_ANALYSIS_DIR = THESIS_DIR / "analysis"
THESIS_OUTPUTS_DIR = THESIS_ANALYSIS_DIR / "outputs"

# Category-specific
CSD_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "csd"
CSD_FIGURES_DIR = CSD_OUTPUTS_DIR / "figures"

# ... repeat for all 7 categories (danskvand, energidrikke, rtd_v2, totalbeer, pooled_4, pooled_5)

# Feature matrices
FEATURE_MATRIX_OUTPUTS_DIR = THESIS_OUTPUTS_DIR / "feature_matrices"

# Data
THESIS_NIELSEN_DIR = THESIS_DATA_DIR / "nielsen"
# ... etc
```

### Notebook Setup Pattern (each notebook's §0)

```python
# 1. Find PROJECT_ROOT dynamically
from pathlib import Path
current = Path.cwd()
while current != current.parent:
    if (current / "CLAUDE.md").exists():
        PROJECT_ROOT = current
        break
    current = current.parent
else:
    raise FileNotFoundError("Could not find project root (CLAUDE.md)")

# 2. Add to sys.path
import sys
sys.path.insert(0, str(PROJECT_ROOT))

# 3. Import all paths from config
from config import *

# 4. Define category-specific paths
CSD_FEATURE_MATRIX = FEATURE_MATRIX_OUTPUTS_DIR / "csd_feature_matrix.parquet"
CSD_OUTPUTS = CSD_OUTPUTS_DIR
CSD_FIGURES = CSD_OUTPUTS_DIR / "figures"

# 5. Validate critical paths exist
if not CSD_OUTPUTS.exists():
    raise FileNotFoundError(f"CSD_OUTPUTS does not exist: {CSD_OUTPUTS}\nCheck config.py paths.")

# 6. Auto-create subdirectories on first use (figures)
CSD_FIGURES.mkdir(parents=True, exist_ok=True)
```

### Benefits

1. **Single source of truth**: Change `config.py` once, all notebooks follow
2. **Team-friendly**: No coordination needed when paths move
3. **Explicit validation**: Fails loudly if paths are misconfigured
4. **Auto-creation**: Subdirectories (figures) created on first write, main outputs must exist
5. **Self-documenting**: Variable names (`CSD_OUTPUTS`, `CSD_FIGURES`) are explicit

---

## Execution Plan

### Phase 1: Finalize config.py (DONE)
- [x] Define all category-specific output directories
- [x] Define feature matrix directory
- [x] Define data directories (Nielsen, Indeks, assessment)
- [x] Add validation that paths are importable

### Phase 2: Update all 10 notebooks (paths + rename)
- [ ] **Phase 2 training notebooks (8)** — update paths + rename for clarity:
  - [ ] specialized_CSD.ipynb → (rename TBD)
  - [ ] specialized_danskvand.ipynb → (rename TBD)
  - [ ] specialized_energidrikke.ipynb → (rename TBD)
  - [ ] specialized_rtd.ipynb → (rename TBD)
  - [ ] specialized_totalbeer.ipynb → (rename TBD)
  - [ ] pooled_4.ipynb → (rename TBD)
  - [ ] pooled_5.ipynb → (rename TBD)
  - [ ] comparison.ipynb → (rename TBD)

- [ ] **Phase 3 agentic notebook (1)** — update paths + rename:
  - [ ] registry_and_forecasting.ipynb → (rename TBD)

- [ ] **Phase 5 evaluation notebook (1)** — update paths + rename:
  - [ ] 4tier_ab_test_final.ipynb → (rename TBD)

### Phase 3: Testing & Validation
- [ ] Run each training notebook §0 setup, verify all paths resolve
- [ ] Run agentic notebook §0-2, verify load_model_for_category() works
- [ ] Run eval notebook §0-2, verify prompts load
- [ ] Dry-run eval (1 prompt × L0 tier, ~$0.05, 2 min)
- [ ] Full eval run (if dry-run passes)

### Phase 4: Documentation
- [ ] Update MESSAGE_TO_BRIAN.md if it references old paths
- [ ] Create thesis/analysis/README.md describing new structure
- [ ] Commit all changes with clear message

---

## Key Decisions Made

| Decision | Choice | Why |
|----------|--------|-----|
| **Figure location** | Category-specific (`outputs/{category}/figures/`) | Self-contained, scalable, no coordination needed |
| **Directory auto-creation** | Auto-create figures, validate main outputs exist | Fail loudly on misconfiguration, smooth first-run experience |
| **Variable naming** | `{CATEGORY}_{TYPE}` (e.g., `CSD_OUTPUTS`, `CSD_FIGURES`) | Explicit, self-documenting, no ambiguity |
| **Import pattern** | `from config import *` + `importlib.reload()` | Kernels must reload after config.py changes |

---

## Blockers & Mitigations

| Blocker | Status | Mitigation |
|---------|--------|------------|
| Kernel reload required after config changes | ⚠️ Known | Document: restart kernel or use `importlib.reload(config)` |
| Feature matrix parquet doesn't exist yet | ⚠️ Expected | Validate parent dir exists, not the file itself |
| Old pickles in wrong location | ⏳ Pending | Decision: move vs regenerate (affects Phase 3 timeline) |
| Paths differ between Brian & Enrico's machines | ⚠️ Risk | Mitigated: CLAUDE.md-relative discovery + config.py centralization |

---

## Cross-References

- **Current state analysis**: docs/analyses/2026-04-27_1535_NOTEBOOK_STRUCTURE_ANALYSIS.md
- **Migration plan** (old structure → new): docs/analyses/2026-04-27_1534_MIGRATION_QUICK_REFERENCE.md
- **Config.py**: C:\dev\thesis-manifold\config.py
- **First notebook updated**: thesis/analysis/notebooks/02_ml_training/specialized_CSD.ipynb

---

## Next Actions

1. **For Brian** (during this session):
   - Finish updating all 8 training notebooks (Phase 2)
   - Test agentic notebook setup (Phase 3)
   - Document in this plan if decisions change

2. **For Claude Code** (in future sessions):
   - Reference this plan before making config/notebook changes
   - Update `updated: YYYY-MM-DD HH:MM:SS` when plan changes
   - Create outcome file in `plans/outcome_files/` when phase completes

3. **For team (Brian + Enrico)**:
   - Sync on pickles decision: move vs regenerate?
   - Run full eval once all paths are updated
   - Extract Chapter 7 results

---

## Notebook Naming & Folder Structure

**Current state**: Notebooks have poor descriptive names (`specialized_CSD.ipynb`, `pooled_4.ipynb`, etc.)

**Renaming scope**:
- Phase 2 & 3 & 5 notebooks need better names that describe their actual purpose
- Rename decisions: TBD during Phase 2 execution

**Folder renaming (DEFERRED)**:
- Current folders: `02_ml_training/`, `03_agentic/`, `05_evaluation/`
- These folder names are also non-descriptive and tied to phase numbers
- **Decision**: Folder reorganization deferred to a separate chore branch after paths are centralized
- **Why**: Folder changes would require coordination across team + git history complexity
- **Future**: Plan a dedicated `chore/folder-reorganization` branch to rename both folders and update all references

## Questions to Resolve

- [ ] What should each notebook be renamed to? (descriptive, purpose-driven names)
- [ ] Should feature matrices be per-category or global?
- [ ] Move old pickles or regenerate models from scratch?
- [ ] Should old `docs/thesis/analysis/` be archived or deleted?

