---
name: 2026-09-14_BRANCH_A_ch3-rewrite
description: NOTE - Chapter 3 rewritten against BRANCH A. It describes a study that was not run - an LLM judge in four places, fifty prompts in three, five categories in three, and a sequential-execution limitation the measurements refute. Full replacement prose for 3.3 to 3.7, resolving all 32 comment threads.
category: workflow
applies-to: [ch3_methodology]
triggers: [chapter 3, methodology, branch a, rewrite, llm judge, fifty prompts]
created: 2026_09_14-13_10
updated: 2026_09_14-13_10
snapshot: 2026-09-14_12-32_comment-sweep-and-archive
status: prose ready to paste, awaiting human review
---

# Chapter 3 — BRANCH A rewrite

Verified at `41ecb76`, fetch clean, origin and HEAD level. Snapshot
`2026-09-14_12-32_comment-sweep-and-archive` (47,593 words, 122 comments in 100
threads). Zotero re-pulled: **89 items**.

**Notes swept:** `srq4-data-input-is-a-constructed-choice.md` and
`verification-of-the-experimental-harness.md` — both **live, neither applied**,
both still relevant. They are design-rationale references rather than staged
prose, and they are left in place. `2026-09-14_appendix-citations-ch3.md` is
also live and explicitly **blocked on this rewrite**, so read it after this one,
not before.

---

# Why this is a rewrite and not a comment pass

**Chapter 3 carries 32 open threads — a third of every comment in the thesis**,
and they are not distributed. They cluster in §3.4 through §3.7, and they say the
same four things repeatedly because the chapter describes **a study that was not
run**.

| What the chapter says | What happened | Threads |
|---|---|---|
| "Scoring uses an LLM-as-judge protocol with a separate judge model" | **No judge exists.** Chapter 7 argues against one by design | 128, 132, 133, and §3.6 construct-validity |
| "approximately fifty decision-support prompts" | **One prompt**, 7 scenarios x 3 brands x 3 repeats = 63 runs | 125, 139 |
| "five Nielsen categories" / "five forecasting models" | **Four** categories; beer excluded. Six model families evaluated | §3.3, §3.4, §3.6 |
| "The four-gigabyte RAM budget requires models to be executed sequentially" | **Refuted by measurement.** Peak fit 31.9 MB; all four fit concurrently | 140 |
| "MAPE and RMSE as accuracy metrics" | **WMAPE primary**, median APE and MASE reported; MAPE is not the headline | 122 |
| "sandboxed environment (for example E2B) ... runnable locally" | E2B is **hosted**, instantiated per request via the API | 126, 127 |
| "March 2026" as the data cutoff | Data runs to **July 2026** | 117 |

A chapter that specifies a judge protocol the thesis spends Chapter 7 arguing
against is not stale in the way a number is stale. **It describes a different
research design**, and an examiner reading Chapter 3 then Chapter 8 meets two
studies.

⚠ **This is the same diagnosis Ch9 and Ch10 had**, and it needs the same
treatment. Nine of the twelve `OUTDATED` tags in the entire document are here.

---

# What is NOT rewritten

**§3.1 and §3.2 stand.** The pragmatist philosophy, the DSR framing, Hevner's
three cycles and Peffers' six activities are correct, well-sourced and unaffected
by what the experiment turned out to be. They take **four small fixes** (below),
not replacement.

That is worth saying plainly: **two of seven sections are sound, and the
chapter's foundations are not the problem.**

---

# Part 1 — the four small fixes to §3.1 and §3.2

## Fix 1 — 3.1, the pragmatism claim needs its source (threads 104, 105)

### Anchor

**Section 3.1**, first sentence: *"This thesis adopts a pragmatist philosophy of
science, a position that evaluates knowledge claims by their practical
consequences and their capacity to generate useful solutions to real-world
problems."*

### Action

REWORD — append the citation.

**After:**
> "This thesis adopts a pragmatist philosophy of science, a position that
> evaluates knowledge claims by their practical consequences and their capacity
> to generate useful solutions to real-world problems (Saunders et al., 2023)."

**And the second flagged sentence**, *"Consistent with this pragmatist
orientation, the thesis adopts a modest realism about the business realities it
studies"* — append the same citation at the end of that sentence.

### Note

Saunders et al. (2023) is **in Zotero** and is already cited in Ch2 and Ch4. It
is the CBS methodology text and it covers pragmatism directly, which is what
threads 104 and 105 ask for. **This also partly answers thread 97**, which asks
why Saunders is not cited alongside Hevner and Peffers in the DSR section.

## Fix 2 — 3.2, define IS on first use (thread 109)

### Anchor

**Section 3.2**: *"DSR is distinguished from purely behavioural IS research by
its dual emphasis..."*

### Action

REWORD — *"purely behavioural information systems (IS) research"*.

⚠ **Check whether IS appears earlier than this** in the chapter. If it does, the
definition belongs at that first occurrence instead.

## Fix 3 — 3.1 and 3.5, the parenthesis and colon patterns (threads 106, 107, 123, 124)

**These four threads are one request**, and it is a house-style matter rather
than a content one. You flagged: the `word:` construction, the `not incidental;`
construction, and two parenthetical asides in §3.5.

### The two §3.5 parentheticals, reworded

**Before:** *"a lightweight Python coordinator that passes typed state between
components; "LangGraph" is the intended production substrate (the Prometheus
production system, whose Graph Engine is the concrete integration target
examined under SRQ3), not the evaluated implementation."*

**After:**
> "a lightweight Python coordinator that passes typed state between components.
> The intended production substrate is the Prometheus production system, whose
> Graph Engine is the concrete integration target examined under SRQ3, rather
> than the implementation evaluated here."

**Before:** *"a real production-oriented agentic system (Prometheus, whose Graph
Engine is the concrete integration interface) as the empirical case"*

**After:**
> "a real production-oriented agentic system as the empirical case, namely
> Prometheus, whose Graph Engine is the concrete integration interface"

### Note — on the `word:` pattern

⚠ **I am not proposing a document-wide sweep.** You flagged it as something for
the watermark-removal repository, and a global find-and-replace on colons would
damage legitimate uses. The two §3.1 instances you marked are:

- *"the pragmatist criterion for success is not whether..."* — already reads
  without a colon
- *"is not incidental; it reflects the deliberate choice"* — → *"is not
  incidental, and reflects the deliberate choice"*

**Both are one-word edits. The systematic version is a separate task.**

## Fix 4 — 3.3, the CBS guidelines sentence (thread 112)

### Anchor

**Section 3.3**, final paragraph: *"The CBS case study guidelines apply to this
research, and the Nielsen data are used under a confidentiality agreement with
Manifold AI, as documented in Chapter 4."*

### Action

REWORD — delete the first clause.

**After:**
> "The Nielsen data are used under a confidentiality agreement with Manifold AI,
> as documented in Chapter 4."

### Note

You are right that citing institutional formatting guidance is not academic
practice, and the clause carries no methodological content — the case-study
design is already justified in the preceding paragraphs from Saunders. **Deleting
it costs nothing.**

---

# Part 2 — the rewritten sections

## Fix 5 — 3.3, the research strategy (five categories, the unit of analysis)

### Anchor

**Section 3.3 Research Strategy**, the **second and third paragraphs**, from
*"The single-case embedded study component provides the organisational
context..."* through *"...to prevent retroactive revision based on observed model
performance."*

### Action

REPLACE both paragraphs.

#### Replace with

> The single-case embedded study component provides the organisational context
> that grounds the experimental findings in a real application environment.
> Manifold AI serves as the case organisation, its production-oriented agentic
> system serves as the empirical case for the integration-readiness assessment in
> SRQ3, and the Danish beverage retail market across four Nielsen categories
> constitutes the empirical context. The case study orientation means that all
> experimental data, evaluation protocols and baseline comparisons are anchored
> in the actual data and operational context of the case rather than in synthetic
> benchmarks. This design choice reflects the design-science relevance criterion:
> an artefact must be evaluated in a context relevant to the problem it
> addresses. The Nielsen data are used under a confidentiality agreement with
> Manifold AI, as documented in Chapter 4.
>
> The unit of analysis is the predictive-extension artefact, evaluated on the
> Nielsen panel across four Danish beverage categories at brand-and-month
> granularity. A fifth category, beer, is available in the source and is excluded
> before any modelling: its panel is structurally unlike the other four, and the
> exclusion is recorded here rather than presented as an absence. The granularity
> choice reflects the operational planning horizon relevant to Manifold AI's
> client organisations and the temporal resolution at which the panel is
> reported. The default market definition, DVH EXCL. HD, is Nielsen's own
> recommended default and the scope on which Manifold AI reports; it denotes
> Danish grocery retail excluding the hard-discount channel, which is
> structurally different in assortment and pricing and would otherwise be pooled
> with it. These choices are documented as design decisions fixed before
> analysis, so that they cannot be revised retroactively in the light of observed
> model performance.

### Note — what changed, thread by thread

| Thread | Resolution |
|---|---|
| §3.3 "five Nielsen categories" | **four**, with the beer exclusion stated — also answers **thread 115** |
| **113** — explain DVH EXCL. HD | one clause, from the Nielsen metadata: grocery retail excluding hard discount, and *why* that matters |
| **112** — CBS guidelines | the clause is gone (Fix 4) |

⚠ **"brand-times-retailer granularity" was wrong and is now "brand-and-month".**
The chain grain was deleted in August under DEC-GRAIN. This is a factual
correction beyond the comments, and it is the kind an examiner would catch by
comparing Chapter 3 against Chapter 4.

---

## Fix 6 — 3.4, the data source section

### Anchor

**Section 3.4 Data Sources**, the **entire section**, both paragraphs, from
*"This thesis uses one data source"* to *"...which is itself a Saunders-listed
advantage of using secondary data."*

### Action

REPLACE.

#### Replace with

> This thesis uses one data source: the Nielsen beverage scanner panel, which is
> the forecasting input for every category studied.
>
> The panel provides longitudinal retail transaction data for Danish beverage
> categories, of which four are used here: carbonated soft drinks, still and
> sparkling water, energy drinks, and ready-to-drink beverages. A fifth, beer, is
> present in the source and excluded, for the reasons given in Chapter 4. Its
> structure follows a star schema, with a facts table recording sales value,
> sales in litres, sales units and a weighted-distribution measure at the
> brand-by-market-by-period level, linked to dimension tables for market, period
> and product. The panel is updated monthly and provides between forty-one and
> forty-six monthly periods per category, ending in July 2026, giving a
> transaction history of roughly three and a half to four years. The sales
> metrics include both base and promotional variants, which is what makes a
> promotional-intensity feature constructible where the category reports one. The
> weighted-distribution measure proxies product availability as a share of
> category volume rather than counting shelf presence directly, and its status as
> a proxy is carried into how it is used. The data are commercial and are not
> redistributed: they remain in the local research environment and are not
> published with this thesis. Because access is commercial and restricted, the
> data could not have been collected independently within the scope of a thesis,
> which is itself a recognised advantage of secondary data (Saunders et al.,
> 2023).

### Note — the four threads this closes

| Thread | Resolution |
|---|---|
| **115** — why was beer removed | stated, with a forward reference to Ch4 rather than repeating the reason |
| **117** — "March 2026" is wrong | now **July 2026**, and the monthly-update property is stated |
| **116** — star schema appendix image | **deferred, see below** |
| **118** — feature descriptions from the metadata | partly addressed: the two measures are now described by what they are |

⚠ **"37 to 42 monthly periods" was also wrong** and is corrected to 41–46,
matching Chapter 4's measured spans. The old figure appears again in §3.7 and is
corrected there too (Fix 9).

### Note — threads 116 and 118, the appendix requests

Both ask for generated artefacts: a star-schema diagram and a condensed data
dictionary spanning the four categories.

**Neither is written here**, because both are artefact-generation tasks rather
than prose, and `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`
is where they belong. ⚠ **A star-schema figure already exists** —
`ch4_raw_schema_v1.svg`, rendered 2026-09-10 — and Chapter 4 already says *"A
visualization of the star schema can be found in Appendix A."* **So thread 116
may already be satisfied by an existing figure**; what it needs is a
cross-reference from Chapter 3, not a new diagram. **NEEDS-BRIAN** — confirm the
existing figure is the one you meant.

---

## Fix 7 — 3.5, the analytical approach (the largest single replacement)

### Anchor

**Section 3.5 Analytical Approach.** Replace the **SRQ1 paragraph** and the
**SRQ4 paragraph**. The SRQ2 and SRQ3 paragraphs take smaller edits, given
separately as Fix 8.

The SRQ1 paragraph begins *"**SRQ1** **-** **forecasting accuracy and
computational efficiency.** Five forecasting models are evaluated..."* and ends
*"...the RSS measurements are reported in Chapter 6."*

The SRQ4 paragraph begins *"**SRQ4** **-** **dedicated-model integration versus
a code-as-action LLM.**"* and ends *"...are identified as further work."*

### Action

REPLACE both.

#### Replace with — SRQ1

> **SRQ1, forecasting accuracy and computational efficiency.** Six model
> families are evaluated across the four Nielsen beverage categories, spanning
> the inductive biases most relevant to the problem: ARIMA and Prophet as
> classical statistical methods, LightGBM and XGBoost as gradient-boosted
> ensembles, Ridge regression as a regularised linear baseline, and a set of
> parameter-free benchmarks including the naive and seasonal-naive forecasts.
> Exponential smoothing is a deliberate omission and is recorded as a limitation
> of the comparison rather than as a judgement on the family. Hyperparameters for
> the gradient-boosted models are tuned with Optuna, which implements the
> tree-structured Parzen estimator for sequential model-based optimisation
> (Akiba et al., 2019), against an expanding-window cross-validation objective
> that never observes the test split. Models are evaluated on a common held-out
> test set. Weighted mean absolute percentage error is the primary accuracy
> metric, reported alongside median absolute percentage error and the mean
> absolute scaled error, with the choice of primary metric derived in Chapter 5
> from the scoring-function argument rather than adopted by convention. Peak
> resident set size and runtime serve as efficiency metrics and the coefficient
> of variation across repeated runs as a stability metric, following Klee and Xia
> (2025). The benchmark additionally tests whether category-specialised models
> outperform a single pooled model trained across categories. Memory profiling
> measures process resident set size through the operating system rather than
> Python-level allocation tracking alone, because the latter does not capture the
> native allocations of the gradient-boosted implementations.

#### Replace with — SRQ4

> **SRQ4, dedicated-model integration versus code execution.** SRQ4 concerns
> whether integrating dedicated lightweight forecasting models into the agentic
> system is warranted at all, or whether a general-purpose language model that
> writes and executes its own forecasting code is already sufficient. The
> comparison is structured as a ladder of seven scenarios rather than as a
> two-way contrast, so that the value of data access and the value of the
> dedicated model can be attributed separately: a scenario with no access to firm
> data, scenarios given the brand's history in a code-execution sandbox,
> scenarios given the same data behind a typed tool, and scenarios given both.
> Three of the seven run inside the production agentic platform rather than the
> hosted coordinator, which pairs them column-wise with their counterparts and
> makes the orchestrator the only difference between each pair. Every scenario is
> asked an identical question, and consistency is measured by repetition of that
> identical question rather than by breadth of prompt coverage, because
> run-to-run variation is itself one of the properties under test. Code execution
> is performed in a hosted sandbox instantiated per request through the model
> provider's API, which is also the pattern the production system uses, so no
> component runs on local infrastructure. Outputs are scored on correctness,
> consistency and replicability as primary dimensions and on cost and latency as
> secondary ones. Consistency is measured over repeated runs because generated
> code varies substantially across identical requests even at nominally
> deterministic settings (Ouyang et al., 2025; Atıl et al., 2025); cost and
> latency are treated as evaluation dimensions in their own right, following the
> argument that computational cost belongs among a system's first-class
> evaluation criteria (Schwartz et al., 2020) and the evidence that inference
> cost differs by orders of magnitude across models of comparable quality (Chen
> et al., 2024); the overall multidimensional frame follows Mehta (2025). All
> scoring is arithmetic. Numbers stated in an answer are extracted and compared
> against the payload the tool returned, and no language model judges any output,
> for reasons set out in Chapter 7.

### Note — the seven threads this closes

| Thread | Resolution |
|---|---|
| **120** — sources for the model claims | the five families are now characterised by inductive bias, which is Chapter 5's own framing, and the claim about memory footprints is dropped rather than left unsourced |
| **121** — Optuna needs a citation | **Akiba et al. (2019)** ⚠ see the citation note below |
| **122** — we track median APE too, needs a source | WMAPE, median APE and MASE are all named; the *derivation* is pointed at Ch5 §5.4.1 rather than asserted here |
| **125, 139** — fifty prompts | **gone.** One identical question, with repetition as the design |
| **126, 127** — E2B and "runnable locally" | now "a hosted sandbox instantiated per request through the model provider's API", which is what actually happens |
| **128, 132, 133** — no LLM judge | **"All scoring is arithmetic. No language model judges any output."** |
| **130** — stratified brand evaluation | the three-brand stratification is Chapter 8's; §3.6 now carries it (Fix 8) |

### ✅ Citation verified — Optuna

**Akiba et al. (2019), "Optuna: A Next-generation Hyperparameter Optimization
Framework", is IN the Zotero library** — `conferencePaper`, dated 25 July 2019,
five authors (Akiba, Sano, Yanase, Ohta, Koyama). Verified 2026-09-14 by querying
the group library API directly, unfiltered, across all 89 items.

⚠ **An earlier draft of this note flagged it as unverified. That was my error**,
not a library gap: I searched a derived export with a term that did not match,
rather than querying the API. The citation is safe to paste.

---

## Fix 8 — 3.5 SRQ2/SRQ3 and 3.6, the judge protocol's last traces

### 8a — SRQ2, the calibration claim

**Anchor:** *"receives point forecasts accompanied by interval information,
prediction intervals following Kuleshov et al. (2018). That said, interval
calibration is a design target, not an empirically validated property of the
current prototype"*

**Action:** REWORD.

> "receives point forecasts accompanied by a prediction interval constructed by
> split conformal calibration on held-out residuals (Lei et al., 2018). Interval
> coverage is measured rather than assumed, and Chapter 5 reports both the
> coverage attained and the width at which it is attained."

⚠ **This is a substantive correction.** The interval is **split conformal (Lei et
al., 2018)**, which is what Chapter 7 cites, not the Kuleshov recalibration
method. And calibration is **no longer** "not empirically validated" — it is
measured in Ch5 Table 13. Both halves of the sentence were false.

✅ **Lei et al. (2018), "Distribution-Free Predictive Inference for Regression",
is in the library** — `journalArticle`, 2018-07-03. Verified against the API.

⚠ **Kuleshov et al. (2018) is also in the library** and is cited nowhere else in
the thesis after this change. That is fine — an unused library entry costs
nothing — but do not re-add it here on the assumption it belongs.

### 8b — 3.6, construct validity

**Anchor:** *"and the correctness, consistency, replicability, cost, and latency
dimensions, scored via an LLM-as-judge protocol with a human-rated subset, for
SRQ4."*

**Action:** REWORD → *"and the correctness, consistency, replicability, cost and
latency dimensions, scored by arithmetic comparison against the tool payload, for
SRQ4."*

### 8c — 3.6, reliability

**Anchor:** the sentence beginning *"The LLM-as-judge evaluation introduces a
source of non-determinism"* through *"...enabling retrospective auditing."*

**Action:** REPLACE.

> "Language-model non-determinism is a property of the object under study rather
> than of the evaluation instrument: outputs at temperature zero are highly
> reproducible but not guaranteed to be identical across provider versions, which
> is precisely why consistency is measured over repeated runs rather than
> assumed. Every call is logged with its exact prompt and output, and the prompt
> set is identified by a hash computed over every string that reaches the model,
> so that runs may be pooled only when they carry the same identifier."

### 8d — 3.6, internal validity, the third design choice

**Anchor:** *"Third, the controlled comparison used for SRQ4, in which the
decision-support pipeline (dedicated-model integration versus the code-as-action
baseline) is the sole manipulation while the prompt set and inputs remain
constant, isolates the contribution of dedicated-model integration from potential
confounders."*

**Action:** REPLACE.

> "Third, the SRQ4 comparison varies one thing at a time. The scenario ladder is
> the sole manipulation, the question and its output instructions are identical
> across every scenario, and the brands are stratified by volume rather than
> chosen, so that differences are attributable to the scenario rather than to
> which brands it happened to draw. Three brands spanning three orders of
> magnitude of volume are used, which is a deliberate bound on what the
> comparison can establish and is stated as such in Chapter 8."

### 8e — 3.6, external validity

**Anchor:** *"The findings of this thesis are applicable to the Danish beverage
retail market (the five Nielsen categories) under an four-gigabyte RAM cloud
deployment constraint and a monthly batch processing mode."*

**Action:** REWORD.

> "The findings of this thesis are applicable to the Danish beverage retail
> market across four Nielsen categories, under a four-gigabyte memory budget and
> a monthly planning cycle, which is the cadence at which the panel is reported
> and at which the decisions it supports are taken."

### Note — threads closed by Fix 8

**128, 130, 131, 132, 133**, plus the "five categories" and "an four-gigabyte"
typo. ⚠ **Thread 131** asked what "monthly batch processing mode" means — the
reword answers it: the panel is monthly, so the planning cycle is monthly.

---

## Fix 9 — 3.7, the limitations (two are false as written)

### Anchor

**Section 3.7 Limitations.** Replace the **Training sample size**, **Pilot-scale
evaluation** and **Sequential model execution** paragraphs. The **Data
confidentiality** and **Case study generalisability** paragraphs stand unchanged.

### Action

REPLACE the three named paragraphs; also change the opening line from *"five
limitations"* to **"four limitations"**.

#### Replace with

> **Training sample size.** Between forty-one and forty-six monthly periods per
> category is a short series for time-series estimation, and it bounds what the
> classical baselines can identify: a seasonal term requires several complete
> annual cycles to estimate stably, and this panel provides between three and
> four. The gradient-boosted models are less sensitive to series length because
> they pool across brands within a category, but the restricted window still
> limits their ability to learn effects with a cycle longer than a year. The
> retention rule applied in Chapter 4 follows from the feature specification
> rather than from a conventional minimum, and is the mechanism by which series
> too short to support the feature set are excluded rather than modelled poorly.
>
> **Scale of the scenario evaluation.** The SRQ4 comparison runs seven scenarios
> over three brands with three repeats each, for sixty-three runs in total. It is
> sized to detect differences between scenarios that are large relative to the
> variation within them, and not to establish that a result generalises across
> categories. Findings on correctness, consistency, replicability, cost and
> latency are therefore bounded to this design, and a wider evaluation across
> categories and repeats is identified as further work in Chapter 10.
>
> **Memory budget.** The four-gigabyte memory budget bound the selection of model
> families before any of them was fitted, excluding transformer-based and locally
> hosted architectures on grounds of footprint alone. It did not bind at run
> time: the measured peak for fitting is a small fraction of the budget and the
> serving footprint smaller still, so the models could be executed concurrently
> rather than sequentially. The constraint did its work at design time, and
> reporting the realised footprint is what allows a reader to see that.

### Note — the three threads, and one correction beyond them

| Thread | Resolution |
|---|---|
| **135** — "ARIMA requires 24 periods", needs a source | ⚠ **The claim is removed rather than sourced.** See below |
| **137** — LightGBM/XGBoost sample-size claim, needs a source | reworded to the mechanism (*pooling across brands*), which is a fact about the implementation and needs no source |
| **139** — "fifty prompts" | gone; the paragraph now states the actual design |
| **140** — sequential execution is INCORRECT | ⚠ **You are right, and the limitation is inverted.** See below |

### ⚠ Why the 24-period claim is deleted rather than cited

Thread 135 asks for a source for *"ARIMA models generally require a minimum of 24
periods for stable parameter identification."*

**There is no good source, because the claim is of a kind the literature
explicitly rejects.** Hyndman & Athanasopoulos (2021) §13.7 calls minimum-sample
rules of thumb *"misleading and unsubstantiated in theory or practice"*, and
names the magic number 30 specifically. Citing a source for a 24-period rule
would cite against the standard reference.

**So the paragraph now argues from what actually constrains estimation here** —
annual cycles available for a seasonal term — which is true, checkable, and needs
no rule of thumb. **Chapter 4 makes the same move**, and its retention rule is
derived from the feature specification rather than from a threshold.

### ⚠ The sequential-execution limitation was backwards

Thread 140 says the constraint is *"not really the case"*, and the measurements
agree: peak fit memory is 31.9 MB against a 4,096 MB budget.

**The old paragraph claimed a binding run-time constraint that the thesis's own
profiling refutes** — and it is the kind of claim an examiner checks, because
Chapter 5 §5.5.6 reports the measurement two chapters later.

The replacement states the honest and more interesting version: **the budget
bound the selection space, not the run time.** That is the same framing Ch9 and
Ch10 now use, so the three chapters agree.

---

# Part 3 — threads that need no prose

| Thread | Verdict |
|---|---|
| **102** — chapter could use a subtitle | **NEEDS-BRIAN.** Suggestion: *How the artefact was built, and how it was judged* |
| **110** — submission-ready repository | **FLAGGED**, not a prose item. The `/submission-export` skill exists for this; it is a task, not a sentence |
| **136** — quote model names consistently | **NEEDS-BRIAN, document-wide.** §3.5 currently quotes `"ARIMA"`, `"LightGBM"` and so on; my replacement prose does **not** quote them, matching Chapters 4, 5 and 8. **The chapter should be internally consistent either way, and the rest of the thesis is unquoted** — so I recommend dropping the quotes here rather than adding them elsewhere |
| **138** — add a holiday calendar | ✅ **DONE.** The holiday features are in the model: `n_holidays`, `days_in_month`, `non_holiday_days`. This thread predates that work and can be resolved as **VERIFIED-OK** |
| **116, 118** — appendix artefacts | **deferred** to the appendix audit; see Fix 6's note |

---

# Comment ledger — all 32 threads

| Thread, by content | Verdict |
|---|---|
| 102, subtitle | **NEEDS-BRIAN** |
| 104, 105, pragmatism sources | **ADDRESSED** — Fix 1 |
| 106, 107, colon and semicolon patterns | **ADDRESSED** — Fix 3 |
| 109, define IS | **ADDRESSED** — Fix 2 |
| 110, submission repository | **FLAGGED** — a task, not prose |
| 112, CBS guidelines | **ADDRESSED** — Fix 4 |
| 113, explain DVH EXCL. HD | **ADDRESSED** — Fix 5 |
| 115, why beer was removed | **ADDRESSED** — Fixes 5, 6 |
| 116, star-schema image | **NEEDS-BRIAN** — a figure may already exist |
| 117, March 2026 | **ADDRESSED** — Fix 6, now July 2026 |
| 118, data dictionary appendix | **DEFERRED** — appendix audit |
| 120, model claim sources | **ADDRESSED** — Fix 7, claim reframed |
| 121, Optuna citation | **ADDRESSED** — Fix 7 ⚠ verify Akiba in Zotero |
| 122, median APE and metrics source | **ADDRESSED** — Fix 7 |
| 123, 124, parentheses | **ADDRESSED** — Fix 3 |
| 125, 139, fifty prompts | **ADDRESSED** — Fixes 7, 9 |
| 126, 127, E2B and local execution | **ADDRESSED** — Fix 7 |
| 128, 132, 133, LLM judge | **ADDRESSED** — Fixes 7, 8b, 8c |
| 130, stratified brands | **ADDRESSED** — Fix 8d |
| 131, monthly batch mode | **ADDRESSED** — Fix 8e |
| 135, 24-period claim | **ADDRESSED** — Fix 9, claim removed |
| 136, quoting model names | **NEEDS-BRIAN** — document-wide style |
| 137, LightGBM sample size | **ADDRESSED** — Fix 9 |
| 138, holiday calendar | **VERIFIED-OK** — already implemented |
| 140, sequential execution | **ADDRESSED** — Fix 9, limitation inverted |

**32 of 32 accounted for. 24 addressed in prose, 4 need your decision, 2
deferred, 1 flagged as a task, 1 verified already done.**

---

# Citations register

**All three verified 2026-09-14 against the Zotero group-library API,
unfiltered, 89 items. None carries verification debt.**

| Source | Type in library | Used for |
|---|---|---|
| Saunders et al. (2023), *Research Methods for Business Students* | `book`, March 2023 ✓ | pragmatism (Fix 1), secondary-data advantage (Fix 6) |
| Lei et al. (2018), *Distribution-Free Predictive Inference for Regression* | `journalArticle`, 2018-07-03 ✓ | split conformal interval (Fix 8a) |
| Akiba et al. (2019), *Optuna: A Next-generation Hyperparameter Optimization Framework* | `conferencePaper`, 2019-07-25 ✓ | Optuna (Fix 7) |

**Klee and Xia (2025)** is also present (`conferencePaper`, 2025-07-30) and is
already cited in the existing §3.5 — the replacement keeps it.

⚠ **Query the API, not `citations.json`, when checking a source.** The derived
export filters by item type, and a search term that does not match a title field
returns a false negative either way. All three of these were confirmed by
searching title, creators and publication fields across every item.
