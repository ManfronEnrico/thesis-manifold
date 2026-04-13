---
paths:
  - "**"
---

# Plan Workflow

> Auto-loaded every session. Governs how Claude updates plan files after execution.

## Trigger

Invoke the `/update_plan` skill (optionally followed by a plan name or partial filename):

```
/update_plan
/update_plan <plan-name-or-partial-filename>
```

Claude must execute the following steps **in order**:

1. **Locate the plan file** — search both `~/.claude/plans/` (global) and `<project-root>/.claude/plans/` (project). Prefer the project location if a copy already exists there.
2. **Relocate if misplaced** — if the file is in the global `~/.claude/plans/` folder, move it to the project's `.claude/plans/` folder (see "Relocate & Rename" below) before doing anything else.
3. **Rename if needed** — if the filename does not follow `YYYY-MM-DD_<short-slug>.md`, rename it to a proper slug derived from the plan's title or topic.
4. **Append the `## Outcome` section** to the correctly located and named file.

Do **not** wait to be asked twice. Do it inline, before continuing any other work.

---

## Outcome Section Format

Append at the **bottom** of the plan file:

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
<any other context useful for future reference — deviations, insights, follow-up work>
```

Omit `### 🔄 Adjusted`, `### ❌ Dropped`, or `### Notes` entirely if there is nothing to record.

---

## When to Apply

- Triggered manually by Brian saying `"update plan"` after a plan has been executed.
- Do **not** auto-trigger — always wait for Brian to confirm he is happy with the outcome first.
- If multiple plans were touched in a session, ask Brian which one to update (or update all if he says so).

---

## Relocate & Rename

When the plan file is found in the wrong location or has a non-conforming name, Claude must fix it **before** appending the Outcome section. Steps:

1. **Read** the file content from its current path (global or misnamed).
2. **Derive the correct filename**: `YYYY-MM-DD_<short-slug>.md`
   - Use today's date (or the plan's creation date if visible in the content).
   - Derive the slug from the plan's title or topic — lowercase, hyphen-separated, ≤ 5 words.
   - Example: a plan titled "LaTeX pipeline setup" created on 2026-04-14 → `2026-04-14_latex-pipeline-setup.md`
3. **Write** the content to `<project-root>/.claude/plans/<correct-filename>.md` using the Write tool.
4. **Delete** the original misplaced/misnamed file using `Bash`: `rm "<original-path>"`.
5. Confirm to Brian: `Moved → .claude/plans/<correct-filename>.md` (one line, inline).
6. Continue with appending the Outcome section to the new path.

Do NOT leave the original file in place after moving. Do NOT create duplicates.

---

## Plan File Location

All plan files live in the **active project's own directory**: `<project-root>/.claude/plans/`
Do NOT save plans to the global `~/.claude/plans/` folder.

Naming convention: `YYYY-MM-DD_<short-slug>.md`
Do NOT use auto-generated random names (e.g. `valiant-booping-widget.md`). Always use a short descriptive slug.

---

## Skill Reference

See `.claude/skills/update_plan.md` for the skill implementation.
