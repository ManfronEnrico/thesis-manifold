# CLAUDE.md — Manifold AI Thesis: CBS Master's 2026
> Automatically read every session. Navigation hub only.
> Full specs in linked docs and `.claude/rules/`

---

## Quick Start — Current Repo Structure

**As of 2026-07-11:** Repo restructured from `docs/thesis/` to `00_thesis_*` folders. Old `docs/` folder → `user-docs/`.

**Read these in order:**

1. [README.md](README.md) — Project overview, systems A/B
2. [00_thesis_context/formal-requirements/](00_thesis_context/formal-requirements/) — CBS compliance
3. [01_thesis_research/research-questions/](01_thesis_research/research-questions/) — RQs (v2)
4. [02_thesis_data/](02_thesis_data/) — Data folder structure & Nielsen catalog
5. [user-docs/architecture/](user-docs/architecture/) — System design docs
6. [user-docs/contributing/repository_map.md](user-docs/contributing/repository_map.md) — File locations

---

## Folder Map

| Folder | Purpose | Status |
|--------|---------|--------|
| **00_thesis_context** | Research questions, methodology, formal requirements | Active thesis |
| **01_thesis_research** | Literature review, RQ deep-dives | Active thesis |
| **02_thesis_data** | Raw/processed data, Nielsen catalog, preprocessing | Data pipeline |
| **03_thesis_modelling** | Model experiments, training scripts, results | Modeling layer |
| **04_thesis_results** | Final outputs, comparison reports | Results archive |
| **05_thesis_writing** | Thesis chapters, prose, submission artifacts | Writing phase |
| **plans/** | P-ID folder organization, session planning | Planning artifact |
| **user-docs/** | Architecture, integration, handovers, reference | Documentation |
| **.claude/rules/** | Session workflow automation | Governance |
| **utility_scripts/** | Helper scripts for data/setup | Utilities |

---

## Workflows (Slash Commands)

| Command | Purpose |
|---------|---------|
| `/git-draft-commit` | Generate commit message from session |
| `/git-commit` | Stage + submit approved commit |
| `/git-using-worktrees` | Create isolated worktree for parallel work |
| `/planning-with-files` | Create dated P-ID plan folder + tracking files |

---

## Rules (TL;DR)

- **Model**: Haiku by default | Upgrade with `/model sonnet` or `/model opus`
- **Python files**: Never Edit/Write directly; use temp script pattern via `C:\Users\brian\AppData\Local\Temp\`
- **Tools**: Read, Grep, Glob (not cat/rg/find); Bash for shell ops
- **Thesis**: Bullets first—never prose without human approval
- **Git**: Feature branch per session, never direct `main` commits
- **Staging**: Explicit paths only (`git add file1 file2`), never `-A` or `.`

---

## Key References

| Topic | Location |
|-------|----------|
| **Architecture** | [user-docs/architecture/architecture.md](user-docs/architecture/architecture.md) |
| **Git workflow** | [user-docs/contributing/git-branch-strategy.md](user-docs/contributing/git-branch-strategy.md) |
| **Worktrees** | [user-docs/contributing/git-worktrees-and-parallel-sessions.md](user-docs/contributing/git-worktrees-and-parallel-sessions.md) |
| **Data access** | [02_thesis_data/nielsen/](02_thesis_data/nielsen/) |
| **Compliance** | [00_thesis_context/formal-requirements/](00_thesis_context/formal-requirements/) |
| **Session rules** | [.claude/rules/](.claude/rules/) |
| **Tooling issues** | [user-docs/integration/tooling-issues.md](user-docs/integration/tooling-issues.md) |
| **Zotero setup** | [user-docs/integration/zotero-integration-setup.md](user-docs/integration/zotero-integration-setup.md) |
| **Quick reference** | [user-docs/reference/CHEATSHEET.md](user-docs/reference/CHEATSHEET.md) |

---

**Full specs in linked docs. This is a navigation hub only — do not bloat.**
