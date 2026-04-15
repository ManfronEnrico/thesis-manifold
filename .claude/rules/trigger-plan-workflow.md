---
paths:
  - "**"
---

# Plan Workflow

**Automatic mirroring enabled** (via PostToolUse hook in `.claude/settings.json`)

## Steps
1. **Locate** ✅ *Automatic*: Global `~/.claude/plans/` → Project `.claude/plans/plan_files/`
2. **Relocate** ✅ *Automatic*: PostToolUse hook mirrors on every Write/Edit
3. **Rename** ✅ *Automatic*: Generates `YYYY-MM-DD_<slug>.md` from plan title (fallback: session name)
4. **Create outcome**: Manually write to `.claude/plans/outcome_files/YYYY-MM-DD_<short-slug>.md` after plan completes

## Plan File Format

Plans in `plan_files/` automatically include YAML frontmatter with timestamps:

```yaml
---
created: 2026-04-15 14:32:18
updated: 2026-04-15 15:45:22
---

# Plan Title

[plan content]
```

**Fields:**
- `created`: Set on first Write, never changes (shows when planning began)
- `updated`: Set on every Write/Edit (shows last modification time)

Both timestamps are YYYY-MM-DD HH:MM:SS for precise tracking.

## Outcome Format
```
# Outcome: <Plan Title>

_Plan: plan_files/YYYY-MM-DD_<short-slug>.md_
_Created: YYYY-MM-DD HH:MM:SS_
_Completed: YYYY-MM-DD HH:MM:SS_

### ✅ Completed
- <what was implemented>

### 🔄 Adjusted
- **What**: <change>
  **Why**: <reason>
  **How**: <what was done instead>

### ❌ Dropped
- **What**: <item not done>
  **Why**: <reason>
```
(Omit sections if empty)

## How Mirroring Works

The PostToolUse hook (`.claude/hooks/mirror_plan.py`) intercepts every Write/Edit targeting `~/.claude/plans/`:

1. **First Write** (plan creation): Extracts `# Heading` from content → kebab-case slug. Falls back to session filename if no heading yet. Injects HTML marker `<!-- mirror-plan-to: YYYY-MM-DD_<slug>.md -->`. Adds frontmatter with `created:` and `updated:` timestamps (YYYY-MM-DD HH:MM:SS).
2. **Subsequent Edits**: Reads existing marker from global file, preserves it, updates mirrored copy in `plan_files/`. Updates `updated:` timestamp; preserves `created:`.
3. **Stripping**: Marker is removed from the project copy (but retained in global file for determinism). Frontmatter timestamps remain in both global and mirrored files.
4. **Frontmatter schema**: Plans automatically include `created: YYYY-MM-DD HH:MM:SS` (first write only) and `updated: YYYY-MM-DD HH:MM:SS` (every write/edit).

This makes plan relocation **deterministic and zero-token-cost** — no manual `/update_plan` trigger needed for steps 1-3.

## Rules
- **When**: Create outcome after plan execution (manual step only)
- **Location**: `.claude/plans/plan_files/` (plan) and `.claude/plans/outcome_files/` (outcome)
- **Naming**: Both auto-generated during Write, locked by HTML marker after first Write
- **Timestamps**: Plans include `created:` (first write) and `updated:` (every edit) in frontmatter; outcomes should reference both with `_Created:` and `_Completed:` fields
- **No outcome file** = plan not completed (instant visual scan)
