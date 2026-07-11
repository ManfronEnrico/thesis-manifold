# Contributor Guide — Git Workflow

This guide explains how to work on the thesis codebase without breaking `main`.
It applies to all contributors (Brian, Enrico, supervisors with edit access).

---

## The Golden Rule

```
main = only stable, reviewed work
branch = where all actual work happens
```

Never commit directly to `main`. Every piece of work lives on its own branch first.

---

## Step-by-Step Workflow

### 1. Start a session — create a branch

Open Claude Code and run:
```
/git-worktrees
```
This creates an isolated workspace at `.cc/worktrees/<topic>/` and a branch
named after your topic (e.g. `thesis/ch2-literature`, `config/zotero-setup`).

Do all your work inside that worktree.

---

### 2. Commit as you go

When you have a logical chunk of work done:
```
/git-draft-commit    ← Claude generates a commit message from your session
/git-commit          ← stages files and runs the commit
```

You can commit multiple times per session.

---

### 3. End of session — merge back to main

Run:
```
/git-worktree-merge
```

Claude will:
- Show you what changed
- Check if any other open branches touch the same files
- If no overlap → push your branch and open a **draft PR** on GitHub
- If overlap → guide you through a **reconcile** step first

---

### 4. Merge to main

**Option A — via GitHub (recommended for review)**
1. Go to the repo on GitHub
2. Switch to your branch using the branch dropdown
3. Review the diff to confirm it looks right
4. Click **"Ready for review"** (removes draft status)
5. Click **"Merge pull request"** → **"Create a merge commit"**

**Option B — from the terminal (faster, skip browser)**
```
gh pr merge <PR-number> --merge
```
Find the PR number from the output of `/git-worktree-merge`.

---

### 5. Pull main locally and clean up

```bash
git checkout main
git pull origin main
git worktree remove .cc/worktrees/<name> --force
```

Or delete the `.cc/worktrees/` folder manually in Windows Explorer — both work.

---

## When Two Sessions Touch the Same Files

If you and a colleague both have open branches that edit the same file,
`/git-worktree-merge` will detect this and suggest a **reconcile workflow**:

1. A new reconcile branch is created from `main`
2. Both branches are merged into it (conflicts resolved manually)
3. Only the reconcile branch is merged to `main`

This happened on 2026-04-20 when three branches were merged simultaneously —
see the reconcile PR #2 in the GitHub history as an example.

---

## Branch Naming Convention

| Prefix | Use for |
|--------|---------|
| `thesis/<topic>` | thesis content (chapters, outline, RQs) |
| `data/<topic>` | data scripts or pipeline |
| `config/<topic>` | settings, tooling, integrations |
| `chore/<topic>` | refactoring, cleanup |
| `session/<topic>` | exploratory / general work |
| `cc/<date>-<initials>/<topic>` | Claude Code worktree sessions |

---

## What to Never Do

- **Never commit directly to `main`** — the branch guard hook will warn you
- **Never force-push to `main`**
- **Never delete `.cc/` from `.gitignore`** — it holds local worktree folders that shouldn't be tracked

---

## Quick Reference

| Task | Command |
|------|---------|
| Start new session | `/git-worktrees` |
| Generate commit message | `/git-draft-commit` |
| Run the commit | `/git-commit` |
| Merge branch to main | `/git-worktree-merge` |
| Merge PR from terminal | `gh pr merge <number> --merge` |
| Pull latest main | `git pull origin main` |

---

## Further Reading

- [git-branch-strategy.md](git-branch-strategy.md) — full branch naming spec
- [git-worktrees-and-parallel-sessions.md](git-worktrees-and-parallel-sessions.md) — parallel session and reconcile workflow details
