# Rule System Reform: Implementation Roadmap

**Status:** Planning phase  
**Context:** Rule system audit complete (see `rule-reform-gaps.md`)  
**Goal:** Enforce-able, concise, effective rules with zero behavioral coverage loss

---

## Executive Summary

Your rule system has good foundations but suffers from **instruction fatigue** (too many rule files) and **scattered procedures** (should be in skills, not rules).

**Target state:**
- **4 core rules** in `.claude/rules/` (Trust tier only)
- **7 conventions** in memory (facts about your project)
- **5 enforcement skills** (automate rule compliance)
- **1 master skill** `/enforce-repo-cleanliness` (orchestrate all checks)

**Token savings:** ~1,200 tokens in rules + memory consolidation  
**Compliance improvement:** Reduced instruction fatigue, explicit priority hierarchy

---

## Phase 1: Reclassify Existing Rule Files

### Task 1.1: Audit Each Rule File

| File | Classification | Action | New Home | Notes |
|---|---|---|---|---|
| `trigger-branch-strategy.md` | RULE | Keep + compress | `.claude/rules/` | Trust tier; hook enforcement exists |
| `root-documentation-boundary.md` | RULE + ROUTING | Keep + compress | `.claude/rules/` | Trust tier; `/move-docs-to-folders` enforces |
| `one-off-execution.md` | RULE | Keep (brief) | `.claude/rules/` | Efficiency tier; already concise |
| `trigger-plan-workflow.md` | RULE + PROCEDURE | Split | `.claude/rules/` + `.claude/skills/` | Extract procedure → `/plan-workflow` skill |
| `plan-documentation-structure.md` | CONVENTION + ROUTING | Merge + consolidate | Memory + routing file | Consolidate with `trigger-plan-workflow.md` |
| `trigger-git-commit-workflow.md` | PROCEDURE | Move | `.claude/skills/git-draft-commit/` | Move to skill SKILL.md |
| `trigger-docs-workflow.md` | PROCEDURE | Move | `.claude/skills/docs-update-all/` | Move to skill SKILL.md |
| `context-token-optimization.md` | CONVENTION | Move | `memory/` | Create `convention_model_selection.md` |
| `worktree-workflow.md` | CONVENTION | Move | `memory/` | Create `convention_worktree_organization.md` |
| `repository-map-reference.md` | PROCEDURE (pre-check) | Move | Memory checklist | Create `checklist_consult_map.md` |
| `tooling-issues-workflow.md` | CONVENTION + ROUTING | Split | Memory + tooling docs | Move workflow to skill; convention to memory |

### Task 1.2: Create Consolidated Conventions File

**File:** `C:\Users\brian\.claude\projects\C--dev-thesis-manifold\memory\convention_project_standards.md`

**Contents:**
- Model selection (Haiku default, Sonnet for multi-file, Opus for architecture)
- Worktree organization (worktrees/ directory, gitignored)
- Plan P-ID naming (P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug})
- JSONL/markdown authority (JSONL authoritative, markdown derived)
- Repository map consultation checklist

**Example format:**
```markdown
---
name: Project Standards & Conventions
type: convention
---

## Model Selection
Use Haiku by default (cost-optimized).
Upgrade to Sonnet for multi-file refactors, chapter editing.
Use Opus for architecture decisions, literature synthesis.

## Worktree Organization
Worktrees live at `worktrees/` directory (root level).
Each session = one worktree (isolation).
Gitignored; safe to create/delete.

## Plan Naming Convention
Format: P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}
- P{NNNN}: Unique sequential ID (P0001, P0002, ...)
- YYYY-MM-DD: ISO date (plan creation date)
- HHMM: 24hr time (use 0800 default for undated)
- slug: lowercase, hyphens (e.g., jupyter-path-cleanup)
```

---

## Phase 2: Compress Rules (Scenario Testing)

### Task 2.1: Scenario Test `root-documentation-boundary.md`

**Current:** 126 lines  
**Target:** ~85 lines (-33%)

**Test protocol:**

For each phrase, ask: "Is there a scenario where this phrase catches a mistake but a shorter version wouldn't?"

**Example compression:**

**Original phrase (line 27-35):**
```
## Whitelist (Allowed at Root)

These files MUST stay at root for discoverability and project initialization:

- **CLAUDE.md** — Project instructions & workflows (entry point for Claude Code sessions)
- **INDEX.md** — Repository index & navigation hub
- **paths.py** — Centralized path configuration (Python executable)
- **README.md** — Project overview & setup (discoverable by any developer)
- **requirements.txt** — Dependencies manifest
```

**Scenario test:** User creates SETUP.md at root. Does shortened version catch this?
- Original says "THESE FILES MUST STAY" (explicit whitelist) → catches it
- Shortened to just the list → might miss it if user thinks "setup is kind of foundational"

**Verdict:** Keep full list + rationale, compress rationale phrases instead.

**Compressed version:**
```
## Whitelist (Allowed at Root)

- **CLAUDE.md** — Project instructions & workflows
- **INDEX.md** — Navigation hub
- **paths.py** — Centralized path configuration
- **README.md** — Project overview & setup
- **requirements.txt** — Dependencies manifest
```

**Compression done:** Removed "entry point", "discoverable by any developer" (redundant context)

### Task 2.2: Scenario Test `trigger-branch-strategy.md`

**Current:** 78 lines  
**Target:** ~55 lines (-29%)

**Focus:** Remove verbose examples, keep edge cases

---

## Phase 3: Move Procedures to Skills

### Task 3.1: Move `trigger-git-commit-workflow.md` → `/git-draft-commit` SKILL.md

**Current state:**
- Rule file: `.claude/rules/trigger-git-commit-workflow.md` (79 lines, procedure)
- Skill: `.claude/skills/git-draft-commit/SKILL.md` (exists but brief)

**Action:**
1. Extract workflow steps from rule file
2. Paste into skill SKILL.md (with code examples)
3. Delete rule file
4. Update CLAUDE.md to reference skill instead of rule

**New SKILL.md structure:**
```markdown
# Git Draft Commit Workflow

## How It Works

### Pre-step: Branch Check
Run `git branch --show-current` to verify feature branch.
If on main, prompt user to create branch first.

### Step 1: Log Tooling Issues
Invoke `/log_errors` skill to scan session for tooling problems.
Append any findings to `docs/tooling-issues.md`.

### Step 2: Gather Session Context
Review conversation for files changed & why.
Look for standup entries (HH-MM-SS format) in `project_updates/standup_draft.md`.

### Step 3: Check Git Status
Run `git status --short` to confirm changed files on disk.
Run `git log -1 --format="%H %ai %s"` to find cutoff point for uncommitted work.

### Step 4: Draft Message
Format:
\`\`\`
<type>: <subject> (≤60 chars)

- <what changed and why, one line per logical unit>
- ...

Sessions: HH-MM-SS (timestamps from standup entries)
\`\`\`

Types: feat, fix, refactor, chore, docs

### Step 5: Present for Approval
Show message in code block (copy-paste ready).
Flag if standup entries were ambiguous or files have no session record.
```

### Task 3.2: Move `trigger-docs-workflow.md` → `/docs-update-all` SKILL.md

Same pattern as 3.1.

**Order to document:**
1. Thesis sections → if bullet/outline changes
2. Compliance notes → if checks ran
3. CLAUDE.md → if structure/rules changed
4. README.md → if setup/behavior changed
5. Plans → if plan executed
6. Rules → if references staled

---

## Phase 4: Add Priority Hierarchy Labels

### Task 4.1: Create `rule-priority-hierarchy.md`

**File:** `.claude/rules/rule-priority-hierarchy.md`

**Contents:**
```markdown
# Rule Priority Hierarchy

When rules conflict, resolve by tier (top tier always wins):

## Trust (Never Yield)
- Branch strategy: No commits on main
- Root documentation boundary: Analysis docs not at root

## Correctness (Yield only to Trust)
- Plan outcome discipline: No outcome file = plan not done

## Quality (Yield to Trust + Correctness)
- One-off execution default: Don't schedule recurring tasks without explicit interval

## Efficiency (Yields to all)
(Reserve for future rules that optimize performance)

---

## How to Apply

When in doubt, check this list. Trust rules always override Efficiency rules.
```

### Task 4.2: Update CLAUDE.md "Rules (TL;DR)" Section

Change from flat list to tiered:

```markdown
## Rules (Tiered Priority)

**TRUST (non-negotiable):**
- No commits on `main` — each session gets worktree + branch
- Analysis docs not at root — use `/move-docs-to-folders` to enforce

**CORRECTNESS:**
- Plan outcomes required — no outcome file = plan not done

**QUALITY:**
- Execute immediately by default — don't use `/loop` unless interval specified

See `.claude/rules/rule-priority-hierarchy.md` for conflict resolution.
```

---

## Phase 5: Build Enforcement Skills

You already have `/move-docs-to-folders`. Build these next:

### Task 5.1: `/validate-plan-ids` Skill

**Purpose:** Enforce P-ID naming convention (P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug})

**Function:**
```
/validate-plan-ids
├─ Scan plans/ directory
├─ Check each folder against P-ID regex
├─ Flag misnamed folders
├─ Suggest corrections
└─ (Optional) Rename with confirmation
```

**When to trigger:** Before committing plan work, as part of `/enforce-repo-cleanliness`

### Task 5.2: `/audit-plan-outcomes` Skill

**Purpose:** Verify every plan in 02-in_progress-plans has corresponding outcome file in 03-outcome_plans

**Function:**
```
/audit-plan-outcomes
├─ List all plans in 02-in_progress-plans/
├─ Check 03-outcome_plans/ for matching outcome files
├─ Flag missing outcomes
├─ Summarize completion rate
```

### Task 5.3: `/audit-cross-references` Skill

**Purpose:** Verify CLAUDE.md, README.md, PLANS_INDEX.md link to correct paths

**Function:**
```
/audit-cross-references
├─ Scan CLAUDE.md for file links
├─ Check each file exists at path
├─ Flag broken references
├─ Suggest correct paths
```

### Task 5.4: `/sync-memory-indices` Skill

**Purpose:** Verify MEMORY.md index matches files in memory/ directory

**Function:**
```
/sync-memory-indices
├─ List all .md files in memory/
├─ Check each is referenced in MEMORY.md
├─ Flag orphaned files or missing entries
├─ Suggest additions to MEMORY.md
```

---

## Phase 6: Build Master Enforcement Skill

### Task 6.1: Create `/enforce-repo-cleanliness` Skill

**File:** `.claude/skills/enforce-repo-cleanliness/SKILL.md`

**Function:**
```
/enforce-repo-cleanliness
├─ Check 1: `/move-docs-to-folders` — Root doc violations
├─ Check 2: `/validate-plan-ids` — P-ID naming
├─ Check 3: `/audit-plan-outcomes` — Missing outcomes
├─ Check 4: `/audit-cross-references` — Broken links
├─ Check 5: `/sync-memory-indices` — Memory coherence
└─ Report: Summary + violations + suggested fixes
```

**Usage:**
```
/enforce-repo-cleanliness
```

**Output:**
```
================================================================================
Repository Cleanliness Report
================================================================================

Check 1: Root Documentation Boundary
  Status: ✓ PASS
  Root files: CLAUDE.md, README.md, paths.py, requirements.txt, INDEX.md
  
Check 2: Plan P-ID Naming
  Status: ✗ FAIL (1 violation)
  ✗ plans/02-in_progress-plans/preprocessing-unification/ (missing P-ID)
     → Suggest: P0019_2026-05-04_1400_PLAN-preprocessing-unification

Check 3: Plan Outcome Completeness
  Status: ⚠ WARNING (2 missing)
  ⚠ P0017 (in progress since 2026-04-27) — missing outcome
  ⚠ P0018 (in progress since 2026-04-28) — missing outcome

Check 4: Cross-Reference Integrity
  Status: ✓ PASS
  Checked: CLAUDE.md (12 refs), README.md (8 refs), PLANS_INDEX.md (18 refs)

Check 5: Memory Index Coherence
  Status: ✓ PASS
  Memory files: 14 documented, 14 files found

Summary:
  Overall: 2 failures, 2 warnings
  Action: Rename plan folder, create outcome files, review plan status

================================================================================
```

---

## Phase 7: Update CLAUDE.md Navigation

### Task 7.1: Reorganize Rules Section

**Before:**
```
- **Model**: Haiku by default | Upgrade with `/model sonnet`...
- **Python files**: Never Edit/Write...
- **Tools**: Read, Grep, Glob...
- **Thesis**: Bullets only...
- **Every phase transition**: Requires explicit human approval
- **Git**: Each session gets its own worktree...
```

**After:**
```
**CORE RULES (Trust Tier):**
- No commits on `main` — isolated branch per session
- Analysis docs not at root — use `/move-docs-to-folders` to enforce

**COMPLIANCE (Correctness Tier):**
- Plan outcomes required — no outcome file = plan not done

**CONVENTIONS & FACTS:**
See `memory/` for: model selection, worktree organization, plan naming, etc.

**ENFORCEMENT SKILLS:**
- `/enforce-repo-cleanliness` — Master audit (all checks)
- `/move-docs-to-folders` — Root documentation cleanup
- `/validate-plan-ids` — Plan naming convention
- `/audit-plan-outcomes` — Plan completion tracking
```

---

## Implementation Checklist

### Pre-Implementation
- [ ] Read `docs/reference/rule-reform-gaps.md` (gap analysis)
- [ ] Approve phase sequence
- [ ] Assign reviewer (for cross-validation)

### Phase 1: Reclassify
- [ ] Complete audit table (Task 1.1)
- [ ] Create memory files (Task 1.2)
- [ ] Verify MEMORY.md index updated

### Phase 2: Compress
- [ ] Scenario test `root-documentation-boundary.md` (Task 2.1)
- [ ] Scenario test `trigger-branch-strategy.md` (Task 2.2)
- [ ] Compress remaining rules

### Phase 3: Move Procedures
- [ ] Move git-commit workflow to skill (Task 3.1)
- [ ] Move docs-workflow to skill (Task 3.2)
- [ ] Update skill SKILL.md files

### Phase 4: Hierarchy
- [ ] Create priority hierarchy file (Task 4.1)
- [ ] Update CLAUDE.md (Task 4.2)
- [ ] Verify no conflicting instructions

### Phase 5: Enforcement
- [ ] Build `/validate-plan-ids` (Task 5.1)
- [ ] Build `/audit-plan-outcomes` (Task 5.2)
- [ ] Build `/audit-cross-references` (Task 5.3)
- [ ] Build `/sync-memory-indices` (Task 5.4)

### Phase 6: Master Skill
- [ ] Create `/enforce-repo-cleanliness` (Task 6.1)
- [ ] Test against actual repo state
- [ ] Document in CLAUDE.md

### Phase 7: Navigation
- [ ] Update CLAUDE.md rules section (Task 7.1)
- [ ] Update README if needed
- [ ] Verify all cross-references

### Final Validation
- [ ] Run `/enforce-repo-cleanliness` against live repo
- [ ] Verify no broken links
- [ ] Check memory indices coherence
- [ ] Create commit with all changes

---

## Success Criteria

✓ Rules reduced from ~10 files to 4 core files  
✓ Conventions consolidated in memory (1 file)  
✓ Procedures moved to skills (5 updated SKILL.md files)  
✓ Priority hierarchy explicit and documented  
✓ Enforcement skills operational and integrated  
✓ CLAUDE.md updated with new navigation  
✓ Zero behavioral coverage lost (scenario testing passed)  
✓ Token savings: ~1,200 tokens in rules  

---

## Next Step

Which phase should we start with? I recommend:
1. **Phase 1** (reclassify) — Reveals exact scope
2. **Phase 2** (compress) — Quick wins, token savings
3. **Phases 3-4** (move procedures, add hierarchy) — Structural fixes
4. **Phases 5-7** (enforcement, navigation) — Complete picture

Ready to begin?
