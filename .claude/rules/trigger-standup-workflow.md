---
paths:
  - "project_updates/"
---

# Standup Workflow

> Auto-loaded every session. Governs how Claude maintains the running standup draft and the full meeting lifecycle.

## File Roles

| File | Role |
|------|------|
| `standup_draft_formatting.md` | Gold standard blank template. Static — never written by skills. Read by `/init_standup` as structural scaffold. |
| `standup_draft.md` | Live active draft (LLM meta-notes always present). Updated by `/log_standup`. Source of truth for carry-over. Reset (overwritten) by `/init_standup`. |
| `standup_draft_archive.md` | Verbatim copy of previous meeting's completed draft (with meta-notes). Written by `/finalize_standup`. Read by `/init_standup` for carry-over. Permanent — do not delete. |
| `YYYY-MM-DD_HH-MM_update_meeting_N.md` | Single unified document: shown in meeting (created by `/prep_standup`) AND serves as final supervisor copy (overwritten by `/finalize_standup` after meeting edits). Includes full Progress Log for transparency. |

## Skill Triggers

| Skill | When to Run | Purpose |
|-------|-----------|---------|
| `/log_standup` | Anytime during the active meeting period when work is done | Append session entry to Progress Log in `standup_draft.md` |
| `/prep_standup` | Just before the supervisor meeting | Draft Non-Technical Summary, strip meta-notes, create `YYYY-MM-DD_HH-MM_update_meeting_N.md` (shown in meeting) |
| `/finalize_standup` | After the meeting, once post-meeting edits are done | Overwrite the meeting file with final version (including any post-meeting edits + full progress log) + archive verbatim draft |
| `/init_standup` | After finalization, to reset draft for the next meeting | Load template + carry over unchecked tasks + reset progress log |

## Trigger

Invoke the `/log_standup` skill to append a session entry to `project_updates/standup_draft.md`:

```
/log_standup
```

Do **not** wait to be asked twice. Do it inline, before continuing any other work.

---

## Auto-Trigger at Session End

At the end of every session **where writing or code changes were made**, append a session entry to
`project_updates/standup_draft.md` without being asked. If no changes occurred,
skip the auto-update (no noise entries).

---

## Entry Format

Append under the `## Progress Log` section using a date > priority > time hierarchy:

```
### YYYY-MM-DD                         ← create once per day; reuse if already present
#### [PRIMARY]                         ← omit if no primary work this session
##### HH-MM-SS — <short session title>
- <what was done toward thesis writing deliverables>

#### [SECONDARY]                       ← omit if nothing secondary done
##### HH-MM-SS — <short session title>
- <infrastructure/tooling work, only after primary was addressed>
```

**Insertion logic when appending:**
1. Get current wall-clock time: `datetime.datetime.now()` → `date_str = YYYY-MM-DD`, `time_str = HH-MM-SS`
2. If `### {date_str}` heading does **not** exist in the Progress Log → insert a new `### {date_str}` block in **descending date order** (most recent date first)
3. If `### {date_str}` already exists:
   - Find `#### [PRIMARY]` or `#### [SECONDARY]` subsection under it (whichever applies)
   - If the priority subsection exists → insert the new `##### HH-MM-SS` entry in **ascending time order** (earliest first) within that subsection
   - If priority subsection does **not** exist under that date → insert it with the `##### HH-MM-SS` entry at end of the date's block
4. Never overwrite existing entries — insert only

**Ordering rules:**
- Date headings (`### YYYY-MM-DD`): **descending** — most recent date at the top of the Progress Log
- Entries within a priority group (`##### HH-MM-SS`): **ascending** — earliest timestamp first, latest last

**Rules:**
- `[PRIMARY]` = thesis writing deliverables (chapters, sections, figure drafts, literature synthesis)
- `[SECONDARY]` = infrastructure, tooling, agents, code — only after primary tasks are addressed
- Be specific: name the chapter, section, or agent changed
- Keep bullets tight (1-2 lines each)

---

## Enforced Section Order

Every `standup_draft.md` must contain exactly these H2 sections in this order:

1. `## Non-Technical Summary Draft`
2. `## PRIMARY Tasks` (thesis writing deliverables)
3. `## SECONDARY Tasks` (infrastructure/tooling/code)
4. `## Backlog Tasks`
5. `## Performance Snapshot`
6. `## Current Focus (Next Steps)`
7. `## Progress Log`

`## Backlog Tasks` holds deprioritized items that are not committed deliverables for the supervisor. When initializing a new draft, carry relevant backlog items forward unless explicitly dropped.

---

## Pre-Meeting Reminder

If today is the day before or of a supervisor meeting and `project_updates/standup_draft.md` has not yet been
renamed/finalized, remind Brian at the start of the session:

> "The standup draft hasn't been finalized yet. Review `project_updates/standup_draft.md`
> and run `/prep_standup` before the meeting."

---

## Finalize Stand-up Draft

**Trigger:** `/finalize_standup` skill

**Actions (in order):**
1. Read `project_updates/standup_draft.md` (which now contains post-meeting edits)
2. Remove all internal meta-notes — delete lines matching `_(... Claude ...)_` patterns
3. Get current datetime: `date_str = YYYY-MM-DD`, `time_str = HH-MM`
4. Read meeting number N from H1: `# Standup Draft — Meeting N`
5. Write the cleaned content to `project_updates/{date_str}_{time_str}_update_meeting_{N}.md` (the finalized, supervisor-ready copy)
6. Write a **verbatim copy** of the original `standup_draft.md` (unmodified, with all meta-notes intact) to `project_updates/standup_draft_archive.md` — permanent, do not delete
7. Confirm: "Finalized as `project_updates/YYYY-MM-DD_HH-MM_update_meeting_N.md`. Archive updated. Run `/init_standup` when ready to begin the next meeting."

---

## Initialize Stand-up Draft

**Triggers:**
- Invoke `/init_standup` after `/finalize_standup` has run
- Or provide next meeting's agreed deliverables, and Claude will automatically initialize the new draft

**Actions (in order):**

**Pre-flight checks:**
1. Verify `project_updates/standup_draft_archive.md` exists. If not, stop with error: "No archive found. Run `/finalize_standup` first."
2. Verify `project_updates/standup_draft_formatting.md` exists. If not, stop with error: "Gold standard template missing."

**Initialization:**
1. Read `standup_draft_formatting.md` as the structural template
2. Read `standup_draft_archive.md` as the carry-over source
3. Determine meeting number: read N from archive H1 (`# Standup Draft — Meeting N`) → new draft = Meeting N+1
4. Write new `project_updates/standup_draft.md` with enforced section order

**Carry-over rules:**
- PRIMARY tasks: all `- [ ]` unchecked items; drop all `- [x]` completed
- SECONDARY tasks: same — unchecked only
- Backlog: carry all items unless Brian explicitly drops one
- Performance Snapshot: copy entire table verbatim (it accumulates across all meetings)
- Progress Log: start empty (NOT carried over)
- Non-Technical Summary: start blank (NOT carried over)
- LLM meta-comments: sourced from template (NOT from archive)

---

## Skill References

See the following for skill implementations:
- `.claude/skills/log_standup.md` — Log a session entry
- `.claude/skills/prep_standup.md` — Prepare for supervisor meeting
- `.claude/skills/finalize_standup.md` — Finalize the draft
- `.claude/skills/init_standup.md` — Initialize a new draft

---

## Priority Rule (Every Session)

1. **PRIMARY tasks first** — thesis writing deliverables (chapters, sections, outlines)
2. **SECONDARY tasks only if time remains** after primary work is done or meaningfully advanced
3. Never let SECONDARY work crowd out PRIMARY in the same session

This mirrors the `[PRIMARY]` / `[SECONDARY]` tagging in the standup entries.
