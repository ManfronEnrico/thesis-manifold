---
paths:
  - "**"
---

# Tooling Issues Workflow

**Purpose**: `docs/tooling-issues.md` is the living reference for solved Windows/OneDrive/tooling problems.

**Trigger phrases**: "update tooling", "log tooling issue", "tooling update", "add tooling issue"

**Before any plan**: Read `docs/tooling-issues.md` in full. Check if planned actions repeat known failure patterns. If found, apply documented safe pattern.

**What qualifies**: Tool failures (Write, Edit, Bash), Windows/OneDrive/CRLF bugs, workarounds, environment constraints, LaTeX/Pandoc build errors.

**Format for new issue**:
```
---
## Issue N: <short title>
**Symptom**: <failure appearance>
**Cause**: <root cause>
**Solution**: <safe pattern or fix>
**Key lesson**: <rule to carry forward>
```

See `docs/tooling-issues.md` for examples.
