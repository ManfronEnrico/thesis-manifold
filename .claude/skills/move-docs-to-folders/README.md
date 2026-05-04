# move-docs-to-folders

**Tier:** Core

## Purpose

Auto-scan root directory for markdown documentation violations, analyze document content to determine type, suggest appropriate destination using the routing table from `root-documentation-boundary` rule, and move files with cross-reference updates.

## Quick Start

```
/move-docs-to-folders
```

Scans root, identifies violations, suggests destinations, and prompts for move confirmation.

## Installation

Already installed in project `.claude/skills/move-docs-to-folders/`.

## See Also

- `.claude/rules/root-documentation-boundary.md` — Root whitelist and routing table
- `/docs-update-all` — Enhanced with violation detection
- `plans/02-in_progress-plans/P0019_.../` — Documentation reorganization plan
