# Git Worktrees and Parallel Sessions — Plain-Language Guide

> For Brian and Enrico: how to run multiple Claude Code sessions safely in one repo.

---

## The core problem this solves

Imagine two people (or two Claude sessions) both working in the same folder.
They're on different branches, but they share one invisible holding zone — the **staging area** — where `git add` puts files before a commit.

If Chat A runs `git add -A` and doesn't commit yet, then Chat B runs a commit,
Chat B accidentally sweeps up Chat A's staged files too. This is exactly what
caused a 300-file accidental commit in this project.

Worktrees solve this by giving each session a **physically separate folder** on disk.

---

## Branches vs. Worktrees — the plain-language difference

| Concept | Analogy | Technical reality |
|---|---|---|
| **Branch** | A parallel storyline in a book | A logical label pointing to a commit chain — only one branch can be "active" in a folder at a time |
| **Worktree** | A second physical copy of the house | A separate folder on disk, each with its own staging area and active branch |

**With plain branches (what we had before):**
- `CMT_Codebase/` is the one house
- Switching branches redecorates the rooms — same house, different wallpaper
- Two terminals in the same folder share the same staging area → collision risk

**With worktrees (what we're moving to):**
- `CMT_Codebase/` remains the "main house" — you work here for single-session work
- `CMT_Codebase/.cc/worktrees/session-a/` is a second house for Chat A
- `CMT_Codebase/.cc/worktrees/session-b/` is a third house for Chat B
- All three houses share the same basement (git history, all commits ever made)
- But each has its own rooms (files), its own staging area, and its own active branch
- Git physically prevents two worktrees from being on the same branch at the same time

---

## How it works in practice

### Starting a session with a worktree

You do not manually create a folder. One command does everything:

```bash
# Format: git worktree add <path> <branch-name>
git worktree add .cc/worktrees/session-config cc/20260420-1530/config-fix
```

This:
1. Creates the folder `.cc/worktrees/session-config/`
2. Creates the branch `cc/20260420-1530/config-fix`
3. Checks that branch out into the new folder
4. All in one shot

Then open that folder in VS Code or point your terminal at it:

```bash
cd .cc/worktrees/session-config
# or open in VS Code: code .cc/worktrees/session-config
```

From this point, everything Claude Code does in that terminal is isolated to this folder and this branch.

### Ending a session

```bash
# From the main CMT_Codebase folder (not inside the worktree)
git worktree remove .cc/worktrees/session-config
```

This deletes the folder. The branch and all commits survive in git history — you haven't lost anything. You can still merge that branch to `main` after removing the worktree.

### Listing active worktrees

```bash
git worktree list
```

Example output:
```
C:/Users/brian/.../CMT_Codebase              abc1234 [main]
C:/Users/brian/.../worktrees/session-config  def5678 [cc/20260420-1530/config-fix]
C:/Users/brian/.../worktrees/session-thesis  ghi9012 [cc/20260420-1605/thesis-ch3]
```

---

## Session startup workflow (full)

This is the recommended sequence every time you start a new Claude Code session:

```bash
# 1. Go to the main repo folder
cd "C:/Users/brian/.../CMT_Codebase"

# 2. Sync with remote (get latest from GitHub)
git fetch origin
git checkout main
git pull

# 3. Create a session ID (date + time + initials)
#    Format: cc-YYYYMMDD-HHMM-XX  (XX = your initials: br = Brian, en = Enrico)
#    Example: cc-20260420-1530-br

# 4. Create the worktree + branch in one command
git worktree add .cc/worktrees/<short-name> cc/<session-id>/<slug>

# Example (Brian, working on config):
git worktree add .cc/worktrees/config-fix cc/20260420-1530-br/config-fix

# 5. Open the worktree folder in your terminal or VS Code
cd .cc/worktrees/config-fix
```

From step 5 onward, all Claude Code work happens inside this folder. The main `CMT_Codebase` folder is untouched.

---

## Session naming conventions

### Branch names

```
cc/<session-id>/<slug>

cc/20260420-1530-br/config-permissions     ← Brian, config work
cc/20260420-1605-en/thesis-ch3-bullets     ← Enrico, thesis content
cc/20260420-1720-br/data-nielsen-cache     ← Brian, data scripts
cc/20260420-1800-br/reconcile-ch3-overlap  ← reconcile branch (see below)
```

The session ID encodes who did the work and when. Six months from now, you can trace any commit back to a specific session.

### Worktree folder names (short, human-readable)

```
.cc/worktrees/config-fix
.cc/worktrees/thesis-ch3
.cc/worktrees/data-cache
```

These are temporary folders — they get removed when the session ends.

---

## Committing during a session — checkpoint rule

**Do not commit after every file edit.** This creates noisy history that's hard to review and hard to roll back.

**Do commit at logical checkpoints:**

| Trigger | Example |
|---|---|
| The diff has one clear purpose | "Added all methodology bullets for RQ2" |
| Before a risky operation (rebase, major restructure) | "Checkpoint before reorganising section order" |
| Before handing off to another person | "End-of-session checkpoint — remaining work in PR" |
| End of the session | Always commit before closing the terminal |

**The test:** If you can't write a one-line commit message that explains *why* these changes belong together, it's probably not a clean checkpoint yet.

### Commit message format

```
<type>: <subject line, ≤60 chars>

<optional body — why this change exists>

Session-ID: cc-20260420-1530-br
Agent: claude-code
Operator: brianrohde
Base-Commit: abc1234
```

The lines at the bottom are **trailers** — structured metadata. They're optional but recommended for collaborative repos (like this one) because they make every Claude-assisted commit traceable.

**Commit types:**

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

## Draft PRs — remote backup and audit trail

As soon as you reach the first meaningful checkpoint, push the branch and open a **draft PR** on GitHub.

A draft PR:
- **Cannot be accidentally merged** — it's locked until you promote it to "Ready for review"
- **Backs up your work remotely** — if your machine dies, nothing is lost
- **Creates a permanent audit record** — the PR shows every commit, every file changed, every discussion

```bash
# Push the branch
git push -u origin cc/20260420-1530-br/config-fix

# Open a draft PR (GitHub CLI)
gh pr create --draft \
  --title "[cc 20260420-1530-br] Config permissions fix" \
  --body "Objective: Fix git commit being blocked by global deny rules.
Files touched: .claude/settings.json, .claude/settings.local.json
Status: In progress"
```

When the session is done and the work is reviewed, promote to ready:

```bash
gh pr ready
```

Then merge through GitHub UI — never push directly to `main`.

---

## What Enrico needs to do (collaborator setup)

When Enrico clones the repo, worktrees work exactly the same way on his machine.
The `.cc/worktrees/` folder is in `.gitignore` — it's local to each person's computer.

Enrico's setup:

```bash
# Clone the repo
git clone <repo-url> CMT_Codebase
cd CMT_Codebase

# Start a session
git fetch origin
git worktree add .cc/worktrees/thesis-intro cc/20260420-1530-en/thesis-intro-bullets
cd .cc/worktrees/thesis-intro
```

From that point his workflow is identical to Brian's. Each person has their own physical folder, their own branch, their own staging area. When both push branches to GitHub and open draft PRs, you review each other's work before merging.

If both sessions happened to touch the same file, the PR diff will show it clearly before anything reaches `main`.

---

## Conflict detection and reconcile workflow

Git cannot stop two branches from editing the same file — only the merge step reveals the conflict. The goal is to **detect overlap before merge**, not repair it afterward.

### Detection rule

Before merging any branch to `main`, check whether other open branches touched the same files:

```bash
# See which files branch A changed
git diff --name-only main..cc/20260420-1530-br/config-fix

# See which files branch B changed
git diff --name-only main..cc/20260420-1605-en/thesis-ch3

# Compare the two lists manually — any file appearing in both = overlap risk
```

### If overlap is found — reconcile workflow

1. Keep both PRs as **draft** — don't promote either yet
2. One person (the "merge steward") creates a reconcile branch and worktree:
   ```bash
   git worktree add .cc/worktrees/reconcile cc/20260420-1800-br/reconcile-config-ch3
   cd .cc/worktrees/reconcile
   ```
3. Merge both candidate branches in, one at a time:
   ```bash
   git merge cc/20260420-1530-br/config-fix
   git merge cc/20260420-1605-en/thesis-ch3
   ```
4. Resolve any conflicts manually — edit the files, keep the right content
5. Push the reconcile branch and open a PR titled "Reconcile: config-fix + thesis-ch3"
6. Review the final combined diff together
7. Merge only the reconcile PR into `main`

---

## Merge strategy — which button to click on GitHub

GitHub offers three merge options. For this project:

| Option | Use it when | Why |
|---|---|---|
| **Merge commit** ✅ Default | Always | Preserves every commit from the branch; creates a visible integration event; full audit trail |
| **Squash and merge** | Branch has messy micro-commits you want to clean up | Collapses everything to one commit on `main` — simpler history, but loses detail |
| **Rebase and merge** ❌ Avoid | Never | GitHub rewrites commit SHAs and timestamps — breaks traceability and signed commits |

**Default rule: always use Merge commit.**

---

## Quick reference — daily commands

```bash
# Start a session
git fetch origin && git pull
git worktree add .cc/worktrees/<name> cc/<date-id-initials>/<slug>
cd .cc/worktrees/<name>

# Check where you are
git branch                          # shows current branch (* = active)
git worktree list                   # shows all active worktrees

# Commit at a checkpoint
git add -A                          # safe — worktree is isolated
git commit -m "<type>: <message>"

# Push and open draft PR
git push -u origin <branch-name>
gh pr create --draft --title "[cc <id>] <title>" --body "<description>"

# End a session
cd ../..                            # back to CMT_Codebase root
git worktree remove .cc/worktrees/<name>

# Check for overlap before merging
git diff --name-only main..<branch-a>
git diff --name-only main..<branch-b>

# Merge to main (through GitHub PR, not command line)
gh pr ready                         # promote draft to ready
# then merge via GitHub UI
```

---

## What's in `.gitignore` for this workflow

The `.cc/worktrees/` folder is excluded from git tracking — it's local scaffolding, not code. Each collaborator has their own worktrees on their own machine.

```
.cc/worktrees/
```

This is already added to `.gitignore` as part of this workflow setup.
