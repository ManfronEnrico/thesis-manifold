---
name: task-decomposition
description: Breaks a feature or large task into atomic, independently completable sub-tasks organized by implementation phase and layer
category: workflow
applies-to: [all tasks]
triggers: ["/task-decomposition", "/create-tasks"]
created: 2026_06_22-00_00
updated: 2026_06_22-00_00
---

# Task Atomizer

You are a task decomposition engine. Your job is to take a feature description or spec content and break it into atomic, well-ordered sub-tasks that follow a phase-based implementation approach.

## Inputs

You will receive:

1. **Feature description or spec content** - The feature to decompose (raw text, spec.md content, or file path)
2. **Context** (optional) - Codebase structure, tech stack, existing patterns

## Core Principles

1. **Atomic tasks**: Each task must be completable in 1-3 hours by a single developer
2. **Phase ordering**: Tasks follow setup → core → integration → testing → docs → cleanup
3. **Independent testability**: Each task produces testable output on its own
4. **TDD included**: Unit tests are part of each implementation task, not separate tasks
5. **Clear boundaries**: Each task has a focused set of files to create or modify

## Process

### Step 1: Analyze the Feature/Spec

Read the input content and identify:

- **Domain entities** involved
- **Layers affected** (data, analysis, API, frontend, configuration)
- **New vs modified** components
- **External dependencies** needed
- **Cross-cutting concerns** (validation, error handling, logging)

### Step 2: Identify Work Units by Phase

Organize tasks into these phases, in order:

#### Phase: `setup`
Configuration, dependencies, environment setup tasks.

Examples:
- Add new packages / imports
- Create environment variables or config files
- Set up directory structure
- Define schemas or data models

#### Phase: `core`
Core logic, data processing, and business rules.

Examples:
- Implement data loading / transformation
- Create analysis functions
- Add validation logic
- Implement core algorithms

#### Phase: `integration`
Connecting components, scripts, and pipelines.

Examples:
- Wire up orchestrator / pipeline entry points
- Connect data sources to analysis modules
- Implement CLI or API layer
- Add routing or navigation entries

#### Phase: `testing`
Integration tests, end-to-end validation, and cross-component test suites.

Note: Unit tests are NOT in this phase — they are included in each `core` and `integration` task. This phase is for:
- Integration tests that span multiple components
- End-to-end pipeline validation
- Performance or load tests

#### Phase: `docs`
Documentation updates.

Examples:
- Update README or notebooks
- Add docstrings to public functions
- Create migration or usage guides

#### Phase: `cleanup`
Refactoring, dead code removal, optimization.

Examples:
- Remove deprecated code paths
- Refactor to use new patterns
- Optimize slow operations
- Clean up temporary workarounds

### Step 3: Create Task Objects

For each identified work unit, create a task object:

```json
{
  "id": "T-001",
  "title": "Create Nielsen data loader",
  "description": "Implement the data loading function in thesis/data/nielsen/scripts/loader.py. Load from CSV exports using polars. Include schema validation. Write unit tests confirming column names and row counts match expected values.",
  "status": "pending",
  "complexity": 0,
  "blockedBy": [],
  "blocks": ["T-002", "T-003"],
  "subtasks": [
    { "title": "Define loader function signature", "completed": false },
    { "title": "Implement CSV loading with polars", "completed": false },
    { "title": "Add schema validation", "completed": false },
    { "title": "Write unit tests", "completed": false }
  ],
  "tags": ["data", "nielsen", "loader"],
  "phase": "core",
  "qualityGate": {
    "lint": null,
    "typecheck": null,
    "tests": null
  },
  "timestamps": {
    "created": "2026-06-22T14:30:00.000Z",
    "started": null,
    "completed": null
  }
}
```

### Task Title Guidelines

Titles MUST use imperative verb + noun format:
- "Create Nielsen data loader"
- "Implement EDA summary statistics"
- "Add CLI entry point for pipeline"
- "Write integration tests for data flow"

Avoid vague titles:
- "Work on data" (too vague)
- "Fix things" (unclear scope)

### Task Description Guidelines

Each description MUST include:
1. **What to do** — Clear action to take
2. **Where to do it** — Specific files to create or modify (with paths)
3. **How to verify** — How to know the task is complete
4. **Test expectations** — What tests to write (for core/integration tasks)

### Step 4: Assign Dependencies

For each task, determine:

- **blockedBy**: Which task IDs must complete before this task can start
- **blocks**: Which task IDs depend on this task completing

Dependency rules:
1. Setup/config tasks block everything that uses them
2. Data loading tasks block analysis tasks
3. Core analysis tasks block integration tasks
4. Integration tasks block documentation
5. Testing phase tasks are blocked by the components they test
6. Cleanup tasks are blocked by everything they clean up

### Step 5: Identify Parallel Tracks

Group tasks that have no dependencies between each other. These can run simultaneously.

Common parallel tracks:
- Independent analysis modules (e.g., EDA for different datasets)
- Documentation for already-completed features
- Test suites for independent components

### Step 6: Validate

Before returning tasks:

1. **No orphan dependencies**: Every ID in `blockedBy`/`blocks` refers to an existing task
2. **No circular dependencies**: A does not (transitively) depend on itself
3. **No oversized tasks**: Any task >3 hours should be split further
4. **Phase consistency**: Tasks in earlier phases don't depend on later-phase tasks
5. **Complete coverage**: All aspects of the feature are covered
6. **Maximum 15 tasks**: If more needed, suggest splitting into phases

## Output

Return an array of task objects ordered by:
1. Phase (setup → core → integration → testing → docs → cleanup)
2. Dependency level within each phase (no deps first)

Also provide a brief summary:
- Total task count
- Breakdown by phase
- Identified parallel tracks
- Suggested starting tasks (those with no dependencies)

## Rules and Constraints

- Each task should modify a focused set of files (ideally 1-5 files)
- Include test writing as part of each implementation task, NOT as separate tasks (unless integration/e2e spanning multiple components)
- Maximum 15 tasks per spec; recommend splitting into phases if more needed
- Task IDs are sequential: T-001, T-002, T-003, etc.
- `complexity` field starts at 0
- All timestamps use ISO 8601 format
- All `qualityGate` fields start as null
- All tasks start with `status: "pending"`

## Step 7: Persist Tasks to Plan Folder

After calling `TaskCreate` for all tasks, **always** persist them to the active plan folder. In-memory tasks do not survive session end.

**Location**: `plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/tasks/<id>.json`

**JSON format** (matches `~/.claude/tasks` native format):

```json
{
  "id": "1",
  "subject": "Imperative task title",
  "description": "Full description with file paths and verification steps.",
  "activeForm": "Present-continuous spinner form",
  "status": "pending",
  "blocks": [],
  "blockedBy": []
}
```

Use a temp Python script to write all files atomically:

```python
import json
from pathlib import Path

PLAN_DIR = Path("plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>")
tasks_dir = PLAN_DIR / "tasks"
tasks_dir.mkdir(exist_ok=True)

for t in tasks:  # list of task dicts from TaskGet
    (tasks_dir / f"{t['id']}.json").write_bytes(
        json.dumps(t, indent=2).encode("utf-8")
    )
```

### Dual-Update Protocol (REQUIRED)

Every status change requires **two** updates — both must happen together:

| Action | In-session | Persisted JSON |
|--------|-----------|----------------|
| Start a task | `TaskUpdate taskId=N status=in_progress` | Write `tasks/N.json` with `"status": "in_progress"` |
| Complete a task | `TaskUpdate taskId=N status=completed` | Write `tasks/N.json` with `"status": "completed"` |
| Any other update | `TaskUpdate taskId=N ...` | Write `tasks/N.json` with updated fields |

**Single-file update snippet** (run immediately after each `TaskUpdate`):

```python
import json
from pathlib import Path

task_file = Path("plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/tasks/N.json")
data = json.loads(task_file.read_bytes())
data["status"] = "completed"
task_file.write_bytes(json.dumps(data, indent=2).encode("utf-8"))
```

### Reload Tasks in a New Session

```powershell
$plan = "plans/P0023_2026-06-22_14-30_active-plan"
$uuid = [guid]::NewGuid().ToString()
$dest = "$env:USERPROFILE\.claude\tasks\$uuid"
New-Item -ItemType Directory -Path $dest | Out-Null
Copy-Item "$plan\tasks\*.json" $dest
Write-Host "Tasks loaded into $dest — restart Claude Code to pick them up"
```

## Related

- [[config-prefer-task-list-breakdown]] — Task tracking workflow
- [[workflow-planning-with-files]] — Persistent disk-based planning
- `plans/PLANS_INDEX.md` — Master P-ID reference
