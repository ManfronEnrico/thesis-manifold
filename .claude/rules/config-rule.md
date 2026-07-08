---
name: config-rule
description: RULE - Standards for creating .claude/rules/*.md files with frontmatter, hybrid table format, and structured content
category: governance
applies-to: [.claude/rules/*.md]
triggers: [creating a new rule file, documenting a convention, adding a constraint]
created: 2026_06_22-00_00
updated: 2026_06_22-00_00
---

# Rule Files

Rule files document project constraints, patterns, workflows, and decisions. They live in `.claude/rules/`.

## Naming & Location

`{category}-{slug}.md` in kebab-case. Categories: `workflow-`, `format-`, `session-`, `config-`, or descriptive noun (e.g., `rule.md`, `windows-env.md`).

## Frontmatter

```yaml
---
name: <kebab-case-filename>
description: RULE - <one-line summary>
category: governance | pattern | workflow | reference
applies-to: [scopes]
triggers: [situations]
created: YYYY_MM_DD-HH_mm
updated: YYYY_MM_DD-HH_mm
---
```

See `config-markdown.md` for timestamp extraction commands and frontmatter checklist.

## Format — Hybrid Table + Detail

Use the **hybrid pattern**: a compact reference table at the top, anchored detail sections below.

**Table** = recognition surface (symptom → cause → fix pointer). Defined once, scanned fast.
**Sections** = full detail with code examples, linked from the table's fix column.

```markdown
## Quick Reference

| symptom | cause | fix |
|---------|-------|-----|
| Replace not found | CRLF mismatch | [Normalize LF](#line-endings) |
| charmap error | cp1252 + emoji | [Remove emoji](#encoding) |

---

## Line Endings
<full detail + code block>

## Encoding
<full detail + code block>
```

### When to Use Tables vs. Lists

| Content type | Format | Why |
|--------------|--------|-----|
| Diagnostic rules (symptom → cause → fix) | Table | Eliminates repeated column headers; 30-50% fewer lines |
| Command/flag references | Table | Column-wise extraction |
| Anti-pattern catalogs | Table | Pattern recognition |
| Architectural decisions with "why" rationale | List | Nuanced prose needed |
| Rules needing multi-paragraph context | List | Tables can't hold paragraphs |
| Code examples | Fenced block under anchored section | Tables cannot hold multi-line code |

## Content Structure

1. **Title + one-line preamble** — what this governs and why it exists
2. **Quick Reference table** — symptom/trigger → fix pointer (omit if <3 entries)
3. **Anchored detail sections** — full patterns + code, one section per rule
4. **Related** — links to connected files

## Rule of Thumb

Rule files are prescriptive (govern what to do). Put structural facts in CLAUDE.md.
Keep rule files under 5 minutes to read. Prefer hybrid format over pure long-form lists
when content has consistent categorical structure.
