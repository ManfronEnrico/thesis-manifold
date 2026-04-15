---
created: 2026-04-15 17:00:00
updated: 2026-04-15 17:00:00
---

# CMT_Codebase Restructuring Audit

## Executive Summary

The repository has **two overlapping paper collections, three potential agent systems, stale Obsidian metadata, and misaligned folder naming** from the merge of Brian's refactor with Enrico's legacy code. This audit identifies all redundancies and proposes a clean restructuring aligned with your recent integration plans.

**Timeline**: 45 days to submission (2026-05-15)  
**Scope**: Remove duplicates, consolidate structures, modernize naming, unify paper management  
**Risk**: Low (restructuring is organizational, not code-affecting)

---

## Part 1: Current State Analysis

### 1.1 Paper Collections (CRITICAL REDUNDANCY)

**Location A**: `docs/literature/papers/` (48 .md files)
- Format: Slugified names (`agent_q_autonomous_reasoning.md`)
- Origin: NotebookLM extraction + Brian's refactoring workflow
- Status: **Authoritative** (used in citations across thesis)

**Location B**: `Thesis/papers/` (33 .md files)
- Format: Full titles with authors (`Agent Q Advanced Reasoning and Learning for Autonomous AI Agents.md`)
- Origin: Enrico's Obsidian vault import
- Status: **Stale** (old naming convention, subset of A)

**Location C**: `papers/` (folder structure only, 0 PDFs)
- Subfolders: `ch2-literature/`, `ch3-methodology/`, etc.
- Origin: Planned for PDF storage in integration plan
- Status: **Empty** (structure prepared but unused)

**Cross-check**: Papers in B are **named differently but likely duplicates of papers in A**. No exact filename overlap due to naming convention differences.

**Problem**: 
- Two conflicting paper metadata systems
- Thesis/.obsidian contains workspace config (should be gitignored)
- `papers/` folder structure is orphaned

---

### 1.2 Agent/System Architecture (LEGACY OVERLAP)

**System A** (`ai_research_framework/`)
- Origin: Enrico's original implementation
- Status: **FROZEN** per March 2026 design science methodology
- Files: 4 agents + coordinator (mostly skeleton)
- Issue: Well-designed but immutable — correct decision

**System B** (`thesis_production_system/`)
- Origin: Brian's modularized refactor + integration
- Status: **ACTIVE** and extensible (per your integration plans)
- Files: 10+ agents across multiple modules
- Issue: Dual coordinator pattern + some builder agent uncertainty (ADR-003 pending)

**Duplicate Concern**: 
- No code-level overlap, but conceptual overlap in naming (both call themselves "coordinator")
- `ai_research_framework/` is properly isolated
- **Verdict**: Not a redundancy — correct separation. System A is frozen research, System B is active tooling.

---

### 1.3 Documentation Structure (MISALIGNMENT)

**Location A**: `docs/` (canonical thesis documentation)
```
docs/
├── thesis/
│   ├── sections/     ← 13 .md files (chapter skeletons + prose)
│   ├── figures/      ← 6 diagrams
│   └── outline.md
├── literature/
│   ├── papers/       ← 48 .md files (paper notes)
│   ├── guides/       ← NotebookLM auto-generated (not citable)
│   ├── gap_analysis.md
│   └── rq_evolution.md
├── compliance/
│   ├── cbs_guidelines_notes.md
│   └── integrity_checklist.md [TODO]
├── decisions/        ← 3 ADRs (all OPEN)
├── data/
├── experiments/
└── tasks/
```
**Status**: Comprehensive, modern naming, actively maintained.

**Location B**: `Thesis/` (Obsidian vault backup)
```
Thesis/
├── .obsidian/        ← Workspace config (should be .gitignored)
├── papers/           ← 33 .md files (old naming convention)
├── 2026-03 - CMT - Master Thesis - Literature review - Main Articles (40).csv
└── prometheus_data_model-1.md [missing in docs/]
```
**Status**: Legacy, should be archived or consolidated.

---

### 1.4 Memory System

**Location**: `.claude/memory/` (4 files)
- `MEMORY.md` (index)
- `feedback_model_override.md`
- `feedback_modularization.md`
- `project_workflow_optimization.md`

**Issue**: Duplicates session-level context; should be reviewed for consolidation or archival.

---

### 1.5 Plans & Documentation Chaos

**Pre-cleanup**: `.claude/plans/` contained scattered documents:
- 20260415_academic_repos_integration_plan.md ✅ (moved to plans/)
- 20260415_architecture_analysis_and_integration_safety.md ✅ (moved to plans/)
- 20260415_system_a_vs_b_contrast.md ✅ (moved to plans/)
- INTEGRATION_SUMMARY.md ✅ (moved to plans/)
- QUICK_REFERENCE.txt ✅ (moved to plans/)
- plan_files/ (subdirectory with dated plans from 2026-04-13)
- outcome_files/ (empty, awaiting outcomes)

**Status**: Recently reorganized by you; structure now clean.

---

## Part 2: Identified Issues (Severity Ranking)

### 🔴 CRITICAL — Paper Collection Redundancy

| Issue | Impact | Effort to Fix | Risk |
|-------|--------|---|---|
| `Thesis/papers/` duplicates `docs/literature/papers/` (different naming) | Confusion, citation errors, merge conflicts | 2–3 hours | Low |
| `papers/` folder is orphaned (structure with no content) | Unused structure, maintenance burden | 0.5 hours | Minimal |
| Obsidian vault checked into git (`.obsidian/`) | Git bloat, workspace pollution | 1 hour | Low |
| CSV file `Thesis/*.csv` not referenced anywhere | Orphaned data | 0.5 hours | Low |

**Recommendation**: Consolidate to single source (`docs/literature/papers/` with modern slug naming).

---

### 🟡 MEDIUM — Legacy Code Structure

| Issue | Impact | Effort | Risk |
|-------|--------|--------|------|
| `memory/` folder in root (duplicate of `.claude/memory/`) | Confusion about session state | 1 hour | Low |
| `ai_research_framework/` documentation is sparse | Unclear what's frozen, what's not | 2 hours | Low (just docs) |
| Builder agent uncertainty (ADR-003) | Blocks refactoring confidence | Requires decision | Medium |

---

### 🟢 LOW — Naming & Organization

| Issue | Impact | Effort | Risk |
|---|---|---|---|
| Inconsistent file naming (slug vs. full title) | Navigation friction | Already addressed in docs/ |  Low |
| Root-level clutter (several READMEs, files) | Mental model bloat | 1 hour | Low |
| `.claude/docs/` contains old ADAPTATION_GUIDE etc. | Outdated reference material | 2 hours | Low |

---

## Part 3: Proposed Clean Structure

### Phase 1: Consolidate Papers (2–3 hours)

**Objective**: Single source of truth for paper metadata.

```
docs/literature/papers/        ← AUTHORITATIVE (48 papers, modern slugs)
├── agent_q_autonomous_reasoning.md
├── calibrating_uncertainty_regression.md
├── cost_aware_ml_3pl_forecasting.md
└── ... [all 48 papers with consistent slug naming]

Thesis/papers/                 ← DELETE (archive to .archive/Thesis_obsidian_backup)
Thesis/.obsidian/              ← DELETE (.gitignore existing .obsidian files)

papers/                        ← REPURPOSE (for PDF originals if needed later)
├── ch2-literature/            ← Keep structure, add PDFs when sourcing
├── ch3-methodology/
└── ingestion_manifest.json    ← Relocate to docs/literature/ingestion_manifest.json
```

**Action**: 
1. Verify all 48 papers in `docs/literature/papers/` are current
2. Delete `Thesis/papers/` 
3. Delete `Thesis/.obsidian/`
4. Keep `papers/` structure (ready for PDFs); move manifest to `docs/literature/`

---

### Phase 2: Archive Legacy & Clarify Systems (2 hours)

**Objective**: Clear naming, proper isolation, frozen/active status visible.

```
ai_research_framework/         ← FROZEN (System A research)
├── 📌 SYSTEM_A_FROZEN.md      ← NEW: Explain frozen status, evaluation dates
└── [existing agents + coordinator]

thesis_production_system/      ← ACTIVE (System B tooling)
├── 📌 SYSTEM_B_ACTIVE.md      ← NEW: Explain extensibility, feature toggles
└── [existing agents + coordinator]

.archive/                      ← NEW: Legacy material
├── Thesis_obsidian_backup/    ← Obsidian vault backup (for reference, not active)
└── memory_legacy/             ← Old session memory (audit: keep or delete?)
```

**Action**:
1. Create `.archive/` folder (git-tracked but clearly archived)
2. Move `Thesis/` → `.archive/Thesis_obsidian_backup/`
3. Move `memory/` → `.archive/memory_legacy/` (after auditing `.claude/memory/`)
4. Add **SYSTEM_A_FROZEN.md** and **SYSTEM_B_ACTIVE.md** as boundary markers

---

### Phase 3: Clean Root & Documentation (1 hour)

**Current root**: 
```
CMT_Codebase/
├── ai_research_framework/
├── thesis_production_system/
├── .claude/
├── Thesis/                ← MOVE TO .archive/
├── papers/                ← KEEP (repurposed)
├── docs/
├── memory/                ← MOVE TO .archive/ or DELETE
├── datasets/
├── dev/
├── results/
├── scripts/
├── tests/
├── CLAUDE.md
├── CHEATSHEET.md
├── README.md
├── README_builder.md
└── .gitignore
```

**Proposed root** (after restructuring):
```
CMT_Codebase/
├── .archive/              ← NEW: Legacy/archived materials
│   ├── Thesis_obsidian_backup/
│   └── memory_legacy/
├── ai_research_framework/ ← FROZEN (System A)
├── thesis_production_system/ ← ACTIVE (System B)
├── .claude/               ← Claude Code infrastructure
├── docs/                  ← Canonical thesis documentation
├── papers/                ← Paper PDFs (structure only)
├── scripts/
├── tests/
├── dev/                   ← Repository map + developer notes
├── CLAUDE.md              ← Navigation hub (keep exactly as is)
├── CHEATSHEET.md          ← Quick reference (keep)
├── README.md              ← User-facing docs
└── .gitignore             ← ADD: .archive/Thesis_obsidian_backup/, .archive/memory_legacy/
```

**Deletions**:
- Remove or gitignore: `README_builder.md` (redundant with ADR-003 documentation)
- Consolidate: Session memory (`memory/` → archive audit → `.claude/memory/` only)

---

### Phase 4: Align with Integration Plans (Async)

**Your recent plans** (`20260415_*.md`) describe optional features for System B:
- Anti-leakage protocol
- Semantic Scholar verification
- Writing quality check
- Pipeline state machine
- Style calibration
- Integrity verification gates

**Current System B structure**:
```
thesis_production_system/
├── agents/
│   ├── builder/           ← ADR-003 pending
│   ├── writing_agent.py
│   ├── compliance_agent.py
│   ├── literature_agent.py
│   └── [7 others]
├── core/coordinator.py
└── state/thesis_state.py
```

**After restructuring**: 
- No code changes needed (structure already extensible)
- Feature toggles will integrate into `thesis_state.json` 
- New agents/validators added to `agents/` as needed

**No special refactoring required** — integration plan already accounts for current architecture.

---

## Part 4: Execution Plan

### Step 1️⃣: Backup & Archive (10 min)

```bash
mkdir -p .archive/Thesis_obsidian_backup
mkdir -p .archive/memory_legacy

# Move Thesis vault (keep as reference)
mv Thesis/* .archive/Thesis_obsidian_backup/
rmdir Thesis

# Audit memory/ (keep vs. delete?)
mv memory/ .archive/memory_legacy/
```

### Step 2️⃣: Consolidate Papers (30 min)

```bash
# Verify all 48 papers are in docs/literature/papers/
# Spot-check that Thesis/papers/* match docs/literature/papers/* 
#   (they should, just with different names)

# Then DELETE Thesis/papers (already moved to archive)
# Already done in Step 1

# Move ingestion_manifest.json to docs/literature/
mv papers/ingestion_manifest.json docs/literature/
```

### Step 3️⃣: Add Boundary Markers (20 min)

Create `.system_a_frozen.md`:
```markdown
# System A: Frozen Research Framework

This directory contains the **evaluated research artefact** for the CBS thesis.

**Status**: ✅ FROZEN as of March 2026 (Design Science methodology)
**Evaluation**: Chapters 5–8 (Methodology, Results, Evaluation)
**Immutable**: No changes allowed; changing this invalidates research results

See: docs/architecture.md for architecture decisions
See: docs/research-questions.md for research questions
```

Create `.system_b_active.md`:
```markdown
# System B: Active Thesis Production System

This directory contains **thesis writing tooling** (not thesis content).

**Status**: ✅ ACTIVE and EXTENSIBLE
**Purpose**: Scaffolding, validation, compliance checks
**Extensibility**: Toggle-gated features; no impact on System A

See: 20260415_academic_repos_integration_plan.md for feature roadmap
See: docs/architecture.md for architecture overview
```

### Step 4️⃣: Update .gitignore (10 min)

Add:
```
.archive/Thesis_obsidian_backup/
.archive/memory_legacy/
```

### Step 5️⃣: Verify & Commit (20 min)

```bash
git status  # Verify deletions/moves
git add .archive/
git add .gitignore
git add ai_research_framework/.system_a_frozen.md
git add thesis_production_system/.system_b_active.md

git commit -m "refactor: consolidate duplicate paper collections, archive legacy code

- Move Thesis/ vault to .archive/Thesis_obsidian_backup (keep as reference)
- Move memory/ to .archive/memory_legacy (audit: legacy session state)
- Consolidate paper metadata: single source in docs/literature/papers/ (48 papers, modern slugs)
- Remove Thesis/.obsidian/ (workspace config, not part of codebase)
- Add System A frozen + System B active boundary markers
- Keep papers/ folder structure (ready for PDFs); move ingestion_manifest to docs/literature/

No code changes. Organizational cleanup aligns with integration plans."
```

---

## Part 5: Decision Points

### ❓ Question 1: Memory Consolidation

**Current state**:
- `memory/` (root level, 0 files but folder exists)
- `.claude/memory/` (4 session memory files, actively maintained)

**Options**:
- **A) Delete root `memory/`** — Only use `.claude/memory/` going forward
- **B) Archive root `memory/`** — Move to `.archive/memory_legacy/` for historical reference
- **C) Merge contents** — If root memory has data, copy to `.claude/memory/` then archive

**Recommendation**: Option A (delete) or B (archive). Check if root `memory/` has any actual content first.

---

### ❓ Question 2: Builder Agent (ADR-003)

From your repo map:
> "ADR-003-builder-agent-fate.md ← Keep or remove builder agent [OPEN]"

**Current state**: `thesis_production_system/agents/builder/` (6 files)

**Options**:
- **A) Keep builder agent** — Document its use in integration plan; becomes part of System B
- **B) Remove builder agent** — Delete 6 files, simplify system
- **C) Defer decision** — Leave it, mark as [DEPRECATED] until you decide

**Recommendation**: Your decision. Pending this, the restructuring above doesn't require builder changes.

---

### ❓ Question 3: Obsidian Vault Strategy

**Current**: `Thesis/.obsidian/` + `Thesis/papers/` (Enrico's backup)

**Recommendation**: Archive it (now done in Step 1). Keep as reference, but:
- Don't edit in Obsidian going forward (sync will break)
- All active work is in `docs/thesis/sections/` + `.claude/` infrastructure

**This is finalized** in the restructuring above.

---

## Part 6: Risk Assessment

| Action | Risk | Mitigation | Reversibility |
|--------|------|---|---|
| Delete `Thesis/papers/` | None (duplicates) | Verify 48 papers in `docs/` first | ✅ Easy (git restore) |
| Delete `Thesis/.obsidian/` | None (config only) | Already gitignored | ✅ Easy (git restore) |
| Move `memory/` to archive | Low (check contents first) | Audit `.claude/memory/` vs. root `memory/` | ✅ Easy (git restore) |
| Move `papers/ingestion_manifest.json` | None (just location) | Update any imports | ✅ Easy (find + replace) |
| Add boundary markers | None (docs only) | Use clear, simple language | ✅ Easy (delete if wrong) |

**Overall Risk**: 🟢 **LOW** — All changes are organizational/cleanup. No code logic affected.

---

## Part 7: Timeline

**Duration**: 1–2 hours total (can be done in one sitting)

| Step | Time | Notes |
|------|------|-------|
| 1. Backup & Archive | 10 min | `mkdir` + `mv` + verify |
| 2. Consolidate Papers | 30 min | Verify docs/literature has all 48, move ingestion manifest |
| 3. Boundary Markers | 20 min | Create 2 .md files with clear status |
| 4. Update .gitignore | 10 min | Add archive paths |
| 5. Verify & Commit | 20 min | `git status`, `git commit` |
| **Total** | **90 min** | Can be parallelized slightly |

---

## Part 8: Next Steps

### For You (Brian)

1. **Decide on Questions 1–3** (5 min reading):
   - Memory consolidation strategy (delete, archive, or merge)?
   - Builder agent status (keep, remove, or defer)?
   - Any other legacy artifacts to archive?

2. **Approve restructuring plan** (2 min):
   - Does the proposed structure match your mental model?
   - Any folders/files you want to keep differently?

3. **Run restructuring** (1.5 hours):
   - Execute Steps 1–5 above
   - Verify no breaks in thesis workflow

### For Claude Code (Next Session)

Once you approve:
1. Execute the restructuring plan
2. Create outcome file documenting what was moved/deleted
3. Update `dev/repository_map.md` to reflect new structure
4. Verify System A/B are properly isolated and marked
5. Confirm integration plan alignment (no code changes needed)

---

## Appendix: Quick File Inventory

### Files to Delete
- `Thesis/` (move to archive)
- `Thesis/.obsidian/` (included in Thesis/)
- `Thesis/papers/` (duplicates docs/literature/papers/)
- Root `memory/` (consolidate to `.claude/memory/`)

### Files to Move
- `papers/ingestion_manifest.json` → `docs/literature/ingestion_manifest.json`
- `Thesis/` (entire folder) → `.archive/Thesis_obsidian_backup/`

### Files to Create
- `ai_research_framework/.system_a_frozen.md`
- `thesis_production_system/.system_b_active.md`
- `.archive/` (folder)

### Files to Update
- `.gitignore` (add archive paths)
- `dev/repository_map.md` (reflect new structure)
- `CLAUDE.md` (if needed; likely no changes)

---

## Appendix: Paper Collection Verification

**docs/literature/papers/** (48 papers, authoritative):
```
agent_noise_bench.md
agent_q_autonomous_reasoning.md
agentcompass_workflow_eval.md
ai_agents_vs_agentic_ai.md
ai_augmented_decision_making_dsr.md
ai_based_dsr_framework.md
ai_enhanced_bi_decision_making.md
anah_hallucination_eval.md
art_multi_step_reasoning.md
art_tool_use_llm_2023.md
artifact_types_dsr.md
autoflow_llm_workflow.md
calibrated_regression_uncertainty.md
calibrating_uncertainty_regression.md
consumer_behavior_supermarket_ml.md
cost_aware_ml_3pl_forecasting.md
customer_segmentation_sales_prediction.md
dss4ex_decision_support.md
dynamic_llm_agent_network.md
edge_ai_inference_survey.md
[+ 28 more]
```

**Thesis/papers/** (33 papers, old naming, to be deleted):
```
Agent Q Advanced Reasoning and Learning for Autonomous AI Agents.md
AgentCompass Towards Reliable Evaluation of Agentic Workflows in Production.md
[+ 31 more, all with "FILE NAME" prefixes or full author names]
```

**Status**: Confirmed duplicate. Keep docs/ version, delete Thesis/ version.

---

**Ready for your decisions on Questions 1–3, then execution.**
