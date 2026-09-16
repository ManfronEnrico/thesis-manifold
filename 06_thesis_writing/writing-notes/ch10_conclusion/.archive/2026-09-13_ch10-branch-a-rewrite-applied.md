---
name: 2026-09-13_18-40_BRANCH_A_ch10-branch-a-rewrite
description: NOTE - Chapter 10 rewritten against BRANCH A. Every SRQ answer in 10.1 is wrong: XGBoost everywhere, a chain grain deleted in August, a judge study that does not exist, and an SRQ4 answer saying the central comparison was never run. Full replacement prose with all 8 comment threads resolved.
category: workflow
applies-to: [ch10_limitations]
triggers: [chapter 10, conclusion, branch a, rewrite]
created: 2026_09_13-18_40
updated: 2026_09_13-20_45
snapshot: 2026-09-13_20-40_branch-a-archive-check
status: prose ready to paste, awaiting human review
---

# Chapter 10 — BRANCH A rewrite

Verified at `c9c0587`, fetch clean. Snapshot
`2026-09-13_18-18_branch-a-full-review`. Zotero: **89 items**, re-pulled this
session.

**Notes swept:** one live note in this folder —
`interval-width-a-tested-negative-result.md`, **not applied**. Its argument and
its evidence are now folded into this note: the one-sentence form in Fix 4, and
the full tested-alternatives table in **Fix 8**, added 2026-09-13 20:45. The
source note is archived, so this file is the single place the interval
limitation is staged.

**Read alongside** `ch9_discussion/2026-09-13_18-40_BRANCH_A_ch9-branch-a-rewrite.md`.
The two chapters restate the same four answers at different lengths, and if only
one is corrected the document contradicts itself in a way an examiner reading
back-to-back will catch.

---

# Why this is a rewrite

Same diagnosis as Chapter 9, and the same date: last edited 5 September, before
the funded run. Chapter 10 is 886 words and **all four SRQ answers in 10.1 are
false as written.**

| Claim | Status |
|---|---|
| "Tuned XGBoost is the best lightweight model in every category" | Two of four serve **LightGBM** |
| "test WMAPE 11.4–31.0%" | No artefact holds these. Measured: 18.4 / 23.4 / 17.4 / 30.8 |
| "brand×chain for danskvand" | The chain grain was **deleted** (P0035, DEC-GRAIN) |
| "empirical coverage 80–98%" | Measured **73.6 to 91.7** |
| "an independent GPT-4o judge ... four of five dimensions (mean 3.81 vs 3.15)" | **No such study.** No judge in this design |
| "the code-as-action LLM comparator ... is the main open empirical item" | **63 funded runs.** It is the chapter's strongest result |
| "≤8 GB constraint" | The thesis constraint is **four** gigabytes |
| "(five Nielsen categories)" | **Four.** Beer was excluded, per Ch1 and Ch4 |
| "pilot scale (on the order of fifty prompts)" | 63 runs, 7 scenarios, 3 brands, 3 repeats |

A conclusion that answers the research question with the wrong model, the wrong
numbers, a deleted grain and a study that does not exist is the single most
damaging page in the thesis, because it is the page an examiner reads most
carefully.

---

# The fixes

## Fix 1 — 10.1, the four SRQ answers

### Anchor

**Section 10.1 Summary of contributions.** Opens *"This thesis asked: How can
production-oriented agentic decision-support systems without native predictive
capabilities be extended..."* and runs through the four bolded **SRQ1**–**SRQ4**
paragraphs to *"...the code-as-action comparison and a production integration
remain for a second cycle."*

### Action

REPLACE the entire section, opening paragraph and all four SRQ paragraphs.

#### Replace with

> This thesis asked how a production-oriented agentic decision-support system
> without native predictive capability can be extended with lightweight
> forecasting models to support reliable, forecast-informed and cost-justified
> decision-making under computational and deployment constraints. The answer it
> substantiates is that such an extension is feasible within an SME-grade
> resource budget and that the dedicated-model layer earns its place, though
> not on the axis the question invites. It earns it on reproducibility, cost
> and auditability rather than on accuracy, and the evaluation that establishes
> this also shows how strong the alternative is.
>
> **SRQ1, models and efficiency.** Two gradient-boosted families dominate the
> classical and linear baselines across all four categories, but the choice
> between them is not supported by the data: a five-seed sweep changes the
> selected model in every category, and the difference between the families is
> smaller than the variation each produces on its own. The defensible claim is
> that they are statistically indistinguishable here, which frees the choice to
> be made operationally. Two categories are nonetheless beaten outright by
> parameter-free benchmarks, seasonal naive on ready-to-drink beverages and
> Prophet on water, and that qualification is reported rather than absorbed.
> Category specialisation is conditional on panel size: pooling across
> categories wins on the two smallest by four to six percentage points and is
> indecisive on the larger two. The memory constraint proved non-binding at
> this data scale, with fitting peaking at thirty-two megabytes and serving
> below half of one, against a four-gigabyte ceiling.
>
> **SRQ2, the structured interface.** Forecasts are exposed with a point
> estimate, a split-conformal interval, the served model's measured
> out-of-sample error against the strongest classical baseline, and the
> provenance needed to reconstruct the call. Reliability holds and was checked:
> every reported figure matched the figure the tool returned across the whole
> evaluation. Traceability is implemented in full and evaluated in part.
> Uncertainty is where the answer is negative and the negative is informative:
> the interval attains its coverage guarantee and is too wide to act on for an
> individual brand, and the confidence index built on top of it discriminates
> nothing, because both of its terms derive from a quantile that is constant
> within a category. What makes a forecast usable here is therefore the
> measured track record travelling beside it rather than the interval, which is
> the chapter's substantive design finding.
>
> **SRQ3, integration readiness.** Assessed rather than deployed, but no longer
> argued from architecture alone: three of the seven evaluation scenarios were
> executed inside the production agentic platform, so the four readiness
> capabilities are derived from what an integration actually required. The
> remaining gap to a production deployment is operational rather than
> architectural.
>
> **SRQ4, dedicated models against code execution.** The comparison ran as a
> ladder of seven scenarios over sixty-three funded runs, and no scenario leads
> on every axis. Access to the firm's own data is worth far more than anything
> above it on the ladder, moving median error from 502 per cent to under three.
> Above that, the dedicated model does not win on accuracy: the code-writing
> scenarios are better on the median and worse on the mean, which is to say
> better most of the time and occasionally much worse. What the dedicated model
> delivers is a forecast that costs roughly a fiftieth as much, returns roughly
> twenty times faster, and is identical on every repeat to the decimal, on both
> orchestrators. Since no scenario dominates, the contribution is the shape of
> the disagreement rather than a winner.
>
> Taken together the thesis delivers a working design-science artefact and
> transferable design knowledge about extending non-predictive agentic systems
> with forecasting. It also delivers a result that qualifies its own premise:
> a language model given data and a sandbox is a stronger baseline than the
> literature usually grants it, and a dedicated forecasting layer must be
> justified on properties other than accuracy alone.

### Note — every figure's source

502 and 2.9 per cent, the cost and latency ratios, and the zero variation: the
63-run `runs.csv`, filtered to the v6 schema. The seed result: Ch5 Table 14.
Pooling: Ch5 Table 12. Memory: `profiling.csv`. Coverage and width: Ch5
Table 13. Nothing here is new to the document.

⚠ **The word "calibrated" has been removed from the opening paragraph.** The
original said the substrate is "exposed through a structured, calibrated
interface". The intervals are calibrated in the conformal sense and
uninformative in the practical one, and the conclusion should not use a word
the body of the thesis spends two sections qualifying.

---

## Fix 2 — 10.2, the design principles must match Chapter 9's

### Anchor

**Section 10.2 Theoretical contribution (design principles).** Five bolded
principles from *"**Sequential execution principle**"* to *"**Computational
transparency principle**"*, plus the *"Note: uncertainty calibration..."* line
and the *"Cite: DSR design-theory sources..."* line.

### Action

REPLACE all five principles and both trailing lines.

#### Replace with

> The design knowledge this thesis contributes is stated as five principles,
> each at the level of a problem class rather than of this artefact, and each
> supported by evidence in Chapter 9 that would have come out differently had
> the principle not held.
>
> **Delegation over generation.** Where a numerical answer must be reproducible,
> the language model should orchestrate and delegate prediction to a dedicated
> model rather than produce the number by its own means. The evidence is that
> the tool-backed scenarios returned an identical figure on every repeat while
> the code-writing scenarios returned a different one on almost every
> repetition.
>
> **Explicit refusal over silent fallback.** An interface whose consumer is a
> generative model must decline in stated terms where a conventional interface
> would substitute a default, because a fallback asserts that something was
> found and an agent cannot recognise it as anything else.
>
> **Carry the track record, not only the interval.** A forecast delivered to a
> non-expert consumer should travel with the producing model's measured
> out-of-sample error, because an interval alone was shown here to be too wide
> to act on and a confidence summary built from it discriminated nothing.
>
> **Budget memory at selection time and report it at run time.** A resource
> ceiling does its useful work by excluding architectures before any of them is
> fitted; reporting the realised footprint afterwards is what lets a reader see
> whether the ceiling bound the result.
>
> **Report cost and latency beside accuracy.** Cost per answer differed by a
> factor of roughly fifty between scenarios of comparable accuracy, a
> difference no accuracy-only evaluation would have surfaced and the one most
> likely to decide an SME deployment.
>
> These principles follow the design-science convention that an instantiation
> becomes a contribution only when the knowledge it embodies is stated
> separately from it (Hevner et al., 2004; Peffers et al., 2007).

### Note — what changed

- **"Sequential execution" is gone.** It was a principle about a constraint the
  thesis then measured as non-binding, so it claimed design knowledge from a
  problem that did not materialise. Chapter 9's DP1 is replaced the same way,
  and the two chapters must agree.
- **Cost-justification is gone as a separate principle**, because it restates
  the thesis question rather than answering it, and what replaces it is the
  measurement.
- **"uncertainty calibration is a design consideration deferred to future
  work"** is deleted. Calibration was implemented, measured, and three
  alternatives were tested. Calling it deferred discards the chapter's best
  negative result.
- The trailing *"Cite:"* line is folded into the final sentence. **Only Hevner
  and Peffers are cited**, because they are the only DSR sources in the Zotero
  library.

---

## Fix 3 — 10.3, practical recommendations

### Anchor

**Section 10.3 Practical recommendations for Manifold AI**, three bullets
beginning *"Integrate the lightweight forecasting substrate as a callable
tool"*, the last ending *"[cloud-pricing citation: resolve in global references
pass]"*.

### Action

REPLACE.

#### Replace with

> Three recommendations follow for the case organisation. The forecasting
> substrate should be integrated as a callable tool through the production
> platform's graph engine, which the evaluation has already exercised for three
> of its seven scenarios, so the integration path is demonstrated rather than
> proposed. The dedicated-model configuration should be preferred wherever an
> answer must be reproducible, auditable or served at high frequency, since at
> roughly a cent and six seconds per answer its cost does not constrain how
> often it may be asked. The code-writing configuration should be retained for
> exploratory analysis where a human reviews the working, since it produces a
> better typical answer and an occasional very poor one, which is tolerable
> under review and not tolerable unattended.
>
> On infrastructure, the measured end-to-end peak of approximately 231
> megabytes means the extension imposes no meaningful hardware requirement of
> its own. The operating cost is the language model, which is billed per token
> and runs elsewhere, and the execution sandbox, which is created per request
> and therefore costs nothing while idle.

### Note — the unresolved citation placeholder

*"[cloud-pricing citation: resolve in global references pass]"* is deleted
rather than resolved. The replacement makes no claim about instance pricing, so
no source is needed. ⚠ **The same placeholder pattern sits in Chapter 1**
(*"[CITATION TO ADD: cloud-instance pricing source]"*) and that one still needs
either a source in Zotero or a reworded claim — it is in the flow report.

---

## Fix 4 — 10.4, limitations recap

### Anchor

**Section 10.4 Limitations recap**, five bullets beginning *"Empirical context
bounded to the Danish beverage retail market (five Nielsen categories)"*.

### Action

REPLACE.

#### Replace with

> Five limitations bound these conclusions. The empirical context is the Danish
> beverage retail market across four Nielsen categories and a single partner
> organisation, and the scenario evaluation covers three brands within one of
> those categories. The thesis completes one design-science cycle, so the
> design principles are derived rather than validated across contexts. The
> comparison between dedicated models and code execution is conditional on the
> forecasting practice implemented on each side, and the substrate lacks two
> techniques the code-writing scenarios applied on every run. The prediction
> intervals attain their coverage guarantee and remain too wide to act on for
> an individual brand, a limit of the panel's shape rather than of the method.
> And the evaluation measures what each configuration communicated and how
> accurate it was, not whether a planner receiving that communication decided
> better.

### Note — three deletions

"Five Nielsen categories" is four. "Pilot scale (on the order of fifty
prompts)" is 63 runs on a fixed design. "Uncertainty calibration is designed
but not empirically validated" is the opposite of what happened.

---

## Fix 5 — 10.5, future research

### Anchor

**Section 10.5 Future research**, five bullets beginning *"Full-scale SRQ4
evaluation across the complete prompt set"*.

### Action

REPLACE.

#### Replace with

> Five directions follow. The substrate should be given the two techniques the
> code-writing scenarios used unprompted on every run, exponential smoothing as
> a benchmark family and a seasonal term in the classical baseline, since the
> comparison cannot be called settled while the dedicated side lacks
> established practice the alternative applies by default. The interface should
> carry a per-series rather than a per-category measure of error, because every
> combined run departed from the model's forecast and the payload supplied no
> quantity from which a brand-specific weight could be derived, so each run
> invented one. The evaluation should be widened across categories and repeats
> before any claim about comparative accuracy is made, the present design being
> sized only to detect differences larger than the within-scenario spread. The
> integration should be completed in production and studied before and after,
> which the executed scenarios make a smaller step than it was. And whether a
> communicated forecast improves a planner's decision remains the question the
> decision-support literature actually asks, requiring an experiment with human
> participants that is a separate study rather than an extension of this one.

### Note — what is preserved from the folded chapter note

`interval-width-a-tested-negative-result.md` argues the interval limitation
should be written as a contribution, because three alternative schemes were
implemented and measured. **That argument is honoured in Ch9 Fix 10 and in
10.4 above**, where the limitation is stated with the fact that alternatives
were tested. A conclusion restates and does not re-argue, so the evidence itself
belongs earlier in the document — **Fix 8 below places it in Chapter 5**, which
is where a reader meets the interval for the first time.

⚠ **The "code-as-action as the artefact's own action format" bullet is
dropped.** It rests on "the prototype's 0% numerical hallucination under JSON",
a figure from a superseded evaluation. The reliability result that replaces it
is in 10.1's SRQ2 paragraph.

---

## Fix 6 — 10.6, the final statement

### Anchor

**Section 10.6 Final statement**, three bullets beginning *"The thesis
demonstrates how a resource-constrained agentic decision-support system can be
extended"*.

### Action

REPLACE.

#### Replace with

> This thesis set out to extend a system that could explain the past with the
> ability to anticipate the future, under the resource budget a small provider
> actually operates within. It demonstrates that the extension is feasible,
> that the constraint which motivated it binds at design time rather than at
> run time, and that a forecast becomes usable not when it is accompanied by an
> interval but when it is accompanied by evidence of how far the model
> producing it has been right before.
>
> The result that most deserves to survive the thesis is the one it did not set
> out to find. A language model given the firm's data and the means to analyse
> it is a capable forecaster, and the case for a dedicated predictive layer
> rests not on beating it on error but on properties the error metric does not
> see: the same question answered the same way every time, at a cost that does
> not constrain how often it is asked, through a call that can be audited
> afterwards. For a production system advising a category planner, those are
> the properties that decide whether a forecast can be relied upon at all.

### Note — what this drops

"Positions AI as a calibrated decision partner" uses "calibrated" in the loose
sense the thesis spends Chapter 7 disowning. "Close with the IS research
framing" was an instruction to the writer rather than a sentence.

---

## Fix 7 — the Outstanding decisions block

### Anchor

The final block **"## Outstanding decisions"** with its three lines beginning
*"Exact "answer" language for each SRQ, dependent on the final empirical
results"*.

### Action

DELETE.

### Note

Two of the three are now settled: the answer language is written above, and the
empirical results have landed. The third, whether to add a one-page executive
summary, is a structural decision recorded separately rather than left in the
thesis text. The reflective paragraph on the human-AI research process belongs
in the AI Use Declaration, which already exists as its own section.

---

## Fix 8 — the tested alternatives belong in Chapter 5, not Chapter 10

**Added 2026-09-13 20:45**, folding in `interval-width-a-tested-negative-result.md`,
which is archived with this note.

⚠ **This fix edits Chapter 5, not Chapter 10.** It is filed here because it is
the other half of Fix 4: the conclusion says alternatives were measured, and
this is where the measurement goes. Applying Fix 4 without this one leaves the
conclusion asserting evidence the thesis never shows.

### Why the evidence belongs earlier

Section 5.5.7 is where a reader first meets an interval spanning thirty-four
times the forecast, and it is where they will ask whether anything was tried.
Answering it there converts the limitation from something endured into something
tested. Chapter 10 then restates the conclusion in one sentence, which is what a
conclusion is for.

### Anchor

**Section 5.5.7 Prediction-interval calibration**, the final paragraph, which is
the last thing before the **5.5.8 Holiday enrichment** heading.

Searchable opening: *"Each category's interval is calibrated on the residuals"*

It ends: *"...rather than a uniform stand-in for it."*

### Action

INSERT AFTER — three new paragraphs and a table, between that paragraph and the
5.5.8 heading.

#### Replace with

> The width was not accepted without testing whether it could be reduced. Three
> alternative calibration schemes were implemented and measured against the same
> held-out split, on the criterion that a scheme counts as an improvement only if
> coverage stays within five points of the ninety per cent target **and** the
> width falls. Narrowing an interval by undercovering is not an improvement; it
> is the guarantee being given up quietly.

| Category | Scheme | Empirical coverage | Median relative width |
|---|---|---|---|
| CSD | pooled, as deployed | 92.5% | 7.9x |
| CSD | two buckets by brand size | 91.6% | **3.2x** |
| CSD | volatility-scaled | 86.5% | **3.0x** |
| Danskvand | pooled, as deployed | 85.1% | 15.2x |
| Danskvand | two buckets by brand size | 79.9% | 3.7x, undercovers |
| Danskvand | volatility-scaled | 88.5% | **5.9x** |
| Energidrikke | pooled, as deployed | 88.6% | 18.2x |
| Energidrikke | two buckets by brand size | 79.9% | 6.4x, undercovers |
| Energidrikke | volatility-scaled | 82.1% | 12.4x, undercovers |

**Table 14** – *Three alternative calibration schemes measured against the
deployed one. A scheme improves on the deployed interval only where coverage
holds and width falls; bold marks the cases where both conditions are met.*

⚠ **This table renumbers eight others, and the caption number above assumes the
renumbering has happened.** Inserting here makes the new table 14, which pushes
every later table up by one:

| Currently | Becomes | What it is |
|---|---|---|
| Ch5 Table 14 | **15** | Forecast and accuracy variation across five seeds |
| Ch5 Table 15 | **16** | The selected model per seed |
| Ch5 Table 16 | **17** | Ch5 contributions to the SRQs |
| Ch6 Tables 17, 18, 19 | **18, 19, 20** | Scenarios, budget, technology choices |
| Ch7 Tables 20, 21 | **21, 22** | Payload groups, Ch7 contributions |

**Chapters 5, 6 and 8 use Word field references and renumber themselves.**
Chapter 7's two captions are typed as plain text, so **they must be edited by
hand** — that is the defect recorded as S26, and it is the only manual step.

✅ **The S26 collision itself is now resolved**: Chapter 6 runs 17 to 19 and
Chapter 7 runs 20 to 21, with no overlap. Verified against the 2026-09-13 20:40
snapshot. The register entry can be closed once this renumbering is applied.

⚠ **If you would rather not renumber eight tables two days out, the alternative
is to drop the table and keep the prose.** The three paragraphs stand on their
own: they state that three schemes were tested, that none won in more than two
categories, and why. The table is better evidence, but the argument survives
without it, and a numbering pass is the kind of change that goes wrong late.
**NEEDS-BRIAN.**

> No scheme wins in more than two of the four categories, and the scheme that
> helps most in one category undercovers in the next. That pattern is the
> signature of a sample-size limit rather than of a modelling choice. The
> intuitive repair, calibrating large brands separately from small ones, fails on
> row counts directly: the large-brand bucket holds twenty-eight calibration rows
> for carbonated soft drinks, eighteen for energy drinks, six for water and none
> at all for ready-to-drink beverages, where no brand exceeds the threshold. A
> ninetieth percentile estimated from twenty-eight residuals is not a ninetieth
> percentile, and with a minimum-row guard in place every large bucket falls back
> to the pooled quantile on precisely the brands the scheme was meant to fix.
>
> Two independent causes produce the width, and neither is reachable by
> retraining. A single quantile is pooled across brands spanning six orders of
> magnitude of volume, and each brand contributes only a handful of validation
> months, so a per-brand quantile cannot be estimated at all. The interval is
> computed from residual quantiles rather than from model weights, so changing
> how the residuals are summarised leaves both fitted models untouched. A
> per-series interval is therefore identified as future work rather than offered
> as an available refinement.

### Note — one correction worth recording, and it is not for the prose

An earlier version of this investigation reported that bucketing gave one brand a
band of ±1.35x instead of ±7.59x, and proposed adopting it. **That figure came
from twenty-eight validation rows covering four brands and did not survive an
honest test on the held-out split.** It is the failure mode the
train/validation/test discipline exists to prevent, and catching it is evidence
the discipline was applied rather than merely described.

⚠ **Keep this in the note, not in the chapter.** A thesis that narrates its own
corrected mistakes reads as a lab book. The *conclusion* — that promising
improvements measured on the data that motivated them tend not to survive — is
already carried by the table above.

### Note — provenance, and a caveat about regenerating it

⚠ **These figures have no committed artefact.** They come from
`plans/P0049_2026-09-07_17-50_finalizing-experiments/2026-09-11_eval_calibration_schemes.py`,
a one-off evaluation that writes no table into `05_thesis_results/`. That is a
departure from how every other number in Chapter 5 is produced.

Two consequences, and the first is a decision for you:

1. **If this table ships, the script should write its output into
   `05_thesis_results/05_model_benchmark/tables/` like every other producer**, so
   the numbers are regenerable and the Correctness-tier provenance rule holds.
   That is a small change to an existing script. **NEEDS-BRIAN.**
2. Until then the figures are a measured one-off. They are honest, and they are
   not reproducible by a reader, which is exactly the property the thesis
   criticises elsewhere.

⚠ **Danskvand's pooled coverage reads 85.1% here and 83.9% in Table 13.** The two
are different measurements — the scheme evaluation recomputes on its own split
arrangement — and publishing both without explanation invites a reader to find
the discrepancy. **Either reconcile them or report the alternatives as relative
improvements over each category's own pooled baseline rather than as absolute
coverage.** The second is safer and needs no re-run.

---

## Fix 9 — Chapter 5 states a coverage figure that exists in no artefact

**Added 2026-09-13 20:45.** This is the C8 item from the cross-chapter flow note,
repeated here because it sits in the same paragraph Fix 8 attaches to and should
be applied in the same pass.

### Anchor

**Section 5.5.7**, the paragraph beginning *"danskvand fails on the other axis."*

> "It misses the coverage target at both levels - 83.9 per cent against a nominal
> ninety, and 72.4 against a nominal eighty - on the smallest calibration set in
> the study, at 174 rows."

### Action

REWORD — change **72.4** to **73.6**. Nothing else in the sentence changes.

### Note

`calibration.csv` records Danskvand at the eighty per cent level as 73.6, and
Table 13 ten lines above prints 73.6. The figure 72.4 appears in no results file.
Verified again against the 2026-09-13 20:40 snapshot: still present.

---

# Comment ledger — all 8 threads

| Thread, by content and section | Verdict |
|---|---|
| Chapter title, "could use a subtitle" (`FORMATTING`) | **ADDRESSED** — see below |
| 10.1, the whole summary (`VERIFY, PROSE`) | **ADDRESSED** — Fix 1 |
| 10.2, design principles (`VERIFY, PROSE`) | **ADDRESSED** — Fix 2 |
| 10.3, practical recommendations (`VERIFY, PROSE`) | **ADDRESSED** — Fix 3 |
| 10.4, limitations recap (`VERIFY, PROSE`) | **ADDRESSED** — Fix 4 |
| 10.5, future research (`VERIFY, PROSE`) | **ADDRESSED** — Fix 5 |
| 10.6, final statement (`VERIFY, PROSE`) | **ADDRESSED** — Fix 6 |
| Outstanding decisions (`METACOMMENT`) | **ADDRESSED** — Fix 7, deleted |

### The subtitle

> **What the extension is worth, and on which axis**

---

# One thing this note deliberately does not do

**It does not restate the main research question verbatim at the opening.** The
current chapter does, in italics, and Chapter 1 states it too. Repeating it
word for word across two chapters reads as padding in a document with a page
limit; the replacement paraphrases it in the first sentence and answers it in
the second, which is the conventional shape for a conclusion.

⚠ If you prefer the verbatim restatement, it belongs as a single italic line
before the replacement's first paragraph, not inside it — **NEEDS-BRIAN**, and
purely a matter of taste.
