---
name: draft_commit
description: Generate a ready-to-paste git commit message following the project's trigger-git-commit-workflow
---

# Draft Commit Message

Generate a ready-to-paste git commit message for manual submission. Never auto-executes — you copy and submit it yourself.

## Usage

```
/draft_commit
```

## How It Works

This skill implements the deduction algorithm from `.claude/rules/trigger-git-commit-workflow.md`:

1. **Reconstruct current session work** — Review everything done in this session from conversation context
2. **Get git status** — List modified, staged, and untracked files
3. **Get last commit timestamp** — Find the cutoff for uncommitted work
4. **Read standup_draft.md** — Extract entries timestamped after the last commit
5. **Cross-reference** — Merge session context + standup entries into a unified list
6. **Draft the message** — Format as conventional commit with bullets and session timestamps

## Output

A single fenced code block containing a ready-to-paste commit message:

```
<type>: <subject>

- <bullet>
- <bullet>

Sessions: HH-MM-SS, HH-MM-SS
```

Then a brief note explaining which entries were included and any ambiguities.

## You Control Submission

Copy the message from the code block and paste it into your terminal:

```bash
git commit -m "chore: your message here"
```

This skill never calls `git commit` — you do.
