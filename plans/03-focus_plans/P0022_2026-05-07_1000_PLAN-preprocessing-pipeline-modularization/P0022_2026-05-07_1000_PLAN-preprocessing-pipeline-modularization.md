---
created: 2026-05-07 10:00:00
updated: 2026-05-12 16:20:00
status: Phase 2 Complete (Data Restructure + CSD Testing), Phase 3 Ready (4-Category Validation)
focus_detail: "Data folder fully restructured into 3-tier hierarchy (raw/ → converted/ → preprocessing/). Stage 1 & 2 scripts migrated and tested. CSD end-to-end validated (36.1s Stage 1, 3.3s Stage 2). Progress bar fix applied (transient=True → keep_visible parameter). Ready to test remaining 4 categories (Energidrikke, Danskvand, RTD, Totalbeer). ~3–4 hours remaining for Phase 3 validation."
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

**Testing Status:**
- ✅ CSD: TESTED (Stage 1 + Stage 2)
- ⏳ Energidrikke: Ready for testing
- ⏳ Danskvand: Ready for testing
- ⏳ RTD: Ready for testing
- ⏳ Totalbeer: Ready for testing

## In Progress (Phase 3 🔧)

**Remaining Work:**
- [ ] Run `python thesis/data/converted/nielsen/jsonl_to_parquet/run_all_conversions.py` (Stage 1 for 4 categories)
- [ ] Test Stage 2 legacy scripts: `python preprocessing_energidrikke.py`, etc.
- [ ] Test Stage 2 modular orchestrators (per-category, if deploying)
- [ ] Verify all categories produce expected engineered features
- [ ] Compare outputs with previous preprocessing baseline (optional but recommended)

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

## Phase 3-4 (Pending)

- [ ] **Phase 3:** Create `preprocessing_all.py` master orchestrator
- [ ] **Phase 4:** Documentation (parameter reference, troubleshooting guide)

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

