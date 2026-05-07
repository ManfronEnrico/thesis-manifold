# /validate-plan-ids

Validate that all plan folders and files follow the P-ID naming convention.

## Purpose

Enforce compliance with the P-ID naming system: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}`.

## Invocation

```
/validate-plan-ids
/validate-plan-ids <status-bucket>     # Validate single bucket (01-backlog-plans, 02-in_progress-plans, etc.)
/validate-plan-ids --fix               # Auto-fix violations where safe
```

## How It Works

### Step 1: Scan Directory

Scans `plans/` and each status bucket:
- `01-backlog-plans/`
- `02-in_progress-plans/`
- `03-outcome_plans/`
- `04-archive_plans/`

### Step 2: Validate Each Item

For **plan folders**, check:
- Folder name matches: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}` OR `P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}`
- P-ID is unique (no duplicates)
- YYYY-MM-DD is valid ISO date
- HHMM is valid 24hr time (0000–2359)
- slug is lowercase, hyphens only (no spaces, underscores, etc.)

For **plan files** inside folders, check:
- Main plan file: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md` OR `P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}.md`
- Supporting docs: `YYYY-MM-DD_DOC-{description}.md` or `YYYY-MM-DD_DOC-{description}.{ext}`
- All dates are ISO format
- All filenames are valid

For **PLANS_INDEX.md**, check:
- All in-progress and backlog P-IDs listed
- Dates match folder names
- No orphaned IDs (folders with no index entry)

### Step 3: Report Violations

Return a summary:

```
✅ VALID:
- P0001_2026-04-13_0800_PLAN-cmt-master-upgrade (folder + file match)
- P0020_2026-05-04_1430_PLAN-rule-system-reform (folder + file match)

⚠️  WARNINGS:
- P0005 in PLANS_INDEX but marked "DRAFT" — should be either "In Progress" or moved to backlog

❌ ERRORS:
- /plans/02-in_progress-plans/P0020_rule-system-reform/ (folder name does not include date/time)
- /plans/03-outcome_plans/P0017_OUTCOME_.../ (folder uses "OUTCOME_" instead of underscore pattern)
- /plans/02-in_progress-plans/P0020_2026-05-04_1430_PLAN-rule-system-reform/old-plan-v1.md (file does not follow naming convention)

DUPLICATE P-IDs:
- None found ✓

ORPHANED FOLDERS:
- None found ✓

ORPHANED INDEX ENTRIES:
- None found ✓
```

### Step 4: Suggest Fixes (with --fix flag)

If `--fix` is specified, offer to:
1. Rename folders to correct format
2. Rename files to correct format
3. Create/update PLANS_INDEX.md entries
4. Remove old/malformed files (with confirmation)

Example output with --fix:

```
Renaming 1 folder:
  /plans/02-in_progress-plans/P0020_rule-system-reform/
  → /plans/02-in_progress-plans/P0020_2026-05-04_1430_PLAN-rule-system-reform/

Renaming 2 files:
  /plans/03-outcome_plans/P0017_OUTCOME_.../ → P0017_2026-04-28_XXXX_OUTCOME-...
  
Confirming PLANS_INDEX.md entries...
  All entries valid ✓

Ready to apply? [Y/n]
```

## Rules Enforced

- **P-ID Format**: `P{NNNN}` where NNNN is 4 digits (P0001, P0020, etc.)
- **Date Format**: ISO 8601 (`YYYY-MM-DD`)
- **Time Format**: 24-hour (`HHMM`, 0800 default)
- **Keywords**: `PLAN` or `OUTCOME` (case-sensitive)
- **Slug Format**: Lowercase, hyphens, no spaces or underscores
- **File Naming**: Main plan file must match folder name; supporting docs use `YYYY-MM-DD_DOC-{description}.{ext}`
- **Index Authority**: PLANS_INDEX.md is authoritative for which plans exist; folders without index entries are flagged

## Integration with P0020

This skill enforces the P-ID naming convention defined in `.claude/rules/plan-documentation-structure.md` and consolidated in `memory/convention_project_standards.md`.

**Related:** `/audit-plan-outcomes`, `/audit-cross-references`, `/sync-memory-indices`, `/enforce-repo-cleanliness`

## Example Scenarios

### Scenario 1: Validating All Plans

User: `/validate-plan-ids`

Output:
```
Scanning 4 status buckets...

✅ ALL VALID (20 plans scanned)
  - 4 backlog plans (P0001–P0004)
  - 5 in-progress plans (P0005, P0017–P0020)
  - 6 outcome plans (P0006–P0009, P0017-OUTCOME, P0021)
  - 5 archive plans (P0010–P0016)

No violations found.
```

### Scenario 2: Detecting Malformed Folder

User: `/validate-plan-ids 02-in_progress-plans`

Output:
```
Scanning 02-in_progress-plans/...

❌ VIOLATIONS FOUND (1 error, 1 warning):

ERRORS:
1. Folder name invalid: P0020_rule-system-reform/
   Expected: P0020_YYYY-MM-DD_HHMM_PLAN-{slug}/
   Fix: Rename to P0020_2026-05-04_1430_PLAN-rule-system-reform/

WARNINGS:
1. P0005 marked "DRAFT" in PLANS_INDEX
   Status should be "In Progress" or plan should be moved to backlog

Run `/validate-plan-ids --fix` to auto-correct.
```

### Scenario 3: Fixing with --fix Flag

User: `/validate-plan-ids --fix`

Output:
```
Found 1 correctable violation:
  Renaming: P0020_rule-system-reform/
         → P0020_2026-05-04_1430_PLAN-rule-system-reform/

Apply fixes? [Y/n]: Y

✅ Renamed 1 folder
✅ All files are now valid
✅ PLANS_INDEX.md is in sync

Validation complete. Run `/validate-plan-ids` again to verify.
```

## Implementation Notes

- Uses Glob to scan `plans/` directory
- Parses folder and file names using regex: `P(\d{4})_(\d{4}-\d{2}-\d{2})_(\d{4})_(PLAN|OUTCOME)-(.+)`
- Validates dates with strptime (Python stdlib)
- Reads PLANS_INDEX.md to cross-reference plan entries
- On --fix, uses Bash/PowerShell to rename folders/files
- Does not delete files (manual confirmation required)
- Reports all violations in one pass (not iterative)

---

**Reference**: `.claude/rules/plan-documentation-structure.md`, `memory/convention_project_standards.md`

**Related Skills**: `/audit-plan-outcomes`, `/enforce-repo-cleanliness`

