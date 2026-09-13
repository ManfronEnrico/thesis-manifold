---
name: 2026-09-13_18-40_BRANCH_A_ch10-branch-a-rewrite
description: NOTE - Chapter 10 rewritten against BRANCH A. Every SRQ answer in 10.1 is wrong: XGBoost everywhere, a chain grain deleted in August, a judge study that does not exist, and an SRQ4 answer saying the central comparison was never run. Full replacement prose with all 8 comment threads resolved.
category: workflow
applies-to: [ch10_limitations]
triggers: [chapter 10, conclusion, branch a, rewrite]
created: 2026_09_13-18_40
updated: 2026_09_13-18_40
snapshot: 2026-09-13_18-18_branch-a-full-review
status: prose ready to paste, awaiting human review
---

# Chapter 10 — BRANCH A rewrite

Verified at `c9c0587`, fetch clean. Snapshot
`2026-09-13_18-18_branch-a-full-review`. Zotero: **89 items**, re-pulled this
session.

**Notes swept:** one live note in this folder —
`interval-width-a-tested-negative-result.md`, **not applied**, carried into F5
below. Not archived, because it holds the alternative-scheme table that F5 only
summarises and Chapter 9's limitations section also draws on.

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

### Note — what is preserved from the live chapter note

`interval-width-a-tested-negative-result.md` argues the interval limitation
should be written as a contribution, because three alternative schemes were
implemented and measured. **That argument is honoured in Ch9 Fix 10 and in
10.4 above**, where the limitation is stated with the fact that alternatives
were tested. It is deliberately not repeated at length here; a conclusion
restates, it does not re-argue.

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
