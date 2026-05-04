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

Without boundaries, root becomes a dumping ground: hard to navigate, hard to discover docs, hard to maintain. **Solution:** Root = entry points only. Everything else = organized by type.

---

## How to Apply This Rule

**When creating a document:** Use routing table above. If unsure, ask: "Is this needed on day 1?" If no → goes to `docs/` or plan folder.

**When catching a violation:** Identify type, use routing table to find destination, move file, update cross-references.

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

**Analysis doc:** ✓ `docs/architecture/preprocessing-analysis.md` ✗ `/PREPROCESSING_ANALYSIS.md`

**Plan artifact:** ✓ `plans/02-in_progress-plans/P0019_.../2026-05-04_DOC-test-report.md` ✗ `/TEST_REPORT.md`

**Setup guide:** Check if foundational → if yes (about Claude Code), update CLAUDE.md; if no → `docs/integration/`

