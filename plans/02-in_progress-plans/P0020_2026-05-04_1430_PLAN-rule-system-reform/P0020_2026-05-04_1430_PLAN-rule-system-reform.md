---
created: 2026-05-04 14:30:00
updated: 2026-05-04 14:30:00
status: In Progress
---

# P0020: Rule System Reform — Enforceable, Concise, Effective Rules

**Plan ID:** P0020  
**Created:** 2026-05-04 14:30  
**Status:** In Progress  
**Duration:** 7-8 sessions (estimated)

---

## Objective

Reform your rule system from scattered, verbose enforcement to a **concise, enforceable, effective** system with:
- **4 core rules** (trust tier only) in `.claude/rules/`
- **7 consolidated conventions** in memory (facts about your project)
- **5 enforcement skills** (automate rule compliance)
- **1 master skill** (`/enforce-repo-cleanliness`) orchestrating all checks

**Outcome:** Zero behavioral coverage loss, ~35% token savings in rules, explicit priority hierarchy for conflict resolution.

**Reference:** Based on jlacour-git's Rule System Reform framework (danielmiessler/Personal_AI_Infrastructure#908)

---

## Context & Rationale

### The Problem
Your rule system grew organically to ~10 rule files, consuming ~3,500 tokens with scattered procedures, conventions, and routing entries all competing for attention. Result: instruction fatigue → reduced compliance despite having good rules.

### The Framework (jlacour-git)
Three transformation approaches:
1. **Lateral reclassification** — "Is this actually a rule?" (Rules vs. Procedures vs. Conventions vs. Routing)
2. **Priority hierarchy** — Trust > Correctness > Quality > Efficiency (resolve conflicts)
3. **Prose compression** — Scenario Test + Walkthrough Test (no behavioral coverage loss)

### Your Existing Work
You've already built `/move-docs-to-folders` skill correctly, demonstrating the pattern:
- Detect violations automatically
- Suggest fixes
- Move enforcement to a skill, not a rule

---

## Scope

### In Scope
- Reclassify all ~10 rule files (RULE vs. PROCEDURE vs. CONVENTION vs. ROUTING)
- Move procedures to skill SKILL.md files (git-commit workflow, docs workflow)
- Consolidate all conventions into single memory file
- Compress rules with scenario testing (keep all behavioral coverage)
- Add explicit priority hierarchy to rules
- Build 4 new enforcement skills (validate-plan-ids, audit-plan-outcomes, audit-cross-references, sync-memory-indices)
- Build 1 master `/enforce-repo-cleanliness` skill (orchestrates all checks)
- Update CLAUDE.md to reflect new structure

### Out of Scope
- Changing actual rule behaviors (only reorganizing)
- Modifying hooks (keep as-is; reference in documentation)
- Creating new rules (only reforming existing ones)
- Designing a learning loop `/digest` skill (future work)

---

## Success Criteria

✅ **Structure:**
- 4 core rule files in `.claude/rules/`
- 1 consolidated conventions file in `memory/`
- All procedures in skill SKILL.md files
- Priority hierarchy explicit and documented

✅ **Compliance:**
- Zero behavioral coverage lost (all scenario tests pass)
- All original rule behaviors preserved (rule, skill, or memory)
- No unintended side effects from reorganization

✅ **Automation:**
- 5 new enforcement skills operational (`/validate-plan-ids`, `/audit-plan-outcomes`, `/audit-cross-references`, `/sync-memory-indices`, and master skill)
- `/enforce-repo-cleanliness` runs all checks and reports status

✅ **Documentation:**
- CLAUDE.md reorganized by rule tier
- rule-priority-hierarchy.md created
- All cross-references verified working
- Completion report with before/after metrics

✅ **Token Savings:**
- Rules: ~3,500 → ~2,300 tokens (-35%)
- Conventions: moved to memory (space savings in always-loaded rules)

---

## 8-Phase Implementation Plan

### Phase 1: Reclassify Rule Files (Audit + Consolidate Conventions)
**Duration:** 1-2 sessions

**Tasks:**
1. Audit each rule file and classify:
   - RULE (behavioral correction) → keep in `.claude/rules/`
   - PROCEDURE (multi-step workflow) → move to skill SKILL.md
   - CONVENTION (fact about project) → move to memory
   - ROUTING (path mapping) → consolidate into reference

2. Create `memory/convention_project_standards.md` with:
   - Model selection (Haiku/Sonnet/Opus guidance)
   - Worktree organization (worktrees/ directory)
   - Plan P-ID naming (P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug})
   - JSONL/markdown authority (JSONL is authoritative)
   - Repository map consultation checklist

3. Update MEMORY.md index

**Deliverables:**
- Audit table complete (rule-reform-implementation.md Task 1.1)
- convention_project_standards.md created
- MEMORY.md updated

**Files affected:** `.claude/rules/*`, `memory/`, MEMORY.md

---

### Phase 2: Prose Compression with Scenario Testing
**Duration:** 1 session

**Approach:** For each compression, ask: "Is there a scenario where original wording catches a mistake but compressed version doesn't?"

**Priority compression targets:**
1. `root-documentation-boundary.md` (126 → ~85 lines, -33%)
2. `trigger-branch-strategy.md` (78 → ~55 lines, -29%)
3. Other rules: compress examples, keep edge cases

**Deliverables:**
- Compressed rule files
- Scenario test checklist (all compressions verified)
- Token savings estimate

**Files affected:** `.claude/rules/root-documentation-boundary.md`, `.claude/rules/trigger-branch-strategy.md`

---

### Phase 3: Move Procedures to Skill SKILL.md Files
**Duration:** 1 session

**Procedures to move:**
1. `trigger-git-commit-workflow.md` → `.claude/skills/git-draft-commit/SKILL.md`
   - Extract: Branch check, log errors, session context, git status, draft format steps
2. `trigger-docs-workflow.md` → `.claude/skills/docs-update-all/SKILL.md`
   - Extract: Phase order, when to update each, example outputs
   - Align with updated SKILL.md (Phases 0-10 already added)

**Post-move:**
- Delete empty rule files
- Update CLAUDE.md to reference skills instead of rules
- Verify no broken cross-references

**Deliverables:**
- Updated skill SKILL.md files
- Deleted empty rule files
- CLAUDE.md cross-references updated

**Files affected:** `.claude/rules/trigger-git-commit-workflow.md`, `.claude/rules/trigger-docs-workflow.md`, `.claude/skills/git-draft-commit/SKILL.md`, `.claude/skills/docs-update-all/SKILL.md`

---

### Phase 4: Add Explicit Priority Hierarchy to Rules
**Duration:** 0.5 sessions

**Deliverables:**
1. `.claude/rules/rule-priority-hierarchy.md` with:
   - TRUST tier (never yield): Branch strategy, Root documentation boundary
   - CORRECTNESS tier (yield only to Trust): Plan outcome discipline
   - QUALITY tier (yield to Trust + Correctness): One-off execution default
   - EFFICIENCY tier (yields to all): Reserve for future
   - Conflict resolution guidance

2. Update CLAUDE.md "Rules (TL;DR)" section:
   - Group rules by tier (not flat list)
   - Link to priority hierarchy file
   - Show example conflict resolution

**Deliverables:**
- rule-priority-hierarchy.md created
- CLAUDE.md reorganized by tier
- Edge cases tested for conflicts

**Files affected:** `.claude/rules/rule-priority-hierarchy.md`, CLAUDE.md

---

### Phase 5: Build Enforcement Skills (Missing Validators)
**Duration:** 2-3 sessions

**New skills to build:**

1. **`/validate-plan-ids`** — Enforce P-ID naming convention
   - Scan `plans/` for P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}
   - Flag misnamed folders
   - Suggest corrections

2. **`/audit-plan-outcomes`** — Verify outcome completeness
   - List all plans in `02-in_progress-plans/`
   - Check `03-outcome_plans/` for matching outcomes
   - Flag missing outcomes
   - Summarize completion rate

3. **`/audit-cross-references`** — Validate all links
   - Scan CLAUDE.md, README.md, PLANS_INDEX.md
   - Check files exist at paths
   - Flag broken references
   - Suggest corrections

4. **`/sync-memory-indices`** — Keep MEMORY.md coherent
   - List all `.md` files in `memory/`
   - Check each referenced in MEMORY.md
   - Flag orphaned files or missing entries
   - Suggest additions to MEMORY.md

**Deliverables:**
- 4 new skill folders with SKILL.md files
- Each skill includes: Quick Start, When to Use, Trigger Phrases, How It Works, Output Format
- All integrated with Phase 6 master skill

**Files affected:** `.claude/skills/validate-plan-ids/`, `.claude/skills/audit-plan-outcomes/`, `.claude/skills/audit-cross-references/`, `.claude/skills/sync-memory-indices/`

---

### Phase 6: Build Master `/enforce-repo-cleanliness` Skill
**Duration:** 1 session

**Function:**
```
/enforce-repo-cleanliness
├─ Check 1: /move-docs-to-folders → Root doc violations
├─ Check 2: /validate-plan-ids → P-ID naming
├─ Check 3: /audit-plan-outcomes → Missing outcomes
├─ Check 4: /audit-cross-references → Broken links
├─ Check 5: /sync-memory-indices → Memory coherence
└─ Report: Summary + violations + suggested fixes
```

**Output:** Structured status report showing:
- Overall health (✓ PASS / ⚠ WARNING / ✗ FAIL)
- Per-check results
- Violations + recommended fixes
- One-line action summary

**Deliverables:**
- `.claude/skills/enforce-repo-cleanliness/SKILL.md`
- Master orchestrator ready for integration
- Single entry point for repo validation

**Files affected:** `.claude/skills/enforce-repo-cleanliness/`

---

### Phase 7: Update CLAUDE.md Navigation and Finalize
**Duration:** 0.5 sessions

**Changes:**
1. Reorganize "Rules (TL;DR)" section by tier:
   - CORE RULES (Trust Tier)
   - COMPLIANCE (Correctness Tier)
   - CONVENTIONS & FACTS (→ memory/)

2. Add new "Enforcement Skills" section:
   - `/enforce-repo-cleanliness` (master)
   - `/move-docs-to-folders`, `/validate-plan-ids`, etc.

3. Update workflows table to reference skills

4. Add "Rule Priority Hierarchy" reference link

5. Verify all cross-references resolve

6. Update CHEATSHEET.md with new trigger phrases

**Deliverables:**
- CLAUDE.md fully reorganized
- CHEATSHEET.md updated
- All cross-references verified
- Clear distinction between rules, conventions, skills

**Files affected:** CLAUDE.md, CHEATSHEET.md

---

### Phase 8: Final Validation and Documentation
**Duration:** 1 session

**Validation checklist:**

1. **Structural integrity:**
   - All CLAUDE.md, README.md, memory file cross-references resolve
   - No orphaned rule files
   - No broken skill references

2. **Completeness:**
   - All rules classified (audit table complete)
   - All conventions in memory
   - All procedures in skills
   - All enforcement skills built

3. **Behavioral coverage:**
   - Scenario Test passed on all compressed rules
   - All original behaviors preserved
   - No unintended side effects

4. **Live repo validation:**
   - Run `/enforce-repo-cleanliness` against actual repo
   - Verify all checks pass (or report violations correctly)
   - Verify suggestions actionable

5. **Documentation:**
   - Update `docs/reference/rule-reform-gaps.md` with Results section
   - Create `docs/reference/rule-reform-completion-report.md`
   - Document any adjustments vs. original plan

**Deliverables:**
- Validation report (pass/fail per check)
- Before/after metrics
  - Rule files: 10 → 4
  - Tokens in rules: ~3,500 → ~2,300
  - Skills: +4 validators, +1 master
  - Memory files: +1 consolidated conventions
- Completion sign-off

**Files affected:** Validation reports, completion documentation

---

## Task Assignments (Session-Based)

**Session 1:** Phase 1 (Reclassify) + Phase 2 (Compress)  
**Session 2:** Phase 3 (Move Procedures)  
**Session 3:** Phase 4 (Priority Hierarchy)  
**Sessions 4-5:** Phase 5 (Build Enforcement Skills) — parallel skill builds if possible  
**Session 6:** Phase 6 (Master Skill)  
**Session 7:** Phase 7 (Update Navigation)  
**Session 8:** Phase 8 (Final Validation)

---

## Dependencies & Risks

### Dependencies
- jlacour-git framework understanding (read: rule-reform-gaps.md)
- **P0021 (Docs Reorganization) COMPLETED** — 4-folder structure now authority
  - Routing table: `.claude/rules/root-documentation-boundary.md`
  - Enforcement skills: `/move-docs-to-folders`, `/docs-update-all` Phase 0
  - See: `2026-05-04_DOC-p0021-integration.md` (in this plan folder) for cross-phase integration
- Existing skills (`/move-docs-to-folders`, `/docs-update-all`) already enhanced
- MEMORY.md index maintained
- Cross-references tracked

### Risks & Mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| Compression removes needed behavioral detail | High | Run Scenario Test on every compression; 7 of 13 initially failed in jlacour-git's work |
| Procedures moved incorrectly to skills | High | Verify each procedure call/invocation in SKILL.md after move |
| Cross-references break after reorganization | High | Use grep to find all references; verify each still resolves |
| Behavioral coverage lost in any phase | Critical | Keep audit trail; Phase 8 validation includes full coverage check |
| New enforcement skills have bugs | Medium | Test each skill against known violations in repo before Phase 6 integration |

---

## Success Metrics

**Token Consumption:**
- Before: ~3,500 tokens in rules
- Target: ~2,300 tokens (-35%)
- Measurement: Count tokens in all `.claude/rules/*.md` files

**Rule Count:**
- Before: ~10 files
- Target: 4 core rule files
- Measurement: `ls -1 .claude/rules/*.md | wc -l`

**Enforcement Coverage:**
- Before: 1 enforcement skill (`/move-docs-to-folders`)
- Target: 6 enforcement skills (5 validators + 1 master)
- Measurement: Can invoke `/enforce-repo-cleanliness` and get full report

**Behavioral Coverage:**
- Target: 100% (zero behaviors lost)
- Measurement: Scenario Test pass rate on all compressions

**Cross-Reference Integrity:**
- Before: Manual tracking
- Target: All references verified + `/audit-cross-references` checks them
- Measurement: Zero broken links in validation report

---

## References & Resources

**Analysis documents:**
- `docs/reference/rule-reform-gaps.md` — Gap analysis (7 specific gaps identified)
- `docs/reference/rule-reform-implementation.md` — Detailed roadmap with task checklists

**Framework:**
- jlacour-git's Rule System Reform (danielmiessler/Personal_AI_Infrastructure#908)
- Three approaches: lateral reclassification, priority hierarchy, prose compression

**Related skills (already built):**
- `/move-docs-to-folders` — Root doc violations (Phase 0 of /docs-update-all)
- `/docs-update-all` — Documentation sync (includes Phase 0 + 10 phases)

**Plan discipline:**
- `.claude/rules/plan-documentation-structure.md` — P-ID folder structure
- `.claude/rules/plan-structure.md` — Plan workflow (outcome required on completion)

---

## Notes for Future Sessions

- **Phase 1 is the most important phase** — Audit determines exact scope and reveals what's actually being used
- **Keep compression conservative** — Better to have slightly verbose rules than lose behavioral coverage
- **Test enforcement skills in isolation** — Build each validator, test independently, then integrate
- **Cross-reference updates are tedious but critical** — Use grep + Bash to batch-update paths
- **Session context:** This plan can be referenced across sessions as P0020

---

## Checklist (Copy-Paste for Session Start)

### Phase 1
- [ ] Audit table complete (rule-reform-implementation.md Task 1.1)
- [ ] convention_project_standards.md created
- [ ] MEMORY.md index updated
- [ ] Cross-references verified

### Phase 2
- [ ] root-documentation-boundary.md compressed + scenario tested
- [ ] trigger-branch-strategy.md compressed + scenario tested
- [ ] Token savings measured

### Phase 3
- [ ] git-draft-commit SKILL.md updated with procedures
- [ ] docs-update-all SKILL.md verified (Phases 0-10 present)
- [ ] Empty rule files deleted
- [ ] CLAUDE.md cross-references updated

### Phase 4
- [ ] rule-priority-hierarchy.md created
- [ ] CLAUDE.md reorganized by tier
- [ ] Edge cases tested for conflicts

### Phase 5
- [ ] /validate-plan-ids skill created + tested
- [ ] /audit-plan-outcomes skill created + tested
- [ ] /audit-cross-references skill created + tested
- [ ] /sync-memory-indices skill created + tested

### Phase 6
- [ ] /enforce-repo-cleanliness master skill created
- [ ] All 5 checks integrated
- [ ] Output format verified

### Phase 7
- [ ] CLAUDE.md "Rules" section reorganized
- [ ] CLAUDE.md "Enforcement Skills" section added
- [ ] CHEATSHEET.md updated with trigger phrases
- [ ] All cross-references verified

### Phase 8
- [ ] Structural integrity validated
- [ ] Completeness validated
- [ ] Behavioral coverage validated (Scenario Tests pass)
- [ ] Live repo validation (`/enforce-repo-cleanliness` runs)
- [ ] Completion report created
- [ ] Sign-off: All phases complete, plan moved to outcome_plans/

---

**Status:** Ready to begin Phase 1 on next session.  
**Approval:** Waiting for user confirmation before proceeding.
