---
name: 2026-09-14_BRANCH_A_ch2-pass
description: NOTE - Chapter 2 against BRANCH A. The research-gap section still labels all four contributions "designed, pending", the judge-model method is promised, and four verification threads are now answerable from measured results. Resolves all 15 threads.
category: workflow
applies-to: [ch2_literature_review]
triggers: [chapter 2, literature review, branch a, research gap, judge model]
created: 2026_09_14-13_10
updated: 2026_09_14-13_10
snapshot: 2026-09-14_12-32_comment-sweep-and-archive
status: prose ready to paste, awaiting human review
---

# Chapter 2 — BRANCH A pass

Verified at `41ecb76`, fetch clean. Snapshot
`2026-09-14_12-32_comment-sweep-and-archive`. Zotero: **89 items**.

**Notes swept:** `2026-09-14_appendix-citations-ch2.md` — live, not applied,
recommendations only. No overlap with this note.

**15 threads, 10 open, 5 already resolved** (71, 72, 73, 74, and the three
2.2 hosting threads 81, 82, 83 which are marked resolved).

**Chapter 2 is the best-structured chapter in the thesis** — the flow read said
so, and it holds up. Nine sections, each closing by naming what the next
supplies. **Nothing here is a rewrite.** Two fixes are substantive, the rest are
verifications you can now answer.

---

# Part 1 — the two substantive fixes

## Fix 1 — 2.7, the research gap still says the thesis is unfinished (thread 95)

### Anchor

**Section 2.7 Research Gap.** The four bolded contribution statements, beginning
*"Predictive substrate (SRQ1): designed; benchmark to be built."* and ending
*"...planned at the scale of a pilot in the first instance rather than a full
study."*

### Action

REPLACE all four.

#### Replace with

> **Predictive substrate (SRQ1).** A memory-profiled benchmark of lightweight
> forecasting models across multiple FMCG beverage categories, characterising the
> accuracy, efficiency and specialisation trade-off under a constrained compute
> budget.
>
> **Structured forecast-tool interface (SRQ2).** A tool and action interface
> exposing forecasts and their uncertainty to a tool-using agent, with
> traceability treated as an explicit design objective rather than as a property
> assumed to follow from logging.
>
> **Integration readiness (SRQ3).** A specification of the architectural and
> operational capabilities a production-oriented agentic system requires in order
> to integrate forecast-informed decision-support, derived from an integration
> performed against a real production system rather than from architectural
> analysis alone.
>
> **Evaluation (SRQ4).** A comparison of dedicated-model agentic
> decision-support against scenarios in which a language model writes and
> executes its own forecasting code, on correctness, consistency and
> replicability as primary dimensions and cost and latency as secondary ones,
> conducted as a ladder in which capability is added one variable at a time.

### Note — why this is the highest-value small fix in the document

Your comment: *"I suppose the 'designed; …' parts are the current status? We must
remove that in the final version if those are meta commetns."*

**They are, and they must.** As written, the literature review tells an examiner
that the benchmark is *"to be built"*, the assessment *"planned"*, and the
evaluation *"pending"* — in a submitted thesis where all four have landed. It is
**four label deletions** and it changes the chapter from a proposal into a thesis.

⚠ The replacement also drops **"at the scale of a pilot"**, which is superseded:
63 funded runs on a fixed design is not a pilot. And **"code-as-action baseline"**
becomes the ladder, matching Ch8, Ch9 and Ch10.

---

## Fix 2 — 2.5, the judge-model method (thread 92)

### Anchor

**Section 2.5**, final paragraph, the clause:

> "using a separate judge model with bias awareness and a human-rated subset"

### Action

REPLACE the sentence containing it.

#### Replace with

> Applied to this thesis, the implication is narrower and stricter: where a claim
> can be checked arithmetically against a recorded source, it should be, and a
> model-based judgement should be reserved for claims that cannot. Every quantity
> an agent states in this evaluation is extracted and compared against the
> payload the tool returned, so the reliability check is a numeric comparison
> rather than an assessment, and no language model judges any output.

### Note

Your comment: *"As far as I know we removed the judge model entirely."* Correct
— and Chapter 7 §7.3 argues **against** one on principle: *"a model acting as
judge would introduce non-determinism, and with it a requirement for its own bias
controls, into a question that arithmetic already answers."*

⚠ **Chapter 2 currently promises the method Chapter 7 rejects.** Same defect as
Chapter 3's four judge threads, and the two chapters must land together — if Ch3
is fixed and Ch2 is not, the literature review still advertises it.

⚠ **Keep the surrounding citation.** The paragraph's source (on checking
generated statements against a retrieved reference) is sound and still supports
the narrower claim. Only the *method* sentence changes.

---

# Part 2 — four verifications you can now answer

**These threads ask "is this actually implemented?" Each is now answerable from a
measured result.** None needs prose; each needs a verdict in Word.

## Thread 86 — is uncertainty communication passed along in the scenarios?

✅ **Yes, and it is measured.** Chapter 7 §7.3 scores four criteria against the
tool payload, one of which is whether a range is stated and whether its bounds
match the payload within five per cent. Chapter 8 reports the result per
scenario. `interval_communication.csv` is the artefact.

⚠ **The honest qualifier**: what is measured is whether uncertainty was
*communicated*, not whether it *improved a decision*. Ch7 §7.3 and Ch9 §9.4 both
state that boundary explicitly. **Resolve as VERIFIED-OK with that caveat.**

## Thread 87 — is the "interpretive step" argument reflected in the experiments?

✅ **Yes.** The fourth scoring criterion is whether a course of action is proposed
rather than a number alone — which is precisely Goodwin's interpretive step,
operationalised. Chapter 7 §7.3 records that the shared question was amended to
ask for a recommendation so the criterion would be scoreable, and that answers
recorded before the amendment are not pooled with those after.

**That is the strongest possible answer to this thread**: the argument is not
only reflected, it changed the instrument. **VERIFIED-OK.**

## Thread 89 — is structured tool invocation implemented (ART)?

✅ **Yes.** `forecast_tool.py` is a typed, schema-constrained call; the agent
translates intent into parameters and a payload into prose, and never handles a
feature vector. Recorded spans carry `args_match_request`. **VERIFIED-OK.**

## Thread 91 — how are figures "checked against the source forecast"?

✅ **Implemented and measured.** The harness extracts the stated number from the
answer and compares it against the tool's returned value. Chapter 9 §9.1.2
reports the outcome: every reported figure matched the figure the tool returned
across the whole evaluation.

⚠ **One precision worth having at the viva**: the check runs **after** the answer
is produced, as an evaluation instrument — not as a pre-delivery gate inside a
deployed system. Chapter 2's sentence says *"before delivery"*, which overstates
it slightly.

**Recommended one-word fix:** change *"are checked against the source forecast
before delivery"* → *"are checked against the source forecast"*. **NEEDS-BRIAN.**

---

# Part 3 — the remaining threads

## Thread 85 — "Could use a source" for the descriptive-BI claim

**Anchor:** §2.3 opening, *"Business intelligence systems have historically
occupied the descriptive tier of the analytics spectrum..."*

⚠ **I am not proposing a citation, because I cannot verify one exists in the
library that says this.** The claim is a broad characterisation of BI practice,
and the honest options are:

1. **Reword to stand on what follows it.** The paragraph's *next* sentences cite
   Pathirannehelage et al. (2025) and are evidenced. Making the opening a
   framing sentence rather than an assertion removes the debt: *"Business
   intelligence systems have conventionally served the descriptive tier..."*
   still reads as orientation rather than as a claim needing support.
2. **Find a source** — a real search, not a guess.

**Recommendation: option 1**, given the date. **NEEDS-BRIAN.**

## Threads 76, 79 — arguments for exogenous features

✅ **VERIFIED-OK, both.** These argue the thesis should enrich with a holiday
API. **It did** — `n_holidays`, `days_in_month`, `non_holiday_days`, joined from
Nager.Date and ablation-tested. Your thread 76 even names the API you used.

**No prose change.** §2.1's sentences about exogenous features in M5 are accurate
and now consistent with what the thesis delivers.

## Thread 97 — why not cite Saunders alongside Hevner and Peffers?

✅ **Saunders et al. (2023) is in the library** (`book`, March 2023, verified
against the API) and is already cited in Ch2's own opening and in Ch4.

**Recommendation:** add it to §2.8 where the chapter describes DSR's fit to the
research design — Saunders covers research-strategy selection, which is the claim
being made there. One citation, no rewording:

**Anchor:** *"Such questions are the province of Design Science Research (DSR),
the information-systems paradigm concerned with building and evaluating novel
artefacts..."*

⚠ **Do not cite Saunders for the DSR framework itself** — that is Hevner and
Peffers, correctly cited. Saunders supports the *choice* of a design-oriented
strategy, not the paradigm's content. **NEEDS-BRIAN** on whether it is worth the
sentence.

---

# Comment ledger — all 15 threads

| Thread | Verdict |
|---|---|
| 71, 72, 73, 74 | ✅ already RESOLVED |
| 76, 79, exogenous features | ✅ **VERIFIED-OK** — implemented |
| 81, 82, 83, hosting claims | ✅ already RESOLVED |
| 85, descriptive-BI source | **NEEDS-BRIAN** — recommend rewording |
| 86, uncertainty communication | ✅ **VERIFIED-OK** — measured |
| 87, interpretive step | ✅ **VERIFIED-OK** — it changed the instrument |
| 89, structured invocation | ✅ **VERIFIED-OK** — implemented |
| 91, checking against source | ✅ **VERIFIED-OK** ⚠ one-word precision fix offered |
| 92, judge model | **ADDRESSED** — Fix 2 |
| 95, "designed; pending" labels | **ADDRESSED** — Fix 1 |
| 97, Saunders in 2.8 | **NEEDS-BRIAN** — recommended |

**15 of 15 accounted for. 2 addressed in prose, 6 verified already done, 4
already resolved, 3 need your decision.**

---

# Citations

| Source | Status |
|---|---|
| Saunders et al. (2023) | ✅ in library, `book`, verified against the API 2026-09-14 |

**No new sources required.** Fix 1 and Fix 2 remove claims; they add none.
