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

**Default rule: when in doubt, go to `docs/`.** All analysis, reports, checklists, session notes, and reference material belong under `docs/` subfolders.

| Document Type | Goes To | Naming Convention |
|---|---|---|
| **System Design, Architecture, ADRs** | `docs/architecture/` | Descriptive name |
| **Setup Guides, Integration, Tooling** | `docs/integration/` | Descriptive name |
| **Verification / Audits, Test Reports, Session Notes, Checklists** | `docs/reference/` | Descriptive name |
| **Handover Documents (cross-session, cross-person)** | `docs/handovers/` | `{topic}-handover-{person}.md` or index |
| **Developer Guide, Repo Structure, Git Workflow** | `docs/contributing/` | Descriptive name |
| **Compliance Notes** | `thesis/thesis-context/formal-requirements/` | Descriptive name |
| **Workflow Automation** | `.claude/rules/` | For trigger phrases / rules only |
| **Plan Artifacts** | `plans/P{NNNN}_YYYY-MM-DD_.../` | `YYYY-MM-DD_DOC-{slug}.md` |

> **If it's analysis, a checklist, a migration guide, or session log → `docs/reference/`. Handovers for another person or session → `docs/handovers/`. No exceptions.**

### Examples

✅ **CORRECT:**
```
docs/architecture/architecture.md
docs/integration/zotero-integration-setup.md
docs/integration/tooling-issues.md
docs/reference/verification-report.md
docs/reference/CHEATSHEET.md
docs/handovers/2026-06-22_15-00_preprocessing-eda-handover-enrico.md
docs/handovers/2026-06-22_15-00_HANDOVER_INDEX.md
docs/contributing/repository_map.md
docs/contributing/git-branch-strategy.md
plans/03-focus_plans/P0019_.../2026-05-04_DOC-test-report.md
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

**This rule is Trust Tier — non-negotiable. Never write analysis, checklists, session notes, or any ad-hoc docs outside `docs/`.** Not at root, not inside `thesis/` (unless native thesis content), not in any other folder.

**Automated check:** `/move-docs-to-folders` skill scans root for violations and prompts relocation.

**Manual audit (PowerShell):**
```powershell
Get-ChildItem "Z:\_dev-ssd\thesis-manifold\*.md" | Where-Object { $_.Name -notmatch "^(CLAUDE|INDEX|README)" }
# Should return nothing — any result is a violation
```

**Before writing any `.md` file, ask:** "Is this a foundational project file?" If no → write it under `docs/` (pick the right subfolder from the routing table above). Never create it at root first and move it later.

---

## See Also

- `.claude/rules/plan-documentation-structure.md` — P-ID folder organization
- `.claude/rules/trigger-docs-workflow.md` — Docs update workflow
- `.claude/skills/move-docs-to-folders/` — Skill for auto-relocation (planned)

---

## Session Example

**Analysis doc:** ✓ `docs/architecture/preprocessing-analysis.md` ✗ `/PREPROCESSING_ANALYSIS.md`

**Plan artifact:** ✓ `plans/03-focus_plans/P0019_.../2026-05-04_DOC-test-report.md` ✗ `/TEST_REPORT.md`

**Setup guide:** Check if foundational → if yes (about Claude Code), update CLAUDE.md; if no → `docs/integration/`

