## 🧠 Master Thesis Codebase — Memory Index

This directory holds persistent knowledge across sessions. Files live in `memory/` and are auto-loaded at session start.

### Structure

Memory files use frontmatter format:
```yaml
---
name: [title]
description: [one-line purpose]
type: [user|feedback|project|reference]
---
[content]
```

Files in this index are loaded every session. Keep total size manageable (~30 entries max).

---

### Current Memories

#### Feedback (How to approach work)

- [feedback_model_override.md](feedback_model_override.md) — Model selection: Haiku default, escalate to Sonnet for complex work (5+ files, architecture decisions)
- [feedback_modularization.md](feedback_modularization.md) — Keep individual docs <300 lines; split when adding 50+ lines to CLAUDE.md

#### Project (Active work context)

- [project_workflow_optimization.md](project_workflow_optimization.md) — Context efficiency improvements from pta-cbp-parser (model override, doc modularization, plan timestamps)

#### Reference (Where to find things)

_(None yet; add as needed)_

#### User (About collaboration)

_(None yet; add as needed)_

---

**Last updated**: 2026-04-15  
**Maintained by**: Brian & Claude Code
