---
paths:
  - "**"
---

# Docs Workflow

**Trigger**: `/update-all-docs` reviews session and updates relevant documents in order.

**Order**: 
1. Thesis sections (`thesis/writing/sections/`) — if bullet/outline changes
2. Compliance (`thesis/compliance/`) — if checks ran
3. CLAUDE.md — if structure/rules changed
4. CHEATSHEET.md — if commands/triggers changed
5. README.md — if setup/behavior changed
6. Plans (`plan_files/`) — if plan executed (append Outcome section)
7. Rules (`.claude/rules/`) — if references staled

**Output**: List what was updated and what was skipped (with reason).

See `.claude/skills/update-all-docs/SKILL.md` for implementation.
