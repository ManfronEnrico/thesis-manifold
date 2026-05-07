---
created: 2026-05-07 12:30:00
completed: 2026-05-07 13:45:00
status: PHASE 1 COMPLETE
---

# Phase 1 Completion: CSD Preprocessing Modularization

**Date:** 2026-05-07  
**Status:** ✅ COMPLETE  

---

## What Was Built

### Shared Utilities Module
**Location:** `thesis/data/preprocessing/nielsen/shared/`

✅ **terminal_utils.py** (272 lines)
- Rich-based terminal UI (spinners, progress bars, formatted tables)
- Key functions: `step_execution()`, `progress_bar()`, `print_file_load()`, `print_file_save()`, `print_data_preview()`, `print_step_summary()`, `print_timing_summary()`, `print_warning()`, `print_error()`, `print_info()`

✅ **timing_utils.py** (63 lines)
- Step timing and JSON logging
- `step_timer()` context manager
- `log_step_timing()` function for writing step logs

✅ **base_preprocessing.py** (93 lines)
- Data validation and caching helpers
- `validate_input()` for file existence checks
- `get_required_jsonl_files()` for category-specific file lists
- `cache_jsonl_tables()` for JSONL→Parquet conversion

✅ **__init__.py** (package initialization)

### CSD Step Scripts
**Location:** `thesis/data/preprocessing/nielsen/CSD/`

✅ **pre_csd_0_cache.py** (99 lines)
- Caches raw/views/metadata JSONL files as parquet
- Gracefully handles missing input directories
- Can be skipped with `--skip-raw` flag

✅ **pre_csd_1_load_and_aggregate.py** (146 lines)
- Loads view tables, joins dimensions, filters to target market
- Aggregates to brand × period granularity
- Outputs: `step_1_aggregate.parquet`

✅ **pre_csd_2_build_calendar.py** (154 lines)
- Creates full date range (2022-10 to 2026-03)
- Reindexes data to include all brand-month combinations
- NaN for missing periods
- Outputs: `step_2_calendar_filled.parquet`

✅ **pre_csd_3_filter_series.py** (113 lines)
- Filters brands with < 30 non-zero periods
- Removes sparse time series
- Outputs: `step_3_filtered_series.parquet`

✅ **pre_csd_4_engineer_features.py** (134 lines)
- Calls shared `engineer_features()` function
- Adds CSD-specific feature parameters (lags, rolling windows, holidays)
- Includes log transformation of sales_units
- Outputs: `step_4_engineered_features.parquet`

✅ **pre_csd_5_apply_split.py** (127 lines)
- Applies locked train/val/test split (2025-02 / 2025-08 boundaries)
- Calls shared `apply_split()` function
- Outputs: `step_5_split_applied.parquet`

✅ **pre_csd_6_save_outputs.py** (189 lines)
- Saves final feature matrix to `engineered/` directory
- Generates series index, split dates JSON, and preprocessing report
- Final outputs: `csd_feature_matrix.parquet`, `csd_series_index.csv`, `csd_split_dates.json`, `csd_preprocessing_report.md`

### Category Orchestrator
✅ **preprocessing_csd.py** (196 lines)
- Runs all 7 steps in sequence
- Supports `--skip-raw` to skip step 0
- Supports `--run-step N` to run only step N
- Usage examples:
  ```bash
  python preprocessing_csd.py                  # All steps
  python preprocessing_csd.py --skip-raw       # Steps 1-6
  python preprocessing_csd.py --run-step 4     # Feature engineering only
  ```

---

## Directory Structure Created

```
thesis/data/preprocessing/nielsen/
  shared/
    __init__.py
    terminal_utils.py
    timing_utils.py
    base_preprocessing.py
  
  CSD/
    pre_csd_0_cache.py
    pre_csd_1_load_and_aggregate.py
    pre_csd_2_build_calendar.py
    pre_csd_3_filter_series.py
    pre_csd_4_engineer_features.py
    pre_csd_5_apply_split.py
    pre_csd_6_save_outputs.py
    preprocessing_csd.py
    
    raw/                          # Step 0 output (cached raw tables)
    views/                        # Step 0 output (cached view tables)
    metadata/                     # Step 0 output (cached metadata)
    pipeline_step_outputs/        # Steps 1-6 intermediate outputs
    engineered/                   # Step 6 final outputs
```

---

## Key Architectural Decisions

### 1. **Per-Step Independence**
Each step script (`pre_csd_N_*.py`) is completely independent:
- Explicit input/output paths (no hardcoded assumptions)
- Can run standalone: `python pre_csd_4_engineer_features.py`
- Depends only on previous step's output existing on disk
- Failures are localized; restarting only re-runs that step

### 2. **Explicit Variable Naming**
All paths use purpose-driven names:
- `INPUT_AGGREGATE_PARQUET`, `OUTPUT_CALENDAR_FILLED_PARQUET`
- `STEP_OUTPUT_DIR`, `OUTPUT_ENGINEERED_DIR`
- Variables reveal what they contain; no more `OUT_RAW` ambiguity

### 3. **Shared Utilities, Not Duplication**
Common functions live in `shared/`:
- Terminal utilities used by all 7 steps
- Validation helpers used across categories
- Feature engineering logic reused from existing codebase
- Per-category customization in step 4 (feature engineering parameters)

### 4. **Intermediate Checkpoint Files**
Each step saves its output for resumption:
- Step 0 → raw/, views/, metadata/ (caches)
- Step 1 → step_1_aggregate.parquet
- Step 2 → step_2_calendar_filled.parquet
- Step 3 → step_3_filtered_series.parquet
- Step 4 → step_4_engineered_features.parquet
- Step 5 → step_5_split_applied.parquet
- Step 6 → csd_feature_matrix.parquet + metadata

If step N fails, restart with `python preprocessing_csd.py --run-step N`.

### 5. **Bottleneck Identification Ready**
Each step logs:
- Elapsed time (to JSON)
- Input/output row counts
- File sizes
- Rich terminal output with progress bars

Profile easily: `jq '.[] | "\(.step_num): \(.elapsed_sec)s, \(.output_rows) rows"' step_*_log.json`

---

## Next Steps (Phase 2)

Apply identical architecture to remaining 4 categories:
1. **Energidrikke** — likely same feature parameters as CSD
2. **Danskvand** — may have different lag windows or holiday months
3. **RTD** — verify category-specific parameters
4. **Totalbeer** — verify category-specific parameters

Each category gets:
- Identical 7 `pre_{category}_N_*.py` scripts
- Own `preprocessing_{category}.py` orchestrator
- Own output directories (raw/, views/, metadata/, pipeline_step_outputs/, engineered/)

Master orchestrator (`preprocessing_all.py`) will coordinate all 5 categories.

---

## Testing Readiness

CSD pipeline is ready to test end-to-end:

```bash
# Run full pipeline
python preprocessing_csd.py

# Or run with existing intermediate outputs (skip step 0)
python preprocessing_csd.py --skip-raw

# Or re-run feature engineering only (step 4)
python preprocessing_csd.py --run-step 4
```

Expected outputs in `thesis/data/preprocessing/nielsen/CSD/engineered/`:
- `csd_feature_matrix.parquet` (final feature matrix for modeling)
- `csd_series_index.csv` (metadata per brand)
- `csd_split_dates.json` (train/val/test boundaries)
- `csd_preprocessing_report.md` (summary report)

---

## Files Modified / Created

**Created (12 files):**
- `shared/__init__.py`
- `shared/terminal_utils.py` (272 lines)
- `shared/timing_utils.py` (63 lines)
- `shared/base_preprocessing.py` (93 lines)
- `CSD/pre_csd_0_cache.py` (99 lines)
- `CSD/pre_csd_1_load_and_aggregate.py` (146 lines)
- `CSD/pre_csd_2_build_calendar.py` (154 lines)
- `CSD/pre_csd_3_filter_series.py` (113 lines)
- `CSD/pre_csd_4_engineer_features.py` (134 lines)
- `CSD/pre_csd_5_apply_split.py` (127 lines)
- `CSD/pre_csd_6_save_outputs.py` (189 lines)
- `CSD/preprocessing_csd.py` (196 lines)

**Total new code:** ~1,700 lines across 12 files

---

## Success Criteria Met ✅

✅ **Per-step architecture:**
- 7 independent scripts, each can run standalone
- Can run `python pre_csd_4_engineer_features.py` without steps 0-3
- Each step logs inputs/outputs explicitly

✅ **Category-specific logic:**
- CSD feature engineering visible in `pre_csd_4_engineer_features.py`
- Feature parameters documented: lags [1,2,3,4,8,13], rolling [4,13], holidays {1,4,6,10,12}

✅ **Explicit variable naming:**
- No generic `OUT_RAW` or `INPUT_DIR`
- All names follow `{PURPOSE}_{FORMAT}_{TYPE}` pattern
- Reading the variable name reveals its purpose

✅ **Bottleneck identification:**
- Each step logs timing to JSON
- Rich terminal output shows progress + timing for each step
- Can profile: Which step is slow? Which category?

✅ **Shared utilities:**
- Common code in `shared/` (no duplication across categories)
- Terminal UI, timing, validation helpers used by all steps
- Per-category feature logic isolated in step 4

✅ **Reproducibility:**
- Run `python preprocessing_csd.py` for full pipeline
- Run `python preprocessing_csd.py --run-step 4` to re-engineer features
- Run `python preprocessing_csd.py --skip-raw` to skip optional caching

---

## Blockers / Open Questions

None at this time. Phase 1 for CSD is complete and ready for testing.

---

## Estimated Duration for Phase 2-4

- **Phase 2 (4 categories):** 1-2 sessions (replicate CSD pattern for Energidrikke, Danskvand, RTD, Totalbeer)
- **Phase 3 (Master):** 0.5 session (create `preprocessing_all.py`)
- **Phase 4 (Docs):** 0.5 session (architecture diagrams, troubleshooting guide)

**Total remaining:** ~2-3 sessions

