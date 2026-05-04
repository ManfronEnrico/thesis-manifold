---
name: Rule System Reform - Current vs. Best Practice
description: Gap analysis comparing your current implementation to jlacour-git's framework
created: 2026-05-04
---

# Rule System Gap Analysis

## What You've Built (Strengths)

### ✓ `/move-docs-to-folders` Skill
This is **exactly** what jlacour-git advocates for: **proceduralization**.

**Your approach:**
- Detected that `root-documentation-boundary` rule requires enforcement
- Built a skill to automate the multi-step workflow (scan → analyze → route → move → update refs)
- Integrated with other skills (`/docs-update-all`, `/git-draft-commit`)

**Framework alignment:**
- ✓ Rules are enforcement targets, not procedures
- ✓ Procedures live in skills, not rules
- ✓ Clear separation of concerns

### ✓ `root-documentation-boundary` Rule
Clear, scoped, non-negotiable enforcement point.

**What works:**
- Whitelist/blacklist is precise (5 allowed files vs. everything else)
- Routing table is comprehensive and unambiguous
- Examples show both correct and incorrect patterns

---

## What's Not Working (Gaps)

### Gap 1: Instruction Fatigue (Multiple Rule Files)

**Problem:** You have ~10 rule files across `.claude/rules/`, but most are either:
- **Procedures** (step-by-step workflows) that should be in skills
- **Conventions** (facts about how things work) that should be in memory
- **Routing entries** (path mappings) that should be in a single reference file

**Example of the problem:**

File: `.claude/rules/trigger-git-commit-workflow.md` (79 lines)
```
"0. **Branch check**: Run git branch --show-current..."
"1. **Log errors**: Run `/log_errors` to scan conversation..."
"2. **Session context** (PRIMARY)..."
```

This is a **procedure**, not a rule. It should live in `/git-draft-commit` SKILL.md, not in `.claude/rules/`.

**Current effect:** Rules compete for attention. You have "Check before classifying" (trust) side-by-side with "Minimize ceremony for simple tasks" (efficiency) with no priority resolution.

---

### Gap 2: No Explicit Priority Hierarchy

**Problem:** Your rules have equal weight in the system.

**Example of a conflict that can't be resolved:**

Rule 1 (in `trigger-plan-workflow.md`): "Always move plan folders to status buckets (01-backlog, 02-in-progress, etc.)"

Rule 2 (implied in `one-off-execution.md`): "Execute immediately unless user says 'every N minutes'"

**Scenario:** User says "I'm working on a plan, don't execute anything recurring."
- Hierarchy: Trust > Correctness > Quality > Efficiency
- **Trust rule**: "Always move between status buckets on phase transition"
- **Efficiency rule**: "Don't invoke /loop unless interval specified"

Without explicit hierarchy, the model has to infer which rule wins. With hierarchy, it's unambiguous: Trust always wins.

**Current effect:** Reduces compliance on edge cases.

---

### Gap 3: Conventions Scattered Instead of Consolidated

**Problem:** Facts about your project are spread across multiple rule files and memory files.

**Convention examples currently scattered:**
- `context-token-optimization.md` — "Use Haiku by default, Sonnet for multi-file, Opus for architecture"
- `worktree-workflow.md` — "Worktrees live at worktrees/ directory, gitignored"
- `plan-documentation-structure.md` — "Plan folders use P-ID naming: P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}"
- `trigger-plan-workflow.md` — "Plan YAML frontmatter auto-included"
- `tooling-issues-workflow.md` — "JSONL is authoritative, markdown is derived"
- `repository-map-reference.md` — "Consult repository_map.md before exploring"

**What jlacour-git did:** Moved all conventions to MEMORY.md, leaving only behavioral corrections in rules.

**Your hybrid state:** Some conventions are in rules (causing rule bloat), some are in memory (correct).

**Current effect:** +2,000 tokens in rules that could be in memory; rules harder to scan.

---

### Gap 4: Procedures Not Decentralized to Skills

**Problem:** Workflows are documented in `.claude/rules/`, not in the skills that implement them.

**Examples:**

`.claude/rules/trigger-git-commit-workflow.md` (79 lines):
```
"1. **Log errors**: Run `/log_errors` to scan conversation and append..."
"4. **Last commit**: `git log -1 --format="%H %ai %s"` — cutoff..."
"7. **Draft**: Format as `<type>: <subject>` + bullets..."
```

This is the procedure for `/git-draft-commit` skill. It should be in that skill's SKILL.md, not in a separate rule file.

**What should happen:** Each skill owns its own procedure documentation.

Current structure:
```
.claude/rules/trigger-git-commit-workflow.md  (procedure)
.claude/skills/git-draft-commit/SKILL.md      (empty or brief)
```

Should be:
```
.claude/rules/                                 (only behavioral corrections)
.claude/skills/git-draft-commit/SKILL.md      (complete procedure + examples)
```

**Current effect:** Users must read 2 files to understand a workflow; procedures aren't versioned with skill code.

---

### Gap 5: No Scenario Testing on Prose Compression

**Problem:** Your rules are verbose but not tested for behavioral completeness.

**Example:**

`root-documentation-boundary.md` includes a 60+ line "How to Apply" section with step-by-step examples.

**Question:** Does every word matter?

Phrase: "ANY markdown documentation not in the whitelist above belongs elsewhere"

Could this be compressed to: "Non-whitelisted docs move to docs/ or plans/" without losing behavioral coverage?

**Scenario Test:** Can I construct a case where the original catches a mistake but the compressed version doesn't?

- User creates `MIGRATION_NOTES.md` at root
- **Original:** Explicit "not in whitelist → belongs elsewhere" — catches it
- **Compressed:** Vague "move to docs/" — user might think "this is notes, maybe root is OK?"

**jlacour-git's approach:** Run this test before compressing. 7 of 13 compressions initially failed. This catches the gaps.

**Your current state:** No compression attempted; rules are maximally verbose.

**Current effect:** Rules are clear but consume excess tokens; opportunity for 20-40% compression with testing.

---

### Gap 6: Enforcement Points Are Hooks + Skills, But Rules Are Separate

**Problem:** The actual enforcement mechanisms (hooks + skills) are decoupled from rules that describe them.

**Example:**

Rule: `.claude/rules/trigger-branch-strategy.md` says "Every session should work on a dedicated branch"

Enforcement: `.claude/hooks/branch_guard.py` (runs on `UserPromptSubmit`)

**Disconnect:** The rule file explains the rule in prose. The hook implements it in code. They're not versioned together.

**What jlacour-git did:** Enforcement capabilities become part of the rule specification. "Rule X enforced by: hook Y, skill Z" — not separate concerns.

**Your current state:** Rules describe intent; hooks/skills implement intent; gap between description and code.

**Current effect:** Harder to audit compliance; if hook breaks, rule is still in the file saying it should work.

---

### Gap 7: No Learning Loop (Digest Skill Missing)

**Problem:** jlacour-git built a `/digest` skill that closes the learning loop:
- Reads failure records + low ratings + algorithm reflections
- Extracts improvement proposals
- Classifies by layer (rules vs. hooks vs. skills)
- Presents with human-in-the-loop review

**Your current state:** You manually identify patterns across sessions and update rules/procedures by hand.

**Example of the gap:**

You notice across 3 sessions:
- Session A: "Added plan to wrong status bucket"
- Session B: "Forgot to create outcome file"
- Session C: "Moved plan but didn't update PLANS_INDEX.md"

**jlacour-git's approach:** Extract these as three proposals:
1. USER-SAFE → Add checkpoint to plan-status-transitions rule
2. USER-SAFE → Make outcome-file-creation mandatory before phase transition
3. UPSTREAM-ONLY → Needs hook to auto-update PLANS_INDEX

**Your approach:** You'd manually update the rule, possibly missing the interaction effects.

**Current effect:** Slower feedback loop; harder to validate that rule changes actually improve compliance.

---

## Comparison Table: Rule System Maturity

| Dimension | jlacour-git | You (Current) | Gap |
|---|---|---|---|
| **Rule count** | 26 (consolidated) | ~10 files (but scattered) | Looks good, but some aren't rules |
| **Token consumption** | ~2,900 tokens | ~3,500+ tokens (rough estimate) | +20% bloat |
| **Lateral reclassification** | ✓ Explicit | ⚠ Partial (good on move-docs, weak on conventions) | Conventions not consolidated |
| **Priority hierarchy** | ✓ Trust > Correctness > Quality > Efficiency | ✗ Implicit only | No explicit tier labels |
| **Procedure decentralization** | ✓ All procedures → skills | ⚠ Partial (move-docs is skill, git-commit still in rules) | ~50% done |
| **Prose compression** | ✓ Scenario-tested | ✗ No compression attempted | Opportunity: 20-40% savings |
| **Enforcement coupling** | ✓ Rule + hook/skill versioned together | ⚠ Separate (rule file vs. hook code) | Gap in audit trail |
| **Learning loop (Digest)** | ✓ /digest skill | ✗ Manual identification | No automated proposal extraction |
| **Cross-reference validation** | ✓ Structural integrity checked | ⚠ Manual cross-reference tracking | Brittle to renames |

---

## What Needs to Happen (3-Step Path Forward)

### Step 1: Reclassify What You Have

Go through each `.claude/rules/` file and label it:
- **RULE** (behavioral correction) → keep in `.claude/rules/`
- **PROCEDURE** (multi-step workflow) → move to relevant skill's SKILL.md
- **CONVENTION** (fact about the project) → move to memory
- **ROUTING** (path mapping) → consolidate into single reference file

**Quick audit:**

| File | Current Classification | Correct Classification |
|---|---|---|
| `root-documentation-boundary.md` | Rule | RULE ✓ + ROUTING |
| `trigger-branch-strategy.md` | Rule | RULE ✓ |
| `trigger-plan-workflow.md` | Rule + Procedure | RULE + PROCEDURE (split) |
| `trigger-git-commit-workflow.md` | Procedure | PROCEDURE (move to skill) |
| `trigger-docs-workflow.md` | Procedure | PROCEDURE (move to skill) |
| `context-token-optimization.md` | Convention | CONVENTION (move to memory) |
| `worktree-workflow.md` | Convention | CONVENTION (move to memory) |

---

### Step 2: Create Enforcement Rules (Like `/move-docs-to-folders`)

You already started this correctly with `/move-docs-to-folders`.

**Pattern to replicate:** For each RULE, ask:
- "What could go wrong if someone ignores this rule?"
- "Can I automate detection + enforcement?"
- "Does this need a skill?"

**Examples:**

Rule: "Plans use P-ID naming (P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug})"
→ Enforcement needed: `/validate-plan-ids` skill (scan plans/, check P-ID format, suggest fixes)

Rule: "Every phase transition requires outcome file"
→ Enforcement needed: Hook in plan-workflow that blocks transition without outcome file

Rule: "Branch strategy: never commit on main"
→ Enforcement already exists: `.claude/hooks/branch_guard.py` ✓

---

### Step 3: Build `/enforce-repo-cleanliness` Master Skill

Combine all enforcement points into one orchestrator:

```
/enforce-repo-cleanliness
├─ Check 1: Root documentation boundary → /move-docs-to-folders
├─ Check 2: Plan P-ID format validation → /validate-plan-ids (new)
├─ Check 3: Cross-reference integrity → /audit-references (new)
├─ Check 4: Memory file sync → /sync-memory-indices (new)
└─ Report: Summary of all violations + suggested fixes
```

This becomes your single enforcement entry point, replacing scattered manual audits.

---

## Summary: The Real Problem

You have **good rules** but they're **inefficiently organized**.

jlacour-git's insight: At high rule density, compliance drops because the model has to re-infer what kind of instruction each one is on every response. By the time it gets to rule #8, it's dropped 30% of them.

Your path forward:
1. Consolidate scattered conventions into memory (saves ~500 tokens, zero compliance loss)
2. Move procedures from rules into skills (saves ~800 tokens, improves versioning)
3. Create explicit priority hierarchy (label each rule tier; improves conflict resolution)
4. Build enforcement skills (like you already did with `/move-docs-to-folders`) for each rule
5. Create master `/enforce-repo-cleanliness` skill as single entry point

**Result:** Cleaner, leaner rules + higher compliance + automated enforcement.
