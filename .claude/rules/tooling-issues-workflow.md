---
paths:
  - "**"
---

# Tooling Issues Workflow

> Auto-loaded every session. Governs how Claude maintains the running tooling issues log.

## Purpose

[`docs/tooling-issues.md`](../../docs/tooling-issues.md) is a living reference of solved Windows/OneDrive/tooling problems encountered
in this project. Claude **must read it before executing any plan, task, or solution** to avoid
re-engineering problems that have already been diagnosed and solved.

---

## Trigger Phrases

When Brian says any of the following (case-insensitive), **immediately** review the current
session for new issues or updates to existing ones, then update [`docs/tooling-issues.md`](../../docs/tooling-issues.md):

- `update tooling`
- `log tooling issue`
- `tooling update`
- `add tooling issue`

Do **not** wait to be asked twice. Do it inline, before continuing any other work.

---

## What Qualifies as a Tooling Issue

Record an issue when the session revealed any of the following:

- A tool (Write, Edit, Bash, python, etc.) failed or produced wrong output in a non-obvious way
- A Windows / OneDrive / CRLF / encoding behaviour that caused a silent or unexpected error
- A workaround or safe pattern that replaced a naive approach
- A constraint in the environment that future plans must account for
- A LaTeX / Pandoc / Make build error that required a non-obvious fix
- An update or clarification to an existing issue (e.g. a new symptom, a better fix)

Do **not** record:
- Business logic bugs unrelated to tooling/environment
- One-off data quality problems
- Issues that are obvious from the standard Python or LaTeX docs

---

## Mandatory Pre-Task Check

Before starting **any** plan, solution, or multi-step task, Claude must:

1. Read `docs/tooling-issues.md` in full.
2. Check whether any of the planned actions would repeat a known failure pattern.
3. If a conflict is found, apply the documented safe pattern instead — no need to ask Brian first.

This check is required even if the file was loaded earlier in the session.

---

## How to Update `tooling-issues.md`

### Adding a new issue

Append at the bottom of the file using this format:

```
---

## Issue N: <short title — what went wrong>

**Symptom**: <what the failure looked like — error message, wrong output, silent failure>
**Cause**: <root cause — why it happens in this environment>
**Solution**:
<the safe pattern or fix — prefer code blocks for multi-step solutions>

**Key lesson**: <one-line rule to carry forward> _(omit if already obvious from Solution)_
```

- Increment N from the highest existing issue number.
- Keep the title concise: 5–8 words describing the failure, not the solution.

### Updating an existing issue

If the session revealed a new symptom, a better fix, or additional nuance for an existing issue:

1. Find the issue by number or title.
2. Append the new information under the existing content — **never delete existing content**.
3. Add a `**Update YYYY-MM-DD**:` line before the new material so the history is preserved.
