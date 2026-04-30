---
created: 2026-04-27 14:20:00
updated: 2026-04-30 10:15:00
status: PHASE 3 IN PROGRESS — Manual notebook-by-notebook setup
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

## Execution Plan

### Phase 1: Finalize config.py (✅ DONE)
- [x] Define all category-specific output directories
- [x] Define feature matrix directory
- [x] Define data directories (Nielsen, Indeks, assessment)
- [x] Add validation that paths are importable

### Phase 2: Update all 10 notebooks — ROLLED BACK (Manual Approach)
**Status**: Phase 2 was attempted via automated agent refactoring but rolled back per Brian's direction (2026-04-30).

**Reason**: To maintain consistency with colleague's naming conventions and avoid breaking changes, all notebook setup must be done manually by Brian with Claude's guidance, cross-referencing against `config.py` each time.

**New approach (Phase 2 REVISED)**:
- [ ] Notebook-by-notebook manual setup with Claude guidance
- [ ] Brian provides screenshots/code excerpts
- [ ] Claude cross-references `config.py` and suggests fixes
- [ ] Brian executes the setup changes
- [ ] Process repeats for each notebook

**Notebooks to update (10 total)**:
1. [ ] `thesis/analysis/notebooks/SRQ_1/specialized_CSD.ipynb`
2. [ ] `thesis/analysis/notebooks/SRQ_1/specialized_danskvand.ipynb`
3. [ ] `thesis/analysis/notebooks/SRQ_1/specialized_energidrikke.ipynb`
4. [ ] `thesis/analysis/notebooks/SRQ_1/specialized_rtd.ipynb`
5. [ ] `thesis/analysis/notebooks/SRQ_1/specialized_totalbeer.ipynb`
6. [ ] `thesis/analysis/notebooks/SRQ_1/pooled_4.ipynb`
7. [ ] `thesis/analysis/notebooks/SRQ_1/pooled_5.ipynb`
8. [ ] `thesis/analysis/notebooks/SRQ_1/comparison.ipynb`
9. [ ] `thesis/analysis/notebooks/SRQ_2_and_3/registry_and_forecasting.ipynb`
10. [ ] `thesis/analysis/notebooks/SRQ_2_and_3/4tier_ab_test_final.ipynb`

### Phase 3: Testing & Validation
- [ ] Run each training notebook §0 setup, verify all paths resolve
- [ ] Run agentic notebook §0-2, verify load_model_for_category() works
- [ ] Run eval notebook §0-2, verify prompts load

---

## Next Actions

1. **For Brian** (Phase 2 REVISED — this session):
   - Work notebook-by-notebook with Claude
   - Share screenshot/code of current setup cell
   - Accept Claude's cross-reference advice
   - Execute the recommended changes
   - Move to next notebook when done

2. **For Claude Code** (in future sessions):
   - Reference this plan before making config/notebook changes
   - Cross-reference `config.py` for every notebook update
   - Create outcome file when phase completes
