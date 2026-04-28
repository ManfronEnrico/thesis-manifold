# Plan Documentation Structure Rule

**Purpose**: Enforce consistent organization of plans and their supporting documentation across the project lifecycle.

**Scope**: All plan files and plan-related documentation.

---

## Folder Structure

Plans live in one of four status buckets:

```
plans/
  01-backlog-plans/         ← Not yet started
  02-in_progress-plans/     ← Currently being executed
  03-outcome_plans/         ← Completed with outcomes
  04-archive_plans/         ← Old/deprecated plans
```

**Each plan is a folder**, not a single file. This enables bundling the plan with all its supporting documentation.

---

## Naming Convention

### Plan Folder Name

```
YYYY-MM-DD_HHMM_PLAN-{slug}
```

**Format**:
- `YYYY-MM-DD_HHMM` — ISO date + time (24hr format, no separators)
- `PLAN` — literal keyword (always "PLAN" for plan folders)
- `{slug}` — lowercase, hyphens (e.g., `jupyter-notebook-path-centralization`)

**Examples**:
- `2026-04-27_1420_PLAN-jupyter_notebook_path_centralization`
- `2026-04-15_0830_PLAN-ml-model-retraining`
- `2026-04-23_1530_PLAN-data-pipeline-refactor`

### Plan File (inside folder)

**Same name as folder, but with `.md` extension:**

```
2026-04-27_1420_PLAN-jupyter_notebook_path_centralization.md
```

This is **always** the primary plan document. It contains the plan details, objectives, execution steps, and outcomes.

### Documentation Files (inside folder)

**Supporting documents** generated while working on the plan:

```
YYYY-MM-DD_DOC-{description}.{ext}
```

**Format**:
- `YYYY-MM-DD` — Date the document was created (ISO date only, no time)
- `DOC` — literal keyword (always "DOC" for documentation)
- `{description}` — lowercase, hyphens (e.g., `phase2-migration-summary`)
- `.{ext}` — File extension (`.md`, `.txt`, `.json`, etc.)

**Examples**:
- `2026-04-28_DOC-phase2-migration-summary.md`
- `2026-04-28_DOC-phase3-testing-guide.md`
- `2026-04-28_DOC-completion-status.txt`
- `2026-04-29_DOC-validation-report.json`

---

## Complete Example

```
plans/02-in_progress-plans/
  2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/
    2026-04-27_1420_PLAN-jupyter_notebook_path_centralization.md
    2026-04-28_DOC-phase2-migration-summary.md
    2026-04-28_DOC-phase3-testing-guide.md
    2026-04-28_DOC-completion-status.txt
    2026-04-29_DOC-validation-results.md
```

---

## Rules for Documentation Files

### What Goes Inside a Plan Folder

✅ **Include**:
- Plan file (always `YYYY-MM-DD_HHMM_PLAN-{slug}.md`)
- Supporting documentation created while executing the plan
- Analysis, reports, or notes specific to this plan
- Test results or validation outputs

❌ **Never include**:
- Unrelated project documentation
- General tooling notes
- Reusable templates or guides
- Files that apply to multiple plans

### Documentation Lifecycle

1. **During execution**: Create supporting docs inside the plan folder
   - Use `YYYY-MM-DD_DOC-{description}.md`
   - Include the document in the plan folder

2. **When moving to outcome**: 
   - Keep all supporting docs in the folder
   - Move the entire folder from `02-in_progress-plans/` to `03-outcome_plans/`
   - Optionally add a new `YYYY-MM-DD_DOC-outcome-summary.md` with final results

3. **When archiving**:
   - Move the entire folder from current status to `04-archive_plans/`
   - Keep all supporting docs intact
   - No cleanup needed

---

## Never Create Documentation in Root

❌ **DO NOT** create these in `C:/dev/thesis-manifold/`:
- `PHASE2_MIGRATION_SUMMARY.md`
- `JUPYTER_PATH_CLEANUP_SUMMARY.md`
- `TESTING_GUIDE.md`
- Any plan-related documentation

✅ **Always** create them inside the plan folder:
- `plans/02-in_progress-plans/2026-04-27_1420_PLAN-name/2026-04-28_DOC-summary.md`

---

## How to Apply This Rule

### When Creating a New Plan

1. Create folder: `plans/02-in_progress-plans/YYYY-MM-DD_HHMM_PLAN-{slug}/`
2. Create plan file: `YYYY-MM-DD_HHMM_PLAN-{slug}.md` inside
3. All supporting docs go in the same folder

### When Documenting During Execution

1. Create docs inside the plan folder
2. Use naming: `YYYY-MM-DD_DOC-{description}.md`
3. Never put docs in project root

### When Moving a Plan Between Statuses

1. Move the **entire folder** (plan + all docs) to the new status
2. Example: Move from `02-in_progress-plans/2026-04-27_1420_PLAN-x/` → `03-outcome_plans/2026-04-27_1420_PLAN-x/`

---

## Rationale

**Why folders instead of flat files?**
- Bundles related documents together
- Easy to move entire plan + docs to different status
- Prevents documentation from scattering across the project
- Clear visual grouping in file explorer

**Why timestamp in folder AND filename?**
- Folder timestamp shows when plan was created (discovery, sorting)
- Document timestamp shows when doc was created (evolution tracking)
- Both sorted chronologically without collision

**Why "PLAN" and "DOC" keywords?**
- Instantly identifies file type
- Enables automation (scripts can parse naming)
- Prevents ambiguity (is this a plan or a doc?)

---

## Triggers for This Rule

This rule applies automatically when:
- ❓ Claude is about to create plan-related documentation
- ❓ Claude creates files that don't belong in project root
- ❓ Claude creates supporting documents for a plan

**Expected behavior**:
- Documentation is organized inside plan folder
- Files have proper timestamp + keyword prefixes
- Nothing ends up in project root

---

## See Also

- `.claude/skills/plan-documentation-organizer/` — Skill to automate this structure
- `docs/reference/repository_map.md` — Where each file type belongs
- `CLAUDE.md` → Plans section — Overview of plan workflows
