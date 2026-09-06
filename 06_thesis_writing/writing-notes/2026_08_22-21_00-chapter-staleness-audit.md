---
name: chapter-staleness-audit
description: Audit of which thesis chapters contradict the artefacts on disk as of 2026-08-22, what the corrected values are, and which errors the automated fact-checker cannot catch.
category: reference
applies-to: [ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10]
triggers: [revising a chapter, checking whether a number is current, planning the writing pass]
created: 2026_08_22-21_00
updated: 2026_08_22-21_00
---

# Chapter staleness audit — 2026-08-22

Two sources: `check_chapter_facts.py` (automated, catches stale *phrases*) and a
manual number-by-number comparison against the results files (catches stale
*values*, which the tool cannot see).

## Automated results — 42 ERROR, 6 CHECK

| Chapter | Items | Dominant cause |
|---------|------:|----------------|
| ch1-introduction | **1** | one benign mention of totalbeer while explaining its exclusion — **effectively clean after the 2026-08-22 rewrite** (was 46) |
| ch3-methodology | 10 | LLM-as-judge, Claude as the model, System A/B vocabulary |
| ch4-data-assessment | 2 | category count / period count |
| ch5-framework-design | 3 | System A/B vocabulary |
| ch7-synthesis | 9 | LLM-as-judge, Claude, E2B/Code-Interpreter |
| **ch8-evaluation** | **11** | LLM-as-judge (N=50, GPT-4o), Claude, E2B |
| ch9-discussion | 5 | LLM-as-judge, Claude, System A/B |
| ch10-conclusion | 3 | inherited from the above |
| **ch6-model-benchmark** | **0** | **but see below — this is the most misleading result in the table** |

## THE CRITICAL FINDING: ch6 passes the checker and is wrong throughout

`check_chapter_facts.py` matches known-stale **phrases**. It has no rule for a
**number that used to be right**. Ch6 is almost entirely numbers, so it scores zero
errors while contradicting every current results file.

### Headline accuracy table (ch6 lines 136–143)

| Category | ch6 claims (XGBoost) | **current (cv_metrics.csv)** | drift |
|----------|---------------------:|-----------------------------:|------:|
| CSD | 16.5% | **15.2%** | −1.3pp |
| danskvand | 23.8% | **20.9%** | −2.9pp |
| energidrikke | 11.4% | **13.0%** | +1.6pp |
| RTD | 31.0% | **36.1%** | **+5.1pp** |

Every figure is wrong. RTD by 5pp. **And ch6 line 158 claims energidrikke "reaches
11.4% WMAPE, near the ≤15% target"** — the current figure is 13.0%, still under target
but the sentence cites a number that no longer exists.

### Baseline comparison table (ch6 lines 167–177)

| Category | ch6 ARIMA | **current ARIMA** |
|----------|----------:|------------------:|
| CSD | 24.2% | **21.8%** |
| danskvand | 33.4% | **33.5%** |
| energidrikke | 15.7% | **19.4%** |
| RTD | 48.2% | **53.3%** |

The verdict column ("ML wins +7.7pp" etc.) is computed from two stale numbers, so
every margin is wrong.

### What ch6 is missing entirely

1. **The simple benchmarks do not appear.** Naive, seasonal-naive and drift were added
   2026-08-22 and are the standard benchmark set. Their absence is the single most
   likely examiner question.
2. **Seasonal-naive beats every tuned model on RTD** (27.3% vs 31.8–36.1%). This is the
   M4 finding reproduced on this data. It must be reported, not omitted.
3. **The pooled-vs-per-category result is absent** — SRQ1's third named axis. The
   crossover at ~750–1000 training rows, replicated across both algorithms.
4. **Ridge is absent**, including the finding that per-brand Ridge is legitimate on two
   categories and unusable on two.
5. **Tuning protocol is stale**: line 42 says "Optuna ≤50 trials"; it is now **100
   trials with 4-fold expanding-window CV**. Line 147 claims tuning improved WMAPE
   "2–4pp" — recompute.
6. **The dual-objective result is absent**: tuning for medMAPE costs 8–13pp of WMAPE
   and buys 2–3pp of medMAPE.
7. **Line 26 cites `auto_arima` (pmdarima)**, which the implementation does not use —
   `srq1_baselines_stat.py` uses `SARIMAX(order=(1,1,1))` because pmdarima was
   unavailable.

### The RAM claim (ch6 lines 190–192) is the one to fix first

Ch6 states peak RAM is "orders of magnitude under the 8 GB budget", which is **true and
measured** (3–4 MB). But `04_thesis_results/generate_figures.py::fig4_ram_budget` is
**entirely hardcoded**, including a literal 512 MB "active ML model".

**The chapter's prose and its own figure contradict each other.** Fix the figure to
match the prose, not the reverse.

The honest version is a stronger argument: *the trained model is the cheap part; the
agent runtime is where the budget goes* — now measurable with the Prometheus engine
running locally.

## Ch8 — the most stale chapter, and it needs restructuring not patching

11 automated errors, all pointing the same way: **ch8 describes an evaluation that is
no longer the design.**

| Ch8 says | Reality |
|----------|---------|
| GPT-4o as LLM-as-Judge, N=50 | **Judge dropped (B-DEC-2)** — all metrics programmatic |
| N=50 stratified test cases | **1 prompt × N repeats × 12 stratified brands** |
| claude-sonnet-4-6 | **gpt-5.5-2026-04-23** (DEC-LLM) |
| E2B key "not configured" | E2B key configured; template built and verified |
| Two-approach comparison | **Five-scenario ladder** (A–E), sixth proposed |

**This is a rewrite, not an edit.** The chapter's structure assumes a judge-scored
two-arm comparison; the design is a capability ladder with programmatic measures.
Do not attempt line-by-line patching.

## Ch9 — mostly inherited, one structural item

Four of five errors are inherited vocabulary (judge, Claude, E2B). The structural item
is **line 85's "System A / System B"** framing, retired in favour of the scenario
ladder — and note the old lettering ran the *other way*, so a careless rename inverts
the meaning.

Ch9 will also need the SRQ3 framing agreed 2026-08-22: readiness criteria **derived
from a working integration**, without claiming a completed production deployment.

## Recommended order of work

1. **Ch6 numbers** — highest value per hour. The chapter's structure is sound; the
   values are stale. Regenerate from `cv_metrics.csv` and `stat_baselines.csv`.
2. **`fig4_ram_budget`** — a fabricated figure contradicting its own chapter's prose.
   Cheap to fix, embarrassing if found.
3. **Ch8 rewrite** — largest job, blocked until the D/E runs produce results anyway.
4. **Ch3 methodology** — 10 errors, and it is where the judge protocol is *specified*
   rather than merely referenced.
5. **Ch9/Ch10** — mostly follow from the above.

## A caution about the fact-checker

**Zero errors does not mean current.** `check_chapter_facts.py` catches stale phrases,
not stale numbers, and ch6 demonstrates the gap emphatically.

Worth adding number-level rules for the headline accuracy figures, so a regenerated
results file automatically flags the chapters citing the old values. Until then, treat
every number in a chapter as unverified unless traced to a results file by hand.

## Related

- `04_thesis_results/srq1/cv_metrics.csv` — current tuned accuracy (supersedes `tuned_metrics.csv`)
- `04_thesis_results/srq1/stat_baselines.csv` — eight benchmark methods
- `04_thesis_results/srq1/pooled_summary.md` — pooled vs per-category
- `srq1-model-ladder-and-baselines.md`, `srq1-pooled-vs-per-category.md`,
  `srq1-tuning-and-validation-protocol.md` — the write-up notes for the new material
- `plans/P0040_.../findings.md` — F49–F65

---

# Deferred: the full prose read (Brian, 2026-08-22)

**This audit is not sufficient and must not be treated as one.** Phrase-matching and
grepping were used because they are cheap, not because they are adequate. They catch
*known-stale strings* and, as ch6 demonstrates, miss stale numbers entirely. Neither
touches:

- whether an argument actually follows from its evidence
- whether a claim is supported by the source cited next to it
- whether two chapters contradict each other
- whether the prose says what the author meant
- whether a section still belongs, given how the design changed

**The plan Brian set:** work through the chapters **incrementally, one at a time**,
spending the full compute budget on *reading the whole text* rather than scanning it,
then making considered edits. Not now -- a separate, dedicated effort.

## Why incremental rather than batch

A whole-thesis pass forces skimming, which reproduces exactly the failure this audit
found: surface checks that miss substance. One chapter at a time, read completely,
with the relevant results files open alongside, is the only approach that catches
argument-level problems.

## Suggested protocol per chapter, when that work starts

1. Read the chapter **in full**, without searching, before making any judgement.
2. Read the results files it cites, in full.
3. Check every number against its artefact by hand.
4. Check every citation against the P0041 register -- is the source `VERIFIED`?
5. Check claims against the *other* chapters for contradiction.
6. Only then edit.

Budget roughly one session per chapter. Ch6 and Ch8 will need more.

## Priority for that pass

Highest first, reflecting how much has changed underneath them:

| Chapter | Why |
|---------|-----|
| ch6-model-benchmark | every number stale; missing the whole 2026-08 body of work |
| ch8-evaluation | describes a design that no longer exists |
| ch2-literature-review | never audited at all -- see the separate literature audit |
| ch3-methodology | specifies a dropped protocol |
| ch9-discussion | conclusions drawn from stale results |
| ch5, ch7 | vocabulary and framing |
| ch4, ch10 | smaller inherited items |
