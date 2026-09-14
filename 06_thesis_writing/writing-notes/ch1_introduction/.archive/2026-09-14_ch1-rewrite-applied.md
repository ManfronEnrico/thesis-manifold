---
name: 2026-09-14_BRANCH_A_ch1-rewrite
description: NOTE - Chapter 1 against BRANCH A. The 8 GB budget contradicts six chapters, the chapter map is off by one from Chapter 5 onward, and the structure section promises nine chapters and eight sections against ten and nine. Resolves all 15 open threads.
category: workflow
applies-to: [ch1_introduction]
triggers: [chapter 1, introduction, branch a, RAM budget, chapter map]
created: 2026_09_14-13_10
updated: 2026_09_14-13_10
snapshot: 2026-09-14_12-32_comment-sweep-and-archive
status: prose ready to paste, awaiting human review
---

# Chapter 1 — BRANCH A pass

Verified at `41ecb76`, fetch clean. Snapshot
`2026-09-14_12-32_comment-sweep-and-archive`. Zotero: **89 items**.

**Notes swept:** `2026-09-14_appendix-citations-ch1.md` — live, not applied,
`status: recommendations - no prose written, awaiting a Ch1 pass`. **This is that
pass**, but the two do not overlap: that note decides which artefacts Chapter 1
should cite, this one fixes what the chapter says. Read both.

**17 threads, 15 open.** Two are already resolved (65, 67) and need no action.

---

# The three that matter most

| | What | Cost |
|---|---|---|
| **1** | The RAM budget says **8 GB** here and **4 GB** in six other chapters | 3 edits |
| **2** | §1.5's chapter map is **off by one** from Chapter 5 onward, and promises **nine** chapters against ten | 1 replacement |
| **3** | The pricing claim carries an unresolved `[CITATION TO ADD]` placeholder | 1 reword |

**All three are visible to a reader who does nothing but read the introduction
and the table of contents.** That is what makes them worth doing before anything
subtler.

---

# Part 1 — the fixes

## Fix 1 — the RAM budget, three sites (threads 36, 43)

### Anchor A — Section 1.2, final paragraph

> "all designed to operate within the 8GB RAM budget characteristic of realistic
> SME cloud deployment."

**Action:** REWORD → *"all designed to operate within the four-gigabyte memory
budget characteristic of a realistic small-provider cloud deployment."*

### Anchor B — Section 1.1, the pricing paragraph

> "whereas a general-purpose instance with eight gigabytes of RAM costs a small
> fraction of that"

**Action:** REWORD → *"whereas a general-purpose instance with a few gigabytes
of memory costs a small fraction of that"*

### Anchor C — Section 1.4 Delimitation

⚠ **Search the section for "eight gigabytes" and any "8GB".** The flow note
records the delimitation as carrying the budget in its reasoning, and it must
match. **NEEDS-BRIAN** if the delimitation argues *from* eight rather than merely
stating it — the reasoning may need a sentence, not a number.

### Note — why four, and why this is the highest-value fix in the chapter

**Six chapters say four; three say eight.** Ch2 §2.2, Ch3 §3.6, §3.7, Ch5 §5.1,
§5.5.6, Ch6 §6.1, §6.8 all say four gigabytes, and the Ch9 and Ch10 rewrites you
have already applied say four. **Chapter 1 is now the only holdout**, alongside
Figure 1, which you already regenerated.

The budget is the thesis's headline design criterion — it appears in the main
research question — and the document cannot disagree with itself about it.

⚠ **Threads 36, 39 and 43 go further than the number**, and they are right: they
argue the RAM framing is over-weighted, because training happens outside the
deployment and serving costs megabytes. **That argument is now won and recorded**
— Ch3 §3.7, Ch9 and Ch10 all state that the budget bound the *selection space*
rather than run time. Chapter 1 does not need to make that argument, but it must
not contradict it. **Fix 2 below adjusts the framing minimally.**

---

## Fix 2 — 1.1, the cost-asymmetry paragraph (threads 39, 40)

### Anchor

**Section 1.1**, the paragraph beginning *"Yet the practical deployment of
predictive AI systems in business settings faces a constraint that the academic
forecasting literature has largely left unexamined"*.

The specific sentence:

> "The cost asymmetry is stark: transformer-based forecasters and locally hosted
> large language models require GPU instances with tens to hundreds of gigabytes
> of accelerator memory, which on major cloud platforms cost on the order of one
> to seven US dollars per hour of continuous operation [CITATION TO ADD:
> cloud-instance pricing source], whereas a general-purpose instance with eight
> gigabytes of RAM costs a small fraction of that."

### Action

REPLACE that sentence.

#### Replace with

> The cost asymmetry is structural rather than marginal: transformer-based
> forecasters and locally hosted language models require accelerator memory
> measured in tens to hundreds of gigabytes, available only on instance classes
> that are an order of magnitude more expensive to run continuously than a
> general-purpose instance with a few gigabytes of memory.

### Note — three problems in one sentence

1. **The placeholder.** `[CITATION TO ADD: cloud-instance pricing source]` is in
   the running text of the first page. Thread 40 says plainly: *"We would need a
   source for that, which we dont have time to check. Reword to fit thesis and
   does not cite."* **The replacement makes no numeric pricing claim, so no
   source is needed.**
2. **The eight-gigabyte figure**, per Fix 1.
3. ⚠ **Thread 39's substantive objection.** *"This thesis is not about running
   LLMs in cloud (API access instead)."* True — and the replacement no longer
   implies the thesis hosts anything. It states the asymmetry as the reason
   **lightweight tabular models** are the viable class, which is the argument
   Chapter 2 §2.2 makes and Chapter 5 measures.

**"An order of magnitude" is the qualitative claim Chapter 2 already makes
without a citation**, so the two chapters now agree and neither carries debt.
This closes **S31** for Chapter 1; the Chapter 10 half was already deleted by
that chapter's rewrite.

---

## Fix 3 — 1.5, the chapter map is off by one (thread 60, and C5 in the flow note)

### Anchor

**Section 1.5 Thesis Structure.** The **entire section**, from *"The remainder of
this thesis is organised into nine chapters"* through the Chapter 9 paragraph.

### Action

REPLACE the whole section.

#### Replace with

> The remainder of this thesis is organised into nine chapters, each
> corresponding to a phase of the Design Science Research process (Peffers et
> al., 2007).
>
> **Chapter 2** reviews the literature across nine thematic sections:
> forecasting as a predictive substrate for FMCG demand; lightweight machine
> learning under computational and deployment constraints; the transition from
> descriptive business intelligence to forecast-informed decision-support; LLM
> agents and tool-mediated reasoning; the reliability, traceability, uncertainty
> and evaluation of agentic outputs; production-oriented agentic systems and
> integration readiness; the research gap; Design Science Research; and the
> synthesis that positions the thesis against the reviewed work.
>
> **Chapter 3** details the research methodology, grounding the thesis in Design
> Science Research and specifying the data source, the forecasting-model
> benchmark, the structured forecast-tool interface, the integration-readiness
> assessment, and the evaluation design that compares dedicated-model
> decision-support against scenarios in which a language model writes and
> executes its own forecasting code.
>
> **Chapter 4** presents the data assessment, characterising the quality,
> structure and forecasting suitability of the Nielsen scanner panel across the
> four beverage categories, and documenting the preprocessing decisions that
> inform the modelling.
>
> **Chapter 5** addresses SRQ1 through the empirical model benchmark, comparing
> lightweight forecasting models across the four categories on accuracy, memory
> footprint and stability, and testing category specialisation against pooling.
>
> **Chapter 6** describes the predictive-extension architecture: the forecasting
> substrate, the structured forecast-tool interface and the bounded tool-using
> agentic layer, together with the integration-readiness capabilities the
> extension requires.
>
> **Chapter 7** addresses SRQ2 through the structured tool interface itself,
> setting out the contract by which a forecast reaches the agent with its
> reliability, uncertainty and traceability preserved, and the checks that
> establish whether each property holds.
>
> **Chapter 8** addresses SRQ4 through the scenario evaluation, comparing
> dedicated-model decision-support against code-writing scenarios on
> correctness, consistency and replicability, and on cost and latency.
>
> **Chapter 9** discusses the contributions, the integration-readiness findings
> and the limitations of the thesis, and identifies directions for future
> research.
>
> **Chapter 10** concludes by answering each subsidiary research question and
> stating the design knowledge the thesis contributes.

### Note — everything that was wrong here

| Was | Is |
|---|---|
| "organised into nine chapters" then lists Ch2–Ch9 | **ten chapters**; Chapter 10 was missing entirely |
| "eight thematic sections" | Chapter 2 has **nine** (§2.1–2.9) |
| Ch5 = architecture, Ch6 = benchmark | **swapped on 2026-09-08.** Ch5 is the benchmark |
| Ch7 = "agentic extension prototype" | Ch7 is **the structured tool interface** (renamed, thread 316) |
| Ch8 = "pilot evaluation ... code-as-action LLM baseline" | the **scenario ladder**; "pilot" and "baseline" are both superseded |
| Ch9 "including pilot-scale evaluation and designed-but-unevaluated calibration" | calibration **was** evaluated; the clause is deleted |
| "the 8GB RAM budget" in the Ch5 paragraph | gone |

⚠ **This is the single most consequential paragraph in the chapter for an
examiner**, because it is the map they read before everything else, and it
currently sends them to the wrong chapter five times.

⚠ **Thread 60 also asks for an in-text reference to Figure 1.** The figure is
already regenerated with the correct budget; what remains is a sentence
referring to it from the body. The current text has *"An overview of the main and
sub research questions can be found in **Figure 1**, below"* — which **is** an
in-text reference. **I read thread 60 as already satisfied; confirm.**

---

## Fix 4 — 1.1, the exogenous-predictor sentence (threads 27, 34)

### Anchor

**Section 1.1**, final sentence of the M4/M5 paragraph:

> "This thesis takes up that direction by incorporating exogenous predictors into
> its forecasting substrate, while extending the problem beyond forecasting
> accuracy alone to how such forecasts can be reliably integrated into a
> resource-constrained agentic decision-support system."

### Action

**KEEP AS WRITTEN.** No edit.

### Note — ✅ these two threads are now VERIFIED-OK, and the reason matters

Threads 27 and 34 both say the thesis adds no exogenous enrichment. **That was
true when written, on 1 September. It is no longer true.**

The substrate carries **four exogenous features** — `n_holidays`,
`days_in_month`, `non_holiday_days` from the Danish public-holiday calendar, and
`promo_intensity` where Nielsen reports it. The holiday calendar is joined from
Nager.Date, cached with a per-year checksum, and **its contribution was measured
rather than assumed**: an ablation tuning both arms independently found the
calendar columns improved accuracy in six of nine category-and-model
combinations (Ch4 §4.3).

Your own reply in thread 29 proposed exactly this — *"option c), simply include
one exogenous variable (the holiday API)"* — **and it was implemented.**

**Resolve 27 and 34 as VERIFIED-OK.** The sentence is accurate as written.

⚠ **Thread 386 in the AI Use Declaration defines exogenous variables** and lists
the ones the thesis uses — including the weighted-distribution measure, which was
**tested and excluded**. That footnote needs correcting; it is in the combined
note.

---

## Fix 5 — 1.3, the SRQ1 and SRQ2 cross-references (C5)

### Anchor A — the SRQ1 paragraph

> "SRQ1 motivates the empirical model benchmark in Chapter 6"

**Action:** REWORD → **Chapter 5**.

### Anchor B — the SRQ2 paragraph

> "SRQ2 motivates the design of a structured forecast-tool interface (Chapter 5)
> and its realisation in a bounded tool-using agentic decision-support layer
> (Chapter 7)."

**Action:** REWORD → *"(Chapter 6)"* for the design. Chapter 7 is correct.

### Anchor C — the SRQ3 paragraph

> "SRQ3 motivates an integration-readiness specification (Chapter 5, assessed in
> Chapters 7 and 9)"

**Action:** REWORD → *"(Chapter 6, assessed in Chapters 7 and 9)"*.

### Note

Same Ch5/Ch6 swap as Fix 3. **These three plus §1.5 are four of the eight stale
cross-references in C5**; the others are in Ch2 (two), Ch3 (one) and Ch6 §6.2
(one). Ch5 §5.7's has already been fixed.

---

## Fix 6 — 1.3, the SRQ1 memory claim (thread 48)

### Anchor

**Section 1.3**, SRQ1 paragraph: *"Accuracy alone is insufficient for production
deployment: a model with marginally lower error but higher memory use or unstable
output is a worse engineering choice under a fixed RAM budget (Klee & Xia,
2025)."*

### Action

**KEEP, with one reword** — *"under a fixed memory budget"* to match the
vocabulary used elsewhere after Fix 1.

### Note — ✅ thread 48 is VERIFIED-OK

Thread 48 says memory efficiency *"is not actually tracked or logged as far as I
know"*. **It is now**, comprehensively: `profiling.csv` records peak fit and
predict memory per model per category, Chapter 5 §5.5.6 reports it, and your own
reply in thread 50 lists the twelve auto-generated appendix tables.

**Resolve as VERIFIED-OK.** Same for **thread 51** on observability and
traceability, which your reply 53 already marks answered — the tool records
`args_match_request`, and Chapter 7 §7.5 is devoted to traceability.

---

# Part 2 — threads needing no prose

| Thread | Verdict |
|---|---|
| **20** — chapter subtitle | **NEEDS-BRIAN.** Suggestion: *A capability gap in a deployed system* |
| **23, 26** — Zotero in-text citation workflow | **FLAGGED** — a mechanical task, not prose. These are your own workflow notes |
| **32** — VERIFY the M5 exogenous claim | ⚠ **Verify against Makridakis et al. (2022) before the viva.** The claim is that exogenous variables "materially improved forecasting accuracy" in M5. The source is in Zotero; this is a read, not a rewrite |
| **54** — SRQ4 is very long | **NEEDS-BRIAN.** It is long, and it is the only SRQ carrying two clauses. ⚠ Shortening it means editing the research question, which appears in Ch3, Ch8, Ch9 and Ch10 — **not a late edit.** My recommendation: leave it |
| **55** — will we ship the repository | **FLAGGED** — the `/submission-export` skill exists for exactly this |
| **65, 67** | ✅ already RESOLVED |

---

# Comment ledger — all 17 threads

| Thread | Verdict |
|---|---|
| 20, subtitle | **NEEDS-BRIAN** |
| 23, 26, citation workflow | **FLAGGED** — mechanical |
| 27, 34, exogenous predictors | ✅ **VERIFIED-OK** — implemented since the comment |
| 32, M5 claim | **FLAGGED** — verify against the source |
| 36, 39, 43, RAM framing | **ADDRESSED** — Fixes 1, 2 |
| 40, pricing placeholder | **ADDRESSED** — Fix 2 |
| 48, 51, memory and traceability | ✅ **VERIFIED-OK** — implemented, Fix 6 |
| 54, SRQ4 length | **NEEDS-BRIAN** — recommend leaving it |
| 55, repository | **FLAGGED** — submission-export |
| 60, Figure 1 reference | **LIKELY DONE** — confirm |
| 65, 67 | ✅ already resolved |

**17 of 17 accounted for. 6 addressed in prose, 4 verified already done, 4
flagged as tasks, 3 need your decision.**

---

# Citations

**No new sources.** Fix 2 removes a placeholder by removing the claim that needed
it; every other fix edits existing text. Peffers et al. (2007) in §1.5 is already
cited and in the library.
