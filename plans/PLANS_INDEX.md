# Plans Index — Organization & Status

Last updated: 2026-04-28

---

## Structure

Plans are organized into four folders based on their lifecycle:

```
plans/
├── 01-backlog-plans/           (4 plans) — Early analysis, not started
├── 02-in_progress-plans/       (9 plans) — Active work, partial progress
├── 03-outcome_plans/           (4 plans) — ✅ Completed, outcomes documented
└── 04-archive_plans/           (0 plans) — Deprecated or superseded
```

---

## 📋 BACKLOG — Analysis Only (4 plans)

**Status**: No implementation yet. Strategic exploration and decision-making.

| Plan | Created | Purpose | Next Step |
|------|---------|---------|-----------|
| **CMT_Codebase Master Upgrade** | 2026-04-13 | Synthesize forked repos + PTA best-practices into roadmap | Review, decide adoption level |
| **NotebookLM Integration** | 2026-04-13 | Evaluate NotebookLM API for literature grounding | Pilot phase (post-deadline suggested) |
| **PTA Best-Practices Extraction** | 2026-04-13 | Extract Claude Code patterns from reference project | Apply learnings to thesis-manifold |
| **Thesis Repo Upgrade** | 2026-04-13 | LaTeX pipeline, integrity gates, skill modularity | Integrate Phase 2+3 findings |

**Recommendation**: These are well-researched but require resourcing decisions. Review after Jupyter path cleanup completes.

---

## 🔄 IN PROGRESS — Active Work (9 plans)

**Status**: Started, partially executed, or awaiting next phase.

| Plan | Created | Status | Blocker |
|------|---------|--------|---------|
| **Jupyter Notebook Path Centralization** | 2026-04-27 | Phase 1 done (config.py), Phase 2 in progress (notebook refactor) | Merge main after completion |
| **System A Feature-Eng Integration** | 2026-04-23 | Analysis complete, awaiting Enrico's next PR | Data access unblocked 2026-04-22 |
| **ML Retraining with New Skills** | 2026-04-16 | Approved structure, awaiting operational decisions | Budget/timeline constraints |
| **Integration Phase 1: State Extension** | 2026-04-15 | Ready to implement, infrastructure designed | No blockers |
| **Academic Repos Integration** | 2026-04-15 | Optional enhancements, toggleable features designed | Resource allocation |
| **Architecture Analysis & Safety** | 2026-04-15 | Complete, integration is safe | Awaiting phase 1 completion |
| **Integration Summary** | 2026-04-15 | Decision framework documented | Scenario choice (baseline / standard / full) |
| **Session Progress** | 2026-04-15 | Snapshot from that session | Historical reference |
| **System A vs B Contrast** | 2026-04-15 | Reference document, no action needed | N/A |

**Recommendation**: 
- **Priority now**: Complete Jupyter path cleanup (Phase 2 + Phase 3 validation)
- **Quick win**: Integration Phase 1 (state extension infrastructure)
- **Defer**: ML retraining, academic repos integration (post-Phase-5 eval)

---

## ✅ OUTCOMES — Completed (4 plans)

**Status**: ✅ Done. Outcomes documented and lessons learned captured.

| Plan | Completed | What Was Done | Outcome |
|------|-----------|---------------|---------|
| **Integration Phase 1: State Extension** | 2026-04-15 | Extended ThesisState + ComplianceState with toggleable features | ✅ Infrastructure ready |
| **Restructuring Audit** | 2026-04-15 | Consolidated papers, archived legacy, added System A/B markers | ✅ Repo cleaned, ready for next phase |
| **Integration Audit & Handover** | 2026-04-18 | Audited Zotero, Google Drive, NotebookLM integrations | ✅ 3 systems operational, documented |
| **Nielsen Pipeline + Agent Paths** | 2026-04-22 | Fixed data connectors, migrated agents to local CSV paths, cleaned hooks | ✅ Data pipeline unblocked |

**Lessons Learned**: See each outcome file for "Adjusted" sections.

---

## 📦 ARCHIVE — Deprecated (0 plans)

(Currently empty. Plans move here when superseded or after 60 days with no progress.)

---

## How to Use This Index

**Starting a session?**
1. Check 02-in_progress-plans/ for current priorities
2. Read the relevant plan's "Next Steps" section
3. Update status when work completes

**Plan completed?**
1. Create outcome file in 03-outcome_plans/
2. Move plan from 02 → 04-archive_plans/ (optional, or leave for reference)
3. Update this index

**Plan decision deferred?**
1. Move from 01-backlog to 02-in_progress when work starts
2. Add blocker/notes in this index

**Plan superseded?**
1. Move to 04-archive_plans/
2. Note reason in this index

---

## Current Priority (2026-04-28)

**🎯 Focus**: Jupyter notebook path centralization (Phase 2 + 3)
- **Duration**: 2–4 hours
- **Blocker for merge**: Don't pull main until this completes
- **After completion**: Create outcome file, then revisit Phase 1 state extension

---

## Contact

For questions on plan strategy: See CLAUDE.md → Workflows section
