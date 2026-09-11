---
name: ch6-prose-pass
description: NOTE - The full Chapter 6 pass. Every section in document order, all 17 comment threads verdicted, prose ready to paste. Read top to bottom with the .docx open.
snapshot: 2026-09-11_17-24_ch6-prose-pass
category: workflow
applies-to: [ch6-architecture]
triggers: [applying chapter 6 edits]
created: 2026_09_11-17_45
updated: 2026_09_11-17_45
status: ready
---

# Chapter 6 - the full pass

**Verified at `cf88039`**, fetch clean, nothing incoming. Snapshot
`2026-09-11_17-24_ch6-prose-pass`. Zotero re-pulled the same minute: **89 items**,
up from 86.

**Notes swept:**

| Note | State |
|---|---|
| `2026-09-11_experiment-state-for-ch6-prose.md` | not applied - **all four fixes are folded into this pass**, credited where they land |
| `...-followup-01.md` | not applied - **all three defects folded in** |
| `sample-size-and-tool-interface-rationale.md` | not applied, left in place. Its own banner says every count in it is superseded. Nothing here duplicates it |

Chapter 6 is **2,176 words and unchanged** since the last snapshot. All **17
comment threads are open**. Every one gets a verdict below.

---

# Before the fixes - three things worth knowing

## 1. Two of your comments found real defects in the artefact, not the prose

Threads **274/275/287** (human-in-the-loop) and **289** (temperature) are both
correct, and I verified them against the code rather than taking them as read.
There is no approval gate anywhere in the artefact. Every match for
"checkpoint" in the harness is a LangGraph state saver or a crash-recovery
save, which is an unrelated meaning of the word. Temperature is genuinely not
settable on the pinned model, and the harness records that on every run.

**These are the highest-value comments in the chapter**, because both claim a
control an examiner would expect to see demonstrated.

## 2. A citation in this chapter is not in the library

**Semerikov et al. (2025) is not in Zotero.** It is cited twice, in Section 6.5
and in the Table 18 row for the remote-API choice. Under the standing rule -
if it is not in the library, it is not a source - both citations have to go or
the source has to be added. Fix 9 handles it.

## 3. The measurement figures in Section 6.3 are wrong in both directions

Not stale in one direction, **wrong in both**, against the artefact they claim
to come from. This is Fix 4, and it is the defect most likely to be caught by
someone without domain knowledge, because Chapter 5 states different numbers
from the same file.

---

# The fixes

## Fix 1 - Section 6.1, the status note is a metacomment, and its facts are wrong

Threads **271** and **272** both tag the status note as METACOMMENT. They are
right, and the passage additionally carries the two wrong facts my followup
note found.

### Anchor

**Section 6.1 Design Objectives and Constraints**, the final paragraph, which
begins:

> "A note on status: this is a design specification, but its lower layers are
> implemented and measured."

It runs to the end of that paragraph:

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

### Note - what this fixes beyond the metacomment tag

Three separate problems, in one paragraph:

| Was | Is |
|---|---|
| "five categories" | **four** - CSD, danskvand, energidrikke, RTD |
| "(Chapter 6)" - the chapter citing itself | **Chapter 5** |
| "A note on status:" addressing the reader about the document | states the status as fact |

The "five" was counting the dropped `totalbeer` category, confirmed against the
results artefacts. The chapter self-reference is 8 September swap residue.

⚠ **The same pair recurs twice more.** Fix 2 and Fix 12 carry them.

---

## Fix 2 - Section 6.2, "benchmarked in Chapter 6" points at itself

### Anchor

**Section 6.2 Architectural Overview**, the first item in the three-layer list:

> "a **forecasting substrate**, a set of lightweight machine learning models that
> produce point forecasts and interval information (SRQ1; benchmarked in Chapter 6);"

### Action

REWORD.

#### Replace with

> a **forecasting substrate**, a set of lightweight machine learning models that
> produce point forecasts and interval information (SRQ1; benchmarked in Chapter 5);

---

## Fix 3 - Sections 6.2 and 6.5, the human-in-the-loop claim is not implemented

Threads **274**, **275** and **287**. Your comment: *"Not really implemented as
far as I know. There is no gate where a human must validate or greenlight any
information or outcomes before the Agent makes its recommendation."*

**Verified: you are right.** There is no approval gate in the artefact.

### 3a - Section 6.2, the layer list

#### Anchor

**Section 6.2**, the third item in the three-layer list, ending:

> "...and synthesises a confidence-qualified recommendation, with
> human-in-the-loop checkpoints."

#### Action

REWORD - the clause after the comma only.

#### Replace with

> ...and synthesises a confidence-qualified recommendation, which is presented
> for human judgement rather than acted on automatically.

### 3b - Section 6.2, "human oversight"

#### Anchor

**Section 6.2**, the paragraph beginning *"In the conceptual taxonomy of Sapkota
et al. (2025)"*, the clause:

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

### Note - why this is a better claim than the one it replaces

"Human-in-the-loop checkpoints" promises a gate **inside** the pipeline, which
an examiner would expect to see demonstrated and which does not exist. What the
artefact actually offers is **advisory output**: it produces a recommendation
and stops. That is a real and defensible architectural property, it is true of
every scenario in the harness, and it does not overclaim.

⚠ **Do not replace this with a promise to add a gate later.** A design
specification describing a control it does not have is the defect; describing a
different control it does have is the fix.

---

## Fix 4 - Section 6.3, the memory figures contradict Chapter 5

Thread **282** tags the RSS sentence VERIFY. **Verified, and it does not
survive.**

### The measurement

`05_thesis_results/05_model_benchmark/tables/profiling.csv`, the artefact both
chapters read:

| Model | Chapter 6 says | The artefact says | Chapter 5 says |
|---|---|---|---|
| XGBoost | ~15 MB | **29.2** | 29.2 ✓ |
| LightGBM | ~7 MB | **38.1** | 38.1 ✓ |
| Ridge | < 1 MB | **5.4** | 5.4 ✓ |

⚠ **Chapter 6 is wrong in both directions** - it understates LightGBM by a
factor of five and inverts the ordering of the two boosters. Its tracemalloc
figures are wrong too: it says LightGBM 18.7 and XGBoost 0.2; the file says 23.0
and 0.1.

**Two chapters citing one artefact with different numbers is the defect an
examiner is most likely to catch**, because spotting it needs no domain
knowledge.

### Anchor

**Section 6.3 The Forecasting Substrate (SRQ1)**, the entire final paragraph,
beginning:

> "Measured locally on the largest category (CSD), the per-model fit footprint is
> small in RSS terms:"

and ending:

> "...Component figures are consolidated in **Table 17**."

### Action

REPLACE the whole paragraph.

#### Replace with

> Peak resident memory during fitting is in the tens of megabytes for every model
> in the substrate, and the per-model figures are reported with the benchmark in
> Chapter 5. The substrate therefore operates roughly two orders of magnitude
> below the four-gigabyte ceiling. The memory budget does its work at selection
> time rather than at run time: it excludes transformer and locally hosted
> options before any of them is fitted, and leaves the footprint of the models
> eventually selected far from the constraint.

### Note - state a measurement once

Cutting the numbers rather than correcting them is deliberate. The architecture
chapter's argument needs the **conclusion** - the footprint is orders of
magnitude below the ceiling - not a second copy of the measurements. Stating
them once is also what stops them diverging again, which is how they came to
disagree in the first place.

⚠ **The artefact itself is stale**, separately from this. `profiling.csv` was
written on 1 September against a **13-feature** matrix; the current set is 18.
Chapter 5 already discloses this in Section 5.5.6 and argues the conclusion is
unaffected. Chapter 6 no longer needs to, because after this fix it quotes no
figures. Tracked as S19 on the deferred list.

---

## Fix 5 - Section 6.3, the feature description is missing half the feature set

Thread **280**: *"MISSING: the holiday api enrichment."* Correct, and
intermittency is missing too.

### Anchor

**Section 6.3**, first paragraph, the sentence beginning:

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

### Note - the count, and why it is not in the prose

The canonical list is six groups, **18 features**, in
`model_training/srq1/_features.py`. I have deliberately **not** put "18" in the
prose: Chapter 4 owns the feature count, Chapter 5 quotes it, and a third copy
is a third thing to keep in step. The description above is complete without it.

⚠ **"distribution" was wrong** in the sentence being replaced. There is no
distribution feature in the model's feature set. `weighted_distribution` exists
in the panel but is not a model input.

---

## Fix 6 - Section 6.3, sequential execution is no longer load-bearing

Thread **281**: *"Not really relevant due to the low ram usage on deploy (50mb).
As i said before, so sequential is not necessary."*

**You are right that it is not necessary.** But I recommend keeping the
sentence and changing what it claims, rather than cutting it.

### Anchor

**Section 6.3**, the paragraph beginning *"Two design decisions follow from the
RAM constraint."* Replace from that opening through to:

> "...because tracemalloc does not capture the native allocations of XGBoost and
> LightGBM."

### Action

REPLACE that span. The rest of the paragraph, from *"The substrate exposes, for
each forecast..."*, is unchanged.

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

Because it is the honest history of the design, and it is a Design Science
point rather than an engineering one. The constraint was real when the choice
was made, the choice was correct under it, and the measurement later showed the
constraint was slack. **A design chapter that reports this is stronger than one
that quietly drops the decision**, because it shows the budget actually
governing a choice.

⚠ **I have not put your 50 MB deployment figure in the prose.** I could not
find it in any artefact in the repository - it is not in `profiling.csv` and
not in the note folder. If it is measured somewhere, tell me where and it
becomes the better number to cite. If it is from the deployment rather than the
benchmark, it belongs in Chapter 7 or 8 with its own provenance, not asserted
here.

---

## Fix 7 - Section 6.4, the three properties are now measured

Thread **284** tags all three bullets VERIFY. They verify as **design
intentions**, and two of the three are now measured. This is Fix 2 of the
experiment-state note, extended.

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

### Note - why the old sentence had to change, and what it must not become

The sentence said calibration is *"a design target, not an empirically validated
property"*. **It has since been validated**: observed coverage is 83.9 to 91.7
per cent against a 90 per cent target across four categories, and the calibration
now runs against the model each category actually serves.

⚠ **Do not replace it with a claim that the intervals are informative.** They
attain their coverage guarantee and are simultaneously **very wide** - the
guarantee is marginal, and one pooled quantile spans brands of six orders of
magnitude. That finding belongs to Chapter 8 and Chapter 10. The wording above
points at both chapters without asserting either result here.

⚠ **Kuleshov et al. (2018) is dropped by this reword.** It is in Zotero
(`E4GHQL9A`) and correctly cited today, but it describes recalibration of deep
learning uncertainties, and the artefact uses split conformal. If you would
rather keep a citation here, the honest one is the conformal source Chapter 5
already uses.

### 7c - Traceability

**VERIFIED-OK, no edit.** The recording described is implemented: every run
writes a tool-call span carrying the arguments, an `args_match_request` flag and
the horizon, and the sentence claims exactly that and no more.

---

## Fix 8 - Section 6.4, the cross-reference points at the wrong chapter

This is Fix 3 of the experiment-state note.

### Anchor

**Section 6.4**, last paragraph, final clause:

> "...it is instead the baseline against which the artefact is compared (Section 5.7)."

### Action

REWORD.

#### Replace with

> ...it is instead the comparator against which the artefact is evaluated
> (Section 6.7).

### Note

Ch5/Ch6 swap residue. The section is 6.7 in this document. **Word will not
update this automatically** - it is typed text, not a field reference.

"Baseline" becomes "comparator" because the design is now a ladder in which
every rung is a comparator for the one below. See S20.

⚠ **The same defect sits in Section 6.2**, in the paragraph beginning *"The
layers are coordinated by a lightweight Python coordinator"*:
`(SRQ3, Section 5.6)` → **`(SRQ3, Section 6.6)`**.

---

## Fix 9 - Section 6.5, two claims that are not supported

The temperature claim is thread **289**, and it is correct. The Semerikov
citation is a defect I found while verifying the paragraph around it.

### 9a - the decoding claim

#### Anchor

**Section 6.5**, second paragraph, the sentence:

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

### Note - the replacement claim is the stronger one

Your comment is right: **temperature is not settable on this model.** The
harness records that fact on every run, and its pre-flight check asserts the
recorded claim matches reality before any paid run.

An examiner reading "temperature zero" expects determinism. What the artefact
offers is a **pinned dated snapshot plus a hashed prompt identity recorded per
run**, which is a different and arguably better reproducibility story because it
survives a provider changing its defaults. Claim the one that is true.

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

⚠ **Semerikov et al. (2025) is not in the Zotero library.** Verified against
the 2026-09-11 17:24 pull, 89 items, searched by author across every item type
rather than only the filtered export. It is cited **twice** in this chapter:
here, and in the Table 18 row for the remote-API choice.

Two honest options:

1. **Add it to Zotero**, if it is a real source one of you has read, and restore
   both citations.
2. **Drop it**, as the reword above does. The claim then rests on arithmetic -
   weights against a stated ceiling - which needs no citation.

The reword takes option 2 so the chapter is consistent today. **If you add the
source, revert this and keep the citation.** The same choice applies to the
Table 18 row, which Fix 11 handles.

---

## Fix 10 - Section 6.5, the delegation claim needs a boundary

Thread **288**: *"Besides in Scenarios A, B, and D."* Correct - and the
distinction is worth making precisely, because it is what the experiment
measures.

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

### Note - what your comment protects against

Without the boundary, an examiner who reaches Chapter 8 and finds a scenario in
which the language model does compute a forecast reads Section 6.5 as having
been contradicted. Naming the scope turns that into the point being tested.

⚠ **Do not name the scenarios by letter here.** Section 6.7 enumerates them,
and the letters are moving - see Fix 12 and S20.

---

## Fix 11 - Section 6.9, the table rows carry two defects and a metacomment

Thread **301** tags "(evaluated)" METACOMMENT. Two further defects sit in the
same table.

### 11a - the metacomment

#### Anchor

**Section 6.9 Technology Choices and Justification**, **Table 18**, first data
row, first cell:

> "Lightweight Python coordinator (evaluated)"

and the same row's reason cell, which ends *"...the lightweight coordinator is
leaner for the evaluated prototype under the RAM budget"*.

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
`container: auto`, which creates a fresh container per call. E2B appears in one
standalone cost-measurement script that nothing imports, and nowhere in the
experiment path.

The replacement row also carries thread **286**'s point: the sandbox is
instantiated on demand, so cost is incurred only when a query is actually sent.
Fix 13 puts the same fact in Section 6.8, where the cost argument lives.

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

**Section 6.10 Summary**, the whole section - it is one paragraph, beginning:

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

### Note - the three defects

| Was | Is |
|---|---|
| "eight-gigabyte budget" | **four** - see Fix 13 |
| "benchmarked in Chapter 6 (SRQ1)" | **Chapter 5** |
| no mention of the advisory boundary | added, matching Fix 3 |

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

**Chapter 5 says four**, in Section 5.1 and Section 5.5.6, and that was settled
deliberately. Chapter 6 should say four everywhere.

### Anchor

**Section 6.8 Memory, Cost, and Latency Budget**, the paragraph below Table 17,
beginning:

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
against the eight-gigabyte number, so correcting the budget without correcting
the percentage would leave a second error behind. I have written "under six per
cent" rather than "5.6 per cent" because 231 is itself approximate.

The final sentence answers thread **286**.

---

## Fix 14 - Section 6.7 is BLOCKED, and the smoke test is why

Thread **294**: *"I think it would help tremendously to name each scenario and
map it to the respective set-up."* **Agreed, and that is exactly what this
section should become** - but not in this pass.

### Action

**BLOCKED** until the F/G smoke test completes and the funded run is scoped.

### Note - why blocked, precisely

The harness registers **seven scenarios** as of `3c37ffd` today:

| | scenario | adds |
|---|---|---|
| A | plain language model, web search | - |
| B | + brand history in a code sandbox | what data access buys |
| C | + the trained model behind a tool | what the artefact adds |
| D | B's task on the production orchestrator | orchestrator effect on B |
| E | C's task on the production orchestrator | orchestrator effect on C |
| F | data, code **and** the model together | what code adds on top of the model |
| G | F's task on the production orchestrator | the combined arm, on production |

**F and G were smoke-testing while this pass was written and had not yet
produced rows.** The current `runs.csv` holds A through E only.

Writing the enumeration now means writing it twice, and Section 6.7 should
describe a design that has been exercised rather than one that has been
registered.

⚠ **Two things the rewrite will need, recorded now so they are not
rediscovered:**

1. **The sandbox is OpenAI's Code Interpreter, not E2B.** The current text says
   *"for example, E2B as it is used in our testing scenarios"*, and E2B is used
   nowhere in the harness.
2. **DEC-COMBINED-INPUT.** In the combined arms the model's forecast is supplied
   as one input among several, never as a starting point to revise. An agent
   handed a number and told it may keep it will mostly keep it, which would
   measure deference rather than integration.

### Note - the display labels are a defect in the harness, not the prose

While verifying the scenario names I found that the summary writer maps only
three of the seven to display labels, and **inverts the lettering** doing it:
the internal `C_model` prints as "A", and `A_plain` prints as "C". With seven
scenarios registered, D through G fall through to their raw internal names, so
one header row can mix inverted display letters with raw internal names.

**This is a code defect, and Section 6.7 cannot be written against an output
whose labels contradict its own naming.** Recorded as S21. It should be fixed
before the funded run, not after, because published tables would carry it.

---

## Fix 15 - Section 6.7, "locally" is misleading

Thread **295**: *"'locally' is a bit deceiving, because the API needs internet
access and nothing is hosted on our end, except the python code orchestrating
the data flow and supplying the API with prompts."*

**Correct.** This one sentence can be fixed now even though the section is
otherwise blocked, because it does not depend on the scenario enumeration.

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

The claim being protected is **"no production access needed"**, which is true
and load-bearing. "Locally" overstated it into "no external dependency", which
is false - the comparison cannot run without internet access and a funded API
account.

---

## Fix 16 - Section 6.9, the closing sentence and Table 18's reference

Thread **303**: `PROSE & TABLE REFERENCE`, on *"Each choice is argued against
the four-gigabyte constraint, in keeping with the design criterion of Chapter 1."*

### Anchor

**Section 6.9**, the single sentence below Table 18.

### Action

REPLACE.

#### Replace with

> Every choice in Table 18 is argued against the four-gigabyte constraint
> established in Chapter 1, and in each case the alternative was rejected for
> what it would have cost in memory or in auditability rather than for what it
> would have gained in capability.

### Note - what the comment is asking for

Two things, and the reword does both. It **names the table** rather than
gesturing at it, so the sentence still works when the table moves. And it says
something the table does not already say: the rejections share a reason. As
written, the sentence only restated the table's existence.

---

## Fix 17 - the chapter subtitle

Thread **269**: *"Could use a subtitle for the chapter."*

### Action

NEEDS-BRIAN - pick one. The placeholder text **"COULD USE A SUBTITLE"** sits
in the document body and must be deleted either way.

Chapter 6 is the design-specification chapter, and its distinguishing move is
that prediction is delegated to dedicated models behind a typed interface rather
than generated by the language model:

| Option | Reads as |
|---|---|
| **Delegating Prediction Behind a Typed Interface** | names the central design decision |
| **A Bounded Tool-Using Extension Under a Memory Budget** | names the artefact and its binding constraint |
| **From Explanation to Forecast: Extending a Production Agent** | names the capability gap the thesis opens with |

**My recommendation is the first.** It states what the chapter argues rather
than what it describes, and "delegation over generation" is the phrase Section
6.5 already uses, so the subtitle and the chapter reinforce each other.

⚠ Other chapter titles use a `Chapter N | Subject` pattern. Check whether
subtitles elsewhere are set as a separate styled line before pasting, so this
one matches.

---

# Comment ledger - all 17 threads

| Thread | Opens | Verdict |
|---|---|---|
| 269, subtitle | "Could use a subtitle" | **NEEDS-BRIAN** - Fix 17, three options, one recommended |
| 271, status note | "METACOMMENT" | **ADDRESSED** - Fix 1 |
| 272, hedging sentence | "METACOMMENT" | **ADDRESSED** - Fix 1, removed with the paragraph |
| 274, checkpoints | "Not really implemented as far as I know" | **ADDRESSED** - Fix 3a. You were right |
| 275, human oversight | "See previous comment" | **ADDRESSED** - Fix 3b |
| 280, predictors | "MISSING: the holiday api enrichment" | **ADDRESSED** - Fix 5. Intermittency was missing too |
| 281, sequential | "Not really relevant due to the low ram usage" | **ADDRESSED** - Fix 6, reframed rather than cut |
| 282, RSS figures | "VERIFY" | **ADDRESSED** - Fix 4. They were wrong in both directions |
| 284, three properties | "VERIFY" | **ADDRESSED** - Fix 7a, 7b; traceability VERIFIED-OK |
| 286, sandbox on demand | "only if queries are actually send" | **ADDRESSED** - Fix 13, and Fix 11b |
| 287, no human in loop | "No human in loop atp i think" | **ADDRESSED** - Fix 3c. Confirmed |
| 288, scenarios A/B/D | "Besides in Scenarios A, B, and D" | **ADDRESSED** - Fix 10 |
| 289, temperature | "the model we have pinned does not even accept temperature" | **ADDRESSED** - Fix 9a. Confirmed |
| 294, name the scenarios | "would help tremendously to name each scenario" | **FLAGGED** - Fix 14, blocked on the F/G smoke |
| 295, "locally" | "a bit deceiving, because the API needs internet" | **ADDRESSED** - Fix 15 |
| 301, "(evaluated)" | "METACOMMMENT" | **ADDRESSED** - Fix 11a |
| 303, closing sentence | "PROSE & TABLE REFERENCE" | **ADDRESSED** - Fix 16 |

**16 of 17 resolved in this pass.** Thread 294 is the one that waits, and it
waits on a run that is in flight.

---

# What the book chapters offer, and what I did not use

Per the standing order, I checked the forecasting textbook and the literature
already in Zotero for arguments supporting what we built.

**Nothing from the forecasting textbook belongs in this chapter.** It is a
forecasting-methods text, and Chapter 6 argues about software architecture. Its
place is Chapters 4, 5 and 8, where it is already used. Citing it here to
appear well-read would be worse than not citing it.

**Two sources in the library do apply, and I have not added either:**

| Source | Where it would go | Why not now |
|---|---|---|
| AgentOps: Enabling Observability of LLM Agents (Dong et al., 2024) | Section 6.6, the observability capability | Genuinely on point. But Section 6.6 is four sentences and has no comment on it, so adding a citation is scope I was not asked for |
| Toolformer (Schick et al., 2023) | Section 6.4, the function-calling choice | Same reasoning. Section 6.4's argument rests on reliability and auditability, which is a design claim, not a literature claim |

**Say the word and I will write either in.** Both are in the library, both are
verified, and Section 6.6 in particular is thin enough that one citation would
strengthen it. I left them out because adding citations nobody asked for, to
sections with no open comments, is how a pass grows past what can be checked.

---

# Zotero defects found while verifying

Added to S16 on the deferred list rather than fixed here, since they are library
edits rather than prose:

| Item | Defect |
|---|---|
| **Semerikov et al. (2025)** | **absent entirely**, and cited twice in this chapter. See Fix 9b |
| Sapkota, AI Agents vs. Agentic AI | date stored as `02/2` - will render wrong in the bibliography |
| Wang, Executable Code Actions | **duplicated**; one copy has date `July` instead of a year |
| Paranjape, ART | **duplicated** - `VA9UT3F9` and `paranjape_art:_2023` |
| Ahrens, Model Averaging | **duplicated** - `I86QMNYE` and `ahrens_model_2025` |
| Chen, ACGraph | date stored as `Dece` |

⚠ **The duplicates matter more than they look.** A duplicated item with two
different dates can render as two different in-text citations for one source,
and a reader checking the reference list finds the same paper twice.

---

# For the deferred structural list

**S20 - "baseline" is the wrong frame for Section 6.7.** Already raised; this
pass adds that Section 6.4 uses the word too, so the decision has two sites, not
one. Fix 8 changes 6.4 to "comparator" on the assumption the ladder framing
wins. **If you would rather keep "baseline", revert that one word in Fix 8.**

**S21 - the scenario display labels are inverted and incomplete.** New. See the
note under Fix 14. `srq4_experiment.py` maps three of seven scenarios to display
labels and inverts the lettering doing it. Should be fixed before the funded
run, because published tables would carry it.

---

# One thing I could not verify

Your comment on sequential execution cites **50 MB on deploy**. I could not find
that figure in any artefact in the repository. It is not in `profiling.csv`,
which reports 38.1 MB as the largest single fit, and it is not in the note
folder.

It is plausible as a deployed-service footprint, which is a different
measurement from a fit-time peak. **If it is measured somewhere, tell me where
and it is the better number to cite in Fix 6.** If it is an estimate, it should
not go in the prose as a figure.
