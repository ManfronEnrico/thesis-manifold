---
name: log_standup
description: Append a session entry to the standup draft following the project's trigger-standup-workflow
---

# Log Standup

Append a session entry to `project_updates/standup_draft.md` documenting what was accomplished this session.

## Usage

```
/log_standup
```

## How It Works

This skill implements the standup logging workflow from `.claude/rules/trigger-standup-workflow.md`:

1. **Reconstruct session work** — Review what was done this session
2. **Determine priority** — Classify as `[PRIMARY]` (thesis writing deliverables) or `[SECONDARY]` (infrastructure/tooling)
3. **Get current time** — `HH-MM-SS` timestamp for the entry
4. **Append to Progress Log** — Insert under the correct date and priority section

## Entry Format

Entries are inserted under the `## Progress Log` section using a **date > priority > time hierarchy**:

```
### YYYY-MM-DD                         ← create once per day; reuse if already present
#### [PRIMARY]                         ← omit if no primary work this session
##### HH-MM-SS — <short session title>
- <what was done toward thesis writing deliverables>

#### [SECONDARY]                       ← omit if nothing secondary done
##### HH-MM-SS — <short session title>
- <infrastructure/tooling work>
```

## Ordering Rules

- **Date headings** (`### YYYY-MM-DD`): **descending** — most recent date at the top
- **Entries within a priority group** (`##### HH-MM-SS`): **ascending** — earliest timestamp first

## Rules

- `[PRIMARY]` = thesis writing deliverables (chapters, sections, literature synthesis, figure drafts)
- `[SECONDARY]` = infrastructure, tooling, agent code — only after primary tasks are addressed
- Be specific: name the chapter, section, or agent changed
- Keep bullets tight (1-2 lines each)
