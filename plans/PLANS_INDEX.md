# Plans Index — 8-Status Workflow (2026-05-07+)

All plans are organized by status bucket and identified by unique P-ID for easy reference and tracking. **Status is maintained in plan frontmatter only** (no duplicate outcome files).

---

## 📋 Index Format

Each plan uses the naming convention: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}`

- **P{NNNN}**: Unique sequential plan identifier (e.g., P0001)
- **YYYY-MM-DD**: Plan creation date (ISO format)
- **HHMM**: Plan creation time (24-hour format, 0800 default for undated)
- **{slug}**: Descriptive slug (lowercase, hyphens)

**Status Fields** (in plan frontmatter):
- `status`: Current status (Backlog, In Progress, Focus, Complete, Blocked, Paused, Cancelled, Archived)
- `created`: Creation timestamp
- `updated`: Last update timestamp
- Additional fields per status (e.g., `focus_detail`, `blocked_reason`, `paused_reason`, `outcome_summary`)

---

## 🎯 01. Backlog Plans

Not yet started. Awaiting prioritization or upstream completion.

| ID | Date | Plan | Status in Frontmatter |
|---|---|---|---|
| **P0001** | 2026-04-13 | CMT Master Upgrade | Backlog |
| **P0002** | 2026-04-13 | NotebookLM Integration | Backlog |
| **P0003** | 2026-04-13 | PTA Best Practices Extraction | Backlog |
| **P0004** | 2026-04-13 | Thesis Repository Upgrade | Backlog |
| **P0018** | 2026-04-28 | Restructure Existing Plans | Backlog |

---

## 🚀 02. In-Progress Plans

Active work, not currently highlighted as focus.

| ID | Date | Plan | Status in Frontmatter |
|---|---|---|---|
| (None currently) | — | — | — |

---

## ✨ 03. Focus Plans

Top priority. Actively worked on this session. Next steps defined.

| ID | Date | Plan | Phase/Detail |
|---|---|---|---|
| **P0022** | 2026-05-07 | Preprocessing Pipeline Modularization | Phase 1 Complete & Verified ✅ — Phase 2 Ready (replicate CSD for 4 categories: 3 hrs) |

---

## ✅ 04. Complete Plans

Completed. Outcome tracked in frontmatter `outcome_summary` field. All supporting docs bundled in plan folder.

| ID | Date | Plan | Outcome Summary |
|---|---|---|---|
| **P0006** | 2026-04-15 | Integration Phase 1 Execution | ✅ Phase 1 extended with material_gaps, toggles, chapter_states, style_profile |
| **P0007** | 2026-04-15 | Restructuring Audit | ✅ Audit complete; P-ID system defined and implemented |
| **P0008** | 2026-04-18 | Integration Three Systems | ✅ All 3 systems integrated; System A/B test passes; standalone preprocessing identified |
| **P0009** | 2026-04-22 | Nielsen Pipeline & Agent Paths | ✅ Nielsen data access + path routing verified; preprocessing.py paths fixed |
| **P0018** | 2026-04-28 | Restructure Existing Plans | ✅ Plans migrated to P-ID folder structure with status-based buckets (01-08) |

---

## 🚧 05. Blocked Plans

Awaiting external decision or dependency. Unblock condition defined in frontmatter `blocked_reason`.

| ID | Date | Plan | Blocked Reason |
|---|---|---|---|
| **P0005** | 2026-04-23 | System A Feature Eng Integration | Awaiting decision: Option A (parents[2]→parents[3], 5min) vs Option B (add __init__.py, 30min, cleaner) |
| **P0017** | 2026-04-27 | Jupyter Notebook Path Centralization | Awaiting P0022 Phase 2 completion (stable parquet outputs across all 5 categories) |

---

## ⏸ 06. Paused Plans

Intentionally paused. Resume condition defined in frontmatter `paused_reason` and `dependencies`.

| ID | Date | Plan | Paused Reason | Depends On |
|---|---|---|---|---|
| **P0019** | 2026-05-04 | Root Documentation Boundary & Folder Cleanup | Lower priority infrastructure work (rule + skill); paused pending P0022 completion | P0022 |
| **P0020** | 2026-05-04 | Rule System Reform | Waiting for P0019 Phase 4 (root-documentation-boundary rule + /move-docs-to-folders skill) | P0019 |

**Note**: P0021 (Docs Reorganization) was completed and archived. Work for future doc organization improvements tracked in plan status notes.

---

## ❌ 07. Cancelled Plans

No longer needed. Cancellation reason tracked in frontmatter.

(None currently)

---

## 📦 08. Archived Plans

Old/legacy plans. Preserved for historical reference. No ongoing work.

| ID | Date | Plan | Archive Reason |
|---|---|---|---|
| **P0010** | 2026-04-15 | Academic Repos Integration | Superseded by System A/B architecture |
| **P0011** | 2026-04-15 | Architecture Analysis & Integration Safety | Archived after architecture decision |
| **P0012** | 2026-04-15 | Integration Phase 1 State Extension | Archived after completion; work continued in P0020 |
| **P0013** | 2026-04-15 | Integration Summary | Archived after consolidation |
| **P0014** | 2026-04-15 | Session Progress | Archived after session close |
| **P0015** | 2026-04-15 | System A vs B Contrast | Archived after architecture finalized |
| **P0016** | 2026-04-16 | ML Retraining with New Skills | Archived; pending new feature request |

---

## 📊 Summary

- **Total Plans**: 22 tracked
  - Backlog: 5 (P0001–P0004, P0018)
  - In Progress: 0
  - Focus: 1 (P0022)
  - Complete: 5 (P0006–P0009, P0018)
  - Blocked: 2 (P0005, P0017)
  - Paused: 2 (P0019, P0020)
  - Cancelled: 0
  - Archived: 7 (P0010–P0016)

**Note**: P0021 was completed and merged into broader doc reorganization (no separate folder)

---

## 🔍 Quick Reference

### By Date (Chronological)

**2026-04-13**: P0001, P0002, P0003, P0004  
**2026-04-15**: P0006, P0007, P0010, P0011, P0012, P0013, P0014, P0015  
**2026-04-16**: P0016  
**2026-04-18**: P0008  
**2026-04-22**: P0009  
**2026-04-23**: P0005  
**2026-04-27**: P0017  
**2026-04-28**: P0018  
**2026-05-04**: P0019, P0020, P0021  
**2026-05-07**: P0022  

### By Status

**Backlog**: P0001, P0002, P0003, P0004, P0018  
**Focus**: P0022  
**Complete**: P0006, P0007, P0008, P0009, P0018  
**Blocked**: P0005, P0017  
**Paused**: P0019, P0020  
**Archived**: P0010, P0011, P0012, P0013, P0014, P0015, P0016  
**Retired/Merged**: P0021 (completed, no separate folder)  

---

## 📝 Accessing Plans

All plans are located in their status bucket:

```
plans/
  01-backlog_plans/           (5 plans)
    P0001_2026-04-13_0800_PLAN-cmt-master-upgrade/
      P0001_2026-04-13_0800_PLAN-cmt-master-upgrade.md
    ... (P0002–P0004, P0018)

  02-in_progress_plans/       (0 plans)

  03-focus_plans/             (1 plan)
    P0022_2026-05-07_1000_PLAN-preprocessing-pipeline-modularization/
      P0022_2026-05-07_1000_PLAN-preprocessing-pipeline-modularization.md
      2026-05-07_DOC-fixes-and-next-steps.md
      2026-05-07_DOC-phase1-csd-completion.md
      2026-05-07_DOC-task-summary.md

  04-complete_plans/          (7 plans)
    P0006_2026-04-15_0800_PLAN-integration-phase1-execution/
      P0006_2026-04-15_0800_PLAN-integration-phase1-execution.md
    ... (P0007–P0009, P0018, P0020, P0021)

  05-blocked_plans/                 (2 plans)
    P0005_2026-04-23_0800_PLAN-system-a-feature-eng-integration/
      P0005_2026-04-23_0800_PLAN-system-a-feature-eng-integration.md
    P0017_2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/
      P0017_2026-04-27_1420_PLAN-jupyter_notebook_path_centralization.md
      2026-04-28_DOC-*.md (supporting docs)

  06-paused_plans/                  (2 plans)
    P0019_2026-05-04_1400_PLAN-root-documentation-boundary-and-folder-cleanup/
      P0019_2026-05-04_1400_PLAN-preprocessing-unification.md
      2026-05-04_DOC-*.md (supporting docs)
    P0020_2026-05-04_1430_PLAN-rule-system-reform/
      P0020_2026-05-04_1430_PLAN-rule-system-reform.md

  07-cancelled_plans/               (0 plans)

  08-archived_plans/          (7 plans)
    P0010_2026-04-15_0800_PLAN-academic-repos-integration/
      P0010_2026-04-15_0800_PLAN-academic-repos-integration.md
    ... (P0011–P0016)
```

---

**Last Updated**: 2026-05-07 16:25 (Session reorg: P0022 verified complete, P0017→blocked, P0019→paused + renamed)  
**Status Tracking**: All status maintained in plan `.md` frontmatter (no duplicate outcome files)
