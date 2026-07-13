---
name: 2026-07-13_harness-and-srq4-decisions-handover-brian
description: Handover Enrico → Brian — what the harness is, how to open it, what was decided on 2026-07-12/13, and which design decisions are still open
category: reference
applies-to: [harness, srq4, srq1, planning]
triggers: [brian onboarding, harness usage, open decisions review]
created: 2026_07_13-00_30
updated: 2026_07_13-00_30
---

# Handover — Enrico → Brian (2026-07-13)

> **Read this first.** It tells you (1) what the harness is and how to open it, (2) what we
> decided in the last two days — including adopting your brand×month proposal, (3) what is
> still open, (4) **what you can move forward on right now without waiting for Enrico**, and
> (5) the questions the project still needs answered. Background detail lives in
> `harness/reviews/2026-07-12_prometheus-warehouse-srq4-handoff.md`.

---

## 1. The harness — what it is and how to open it

- **Single source of truth:** `harness/thesis_tasks.json`. Every task, decision, and blocker of
  the remaining thesis work lives in this one file (62 tasks right now). If it's not in there,
  it doesn't exist.
- **Dashboard:** double-click `harness/dashboard/index.html` — it opens in your browser, no
  server needed. You get overall progress, per-phase bars, the "ready now" queue, what's
  blocked and on whom, and all tracks.
- **Statuses:** `done` · `ready` (executable now, free) · `review` (needs Enrico's eng review) ·
  `enrico` (needs an Enrico decision/approval) · `pending` (waiting on dependencies) ·
  `blocked_money` (paid API call — Enrico unblocks) · `blocked_brian` (waiting on you).
- **Walls:** `money` = worker stops before any paid API call; `enrico` = decision/prose/spend
  approval; `brian` = you.
- ⚠️ **Caveat:** the dashboard has the task data *inlined* in the HTML. If you edit
  `thesis_tasks.json` by hand, the dashboard won't update until the data block is re-injected
  (any Claude session can resync it — just ask). Treat the JSON as truth, the dashboard as a view.

## 2. What happened on 2026-07-12/13 (decisions are in the harness as DEC-* / OPEN-*)

**Discoveries**
- **We can reach the Nielsen warehouse directly** (WH1): RU service principal + pyodbc,
  read-only verified — `csd_clean_facts_v` = 9,824,601 rows. The old "we need Nika/Brian for
  data" assumption was wrong. Your B01 parquet delivery is therefore **no longer blocking**:
  a refetch via the RU secret is proven to work.
- Our local April CSD snapshot is only **25.8%** of the warehouse (2,535,464 rows). What
  exactly is missing (periods? markets? chain detail?) is still to be analysed — see OPEN-CSD.

**Decisions taken (Enrico)**
- **DEC-DATA** — the reproducible SRQ4/benchmark comparison runs on the **frozen April
  snapshots**, not the live warehouse (reproducibility + independence from RU creds).
- **DEC-LLM** — base LLM for all SRQ4 arms = **gpt-5.5** (Prometheus's production model),
  temp 0, identical decoding everywhere. Same-LLM control per Ch5 §5.7.
- **DEC-ARMS** — SRQ4 = **3 arms**: (A) Prometheus + our tuned models served as a tool (the
  artefact); (B) code-as-action — the same agent writes/runs/self-corrects its own forecasting
  code on the snapshot (= what Prometheus effectively is today); (C) floor — plain gpt-5.5,
  no tools, no code execution. Your "vs a regular ChatGPT LLM" is arm C, implemented as plain
  gpt-5.5 (not literal ChatGPT) so the same-LLM control holds.
- **DEC-GRAIN** — **your brand×month proposal is adopted**, exactly as you framed it:
  (4 categories + 1 pooled) × the model set as implemented; chain/region grains dropped from
  active results and documented as limitation (historical depth) + future work; pooled-vs-
  specialized re-verified **from scratch** on the corrected pipeline. One nuance: the pipeline
  actually runs 5 models + a naive floor (SeasonalNaive/Ridge untuned ladder, tuned LGB/XGB,
  ARIMA/Prophet), which matches Ch3 — so we keep all of them, "4 models" undercounted.

**Consequences already applied in the harness**
- Dropped: **B02** (region-vs-month WMAPE test — no longer needed), **V1** (danskvand bychain
  re-aggregation), **T03** resolved (danskvand stays brand×month, tuned XGB 22.0% WMAPE stands).
- New: **S01** — SRQ1 retrain from scratch folding the code-review fixes, including a real
  **target-leakage bug** (`promo_intensity` has `sales_units_t` in its denominator, consumed at
  current t in the tuned benchmark) plus mean-MAPE suppression and a `market_id` assert.
  Expect CSD + energidrikke numbers to move; danskvand/RTD are promo-zero.
- New: **SPIKE1** — feasibility spike on reusing the real Prometheus pieces (E2B template,
  persona, coder loop) for the SRQ4 harness. **T19** — chapter alignment diffs (categories
  5→4, grain-only, 3-arm wording).

## 3. Open decisions (all in the harness — this is the part to react to)

| ID | Decision | State |
|---|---|---|
| **OPEN-BASELINE** | (a) run the *real* graph-engine Prometheus for both arms vs build a faithful harness reusing its real parts (gpt-5.5 + its E2B template + its persona/prompts) with the tool as an on/off flag; (b) snapshot access in the sandbox: parquet direct vs a local SQL layer (DuckDB) so the coder keeps writing SQL | Sparring done; **leaning: faithful shared harness + DuckDB** (single-variable control requires both arms on the same scaffolding; wiring our tool *into* graph-engine = the real integration, which is out of scope by the locked "readiness, not live" decision). Enrico's final call pending SPIKE1. |
| **OPEN-PARAMS** | K repeats (3 vs 5), numeric tolerance, judge model + qualitative dims, drop old template baseline | One-batch call. NB: **GPT-4o is no longer a valid judge** for SRQ4 — same OpenAI family as gpt-5.5 → judge must be another family (Claude/Gemini). |
| **OPEN-CSD** | keep the 26% April CSD slice vs one-time full 9.8M fetch + freeze | Deliberately **last**. With brand×month fixed, the question narrows to: is brand×month DVH EXCL. HD coverage complete in the snapshot? Slice analysis first (free). |
| **T02** | approve the 25 Tier-2 prompts | Postponed by Enrico. |
| **T04/T05/T07** | spend approvals (~$0.2 / ~$9 / ~$25, to re-estimate on gpt-5.5 pricing) | Money wall. |
| **F03** | solo vs group CBS page limit (80 vs 120 standard pages) | Must be confirmed before any cut decisions. |

## 4. What can move forward WITHOUT Enrico — start here

The key point of this handover: **none of the open decisions in §3 blocks the work below.**
They only gate the paid SRQ4 runs (T04 onwards) and the landing of prose into chapters.
Everything here is free (no API), fully specified, and can be done end-to-end right now —
by you, or by a Claude session you drive:

- **S01 — SRQ1 retrain from scratch.** The spec is fully fixed by DEC-GRAIN (brand×month,
  4 categories + pooled, model set as implemented) and it folds the three code-review fixes,
  including the `promo_intensity` target-leakage bug. No open decision touches it. Biggest
  single item on the critical path — the retrained models are also what arm A serves in SRQ4.
- **B03 — EDAs danskvand/energidrikke/RTD + finish Ch4.** Yours, unchanged, independent of
  everything above.
- **OPEN-CSD STEP 1 — the slice analysis.** The *decision* is Enrico's, but the analysis that
  informs it is not: compare the April CSD snapshot vs the warehouse (or vs expected
  dimensions) and establish WHAT the missing 74% is (periods? markets? chain detail?).
  With DEC-GRAIN, the operative check is narrow: is brand×month DVH EXCL. HD complete?
- **T01 — draft the 25 Tier-2 prompts** with computable ground truth. Drafting is free;
  Enrico's approval (T02) only gates *running* them.
- **SPIKE1 — Prometheus reuse inventory.** How much of the real graph-engine Prometheus
  (E2B template, persona, coder prompts) can be reused in the SRQ4 harness. Free as a
  dry-run; stops at the money wall before any paid call.
- **T13 — Ch5 gap analysis** (missing sections vs outline) · **T19 — chapter alignment
  diffs** (prepare only; landing is approval-gated) · **C19/C21** (citations check,
  housekeeping).

If you pick something up, set its status in `thesis_tasks.json` so we don't collide.

## 5. Open questions for the project (not homework for me)

These are the things the project still doesn't know — anyone who can answer or challenge
them should. You have the best view on the data side, so you'll likely spot gaps we missed:

1. **Is the decision list complete?** The harness only tracks what we've thought of. Are
   there pending choices on the preprocessing/EDA/Ch4/data-quality side that should exist
   as OPEN-* entries and currently don't? (Examples of the kind of thing we mean: outlier
   policy per category, how Ch4 treats the partial CSD, whether any feature besides
   `promo_intensity` is contemporaneous with the target.)
2. **Does the leakage fix interact with anything in your pipeline plans?** The retrain will
   shift CSD + energidrikke numbers; if any EDA/Ch4 statement hard-codes the old numbers,
   it needs to be flagged now, not after the retrain.
3. **Is 4 categories the right final scope?** Ch3/Ch4 prose still says five (beer included).
   Dropping beer from the prose is currently treated as a text-alignment fix (T19) — if
   there's a data reason to keep or re-add it, now is the moment to say so.
4. **Is the baseline construct airtight from the data side?** Arm B writes its own SQL/code
   against the frozen snapshot via DuckDB (leaning). If you see a reason the snapshot-behind-
   SQL setup misrepresents what Prometheus sees in production, raise it before we build.

## Key files

| What | Where |
|---|---|
| Task board (source of truth) | `harness/thesis_tasks.json` |
| Dashboard (open in browser) | `harness/dashboard/index.html` |
| Discovery/decisions background | `harness/reviews/2026-07-12_prometheus-warehouse-srq4-handoff.md` |
| SRQ4 protocol spec (open params §8) | `00_thesis_context/methodology/srq4-evaluation-protocol.md` |
| Methodology / architecture / evaluation | `05_thesis_writing/sections-drafts/ch3-methodology.md`, `ch5-framework-design.md`, `ch8-evaluation.md` |
