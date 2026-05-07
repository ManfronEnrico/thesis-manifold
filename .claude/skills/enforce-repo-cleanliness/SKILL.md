# /enforce-repo-cleanliness

Master orchestrator skill that runs all repo validation checks in sequence and produces a unified enforcement gate report.

## Purpose

Coordinate all four enforcement validators into a single coherent audit:
1. `/validate-plan-ids` — P-ID naming convention compliance
2. `/audit-plan-outcomes` — Plan outcome completeness
3. `/audit-cross-references` — Link/reference integrity
4. `/sync-memory-indices` — Memory discoverability

Use this skill to:
- Run full repo validation before major phases
- Enforce rules during session handoff
- Generate compliance reports for plan completion
- Block non-compliant commits (when used as CI gate)

## Invocation

```
/enforce-repo-cleanliness
/enforce-repo-cleanliness --strict          # Fail on any warning (not just errors)
/enforce-repo-cleanliness --fix             # Apply all auto-fixable violations
/enforce-repo-cleanliness --report          # Generate detailed audit report
/enforce-repo-cleanliness --phase <N>       # Run checks relevant to Phase N of P0020
```

## How It Works

### Step 1: Pre-Flight Checks

Before running validators, verify:
- Git repo is clean (no uncommitted changes that would be stale during validation)
- All required directories exist (`plans/`, `docs/`, `.claude/rules/`, `memory/`)
- No lock files preventing reads (permissions OK)

If issues found, report and ask for confirmation to proceed anyway.

### Step 2: Run Validators in Sequence

Execute in this order (dependencies):

**1. `/validate-plan-ids` (no dependencies)**
```
Validating P-ID naming conventions...
Checking: 20 plans (4 backlog + 5 in-progress + 6 outcomes + 5 archive)
```

**2. `/sync-memory-indices` (independent)**
```
Synchronizing memory index...
Checking: 15 memory files + 1 index
```

**3. `/audit-plan-outcomes` (depends on valid P-IDs from Step 1)**
```
Auditing plan outcomes...
Checking: 6 completed plans + 5 in-progress plans
```

**4. `/audit-cross-references` (depends on valid file structure from Steps 1–3)**
```
Auditing cross-references...
Checking: 247 references across all docs + plans + memory
```

### Step 3: Aggregate Results

Collect all validator outputs:

```
═══════════════════════════════════════════════════════════════
        REPOSITORY CLEANLINESS ENFORCEMENT REPORT
═══════════════════════════════════════════════════════════════

Generated: 2026-05-04 15:30:00
Scope: Full repository validation (4 validators)
Mode: STANDARD (report only, no fixes applied)

───────────────────────────────────────────────────────────────
VALIDATOR 1: Plan ID Validation
───────────────────────────────────────────────────────────────
Status: ✅ PASS
  - 20 plans scanned
  - 20 valid P-ID formats
  - 0 duplicates
  - 0 violations

───────────────────────────────────────────────────────────────
VALIDATOR 2: Memory Index Synchronization
───────────────────────────────────────────────────────────────
Status: ✅ PASS
  - 16 memory files scanned (15 files + 1 index)
  - 16 entries in MEMORY.md
  - 0 orphaned files
  - 0 stale entries

───────────────────────────────────────────────────────────────
VALIDATOR 3: Plan Outcome Audit
───────────────────────────────────────────────────────────────
Status: ✅ PASS
  - 6 completed plans checked
  - 6 outcome files present
  - 6 frontmatter valid
  - 5 in-progress plans (no outcome expected)
  - 0 violations

───────────────────────────────────────────────────────────────
VALIDATOR 4: Cross-Reference Audit
───────────────────────────────────────────────────────────────
Status: ✅ PASS
  - 247 references validated
  - 247 targets exist
  - 0 broken links
  - 0 circular references

───────────────────────────────────────────────────────────────
OVERALL RESULT: ✅ ALL CHECKS PASSED
───────────────────────────────────────────────────────────────

Summary:
  Total violations: 0
  Total warnings: 0
  Auto-fixable issues: 0
  Manual fixes needed: 0

✓ Repository is CLEAN and COMPLIANT

Next steps:
  - Proceed with session work (no blockers)
  - Continue with Phase 6 (master skill complete)
  - Schedule next validation before Phase 8
```

### Step 4: Handle Violations

If violations found, categorize by severity:

```
❌ VIOLATIONS FOUND (5 total)

ERRORS (Blocking):
  - 1 error from validate-plan-ids
  - 2 errors from audit-cross-references

WARNINGS (Non-blocking):
  - 2 warnings from sync-memory-indices

STATUS: ❌ FAILED (errors must be fixed)
```

### Step 5: Apply Fixes (with --fix flag)

If `--fix` specified and issues are auto-fixable:

```
Applying fixes...

FROM validate-plan-ids:
  ✓ Renamed 1 folder (P-ID format)

FROM sync-memory-indices:
  ✓ Added 2 orphaned files to index
  ✓ Removed 1 stale index entry

FROM audit-cross-references:
  ✓ Updated 3 broken links

SUMMARY:
  ✅ Fixed 6 issues
  ⚠️  2 issues require manual intervention

Next: Review manual fixes and run /enforce-repo-cleanliness again
```

### Step 6: Generate Report (with --report flag)

Produces detailed audit report:

```
Generating comprehensive enforcement report...

[HTML report saved to docs/reference/enforcement-audit-2026-05-04.html]
[Markdown report saved to docs/reference/enforcement-audit-2026-05-04.md]

Report includes:
  - Detailed results from all 4 validators
  - Violation categorization (error/warning/info)
  - Suggested fixes for each violation
  - Cross-validator dependency analysis
  - Compliance timeline (when each check last passed)
  - Recommendations for future validation
```

## Phase-Specific Validation (--phase flag)

Run only checks relevant to specific P0020 phases:

```
/enforce-repo-cleanliness --phase 4
```

**Phase 1:** Reclassify + consolidate
- Checks: `/sync-memory-indices` only
- Purpose: Verify conventions moved to memory

**Phase 2:** Prose compression
- Checks: `/validate-plan-ids` only
- Purpose: Ensure plan naming stable during compression

**Phase 3:** Move procedures
- Checks: `/audit-cross-references` only
- Purpose: Verify all skill references updated

**Phase 4:** Priority hierarchy
- Checks: `/validate-plan-ids` + `/audit-cross-references`
- Purpose: Ensure rules & cross-refs valid

**Phase 5:** Build validators
- Checks: All 4 validators
- Purpose: Self-check new validation skills

**Phase 6:** Build master skill
- Checks: All 4 validators (this skill)
- Purpose: Orchestrator working correctly

**Phase 7:** Update navigation
- Checks: `/audit-cross-references` only
- Purpose: CLAUDE.md links all valid

**Phase 8:** Final validation
- Checks: All 4 validators + full report
- Purpose: Complete repo cleanliness before completion

## Integration with Rule Hierarchy

This skill enforces multiple tiers from `.claude/rules/rule-priority-hierarchy.md`:

**Trust Tier:**
- Root documentation boundary (checked by `/audit-cross-references`)
- Branch strategy (verified by git state, not in this skill)

**Correctness Tier:**
- Plan outcome discipline (checked by `/audit-plan-outcomes`)

**Quality Tier:**
- One-off execution + bullets-only (enforced by other mechanisms, this skill validates supporting structures)

## Exit Codes

For use in CI/CD gates:

```
0 = All checks passed (clean)
1 = Warnings only (review but not blocking)
2 = Errors found (must fix before proceeding)
3 = Validators themselves failed (implementation issue)
```

## Example Scenarios

### Scenario 1: Full Pre-Phase Validation

User: `/enforce-repo-cleanliness`

Output: (see Step 3 above — clean case)

### Scenario 2: Strict Mode (Fail on Warnings)

User: `/enforce-repo-cleanliness --strict`

Output:
```
Running in STRICT mode (warnings = failures)...

❌ STRICT CHECK FAILED

Warnings found:
  - 1 warning from sync-memory-indices
    (P0005 marked "DRAFT" in PLANS_INDEX, should be explicit status)

Under strict mode, fix and re-run: /enforce-repo-cleanliness --strict
```

### Scenario 3: Fix and Report

User: `/enforce-repo-cleanliness --fix --report`

Output:
```
Running validators with auto-fix enabled...
[validators run and apply fixes]

Generating detailed report...
[report saved]

✅ Fixed 3 issues
📋 Report saved to docs/reference/enforcement-audit-2026-05-04.html

Next: Review report and verify fixes are correct
```

### Scenario 4: Phase-Specific Check

User: `/enforce-repo-cleanliness --phase 5`

Output:
```
Running Phase 5 validation (all 4 validators)...

This is a self-check that the new enforcement skills are working.

Validator 1: /validate-plan-ids ... ✅ PASS
Validator 2: /sync-memory-indices ... ✅ PASS
Validator 3: /audit-plan-outcomes ... ✅ PASS
Validator 4: /audit-cross-references ... ✅ PASS

✅ ALL PHASE 5 CHECKS PASSED
Enforcement skills are operational.
```

## Implementation Notes

- Calls each validator as independent subprocess
- Aggregates exit codes (0 = pass, 1 = warning, 2 = error)
- Captures and formats output from each validator
- Runs validators in dependency order (1 → 2 → 3 → 4)
- Collects all results before reporting (not streaming)
- Supports --fix by passing flag to each validator
- Supports --report by generating unified markdown/HTML output
- Supports --phase by determining which validators to run
- Exit code is MAX(all validator exit codes) for overall status
- Does not modify files unless --fix explicitly specified
- Timestamps all reports with generation time

## Data Integrity

- **Read-only by default**: Reports violations without modifying
- **Explicit fix with --fix**: Shows summary of changes before applying
- **Atomic violations collection**: All validators run regardless of individual failures
- **No partial fixes**: Either all fixes apply or none do (manual recovery if interrupted)
- **Comprehensive audit trail**: All fixes logged with before/after values

---

**Reference**: `.claude/rules/rule-priority-hierarchy.md`, `.claude/rules/plan-documentation-structure.md`, `memory/convention_project_standards.md`

**Depends On**: `/validate-plan-ids`, `/sync-memory-indices`, `/audit-plan-outcomes`, `/audit-cross-references`

**Used By**: P0020 Phase 5–8, CI/CD gates, session handoff validation

