---
name: Token optimization of CLAUDE.md and rules (2026-04-15)
description: Major reduction of auto-loaded tokens by converting CLAUDE.md to nav hub and collapsing rule files to action-focused summaries
type: feedback
---

# Token Optimization: CLAUDE.md & Rules (2026-04-15)

**What**: Reduced auto-loaded session tokens from ~15k to ~4.3k (71% reduction) by restructuring CLAUDE.md and rule files.

**Why**: Memory files and CLAUDE.md were consuming 7.5% of each session's token budget (~15k tokens), with 80% of CLAUDE.md being project details that live in `docs/` anyway. Rules duplicated CLAUDE.md instructions, creating double-loading overhead.

**How**:
- CLAUDE.md: Converted 580 lines → 40 lines (nav hub only; content moved to docs/)
- Rule files: Collapsed verbose deduction algorithms to action-focused summaries (trigger + link to skill)
- Removed duplication: rules no longer repeat CLAUDE.md model/tool guidance
- Single source of truth: all details now in `docs/` with CLAUDE.md as pure index

**Tokens freed**: ~10.7k per session (now available for work)
**No functionality lost**: All commands, triggers, workflows unchanged

**Applies to**: CLAUDE.md, context-token-optimization.md, trigger-git-commit-workflow.md, trigger-docs-workflow.md, trigger-plan-workflow.md, tooling-issues-workflow.md

**Key lesson**: Large configuration files (CLAUDE.md) should be pure navigation hubs—push all details to dedicated docs/ that have no cost of retrieval (they're already project state, not Claude instruction overhead).

