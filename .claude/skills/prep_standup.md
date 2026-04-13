---
name: prep_standup
description: Draft non-technical summary and produce presentation-ready copy for the supervisor meeting
---

# Prep Standup

Prepares the standup draft for the supervisor meeting by drafting the Non-Technical Summary and producing a clean presentation-ready copy.

## Usage

```
/prep_standup
```

Run this just before the supervisor meeting.

## How It Works

This skill implements the pre-meeting preparation workflow:

1. **Read** `project_updates/standup_draft.md`

2. **Draft Non-Technical Summary** — Claude writes a concise summary of PRIMARY task progress, suitable for a non-technical supervisor. This summary should:
   - Highlight key accomplishments since the last meeting
   - Mention any major blockers or risks (e.g., data access delays)
   - Keep to 3-5 bullet points
   - Be written in clear, non-technical language appropriate for a CBS thesis supervisor
   - Write this directly into `standup_draft.md` under `## Non-Technical Summary Draft`

3. **Strip meta-notes & create finalized copy** — Remove all internal Claude notes:
   - Delete all lines matching `_(... Claude ...)_` patterns
   - Delete lines 2-3 of the header (the "Updated incrementally..." and "Manual trigger..." lines)
   - Write the cleaned content to `project_updates/YYYY-MM-DD_HH-MM_update_meeting_N.md` (this will be used as the presentation document during the meeting)

4. **Confirm** — Report that the document is ready for the meeting. Remind user that during/after the meeting, any edits (additional To-Dos, task updates, progress log entries) should be made directly in `standup_draft.md`, then `/finalize_standup` is run to prepare the final supervisor copy.

## Important

- `standup_draft.md` is NOT modified by this skill — it retains all meta-notes as the source of truth
- The output file (`YYYY-MM-DD_HH-MM_update_meeting_N.md`) is clean and ready to show in the meeting
- During the meeting, Brian can edit this output file directly if needed, or make changes to `standup_draft.md` afterward
- After the meeting, run `/finalize_standup` which will overwrite this file with the final version including any post-meeting edits
- Supervisors see the complete document including the full Progress Log (all activity since last meeting)
