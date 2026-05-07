# /sync-memory-indices

Synchronize memory files with their index (MEMORY.md) to ensure discoverability and prevent orphaned memory entries.

## Purpose

Enforce consistency between:
- **Memory files** in `C:\Users\brian\.claude\projects\C--dev-thesis-manifold\memory\`
- **Memory index** at `MEMORY.md` in the same directory

This skill detects:
- Memory files with no index entry (orphaned files)
- Index entries pointing to non-existent files (stale entries)
- Duplicate entries in the index
- Memory files with outdated or incorrect descriptions
- Inconsistent frontmatter across memory files

## Invocation

```
/sync-memory-indices
/sync-memory-indices --scan                # Audit without making changes
/sync-memory-indices --fix                 # Apply all suggested changes
/sync-memory-indices --update-frontmatter  # Refresh all frontmatter metadata
```

## How It Works

### Step 1: Scan Memory Directory

Lists all `.md` files in `memory/` directory:
- `user_*.md` (user profile memories)
- `feedback_*.md` (feedback/behavioral guidance)
- `project_*.md` (project state memories)
- `reference_*.md` (reference/external resource pointers)
- `convention_*.md` (conventions & standards)
- `MEMORY.md` (index file itself)

For each file, extract:
- Filename
- Frontmatter: `name`, `description`, `type`
- First 3 lines of content (for validation)

### Step 2: Validate Each File

For **each memory file**, check:

**Frontmatter structure:**
```yaml
---
name: <descriptive name>
description: <one-line hook for relevance decision>
type: <user|feedback|project|reference|convention>
---
```

All three fields required; `type` must be one of the five allowed values.

**File naming convention:**
- Format: `<type>_<slug>.md`
- Examples: `user_brian.md`, `feedback_bullets_only.md`, `project_thesis_scope.md`
- Must match declared `type` in frontmatter

**Content validation:**
- Non-empty file (not stubs)
- At least one sentence of actual content
- No obvious placeholder text ("TODO", "fill in", "TBD")

### Step 3: Validate Index

For **MEMORY.md index**, check:

**Format:**
```markdown
- [Title](file.md) — one-line hook
- [Title](file.md) — one-line hook
...
```

**Validation rules:**
- Each line starts with `- ` (bullet)
- Title is descriptive (not filename)
- File reference is correct `.md` filename
- One-line hook matches (or closely matches) frontmatter `description`
- No duplicates (same filename listed twice)
- No stale entries (file doesn't exist)
- Lines are under ~150 characters (readability)

### Step 4: Cross-Reference

For **each memory file**, verify:
- File is listed in MEMORY.md index
- Index entry points to correct filename
- Description in index matches frontmatter `description` (closely)

### Step 5: Report

Return audit results:

```
✅ MEMORY INDEX VALIDATED

Status:
- Memory files scanned: 15
- Files with valid frontmatter: 15
- Index entries: 15
- Entries matching files: 15

SYNC COMPLETE: All memory files are discoverable and consistent.
```

### Example Violation Report

If inconsistencies exist:

```
⚠️  SYNC ISSUES FOUND (3 issues)

ORPHANED FILES (file exists, not in index):
1. memory/convention_project_standards.md
   Name: Project Standards & Conventions
   Type: convention
   Description: Consolidated conventions about models, worktrees, plan naming, tooling, and documentation routing
   Fix: Add to MEMORY.md index

STALE ENTRIES (index entry, file doesn't exist):
1. [Reference: Plan IDs](reference_plan_ids.md)
   Expected file: memory/reference_plan_ids.md
   Actual: FILE NOT FOUND
   Fix: Remove from MEMORY.md OR restore file

DESCRIPTION MISMATCH (file and index have different descriptions):
1. memory/feedback_bullets_only.md
   Frontmatter: "WritingAgent never produces prose without explicit approval"
   Index entry: "bullets-only before prose" — too abbreviated
   Fix: Update MEMORY.md to: "WritingAgent never produces prose without explicit approval"

DUPLICATE ENTRIES:
None found ✓

FRONTMATTER ERRORS:
None found ✓

FILENAME MISMATCH:
None found ✓
```

### Step 6: Apply Fixes (with --fix flag)

```
Found 3 sync issues. Apply fixes?

1. Add orphaned file to index:
   + [Project Standards & Conventions](convention_project_standards.md) — Consolidated conventions about models, worktrees, plan naming, tooling, and documentation routing
   [Y/n] Y

2. Remove stale index entry:
   - [Reference: Plan IDs](reference_plan_ids.md)
   [Y/n] Y

3. Update description in index:
   OLD: [Feedback: bullets-only](feedback_bullets_only.md) — bullets-only before prose
   NEW: [Feedback: bullets-only](feedback_bullets_only.md) — WritingAgent never produces prose without explicit approval
   [Y/n] Y

✅ Fixed 3 sync issues
✅ MEMORY.md is now current
```

### Step 7: Refresh Frontmatter (with --update-frontmatter flag)

```
Updating all memory file frontmatter...

For each file, refresh:
- Last accessed date
- Update count
- Relevance tags (auto-extracted from content)

✅ Updated 15 memory files
✅ Frontmatter is current
```

## Integration with P0020

This skill ensures memory consistency during rule system reorganization by:
- Keeping memory index synchronized with new convention files
- Detecting when feedback/project memories become orphaned
- Maintaining discoverability of all session-persistent information

**Related:** `/validate-plan-ids`, `/audit-plan-outcomes`, `/audit-cross-references`, `/enforce-repo-cleanliness`

## Example Scenarios

### Scenario 1: Audit Current State

User: `/sync-memory-indices --scan`

Output:
```
Scanning memory/ directory...
Found 16 files + 1 index.

Memory files (by type):
- user (1): user_brian.md ✓
- feedback (10): feedback_*.md ✓
- project (4): project_*.md ✓
- reference (5): reference_*.md ✓
- convention (1): convention_project_standards.md ✓

Index entries (15):
All entries valid ✓

SYNC STATUS: All files are discoverable and in sync.
```

### Scenario 2: Detect Orphaned File

User: `/sync-memory-indices`

(Assume convention_project_standards.md was created but not added to index)

Output:
```
⚠️  SYNC ISSUE FOUND (1 orphaned file)

ORPHANED FILES:
1. memory/convention_project_standards.md
   Type: convention
   Description: Consolidated conventions about models, worktrees, plan naming, tooling, and documentation routing
   Fix: Add to MEMORY.md index with /sync-memory-indices --fix
```

### Scenario 3: Fix All Issues

User: `/sync-memory-indices --fix`

Output:
```
Found 1 issue to fix.
Adding orphaned file to MEMORY.md index...

✅ Added 1 entry to MEMORY.md
✅ MEMORY.md index is now current

Verify with: /sync-memory-indices --scan
```

### Scenario 4: Refresh Frontmatter

User: `/sync-memory-indices --update-frontmatter`

Output:
```
Updating frontmatter for all memory files...

Processing:
- user_brian.md: Updated metadata
- feedback_bullets_only.md: Updated relevance tags
- project_thesis_scope.md: Updated last_used date
... (12 more)

✅ Updated 15 memory files with current metadata
```

## Implementation Notes

- Uses Glob to scan `memory/` directory
- Regex to validate YAML frontmatter: `^---\nname: .*\ndescription: .*\ntype: (user|feedback|project|reference|convention)\n---$`
- Regex to validate index format: `^- \[.+\]\(.+\.md\) — .+$`
- Regex to validate filename: `^(user|feedback|project|reference|convention)_[a-z_]+\.md$`
- Compares descriptions using fuzzy string matching (allows minor wording differences)
- Batch processes all files in single pass
- Report is read-only by default; uses --fix to modify files
- Frontmatter updates use timestamp and content analysis

## Data Integrity Guarantees

- **Read-only by default**: --scan reports issues without modifying
- **Explicit confirmation with --fix**: Shows each change before applying
- **Atomic updates**: Either all changes succeed or none are applied
- **Backup awareness**: Does not delete files (only adds/updates/removes index entries)
- **Validation-first**: Checks all files before making any changes

---

**Reference**: `memory/MEMORY.md` (index), `.claude/rules/rule-priority-hierarchy.md`

**Related Skills**: `/validate-plan-ids`, `/audit-cross-references`, `/enforce-repo-cleanliness`

