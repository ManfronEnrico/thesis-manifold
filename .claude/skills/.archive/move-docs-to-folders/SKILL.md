---
name: move-docs-to-folders
description: >
  Auto-scan root directory for markdown documentation violations, analyze document 
  content to determine type, suggest appropriate destination using the routing table 
  from root-documentation-boundary rule, and move files with cross-reference updates.
---

# Move Docs to Folders

Automatically detect markdown files at root that violate the root-documentation-boundary rule, analyze their content to determine document type, suggest appropriate destinations, and move files with cross-reference updates.

---

## Quick Start

```
/move-docs-to-folders
```

**No arguments required.** The skill scans root, identifies violations, analyzes content, suggests destinations, and prompts for confirmation before moving.

---

## When to Use This Skill

Use `/move-docs-to-folders` when:

- **Root contains markdown violations** — Analysis docs, test reports, or guides accidentally created at root
- **Cleaning up after documentation pass** — Moving generated docs to appropriate folders
- **Periodic root hygiene** — Scanning to ensure no new violations have accumulated
- **After new rules established** — Enforcing new documentation boundaries retroactively
- **As part of documentation workflow** — Complementing `/docs-update-all` for ongoing cleanup

**Do NOT use** if root is clean or violations are intentional (rare).

---

## Trigger Phrases

The skill activates when you use any of these phrases:

- `move docs to folders`
- `clean up root documentation`
- `relocate root docs`
- `move markdown files`
- `reorganize documentation`
- `audit root for violations`
- `check root documentation`

---

## Compatibility

**Required tools:**
- `Read` — Load document contents for analysis
- `Write` — Move files to new locations
- `Glob` — Scan root for markdown files
- `Grep` — Analyze content and update cross-references

**File system access required:**
- Read: root `*.md` files, `.claude/rules/root-documentation-boundary.md`
- Write: All destination folders (docs/, plans/, thesis/)

**Reference files:**
- `.claude/rules/root-documentation-boundary.md` — Routing table, whitelists, examples

---

## How It Works

The skill processes violations in three phases:

### Phase 1: Scan & Whitelist Check

**Action:**
1. Scan root directory for all `.md` files
2. Compare against whitelist (CLAUDE.md, INDEX.md, README.md, paths.py, requirements.txt)
3. Flag any file NOT in whitelist as violation

**Output:**
```
Root Scan Results:
  ✓ CLAUDE.md (whitelisted)
  ✓ README.md (whitelisted)
  ✗ PREPROCESSING_ANALYSIS.md (VIOLATION)
  ✗ TEST_REPORT.md (VIOLATION)
```

---

### Phase 2: Content Analysis & Destination Suggestion

**For each violation, analyze:**

1. **Document type detection:**
   - Read first 500 chars + headers
   - Search for keywords: "test", "report", "analysis", "audit", "verification", "design", "plan"
   - Check for plan-related markers (plan folder reference, project-specific ID patterns)

2. **Route using routing table:**

| Content Keywords | Default Destination | Notes |
|---|---|---|
| "test", "report", "test report", "execution" | `docs/tooling/` OR plan folder | If plan-related → plan folder; else tooling |
| "analysis", "pipeline", "architecture", "data" | `docs/tooling/` OR plan folder | Same logic as above |
| "verification", "audit", "report", "documentation" | `docs/reference/` | Reference docs, audits, verification records |
| "design", "decision", "architecture", "pattern" | `docs/codebase/` | Design decisions, architectural notes |
| "compliance", "requirement", "regulation" | Project-specific compliance folder* | *Example: `thesis/thesis-context/formal-requirements/` |
| Plan artifact markers (IDs, folder refs) | Project's plan folder structure | Example: `plans/{status}/P{NNNN}_.../ ` |

*Note: Compliance and plan artifacts are project-specific. Adjust destinations based on your project structure (e.g., `docs/compliance/`, `governance/`, or custom plan hierarchy).

3. **Output suggestion:**
```
PREPROCESSING_ANALYSIS.md
  → Content: Preprocessing pipeline architecture analysis
  → Keywords detected: "pipeline", "analysis", "architecture"
  → Routing decision: `docs/tooling/` (generic analysis)
  → Suggested path: docs/tooling/preprocessing-analysis.md
```

---

### Phase 3: User Confirmation & File Move

**For each suggested move:**

1. **Present confirmation prompt:**
```
Move file?
  From: /PREPROCESSING_ANALYSIS.md
  To:   docs/tooling/preprocessing-analysis.md
  
  [Confirm] [Suggest Different Destination] [Skip]
```

2. **If confirmed:**
   - Copy file to destination
   - Update cross-references (CLAUDE.md, README.md, INDEX.md, etc.)
   - Search for links to original location, update to new path
   - Delete original file from root
   - Log move to summary report

3. **If different destination suggested:**
   - Use user's path instead
   - Execute same move logic

4. **If skipped:**
   - Record as skipped in report
   - Continue to next violation

---

## Output & Report

**Summary Report:**
```
================================================================================
Documentation Relocation Summary
================================================================================

Violations Found: 3
  ✓ Moved: 2
  ✗ Failed: 0
  ⊘ Skipped: 1

Detailed Results:

✓ PREPROCESSING_ANALYSIS.md
  → Moved to: docs/tooling/preprocessing-analysis.md
  → Cross-references updated: 2 (CLAUDE.md, INDEX.md)

✓ TEST_REPORT.md
  → Moved to: plans/02-in_progress-plans/P0019_.../2026-05-04_DOC-test-report.md
  → Cross-references updated: 1 (P0019 plan folder reference)

⊘ FUTURE_GUIDE.md
  → Skipped at user request

================================================================================
Root Status After Relocation:
  CLAUDE.md ✓
  README.md ✓
  paths.py ✓
  INDEX.md ✓
  
All violations resolved.
================================================================================
```

---

## Algorithm: Content Type Detection

```python
def detect_document_type(content: str) -> str:
    """Analyze content to determine document type (project-agnostic)."""
    
    keywords = {
        'test_report': ['test', 'report', 'execution', 'validation', 'results'],
        'analysis': ['analysis', 'pipeline', 'architecture', 'comparison'],
        'verification': ['verification', 'audit', 'documentation', 'check'],
        'design_decision': ['design', 'decision', 'architecture', 'pattern'],
        'compliance': ['compliance', 'requirement', 'regulation', 'governance'],
        'plan_artifact': ['plan', 'artifact', 'project tracking'],  # Project-agnostic markers
    }
    
    detected = []
    for doc_type, words in keywords.items():
        score = sum(content.lower().count(word) for word in words)
        if score > 0:
            detected.append((doc_type, score))
    
    if not detected:
        return 'general_documentation'  # Fallback
    
    # Return highest-scoring type
    return max(detected, key=lambda x: x[1])[0]


def route_by_type(doc_type: str, project_config: dict) -> str:
    """Route document to destination based on type and project configuration."""
    
    # Project-agnostic base routes
    base_routes = {
        'test_report': project_config.get('tooling_dir', 'docs/tooling/'),
        'analysis': project_config.get('tooling_dir', 'docs/tooling/'),
        'verification': project_config.get('reference_dir', 'docs/reference/'),
        'design_decision': project_config.get('codebase_dir', 'docs/codebase/'),
        'compliance': project_config.get('compliance_dir', 'docs/compliance/'),  # Customize per project
        'plan_artifact': project_config.get('plan_dir', 'plans/'),
        'general_documentation': project_config.get('tooling_dir', 'docs/tooling/'),
    }
    
    return base_routes.get(doc_type, base_routes['general_documentation'])


def route_plan_artifact(content: str, plan_config: dict) -> str:
    """Route plan artifacts using project-specific plan ID markers."""
    # Extract project-specific plan ID pattern from content
    # Example: P(\d{4}) for this thesis project, or custom pattern for others
    id_pattern = plan_config.get('plan_id_pattern', r'P(\d{4})')
    match = re.search(id_pattern, content)
    if match:
        plan_id = match.group(0)  # Keep full match (e.g., 'P0017')
        return f"{plan_config.get('plan_dir', 'plans/')}{plan_id}/"
    return plan_config.get('plan_dir', 'plans/')
```

**Configuration Example (Thesis Project):**
```python
project_config = {
    'tooling_dir': 'docs/tooling/',
    'reference_dir': 'docs/reference/',
    'codebase_dir': 'docs/codebase/',
    'compliance_dir': 'thesis/thesis-context/formal-requirements/',  # Project-specific
    'plan_dir': 'plans/02-in_progress-plans/',
    'plan_id_pattern': r'P(\d{4})',  # Project-specific ID format
}
```

---

## Cross-Reference Update Strategy

After moving a file, update references in these locations:

1. **CLAUDE.md** — If doc is referenced in project instructions
2. **README.md** — If doc is referenced in project overview
3. **INDEX.md** — If doc is part of navigation
4. **Plan folders** — If doc is referenced in any plan file
5. **.claude/rules/** — If doc is referenced in any rule

**Search pattern:** `filename` (without extension), `/FILENAME.md`, `FILENAME`

**Replacement pattern:** Use new path with relative links from referencing file

---

## Limitations & Notes

- **Symlinks:** Skipped (not moved, reported separately)
- **Non-markdown:** Ignored (only scans `.md` files)
- **Large files:** No size limit; processes all
- **Encoding:** Assumes UTF-8; reports encoding errors
- **Partial moves:** If one file fails, others continue; failed files reported

---

## Integration with Other Skills

### Works With: `/docs-update-all`

Enhanced `/docs-update-all` now:
1. Detects root violations during docs workflow
2. Prompts user to run `/move-docs-to-folders` if violations found
3. Skips doc updates for files at root (they shouldn't be there)

### Works With: `/git-draft-commit`

Moved files automatically tracked by git:
```
Moved: docs/tooling/preprocessing-analysis.md (was at root)
Moved: plans/.../2026-05-04_DOC-test-report.md (was at root)
```

Include in commit message if desired.

---

## Examples

### Example 1: Analysis Doc

**Violation:** `PREPROCESSING_ANALYSIS.md` at root

**Analysis:**
```
Keywords: "preprocessing", "analysis", "pipeline", "architecture"
Type detected: analysis
Plan-related: Yes (mentions "P0019")
Routing: plans/02-in_progress-plans/P0019_.../2026-05-04_DOC-preprocessing-analysis.md
```

**Result:** ✓ Moved with cross-references updated

---

### Example 2: Verification Report

**Violation:** `VERIFICATION_REPORT.md` at root

**Analysis:**
```
Keywords: "verification", "audit", "documentation"
Type detected: verification
Plan-related: No
Routing: docs/reference/VERIFICATION_REPORT.md
```

**Result:** ✓ Moved with cross-references updated

---

### Example 3: Future Test Report

**Violation:** `TEST_REPORT_FUTURE.md` at root (hypothetical)

**Analysis:**
```
Keywords: "test", "report", "execution"
Type detected: test_report
Plan-related: No (no plan reference)
Routing: docs/tooling/test-report-future.md
```

**Result:** ✓ Moved (or skipped if user prefers)

---

## See Also

- `.claude/rules/root-documentation-boundary.md` — Complete routing table and rationale
- `.claude/skills/docs-update-all/` — Enhanced with violation detection
- `plans/02-in_progress-plans/P0019_2026-05-04_1400_PLAN-preprocessing-unification/` — Documentation reorganization plan

