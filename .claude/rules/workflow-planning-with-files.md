---
name: workflow-planning-with-files
description: RULE - Planning-with-files skill as canonical plan creation and management workflow
category: workflow
applies-to: [plans, workflows, plan-creation, plan-updates]
triggers: [plan-creation, plan-update, planning, outcome-logging, plan-management]
created: 2026_06_22-00_00
updated: 2026_06_22-00_00
---

# Planning-with-Files Workflow

**Rule**: Use the `planning-with-files` skill as the canonical tool for all plan management, using dedicated date-stamped subfolders with P-IDs to organize working files.

**Why**: Persistent disk-based planning prevents context loss across session compression. P-ID + date-stamped folders enable parallel task tracking without conflicts and preserve cross-reference capability.

## Quick Decision

| Task | Tool | Location |
|------|------|----------|
| Start new plan | `/planning-with-files` | `plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/` |
| Create working files | Manually (from skill templates) | Same subfolder |
| View active plans | Browse `plans/` folder | `<project-root>/plans/` |
| Resume after compression | Read `task_plan.md` + `TaskList` | Same subfolder (auto-discovered) |
| Archive finished plan | Move folder to `plans/.archive/` | `plans/.archive/P{NNNN}_...` |

## The Rule

**Always use planning files in dedicated P-ID + date-stamped subfolders at `<project-root>/plans/`.**

This applies to:
1. Every task with 3+ steps or cross-component scope
2. Multi-phase work requiring persistent tracking
3. Parallel work (multiple plans in same repo)

Never:
- Store working files in project root directly
- Leave plans without written outcomes after completion (update frontmatter instead)
- Create separate outcome files — status lives in frontmatter only

## Plan File Structure

**Location**: `<project-root>/plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/`

**Naming convention**:
- `P{NNNN}` — Unique sequential P-ID (P0023, P0024, etc. — check `PLANS_INDEX.md` for next available)
- `YYYY-MM-DD` — Creation date (ISO format, e.g., `2026-06-22`)
- `HH-mm` — Creation time (24-hour format with hyphen, e.g., `14-30`)
- `<slug>` — 2–4 words, lowercase, hyphenated (e.g., `field-schema-refactor`)

**Example**: `plans/P0023_2026-06-22_14-30_nielsen-eda-phase2/`

**Required files in subfolder**:
1. `task_plan.md` — Phases, progress, decisions (auto-injected pre-tool-use)
2. `findings.md` — Research, discoveries, external content
3. `progress.md` — Session log, test results, errors

**Optional**:
- `tasks/N.json` — Persisted task JSON files (see Task Persistence below)
- `YYYY-MM-DD_DOC-{description}.md` — Supporting docs created during execution

## Plan Frontmatter

Every plan file must include YAML frontmatter:

```yaml
---
pid: P0023
created: 2026-06-22 14:30:00
updated: 2026-06-22 14:30:00
status: in_progress
focus_detail: "What is currently being done and next steps"
---
```

**Status values**: `in_progress` | `focus` | `complete` | `paused` | `blocked` | `cancelled`

**Status-specific fields**:

| Status | Required Additional Fields |
|--------|---------------------------|
| `focus` | `focus_detail` |
| `complete` | `completed: YYYY-MM-DD HH:MM:SS`, `outcome_summary` |
| `blocked` | `blocked_reason` |
| `paused` | `paused_reason` |
| `cancelled` | `cancellation_reason` |

**No folder movement required** — status changes are frontmatter-only. Exception: move to `plans/.archive/` when archiving.

## Archiving Plans

Completed or stale plans move to `plans/.archive/` — the folder structure stays flat:

```
plans/
  .archive/
    P0001_2026-04-13_0800_cmt-master-upgrade/
    P0022_2026-05-07_0800_preprocessing-pipeline/
  P0023_2026-06-22_14-30_active-plan/
```

## Legacy Plans (P0001–P0022)

Existing plans in `plans/{01-backlog_plans,...,08-archived_plans}/` are **not migrated**. They remain in their status bucket folders. New plans (P0023+) use the flat structure above. The `PLANS_INDEX.md` tracks both.

## Integration with Task Decomposition

1. **Decompose**: Use `/task-decomposition` skill to break work into atomic 1-3 hour tasks
2. **Create**: Call `TaskCreate` for each task
3. **Plan**: Document phases and dependencies in `task_plan.md`
4. **Track**: Use `TaskList` / `TaskUpdate` for execution; log progress in `progress.md`
5. **Persist**: Write JSON files to `tasks/` subfolder immediately after each `TaskCreate` / `TaskUpdate`

See [[config-prefer-task-list-breakdown]] for the full task tracking workflow.

## Task Persistence

After calling `TaskCreate`, persist all tasks to the plan folder as JSON files — in-memory tasks do not survive session end.

**Location**: `plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/tasks/<id>.json`

**Format** (matches `~/.claude/tasks` native format):
```json
{
  "id": "1",
  "subject": "Imperative task title",
  "description": "Full description...",
  "activeForm": "Present-continuous form",
  "status": "pending",
  "blocks": [],
  "blockedBy": []
}
```

**When to write**: immediately after all `TaskCreate` calls complete, AND after every `TaskUpdate` that changes status. Never batch.

### Dual-Update Protocol

Every status change is two operations — both required:

| Trigger | In-session call | Persisted JSON update |
|---------|-----------------|-----------------------|
| Start task | `TaskUpdate taskId=N status=in_progress` | Write `tasks/N.json` `"status": "in_progress"` |
| Complete task | `TaskUpdate taskId=N status=completed` | Write `tasks/N.json` `"status": "completed"` |
| Any field change | `TaskUpdate taskId=N ...` | Write updated `tasks/N.json` |

**Single-file update** (run immediately after each `TaskUpdate`):

```python
import json
from pathlib import Path

f = Path("plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/tasks/N.json")
data = json.loads(f.read_bytes())
data["status"] = "in_progress"
f.write_bytes(json.dumps(data, indent=2).encode("utf-8"))
```

### Reload Tasks in a New Session

**Option A — From plan folder (recommended)**:

```powershell
$plan = "plans/P0023_2026-06-22_14-30_active-plan"
$uuid = [guid]::NewGuid().ToString()
$dest = "$env:USERPROFILE\.claude\tasks\$uuid"
New-Item -ItemType Directory -Path $dest | Out-Null
Copy-Item "$plan\tasks\*.json" $dest
Write-Host "Tasks loaded into $dest — restart Claude Code to pick them up"
```

**Option B — List existing task sets**:

```powershell
Get-ChildItem "$env:USERPROFILE\.claude\tasks" -Directory | ForEach-Object {
    $first = Get-ChildItem $_.FullName -Filter "1.json" | Select-Object -First 1
    if ($first) {
        $subject = (Get-Content $first.FullName | ConvertFrom-Json).subject
        Write-Host "$($_.Name)  ->  $subject"
    }
}
```

**After reloading**:
1. Start new Claude Code session in project directory
2. Run `TaskList` to confirm tasks visible
3. Read `task_plan.md` + `progress.md` to restore context
4. Resume from first `pending` task with no blockers

## Context Recovery After Compression

When session context compacts:
1. Plan files remain on disk at `plans/<active-plan>/`
2. After compaction, re-read `task_plan.md` + `progress.md` + run `TaskList`
3. Skill auto-discovers active plan (newest by mtime)

## Related

- [[config-prefer-task-list-breakdown]] — Task decomposition and tracking workflow
- `plans/PLANS_INDEX.md` — Master P-ID reference
- `.claude/rules/workflow-standup.md` — Standup logging (uses plan context)
- `.claude/rules/workflow-docs.md` — Documentation updates (references plans)
