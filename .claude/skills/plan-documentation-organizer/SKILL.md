# Skill: plan-documentation-organizer

**Purpose**: Organize plan documentation following the standardized structure defined in `.claude/rules/plan-documentation-structure.md`

**Invocation**: `/plan-docs` + subcommand

---

## Commands

### 1. `create` — Create new plan folder + structure

```bash
/plan-docs create --plan-slug "jupyter-notebook-path-centralization" --status in_progress
```

**What it does:**
- Creates folder: `plans/02-in_progress-plans/YYYY-MM-DD_HHMM_PLAN-{slug}/`
- Creates plan file: `YYYY-MM-DD_HHMM_PLAN-{slug}.md` inside
- Opens editor for plan content
- Returns folder path and instructions

**Options:**
- `--plan-slug` (required): Plan slug (lowercase, hyphens)
- `--status` (optional): One of `backlog`, `in_progress`, `outcome`, `archive` (default: `in_progress`)
- `--title` (optional): Human-readable plan title
- `--description` (optional): Brief plan description

**Output:**
```
✅ Created plan folder:
   plans/02-in_progress-plans/2026-04-28_1534_PLAN-jupyter_notebook_path_centralization/
   
Plan file ready for editing:
   2026-04-28_1534_PLAN-jupyter_notebook_path_centralization.md
   
Next step: Add documentation as you work:
   /plan-docs add-doc --plan-slug "jupyter_notebook_path_centralization" --doc-type "phase2-summary"
```

---

### 2. `add-doc` — Add documentation to existing plan

```bash
/plan-docs add-doc --plan-slug "jupyter-notebook-path-centralization" --doc-type "phase2-migration-summary"
```

**What it does:**
- Creates doc file: `YYYY-MM-DD_DOC-{doc-type}.md` inside plan folder
- Inserts timestamp and description into filename
- Returns file path
- Optionally opens editor

**Options:**
- `--plan-slug` (required): Plan slug (find automatically if only one plan exists)
- `--doc-type` (required): Document type (lowercase, hyphens)
- `--extension` (optional): File extension (default: `.md`, can be `.txt`, `.json`, etc.)
- `--open` (optional): Open in editor after creating (default: true)

**Output:**
```
✅ Added documentation to plan:
   plans/02-in_progress-plans/2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/
   2026-04-28_DOC-phase2-migration-summary.md
```

---

### 3. `list` — Show all plans (or plans in specific status)

```bash
/plan-docs list
/plan-docs list --status in_progress
```

**What it does:**
- Lists all plan folders in the specified status
- Shows creation date, slug, and status
- Shows count of supporting docs in each plan

**Output:**
```
PLANS BY STATUS
================

02-in_progress-plans/
  └─ 2026-04-27_1420_PLAN-jupyter_notebook_path_centralization
     Created: 2026-04-27 14:20
     Documents: 4 (phase2-migration-summary, phase3-testing-guide, ...)

  └─ 2026-04-23_1530_PLAN-data-pipeline-refactor
     Created: 2026-04-23 15:30
     Documents: 2 (implementation-plan, validation-results)

03-outcome_plans/
  └─ 2026-04-28_PLAN-config-centralization
     Created: 2026-04-28 09:00
     Documents: 1 (outcome-summary)

Total: 3 active plans
```

---

### 4. `move` — Move plan between status buckets

```bash
/plan-docs move --plan-slug "jupyter-notebook-path-centralization" --from in_progress --to outcome
```

**What it does:**
- Moves entire plan folder (with all docs) to new status
- Updates any references in parent files (if applicable)
- Returns verification and new path

**Options:**
- `--plan-slug` (required): Plan slug
- `--from` (optional): Current status (auto-detect if only one match)
- `--to` (required): Target status: `backlog`, `in_progress`, `outcome`, `archive`

**Output:**
```
✅ Moved plan to outcome:
   FROM: plans/02-in_progress-plans/2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/
   TO:   plans/03-outcome_plans/2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/
   
Preserved: 4 supporting documents
Status: outcome
```

---

### 5. `validate` — Check folder structure compliance

```bash
/plan-docs validate
/plan-docs validate --plan-slug "jupyter-notebook-path-centralization"
```

**What it does:**
- Checks all plans against naming standard
- Identifies non-compliant filenames or structures
- Suggests fixes

**Output:**
```
VALIDATION REPORT
=================

✅ 2026-04-27_1420_PLAN-jupyter_notebook_path_centralization
   └─ Plan file: ✅ Correct naming
   └─ Docs: ✅ 4 documents with correct prefixes
   └─ Status: in_progress (correct bucket)

⚠️  2026-04-15_academic-repos-integration (from old archive)
   └─ Plan file: ❌ Missing extension (.md required)
   └─ Docs: ❌ 1 old-style doc (no DOC- prefix)
   └─ Suggestion: Rename files or move to 04-archive_plans/

Summary: 1 compliant, 1 needs attention
```

---

### 6. `cleanup-root` — Remove stray documentation from root

```bash
/plan-docs cleanup-root
```

**What it does:**
- Scans project root for likely plan-related documentation
- Prompts for each file: move, delete, or ignore
- Moves files to appropriate plan folders or archive

**Output:**
```
Found stray documentation files:

  PHASE2_MIGRATION_SUMMARY.md
  → Belongs to: 2026-04-27_1420_PLAN-jupyter_notebook_path_centralization
  → Action: [M]ove / [D]elete / [I]gnore? 

  JUPYTER_PATH_CLEANUP_SUMMARY.md
  → Belongs to: Same plan
  → Action: [M]ove / [D]elete / [I]gnore?

✅ Moved 2 files to plan folder
```

---

## Behavioral Rules

### When Creating Plans

1. **Always use `/plan-docs create`** (or equivalent pattern)
2. **Plan slug must be lowercase with hyphens** (e.g., `my-plan-name`, not `MyPlanName`)
3. **Timestamp is generated automatically** (current date + time in 24hr format)
4. **Plan file always created** with matching name to folder

### When Adding Documentation

1. **Never create docs in project root**
2. **Always use `/plan-docs add-doc`** or manually follow naming pattern
3. **Doc naming**: `YYYY-MM-DD_DOC-{description}.{ext}`
4. **If creating manually**: Add doc inside plan folder, follow naming pattern

### When Moving Plans

1. **Move the entire folder** (plan + all docs together)
2. **Never split plan and docs**
3. **Validate after move** using `/plan-docs validate`

### When Archiving Plans

1. **Use `/plan-docs move --to archive`**
2. **All supporting docs move with the plan**
3. **No cleanup needed — everything stays together**

---

## Integration with Claude Code

### Auto-Trigger on Plan Creation

When Claude creates plan-related files without using this skill:
- ⚠️ Trigger warning that rule is being violated
- 📝 Suggest using `/plan-docs create` instead
- 🛠️ Offer to reorganize files after fact

### Hook Integration (if enabled)

Hooks can monitor for `.md` file creation in root:
- Detect plan-related content
- Suggest moving to proper plan folder
- Block creation if in root (optional strict mode)

---

## Examples

### Example 1: Create plan, add docs while working

```bash
# Create plan
/plan-docs create --plan-slug "data-pipeline-optimization" --status in_progress

# Work on plan, then add docs as you go
/plan-docs add-doc --plan-slug "data-pipeline-optimization" --doc-type "implementation-phase1"
/plan-docs add-doc --plan-slug "data-pipeline-optimization" --doc-type "test-results-v1"
/plan-docs add-doc --plan-slug "data-pipeline-optimization" --doc-type "performance-analysis"

# When done, move to outcome
/plan-docs move --plan-slug "data-pipeline-optimization" --to outcome
```

### Example 2: Reorganize existing plans

```bash
# List all plans to see current state
/plan-docs list

# Move completed plan to outcome
/plan-docs move --plan-slug "jupyter-notebook-path-centralization" --to outcome

# Validate everything is correct
/plan-docs validate

# Check for stray files in root
/plan-docs cleanup-root
```

---

## Configuration

**In `.claude/settings.json`:**

```json
{
  "skills": {
    "plan-documentation-organizer": {
      "enabled": true,
      "default_status": "02-in_progress-plans",
      "auto_timestamp": true,
      "create_plan_file": true,
      "validate_on_move": true,
      "strict_root_protection": false
    }
  }
}
```

---

## Related Documentation

- **Rule**: `.claude/rules/plan-documentation-structure.md` — Full specification
- **Example**: `plans/02-in_progress-plans/2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/`
- **CLAUDE.md**: Workflows section → Plans
