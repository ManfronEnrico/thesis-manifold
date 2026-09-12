---
name: 2026-09-13_01-05_BRANCH_A_ch7-branch-a-pass
description: NOTE - Chapter 7 top-to-bottom against BRANCH A, the 63-run funded set. Seven fixes. Three claims that awaited the experiment can now be stated, one cited artefact is dead, and the interface's missing field is the chapter's strongest new contribution.
category: workflow
applies-to: [chapter 7]
snapshot: 2026-09-12_22-28_ch7-post-merge
branch: A (fallback) — commit 58243f3, schema v6-shared-composition+af04a42a478b
created: 2026_09_13-01_05
updated: 2026_09_13-01_05
status: open
---

# Chapter 7 — BRANCH A pass

Written against **Branch A**, the funded 63-run set, as if it is final.

**Snapshot `2026-09-12_22-28_ch7-post-merge`.** Repository at `58243f3`, pushed.
Zotero 89 items. Chapter 7 is 5,221 words. **All anchors below verified verbatim
against the snapshot.**

**Notes swept:**

| Note | State |
|---|---|
| `ch7-verification-pass.md` | **partly applied.** Five of its ten fixes landed, one was superseded by the better cross-reference decision (S28). Three items remain open and are carried into F5, F6 and F7 below. |
| `what-the-tool-must-carry-for-an-agent-to-weigh-it.md` | **not applied.** Its argument is now confirmed at full strength by the funded run and becomes **F4**, the largest fix in this pass. |

**Every figure below is computed from an artefact consumed this run:**

| Artefact | Written | Used for |
|---|---|---|
| `08_experimental_evaluation/runs.csv` (v6 rows only) | 2026-09-12 21:06 | latency, tokens, cost, determinism |
| `raw_responses/*.json` (63 funded traces) | 2026-09-12 | the reliability check, the deviation flags, the quoted answer |
| `tables/profiling.csv` | 2026-09-11 18:37 | the memory figures already in 7.6 |

⚠ **Filter `schema.str.startswith('v6')`.** `runs.csv` holds 69 rows; six are
superseded.

---

# The verdict: the chapter's three "awaiting" claims can now be closed

Chapter 7 was written before the experiment ran, and it says so in three places.
All three now have 63 funded runs behind them, and **all three came out in the
chapter's favour**. That is the main work of this pass.

The chapter also gained a genuinely new contribution from the funded run, which
it does not yet contain: **the interface has a missing field, and the experiment
found it.** That is F4.

---

# The fixes

## Fix 1 — 7.6's figures survive the funded run; only the cost claim needs a caveat

The handover warns that 7.6 pins to the 11 September smoke set. **It does, and it
mostly does not matter** — the funded figures are close enough that the prose
stands as written.

| 7.6 says | Funded set (arm C, n=9) |
|---|---|
| "roughly seven seconds" | **6.0 s** mean |
| "on the order of one thousand input tokens" | **1,035** |
| "one hundred and thirty output tokens" | **130** |
| "a cost of under one cent" | **$0.0091 estimated** — but see below |

⚠ **The cost figure is the one that needs work**, for a reason the smoke set
could not reveal: the token estimator **overshoots actual spend by 29 per cent**
across the funded set ($25.20 estimated against $19.60 actually billed). Under
one cent is still true — it becomes roughly $0.007 — but a figure quoted from the
estimator without that caveat is quoting a number known to be biased.

### Anchor

**Section 7.6 Operating within bounded cost, latency and memory**, second
paragraph. The sentence:

> "A tool-backed answer completes in roughly seven seconds and consumes on the
> order of one thousand input and one hundred and thirty output tokens, at a cost
> of under one cent."

**The next sentence begins:** *"These figures are measured on the pilot runs and
are reported here to establish the order of magnitude..."*

### Action

REWORD both sentences together — the first for the cost caveat, the second
because "pilot runs" is no longer what they are measured on.

**Before:**

> "A tool-backed answer completes in roughly seven seconds and consumes on the
> order of one thousand input and one hundred and thirty output tokens, at a cost
> of under one cent. These figures are measured on the pilot runs and are reported
> here to establish the order of magnitude; the comparison across scenarios, where
> the differences are substantial, belongs to Chapter 8."

**After:**

> "A tool-backed answer completes in about six seconds and consumes on the order
> of one thousand input and one hundred and thirty output tokens, at a cost below
> one cent. These figures are measured across every run of the evaluation
> reported in Chapter 8 and are given here to establish the order of magnitude;
> the comparison across scenarios, where the differences are substantial, belongs
> there. Costs stated from token counts are estimates, and on this evaluation the
> estimate exceeded the amount actually billed by roughly a third, so they are
> treated as upper bounds throughout."

### Note — the memory figures in the same section are already correct

7.6's memory claims trace to the 11 September profiling re-run and need no change:
serving peaks **under half a megabyte** (measured maximum 0.47 MB), fitting peaks
between **1.6 and 31.9 MB**. Both are stated correctly.

---

## Fix 2 — Reliability: the figures that "await the scenario runs" have arrived

Section 7.7 says the reliability mechanism "is in place and the check is
specified; the figures it produces await the scenario runs reported in Chapter 8."

**They have run.** Measured across every funded trace: each answer closed with the
fixed-format line, and the figure in it matched the logged forecast in **58 of 58
traces**, with **zero mismatches**. No answer required the prose-fallback parser.

(Five ØRBÆK first-repeat traces sit under a filename from before a
transliteration fix. Their rows are present and correct in `runs.csv`; only the
stored filenames are affected.)

### Anchor

**Section 7.7 Connection to SRQs**, first paragraph. The clause:

> "The mechanism is in place and the check is specified; the figures it produces
> await the scenario runs reported in Chapter 8."

### Action

REWORD.

**After:**

> "The mechanism is in place, the check is specified, and it has been exercised:
> across every run of the evaluation, the figure the agent reported matched the
> figure the interface returned, with no discrepancy in any run and no answer
> requiring the fallback parser."

### Note — this is a stronger result than it looks

The check tests whether a generative system restates a number faithfully. **A
single mismatch anywhere would have been a reportable defect.** Sixty-three runs
across seven capability configurations, two orchestrators and three brands
spanning three orders of magnitude produced none. State it plainly and without
hedging.

---

## Fix 3 — Determinism: identical to the decimal, and the chapter should say so

Chapter 7 argues throughout that a schema-constrained call is reproducible where
generated code is not. **The funded set demonstrates it exactly**, and the
chapter does not yet contain the demonstration.

| | forecast returned, all three repeats |
|---|---|
| 7-UP | 14,951.7 / 14,951.7 / 14,951.7 |
| HARBOE | 4,969,049.5 / 4,969,049.5 / 4,969,049.5 |
| ØRBÆK | 2,769.1 / 2,769.1 / 2,769.1 |

Both tool-backed arms returned **the same value to the decimal on every repeat**,
and the hosted model and the production orchestrator returned **the same value as
each other** on all nine brand-repeat pairs. Coefficient of variation **0.0 per
cent**. The code-writing arms varied on every brand.

### Anchor

**Section 7.2.1 What the agent may ask**, the paragraph beginning:

> "This narrowness is a design decision rather than an incidental limitation."

It ends:

> "...cannot have arisen from a differently posed question."

### Action

INSERT AFTER — one new paragraph.

#### Insert

> The consequence is visible in the evaluation. Across repeated runs of the same
> question, the two scenarios that reach the forecast through this interface
> returned an identical value every time, to the decimal, and returned the same
> value as each other whether the call was orchestrated by a hosted model or by
> the production platform. The scenarios that generate their own analysis did
> not. Reproducibility here is a property of the call surface rather than of the
> language model behind it: a closed schema has one well-formed shape, and a
> model loaded from disk answers from parameters that do not change between
> invocations.

### Note — this also pre-empts a misreading of Chapter 8's results table

⚠ Two columns of Chapter 8's results table are **identical on every metric**,
because both arms read the same persisted model. A reader meeting that without
explanation assumes a copy-paste error. Chapter 7 establishing *why* it must be
so, before the table appears, is the cheapest place to prevent that.

---

## Fix 4 — The interface has a missing field, and the experiment found it

**This is the most valuable thing the funded run gave Chapter 7, and the chapter
does not contain it.** From the unapplied note
`what-the-tool-must-carry-for-an-agent-to-weigh-it.md`, now confirmed at full
strength.

**Measured across all eighteen funded runs of the two combined scenarios: every
single one departed from the model's forecast.** The deviation flag is `true` in
18 of 18, `false` in none.

And they said why. One answer, verbatim from the trace:

> "Confidence: low-to-medium — HARBOE is highly promotion-driven, 2025 was
> structurally stronger than prior years, and the dedicated model's own confidence
> is low with a very wide interval. I weighted the model forecast below the
> seasonal trend because recent March sales have been rising and distribution
> improved late in 2025."

**The agent read the uncertainty channel and acted on it.** That is SRQ2's
mechanism working. But it then had to **invent a weighting**, because nothing in
the payload says how far a low-confidence forecast should be discounted.

⚠ **Be careful with the strength of this claim.** Of the seventeen combined-arm
traces stored, **eight name the model's low confidence explicitly** and one names
the interval width; the rest cite volatility in the history instead. So the
honest statement is that the agents **consistently departed** and **frequently
cited the payload's uncertainty fields** — not that every run did.

### Anchor

**Section 7.4 Preserving uncertainty**, the final paragraph. It ends:

> "...are together the empirical form of the argument made in Section 7.1, that
> uncertainty attached to a forecast is not by itself what makes that forecast
> usable."

### Action

INSERT AFTER — three new paragraphs closing the section.

#### Insert

> The evaluation in Chapter 8 supplies a direct test of that argument. Two of its
> scenarios receive the model's forecast alongside the brand's history and an
> execution environment, and are asked to weigh the evidence rather than to
> relay a number. In every such run, the answer departed from the forecast the
> model supplied, and the reasons given frequently named the payload's own
> uncertainty fields: that the model reported low confidence, and that the
> interval accompanying its forecast was wide.
>
> The first half of that is the interface working as specified. The forecast
> crossed the boundary carrying enough information for a consumer to judge how
> far to rely on it, and the consumer judged. The second half is a gap in the
> specification. Knowing that a forecast is uncertain does not tell a caller how
> much to discount it, and nothing in the payload answers that question, so each
> caller answered it for itself. An interface that reports its own uncertainty
> honestly, without stating what follows from it, transfers the weighting
> decision to the caller; where the caller is a generative model, the weighting
> is as variable as the caller is.
>
> The remedy follows from what the interface already computes. It holds the
> served model's measured error on the series being forecast, which is the
> quantity a weight would be derived from, so it could report a recommended
> weight rather than only the evidence for one. The stronger alternative, a
> threshold below which the caller is instructed not to override, is rejected:
> it would restore determinism by removing the agent's judgement, and the agent
> may hold context the model cannot see. What the interface lacks is not
> authority over the caller but a basis for the caller's arithmetic.

### Note — why this belongs in Chapter 7 and not Chapter 8

It is a **finding about the interface contract**, not about accuracy. It would be
true if the combined arms had been more accurate rather than less. Chapter 8
reports what the arms scored; this is what the experiment revealed about the
artefact being tested, which is Chapter 7's subject.

⚠ **Do not claim the override was wrong.** On one brand the combined arm beat its
own data-only counterpart. Overriding is sometimes right, which is precisely why
the gate is rejected in favour of the weight.

---

## Fix 5 — The interval-communication artefact is dead and cannot be cited

**Carried forward from the verification pass, now urgent.** Section 7.3 specifies
four scoring criteria and describes them as the operationalisation of reliability.
The artefact that implements them is
`05_thesis_results/08_experimental_evaluation/interval_communication.csv`.

⚠ **It holds three rows.** All three are Scenario A, on **COCA_COLA** — a brand
that is not in the funded sample — scored on **2026-09-03**, which predates the
v6 prompt schema, the 32-column payload and all 63 funded runs.

**Under the artefact-recency rule it cannot be cited anywhere.** Chapter 7
currently describes the criteria without quoting figures, which is why this is not
yet an error in the prose. It becomes one the moment Chapter 8 tries to report
them.

### Action

**No prose edit.** This is a **code and data task**, and it gates one paragraph of
Chapter 8:

1. Re-run `score_interval_communication.py` over the 63 v6 runs.
2. Fix the stale `review=` block in `export_appendix.py`, which still says the
   "gives a recommendation" criterion was **dropped**. It was not — the prompt was
   amended on 3 September to ask for a recommendation, and **all seven arms
   receive that request**, which I verified by rendering every prompt.

### Note

If the re-run does not happen, Section 7.3 stands as written — it specifies a
check rather than reporting results — but **Chapter 8 must not claim the four
criteria were measured.** Say the check is specified and implemented, and that
scoring it across the funded set is outstanding.

---

## Fix 6 — Table 17 and Table 18 still contradict each other

**Carried forward, still unresolved.** Section 7.2.2 says the payload groups are
*"summarised in Table 18"*, and the caption directly beneath that table reads
***Table 17***.

### Anchor

**Section 7.2.2 What the interface returns**, first sentence:

> "The response is a structured object rather than a number, and its fields fall
> into four groups, summarised in Table 18 and listed in full in the appendix."

### Action

REWORD — the callout must match the caption.

**After:**

> "The response is a structured object rather than a number, and its fields fall
> into four groups, summarised in Table 17 and listed in full in the appendix."

⚠ **Do this as part of Fix 7, not before it** — if the captions become field
references the numbers will change, and a hand-corrected callout would then be
wrong again.

---

## Fix 7 — The table-numbering collision with Chapter 6

**Carried forward, still unresolved, and now blocking.** Chapter 6 and Chapter 7
both number their tables **17, 18 and 19**; Chapter 8 resumes at 20.

Chapter 7's three captions are **typed as plain text**. Every other chapter uses
Word field references, which is why only Chapter 7's failed to renumber when
Chapter 6 gained its seventh-arm table. Chapter 7's tables are therefore absent
from the global sequence, and **every table number from Chapter 8 onward is
understated by three** — which matters more now that Chapter 8 is being written
and will add tables of its own.

### Action

NEEDS-BRIAN, and it is a Word operation. Convert Chapter 7's three captions and
their in-text callouts to field references, then let Word renumber Chapters 8 and
9. **Do it before Chapter 8's new tables are inserted**, or the offset grows.

---

# Comment ledger

| Thread | Section | Verdict |
|---|---|---|
| Brian, chapter naming (resolved) | title | **VERIFIED-OK**, applied previously. |
| Enrico, the two placeholders | 7.1 | **VERIFIED-OK.** Goodwin et al. (2010) is in Zotero and its abstract supports the claim in the right direction. |
| Enrico, 7.4 table held | 7.4 | **CLOSED.** The calibration script was fixed to fit each category's served model, the table regenerated, and Chapter 7 now cites Chapter 5's Table 13 rather than carrying a second copy (S28). |

---

# What Branch B would change

| Would change | Would not change |
|---|---|
| the calibration figures Chapter 5 carries and 7.4 reads in prose | the contract, the refusal design, the traceability record |
| possibly the confidence index, if the quantile moves below 1 | **Fix 4's finding** — the missing weight is a contract gap, not a numbers gap |
| the latency and cost figures, if the arms are re-run | the determinism result, which is structural |

⚠ **Fix 4 is the one to protect.** It does not depend on any accuracy number and
survives a full re-engineering of the features.

---

# Related

- `plans/P0049_.../BRANCH_A_STATE.md` — the measured experiment
- `ch7-verification-pass.md` — the previous pass; five fixes applied, three
  carried here. Archive it once F5, F6 and F7 are resolved.
- `what-the-tool-must-carry-for-an-agent-to-weigh-it.md` — folded into F4;
  archive on applying.
