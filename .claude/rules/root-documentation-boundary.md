---
name: Root Documentation Boundary
description: Enforce clean root—only foundational project files allowed; all analysis/reference docs in respective folders
type: feedback
---

# Root Documentation Boundary Rule

**Principle:** Root directory contains ONLY foundational project artifacts. All markdown documentation—analysis, reports, audits, guides—goes to appropriate respective folders.

---

## Whitelist (Allowed at Root)

These files MUST stay at root for discoverability and project initialization:

- **CLAUDE.md** — Project instructions & workflows (entry point for Claude Code sessions)
- **INDEX.md** — Repository index & navigation hub
- **paths.py** — Centralized path configuration (Python executable)
- **README.md** — Project overview & setup (discoverable by any developer)
- **requirements.txt** — Dependencies manifest

---

## Blacklist (Never at Root)

ANY markdown documentation not in the whitelist above belongs elsewhere:

- ✗ Analysis documents (e.g., `PREPROCESSING_ANALYSIS.md`)
- ✗ Test reports (e.g., `TEST_REPORT_PREPROCESSING.md`)
- ✗ Verification audits (e.g., `VERIFICATION_REPORT.md`)
- ✗ Implementation guides
- ✗ Workflow documentation (except CLAUDE.md)
- ✗ Data pipeline descriptions
- ✗ Meeting notes / summaries

---

## Destination Routing

When creating markdown documentation, use this routing table:

| Document Type | Goes To | Naming Convention |
|---|---|---|
| **System Design, Architecture, ADRs** | `docs/architecture/` | Descriptive name |
| **Setup Guides, Integration, Tooling** | `docs/integration/` | Descriptive name |
| **Verification / Audits, Test Reports** | `docs/reference/` | Descriptive name |
| **Developer Guide, Repo Structure, Git Workflow** | `docs/contributing/` | Descriptive name |
| **Compliance Notes** | `thesis/thesis-context/formal-requirements/` | Descriptive name |
| **Workflow Automation** | `.claude/rules/` | For trigger phrases / rules only |
| **Plan Artifacts** | `plans/{status}/P{NNNN}_.../` | `YYYY-MM-DD_DOC-{slug}.md` |

### Examples

✅ **CORRECT:**
```
docs/architecture/architecture.md
docs/integration/zotero-integration-setup.md
docs/integration/tooling-issues.md
docs/reference/verification-report.md
docs/reference/CHEATSHEET.md
docs/contributing/repository_map.md
docs/contributing/git-branch-strategy.md
plans/03-outcome_plans/P0021_.../2026-05-04_DOC-reorganization-summary.md
```

❌ **INCORRECT:**
```
/PREPROCESSING_ANALYSIS.md        (root)
/TEST_REPORT_PREPROCESSING.md     (root)
/VERIFICATION_REPORT.md           (root)
/DATA_PIPELINE_GUIDE.md           (root)
```

---

## Why This Rule Exists

**Root clutter problem:** Without boundaries, root accumulates analysis docs, test reports, audit files, guides, summaries—becoming a dumping ground. This makes:
- Navigation harder (too many files to scroll through)
- Discovery harder (unclear where to find specific docs)
- Maintenance harder (where does each doc belong? can it move?)
- Onboarding harder (new developers see chaos)

**Solution:** Enforce clear boundaries. Root = entry points only. Everything else = organized by type/phase.

---

## How to Apply This Rule

### When Creating a Document

1. **Is it analysis, report, or reference?** → Goes to `docs/` hierarchy
2. **Is it part of an active plan?** → Goes to `plans/` in P-ID folder
3. **Is it foundational project info?** → Only if CLAUDE.md, INDEX.md, README.md, paths.py, or requirements.txt
4. **Otherwise?** → Ask yourself: "Is this a discovery document someone needs on day 1?" If no, it goes to `docs/` or plan folder

### When You Catch a Violation

If you see markdown at root that shouldn't be there:
1. Identify document type
2. Use routing table above to find destination
3. Move file (with path updates)
4. Update any cross-references

---

## Enforcement

**Automated check (proposed):** `/move-docs-to-folders` skill scans root for violations and prompts relocation.

**Manual check (now):** Run this to audit:
```bash
cd /dev/thesis-manifold
ls -1 *.md | grep -v "CLAUDE\|INDEX\|README"
# Should return empty (no violations)
```

---

## See Also

- `.claude/rules/plan-documentation-structure.md` — P-ID folder organization
- `.claude/rules/trigger-docs-workflow.md` — Docs update workflow
- `.claude/skills/move-docs-to-folders/` — Skill for auto-relocation (planned)

---

## Session Example

**User creates analysis doc:**
```
"I completed preprocessing analysis. Let me document it."

✓ CORRECT: `docs/tooling/preprocessing-analysis.md`
✗ WRONG: `/PREPROCESSING_ANALYSIS.md` (root violation)
```

**User creates test report for a plan:**
```
"I ran tests for the preprocessing unification plan."

✓ CORRECT: `plans/02-in_progress-plans/P0019_.../2026-05-04_DOC-test-report.md`
✗ WRONG: `/TEST_REPORT_PREPROCESSING.md` (root violation)
```

**User creates project guide:**
```
"I'm writing setup instructions for new developers."

Check: Is this foundational? Is it needed on day 1?
  → If about Claude Code usage → CLAUDE.md (update it)
  → If about repository structure → docs/dev/ (create guide there)
  → If about tooling → docs/tooling/
  → If general onboarding → Update README.md (keep short, link to docs/)
```

