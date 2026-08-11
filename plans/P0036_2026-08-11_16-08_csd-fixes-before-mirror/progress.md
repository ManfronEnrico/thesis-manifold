---
pid: P0036
created: 2026-08-11 16:08:00
updated: 2026-08-11 16:08:00
---

# P0036 — Progress

## 2026-08-11 — Session 1 (plan creation)

Investigation session. No code changed; all queries read-only.

### What happened

Began as a state check (remote main + active plans), turned into a root-cause
investigation when Brian challenged two framings:

1. That the F10.5 "grain decision" was blocking — it was not. Market scope and
   aggregation grain are independent axes; DEC-GRAIN was never in question.
2. That promo-zero might follow from excluding discounts — refuted (F2), but the
   challenge prompted the market-hierarchy check that found the real cause.

Brian's instruction to fix CSD before mirroring drove the plan's shape.

### Findings recorded

F1–F9 in `findings.md`. Headline: **promo-zero is an artifact of the region-child
market filter, not a property of the data.** Parent scope `1256338` carries 119,010
nonzero promo rows; the 9 region children carry zero.

### Corrections to earlier analysis in this session

| Claimed | Corrected |
|---------|-----------|
| F10.5 is a blocking thesis-level grain decision | Scope choice, independent of DEC-GRAIN; not blocking |
| Drop promo columns as structurally dead | **Wrong** — would discard a real feature to accommodate a filter bug |
| Parent scope costs row count (~2.3k vs 25.1k) | Conflated fact rows with feature-matrix rows. Parent yields *more* brand-month rows (3,917 vs 3,641) |
| Region filter is pure drift from P0024 | P0026 chose it deliberately; DEC-SCOPE reverses that decision on supplier-metadata grounds |
| Other 3 categories' filter state needs checking | Moot — they inherit the corrected CSD template (Brian) |

### Decisions

- **DEC-SCOPE** — market scope = parent `1256338` (DVH EXCL. HD). Free win: more rows,
  more brands, plus the promo feature.
- **P0034 (chapter numbers) stays last** — prose will be rewritten once EDA and model
  training settle.
- **Single-brand training** — measured, not adopted. Task 7 carries the numbers; Brian
  decides. Recommendation is pooled training + Faxe Kondi evaluation.

### Tooling note

Two `grep -rn` calls via Bash timed out at 120s on this repo. The Grep tool returned the
same searches immediately. Project rules already mandate Grep over shell grep — followed
from that point on.

### Next session starts with

Task 1 (commit the V3/V4 fixes off the **locked** worktree
`worktrees/p0032-leakage-fix-v3-v4`) — the only work currently at risk of loss —
then task 2 (market filter switch).

## 2026-08-11 — Session 1, part 2 (RQ verification + doc slimming)

No code changed. Plan/doc files only.

### RQ check (Brian asked whether SRQ1 is a pure accuracy claim)

Read canonical RQ v4. **Yes for SRQ1, no for SRQ4** — recorded as F10.

Trap found: Brian opened `00_thesis_context/thesis-topic/project-overview.md`, which was
marked SUPERSEDED and carried **v2** RQs. Canonical is
`01_thesis_research/research-questions/research-questions.md`. Also corrected an earlier
mis-statement in this session: SRQ4's arms are not "base LLM / LLM+data / LLM+model" but
**dedicated ML vs code-as-action LLM**.

### Thesis notes written

`05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md` — write-up material
organised by chapter: the 196k→2,552 funnel explanation (Ch4), why pooled training helps a
single-brand forecast (Ch4/Ch6), adequacy by model class, the per-SRQ sample-size table, and
the tool-call flow (Ch5/Ch7). Written as answers to anticipated defence questions.

### Doc slimming (Brian's request)

| File | Before | After | Action |
|------|--------|-------|--------|
| `project-overview.md` | 314 | ~165 | Merge conflict resolved (title = "Extending Production Agentic Decision-Support..."); SUPERSEDED banner removed; RQs/literature/architecture → pointers |
| `research-questions.md` | 59 | 47 | Meta-commentary and supersession history cut; operative scope decisions kept as a plain list |
| `system-a-and-b-agent-design-FROZEN.md` | — | new | System A/B agent tables moved verbatim to `05_thesis_writing/writing_agents/`, frozen not deleted |

Literature became a pointer to `gap_analysis_v4.md` (58 papers) — the embedded copy was a
stale 26-paper March snapshot.

### Open reconciliations flagged, not resolved

1. **Thesis title** — Brian chose "Extending Production Agentic Decision-Support with
   Lightweight Forecasting for FMCG Retail". Not attested elsewhere: `frontpage.md` is a
   2026-03-14 template with v2-era candidates, Ch1 has no title. Reconcile against the
   thesis contract.
2. **Categories** — Ch1 §1.4 says five (incl. Totalbeer); P0034 records the 2026-08-01
   exclusion on compute grounds. Overview now says four.
3. **Periods** — Ch1 §1.4 says 37–42; CSD measures **44** at parent scope (F5). Overview
   now says 44.

### SRQ4 third arm — proposed, not adopted

Brian proposed adding **code-as-action LLM + dataset access** as a third arm, funds and time
permitting.

Assessment: this is a real design improvement, not just an extra data point. Two arms
confound *model value* with *data-access value*; three arms isolate them —
A (code-as-action) → B (+ dataset access) → C (+ trained ML tool). B→C then tests whether
dedicated ML is warranted **with data access held constant**, which is precisely the open
question. Cost ≈ +50% of SRQ4 eval spend (LLM API calls, same ~50 prompts).

Fallback if Prometheus stays inaccessible: point arm B at the same feature-matrix parquet
arm C's service reads. Preserves the isolation logic; loses only the "real production
system" external-validity claim.

**Requires rewording SRQ4** from a two-way to a three-way comparison. Per the canonical
file's own rule, **Ch1 §1.3 is the editing surface** — the reword lands there first, then
mirrors to `research-questions.md`. Brian deferred drafting (2026-08-11): no chapter work yet.

### Next session

Task 1 — commit the V3/V4 fixes off the **locked** worktree
`worktrees/p0032-leakage-fix-v3-v4` (only work at risk of loss). Then task 2, the market
filter switch. Goal per Brian: get CSD running cleanly, then mirror to the other categories.

---

## 2026-08-11 — Session 2 (tasks 1–2: cherry-pick + worktree cleanup)

First execution session. Sequential on `main` per Brian, with a push checkpoint
after each task.

### Task 1 — Cherry-pick V3/V4 ✅

Copied **only** `_shared_modules/engineer_features.py` from the locked worktree.
The 12 accompanying `plans/P0032_*/` edits were deliberately excluded: P0032 is
superseded by P0036, so re-committing them would resurrect stale plan status.

- Branch `fix/p0036-v3-v4-leakage-asserts`, commit `e7e5ccb` (1 file, +65/−6)
- 3 hunks as expected; `ast.parse` clean
- Merged to `main` as `74c20f1`

**Correction to the plan's framing.** `task_plan.md` called this work "one power
cycle from loss." Overstated — the lock reason was `"initializing"`, an artifact
of worktree creation, not a deliberate hold. The worktree's base blob (`10be658`)
was byte-identical to `main`'s, so this was a clean patch, not a reconciliation.

### Task 2 — Worktree cleanup ✅ (scope expanded)

**Near-miss worth recording.** Task 2 was written on the premise that
p0033/p0034/p0035 were "empty scaffolding" — based on `git worktree list` showing
all four at `958787b`. That reads the *committed* HEAD and says nothing about the
working tree. An audit before removal found substantial uncommitted work:

| Worktree | Found |
|---|---|
| p0032 | Plan files only — code already cherry-picked, safe |
| **p0033** | **2 untracked notebooks** (Danskvand, Energidrikke) |
| **p0034** | Untracked `DOC-prep-output.md` + 9 plan files |
| **p0035** | **35 files** — 9 script archives, PATHS.py, preserved chain-grain results |

`git worktree remove` refuses on a dirty tree, so nothing would have vanished
silently — but the fix is `--force`, which **would** have permanently deleted the
untracked notebooks and preserved results, with no reflog to recover them.

**Lesson: `git worktree list` is not an emptiness check.** Audit
`git status --untracked-files=all` in each tree before removal.

Each worktree's work was committed to its own branch first:

| Branch | Commit | Contents |
|---|---|---|
| `data/p0033-eda-mirror-three-categories` | `e0f3fbb` | 2 notebooks + plan files |
| `thesis/p0034-chapter-numbers-totalbeer` | `ba9ee48` | plan files + prep doc |
| `chore/p0035-grain-artifact-removal` | `f481df0`, `fb4ee64` | 39 files total |

All four worktrees then removed; **all branches preserved**. p0032's 13 files were
discarded only after verifying its code file was byte-identical to `main`.

### Two findings that change downstream tasks

**F13 — P0033 is partly done.** The Danskvand and Energidrikke notebooks already
exist on `data/p0033-eda-mirror-three-categories`. They were mirrored from the CSD
template *before* DEC-SCOPE, so they carry the same region-filter defect and
all-zero promo columns. A real head start, but they need the scope fix applied —
they are not ready to run. RTD has no notebook yet.

**F14 — P0035 already deletes the `byregion` grain config.** Session 1 flagged
`:722-725` as an open question for task 3 (the `byregion` config consumes
`DVH_REGION_IDS`, which a single-parent-id switch makes incoherent). Inspecting
P0035's uncommitted CSD notebook edit before touching the file showed it **already
removes both the `bychain` and `byregion` config blocks** and does not touch the
market filter at all.

The two changes are therefore **complementary, not conflicting**. P0035 also
removed the deprecated `get_category_engineered_dir()` alias from `PATHS.py` —
the exact failure mode `.claude/rules/repo-tier-structure.md` warns about.

**Implication for task 3:** merge `chore/p0035-grain-artifact-removal` into `main`
*before* editing the notebook. That deletes the `byregion` consumer, leaving the
market filter as the only remaining `DVH_REGION_IDS` site and reducing task 3 to a
single focused change. Sequencing this the other way round would mean resolving a
notebook merge conflict by hand.

### State at session end

- `main` at `74c20f1`, one merge ahead of `origin/main`
- 4 worktrees removed, 0 remaining; every branch preserved
- Tasks 1–2 complete; task 3 next, gated on the P0035 merge decision above
