---
pid: P0042
created: 2026-08-25 12:45:00
updated: 2026-08-25 12:45:00
status: focus
focus_detail: "Sequencing plan for the funded phase. Two workstreams that must not block each other: (A) NotebookLM review rounds, run in the browser, no API budget; (B) the remaining SRQ4 scenario runs in a cloud session. IMPORTANT: the A/B/C ladder is ALREADY DELIVERED (2026-08-19, $4.92) -- C beat B on every run of both brands. Funding unblocks D_prometheus/E_prometheus_model plus the optional scale-up, which externally replicate an existing result rather than producing the first one. This plan does NOT duplicate P0039/P0040 task tables -- it orders them and states the go/no-go gates."
---

# P0042 — Funded testing and review sequencing

## Why this plan exists

Three things became true on 2026-08-25 and they interact:

1. **Funding landed**, unblocking P0040 tasks 4–10 (Prometheus D/E) and the
   optional P0039 scale-up.
2. **The literature and modelling verification runs completed**, and their corrections
   are merged. Ch2 and Ch6 now pass the fact-checker clean.
3. **The methodology corpus arrived** (14 Saunders chapters), enabling a third
   verification run.

P0039 and P0040 already hold detailed, current task tables. **This plan does not repeat
them.** It answers the question those plans cannot answer individually: *in what order,
and what must be true before each step starts.*

---

## The two workstreams

They are genuinely independent and should run in parallel.

| | **A — Review rounds** | **B — Scenario runs** |
|---|---|---|
| Where | NotebookLM browser + this repo | Cloud session |
| Cost | none | API spend |
| Blocks on | nothing | funding *(now cleared)* |
| Owner | Brian, interactively | separate session |
| Produces | chapter corrections | D/E results + replication check |

**The one coupling:** workstream B produces the numbers that Ch7/Ch8 report, and
workstream A's Ch7/Ch8 review cannot run until those numbers exist. Everything else is
parallel. Do not serialise them.

### What already exists — read before planning any run

**The A/B/C ladder is delivered** (2026-08-19, $4.92 total). See
`04_thesis_results/srq4/RESULTS_2026-08-19.md`. On HARBOE:

| Scenario | median APE | CV across repeats | latency | cost (3 runs) |
|----------|-----------:|------------------:|--------:|--------------:|
| A_plain | 35.1% | 3.65% | 108.7 s | $1.482 |
| B_data | 17.3% | 5.27% | 115.4 s | $0.830 |
| **C_model** | **13.8%** | **0.00%** | **5.9 s** | **$0.020** |

`C_model` beat `B_data` on **every run of both brands**; C's worst run beat B's best.
A→B is +17.8pp and B→C is +3.5pp — so **most of the value comes from data access**, and
model integration adds a smaller accuracy gain whose case rests on consistency (CV 0.00%),
cost (~28×) and latency (~22×). That framing is already written into the results file and
should not be quietly upgraded later.

> **The P0039 in-file task table still reads all-pending and is stale.** `PLANS_INDEX.md`
> is the accurate record. Do not re-run tasks 1–6.

---

## Workstream A — review rounds

### A1. Methodology verification *(ready now)*

**Upload:** 14 Saunders PDFs + `ch3-methodology.md` + `ch4-data-assessment.md` +
`02-Methodology_Review/Methodology_Review-00-MASTER-verification-brief.md`

**Why this is the highest-value review remaining.** Unlike the literature run, where 36
papers each backed a claim or two, here **one source underpins two chapters**. A
misapplied framework is a structural fault, not a bad sentence. MR-01/02/03 in the brief
each carry that risk: research purpose, case-study type, and philosophy.

**Expected output shape:** the same verdict format as the completed runs, plus a
coherence read (Part 4 of the brief) that the earlier runs had no equivalent of.

**Known independent of the run** — 10 repo fixes (S1–S10 in the brief) that need no PDF.
S5 (the specified LLM judge) and S9 (brand × retailer grain) are the two that would
actively mislead an examiner.

### A2. Improvement rounds *(ready now, run after A1 or in parallel)*

**Use:** `00-REVIEW-METHOD-and-improvement-questions.md`, section by section, with the
corresponding corpus re-uploaded.

**Why this is a different exercise from verification** and why it comes second: the
verification runs asked *"does the source say this?"* — a closed test over a fixed
corpus. It cannot find claims that have **no** citation, arguments that are incomplete,
or framing that is wrong. Those need a different question, which is what that document
asks.

**Discipline that keeps this bounded:** every question carries a standing instruction to
answer only from the uploaded corpus, and to reply `corpus gap: <one line>` rather than
recommending literature. Gaps are collected and decided **in one batch at the end**, not
one paper at a time. This is the explicit guard against the round turning into an
open-ended reading list.

### A3. Chapter reviews *(gated)*

Per-chapter NotebookLM passes for Ch5, Ch7, Ch8, Ch9, Ch10.

**Gate:** Ch7 and Ch8 must wait for workstream B. Reviewing a chapter whose numbers are
about to change wastes the run and risks correcting toward a stale result. Ch5 can go any
time.

---

## Workstream B — scenario runs

**Read `plans/P0039_.../task_plan.md` and `plans/P0040_.../task_plan.md` for the task
detail.** What follows is the ordering and the gates.

### Sequence

| Step | From | What it establishes | Gate before starting |
|---|---|---|---|
| ~~B0~~ | ~~P0039 t1–6~~ | ~~A/B/C ladder~~ | **DONE 2026-08-19** — do not re-run |
| B1 | P0040 t4 | Prometheus engine runs locally on the shipped project | template built (done, F42) |
| B2 | P0040 t5 | `D_prometheus` run on the SRQ4 prompt, logged, cost captured | B1 |
| B3 | P0040 t6 | `forecast_demand` ported to the verified API; `chain` dropped | B1 |
| B4 | P0040 t7 | tooled project registered; `E_prometheus_model` run | B2, B3 |
| B5 | P0040 t8–9 | **D→E checked against B→C for agreement**; engine RAM measured | B4 |
| B6 | P0040 t10 | write-up folded into the SRQ4 results section | B5 |
| B7 | P0039 remainder *(optional)* | scale-up 5 brands × 10 repeats (~$35); Coca Cola `A_plain` (~$1.27); `C_model` re-run on re-tuned models (~$0.04) | B5 — lower priority than D/E |

### The gates that matter most

**Gate 1 — freeze the D/E scope in writing before B2 runs.** Brands, prompt count and
repeat count must be committed to the plan file *before* any D/E result is seen. A/B/C
was run at 2 brands × 3 repeats; D/E should match that unless there is a stated reason,
because **a scope difference between the two ladders weakens the B→C / D→E comparison
that B5 exists to make**. Commit the choice either way, in writing, first.

**Gate 2 — cost is already measured, so use the real figures.** A/B/C cost $4.92 for 18
runs; E2B is ~$0.0001/run (F38). These are measurements, not estimates. The optional
scale-up is ~$35. Decide the D/E repeat count against these numbers rather than
re-deriving them.

**Gate 3 — decide before B5 what a disagreement means.** If D→E contradicts B→C in
direction, that is a finding and must be reported as one. Write that commitment down now,
while the answer is unknown.

### What B6 is actually for

D→E and B→C are **the same intervention on two different orchestrators**. If they agree
in direction, that is a materially stronger claim than either alone, and it is the
strongest evidence the thesis can produce for its central premise. If they *disagree*,
that is also a finding and must be reported as one — decide now that it will be, before
knowing which way it goes.

---

## Reproducibility tiering (state this in Ch3 before B runs)

| Tier | Scenarios | An examiner can rerun? |
|---|---|---|
| Core | A_plain, B_data, C_model | **yes** — repo + one API key |
| Ecological | D_prometheus, E_prometheus_model | **no** — NDA/proprietary engine |

Presenting these as two tiers that *agree* is stronger than implying the whole ladder is
reproducible. **This is a framing decision to write into Ch3 now**, not a caveat to add
after results arrive.

---

## Deferred, with reasons

| Item | Why not now |
|---|---|
| `F_ensemble` (P0040 t12) | ~$2, decided (F55), but it only determines whether one deferral sentence gets written. Run it alongside the optional scale-up if convenient; it gates nothing |
| Ch3 rewrite | Wait for A1 — S1–S10 plus whatever the Saunders run returns should be one edit, not two |
| Ch7/Ch8 rewrite (P0040 t23) | Blocked on B6 by construction. **Note Ch7/Ch8 can already be partly written** against the delivered A/B/C result; only the D/E half is pending |
| Second-round downloads | Ouyang, Atıl, Schwartz, Chen (§2.5) + whatever A2 returns as `corpus gap`. **One batch** |

---

## Chapter staleness — the standing backlog

`check_chapter_facts.py` currently reports **46 errors**, none in Ch2 or Ch6 (both clean
as of 2026-08-25). The rest are pre-existing:

| Chapter | Items | Nature |
|---|---|---|
| Ch3 | 10 | S1–S10 above; mostly stale scope + the dropped judge |
| Ch8 | 13 | structure assumes a two-arm judge-scored design |
| Ch7 | 9 | built around the dropped judge |
| Ch9 | 7 | stale numbers, judge, E2B, System A/B vocabulary |
| Ch10 | 3 | inherited vocabulary |
| Ch5 | 3 | — |
| Ch4 | 2 | — |
| Ch1 | 1 | a CHECK, correct in context (beer exclusion) |

**Do not fix Ch7/Ch8/Ch9 by hand before B7.** Their numbers change. Ch3, Ch4, Ch5 are
safe to fix now.

Also outstanding: `fig4_ram_budget` is hardcoded (512 MB) and contradicts §6.5.6's
measured 3–4 MB — P0040 t21.

---

## Tasks

| # | Task | Stream | Depends on | Status |
|---|------|--------|-----------|--------|
| 1 | Run A1: methodology verification in NotebookLM | A | — | pending |
| 2 | Apply S1–S10 + A1 findings to Ch3/Ch4 as one edit | A | 1 | pending |
| 3 | Run A2 improvement rounds, section by section | A | — | pending |
| 4 | Consolidate every `corpus gap` into one download decision | A | 3 | pending |
| 5 | Freeze the D/E scope in writing (**gate 1**) | B | — | pending |
| 6 | B1: get the Prometheus engine running locally | B | — | pending |
| 7 | B2: run + log `D_prometheus` | B | 5, 6 | pending |
| 8 | B3–B4: port `forecast_demand`; run `E_prometheus_model` | B | 6 | pending |
| 9 | B5: check D→E agrees with B→C; measure engine RAM | B | 7, 8 | pending |
| 10 | B6: write the SRQ4 results section | B | 9 | pending |
| 15 | *(optional)* P0039 scale-up + Coca Cola A_plain + C_model re-run | B | 9 | pending |
| 11 | Rewrite Ch7/Ch8 against real results | A | 10 | pending |
| 12 | Run A3 chapter reviews for Ch7/Ch8/Ch9/Ch10 | A | 11 | pending |
| 13 | Regenerate `fig4_ram_budget` | B | — | pending |
| 14 | Write the reproducibility tiering into Ch3 | A | — | pending |

---

## Related

- `plans/P0039_2026-08-19_01-45_srq4-system-a-vs-b/` — SRQ4 A/B/C task detail
- `plans/P0040_2026-08-20_prometheus-scenarios-d-e/` — Prometheus D/E task detail + findings F1–F67
- `05_thesis_writing/notebookLM/00-REVIEW-METHOD-and-improvement-questions.md` — A2 input
- `05_thesis_writing/notebookLM/02-Methodology_Review/Methodology_Review-00-MASTER-verification-brief.md` — A1 input
