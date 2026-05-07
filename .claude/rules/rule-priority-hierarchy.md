---
name: Rule Priority Hierarchy
description: Conflict resolution framework for rules; establishes tier-based precedence (Trust > Correctness > Quality > Efficiency)
type: rule
---

# Rule Priority Hierarchy

When multiple rules conflict, resolve by tier. **Higher tier always wins.**

---

## Trust Tier (Never Yield)

These rules are non-negotiable. They protect integrity and safety.

- **Branch strategy**: No commits directly on `main`. Every session gets its own branch (feature branch or worktree-isolated)
  - Why: Prevents accidental direct commits to main, enables safe parallel work
  - Exception: Only when explicitly merging completed work back to main after review

- **Root documentation boundary**: Analysis docs, reports, audits, guides stay out of root directory. All markdown documentation → `docs/` folders per routing table
  - Why: Prevents root clutter, maintains discoverability, enforces semantic folder organization
  - Enforced by: `/move-docs-to-folders` skill; P0021 structure authority

---

## Correctness Tier (Yield Only to Trust)

These rules maintain data integrity and plan discipline.

- **Plan outcome discipline**: A plan is not considered complete until its outcome file exists in `03-outcome_plans/`
  - Why: Prevents dangling in-progress plans; outcome files = audit trail of completed work
  - When: Every plan execution must produce an outcome file (Completed, Adjusted, Dropped sections)

---

## Quality Tier (Yield to Trust + Correctness)

These rules improve usability and reduce cognitive load.

- **One-off execution default**: Workflow commands without explicit intervals execute once immediately, not recurring
  - Why: Recurring tasks require explicit intent; default to "do this now" to prevent unwanted automation
  - When: User says `"update all docs"` → execute once. User says `"update all docs every 10m"` → schedule recurring

- **Bullets-only before prose**: Thesis content starts as bullets. Never generate prose without explicit human approval
  - Why: Bullets are reversible and iterable; prose is hard to change without losing nuance
  - When: Thesis sections are always written as bullets first, then approved for prose conversion via `/write-section`

---

## Efficiency Tier (Yields to All)

These rules optimize performance or convenience. Reserved for future use.

(No rules currently assigned to Efficiency tier.)

---

## Conflict Resolution Examples

### Example 1: Branch strategy vs. One-off default

**Scenario:** User says "merge this feature branch back to main without a separate review commit"

**Resolution:**
1. Check: Does this violate branch strategy (Trust tier)? NO — user is merging (allowed exception)
2. Check: Does this violate outcome discipline (Correctness tier)? YES if not documented
3. **Action:** Allow merge, but ensure outcome file exists documenting the merge

**Tier precedence:** Trust (allowed) > Correctness (require documentation) → Proceed

---

### Example 2: Root boundary vs. Plan structure

**Scenario:** User creates a analysis document for a plan. Should it go at root or in plan folder?

**Resolution:**
1. Check: Root boundary rule (Trust tier) says "documentation → `docs/` or plan folder, never root"
2. Check: Plan structure (Quality tier) says "plan artifacts → `plans/{status}/P{NNNN}_.../`"
3. **Action:** If it's a plan artifact, place in plan folder per plan structure. If it's analysis used by the plan, place in `docs/` per root boundary
4. **Tier precedence:** Trust (root boundary) > Quality (plan structure) → Document goes to appropriate `docs/` folder or plan folder, never root

---

## How to Apply This Hierarchy

When faced with conflicting rules:

1. **Identify both rules** and their tiers
2. **Compare tiers** — higher tier wins
3. **If same tier**, use the rule's documented "why" to decide
4. **Document the decision** (especially if yielding a rule)

---

## See Also

- `.claude/rules/trigger-branch-strategy.md` — Branch strategy (Trust tier)
- `.claude/rules/root-documentation-boundary.md` — Root boundary (Trust tier)
- `.claude/rules/trigger-plan-workflow.md` — Plan structure (Quality tier)
- `.claude/rules/one-off-execution.md` — One-off execution default (Quality tier)
- CLAUDE.md → Thesis section → Bullets-only discipline (Quality tier)

---

**Last Updated:** 2026-05-04  
**Status:** Core rule for P0020 rule system reform
