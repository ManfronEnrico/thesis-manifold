---
name: draft_commit
description: Generate a ready-to-paste git commit message from the current session. Trigger this skill whenever the user mentions committing changes, preparing a git message, or wants to submit work. Use it after significant coding sessions, refactors, feature work, or bug fixes. The skill reconstructs what was done in the session, checks git status, reads any standup notes, and outputs a conventional commit message the user can immediately copy and paste. Output is formatted as genuine human work — no bot or agent attribution.
compatibility:
  tools: [Bash, Read, Grep]
  requires: git repository
---

# Draft Commit Message

Generate a ready-to-paste git commit message from session work and git state.

## When to use this skill

Invoke this skill when:
- The user says "commit", "git commit", "prepare commit", "what should my commit message be?"
- The user has finished a task and is ready to stage and push
- The session has accumulated changes and the user wants to bundle them
- The user asks "should I commit this?" or "make a commit"

The skill never auto-executes — you copy the message from the code block and submit it yourself.

## How it works

This skill reconstructs what was done in the session using this algorithm:

1. **Reconstruct session context** — Review the conversation to understand what was changed and why
2. **Get current git state** — Run `git status` to see modified, staged, and untracked files
3. **Find the cutoff** — Determine the last commit timestamp to identify what's uncommitted
4. **Read standup notes** — Extract entries from `project_updates/standup_draft.md` timestamped after the last commit
5. **Merge context** — Combine session work + standup entries into a unified changes list
6. **Format message** — Create a conventional commit with type (feat/fix/refactor/chore/docs/test), subject, bullet points, and optional body text that reads naturally as human work

## Output format

The skill outputs a single fenced code block with a ready-to-paste commit message. **Commits are formatted as genuine human work with no "Co-Authored-By" or agent attribution lines.** Just the substance:

```
<type>: <subject>

- <bullet describing change>
- <bullet describing change>
```

Followed by a brief explanation of which standup entries were included and any ambiguities.

## Example

**Input:** User says "let me prepare a commit for this work"

**Output:**
```
feat: add APA citation skill and improve trigger descriptions

- Integrated apa-citation skill into thesis workflow
- Optimized trigger descriptions for better skill discovery
- Updated CLAUDE.md with citation workflow section
```

## You control submission

Copy the message and run in your terminal:

```bash
git commit -m "feat: your message here"
```

This skill never runs `git commit` itself — you maintain full control over what gets committed and when.

## Integration with project workflow

This skill implements the deduction algorithm from `.claude/rules/trigger-git-commit-workflow.md` and is designed to work with the CMT thesis project's standup system. If you have uncommitted work from multiple sessions, it merges them intelligently based on timestamps.

**Important**: Generated commit messages are formatted as your own work. No attribution, no bot markers, no "Co-Authored-By" lines. The message reflects your authentic development session.
