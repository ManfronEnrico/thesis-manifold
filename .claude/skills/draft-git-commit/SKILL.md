---
name: draft-git-commit
description: Generate a ready-to-paste git commit message from the current session. Trigger whenever the user mentions committing changes, preparing a git message, or wants to submit work. Includes worktree awareness (delegates setup to /using-git-worktrees), commit discipline check, trailers, draft PR reminder, and session summary.
compatibility:
  tools: [Bash, Read, Grep]
  requires: git repository
---

# Draft Git Commit Message

Generate a ready-to-paste git commit message with full session context, worktree safety checks, and audit metadata.

---

## When to use this skill

Invoke when:
- The user says "commit", "git commit", "prepare commit", "draft commit", "what should my commit message be?"
- The session has accumulated changes and the user wants to bundle them
- End of a session — always suggest committing before closing

**To execute the commit** (stage + submit), use `/git-commit` after the message is approved.

This skill never runs `git commit` itself — it only drafts the message.

---

## Algorithm

### Step 0 — Worktree and branch check

```bash
git branch --show-current
git worktree list
```

**Case A — in a worktree** (path contains `.cc/worktrees/`): Confirm which branch. Proceed freely.

**Case B — on a feature branch** (not `main`, not in a worktree): Proceed. Note the plain branch in the trailers.

**Case C — on `main`**: Stop. Delegate to `/using-git-worktrees` before proceeding.

```
⚠️  You are on `main`.

Run /using-git-worktrees to create an isolated workspace first.

Options:
  [1] Run /using-git-worktrees now (recommended)
  [2] Stay on main and commit anyway (only if merging completed work)
  [3] Cancel
```

---

### Step 1 — Commit discipline check

```bash
git diff --stat HEAD
git log --oneline -5
```

If the diff spans multiple unrelated areas, flag it and ask whether to split before continuing.

---

### Step 2 — Reconstruct session context

Review the conversation: what changed, why, what decisions were made. This is the primary input — more important than `git status` alone.

---

### Step 3 — Git state

```bash
git status --short
git log -1 --format="%H %ai %s"
```

Flag any files in `git status` that have no session record.

---

### Step 4 — Standup notes (if present)

If `project_updates/standup_draft.md` exists, extract entries after the last commit timestamp and merge into the changes list.

---

### Step 5 — Draft the commit message

```
<type>: <imperative subject, ≤60 chars>

- <what changed and why — one line per logical unit>
```

**Types:** `feat` · `fix` · `refactor` · `chore` · `docs` · `thesis` · `data`

Subject is imperative ("add", "fix", "update"). Bullets explain the *why*.

---

### Step 6 — Trailers block

Always include for this repo (collaborative, `cc/<id>/<slug>` branches).

```
Session-ID: cc-<YYYYMMDD-HHMM-initials>
Agent: claude-code
Operator: <git config user.name>
Worktree: <path, or "none — plain branch">
Base-Commit: <SHA>
```

```bash
git config user.name
git log -1 --format="%H"
```

If Enrico co-authored, add `Co-authored-by: Enrico <email>`. Never add `Co-authored-by: Claude`.

---

### Step 7 — Draft PR reminder

```
After committing, push and open a draft PR:

  git push -u origin <branch-name>
  gh pr create --draft --title "[cc <session-id>] <title>" --body "..."

Promote when done: gh pr ready
```

---

### Step 8 — Session summary (end of session)

When the user signals wrap-up, output:

```
Session-ID: cc-<YYYYMMDD-HHMM-initials>
Branch: <branch>
Worktree: <path or none>
PR: <link or "not yet opened">

Completed: <bullets>
Remaining: <bullets>
Files touched: <list>
Overlap risk: <files other branches may also touch>
Next action: <merge PR / continue / open reconcile branch>
```

---

## Example output

```
docs: slim draft-git-commit and add git-commit skill

- Remove inline worktree setup from draft-git-commit; delegate to /using-git-worktrees
- Add git-commit skill for staging and submitting approved messages
- Rename draft-commit → draft-git-commit for clarity

Session-ID: cc-20260420-br
Agent: claude-code
Operator: brianrohde
Worktree: none — plain branch
Base-Commit: 18456b6
```

---

## Reference docs

- Worktree setup: `/using-git-worktrees`
- Commit submission: `/git-commit`
- Full worktree guide: `docs/reference/git-worktrees-and-parallel-sessions.md`
- Branch strategy: `docs/reference/git-branch-strategy.md`
- Trigger rule: `.claude/rules/trigger-git-commit-workflow.md`
