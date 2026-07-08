---
created: 2026-05-07 14:15:00
title: P0022 Task Summary & Workflow
type: reference
---

# P0022 Tasks Summary

**Total Tasks Created:** 13 (Tasks #9-21)  
**Status:** All pending, ready for execution  
**Workflow:** Sequential (fixes first, then phases)

---

## 🔴 BLOCKING FIXES (Do These First)

### Priority 1: Format Errors
- **Task #10** — Fix period_month format error (int casting) — **5 min**
  - File: `pre_csd_1_load_and_aggregate.py`
  - Also check: `pre_csd_2_build_calendar.py` for similar issues

### Priority 2: Optimization
- **Task #9** — Load from parquet cache if available (else JSONL) — **15 min**
  - File: `pre_csd_1_load_and_aggregate.py`
  - Benefit: ~10x speed improvement (15s → 2s)

### Priority 3: Code Quality
- **Task #11** — Add PATHS.py helpers (get_category_preprocessing_scripts_dir, get_category_pipeline_step_outputs_dir) — **20 min**
  - File: `PATHS.py`
  - Update: `preprocessing_csd.py` + all 7 step scripts

### Priority 4: UX Improvement
- **Task #12** — Make --skip-raw default (only run with --run-raw flag) — **10 min**
  - File: `preprocessing_csd.py`

**Total Fix Time: ~50 minutes**

---

## ✅ TESTING (After Fixes)

### Task #13
**Phase 1.5: Test CSD pipeline end-to-end**
- Run full pipeline: `python preprocessing_csd.py`
- Verify all 7 steps complete
- Check outputs exist in `engineered/` directory
- Document test results
- **Estimated: 30 minutes** (including any debugging)

---

## 🚀 PHASE 2: Replicate for Other Categories

**Prerequisite:** Task #13 must pass (CSD working flawlessly)

### Task #14 — Energidrikke
- Replicate 7-step architecture from CSD template
- Create: pre_energidrikke_0 through pre_energidrikke_6 + preprocessing_energidrikke.py
- Verify category parameters
- Test end-to-end
- **Estimated: 45 min** (using CSD as template)

### Task #15 — Danskvand
- Same as Energidrikke
- **Estimated: 45 min**

### Task #16 — RTD
- Same as Energidrikke
- **Estimated: 45 min**

### Task #17 — Totalbeer
- Same as Energidrikke
- **Estimated: 45 min**

**Total Phase 2 Time: ~3 hours** (all 4 categories)

---

## 🔗 PHASE 3: Master Orchestrator

**Prerequisite:** Tasks #14-17 must pass (all 5 categories working)

### Task #18 — preprocessing_all.py
- Create master orchestrator at `thesis/data/preprocessing/nielsen/preprocessing_all.py`
- Orchestrate all 5 categories in sequence
- Support flags: `--categories CSD RTD`, `--run-step 4`, `--run-raw`
- Final summary with per-category timing
- **Estimated: 1 hour**

---

## 📚 PHASE 4: Documentation

**Prerequisite:** Task #18 must pass (master orchestrator working)

### Task #19 — Step Dependency Graph
- Create visual diagram showing:
  - 7-step data flow
  - Dependencies (step N → step N+1)
  - Checkpoint files
  - Resumption points
- Format: PNG or ASCII diagram
- **Estimated: 30 min**

### Task #20 — Category Parameter Reference
- Create comparison table:
  - Feature lag windows per category
  - Rolling window periods
  - Holiday months definition
  - min_periods threshold
  - Train/val/test split dates
- Side-by-side table (CSD, Energidrikke, Danskvand, RTD, Totalbeer)
- Document rationale for differences
- **Estimated: 45 min**

### Task #21 — Troubleshooting Guide
- "Which step is slow?" — profiling tips
- "How to restart from step N" — command examples
- "Output rows mismatch" — debugging checklist
- "Memory per step" — monitoring guide
- "Common errors" — solutions
- **Estimated: 1 hour**

**Total Phase 4 Time: ~2.25 hours**

---

## 📊 Overall Timeline

| Phase | Tasks | Status | Time Est. | Priority |
|-------|-------|--------|-----------|----------|
| **Fixes** | #10, #9, #11, #12 | 🔴 BLOCKING | 50 min | **NOW** |
| **Test** | #13 | ⏳ PENDING | 30 min | After fixes |
| **Phase 2** | #14-17 | ⏳ PENDING | 3 hours | After Phase 1.5 ✅ |
| **Phase 3** | #18 | ⏳ PENDING | 1 hour | After Phase 2 ✅ |
| **Phase 4** | #19-21 | ⏳ PENDING | 2.25 hours | After Phase 3 ✅ |
| **TOTAL** | 13 tasks | 🔴 IN PROGRESS | **~6.75 hrs** | Sequential |

---

## 🎯 Execution Checklist

### Session 1: Fixes & Testing (Today)
```
[ ] Task #10: Fix format error (5 min)
    [ ] Apply to pre_csd_1_load_and_aggregate.py
    [ ] Test: python pre_csd_1_load_and_aggregate.py
    
[ ] Task #9: Load from parquet cache (15 min)
    [ ] Modify load_and_aggregate() function
    [ ] Add fallback logic
    [ ] Test with --run-raw first, then default
    
[ ] Task #11: Add PATHS.py helpers (20 min)
    [ ] Add 2 new helper functions to PATHS.py
    [ ] Update preprocessing_csd.py
    [ ] Update all 7 pre_csd_N_*.py scripts
    
[ ] Task #12: Make --skip-raw default (10 min)
    [ ] Update preprocessing_csd.py arg parser
    [ ] Update run_step() logic
    [ ] Test: python preprocessing_csd.py (should skip step 0)
    
[ ] Task #13: End-to-end testing (30 min)
    [ ] Run full pipeline
    [ ] Check all outputs
    [ ] Document results
```

### Session 2+: Phases 2-4
```
[ ] Task #14-17: Replicate for 4 categories (3 hours)
    [ ] Energidrikke
    [ ] Danskvand
    [ ] RTD
    [ ] Totalbeer
    
[ ] Task #18: Master orchestrator (1 hour)
    [ ] Create preprocessing_all.py
    [ ] Test end-to-end
    
[ ] Task #19-21: Documentation (2.25 hours)
    [ ] Step dependency graph
    [ ] Parameter reference table
    [ ] Troubleshooting guide
```

---

## 📝 How to Track Progress

1. **Before starting a task:** `TaskUpdate --taskId X --status in_progress`
2. **After completing a task:** `TaskUpdate --taskId X --status completed`
3. **View current status:** `TaskList`

Example:
```
TaskUpdate --taskId 10 --status in_progress
# ... do work ...
TaskUpdate --taskId 10 --status completed
```

---

## 🔗 Related Documents

- [2026-05-07_DOC-fixes-and-next-steps.md](2026-05-07_DOC-fixes-and-next-steps.md) — Detailed fix instructions
- [2026-05-07_DOC-phase1-csd-completion.md](2026-05-07_DOC-phase1-csd-completion.md) — What was built in Phase 1
- [P0022_2026-05-07_1000_PLAN-preprocessing-pipeline-modularization.md](P0022_2026-05-07_1000_PLAN-preprocessing-pipeline-modularization.md) — Full plan

