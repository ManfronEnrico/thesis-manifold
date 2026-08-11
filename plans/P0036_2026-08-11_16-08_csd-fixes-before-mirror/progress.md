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
