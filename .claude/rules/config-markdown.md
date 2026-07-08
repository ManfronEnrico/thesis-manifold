---
name: config-markdown
description: RULE - Frontmatter standards, timestamp extraction, and hybrid table/list format guidance for all markdown files
category: governance
applies-to: ["**/*.md"]
triggers: [creating or updating any markdown file, choosing between table and list format]
created: 2026_06_22-00_00
updated: 2026_06_22-00_00
---

# Markdown Standards

Covers frontmatter requirements and format selection (hybrid table vs. list) for all `.md` files.

## Frontmatter

Every markdown file must include YAML frontmatter. Required fields:

```yaml
---
name: <kebab-case-filename>
description: RULE - <summary> | COMMAND - <summary> | SKILL - <summary>
category: governance | pattern | workflow | reference
applies-to: [scopes]
triggers: [situations]
created: YYYY_MM_DD-HH_mm
updated: YYYY_MM_DD-HH_mm
---
```

### Timestamp Extraction (PowerShell)

```powershell
(Get-Item "file.md").CreationTime.ToString('yyyy_MM_dd-HH_mm')   # created (set once)
(Get-Item "file.md").LastWriteTime.ToString('yyyy_MM_dd-HH_mm')  # updated (every edit)
```

### Checklist

| Field | Rule |
|-------|------|
| `name` | Matches filename, kebab-case |
| `description` | Starts with `RULE -`, `COMMAND -`, or `SKILL -` (dash not colon) |
| `category` | One of: `governance`, `pattern`, `workflow`, `reference` |
| `applies-to` | Non-empty array |
| `triggers` | Non-empty array |
| `created` | Set once at creation; format `YYYY_MM_DD-HH_mm` |
| `updated` | Updated on every edit; same format |

---

## Format — Hybrid Table + Detail Sections

Prefer the **hybrid pattern** for rule files, reference docs, and any content with consistent
categorical structure. Pure long-form lists are reserved for nuanced prose where context matters.

### The Hybrid Pattern

```markdown
## Quick Reference

| symptom | cause | fix |
|---------|-------|-----|
| Replace not found | CRLF mismatch | [Normalize LF](#line-endings) |
| charmap error | cp1252 + emoji | [Remove emoji](#encoding) |

---

## Line Endings
<anchored detail section with code block>

## Encoding
<anchored detail section with code block>
```

- **Table** = recognition surface. Defined once; column headers not repeated per entry.
- **Anchored sections** = full detail + code examples, linked from the table's fix column.
- **Result**: 30-50% fewer lines than equivalent long-form lists for structured rule sets.

### Format Decision Table

| Content type | Format |
|--------------|--------|
| Diagnostic rules (symptom → cause → fix) | Table + anchored sections |
| Command/flag references | Table |
| Anti-pattern catalogs (pattern → risk → correction) | Table |
| File/type mappings | Table |
| Architectural decisions requiring "why" rationale | List (prose) |
| Rules needing multi-paragraph context | List (prose) |
| Code examples | Fenced block in anchored section — never in table cell |

### Why Not Pure Tables

Tables cannot hold multi-line code blocks. Code examples live in anchored `##` sections
below the table, linked from the fix/detail column. This keeps the table scannable while
preserving the full safe pattern.

---

## Staleness Checks (on Every Edit)

Before finalizing any markdown file edit:

| Check | Verify |
|-------|--------|
| Filename | Matches `name:` field (kebab-case) |
| Description prefix | Starts with `RULE -`, `COMMAND -`, or `SKILL -` |
| Category | One of four allowed values |
| `updated:` timestamp | Set to current time |
| Slash-command references | Match current file names in `.claude/skills/` |
| External file references | Exist on disk |

---

## Related

- `config-rule.md` — rule file standards
- `config-skill.md` — skill file standards (if present)
