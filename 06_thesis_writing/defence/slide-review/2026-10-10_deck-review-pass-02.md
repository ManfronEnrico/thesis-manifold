---
name: 2026-10-10_deck-review-pass-02
description: REFERENCE - Finalisation pass on the defence deck. Answers the three open comments, adds new fact-check findings, and drafts speaker notes for every presented content slide, each grounded in a thesis section.
category: reference
applies-to: [oral defence, slide deck]
triggers: [finalise the deck, speaker notes, fact check slides]
created: 2026_10_10-17_10
updated: 2026_10_10-18_05
snapshot_deck: 2026-10-10_16-39_finalise_and_divide
snapshot_thesis: 2026-10-10_16-42_deck-finalisation
follows: 2026-09-20_deck-review-pass-01.md
---

# Deck review — pass 02 (finalisation)

## What was checked, and against what

| Surface | State |
|---|---|
| Deck | `2026-10-10_16-39_finalise_and_divide` — **slide content identical to 20 Sept**; the only change is three comments by Brian (slides 13, 23, 25) |
| Thesis | `2026-10-10_16-42_deck-finalisation` — **byte-identical to 20 Sept** (47,139 words, 0 comments) |
| Zotero | re-pulled 2026-10-10, 88 items |
| Repository | `b9a97fc`, in sync with origin |

**So pass 01 stands in full, and none of its fixes have been applied yet.**
This note does not repeat them; the checklist below points back to them.
Everything after that is new.

Numbering: sections and items carry `1.1`-style numbers for cross-referencing; pass-01 items are cited by their own labels (A1, 8a, 21c...).

---

# 1 Still open from pass 01

Tick these off in PowerPoint. Detail and paste-ready text are in pass 01.

| | Slide | Fix | Pass 01 |
|---|---|---|---|
| ☐ 1.1 | 15 | `Saunders et al. (2021)` → **2023** | A1, 15a |
| ☐ 1.2 | 8 | `~150 / ~60` → **~100 / ~40** | A2, 8a |
| ☐ 1.3 | 20, 23 | memory: say **34.5 MB** (or 35) — not 34 | A3 (and 3.1 below) |
| ☐ 1.4 | 8 | `61 sources cited` → **42 in this chapter, 62 across the thesis** — closes Enrico's comment | 8b |
| ☐ 1.5 | 8 | notes: chapter has **ten** sections; 2.8 is Contributions, **2.9** is DSR | 8c |
| ☐ 1.6 | 9 | `Adress` → Address; row 4 drop **"at scale"**; row 5 gap cell is unsourced | 9a–9c |
| ☐ 1.7 | 10 | RQ in quotation marks is **not verbatim** — restore it or drop the quotes | 10 |
| ☐ 1.8 | 15 | `MdAPE` → **median APE**; three cycles are **Hevner (2007)** | 15c, 15d |
| ☐ 1.9 | 15, 16 | `METHDOLOGY` → METHODOLOGY | 15b |
| ☐ 1.10 | 21 | `51× / 21×` → **~50× / ~20×** (matches slide 23 and the thesis) | 21a |
| ☐ 1.11 | 23 | "across the whole evaluation" → **"in every run where the tool was called"** | 23b |
| ☐ 1.12 | 2 | agenda is missing **DISCUSSION** | Slide 02 |

---

# 2 Your three comments

## 2.1 — Slide 13 "approach": *"DESIGN & KEEP?: Still Ugly. Also do we still need this?"*

### Answer: delete it.

The slide's entire content is the word `approach` and the word `Relevant literature`.
It sits between the research-question tree (12) and the Methodology divider (14),
so it introduces nothing that follows it. Everything it might have said is already
said: the review method is slide 8, the strands are slide 9, the gap is slide 11.

If you want a bridge into Methodology, put it in slide 12's notes instead (see
§4): *"Four questions, one per layer — which makes this a design problem, not a
hypothesis test. That is why the method is Design Science."*

---

## 2.2 — Slide 23 Findings: *"DESIGN: Still Ugly. Also Double Check with Thesis Prose"*

### Verdict: all four rows are faithful to Ch10 §10.1 — two fixes, one addition.

Each row checked sentence by sentence against Ch10's SRQ paragraphs (which are
the source; Ch9 §9.1 is the long form).

| Row | Claim on slide | Verdict |
|---|---|---|
| SRQ1 | boosters beat Ridge and ARIMA in all four; seed changes the winner in all four; two categories beaten by parameter-free benchmarks | **CONFIRMED** — Ch10 §10.1 near-verbatim |
| SRQ1 | "fitting peaks at 35 MB" | **CONFIRMED** — Ch10 and the abstract both say *"thirty-five megabytes"*. Slide 23 is right; slide 20 is the outlier |
| SRQ2 | every reported figure matched the tool payload | **CONFIRMED but exposed** — see pass 01 §23b |
| SRQ2 | interval 8–34× the forecast at 90% | **CONFIRMED** — Ch9 §9.2.2 DP3 |
| SRQ3 | three of seven scenarios in production; gap is credentials and a merge | **CONFIRMED** — Ch9 §9.1.3, Ch10 §10.1 |
| SRQ4 | 502% → 2.9%; ~50× cost, ~20× speed, zero variance | **CONFIRMED** — Ch10 §10.1 |

### What the slide leaves out of SRQ1

SRQ1 asks about accuracy, memory **and category specialisation**. The slide answers
the first two only. The thesis's answer to the third:

> *"Category specialisation is conditional on panel size: pooling across categories
> wins on the two smallest by four to six percentage points and is indecisive on the
> larger two."* — Ch10 §10.1 (Ch9 §9.1.1 gives **4.5 to 5.7 pp**)

Not necessarily on the slide — the cell is already full — but it belongs in the
notes, because an examiner reading SRQ1's wording will notice the third clause is
unanswered.

### Design suggestion only

The table is 4 rows × 2 long sentences, every cell bold. Un-bolding everything except
the first clause of each cell (*"Both gradient boosters beat Ridge and ARIMA"*,
*"Reliability holds by construction"*, …) gives the eye a scannable left edge.

---

## 2.3 — Slide 25 Limitations: *"DESIGN: Still Ugly. Also Double Check with Thesis Prose"*

### Verdict: 9 of 10 items faithful to Ch9 §9.4 / §9.5. One bullet merges two unrelated limitations.

The slide follows **Ch9, not Ch10** — Ch10 §10.4/§10.5 recap a different five.
Don't "fix" it against Ch10.

**Future work: all five CONFIRMED**, in the thesis's own order, several near-verbatim.

**Limitations:** §9.4 announces *"Five limitations"* and then has **seven**
paragraphs. The slide's five headings group them as 1 + (2+3) + 4 + 5 + (6+7). Items
2 and 4 merge paragraphs the thesis itself links (*"a further asymmetry inside the
substrate"*, *"a related limitation of a different kind"*). **Item 5 does not:**

> **Planner Decisions and the Mixed Hierarchical and Grouped Structure**

joins *"no human-decision study"* (para 6) and *"hierarchical reconciliation never
applied"* (para 7). Para 7 opens *"One structural property of the panel is left
entirely unexploited"* — a fresh start, not a continuation. No sentence in the
thesis connects them.

#### Action — split item 5 into two

> - **Planner Decisions Untested**
> - **Hierarchical and Grouped Structure Unexploited**

### Why it's worth the edit: the lists pair, and the slide hides it

§9.5 opens *"Five directions follow from what this evaluation could not settle"* —
each future-work item is the remedy for a limitation:

| Limitation | → | Future work |
|---|---|---|
| 1 Sample size | → | 4 Widen across categories and repeats |
| 2 Forecasting practice | → | 1 Exponential smoothing + seasonal term |
| 2′ Asymmetry inside the substrate (lag 13) | → | *none* |
| 3 Per-series adaptation vs code execution | → | *none directly* |
| 4 Interval width | → | 2 Per-series error, not per-category |
| 5a Planner decisions | → | 5 Does a forecast improve a planner's decision |
| 5b Hierarchical structure | → | 3 Reconcile brand forecasts against aggregates |

**5b → 3 is the tightest pair in the thesis**, and it's hidden inside a bullet
headed "Planner". With item 5 split, consider re-ordering future work so each sits
beside its limitation — then the slide says *"every limitation has a next step"* on
its own.

### ⚠ The lag-13 defect is already on this slide

*"Asymmetry inside the Substrate"* **is** the lag-13 defect (§9.4 para 3). The deck
names it, quietly. A committee member who reads §9.4 will ask. The answer is in the
thesis: *"a gap of provenance between the analytical and engineering layers rather
than of method"* — and see §4's notes for slide 25.

**Which limitation worries us most?** The thesis doesn't rank them. Honest answer:
the hierarchical one — it's the only place where an established, cheap method
existed and wasn't applied, and §9.4 concedes reconciliation *"would very likely
improve accuracy at every level"*.

---

# 3 New fact-check findings

## 3.1 — Slide 20: why the caption says 34 MB

The note is the figure's own caption, generated by
`generate_architecture_diagrams.py`, which prints `{largest:.0f}` on **34.5**.
Python rounds half to even, so it prints **34**. The thesis prose says 34.5 (Ch5,
Ch9) and 35 (Ch10, abstract).

**Nothing to change in the thesis.** If the caption is visible on the projected
figure, just say *"thirty-four and a half"* aloud. In the notes, correct to 34.5.

There is also a third number: **Ch6's memory table says XGBoost 31.9 MB**, from a
separate profiling run. Immaterial (0.78% vs 0.84% of 4 GB), already drilled in
`qa-drill.md` (P0056 F9). Don't put it on a slide.

## 3.2 — Slide 4: four of six sources are not in the thesis

| Source on slide 4 | In the thesis reference list? |
|---|---|
| Stackpole (2020) | **no** |
| Chen & Bibi (2026) | yes |
| Gartner (2026) | **no** |
| Olszak & Bartuś (2025) | yes |
| Newmark (2026) | **no** |
| Green (2026), Forbes | **no** |

Introducing sources at the defence is allowed — slide 26 lists them, which is the
right thing to do. But the examiners can't check them against the thesis, and two
are a vendor press release and a magazine column. If one is challenged, fall back
to what Ch1 §1.1 actually argues:

- BI has served *"a primarily descriptive function"* — the thesis's own framing
- the binding constraint is cost: *"transformer-based forecasters and locally hosted
  language models require accelerator memory measured in tens to hundreds of
  gigabytes… an order of magnitude more expensive"* (Ch1 §1.1)

**The AI-generated image** is footnoted as AI-generated, which is correct and
necessary. Keep the footnote.

## 3.3 — Slide 5: "Royal Unibrew" appears nowhere in the thesis

The thesis says Manifold AI's system is *"deployed with Danish retailers and
consumer-goods manufacturers"* and never names a client. Check that naming one is
cleared with Manifold — the thesis's own restraint suggests it may not be.

## 3.4 — Three things the thesis claims as contributions that the deck never shows

The abstract names the contributions: *"a working artefact, five design principles
for extending non-predictive agentic systems with forecasting, and an evaluation
design that measures cost and latency beside accuracy."* The deck shows the first
and third. **The design principles never appear.** Nor do two strong closing lines.

| What | Where in the thesis | Suggested home |
|---|---|---|
| **Five design principles, DP1–DP5** (*"Delegate prediction; do not generate it"*, *"Refuse explicitly rather than fall back"*, *"Carry the model's track record, not only its interval"*, *"Budget memory at selection time, report it at run time"*, *"Report cost and latency beside accuracy"*) | Ch9 §9.2.2, Table 28 | One content slide in Section 06 — **this is the DSR "transferable design knowledge" that slide 15 promises** |
| **Which configuration to deploy** — the dedicated model where an answer must be reproducible, auditable and cheap; the code agent for one-off analysis a human will read | Ch9 §9.1.5 | Slide 23 notes, or the closing line |
| *"It wins on the axis usually reported and loses on three that usually are not."* | Ch9 §9.2.3 | Closing sentence before "Let's discuss" |

The first matters most. Slide 15 says DSR's consequence is *"build an artefact and
produce transferable design knowledge; both are assessed"*. If the knowledge is
never shown, the examiner has only the artefact to assess.

---

# 4 Speaker notes, slide by slide

Bullets to speak from, not a script. **Each bullet is grounded in the section
named after it**, so you can check or expand it. Slides not listed are dividers,
the reference list, appendix or backup.

The 13 slides whose notes field currently holds a pasted figure caption: the
caption is already in the alt text, so **replace it** rather than add beneath it.

---

### 4.1 Slide 04 — OUR INTEREST | Embedding Forecasting into LLMs

- Business analytics has mostly told companies what already happened. The
  interesting move is from describing the past to anticipating it. *(Ch1 §1.1)*
- Language-model agents are now good at the describing part. Pairing them with
  dedicated forecasting models is new, and the work that exists is small and
  pre-review. *(Ch2 §2.7: Chen & Bibi 2026, "small, non-peer-reviewed proofs of
  concept")*
- And cost is what decides whether a firm adopts any of this — which turns out to
  be the thread through the whole thesis. *(Ch1 §1.1)*

### 4.2 Slide 05 — BUSINESS CASE | Manifold AI

- Manifold AI builds "AI Colleagues". Prometheus, the quantitative one, is in
  production with Danish retailers and consumer-goods manufacturers. *(Ch1 §1.2;
  abstract)*
- It reads Nielsen panel data and reports volumes, shares and distribution. It does
  not forecast. *(Ch1 §1.2: "does not forecast, anticipate, or recommend")*
- So the task is an **extension of a live system, not a rebuild** — which rules
  out the greenfield architecture most of the literature assumes. *(Ch1 §1.2)*
- *If asked about the website's "enhances forecasting accuracy":* it has data access
  and can write code. Whether that is enough is precisely what SRQ4 tests.

### 4.3 Slide 06 — RESEARCH AREA | Forecasting as an extension, not a rebuild

- Five things define the problem, one per bullet. Each becomes a research question
  later.
- The constraint is concrete: **4 GB of RAM** for everything running at once. That
  excludes transformer forecasters before anything is fitted. *(Ch1 §1.4)*
- And the question we put to ourselves: is a dedicated model even needed, now that
  an LLM can write its own forecasting code? *(Ch1 §1.3, SRQ4)*

### 4.4 Slide 08 — REVIEW APPROACH

- A narrative, integrative review — not a systematic one — because the contribution
  sits where several literatures meet, not inside one. *(Ch2 preamble, Saunders et
  al. 2023)*
- Search terms per theme, from the research questions. **About a hundred records
  screened by title, around forty read closely**, and themes that came out thin
  went back for another round. *(Ch2 preamble)*
- Peer review prioritised; preprints only where they're the nearest precedent, and
  flagged. **Forty-two sources in this chapter, sixty-two across the thesis.**
- Keep the existing note's first paragraph (scope refined as the questions moved).
  Replace the second with pass 01 §8c.

### 4.5 Slide 09 — FIVE STRANDS

- Read across each row: what the literature gives us, and where it stops.
- Every strand is well populated. **None reaches the point where all of them meet** —
  extending a production agent with forecasting under a small provider's budget.
  *(Ch2 §2.7)*
- Retail forecasting gives the method: gradient boosting won M5 and training across
  series beats one model per series. That's the precedent for our pooled-vs-category
  comparison. *(Ch2 §2.1)*
- Forecast-to-decision couples the two tightly, through optimisation. We couple them
  loosely, through an agent. *(Ch2 §2.7)*

### 4.6 Slide 10 — RESEARCH QUESTION

- Read it in full. Then name the three words that do the work: **production-oriented**
  — an extension of a live system; **lightweight** — the 4 GB budget; and
  **cost-justified** — which is where the findings will land.
- *(Only if you restore the full RQ — see pass 01 §10.)*

### 4.7 Slide 11 — THE GAP

- Keep the existing note. Add:
- Four literatures, each stopping short of the same point. *(Ch2 §2.7)*
- "Loose, agent-mediated": the agent decides when to ask for a forecast; the model
  never sees the conversation and the agent never sees a feature vector. *(Ch2 §2.7;
  Ch6)*
- "Code-as-action baseline": we hold ourselves against an LLM writing its own
  forecasting code, not against nothing. *(Ch1 §1.3.3)*

### 4.8 Slide 12 — THE RESEARCH QUESTIONS

- One main question, four sub-questions — **one per layer of the extension**:
  the models, the interface, the host system, and the evidence that it's worth it.
  *(Ch1 §1.3)*
- SRQ2 and SRQ3 are framed as principles and criteria rather than descriptions of
  what we built — that's what makes the contribution transferable. *(Ch3)*
- Bridge: four questions about designing something is a design problem, not a
  hypothesis test. That's why the method is Design Science. *(replaces slide 13)*

### 4.9 Slide 15 — METHODOLOGY | Central Academic Grounding

- Three columns, three sources of rigour. Don't read the bullets; take one line from
  each.
- **Research:** pragmatism — a claim is judged by what it enables. *(Ch3, Saunders et
  al. 2023)*
- **Forecasting:** the test split is never seen during selection *or* calibration,
  and the naive benchmarks are the floor everything must clear. *(Ch3 §3.5.1; Ch5)*
- **Design science:** we produce an artefact *and* transferable design knowledge,
  and both are assessed. Relevance cycle from Manifold, rigour cycle from Chapter 2.
  *(Ch3 §3.2; Hevner et al. 2004, Hevner 2007)*
- *If asked about exponential smoothing:* omitted deliberately and recorded as a
  limitation, not a verdict on the family. *(Ch3 §3.5.1; Ch5 §5.1)*

### 4.10 Slide 16 — METHODOLOGY | Summarized Approach

- Replace the caption with:
- Peffers' six activities map onto the chapters: problem in 1–2, objectives as the
  four sub-questions, design in 5–6, demonstration in 7, evaluation in 8. *(Ch3 §3.2)*
- Each sub-question gets its own evaluation protocol, so each answer can be judged on
  its own terms. *(Ch3)*

### 4.11 Slide 18 — DATA ASSESSMENT | Preprocessing Pipeline

- Replace the caption with:
- Nielsen scanner data, four Danish beverage categories, aggregated to **brand by
  month**. *(Ch4 §4.1)*
- The data contract is **measured from the panel**, not assumed — minimum history,
  lag depth, transformation all follow from what the data shows. *(Ch4 §4.2)*
- At the three-month horizon that retains **95 brands for soft drinks, 44 energy
  drinks, 29 water, 62 ready-to-drink.** *(Ch4 §4.1)*

### 4.12 Slide 19 — DATA ASSESSMENT | Exploratory Data Analysis

- Replace the caption with:
- Soft drinks is the worked example; every category goes through the same four
  lines of enquiry. *(Ch4 §4.2)*
- The one result to name: the autocorrelation analysis finds an **annual cycle** —
  which matters later. *(Ch4 §4.2; Ch9 §9.4)*
- ⚠ Don't volunteer the lag-13 point here. It's on slide 25.

### 4.13 Slide 20 — MODELLING & EXPERIMENT | Combined Overview

- Replace the caption with:
- Three layers. Bottom: models benchmarked on identical data, one deployed per
  category. Middle: a typed tool carrying the forecast, an interval, the model's
  measured error and its provenance. Top: the agent. *(Ch6; abstract)*
- **The one decision that carries SRQ2: the language model never touches a feature
  vector.** It asks for a forecast and gets one back with its evidence attached.
  *(Ch6; Ch7)*
- The LLM is reached over an API, so the 4 GB goes to data and models. The heaviest
  model peaks at **34.5 MB** to fit. *(Ch5 §5.6; Ch9 §9.1.1)*
- *If asked why the budget matters when you use 1% of it:* it bound **which
  architectures we could consider**, not run time. It excluded transformers before
  anything was fitted. *(Ch9 §9.1.1, DP4)*

### 4.14 Slide 21 — EXPERIMENT | Performance Overview

- Pass 01 §21c has the full set. In short:
- A → B is **data access alone**: median error from 502% to 2.9%. Worth more than
  anything above it on the ladder. *(Ch9 §9.1.4)*
- B → C is our step, and it **doesn't go the way we expected**: worse on the median,
  better on the mean. *(Ch8 §8.3)*
- What C buys: ~50× cheaper, ~20× faster, **identical on every repeat** — zero
  variance, because the model is fitted once and loaded. *(Ch10 §10.1)*
- ⚠ Scenario D (code agent, production orchestrator) reaches 0.9% median. If raised:
  an orchestrator effect on the code path, not a point for our artefact.

### 4.15 Slide 23 — FINDINGS

- Four rows, one per question. **Every row carries a qualification we put there
  ourselves.**
- **SRQ1:** the boosters win, but we won't name which — five seeds change the winner
  in every category. And pooling only helps on the two smallest panels, by 4.5 to 5.7
  points. *(Ch9 §9.1.1)*
- **SRQ2:** reliability holds by construction. The interval is honest but too wide to
  act on, so the measured track record carries the reliability claim, not the
  interval. *(Ch10 §10.1; Ch9 DP3)*
- **SRQ3:** assessed, not deployed — but three scenarios ran inside the production
  platform, so readiness comes from what integration actually required. *(Ch9
  §9.1.3)*
- **SRQ4:** no scenario leads everywhere. So the recommendation depends on the job:
  **the dedicated model where an answer must be reproducible and auditable; the code
  agent for one-off analysis a person will read.** *(Ch9 §9.1.5)*

### 4.16 Slide 25 — LIMITATIONS & FUTURE WORK

*Revised 2026-10-12 (R-1012-01): strategy is **don't volunteer, never deny**.
Speak to the limitations that make the work look careful; leave the substrate
item to its bullet unless asked.*

- Each limitation on the left has a next step on the right. *(Ch9 §9.5: "Five
  directions follow from what this evaluation could not settle")*
- **Sample:** three brands, one category, sixty-three runs — enough for large
  differences, nothing finer. *(§9.4)*
- **Forecasting practice:** the code agents used exponential smoothing and a
  seasonal model on every run; our classical baseline has neither — which is
  exactly the first next step on the right. *(§9.4; §9.5)*
- **Interval:** we tried three alternative calibrations; none improved coverage and
  width together in more than two of four categories — a sample-size limit, not a
  modelling choice. *(§9.4)*

**Only if asked about the lags / seasonality** (about 20 seconds, then stop):

> "The analysis found a yearly pattern, but the lag settings in the model never
> picked up the value from the same month last year. The model still knows which
> month it is forecasting, through the calendar features, so seasonality isn't
> missing entirely — it's just weaker than it could be. It's listed in Chapter 9
> as a limitation, and fixing it would only make our model more accurate, so it
> doesn't change our conclusion."

- ⚠ Never say "off by one month" — at the three-month horizon it's three.
- ⚠ Don't claim it was noticed before submission. Don't say "our code documents
  the bug".

### 4.17 Slide 27 — Let's discuss

- Close on the thesis's own line before taking questions:
  **"The contribution is qualified, and the qualification is the point. A dedicated
  forecasting layer must be justified on reproducibility, cost and auditability —
  not on error alone."** *(abstract)*

---

# 5 Design suggestions

*Suggestions only — you said you'll handle design. Measured from the slide XML, not
eyeballed, so confirm each one on screen. Ranked by how visible it is when projected.*

## 5.1 Fix first — visible defects, not taste

| Slide | Defect | Fix |
|---|---|---|
| **15** | **Column 3 (DESIGN SCIENCE) runs off the slide** — its text box auto-grows to 7.92 in on a 7.50 in slide, 0.81 in past its grey panel. Column 1's panel and header also sit 0.16 in higher than columns 2–3 | move column 3's last bullet (*"The consequence…"*) to the notes; set all three panels to the same top and height |
| **9** | **The whole table is `-apple-system`** (24 runs — every run on the slide, more than MANIFEST's 16). That's a CSS keyword from a Mac/web paste, not a font, so Windows PowerPoint substitutes something else on the day | select the table, set **Inter** |
| **23** | 14 of 14 filled cells bold; body at **18 pt** where slide 21's table is 12 pt; row labels stored as `SRQ1substrate` (line break, no space) | bold only the SRQ labels and header; body to 12–14 pt; put a space or line break between `SRQ1` and `substrate` |
| **21** | 27 of 32 cells bold — and the three cells with the strongest claims (`100%`, `$0.0091`, `6.0 s`) are split: number bold, unit plain | un-bold the body; bold only the winning value per row |
| **25** | all 10 bullets fully bold, title lowercase. Geometry is the cleanest in the deck — the "ugly" is just the bold | regular weight; `LIMITATIONS & FUTURE WORK`; split item 5 (2.3) |
| **13** | two empty frames, different widths and shapes | delete (2.1) |

## 5.2 Then — one pass for consistency

| Slides | Issue | Fix |
|---|---|---|
| 15, 16 | `METHDOLOGY` | METHODOLOGY |
| 29–35 (all seven appendix slides) | `MODELLING \|Model…` — no space after the pipe | find-replace space-pipe with space-pipe-space |
| 6, 10 | titles at 28 pt (all others 32), and the pipe is bolded | 32 pt; un-bold the pipe |
| 10, 11 | subtitle half title-case (`with predictive capabilities`, `with dedicated ML Models`) | pick one case |
| 3, 17, 28 | dividers `BACKGROUND & Motivation`, `Modelling, ARCHITECTURE…`, `appendix` | ALL CAPS like the other six |
| 2 vs 39/40 | two different agendas; slide 2 splits 4/2 and lacks DISCUSSION | one agenda, 7 items; delete 39/40 |
| 15 | 12 lead-ins bold **and** underlined — the deck's entire underline budget | drop the underline |
| 6 | 14 separate bold fragments in 5 bullets (`**Agentic** systems **mainly** **explain**…`) | one bold phrase per bullet |
| 4 | row 1's icon sits 0.20 in right of rows 2–6 | align |
| 27 | `Let‘s` uses an opening quote | `Let's` |
| 37 | `UNIFCATED RESOURCES CONSTRANIS` | copy slide 1's title, or delete the slide |
| 36 | untitled, no text | title or delete |
