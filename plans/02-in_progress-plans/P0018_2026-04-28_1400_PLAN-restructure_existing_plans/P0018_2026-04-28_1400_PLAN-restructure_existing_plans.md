---
created: 2026-04-28 14:00:00
updated: 2026-04-28 19:45:00
---

# Plan: Restructure Existing Plans — Migrate to New Folder Convention

**Objective**: Restructure all existing markdown plan files in `plans/` to follow the new plan-documentation-structure standard. Each plan should be a folder containing the plan file + supporting documentation files.

**Status**: Pending (tomorrow)

---

## Current State (Problem)

Currently, plans in `04-archive_plans/` are individual `.md` files (flat structure):

```
plans/04-archive_plans/
  2026-04-15_integration-phase1-execution.md
  2026-04-15_restructuring-audit.md
  2026-04-18_integration-three-systems.md
  2026-04-22_nielsen-pipeline-and-agent-paths.md
  ... (more files)
```

**Issues**:
- No folder structure (hard to group related docs)
- No PLAN/DOC keyword distinction
- Can't bundle supporting documentation with plan
- Doesn't follow new `YYYY-MM-DD_HHMM_PLAN-{slug}` convention

---

## Solution: Folder per Plan

### New Structure (Target)

```
plans/04-archive_plans/
  2026-04-15_0800_PLAN-integration-phase1-execution/
    2026-04-15_0800_PLAN-integration-phase1-execution.md
    
  2026-04-15_0800_PLAN-restructuring-audit/
    2026-04-15_0800_PLAN-restructuring-audit.md
    
  2026-04-18_0800_PLAN-integration-three-systems/
    2026-04-18_0800_PLAN-integration-three-systems.md
    2026-04-18_DOC-completion-notes.md  (if exists)
    
  ... (etc for all plans)
```

Each plan gets:
1. A folder: `YYYY-MM-DD_HHMM_PLAN-{slug}`
2. A plan file: `YYYY-MM-DD_HHMM_PLAN-{slug}.md`
3. Any supporting docs: `YYYY-MM-DD_DOC-{description}.{ext}`

---

## Execution Steps (Tomorrow)

### Step 1: Audit existing files

Count how many plans need migrating in each bucket:
- `04-archive_plans/`: ~9 files
- `03-outcome_plans/`: ~4 files  
- `02-in_progress-plans/`: Already has new structure (jupyter plan is done)
- `01-backlog-plans/`: 0 files

**Total: ~13 files to migrate into folders**

### Step 2: Create migration automation

For each `.md` file:
1. Extract filename and create folder
2. Move file into folder with PLAN naming
3. Assign time: use 0800 for all (since old files lack timestamps)

### Step 3: Migrate bucket by bucket

Start with `04-archive_plans/` (safest, already archived), then `03-outcome_plans/`, etc.

### Step 4: Validate

Run `/plan-docs validate` to check all plans are now compliant.

---

## Decisions Needed Tomorrow

1. **Time assignment for old files**: Use 0800 for all? (Recommended: YES)
2. **Automation approach**: Bash script or Python?
3. **Supporting docs**: If old plans have related docs, bundle them in same folder?
4. **Validation**: Require `/plan-docs validate` to pass before moving on?

---

## Success Criteria

- ✅ All 13 old flat files in plan-specific folders
- ✅ Each named: `YYYY-MM-DD_HHMM_PLAN-{slug}.md`
- ✅ No `.md` files left in bucket root
- ✅ All plans pass `/plan-docs validate`
- ✅ Structure matches `plan-documentation-structure.md` rule

---

## Estimated Time

- Audit: 5 min
- Script creation: 15 min
- Migration: 10 min
- Validation: 5 min

**Total: ~40 minutes**

---

## Related

- **Rule**: `.claude/rules/plan-documentation-structure.md`
- **Skill**: `.claude/skills/plan-documentation-organizer/`
- **Example**: `2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/` (already migrated)

