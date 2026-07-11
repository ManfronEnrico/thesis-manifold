# Step 2 — Workstream C: thesis_state.json sync (BLOCKED)

**Status**: diagnostic complete, edits paused awaiting Brian's call on
naming convention.

## What the plan asked for

Sync `docs/tasks/thesis_state.json` with the actual repo state:
- Verify `last_scraped`, `session_id`, `compliance_note` dates
- Verify `word_count_estimate` for chapters 1-4 against actual section files
- Reconcile `literature_state.papers` (23 entries) with
  `literature.confirmed_papers` (11 + `total_confirmed: 37`)
- Confirm `rq_version: v2` and `gap_analysis_version: v3`

## Finding 1 — `word_count_estimate` is actually a CHARACTER count

| Section | JSON value | Real `wc -w` (words) | Real `wc -m` (chars) |
|---------|-----------:|---------------------:|---------------------:|
| ch1-introduction | 21,400 | **2,889** | 21,749 ← match |
| ch2-literature-review | 50,500 | **7,323** | 54,307 ← match |
| ch3-methodology | 27,300 | **3,348** | 24,259 ← match |
| ch4-data-assessment | 22,700 | **4,249** | 28,823 ← match |

The JSON values match the **character counts**, not word counts. Brian
correctly suspected this in the plan and asked for human review before
renaming the field.

**Two options to align**:
- Rename field to `character_count_estimate` and update values to exact
  `wc -m` figures.
- Keep field name and recompute with actual word counts (yielding
  ~3,000–7,000 per section).

Decision required from Brian.

## Finding 2 — Stale dates and session ID

| Field | Current value | Should be |
|---|---|---|
| `last_scraped` | `2026-03-15` | unknown — Brian must confirm actual scrape date |
| `session_id` | `20260315-000000` | likely `20260423-XXXXXX` (today) |
| `compliance_note` (multiple) | references `2026-04-12` | needs verification each is still latest check |

## Finding 3 — Two parallel paper structures

- `literature_state.papers` lists **23** confirmed papers
- `literature.confirmed_papers` lists **11** more (with `run: 3`)
- Header `total_confirmed: 37` (expected: 23 + 11 = 34, doesn't match either)

Either both structures are needed (some semantic distinction) or one is
legacy data. Brian must confirm before reconciliation.

## Finding 4 — Versions

`rq_version: v2`, `gap_analysis_version: v3` — values look plausible but
were not verified against the underlying RQ / gap-analysis docs in this
session.

## Why this step was paused

Each of the 4 findings requires a Brian decision (naming, scrape date,
structure semantics). Per his own plan, Workstream C is "report findings
and pause for Brian's call before committing." Document delivered, awaiting
input.

## Recommended next action

Bundle findings 1-4 into a single message to Brian, request decisions, then
apply edits in a single pass.
