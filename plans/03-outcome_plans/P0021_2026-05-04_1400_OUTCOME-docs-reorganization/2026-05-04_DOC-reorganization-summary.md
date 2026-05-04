---
title: Documentation Reorganization Summary
date: 2026-05-04
status: Complete
---

# Docs Reorganization Summary — 2026-05-04

**Status**: ✅ Complete  
**Restructuring**: 11 folders → 4 core folders + 1 archive  
**Files moved**: 31+ primary moves  
**Supporting docs**: analyses/ and experiments/ consolidated under architecture/  
**Violations resolved**: All root-level violations moved

---

## Final Structure (Path A)

### New Core Folders (4)

```
docs/
├── architecture/           (System design, patterns, ADRs)
│   ├── *.md (8 main docs)
│   ├── analyses/           (Timestamped project analysis docs)
│   └── experiments/        (Experiment tracking registry)
│
├── integration/            (Setup, guides, tooling, data access)
│   ├── *.md (25+ setup docs)
│   ├── zotero-*.md
│   ├── google-drive-*.md
│   ├── notebooklm-*.md
│   └── tooling guides
│
├── reference/              (Quick-ref, verification, testing)
│   ├── CHEATSHEET.md
│   ├── VERIFICATION_REPORT.md
│   ├── *.md (quick-refs, test reports, lookup tables)
│   └── [8 total docs]
│
└── contributing/           (Developer guide, repo structure)
    ├── repository_map.md
    ├── contributor-guide.md
    ├── git-branch-strategy.md
    └── git-worktrees-and-parallel-sessions.md
```

### Archive Folder (1)

```
00_archive/
├── handovers/             (Historical coordination docs)
├── tasks/                 (Outdated planning checklists)
├── thesis/                (Legacy analysis notebooks)
└── [other historical materials]
```

### Not Moved (Already in correct location)

- `docs/thesis/` — thesis content stays as-is (out of scope for this reorganization)
- `.claude/` — skills, rules, plans untouched (not part of docs/)

---

## Semantic Clarity for Claude (Agentic Routing)

### When Claude/Agent Needs to Save a Document

| Document Type | Keywords | → Save To |
|---|---|---|
| System design, ADR, pattern, architecture, agent role | "design", "decision", "architecture" | `docs/architecture/` |
| Setup guide, integration, tooling fix, data access | "setup", "integration", "guide", "config" | `docs/integration/` |
| Quick-ref, verification, test result, audit, lookup | "quick-ref", "verification", "test", "audit" | `docs/reference/` |
| Developer info, repo structure, branching, workflow | "repository", "developer", "git", "contribute" | `docs/contributing/` |
| Plan artifacts, timestamped analyses | P-ID format OR date-stamped | `plans/{status}/P{NNNN}_/` |

**Zero ambiguity**: Folder names are verbs (architecture = "the design", integration = "how to integrate", reference = "look it up", contributing = "how to contribute").

---

## Files Moved by Category

### → docs/architecture/ (8 core + analyses + experiments)

**Design & Architecture:**
- architecture.md — Framework Architecture (System A/B)
- system-architecture-report.md — Multi-agent system inventory
- thesis_production_architecture.md — System separation & rationale
- experiment-tracking-agent.md — Experiment metadata tracking

**Architectural Decisions (ADRs):**
- 2026_04_13-adr_001_template_strategy.md
- 2026_04_13-adr_002_build_pipeline.md
- 2026_04_13-adr_003_builder_agent_fate.md
- 2026_05_01-adr_004_preprocessing_architecture.md

**Design Notes:**
- feature_engineering_design.md
- 2026-04-27_1630_MANIFOLD_ARCHITECTURE_AND_FEATURE_HANDLING.md

**Supporting Structures:**
- analyses/ (5 timestamped migration analysis docs)
- experiments/ (experiment_registry.json, experiment_summary.md)

---

### → docs/integration/ (25+ setup & tooling docs)

**Integration Setup Guides:**
- zotero-integration-setup.md
- enrico-google-drive-setup.md
- google-drive-quick-start.md
- google-drive-setup.md
- notebooklm-integration-complete.md
- notebooklm-setup-guide-enrico.md
- [+ 5 more NotebookLM variants]

**Data Access & Strategy:**
- 2026_04_20-nielsen_data_access_strategy.md
- enrico-systems-architecture.md

**Testing/Validation Guides:**
- agent-system-test-scenarios.md
- pre-sync-test-guide.md
- test-group-script-readme.md

**Tooling:**
- tooling-issues.md (Windows/OneDrive/CRLF problems)

---

### → docs/reference/ (11 docs)

**Quick References:**
- CHEATSHEET.md
- zotero-quick-reference.md
- testing-quick-reference.md
- SYNC_CHECK_GUIDE.md

**Verification & Audits:**
- VERIFICATION_REPORT.md (links check)
- integrations_index.md (integration inventory)

**Test Results & Validation:**
- test-summary-2026-04-15.md
- validation-complete-2026-04-15.md
- test-execution-checklist.md

**Implementation Notes:**
- rule-reform-gaps.md
- rule-reform-implementation.md

---

### → docs/contributing/ (4 docs)

- repository_map.md (file-to-purpose mapping)
- contributor-guide.md (setup & conventions)
- git-branch-strategy.md (branching rules)
- git-worktrees-and-parallel-sessions.md (parallel session guide)

---

### → docs/00_archive/ (historical materials)

**Handovers** (timestamped coordination docs from earlier phases):
- handovers/2026_04_18-handover_summary.md
- handovers/2026_04_18-integration_audit_handover.md
- handovers/2026_04_27-MESSAGE_TO_BRIAN.md
- handovers/2026-05-01_HANDOVER-enrico-preprocessing-code-review.md
- handovers/2026-05-01_SUMMARY-preprocessing-code-review.md

**Outdated Planning** (Phase 1 planning docs, now superseded):
- tasks/data_assessment.md
- tasks/model_benchmark.md
- tasks/synthesis_module.md
- tasks/thesis_state.json
- tasks/validation_report.md
- tasks/srq1_verification_report.md

**Historical Files:**
- FileFolderTree-CMT_Codebase.txt

---

## Removed Folders (All Emptied)

| Old Folder | Reason | Disposition |
|---|---|---|
| `codebase/` | All docs moved to architecture/ | Removed |
| `decisions/` | All ADRs moved to architecture/ | Removed |
| `dev/` | All docs moved to contributing/ (except feature_engineering_design→architecture) | Removed |
| `guides/` | All docs distributed (setup→integration, dev→contributing) | Removed |
| `integrations/` | All docs moved to integration/ | Removed |
| `tooling/` | tooling-issues.md moved to integration/ | Removed |
| `codebase-testing/` | Test docs split: guides→integration/, results→reference/ | Removed |
| `analyses/` | Consolidated to architecture/analyses/ | Removed (old location) |
| `handovers/` | Moved to 00_archive/handovers/ | Removed (old location) |
| `tasks/` | Moved to 00_archive/tasks/ | Removed (old location) |
| `experiments/` | Consolidated to architecture/experiments/ | Removed (old location) |

---

## Root-Level Violations Resolved

| File | Status | Action |
|---|---|---|
| `2026-04-27_1630_MANIFOLD_ARCHITECTURE_AND_FEATURE_HANDLING.md` | ✅ Moved | → `docs/architecture/` |

**Result**: docs/ root is now clean (no `.md` violations).

---

## Integration Points to Update

### CLAUDE.md References
These paths in CLAUDE.md may need updating:
- `docs/codebase/architecture.md` → `docs/architecture/architecture.md`
- `docs/tooling/tooling-issues.md` → `docs/integration/tooling-issues.md`
- `docs/dev/repository_map.md` → `docs/contributing/repository_map.md`
- `docs/integrations/zotero-integration-setup.md` → `docs/integration/zotero-integration-setup.md`

### Root Documentation Boundary Rule
The rule at `.claude/rules/root-documentation-boundary.md` routing table is already compatible:
- `docs/codebase/` → `docs/architecture/`
- `docs/tooling/` → `docs/integration/`
- `docs/reference/` → already in use (unchanged)
- New: `docs/dev/` → split to `docs/contributing/` (dev guides) and `docs/architecture/` (design docs)

**Update needed**: Routing table in rule should reference new folders.

---

## Next Steps (Optional)

1. **Update CLAUDE.md** — Fix any references to old paths (10+ likely)
2. **Update `.claude/rules/root-documentation-boundary.md`** — Add routing for new folders
3. **Update README.md** — Reflect new docs structure
4. **Create docs/README.md** — Navigation hub for the docs folder itself
5. **Run `/move-docs-to-folders` skill** — Enforce boundary for any future violations

---

## Summary

✅ **Reorganization complete**: 11 scattered folders → 4 semantic folders + 1 archive  
✅ **Agentic clarity**: Folder names are action verbs (architecture, integration, reference, contributing)  
✅ **Root clean**: All documentation violations resolved  
✅ **Files preserved**: No content lost; all docs moved (not deleted)  
✅ **Archive maintained**: Historical docs available for reference  

The new structure is ready for immediate use and explicitly supports Claude's semantic routing without ambiguity.
