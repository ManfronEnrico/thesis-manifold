# Worktree Workflow

**Purpose**: Standardize how Claude Code sessions use git worktrees for isolation and parallel work.

**Location**: Worktrees live at `worktrees/` directory (root level of repo), already gitignored.

---

## Quick Reference

| Need | Action |
|------|--------|
| New isolated session | Create worktree with `/git-using-worktrees` skill |
| Parallel work on same branch | Use Step 1.5 [A] in skill — create new worktree on existing branch |
| Reuse existing worktree | Use Step 1.5 [B] — cd into existing worktree, launch new Claude session |
| Clean up after work | `git worktree remove worktrees/<slug>` from main repo folder |

---

## Session → Worktree → Claude Mapping

**One Claude session = One worktree (isolation)**

```
Main repo folder
  └─ worktrees/
       ├─ folder-cleanup/           ← Claude Session A (chore/folder-cleanup branch)
       ├─ chapter-2-writing/        ← Claude Session B (thesis/chapter-2 branch)
       └─ data-pipeline-fix/        ← Claude Session C (data/pipeline-fix branch)
```

Each Claude session runs in its own worktree folder with its own git state.

---

## Dual Instruction Format

**All instructions in the skill provide BOTH options:**

### Option 1: PowerShell (exit Claude, use native shell)
```powershell
exit
cd worktrees\<slug>
claude
```

### Option 2: Bash with `!` prefix (stay in Claude CLI)
```
! cd worktrees/<slug>
! claude
```

Choose whichever feels natural. Option 2 keeps you in Claude; Option 1 switches to native shell.

---

## When to Use Worktrees

**Always use worktrees when:**
- Starting a new Claude session for non-trivial work (features, chapters, refactors)
- Making changes that should be isolated from the main folder
- Working with Enrico in parallel (separate worktrees per person, same branch OK)

**OK to skip worktrees:**
- Quick single-file edits in the main folder
- Read-only exploration or research
- First-time setup/learning

---

## Conventions

| Convention | Value |
|---|---|
| Root directory | `worktrees/` at repo root |
| Folder name | `<slug>` (lowercase, hyphens) — e.g., `folder-cleanup`, `chapter-2-writing` |
| Branch name | `cc/<YYYYMMDD-HHMM>/<slug>` (new) OR existing branch (parallel) |
| Gitignore | `worktrees/` already in `.gitignore` — no action needed |

---

## How to Apply

### Starting a new session
```
/git-using-worktrees
```
Skill walks through steps and provides both PowerShell and bash instructions.

### Cleaning up after session
Run from main repo folder (not inside worktree):

**PowerShell:**
```powershell
git worktree remove worktrees\<slug>
```

**Bash:**
```
! git worktree remove worktrees/<slug>
```

---

## See Also

- `.claude/skills/git-using-worktrees/SKILL.md` — Full skill with all steps
- `docs/reference/git-worktrees-and-parallel-sessions.md` — Plain-language guide for Brian and Enrico
- `.claude/rules/trigger-branch-strategy.md` — Branch naming and when to create branches
