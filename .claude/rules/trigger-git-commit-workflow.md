---
paths:
  - "**"
---

# Git Commit Workflow

**Trigger**: `/draft_commit` generates a ready-to-paste commit message.

**Steps**:
1. Reconstruct session work from conversation context (what changed, why)
2. Run `git status` to verify files on disk
3. Read `project_updates/standup_draft.md` for uncommitted work (timestamp comparison)
4. Merge session context + standup into unified changes list
5. Draft message: `<type>: <subject>` + bullets + session timestamps

**Types**: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`
**Subject**: Imperative, ≤60 chars, no period

**Output**: Single code block, copy-paste ready. List which standup entries included.

See `.claude/skills/draft_commit.md` for skill implementation.
