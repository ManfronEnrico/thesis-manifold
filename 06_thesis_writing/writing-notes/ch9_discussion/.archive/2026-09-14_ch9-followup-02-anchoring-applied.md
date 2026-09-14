---
name: 2026-09-14_BRANCH_A_ch9-followup-02-anchoring
description: FOLLOW-UP - The anchoring test, run on the 18 recoverable funded runs. The data arms do not anchor on the last observed value. Includes two corrections to the consolidated note this follows, one of them a retracted claim about the funded data.
category: workflow
applies-to: [ch9_discussion]
triggers: [ch9 prose pass, anchoring, judgmental forecasting, defence preparation]
created: 2026_09_14-12_20
updated: 2026_09_14-12_20
snapshot: 2026-09-14_11-55_ch9-followup-defence-and-anchoring
status: prose ready to paste, awaiting human review
---

# Chapter 9 — follow-up 02, the anchoring test

Verified at `41ecb76`, fetch clean, origin and HEAD level. Snapshot
`2026-09-14_11-55_ch9-followup-defence-and-anchoring` (47,296 words, 121
comments, 99 threads). Zotero re-pulled the same minute: **89 items**.

**This follow-up supersedes nothing in the consolidated note except Part 2's
anchoring proposal.** Everything else in
`2026-09-14_BRANCH_A_ch9-consolidated-defence-and-limitations-citations.md`
stands: Fixes 1 through 4 are applied and verified in this snapshot.

| In the consolidated note | Status |
|---|---|
| Fixes 1–4 | ✅ **applied**, verified against this snapshot |
| Part 2, the anchoring test | **replaced by F1 below** — the proposal was structurally wrong |
| Part 2, judgmental-adjustment frame | still **NEEDS-BRIAN**, unchanged |

---

# Two corrections, both mine

## Correction 1 — the anchoring test could never have run as I proposed it

The consolidated note proposed testing whether **`A_llm_plain` anchors on the
last observed value**. That is not testable, and the reason is structural:
**Scenario A is the no-data arm.** It is shown no series at all, so there is no
last observed value for it to anchor on.

I proposed a measurement against an input the design deliberately withholds.
The test below therefore measures the **data arms**, which are the only runs
where the hypothesis is meaningful.

## Correction 2 — a retracted claim about the funded data

⚠ **Mid-investigation I told Brian that every per-brand APE for two CSD brands
was suspect. That was wrong, and it is retracted here in full.**

What happened: I joined `runs.csv` against
`05_thesis_results/08_experimental_evaluation/scenario_inputs/`, which is a
**stale export**. It was written 2026-09-10 against the pre-F58 brand selection
(HARBOE / NIKOLINE / VOELKEL). The funded runs are from 2026-09-12 against the
post-floor selection (HARBOE / 7-UP / ØRBÆK), because F58 raised the volume
floor to 1,000 units — VOELKEL at nine units a month made APE measure integer
rounding rather than forecasting skill.

So I compared two different brand sets and got ratios up to 9,230x.

**The funded data is sound.** `runs.csv` and `raw_responses/` agree to the
decimal — ØRBÆK's actual is 2850.1309 in both. No number in Chapter 8 or
Chapter 9 is affected.

### The one real finding from that detour

`scenario_inputs/` **is stale on disk** and its README claims it "cannot drift"
from what the scenarios run on. That claim is now false: it names brands the
funded experiment did not use.

**It is not cited by any chapter**, so nothing in the thesis is wrong. But it is
a trap for the next person who reaches for it, and it will be in the submission
repository.

→ **Recommend: re-export it, or delete it.** Two minutes either way.
**NEEDS-BRIAN.** Recorded as S33 below.

---

# The test, and what it found

## Method

For each funded run, the history the agent was actually shown is embedded in its
own logged prompt, so the denominator comes from the same artefact as the
forecast and cannot drift. **18 of 63 runs carry a recoverable series**: the nine
`B_llm_data` runs and the nine `F_llm_data_model` runs. The other arms either
receive no history (A) or run through the production orchestrator, which logs the
payload differently (D, E, G).

Two reference points per run: the **last observed month**, which is what the
anchoring heuristic predicts, and the **trailing twelve-month mean**, which is
what a seasonally-aware average would produce.

## Result

| | ratio to last observed | ratio to trailing 12-month mean |
|---|---|---|
| median | **0.860** | **0.991** |
| interquartile range | 0.788 – 1.188 | 0.921 – 1.051 |
| standard deviation | 0.243 | 0.133 |
| runs within 5% of it | **0 of 18** | 7 of 18 |
| runs within 10% of it | — | 11 of 18 |

**Not one run of eighteen landed within five per cent of the last observed
value.** The anchoring heuristic the book warns about is absent here.

## ⚠ The honest reading, which is narrower than the pooled table

The pooled 0.991 makes it look as though the agents land on the trailing mean.
**Per brand they do not, and the pooled figure is three behaviours averaging into
one:**

| Brand | median ratio to trailing mean | reading |
|---|---|---|
| HARBOE | **1.082** | forecasts *above* its trailing mean |
| ØRBÆK | **0.991** | sits on its trailing mean |
| 7-UP | **0.825** | forecasts well *below* its trailing mean |

Only ØRBÆK is actually centred on its trailing mean. **Do not write "the agents
forecast the trailing mean".** The defensible claim is the negative one plus a
weak positive:

- **Strong, and the one to make:** they do not anchor on the last value.
- **Weak, and must be hedged:** their forecasts sit far closer to a trailing
  average than to the last observation, with the dispersion roughly halved.

**And 7-UP's 0.825 is the interesting cell**, because 7-UP is the brand where
both data arms over-forecast badly against the actual of 13,042. They pulled
*down* from both reference points and still landed high, which says the series
itself fell sharply and they under-adjusted. That is a different failure from
anchoring and it is worth not obscuring.

---

# The fix

## F1 — 9.1.4, a mechanism for the increment rather than only a size

### Anchor

**Section 9.1.4 SRQ4.** The paragraph beginning *"The comparison is nonetheless
conditional on forecasting practice on both sides"*.

It ends: *"...That is a limitation of this comparison and a concrete, cheap
direction for the next cycle."*

### Action

INSERT AFTER — one new paragraph, between that paragraph and the one beginning
*"A second qualification bears on what is being compared."*

#### Replace with

> What the code-writing scenarios did with the history can be characterised more
> precisely than by their error alone. A recurring concern about judgmental
> forecasting is that a forecaster handed a series will take its final
> observation as a reference point and adjust insufficiently from it, producing
> what is effectively a naive forecast in narrative form (Hyndman &
> Athanasopoulos, 2021). That behaviour is measurable here, because the history
> each scenario received is recorded alongside the answer it gave. Across the
> eighteen runs for which the series is recoverable, not one forecast fell within
> five per cent of the brand's last observed month, and the forecasts sat
> substantially closer to a trailing twelve-month average than to the final
> observation, with roughly half the dispersion around it. The scenarios were
> therefore performing some form of seasonal averaging rather than adjusting from
> the most recent value, which is the more defensible of the two behaviours and
> is consistent with the explicit model-fitting visible in their working.

### Note — why this earns its paragraph

It converts a **size** into a **mechanism**. Section 9.1.4 currently reports that
the code-writing scenarios win on the median and says the reason is plausibly the
techniques the substrate lacks. This adds a measured statement about what they
were actually doing with the data — and it is the same answer, arrived at
independently: they fitted models and averaged, rather than reading off the last
number.

It also **closes an examiner's cheapest attack** on the whole SRQ4 result. *"Your
language model just repeated the last month and got lucky"* is the obvious
challenge to a strong LLM baseline, and it is now answered with a measurement
rather than an assertion.

### Note — what the prose deliberately does not claim

- **No ratio figures.** "Closer to a trailing average, with roughly half the
  dispersion" is what the per-brand split supports. Printing 0.991 would assert a
  centring that only one of three brands shows.
- **No claim about the plain arm.** It has no history, so it is outside this
  measurement entirely. ⚠ **Do not let this paragraph drift into explaining
  `A_llm_plain`'s 502 per cent error** — that arm's failure is a different
  phenomenon and Section 9.1.4 already accounts for it.
- **No claim about the model-backed arms' superiority.** `F_llm_data_model`
  behaves almost identically to `B_llm_data` on this measure, which is its own
  small finding and not one the chapter needs.

---

# The provenance question this raises

⚠ **These figures have no committed artefact**, which is the same defect the Ch10
note flagged for the calibration schemes.

They are computed from `raw_responses/*.json`, which is **gitignored** (65 MB,
and it embeds Nielsen data under the confidentiality terms). So a reader cannot
reproduce them, and neither can a future session without the local files.

**Two honest options:**

1. **Write a small producer** into
   `05_thesis_results/08_experimental_evaluation/tables/` that recomputes the
   ratio table from the raw responses and emits it. The Correctness-tier rule
   then holds, and the number in the prose is regenerable. Perhaps thirty lines.
2. **Keep the claim qualitative**, exactly as F1's prose already does. It states
   *"not one within five per cent"* and *"closer to a trailing average"* — a
   count and a direction, both of which survive a re-run and neither of which is
   a decimal that can go stale.

**F1 as written is safe under option 2**, which is why it carries no ratios.
Option 1 is better if there is time, and it is not required for the paragraph to
ship. **NEEDS-BRIAN.**

---

# For the deferred structural list

## S33 - `scenario_inputs/` is a stale export whose README claims it cannot drift

**Status:** `recommended` - re-export or delete
**Found:** 2026-09-14, anchoring test

`05_thesis_results/08_experimental_evaluation/scenario_inputs/` was written
2026-09-10 and names CSD brands **NIKOLINE** and **VOELKEL**. The funded runs
(2026-09-12) used **7-UP** and **ØRBÆK**, following F58's 1,000-unit volume
floor. `index.csv` therefore records held-out actuals of 457.1 and 9.0 for brands
no funded run scored.

Its README states the files *"cannot drift from what the scenarios actually run
on"*, because they are written by the harness's own `_brand_history()`. That was
true when written and is false now — the export simply was not re-run after the
brand selection changed.

**No chapter cites it**, so nothing in the thesis is wrong. The risk is a reader
of the submission repository joining against it, as I did.

**Recommendation:** re-run `export_scenario_inputs.py`, which takes seconds and
makes the README true again. If the folder is not needed for submission, delete
it instead — it is the only copy of the pre-F58 selection and nothing depends on
it.

---

# Citations register row

| | |
|---|---|
| Source | Hyndman & Athanasopoulos (2021), *Forecasting: Principles and Practice*, 3rd ed. |
| Zotero key | `5NFQRRXS` |
| Status | **IN-ZOTERO** ✓ — verified against the 2026-09-14 pull, 89 items |
| Lands in | Chapter 9, Section 9.1.4 |
| Supports | "...a forecaster handed a series will take its final observation as a reference point and adjust insufficiently from it" |

**NLM-CONFIRMED not required.** The supported sentence restates §6.1's own claim,
that it is common to *"take the last observed value as a reference point... may
lead to conservatism and undervaluing new information"*. The quotation is
recorded in the archived P0055 scan note.

⚠ **This is a citation used to frame a concern the thesis then measures and
finds absent.** That is a legitimate use and it should read that way in the
prose — the source supplies the hypothesis, the runs supply the answer. F1's
wording does this deliberately: *"A recurring concern... That behaviour is
measurable here."*
