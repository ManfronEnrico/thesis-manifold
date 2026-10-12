---
name: qa-drill
description: REFERENCE - Defence drill. Every likely examiner question in a 20-second-answer format, printable and usable in the exam room. EXTENDS anticipated-assessor-questions.md; does not replace it.
category: reference
applies-to: [oral defence]
triggers: [rehearsing for the defence, the day before, in the room]
created: 2026_09_15-18_30
updated: 2026_10_12-10_30
---

# Q&A drill

**Exam aids are permitted. No GenAI tool may be used during the defence.** So
this file has to work on paper, from memory, under pressure.

## How it differs from `anticipated-assessor-questions.md`

That file is the **evidence base** — 25 questions with full answers, artefact
paths and reasoning. It is the thing to read the week before.

This file is the **drill** — the same material compressed to what can be said in
twenty seconds, plus the questions that file does not yet cover. Read this the
morning of.

⚠ **Three rows in that file are now stale.** Its "Questions we cannot yet
answer" table lists U1, U2 and U3 as blocked on "the funded run". **The funded
run has happened** — 63 runs, 2026-09-12. All three are answered. Do not read
those rows as open questions.

## The format

> **Q** — the question as an examiner would ask it
> **20s** — what to say, out loud, in about twenty seconds
> **Then** — the evidence, if they push
> **Concede** — what the honest answer gives up

---

# Part 1 — The questions most likely to open the dialogue

## Q1 · "Your own thesis says a scenario without your model was more accurate. Why did you build it?"

**20s.** "Because accuracy was never the axis the artefact competes on. The
code-writing scenario is better on the median and worse on the mean — better
most of the time, occasionally much worse. Our model costs a fiftieth as much,
answers twenty times faster, and returns an identical figure on every repeat.
For a system answering the same question on every query, those are the
properties that decide whether it can be relied on."

**Then.** Funded set, 63 runs: C at $0.0091 and 6.0 s against B at $0.4667 and
123.8 s — roughly fifty times the cost and twenty times the latency (the
thesis's own wording; never "51" or "21"). Median 14.6 against 2.9; mean
13.1 against 27.9. Coefficient of variation 0.0 against 4.1.

**Concede.** "At this data scale" is load-bearing and must carry its numbers
every time: 46 months of history with the last six or seven held out, 95 brands
in the category, one category-tuned model. *(Ch4 §4.1, §4.4)*
Without them the claim degrades into a universal one the evidence cannot
support.

⚠ **Never let "the code arm won" stand bare.** As a bare fact it invites the
conclusion that the artefact is unnecessary.

## Q2 · "Three brands from one category. What can that possibly establish?"

**20s.** "It is sized to detect differences between scenarios that are large
relative to the variation within them — not to establish cross-category
generalisation, and we do not claim that. The three brands span three orders of
magnitude of volume, and every scenario answers for the same three brands, so
differences are attributable to the scenario rather than to the draw."

**Then.** Stratified by volume — largest, median, smallest — from a population
defined by three criteria fixed before any run.

**Concede.** It is declared in the design chapter, not only in limitations. A
scope limitation appearing first in Chapter 10 reads as something discovered
late.

⚠ **Never** justify the brand selection on "hard to forecast" grounds. That is
outcome-based selection.

## Q3 · "Did your language model just repeat each brand's last month?"

**20s.** "No — and not once in eighteen runs. The history each scenario was
shown is recorded alongside the answer it gave, so this is measurable rather
than arguable. Not one forecast fell within five per cent of the brand's last
observed month. They sat much closer to a trailing twelve-month average, with
about half the dispersion around it."

**Then.** Consistent with the explicit model-fitting visible in their working: every
code-writing scenario fitted exponential smoothing and a seasonal ARIMA, and
twelve of fourteen combined their models. *(Ch9 §9.3.)* **Exact counts, from the raw responses, if pushed:** 36 of 37
data-scenario responses used exponential smoothing and 32 of 37 a seasonal
ARIMA; in the code-only scenarios (B, D) it is 18 of 18 and 17 of 18. Ch9's
"every one" rounds the seasonal-ARIMA count up by one — so lead with the
counts, not "every".

**Concede.** Quote the **count**, not the ratios (the ratios come from the run
records and are not in the thesis) — per brand the medians are
1.082, 0.991 and 0.825, so only one of three is genuinely centred on its
trailing mean. And it does not cover scenario A, which receives no history and
cannot anchor.

**Why this matters more than it looks.** It is the cheapest attack on the whole
SRQ4 result. If the strong baseline were echoing the last number, the comparison
would be measuring nothing.

## Q4 · "Did code execution win, or did fitting per brand win?"

**20s.** "The design cannot separate them, and we say so rather than choosing.
The agent fits a bespoke model to the exact series it is asked about; our
pipeline serves a slice of a model fitted across ninety-five brands. That is the
largest of four competing explanations and the cheapest to test — one training
run per brand would settle it."

**Then.** 36 of 37 data-scenario responses used exponential smoothing and 32 a
seasonal ARIMA (raw responses; Ch9 §9.3 rounds this to "every one") —
precisely the techniques our substrate lacks.

**Concede.** The grain choice was deliberate, not an oversight: a large
competition found cross-learning superior to series-by-series training at scale,
the panel gives under four years of monthly history per brand, one model per brand is not a
small-business memory budget, and it could not serve a brand with no history.

## Q5 · "Your memory budget is four gigabytes and your system uses 231 megabytes. Was the constraint real?"

**20s.** "It bound the selection space, not the final footprint. It excluded
transformer and locally hosted options before any of them was fitted, which is
the decision it existed to make. That the selected models then sat far below the
ceiling is a result, not a failure of the constraint."

**Then.** Peak fit memory 0.04 to 0.84 per cent of the 4096 MB budget across all
models. Serving stays under one megabyte for the deployed
models (XGBoost 0.65, LightGBM 0.07). ⚠ Ch8 and Ch9 say "below half a megabyte
for every model family"; the results table says 0.65 for XGBoost and 1.73 for
Prophet. Say "under a megabyte"; don't quote "half".

**Concede openly.** The budget did its work at design time. A thesis claiming it
was binding at run time would be contradicted by its own table.

---

# Part 2 — Questions the inherited file does not yet cover

## Q6 · "Scenario D is your most accurate rung. It is the code arm, in production. Doesn't that undercut you?"

**20s.** "It is the most accurate on the median, at 0.9 per cent, and it is the
code path — so it is an orchestrator effect on the comparator, not a point for
our artefact. It is also the reason we ran paired rungs at all: without D and E
we could not have told an orchestrator effect from a capability effect."

**Then.** D 0.9% median but 8.1% CV, $0.7664 and 111.3 s. E — the model on the
same orchestrator — is 14.6% median, 0.0% CV, $0.1994 and 31.7 s. The trade is
the same shape on both orchestrators, which is the structural finding.

**Concede.** D's mean is 25.0 against E's 13.1, so the median/mean split that
governs B-versus-C governs D-versus-E identically. That consistency across two
independently built systems is the strongest thing in the experiment.

## Q7 · "Chapter 8 is your contribution and it is the shortest substantive chapter. Why?"

**20s.** "The chapter reports a comparison whose design is specified in Chapter
3 and whose substrate is established in Chapter 5, so it deliberately does not
re-report either. What it carries is the ladder, the seven-scenario table, the
threats to validity and the cost analysis. We would rather it were longer on
interpretation, and Chapter 9 carries that instead."

**Concede.** Honest answer if pushed: the funded experiment completed late in
the project. The design and the controls were in place well before, and the
audit that caught the drifted capability notes happened before any funded run —
but the write-up had less time than the chapters around it.

## Q8 · "You generated 87 figures and cite two. Why is so little shown?"

**20s.** "Most of those are per-category exploratory plots and the appendix
tables, which are evidence rather than argument — they exist so a claim can be
checked, not so a reader has to walk through them. In hindsight the model
benchmark and the scenario comparison would each have carried a figure in the
body."

**Concede.** This is a presentation weakness, not an evidence weakness. Say so
directly; do not defend the ratio.

## Q9 · "Two of four categories lose to a parameter-free benchmark. Is your substrate worth anything?"

**20s.** "In two categories a seasonal naive or Prophet forecast is better, and
we report it rather than absorbing it. Both gradient boosters still beat Ridge
and ARIMA in every category, and those differences exceed the seed noise. What
the result actually tells a practitioner is to benchmark against free methods
before deploying a trained one — which is a finding, not an embarrassment."

**Then.** Seasonal naive 27.3 on RTD (our best 30.2); Prophet 19.4 on
Danskvand (ours 27.1). ⚠ On CSD we win, but narrowly: XGBoost 18.4 against
seasonal naive 19.2 — a 0.8-point gap, inside the 2.81-point seed variation.
If pressed: "on CSD the trained model and the free benchmark are effectively
tied." Don't claim a clear win there. Prophet also returns 975.0 on Energidrikke — its variance across
categories is enormous, which is itself the argument for selecting per category.

## Q10 · "Your thesis calls itself a bounded tool-using agent, not a multi-agent system. So what is agentic about it?"

**20s.** "Tool-mediated reasoning under a schema. The model decides when to
call, translates intent into typed parameters, and translates a structured
payload into a recommendation — but it holds a fixed tool set, delegates to no
other agent, and does not act on its own recommendation. We make that
correction ourselves because describing it otherwise would claim a coordination
contribution we did not make."

**Concede.** The boundedness is a design choice, and it is what keeps the system
auditable and inside the memory budget. A multi-agent decomposition is named as
future work.

## Q11 · "You report two different peak-memory figures in two chapters."

**20s.** "Two profiling runs at different dates that were not reconciled before
submission. The results artefact carries 34.5 for XGBoost, which is what Chapter
9 reports; Chapter 6's table is the earlier run. Neither changes anything — the
difference is 0.84 versus 0.78 per cent of a four-gigabyte budget."

**Concede.** Do not claim the difference is meaningful, and do not suggest it
was noticed before submission. It was not.

## Q12 · "You completed one design science cycle. Are your design principles worth anything?"

**20s.** "One cycle is what a thesis-scale study delivers, and we state that the
principles are derived rather than validated. What makes them more than
description is that each is stated at the level of a problem class and each
carries an evidence column — we assert them because something in the evaluation
would have come out differently had they not held. That makes them falsifiable
by the next cycle rather than just plausible."

## Q13 · "What did 'editorial support' in your AI declaration cover?"

**The likeliest compliance question. Answer plainly rather than standing on the
wording.**

**20s.** "Generative AI was used as a language assistant on the manuscript and
to discuss how arguments were organised and chapters sequenced. What to claim,
which evidence supports a claim, and how to interpret a result were our
decisions. Every empirical claim was verified against the artefact that produces
it before it entered the text."

⚠ **Do not deny drafting assistance.** The submitted repository carries its own
history. A denial is disprovable; the declaration as written is not.

**On the "specific reference" rule.** The guidelines separate assistance in
producing your own product — compared to Grammarly and to asking a mentor for
input, needing no per-passage reference — from generated content as a component
of the final product, which does. Drafting that we reviewed, revised and
verified is the first. State it as an interpretation if pressed; it is declared
in the front matter and in Section 3.8.

**On the data.** The licensed panel never reached an AI tool. It never leaves the
local environment and the repository has no copy. The only data reaching an
external model is the brand-level aggregates that form the documented inputs to
the Chapter 8 experiment — which were the object of the experiment and are
reproduced in the appendix.

---

# Part 3 — The methodology and SRQ2 questions

## Q14 · "How does the language model get the lag values?"

**20s.** "It does not, and must not. The model performs exactly two
translations: intent into typed parameters, and a structured payload into prose.
Feature construction happens server-side, where it is versioned and identical on
every call. The model never sees a feature vector."

**This is the SRQ2 contribution**, so the question is a gift rather than a
threat.

## Q15 · "Why function calling rather than letting the model write code?"

**20s.** "A schema-constrained call has one well-formed shape, and its arguments
can be checked against the request that produced it. Generated code is
re-derived on every invocation and is not guaranteed to be the same twice —
which is measurable and substantial."

**Concede.** Do not claim it is more accurate. The justification is reliability,
reproducibility and auditability. On the funded set the code-writing scenario was *more* accurate on the median
(2.9 against 14.6), and the argument survives that because it never rested on
accuracy.

## Q16 · "Your prediction intervals attain coverage but are enormous. Is that useful?"

*Corrected 2026-10-12: this answer previously said coverage holds everywhere and
cited "six orders of magnitude", which is not in the thesis.*

**20s.** "Not as a range on its own, and we say so. On the two largest categories
the interval hits its target — 91.7 and 91.4 per cent against ninety. On the two
smallest it falls short, because there are too few months to calibrate on. And
where it does hit the target it's around nine times the forecast — honest, but
too wide to plan with. That's why the tool also sends the model's past accuracy."
*(Ch5 §5.6.7; Ch9 DP3)*

**Then.** At 90%: CSD 91.7, RTD 91.4, Energidrikke 86.7, Danskvand 83.9.
Calibration quality tracks calibration-set size (Danskvand has 174 rows). Three
alternative schemes were implemented and none improved coverage and width
together in more than two of four categories.

⚠ **Known tension.** The abstract and Ch10 say the interval "attains its coverage
guarantee"; Ch5's table shows two categories missing it. If pressed: "the
guarantee is finite-sample, and it is met where the calibration set is large —
Chapter 5 reports the two misses as limitations." Don't claim it holds
everywhere.

## Q17 · "Your confidence index returns the same value for every brand. Why ship it?"

**20s.** "It is degenerate and the thesis says so. The forecast cancels out of
the relative width, leaving a function of the per-category quantile alone, and
the second term is identically zero. It returns one value per category, so it
discriminates nothing between brands. *(Ch7; Ch9 DP3)* It is retained only because published runs are scored against it."

**The unexpected defence.** In the combined scenarios both agents departed from
the model's forecast and cited its confidence tier and interval width as the
reason. A constant "low" was, on that brand, the honest signal — and it changed
behaviour. That is the uncertainty channel working through a broken index.

## Q18 · "If the model needs thirteen months of lag depth, how does it answer today?"

**20s.** "Warm-up is a training-time concept, not a runtime phase. It is the set
of rows at the start of each brand's series whose lag features point before the
data begins, so they cannot be training examples. At serving time the history is
already stored and the feature row is built from it directly."

**Concede.** The real serving constraint is **cold start**: a brand with too
little stored history cannot be forecast at all. That is a coverage limitation,
and the correct response is a typed refusal naming the brand rather than a
degraded forecast.

## Q19 · "Why three months ahead?"

*Corrected 2026-10-12: this question previously defended a one-month horizon,
which contradicts the thesis. The primary horizon is three months.*

**20s.** "Because a quarter is when the decisions this forecast supports are
actually taken — promotional plans and range changes are set per quarter. A
one-month forecast would be accurate and arrive too late to change anything."
*(Ch5 §5.4: "chosen because a quarter is the period over which the promotional
and range decisions this forecast supports are taken.")*

**Then.** The cost of the longer horizon is data: it needs two more months of
history per brand, so CSD keeps 95 brands at three months against 106 at one
(Ch4 §4.2.1). A one-month run exists as a secondary result.

## Q20 · "You compare models 'on identical data', but the categories differ."

**20s.** "Not entirely, and the asymmetry is real. The panel reports promotion
for two of four categories, because the source lacks the measures rather than
through a configuration gap. Where absent, the column is omitted and never
zero-filled — a constant-zero column would assert that no promotion ran. Panel
depth also differs by category."

**Concede.** This limits cross-category generalisation of any promotion-driven
finding, and the interval coverage differences track calibration-set size for
the same underlying reason.

## Q21 · "Is your cost figure measured or estimated?"

**20s.** "Total spend is measured — $19.60, the change in the account balance
across the two invocations that ran the experiment. Token counts come from the
provider's own usage object. The per-scenario figures are token estimates and
therefore upper bounds; the estimate overshot actual billing by about
twenty-nine per cent. The one genuine unknown is sandbox duration, which the API
does not expose to anyone."

---

## Q22 · "Does your model use last year's sales for the same month?"

*Added 2026-10-12. **Only if asked — do not volunteer.** Full account: P0056
findings F16.0 (plain) and F16.1 (technical).*

**20s.** "Not directly. The analysis found a yearly pattern, but the lag settings
never picked up the value from the same month last year. The model still knows
which month it's forecasting, through the calendar features, so seasonality isn't
missing — it's weaker than it could be. It's a limitation in Chapter 9, and fixing
it would make our model more accurate, so it doesn't change the conclusion."

**If pushed on the numbers.** Thirteen-month lag in the configuration; at the
three-month horizon it reaches fifteen months back. The year-ago value would need
a different lag at each horizon.

**Never.** Say "off by one month" (true only at one month ahead). Guess how much
accuracy it cost (never re-run). Claim it was noticed before submission.

---

# Part 4 — The one-line answers

Questions that need no more than a sentence.

| Q | Answer |
|---|---|
| Why not deep learning? | Excluded by delimitation on RAM, before any fit. Transformer forecasters need accelerator memory measured in tens of gigabytes. |
| Why four categories, not five? | Beer has 455 brands — an order of magnitude larger — and would have dominated both preprocessing and the memory budget. |
| Why monthly, not weekly? | The panel's grain at the market scope used, and it matches the tactical planning cycle. |
| Why no LLM-as-judge? | It would introduce non-determinism and a need for its own bias controls into a question arithmetic already answers. All measures are programmatic. |
| Why Prophet at all, given 975% on one category? | It is the best model on Danskvand at 19.4. The variance across categories is itself the argument for per-category selection. |
| Why cross-validation for selection? | Selecting on test is selection on the evaluation set, which biases every number downstream. |
| Who did what? | Be ready with a concrete, honest division. **The examiners must satisfy themselves you are both authors of the whole.** |
| Does the artefact run in production today? | No. Three of seven scenarios executed inside the production platform for evaluation; the remaining gap is operational — credentials and a merge — not architectural. |

---

# Before the room

| | |
|---|---|
| ⚠ | **GenAI in defence preparation:** CBS asks students to inform supervisor and censor. Whether the slide-4 disclosure and §3.8 cover it is your call; a draft email exists (R-1012-03) if you want it. |
| ⚠ | **No GenAI during the defence.** |
| | Print the deck for the examiners. |
| | Bring this file on paper. |
| | Read `anticipated-assessor-questions.md` in full the week before — this is the compression, not the substance. |
| | Rehearse the two handover slides out loud. Group defences stumble there. |
| | Agree who takes an unexpected question first, and the phrase that hands it over. |
