# Docs Folder Cleanup Analysis

**Date:** 2026-04-27  
**Branch:** chore/folder-cleanup  
**Objective:** Understand current state, identify references, and propose reorganization strategy

---

## Current Structure (14 folders)

| Folder | Files | Size | Purpose | Audience |
|--------|-------|------|---------|----------|
| **00_archive** | 1 | 12K | Old Zotero setup guide | Neither (archive) |
| **analyses** | 6 | 92K | Migration & analysis reports (dated 2026-04-27) | Dev/internal |
| **codebase** | 4 | 92K | Architecture, system design, experiment tracking | Mixed |
| **codebase-testing** | 6 | 80K | Test scenarios, test guides, checklists | Dev |
| **decisions** | 3 | 16K | ADRs (architecture decision records) | Dev/internal |
| **dev** | 3 | 36K | Repository map, feature design, file tree dump | Dev |
| **experiments** | 2 | 8K | Experiment registry & summary | Dev/internal |
| **guides** | 4 | 32K | Nielsen data, contributor guide, git strategy | Mixed |
| **handovers** | 3 | 52K | Handover summaries, audit reports | Internal |
| **integrations** | 12 | 148K | Zotero, Google Drive, systems architecture setup | Mixed |
| **reference** | 5 | 52K | Cheatsheet, sync guide, integrations index | User-facing |
| **tasks** | 6 | 56K | Data assessment, model benchmarks, verification | Dev/internal |
| **thesis** | 12 | 3.4M | *Mostly figures/images, should be in thesis/* | N/A (wrong place) |
| **tooling** | 1 | 12K | Tooling issues (Windows/OneDrive problems) | User-facing |

---

## Category Analysis

### **User-Facing Documentation** (What users need to work/understand the project)
- **reference/CHEATSHEET.md** — CLI commands, skills, workflows
- **reference/integrations_index.md** — Integration overview
- **guides/contributor-guide.md** — How to contribute
- **guides/git-branch-strategy.md** — Git workflow explained
- **tooling/tooling-issues.md** — Known problems & solutions
- **codebase/architecture.md** — System A/B design (frozen)
- **integrations/zotero-integration-setup.md** — Setup instructions
- **integrations/google-drive-quick-start.md** — Integration setup
- **integrations/enrico-google-drive-setup.md** — Partner setup notes

**Count:** ~9 files  
**Purpose:** Help users/collaborators understand & use the system

### **Development/Internal Documentation** (For agents, maintenance, debugging)
- **analyses/** — Migration reports, audit logs (time-stamped)
- **codebase-testing/** — Test scenarios, execution guides
- **decisions/** — ADRs (architecture decisions)
- **dev/repository_map.md** — Module inventory (referenced by rules)
- **dev/feature_engineering_design.md** — Technical design
- **experiments/** — Experiment registry & tracking
- **handovers/** — Handover summaries, audit handovers
- **tasks/** — Task descriptions (data assessment, model benchmark)
- **codebase/system-architecture-report.md** — Deep technical report
- **codebase/experiment-tracking-agent.md** — Agent-specific docs

**Count:** ~15+ files  
**Purpose:** Internal knowledge, debugging, audit trails, agent context

### **Archive** (Obsolete)
- **00_archive/zotero-setup-guide.md** — Superseded by integrations docs

---

## Current Problems

### 1. **Overmixing of Concerns**
- `guides/` contains both user docs (contributor guide) AND developer docs (git strategy)
- `codebase/` contains both user-facing (architecture.md) AND internal (experiment-tracking-agent.md)
- `integrations/` contains setup guides AND internal partner notes

### 2. **No Clear User vs Dev Boundary**
- A new user can't easily find "what do I need to know to get started?"
- An agent/developer can't easily find "where are the internal docs?"

### 3. **Misplaced Thesis Content**
- `docs/thesis/` exists and contains figures, but thesis content should live in `thesis/thesis-writing/`
- This folder is 3.4M — mostly images that probably belong in `thesis/thesis-writing/figures/`

### 4. **Too Many Small Folders**
- 14 folders for ~50 files (average 3.6 files per folder)
- Cognitive load: "where should I put/find X?"

### 5. **Stale/Temporary Content**
- `analyses/` folder contains 6 dated analysis reports (2026-04-27) that look like one-off migrations
- `handovers/` has audit handovers that may not be current
- `00_archive/` has old Zotero guide

---

## Proposed Reorganization

### **Option A: Two-Level Split (RECOMMENDED)**

```
docs/
├── user/                          ← User-facing documentation
│   ├── README.md                  # Start here (what is this project?)
│   ├── guides/                    # How-to guides
│   │   ├── setup-and-installation.md   # Initial setup
│   │   ├── git-workflow.md             # Git branch strategy
│   │   ├── contributor-guide.md        # How to contribute
│   │   └── data-access-guide.md        # Nielsen & Indeks access
│   ├── reference/                 # Quick reference materials
│   │   ├── CHEATSHEET.md               # CLI commands & skills
│   │   ├── architecture.md             # System A/B design (frozen)
│   │   ├── integrations-index.md       # Integration overview
│   │   └── troubleshooting.md          # Common issues & solutions
│   └── integrations/              # Integration setup instructions
│       ├── zotero-setup.md
│       ├── google-drive-setup.md
│       └── mcp-integration.md
│
├── dev/                           ← Development/internal documentation
│   ├── README.md                  # Developer onboarding
│   ├── architecture/              # Technical deep dives
│   │   ├── system-architecture-report.md
│   │   ├── experiment-tracking-agent.md
│   │   └── feature-engineering-design.md
│   ├── decisions/                 # ADRs (why we made certain choices)
│   │   ├── adr-001-template-strategy.md
│   │   ├── adr-002-build-pipeline.md
│   │   └── adr-003-builder-agent.md
│   ├── testing/                   # Test scenarios & guides
│   │   ├── test-execution-checklist.md
│   │   ├── pre-sync-test-guide.md
│   │   └── agent-system-test-scenarios.md
│   ├── audit/                     # Audit trails & handovers
│   │   ├── 2026-04-27_integration_audit.md
│   │   ├── 2026-04-27_migration_summary.md
│   │   └── migration-executive-summary.md
│   ├── experiments/               # Experiment tracking
│   │   ├── experiment_registry.json
│   │   └── experiment_summary.md
│   ├── repository_map.md          # Module inventory (HIGH VALUE - referenced by rules)
│   ├── tooling-issues.md          # Windows/OneDrive problems (or move to user/reference/troubleshooting)
│   └── dev-notes/                 # Temporary dev notes (auto-cleanup monthly)
│       └── 2026-04-13_18-59-FileFolderTree-CMT_Codebase.txt
│
└── archive/                       ← Deprecated/old docs (readonly)
    └── zotero-setup-guide.md.old
```

**Benefits:**
- ✅ Clear: `/user/` = what I need to know; `/dev/` = internal/agent docs
- ✅ User onboarding: start with `/user/README.md`
- ✅ Developer onboarding: start with `/dev/README.md`
- ✅ Atomic folders (each has a clear purpose)
- ✅ `repository_map.md` stays prominent (referenced by rules)
- ✅ Consolidates integrations into one place

**Reorganization effort:** Medium (move ~50 files, update ~20 references)

---

### **Option B: Three-Level Split (More granular)**

```
docs/
├── user/                    # End-user docs (collaborators, thesis readers)
├── dev/                     # Developer/agent docs (internal team)
├── api/                     # API reference (for Prometheus integration)
├── archive/
```

**Pros:** Even clearer separation  
**Cons:** May be over-engineered for current project size

---

### **Option C: Keep Current + Reorganize Within** (Minimal)

```
docs/
├── 00_archive/              # (delete or move to archive/)
├── analyses/ → dev/analyses/
├── codebase/ → dev/architecture/
├── codebase-testing/ → dev/testing/
├── decisions/ → dev/decisions/
├── dev/ → dev/core/
├── experiments/ → dev/experiments/
├── guides/ → user/guides/
├── handovers/ → dev/audit/
├── integrations/ → user/integrations/
├── reference/ → user/reference/
├── tasks/ → dev/tasks/
├── thesis/ → (move to thesis/thesis-writing/)
└── tooling/ → user/reference/troubleshooting/
```

**Pros:** Minimal renaming, follows Option A structure  
**Cons:** Still leaves us with two top-level folders, but cleaner

---

## References to Update

### Critical (Used by rules/skills/main navigation)

1. **CLAUDE.md** (12 references)
   - `docs/codebase/architecture.md` → `docs/user/reference/architecture.md`
   - `docs/dev/repository_map.md` → `docs/dev/core/repository_map.md`
   - `docs/reference/cheatsheet.md` → `docs/user/reference/cheatsheet.md`
   - `docs/tooling/tooling-issues.md` → `docs/user/reference/troubleshooting.md`
   - `docs/integrations/zotero-integration-setup.md` → `docs/user/integrations/zotero.md`
   - `docs/reference/zotero-quick-reference.md` → `docs/user/integrations/zotero-quick-ref.md`
   - etc.

2. **README.md** (5 references)
   - Update links to match new structure

3. **INDEX.md** (5 references)
   - Update folder descriptions to match new structure

4. **.claude/rules/** (3 files reference `docs/`)
   - `trigger-git-commit-workflow.md`
   - `repository-map-reference.md`
   - `context-token-optimization.md`

5. **.claude/skills/** (20+ files reference `docs/`)
   - Update all skill documentation

6. **Python code** (10+ scripts reference docs/)
   - `thesis_agents/*/agents/*.py`
   - `scripts/*.py`

---

## Recommendation

### **Go with Option A: Two-Level Split (user/ + dev/)**

**Why:**
1. **Clear mental model:** "Is this for users or for developers?"
2. **Scalable:** Easy to add subfolders without confusion
3. **Aligns with project communication:** We talk about "user docs" vs "internal docs"
4. **Fixes overloading:** Separates concerns cleanly
5. **Manageable effort:** ~50 file moves + ~20 reference updates

**Not Option B:** Too granular for current project size  
**Not Option C:** Doesn't solve the core problem of ambiguity

---

## Implementation Roadmap

### Phase 1: Audit & Planning (This session)
- [x] Understand current state
- [x] Identify all references
- [x] Propose structure
- [ ] Get user approval

### Phase 2: Preparation (Next session)
- Create target structure (`docs/user/` and `docs/dev/`)
- Move files carefully
- Verify no broken references

### Phase 3: Update References
- CLAUDE.md (12 links)
- README.md (5 links)
- INDEX.md (5 links)
- Rules & skills (20+ files)
- Python code (10+ files)

### Phase 4: Cleanup
- Delete old empty folders
- Remove `docs/thesis/` (move to thesis/thesis-writing/)
- Archive stale docs

### Phase 5: Commit & Verify
- Single commit: "docs: reorganize into user/ and dev/"
- Test that all links work

---

## Questions for Brian

1. **Do you like Option A (user/ + dev/) as the split?**
2. **Should we move `docs/thesis/figures/` to `thesis/thesis-writing/figures/`** (proper location)?
3. **For tooling-issues.md:** User-facing reference or dev-internal? (I'd say user → `docs/user/reference/troubleshooting.md`)
4. **Archive strategy:** Delete old files or move to `docs/archive/`?
5. **Timing:** Do this now or defer until after model training?

