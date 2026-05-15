---
created: 2026-05-07 10:00:00
updated: 2026-05-15 10:30:00
status: Phase 5 Ready (CSD EDA Canonical, Ready for Replication)
focus_detail: "CSD EDA consolidated: canonical pre_csd_eda.py established (bug fix: log_necessary default), 3 superseded scripts deleted, 6 planning docs consolidated into 1 reference doc + archive. Ready to replicate for Energidrikke, Danskvand, RTD in Phase 5."
---

# P0022: Preprocessing Pipeline Modularization

**Objective:** Refactor Nielsen preprocessing from monolithic into per-step, per-category independent scripts with shared utilities.

---

## Completed (Phase 1 ✅)

- ✅ 7 CSD step scripts (pre_csd_0 through pre_csd_6) + orchestrator
- ✅ Shared utilities: `terminal_utils.py`, `timing_utils.py`, `base_preprocessing.py`
- ✅ All fixes implemented: parquet caching, format casting, PATHS helpers, smart caching

---

## Completed (Phase 2 ✅)

**Data Folder Restructure (Steps 1-7: Complete)**
- ✅ Moved raw JSONL files → `thesis/data/raw/nielsen/data_jsonl/`
- ✅ Moved Stage 1 scripts → `thesis/data/converted/nielsen/jsonl_to_parquet/`
- ✅ Updated PATHS.py with new constants (THESIS_DATA_RAW_*, THESIS_DATA_CONVERTED_*)
- ✅ Updated all 5 legacy preprocessing_*.py scripts (hard-fail if Stage 1 cache missing)
- ✅ Updated Stage 1 README.md with new paths and diagram
- ✅ Fixed progress bar visibility (transient=True → keep_visible parameter in terminal_utils.py)
- ✅ CSD end-to-end testing: Stage 1 (36.1s), Stage 2 (3.3s), 78 brands, 3,354 rows output

**Testing Status (Updated 2026-05-14):**
- ✅ CSD: TESTED (Stage 1 + Stage 2)
- ✅ Danskvand: TESTED end-to-end (6.8s total pipeline, 20 brands after filtering)
- ✅ Energidrikke: TESTED end-to-end
- ✅ RTD: TESTED end-to-end
- ❌ Totalbeer: SKIPPED (missing facts table in source data)

## Completed (Phase 3 ✅)

**CSD EDA & Steps 2-6 Implementation**
- ✅ Created pre_csd_eda_and_parameter_analysis.py with 8 executable cells
- ✅ EDA executed: missing value analysis, brand stability, seasonal patterns, lag/rolling analysis
- ✅ Generated csd_eda_findings.json with empirically-justified parameters
- ✅ Step 2 (Build Calendar): Updated date range to 2026-04, tested → 6,149 rows
- ✅ Step 3 (Filter Series): MIN_PERIODS = 40 (thesis quality focus), tested → 2,666 rows (62 brands)
- ✅ Step 4 (Engineer Features): CSD-specific parameters with HOLIDAY_MONTHS={3,6,12} (different from default), tested → 23 features
- ✅ Step 5 (Apply Split): EDA-driven dates (TRAIN_END=2024-10, VAL_END=2025-04), tested → split applied
- ✅ Step 6 (Save Outputs): Generated feature matrix, series index, split dates, preprocessing report
- ✅ All steps tested end-to-end: 2.6s total pipeline time
- ✅ Feature matrix ready: 62 brands × 43 periods × 24 features (2,666 rows)

**Documentation Created:**
- ✅ 2026-05-14_DOC-monolithic-to-modularized-insights.md (12 core architectural insights)
- ✅ 2026-05-14_DOC-csd-eda-analysis-and-parameter-justification.md (EDA template)
- ✅ 2026-05-14_DOC-csd-eda-findings-populated.md (findings summary)

## Completed (Phase 4 — Bug Fix Pass ✅)

**Filename Case-Sensitivity & Schema Bugs Fixed (2026-05-14)**
- ✅ Fixed orchestrator cache existence checks: lowercase filenames in preprocessing_danskvand.py, preprocessing_rtd.py, preprocessing_totalbeer.py
  - Bug: checked for `Danskvand_clean_facts_v.parquet`, actual files are `danskvand_clean_facts_v.parquet` (Linux case-sensitive)
- ✅ Fixed Step 1 load scripts: hardcoded JSONL and parquet filenames now lowercase across Danskvand, RTD, Totalbeer
  - Affected: pre_danskvand_1_load_and_aggregate.py, pre_rtd_1_load_and_aggregate.py, pre_totalbeer_1_load_and_aggregate.py
- ✅ Fixed Step 1 aggregation schema mismatch: made sales_units_any_promo column optional
  - Bug: CSD has promo data; Danskvand/RTD/Totalbeer don't; script failed on KeyError
  - Fix: dynamically build agg_dict, fill promo_units with zeros if missing
- ✅ All 3 working categories verified end-to-end:
  - Danskvand: 6.8s total (20 brands after MIN_PERIODS=40 filter)
  - Energidrikke: PASS
  - RTD: PASS
- ⏭️ Totalbeer: SKIPPED (missing facts table in source JSONL)

## In Progress (Phase 5 — 4-Category EDA Replication 🔧)

**Next Steps (3 Working Categories):**
- [ ] Run EDA analysis for Energidrikke (pre_energidrikke_eda_and_parameter_analysis.py)
- [ ] Run EDA analysis for Danskvand (pre_danskvand_eda_and_parameter_analysis.py)
- [ ] Run EDA analysis for RTD (pre_rtd_eda_and_parameter_analysis.py)
- [ ] Replicate Steps 2-6 for each category with category-specific EDA parameters
- [ ] Create unified preprocessing_all.py master orchestrator (Phase 5 extension)
- [ ] Validate all 4 working categories produce expected engineered features

---

## Folder Structure (Target - Complete)

```
thesis/data/preprocessing/nielsen/
  ├─ shared/ (✅ complete + terminal_utils.py progress bar fix)
  │  ├─ __init__.py
  │  ├─ base_preprocessing.py
  │  ├─ terminal_utils.py (keep_visible parameter added)
  │  └─ timing_utils.py
  ├─ CSD/ (✅ tested end-to-end)
  ├─ Energidrikke/ (✅ orchestrator updated, ready for testing)
  ├─ Danskvand/ (✅ orchestrator updated, ready for testing)
  ├─ RTD/ (✅ orchestrator updated, ready for testing)
  ├─ Totalbeer/ (✅ orchestrator updated, ready for testing)
  └─ preprocessing_all.py (pending Phase 3)

thesis/data/raw/nielsen/
  └─ data_jsonl/ (✅ contains all JSONL source files)

thesis/data/converted/nielsen/
  ├─ jsonl_to_parquet/ (✅ Stage 1 scripts, ready for batch run)
  └─ parquet_nielsen/ (✅ Stage 1 cache by category, CSD populated)
```

---

## Success Criteria

✅ Per-step architecture: 7 scripts per category, each independent  
✅ Explicit variable naming: `OUTPUT_CALENDAR_FILLED_PARQUET` (not `OUT`)  
✅ Shared utilities: No duplication across 5 categories  
✅ Smart caching: Step 0 skipped if cache exists, auto-run if missing  
✅ Logging: Per-step JSON timing logs  
✅ Data folder 3-tier hierarchy: raw/ → converted/ → preprocessing/  
✅ Stage 1 & Stage 2 separation: JSONL parsing vs. feature engineering  
✅ Progress bar visibility: terminal_utils.py fixed (keep_visible parameter)  
✅ End-to-end tested: CSD category validated (36.1s Stage 1 + 3.3s Stage 2)  

---

## Phase 4-5 (Pending)

- [ ] **Phase 4 Extension:** Create `preprocessing_all.py` master orchestrator (run all 5 categories)
- [ ] **Phase 5:** Thesis documentation (parameter justification, EDA methodology guide, troubleshooting)

---

## Related Plans

- **P0017:** Notebook paths (blocked: awaiting P0022 stable outputs)
- **P0019:** Root docs boundary (paused: lower priority)

---

## Parallel Architecture (Legacy Monolithic Scripts) — 2026-05-09

The legacy monolithic preprocessing scripts at `thesis/data/preprocessing/preprocessing_*.py`
(still imported by `run_all_preprocessing.py`) were also refactored into a 2-stage
architecture this session, mirroring the same caching principle P0022 implements at finer granularity.

**Changes:**
- New folder: `thesis/data/preprocessing/jsonl_to_parquet/`
  - `convert_category.py` — parametric `--category` JSONL→Parquet converter, idempotent mtime check
  - `run_all_conversions.py` — loops all 5 categories; supports `--only`, `--force`; writes manifest
  - `README.md` — documents Stage 1 vs Stage 2 separation
- Removed `save_dimension_tables()` from legacy `preprocessing_csd.py` (moved to Stage 1)
- All 5 legacy scripts now read **only Parquet** (hard-fail with Stage 1 instructions if cache missing)
- No JSONL fallback in Stage 2 — clean dependency boundary

**Verification:**
- All 5 scripts pass `py_compile`, import cleanly, resolve to correct parquet paths
- `validate_input_data` hard-fail message smoke-tested

**Relationship to P0022:**
- P0022 modularizes one category into 7 step scripts (cache → load → calendar → filter → engineer → split → save)
- This parallel work leaves the legacy scripts monolithic but separates the cache step (same principle, coarser granularity)
- The two architectures coexist: P0022 modular under `nielsen/`, legacy monolithic in parent folder. `run_all_preprocessing.py` still drives the legacy path.
- When P0022 Phase 3 introduces `preprocessing_all.py` master orchestrator and the modular path becomes canonical, the legacy `preprocessing_*.py` and the standalone `jsonl_to_parquet/` folder can be retired together.

---

## Session Update (2026-05-12)

**What Was Verified and Fixed:**
1. **Plan verification** (per discipline rule): CSD orchestrator code reviewed; found Step 0 logic was correct in CSD (fixed in previous session), but Energidrikke/Danskvand/RTD/Totalbeer had incomplete refactoring (cache_exists() updated but old run_step() logic not removed). Non-blocking since Step 0 no longer in STEPS list.
2. **Progress bar investigation**: Determined transient=True was causing spinners to disappear. Fixed by adding keep_visible parameter (default True) to terminal_utils.py progress_bar(). Rich library works correctly when transient=False (keep_visible=True).
3. **Testing plan documented**: Identified 3–4 hours remaining for Phase 3 (Energidrikke, Danskvand, RTD, Totalbeer end-to-end validation).

## Note on Plan Accuracy

**Important:** Do NOT take plan documents at face value. Always verify implementation against actual code:
- Plans document intent; code is ground truth
- In-progress plans become stale quickly (flag changes discovered during execution)
- When verifying claims: check the actual script, not the plan description
- Update plan after discovering drift (this session verified orchestrator refactoring status and progress bar fix)

