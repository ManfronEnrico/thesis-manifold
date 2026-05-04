---
name: plan-update-all
trigger_phrases:
  - "update plan"
  - "log plan outcome"
  - "finalize plan"
  - "plan is done"
  - "plan completed"
  - "document plan outcome"
description: Verification + sync workflow. Scan all active plans, cross-reference conversation context, auto-update plan files with new information from this session, report changes. No clarifying questions—the goal is always to ensure plans are current and execution-ready.
compatibility:
  tools_required:
    - Read
    - Write
    - Bash
    - Grep
  os: any
  note: Works with both global and project-specific plan directories
---

# Update Plan Skill — Verification + Sync Workflow

**Core behavior:** Scan all in-progress plans, cross-reference conversation context against plan files, auto-update with new information, report what changed. This workflow ensures plans stay synchronized with current understanding and remain execution-ready.

## Standard Workflow (Every Invocation)

This skill follows the same pattern **every time you invoke it**, without needing you to explain intent:

1. **Scan all active plans** (`02-in_progress-plans/`) for staleness
2. **Cross-reference conversation context** — capture any new info, decisions, or understanding mentioned in this session that isn't yet in the plan file
3. **Auto-update plan files** with that context (no permission prompts, just do it)
4. **Report changes** — list what was updated in each plan
5. **Flag blockers only** — report if something prevents execution (unresolved decision, missing dependency)

**Result:** Plans are always current with the latest session context and ready to execute.

## When to Use

Invoke `/plan-update-all` to:
- Verify all active plans are synced with current session understanding
- Capture any new info from conversation into plan files automatically
- Check execution-readiness (identify blockers, missing dependencies, unresolved decisions)
- Before beginning execution of any plan, ensure it reflects current state

**You never need to answer clarifying questions again.** The skill assumes: "Is there new context from this session that should go into the plan file?" and updates accordingly.

## Invocation

```bash
/plan-update-all              # Verify + sync ALL in-progress plans
/plan-update-all <plan-id>    # Verify + sync specific plan (e.g., P0020)
```

Invoke without arguments to sync **all** in-progress plans at once.

## How It Works

The skill executes five steps in sequence:

### Step 1: Scan Active Plans

Search `plans/02-in_progress-plans/` for all plan folders using P-ID naming convention:
- `P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/`
- Return list of all P-IDs, creation dates, and status

### Step 2: Cross-Reference Conversation Context

For each in-progress plan, check:
- **Plan file:** Read the main plan markdown file
- **Session context:** Any new information, decisions, or understanding mentioned in this conversation that isn't yet in the file
- **Integration guides:** Any supporting docs (e.g., `YYYY-MM-DD_DOC-*.md`) that need updates
- **Dependencies:** Check if any referenced plans (e.g., P0021 in P0020) have new information

### Step 3: Auto-Update Plan Files

For each plan, if new context is found:
- **Update relevant sections:** Add new info to appropriate place in plan file (phases, objectives, dependencies, risks, etc.)
- **Update timestamps:** Revise `updated: YYYY-MM-DD HH:MM:SS` in file frontmatter
- **Preserve structure:** Keep all existing content; only add/revise sections with new info
- **No permission prompts:** Just do the updates and report what changed

### Step 4: Check for Blockers

Scan each plan for unresolved items that prevent execution:
- **Unresolved decisions:** Any "TBD", "to be decided", "pending approval" in plan file?
- **Missing dependencies:** Referenced plans (e.g., "P0021 completed") — is that true? If blocked plan not completed, flag it
- **Incomplete sections:** Missing description, success criteria, or phase details?
- **Cross-reference breaks:** Any linked files that no longer exist?

### Step 5: Report Status

Output structured report for **each plan**:
```
P0020: Rule System Reform
  Status: In Progress
  Last updated: 2026-05-04 14:30
  
  ✅ Updated in this session:
     - Dependencies section: Added P0021 integration details
     - Phase 1 tasks: Clarified audit checklist
  
  ⚠️  No blockers found
  
  ✔️ Execution-ready (can begin Phase 1)
```

Then final summary: "All plans current, X updates made, Y blockers flagged."

## What Gets Updated

When `/plan-update-all` finds new context in conversation, it updates:

| Element | Update Behavior |
|---------|-----------------|
| **Objective** | If clarified or refined during discussion |
| **Context & Rationale** | If new understanding of problem discovered |
| **Scope** | If boundaries expanded, reduced, or clarified |
| **Success Criteria** | If additional criteria identified |
| **Phase descriptions** | If approach adjusted or refined |
| **Dependencies** | If new plan dependencies identified (e.g., "awaiting P0021") |
| **Risks & Mitigations** | If new risks discovered or mitigations added |
| **Timestamps** | Updated `updated:` field in frontmatter always |

**Never removes or loses information.** Only adds, clarifies, or refines. All edits are additive.

## File Locations and Naming

All plans live in status-organized buckets:

```
plans/
  01-backlog-plans/
    P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/
      P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md
      YYYY-MM-DD_DOC-{description}.md  (supporting docs)
  
  02-in_progress-plans/          # ← This skill syncs these
    P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/
      P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}.md
      YYYY-MM-DD_DOC-*.md
  
  03-outcome_plans/
    P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}/
      P{NNNN}_YYYY-MM-DD_HHMM_OUTCOME-{slug}.md
  
  04-archive_plans/
    P{NNNN}_YYYY-MM-DD_HHMM_PLAN-{slug}/
```

**Naming convention:**
- `P{NNNN}` — Unique sequential ID (P0001, P0002, ..., P0020, etc.)
- `YYYY-MM-DD_HHMM` — ISO date + 24hr time
- `PLAN` / `OUTCOME` — Literal keywords
- `{slug}` — Lowercase, hyphens

## Common Scenarios

### Scenario 1: Start of Session

You begin a new Claude session. You want to ensure all active plans have the latest context before proceeding:

```
/plan-update-all
```

Skill will:
1. Scan `02-in_progress-plans/` (all active plans)
2. Cross-reference conversation context (if any references to plans in your prompt)
3. Update any plan files with new context
4. Report status and blockers (if any)

**Output:**
```
P0020: Rule System Reform — ✅ All updates synced (2 sections updated)
P0019: Preprocessing Unification — ✔️ No new context found
P0018: Plan Restructuring — ✔️ Already complete (moved to outcomes)

Overall: ✔️ All plans current and execution-ready
```

### Scenario 2: Mid-Session Plan Sync

You're discussing details about a specific plan. Before executing it, ensure it has all the new understanding:

```
/plan-update-all P0020
```

Skill will:
1. Locate P0020 plan file
2. Check conversation for context relevant to P0020 (e.g., "P0021 integration", "new task details")
3. Update P0020 with any new information
4. Report changes and blockers

**Output:**
```
P0020: Rule System Reform
  
  ✅ Updated in this session:
     - Phase 1 tasks: Clarified audit checklist with 3 new items
     - Dependencies: Added explicit link to P0021 integration guide
  
  ⚠️ No blockers found
  
  ✔️ Execution-ready (can begin Phase 1)
```

## Integration with Project Workflow

This skill connects to:
- **`.claude/rules/trigger-plan-workflow.md`** — Plan structure, naming, and organization standards
- **`plans/PLANS_INDEX.md`** — Master reference of all P-IDs and plan statuses
- **Memory system** — Auto-updates reference_plan_ids.md if new plans created
- **`/plan-documentation-organizer`** skill — For creating/moving/validating plans

## No Permission Prompts

The skill updates plan files **without asking for confirmation**. It will:
- Never ask "should I update P0020?"
- Never ask "do you want this change?"
- Simply update, then report what changed

This is intentional. The goal is **verification + sync**, not decision-making. You trust the skill to add new context accurately.

## Example Session Flow

**You start a session discussing P0020 details:**

```
In this session, you talk about:
- Phase 1 audit checkpoints (new detail)
- How P0021 integration affects Phase 2 (new dependency)
- Updated success criteria (clarification)
```

**You invoke:**
```
/plan-update-all P0020
```

**Skill does:**
1. Reads P0020 plan file
2. Scans conversation for new P0020-relevant context
3. Finds: audit details, P0021 dependency link, success criteria
4. Updates plan file with those details
5. Updates `updated:` timestamp
6. Reports what changed

**Skill outputs:**
```
P0020: Rule System Reform
  
  ✅ Updated in this session:
     - Phase 1 tasks: Added 3 audit checkpoints
     - Dependencies: Linked to P0021 integration guide (2026-05-04_DOC-p0021-integration.md)
     - Success Criteria: Refined token savings target with explicit measurement
  
  ⚠️ No blockers found
  
  ✔️ Execution-ready (can begin Phase 1)
```

**Next time you invoke it, the skill remembers none of this.** It simply:
- "Is there new context from this conversation that's not in the plan file?"
- If yes, update. If no, skip.
- Report status and blockers.

---

## Troubleshooting

**Skill says "no blockers" but I know there's an issue:**
- Blockers are only: unresolved decisions, missing dependencies, broken cross-refs
- If something else is preventing execution, that's a scope/readiness issue, not a blocker
- Create a task or note in plan file to track it

**Skill found a blocker I forgot about:**
- Great! Fix it before execution
- Common blockers: "awaiting P0021" (now completed), "TBD" (needs decision), missing phase description

---

**Related:** `.claude/rules/trigger-plan-workflow.md` | `plans/PLANS_INDEX.md` | `/plan-documentation-organizer`
