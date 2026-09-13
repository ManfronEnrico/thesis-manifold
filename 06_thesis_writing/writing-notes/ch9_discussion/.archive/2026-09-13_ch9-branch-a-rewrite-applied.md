---
name: 2026-09-13_18-40_BRANCH_A_ch9-branch-a-rewrite
description: NOTE - Chapter 9 rewritten against BRANCH A. The chapter predates the funded experiment entirely: it states the code-as-action baseline was never run, names XGBoost in every category, and cites an LLM-as-judge study that does not exist in this design. Full replacement prose, section by section, with all 17 comment threads resolved.
category: workflow
applies-to: [ch9_discussion]
triggers: [chapter 9, discussion, branch a, rewrite]
created: 2026_09_13-18_40
updated: 2026_09_13-18_40
snapshot: 2026-09-13_18-18_branch-a-full-review
status: prose ready to paste, awaiting human review
---

# Chapter 9 — BRANCH A rewrite

Verified at `c9c0587`, fetch clean, 0 ahead / 0 behind. Snapshot
`2026-09-13_18-18_branch-a-full-review` (43,584 words, 152 comments, source
modified 2026-09-13 13:45). Zotero re-pulled the same session: **89 items**.

**Notes swept:** four live notes in this folder, none applied, all carried
forward rather than duplicated —
`ad-hoc-data-science-vs-a-trained-pipeline.md` (→ F2, F9),
`srq4-interpreting-the-accuracy-gap.md` (→ F4),
`the-result-hinges-on-forecasting-practice.md` (→ F4, F10),
`when-to-use-which-scenario-group.md` (→ F5). None is archived by this note,
because each holds reasoning this chapter only partly consumes.

---

# Why this is a rewrite and not a pass

Chapter 9 was last edited on 5 September. That is **before the funded
experiment, before the Ch5/Ch6 swap, and before the ladder existed.** It is not
a chapter with stale numbers in it. Every substantive claim in 9.1 is about a
study that was either never run or has since been replaced.

| Claim in the chapter | Status |
|---|---|
| "the code-as-action LLM baseline ... was *not* executed" | **false.** 63 funded runs, 2026-09-12 |
| "Tuned XGBoost was the best model in every category" | **false.** Two of four serve LightGBM |
| test WMAPE "16.5 / 22.0 / 11.4 / 31.0" | **wrong in all four.** No artefact holds these |
| "disaggregating to a retail-chain dimension" | the chain grain was **deleted** from the repo, P0035 |
| "GPT-4o (LLM-as-Judge, N=50)" scores on five dimensions | **no such study exists** in this design |
| "empirical coverage 80–98%" | **not the measured range.** 73.6 to 91.7 |
| DP1 "Ridge 1.5, LightGBM 18.7, XGBoost 0.2 MB" | **wrong**, and internally impossible |
| "≤8 GB constraint" | the thesis constraint is **four** gigabytes |
| SHAP "lag_1 and weighted_distribution" | `weighted_distribution` was **tested and excluded** (Ch4) |

Nine independent defects in a 1,210-word chapter, most of them load-bearing.
Editing around them would leave a chapter arguing for a study the thesis did
not run. The replacement below is the same length.

---

# The fixes

## Fix 1 — 9.1.1 states SRQ1 results that match no artefact

### Anchor

**Section 9.1.1 SRQ1: Forecasting accuracy under constraints.** The whole
section is one paragraph.

⚠ **The model names in this sentence are italicised in Word**, so search on a
fragment without them. Searchable opening: *"was the best model in every
category, ahead of"*. In the snapshot the line reads
`Tuned *XGBoost* was the best model in every category, ahead of *LightGBM*,
*Ridge*, and the *SeasonalNaive* baseline`.

The paragraph ends *"...and lends face validity to the models."* The italic
line beneath it starts *"Connect to: Edge AI / Efficient & Green LLMs"*.

### Action

REPLACE the paragraph. **Delete the italic "Connect to:" line entirely** (it is
a note to yourselves; see Fix 11).

#### Replace with

> The benchmark's headline result is that the choice between the two
> gradient-boosted families is not supported by this data. A five-seed sweep
> holding every other input identical shows the selected model changing with
> the seed in all four categories, and the difference in weighted error between
> the two families, between 0.3 and 1.2 percentage points, sits inside a
> between-seed standard deviation reaching 2.81. The defensible claim is
> therefore that the two are statistically indistinguishable here, which is a
> weaker headline than naming a winner and a more useful one: a practitioner
> may choose on training time, memory footprint or tooling maturity without
> forfeiting accuracy.
>
> What the benchmark does support is the gap between model families. Both
> gradient boosters beat Ridge and ARIMA in every category, and both lose to a
> parameter-free seasonal naive forecast on ready-to-drink beverages and to
> Prophet on water. Those differences exceed the seed noise. That two of four
> categories are beaten outright by a benchmark costing nothing to compute is
> the most important qualification this thesis places on its own substrate, and
> it is reported rather than absorbed.
>
> The pooling question resolves conditionally, and the condition is data
> volume. Pooling across categories wins on the two smallest panels by between
> 4.5 and 5.7 percentage points, and the agreement between the two model
> families on that point is what makes it a finding rather than one algorithm's
> inductive bias. On the larger panels the arms disagree, so the claim is
> confined to the direction of the small-panel effect.
>
> On the operational axis the constraint that motivated the whole substrate
> does not bind. Peak resident memory during fitting is 31.9 megabytes for
> XGBoost and 14.9 for LightGBM, against a four-gigabyte ceiling, and serving a
> forecast peaks below half a megabyte. The budget does its work at selection
> time, excluding transformer and locally hosted options before any of them is
> fitted, rather than at run time. That is a substantive answer to the research
> question rather than a missing measurement: the constraint is real as a
> design criterion and slack as a runtime one.

### Note — where each figure comes from

Seed table and the 2.81: Ch5 Table 14. Pooling deltas: Ch5 Table 12. Memory:
`tables/profiling.csv`. All four are already in the document, so this paragraph
introduces no number the thesis does not already carry.

⚠ **Do not restore a per-category WMAPE list here.** Ch5 reports those, and
naming a winner per category is precisely what Ch5's Section 5.6 withdraws.

---

## Fix 2 — 9.1.2 describes a synthesis study that no longer exists

### Anchor

**Section 9.1.2 SRQ2: Synthesis quality.** One paragraph, starting *"The
deterministic synthesis core produced well-to-conservatively calibrated
ensemble intervals"*, ending *"...the clearest target for prompt hardening."*
with the italic *"Connect to: Kuleshov 2018 (calibration)"* line.

### Action

REPLACE the paragraph and delete the "Connect to:" line.

#### Replace with

> The interface answers SRQ2 unevenly, and the unevenness is the finding.
> Reliability holds by construction and was checked rather than asserted:
> across every run of the funded evaluation the figure the agent reported
> matched the figure the tool returned, and every answer carried the
> fixed-format closing line, so no answer required the fallback parser.
> Traceability is implemented in full and evaluated in part, in that a
> recommendation can be reconstructed from the question that produced it
> through to the value extracted from the answer, while only one of the two
> checks that would demonstrate as much is reported.
>
> Uncertainty is where the chapter returns a negative result. The interval is
> preserved in form: every forecast carries one, it is built empirically from
> held-out residuals rather than assumed, and its coverage is measured rather
> than claimed. It is not preserved in usable substance. At the ninety per cent
> level the interval spans between roughly eight and thirty-four times the
> quantity being forecast, which is not a range a planner can act on; at eighty
> per cent it narrows to a workable three to four times for three categories
> while energy drinks remain above ten. The confidence index intended to
> summarise this discriminates nothing at all, because both of its terms are
> functions of a quantile that is fixed within a category, so every forecast in
> every category is assigned the lowest of three bands.
>
> The honest formulation is that the interface delivers a truthful account of
> its own uncertainty rather than a useful one. That distinction strengthens
> rather than weakens the chapter's central claim, which is that an interval
> attached to a forecast is not by itself what makes the forecast usable: the
> measured track record travelling in the same payload is what carries the
> claim about how far a forecast may be relied upon.

### Note — thread on 9.1.2 closes as ADDRESSED

The thread tagged `VERIFY` on this paragraph asked for verification. The
verdict is that none of it survived: there is no ensemble, no judge, no N=50,
and the coverage range is 73.6 to 91.7 rather than 80 to 98. The replacement
rests only on Ch5 Table 13 and Ch7.

---

## Fix 3 — 9.1.3 overstates what SRQ3 could not do

### Anchor

**Section 9.1.3 SRQ3: Integration readiness.** Starts *"SRQ3 is addressed as an
integration-readiness assessment, not a live integration: production access to
the Prometheus platform was not available"*, ends *"...not architectural."*

### Action

REWORD the opening clause; keep the rest of the paragraph. Delete the
"Connect to:" line.

**Before:**

> "SRQ3 is addressed as an integration-readiness assessment, not a live
> integration: production access to the Prometheus platform was not available
> and was not required for the thesis, which runs entirely on a local Nielsen
> snapshot."

**After:**

> "SRQ3 is addressed as an integration-readiness assessment rather than a
> production deployment, but it is no longer argued from architecture alone.
> Three of the seven evaluation scenarios were executed inside the production
> agentic platform, so the readiness criteria are derived from the capabilities
> an integration actually depended upon rather than from the capabilities an
> integration was expected to need."

### Note — this is the thread tagged OUTDATED on 9.1.3, and it closes

The comment is right that the paragraph is outdated, and right in a direction
that **favours the thesis**. Scenarios D, E and G ran on Prometheus; 27 of the
63 funded runs are production-orchestrated. Chapter 1 already claims this
("the forecasting tool developed for SRQ2 is registered with and executed
inside the production system"), so the discussion was contradicting the
introduction.

⚠ **Do not upgrade this to a claim of completed deployment.** Operational
hardening, monitoring and adoption remain out of scope, and the existing final
sentence about the remaining gap being operational is still correct.

---

## Fix 4 — 9.1.4 says the central experiment never ran

### Anchor

**Section 9.1.4 SRQ4: dedicated ML vs the LLM/traditional baselines.** Starts
*"Against the **traditional statistical baseline**, dedicated ML (XGBoost)
beats ARIMA in three of four categories"*, ends *"...both favouring the
dedicated/structured approach on the decision-relevant dimensions."*

### Action

REPLACE the entire section. This is the largest single edit in the chapter.
Delete the "Connect to:" line.

#### Replace with

> The comparison that motivates the thesis was executed as a ladder of seven
> scenarios over sixty-three funded runs, and its result is that no scenario
> leads on every axis. That disagreement is the contribution rather than an
> inconvenience, because it is what allows a deployment decision to be made on
> grounds other than a single accuracy number.
>
> The bottom rung behaves as the design predicts. A language model given no
> access to the firm's data is the only scenario that fails, and it fails on
> the smallest brand, answering in the wrong order of magnitude three times in
> succession. Giving the same model the brand's history and an execution
> environment moves the median absolute percentage error from 502 to 2.9. That
> first increment, the value of data access at all, is far larger than anything
> measured above it, and a two-way comparison would have folded it into the
> effect the thesis is actually about.
>
> The second increment is the thesis contribution, and it is not an accuracy
> gain. Replacing self-written analysis with a dedicated model behind a
> structured interface produces a worse median error and a better mean, which
> is to say the code-writing scenarios are better most of the time and
> occasionally much worse. What the dedicated model buys instead is cost, speed
> and reproducibility: it is cheaper by a factor of roughly fifty, faster by a
> factor of roughly twenty, and it returns an identical figure on every repeat,
> to the decimal, on both orchestrators. Its coefficient of variation is zero
> because a persisted model answers from parameters that do not change between
> invocations, while a generated analysis is re-derived each time.
>
> That reproducibility result deserves to be stated as a property rather than a
> statistic. Across three repeats of an identical prompt, the scenario with no
> firm data varied by 767 percentage points on a single brand and the
> code-writing scenario by 23, while the dedicated-model scenarios varied by
> nothing at all. Differences between scenarios smaller than the variation
> within them cannot be read as an ordering, and a single run of each would
> have produced a ranking that looked clean and meant nothing.
>
> The comparison is nonetheless conditional on forecasting practice on both
> sides, and saying so is necessary to keep the reader from over-generalising.
> The code-writing scenarios did not improvise: every one of them fitted
> exponential smoothing and a seasonal ARIMA, most added a decomposition, and
> twelve of fourteen combined their candidate models explicitly. Those are
> precisely two techniques the thesis pipeline lacks, since exponential
> smoothing is absent from the benchmark and the pipeline's ARIMA carries no
> seasonal term. A material part of the code-writing scenarios' median accuracy
> is therefore plausibly attributable to established practice the substrate
> does not yet implement, rather than to code execution as such. That is a
> limitation of this comparison and a concrete, cheap direction for the next
> cycle.
>
> A second qualification bears on what is being compared. The dedicated model
> is one configuration tuned once for an entire category and serving
> ninety-five brands; the code-writing scenarios fit a fresh small model
> competition to each brand's own history. Where the code-writing scenarios
> win, the result may be measuring per-series adaptation rather than code
> execution, and the two are different claims. The thesis reports the
> measurement and declines to resolve the attribution, which the present design
> cannot separate.

### Note — the three threads on 9.1.4

All three close. The `OUTDATED` tag is correct and now inverted: the baseline
ran. The `VERIFY` tag is answered by the recomputation. The `PROSE` tag is
answered by the replacement being prose.

⚠ **The chapter must not claim the code-writing scenarios are less accurate.**
On the median they are better. The defensible claim is the one written above:
they win the median, lose the mean, and lose cost, latency and reproducibility
outright.

---

## Fix 5 — a missing section: deployment guidance

### Anchor

**End of Section 9.1**, after the replaced 9.1.4 and before *"9.2 Theoretical
contributions"*.

### Action

INSERT AFTER — a new subsection 9.1.5.

#### Replace with

> ### 9.1.5 Which configuration to deploy
>
> The ladder supports a recommendation that a two-way comparison could not,
> because it measures the axes separately. Where a forecast must be
> reproducible, auditable and cheap enough to serve on every query, the
> dedicated model behind the structured interface is the configuration to
> deploy: it is the only one whose answer does not change between runs, and at
> roughly a cent per answer its cost does not constrain how often it may be
> asked. Where a one-off analysis is wanted and a human will read the working,
> the code-writing configuration produces a better typical answer and an
> occasional very poor one, which is acceptable under review and not acceptable
> unattended.
>
> The combined configurations, which receive both, are the least expected
> result. They are not better than their own components: on this evaluation
> they sit between the two on accuracy while carrying the cost and latency of
> the code-writing path. Their value is not accuracy but the behaviour reported
> in Chapter 7, where every combined run departed from the model's forecast and
> frequently cited the model's own stated uncertainty as the reason. That is
> the integration the architecture was built to support, and it is also the
> configuration that most clearly exposes what the interface does not yet
> carry.

### Note — provenance

Cost and latency from the recomputed ladder; the 18-of-18 departure from the
Chapter 7 pass. `when-to-use-which-scenario-group.md` is the source note; its
figures were re-derived from the funded set rather than carried over, and the
provisional smoke numbers in it are superseded.

---

## Fix 6 — 9.2.1 names an artefact the thesis does not build

### Anchor

**Section 9.2.1 Design knowledge contribution (DSR framing).** Begins *"The
multi-agent framework constitutes a DSR artefact at two levels"*, and includes
the bolded **Instantiation level** and **Method/design-theory level** lines and
a trailing *"Cite:"* line.

### Action

REPLACE the whole subsection, bullets and Cite line together.

#### Replace with

> The thesis produces a design-science contribution at two levels, following
> Hevner et al. (2004). At the instantiation level it delivers a working
> predictive extension: a forecasting substrate, a structured tool interface
> and a bounded tool-using agentic layer, exercised on commercial retail
> scanner data and evaluated in both a general-purpose orchestrator and a
> production one. At the method level it contributes transferable design
> knowledge about extending a non-predictive agentic system with forecasting,
> stated below as design principles and derived from what the evaluation
> measured rather than from what the architecture intended.
>
> One framing correction belongs here, because it recurs through earlier
> chapters. The artefact is a bounded tool-using agent and not a multi-agent
> system, in the sense Sapkota et al. (2026) distinguish: it holds a fixed tool
> set, delegates to no other agent, and does not act on its own
> recommendation. Describing it otherwise would claim a coordination
> contribution the thesis does not make.

### Note — the `VERIFY, PROSE` thread closes

"Multi-agent framework" and "System A" are both vocabulary from a superseded
design. Ch6 already calls the artefact a bounded tool-using agent, so this
section was contradicting the architecture chapter.

⚠ `Artifact Types in IS Design Science (LNCS 2012)`, `AI-Based DSR Framework
2024` and `Pathways for Design Research on AI 2024` are **cited in this chapter
and are not in the Zotero library.** The library holds Hevner (2004) and
Peffers (2007) and no other DSR methodology source. The replacement cites only
those two. Adding the others means adding them to Zotero first — see the
register entry below.

---

## Fix 7 — the design-principles table (Table 23) carries wrong figures

### Anchor

**Section 9.2.2**, the four-row table whose header is
*"# | Principle | Problem class | Evidence from this thesis"*, captioned
**Table 23 - Contributions - Design Principles**. Its DP1 row contains the
searchable string *"Ridge 1.5, LightGBM 18.7, XGBoost 0.2 MB"*, which is unique
in the document and the safest thing to search for.

⚠ **The caption's "Table" and its number are separately bolded in Word**
(`**Table** **23**`), which is the house pattern throughout the thesis. Search
on *"Contributions - Design Principles"* rather than on the whole caption.

### Action

EDIT-THEN-INSERT. Replace the table body and caption, then add the paragraph
below it.

#### Replace the table with

| # | Principle | Problem class | Evidence from this thesis |
|---|---|---|---|
| DP1 | Delegate prediction; do not generate it | Numerical decision-support where an answer must be reproducible | The two tool-backed scenarios returned an identical figure on every repeat and on both orchestrators; the code-writing scenarios returned a different value on almost every repetition |
| DP2 | Refuse explicitly rather than fall back | Any interface whose consumer is a generative model | Three refusal conditions return a stated reason instead of a substituted value; a fallback asserts that something was found, and an agent cannot recognise it as anything else |
| DP3 | Carry the model's track record, not only its interval | Forecast delivery to a non-expert consumer | The interval spans 8 to 34 times the forecast at the ninety per cent level and the confidence index returns one value per category, so neither carries the reliability claim; the measured out-of-sample error does |
| DP4 | Budget memory at selection time, report it at run time | Resource-constrained ML deployment | The four-gigabyte ceiling excluded transformer and locally hosted options before fitting, while the realised end-to-end peak is approximately 231 MB, under six per cent of the budget |
| DP5 | Report cost and latency beside accuracy | Deployment-oriented AI artefacts | Cost per answer differs by a factor of roughly fifty between scenarios of comparable accuracy, which no accuracy-only evaluation would surface |

**Table 23** – *Design principles, with the evidence in this thesis that
supports each*

#### Then INSERT AFTER the table

> Each principle is stated at the level of the problem class rather than of
> this artefact, which is what makes it design knowledge rather than a
> description. Each is also falsifiable against the evidence column: the
> principles are asserted because something in this evaluation would have come
> out differently had they not held.

### Note — what changed and why

- **DP1 renamed.** "Sequential execution" was a principle about the memory
  budget, and the memory budget turned out not to bind; delegation-over-
  generation is the principle the evaluation actually supports.
- **Old DP1's figures deleted.** "Ridge 1.5, LightGBM 18.7, XGBoost 0.2 MB" is
  wrong and internally impossible, since it makes XGBoost the smallest. The
  measured figures are XGBoost 31.9, LightGBM 14.9, Ridge 1.6.
- **"≤4 GB" throughout**, not 8. The thesis constraint is four gigabytes in
  Ch6, Ch5 and Ch2; only Ch1, Ch9 and Ch10 say eight. See the flow report.
- **DP3 is new** and is the chapter's strongest principle, because it is the
  one the negative result produces.
- There was no DP3 in the original table. It ran DP1, DP2, DP4, DP5 — the
  numbering skipped, which is itself a sign the table had been edited without
  being re-read.

---

## Fix 8 — 9.2.3 and 9.2.4 claim novelty the thesis cannot defend

### Anchor

**Section 9.2.3 Novelty claims**, three bullets beginning *"First system to
combine: LLM orchestration + ≤8GB constrained ML ensemble + MCDM synthesis"*,
and **Section 9.2.4 Contribution to IS literature**, two bullets beginning
*"Extends Pathways for Design Research on AI (ISR 2024)"*.

### Action

REPLACE both subsections with a single subsection.

#### Replace with

> ### 9.2.3 Contribution to the literature
>
> The contribution is an intersection rather than a component. Each of the four
> literatures reviewed in Chapter 2 supplies one element of the problem and
> none addresses their combination: the forecast-to-decision literature couples
> prediction and decision tightly through a formally specified objective, the
> agent literature establishes tool delegation without connecting it to
> statistical forecasting, the reliability literature specifies requirements
> without an integration, and the production-agent exemplars are built for
> real-time supervision on dedicated infrastructure. What this thesis adds is a
> loosely coupled, agent-mediated extension of a non-predictive production
> system, with the increment attributable to the dedicated model measured
> against a code-writing alternative rather than assumed.
>
> The measurement is the part that is hardest to find elsewhere. The
> code-as-action pattern is normally proposed as an alternative to structured
> tool calls on the strength of benchmark performance; here it is run as a
> controlled comparator on the same question, with the same base model, in two
> independently built orchestrators, and it wins on the axis usually reported
> and loses on three that usually are not.

### Note — what was removed, and why it cannot be restored

| Claim | Problem |
|---|---|
| "First system to combine..." | A priority claim needs a systematic search to support it. Chapter 2 is explicitly a narrative review |
| "MCDM synthesis" | There is no multi-criteria decision method in the artefact |
| "ML ensemble" | One model is served per category; Ch5 settles this |
| "Memory profiling methodology ... replicable protocol contribution" | Measuring RSS is standard practice, not a contribution |
| "SME-grade hardware is sufficient" | Supportable, but it is DP4, not a separate novelty claim |
| "Extends *Pathways for Design Research on AI* (ISR 2024)" | **Not in Zotero.** Cannot be cited |
| "Extends AI-augmented decision making design principles (2024)" | **Not in Zotero.** Cannot be cited |

---

## Fix 9 — 9.3 practical implications, restated against measurement

### Anchor

**Section 9.3 Practical implications**, three bullets beginning *"For Manifold
AI: validated architecture for integrating predictive analytics"*.

### Action

REPLACE with prose.

#### Replace with

> For the case organisation, the practical finding is that the extension is
> deployable at a cost that does not constrain how often it is used. Serving a
> forecast costs roughly a cent and returns in about six seconds, against
> roughly thirty-one cents and two minutes for an equivalent answer generated
> by code. Because both the language model and the execution sandbox are
> reached as hosted services created per request, an idle deployment carries no
> compute cost at all, which matters more to a small provider than the peak
> figure does.
>
> For practitioners considering the same extension, the transferable result is
> that the decision should not be made on accuracy. On this evaluation the two
> approaches are close enough on error that the choice is properly made on
> reproducibility, auditability and cost, all three of which favour the
> dedicated model, and on flexibility, which favours code execution. An
> organisation that needs the same question answered the same way every time
> should not be choosing on a median error difference that a different seed
> would reverse.
>
> For the field, the caution is that an agent given data and a sandbox is a
> stronger baseline than it is usually credited as being. It reached for
> exponential smoothing and seasonal ARIMA unprompted on every run, and
> combined its candidate models in the great majority of them. A thesis
> proposing a dedicated forecasting layer owes that baseline a fair test, and
> the finding here is that it clears a bar the literature does not usually set
> for it.

---

## Fix 10 — 9.4 limitations, rebuilt on what was measured

### Anchor

**Section 9.4 Limitations**, five bullets beginning *"Single company/context:
Nielsen CSD data from one company's clients"*.

### Action

REPLACE.

#### Replace with

> Five limitations bound what this chapter may claim.
>
> The evaluation covers three brands in one of the four categories, with three
> repeats, for a total of sixty-three runs. The brands are stratified by volume
> rather than chosen, so the range is covered, but a sample of this size
> establishes differences that are large relative to the variation within
> scenarios and nothing finer.
>
> The forecasting practice on both sides is a property of this comparison
> rather than of the approaches in general. The substrate lacks exponential
> smoothing and a seasonal ARIMA term; the code-writing scenarios used both on
> every run. A substrate that closed that gap would be a different comparator,
> and the direction of the accuracy result on the median might not survive it.
>
> The dedicated model is tuned per category and the code-writing scenarios fit
> per brand, so where the latter win, per-series adaptation and code execution
> are confounded. Separating them would require a per-brand dedicated model,
> which the panel's length does not support.
>
> The intervals attain their coverage guarantee and are too wide to act on for
> an individual brand. Three alternative calibration schemes were implemented
> and measured, and none improved coverage and width together in more than two
> of four categories, which is the signature of a sample-size limit rather than
> a modelling choice.
>
> What the evaluation measures is what each scenario communicated and how
> accurate it was, not whether a planner receiving that communication decided
> better. Establishing the latter requires an experiment with human
> participants and ethical approval, and is outside the scope of this thesis.

### Note — deletions

`claude-sonnet-4-6 at temperature=0` is doubly wrong: the pinned model is not
that, and temperature is not settable on it, which the harness records
explicitly. "LLM-as-Judge N=50" does not exist. "Fallback dataset" never
happened.

---

## Fix 11 — the "Connect to:" lines and the Outstanding decisions block

### Anchor

Four italic lines beginning *"Connect to:"* in 9.1.1, 9.1.3 and 9.1.4, and the
final block **"## Outstanding decisions"** with its two lines beginning *"Depth
of theoretical contribution section"*.

### Action

DELETE all five.

### Note — this is the `METACOMMENT` tag, five threads at once

These are notes to yourselves inside submission prose. An examiner reading
"Connect to: Edge AI / Efficient & Green LLMs" learns that the chapter has a
to-do list. The green tick in the Outstanding decisions block is the same
problem in a stronger form, since it also says the values "will be filled after
empirical results" — which invites the question of whether they were.

---

# Comment ledger — all 17 threads

| Thread, by content and section | Verdict |
|---|---|
| Chapter title, "could use a subtitle" | **ADDRESSED** — see below |
| 9.1.1, the SRQ1 results paragraph (`VERIFY`) | **ADDRESSED** — Fix 1 |
| 9.1.1, "Connect to: Edge AI" (`METACOMMENT`) | **ADDRESSED** — Fix 11, deleted |
| 9.1.2, the synthesis-quality paragraph (`VERIFY`) | **ADDRESSED** — Fix 2 |
| 9.1.3, integration readiness (`VERIFY, OUTDATED`) | **ADDRESSED** — Fix 3 |
| 9.1.3, "Connect to: Ch3/Ch5" (`METACOMMENT`) | **ADDRESSED** — Fix 11, deleted |
| 9.1.4, the SRQ4 paragraph (`VERIFY, PROSE, OUTDATED`) | **ADDRESSED** — Fix 4 |
| 9.1.4, "Connect to: Humans vs. LLMs" (`METACOMMENT`) | **ADDRESSED** — Fix 11, deleted |
| 9.2.1, DSR framing bullets (`VERIFY, PROSE`) | **ADDRESSED** — Fix 6 |
| 9.2.2, Table 23 caption (`VERIFY, NAMING`) | **ADDRESSED** — Fix 7 |
| 9.2.2, the "Cite:" line (`VERIFY, PROSE`) | **ADDRESSED** — Fix 7, folded into prose |
| 9.2.3, novelty claims (`VERIFY, PROSE`) | **ADDRESSED** — Fix 8 |
| 9.2.4, IS contribution (`VERIFY, SOURCE, PROSE`) | **ADDRESSED** — Fix 8; both sources absent from Zotero |
| 9.3, practical implications (`VERIFY, SOURCE, PROSE`) | **ADDRESSED** — Fix 9 |
| 9.4, limitations (`VERIFY, PROSE`) | **ADDRESSED** — Fix 10 |
| 9.5, future research (`VERIFY, PROSE`) | **ADDRESSED** — see Fix 12 below |
| Outstanding decisions (`METACOMMENT`) | **ADDRESSED** — Fix 11, deleted |

### The subtitle

Every other chapter now carries one. Suggested, matching the pattern:

> **What the ladder measured, and what follows for deployment**

---

## Fix 12 — 9.5 future research

### Anchor

**Section 9.5 Future research directions**, four bullets beginning
*"Multi-agent memory sharing"*.

### Action

REPLACE.

#### Replace with

> Four directions follow from what this evaluation could not settle.
>
> The substrate should be given the two techniques the code-writing scenarios
> applied unprompted on every run: exponential smoothing as a benchmark family,
> and a seasonal term in the classical baseline. Both are established practice,
> both are cheap, and the comparison cannot be called settled until the
> dedicated side has them.
>
> The interface should carry a per-series error rather than a per-category one.
> Every combined run departed from the model's forecast and several cited its
> uncertainty in doing so, but the payload supplies no quantity from which a
> brand-specific weight could be derived, so each run invented its own. That is
> a contract gap the experiment identified and the next cycle can close.
>
> The evaluation should be widened across categories and repeats before any
> claim about which approach is more accurate is made at all. The present
> design is sized to detect differences larger than the within-scenario spread,
> and the accuracy difference is not one of them.
>
> Finally, whether a communicated forecast improves a planner's decision
> remains untested here and is the question the decision-support literature
> actually asks. Answering it requires the experimental design of Goodwin,
> Önkal and Thomson (2010) with human participants, which is a different study
> rather than an extension of this one.

---

# Claims register additions

Two sources are cited in the current Chapter 9 and are **not in the Zotero
library** (verified against the 89-item pull this session, and against an
unfiltered API query, since `citations.json` drops non-scholarly types):

| Source as cited | Where | Action |
|---|---|---|
| *Artifact Types in IS Design Science*, LNCS 2012 | 9.2.1 | Find and add, or drop the claim. The replacement drops it |
| *Pathways for Design Research on AI*, ISR 2024 | 9.2.4, 9.2.2 | Same. The replacement drops it |
| *AI-Based DSR Framework 2024* | 9.2.1, 9.2.2 | Same. The replacement drops it |
| *AI-augmented decision making DSR 2024* | 9.1.2, 9.2.2 | Same. The replacement drops it |

⚠ **None of the four resolves to a real, identifiable reference as written.**
Each is a descriptive phrase rather than an author-and-year, which is what a
citation written from memory looks like. The replacement prose cites only
Hevner et al. (2004), Peffers et al. (2007), Sapkota et al. (2026) and Goodwin
et al. (2010), all four of which are in the library and already cited elsewhere
in the thesis.

---

# What this note does not fix

- **Table 23's number.** Ch7's final table is already Table 19 and Ch8's run to
  23, so Chapter 9's "Table 23" collides. This is the same numbering collision
  recorded as S26; it needs a Word pass over the whole document rather than a
  per-chapter edit. **NEEDS-BRIAN.**
- **The ≤8 GB / ≤4 GB split.** Ch1, Ch9 and Ch10 say eight; Ch2, Ch5 and Ch6
  say four. The replacement prose says four. Chapter 1 still needs the same
  correction, and it is in the flow report rather than here because it is a
  cross-chapter defect.
