---
name: thesis-structuring
description: >
  Maintain and evolve the thesis outline in a disciplined, pattern-aware way — integrated
  into the thesis_production_system pipeline. Activate this skill whenever the user provides
  new thesis context (research questions, methodology decisions, supervisor feedback, draft
  sections, new literature), asks whether the structure still makes sense, or requests a
  /restructure-section or /update-outline operation. Also activate before WritingAgent
  drafts bullets for a chapter that has no approved structural skeleton yet.
  Do NOT use for writing content. Only for managing thesis/thesis-writing/outline.md and chapter stubs.
---

# Thesis Structuring Skill

Manages `thesis/thesis-writing/outline.md` and chapter skeleton stubs within System B (thesis_production_system).
Does not write prose. Does not interact with System A (ai_research_framework).
Conservative by design: restructures only when conceptually justified.

---

## Integration Points in System B

This skill operates at two points in the existing pipeline:

**Point 1 — Pre-bullets gate (between PlannerAgent P2 and WritingAgent)**
Before WritingAgent drafts bullets for any chapter, verify that chapter has an approved
structural skeleton in `thesis/thesis-writing/outline.md`. If not, run this skill first.

**Point 2 — Slash command `/update-outline`**
User-triggered. Reads all current section files and state, then decides whether the outline
needs updating. Produces a restructuring decision and updates `thesis/thesis-writing/outline.md`.

---

## Files This Skill Reads

| File | Purpose |
|---|---|
| `thesis/thesis-writing/outline.md` | Current target structure — primary input |
| `docs/tasks/thesis_state.json` | Section statuses (no_bullets / bullets_draft / bullets_approved / prose_approved) |
| `thesis/thesis-writing/sections-drafts/*.md` | Existing bullet skeletons and their content |
| `.claude/agents/thesis-writer.md` lines 154–169 | Chapter page budget table |
| `docs/project-management/context.md` | Thesis framing, RQ, methodology |

## Files This Skill Writes

| File | Condition |
|---|---|
| `thesis/thesis-writing/outline.md` | Always — even if "no change", confirm current version is valid |
| `thesis/thesis-writing/sections-drafts/{chapter_id}.md` | Only when creating a new stub (status → `no_bullets`) |

---

## Two Modes

**Initial structuring** — `thesis/thesis-writing/outline.md` is empty or missing. Given `docs/project-management/context.md`
and archetype inference, propose a first complete outline with page budget allocation.

**Restructuring** — outline exists. Given new inputs, decide whether to preserve, refine,
or restructure. Always compare against the page budget table before proposing splits or merges.

---

## Step 1 — Read System State

```
1. Read docs/tasks/thesis_state.json → note which sections exist and their statuses
2. Read thesis/thesis-writing/outline.md → current structure
3. Read .claude/agents/thesis-writer.md lines 154–169 → page budgets per chapter
4. Read docs/project-management/context.md → RQ, methodology, thesis framing
5. Read any new input provided by the user
```

---

## Step 2 — Infer Thesis Archetype

Read `references/archetypes.md`. Given that this thesis involves:
- A multi-agent AI system (System A) as the research object
- Empirical benchmarking (SRQ1–SRQ4)
- Framework design and evaluation

This thesis is almost certainly a **Technical / DSR Hybrid**. Confirm or adjust based on `docs/project-management/context.md`.

---

## Step 3 — Apply Restructuring Logic

Read `references/restructuring-heuristics.md`.

Additionally enforce these System B-specific constraints:

**Page budget constraint**: Total thesis max = 120 pages (2,275 chars excl. spaces = 1 page).
Before proposing any split or new chapter, verify the page budget allows it.
If a chapter is already at budget, do not propose adding subsections — flag as open question instead.

**Status constraint**: Never restructure a section with status `prose_approved`.
Sections with `bullets_approved` can be restructured only with explicit user confirmation.
Sections with `no_bullets` or `bullets_draft` are free to restructure.

**Determine change level:**

| Level | Condition |
|---|---|
| **No change** | New input consistent with outline; no budget or status conflicts |
| **Minor revision** | Local tension in 1–2 sections; rename, split, or merge within budget |
| **Major restructuring** | RQ shifted, methodology changed, chapter sequence logically broken, or systemic overlap across 3+ sections |

---

## Step 4 — Produce Output

```markdown
## Thesis Archetype
[name + one-sentence rationale]

## Structural Diagnosis
[3–6 sentences. Reference specific files and section statuses.]

## Recommended Outline
[Hierarchical numbered outline — see format below]

## Page Budget Allocation
[Table: chapter | target pages | current status]

## Change Level
[no change | minor revision | major restructuring]

## Rationale
[One bullet per change. Or: "Structure preserved — no changes required."]

## Open Questions
[Unresolved structural risks or budget conflicts. Or: "None."]

## Next Action for System B
[Specific instruction for the pipeline. E.g.:
"PlannerAgent may now schedule WritingAgent for ch3."
"Await human approval — change level is major restructuring."]
```

### Outline format

```
1. Introduction
   1.1 Background and Motivation
   1.2 Research Problem and Gap
   1.3 Research Question and Sub-questions
   1.4 Scope and Delimitations
   1.5 Thesis Structure

2. [Chapter name]
   2.1 ...
```

Use chapter names from existing `thesis/thesis-writing/outline.md` unless renaming is justified.
Do not create sections without argumentative or page-budget justification.

---

## Mandatory Rules (mirror System B conventions)

- Never auto-proceed after proposing major restructuring — output must say "Await human approval"
- Never touch `prose_approved` sections
- Never write to `thesis/thesis-writing/sections-drafts/` except to create new stubs (status `no_bullets`)
- Page budget must be checked before every split or addition proposal
- Output must always include "Next Action for System B" so PlannerAgent has a clear signal
