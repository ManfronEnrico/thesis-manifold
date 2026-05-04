# P0020 Plan Readiness Checklist

**Date**: 2026-05-04  
**Status**: ✅ READY FOR EXECUTION  
**Target Session**: Next session (Phase 1 approval needed)

---

## Plan Structure Verification

✅ **P0020 Plan Files Complete**
- [x] Main plan file: `P0020_2026-05-04_1430_PLAN-rule-system-reform.md` (432 lines)
- [x] Quick reference: `2026-05-04_DOC-quick-reference.md` (115 lines)
- [x] P0021 integration guide: `2026-05-04_DOC-p0021-integration.md` (339 lines)
- [x] Plan folder: `plans/02-in_progress-plans/P0020_2026-05-04_1430_PLAN-rule-system-reform/`

✅ **PLANS_INDEX.md Updated**
- [x] P0020 registered in "In Progress" section
- [x] Metadata correct: P0020 | 2026-05-04 | 1430 | Rule System Reform | In Progress
- [x] Summary statistics updated: 5 in-progress plans (P0005, P0017–P0018, P0019–P0020)
- [x] Total plans: 20 (4 backlog + 5 in-progress + 6 outcomes + 5 archive)

---

## Documentation & Dependencies

✅ **Reference Documentation Linked**
- [x] `docs/reference/rule-reform-gaps.md` — Gap analysis (7 gaps identified)
- [x] `docs/reference/rule-reform-implementation.md` — Detailed implementation roadmap
- [x] `.claude/rules/` — All current rule files present (10 files to be reorganized)
- [x] `.claude/skills/` — Existing skills ready (move-docs-to-folders, docs-update-all enhanced)

✅ **P0021 (Docs Reorganization) Integration**
- [x] P0021 marked COMPLETE in outcomes
- [x] P0021 integration guide created (2026-05-04_DOC-p0021-integration.md)
- [x] P0020 Dependencies section updated to reference P0021
- [x] All 8 task descriptions updated with P0021 context
- [x] Routing table authority: `.claude/rules/root-documentation-boundary.md`

✅ **Framework & Resources**
- [x] jlacour-git framework understood (lateral reclassification, priority hierarchy, prose compression)
- [x] Scenario testing approach documented
- [x] Enforcement skill pattern established (via /move-docs-to-folders example)
- [x] Token savings target defined: ~35% (3,500 → 2,300 tokens)

---

## Task System

✅ **All 8 Tasks Created & Updated**
- [x] Task #1: Phase 1 — Reclassify + consolidate conventions (P0021-integrated)
- [x] Task #2: Phase 2 — Prose compression + scenario testing (P0021-integrated)
- [x] Task #3: Phase 3 — Move procedures to skills (P0021-integrated)
- [x] Task #4: Phase 4 — Priority hierarchy (P0021-integrated)
- [x] Task #5: Phase 5 — Build 4 validators (P0021-integrated)
- [x] Task #6: Phase 6 — Build master orchestrator (P0021-integrated)
- [x] Task #7: Phase 7 — Update CLAUDE.md navigation (P0021-integrated)
- [x] Task #8: Phase 8 — Final validation (P0021-integrated)

**Status**: All pending, awaiting Phase 1 approval

---

## Execution Plan

✅ **8 Phases (One Per Session)**

| Phase | Duration | Task | Deliverables |
|-------|----------|------|---|
| 1 | 1-2 sessions | Reclassify + consolidate | Audit table, convention_project_standards.md, MEMORY.md updated |
| 2 | 1 session | Prose compression | Compressed rules, scenario tests passed |
| 3 | 1 session | Move procedures → skills | Updated SKILL.md files, empty rule files deleted |
| 4 | 0.5 sessions | Priority hierarchy | rule-priority-hierarchy.md, CLAUDE.md reorganized |
| 5 | 2-3 sessions | Build validators | 4 new skills (/validate-plan-ids, /audit-plan-outcomes, /audit-cross-references, /sync-memory-indices) |
| 6 | 1 session | Build master skill | /enforce-repo-cleanliness orchestrator |
| 7 | 0.5 sessions | Update navigation | CLAUDE.md, CHEATSHEET.md finalized |
| 8 | 1 session | Final validation | Validation report, completion sign-off |

**Total Duration**: 7-8 sessions (estimated)

---

## Success Metrics

✅ **Defined & Measurable**

| Metric | Before | Target | Status |
|--------|--------|--------|--------|
| Rule files | 10 | 4 core | Planned |
| Tokens in rules | ~3,500 | ~2,300 (-35%) | Target set |
| Enforcement skills | 1 | 6 (5 validators + 1 master) | Planned |
| Behavioral coverage | — | 100% (zero loss) | Scenario testing defined |
| Cross-ref integrity | Manual | Automated (/audit-cross-references) | Planned |
| P0021 compliance | — | Enforced in Phase 8 | Integration guide ready |

---

## Risk Mitigation

✅ **All Risks Identified & Mitigations Planned**

| Risk | Impact | Mitigation Status |
|---|---|---|
| Compression removes needed detail | High | Scenario testing defined (7 compressions tested in jlacour-git) |
| Procedures moved incorrectly | High | Verification checklist in Phase 3 |
| Cross-references break | High | grep + manual verification in Phase 8 |
| Behavioral coverage lost | Critical | Scenario Test all compressions, Phase 8 validation |
| New enforcement skills have bugs | Medium | Test each independently before Phase 6 integration |

---

## Related Plans Status

| Plan | Status | Integration | Notes |
|------|--------|-------------|-------|
| P0019 | In Progress | Independent | Preprocessing pipeline unification (separate track) |
| P0021 | ✅ Complete | FEEDS P0020 | Docs reorganization (4-folder structure now authority) |
| P0018 | In Progress | Independent | Plan restructuring (completed 2026-04-28) |
| P0017 | In Progress | Independent | Jupyter path centralization (Phase 3 manual) |

---

## Pre-Execution Checklist

**Before Phase 1 Begins**:
- [ ] User reviews P0020 full plan and approves
- [ ] User reviews P0021 integration guide and confirms P0021 is authority
- [ ] User confirms 8 tasks with P0021 context are acceptable
- [ ] User approves proceeding with Phase 1

**When Phase 1 Starts**:
- [ ] Mark Task #1 as `in_progress`
- [ ] Execute Phase 1 steps (audit, create convention_project_standards.md, update MEMORY.md)
- [ ] Mark Task #1 as `completed` when phase finishes
- [ ] Begin Phase 2 (or wait for next session)

---

## Quick Links

**Plan Files**:
- Full plan: `plans/02-in_progress-plans/P0020_2026-05-04_1430_PLAN-rule-system-reform/P0020_2026-05-04_1430_PLAN-rule-system-reform.md`
- Quick reference: `2026-05-04_DOC-quick-reference.md` (in same folder)
- P0021 integration: `2026-05-04_DOC-p0021-integration.md` (in same folder)

**Supporting Reference**:
- Gap analysis: `docs/reference/rule-reform-gaps.md`
- Implementation guide: `docs/reference/rule-reform-implementation.md`
- P0021 outcome: `plans/03-outcome_plans/P0021_2026-05-04_1400_OUTCOME-docs-reorganization/`

**Authority Documents**:
- Root boundary rule (P0021 enforcement): `.claude/rules/root-documentation-boundary.md`
- Current rules (to be refactored): `.claude/rules/` (10 files)
- Existing enforcement skills: `.claude/skills/move-docs-to-folders/`, `.claude/skills/docs-update-all/`

---

## Sign-Off

**Plan Structure**: ✅ COMPLETE  
**Dependencies**: ✅ ALL VERIFIED  
**Tasks**: ✅ ALL CREATED & UPDATED  
**Documentation**: ✅ ALL CURRENT  
**P0021 Integration**: ✅ COMPLETE  

**Status**: READY FOR EXECUTION (Phase 1 approval needed)

---

**Prepared**: 2026-05-04  
**Next Action**: User approves Phase 1 → Mark Task #1 in_progress → Execute Phase 1

