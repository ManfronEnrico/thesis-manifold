# Git Branch Strategy — Multi-Session Claude Code Workflow

> For Brian and Enrico. Full worktree guide: `docs/reference/git-worktrees-and-parallel-sessions.md`

---

## Core model: branch-per-session, worktree-per-session, PR-per-task

Each Claude Code session gets:
- Its **own branch** — isolated commit history
- Its **own worktree** — a physically separate folder on disk, its own staging area
- Its **own draft PR** — remote backup + audit trail on GitHub

Nothing a session does can bleed into `main` or another session's work.

```
main (GitHub — protected, never pushed to directly)
 ├── cc/20260420-1530-br/config-fix       ← Brian's Chat A (worktree: .cc/worktrees/config-fix)
 ├── cc/20260420-1605-en/thesis-ch3       ← Enrico's Chat B (worktree: his machine)
 └── cc/20260420-1720-br/data-cache       ← Brian's Chat C (worktree: .cc/worktrees/data-cache)
          ↓ each reviewed via draft PR, then merged to main separately
```

---

## Git concepts — plain language

| Term | What it means |
|---|---|
| **Repository** | The tracked project folder (`CMT_Codebase`) |
| **Branch** | A logical parallel version — commits here don't affect other branches |
| **Worktree** | A physically separate folder, each with its own branch and staging area |
| **`main`** | The primary branch — stable, reviewed work only |
| **Staging area** | The holding zone between editing and committing — `git add` moves files here |
| **Commit** | A saved snapshot with a message, saved on the current branch |
| **Draft PR** | A GitHub pull request locked from merging — for backup and visibility only |
| **Merge commit** | Brings a branch into `main` while preserving all branch commits |
| **Reconcile branch** | A temporary branch for combining two overlapping branches before merging |

---

## Session startup — run this at the start of every Claude Code session

```bash
# 1. Sync with remote
cd "C:/Users/.../CMT_Codebase"
git fetch origin && git checkout main && git pull

# 2. Create worktree + branch (one command)
git worktree add .cc/worktrees/<short-name> cc/<date-time-initials>/<slug>

# Example — Brian starting a config session at 15:30 on 2026-04-20:
git worktree add .cc/worktrees/config-fix cc/20260420-1530-br/config-fix

# 3. Move into the worktree — all work happens here
cd .cc/worktrees/config-fix
```

### Branch naming convention

```
cc/<YYYYMMDD-HHMM-initials>/<slug>

cc/20260420-1530-br/config-permissions    ← Brian
cc/20260420-1605-en/thesis-ch3-bullets    ← Enrico
cc/20260420-1720-br/data-nielsen-cache    ← Brian, second session
cc/20260420-1800-br/reconcile-ch3-config  ← reconcile branch
```

**Initials:** `br` = Brian, `en` = Enrico

---

## Committing — checkpoint rule

**Do not commit after every file edit.** Commit at logical checkpoints only.

**Commit when:**
- The diff has **one clear purpose** — one commit, one story
- The code is in a stable, reviewable state
- Before a risky operation (rebase, major restructure)
- Before handing off to the other person
- At **end of session** — always commit before closing

**The test:** If you can't write a one-line message explaining why all these changes belong together, don't commit yet.

### Commit message format

```
<type>: <subject, ≤60 chars>

<optional body — why this change exists>

Session-ID: cc-20260420-1530-br
Agent: claude-code
Operator: brianrohde
Base-Commit: abc1234
```

The bottom lines are **trailers** — structured metadata for traceability. Recommended for this collaborative repo.

| Type | When |
|---|---|
| `feat` | New feature or capability |
| `fix` | Bug or error correction |
| `refactor` | Restructuring, no behavior change |
| `chore` | Config, tooling, settings |
| `docs` | Documentation only |
| `thesis` | Thesis content (bullets, sections) |
| `data` | Data scripts or pipeline |

---

## Draft PRs — push early, merge late

As soon as you reach the first checkpoint, push and open a draft PR:

```bash
git push -u origin cc/20260420-1530-br/config-fix

gh pr create --draft \
  --title "[cc 20260420-1530-br] Config permissions fix" \
  --body "Objective: ...
Files touched: ...
Status: In progress"
```

A draft PR cannot be merged accidentally. It gives you remote backup, a full diff view, and a permanent audit record of what the session did.

When the session work is reviewed and ready:
```bash
gh pr ready   # promote to ready-for-review
# then merge via GitHub UI — never push directly to main
```

---

## Merge strategy — always use Merge Commit

| GitHub option | Use? | Why |
|---|---|---|
| **Merge commit** | ✅ Default | Preserves all branch commits; visible integration event; full audit trail |
| **Squash and merge** | Only if branch has messy micro-commits | Collapses to one commit — simpler but loses detail |
| **Rebase and merge** | ❌ Never | Rewrites commit SHAs — breaks traceability and signed commits |

---

## Overlap detection — before merging any PR

Check whether another open branch touched the same files:

```bash
# Files changed in branch A
git diff --name-only main..cc/20260420-1530-br/config-fix

# Files changed in branch B
git diff --name-only main..cc/20260420-1605-en/thesis-ch3
```

If any file appears in both lists → use the reconcile workflow (see `git-worktrees-and-parallel-sessions.md`).

---

## End-of-session checklist

```
[ ] Committed all session work (at logical checkpoint)
[ ] Pushed branch to remote
[ ] Draft PR open and description updated
[ ] Removed local worktree: git worktree remove .cc/worktrees/<name>
[ ] Branch stays alive on GitHub until PR is merged — don't delete it yet
```

---

## Quick reference

```bash
# Start session
git fetch origin && git pull
git worktree add .cc/worktrees/<name> cc/<date-id>/<slug>
cd .cc/worktrees/<name>

# During session — commit at checkpoints
git add -A
git commit -m "<type>: <message>"

# Push and open draft PR
git push -u origin <branch>
gh pr create --draft --title "[cc <id>] <title>" --body "..."

# End session
cd ../..
git worktree remove .cc/worktrees/<name>

# Check all active worktrees
git worktree list

# Check overlap before merging
git diff --name-only main..<branch-a>
git diff --name-only main..<branch-b>
```

---

## Why this matters — the 300-file incident

Before this strategy was in place, two Claude sessions were both working in the main `CMT_Codebase` folder on `main`. Session A ran `git add -A` and left files staged. Session B then committed — and swept up all of Session A's staged files too. Result: a 300-file commit that had nothing to do with the intended change.

Worktrees eliminate this entirely. Each session has its own staging area. It is physically impossible for one to sweep up another's staged files.
