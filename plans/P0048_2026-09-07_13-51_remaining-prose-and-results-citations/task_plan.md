---
pid: P0048
created: 2026-09-07 13:51:00
updated: 2026-09-07 16:40:00
status: in_progress
focus_detail: "HANDOFF PLAN — written to survive an account switch that loses session history. Read START_HERE.md first. Chapter-by-chapter prose pass from ch4 onward, working the results-folder tables/figures into the text as in-text citations. Session's main discovery: the H1/H3 forecast horizon is never applied to feature construction, so both matrices are one-month tasks and the published 'H3' results do not measure the horizon the prose claims (F1). Two prose blocks are ready to paste now (split correction, feature count); the horizon blocks are blocked on a code fix + re-run."
---

# P0048 — Remaining prose & working in-text citations of results

> **Figures, tables and diagrams are owned by
> [P0050](../P0050_2026-09-07_18-40_figure-table-generation-and-provenance/START_HERE.md)**
> (also written for this account switch). Any artefact you need to cite, or find
> stale, belongs to that plan — 11 diagrams and 25 appendix tables regenerate
> from 5 scripts.


> **This plan was written as a handoff.** The session that produced it will not be
> recoverable (account switch). Everything needed to resume is on disk. Start with
> `START_HERE.md`.

## Objective

Two intertwined jobs, done chapter by chapter and within chapter section by section:

1. **Finish the prose.** From chapter 4 onward much of the `.docx` is still bullet
   fragments or stale prose written before the pipeline was regenerated.
2. **Work in the results.** `05_thesis_results/` holds ~317 files — 26 export-ready
   appendix tables, 44 SRQ1 tables, and per category 31 EDA tables + 8 plots. The
   thesis currently cites **2 figures in total**. Chapter 4 is the data assessment
   chapter and cites none of the EDA plots that exist to support it.

**Method for every section:** verify the facts against the current result files
first, then write context-aware prose with anchors, per
`.claude/rules/prose-insertion-discipline.md` and the `write-prose-from-bullets`
skill. Brian pastes into the OneDrive `.docx`; the `.docx` stays authoritative.

## Absorbed plans (archived 2026-09-07)

**P0045** (draft bullet reconstruction) and **P0047** (exogenous enrichment, folder
`P0046_..._21-10`) were archived and their open work moved here. Everything still live
from them is in **`INHERITED_CONTEXT.md`** — read it rather than the archived folders.

- From **P0047**: 3 open tasks, all Brian's and all writing-side — the five Word threads
  and the NotebookLM claims verification (now tasks 9–10). Its 19 completed experimental
  tasks are history; its determinism contract stays in `LOCKED_STATE.md`.
- From **P0045**: 6 genuinely open tasks — the draft-bullet rebuild (now tasks 11–16).

**Division of labour with P0049** (created in parallel the same day):

| Plan | Owns |
|---|---|
| **P0048** (this) | Prose, drafts, Word threads, claims verification, citations |
| **P0049** | Horizon fix, SRQ1 re-runs, funded SRQ4 scenarios |

P0049 independently reproduced the horizon defect as its F22 and owns the fix. Its
`START_HERE.md` says *"Don't do prose from P0049."* Honour that in both directions.

## Why this plan is separate

- **Not P0045** (draft bullet reconstruction) — that rebuilds `sections-drafts/*.md`
  planning skeletons. This produces *prose for the `.docx`*. P0045's phase 4 lists
  ch4/ch7/ch8; the boundary is: P0045 writes bullets into drafts, P0048 writes prose
  into Word. **Do not let P0048 write prose into `sections-drafts/` — that is exactly
  the drift `writing-surface-authority` removed.**
- **Not P0043** (Word comment audit) — that builds *tooling* to triage comments.
  P0048 *closes* specific threads as a by-product of rewriting sections.
- **Not P0047** (exogenous/holiday enrichment) — numbers locked, prose staged in its
  own note. P0048 inherits that note as a ready-to-paste input and must respect one
  sequencing constraint (see below).
- **Not P0046** (figure/table provenance) — that made artefacts regenerable and
  traceable. P0048 consumes that inventory to decide what to cite. P0046 F19 already
  settled the method: *build the regenerable inventory first, choose citations
  second.*

## The finding that dominates this plan

**F1 — the forecast horizon is never applied to feature construction.**

`engineer_features()` has no `horizon` parameter and step 4 passes none. Lags are
`shift(lag)` at both horizons, so `lag_1` is month *t−1* whether the horizon is 1 or
3. Verified by merging the two CSD matrices on brand × year × month: across all 4,370
shared rows `sales_units`, `lag_1`, `lag_3` and `lag_13` are **identical**. The only
difference is `min_periods` (15 vs 17), dropping 11 brands and 506 rows.

Every SRQ1 script hardcodes `_feature_matrix_h3.parquet`; there is **zero** occurrence
of `_h1` in SRQ1 training code. Row counts confirm the published numbers come from the
h3 file (1805/665/95 matches `summary.md` exactly).

**Consequence:** the thesis reports one-month-ahead accuracy while describing a
three-month horizon. This is a bug, not a documented simplification — step 3's own
docstring says *"The primary reported horizon is 3 months... Both are real runs."*

**Brian's decision (2026-09-07):** document both horizons and make sure both are
benchmarked; evaluate the SRQ4 prompt-schema experiments at 3 months too, provided
held-out ground truth is retained. Ground truth **is** retained — see F5.

## Phases

| # | Phase | Scope | Status |
|---|---|---|---|
| 0 | Handoff safety | START_HERE, findings, tasks on disk | complete |
| 1 | Paste-ready blocks | split correction, feature count | pending (Brian) |
| 2 | Horizon decision + fix | raise with Enrico, then `engineer_features()` | pending |
| 3 | Regenerate + re-benchmark | 8 matrices, SRQ1 both horizons, SRQ4 @H3 | blocked on 2 |
| 4 | Ch4 complete pass | §4.1–§4.6, EDA plots cited | partially blocked on 3 |
| 5 | Ch5–Ch9 prose + citations | section by section | pending |
| 6 | **Inherited: draft bullets** | ch3/ch6 merge, ch4/ch7/ch8, short files, verify | pending (tasks 11–16) |
| 7 | **Inherited: Brian's writing items** | 5 Word threads, NotebookLM claims verification | pending (tasks 9–10) |

**Phase 4 is not fully blocked.** §4.1/§4.2 narrative and §4.3/§4.4 (blocks P1/P2)
can proceed now; only the horizon subsection and the numbers that move with the
re-run wait on phase 3.

## Sequencing constraints

1. **P2 before the holiday note's P1.** The holiday note says amend "14 → 17"
   features. P0048 F3 establishes the base is **13**, not 14, so the corrected count
   is **16**. Applying them in the wrong order bakes in an off-by-one.
2. **Holiday note P3 and P4 ship together** (constraint inherited from P0047): P4
   leaves two sentences claiming "every input held identical", which are only true
   once P3 records that XGBoost is pinned to one thread.
3. **Do not write the §4.2 EDA pass before phase 3.** Every figure there is stale;
   doing it twice is waste.

## Related

- `06_thesis_writing/writing-notes/srq1-forecast-horizon-defect-and-split-correction.md`
  — this session's deliverable: bullets, anchors, prose, provenance
- `06_thesis_writing/writing-notes/srq1-holiday-enrichment-result-and-limitations.md`
  — P0047's deliverable; ready to paste, interacts via constraint 1
- `plans/.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision/LOCKED_STATE.md`
  — the determinism contract (`XGB_N_JOBS=1`). **Any re-run in phase 3 must honour
  it or the new numbers are not reproducible either.**
- `.claude/rules/prose-insertion-discipline.md` · `.claude/skills/write-prose-from-bullets/`
- `.claude/rules/writing-surface-authority.md` — the `.docx` is authoritative
