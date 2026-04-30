# Plan Workflow

**Plan location**: Project-relative at `plans/{01-backlog-plans, 02-in_progress-plans, 03-outcome_plans, 04-archive_plans}/`. All plans use unique P-IDs for easy reference.

**Plan naming convention** (NEW 2026-04-30):
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

**Plan format**: Plans auto-include YAML frontmatter:
```yaml
---
created: 2026-04-27 14:20:00
updated: 2026-04-30 10:15:00
status: In Progress
---
# Plan Title
[content]
```

**After execution**: Create outcome file in `03-outcome_plans/` with structure:
```yaml
---
created: YYYY-MM-DD HH:MM:SS
completed: YYYY-MM-DD HH:MM:SS
plan_reference: plans/02-in_progress-plans/P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md
---

# Outcome: <Title>

_Plan: P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}_  
_Status: COMPLETE (YYYY-MM-DD)_

## ✅ Completed
- [what was done]

## 🔄 Adjusted
- **What**: [change] **Why**: [reason] **How**: [done instead]

## ❌ Dropped
- **What**: [item] **Why**: [reason]
```

**Rule**: No outcome file = plan not completed (instant visual check).

**Status buckets** (organize plans by status):
- `01-backlog-plans/` — Not yet started
- `02-in_progress-plans/` — Currently being executed
- `03-outcome_plans/` — Completed with outcomes
- `04-archive_plans/` — Old/deprecated plans

**Index**: See `plans/PLANS_INDEX.md` for master reference of all plans by P-ID, date, and status.

---

## Key Changes (2026-04-30 Restructuring)

### Before
```
plans/
  01-backlog-plans/
    2026-04-13_cmt-master-upgrade-plan.md        (flat, no P-ID)
    2026-04-13_notebooklm-integration-plan.md    (flat, no P-ID)
```

### After
```
plans/
  01-backlog-plans/
    P0001_2026-04-13_0800_PLAN-cmt-master-upgrade-plan/
      P0001_2026-04-13_0800_PLAN-cmt-master-upgrade-plan.md
    P0002_2026-04-13_0800_PLAN-notebooklm-integration-plan/
      P0002_2026-04-13_0800_PLAN-notebooklm-integration-plan.md
```

**Why P-IDs?**
- Quick reference: "P0017" vs. "jupyter notebook path centralization"
- Sequential allocation for future plans (P0019, P0020, etc.)
- Chronological + ID sorting capability
- Persistent knowledge across sessions (stored in memory system)

---

## How to Apply This Rule

### When Creating a New Plan
1. Check `plans/PLANS_INDEX.md` to find the next available P-ID
2. Create folder: `plans/02-in_progress-plans/P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/`
3. Create plan file: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md` inside
4. All supporting docs go in the same folder
5. Update `plans/PLANS_INDEX.md` to register the new P-ID

### When Documenting During Execution
1. Create docs inside the plan folder
2. Use naming: `YYYY-MM-DD_DOC-{description}.md`
3. Never put docs in project root

### When Moving a Plan Between Statuses
1. Move the **entire folder** (plan + all docs) to the new status
2. Example: `02-in_progress-plans/P0017_2026-04-27_1420_PLAN-x/` → `03-outcome_plans/P0017_2026-04-27_1420_PLAN-x/`
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
