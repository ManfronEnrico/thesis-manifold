---
name: 2026-10-14_speaker-notes-draft-02
description: REFERENCE - Speaker notes for every content slide, reformatted for pasting - plain headers, no bullet markers, Final Speaker Notes left empty for the authors to fill.
category: reference
applies-to: [oral defence, slide deck, speaker notes]
triggers: [speaker notes, rehearsal, notes pass]
created: 2026_10_14-15_00
updated: 2026_10_14-15_30
snapshot_deck: 2026-10-14_14-04_pre_meeting
snapshot_thesis: 2026-10-10_16-42_deck-finalisation
supersedes: 2026-10-13_speaker-notes-draft-01.md (same content, new layout)
---

# Speaker notes, draft 02

## How to use this

Same content as draft 01, in the layout you asked for:

- **Final Speaker Notes** is left empty for you to write.
- The draft talking points that used to sit there are now the **first lines of What can be said (Suggestions)**, followed by the extra material.
- Headers carry no `#`; each is followed by a blank line.
- One point per line, with a blank line between points and no `- ` markers, so you can turn them into bullets in PowerPoint.
- Section tags like *(Ch9 §9.4)* are for you; don't read them out.
- Dividers (3, 7, 13, 16, 24, 27), the reference list (30) and the appendix title (32) are left out. Slides 20–23 share one block.
- Slides 28 and 29 currently hold a copy of slide 26's notes, so replace them completely.

---

## Slide 01 — Title (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Good afternoon. I'm Brian, this is Enrico.

Our thesis: forecast-informed agentic decision support under resource constraints, a design science study in FMCG retail.

In one sentence: we took a live AI assistant that explains past sales but can't forecast, and gave it forecasting light enough to run on a small cloud budget.

Written in collaboration with Manifold AI, whose production system is the case.

---

Content in Plain English

The chatbot can tell you what sold last month. We taught it to say what will probably sell next quarter, cheaply.

---

Practice Notes:

Under 30 seconds. Don't explain the title word by word; the next slides do that.
```

---

## Slide 02 — Agenda (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Six parts: why, what others have done, how we did it, what we built and tested, what it means, and what it can't tell us.

Then the main part: discussion with you.

Brian takes motivation, the build and limitations; Enrico takes literature, method and findings.

---

Content in Plain English

The roadmap.

---

Practice Notes:

10 seconds. Say who presents what so the hand-overs feel planned.
```

---

## Slide 04 — OUR INTEREST | Embedding Forecasting into LLMs (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Most business analytics still describes the past. Firms want to anticipate. (Stackpole, 2020)

Language-model agents are now good at describing. Pairing them with real forecasting models is new, and what exists is small and pre-review. (Chen & Bibi, 2026)

Investment is flowing in (Gartner, 2026), but cost is a key barrier to adoption (Olszak & Bartuś, 2025), and sometimes AI costs more than the people it replaced (Green, 2026).

That gap between providers and firms willing to pay is where we sit. (Newmark, 2026)

The thread through the whole thesis is cost: not "can we forecast?", but "can we forecast at a price a small provider can run?"

Chen & Bibi expose ML models as tools for LLM agents. Our thesis is the production-grade, evaluated version of that idea. (Ch2 §2.7)

---

Content in Plain English

Companies mostly look backwards with their data. AI could help them look forwards, but only if it's affordable.

---

Practice Notes:

Four of the six sources here are not in the thesis (industry and press). If challenged, fall back on the thesis's own framing: BI has served a primarily descriptive function, and cost is the binding constraint. (Ch1 §1.1)

The image is AI-generated and footnoted. Leave it that way.
```

---

## Slide 05 — BUSINESS CASE | Manifold AI (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Manifold AI builds AI agents that work as "colleagues". Prometheus is the quantitative one, deployed with Danish retailers and consumer-goods manufacturers. (abstract)

It reads Nielsen panel data, writes and runs code, and reports what happened. It does not forecast.

So our task is an extension of a live system, not a rebuild. That rules out the greenfield architectures most of the literature assumes.

The open question for Manifold: pre-trained models, or let the agent write code? That's a cost-and-accuracy trade-off, and it became our SRQ4.

Prometheus is the empirical case; its Graph Engine is the concrete integration point. (Ch3; Ch6)

Three of our seven test scenarios ran inside Prometheus itself.

---

Content in Plain English

A real company already sells an AI analyst. It can describe sales but not predict them. We worked out how to add prediction without rebuilding it.

---

Practice Notes:

If asked whether Prometheus "already forecasts" (the website mentions accuracy): it has data and can write code. Whether that's enough is exactly what we tested.

Royal Unibrew is named from Manifold's public client-cases page. The thesis itself doesn't name clients.
```

---

## Slide 06 — RESEARCH AREA | Forecasting as an extension, not a rebuild (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Five bullets, five parts of the problem, and each becomes part of a research question.

Agents explain the past, not the future.

Forecasting must be lightweight: a 4 GB memory budget for everything running at once.

Forecasts reach the agent through a structured tool, with uncertainty attached.

We test dedicated models against an LLM writing its own code, on accuracy, cost and reliability.

And it's an extension of an existing production system.

The 4 GB budget excluded transformer forecasters and locally hosted LLMs before anything was fitted. (Ch2 §2.2; Ch6)

---

Content in Plain English

Add a small, cheap forecasting engine to an existing AI assistant, and check whether it beats just letting the AI do the maths itself.

---

Practice Notes:

Don't explain each bullet in depth; the research questions slide does that. Name them and move on.
```

---

## Slide 08 — REVIEW APPROACH (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

A narrative, integrative review, not a systematic one, because our problem sits where several literatures meet, not inside one. (Saunders et al., 2023)

The search was iterative: terms per theme, taken from the research questions and refined as the questions moved. We began from a multi-agent framing and narrowed to forecast-informed, cost-justified decision support.

About a hundred records screened by title, around forty read closely, and thin themes were searched again.

Peer review prioritised: 42 sources in the chapter, 28 peer-reviewed and 14 preprints, each preprint flagged.

Preprints are included only where they're the closest available precedent, and the LLM-agent field moves faster than peer review. (Ch2 preamble)

Literature and questions shaped each other: early reading refined the questions, and the refined questions drove the next search.

---

Content in Plain English

We didn't follow a rigid checklist search. We read around the problem, kept the best and most relevant work, and searched again where we were thin. Most sources are peer-reviewed.

---

Practice Notes:

ONLY IF ASKED, "Chapter 3 calls it a systematic review": "Chapter 2's description is the accurate one: a structured, iterative search, but not a systematic-review protocol. 'Systematic' in Chapter 3 is loose wording." Don't deny it.

The old note said "eight sections, 2.8 paradigm". That's wrong (the chapter has ten sections). Don't use it.
```

---

## Slide 09 — FIVE STRANDS (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Read across each row: what each literature gives us, and where it stops.

Retail forecasting gives the method: gradient boosting won M5, and training across many series beats one model per series. But it's accuracy-first; compute is secondary.

Forecast-to-decision shows forecasts create value through decisions, but couples the two tightly, through optimisation, and doesn't involve LLM agents.

LLM agents and tool use: delegating to tools can substitute for model size. Nothing on forecasting or production.

Reliability: agent outputs carry measurable risks; the requirements are there but not the integration.

Production agentic systems: feasible, but built for live process supervision on dedicated hardware.

The line below: each stops short of the same point. That point is our gap.

M5's cross-learning result is the direct precedent for our pooled-versus-per-category comparison in SRQ1. (Ch2 §2.1)

---

Content in Plain English

Five research areas each solve a piece. None puts the pieces together for a real, budget-limited business AI.

---

Practice Notes:

Don't read all five rows. Pick two (retail and LLM agents), then land the bottom line.

If asked "five strands, but slide 11 shows four?": retail forecasting is the method source (§2.1); the gap is the intersection of the other four (§2.7).
```

---

## Slide 10 — RESEARCH QUESTION (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Read the question in full, slowly.

Then name the words that carry it: production-oriented, meaning a live system, extended rather than rebuilt; lightweight, meaning the 4 GB budget; reliable; and cost-justified, which is where our findings land.

"Without native predictive capabilities" is Prometheus today. "Cost-justified" is answered by SRQ4.

---

Content in Plain English

How do you add forecasting to a working business AI so that it's trustworthy, affordable and fits the hardware?

---

Practice Notes:

Pause after reading it. Let it land before explaining.
```

---

## Slide 11 — THE GAP (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Four literatures, each well populated, each stopping short of the same point. (Ch2 §2.7)

Agents that explain, not forecast: a production system with no predictive capability.

Extend, don't rebuild: lightweight models added inside the existing system.

Loosely coupled through a tool: the agent asks, the model answers, every figure is traceable.

Tested against the obvious alternative: an LLM writing its own forecasting code.

"Loose" means the model never sees the conversation and the agent never sees a feature vector. (Ch6)

We hold ourselves against a strong baseline, a code-writing agent, not against nothing. (Ch1 §1.3)

---

Content in Plain English

Nobody has yet shown how to plug a proper forecasting model into a live business chatbot cheaply, and checked whether it's better than the chatbot doing the maths itself.

---

Practice Notes:

The figure's alt text says "Reasearch" (typo, not on screen).
```

---

## Slide 12 — THE RESEARCH QUESTIONS (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

One main question, four sub-questions, one per layer of the extension.

SRQ1, the substrate: which lightweight models trade accuracy against memory best. (Ch5)

SRQ2, the interface: how a forecast reaches the agent with reliability, uncertainty and traceability intact. (Ch6–7)

SRQ3, the host system: what a production agent must already do before forecasting can attach. (Ch7, Ch9)

SRQ4, the evidence: does a dedicated model beat an agent writing its own code, at justified cost? (Ch8)

SRQ2 and SRQ3 are framed as principles and criteria rather than descriptions of what we built. That's what makes them transferable. (Ch3)

Bridge: four questions about designing something make a design problem, not a hypothesis test. That's why the method is Design Science.

---

Content in Plain English

Which forecasting model; how it talks to the chatbot; what the chatbot needs to be ready; and is it worth it.

---

Practice Notes:

Use the bridge sentence to hand over to methodology.
```

---

## Slide 14 — METHODOLOGY | Central Academic Grounding (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Three columns, three sources of rigour. One line from each.

Research: pragmatism. A claim is judged by what it enables. Demand is real, and the panel measures it imperfectly. A quantitative experiment within a single embedded case. (Ch3 §3.1, §3.3)

Forecasting: the test split is never seen during selection; wMAPE is primary, with median APE and MASE alongside; naive and seasonal naive are the floor. (Ch3; Ch5 §5.4.4, §5.5.1)

Design science: we deliver an artefact and design knowledge, and both are assessed. Relevance from Manifold, design across Chapters 5–8, rigour from Chapter 2. (Hevner et al., 2004; Hevner, 2007; Peffers et al., 2007)

wMAPE weights by volume, so big brands count more. Percentage errors break on near-zero demand, which is why median APE and MASE sit alongside it. (Ch5 §5.5.1)

Commercial panel access is a strength: data we couldn't have collected ourselves. (Ch3; Saunders et al., 2023)

---

Content in Plain English

We judge the work by whether it's useful; we test forecasts only on data the model never saw; and we build something real and extract lessons others can reuse.

---

Practice Notes:

Don't read the bullets.

If asked about exponential smoothing: deliberately omitted, recorded as a limitation, not a verdict on the method. (Ch3; Ch5)

If asked about "not novelty": Ch3 says DSR judges knowledge by whether the artefact achieves its design objectives. Stand on that.
```

---

## Slide 15 — METHODOLOGY | Summarized Approach (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Pragmatism grounds the choice of Design Science.

Peffers' six activities map onto the chapters: problem in Chapters 1–2; objectives as the four sub-questions; design in 5–6; demonstration in 7; evaluation in 8; communication is the thesis itself. (Ch3)

Each sub-question has its own evaluation protocol, so each answer is judged on its own terms.

Evaluation in Chapter 8 covers accuracy, computational efficiency, recommendation quality, and comparison with a code-writing LLM baseline. (Ch3)

---

Content in Plain English

Here's the plan of the whole thesis on one page, and where each step happens.

---

Practice Notes:

Point at the figure as you name each activity. Then hand over to Brian.
```

---

## Slide 17 — DATA ASSESSMENT | Preprocessing Pipeline (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Nielsen scanner data, four Danish beverage categories: soft drinks, water, energy drinks, ready-to-drink. (Ch4 §4.1)

Aggregated to brand by month.

The data contract is measured from the panel, not assumed: minimum history, lag depth and transformation follow from the data.

At the three-month horizon that leaves 95 brands for soft drinks, 44 energy drinks, 29 water, 62 ready-to-drink.

41 to 46 monthly periods per category: three to four annual cycles. (Ch3; Ch4)

Beer was available but excluded: its table was an order of magnitude larger than our bandwidth and compute allowed. (Ch4 §4.1)

---

Content in Plain English

We took raw till-receipt data from shops, cleaned it, and turned it into monthly sales per brand.

---

Practice Notes:

The counts on the figure are for the largest category (soft drinks).
```

---

## Slide 18 — DATA ASSESSMENT | Exploratory Data Analysis (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Soft drinks is the worked example; every category goes through the same four lines of enquiry.

Structure and quality; brand coverage and retention; stationarity and seasonality; candidate demand drivers and their redundancy. (Ch4 §4.2)

The findings set the data contract, so lag depth, series length and transformation follow from the data, not from convention.

A log transformation is applied uniformly, not per brand: per-brand estimation isn't supportable at about 46 observations. (Ch4 §4.2.2)

The analysis finds a clear annual cycle. (Ch4 §4.2.4)

---

Content in Plain English

Before modelling, we looked hard at the data to decide what the model should use.

---

Practice Notes:

Don't bring up the lag-13 point here. It has a prepared answer on slide 28, and only if asked.
```

---

## Slide 19 — MODELLING & EXPERIMENT | Combined Overview (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Three layers. Bottom: models benchmarked on identical data, one deployed per category.

Middle: a typed tool that returns the forecast with an interval, the model's measured error and its provenance.

Top: the agent, which asks for a forecast and gets one back with its evidence attached.

The one decision that carries SRQ2: the language model never handles a feature vector. (Ch6; Ch7)

The LLM is reached over an API, so the 4 GB goes to data and models; the heaviest model needs 34.5 MB to fit. (Ch5 §5.6.6)

Train once, serve many: the tool loads models and never fits them.

The tool refuses in three cases rather than guessing: unknown category, a brand with no held-out data, a month outside the test split. (Ch7 §7.2.3)

---

Content in Plain English

The AI doesn't do the maths. It phones a specialist model and gets the answer, plus how sure the model is and how well it has done before.

---

Practice Notes:

The figure caption says 34 MB (a rounding artefact). Say "thirty-four and a half".

If asked why the budget matters when you use about 1% of it: it ruled out which architectures we could consider, not run time. (Ch6; Ch9 DP4)
```

---

## Slides 20–23 — EXPERIMENT | Performance Overview (Brian)

Paste the same notes on all four; the build cue at the top tells you where you are.

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Build: 20 plain; 21 worst per row in red; 22 middle in orange; 23 best in green.

Seven scenarios, one ladder, each adding one thing. Left: our local orchestrator. Right: the same rungs inside Manifold's production platform.

A to B, data access alone: median error from 502% to 2.9%. The biggest step on the ladder. (Ch9)

B to C is our step, and it doesn't go the way you'd expect: worse on the median (14.6 vs 2.9), better on the mean (13.1 vs 27.9).

What C buys: about 50 times cheaper, about 20 times faster, and identical on every repeat. (Ch8; Ch9)

No scenario leads on every axis.

The code agent "wins on the axis usually reported and loses on three that usually are not." (Ch9 §9.2.3)

A plain LLM with no data invents numbers: 502% median error, and only 6 of 9 usable answers.

Combining everything (F, G) doesn't simply take the best of both: the agents depart from our forecast and invent their own weighting. (Ch8; Ch9)

---

Content in Plain English

Giving the AI data helps hugely. Giving it our model makes answers cheap, fast and identical every time, though not always the most accurate on a typical question.

---

Practice Notes:

Scenario D (the code agent inside production) has the best median, 0.9%. If asked: it costs about 84 times more than C, is about 19 times slower, and was never identical across repeats.

ONLY IF ASKED about "Runs in": all seven use the same model, GPT-5.5. What differs is the orchestrator (ours or Manifold's). (Ch3; Ch9 §9.2.3)

63 runs: 7 scenarios × 3 brands × 3 repeats.
```

---

## Slide 25 — FINDINGS (Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

One row per sub-question, and every row carries a caveat we put there ourselves.

SRQ1: gradient boosters beat Ridge and ARIMA in all four categories, and fit in 35 MB of 4 GB. But we won't name XGBoost over LightGBM: five seeds flip the winner in every category. And two categories lose to simple benchmarks. (Ch5; Ch10 §10.1)

SRQ2: every figure the agent reported matched what the tool returned. The interval is honest but 8–34 times the forecast, so the model's track record carries reliability, not the interval. (Ch7; Ch9)

SRQ3: three of seven scenarios ran inside production, so readiness comes from what integration actually needed. The remaining gap is operational: credentials and a merge. (Ch9; Ch10 §10.1)

SRQ4: data access alone does most of the accuracy work; dedicated models win on replicability, cost and latency; code wins on the median.

Pooling across categories wins on the two smallest by 4.5 to 5.7 percentage points. (Ch5; Ch9)

At 80% the interval narrows to a workable 3–4× for three categories. (Ch9)

Which to deploy: the dedicated model where an answer must be reproducible, auditable and cheap; the code agent for one-off analysis a person will read. (Ch9 §9.1.5)

---

Content in Plain English

The small models work and fit easily. The AI always repeats our numbers faithfully. The range of uncertainty is too wide to be useful, so we pass on how accurate the model has been instead. Our approach is cheapest and most consistent, but not always the most accurate.

---

Practice Notes:

Benchmarks: seasonal naive on ready-to-drink, Prophet on water. Prophet is not parameter-free; don't call it that.

Coverage, only if asked: at 90%, met for soft drinks (91.7) and ready-to-drink (91.4); short for water (83.9) and energy drinks (86.7), because there are too few months to calibrate.

Close the slide on: "The contribution is qualified, and the qualification is the point." (abstract)
```

---

## Slide 26 — CONTRIBUTIONS | Five Design Principles (Enrico)

Your existing notes, completed.

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Beyond the artefact, design science asks what transfers. These five principles are that knowledge.

Each is backed by a measurement: if the principle were wrong, our results would have come out differently.

Delegation over generation: tool-backed answers were identical on every repeat; code-written answers were never identical.

Explicit refusal over silent fallback: a fallback looks like a real answer, and an agent can't tell.

Carry the track record: the interval is too wide; the measured error is what carries reliability.

Budget memory at selection time: 4 GB ruled out transformers up front; the realised end-to-end peak was about 231 MB.

Report cost and latency: about a fifty-fold cost difference at comparable accuracy.

Close on the sentence at the top.

Design science says an artefact only becomes a contribution when the knowledge inside it is stated separately. These five are that knowledge. (Ch10 §10.2; Hevner et al. 2004)

Each is stated for a kind of problem, not for our system, so someone building something similar can use them. (Ch9 §9.2.2)

---

Content in Plain English

Delegation over generation	Don't let the chatbot invent the number. Let it fetch the number from a model built for the job.

Explicit refusal over silent fallback	If the tool can't answer, it should say "I can't" rather than quietly give a substitute. The chatbot would pass the substitute on as if it were real.

Carry the track record		A forecast should come with "here's how accurate this model has been before", because a range like "between 100 and 3,000" doesn't help anyone.

Budget memory at selection time	Use the memory limit to rule out heavy models before building anything, then report what you actually used.

Report cost and latency		Two approaches can be equally accurate and differ fifty-fold in price. If you only measure accuracy, you'd never see that.

---

Practice Notes:

Pick one to explain, not all five. The best is the first: when a number has to be the same every time you ask, let the language model ask a model for it rather than calculate it itself.

Close on the sentence at the top. It's the thesis's final statement, nearly word for word. (Ch10 §10.6)

ONLY IF ASKED "comparable accuracy?": code wins on the median, our model on the mean (13.1 vs 27.9); neither dominates on accuracy.

ONLY IF ASKED "how general are these?": "derived rather than validated across contexts", one design cycle, one company. (Ch10 §10.4)
```

---

## Slide 28 — LIMITATIONS (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

What bounds our claims, five rows.

Sample: 7 scenarios × 3 brands × 3 repeats, 63 runs in one category. Sized to detect large differences only. (Ch3 §3.3; Ch9 §9.4)

Forecasting practice: our classical baseline lacks exponential smoothing and a seasonal term, and the code agents used both on every run.

Per-series adaptation: code agents fit per brand, our model per category, so where they win, the two effects can't be separated.

Intervals: too wide to act on for any individual brand; implausible forecasts are clipped after back-transformation rather than prevented by it.

Planner decisions and hierarchy: we didn't test whether a human planner decides better, and brand forecasts aren't reconciled with category totals.

We tried three alternative calibrations; none improved coverage and width together in more than two of four categories. That's a sample-size limit, not a modelling choice. (Ch9)

Each limitation has a matching next step on the next slide.

---

Content in Plain English

We tested on a small slice, our baseline missed two standard tricks, and we didn't test real planners. These are the honest edges of the result.

---

Practice Notes:

ONLY IF ASKED about lags or seasonality (about 20 seconds, then stop):

"The analysis found a yearly pattern, but the model's lag settings never picked up the value from the same month last year. The model still knows which month it is forecasting, through the calendar features, so seasonality isn't missing entirely; it's weaker than it could be. It's listed in Chapter 9, and fixing it would only make our model more accurate, so it doesn't change our conclusion."

Never say "off by one month": at the three-month horizon it's three.

Don't claim it was noticed before submission.

If asked which limitation worries us most: the hierarchy. Reconciliation is cheap and established, and §9.4 concedes it "would very likely improve accuracy at every level".
```

---

## Slide 29 — FUTURE WORK (Brian)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

What the next design cycle closes: "Five directions follow from what this evaluation could not settle." (Ch9 §9.5)

Add exponential smoothing and a seasonal term, the two techniques the code agents used unprompted on every run. Until then the comparison isn't settled.

Send a per-series error, not one per category, so a combined agent has something to weight our forecast by.

Reconcile brand forecasts against category and market totals. One estimator needs no residual history, so it works for agent forecasts too.

Widen the evaluation: more categories, more repeats, before any accuracy claim.

Test whether a communicated forecast improves a planner's decision. That's a different study, with human participants. (Goodwin, Önkal & Thomson, 2010)

Goodwin et al. found that bare intervals don't improve planning decisions and can degrade them, which is why we send the track record rather than the interval alone. (Ch7)

---

Content in Plain English

The obvious next steps: give our model the same tricks the AI used, test on more data, and test with real people.

---

Practice Notes:

Keep it brisk, then hand over to the closing slide.
```

---

## Slide 31 — Let's discuss! (Brian or Enrico)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

One line before questions: "A dedicated forecasting layer must be justified on reproducibility, cost and auditability, not on error alone."

Thank you. We look forward to your questions.

"It wins on the axis usually reported and loses on three that usually are not." (Ch9 §9.2.3)

---

Content in Plain English

Our model isn't always the most accurate, but it's cheap, consistent and checkable, and for a business that's what matters.

---

Practice Notes:

Stop talking after the line. Let the examiners open.
```

---

## Appendix 33–40 (backup, only if asked)

The slides are self-explanatory, so these notes are short. Paste one per slide.

```text
33 Data Pipeline — Raw extract to modelling matrix, four categories, brand × month. Same pipeline for every category; one orchestrator, not per-category copies.

34–36 Raw Nielsen Dataset Schema — The star schema as delivered. Commercial data under licence; it never leaves the local environment.

37 Modelling Pipeline — Each candidate is fitted on the same data under two arms: one model per category, and one pooled model with category as a feature. Neither arm dominates: category-specific wins in 2 of 4, pooled in the rest, so the choice is per category. The winner is retrained on the full training window and deployed.

38 Resource Profile — Peak memory during fitting: XGBoost 34.5 MB, LightGBM 17.9, Ridge 1.5, Prophet 5.2, ARIMA 2.1. Against 4 GB. (Ch5 §5.6.6)

39 Model Performance — Untuned ladder (not a thesis figure). If asked why it says every model beats seasonal naive: this is before tuning; the tuned results in Chapter 5 show two categories losing to simple benchmarks.

40 Forecast Overlay — XGBoost on Harboe, the largest soft-drinks brand: forecast against actuals on the held-out months. (Thesis Fig. 6)
```
