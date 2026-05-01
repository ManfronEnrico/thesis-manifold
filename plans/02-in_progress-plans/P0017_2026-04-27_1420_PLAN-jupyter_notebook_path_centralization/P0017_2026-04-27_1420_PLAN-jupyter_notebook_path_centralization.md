---
created: 2026-04-27 14:20:00
updated: 2026-05-01 10:45:00
status: PHASE 2 IN PROGRESS — Dynamic path helper + comparison.ipynb template
---

# Plan: Jupyter Notebook Path Centralization (P0017)

**Objective**: Refactor all 10 Jupyter notebooks to use centralized, dynamically-computed paths via `paths.py`. Enable team collaboration (Brian + Enrico) with single-point-of-truth path management + proper folder hierarchy (each notebook self-contained with outputs).

---

## Structural Decisions (2026-05-01)

### Folder Hierarchy (NEW)
`
thesis/
  modelling/
    notebooks/
      SRQ_1/
        comparison/
          comparison.ipynb
          comparison_outputs/
            all_notebooks_comparison_outputs/
              headline_table.csv
              pool_vs_spec.csv
              figures/
                fig_headline.png
                fig_pool_vs_spec_heatmap.png
              chapter6_table.md
        specialized_CSD/
          specialized_CSD.ipynb
          specialized_CSD_outputs/
            all_models_metrics.csv
            predictions_val_all.parquet
            figures/
        [... other notebooks, same pattern]
      SRQ_2_and_3/
        [same structure]
  data/
  literature/
  thesis-agents/
  thesis-context/
    formal-requirements/
  thesis-writing/
    [NOTE: junk-drawer folders (analysis/, figures/) — cleanup deferred to Phase 4]
    sections-drafts/
    sections-final/
`

### paths.py Refactoring (✅ DONE)
- Removed hardcoded category/output paths (CSD_OUTPUTS_DIR, etc.)
- Kept only **core directories**: ROOT_DIR, THESIS_MODELLING_DIR, THESIS_DATA_DIR
- Added **helper function**: `get_upstream_notebook_outputs_dir(notebook_name, srq_id)`
- **Directory creation**: Moved from paths.py → each notebook's § 0.0 cell
  - paths.py is **definitions only** (no side effects, no mkdir calls)
  - Each notebook creates its own `OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)` in § 0.0 after defining paths
  - This makes dependencies explicit and ensures directories exist only when notebooks run

---

## Current State (2026-05-01)

### ✅ Completed
- [x] Refactored `paths.py` — clean, only core paths
- [x] Updated `comparison.ipynb` § 0.0-0.4:
  - § 0.0: Find ROOT_DIR via CLAUDE.md, import paths
  - § 0.1: Define notebook identity (SRQ_ID, FOLDER_NAME, NOTEBOOK_NAME)
  - § 0.2: Compute paths dynamically
  - § 0.3: Helper function `get_upstream_notebook_outputs_dir()`
  - § 0.4: Test existence + graceful missing-data warning
- [x] Created template for specialized notebooks (§ 0.0-0.3)

### ⏳ In Progress
- [ ] Fix `comparison.ipynb` § 1-5 (still uses old undefined variables)

### ⏭️ Next Phase
1. Finalize comparison.ipynb § 1-5
2. Apply template to 7 specialized notebooks
3. Apply template to 2 pooled notebooks
4. Apply template to 2 SRQ_2_and_3 notebooks

---

## Issues & Resolutions

### Upstream outputs missing
- **Cause**: 7 upstream notebooks not yet run
- **Fix**: Graceful warning added in § 0.4
- **Next**: Run upstream notebooks first

### thesis-writing cleanup deferred
- Junk drawers: `analysis/`, `figures/` (unclear sources)
- **Decision**: Fix notebook paths first (Phase 2-3), audit thesis-writing later (Phase 4)

---

---

## Phase 2B: Preprocessing Pipeline Refactoring (2026-05-01)

### Current Work: Nielsen Data Preprocessing

**Objective**: Refactor Enrico's preprocessing pipeline to:
1. Use `paths.py` for all directory references (no hardcoded paths)
2. Read from local raw_* CSV folders (no Nielsen connector needed at runtime)
3. Write to per-category subfolders in `preprocessing/parquet_*`
4. Include data validation + helpful error messages
5. Scale to 5+ beverage categories (one script per category)

### ✅ Completed
- [x] Created `preprocessing_csd.py` with dynamic root finder + paths.py integration
- [x] Added data validation (checks for required CSV files; helpful error messages)
- [x] Tested end-to-end with real Nielsen data
- [x] Updated paths.py with `THESIS_DATA_PREPROCESSING_PARQUET_NIELSEN_DIR`, SPSS equivalents
- [x] Created `requirements.txt` documenting dependencies (pandas, numpy, pyarrow, tabulate)
- [x] Created `VERIFICATION_GUIDE.md` with step-by-step success checklist
- [x] Code review: Verified feature engineering pipeline (no data leakage, deterministic)

### 🔍 Code Review Findings (2026-05-01)

**Status**: Technical implementation is sound, but **design choices lack documented justification**.

**Created**: Handover document for Enrico at `docs/handovers/2026-05-01_HANDOVER-enrico-preprocessing-code-review.md`

**Key Questions Raised** (no answers yet):
1. **Lag selection (1,2,3,4,8,13)**: Based on ACF analysis? Domain knowledge? Universal across categories?
2. **Rolling windows (4,13)**: Why these specific windows? Why rolling_std only for w=4?
3. **Holiday months {1,4,6,10,12}**: Why exclude Jul–Aug (summer peak)? Validated via sales data?
4. **min_periods=30**: Data-driven threshold or arbitrary rule?
5. **Train/val/test split (2025-02, 2025-08)**: Do all categories have complete 2019–2025 data?
6. **Category-specific columns**: How do CSV filenames vary? (csd_clean_* vs. danskvand_clean_*?)
7. **Promo intensity**: Denominator clipped to 1; why? Intentional or bug?

**Action**: Waiting for Enrico to provide rationale before scaling to danskvand, energidrikke, rtd, totalbeer.

### ⏳ Blocked Until Enrico Responds
- [ ] Clarify feature engineering design choices (see handover document)
- [ ] Confirm data coverage per category (do they all span 2019–2025?)
- [ ] Confirm CSV filename conventions (category-specific or shared?)

### ⏭️ Once Cleared
1. Restructure `parquet_nielsen/` to per-category subfolders (matching notebook folder names):
   ```
   parquet_nielsen/
     specialized_CSD/
       specialized_CSD_feature_matrix.parquet
       series_index.csv
       split_dates.json
       preprocessing_report.md
     specialized_danskvand/
       specialized_danskvand_feature_matrix.parquet
       series_index.csv
       split_dates.json
       preprocessing_report.md
     specialized_energidrikke/
       ...
     specialized_rtd/
       ...
     specialized_totalbeer/
       ...
   ```
2. Update `preprocessing_csd.py` to write to `OUT / NOTEBOOK_NAME /` where NOTEBOOK_NAME = "specialized_CSD"
3. Create `preprocessing_danskvand.py`, `preprocessing_energidrikke.py`, etc. (duplicates with per-category overrides)
4. Test all 5 scripts end-to-end
5. Update notebooks to load from per-category folders

### Handover Documents
- `docs/handovers/2026-05-01_HANDOVER-enrico-preprocessing-code-review.md` — Detailed code review + questions

---

## Notes
- **Template**: See comparison.ipynb § 0.0-0.4
- **Helper**: `get_upstream_notebook_outputs_dir()` in § 0.4
- **Naming**: `{NOTEBOOK_NAME}_outputs/` for each notebook
- **Preprocessing**: Blocked awaiting Enrico's design rationale (see handover document)
