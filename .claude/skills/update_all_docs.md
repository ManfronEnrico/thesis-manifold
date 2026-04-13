---
name: update_all_docs
description: Update all living project documentation based on current session changes
---

# Update All Docs

Review the current session and update all relevant project documents in sequence.

## Usage

```
/update_all_docs
```

## How It Works

This skill implements the full documentation update workflow from `.claude/rules/trigger-docs-workflow.md`. It works through these documents in order, updating only those affected by this session's work:

### 1. `project_updates/standup_draft.md`
Update if any writing, code, tooling, or workflow changes were made this session.

### 2. Thesis sections — `docs/thesis/sections/`
Update if bullet points were expanded, new content was added, or outlines were revised this session.

### 3. Compliance — `docs/compliance/`
Update if CBS compliance checks ran, integrity gate results were documented, or new compliance notes were added.

### 4. `CLAUDE.md`
Update if a new module/function was added, project structure changed, new rule file was added, a frozen decision was made, or conventions changed.

### 5. `CHEATSHEET.md`
Update if CLI flags, trigger phrases, Make commands, or workflow recipes changed.

### 6. `README.md`
Update if setup steps, major architecture, or described behavior changed.

### 7. `README_builder.md`
Update if builder agent behavior, usage, or architecture changed.

### 8. Plan files — `.claude/plans/`
If a plan was actively discussed, executed, or partially implemented, append an `## Outcome` section.
Also moves and renames misplaced plans to `YYYY-MM-DD_<short-slug>.md` format.

### 9. Other `.claude/rules/` files
Review for stale references — update if any trigger phrases, file paths, formats, or patterns were changed.

## Output

After finishing all updates, a brief summary:

```
**Docs updated:** standup_draft ✅, sections (skipped — no writing changes), compliance (skipped — no checks run), CLAUDE.md ✅, CHEATSHEET ✅, README (skipped — no user-facing changes), README_builder (skipped), plans: `2026-04-13_cmt-claude-infrastructure.md` ✅ (moved from global), rules (skipped — no stale refs)
```
