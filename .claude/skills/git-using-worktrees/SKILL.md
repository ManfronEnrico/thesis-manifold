---
name: git-using-worktrees
description: Use when starting a new Claude Code session that needs isolation — creates a git worktree under .cc/worktrees/ with the project branch naming convention, safety checks, and branch mismatch detection. Pairs with /git-draft-commit for cleanup and audit.
---

# Using Git Worktrees

## Overview

Git worktrees give each Claude Code session a **physically separate folder** with its own staging area, preventing the cross-session staging collisions that caused a 300-file accidental commit in this project.

**Core principle:** One session → one worktree → one branch. Never two sessions in the same folder simultaneously.

**Claude Code integration:** After creating a worktree, launch a new Claude Code session in that directory for full isolation (different context, separate git state). See Step 4 for instructions.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

---

## This Project's Conventions

| Convention | Value |
|---|---|
| Worktree root | `worktrees/<slug>/` at repo root level |
| Branch naming | `cc/<YYYYMMDD-HHMM>/<slug>` |
| Gitignored | `worktrees/` is already in `.gitignore` — no action needed |
| Reference guide | `docs/reference/git-worktrees-and-parallel-sessions.md` |
| Branch strategy | `docs/reference/git-branch-strategy.md` |
| Rules | `.claude/rules/worktree-workflow.md` |

**Examples:**
```
worktrees/nielsen-fix/    →  branch: cc/20260420-1430/nielsen-fix
worktrees/chapter-2/      →  branch: cc/20260420-1600/chapter-2
worktrees/data-pipeline/  →  branch: cc/20260421-0900/data-pipeline
```

---

## Step 0 — Verify `worktrees/` is gitignored

**PowerShell:**
```powershell
git check-ignore -q worktrees
```

**Bash (in Claude CLI):**
```
! git check-ignore -q worktrees
```

If NOT ignored, add it before continuing:
1. Add `worktrees/` to `.gitignore`
2. Commit: `git add .gitignore && git commit -m "chore: gitignore worktrees directory"`
3. Proceed

This is the most critical safety check — worktree contents must never be tracked.

---

## Step 1 — Derive branch name from session topic

From the user's task, extract 2–4 keywords and build the branch name:

```
Topic: "fix Nielsen auth token"
Slug:  nielsen-auth-fix
Date:  2026-04-20, 14:30
Branch: cc/20260420-1430/nielsen-auth-fix
Path:   .cc/worktrees/nielsen-auth-fix/
```

Slug rules:
- Lowercase, hyphens only
- 2–4 words max
- Mirrors topic prefix where possible (thesis, data, config, chore, feat, fix)

---

## Step 1.5 — Check: New branch or existing branch?

Before creating a worktree, determine if you're working on a **new** or **existing** branch:

**PowerShell:**
```powershell
git branch -a | Select-String "<branch-name>"
```

**Bash (in Claude CLI):**
```
! git branch -a | grep -E "<branch-name>"
```

**If branch does NOT exist (new work):**
- Proceed to Step 2 (standard new-worktree flow)

**If branch ALREADY exists (continuing work on existing branch):**
- Ask the user which option:
  - **[A] Create a NEW worktree on the SAME branch** (for parallel isolation)
    - PowerShell: `git worktree add worktrees\<slug> <existing-branch-name>` (omit `-b` flag)
    - Bash: `! git worktree add worktrees/<slug> <existing-branch-name>`
    - Launch a new Claude Code session in that worktree (see Step 4)
    - Useful: Multiple people working simultaneously, or splitting work across sessions
  - **[B] Reuse existing worktree on that branch**
    - PowerShell: `git worktree list`
    - Bash: `! git worktree list`
    - cd into it and continue work there
    - Simplest option if a worktree is already active
  - **[C] Create a fresh branch with new worktree** (new isolated work)
    - Proceed to Step 2 (standard flow, creates new branch name)

---

## Step 2 — Check for existing worktrees

**PowerShell:**
```powershell
git worktree list
```

**Bash (in Claude CLI):**
```
! git worktree list
```

If a worktree already covers this topic/branch, the decision in Step 1.5 handles whether to reuse it or create a parallel one. Do not silently create a duplicate without asking the user.

---

## Step 3 — Create the worktree

**PowerShell:**
```powershell
git worktree add worktrees\<slug> -b cc/<YYYYMMDD-HHMM>/<slug>
```

**Bash (in Claude CLI):**
```
! git worktree add worktrees/<slug> -b cc/<YYYYMMDD-HHMM>/<slug>
```

Then confirm:

**PowerShell:**
```powershell
git worktree list
git branch --show-current
```

**Bash (in Claude CLI):**
```
! git worktree list
! git branch --show-current
```

Output should show the new worktree and its branch.

---

## Step 4 — Open the worktree and launch Claude Code

### Within Claude Code (current session):

You are currently inside Claude Code. To transition to the new worktree:

**Option A — Exit Claude and launch new session:**

1. Exit Claude Code back to PowerShell:
   ```powershell
   exit
   ```
   You'll return to the PowerShell prompt in the main repo folder.

2. Change directory to the worktree:
   ```powershell
   cd worktrees\<slug>
   ```

3. Launch Claude Code in that directory:
   ```powershell
   claude
   ```

**Option B — Use bash within Claude CLI (stays in Claude):**

1. Change directory to worktree:
   ```
   ! cd worktrees/<slug>
   ```

2. Launch Claude from that directory:
   ```
   ! claude
   ```

---

### What happens after launch

A **new Claude Code session** starts in the isolated worktree. That session will:
- See only the worktree folder as its working directory
- Have its own git context (branch is already checked out)
- Have independent staging area and commit history from the main repo
- Have separate Claude conversation context

### Alternative: VS Code in worktree

If you prefer to use VS Code with Claude Code extension:

**PowerShell:**
```powershell
code worktrees\<slug>
```

**Bash:**
```
! code worktrees/<slug>
```

Then open Claude Code within that VS Code window for the same isolation benefits.

---

### Key point

**Launch Claude from *within* the worktree directory.** The isolation works best when Claude is started in the worktree folder. This ensures all file operations, git commands, and context stay within that isolated workspace.

---

## Step 5 — Report ready

```
Worktree ready at .cc/worktrees/<slug>/
Branch: cc/<YYYYMMDD-HHMM>/<slug>
Base: <SHA of HEAD at creation>

You're isolated from main and any other active sessions.
Work here, commit here, and open a draft PR when done.
```

---

## Ending a Session (cleanup)

Run from the **main repo folder** (not inside the worktree):

**PowerShell:**
```powershell
git worktree remove worktrees\<slug>
```

**Bash (in Claude CLI):**
```
! git worktree remove worktrees/<slug>
```

The folder is deleted. The branch and all commits survive in git history. Merge or open a PR before removing if you haven't already.

To list and prune stale worktrees:

**PowerShell:**
```powershell
git worktree list
git worktree prune
```

**Bash (in Claude CLI):**
```
! git worktree list
! git worktree prune
```

---

## Branch Mismatch Detection

Before committing, `/git-draft-commit` re-derives the session topic and checks the current branch using two-level matching:

| Level | Condition | Result |
|---|---|---|
| **Strict** | prefix matches AND ≥1 keyword in slug | Proceed silently |
| **Loose** | ≥1 keyword anywhere in branch name | Proceed, note loose match |
| **None** | Neither condition met | Flag mismatch, ask user to resolve |

If on `main` instead of a worktree branch, `/git-draft-commit` will warn and offer to create a worktree before proceeding.

---

## Quick Reference

| Situation | Action |
|---|---|
| Starting new session (new branch) | Create worktree (Steps 0–5), launch new Claude in that directory (Step 4) |
| Continuing work on existing branch | Use Step 1.5 to choose: reuse existing worktree [B], or create new parallel worktree [A] |
| Multiple worktrees on same branch | Both can be active; isolate each in separate Claude session (Step 1.5 [A]) |
| `.cc/` not gitignored | Add to `.gitignore` + commit first |
| Worktree already exists for topic | Use Step 1.5 decision tree |
| On `main` mid-session | See `/git-draft-commit` Step 0 — offer to create worktree |
| Session complete | Exit Claude, `git worktree remove .cc/worktrees/<slug>` from main repo folder |
| Stale worktrees accumulating | `git worktree prune` |

---

## Common Mistakes

**Skipping the gitignore check**
- Problem: Worktree folder tracked by git, pollutes status
- Fix: Always run `git check-ignore -q worktrees` before creating

**Creating worktree inside an existing worktree**
- Problem: Nested worktrees confuse git and Claude
- Fix: Always run `git worktree list` first; create from repo root

**Using bash heredoc syntax in commit commands (PowerShell)**
- Problem: `$(cat <<'EOF')` throws parser errors in PowerShell
- Fix: Use `!` syntax in Claude CLI instead, or use plain strings in PowerShell

**Two Claude sessions in the same folder**
- Problem: Shared staging area → cross-session commit pollution
- Fix: Each session gets its own worktree path (launch Claude FROM the worktree)

**Mixing root-level and .cc/ worktrees**
- Problem: Confusion about where worktrees live; some gitignored, some not
- Fix: All worktrees go in `worktrees/` at repo root level (already gitignored)

---

## Integration

**Pairs with:**
- `/git-draft-commit` — commit from within the worktree; trailers include worktree path
- `docs/reference/git-worktrees-and-parallel-sessions.md` — plain-language guide for Brian and Enrico
- `docs/reference/git-branch-strategy.md` — full branch naming rules
- `.claude/rules/trigger-branch-strategy.md` — auto-fires on session start if on `main`

**Called when:**
- Starting any session where isolation matters (new feature, chapter edit, data work)
- `/git-draft-commit` detects `main` and offers worktree setup as Option [1]
- The branch guard hook fires and user chooses to create a new branch
