# plan-documentation-organizer

**Status**: Active  
**Purpose**: Create and organize plan documentation following the standardized folder/naming structure  
**Trigger**: `/plan-docs` or when documenting a plan  

## What This Skill Does

Ensures all plan-related documentation is:
- ✅ Organized in plan-specific folders
- ✅ Named with proper timestamp + keyword prefixes
- ✅ Never scattered in project root
- ✅ Easily movable between status buckets (backlog → in-progress → outcome → archive)

## Quick Start

**Create a new plan folder + docs:**

```bash
/plan-docs create --plan-slug "jupyter-notebook-path-centralization" --status in_progress
```

**Add documentation to existing plan:**

```bash
/plan-docs add-doc --plan-slug "jupyter-notebook-path-centralization" --doc-type "testing-guide"
```

**Move plan to different status:**

```bash
/plan-docs move --plan-slug "jupyter-notebook-path-centralization" --from in_progress --to outcome
```

## File Structure

```
plans/
  02-in_progress-plans/
    2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/
      2026-04-27_1420_PLAN-jupyter_notebook_path_centralization.md
      2026-04-28_DOC-phase2-migration-summary.md
      2026-04-28_DOC-phase3-testing-guide.md
```

See `.claude/rules/plan-documentation-structure.md` for full specification.

## Configuration

Set plan creation preferences in `.claude/settings.json`:

```json
{
  "skill": {
    "plan-documentation-organizer": {
      "default_status": "02-in_progress-plans",
      "auto_timestamp": true,
      "create_plan_file": true
    }
  }
}
```

## See Also

- **Rule**: `.claude/rules/plan-documentation-structure.md`
- **Plans**: `plans/` folder (01-04 status buckets)
- **CLAUDE.md**: `→ Workflows → Plan creation`
