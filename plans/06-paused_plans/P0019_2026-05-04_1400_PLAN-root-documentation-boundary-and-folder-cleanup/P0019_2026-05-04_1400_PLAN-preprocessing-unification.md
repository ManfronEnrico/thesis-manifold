---
created: 2026-05-04 14:00:00
updated: 2026-05-07 16:25:00
status: Paused — Lower Priority Infrastructure Work
paused_reason: "Renamed from 'Preprocessing Pipeline Unification' to reflect actual scope: documentation boundary enforcement + auto-folder-relocation. Paused pending completion of P0022 (preprocessing modularization) and P0017 (notebook paths). Will resume once higher-priority work stabilizes."
---

# Plan: Root Documentation Boundary & Folder Cleanup (P0019)

**P-ID:** P0019  
**Created:** 2026-05-04 14:00  
**Status:** Paused (Infrastructure work, lower priority)

---

## Objective

Create infrastructure rules + skills to enforce documentation boundary:
1. **Rule:** `root-documentation-boundary.md` — prevent root clutter (docs → `docs/`, `plans/`, etc.)
2. **Skill:** `/move-docs-to-folders` — auto-detect and relocate misplaced markdown files
3. **Skill enhancement:** `/docs-update-all` — add violation detection

**Why this plan exists:** P0019's original title ("Preprocessing Pipeline Unification") was misleading. Phases 1-3 were actually preprocessing work (now part of P0022). Phase 4 is actually about documentation organization (different concern).

---

## Scope

### Phase 4 Only (Paused)
- [ ] Create rule file: `.claude/rules/root-documentation-boundary.md`
- [ ] Create skill: `/move-docs-to-folders` (auto-relocation)
- [ ] Update skill: `/docs-update-all` (detection + enforcement)

### Already Complete (Phases 1-3)
- ✅ Preprocessing scripts (now P0022)
- ✅ Unified runner (now part of P0022)
- ✅ Path centralization (done in P0022)

---

## Why Paused

This is **infrastructure work**, not core to thesis delivery:
- P0022 (preprocessing modularization) has higher priority
- P0017 (notebook paths) blocks on P0022
- Documentation cleanup is useful but non-blocking

**Resume when:** P0022 Phase 2-4 complete (~3-4 more hours) and the pipeline is stable.

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

