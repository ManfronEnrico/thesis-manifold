---
name: update_plan
description: Log plan outcome and relocate/rename if needed, following the project's trigger-plan-workflow
---

# Update Plan

Log the outcome of a completed or adjusted plan. Automatically relocates and renames misplaced plans to conform to `YYYY-MM-DD_<short-slug>.md` format.

## Usage

```
/update_plan
/update_plan <plan-name-or-partial-filename>
```

If no plan name is provided, Claude will search for recently-touched plans.

## How It Works

This skill implements the plan update workflow from `.claude/rules/trigger-plan-workflow.md`:

1. **Locate the plan file** — Search both `~/.claude/plans/` (global) and `<project-root>/.claude/plans/` (project)
2. **Relocate if misplaced** — If in global `~/.claude/plans/`, move to project's `.claude/plans/`
3. **Rename if needed** — If filename doesn't follow `YYYY-MM-DD_<short-slug>.md`, rename it
4. **Append `## Outcome` section** with format below

## Outcome Section Format

```
---

## Outcome

_Completed: YYYY-MM-DD_

### ✅ Completed
- <what was implemented, as planned>

### 🔄 Adjusted
- **What**: <what changed from the original plan>
  **Why**: <reason — constraint, discovery, user decision>
  **How**: <what was done instead>

### ❌ Dropped
- **What**: <step or item that was not done>
  **Why**: <reason — out of scope, superseded, deferred>

### Notes
<any other context useful for future reference>
```

Omit sections if there is nothing to record.

## Plan File Location

All plan files live in the **project's own directory**: `<project-root>/.claude/plans/`

Naming convention: `YYYY-MM-DD_<short-slug>.md`
