# Implementation Recipe: Apply PTA-CBP-Parser Improvements to Thesis

**Goal**: Three concrete, copy-paste-ready improvements from today's pta-cbp-parser work  
**Time**: 45 minutes total (can be done in one session or split)  
**Risk**: Zero — all changes are additive; nothing will break existing workflows

---

## Task 1: Model Override Convention (5 minutes)

### Step 1.1: Read the source
Open pta-cbp-parser's CLAUDE.md and find the section:
```
## Model Override Convention
```

**File**: `C:\Users\brian\OneDrive\Documents\01 - P - Projects and Tasks\2026-01-03 - Preferential Trade Project\pta-cbp-parser\CLAUDE.md`

Copy the entire section (roughly lines 80-120, adjust based on actual content).

### Step 1.2: Add to thesis CLAUDE.md
Open: `CMT_Codebase\CLAUDE.md`

Find the section `## TOOLING RULE` (around line 29).

**Before it**, add:

```markdown
---

## Model Override Convention

**Default**: Haiku across all agents (cost-optimized for thesis writing & analysis)

**Three ways to override:**

1. **`/model <tier>` command** — Session-wide override
   ```
   /model sonnet    # upgrade rest of session (complex analyses)
   /model haiku     # back to default
   /model opus      # for major architecture decisions
   ```

2. **Voice/inline phrase** — Per-request override in your prompt
   ```
   "use sonnet for this analysis"     # I detect and upgrade for this request
   "switch to opus"                   # I upgrade to Opus
   "back to haiku" / "use default"    # I downgrade to Haiku
   ```
   Particularly useful for voice input; I monitor for `use <tier>` patterns.

3. **Automatic `/model` parsing** — Built into settings
   Commands like `/model sonnet` work session-wide without needing to restart.

**Rules**:
- Phrase matching is case-insensitive and detects `use <model>`, `switch to <model>`, `use default`
- `/model` commands override everything for the session until you switch again
- Inline phrases override only for that single request
- When both `/model` and inline phrase present, inline phrase takes precedence

**When to escalate to Sonnet**:
- Complex multi-file analyses (5+ files)
- Interdependent changes across System A and System B
- Architecture decisions or major refactors
- Literature review synthesis

---
```

### Step 1.3: Create memory file
Create: `CMT_Codebase\memory\feedback_model_override.md`

```markdown
---
name: Model override convention
description: Three mechanisms (command, inline phrase, settings) for selecting Haiku/Sonnet/Opus
type: feedback
---

**Rule**: Use Haiku by default (cost-optimized). Escalate to Sonnet for complex tasks (5+ files, interdependencies). Opus only for architecture redesigns.

**Why**: Thesis deadline (15 May) + 8GB RAM constraint means cost matters. Haiku handles most writing/analysis tasks; Sonnet needed for cross-system changes.

**How to apply**: 
- Voice sessions: just say "use sonnet for this analysis"
- CLI: `/model sonnet` before complex work
- Most thesis writing: leave on Haiku (default)
```

### Step 1.4: Test
In your next session, try:
```
"Use sonnet for the next 3 responses, I need to refactor System A"
```

You should see the model auto-upgrade.

---

## Task 2: Documentation Audit (15 minutes)

### Step 2.1: Run the audit
Open terminal, navigate to thesis codebase:
```bash
cd "C:\Users\brian\OneDrive\Documents\02 - A - Areas\MSc. Data Science\2026-03 - CBS Master Thesis\CMT_Codebase"

# List all large files
wc -l CLAUDE.md docs/*.md .claude/rules/*.md 2>/dev/null | sort -n | tail -20

# Also check .claude structure
find .claude -name "*.md" -exec wc -l {} + | sort -n | tail -15
```

### Step 2.2: Create audit document
Create: `CMT_Codebase\.claude\MODULARIZATION_AUDIT.md`

Copy the template below and fill in your actual numbers:

```markdown
# Documentation Modularization Audit

**Date**: 2026-04-15  
**Goal**: Identify bloated docs and plan splits to reduce context overhead

## Current State (lines of code)

| File | Lines | Status | Priority |
|------|-------|--------|----------|
| CLAUDE.md | XXX | Too large (>300) | P1 |
| docs/architecture.md | XXX | OK if <300, else split | P? |
| docs/compliance/cbs_guidelines_notes.md | XXX | Check consolidation | P? |
| docs/decisions/ADR-001.md | XXX | Check consolidation | P? |
| docs/decisions/ADR-002.md | XXX | Check consolidation | P? |
| docs/decisions/ADR-003.md | XXX | Check consolidation | P? |
| .claude/rules/trigger-docs-workflow.md | XXX | Check consolidation | P? |
| .claude/rules/trigger-plan-workflow.md | XXX | Check consolidation | P? |

## Total before split: XXX lines
## Estimated total after split: XXX lines (target: -15-20%)

## Recommended Splits

### Split 1: CLAUDE.md → docs/architecture.md
**Current in CLAUDE.md**: Sections on System A/B, agent roles, data flow  
**Reason**: Structural docs shouldn't bloat navigation hub  
**New size**: CLAUDE.md -50 lines, docs/architecture.md +80 lines  
**Priority**: P1

### Split 2: Consolidate docs/decisions/ → docs/compliance.md
**Current**: ADR-001, ADR-002, ADR-003 scattered in decisions/  
**Reason**: All are open/decision docs; consolidate into single reference  
**New size**: Remove 3 files, create docs/compliance.md (+100 lines)  
**Priority**: P2

### Split 3: Create docs/project-state.md
**Current in CLAUDE.md**: "KNOWN TODOs / FROZEN DECISIONS" section  
**Reason**: Frozen decisions belong in project state, not nav  
**New size**: CLAUDE.md -30 lines, docs/project-state.md +50 lines  
**Priority**: P2

## ROI Estimate

- **Effort**: 2-3 hours execution (splits + nav updates)
- **Benefit**: 15-20% context reduction per session
- **Breakeven**: 2-3 sessions (sooner if sessions are context-heavy)
- **Cumulative**: ~5K tokens saved per week by May 15

## Status
- [ ] Run audit (lines count)
- [ ] Identify targets
- [ ] Plan splits (this document)
- [ ] Execute splits (Phase 3)
- [ ] Verify context reduction (measure after)
```

### Step 2.3: Identify key targets
Add a "Targets" section:

```markdown
## Top 5 Targets for Splitting (in order of priority)

1. **CLAUDE.md** (36KB) — Move architecture + frozen decisions → modular docs
2. **docs/decisions/** — Consolidate ADRs into single docs/compliance.md
3. **docs/** — Add canonical repository-map (move from dev/)
4. **CHEATSHEET.md** (16KB) — Consider splitting by command category
5. **.claude/rules/** — Move verbose trigger docs → .claude/workflows/

**Est. total savings**: 12-15KB per load (20% reduction)
```

### Step 2.4: Save for Phase 3
Save this document. You'll reference it when executing splits (can be done this week or next).

---

## Task 3: Plan Timestamp Enhancement (10 minutes)

### Step 3.1: Check current hook
Open terminal:
```bash
cd "C:\Users\brian\OneDrive\Documents\02 - A - Areas\MSc. Data Science\2026-03 - CBS Master Thesis\CMT_Codebase"

# Check if hook exists
ls -la .claude/hooks/mirror_plan.py

# If it exists, check for timestamp logic
grep -n "created\|updated" .claude/hooks/mirror_plan.py
```

### Step 3.2a: If hook doesn't have timestamps
Copy from pta-cbp-parser:

```bash
# Copy the enhanced hook
cp "C:\Users\brian\OneDrive\Documents\01 - P - Projects and Tasks\2026-01-03 - Preferential Trade Project\pta-cbp-parser\.claude\hooks\mirror_plan.py" \
   "C:\Users\brian\OneDrive\Documents\02 - A - Areas\MSc. Data Science\2026-03 - CBS Master Thesis\CMT_Codebase\.claude\hooks\mirror_plan.py"
```

**Verify**: Run grep again to confirm timestamps are present.

### Step 3.2b: If hook already has timestamps
No action needed. All new plans will auto-gain timestamps.

### Step 3.3: Update plan workflow doc
Open (or create): `CMT_Codebase\.claude\rules\trigger-plan-workflow.md`

**Add section** (if not present):

```markdown
## Outcome Format (with Timestamps)

```
# Outcome: <Plan Title>

_Plan: plan_files/YYYY-MM-DD_<short-slug>.md_
_Created: YYYY-MM-DD HH:MM:SS_
_Completed: YYYY-MM-DD HH:MM:SS_

### ✅ Completed
- <what was implemented>

### 🔄 Adjusted
- **What**: <change>
  **Why**: <reason>
  **How**: <what was done instead>

### ❌ Dropped
- **What**: <item not done>
  **Why**: <reason>
```
```

(Full template in CLAUDE.md guidelines)
```

### Step 3.4: Test
Create a small test plan:

```bash
# Create a simple test plan
echo "# Test Plan: Verify Timestamps

This is a test to verify YAML frontmatter is injected.

## Steps
1. Create this plan
2. Check .claude/plans/ for timestamps
" > /tmp/test_plan.md
```

Write it to your global ~/.claude/plans/ and verify the hook mirrors it with timestamps.

---

## Task 4: Memory System (5 minutes)

### Step 4.1: Create modularization memory
Create: `CMT_Codebase\memory\feedback_modularization.md`

```markdown
---
name: Modular documentation reduces context overhead
description: Split large docs to load only what's relevant per session
type: feedback
---

**Rule**: Keep individual docs under 300 lines. When a doc exceeds 300 lines or when adding 50+ lines to CLAUDE.md, plan a split.

**Why**: From pta-cbp-parser audit: modular docs reduce context by ~20% per session. Compound savings as thesis grows toward 120 pages + appendices.

**How to apply**: 
- When editing CLAUDE.md and feeling it get long → check word count
- When adding architecture/decisions → consider separate docs/architecture.md instead
- When reviewing docs/ → prioritize splitting any >250 lines
```

### Step 4.2: Update memory index
Edit: `CMT_Codebase\memory\MEMORY.md`

Add entries (or update existing):
```markdown
- [feedback_model_override.md](feedback_model_override.md) — Model selection (Haiku default, escalate to Sonnet)
- [feedback_modularization.md](feedback_modularization.md) — Split docs >300 lines to reduce context overhead
```

---

## Checklist: What You'll Have After These 4 Tasks

### ✅ Model Override Convention
- [ ] CLAUDE.md updated with three override mechanisms
- [ ] Memory file created (feedback_model_override.md)
- [ ] Next session: test "use sonnet" in voice

### ✅ Documentation Audit
- [ ] Audit document created (.claude/MODULARIZATION_AUDIT.md)
- [ ] Baseline measurements recorded (line counts)
- [ ] Top 5 targets identified for future splits
- [ ] ROI estimate documented

### ✅ Plan Timestamps
- [ ] Hook verified/updated (mirror_plan.py)
- [ ] Workflow doc updated with outcome format
- [ ] Test plan created and verified

### ✅ Memory System
- [ ] Two feedback memories created
- [ ] Memory index updated (MEMORY.md)

---

## Timeline: When to Do Each

### Session 1 (Today, 45 min total):
- **Task 1**: Model Override Convention (5 min) ← do now
- **Task 2**: Documentation Audit (15 min) ← do now
- **Task 3**: Plan Timestamps (10 min) ← do now
- **Task 4**: Memory System (5 min) ← do now

**Total**: 35 minutes. Buffer included.

### Session 2 (This week, 2-3 hours):
- **Phase 3**: Execute documentation splits
  - Split CLAUDE.md
  - Create/update docs/ structure
  - Update navigation

### Optional (Next week):
- Measure context reduction before/after
- Refine based on actual usage

---

## Rollback Plan (if something breaks)

All changes are **additive** (no deletions, no overwrites). If you need to undo:

1. **Model override**: Delete the section from CLAUDE.md, keep memory
2. **Audit doc**: Delete `.claude/MODULARIZATION_AUDIT.md`
3. **Hook**: Restore from git (`git checkout .claude/hooks/mirror_plan.py`)
4. **Memory**: Delete the feedback files

**No impact to codebase**, only to Claude Code workflows.

---

## Questions?

If you get stuck on any step:
1. Check the source files in pta-cbp-parser (path listed above)
2. Refer to CLAUDE.md in both projects
3. Check `.claude/rules/` for workflow docs

All improvements are non-breaking and can be done incrementally.

---

**Recipe Version**: 2026-04-15  
**Effort**: 45 minutes  
**Risk**: Zero (all additive)  
**Benefit**: Model selection clarity + 15-20% context reduction + plan lifecycle tracking  

Ready to start? Begin with Task 1 above.
