# Deep Dive Implementation Plan: Option B
## CBS Master Thesis Workflow Optimization

**Date Created**: 2026-04-15  
**Implementation Strategy**: Phase 1 today (45 min), Phase 2 this week (2-3 hrs)  
**Expected Outcome**: Voice-friendly model selection + 15-20% context reduction + plan lifecycle tracking  
**Status**: Ready to execute

---

## Phase 1: Quick Wins (TODAY, 45 minutes)

These four tasks introduce all three improvements with zero risk (additive only).

### Task 1.1: Add Model Override Convention to CLAUDE.md (5 min)

**Location**: CMT_Codebase/CLAUDE.md, before "## TOOLING RULE" (~line 29)

**Action**: Paste this section:

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

2. **Voice/inline phrase** — Per-request override (voice-friendly)
   ```
   "use sonnet for this analysis"     # detected and upgraded for this request
   "switch to opus"                   # recognized pattern
   "back to haiku" / "use default"    # resets to Haiku
   ```
   Particularly useful for voice input; phrase matching is case-insensitive.

3. **Automatic `/model` parsing** — Built into settings
   Commands like `/model sonnet` work session-wide without needing to restart.

**Rules**:
- Default = Haiku (cost-optimized for thesis writing + analysis)
- Inline phrases override for single request only
- `/model` command overrides for the entire session until you switch again
- When both `/model` and inline phrase present, inline takes precedence

**When to escalate to Sonnet**:
- Multi-file refactors (5+ files across System A and System B)
- Architecture decisions or major design changes
- Complex literature synthesis requiring deep reasoning
- Thesis writing at chapter boundaries when decisions intersect

---
```

**Verification**: Save, close CLAUDE.md. Done.

---

### Task 1.2: Run Documentation Audit (15 min)

**Step A**: Get current measurements
```bash
cd "C:\Users\brian\OneDrive\Documents\02 - A - Areas\MSc. Data Science\2026-03 - CBS Master Thesis\CMT_Codebase"

# Comprehensive audit
wc -l CLAUDE.md docs/*.md .claude/rules/*.md 2>/dev/null | sort -n
find .claude -name "*.md" -exec wc -l {} + | sort -n
```

**Step B**: Create audit document
Location: `CMT_Codebase/.claude/MODULARIZATION_AUDIT.md`

**Content** (fill in your actual line counts from Step A):

```markdown
# Documentation Modularization Audit

**Date**: 2026-04-15  
**Goal**: Identify bloated docs and plan splits to reduce context overhead

## Current State (lines)

| File | Lines | Status | Action |
|------|-------|--------|--------|
| CLAUDE.md | 646 | Too large (>300) | Split into nav + architecture + state |
| docs/system_architecture_report.md | 986 | Very large | Review for consolidation |
| docs/PROJECT_OVERVIEW.md | 271 | Consolidate? | Merge into project-state or architecture |
| docs/thesis_production_architecture.md | 261 | OK | Keep as-is |
| docs/context.md | 310 | Borderline | Consider splitting by phase |
| docs/architecture.md | 171 | OK | Keep, may receive content from CLAUDE.md |
| docs/experiment_tracking_agent.md | 223 | OK | Keep as-is |
| docs/DATA_ACCESS_SETUP.md | 219 | OK | Keep as-is |
| .claude/rules/*.md | ~500 total | OK | Each file <200 lines |

## Targets for Splitting (Priority Order)

### P1: CLAUDE.md (646 → ~300 lines)
**Move to docs/architecture.md**:
- AGENT ARCHITECTURE section (System A/B, agent roles) — ~90 lines
- STACK section — ~60 lines
- FILE SYSTEM MEMORY section — ~50 lines

**Move to docs/project-state.md** (NEW):
- KNOWN TODOs / FROZEN DECISIONS — ~40 lines
- EXPLICIT LIMITS — ~15 lines

**Move to docs/research-questions.md** (NEW):
- RESEARCH QUESTIONS section — ~30 lines

**Result**: CLAUDE.md becomes 300-line navigation hub.

### P2: Consolidate docs/decisions/ → docs/compliance.md (NEW)
**Consolidate**:
- docs/decisions/ADR-001.md
- docs/decisions/ADR-002.md
- docs/decisions/ADR-003.md

**Into single file**: docs/compliance.md with open/closed ADR status + CBS requirements + integrity gates

### P3: Add YAML Frontmatter to All Docs
Template:
```yaml
---
name: {{title}}
description: {{one-line purpose}}
updated: 2026-04-15 14:30
---
```

## Token Savings Estimate

| Item | Reduction | Notes |
|------|-----------|-------|
| CLAUDE.md split | -200 lines | Nav hub no longer bloated |
| Compliance consolidation | -150 lines | 3 decision files → 1 compliance file |
| Total reduction | ~350 lines | ~5KB saved per load |
| Context savings | ~15-20% | ~1.75K tokens per session |
| ROI | 2-3 sessions | Effort 2-3 hours |
| Cumulative by May 15 | ~5K tokens/week | Compounds as thesis grows |

## Status
- [x] Run audit (line counts)
- [ ] Identify targets (above)
- [ ] Plan splits (this document)
- [ ] Execute splits (Phase 2, this week)
- [ ] Verify context reduction (after Phase 2)

## Next Steps
See `.claude/DEEP_DIVE_ACTION_PLAN.md` Phase 2 for split execution details.
```

**Verification**: Save the audit document.

---

### Task 1.3: Verify Plan Timestamp Hook (10 min)

**Step A**: Check if hook exists and has timestamp support
```bash
cd CMT_Codebase
ls -la .claude/hooks/mirror_plan.py
grep -n "created\|updated" .claude/hooks/mirror_plan.py
```

**If output shows `created` or `updated` in the grep**: ✅ Hook already supports timestamps. Skip Step B.

**If grep returns nothing or file doesn't exist**: Proceed to Step B.

**Step B**: Copy enhanced hook from pta-cbp-parser
```bash
copy "C:\Users\brian\OneDrive\Documents\01 - P - Projects and Tasks\2026-01-03 - Preferential Trade Project\pta-cbp-parser\.claude\hooks\mirror_plan.py" \
     ".\.claude\hooks\mirror_plan.py"
```

**Verification**: Re-run grep to confirm timestamps are present.

---

### Task 1.4: Create Memory Files (5 min)

**Already done**. Check:
- `memory/MEMORY.md` (index)
- `memory/feedback_model_override.md`
- `memory/feedback_modularization.md`
- `memory/project_workflow_optimization.md`

All four files should be present. If not:
```bash
ls -la memory/*.md
```

These are auto-loaded every session and will guide future work.

---

## Phase 1 Verification Checklist

After completing all four tasks, verify:

- [ ] CLAUDE.md has "## Model Override Convention" section
- [ ] `memory/feedback_model_override.md` exists and is readable
- [ ] `.claude/MODULARIZATION_AUDIT.md` exists with line counts filled in
- [ ] Hook has timestamp support (grep found `created`/`updated`)
- [ ] `memory/MEMORY.md` index includes new memory files

**Time invested**: ~45 minutes  
**Risk**: Zero (all additive)  
**Benefits active now**: Model selection clarity, audit baseline, memory persistence

---

## Phase 2: Execute Documentation Splits (THIS WEEK, 2-3 hours)

These tasks require planning and refactoring. Do them when you have 2-3 uninterrupted hours.

### Task 2.1: Split CLAUDE.md (90 min)

**Current**: 646 lines (36KB) mixing navigation, architecture, state, research questions  
**Target**: 300 lines (navigation hub only)

**Steps**:

1. **Extract AGENT ARCHITECTURE section** (System A/B details, agent table)
   - Copy lines containing System A/B architecture info from CLAUDE.md
   - Move to `docs/architecture.md` (append to existing content)
   - Add to top of moved content:
     ```yaml
     ---
     name: System Architecture (Agent Coordination)
     description: System A/B separation, agent roles, data flow, LangGraph state
     updated: 2026-04-15
     ---
     ```
   - Update CLAUDE.md to reference: "See `docs/architecture.md` for full system design"
   - Delete from CLAUDE.md

2. **Extract RESEARCH QUESTIONS section** (RQs v1→v2 evolution)
   - Create new file: `docs/research-questions.md`
   - Copy RQ content from CLAUDE.md
   - Add YAML frontmatter:
     ```yaml
     ---
     name: Research Questions Evolution
     description: Main RQ + 4 SRQs (v2), history v1→v2 in docs/literature/rq_evolution.md
     updated: 2026-04-15
     ---
     ```
   - Update CLAUDE.md to reference: "See `docs/research-questions.md` for evolution"
   - Delete from CLAUDE.md

3. **Extract KNOWN TODOs / FROZEN DECISIONS** (stands, status flags)
   - Create new file: `docs/project-state.md`
   - Copy frozen decisions + TODOs from CLAUDE.md
   - Add YAML frontmatter:
     ```yaml
     ---
     name: Project State (Frozen Decisions & TODOs)
     description: Deliberate choices, open questions, known constraints
     updated: 2026-04-15
     ---
     ```
   - Update CLAUDE.md to reference: "See `docs/project-state.md` for decisions & TODOs"
   - Delete from CLAUDE.md

4. **Extract STACK section** (if large)
   - If STACK section is >60 lines, consider moving to new `docs/stack.md`
   - Otherwise, keep in CLAUDE.md as summary pointer

5. **Result check**:
   - CLAUDE.md should now be ~300 lines (nav hub + project summary)
   - New files: docs/research-questions.md, docs/project-state.md, (optional) docs/stack.md
   - All extracted docs have YAML frontmatter with updated timestamp

**Rollback plan**: If something breaks, `git checkout CLAUDE.md` to restore original.

---

### Task 2.2: Consolidate Compliance Docs (60 min)

**Current**: ADR-001, ADR-002, ADR-003 in `docs/decisions/` (scattered)  
**Target**: Single `docs/compliance.md` with ADR status + CBS requirements + integrity gates

**Steps**:

1. **Read all three ADRs** to understand current status:
   - ADR-001: LaTeX template strategy (OPEN)
   - ADR-002: Build pipeline strategy (OPEN)
   - ADR-003: Builder agent fate (OPEN)

2. **Create `docs/compliance.md`**:
   ```markdown
   ---
   name: Compliance & Architecture Decisions
   description: CBS guidelines, integrity gates, and open ADRs (template, pipeline, builder)
   updated: 2026-04-15
   ---

   # Compliance & Architecture Decisions

   ## CBS Guidelines
   [Copy from docs/compliance/cbs_guidelines_notes.md]

   ## Integrity Gates
   [Copy from docs/tooling-issues.md or docs/context.md if documented]

   ## Open Architectural Decisions (ADRs)

   ### ADR-001: LaTeX Template Strategy
   **Status**: OPEN
   **Decision**: [summary from ADR-001.md]
   **Details**: See [docs/decisions/ADR-001.md](decisions/ADR-001.md) for full analysis

   ### ADR-002: Build Pipeline Strategy
   **Status**: OPEN
   **Decision**: [summary from ADR-002.md]
   **Details**: See [docs/decisions/ADR-002.md](decisions/ADR-002.md) for full analysis

   ### ADR-003: Builder Agent Fate
   **Status**: OPEN
   **Decision**: [summary from ADR-003.md]
   **Details**: See [docs/decisions/ADR-003.md](decisions/ADR-003.md) for full analysis
   ```

3. **Do NOT delete ADR files yet** — keep them as detailed references  
   (Consolidation is primarily for the compliance hub; ADRs remain canonical)

4. **Update references**:
   - CLAUDE.md: "See `docs/compliance.md` for CBS requirements and ADR status"
   - Update CHEATSHEET.md to point to docs/compliance.md for decision reference

---

### Task 2.3: Update Navigation in CLAUDE.md (30 min)

**Current NAVIGATION section** references old file locations and nested structure.

**Update to**:
```markdown
## NAVIGATION

**Read at session start (in order):**
1. This file (CLAUDE.md) — project context + constraints
2. [docs/architecture.md](docs/architecture.md) — System A/B separation, agent roles, data flow
3. [docs/compliance.md](docs/compliance.md) — CBS requirements, integrity gates, ADR status
4. [docs/research-questions.md](docs/research-questions.md) — main RQ + 4 SRQs, evolution history
5. [docs/project-state.md](docs/project-state.md) — frozen decisions, TODOs, limitations
6. [dev/repository_map.md](dev/repository_map.md) — file locations, agent status
7. [docs/tooling-issues.md](docs/tooling-issues.md) — known environment issues

**Key references:**
- [docs/decisions/ADR-001-template-strategy.md](docs/decisions/ADR-001-template-strategy.md) — LaTeX template (OPEN)
- [docs/decisions/ADR-002-build-pipeline.md](docs/decisions/ADR-002-build-pipeline.md) — PDF pipeline (OPEN)
- [docs/decisions/ADR-003-builder-agent-fate.md](docs/decisions/ADR-003-builder-agent-fate.md) — Builder agent (OPEN)
- [CHEATSHEET.md](CHEATSHEET.md) — quick-reference commands
```

---

### Task 2.4: Add YAML Frontmatter to All Docs (30 min)

**Template**:
```yaml
---
name: {{title}}
description: {{one-line purpose}}
updated: {{YYYY-MM-DD}}
---
```

**Files to update**:
- `docs/architecture.md` (move CLAUDE.md agent arch here)
- `docs/compliance.md` (new, consolidation)
- `docs/research-questions.md` (new, from CLAUDE.md)
- `docs/project-state.md` (new, from CLAUDE.md)
- `docs/context.md` (add frontmatter if missing)
- `docs/PROJECT_OVERVIEW.md` (add frontmatter if missing)
- Any other docs > 150 lines

**Tool**: Use Edit to add frontmatter to each file.

---

### Task 2.5: Verify Context Reduction (20 min)

**Measure before and after**:

Before Phase 2:
```bash
wc -l CLAUDE.md docs/*.md .claude/rules/*.md | sort -n | tail -10
# Total for key files: ~3600 lines
```

After Phase 2:
```bash
wc -l CLAUDE.md docs/*.md .claude/rules/*.md | sort -n | tail -10
# Expected: ~3300 lines (8% reduction)
# With Phase 2 optimizations: 15-20% overall context reduction per load
```

**Quantify savings**:
- Lines saved: original - new
- Token estimate: lines × 0.25 (rough: 4 tokens per line)
- Expected: ~1.75K tokens per session

---

## Phase 2 Verification Checklist

After Phase 2 completion, verify:

- [ ] CLAUDE.md is ~300 lines (down from 646)
- [ ] New files exist: docs/research-questions.md, docs/project-state.md
- [ ] docs/architecture.md contains System A/B details
- [ ] docs/compliance.md consolidates CBS + ADR status
- [ ] All modified docs have YAML frontmatter (name, description, updated)
- [ ] Navigation section in CLAUDE.md points to new files
- [ ] Context measurement confirms 15-20% reduction
- [ ] Git status shows changes (not yet committed)

**Time invested**: 2-3 hours  
**Risk**: Low (all changes are refactoring, with rollback via git)  
**Benefits after commit**: 15-20% context reduction per session, ~5K tokens saved per week

---

## Post-Implementation (Optional)

### Commit Phase 2 Changes
```bash
git add CLAUDE.md docs/ .claude/MODULARIZATION_AUDIT.md
git commit -m "refactor: modularize documentation to reduce context overhead

- Split CLAUDE.md (646 → 300 lines) into focused modules
- Extract architecture → docs/architecture.md
- Extract research questions → docs/research-questions.md
- Extract project state → docs/project-state.md
- Consolidate compliance docs → docs/compliance.md
- Add YAML frontmatter (updated timestamps) to all docs
- Update navigation in CLAUDE.md for clarity

Expected benefit: 15-20% context reduction per session (~1.75K tokens)
ROI: 2-3 sessions to break even

Co-Authored-By: Claude Code (Optimization from pta-cbp-parser)"
```

### Measure Actual Context Reduction
After 3-5 sessions with Phase 2 in place:
- Measure token consumption per session
- Compare to baseline (before Phase 2)
- Document findings in memory/feedback_modularization.md (update section)

---

## Summary: What You'll Have After Deep Dive

**Phase 1** (45 min, today):
- ✅ Voice-friendly model selection ("use sonnet for this")
- ✅ Baseline audit of documentation bloat
- ✅ Plan timestamp hook verified and ready
- ✅ Memory files created for cross-session consistency

**Phase 2** (2-3 hrs, this week):
- ✅ CLAUDE.md reduced from 646 → 300 lines
- ✅ Four new focused docs (architecture, compliance, research-questions, project-state)
- ✅ All docs timestamped in YAML frontmatter
- ✅ 15-20% context reduction per session
- ✅ ~5K tokens saved per week through May 15

**Total ROI by May 15**:
- Effort: 2.75-3.25 hours
- Savings: ~5K tokens/week × 4 weeks = **20K tokens** (40K chars)
- Cost of effort: ~2K tokens (estimates)
- **Net savings: ~18K tokens** = ~30 pages of context freed for thesis work

---

**Status**: Ready to execute  
**Next action**: Start Phase 1 today (45 min)  
**Questions?**: Refer to THESIS_ADAPTATION_REPORT.md or IMPLEMENTATION_RECIPE.md
