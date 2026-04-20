# Branch Strategy Rule

**Reference**: [docs/reference/GIT_BRANCH_STRATEGY.md](../../docs/reference/GIT_BRANCH_STRATEGY.md)

## Core principle

Every Claude Code session should work on a dedicated branch, not on `main`.
`main` is reserved for stable, reviewed, merged work — not active development.

## Session start check (always)

At the start of any session where git work is expected, run:

```bash
git branch --show-current
```

- **If on a feature branch** → proceed normally. `git add -A` is safe.
- **If on `main`** → warn the user (see below). Do not commit without explicit confirmation.

## Warning message when on `main`

> You are currently on `main`. It is recommended to create a dedicated branch for this session's work.
> Suggested command:
> ```bash
> git checkout -b session/<short-topic>
> ```
> If you intend to merge or integrate branches into `main`, that is fine — confirm to proceed.

## When committing on `main` IS allowed

- User is explicitly integrating/merging completed branch work into `main`
- User has reviewed the changes and confirms the commit is intentional
- The commit is a merge commit, not new feature work

In these cases: ask "Are you sure you want to commit directly to `main`?" and proceed on confirmation.

## Branch naming convention

```
session/<topic>          # general chat session work
thesis/<chapter-topic>   # thesis content changes
data/<dataset-topic>     # data scripts or pipeline
config/<tool-topic>      # settings, tooling, integrations
chore/<cleanup-topic>    # refactoring, reorganization
```

## Committing on a feature branch

On a feature branch, `git add -A` is safe — the branch is isolated by design.
The draft-commit skill and all git workflows can proceed without restriction.

## Merging back to `main`

```bash
git checkout main
git merge <branch-name>     # or open a PR on GitHub
```

Before merging, review the diff:
```bash
git diff main..<branch-name>
```
