# Plan System Restructuring — Complete (2026-05-07)

## Overview

Restructured plan system from **4 status buckets + outcome files** to **8 status buckets + frontmatter-based status**.

---

## Changes Made

### Folder Structure (01 → 08)

**Before** (2026-04-30):
```
01-backlog-plans/       (4 plans)
02-in_progress-plans/   (many plans, no distinction)
03-outcome_plans/       (duplicate outcomes, parallel folder)
04-archive_plans/       (old plans)
```

**After** (2026-05-07):
```
01-backlog_plans/       (4 plans: P0001-P0004)
02-in_progress_plans/   (0 plans, cleared)
03-focus_plans/         (3 plans: P0017, P0019, P0022)
04-complete_plans/      (5 plans: P0006-P0009, P0018)
05-blocked_plans/       (1 plan: P0005, awaiting decision)
06-paused_plans/        (1 plan: P0020, awaiting dependency)
07-cancelled_plans/     (0 plans, available for future)
08-archived_plans/      (7 plans: P0010-P0016)
```

### Plan Frontmatter (Status Tracking)

**Removed**: Separate OUTCOME files (P0017-OUTCOME, P0018-OUTCOME, etc.)  
**Added**: Status fields in plan frontmatter:

```yaml
---
created: YYYY-MM-DD HH:MM:SS
updated: YYYY-MM-DD HH:MM:SS
status: <Status String>
# Status-specific fields:
focus_detail: "..."        (for Focus plans)
blocked_reason: "..."      (for Blocked plans)
paused_reason: "..."       (for Paused plans)
dependencies: ["P00XX"]    (optional)
outcome_summary: "..."     (for Complete plans)
---
```

### Rules Updated

1. **trigger-plan-workflow.md** — Updated to reflect 8-bucket structure + frontmatter status
2. **plan-documentation-structure.md** — Updated status bucket descriptions + removed outcome-file guidance
3. **CLAUDE.md** — Updated plan references + correctness tier rule

### Index Updated

**plans/PLANS_INDEX.md** — Regenerated to show:
- All 8 status buckets with current plan counts
- Frontmatter-based status for each plan
- Quick reference by date and status

---

## Plans Affected

### Moved Plans

| Plan | From | To | Reason |
|------|------|----|----|
| P0017 | 02-in_progress | 03-focus | Active focus work (notebook paths) |
| P0019 | 02-in_progress | 03-focus | Active focus work (preprocessing unification) |
| P0022 | 02-in_progress | 03-focus | Active focus work (preprocessing modularization) |
| P0005 | 02-in_progress | 05-blocked | Awaiting Option A vs B decision |
| P0020 | 02-in_progress | 06-paused | Waiting for P0019 Phase 4 |
| P0018 | 02-in_progress | 04-complete | Completed, moved to outcomes |

### Removed Duplicate Files

- P0017-OUTCOME_2026-04-28_PLAN-jupyter_notebook_path_centralization/ ✓ Removed
- P0018_2026-04-28_1400_OUTCOME-restructure_existing_plans/ ✓ Removed
- P0020_2026-05-04_1430_OUTCOME-rule-system-reform/ ✓ Removed
- P0021_2026-05-04_1400_OUTCOME-docs-reorganization/ ✓ Removed

**Reason**: Status now tracked in plan frontmatter only (single source of truth).

---

## Benefits

1. **Single Source of Truth**: Status in frontmatter, no duplicate outcome files
2. **Faster Scanning**: Frontmatter readable without loading full markdown
3. **Clear Priority**: `03-focus_plans` explicitly shows current priorities
4. **Better Workflow**: Blocked/Paused statuses make dependencies visible
5. **Cleaner Archive**: `08-archived_plans` vs future statuses (07-cancelled available)

---

## Verification

```
01-backlog_plans:   4 plans ✓
02-in_progress_plans: 0 plans ✓
03-focus_plans:     3 plans (P0017, P0019, P0022) ✓
04-complete_plans:  5 plans (P0006-P0009, P0018) ✓
05-blocked_plans:   1 plan (P0005) ✓
06-paused_plans:    1 plan (P0020) ✓
07-cancelled_plans: 0 plans ✓
08-archived_plans:  7 plans (P0010-P0016) ✓

Total: 21 active plans tracked
(P0021 completed and merged into broader doc work — no separate folder)
```

---

**Completed**: 2026-05-07 15:45  
**Standardization**: All folders renamed with consistent `_plans` suffix (2026-05-07 16:00)  
**Next**: When plans move status, update frontmatter in place (no file moves needed unless changing buckets)
