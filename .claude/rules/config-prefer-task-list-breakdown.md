---
name: config-prefer-task-list-breakdown
description: RULE - Break tasks into atomic subtasks using task-decomposition skill, then track with TaskCreate/TaskGet/TaskUpdate/TaskList
category: pattern
applies-to: [planning, task-execution, multi-step-work]
triggers: [starting-task, planning-phase, managing-complexity]
created: 2026_06_22-00_00
updated: 2026_06_22-00_00
---

# Task List Breakdown — Atomic Work Tracking

**Rule**: Every task with 3+ steps or cross-component scope must be decomposed into atomic subtasks and tracked in the task system.

**Why**: Clear task lists provide accountability, prevent context loss during session compression, and enable parallel work visibility.

## The Pattern

| Step | Action | Tool |
|------|--------|------|
| 1. Decompose | Break feature into 1-3 hr atomic units by phase | `/task-decomposition` |
| 2. Create | Register each task in the task system | `TaskCreate` |
| 3. Track | Manage execution, log blockers, update status | `TaskList` / `TaskGet` / `TaskUpdate` |
| 4. Persist | Write JSON to plan folder after every status change | Write `tasks/N.json` |

## When NOT to Use

Skip decomposition for:
- Trivial tasks (<1 hour, single file)
- Quick documentation fixes
- One-off data cleanup

## Task Tool Reference

| Tool | Purpose |
|------|---------|
| `TaskCreate` | Create task from decomposition output |
| `TaskList` | View all tasks, filter by status/owner |
| `TaskGet` | Fetch full task details before starting |
| `TaskUpdate` | Mark complete, log blockers, update status |

## Task Persistence Across Sessions

In-memory tasks (TaskCreate/TaskList) do **not** survive session end. After creating tasks, always persist them to the plan folder:

```
plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/tasks/<id>.json
```

One `.json` file per task, matching the native `~/.claude/tasks/<uuid>/` format:

```json
{
  "id": "1",
  "subject": "...",
  "description": "...",
  "activeForm": "...",
  "status": "pending",
  "blocks": [],
  "blockedBy": []
}
```

**When**: immediately after all `TaskCreate` calls complete, AND after every `TaskUpdate` that changes status (in_progress, completed, blocked). Never batch — write the JSON immediately after each `TaskUpdate` call.

**To restore tomorrow**: copy `tasks/` subfolder to `~/.claude/tasks/<new-uuid>/`.

### Dual-Update Protocol

Every status change is two operations — both required:

| Trigger | In-session call | Persisted JSON update |
|---------|-----------------|-----------------------|
| Start task | `TaskUpdate taskId=N status=in_progress` | Write `tasks/N.json` `"status": "in_progress"` |
| Complete task | `TaskUpdate taskId=N status=completed` | Write `tasks/N.json` `"status": "completed"` |
| Any other field change | `TaskUpdate taskId=N ...` | Write updated `tasks/N.json` |

**Single-file update** (run immediately after each `TaskUpdate`):

```python
import json
from pathlib import Path

f = Path("plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/tasks/N.json")
data = json.loads(f.read_bytes())
data["status"] = "in_progress"  # or "completed", etc.
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

**After reloading**:
1. Start new Claude Code session in project directory
2. Run `TaskList` to confirm tasks are visible
3. Read `task_plan.md` + `progress.md` to restore full context
4. Resume from first `pending` task with no blockers

## Related

- [[workflow-planning-with-files]] — Persistent disk-based planning (task_plan.md, progress.md)
- `.claude/skills/task-decomposition/SKILL.md` — Skill that generates decomposed task specs
- `plans/PLANS_INDEX.md` — Master P-ID reference
