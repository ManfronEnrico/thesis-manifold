# Plan Workflow

**Plan location**: Project-relative at `plans/{01-backlog_plans, 02-in_progress_plans, 03-focus_plans, 04-complete_plans, 05-blocked_plans, 06-paused_plans, 07-cancelled_plans, 08-archived_plans}/`. All plans use unique P-IDs for easy reference.

**Plan naming convention** (Finalized 2026-05-07):
```
P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/
  P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md
  YYYY-MM-DD_DOC-{description}.{ext}  (supporting docs)
```

**Format**:
- `P{NNNN}` — Unique sequential identifier (P0001, P0002, etc.)
- `YYYY-MM-DD_HHMM` — ISO date + time (24hr format, no separators). Use `0800` default for undated plans.
- `PLAN` — Literal keyword (always "PLAN" for plan folders)
- `{slug}` — Lowercase, hyphens (e.g., `jupyter-notebook-path-centralization`)

**Plan format**: Plans auto-include YAML frontmatter with status tracking:
```yaml
---
created: 2026-04-27 14:20:00
updated: 2026-05-07 15:30:00
status: Focus — Phase 2 In Progress
focus_detail: "What's currently being done and next steps"
---
# Plan Title
[content]
```

**Frontmatter fields (status-based)**:

| Status | Folder | Required Fields | Optional Fields |
|--------|--------|-----------------|-----------------|
| Backlog | `01-backlog_plans/` | `created`, `updated`, `status` | `priority`, `dependencies` |
| In Progress | `02-in_progress_plans/` | `created`, `updated`, `status` | `phase`, `next_steps`, `dependencies` |
| Focus | `03-focus_plans/` | `created`, `updated`, `status`, `focus_detail` | `phase`, `dependencies` |
| Complete | `04-complete_plans/` | `created`, `updated`, `status`, `completed` | `outcome_summary` |
| Blocked | `05-blocked_plans/` | `created`, `updated`, `status`, `blocked_reason` | `unblocks` |
| Paused | `06-paused_plans/` | `created`, `updated`, `status`, `paused_reason` | `dependencies`, `resume_when` |
| Cancelled | `07-cancelled_plans/` | `created`, `updated`, `status`, `cancellation_reason` | — |
| Archived | `08-archived_plans/` | `created`, `updated`, `status`, `archived_date` | `reason` |

**Rule: No outcome files**. Status is maintained in frontmatter only. When a plan completes:
1. Update `status: Complete` in frontmatter
2. Add `completed: YYYY-MM-DD HH:MM:SS` field
3. Add `outcome_summary:` field with brief ✅/🔄/❌ bullet summary
4. Move folder to `04-complete_plans/`
5. Keep all supporting docs in the same folder

**Status buckets** (organize plans by workflow):
- `01-backlog_plans/` — Not yet started
- `02-in_progress_plans/` — Active work (not highlighted as focus)
- `03-focus_plans/` — Top priority, actively worked on this session
- `04-complete_plans/` — Completed with outcomes
- `05-blocked_plans/` — Awaiting external decision/dependency
- `06-paused_plans/` — Intentionally paused, waiting for X
- `07-cancelled_plans/` — No longer needed
- `08-archived_plans/` — Old/legacy plans

**Index**: See `plans/PLANS_INDEX.md` for master reference of all plans by P-ID, date, and status.

---

## Key Changes (2026-05-07 Status Refactoring)

### Before: Outcome Files (2026-04-30 → 2026-05-07)
```
plans/
  02-in_progress_plans/
    P0017_2026-04-27_1420_PLAN-jupyter-notebook-path-centralization/
      P0017_2026-04-27_1420_PLAN-jupyter-notebook-path-centralization.md
  
  03-outcome_plans/  (duplicate status tracking)
    P0018_2026-04-28_1400_OUTCOME-restructure-existing-plans/
      P0018_2026-04-28_1400_OUTCOME-restructure-existing-plans.md
```

### After: Frontmatter Only (2026-05-07+)
```
plans/
  03-focus_plans/
    P0017_2026-04-27_1420_PLAN-jupyter-notebook-path-centralization/
      P0017_2026-04-27_1420_PLAN-jupyter-notebook-path-centralization.md  (frontmatter has status + phase)
  
  04-complete_plans/  (status in frontmatter, no separate outcome files)
    P0018_2026-04-28_1400_PLAN-restructure-existing-plans/
      P0018_2026-04-28_1400_PLAN-restructure-existing-plans.md  (frontmatter has completed + outcome_summary)
```

**Why this change?**
- Single source of truth: frontmatter has current status, no duplicates
- Frontmatter is scannable: quick status overview without loading full markdown
- Folder location + frontmatter status must agree (automation can validate)
- Less clutter: no parallel OUTCOME folders, all docs in one place

---

## How to Apply This Rule

### When Creating a New Plan
1. Check `plans/PLANS_INDEX.md` to find the next available P-ID
2. Create folder: `plans/02-in_progress_plans/P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/`
3. Create plan file: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md` inside
4. All supporting docs go in the same folder
5. Update `plans/PLANS_INDEX.md` to register the new P-ID

### When Documenting During Execution
1. Create docs inside the plan folder
2. Use naming: `YYYY-MM-DD_DOC-{description}.md`
3. Never put docs in project root

### When Moving a Plan Between Statuses
1. Move the **entire folder** (plan + all docs) to the new status
2. Example: `02-in_progress_plans/P0017_2026-04-27_1420_PLAN-x/` → `03-outcome_plans/P0017_2026-04-27_1420_PLAN-x/`
3. Update `plans/PLANS_INDEX.md` to reflect new status

### When Completing a Plan
1. Create outcome file at: `plans/03-outcome_plans/P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}/`
2. Outcome filename: `P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}.md`
3. Include metadata linking to original plan
4. Document ✅ Completed, 🔄 Adjusted, ❌ Dropped sections
5. Update `plans/PLANS_INDEX.md` to mark plan as "Completed"

---

## See Also

- `plans/PLANS_INDEX.md` — Master reference of all P-IDs, status, dates
- `.claude/rules/plan-documentation-structure.md` — Folder structure rules
- `CLAUDE.md` → Plans section — Overview of plan workflows
- Memory: `reference_plan_ids.md` — P-ID system reference
