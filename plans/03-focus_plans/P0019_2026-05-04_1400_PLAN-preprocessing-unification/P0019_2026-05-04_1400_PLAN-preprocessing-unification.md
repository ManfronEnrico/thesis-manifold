---
created: 2026-05-04 14:00:00
updated: 2026-05-07
status: Focus — Phase 3 Complete, Phase 4 Pending
focus_detail: "Phases 1-3 done (path centralization, unified runner, documentation). Phase 4 pending: Create root-documentation-boundary rule + /move-docs-to-folders skill"
---

# Plan: Preprocessing Pipeline Unification

**P-ID:** P0019  
**Created:** 2026-05-04 14:00  
**Status:** In Progress

---

## Objective

Unify 5 independent preprocessing scripts (CSD, energidrikke, danskvand, RTD, totalbeer) into a single coordinated pipeline with:
1. Centralized path handling via paths.py
2. Dynamic root discovery (CLAUDE.md pattern)
3. Unified runner script for batch execution
4. Complete documentation and testing

---

## Scope

### In Scope
- Preprocessing scripts (5 category variants)
- Unified runner (run_all_preprocessing.py)
- Path centralization (save_all_datasets.py + paths.py alignment)
- Testing & validation
- Documentation (analysis, test reports)

### Out of Scope
- Feature engineering logic (shared library, not modified)
- Notebook integration (separate from pipeline)
- Database schema changes

---

## Key Decisions

1. **CSV-first approach:** Scripts assume CSV data pre-downloaded via save_all_datasets.py
2. **No SQL fallback:** Decouples preprocessing from database credentials
3. **Unified runner:** Single command orchestrates all 5 categories in sequence
4. **Error handling:** Graceful failure reporting with manifest output

---

## Phases

### Phase 1: Path Centralization (COMPLETE)
- [x] Fix save_all_datasets.py output path (parents[2] → parents[1])
- [x] Verify alignment with paths.py THESIS_DATA_NIELSEN_CSV_DIR
- [x] Delete obsolete SQL variants (preprocessing.py, preprocessing_csd_old.py)

### Phase 2: Unified Runner (COMPLETE)
- [x] Create run_all_preprocessing.py with error handling
- [x] Update all 6 scripts to use dynamic root discovery + importlib.reload
- [x] Implement manifest generation with per-category timing
- [x] Test execution (all 5 categories pass)

### Phase 3: Documentation (COMPLETE)
- [x] Create PREPROCESSING_ANALYSIS.md
- [x] Create TEST_REPORT_PREPROCESSING.md
- [x] Validate output files generated
- [x] Move documentation to plan folder (this plan)

### Phase 4: Rules & Skills (PENDING)
- [ ] Create rule: root-documentation-boundary.md
- [ ] Update rule: trigger-docs-workflow.md (add doc placement rules)
- [ ] Create skill: /move-docs-to-folders (auto-relocate root docs)
- [ ] Update skill: /docs-update-all (detect violations)

---

## Supporting Documentation

- `2026-05-04_DOC-preprocessing-analysis.md` — Architecture analysis & path flow
- `2026-05-04_DOC-test-report.md` — Test execution results & output validation

---

## Status Tracking

**Completed:**
- Path centralization & save_all_datasets.py fix
- Unified runner implementation
- All 5 preprocessing scripts tested & working
- Documentation & testing

**In Progress:**
- Rule/skill updates for future doc organization

**Next:**
- Implement root-documentation-boundary rule
- Create /move-docs-to-folders skill
- Enhance /docs-update-all with violation detection

