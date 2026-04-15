# Workflow Improvements: PTA-CBP-Parser → CMT Thesis Codebase
**Date**: 2026-04-15  
**Source**: Today's improvements in pta-cbp-parser (4 commits, 3 major workflow enhancements)  
**Target**: CMT_Codebase (apply learnings and patterns)

---

## Executive Summary

Today's work in pta-cbp-parser focused on **three critical improvements**:
1. **Model Override Convention** — systematic approach to using Haiku/Sonnet/Opus
2. **Modularization & Token Efficiency** — split bloated docs into focused modules
3. **Automatic Plan Mirroring + Timestamps** — plan lifecycle tracking with zero manual steps

**Impact**: Reduced context overhead by ~58%, improved plan traceability, enabled voice-friendly model switching.

**Thesis Codebase Status**: Thesis has rudimentary versions of items 1-3 but they're **scattered, incomplete, and not optimized**. Suggested action: systematically upgrade each area.

---

## 1. Model Override Convention

### What We Did (pta-cbp-parser)
**Commit**: `133dc37` — "docs: add model override convention"

Documented **three model-override mechanisms** in `CLAUDE.md`:

```
1. /model <tier> command          → session-wide override (e.g., /model sonnet)
2. Inline phrase detection       → per-request override (e.g., "use sonnet for this plan")
3. Settings-based parsing        → automatic detection, no restart needed
```

**Why it matters**:
- Default Haiku (cost-optimized) but escalate to Sonnet for complex tasks
- Voice input friendly: just say "use sonnet" instead of remembering slash commands
- Saved to memory (`feedback_model_override.md`) for cross-session consistency

### How to Adapt to Thesis Codebase

**Current state**: CLAUDE.md mentions model selection vaguely; no documented convention.

**Action**:
1. Read pta-cbp-parser's documented convention at:
   - `CLAUDE.md` (search "Model Override Convention")
   - `.claude/rules/context-token-optimization.md` (Task Scope Classification table)

2. Copy the pattern into CMT CLAUDE.md:
   ```markdown
   ## Model Override Convention
   
   **Default**: Haiku (cost-optimized, thesis writing + analysis)
   
   **Three ways to override:**
   
   1. `/model <tier>` — session-wide override
   2. Inline phrase — per-request (`use sonnet for this analysis`)
   3. Settings parsing — automatic, no restart
   ```

3. Link to `.claude/rules/context-token-optimization.md` (which already exists in thesis codebase!)

4. Save memory: create `memory/feedback_model_override.md` (mirror pta-cbp-parser's format)

**Expected benefit**: Clearer guidance for collaborators (Enrico, yourself) on when to escalate models. Reduces ambiguity in voice sessions.

---

## 2. Modularization & Token Efficiency Audit

### What We Did (pta-cbp-parser)
**Commits**: 
- `3183d16` — "feat: modularization audit and token efficiency optimization"
- `f4be699` — "refactor: split docs and canonicalize repository map"

**Key changes**:
1. **Consolidated SKILLS.md**: Merged claude-code-skills.md (240 lines) into SKILLS.md (699 lines)
2. **Split bloated WORKFLOW_AND_LOGGING.md** (415 lines) into:
   - `docs/architecture.md` — pipeline phases, data flow, filtering, design decisions
   - `docs/logging.md` — per-phase log locations, JSON schemas, state persistence
   - `docs/project-state.md` — structured limitations, disabled features, TODOs

3. **Moved repository map**: `dev/repository_map.md` (timestamped) → `docs/repository-map.md` (canonical)
   - Added YAML frontmatter with `updated: YYYY-MM-DD HH:MM` timestamp
   - Canonical file decouples from filename

4. **Token savings**: ~1.75K per session; ROI positive after 2 sessions

**Rationale**:
- Modular docs reduce context overhead (only load what you need)
- Timestamped frontmatter enables lifecycle queries (when was X last updated?)
- Canonical location (`docs/`) prevents scattered versioning

### How to Adapt to Thesis Codebase

**Current state**: Thesis has similar bloat:
- Large CLAUDE.md (36KB, mixes structural facts with ADRs)
- dev/repository_map.md exists but isn't canonical
- docs/ has scattered ADRs, compliance, decisions, but no unified structure
- No YAML frontmatter timestamps

**Action** (in priority order):

#### Phase A — Audit & Consolidate (1-2 hours)
1. Review current structure:
   ```bash
   cd CMT_Codebase
   wc -l CLAUDE.md docs/*.md .claude/rules/*.md | sort -n
   ```
   Identify the largest files (targets for splitting).

2. Create audit document `.claude/MODULARIZATION_AUDIT.md`:
   - List all docs > 200 lines
   - Flag responsibilities that span multiple files
   - Estimate token savings from splitting

#### Phase B — Split Docs (2-3 hours)
Target: Move 15-20KB from CLAUDE.md to modular docs.

**Suggested splits** (mirroring pta-cbp-parser):
- `CLAUDE.md` → keep only navigation + project context (~5KB)
- `docs/architecture.md` — System A/B architecture, agent roles, data flow (NEW)
- `docs/research-questions.md` — RQ evolution, v1→v2 changes (NEW)
- `docs/compliance.md` — CBS guidelines, integrity gates, ADR status (consolidate from `docs/compliance/` + `docs/decisions/`)
- `docs/project-state.md` — TODOs, frozen decisions, known limitations (NEW)
- `docs/repository-map.md` — canonical file map with timestamps (move from dev/)

**YAML frontmatter template**:
```yaml
---
name: {{doc title}}
description: {{one-line purpose}}
updated: 2026-04-15 14:30
---

# {{Title}}

[content]
```

#### Phase C — Update Navigation (30 min)
Update CLAUDE.md with new modular structure:
```markdown
## NAVIGATION

**Read at session start (in order):**
1. This file — project context + constraints
2. [docs/architecture.md](docs/architecture.md) — System A/B, data flow, design patterns
3. [docs/compliance.md](docs/compliance.md) — CBS requirements, ADR status
4. [docs/repository-map.md](docs/repository-map.md) — file locations, agent status
5. [docs/tooling-issues.md](docs/tooling-issues.md) — environment issues

**Key references:**
[...keep existing pointers...]
```

#### Phase D — Memory + Monitoring (ongoing)
1. Create memory file: `memory/feedback_modularization.md`
   ```markdown
   ---
   name: Modular documentation structure
   description: Split large docs to reduce context overhead per session
   type: feedback
   ---
   
   **Rule**: Keep individual docs under 300 lines. Split when adding 50+ lines to a single file.
   **Why**: Reduces context overhead (~58% savings from pta-cbp-parser audit), enables selective loading.
   **How to apply**: When editing CLAUDE.md, architecture.md, or docs/ > 300 lines, plan a split.
   ```

2. Add to CHEATSHEET.md:
   ```
   /audit_docs     → run modularization audit (identify > 200-line files)
   /split_docs     → interactive guide for splitting a doc module
   ```

**Expected benefit**: 
- Thesis sessions load only relevant docs (20% context reduction)
- Timestamps enable tracking "when was RQ evolution last reviewed?"
- Clearer separation of concerns (architecture vs compliance vs state)

---

## 3. Automatic Plan Mirroring + Timestamps

### What We Did (pta-cbp-parser)
**Commit**: `d311285` — "feat: add automatic timestamp tracking to plan mirroring"

**Enhancement to existing plan workflow**:
1. Mirror hook (`.claude/hooks/mirror_plan.py`) now injects YAML frontmatter:
   ```yaml
   ---
   created: 2026-04-15 14:32:18
   updated: 2026-04-15 15:45:22
   ---
   ```

2. **`created`**: Set on first write, never changes (shows when planning began)
3. **`updated`**: Refreshed on every edit (shows last modification time)

**Use cases**:
- Query plans by age: "show me all plans created in the last week"
- Track velocity: "how many plans per session?"
- Lifecycle analysis: "is this plan actively being refined or stale?"

### How to Adapt to Thesis Codebase

**Current state**: Thesis has `.claude/plans/` with timestamps in filenames (`2026-04-13_cmt-master-upgrade-plan.md`) but no YAML frontmatter.

**Action** (minimal, high ROI):

#### Step 1 — Check current mirror hook
```bash
cd CMT_Codebase && ls -la .claude/hooks/
```

If `mirror_plan.py` exists, it's likely an older version without timestamps.

#### Step 2 — Copy pta-cbp-parser's hook
Copy the enhanced hook from pta-cbp-parser:
```bash
# Compare versions
diff <(cat C:\Users\brian\OneDrive\Documents\01\ -\ P\ -\ Projects\ and\ Tasks\2026-01-03\ -\ Preferential\ Trade\ Project\pta-cbp-parser\.claude\hooks\mirror_plan.py) \
     <(cat C:\Users\brian\OneDrive\Documents\02\ -\ A\ -\ Areas\MSc.\ Data\ Science\2026-03\ -\ CBS\ Master\ Thesis\CMT_Codebase\.claude\hooks\mirror_plan.py)
```

If thesis version is older → copy pta-cbp-parser version (will auto-upgrade existing plans on next edit).

#### Step 3 — Verify outcome format
Update `.claude/rules/trigger-plan-workflow.md` (if it exists) with the pta-cbp-parser outcome format:

```markdown
## Outcome Format
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

### ❌ Dropped
- **What**: <item not done>
  **Why**: <reason>
```
```

**Expected benefit**:
- All existing thesis plans auto-gain timestamps on next edit (zero effort)
- Outcome files now reference both created and completed times (lifecycle clarity)
- Enables querying plans by lifecycle (e.g., "which plans are in-flight for >3 days?")

---

## 4. Summary: Immediate Action Items

### For Tomorrow Morning (30 min):

**Priority 1**: Model Override Convention
- [ ] Add convention section to CLAUDE.md (copy from pta-cbp-parser)
- [ ] Create `memory/feedback_model_override.md`
- [ ] Test: say "use sonnet for this analysis" in next session

**Priority 2**: Audit Documentation Structure (1 hour)
- [ ] Run `wc -l` audit on docs/
- [ ] Identify top 5 files > 200 lines
- [ ] Create `.claude/MODULARIZATION_AUDIT.md` with split plan

**Priority 3**: Plan Timestamp Enhancement (15 min)
- [ ] Check `.claude/hooks/mirror_plan.py` version
- [ ] If older → copy from pta-cbp-parser
- [ ] Test: create a small plan, verify YAML frontmatter

### For This Week (optional):

**Phase B**: Execute documentation splits (2-3 hours)
- Split CLAUDE.md + bloated docs
- Reorganize docs/ with canonical structure
- Update navigation

**Outcome**: 
- Clearer model selection (Haiku default, Sonnet/Opus on demand)
- 15-20% context reduction per session
- Full plan lifecycle tracking with timestamps

---

## Reference: Key Files in pta-cbp-parser

If you want to dive deeper, these files are canonical examples:

1. **Model Override**: `CLAUDE.md` section "Model Override Convention" + `.claude/rules/context-token-optimization.md`
2. **Modularization**: 
   - Splits: `docs/architecture.md`, `docs/logging.md`, `docs/project-state.md`
   - Audit: `.claude/MODULARIZATION_TOKEN_AUDIT.md`, `.claude/AUDIT_ACTION_CHECKLIST.md`
3. **Plan Timestamps**: 
   - Hook: `.claude/hooks/mirror_plan.py`
   - Workflow: `.claude/rules/trigger-plan-workflow.md`

All are at: `C:\Users\brian\OneDrive\Documents\01 - P - Projects and Tasks\2026-01-03 - Preferential Trade Project\pta-cbp-parser`

---

## Collaboration Notes

- **Enrico** (thesis collaborator): This guide is for both of you. The model override + timestamp features are particularly useful for voice-based sessions.
- **Brian**: Use the priority ranking to sequence implementation. Priority 1 (model override) is zero-effort; Priority 2 (audit) informs your decisions going forward.
- **Timeline**: Thesis deadline is 15 May (30 days). Token efficiency + plan tracking compound in value as complexity grows.

---

**Document version**: 2026-04-15 (created after today's pta-cbp-parser improvements)  
**Status**: Ready to implement
