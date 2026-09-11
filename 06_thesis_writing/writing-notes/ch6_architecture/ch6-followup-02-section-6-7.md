---
name: ch6-followup-02-section-6-7
description: NOTE - Section 6.7 rewritten against the experiment session's updates, plus the four other remaining threads and three new citations. Read after applying the consolidated pass, which is otherwise done.
snapshot: 2026-09-11_20-08_ch6-prose-start
category: workflow
applies-to: [ch6-architecture]
created: 2026_09_11-20_25
updated: 2026_09_11-20_25
status: ready
---

# Section 6.7, and the last five threads

**Verified at `6ccdcc7`**, fetch clean. Snapshot `2026-09-11_20-08_ch6-prose-start`.
Zotero re-pulled 20:08: **89 items**, author and date checked against the
unfiltered API rather than the export.

**You applied nearly the whole consolidated pass.** Seventeen threads down to
six, chapter up 377 words to 2,553. Every Fix landed and landed correctly, which
I checked rather than assumed.

| In the consolidated pass | Status |
|---|---|
| Fixes 1-3a, 3c, 4-13, 15-17 | **applied.** Verified in the snapshot |
| Fix 3b, "human oversight" | ⚠ **not applied.** F7 below - now the only surviving overclaim |
| Fix 14, Section 6.7 | **written below** - F1 |
| Fix 13's cost note | ⚠ **partly retracted.** See F5. I told you cost under-reports by 1.77x. That was wrong |

Everything else in the consolidated pass stands and needs no revisiting.

---

# F1 - Section 6.7, rewritten

This answers threads **295** (*"name each scenario and map it to the respective
set-up"*) and **296** (*"'locally' is a bit deceiving"*).

### Anchor

**Section 6.7 The Code-as-Action Baseline (SRQ4)** - the whole section, both
paragraphs. It starts:

> "To evaluate whether dedicated-model integration is warranted at all, the
> architecture includes a **code-as-action baseline**:"

and ends:

> "...are specified in Chapter 3 and applied in Chapter 8."

### Action

REPLACE the entire section, heading included.

#### Replace with

> ## 6.7 The Scenario Ladder (SRQ4)
>
> Whether dedicated-model integration is warranted at all is an empirical
> question, and the architecture is built so that it can be asked. The comparison
> is not a contest between the artefact and a single alternative but a ladder of
> seven scenarios, each adding one capability to the one below it, so that the
> increments can be attributed separately. Every scenario answers the same
> question about the same brand and month, from the same history, using the same
> underlying language model; what differs between adjacent rungs is one thing.
>
> | | Scenario | What it is given |
> |---|---|---|
> | A | plain language model | no firm data; web search only |
> | B | code-as-action | the brand's history in an execution sandbox, where it writes and runs its own forecasting code |
> | C | dedicated model | the same history behind the structured forecast tool; it writes no code |
> | D | code-as-action, in production | scenario B, orchestrated by the production agentic platform |
> | E | dedicated model, in production | scenario C, orchestrated by the production agentic platform |
> | F | combined | both the execution sandbox and the forecast tool |
> | G | combined, in production | scenario F, orchestrated by the production agentic platform |
>
> **Table 19 - The Seven Evaluation Scenarios**
>
> The ladder is read in two directions. Reading up from A, the step to B measures
> what access to the firm's own data buys, and the step from B to C measures what
> replacing self-written code with a dedicated model adds; that second increment
> is the thesis contribution, and a two-scenario design would confound it with the
> first. Reading across, D, E and G repeat B, C and F on the production
> orchestrator, so that an effect observed on the lightweight coordinator can be
> checked for survival in the deployment environment rather than assumed to
> transfer.
>
> The code-writing scenarios instantiate the code-as-action pattern (Wang et al.,
> 2024): the language model is given the history and an execution sandbox, and
> writes, runs and self-corrects its own analysis without a pre-built model. They
> use the same base language model as the artefact, so that the comparison
> isolates the effect of dedicated-model integration rather than differences in
> model quality. In the combined scenarios the model's forecast is supplied as one
> input among several rather than as a starting figure to be revised, because an
> agent handed a number and permitted to keep it will usually keep it, and the
> design would then measure deference rather than integration.
>
> No part of the comparison requires access to the production system's own data or
> deployment. What is held locally is the code that assembles the history and
> issues the prompts; the language model and its execution sandbox are reached as
> hosted services, and the sandbox is created per request, so it is charged only
> when a query is actually made. The comparison is therefore feasible
> independently of integration access, which is what makes it runnable at all. Its
> protocol and metrics, with correctness, consistency and replicability as primary
> dimensions and cost and latency as secondary, follow the multidimensional frame
> of Mehta (2025), and are specified in Chapter 3 and applied in Chapter 8.

### Note - four things this fixes

| | |
|---|---|
| **E2B** | gone. The harness uses a hosted execution sandbox, and E2B appears nowhere in it |
| **"baseline"** | gone from the heading and the body. With seven rungs every arm is a comparator for the one below, so a single baseline is the wrong frame |
| **"locally"** | replaced by what is actually true: no *production* access is needed, and the language model is hosted |
| **the enumeration** | thread 295 answered - every scenario named and mapped |

### Note - the table introduces a new number

**Table 19** is new and renumbers nothing, because the chapter's last table is 18.
⚠ Plain-text table callouts do not renumber automatically the way Word field
references do, so if a table is later inserted before this one, this reference
needs updating by hand.

### Note - what I deliberately did NOT write

⚠ **No result.** Not the pilot numbers, not the accuracy ordering, nothing about
which arm won. The section describes a **design**, and nothing from the
experiment is funded yet. The pilot's within-arm spread is comparable to its
between-arm gaps, so any ranking read off it is noise.

⚠ **No scenario letters in Section 6.5.** The consolidated pass deliberately kept
them out of the delegation paragraph, and that still holds - Section 6.7 is the
one place the enumeration lives.

---

# F2 - Section 6.7 must declare the study's scope, per DEC-MVP-DESIGN

**This is new, from the experiment session, and it is an obligation rather than
an improvement.**

The funded design is **three CSD brands, one category**, and the decision record
is explicit that this is *"declared as a single-category study in BOTH the design
section and limitations - not only in limitations."*

**Chapter 6 is the design section.** Declaring a scope limitation only in Chapter
10 is the pattern an examiner reads as burying it.

### Action

INSERT AFTER - one paragraph, appended to the end of Section 6.7 as rewritten in
F1, after *"...specified in Chapter 3 and applied in Chapter 8."*

#### Replace with

> The comparison is deliberately narrow. It is run on three brands drawn from a
> single category, chosen to span three orders of magnitude of sales volume, with
> every scenario answering for the same three brands so that differences are
> attributable to the scenario rather than to which brands it happened to draw. A
> design of this size cannot establish that a result generalises across
> categories, and it is not offered as doing so; it is sized to detect
> differences between scenarios that are large relative to the variation within
> them, which is what the ladder is built to expose.

### Note - why this belongs in Chapter 6 and not only Chapter 10

Because it is a **design decision with a reason**, not an apology. The narrowness
buys the paired-brand property, which is what makes seven arms comparable at all
at this sample size. Stated in the design chapter it reads as a choice; stated
only in limitations it reads as a shortfall.

⚠ **The volume-span clause is load-bearing and must not be dropped.** The
brands span 6,365,900 to 2,850 units per month. A finding that held only at one
volume would be a different and much weaker claim.

⚠ **Do not justify the brand selection on "hard to forecast" grounds.** That
would be outcome-based selection and an examiner would be right to object. The
criterion is volume coverage and a meaningful error metric, both fixed in
advance.

---

# F3 - Thread 284, the five-model claim in Section 6.3

Your `VERIFY` on: *"The substrate comprises lightweight models spanning the
accuracy-efficiency frontier: ARIMA, Prophet, LightGBM, XGBoost, and Ridge
Regression."*

**The five models verify.** All five are evaluated in
`09_statistical_baselines`, alongside three naive baselines. **The framing does
not.**

⚠ *"Spanning the accuracy-efficiency frontier"* asserts that each model sits on a
frontier, trading accuracy against cost. **Prophet does not.** It records a
weighted MAPE of 105.7 on CSD and 975.0 on energidrikke - not a different
trade-off, simply worse. A model that is dominated on both axes is not on a
frontier.

Chapter 5 already has the honest framing: *"Five model families were selected to
cover the inductive biases most relevant to this problem."*

### Anchor

**Section 6.3**, first sentence - note you have **already corrected "five" to
"four"** here, so quote it as it now stands:

> "The substrate comprises lightweight models spanning the accuracy-efficiency
> frontier: ARIMA, Prophet, LightGBM, XGBoost, and Ridge Regression, evaluated
> across the four beverage categories"

### Action

REWORD - the clause up to "evaluated"; the rest of the sentence stays.

#### Replace with

> The substrate comprises five lightweight model families, selected to cover the
> inductive biases most relevant to monthly retail demand: ARIMA and Prophet as
> classical statistical methods, LightGBM and XGBoost as gradient-boosted
> ensembles, and Ridge regression as a regularised linear baseline. They are
> evaluated across the four beverage categories

### Note - "five categories" is fully cleared

✅ Checked the whole chapter: **no occurrence of "five categories" or "five
beverage categories" remains.** All three sites are fixed.

---

# F4 - Thread 287, the determinism claim, and a citation that supports it

Your `VERIFY` on the JSON function-calling paragraph.

**It verifies, and it can now be supported rather than asserted.** The claim that
a schema-constrained interface yields deterministic tool calls is currently made
on its own authority. There is a source in the library that measures the problem
it solves.

### Anchor

**Section 6.4**, the paragraph:

> "The artefact deliberately adopts JSON function-calling, rather than
> code-as-action, for **reliability and reproducibility**: the schema-constrained
> interface yields deterministic, auditable tool calls."

### Action

REWORD that sentence; the rest of the paragraph is unchanged.

#### Replace with

> The artefact deliberately adopts JSON function-calling rather than
> code-as-action, for **reliability and reproducibility**: a schema-constrained
> call has one well-formed shape and its arguments can be checked against the
> request that produced it, whereas generated code must be re-derived on every
> invocation and is not guaranteed to be the same twice. Non-determinism in
> language-model code generation is measurable and substantial (Ouyang et al.,
> 2025), which is why the property is designed for rather than assumed.

### Note - the citation, verified

**Ouyang, Zhang & Harman (2025), "An Empirical Study of the Non-Determinism of
ChatGPT in Code Generation"**, Zotero key `AMB2F6T2`, confirmed present with
authors and date against the unfiltered API.

It is the right source for exactly this claim: it measures that the same prompt
produces different code across runs, which is the failure the typed interface
avoids. **It does not claim function-calling is better** - it establishes the
problem, and the architecture's response is ours to argue.

⚠ **Register it** in `citations-added-register.md` with the sentence above as the
claim it supports.

---

# F5 - CORRECTION to my Fix 13 note: cost does NOT under-report

⚠ **I told you the per-run cost estimate under-reports by 1.20x to 1.77x, and
that the honest wording was "reconciled against billing". The first half was
wrong**, and the experiment session found the error the same evening.

**The costs endpoint buckets by whole day, organisation-wide, regardless of the
window requested.** Every "billed" figure the project has compared against was
therefore the whole day's spend including other sessions, failed runs and
pre-flight checks. Comparing one run's estimate against that measures how much
else ran that day.

**The like-for-like comparison, all of 2026-09-11:**

| | |
|---|---|
| sum of estimated runs | $4.86 |
| whole day, billed, org-wide | $4.03 |

**The estimate is conservative by roughly 17 per cent**, not under-reporting. And
the day contains traffic the estimates do not cover, so the true margin is wider.

**What was genuinely wrong and is now fixed:** web search was unpriced. Scenario
A was the only arm that searches, and its calls contributed nothing to the
estimate. `PRICE_WEB_SEARCH_CALL` now exists and is counted from the response's
own output items.

### What this means for Chapter 6 - and a duplicated clause to delete

**You already applied the reword I offered in Fix 13**, and it is still the right
sentence. My reasoning for offering it was partly wrong; the wording is not.
Token counts come from the provider's usage object, web search is now priced, and
the only remaining unknown is sandbox duration, which the API exposes to nobody.
Reconciling total spend against the billing record is exactly what the harness
does.

⚠ **But the original clause was left in front of it.** Section 6.8 currently
reads:

> "Memory is reported by RSS; Memory is reported by resident set size; token usage
> and wall-clock latency are measured per run..."

**Action: REWORD - delete the first three words and the semicolon**, so the
sentence begins:

> Memory is reported by resident set size; token usage and wall-clock latency are
> measured per run, and total spend is reconciled against the provider's billing
> record rather than inferred from token counts.

This is the only application error I found in the whole pass.

### Note - the lesson worth keeping

The tell was in the data and was walked past: the harness recorded zero cached
input tokens on every run, while the day's billing carried a cached-input charge.
**The harness cannot have issued requests it did not make**, so the window
contained foreign traffic. A number that cannot have come from your own process
is the strongest possible signal that the comparison is not like-for-like.

---

# F6 - Thread 290, the on-demand sandbox

Your comment: *"the sandbox is being instantiated on demand, meaning only if
queries are actually send by end users, will the company be charged, cutting down
the server costs significantly."*

**Already answered**, by the consolidated pass's Fix 13, which you applied. The
Section 6.8 paragraph now ends:

> "...the execution sandbox is created per request and billed only when a query is
> actually made, so an idle deployment carries no compute cost at all."

**Verdict: ADDRESSED, no further edit.** The thread can be resolved.

⚠ It sits on a Section 6.5 sentence while the answer landed in Section 6.8, which
is why it looks unanswered. The cost argument belongs in the budget section.

---

# F7 - Thread 278, "human oversight" - still open, Fix 3b did not land

Your `VERIFY: See previous comment`, on the phrase *"human oversight"* in Section
6.2.

⚠ **This one was NOT applied.** Fix 3b of the consolidated pass proposed replacing
it and the chapter still reads *"a bounded tool-using AI agent with human
oversight"*. Since you removed the human-in-the-loop claim everywhere else, this
is now the **only** surviving assertion of a control the artefact does not have,
which makes it more conspicuous than it was before, not less.

### Anchor

**Section 6.2**, the paragraph beginning *"In the conceptual taxonomy of Sapkota
et al. (2025)"*:

> "...is most accurately described as a **bounded tool-using AI agent** with human
> oversight, rather than a full multi-agent Agentic AI system."

### Action

REWORD.

#### Replace with

> ...is most accurately described as a **bounded tool-using AI agent** rather than
> a full multi-agent Agentic AI system. Its boundedness is a property of what the
> agent is permitted to do: it holds a fixed tool set, it does not delegate to
> other agents, and it does not act on its own recommendation.

### Note

The replacement says what bounded actually means here, which is the part Sapkota
et al.'s taxonomy is being used to claim. **The advisory property is real and is
already stated in Sections 6.2 and 6.5**; only this phrase still implies a gate.

---

# F8 - One more citation worth adding, and one I am not adding

## Worth adding - Section 6.4's uncertainty paragraph

**Goodwin, Önkal & Thomson (2010), "Do forecasts expressed as prediction
intervals improve production planning decisions?"**, Zotero key `IJ8UMZ3X`,
verified present with authors and date.

Section 6.4 asserts that attaching an interval preserves uncertainty, which
assumes intervals help a decision-maker. **This source tested that**, in
production planning, which is the thesis's own setting.

### Action

REWORD the **Uncertainty** paragraph's opening clause. Optional.

> **Uncertainty**, by attaching interval information to every forecast, which is
> what allows a planner to act on the forecast's reliability rather than on its
> point value alone (Goodwin et al., 2010); the interval is produced by split
> conformal calibration, whose marginal coverage guarantee is validated
> empirically in Chapter 5, and the width that guarantee costs on this panel is
> discussed in Chapter 8.

⚠ **Read the source's finding before citing it.** Its result is nuanced - it
tests whether intervals *improve decisions*, and a paper that found they did not
would still support the design's reasoning but would need different wording. I
have verified it exists and is on topic. **I have not verified its conclusion**,
and I am not going to assert it on your behalf.

## Not adding - AgentOps, on observability

**Dong, Lu & Zhu (2024)**, key `DAN2UBT6`, verified present. It is genuinely on
point for Section 6.6's observability capability.

**I am not adding it, and the reason is the same as last time:** Section 6.6 is
four sentences long, has no open comment, and adding a citation there is scope
nobody asked for. **Say the word and it goes in** - it would strengthen the
weakest section in the chapter.

---

# What the experiment session changed that does NOT touch Chapter 6

Checked, so you know it was looked at rather than missed:

| Update | Chapter 6 impact |
|---|---|
| Volume floor on brand stratification | **none.** A Chapter 8 sampling decision. F2 above carries the one sentence Chapter 6 owes |
| The degenerate-brand finding (9 units/month) | **none.** Chapter 8 |
| The conclusion shape for SRQ4 | **none, deliberately.** It is explicitly marked "do not write into prose" |
| MVP trial allocation and cost | **none.** Chapter 3 and Chapter 8 |
| Web search pricing | only via F5 - it makes the chapter's existing sentence right |

⚠ **One finding in that session is a Chapter 6 result in waiting**, and it is
worth knowing before you write anything else in Section 6.4. In the combined
arms, both agents departed from the model's forecast **and cited the model's own
confidence tier and interval width as their reason for doing so.** I verified
this in both traces rather than taking it from the note.

That is the uncertainty channel of the interface doing exactly what Section 6.4
claims it is for: the typed payload carried decision-relevant information rather
than a bare number. **It is a stronger result for SRQ2 than accuracy would be**,
and it does not depend on sample size in the way an accuracy ranking does.

**It is still one brand-month, so it stays out of the prose for now.** When the
funded set lands, it belongs in Section 6.4 as a measured property.
