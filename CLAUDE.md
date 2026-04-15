# CLAUDE.md — Manifold AI Thesis: CBS Master's 2026
> Automatically read every session. Navigation hub only.
> Full specs: `docs/`, `.claude/rules/`, and skill definitions.

---

## Quick Start

**Read these in order:**
1. [docs/architecture.md](docs/architecture.md) — System A/B design
2. [docs/research-questions.md](docs/research-questions.md) — RQs v2
3. [docs/project-state.md](docs/project-state.md) — frozen decisions
4. [docs/compliance.md](docs/compliance.md) — CBS requirements
5. [docs/tooling-issues.md](docs/tooling-issues.md) — known environment problems
6. [dev/repository_map.md](dev/repository_map.md) — file locations

---

## Workflows

| Command | Purpose |
|---------|---------|
| `/draft_commit` | Generate commit message from session |
| `/update_all_docs` | Update all living project documents |
| `/log_standup` | Log standup entry to draft |
| `/update-outline` | Update thesis structure + stubs |
| `/write-section <id>` | Convert bullets to prose (manual approve before) |
| `/cite` | Add APA 7 citation to references |

---

## Rules (TL;DR)

- **Model**: Haiku by default | Upgrade with `/model sonnet` or `/model opus`
- **OneDrive**: Never Edit/Write `.py` files directly (hook enforces safe pattern)
- **Tools**: Read, Grep, Glob (not cat/rg/find); Bash for system commands
- **Thesis**: Bullets only—never prose without human approval
- **Every phase transition**: Requires explicit human approval

---

## Quick References

- [docs/context.md](docs/context.md) — packages, session log
- [CHEATSHEET.md](CHEATSHEET.md) — CLI commands, trigger phrases
- [docs/tooling-issues.md](docs/tooling-issues.md) — solved Windows/OneDrive/tooling problems (7 issues)
- [docs/ZOTERO_SETUP_GUIDE.md](docs/ZOTERO_SETUP_GUIDE.md) — Zotero integration Phase 1 (group library ID: 6479832)
- [ZOTERO_QUICK_REFERENCE.md](ZOTERO_QUICK_REFERENCE.md) — Quick Zotero copy-paste commands
- [.claude/rules/](. claude/rules/) — workflow automation rules
- [dev/repository_map.md](dev/repository_map.md) — module inventory
- [SKILL_ACTIVATION_SUMMARY.md](SKILL_ACTIVATION_SUMMARY.md) — test-codebase-integrity skill status & usage
- [.claude/IMPORTED_SKILLS_ANALYSIS.md](.claude/IMPORTED_SKILLS_ANALYSIS.md) — tier classification for 30 academic research skills
- [.claude/SKILLS_DEMO_EXAMPLES.md](.claude/SKILLS_DEMO_EXAMPLES.md) — 10 concrete demos with expected outputs
- [.claude/SKILLS_INVENTORY.md](.claude/SKILLS_INVENTORY.md) — reference guide for all skills by category

---

**Full details in linked docs above.** This file is a navigation hub, not a spec. Do not bloat it.
