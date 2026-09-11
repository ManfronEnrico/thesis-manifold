---
pid: P0048
created: 2026-09-07 13:51:00
updated: 2026-09-11 13:30:00
status: in_progress
focus_detail: "IN SESSION 2026-09-11: Chapter 5 prose, resume at 5.2.2 — 5.0/5.1/5.2.1 are applied and 3 comments closed (49->46 threads). THE 4 GB QUESTION IS SETTLED: 5.1 now says 4 GB, so 5.5.6 is the section to change, not 5.1. Book PDFs are local at C:\Users\brian\Downloads\Hyndman Book (2021), 42 sections. Per section: verify Word+comments against the repo, then find book support, then argue AROUND what is trained (no re-invention), then note separately what a re-run would buy. Enrico's handover validated as S17-S20: calibration fits XGBoost where energidrikke and RTD serve LightGBM (selection is on CV, not test — do not switch it); profiling.csv is 2026-09-01 and says 13 features; the confidence index is dead two ways (rel width cancels the forecast value, and the second term is identically zero) so every forecast tiers Low — recalibrating cut-offs does NOT fix it, recommend dropping the field; Ch7 rewritten and present. Live state: writing-notes/ch5_model_benchmark/ch5-session-state.md."
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
| 5 | **Ch5 prose + source support + retraining decision** | section by section; see the session below | **NEXT (2026-09-11)** |
| 5b | Ch6–Ch9 prose + citations | section by section | pending |
| 6 | **Inherited: draft bullets** | ch3/ch6 merge, ch4/ch7/ch8, short files, verify | pending (tasks 11–16) |
| 7 | **Inherited: Brian's writing items** | 5 Word threads, NotebookLM claims verification | pending (tasks 9–10) |
| 8 | **Chapter reorder: swap Ch5 and Ch6** | Word half DONE (Brian, 2026-09-08); 37 prose refs verified + staged in `ch5-ch6-swap-reference-repair.md`. Repo half (PATHS.py, 2 folder renames, 6 diagram stems) still open — P0050 | **prose ready to paste**; see F14 |

**Phase 4 is not fully blocked.** §4.1/§4.2 narrative and §4.3/§4.4 (blocks P1/P2)
can proceed now; only the horizon subsection and the numbers that move with the
re-run wait on phase 3.

## The next session: Chapter 5 to finished prose (2026-09-11)

Chapter 5 is the model-benchmark chapter, and it is **the last chapter where a
re-run could still change what the thesis claims**. Everything after it consumes
SRQ1's output rather than producing it. So this session does two things at once:
write the chapter, and settle whether anything needs retraining before the rest
of the thesis is built on top of it.

### Three inputs, all on disk

| Input | What it gives |
|---|---|
| `writing-notes/ch5_model_benchmark/ch5-prose-pass-followup-01.md` | every section walked in document order, verified against the repository, with paste-ready prose and all 49 comment verdicts |
| the 40 FPP3 section PDFs (Google Drive, modelling-papers) | the literature the chapter cites, printed section by section |
| `notebookLM/03-Modelling_Review/fpp3-first-pass-findings.md` | six sections already read, with page-located quotations; 34 unread |

### The method, per section

Work top to bottom through the chapter. For each section:

1. **Verify against the repository first.** The follow-up already did this at
   `303f00f`; re-check anything the fetch shows has moved.
2. **Read the FPP3 sections that bear on it**, and quote from **where the answer
   is**, not from the opening paragraph.

   ⚠ **A caution earned on 2026-09-10.** The first pass read six PDFs in full but
   quoted almost entirely from pages 1 and 2, because that is where each section
   states its thesis and the reading stopped once a usable quote appeared. The
   quotations were real and checkable, but the coverage was not what it looked
   like. **Where a section works an example over eight pages, the finding that
   matters is often on page 6.** Section 12.2's strongest sentence for this thesis
   was on its last page.
3. **Write the prose**, with the citation attached to the claim it actually
   supports.
4. **Record what could only be fixed by retraining**, rather than working around
   it silently.

### The retraining question, which is the second deliverable

The chapter currently carries claims that a re-run would change. The session
produces a decision on each, and **the default is to narrow the claim rather than
re-run**. A re-run costs hours and invalidates every downstream number; a narrowed
claim costs a sentence.

For each candidate, the note records **what a re-run would change, what it costs,
and what the chapter says instead if we do not**:

| Candidate | Why it is open | Cheapest alternative to a re-run |
|---|---|---|
| **ARIMA has no seasonal order** on monthly data the chapter calls strongly seasonal | FPP3 9.9 works only seasonal models on monthly data; the current limitation calls this a tuning gap when it is structural | state it as a **structural** limitation and say the comparison understates the family. Wording drafted in the first-pass findings |
| **ETS is absent** from a claimed spectrum of inductive biases | 5.1 says the five families "span the inductive-bias spectrum" and one of the two dominant classical families is missing | **narrow the claim.** Say which biases are spanned rather than claiming the spectrum |
| **Operational figures measured on 13 features** | `profiling.csv` still reports `n_features: 13`; the model uses 18 (H12) | report them as a **floor** and say so. The margin against the budget is ~100x, so a proportional increase does not approach it |
| **The pooled comparison ran on 12 features** | every other result in the chapter is on 18; the two arms are internally consistent but not comparable with the rest | state the scope: it answers a question about **training rows**, not features |
| **Ridge clipping has no stated bound** | FPP3 13.3 handles bounding through the transformation and calls an artificial constraint "unrealistic" | **state the bound** and explain that the log fit already imposes positivity, so this is upper-tail control rather than a positivity fix |

**Only the first is arguably worth a re-run**, and only if a seasonal ARIMA is
cheap on four categories. Everything else is a wording change.

### One finding that reaches outside the chapter

FPP3 5.6 establishes that a back-transformed log forecast is the **median**, not
the mean, and that medians do not aggregate additively. The forecast tool serves
per-brand forecasts and nothing warns a consumer against summing them to a
category total. **That is an SRQ2 item**, and this session should raise it rather
than resolve it here.

### Two questions only Brian can settle

Both are recorded in the follow-up and neither blocks the writing:

1. **Sections 5.1 and 5.5.6 state different memory budgets** — 4 GB and 8 GB. The
   prose carries a placeholder until this is fixed in one place.
2. **Comment 225 tags the validation scheme `OUTDATED`** and the scheme matches
   the code, the citation checks out, and the section is already prose. The
   follow-up guesses it means the missing K-fold justification and drafts that
   addition. If it means something else, say so.

### Done means

- every section of Chapter 5 is prose, verified, with its comments answered;
- every citation is attached to a claim the source actually supports, quoted from
  the page that supports it;
- the retraining decision is written down with its cost, so it is not re-derived;
- anything deferred is on a register rather than in someone's head.

---

## Sequencing constraints

1. **P2 before the holiday note's P1.** The holiday note says amend "14 → 17"
   features. P0048 F3 establishes the base is **13**, not 14, so the corrected count
   is **16**. Applying them in the wrong order bakes in an off-by-one.
2. **Holiday note P3 and P4 ship together** (constraint inherited from P0047): P4
   leaves two sentences claiming "every input held identical", which are only true
   once P3 records that XGBoost is pinned to one thread.
3. **Do not write the §4.2 EDA pass before phase 3.** Every figure there is stale;
   doing it twice is waste.
4. **Chapter 5 before any further re-run.** It is the last chapter that consumes
   SRQ1 as a producer rather than a consumer, so a retraining decision taken after
   it is written costs the chapter twice. This is why the prose session and the
   retraining decision are one session and not two.
5. **Do not re-run to fix a wording problem.** Four of the five open items in the
   table above are claims that are too strong for what was measured, not
   measurements that are wrong. Narrowing is the cheaper and usually the more
   honest fix.
6. **Phase 8 (the swap) before phase 5 (Ch5–Ch9 prose).** Every cross-reference
   written before the swap has to be rewritten after it. The swap is now a small,
   fully-specified edit (findings F(new)); doing it first is strictly cheaper.
   It does **not** block phase 4 — Ch4's anchors are unaffected by renumbering.

## Related

- `06_thesis_writing/writing-notes/srq1-forecast-horizon-defect-and-split-correction.md`
  — this session's deliverable: bullets, anchors, prose, provenance
- `06_thesis_writing/writing-notes/srq1-holiday-enrichment-result-and-limitations.md`
  — P0047's deliverable; ready to paste, interacts via constraint 1
- `plans/.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision/LOCKED_STATE.md`
  — the determinism contract (`XGB_N_JOBS=1`). **Any re-run in phase 3 must honour
  it or the new numbers are not reproducible either.**
- `06_thesis_writing/writing-notes/ch5_model_benchmark/ch5-prose-pass-followup-01.md`
  — the sequential Chapter 5 pass, every section verified at `303f00f`
- `06_thesis_writing/writing-notes/ch5_model_benchmark/ch5-pending-source-review.md`
  — which Chapter 5 sections must not be closed before the source review lands
- `06_thesis_writing/notebookLM/03-Modelling_Review/forecasting-book-sections-for-citation-verification.md`
  — Brian's section-to-claim mapping and the NotebookLM brief
- `06_thesis_writing/notebookLM/03-Modelling_Review/fpp3-first-pass-findings.md`
  — six sections read, page-located; 34 unread, with the next six named
- `.claude/rules/prose-insertion-discipline.md` · `.claude/skills/write-prose-from-bullets/`
- `.claude/rules/writing-surface-authority.md` — the `.docx` is authoritative
