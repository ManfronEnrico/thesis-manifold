# Documentation — Manifold AI Thesis

Quick navigation for the four-folder documentation structure.

---

## 📚 Four Core Folders

### 🏗️ [architecture/](architecture/) — System Design & Patterns

**What**: WHAT the system is — architectural decisions, design patterns, agent roles, research framework.

**Contains:**
- System A/B architecture & design rationale
- Architectural Decision Records (ADRs)
- Feature engineering design
- Experiment tracking metadata
- Supporting: `analyses/` (timestamped migration studies), `experiments/` (experiment registry)

**Use when**: You need to understand **how the system is designed** or **what architectural decisions were made**.

**Quick links:**
- [System Architecture](architecture/system-architecture-report.md)
- [Framework Design](architecture/architecture.md)
- [ADR Index](architecture/) (browse `adr_*.md` files)

---

### 🔌 [integration/](integration/) — Setup, Integration & Tooling

**What**: HOW to set up and integrate — integration guides, setup instructions, data access strategies, tooling fixes.

**Contains:**
- Third-party integration guides (Zotero, Google Drive, NotebookLM)
- Data access strategies (Nielsen, Indeks Danmark)
- Tooling issues & Windows/OneDrive workarounds
- Testing setup guides
- Agent testing scenarios

**Use when**: You need to **set something up**, **integrate a service**, or **fix a tooling problem**.

**Quick links:**
- [Zotero Setup](integration/zotero-integration-setup.md)
- [Google Drive Setup](integration/google-drive-setup.md)
- [Nielsen Data Access](integration/2026_04_20-nielsen_data_access_strategy.md)
- [Tooling Issues](integration/tooling-issues.md)
- [Testing Setup](integration/agent-system-test-scenarios.md)

---

### 📖 [reference/](reference/) — Quick Reference & Verification

**What**: WHERE to look it up — quick-reference guides, verification reports, test results, lookup tables.

**Contains:**
- Command cheatsheet
- Quick-reference guides (Zotero, testing)
- Verification & validation reports
- Test execution results
- Integration index

**Use when**: You need a **quick lookup**, **verification proof**, or **test result**.

**Quick links:**
- [Cheatsheet](reference/CHEATSHEET.md) — commands & workflows
- [Verification Report](reference/VERIFICATION_REPORT.md) — docs audit
- [Testing Quick-Ref](reference/testing-quick-reference.md)

---

### 👥 [contributing/](contributing/) — Developer Guide & Workflow

**What**: HOW to work here — developer guide, repository structure, git strategy, branching workflow.

**Contains:**
- Repository map (file-to-purpose mapping)
- Contributor setup guide
- Git branch strategy & naming conventions
- Worktree guide for parallel sessions

**Use when**: You're setting up **your development environment**, need **git workflow rules**, or want to understand **repository structure**.

**Quick links:**
- [Repository Map](contributing/repository_map.md) — file locations
- [Contributor Guide](contributing/contributor-guide.md) — setup
- [Git Strategy](contributing/git-branch-strategy.md) — branching rules
- [Worktree Guide](contributing/git-worktrees-and-parallel-sessions.md) — parallel sessions

---

## 📦 Archive

### [00_archive/](../docs/00_archive/) — Historical Materials

**What**: Historical reference — completed plans, old phases, superseded docs, legacy materials.

**Contains:**
- `handovers/` — coordination docs from earlier phases
- `tasks/` — outdated planning checklists
- `thesis/analysis/` — legacy analysis notebooks
- Other archived materials

**Use when**: You need **historical context** or want to **review past work**.

---

## 🎯 Agentic Routing (For Claude)

When Claude saves a document, it uses **semantic folder names**:

| Document Type | Folder | Semantic Signal |
|---|---|---|
| Design, architecture, ADR, pattern | `architecture/` | "WHAT the system is" |
| Setup, integration, guide, tooling, config | `integration/` | "HOW to set up/integrate" |
| Quick-ref, verification, test, audit, lookup | `reference/` | "WHERE to look it up" |
| Developer, repo, git, contribute, workflow | `contributing/` | "HOW to work here" |

**Zero ambiguity**: Folder names are action verbs. Claude matches intent directly to folder.

---

## 📋 Related Documentation

- **CLAUDE.md** — Project instructions & workflows (entry point)
- **ROOT** — `.claude/rules/root-documentation-boundary.md` — root file restrictions
- **PLANS** — `plans/PLANS_INDEX.md` — all plans by P-ID and status

---

## ✨ Last Updated

2026-05-04 — Documentation reorganization complete (P0021)  
Original structure: 11 folders → Path A: 4 semantic folders + 1 archive

For details, see: [P0021 Outcome](../plans/03-outcome_plans/P0021_2026-05-04_1400_OUTCOME-docs-reorganization/)
