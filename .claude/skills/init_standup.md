---
name: init_standup
description: Initialize a new standup draft for the next meeting following the project's trigger-standup-workflow
---

# Initialize Standup Draft

Initialize a new standup draft for the next meeting. Carries over unchecked tasks, backlog items, and the performance snapshot from the previous draft.

## Usage

```
/init_standup
/standup_done
```

Both commands trigger the same workflow (for convenience).

**Alternative:** Provide next meeting's agreed deliverables immediately after standup, and Claude will automatically initialize the new draft.

## How It Works

This skill implements the initialize standup workflow from `.claude/rules/trigger-standup-workflow.md`:

1. **Pre-flight checks** — Verify `standup_draft_archive.md` and `standup_draft_formatting.md` exist. Stop with error if either is missing.
2. **Read template** — Read `standup_draft_formatting.md` as structural base
3. **Read archive** — Read `standup_draft_archive.md` for carry-over: all [ ] tasks, all backlog, full Performance Snapshot table
4. **Determine N+1** — Read meeting number from archive header, increment by 1
5. **Compose new draft** — Combine template structure + carried-over content (no [x] tasks, no old Progress Log entries)
6. **Overwrite** `project_updates/standup_draft.md`

## Carry-Over Rules

- **PRIMARY tasks** — All unchecked `- [ ]` items (and sub-items); drop all `- [x]` completed
- **SECONDARY tasks** — Same as PRIMARY — unchecked only
- **Backlog tasks** — Carry all items unless you explicitly drop one
- **Performance Snapshot** — Copy entire table verbatim (accumulates across all meetings)
- **Progress Log** — Start empty
- **Non-Technical Summary** — Start blank

## Input

If you dictate new PRIMARY tasks immediately after standup, they will be inserted at the top of the PRIMARY section.

## Output

Confirmation: `"Initialized project_updates/standup_draft.md for Meeting N+1."`
