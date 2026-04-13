---
paths:
  - "**"
---

# Git Commit Workflow

> Auto-loaded every session. Governs how Claude generates a ready-to-paste git commit message by combining current session context, the standup draft, git history, and working tree state.

## Trigger

Invoke the `/draft_commit` skill to generate a ready-to-paste commit message.

```
/draft_commit
```

Do **not** wait to be asked twice. Do it inline, before continuing any other work.

---

## Deduction Algorithm

Run these steps in order. Each informs the next.

### Step 0 — Reconstruct current session work (PRIMARY source)
Before touching any external data, recall everything done in the **current session** from conversation context:
- What files were created, modified, or deleted
- What logic was changed and why
- What problems were solved
- What was deferred or left incomplete

This is the richest source of commit content — more detailed than standup entries, which are summaries. Use the session context to write the commit body, then validate and supplement with the steps below.

### Step 1 — Get git status
```bash
git -C "PROJECT_ROOT" status --short
```
Produces the list of modified, staged, and untracked files. Cross-reference with the session context to confirm which changes are on disk and ready to commit.

### Step 2 — Get last commit timestamp
```bash
git -C "PROJECT_ROOT" log -1 --format="%H %ai %s"
```
Returns: `<hash> <ISO datetime with offset> <subject>`. This is the cutoff: any standup entry timestamped **after** this datetime = uncommitted work from **any** session.

Also run for broader context:
```bash
git -C "PROJECT_ROOT" log --oneline -5
```

### Step 3 — Read standup_draft.md Progress Log
Read `project_updates/standup_draft.md` in full.

Extract all `#### HH-MM-SS — <title>` entries under the current date (`## YYYY-MM-DD`).

**Timestamp comparison logic:**
- Combine the entry's date heading (`## YYYY-MM-DD`) with its time (`HH-MM-SS`) → full datetime
- If that datetime > last commit datetime → **uncommitted** → include in commit message
- If that datetime ≤ last commit datetime → **already committed** → exclude

### Step 4 — Cross-reference all sources
Merge session context + standup entries into a unified list of uncommitted changes:
- If `git status` shows a file that matches session context or a standup entry → confirmed uncommitted
- If `git status` shows files with **no** corresponding session context or standup entry → note as "undocumented changes" in the commit body

### Step 5 — Draft commit message

Format:
```
<type>: <short imperative subject, ≤ 60 chars>

- <bullet: what changed and why — one line per logical unit of work>
- <bullet: ...>

Sessions: <HH-MM-SS>, <HH-MM-SS>  ← timestamps of included standup entries
```

**`<type>` values**: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`
- `feat` — new user-facing functionality or thesis chapter content
- `fix` — correcting a bug or factual error
- `chore` / `docs` — tooling, rules, or documentation-only changes
- `refactor` — structural changes with no behaviour change

**Subject line rules:**
- Imperative mood ("add X", "fix Y", not "added" / "adding")
- No period at end
- ≤ 60 characters

---

## Output Format

Present the commit message in a single fenced code block so Brian can copy it directly:

````
```
chore: add .claude infrastructure and standup workflow

- Created .claude/rules/ (8 rule files) and .claude/skills/ (7 skills)
- Installed PreToolUse hook for OneDrive safety
- Initialized project_updates/ standup infrastructure
- Created dev/repository_map.md and docs/tooling-issues.md

Sessions: 19-00-00
```
````

Then add a brief note below the block:
- Which standup entries were included (with timestamps) and why
- Any files in `git status` with no matching session record

---

## Skill Reference

See `.claude/skills/draft_commit.md` for the skill implementation.
