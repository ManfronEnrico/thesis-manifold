# CLAUDE.md — Manifold AI Thesis: CBS Master's 2026
> Automatically read every session. Navigation hub only.
> Full specs: `docs/`, `.claude/rules/`, and skill definitions.

---

## Quick Start

**Read these in order:** architecture → RQs → project-state → compliance → tooling → repo-map

- [docs/architecture/architecture.md](docs/architecture/architecture.md) — System A/B design
- [thesis/thesis-context/research-questions/research-questions.md](thesis/thesis-context/research-questions/research-questions.md) — RQs v2
- [thesis/thesis-context/thesis-topic/project-state.md](thesis/thesis-context/thesis-topic/project-state.md) — frozen decisions
- [thesis/thesis-context/formal-requirements/compliance.md](thesis/thesis-context/formal-requirements/compliance.md) — CBS requirements
- [docs/integration/tooling-issues.md](docs/integration/tooling-issues.md) — known environment problems
- [docs/contributing/repository_map.md](docs/contributing/repository_map.md) — file locations

---

## Workflows

| Command | Purpose |
|---------|---------|
| `/git-draft-commit` | Generate commit message from session |
| `/git-commit` | Stage and submit an approved commit message |
| `/git-worktrees` | Set up isolated worktree for this session |
| `/docs-update-all` | Update all living project documents |
| `/standup-log` | Log standup entry to draft |
| `/update-outline` | Update thesis structure + stubs |
| `/write-section <id>` | Convert bullets to prose (manual approve before) |
| `/cite` | Add APA 7 citation to references |

---

## Rules (TL;DR)

- **Model**: Haiku by default | Upgrade with `/model sonnet` or `/model opus`
- **Python files**: Never Edit/Write `.py` files directly (hook enforces safe pattern — temp script via `C:/Users/brian/AppData/Local/Temp/`)
- **Tools**: Read, Grep, Glob (not cat/rg/find); Bash for system commands
- **Thesis**: Bullets only—never prose without human approval
- **Every phase transition**: Requires explicit human approval
- **Git**: Each session gets its own worktree + branch. Warn on `main`. Never push directly to `main`. Use draft PRs for backup. → [git-branch-strategy.md](docs/contributing/git-branch-strategy.md) · [worktree guide](docs/contributing/git-worktrees-and-parallel-sessions.md)

---

## Quick References

- [docs/reference/cheatsheet.md](docs/reference/cheatsheet.md) — CLI commands, trigger phrases
- [docs/integration/tooling-issues.md](docs/integration/tooling-issues.md) — solved Windows/OneDrive/tooling problems (6 documented)
- [thesis/data/nielsen/scripts/README.md](thesis/data/nielsen/scripts/README.md) — Nielsen data access guide (52 objects cataloged, 29 CSV exports)
- [thesis/data/nielsen/description/SCHEMA_SNAPSHOT.md](thesis/data/nielsen/description/SCHEMA_SNAPSHOT.md) — Auto-generated schema reference (all 52 objects, columns, row counts)
- [docs/integration/zotero-integration-setup.md](docs/integration/zotero-integration-setup.md) — Zotero integration setup (group library ID: 6479832)
- [docs/reference/zotero-quick-reference.md](docs/reference/zotero-quick-reference.md) — Quick Zotero copy-paste commands
- [.claude/rules/](.claude/rules/) — workflow automation rules
- [docs/contributing/repository_map.md](docs/contributing/repository_map.md) — module inventory
- [.claude/skills/](\.claude/skills/) — Project-specific skill definitions
- [.claude/IMPORTED_SKILLS_ANALYSIS.md](.claude/IMPORTED_SKILLS_ANALYSIS.md) — **22 NEW SKILLS IMPORTED** (Apr 16) — tier classification + integration strategy
- [.claude/SKILLS_DEMO_EXAMPLES.md](.claude/SKILLS_DEMO_EXAMPLES.md) — 10 concrete demos with expected outputs (try each in 5-8 min)
- [.claude/SKILLS_INVENTORY.md](.claude/SKILLS_INVENTORY.md) — complete reference for all 35 skills by category + use cases

---

**Full details in linked docs above.** This file is a navigation hub, not a spec. Do not bloat it.
