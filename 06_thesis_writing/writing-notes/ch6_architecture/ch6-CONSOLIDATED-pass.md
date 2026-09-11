---
name: ch6-CONSOLIDATED-pass
description: NOTE - The single Chapter 6 document. Every verified fact from the prose pass, its follow-up and the sample-size rationale, in one place. Work top to bottom with the .docx open. Supersedes all three.
snapshot: 2026-09-11_17-24_ch6-prose-pass
category: workflow
applies-to: [ch6-architecture]
triggers: [applying chapter 6 edits, writing chapter 6 prose]
created: 2026_09_11-18_10
updated: 2026_09_11-18_10
status: ready
---

# Chapter 6 - the consolidated pass

**This one file replaces three.** `ch6-prose-pass.md`,
`ch6-prose-pass-followup-01.md` and `sample-size-and-tool-interface-rationale.md`
are all folded in and archived. Nothing else in the chapter folder is live.

**Verified at `fe0e895`**, fetch clean. Snapshot `2026-09-11_17-24_ch6-prose-pass`.
Zotero re-pulled 17:24: **89 items**. Chapter 6 is **2,176 words**, unchanged
since the previous snapshot, with **17 open comment threads**.

## How to use this document

| Part | What it is |
|---|---|
| **Part 1** | The 17 fixes, in document order. Each has an anchor, an action and paste-ready text |
| **Part 2** | The comment ledger - every thread, its verdict, where it is answered |
| **Part 3** | Verified background that did not become an edit, kept because it answers defence questions |
| **Part 4** | Open items: what needs your decision, and what is blocked |

**Every anchor in Part 1 was checked programmatically against the snapshot and
matches exactly once.** 27 of 27.

## What was carried forward from the sample-size note, and what was not

That note is 978 lines spanning Chapters 4, 5, 7 and 10, and carries a banner
saying its counts are superseded. **That banner is correct and I re-verified it.**

| Section of that note | Disposition |
|---|---|
| §6, how the LLM reaches a forecast | **carried into Part 3.1** - the reasoning is the SRQ2 contribution and is unchanged |
| §8, cross-category asymmetry | **partly carried, partly dead.** The promotional asymmetry is real and is now in Fix 5. Its RTD claim is **superseded** - see Part 3.4 |
| §12, warm-up versus cold start | **carried into Part 3.2** - still correct, still a defence question |
| §§1-5, 7, 9-11, 13 | **not Chapter 6 material.** They belong to Chapters 4, 5 and 10, and the archived note remains their source |

⚠ **I have carried no count from that note into any paste block.** Every number
below was re-measured today against the artefact that produces it.

---

# Part 0 - the three things to know before starting

## 1. Two of your comments found defects in the artefact, not the prose

Threads **274/275/287** (human-in-the-loop) and **289** (temperature) are both
correct, verified against code rather than taken as read.

**There is no approval gate anywhere in the artefact.** Every match for
"checkpoint" in the harness is a LangGraph state saver or a crash-recovery save,
an unrelated meaning of the word. **Temperature is genuinely not settable** on
the pinned model, and the harness records that on every run.

These are the highest-value comments in the chapter, because both claim a
control an examiner would expect demonstrated.

## 2. A citation in this chapter is not in the library

**Semerikov et al. (2025) is absent from Zotero**, and is cited twice - Section
6.5 and the Table 18 row for the remote-API choice. Fix 9 handles it.

## 3. The Section 6.3 measurements are wrong in both directions

Not stale in one direction. **Wrong in both**, against the artefact they claim
to come from, and contradicting Chapter 5 which reads the same file. Fix 4.

---

# Part 1 - the fixes

## Fix 1 - Section 6.1, the status note is a metacomment with two wrong facts

Threads **271** and **272**.

### Anchor

**Section 6.1 Design Objectives and Constraints**, the final paragraph, from:

> "A note on status: this is a design specification, but its lower layers are
> implemented and measured."

through to:

> "...this is stated explicitly rather than presented as a settled result."

### Action

REPLACE the whole paragraph.

#### Replace with

> The architecture specified here is implemented, not proposed. The forecasting
> substrate is realised and benchmarked across the four categories in Chapter 5,
> and its component memory figures are measured by resident set size. The
> structured interface and the bounded agentic layer are realised in a
> lightweight Python coordinator and exercised in Chapter 7, and the cost and
> latency of the agentic and code-writing paths are reported in Chapter 8. The
> layers that remain design targets rather than measured properties are named as
> such where they arise.

### Note - three problems in one paragraph

| Was | Is |
|---|---|
| "five categories" | **four** - CSD, danskvand, energidrikke, RTD |
| "(Chapter 6)" - the chapter citing itself | **Chapter 5** |
| "A note on status:" addressing the reader | states the status as fact |

The "five" counted the dropped `totalbeer` category. The self-reference is
8 September swap residue. **The same pair recurs in Fix 2 and Fix 12.**

---

## Fix 2 - Section 6.2, "benchmarked in Chapter 6" points at itself

### Anchor

**Section 6.2 Architectural Overview**, first item of the three-layer list:

> "a **forecasting substrate**, a set of lightweight machine learning models that
> produce point forecasts and interval information (SRQ1; benchmarked in Chapter 6);"

### Action

REWORD.

#### Replace with

> a **forecasting substrate**, a set of lightweight machine learning models that
> produce point forecasts and interval information (SRQ1; benchmarked in Chapter 5);

---

## Fix 3 - Sections 6.2 and 6.5, the human-in-the-loop claim is not implemented

Threads **274**, **275**, **287**. Your comment: *"There is no gate where a human
must validate or greenlight any information or outcomes before the Agent makes
its recommendation."* **Verified: correct.**

### 3a - Section 6.2, the layer list

#### Anchor

**Section 6.2**, third item of the three-layer list, ending:

> "...and synthesises a confidence-qualified recommendation, with
> human-in-the-loop checkpoints."

#### Action

REWORD - the clause after the comma.

#### Replace with

> ...and synthesises a confidence-qualified recommendation, which is presented
> for human judgement rather than acted on automatically.

### 3b - Section 6.2, "human oversight"

#### Anchor

**Section 6.2**, the paragraph beginning *"In the conceptual taxonomy of Sapkota
et al. (2025)"*:

> "...is most accurately described as a **bounded tool-using AI agent** with human
> oversight, rather than a full multi-agent Agentic AI system."

#### Action

REWORD.

#### Replace with

> ...is most accurately described as a **bounded tool-using AI agent** rather than
> a full multi-agent Agentic AI system. Its boundedness is a property of what the
> agent is permitted to do: it holds a fixed tool set, it does not delegate to
> other agents, and it does not act on its own recommendation.

### 3c - Section 6.5

#### Anchor

**Section 6.5 The Bounded Tool-Using Agentic Layer**, first paragraph, ending:

> "...and produces a concise, confidence-qualified natural-language
> recommendation, subject to human-in-the-loop checkpoints."

#### Action

REWORD.

#### Replace with

> ...and produces a concise, confidence-qualified natural-language recommendation.
> The recommendation terminates the automated path: the system advises and does
> not execute, so the decision to act on a forecast remains with the planner who
> receives it.

### Note - why the replacement is the better claim

"Human-in-the-loop checkpoints" promises a gate **inside** the pipeline, which
an examiner would expect demonstrated and which does not exist. What the artefact
offers is **advisory output**: it produces a recommendation and stops. That is a
real architectural property, true of every scenario in the harness, and it does
not overclaim.

⚠ **Do not replace this with a promise to add a gate later.** A specification
describing a control it lacks is the defect; describing a different control it
has is the fix.

---

## Fix 4 - Section 6.3, the memory figures contradict Chapter 5

Thread **282** tags the RSS sentence VERIFY. **It does not survive.**

`05_thesis_results/05_model_benchmark/tables/profiling.csv`, the artefact both
chapters read:

| Model | Chapter 6 says | The artefact says | Chapter 5 says |
|---|---|---|---|
| XGBoost | ~15 MB | **29.2** | 29.2 ✓ |
| LightGBM | ~7 MB | **38.1** | 38.1 ✓ |
| Ridge | < 1 MB | **5.4** | 5.4 ✓ |

⚠ Chapter 6 **understates LightGBM by a factor of five and inverts the ordering
of the two boosters**. Its tracemalloc figures are wrong too: it says LightGBM
18.7 and XGBoost 0.2; the file says 23.0 and 0.1.

**Two chapters citing one artefact with different numbers is the defect an
examiner is most likely to catch**, because spotting it needs no domain
knowledge.

### Anchor

**Section 6.3 The Forecasting Substrate (SRQ1)**, the entire final paragraph,
from:

> "Measured locally on the largest category (CSD), the per-model fit footprint is
> small in RSS terms:"

to:

> "...Component figures are consolidated in **Table 17**."

### Action

REPLACE the whole paragraph.

#### Replace with

> Peak resident memory during fitting is in the tens of megabytes for every model
> in the substrate, and the per-model figures are reported with the benchmark in
> Chapter 5. Serving is cheaper still, by roughly two further orders of
> magnitude, because a served model answers from parameters already in memory
> rather than rebuilding them. The substrate therefore operates far below the
> four-gigabyte ceiling in both phases. The memory budget does its work at
> selection time rather than at run time: it excludes transformer and locally
> hosted options before any of them is fitted, and leaves the footprint of the
> models eventually selected nowhere near the constraint.

### Note - state a measurement once

Cutting the numbers rather than correcting them is deliberate. The architecture
chapter needs the **conclusion**, not a second copy of the measurements. Stating
them once is also what stops them diverging again.

⚠ **The artefact is itself stale**, separately. `profiling.csv` was written on
1 September against a **13-feature** matrix; the current set is 18. Chapter 5
discloses this in Section 5.5.6 and argues the conclusion is unaffected. After
this fix Chapter 6 quotes no figures, so it needs no equivalent disclosure.
Tracked as S19.

---

## Fix 5 - Section 6.3, the feature description is missing half the feature set

Thread **280**: *"MISSING: the holiday api enrichment."* Correct, and
intermittency is missing too.

### Anchor

**Section 6.3**, first paragraph:

> "The gradient-boosted models use the exogenous predictors described in Chapter
> 4, namely promotional, distribution, and calendar features, alongside
> autoregressive features; the two promotional features are inactive for the
> promo-zero categories."

### Action

REPLACE that sentence.

#### Replace with

> The gradient-boosted models consume the engineered predictors described in
> Chapter 4: autoregressive lags and rolling summaries, calendar position,
> promotional intensity, a Danish public-holiday enrichment giving the trading
> days and holiday count of each month, and two intermittency features that
> record whether a brand is in a run of zero sales and how long that run has
> lasted. Promotional intensity is a category capability rather than a guarantee,
> and is absent for the two categories in which the panel does not report
> promotion; where it is absent the column is omitted rather than zero-filled,
> because a constant-zero column would assert that no promotion ran.

### Note - the count, and two corrections

The canonical list is six groups, **18 features**, in
`model_training/srq1/_features.py`. I have deliberately **not** put "18" in the
prose: Chapter 4 owns the count and Chapter 5 quotes it, and a third copy is a
third thing to keep in step.

⚠ **"distribution" was wrong.** There is no distribution feature in the model's
input set. `weighted_distribution` exists in the panel but is not a model input.

⚠ **"the two promotional features" was also wrong.** There is **one**,
`promo_intensity`. The replacement avoids the count entirely.

The absent-not-zero treatment is the sample-size note's §8 asymmetry finding,
re-verified today and stated at the point it matters.

---

## Fix 6 - Section 6.3, sequential execution is no longer load-bearing

Thread **281**: *"Not really relevant due to the low ram usage on deploy (50mb).
As i said before, so sequential is not necessary."*

**You are right that it is not necessary.** Keep the sentence, change what it
claims. **And see Part 4.1 - I found where your 50 MB comes from, and there is a
better number.**

### Anchor

**Section 6.3**, the paragraph beginning *"Two design decisions follow from the
RAM constraint."* Replace from that opening through:

> "...because tracemalloc does not capture the native allocations of XGBoost and
> LightGBM."

The rest of the paragraph, from *"The substrate exposes, for each forecast..."*,
is unchanged.

### Action

REPLACE that span.

#### Replace with

> Two decisions follow from the memory constraint. Models are executed
> sequentially, loading, running and unloading one at a time, so that the
> substrate's footprint is set by its largest single model rather than by their
> sum. The measured footprint turned out to sit far enough below the ceiling that
> concurrent execution would also have fitted, so sequential execution is better
> understood as what made the budget safe to design against in advance than as
> what keeps the system inside it now. Memory is profiled by process resident set
> size rather than by Python-level allocation tracking alone, because the
> gradient-boosted libraries allocate natively and a Python-level tracker does not
> see those buffers.

### Note - why keep it at all

Because it is the honest history of the design, and a Design Science point
rather than an engineering one. The constraint was real when the choice was
made, the choice was correct under it, and measurement later showed the
constraint slack. **A design chapter that reports this is stronger than one that
quietly drops the decision**, because it shows the budget actually governing a
choice.

---

## Fix 7 - Section 6.4, the three properties are now measured

Thread **284** tags all three bullets VERIFY. They verify as **design
intentions**; two are now measurements.

### 7a - Reliability

#### Anchor

**Section 6.4**, the bolded paragraph:

> "**Reliability**, by validating the agent's stated numbers against the source
> forecast values before delivery, so that the agent reports the model's numbers
> rather than its own."

#### Action

INSERT AFTER - one sentence appended to that paragraph.

#### Replace with

> In the pilot run this validation was exercised: the figure the agent reported
> and the figure the model produced agreed exactly, and the recorded tool-call
> span confirmed that the agent had queried the series it was asked about at the
> intended horizon.

### 7b - Uncertainty

#### Anchor

**Section 6.4**, the bolded paragraph:

> "**Uncertainty**, by attaching interval information to every forecast; interval
> calibration follows the post-hoc approach of Kuleshov et al. (2018) and is
> treated as a design target, not an empirically validated property of the
> current prototype."

#### Action

REWORD - the clause after the semicolon.

#### Replace with

> **Uncertainty**, by attaching interval information to every forecast; the
> interval is produced by split conformal calibration, whose marginal coverage
> guarantee is validated empirically in Chapter 5, and the width that guarantee
> costs on this panel is discussed in Chapter 8.

### Note - what changed and what it must not become

The sentence said calibration is *"a design target, not an empirically validated
property"*. **It has since been validated**: observed coverage is 83.9 to 91.7
per cent against a 90 per cent target across four categories, and calibration now
runs against the model each category actually serves.

⚠ **Do not replace it with a claim that the intervals are informative.** They
attain coverage **and are very wide** - the guarantee is marginal, and one pooled
quantile spans brands of six orders of magnitude. That belongs to Chapters 8 and
10. The wording points at both without asserting either here.

⚠ **Kuleshov et al. (2018) is dropped by this reword.** It is in Zotero
(`E4GHQL9A`) and correctly cited today, but describes recalibration of deep
learning uncertainties, and the artefact uses split conformal. If you want a
citation here, the honest one is the conformal source Chapter 5 already uses.

### 7c - Traceability

**VERIFIED-OK, no edit.** Implemented as described: every run writes a tool-call
span carrying the arguments, an `args_match_request` flag and the horizon. The
sentence claims exactly that and no more.

---

## Fix 8 - Section 6.4, the cross-reference points at the wrong chapter

### Anchor

**Section 6.4**, last paragraph, final clause:

> "...it is instead the baseline against which the artefact is compared (Section 5.7)."

### Action

REWORD.

#### Replace with

> ...it is instead the comparator against which the artefact is evaluated
> (Section 6.7).

### Note

Ch5/Ch6 swap residue; the section is 6.7 here. **Word will not update this
automatically** - it is typed text, not a field reference.

"Baseline" becomes "comparator" because the design is a ladder in which every
rung is a comparator for the one below. See Part 4.3. **If you prefer to keep
"baseline", revert that one word** - the decision has two sites and should be
taken once.

⚠ **The same defect sits in Section 6.2**, in the paragraph beginning *"The
layers are coordinated by a lightweight Python coordinator"*:
`(SRQ3, Section 5.6)` → **`(SRQ3, Section 6.6)`**.

---

## Fix 9 - Section 6.5, two unsupported claims

### 9a - the decoding claim

Thread **289**, and it is correct.

#### Anchor

**Section 6.5**, second paragraph:

> "Decoding is configured for reproducibility (temperature zero)."

**Next sentence begins:** *"This separation of a generative orchestrator from
deterministic predictive components..."*

#### Action

REWORD.

#### Replace with

> Decoding parameters are left at the provider's defaults, because the pinned
> model does not expose temperature or top-p. Reproducibility is pursued instead
> through a dated model snapshot and a recorded prompt registry, so that a run can
> be reconstructed from what was sent rather than from a sampling setting.

### Note - the replacement is the stronger claim

**Temperature is not settable on this model.** The harness records the fact on
every run and its pre-flight check asserts the recorded claim matches reality
before any paid run.

An examiner reading "temperature zero" expects determinism. What the artefact
offers is a **pinned dated snapshot plus a hashed prompt identity recorded per
run**, which is arguably better because it survives a provider changing its
defaults.

### 9b - the Semerikov citation

#### Anchor

**Section 6.5**, first paragraph:

> "...a decision that keeps the language model out of the RAM budget entirely (a
> locally hosted model would add several gigabytes; Semerikov et al., 2025)."

#### Action

REWORD.

#### Replace with

> ...a decision that keeps the language model out of the memory budget entirely,
> since model weights large enough to be useful would exhaust a four-gigabyte
> ceiling on their own.

### Note - NEEDS-BRIAN

⚠ **Semerikov et al. (2025) is not in the Zotero library.** Verified against the
2026-09-11 17:24 pull, 89 items, searched by author across every item type rather
than the filtered export. Cited **twice**: here, and in Table 18.

1. **Add it to Zotero** if it is real and one of you has read it, and restore
   both citations.
2. **Drop it**, as the reword does. The claim then rests on arithmetic - weights
   against a stated ceiling - which needs no citation.

The reword takes option 2 so the chapter is consistent today. Fix 11c handles
the table row.

---

## Fix 10 - Section 6.5, the delegation claim needs a boundary

Thread **288**: *"Besides in Scenarios A, B, and D."* Correct, and the
distinction is what the experiment measures.

### Anchor

**Section 6.5**, second paragraph, opening:

> "The layer embodies a **delegation-over-generation** principle: the LLM does not
> itself predict demand or compute the forecast, but delegates numerical
> prediction to the dedicated models and confines itself to orchestration,
> validation, and communication."

### Action

REPLACE that sentence, and append a second.

#### Replace with

> The layer embodies a **delegation-over-generation** principle: within the
> artefact, the language model does not itself predict demand, but delegates
> numerical prediction to the dedicated models and confines itself to
> orchestration, validation, and communication. The principle describes the
> artefact rather than the language model's capability, and the comparison in
> Chapter 8 turns on exactly that difference: the scenarios that withhold the
> dedicated model leave the language model to produce a number by its own means,
> which is the alternative this design rejects.

### Note

Without the boundary, an examiner who reaches Chapter 8 and finds a scenario in
which the language model does compute a forecast reads Section 6.5 as
contradicted. Naming the scope turns that into the point being tested.

⚠ **Do not name the scenarios by letter here.** Section 6.7 enumerates them and
the letters are moving - see Fix 14 and Part 4.2.

---

## Fix 11 - Section 6.9, two defects and a metacomment in Table 18

### 11a - the metacomment

Thread **301**.

#### Anchor

**Section 6.9**, **Table 18**, first data row, first cell:

> "Lightweight Python coordinator (evaluated)"

and that row's reason cell, ending *"...leaner for the evaluated prototype under
the RAM budget"*.

#### Action

REWORD both cells.

| Cell | Replace with |
|---|---|
| Choice | Lightweight Python coordinator |
| Reason | The production target is a LangGraph deployment; a lightweight coordinator is leaner under the memory budget and sufficient for the comparison the thesis runs |

### 11b - the sandbox row names the wrong sandbox

#### Anchor

**Table 18**, last row:

> "| Sandbox (e.g. E2B) for the baseline | Bespoke execution harness | Open and
> local; runs the code-as-action baseline without production access |"

#### Action

REPLACE the row.

> | Hosted code-execution sandbox for the comparator | Bespoke execution harness | The provider's sandbox is created per call and billed only when used, so the comparator needs no infrastructure of its own |

### Note - E2B is not what the harness uses

**Verified.** The harness uses **OpenAI's Code Interpreter**, requested as
`container: auto`, creating a fresh container per call. E2B appears in one
standalone cost-measurement script that nothing imports, and nowhere in the
experiment path.

The replacement also carries thread **286**'s point about on-demand
instantiation. Fix 13 puts the same fact where the cost argument lives.

### 11c - the Semerikov row

#### Anchor

**Table 18**, the row *"LLM via remote API | Locally hosted LLM | Avoids several
gigabytes of model weights, keeping the language model out of the RAM budget
(Semerikov et al., 2025)"*.

#### Action

REWORD the reason cell - delete the citation, per Fix 9b.

> Avoids several gigabytes of model weights, keeping the language model outside the memory budget entirely

---

## Fix 12 - Section 6.10, three defects in the summary

### Anchor

**Section 6.10 Summary**, the whole section - one paragraph, beginning:

> "The architecture instantiates the predictive extension as three layers,"

### Action

REPLACE the paragraph.

#### Replace with

> The architecture instantiates the predictive extension as three layers: a
> forecasting substrate, a structured forecast-tool interface, and a bounded
> tool-using agentic layer, coordinated by a lightweight Python coordinator and
> designed to operate within a four-gigabyte budget. It is deliberately a bounded
> tool-using agent rather than a multi-agent system, it delegates prediction to
> dedicated models rather than generating it, and it advises rather than acts.
> The forecasting substrate is benchmarked in Chapter 5 (SRQ1), the interface and
> agentic layer are realised and exercised in Chapter 7 (SRQ2, informing SRQ3),
> and the dedicated-model approach is compared against the code-writing
> scenarios in Chapter 8 (SRQ4).

### Note

| Was | Is |
|---|---|
| "eight-gigabyte budget" | **four** - see Fix 13 |
| "benchmarked in Chapter 6 (SRQ1)" | **Chapter 5** |
| no advisory boundary | added, matching Fix 3 |

---

## Fix 13 - Section 6.8, the memory budget contradicts itself

⚠ **The most serious defect in the chapter**, because it is internally
contradictory rather than merely stale.

| Where | Says |
|---|---|
| Section 6.1 | four gigabytes |
| Section 6.3 | four-gigabyte |
| Section 6.8, first paragraph | four-gigabyte |
| **Section 6.8, the peak sentence** | ⚠ **eight-gigabyte** |
| Section 6.9 | four-gigabyte |
| **Section 6.10** | ⚠ **eight-gigabyte** |

**Chapter 5 says four**, in Sections 5.1 and 5.5.6, settled deliberately. The
results artefact agrees: `05_substrate_resource_profile` computes its budget
share against **4096 MB**. Chapter 6 should say four everywhere.

### Anchor

**Section 6.8 Memory, Cost, and Latency Budget**, the paragraph below Table 17:

> "The end-to-end peak of approximately 231 MB is about 2.8% of the
> eight-gigabyte budget."

### Action

REPLACE the paragraph.

#### Replace with

> The end-to-end peak of approximately 231 MB is under six per cent of the
> four-gigabyte budget. The budget therefore binds the space of models that could
> be selected, excluding transformer and locally hosted options before any of them
> is fitted, rather than the footprint of what was selected. The realised
> footprint sits well below the ceiling for two reasons: the language model is
> kept out of process behind a remote interface, and only one lightweight model is
> resident at a time. Cost behaves the same way, because the execution sandbox is
> created per request and billed only when a query is actually made, so an idle
> deployment carries no compute cost at all.

### Note - the percentage moves too

⚠ **231 MB against 4 GB is 5.6 per cent, not 2.8.** The old figure was computed
against eight gigabytes, so correcting the budget without correcting the
percentage would leave a second error behind. "Under six per cent" rather than
"5.6 per cent" because 231 is itself approximate.

The final sentence answers thread **286**.

---

## Fix 14 - Section 6.7 is BLOCKED

Thread **294**: *"I think it would help tremendously to name each scenario and
map it to the respective set-up."* **Agreed, and that is what the section should
become** - but not yet.

### Action

**BLOCKED** on Part 4.2, the display-label defect.

### Note - the seven scenarios, verified

The harness registers **seven** as of `3c37ffd`:

| | scenario | adds |
|---|---|---|
| A | plain language model, web search | - |
| B | + brand history in a code sandbox | what data access buys |
| C | + the trained model behind a tool | what the artefact adds |
| D | B's task on the production orchestrator | orchestrator effect on B |
| E | C's task on the production orchestrator | orchestrator effect on C |
| F | data, code **and** the model together | what code adds on top of the model |
| G | F's task on the production orchestrator | the combined arm, on production |

**F and G completed at 17:31**, both clean on the first attempt, so the earlier
block - that the arms were unexercised - is gone. What remains is that the
display labels in the harness contradict these names. Section 6.7's job is
precisely to fix the naming, and writing it against output that contradicts it
would bake the contradiction into the chapter.

⚠ **Two things the rewrite will need:**

1. **The sandbox is OpenAI's Code Interpreter, not E2B.** The current text says
   *"for example, E2B as it is used in our testing scenarios"*.
2. **DEC-COMBINED-INPUT.** In the combined arms the model's forecast is supplied
   as one input among several, never as a starting point to revise. An agent
   handed a number and told it may keep it will mostly keep it, which would
   measure deference rather than integration. **The traces confirm the decision
   held** - see Part 3.3.

---

## Fix 15 - Section 6.7, "locally" is misleading

Thread **295**. **Correct**, and fixable now even though the section is
otherwise blocked, because it does not depend on the enumeration.

### Anchor

**Section 6.7**, second paragraph, opening:

> "The baseline is runnable locally and does not require access to the production
> system, which makes the SRQ4 comparison feasible independently of integration
> access."

### Action

REWORD.

#### Replace with

> The comparison requires no access to the production system: everything held on
> our side is the Python code that assembles the data and issues the prompts,
> while the language model and its execution sandbox are reached as hosted
> services. The comparison is therefore feasible independently of integration
> access, which is what makes it possible to run at all.

### Note

The claim being protected is **"no production access needed"**, which is true and
load-bearing. "Locally" overstated it into "no external dependency", which is
false - the comparison needs internet access and a funded API account.

---

## Fix 16 - Section 6.9, the closing sentence

Thread **303**: `PROSE & TABLE REFERENCE`.

### Anchor

**Section 6.9**, the single sentence below Table 18:

> "Each choice is argued against the four-gigabyte constraint, in keeping with the
> design criterion of Chapter 1."

### Action

REPLACE.

#### Replace with

> Every choice in Table 18 is argued against the four-gigabyte constraint
> established in Chapter 1, and in each case the alternative was rejected for
> what it would have cost in memory or in auditability rather than for what it
> would have gained in capability.

### Note

Two things, and the reword does both. It **names the table** rather than
gesturing at it, so the sentence survives the table moving. And it says something
the table does not already say: the rejections share a reason. As written, the
sentence only restated the table's existence.

---

## Fix 17 - the chapter subtitle

Thread **269**. The placeholder **"COULD USE A SUBTITLE"** sits in the document
body and must be deleted either way.

### Action

NEEDS-BRIAN - pick one.

| Option | Reads as |
|---|---|
| **Delegating Prediction Behind a Typed Interface** | names the central design decision |
| **A Bounded Tool-Using Extension Under a Memory Budget** | names the artefact and its binding constraint |
| **From Explanation to Forecast: Extending a Production Agent** | names the capability gap the thesis opens with |

**Recommendation: the first.** It states what the chapter argues rather than what
it describes, and "delegation over generation" is the phrase Section 6.5 already
uses, so subtitle and chapter reinforce each other.

⚠ Check how subtitles are styled in other chapters before pasting, so this one
matches.

---

# Part 2 - the comment ledger

| Thread | Opens | Verdict |
|---|---|---|
| 269, subtitle | "Could use a subtitle" | **NEEDS-BRIAN** - Fix 17, three options, one recommended |
| 271, status note | "METACOMMENT" | **ADDRESSED** - Fix 1 |
| 272, hedging sentence | "METACOMMENT" | **ADDRESSED** - Fix 1, removed with the paragraph |
| 274, checkpoints | "Not really implemented as far as I know" | **ADDRESSED** - Fix 3a. Confirmed |
| 275, human oversight | "See previous comment" | **ADDRESSED** - Fix 3b |
| 280, predictors | "MISSING: the holiday api enrichment" | **ADDRESSED** - Fix 5. Intermittency was missing too |
| 281, sequential | "Not really relevant due to the low ram usage" | **ADDRESSED** - Fix 6, reframed not cut. Figure resolved in Part 4.1 |
| 282, RSS figures | "VERIFY" | **ADDRESSED** - Fix 4. Wrong in both directions |
| 284, three properties | "VERIFY" | **ADDRESSED** - Fix 7a, 7b; traceability VERIFIED-OK |
| 286, sandbox on demand | "only if queries are actually send" | **ADDRESSED** - Fix 13, and Fix 11b |
| 287, no human in loop | "No human in loop atp i think" | **ADDRESSED** - Fix 3c. Confirmed |
| 288, scenarios A/B/D | "Besides in Scenarios A, B, and D" | **ADDRESSED** - Fix 10 |
| 289, temperature | "does not even accept temperature" | **ADDRESSED** - Fix 9a. Confirmed |
| 294, name the scenarios | "would help tremendously to name each scenario" | **FLAGGED** - Fix 14, blocked on Part 4.2 |
| 295, "locally" | "a bit deceiving, because the API needs internet" | **ADDRESSED** - Fix 15 |
| 301, "(evaluated)" | "METACOMMMENT" | **ADDRESSED** - Fix 11a |
| 303, closing sentence | "PROSE & TABLE REFERENCE" | **ADDRESSED** - Fix 16 |

**16 of 17 resolved.** Thread 294 waits on a code fix, not on evidence.

---

# Part 3 - verified background that did not become an edit

Kept because these answer questions that will be asked at defence, and because
the sample-size note that held them is being archived.

## 3.1 How the language model reaches a forecast - the SRQ2 mechanism

**Anticipated question:** *"The user asks a natural-language question. How does
the model get the lag values?"*

**It does not, and must not.** Having the language model assemble feature vectors
would be fragile and would defeat traceability.

The call path, verified against `forecast_tool.py`:

1. The language model decomposes intent into a **typed tool call** naming the
   brand and the horizon. Not a feature vector.
2. The service, server-side, looks up that brand's history, constructs the lag,
   rolling and calendar features itself, and runs the trained model.
3. It returns a typed payload: point forecast, calibrated interval, source model,
   and the data window it used.
4. The language model renders that into prose.

**The language model's responsibility is exactly two translations:** intent to
parameters, and structured output to prose. It never sees a lag value. Feature
construction stays server-side, where it is versioned, testable and identical on
every call.

**This is the SRQ2 contribution**, and it is already stated correctly in Section
6.4 - which is why it produces no edit. **It is also the hypothesised SRQ4
mechanism:** the code-writing scenarios must load data and construct features
themselves on every invocation, with no guarantee of doing it identically twice.
That is precisely the consistency and replicability axis the comparison measures.

⚠ The archived note illustrated this with a worked example carrying invented
numbers. **Those were placeholders, never measurements.** Do not quote them.

## 3.2 Warm-up is a training concept; cold start is the serving constraint

**Anticipated question:** *"If the model needs thirteen months of lag depth, how
does the served system answer when a user asks?"*

**It does not warm up. Warm-up is not a runtime phase.** It is the set of rows at
the start of each brand's own series whose lag features point to months before
the data begins. Those rows have a known target but an incomplete feature vector,
so they cannot be training examples. It is not a fourth split, and not a period
the model runs through before it works.

**At serving time** the brand's history is already stored, and the service reads
backwards from the most recent observed month to build the feature row directly.

**The real serving constraint is cold start:** a brand with too little stored
history cannot be forecast, because its deepest lag is undefined. That is a
**coverage limitation**, not a delay, and the correct response is a typed refusal
naming the brand rather than a silently degraded forecast.

⚠ **The refusal path exists but answers a different question.** `forecast_tool.py`
refuses a request for a month outside the test split. I did not find an
equivalent typed refusal for insufficient history. If a brand below the lag depth
is requested, verify what happens before claiming a refusal in prose.

## 3.3 The combined arms behaved as designed

**F and G completed at 17:31**, after the first version of this pass was written.
Both classified `ok`, no retries, no schema violations.

DEC-COMBINED-INPUT held in both traces. Each arm received the model's forecast of
4,969,050 and **neither returned it**:

| Arm | Code executions | Received | Returned |
|---|---|---|---|
| F | 12 | 4,969,050 | 6,200,000 |
| G | 2 | 4,969,050 | 5,604,800 |

Had either echoed the model's number, the experiment would have measured
deference rather than integration and the arm would be worth nothing. **Neither
did.** F ran twelve code executions on top of the forecast it was handed and
moved 25 per cent away from it.

⚠ **This is a check that the instrument works, not a result.** One brand, one
month, one run per arm. It belongs in Chapter 8's method description if anywhere,
not in Chapter 6.

## 3.4 Cross-category asymmetry - what survived and what did not

The archived note recorded, on 11 August, that RTD's fact table was empty and
that any claim of four categories was unsupported for one of them.

⚠ **That is superseded.** Re-verified today: RTD carries **62 brands** in the
statistical baselines and **372 test rows** in the calibration table. All four
categories are fully in scope. **Do not repeat the August warning.**

**What survives is the promotional asymmetry**, and it is real: the panel reports
promotion for two categories and not for the other two, because the source lacks
the measures rather than because of a configuration gap. Where absent, the column
is omitted rather than zero-filled, since a constant-zero column would assert
that no promotion ran. **That is now stated in Fix 5**, at the point in the
chapter where it matters.

Panel depth also differs by category, which is why interval coverage tracks
calibration set size in Chapter 5.

---

# Part 4 - open items

## 4.1 RESOLVED - where your 50 MB figure comes from, and the better number

You asked me to verify this. **I found it, and it is not a measurement of what
the comment assumes.**

Two sources, both estimates written before any profiling run:

| Where | Says | Dated |
|---|---|---|
| `user-docs/architecture/architecture.md` | "Ridge Regression: ~50MB" under **RAM estimate per model** | 11 July |
| `sections-drafts/decision-synthesis.md` | "Total synthesis step RAM: <50MB" | 8 September, but inherited from the same July estimates |

⚠ **Neither is a deployment measurement.** The first is a planning estimate for
Ridge, and the measured value is **5.4 MB** - the estimate was nine times too
high. The same table estimated LightGBM and XGBoost at 200 to 500 MB; measured,
they are 38.1 and 29.2. **Every estimate in that block is wrong by roughly an
order of magnitude**, which is exactly what a pre-measurement estimate is for and
exactly why it should not reach the thesis.

That file also still states an **eight-gigabyte** budget, which is the likely
origin of the eight-gigabyte residue in Chapter 6 that Fix 13 removes.

### The number you actually want is better than 50 MB

`05_thesis_results/05_model_benchmark/tables/05_substrate_resource_profile` is
the measured artefact, and it separates fitting from serving:

| Model | Peak fit RSS | **Peak prediction RSS** |
|---|---|---|
| Ridge | 5.4 MB | **0.02 MB** |
| LightGBM | 38.1 MB | **0.1 MB** |
| XGBoost | 29.2 MB | **0.62 MB** |
| ARIMA (per series) | 1.9 MB | **0.09 MB** |

**Serving costs under one megabyte**, three orders of magnitude below fitting,
because a served model answers from parameters already in memory rather than
rebuilding them. Sampled every 5 ms by a monitoring thread in a separate process
per model.

**This is a much stronger version of your point than 50 MB was.** Your argument
was that sequential execution is unnecessary because deployment memory is low.
The measured serving figures make that argument far better: even all four models
resident at once would cost under a megabyte at prediction time.

**Fix 4 and Fix 6 are written to carry this**, in words rather than figures, so
Chapter 5 stays the single site for the numbers.

⚠ **Do not cite 50 MB anywhere.** It is a superseded estimate, and the measured
value it estimated is off by a factor of nine.

## 4.2 BLOCKING Section 6.7 - the scenario display labels are inverted

`srq4_experiment.py` writes its summary table through a display map covering
**three of seven** scenarios, and **inverting the lettering**:

| internal name | prints as |
|---|---|
| `C_model` | **"A — dedicated model"** |
| `B_data` | "B — code-as-action" |
| `A_plain` | **"C — no firm data"** |

D, E, F and G are not in the map and fall through to raw internal names, so one
header row can mix inverted display letters with raw internal names.

**Why the inversion exists:** the display order runs best-to-worst for a reader,
while the internal order runs as an information ladder from least to most
capability. Both are defensible; **carrying both at once is not.**

**Recommendation:** delete the display map and print the ladder letters the
thesis uses. If a best-first presentation is wanted, sort the columns and leave
the names alone.

**This is a short code fix and I can do it on your word.** I have not done it
unprompted because choosing the display order is a presentation decision about
published tables, not a defect fix. **It should land before the funded run**, or
published tables carry it. Tracked as S21.

## 4.3 NEEDS-BRIAN - three decisions

| | Decision | Default if you say nothing |
|---|---|---|
| **Semerikov et al. (2025)** | add to Zotero, or drop the citation | Fix 9b **drops** it; the claim rests on arithmetic |
| **"baseline" vs "comparator"** | two sites, Sections 6.4 and 6.7 | Fix 8 uses **comparator**, matching the ladder |
| **the chapter subtitle** | three options in Fix 17 | none applied; the placeholder must be deleted regardless |

## 4.4 Zotero defects found while verifying

Recorded in S16. Library edits, not prose:

| Item | Defect |
|---|---|
| **Semerikov et al. (2025)** | **absent entirely**, cited twice in this chapter |
| Wang, Executable Code Actions | **duplicated**; one copy's date reads `July` |
| Paranjape, ART | **duplicated** |
| Ahrens, Model Averaging | **duplicated**; cited in Section 6.3 |
| Sapkota, AI Agents vs. Agentic AI | date stored as `02/2`; cited in Section 6.2 |
| Chen, ACGraph | date stored as `Dece` |

⚠ **The duplicates matter more than they look.** A duplicated item with two
different dates can render as two different in-text citations for one source, and
a reader checking the reference list finds the same paper twice. The Wang pair is
the live risk: cited twice in this chapter, and one copy has no usable year.

## 4.5 Two citations available but not added

Both are in the library and verified. **I left them out** because adding
citations to sections with no open comments is scope nobody asked for.

| Source | Would go | Why it fits |
|---|---|---|
| AgentOps: Enabling Observability of LLM Agents (Dong et al., 2024) | Section 6.6, the observability capability | Directly on point, and Section 6.6 is four sentences with no citation |
| Toolformer (Schick et al., 2023) | Section 6.4, the function-calling choice | Supports the tool-interface argument |

**Say the word and I will write either in.**

⚠ **Nothing from the forecasting textbook belongs in this chapter.** It is a
forecasting-methods text and Chapter 6 argues about software architecture. Its
place is Chapters 4, 5 and 8, where it is already used.
