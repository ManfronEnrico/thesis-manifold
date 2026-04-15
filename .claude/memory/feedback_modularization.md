---
name: Modular documentation reduces context overhead
description: Strategy for splitting large docs to reduce per-session context load
type: feedback
---

**Rule**: Keep individual docs under 300 lines. When a file exceeds 300 lines or when adding 50+ lines to CLAUDE.md, plan a split.

**Why**: From pta-cbp-parser audit (2026-04-15): modular docs reduce context load by ~20% per session (58% reduction measured in audit session). With thesis deadline approaching (30 days) and 120 pages target, compound savings matter—each 5% context reduction = ~1K tokens saved per session.

**How to apply**: 
- When editing CLAUDE.md and feeling it grow → check `wc -l` before adding large sections
- When adding architecture/methodology/compliance decisions → consider separate docs instead of bloating CLAUDE.md
- When reviewing docs/ → prioritize splitting any file >250 lines
- **Canonical structure**: CLAUDE.md (nav hub only, <10KB), docs/ (modular topic files, <300 lines each), .claude/rules/ (workflows, <200 lines each)

**Measurement**: Run periodically (every 5-10 sessions) to confirm 15-20% context reduction per load is maintained.
