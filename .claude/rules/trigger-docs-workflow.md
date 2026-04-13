---
paths:
  - "**"
---

# Docs Workflow

> Auto-loaded every session. Governs how Claude performs a full documentation update across all living project documents.

## Trigger

Invoke the `/update_all_docs` skill to review the current session and update all relevant documents.

```
/update_all_docs
```

Do **not** wait to be asked twice. Work through each document in order, skipping only if the session produced nothing relevant to that document.

---

## Document Update Order

Work through these in sequence. Each has its own update criteria.

### 1. `project_updates/standup_draft.md`
Follow the full standup-workflow rule (trigger = "update standup" fires automatically).
**Update if**: any writing, code, tooling, or workflow changes were made this session.

### 2. Thesis Section Files — `docs/thesis/sections/`
**Update if**: bullet points were expanded, new content was added, or outlines were revised this session.
**Do not** add ephemeral notes — only durable content changes.

### 3. Compliance — `docs/compliance/`
**Update if**: CBS compliance checks ran, integrity gate results were documented, or new compliance notes were added.

### 4. `CLAUDE.md`
Project-level instructions for Claude.
**Update if**: a new module or major function was added, project structure changed, a new rule file was added to `.claude/rules/`, a frozen decision was made, or a standing convention was established/changed.
**Do not** add ephemeral session notes — only durable structural facts.

### 5. `CHEATSHEET.md`
Quick-reference for commands, trigger phrases, and workflow recipes.
**Update if**: a new CLI flag was added/removed, a new trigger phrase was introduced, a workflow recipe changed, or a new Make command was documented.

### 6. `README.md`
User-facing project documentation.
**Update if**: setup steps changed, major architecture changed, or the described behavior no longer matches reality.

### 7. `README_builder.md`
Builder agent documentation.
**Update if**: builder agent behavior, usage, or architecture changed.

### 8. Plan files — `.claude/plans/`
Follow the full plan-workflow rule (Outcome section format: ✅ Completed / 🔄 Adjusted / ❌ Dropped), **including the Relocate & Rename step**: if the plan is in the global `~/.claude/plans/` folder or has a non-conforming name, move and rename it to `<project-root>/.claude/plans/YYYY-MM-DD_<short-slug>.md` before appending the Outcome section.
**Update if**: a plan was actively discussed, executed, or partially implemented this session and does not yet have an `## Outcome` section.

### 9. Other `.claude/rules/` files
Review each rule file for stale references.
**Update if**: a trigger phrase, file path, format, or pattern documented in a rule file was changed this session.

---

## Completion Signal

After finishing all updates, briefly list what was updated and what was skipped (with reason), e.g.:

> **Docs updated:** standup_draft ✅, sections (skipped — no writing changes), compliance (skipped — no checks run), CLAUDE.md ✅, CHEATSHEET ✅, README (skipped — no user-facing changes), README_builder (skipped), plans: `2026-04-13_cmt-claude-infrastructure.md` ✅ (moved from global), rules (skipped — no stale refs)

---

## Skill Reference

See `.claude/skills/update_all_docs.md` for the skill implementation.
