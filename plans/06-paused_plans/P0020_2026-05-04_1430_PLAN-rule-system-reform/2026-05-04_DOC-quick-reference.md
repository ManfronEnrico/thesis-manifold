# P0020 Quick Reference — Rule System Reform

**Plan:** `plans/02-in_progress-plans/P0020_2026-05-04_1430_PLAN-rule-system-reform/`

---

## TL;DR

Reform scattered 10 rule files → 4 core rules + 1 memory conventions file + 5 enforcement skills.

**Timeline:** 7-8 sessions, one phase per session  
**Token savings:** ~35% in rules  
**Zero behavioral coverage loss guaranteed** (Scenario Test all compressions)

---

## Quick Checklist (Copy to Session Start)

### Phase 1: Reclassify + Consolidate Conventions
```
- [ ] Audit table (rule-reform-implementation.md Task 1.1)
- [ ] convention_project_standards.md created
- [ ] MEMORY.md updated
```

### Phase 2: Prose Compression
```
- [ ] root-documentation-boundary.md compressed (126 → ~85)
- [ ] trigger-branch-strategy.md compressed (78 → ~55)
- [ ] Scenario tests pass
```

### Phase 3: Move Procedures to Skills
```
- [ ] git-draft-commit SKILL.md updated
- [ ] docs-update-all SKILL.md verified
- [ ] Empty rule files deleted
```

### Phase 4: Priority Hierarchy
```
- [ ] rule-priority-hierarchy.md created
- [ ] CLAUDE.md reorganized by tier
```

### Phase 5: Build Validators (4 skills)
```
- [ ] /validate-plan-ids
- [ ] /audit-plan-outcomes
- [ ] /audit-cross-references
- [ ] /sync-memory-indices
```

### Phase 6: Master Skill
```
- [ ] /enforce-repo-cleanliness orchestrator
```

### Phase 7: Update Navigation
```
- [ ] CLAUDE.md rules section reorganized
- [ ] CHEATSHEET.md updated
```

### Phase 8: Final Validation
```
- [ ] Structural integrity check
- [ ] Cross-references verified
- [ ] /enforce-repo-cleanliness runs successfully
- [ ] Completion report
```

---

## Key Documents

| Document | Purpose | Access |
|---|---|---|
| **P0020 Full Plan** | Complete spec + rationale + all 8 phases | `P0020_2026-05-04_1430_PLAN-rule-system-reform.md` (this folder) |
| **Gap Analysis** | 7 specific gaps identified | `docs/reference/rule-reform-gaps.md` |
| **Implementation Guide** | Task-by-task roadmap | `docs/reference/rule-reform-implementation.md` |
| **Task List** | 8 session-based tasks | TaskCreate #1-8 in this session |

---

## Key Decisions Made

1. **Next P-ID: P0020** — Assigned 2026-05-04 14:30
2. **Phase-per-session model** — One phase = one session (1-2 weeks to complete)
3. **Scenario Test approach** — Compression is lossy; must test all edge cases
4. **Enforcement-first enforcement** — Every rule gets a skill (not just enforcement via rules)
5. **Master skill as entry point** — `/enforce-repo-cleanliness` orchestrates all checks

---

## References

**Based on:** jlacour-git's Rule System Reform  
**Framework:** Lateral reclassification + Priority hierarchy + Prose compression  
**Your adaptation:** `/move-docs-to-folders` skill (already built correctly)

**Across sessions, reference this plan as: P0020**

---

## Next Step

When ready to start, approve and begin Phase 1:
- Read full plan file
- Execute audit (Task 1.1)
- Create convention_project_standards.md
- Update MEMORY.md

Session end: Mark Task #1 `in_progress` → `completed`, move to Task #2 (Phase 2)
