---
title: "ADR-003: Builder Agent Fate (Keep or Remove)"
type: decision
status: draft
created: 2026-04-13
---

# ADR-003: Builder Agent Fate (Keep or Remove)

**Status**: OPEN — decision pending
**Date**: 2026-04-13
**Deciders**: Brian + thesis partner

---

## Context

`thesis_production_system/agents/builder/` contains 6 substantive Python files:
- `architect.py`
- `builder_graph.py`
- `coder.py`
- `evaluator.py`
- `executor.py`
- `experiment_registry.py`

The builder subsystem appears to be a code-generation / experiment-execution agent. It is more developed than other agents, suggesting significant prior investment. However, its role in the current thesis workflow is unclear.

The master plan (Phase 1) requires a decision before any further development. The plan leans toward **keep + add SKILL.md**.

---

## Assessment

**Arguments for keeping:**
- 6 substantial files already implemented — significant prior work
- `experiment_registry.py` likely integrates with `docs/experiments/experiment_registry.json`
- May be useful for automated benchmarking (SRQ1) or synthesis (SRQ2)
- SKILL.md can document it without requiring active use

**Arguments for removing:**
- If unused in the actual thesis workflow, it adds maintenance overhead
- Could be misleading in the codebase documentation
- Reduces System B complexity for the thesis description

**Current thesis use:** Unknown — needs investigation. Check `thesis_production_system/agents/builder/builder_graph.py` for integration points.

---

## Decision Options

### Option A: Keep + Add SKILL.md (Recommended lean)
- Document the builder subsystem with a `SKILL.md` file in the builder directory
- Keep the code as-is; use if/when useful for benchmarking or code generation
- No active use required; just preserved and documented

### Option B: Remove
- Delete the entire `builder/` directory
- Remove any references in `core/coordinator.py`
- Simplify System B to 9 agents

### Option C: Refactor + Integrate
- Clarify the builder's role; actively integrate into the thesis workflow for SRQ1/SRQ2
- Higher risk; more work; only if data access timeline allows

---

## Decision

[PENDING — complete after reviewing builder_graph.py integration points]

**Chosen option**: [A / B / C]
**Rationale**: [why]

---

## Consequences

[Complete after decision]

**If Option A:** Create `thesis_production_system/agents/builder/SKILL.md` documenting:
- Purpose of each file
- How to invoke the builder
- Integration points with experiment_registry.json

---

## References

- `thesis_production_system/agents/builder/` — the 6 files in question
- `docs/experiments/experiment_registry.json` — likely integration point
- `README_builder.md` — existing builder documentation
