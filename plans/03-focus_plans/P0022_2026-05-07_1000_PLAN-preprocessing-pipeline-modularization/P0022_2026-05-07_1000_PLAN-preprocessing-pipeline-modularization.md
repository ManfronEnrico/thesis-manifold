---
created: 2026-05-07 10:00:00
updated: 2026-05-09 14:50:00
status: Phase 1 Complete, Phase 2 In Progress (Orchestrator Bug Fixed)
focus_detail: "Modular nielsen/ orchestrators ready to test. Parallel work 2026-05-09: legacy monolithic preprocessing_*.py scripts also separated into Stage 1 (jsonl_to_parquet/ cache) + Stage 2 (parquet-only feature engineering)."
---

# P0022: Preprocessing Pipeline Modularization

**Objective:** Refactor Nielsen preprocessing from monolithic into per-step, per-category independent scripts with shared utilities.

---

## Completed (Phase 1 ✅)

- ✅ 7 CSD step scripts (pre_csd_0 through pre_csd_6) + orchestrator
- ✅ Shared utilities: `terminal_utils.py`, `timing_utils.py`, `base_preprocessing.py`
- ✅ All fixes implemented: parquet caching, format casting, PATHS helpers, smart caching

---

## In Progress (Phase 2 🔧)

**Status:** All 4 categories configured (Energidrikke, Danskvand, RTD, Totalbeer)

**Bug Fixed (2026-05-07 17:30):**
- Orchestrators had inverted Step 0 logic (skipped when cache missing)
- Fixed: Now auto-runs Step 0 if cache doesn't exist (no `--run-raw` needed for first run)
- Applied to: CSD, Energidrikke, Danskvand, RTD, Totalbeer

**Caching Strategy (Actual Implementation):**
```
--run-raw        Force step 0 (re-cache existing or new)
(default)        Smart: skip step 0 if cache exists, auto-run if missing
```

**Next Steps:**
- [ ] Run `python preprocessing_energidrikke.py` (auto-runs step 0, creates cache)
- [ ] Repeat for Danskvand, RTD, Totalbeer
- [ ] Verify all categories produce expected parquet outputs
- [ ] Compare outputs with previous preprocessing runs

---

## Folder Structure (Target - On Track)

```
thesis/data/preprocessing/nielsen/
  ├─ shared/ (✅ created)
  │  ├─ __init__.py
  │  ├─ base_preprocessing.py
  │  ├─ terminal_utils.py
  │  └─ timing_utils.py
  ├─ CSD/ (✅ tested)
  ├─ Energidrikke/ (🔧 orchestrator fixed)
  ├─ Danskvand/ (🔧 orchestrator fixed)
  ├─ RTD/ (🔧 orchestrator fixed)
  ├─ Totalbeer/ (🔧 orchestrator fixed)
  └─ preprocessing_all.py (pending Phase 3)
```

---

## Success Criteria

✅ Per-step architecture: 7 scripts per category, each independent  
✅ Explicit variable naming: `OUTPUT_CALENDAR_FILLED_PARQUET` (not `OUT`)  
✅ Shared utilities: No duplication across 5 categories  
✅ Smart caching: Step 0 skipped if cache exists, auto-run if missing  
✅ Logging: Per-step JSON timing logs  

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

## Note on Plan Accuracy

**Important:** Do NOT take plan documents at face value. Always verify implementation against actual code:
- Plans document intent; code is ground truth
- In-progress plans become stale quickly (flag changes discovered during execution)
- When verifying claims: check the actual script, not the plan description
- Update plan after discovering drift (this session fixed orchestrator logic after finding inverted Step 0 check)

