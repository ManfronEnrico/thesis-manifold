# /update-outline

Triggers the thesis-structuring skill to assess and optionally update `thesis/thesis-writing/outline.md`.

## When to use
- After receiving supervisor feedback that implies structural changes
- After the research question or methodology has shifted
- Before WritingAgent drafts bullets for a chapter with no existing skeleton
- When you suspect chapter overlap, redundancy, or page budget problems
- At the start of a new writing phase to sanity-check structure

## Inputs (optional, pass after the command)
- New context: paste supervisor comments, updated RQ, methodology notes, or nothing (skill reads state automatically)

## What happens
1. Skill reads: `thesis/thesis-writing/outline.md`, `docs/tasks/thesis_state.json`, `thesis/thesis-writing/sections-drafts/*.md`, `.claude/agents/thesis-writer.md` (page budgets), `docs/project-management/context.md`
2. Skill determines change level: no change / minor revision / major restructuring
3. Skill produces: updated outline, page budget table, rationale, open questions, and next action for System B
4. If change level = **major restructuring**: output is shown for human approval — pipeline does NOT proceed automatically
5. If change level = **no change** or **minor revision**: `thesis/thesis-writing/outline.md` is updated and PlannerAgent may proceed

## Output written to
- `thesis/thesis-writing/outline.md` (always confirmed/updated)
- `thesis/thesis-writing/sections-drafts/{chapter_id}.md` stubs (only if new chapters are added)

## Hard rules
- Never restructures `prose_approved` sections
- Requires human approval before major restructuring takes effect
- Does not write prose or bullet content — only structural skeletons
