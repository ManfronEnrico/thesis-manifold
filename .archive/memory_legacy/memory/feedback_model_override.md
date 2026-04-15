---
name: Model override convention for tier selection
description: Three mechanisms (command, inline phrase, settings) for selecting Haiku/Sonnet/Opus based on task complexity
type: feedback
---

**Rule**: Use Haiku by default (cost-optimized). Escalate to Sonnet for complex tasks (5+ file changes, cross-system refactors, architecture decisions). Opus only for major redesigns.

**Why**: Thesis deadline (15 May, 30 days) + 8GB RAM constraint + 120-page target means cost-per-session matters. Haiku handles 85% of thesis writing/analysis tasks; Sonnet needed only for interdependent System A/B changes.

**How to apply**: 
- Voice sessions: just say "use sonnet for this analysis" (I auto-detect)
- CLI: `/model sonnet` before complex work
- Default: leave on Haiku (default, cost-optimized)
- Fallback: `use default` or `back to haiku` to reset

**Escalation triggers for Sonnet**:
- Multi-file refactors across System A and System B
- Architecture reviews or major design decisions
- Complex literature synthesis requiring deep reasoning
- Cross-agent coordination changes
