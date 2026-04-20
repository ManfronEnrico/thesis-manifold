# Git Branch Strategy — Multi-Chat Claude Code Workflow

## Core idea

Each Claude Code chat session works on its own isolated branch.
Nothing a chat does touches `main` until you explicitly decide to merge it.

```
main
 ├── session/config-fix          ← Chat A
 ├── thesis/ch3-methodology      ← Chat B
 └── data/nielsen-preprocessing  ← Chat C
          ↓ reviewed and merged into main separately
```

---

## Git concepts (plain language)

| Term | What it means |
|------|--------------|
| **Repository** | The tracked project folder (`CMT_Codebase`) |
| **Branch** | A parallel version of the repo — changes here don't affect other branches |
| **`main`** | The primary branch — stable, confirmed work lives here |
| **`git checkout -b name`** | Create a new branch and switch into it |
| **Commit** | A saved snapshot on the current branch |
| **Merge** | Bring commits from one branch into another |
| **Pull Request (PR)** | GitHub UI checkpoint to review a branch before merging to main |
| **`git stash`** | Temporarily shelve uncommitted changes so you can switch branches |
| **Staging area** | The holding area between editing and committing — `git add` moves files here |

---

## Session startup — run this at the start of every new chat

```bash
git checkout main
git pull                          # sync if you push to remote
git checkout -b session/<topic>   # isolated branch for this chat
```

### Naming conventions

```bash
git checkout -b session/settings-permissions
git checkout -b thesis/ch3-methodology-bullets
git checkout -b data/nielsen-cache-fix
git checkout -b config/notebooklm-integration
git checkout -b chore/skills-reorganization
```

---

## Committing during a session

Because the branch is isolated, you can safely add everything the chat touched:

```bash
git add -A                        # safe — branch is isolated by nature
git commit -m "fix: descriptive message"
```

Or add specific files if you want a tighter commit:

```bash
git add .claude/settings.json
git commit -m "chore: fix git permissions"
```

Multiple small commits per session is fine.

---

## End-of-session decision: what goes to main?

| Change type | Rule |
|-------------|------|
| Config / tooling / settings | Merge immediately — low risk |
| Thesis content (bullets, sections) | Review diff first, then merge |
| Data scripts | Verify no broken imports, then merge |
| Unfinished work | Leave branch open, continue next session |

### To review before merging

```bash
git diff main..session/settings-permissions   # see what changed
```

### To merge when ready

```bash
git checkout main
git merge session/settings-permissions
```

---

## Why this matters for concurrent Claude Code chats

**The problem without branches:** all chats share one staging area on `main`.
If chat-A runs `git add -A` and doesn't commit, then chat-B commits, it picks up chat-A's staged files too — exactly what happened with the 300-file commit.

**With branches:** each chat's staging area is scoped to its own branch.
`git add -A` on `session/config-fix` cannot bleed into `thesis/ch3-methodology`.

---

## Claude Code + VS Code multi-terminal setup

When running multiple Claude Code agents in parallel VS Code PowerShell terminals:

1. **Each terminal = one branch.** Before starting work in a terminal, run the session startup command above.
2. **Each agent commits to its own branch.** The `/draft-commit` skill and `git add -A` are safe because the branch is isolated.
3. **Merge to main asynchronously.** After a session ends, switch to main and merge. No need to coordinate between live terminals.
4. **Check your current branch any time:**
   ```bash
   git branch        # lists all branches, * marks current
   git status        # also shows current branch at top
   ```

### Recommended terminal workflow

```
Terminal 1 (Chat A) → branch: thesis/ch3-methodology
Terminal 2 (Chat B) → branch: config/zotero-integration  
Terminal 3 (Chat C) → branch: data/nielsen-preprocessing

Each terminal commits freely.
You merge to main when each task is done.
```

---

## Quick reference card

```bash
# Start session
git checkout main && git checkout -b session/<topic>

# Commit everything on current branch (safe — isolated)
git add -A && git commit -m "<type>: <message>"

# See what branch you're on
git branch

# See diff vs main before merging
git diff main..<branch-name>

# Merge to main
git checkout main && git merge <branch-name>

# List all branches
git branch -a
```

---

## Commit message types

| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug or error fix |
| `refactor` | Restructuring without behavior change |
| `chore` | Config, tooling, settings |
| `docs` | Documentation only |
| `thesis` | Thesis content changes |
| `data` | Data scripts or pipeline changes |
