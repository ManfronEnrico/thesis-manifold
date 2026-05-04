# Branch Strategy Rule

**Reference**: [docs/reference/GIT_BRANCH_STRATEGY.md](../../docs/reference/GIT_BRANCH_STRATEGY.md)

## Core principle

Every Claude Code session should work on a dedicated branch, not on `main`.
`main` is reserved for stable, reviewed, merged work — not active development.

## Layer A — Deterministic hook (primary)

A `UserPromptSubmit` hook fires on every opening message and runs
`.claude/hooks/branch_guard.py`. That script:

1. Reads the user's prompt text
2. Runs `git branch --show-current`
3. If on a **feature branch** → injects `✓ branch: <name>` and passes through
4. If on **`main`** → extracts topic keywords from the prompt, derives a
   suggested branch name using the naming convention below, and injects a
   structured interactive choice block that Claude must present to the user
   **before answering their question**

The hook is registered in `~/.claude/settings.json` (global, not in repo).

### Branch mismatch detection (used by `/draft-git-commit`)

At commit time, `/draft-git-commit` checks current branch against session topic:
- **Strict match** (prefix + keywords match) → Proceed
- **Loose match** (≥1 keyword anywhere) → Proceed, note mismatch
- **No match** → Flag, ask user to resolve

## Layer B — Rule fallback (backup)

If hook is absent, check manually: `git branch --show-current`
- **Feature branch** → proceed
- **`main`** → present interactive choice block before doing anything

## Interactive choice block (present verbatim when on `main`)

```
You're on `main`. Before we start, let's move to a branch.

Suggested: `<prefix>/<slug>`

  [1] Create and switch to `<prefix>/<slug>`  →  git checkout -b <prefix>/<slug>
  [2] Use a different name (type it)
  [3] Stay on `main` (only if you're merging completed work)

Which would you like?
```

After the user responds:
- **[1]** → run `git checkout -b <suggested>`, confirm success, then answer their question
- **[2]** → use the name they provide, run `git checkout -b <name>`, confirm, then answer
- **[3]** → ask "Are you sure? This is only recommended for merge/integration work." — if confirmed, note you're on `main` and proceed

## Branch naming convention

```
session/<topic>          # general chat / exploratory work
thesis/<chapter-topic>   # thesis content changes
data/<dataset-topic>     # data scripts or pipeline
config/<tool-topic>      # settings, tooling, integrations
chore/<cleanup-topic>    # refactoring, reorganization
```

## When committing on `main` IS allowed

- Explicitly integrating/merging completed branch work
- Changes reviewed and commit intentional
- Merge commit, not new feature work

## Committing on a feature branch

On a feature branch, `git add -A` is safe — branch is isolated by design.

## Merging back to `main`

Review before merging: `git diff main..<branch-name>` then `git merge <branch-name>`
