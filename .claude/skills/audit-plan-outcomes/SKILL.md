# /audit-plan-outcomes

Verify that completed plans have proper outcome files with complete documentation.

## Purpose

Enforce the Correctness Tier rule: **Plan status is tracked in frontmatter only** (no separate outcome files as of 2026-05-07).

This skill detects:
- Plans with missing or malformed frontmatter status fields
- Folder location that doesn't match frontmatter status (e.g., plan in 04-complete_plans but status: "In Progress")
- Completed plans missing `completed` timestamp or `outcome_summary`
- Blocked/Paused plans missing `blocked_reason` / `paused_reason`
- Inconsistencies between PLANS_INDEX and actual plan frontmatter

## Invocation

```
/audit-plan-outcomes
/audit-plan-outcomes <plan-id>         # Audit single plan (e.g., P0020)
/audit-plan-outcomes --strict          # Fail on any missing section or incomplete docs
/audit-plan-outcomes --report          # Generate full audit report (HTML/Markdown)
```

## How It Works

### Step 1: Scan All Plans

Reads all 8 status folders: `01-backlog_plans/`, `02-in_progress_plans/`, `03-focus_plans/`, `04-complete_plans/`, `05-blocked_plans/`, `06-paused_plans/`, `07-cancelled_plans/`, `08-archived_plans/`.

For each plan, extract:
- P-ID, folder location, main plan file
- Read frontmatter to get `status` field

### Step 2: Validate Frontmatter

For **each plan**, verify:
- Frontmatter exists and is valid YAML
- `status` field is present and valid (Backlog, In Progress, Focus, Complete, Blocked, Paused, Cancelled, Archived)
- Folder location matches status type:
  - Status "Focus" → must be in `03-focus_plans/`
  - Status "Complete" → must be in `04-complete_plans/`
  - Status "Blocked" → must be in `05-blocked_plans/`, etc.

### Step 3: Validate Status-Specific Fields

For **each plan by status**, check:

**Complete plans** must have:
```yaml
---
created: YYYY-MM-DD HH:MM:SS
updated: YYYY-MM-DD HH:MM:SS
status: Complete
completed: YYYY-MM-DD HH:MM:SS
plan_reference: plans/04-complete_plans/P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/P{NNNN}_...md
---
```

All three fields required; dates must be valid ISO.

**Content structure:**
```markdown
# Outcome: <Title>

## ✅ Completed
- [at least one item required]

## 🔄 Adjusted
- [optional, but if present must have What/Why/How]

## ❌ Dropped
- [optional, but if present must have What/Why]
```

**Validation rules:**
- Completed section: required, non-empty
- Adjusted section: if present, all items must have **What:**, **Why:**, **How:** format
- Dropped section: if present, all items must have **What:**, **Why:** format
- All sections use consistent bullet point format
- Title in header matches plan topic (rough check)

### Step 4: Cross-Reference PLANS_INDEX.md

For **each outcome listed in PLANS_INDEX.md** as "Completed":
- Verify outcome file exists
- Verify folder exists in `03-outcome_plans/`
- Verify frontmatter is valid

### Step 5: Report

Return audit results:

```
✅ VALID OUTCOMES (6 plans):
- P0006: Complete (Completed 2026-04-15)
- P0007: Complete (Completed 2026-04-15)
- P0008: Complete (Completed 2026-04-18)
- P0009: Complete (Completed 2026-04-22)
- P0017-OUTCOME: Complete (Completed 2026-04-28)
- P0021: Complete (Completed 2026-05-04)

⏳ IN-PROGRESS PLANS (5 plans, no outcome expected yet):
- P0005: System A Feature Eng (started 2026-04-23)
- P0017: Jupyter Notebook Path (started 2026-04-27)
- P0018: Restructure Plans (started 2026-04-28)
- P0019: Preprocessing Pipeline (started 2026-05-04)
- P0020: Rule System Reform (started 2026-05-04, currently in Phase 4)

⚠️  WARNINGS (0):
None

❌ ERRORS (0):
None

AUDIT COMPLETE: All outcomes valid, all in-progress plans tracked.
```

### Example Error Report

If violations exist:

```
❌ ERRORS FOUND (3):

1. Missing outcome file for completed plan:
   Plan: P0019 (Preprocessing Pipeline Unification)
   Status in PLANS_INDEX: Completed
   Expected file: plans/03-outcome_plans/P0019_2026-05-04_1400_OUTCOME-preprocessing-pipeline-unification/
   Actual: FILE NOT FOUND
   Action: Create outcome file OR update PLANS_INDEX to mark as "In Progress"

2. Incomplete outcome file (missing Completed section):
   File: plans/03-outcome_plans/P0006_2026-04-15_0800_OUTCOME-integration-phase1-execution/P0006_...md
   Missing: ## ✅ Completed section
   Action: Add completed items to outcome file

3. Invalid frontmatter:
   File: plans/03-outcome_plans/P0007_2026-04-15_0800_OUTCOME-restructuring-audit/P0007_...md
   Missing field: completed
   Action: Add "completed: YYYY-MM-DD HH:MM:SS" to frontmatter

Fix these before proceeding. Run `/audit-plan-outcomes --strict` to fail on warnings.
```

## Integration with P0020

This skill enforces the **Correctness Tier** rule from `.claude/rules/rule-priority-hierarchy.md`:

> **Plan outcome discipline**: A plan is not considered complete until its outcome file exists in `03-outcome_plans/`. Why: Prevents dangling in-progress plans; outcome files = audit trail of completed work. When: Every plan execution must produce an outcome file (Completed, Adjusted, Dropped sections).

**Related:** `/validate-plan-ids`, `/audit-cross-references`, `/sync-memory-indices`, `/enforce-repo-cleanliness`

## Example Scenarios

### Scenario 1: Audit All Plans

User: `/audit-plan-outcomes`

Output: (see Step 5 above — all valid case)

### Scenario 2: Audit Single Plan

User: `/audit-plan-outcomes P0020`

Output:
```
Auditing P0020 (Rule System Reform)...

Status: IN-PROGRESS (started 2026-05-04 14:30)
Folder: plans/06-paused_plans/P0020_2026-05-04_1430_PLAN-rule-system-reform/

Expected outcome file: 
  plans/03-outcome_plans/P0020_2026-05-04_1430_OUTCOME-rule-system-reform/
  (not yet created, plan still in Phase 4)

✓ No outcome file expected yet (plan in progress)

Next action: When Phase 8 completes, create outcome file with:
- ## ✅ Completed sections for Phases 1-8
- ## 🔄 Adjusted sections for any mid-execution changes
- ## ❌ Dropped sections for deferred tasks
```

### Scenario 3: Strict Audit (Fail on Any Warning)

User: `/audit-plan-outcomes --strict`

Output:
```
Running strict audit...

❌ STRICT AUDIT FAILED (1 issue):
- P0005: Plan marked "DRAFT" in PLANS_INDEX (should be "In Progress" or moved to backlog)

Under strict mode, all status ambiguities are errors. Fix and re-run.
```

### Scenario 4: Generate Full Report

User: `/audit-plan-outcomes --report`

Output:
```
Generating comprehensive audit report...

📋 PLANS OUTCOME AUDIT REPORT
Generated: 2026-05-04 15:00:00
Checked: 11 plans (5 in-progress, 6 outcomes)

[HTML report saved to docs/reference/plan-outcomes-audit-2026-05-04.html]
[Markdown report saved to docs/reference/plan-outcomes-audit-2026-05-04.md]

Report includes:
- Outcome file completeness checklist
- Frontmatter validation details
- Missing/invalid section detection
- PLANS_INDEX cross-reference
- Recommendations for fixes
```

## Implementation Notes

- Uses Glob to scan all 8 status folders (`01-backlog_plans/` through `08-archived_plans/`)
- Regex to parse outcome filenames: `P(\d{4})_(\d{4}-\d{2}-\d{2})_(\d{4})_OUTCOME-(.+)`
- Reads outcome files to check frontmatter (YAML parsing)
- Checks for required sections (✅, optionally 🔄 and ❌)
- Validates section format (bullet points with What/Why/How for adjusted, What/Why for dropped)
- Cross-references PLANS_INDEX.md for status discrepancies
- Does not modify files (report-only skill unless explicitly requested for fixes)
- Reports all violations in single audit pass

## Data Integrity

This skill is read-only and does not modify files. It produces:
- Console report (immediate)
- Optional markdown/HTML audit report (saved to `docs/reference/`)

No file modifications without explicit user confirmation.

---

**Reference**: `.claude/rules/rule-priority-hierarchy.md`, `.claude/rules/plan-documentation-structure.md`, `memory/convention_project_standards.md`

**Related Skills**: `/validate-plan-ids`, `/enforce-repo-cleanliness`

