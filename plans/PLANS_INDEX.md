# Plans Index

All plans are organized by status bucket and identified by unique P-ID for easy reference and tracking.

---

## 📋 Index Format

Each plan uses the naming convention: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}`

- **P{NNNN}**: Unique sequential plan identifier (e.g., P0001)
- **YYYY-MM-DD**: Plan creation date (ISO format)
- **HHMM**: Plan creation time (24-hour format, 0800 default for undated)
- **{slug}**: Descriptive slug (lowercase, hyphens)

---

## 🎯 Backlog Plans (01-backlog-plans/)

| ID | Date | Created | Plan | Status |
|---|---|---|---|---|
| **P0001** | 2026-04-13 | 0800 | CMT Master Upgrade | Pending |
| **P0002** | 2026-04-13 | 0800 | NotebookLM Integration | Pending |
| **P0003** | 2026-04-13 | 0800 | PTA Best Practices Extraction | Pending |
| **P0004** | 2026-04-13 | 0800 | Thesis Repository Upgrade | Pending |

---

## 🚀 In-Progress Plans (02-in_progress-plans/)

| ID | Date | Created | Plan | Status |
|---|---|---|---|---|
| **P0005** | 2026-04-23 | 0800 | System A Feature Eng Integration | In Progress (DRAFT) |
| **P0017** | 2026-04-27 | 1420 | Jupyter Notebook Path Centralization | In Progress (Phase 2B) |
| **P0019** | 2026-05-04 | 1400 | Preprocessing Pipeline Unification | In Progress (Phase 4 pending) |
| **P0022** | 2026-05-07 | 1000 | Preprocessing Pipeline Modularization | In Progress (Phase 1 code ✅, fixes pending) |

---

## ✅ Outcome Plans (03-outcome_plans/)

| ID | Date | Created | Plan | Status | Outcome |
|---|---|---|---|---|---|
| **P0006** | 2026-04-15 | 0800 | Integration Phase 1 Execution | Completed | Phase 1 extended |
| **P0007** | 2026-04-15 | 0800 | Restructuring Audit | Completed | Audit done |
| **P0008** | 2026-04-18 | 0800 | Integration Three Systems | Completed | Integration verified |
| **P0009** | 2026-04-22 | 0800 | Nielsen Pipeline & Agent Paths | Completed | Data access + paths fixed |
| **P0017-OUTCOME** | 2026-04-28 | — | Jupyter Path Centralization Phase 2 | Completed | Phase 2 complete (rolled back 2026-04-30) |
| **P0020** | 2026-05-04 | 1430 | Rule System Reform | Completed | 8 phases delivered; 5 enforcement skills built; conventions consolidated |
| **P0021** | 2026-05-04 | 1400 | Docs Reorganization (11→4 folders) | Completed | 4-folder structure complete, archive organized |

---

## 📦 Archive Plans (04-archive_plans/)

| ID | Date | Created | Plan | Status |
|---|---|---|---|---|
| **P0010** | 2026-04-15 | 0800 | Academic Repos Integration | Archived |
| **P0011** | 2026-04-15 | 0800 | Architecture Analysis & Integration Safety | Archived |
| **P0012** | 2026-04-15 | 0800 | Integration Phase 1 State Extension | Archived |
| **P0013** | 2026-04-15 | 0800 | Integration Summary | Archived |
| **P0014** | 2026-04-15 | 0800 | Session Progress | Archived |
| **P0015** | 2026-04-15 | 0800 | System A vs B Contrast | Archived |
| **P0016** | 2026-04-16 | 0800 | ML Retraining with New Skills | Archived |

---

## 📊 Summary

- **Total Plans**: 22
- **Backlog**: 4 (P0001–P0004)
- **In Progress**: 4 (P0005, P0017, P0019, P0022)
- **Outcomes**: 7 (P0006–P0009, P0017-OUTCOME, P0020, P0021)
- **Archive**: 7 (P0010–P0016)

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
**2026-04-28**: P0017-OUTCOME, P0018  
**2026-05-04**: P0019, P0020, P0021  
**2026-05-07**: P0022

### By Status

**Pending**: P0001, P0002, P0003, P0004  
**In Progress**: P0005, P0017, P0019, P0022  
**Completed**: P0006, P0007, P0008, P0009, P0017-OUTCOME, P0018, P0020, P0021  
**Archived**: P0010, P0011, P0012, P0013, P0014, P0015, P0016  

---

## 📝 Accessing Plans

All plans are located in their status bucket:

```
plans/
  01-backlog-plans/
    P0001_2026-04-13_0800_PLAN-cmt-master-upgrade/
      P0001_2026-04-13_0800_PLAN-cmt-master-upgrade.md
    ... (P0002–P0004)
  
  02-in_progress-plans/
    P0005_2026-04-23_0800_PLAN-system-a-feature-eng-integration/
      P0005_2026-04-23_0800_PLAN-system-a-feature-eng-integration.md
    P0017_2026-04-27_1420_PLAN-jupyter_notebook_path_centralization/
      P0017_2026-04-27_1420_PLAN-jupyter_notebook_path_centralization.md
      2026-04-28_DOC-*.md (supporting docs)
    P0018_2026-04-28_1400_PLAN-restructure_existing_plans/
      P0018_2026-04-28_1400_PLAN-restructure_existing_plans.md
  
  03-outcome_plans/
    P0006_2026-04-15_0800_PLAN-integration-phase1-execution/
      ... (etc)
  
  04-archive_plans/
    P0010_2026-04-15_0800_PLAN-academic-repos-integration/
      ... (etc)
```

---

**Last Updated**: 2026-05-04 14:45  
**Index Maintainer**: Claude Code Session  
**Notes**: P0020 created for rule system reform (based on jlacour-git framework)
