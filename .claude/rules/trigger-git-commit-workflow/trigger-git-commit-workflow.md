---
paths:
  - "**"
---

# Git Commit Workflow

**Trigger**: `/git-draft-commit` — generates ready-to-paste commit message
**Execution**: `/git-commit` — stages files and runs the commit from an approved message

**Pre-step**: Automatically invoke `/errors-log` to capture any session tooling issues before drafting.

## Algorithm
0. **Branch check**: Run `git branch --show-current` — if on `main`, warn the user and suggest creating a branch (see `.claude/rules/trigger-branch-strategy.md`). Ask for explicit confirmation before proceeding. If on a feature branch, proceed freely.
1. **Log errors**: Run `/log_errors` to scan conversation and append any tooling issues to `docs/tooling-issues.md`
2. **Session context** (PRIMARY): What files changed & why (from conversation)
3. **Git status**: `git status --short` — confirm changed files on disk
4. **Last commit**: `git log -1 --format="%H %ai %s"` — cutoff for uncommitted work
5. **Standup entries**: Extract `HH-MM-SS` entries from `project_updates/standup_draft.md` dated after last commit
6. **Cross-reference**: Merge context + standup → unified list of changes
7. **Draft**: Format as `<type>: <subject> ≤60 chars` + bullets + `Sessions: HH-MM-SS`

## Format
```
<type>: <imperative subject, ≤60 chars>

- <what changed and why, one line per logical unit>
- <...>

Sessions: HH-MM-SS (timestamps of included standup entries)
```

**Types**: `feat` (new feature), `fix` (bug), `refactor` (structure), `chore`/`docs` (non-code)

## Selective Staging (Default — Always)

**Never use `git add -A` or `git add .`** — these sweep in untracked files from other sessions.

**Always stage by explicit path**:
```bash
git add path/to/file1 path/to/file2 path/to/folder/
```

**How to identify this session's files**:
1. Cross-reference `git status --short` against the conversation (what did we actually touch?)
2. Untracked files (`??`) not mentioned in the conversation → **exclude**
3. When in doubt, list the files in the commit message draft and ask Brian to confirm before staging

**Rollback if wrong**: `git reset HEAD~1 --mixed` undoes the last commit, keeps files on disk.

## Output
Present in single code block (copy-paste ready). Add note if:
- Standup entries were ambiguous
- Files in `git status` have no session record
- `??-??-??` placeholders are unresolved
