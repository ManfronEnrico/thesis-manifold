---
name: finalize_standup
description: Clean and finalize the standup draft for delivery to supervisor following the project's trigger-standup-workflow
---

# Finalize Standup

Finalize the standup draft by overwriting the meeting document with post-meeting edits and archiving the source.

## Usage

```
/finalize_standup
```

## How It Works

This skill implements the finalize standup workflow from `.claude/rules/trigger-standup-workflow.md`:

1. **Read** `project_updates/standup_draft.md` (includes any post-meeting edits, new to-dos, updated status)
2. **Strip meta-notes** — Remove all internal Claude notes (`_(... Claude ...)_` patterns)
3. **Overwrite meeting file** — Write cleaned content to `project_updates/YYYY-MM-DD_HH-MM_update_meeting_N.md` (this replaces the pre-meeting version with final supervisor copy)
4. **Archive** — Write verbatim `standup_draft.md` (with all meta-notes) to `project_updates/standup_draft_archive.md` as carry-over source

## Output

Two files are maintained:

- **`project_updates/YYYY-MM-DD_HH-MM_update_meeting_N.md`** — Final supervisor copy (clean, with all post-meeting updates + full Progress Log)
- **`project_updates/standup_draft_archive.md`** — Permanent backup with all meta-notes intact (carry-over source for `/init_standup`)

The supervisor receives the single clean document showing all work done, with full transparency of the Progress Log.

## Important

The `standup_draft.md` remains unchanged after finalization. Run `/init_standup` when ready to begin the next meeting cycle.
