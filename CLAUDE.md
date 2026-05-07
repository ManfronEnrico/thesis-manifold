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
- **[METADATA.py](METADATA.py)** — Nielsen metadata reference library (load once, query column definitions by name)

---

## Workflows

### Session & Documentation

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

### Enforcement & Validation

| Command | Purpose |
|---------|---------|
| `/enforce-repo-cleanliness` | **Master gate**: Run all 4 validators + unified report |
| `/validate-plan-ids` | Enforce P-ID naming convention (P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}) |
| `/audit-plan-outcomes` | Verify outcome completeness (Correctness Tier enforcement) |
| `/audit-cross-references` | Validate all links/references are correct |
| `/sync-memory-indices` | Keep memory files synchronized with MEMORY.md index |

---

## Rules by Tier

See [.claude/rules/rule-priority-hierarchy.md](.claude/rules/rule-priority-hierarchy.md) for conflict resolution.

### 🔴 Trust Tier (Non-negotiable)

- **Branch strategy**: Every session gets own branch (feature branch or worktree). Never `main` commits except merges. → [trigger-branch-strategy.md](.claude/rules/trigger-branch-strategy.md)
- **Root documentation boundary**: All analysis/reports → `docs/` folders per routing table. Root reserved for foundational files only. → [root-documentation-boundary.md](.claude/rules/root-documentation-boundary.md)

### 🟡 Correctness Tier (Maintain data integrity)

- **Plan status discipline**: Plan status tracked in frontmatter only (no duplicate outcome files). Folder location + frontmatter status must agree. → [trigger-plan-workflow.md](.claude/rules/trigger-plan-workflow.md)

### 🟢 Quality Tier (Improve usability)

- **One-off execution default**: Workflow commands execute once immediately unless interval specified. → [one-off-execution.md](.claude/rules/one-off-execution.md)
- **Bullets-only before prose**: Thesis content starts as bullets; never prose without explicit approval.
- **Model**: Haiku by default | Upgrade with `/model sonnet` or `/model opus`
- **Python files**: Never Edit/Write directly (hook enforces temp script pattern via `C:/Users/brian/AppData/Local/Temp/`)
- **Tools**: Read, Grep, Glob (not cat/rg/find); Bash for system commands

### 📋 Reference Rules

- [.claude/rules/](.claude/rules/) — All workflow automation rules by trigger phrase

---

## Quick References

### Core Documentation

- [docs/reference/cheatsheet.md](docs/reference/cheatsheet.md) — CLI commands, trigger phrases
- [docs/contributing/repository_map.md](docs/contributing/repository_map.md) — module inventory
- [docs/integration/tooling-issues.md](docs/integration/tooling-issues.md) — solved Windows/OneDrive/tooling problems (6 documented)

### Rule System (P0020 Reform)

- [.claude/rules/rule-priority-hierarchy.md](.claude/rules/rule-priority-hierarchy.md) — Tier-based conflict resolution (Trust > Correctness > Quality > Efficiency)
- [.claude/rules/](.claude/rules/) — All workflow automation rules
- [memory/convention_project_standards.md](C:\Users\brian\.claude\projects\C--dev-thesis-manifold\memory\convention_project_standards.md) — Consolidated conventions (models, worktrees, P-IDs, docs routing, data access)

### Data & Integration

- [thesis/data/nielsen/scripts/README.md](thesis/data/nielsen/scripts/README.md) — Nielsen data access (52 objects, 29 CSV exports)
- [thesis/data/nielsen/description/SCHEMA_SNAPSHOT.md](thesis/data/nielsen/description/SCHEMA_SNAPSHOT.md) — Nielsen schema reference
- [docs/integration/zotero-integration-setup.md](docs/integration/zotero-integration-setup.md) — Zotero setup (group library ID: 6479832)
- [docs/reference/zotero-quick-reference.md](docs/reference/zotero-quick-reference.md) — Quick Zotero commands

### Skills & Project State

- [.claude/skills/](\.claude/skills/) — Project-specific skill definitions (now includes enforcement validators)
- [.claude/IMPORTED_SKILLS_ANALYSIS.md](.claude/IMPORTED_SKILLS_ANALYSIS.md) — Imported skills (22 + 5 new enforcement skills)
- [plans/PLANS_INDEX.md](plans/PLANS_INDEX.md) — All plans by P-ID (P0001–P0022, 8 status buckets: backlog, in_progress, focus, complete, blocked, paused, cancelled, archived)

---

**Full details in linked docs above.** This file is a navigation hub, not a spec. Do not bloat it.
