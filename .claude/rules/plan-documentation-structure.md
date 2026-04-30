# Plan Documentation Structure Rule

**Purpose**: Enforce consistent organization of plans and their supporting documentation using unique P-IDs and status buckets.

**Scope**: All plan files and plan-related documentation.

---

## Folder Structure

Plans live in one of four status buckets:

```
plans/
  01-backlog-plans/         (Not yet started)
  02-in_progress-plans/     (Currently being executed)
  03-outcome_plans/         (Completed with outcomes)
  04-archive_plans/         (Old/deprecated plans)
  
  PLANS_INDEX.md            (Master reference of all P-IDs)
  RESTRUCTURING_SUMMARY.md  (Documentation of P-ID restructuring - 2026-04-30)
```

**Each plan is a folder**, not a single file. This enables bundling with supporting documentation.

---

## Naming Convention (NEW: P-IDs + Timestamps)

### Plan Folder Name

Format: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}`

- `P{NNNN}` = Unique sequential ID (P0001, P0002, ..., P0018, P0019, etc.)
- `YYYY-MM-DD` = ISO date (plan creation date)
- `HHMM` = Time in 24hr format (use 0800 default for undated plans)
- `PLAN` = Literal keyword
- `{slug}` = Lowercase, hyphens

Examples:
- `P0001_2026-04-13_0800_PLAN-cmt-master-upgrade-plan`
- `P0017_2026-04-27_1420_PLAN-jupyter-notebook-path-centralization`
- `P0018_2026-04-28_1400_PLAN-restructure-existing-plans`

### Plan File

File inside folder: `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md`

This is the primary plan document containing details, objectives, steps, and outcomes.

### Outcome File

When plan completes, create: `P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}.md`

In folder: `plans/03-outcome_plans/P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}/`

### Documentation Files

Supporting docs: `YYYY-MM-DD_DOC-{description}.{ext}`

- `YYYY-MM-DD` = Date created (ISO date only)
- `DOC` = Literal keyword
- `{description}` = Lowercase, hyphens
- `.{ext}` = File extension

Examples:
- `2026-04-28_DOC-phase2-migration-summary.md`
- `2026-04-28_DOC-phase3-testing-guide.md`
- `2026-04-28_DOC-completion-status.txt`

---

## Complete Example (P-ID Structure)

```
plans/02-in_progress-plans/
  P0017_2026-04-27_1420_PLAN-jupyter-notebook-path-centralization/
    P0017_2026-04-27_1420_PLAN-jupyter-notebook-path-centralization.md
    2026-04-28_DOC-phase2-migration-summary.md
    2026-04-28_DOC-phase3-testing-guide.md

plans/03-outcome_plans/
  P0018_2026-04-28_1400_OUTCOME-restructure-existing-plans/
    P0018_2026-04-28_1400_OUTCOME-restructure-existing-plans.md
```

---

## Rules for Documentation Files

### What Goes Inside a Plan Folder

Include:
- Plan file (P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md)
- Supporting documentation created during execution
- Analysis, reports, notes specific to this plan
- Test results or validation outputs

Never include:
- Unrelated project documentation
- General tooling notes
- Reusable templates or guides
- Files that apply to multiple plans

### Documentation Lifecycle

1. **During execution**: Create supporting docs in plan folder
   - Use YYYY-MM-DD_DOC-{description}.md format
   - Keep in same plan folder

2. **When moving to outcome**:
   - Keep all supporting docs in folder
   - Move entire folder from 02-in_progress-plans/ to 03-outcome_plans/
   - Optionally add YYYY-MM-DD_DOC-outcome-summary.md with final results

3. **When archiving**:
   - Move entire folder from current status to 04-archive_plans/
   - Keep all supporting docs intact

---

## Never Create Documentation in Root

DO NOT create in C:/dev/thesis-manifold/:
- PHASE2_MIGRATION_SUMMARY.md
- JUPYTER_PATH_CLEANUP_SUMMARY.md
- TESTING_GUIDE.md
- Any plan-related documentation

ALWAYS create inside plan folder:
- plans/02-in_progress-plans/P0017_2026-04-27_1420_PLAN-name/2026-04-28_DOC-summary.md

---

## How to Apply This Rule

### Creating a New Plan

1. Check plans/PLANS_INDEX.md for next available P-ID (e.g., P0019)
2. Create folder: plans/02-in_progress-plans/P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/
3. Create plan file: P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md inside
4. Put all supporting docs in same folder
5. Update plans/PLANS_INDEX.md to register new plan

### Documenting During Execution

1. Create docs inside plan folder
2. Use YYYY-MM-DD_DOC-{description}.md naming
3. Never put docs in project root

### Moving Between Statuses

1. Move entire folder (plan + all docs) to new status
2. Example: 02-in_progress-plans/P0017_2026-04-27_1420_PLAN-x/ → 03-outcome_plans/P0017-OUTCOME_2026-04-28_PLAN-x/
3. Update plans/PLANS_INDEX.md with new status

### Completing a Plan

1. Create outcome folder: plans/03-outcome_plans/P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}/
2. Create outcome file: P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}.md
3. Include frontmatter with completed timestamp and link to original plan
4. Document Completed, Adjusted, Dropped sections
5. Update plans/PLANS_INDEX.md to mark as Completed

---

## Rationale

**Why P-IDs?**
- Quick reference: P0017 vs. full slug
- Automatic allocation of next ID
- Sortable by ID (P0001 < P0002)
- Persistent across sessions

**Why folders vs. flat files?**
- Bundles related documents
- Easy to move plan + docs together
- Prevents documentation scattering
- Clear visual grouping

**Why timestamp in folder AND filename?**
- Folder timestamp = when plan created
- Document timestamp = when doc created
- Both sorted chronologically

**Why PLAN, OUTCOME, DOC keywords?**
- Instantly identifies file type
- Enables automation (scripts can parse naming)
- Prevents ambiguity

---

## See Also

- plans/PLANS_INDEX.md — Master reference of all P-IDs
- .claude/rules/trigger-plan-workflow.md — Workflow and outcome format
- CLAUDE.md → Plans section — Overview of plan workflows
- Memory: reference_plan_ids.md — P-ID system reference
