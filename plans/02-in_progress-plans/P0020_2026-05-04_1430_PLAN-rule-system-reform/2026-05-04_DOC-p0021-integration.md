# P0021 Integration Guide — How Docs Reorganization Feeds P0020

**Date**: 2026-05-04  
**Context**: P0021 (Docs Reorganization) restructured docs from 11→4 folders. P0020 (Rule System Reform) must enforce and leverage this new structure.

---

## Quick Reference

**P0021 Completed Outcome**:
- ✅ Docs folder restructured: 11 folders → 4-folder hierarchy
- ✅ Routing table established in `.claude/rules/root-documentation-boundary.md`
- ✅ Enforcement skills enhanced: `/move-docs-to-folders` and `/docs-update-all` Phase 0
- ✅ Reference materials created (3 files for skill development)

**P0020's Role**:
- Enforce P0021's structure through rule reform
- Consolidate scattered conventions into memory (including folder hierarchy)
- Add Phase 0 (root boundary check) to all doc-related workflows
- Build enforcement skills that validate P0021 compliance

---

## The 4-Folder Structure (P0021 Authority)

```
docs/
  ├── architecture/          — System design, ADRs, architectural decisions
  ├── contributing/          — Developer guides, repo structure, git workflow
  ├── integration/           — Setup guides, tooling, zotero integration
  ├── reference/             — Verification audits, test reports, compliance notes, cheatsheet
  └── README.md              — Navigation hub
```

**Routing Table Authority**: `.claude/rules/root-documentation-boundary.md`

**Enforcement Skills**:
- `/move-docs-to-folders` — Scans root for violations, auto-relocates with cross-ref updates
- `/docs-update-all` Phase 0 — Proactively detects violations before doc sync

---

## How Each P0020 Phase Integrates P0021

### Phase 1: Reclassify + Consolidate Conventions
**Integration**: Conventions should reference P0021 structure.

**Action**:
1. Audit rule files and classify (RULE vs. PROCEDURE vs. CONVENTION)
2. Create `memory/convention_project_standards.md` with:
   - **NEW**: Add section "Docs Folder Routing" → reference to root-documentation-boundary.md
   - **NEW**: Add "Where analysis/verification docs go" → docs/reference/
   - **NEW**: Add "Where integration guides go" → docs/integration/
3. Link memory to P0021 routing table authority

**Deliverable**: convention_project_standards.md includes P0021 structure as living convention.

---

### Phase 2: Prose Compression (Scenario Testing)
**Integration**: Compress docs-workflow rules WITH P0021 structure in mind.

**Files to compress**:
- `trigger-docs-workflow.md` → compress Phase 0 description to reference P0021 structure
- `root-documentation-boundary.md` → prose compression WITH routing table intact

**Scenario Test**: For each compression, ask:
- "Does the compressed version still enforce P0021 boundary rules?"
- "Can someone new to the project still understand where to put docs?"
- "Does the routing table survive compression?"

**Example compression**:
```
BEFORE (verbose):
"All markdown documentation—analysis, reports, audits, guides—goes to 
appropriate respective folders. See routing table for destinations."

AFTER (compressed):
"All markdown documentation goes to docs/ folders per routing table 
(root-documentation-boundary.md). See table for destinations."

SCENARIO TEST: Does reader know WHERE the table is? YES ✓
Does reader know NOT to put docs at root? YES ✓
PASS.
```

**Deliverable**: Compressed rules maintain P0021 enforcement.

---

### Phase 3: Move Procedures to Skill SKILL.md Files
**Integration**: Procedures should move to locations per P0021 structure.

**Action**:
1. Extract procedures from rules → place in skill SKILL.md files
2. Examples of procedure moves:
   - `trigger-docs-workflow.md` procedures → `.claude/skills/docs-update-all/SKILL.md`
   - `trigger-git-commit-workflow.md` procedures → `.claude/skills/git-draft-commit/SKILL.md`

3. Update skill SKILL.md files to reference P0021 structure:
   - `/docs-update-all` should mention Phase 0 checks P0021 compliance
   - `/git-draft-commit` output should note files moved per P0021 rules

**Deliverable**: Skill SKILL.md files reference and enforce P0021 structure.

---

### Phase 4: Priority Hierarchy
**Integration**: Root boundary rule (P0021) is TRUST tier.

**Action**:
1. Create `.claude/rules/rule-priority-hierarchy.md`
2. Add P0021 enforcement to TRUST tier:
   ```
   TRUST TIER (Never yield):
   - Root documentation boundary (P0021 structure)
   - Branch strategy (feature branches, not main)
   ```
3. Explain: "Root boundary enforcement prevents accumulation of scattered docs."

**Deliverable**: rule-priority-hierarchy.md places P0021 structure in TRUST tier.

---

### Phase 5: Build Enforcement Skills (Validators)
**Integration**: New validators should check P0021 compliance.

**New skill focus**: `/audit-cross-references` should verify:
- All references to docs point to P0021-compliant locations
- No broken links to root violations
- All plan-artifact docs are in plan folders (per P0021 structure)

**Action**:
1. Build `/validate-plan-ids` — includes check that docs use YYYY-MM-DD_DOC-{slug}.md naming
2. Build `/audit-cross-references` — includes check that all doc paths match P0021 structure
3. Test against known violations from P0021 cleanup

**Deliverable**: Validators enforce P0021 structure as part of repo health check.

---

### Phase 6: Build Master `/enforce-repo-cleanliness` Skill
**Integration**: Master orchestrator includes P0021 compliance check.

**Action**:
1. `/enforce-repo-cleanliness` includes:
   ```
   ├─ Check 1: /move-docs-to-folders → Root doc violations (P0021)
   ├─ Check 2: /validate-plan-ids → P-ID naming + docs in plan folders
   ├─ Check 3: /audit-plan-outcomes → Missing outcomes
   ├─ Check 4: /audit-cross-references → Broken links + structure violations
   ├─ Check 5: /sync-memory-indices → Memory coherence
   └─ Report: Overall health including P0021 compliance
   ```

2. Output should show:
   - "Root violations (P0021 boundary): X files"
   - "Plan folder docs naming: Y files compliant"
   - "Cross-ref structure violations: Z broken"

**Deliverable**: Master skill reports P0021 compliance status.

---

### Phase 7: Update CLAUDE.md Navigation
**Integration**: CLAUDE.md should document P0021 as enforcement baseline.

**Action**:
1. Update "Quick References" section:
   - Add link: `[docs/reference/root-documentation-boundary.md](docs/reference/root-documentation-boundary.md)` — P0021 routing table (authority)
2. Update "Workflows" table:
   - Add `/move-docs-to-folders` under "Documentation" workflows
3. Update "Rules (TL;DR)" section:
   - Add: "**Root Boundary**: Enforce P0021 4-folder structure via `/move-docs-to-folders`"

**Deliverable**: CLAUDE.md references P0021 structure as living enforcement.

---

### Phase 8: Final Validation
**Integration**: Validation should confirm P0021 compliance is enforced.

**Validation checklist**:
- [ ] Root directory has NO docs violations (run `/move-docs-to-folders` on clean repo)
- [ ] All rule cross-references point to P0021-compliant paths
- [ ] CLAUDE.md and README.md link to root-documentation-boundary.md
- [ ] `/enforce-repo-cleanliness` reports 0 P0021 violations
- [ ] Convention_project_standards.md includes P0021 structure reference
- [ ] Completion report documents P0021 enforcement baseline

**Deliverable**: Validation confirms P0021 structure is living, enforced convention.

---

## Critical Files (Must Stay Synced)

These files form the P0021→P0020 enforcement chain:

| File | Role | P0020 Phase |
|---|---|---|
| `.claude/rules/root-documentation-boundary.md` | Authority (routing table) | 1, 2, 4 |
| `memory/convention_project_standards.md` | Living convention | 1 |
| `.claude/skills/move-docs-to-folders/SKILL.md` | Enforcement automation | 5, 6 |
| `.claude/skills/docs-update-all/SKILL.md` | Phase 0 + proactive checks | 3, 5, 6 |
| `.claude/rules/rule-priority-hierarchy.md` | Trust tier placement | 4, 8 |
| `CLAUDE.md` | Navigation + enforcement reference | 7, 8 |

---

## Testing Strategy

### Phase 1 Audit Test
**Do this during Phase 1**:
```bash
# Verify root is clean (no violations)
ls -1 *.md | grep -v "CLAUDE\|INDEX\|README\|paths\|requirements"
# Should return empty (or show violations to fix)
```

### Phase 5 Enforcement Test
**Do this during Phase 5** (before building validators):
```bash
# Manually create a test violation
touch TEST_VIOLATION.md

# Run skill (should detect)
/move-docs-to-folders

# Skill should:
# 1. Find TEST_VIOLATION.md
# 2. Suggest destination per routing table
# 3. Move it (with confirmation)
# 4. Verify in logs

# Clean up
rm -rf docs/reference/test-violation.md  (or wherever it moved)
```

### Phase 6 Master Skill Test
**Do this during Phase 6** (after all validators built):
```bash
# Create multiple violations across categories
touch ANALYSIS_VIOLATION.md          # Should go to docs/tooling/
touch VERIFICATION_VIOLATION.md      # Should go to docs/reference/
touch TEST_REPORT_VIOLATION.md       # Should go to docs/reference/ or plan folder

# Run master skill
/enforce-repo-cleanliness

# Should report:
# - 3 root violations (P0021 boundary)
# - Suggestions for each
# - Cross-reference check results
# - Overall: ⚠ WARNING (violations found)

# Fix violations
/move-docs-to-folders

# Re-run master skill
/enforce-repo-cleanliness

# Should report:
# - 0 violations
# - Overall: ✓ PASS
```

---

## Summary: P0021 → P0020 Flow

**P0021 provides**:
- ✅ 4-folder structure (authority)
- ✅ Routing table (rule-based)
- ✅ Enforcement skills (manual: `/move-docs-to-folders`)

**P0020 must enforce by**:
- ✅ Phase 1: Consolidate structure as living convention
- ✅ Phase 2: Compress rules while preserving structure
- ✅ Phase 3-4: Embed structure in procedures and hierarchy
- ✅ Phase 5-6: Automate compliance checking
- ✅ Phase 7: Document as enforcement baseline
- ✅ Phase 8: Validate compliance as success criterion

**Result**: P0021's structure becomes automatic, enforced, and teachable to future sessions.

---

## References

- **P0021 Outcome**: `plans/03-outcome_plans/P0021_2026-05-04_1400_OUTCOME-docs-reorganization/`
- **Routing Table**: `.claude/rules/root-documentation-boundary.md`
- **Enforcement Skills**: `.claude/skills/move-docs-to-folders/SKILL.md`, `.claude/skills/docs-update-all/SKILL.md`
- **P0020 Full Plan**: `P0020_2026-05-04_1430_PLAN-rule-system-reform.md` (this folder)

