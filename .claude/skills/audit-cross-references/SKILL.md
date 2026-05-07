# /audit-cross-references

Validate that all cross-references (links, file paths, citations) in the codebase are correct and point to existing targets.

## Purpose

Enforce data integrity by detecting:
- Broken markdown links (`[text](path)` where path doesn't exist)
- Stale file references in documentation
- Missing cross-references when files are moved or deleted
- Inconsistent path formats across documents
- Orphaned image or asset references

## Invocation

```
/audit-cross-references
/audit-cross-references --scan <path>  # Audit single directory (e.g., docs/, thesis/)
/audit-cross-references --fix          # Suggest fixes for broken references
/audit-cross-references --report       # Generate full audit report
```

## How It Works

### Step 1: Identify All Reference Types

Scans repo for references in:

**Markdown links:**
```
[text](../path/to/file.md)
[text](../../docs/architecture/file.md)
```

**Code comments & docstrings:**
```python
# See: path/to/file.py
"""Reference: docs/integration/setup.md"""
```

**YAML frontmatter:**
```yaml
---
reference: plans/06-paused_plans/P0020_YYYY-MM-DD_HHMM_PLAN-{slug}/
related: [file1.md, file2.md]
---
```

**Configuration files:**
```json
{
  "path": "thesis/data/raw_nielsen/scripts/",
  "reference": ".claude/config.json"
}
```

### Step 2: Validate Each Reference

For **each reference found**, check:

1. **Target exists**: File or folder is present in repo
2. **Path format**: Consistent relative path (use `../` for parent dirs, not absolute paths)
3. **Reference is current**: File hasn't moved or been deleted since reference was created
4. **No circular references**: Document A doesn't reference B which references A (simple check)

### Step 3: Cross-Reference with Authority Files

Check against known authorities:
- `.claude/rules/` — all rule files
- `docs/` — all documentation
- `plans/` — all plan files
- `thesis/` — all thesis content
- `CLAUDE.md`, `README.md`, `INDEX.md` — entry points

### Step 4: Report Violations

Return comprehensive report:

```
✅ VALID REFERENCES (247 checked):
- 145 markdown links (all targets exist)
- 62 code references (all files present)
- 40 frontmatter references (all coherent)

❌ BROKEN REFERENCES (3 found):

1. docs/architecture/architecture.md:45
   Link: [git-branch-strategy](docs/contributing/git-branch-strategy.md)
   Error: File not found (moved to .claude/rules/trigger-branch-strategy.md)
   Fix: Update link to ../../.claude/rules/trigger-branch-strategy.md

2. CLAUDE.md:23
   Link: [tooling-issues.md](docs/integration/tooling-issues.md)
   Error: File moved to docs/reference/ (per P0021 routing)
   Fix: Update link to docs/reference/tooling-issues.md

3. plans/02-in_progress-plans/P0020_.../P0020_...md:156
   Link: [rule-reform-gaps.md](docs/reference/rule-reform-gaps.md)
   Error: File path is relative to project root, but file in docs/reference/
   Fix: Use relative path ../../docs/reference/rule-reform-gaps.md

⚠️  WARNINGS (2 found):

1. thesis/thesis-context/thesis-topic/project-state.md:89
   Reference: 'Prometheus integration architecture (2026-04-27)'
   Issue: Date is static; should verify this is still current
   Action: Check memory/prometheus_integration_architecture.md for updates

2. memory/MEMORY.md (index file)
   Missing entry: Convention file convention_project_standards.md
   Added file not yet in MEMORY.md index
   Action: Run /sync-memory-indices to update

AUDIT COMPLETE
```

### Step 5: Suggest Fixes (with --fix flag)

If `--fix` specified, offer:

```
Found 3 broken references. Apply fixes?

1. docs/architecture/architecture.md:45
   OLD: [git-branch-strategy](docs/contributing/git-branch-strategy.md)
   NEW: [git-branch-strategy](../../.claude/rules/trigger-branch-strategy.md)
   [Y/n] Y

2. CLAUDE.md:23
   OLD: [tooling-issues.md](docs/integration/tooling-issues.md)
   NEW: [tooling-issues.md](docs/reference/tooling-issues.md)
   [Y/n] Y

3. plans/02-in_progress-plans/P0020_.../P0020_...md:156
   OLD: [rule-reform-gaps.md](docs/reference/rule-reform-gaps.md)
   NEW: [rule-reform-gaps.md](../../docs/reference/rule-reform-gaps.md)
   [Y/n] Y

✅ Fixed 3 references
```

### Step 6: Generate Full Report (with --report flag)

```
Generating comprehensive audit report...

📋 CROSS-REFERENCE AUDIT REPORT
Generated: 2026-05-04 15:15:00
Scope: All markdown files + code comments + YAML frontmatter

[HTML report saved to docs/reference/cross-reference-audit-2026-05-04.html]
[Markdown report saved to docs/reference/cross-reference-audit-2026-05-04.md]

Report includes:
- All 247 references categorized by type
- Broken references with suggested fixes
- Link graph visualization (which files reference which)
- Update recommendations (files with stale dates/versions)
```

## Integration with P0020

This skill enforces data integrity during the rule system reform by:
- Detecting when rules/docs are moved to new locations (via P0021)
- Verifying all rules/skills reference the correct files
- Updating cross-references when rules are reorganized

**Related:** `/validate-plan-ids`, `/audit-plan-outcomes`, `/sync-memory-indices`, `/enforce-repo-cleanliness`

## Example Scenarios

### Scenario 1: Quick Audit

User: `/audit-cross-references`

Output: (see Step 4 above — 3 broken, 2 warnings case)

### Scenario 2: Audit Specific Directory

User: `/audit-cross-references --scan docs/`

Output:
```
Scanning docs/ directory (recursive)...

Found 95 references in docs/:
- 85 valid markdown links
- 10 code references

✅ ALL REFERENCES VALID
No broken links in docs/ folder.
```

### Scenario 3: Fix and Report

User: `/audit-cross-references --fix --report`

Output:
```
Scanning entire repo...
Found 3 broken references.

Apply fixes?
[1] docs/architecture/architecture.md (1 fix)
[2] CLAUDE.md (1 fix)
[3] Plan P0020 (1 fix)
All fixes? [Y/n] Y

✅ Fixed 3 references
Generating full audit report...
[saved to docs/reference/cross-reference-audit-2026-05-04.html]
```

## Implementation Notes

- Uses Grep to find markdown links: `\[([^\]]+)\]\(([^)]+)\)`
- Uses Grep to find code references: `#.*See:|#.*Reference:|""".*Reference:`
- Uses Glob to verify target files exist
- Parses relative paths (handles `../`, `./`, absolute from project root)
- Does NOT check external links (HTTP/HTTPS) — only local repo files
- Regex for path patterns: supports `.md`, `.py`, `.txt`, `.json`, etc.
- Cross-references authority files (CLAUDE.md, rules, plans, docs)
- Report is read-only (uses --fix to modify files)
- Batch processes all references in single pass

## Data Integrity Guarantees

- **Read-only by default**: Reports findings without modifying
- **Explicit confirmation with --fix**: Shows each change before applying
- **Comprehensive scope**: Covers all file types and reference patterns
- **Authority-aware**: Understands P0021 folder structure and rule locations
- **Audit trail**: All fixes logged with before/after values

---

**Reference**: `.claude/rules/root-documentation-boundary.md`, `.claude/rules/plan-documentation-structure.md`, `memory/convention_project_standards.md`

**Related Skills**: `/validate-plan-ids`, `/sync-memory-indices`, `/enforce-repo-cleanliness`

