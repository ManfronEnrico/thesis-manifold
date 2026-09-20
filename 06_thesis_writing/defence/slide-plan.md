---
name: slide-plan
description: REFERENCE - Slide-by-slide build plan for the oral defence deck; per slide the layout, what goes where on the canvas, the spoken notes, and the thesis section each claim is grounded in.
category: reference
applies-to: [oral defence, slide deck]
triggers: [building the deck, what goes on each slide, what do we say, slide notes]
created: 2026_09_19-12_30
updated: 2026_09_20-14_20
---

# Slide plan — oral defence

**Grounded against `2026-09-20_14-09_defence-deck-citation-audit`** (47,139
words, 61 reference entries, 0 live comments). Every claim carries its chapter
and section. Numbers are read from `05_thesis_results/`, never from the prose —
that is how F3 caught "roughly fifty" actually being 51.3×.

⚠ **The `.docx` moved after submission.** The bibliography field was refreshed,
taking the reference list from 34 entries to 61 (**F12**). An audit against the
09-15 submission snapshot is stale. Chapter prose is unchanged beyond ±1–8 words
of field re-rendering, so every section reference below still holds — but
**re-snap before verifying anything new.**

**Structure** follows the agenda already built in PowerPoint: six numbered
sections. **Discussion is not numbered** — it is the unnumbered wall after 06,
matching the reference deck (F11).

---

## The storyline, in one page

Read this before building anything. Each slide exists to make the next one
land; if a slide does not advance this line, it is decoration.

> **1. The field has been moving from description to prediction for a decade,
> and it knows where its frontier is.** M4 and M5 settled the method question —
> gradient boosting, exogenous variables. Makridakis named the open direction
> explicitly. *(§01)*
>
> **2. But that whole literature assumes compute nobody outside a large lab
> actually has.** Transformer forecasters need accelerator memory in the tens of
> gigabytes. An SME provider has about four. *(§01)*
>
> **3. So there is a real company with a real gap:** Manifold AI's assistant
> explains the past and cannot anticipate. Extend it — do not replace it. *(§01)*
>
> **4. Four literatures meet at this problem and none covers it.** Each supplies
> a piece; the intersection is empty. *(§02)*
>
> **5. That makes it a design problem, not a hypothesis test** — hence DSR, hence
> an artefact *and* transferable design knowledge, both assessed. *(§03)*
>
> **6. Here is what we built, and the one decision that carries it:** the model
> never touches a feature vector. *(§04)*
>
> **7. And here is the question that could have sunk it:** does the dedicated
> model beat an LLM writing its own code? We built a ladder to find out. *(§04)*
>
> **8. It does not win on accuracy. It wins on cost, speed and reproducibility.**
> Data access is worth more than anything above it on the ladder. *(§05)*
>
> **9. So the contribution is qualified — and the qualification is the point.**
> A predictive layer must be justified on reproducibility, cost and auditability,
> not on error alone. *(§06)*

**The last line is the thesis's own**, from the abstract: *"The contribution is
therefore qualified, and the qualification is the point."* Everything builds to
it. Do not let an examiner hear the finding as a disappointment — it is the
result, stated deliberately.

### Three narrative rules

1. **Never present the SRQ4 finding as a loss.** It is a *qualified* contribution
   and the thesis says so on purpose. The framing is "we tested our own premise
   and report what we found", not "our artefact underperformed".
2. **The constraint binds at design time, not run time.** This will be probed.
   Say it before they ask — a budget that excluded transformers before anything
   was fitted did its work, even though the survivors sat far below it.
3. **Every negative result is presented as tested, not discovered late.** The
   interval is too wide; three alternative calibrations were implemented and
   measured. That is a finding with work behind it.

---

## Budget and slide inventory

| Section | Slides | Minutes | Types |
|---|---:|---:|---|
| Title + agenda | 2 | 0:45 | title, list |
| 01 Background & Motivation | 3 | 2:45 | text, chart, text |
| 02 Literature Review | 2 | 2:00 | table, diagram |
| 03 Methodology | 2 | 1:45 | diagram, table |
| 04 Modelling, Architecture & Experiment | 3 | 3:30 | diagram, diagram, table+figure |
| 05 Most Relevant Findings | 3 | 3:15 | table, text, table |
| 06 Limitations & Conclusion | 2 | 1:45 | text, table |
| Let's discuss | 1 | 0:15 | title |
| **Presented** | **18** | **~16:00** | |
| Reserve wall | ~20 | 0 | |

⚠ **16:00 is over a 15-minute budget.** Cut in this order:
1. Slide 03.2 → drop the table, keep one spoken sentence (−45 s)
2. Slide 05.3 → fold into 05.2's notes (−60 s)

Both cuts leave the storyline intact. **Do not cut 01.2 or 02.2** — they are the
two slides that make this a thesis rather than a project report.

**Deliberate type mix: 7 text · 6 diagram/figure · 5 table.** Presented slides
stay sparse; density lives behind the wall.

---

## Layout conventions used below

- **Canvas** assumed 16:9, CBS template, title bar top-left as on your agenda slide.
- **"Left / right"** means a two-column split, roughly 40/60 unless stated.
- **One idea per slide.** If two ideas are fighting, the second is a reserve slide.
- **Figures are referenced by path, never copied.** Tier 06 produces no artefact.
- Every SVG below verified present on disk 2026-09-19.

---

# Section 01 — Background & Motivation

> **Arc of this section:** the field knows where it's going → the field assumes
> compute nobody has → therefore a real company has a real gap.
> **Three slides, and the middle one is the one people remember.**

## Slide 01.1 — From describing the past to anticipating it

**Type:** Text · **Speaker:** A · **0:45–1:45** · **Layout:** full-width, 3 blocks stacked

**On screen**

*Top block — the shift*
- BI has been **descriptive** for decades: dashboards, KPIs, what happened
- FMCG makes that insufficient — volatile demand, promotions, seasonality, SKU proliferation

*Middle block — the field settled the method*
- **M4** (100,000 series, 61 methods): combinations beat any single model
- **M5** (Walmart, hierarchical retail): **all top 50** submissions used LightGBM, >14% over the best statistical benchmark

*Bottom block — pull quote, set apart*
> *"One thing that remains to be determined is the possible improvement … by
> expanding time series forecasting to include explanatory/exogenous variables."*
> — Makridakis et al. (2020)

**Notes — what to say**
> "Business intelligence has been descriptive for decades — it tells managers
> what happened. In fast-moving consumer goods that is no longer enough: demand
> is volatile, promotions distort it, and SKU counts keep climbing.
>
> The forecasting field has already settled the method question. The M4
> competition — a hundred thousand series, sixty-one methods — showed combinations
> beat any single model. M5, on real Walmart retail data, was blunter still: all
> fifty top submissions used LightGBM, better than fourteen per cent over the best
> statistical benchmark. And both found that exogenous variables materially help.
>
> Makridakis closed that analysis by naming the open frontier — bringing
> explanatory variables into forecasting. That is the direction we take up."

**Grounded in:** Ch1 §1.1 — paragraphs 1–3. M4/M5 (Makridakis et al. 2018, 2020,
2022), Ma et al. (2025) on no single model dominating across demand patterns,
Rinaldi et al. (2025) DSS4EX. **The quote is verbatim from §1.1.**

---

## Slide 01.2 — The constraint the literature left out

**Type:** Chart or simple visual · **Speaker:** A · **1:45–2:45** ·
**Layout:** left = one number, huge; right = three short lines

**On screen**

*Left, dominant — a single visual comparison*
> **Transformer forecasters:** tens–hundreds of GB accelerator memory
> **An SME provider's realistic budget:** ~**4 GB**

Render as two bars, or as two numbers with a gap between them. **Do not use a
table** — this is the emotional beat of the opening and it needs scale, not rows.

*Right*
- The cost asymmetry is **structural**, not marginal
- Ng (2017), 4 TB of Nielsen scanner data: **memory is the binding design variable**
- Agentic AI frameworks consistently **assume cloud-scale compute**

**Notes — what to say**
> "But there is a constraint the academic literature has largely left unexamined.
>
> Running transformer-based forecasters or locally hosted language models needs
> accelerator memory measured in tens to hundreds of gigabytes — instance classes
> an order of magnitude more expensive to run continuously. For a provider serving
> inference across many client queries, that compounds into an order-of-magnitude
> difference in operating cost. It is structural, not marginal.
>
> Ng, working with four terabytes of Nielsen scanner data, showed empirically that
> memory is the *primary binding design variable* in this kind of work — even with
> unlimited money, you cannot load the data at once.
>
> And the agentic AI literature assumes cloud-scale compute almost without
> exception. That is a structural asymmetry: systems get validated on
> infrastructure available to large labs, while most organisations that would
> benefit operate with far less. Showing this is achievable inside an SME's
> envelope is itself a contribution, independent of the domain."

**Grounded in:** Ch1 §1.1, paragraphs 4–5 — verbatim on "structural rather than
marginal", the Ng (2017) finding, and the claim that bridging the asymmetry "is
itself a research contribution independent of the specific domain application."

⚠ **This is the slide that earns the thesis.** It converts "a company wanted a
feature" into "a research community has a blind spot". Do not rush it.

---

## Slide 01.3 — A real system, a real gap

**Type:** Text · **Speaker:** A · **2:45–3:30** · **Layout:** left = what it does
now; right = the four problems extension raises

**On screen**

*Left — Manifold AI, "AI Colleagues"*
- Production agentic decision-support for retail analytics
- Reports volumes, market share, weighted distribution
- **Does not forecast, anticipate, or recommend**

*Right — extending it raises four problems → these become our four SRQs*
1. A substrate accurate **and** deployable in a tight budget
2. An interface preserving reliability, uncertainty, traceability
3. A host system with the capabilities to integrate it
4. Proof it beats an LLM writing its **own** code

**Notes — what to say**
> "The commercial context is Manifold AI, a Danish company building what they call
> AI Colleagues — a conversational, production agentic system for retail analytics.
> It operates at the descriptive level: it reports what happened. It does not
> forecast, anticipate, or recommend. It is also our empirical reference case, so
> this is a live system, not a prototype we built to study.
>
> Extending it raises exactly four problems, and those become our four
> sub-questions. The substrate has to be accurate and fit the budget. The forecast
> has to reach the agent with reliability, uncertainty and traceability intact.
> The host system has to be capable of receiving it. And the whole thing has to
> earn its place against a general-purpose model that writes and self-corrects its
> own forecasting code.
>
> That fourth one is the one that could have gone against us."

**Grounded in:** Ch1 §1.2 — the four problems are stated in this order and close
to this wording. "AI Colleagues" and the descriptive-level framing are verbatim.

---

# Section 02 — Literature Review

> **Arc:** four literatures, each giving something, none covering the
> intersection. **Ends by stating the gap as one sentence** — which is the
> research question in disguise.

## Slide 02.1 — Four bodies of work, four things missing

**Type:** Table (4 rows × 3 cols) · **Speaker:** A · **3:30–4:30** ·
**Layout:** full-width table, third column visually emphasised

**On screen**

| Literature | Supplies | Stops short of |
|---|---|---|
| Forecast-to-decision | prediction creates value **through decisions** | assumes **tight** optimisation coupling; no agents |
| LLM agents & tool use | tool delegation substitutes for model scale | not forecasting, not production-constrained |
| Reliability & evaluation | agentic outputs carry measurable risk | requirements, **not integration** |
| Production agentic systems | feasibility demonstrated at scale | real-time supervision on dedicated hardware |

**Notes — what to say**
> "Four literatures meet at this problem, and each gives us something while
> stopping short of the combination.
>
> The forecast-to-decision work — Elmachtoub and Grigas, Mandi and colleagues —
> establishes that predictions create value through the decisions they inform. But
> it couples them tightly, through differentiable optimisation against a formal
> objective. That is not open-ended managerial decision-support, and it does not
> concern language model agents.
>
> The agent literature gives us tool-mediated reasoning — Schick and colleagues
> showed tool delegation substituting for raw model scale. An emerging strand
> begins exposing pre-trained statistical models as agent tools, but it exists as
> small, non-peer-reviewed proofs of concept and does not address forecasting,
> reliability, or production constraints.
>
> The reliability literature tells us what goes wrong — hallucination, input-noise
> sensitivity, coordination failure — and that evaluation must be multidimensional.
>
> And the production systems demonstrate feasibility, but the closest exemplars
> supervise live industrial processes on dedicated infrastructure. Neither
> predictive extension over a historical record nor SME resource constraints fall
> in their scope."

**Grounded in:** Ch2 §2.7 — this table *is* the structure of §2.7, which names
these four strands in this order with these sources. **Add no citation not in
§2.7**; only sources actually used are examinable.

---

## Slide 02.2 — The gap, as one sentence

**Type:** Diagram · **Speaker:** A → B · **4:30–5:30** ·
**Layout:** figure occupies upper two-thirds; the sentence sits below it, boxed

**Figure:** `05_thesis_results/02_literature_review/figures/ch2_gap_diagram_v2.svg`
*(this is Figure 2 in the submitted document)*

**On screen, below the figure**
> How a production agentic system **without native predictive capability** can be
> extended with lightweight forecasting through a **loose, agent-mediated,
> reliable and traceable** tool interface — and whether dedicated-model
> integration improves on a **code-as-action LLM baseline** that writes its own
> forecasting code.

**Notes — what to say**
> A: "Put together, the intersection is under-addressed. The decision literature
> supplies the principle but assumes tight coupling. The agent literature supplies
> tool use, while only emerging work connects it to statistical prediction. The
> reliability and production literatures supply requirements but not the
> integration."
>
> *[handover — A stops, B starts, no pause]*
>
> B: "And the second half of that sentence is what makes this uncomfortable. We
> did not assume a dedicated model was needed. We built the alternative properly
> and tested against it."

**Grounded in:** Ch2 §2.7, final paragraph — the sentence is close to verbatim
and deliberately so.

⚠ **Handover 1 of 2. Rehearse it.** Group defences stumble at handovers more
than anywhere else. One sentence each, no "over to you".

---

# Section 03 — Methodology

> **Arc:** constructive questions → DSR → therefore two outputs, both assessed.
> Keep it short. Methodology examiners probe here, but the slide only has to
> open the door; the answers live in the reserve wall and the drill.

## Slide 03.1 — Design Science Research, and why it fits

**Type:** Diagram · **Speaker:** B · **5:30–6:30** ·
**Layout:** diagram left (60%), four bullets right (40%)

**Figure:** `05_thesis_results/03_methodology/figures/ch3_methodology_design_v1.svg`

**On screen, right column**
- **Pragmatist** philosophy — knowledge judged by whether it enables action
- **DSR**: builds an artefact **and** states transferable design knowledge
- Three cycles: **relevance** (Manifold AI) · **design** (Ch5–8) · **rigour** (Ch2)
- Design type: **explanatory** — why these choices produce better outcomes

**Notes — what to say**
> "Our questions are constructive: how can a system be designed, what does the
> design require. Not tests of an existing theory. That is Design Science Research.
>
> The philosophy underneath is pragmatist — a framework is adequate if it enables
> action in the domain it addresses. So our criterion for success is not whether we
> revealed deep structure in retail demand. It is whether a company like Manifold
> AI can actually extend their system with this.
>
> DSR runs three cycles, and we engage all three. Relevance comes from the
> collaboration with Manifold AI, whose operational need defines the problem.
> Design is the iteration across Chapters 5 to 8. Rigour is the literature review.
>
> And one thing matters for how you assess us: **DSR produces two outputs** — an
> artefact and design knowledge — and both are assessed. That is why our
> contribution is stated as five principles held separate from the thing we built."

**Grounded in:** Ch3 §3.1 (pragmatism, Saunders et al. 2023), §3.2 (Hevner et al.
2004; Hevner 2007 three cycles; Peffers et al. 2007; explanatory design type).

**Hold in reserve:** the artefact's prototype status is explicitly acknowledged
in §3.2 — "a research prototype evaluated on historical data under controlled
conditions, not claimed to be a production-ready deployed system." Say this
yourself if pressed on deployment.

---

## Slide 03.2 — One question per layer  *(first cut candidate)*

**Type:** Table · **Speaker:** B · **6:30–7:15** ·
**Layout:** table top; one data line beneath as a footer strip

**On screen**

| | Layer | Asks |
|---|---|---|
| **SRQ1** | substrate | which lightweight models trade accuracy against memory best |
| **SRQ2** | interface | how a forecast reaches the agent with reliability, uncertainty, traceability intact |
| **SRQ3** | host system | what a production system must already do first |
| **SRQ4** | evidence | do dedicated models beat an agent writing its own code |

*Footer strip:* Nielsen scanner panel · 4 Danish beverage categories · brand ×
month · 41–46 periods to July 2026 · market definition DVH EXCL. HD

**Notes — what to say**
> "One sub-question per layer. SRQ3 produces no code by design — it yields
> criteria, argued from the integration the other layers made possible.
>
> On data: one source, the Nielsen scanner panel, four categories at brand-by-month
> grain, roughly three and a half to four years of history ending July 2026. A
> fifth category, beer, was excluded before any modelling — its panel is
> structurally unlike the others, and we record that as a decision fixed in advance
> rather than as an absence.
>
> The market definition is Nielsen's own recommended default: Danish grocery
> excluding hard discount, which is structurally different in assortment and
> pricing and would otherwise be pooled in."

**Grounded in:** Ch3 §3.3 (unit of analysis, beer exclusion fixed before
analysis, DVH EXCL. HD rationale), §3.4 (41–46 periods, ending July 2026),
§3.5.1–3.5.4. Canonical SRQ wording: `00_thesis_context/research-questions/`.

**If cutting:** drop the table, keep the footer strip, say the SRQ sentence
aloud. Saves ~45 s.

---

# Section 04 — Modelling, Architecture & Experiment

> **Arc:** what we fit → how it reaches the agent → how we tested whether it was
> needed at all. **The third slide sets up the entire findings section.**

## Slide 04.1 — The forecasting substrate

**Type:** Diagram · **Speaker:** B · **7:15–8:15** ·
**Layout:** diagram left, four bullets right

**Figure:** `05_thesis_results/05_model_benchmark/figures/ch5_model_selection_v2.svg`

**On screen, right column**
- Five families: **ARIMA · Prophet · LightGBM · XGBoost · Ridge**
- Benchmarked across four categories, **one served per category**
- Selected on **cross-validated** accuracy — test is never touched by selection
- Fitting peaks **34.5 MB** against a **4096 MB** ceiling

**Notes — what to say**
> "Five model families, chosen to span the space rather than to be exhaustive: two
> classical, two gradient-boosted, one regularised linear baseline.
>
> One model is served per category, and selection runs on cross-validated
> accuracy. The test split is never touched by selection — it is held for the
> number we report and nothing else.
>
> Two models are fitted per category: one on training only, whose validation
> residuals give the conformal quantile, and one on training plus validation,
> which serves. Only the calibration has to be out-of-sample.
>
> Fitting peaks at about thirty-four megabytes against a four-gigabyte ceiling."

**Grounded in:** Ch5 §5.1 (rationale), §5.3.1–5.3.6 (the families), §5.4.4
(validation scheme), §5.7 (selection decision). Memory from
`05_thesis_results/05_model_benchmark/tables/15_substrate_resource_profile.md`;
also Ch5 §5.6.6, Ch6 §6.8.

⚠ **F9 — quote 34.5, not 31.9.** Ch6 Table 20 carries 31.9/14.9 from an earlier
unreconciled profiling run; Ch9 and the artefact say 34.5/17.9. The abstract
rounds to "thirty-five". Reserve slide **R05** handles it if an examiner puts the
two tables side by side.

---

## Slide 04.2 — The architecture, and the decision that carries SRQ2

**Type:** Diagram · **Speaker:** B · **8:15–9:30** ·
**Layout:** diagram fills the slide; **one line overlaid or boxed beneath it**

**Figure:** `05_thesis_results/06_architecture/figures/ch6_layered_architecture_v2.svg`

**On screen — three labels on the diagram, one line below**
- **Substrate** — trained, persisted, loaded never fitted
- **Typed tool interface** — JSON function calling, closed schema, two arguments
- **Bounded tool-using agent** — orchestrates, validates, communicates

> The language model **never handles a feature vector.**

**Notes — what to say**
> "Three layers. The substrate is trained once and persisted — the serving path
> loads, it never fits. That boundary is real: before it existed, three copies of
> our training logic had drifted apart, and a conformal-calibration fix landed in
> one while the other two kept the bug.
>
> The interface is a typed tool with a closed schema taking two arguments:
> category and brand. It returns a point forecast, a split-conformal prediction
> interval, the serving model's measured out-of-sample error, and the provenance
> needed to reconstruct the call.
>
> And the load-bearing decision: **the model never handles a feature vector.** It
> asks for a brand and receives a forecast. Feature construction stays server-side,
> versioned, identical on every call. That is what makes the forecast auditable
> rather than merely available — and it is most of our SRQ2 contribution."

**Grounded in:** Ch6 §6.2 (architectural overview), §6.3, §6.4; Ch7 §7.2.1–7.2.2
(what may be asked, what is returned), §7.3 (reliability), §7.5 (traceability).

**Hold in reserve — the framing correction we make ourselves.** This is a
*bounded tool-using agent*, not a multi-agent system, in Sapkota et al.'s (2026)
sense: **fixed tool set, delegates to no other agent, does not act on its own
recommendation.** We say so twice — Ch6 §6.2 and Ch9 §9.2.1, where we write that
describing it otherwise "would claim a coordination contribution the thesis does
not make." If asked *what is agentic about it then*: tool-mediated reasoning
under a schema, and the boundedness is what keeps it auditable and inside budget.

---

## Slide 04.3 — Why a ladder, not a two-way comparison

**Type:** Table + small figure · **Speaker:** A · **9:30–10:45** ·
**Layout:** table left (55%), scenario figure right (45%), cost line as footer

**Figure:** `05_thesis_results/07_decision_synthesis/figures/ch7_scenarios_v2.svg`

**On screen**

| Rung | Given | Isolates |
|---|---|---|
| **A** | no firm data | — |
| **B** | + the firm's history in a code sandbox | what **data access** buys |
| **C** | + the same data behind the typed tool | what **the artefact** adds |
| **F** | both sandbox and tool | integration behaviour |
| **D · E · G** | B · C · F **inside the production platform** | orchestrator effect |

*Footer:* 7 scenarios × 3 brands × 3 repeats = **63 funded runs, $19.60**

**Notes — what to say**
> "A two-arm design would have confounded two different things: what it is worth
> giving an agent the firm's data at all, and what it is worth giving it a trained
> model rather than a sandbox. Only the second is our contribution.
>
> So every rung adds exactly one capability. A to B measures data access. B to C
> measures what our artefact adds. And three rungs are repeated inside the
> production platform, so each is paired with its counterpart — an effect we see on
> a general-purpose orchestrator can be checked for survival rather than assumed to
> transfer.
>
> Sixty-three funded runs. Nineteen dollars sixty."

**Grounded in:** Ch8 §8.2 (design), §8.3.1 (**$19.60** actual, from the
account-balance delta — the only non-estimated figure; $25.20 is the token-based
estimate and overshoots by 29%).

**Design defences in reserve:** identical question to every scenario; capability
notes composed from shared blocks with an automated byte-identity check; prompt
set hashed. **An audit before the funded run caught the notes having drifted** —
one scenario told to produce an interval while its pair was not — and it was
fixed before any funded run. Volunteer this if instrument validity is questioned;
it shows the control was real rather than claimed.

---

# Section 05 — Most Relevant Findings

> **Arc:** the substrate works and we qualify it → the ladder's first step
> dominates → our step wins on different axes than expected.
> **Do not let the section read as bad news.** It reads as a thesis that tested
> its own premise.

## Slide 05.1 — SRQ1: what the benchmark does and does not support

**Type:** Text (4 findings) · **Speaker:** A · **10:45–11:45** ·
**Layout:** 2×2 grid of short blocks, the warning block visually distinct

**On screen**

| | |
|---|---|
| **Boosters beat Ridge and ARIMA** in all four categories | **But we name no winner** — a five-seed sweep changes the selection in *every* category |
| ⚠ **Two of four categories are beaten outright** by a parameter-free benchmark — seasonal naive on RTD, Prophet on water | **Memory bound selection, not runtime** — 34.5 MB against 4096 MB |

**Notes — what to say**
> "Two things worth saying plainly, because an examiner will find both.
>
> First, we do not name a winner between LightGBM and XGBoost. A five-seed sweep,
> holding everything else identical, changes the selected model in all four
> categories — the difference between the families, between zero point three and
> one point two percentage points, sits inside a between-seed standard deviation
> reaching two point eight. The defensible claim is that they are statistically
> indistinguishable here. That is a weaker headline than naming a winner and a more
> useful one: a practitioner can choose on training time or tooling maturity
> without forfeiting accuracy.
>
> Second, a forecast costing nothing to compute beats our substrate in two of four
> categories. That is the most important qualification we place on our own
> substrate, and we report it rather than absorbing it."

**Grounded in:** Ch9 §9.1.1 — the 0.3–1.2pp gap, the 2.81 between-seed standard
deviation, and "reported rather than absorbed" are all from that section. Also
Ch5 §5.6.10 (seed stability), §5.6.2 (where the simple benchmarks win).

**The memory answer, if challenged:** the budget bound the *selection space*, not
the runtime footprint — it excluded transformer and locally hosted options before
any was fitted. That the survivors sat far below the ceiling is a substantive
answer, not a missing measurement. Ch9 §9.1.1 puts it exactly this way: "the
constraint is real as a design criterion and slack as a runtime one." **Concede
openly** — a thesis claiming the budget bound at run time would be contradicted
by its own table.

---

## Slide 05.2 — SRQ4: no scenario leads on every axis

**Type:** Table · **Speaker:** A · **11:45–13:00** ·
**Layout:** full-width table; the closing line below it, emphasised

**On screen**

| Measure | A plain | B data + code | C model |
|---|---:|---:|---:|
| Usable answers | 6/9 | 9/9 | 9/9 |
| Median APE | 502.2% | **2.9%** | 14.6% |
| Mean APE | 662.1% | 27.9% | **13.1%** |
| Variation across repeats | 26.7% | 4.1% | **0.0%** |
| Identical on repeat | 0% | 0% | **100%** |
| Cost per answer | $0.38 | $0.4667 | **$0.0091** |
| Latency | 69.5 s | 123.8 s | **6.0 s** |

> **B → C: 51× cheaper · 21× faster · zero variance — and worse on the median.**

**Notes — what to say**
> "Read the first increment first. Giving the model the firm's own data moves
> median error from five hundred per cent to under three. That is worth far more
> than anything above it on the ladder — and a two-arm design would have folded it
> into the effect we actually care about.
>
> Now our step, and it does not go the way we expected. Our artefact is **worse on
> the median and better on the mean**. The code-writing agent is better most of the
> time and occasionally much worse.
>
> What the dedicated model buys is fifty-one times the cost efficiency, twenty-one
> times the speed, and an identical answer every single time. Zero variance — not
> low, zero — because the model is fitted once and loaded, so a repeat is a repeated
> read of the same parameters. That is the reproducibility property Chapter 7
> specifies, observed rather than asserted."

**Grounded in:** Ch8 §8.3 — the three findings are stated in this order there.
Numbers from `08_experimental_evaluation/tables/22_scenario_comparison.csv`;
51.3× and 20.6× **computed** from that file (F3), not transcribed.

⚠ **Never let "the code arm won" stand bare.** Always restate: a per-series
ensemble beats a category-tuned booster on the median while costing 51× more,
taking 21× longer, and producing no auditable tool call. Those three are not
independent — a trained pipeline is work done once; an agent handed the same data
repeats that work every session.

⚠ **If they read the appendix:** scenario D (code, production orchestrator) is
the most accurate rung at 0.9% median — better than B. That is an orchestrator
effect on the *code* path, not a point for our artefact. Say so plainly; do not
pretend it is not there. (F3.)

---

## Slide 05.3 — Where the difference actually lives  *(second cut candidate)*

**Type:** Table · **Speaker:** A → B · **13:00–14:00** ·
**Layout:** table upper two-thirds; the failure story as a short block beneath

**On screen**

| Scenario | 7-UP | HARBOE | ØRBÆK |
|---|---:|---:|---:|
| A, no firm data | 1305.8% | 18.5% | **unscored** |
| B, data and code | 78.9% | 4.1% | 0.8% |
| C / E, dedicated model | **14.6%** | 21.9% | 2.8% |
| F, both | 47.0% | 7.3% | 0.6% |

*Beneath:* **3 of 63 runs produced no usable forecast — all one scenario, one brand.**

**Notes — what to say**
> A: "The aggregate hides the mechanism. On the largest brand the code-writing
> scenario errs by seventy-nine per cent where our model errs by fifteen. On the
> smallest it reverses. 'Better on the median, worse on the mean' is this table,
> not a statistical curiosity.
>
> And the three runs that failed are all one scenario on one brand. Asked about a
> small regional Danish producer selling roughly two thousand eight hundred and
> fifty units in the scored month, the no-data scenario answered a hundred and
> twenty thousand, sixty-two thousand, and ninety thousand. Those are not forecasts
> with large errors — they are answers of the wrong order of magnitude. We classify
> them as failures rather than scoring them, because averaging them would let an
> arbitrary number determine the scenario's mean."
>
> *[handover]*

**Grounded in:** Ch8 §8.3 Table 25 (per-brand MAPE) and the ØRBÆK narrative —
2,850 units actual against answers of 120,000 / 62,000 / 90,000, verbatim from
§8.3.

⚠ **Handover 2 of 2. Rehearse it.**

**If cutting:** fold the ØRBÆK failure into 05.2's notes as one spoken sentence.
Keep the failure story — it is the clearest evidence the outcome taxonomy does
real work. Saves ~60 s.

---

# Section 06 — Limitations & Conclusion

> **Arc:** here is what bounds this → here is what transfers anyway.
> **End on the thesis's own closing sentence.** Do not summarise the summary.

## Slide 06.1 — What bounds these conclusions

**Type:** Text (5 items) · **Speaker:** B · **14:00–15:00** ·
**Layout:** single column, five short lines, generous spacing

**On screen**
- One organisation, one market, four categories — **the ladder rests on 3 brands in 1 category**
- **One DSR cycle** — principles are *derived*, not validated across contexts
- The comparison is **conditional**: our substrate lacks two techniques the code arm used on every run
- Intervals **attain coverage** and remain **too wide to act on**
- We measure what was **communicated**, not whether a planner **decided better**

**Notes — what to say**
> "Five limitations, and I want to state them before you ask.
>
> The scope is one organisation, one national market, four categories — and the
> scenario comparison rests on three brands within one of them. That is small, and
> it is why we speak about direction rather than effect size.
>
> We completed one design-science cycle, so our principles are derived rather than
> validated across contexts.
>
> The comparison is conditional on the forecasting practice on each side, and our
> substrate lacks two things the code-writing scenarios applied unprompted on every
> run — exponential smoothing as a benchmark family, and a seasonal term in the
> classical baseline. We do not think the comparison is settled while that is true.
>
> The intervals attain their coverage guarantee and are still too wide to act on
> for an individual brand — at ninety per cent they span eight to thirty-four times
> the quantity forecast. That is a limit of the panel's shape rather than of the
> method, but it is a negative result and we report it as one.
>
> And we measure what each configuration communicated and how accurate it was — not
> whether a planner receiving it decided better. That is the question the
> decision-support literature actually asks, and it needs human participants."

**Grounded in:** Ch10 §10.4 — all five, in this order, close to verbatim. The
8–34× interval width is Ch9 §9.1.2.

⚠ **Variant T only:** add the lag-12/13 provenance defect as a sixth item. It is
already stated in submitted Ch9 §9.4 (F5), so this foregrounds an owned
limitation rather than confessing a new one. **Do not volunteer** the MASE
denominator, the non-seasonal ARIMA, or the in-sample residual gate — one
well-evidenced defect reads as self-awareness; four reads as a thesis that needed
another month. All are prepared in `qa-drill.md`.

---

## Slide 06.x — What we applied, and where the chain broke  *(optional — Variant T only)*

**Type:** Table, two columns · **Speaker:** A · **+60 s** ·
**Layout:** two-column "did / did not", the single defect row emphasised

> **Insert between 06.1 and 06.2 only if running Variant T.** In Variant S this
> content stays in `qa-drill.md` and is never shown. See the honesty note below
> — it constrains how this slide may be worded.

**On screen**

| We applied | Where the chain broke |
|---|---|
| Order-preserving 4-fold expanding-window CV, split on **periods not rows** | — |
| Rolling-origin evaluation, refit each fold (Tashman 2000) | — |
| Test split untouched by selection **or** calibration | — |
| Split-conformal intervals from **held-out validation** residuals | — |
| ACF/PACF per brand, per category — **lag 12 significant for 5 of 5 CSD brands** | ⚠ the feature matrix ships **lag 13** |
| Seasonal naive benchmark reads **12 months back** | ⚠ ARIMA is **non-seasonal** `(1,1,1)` |
| MASE reported against naive **and** seasonal naive | — |

> **One diagnostic did not reach one configuration file.** Everything measured
> was measured correctly. Nothing was carried forward automatically.

**Notes — what to say**
> "I want to be precise about what we did and what we did not, because the
> methodology holds and one link in it does not.
>
> What we applied: order-preserving cross-validation, split on distinct periods
> rather than rows, because our rows are brand-months and a row-wise split would
> put the same month in training and validation for different brands. Rolling
> origin, refitting every fold. The test split untouched by selection and by
> calibration — two models per category, one fitted on training only so its
> validation residuals give a genuinely out-of-sample conformal quantile.
>
> And we ran the autocorrelation analysis properly: per brand, per category. On
> CSD, lag twelve is significant for five of five leading brands. Lag thirteen
> for two — and both of those show *every* lag from one to fifteen, which is
> trend, not seasonality.
>
> Then the chain broke. The feature matrix ships lag thirteen. On monthly data
> the same month last year is twelve months back. So the feature we built to
> carry annual structure is offset by one month from the structure we measured.
>
> The cause is not a misunderstanding of seasonality — the seasonal naive
> baseline in the same codebase reads twelve months back, and our residual
> diagnostics set the seasonal period to twelve. The lag set was configured in a
> separate file that the analysis never wrote to. The analysis produced a figure
> for a human reader; the feature builder read a constant. Nothing connected them.
>
> That is a provenance failure between the analytical and engineering layers,
> and it is the same class of defect the structured interface exists to prevent
> downstream of the model. We state it in Chapter 9 because demonstrating our own
> argument from the negative case is worth more than a clean table."

**Grounded in:**
- **Ch5 §5.4.4** — expanding-window CV, period-wise splitting, Bergmeir et al.
  (2018) and Cerqueira et al. (2020) on why K-fold is rejected *here* and not on
  principle; Tashman (2000) on rolling origin.
- **Ch5 §5.4.2** — the submitted prose states lags "at one, two, three, four,
  eight and **thirteen** months" and calls thirteen "the year-ago comparison."
  ⚠ **The thesis documents the defect's value as correct.** See below.
- **Ch9 §9.4** — states the defect in full: *"the feature intended to carry
  annual structure is offset by one month… a gap of provenance between the
  analytical and engineering layers rather than of method."*
- **Code, verified 2026-09-20:** `engineer_features.py:33`
  `DEFAULT_LAGS = (1,2,3,4,8,13)`; shipped `csd_feature_matrix_h1.parquet`
  carries `lag_13` and `rolling_mean_13`; `srq1_baselines_stat.py:21`
  `y_hat(t+h) = y(t+h-12)`; `srq1_residual_diagnostics.py:105`
  `SEASONAL_PERIOD = 12`.
- **Evidence:** `05_thesis_results/04_data_assessment/eda/CSD/tables/step_2_16_acf_significant_lags.md`
  — HARBOE `[1,2,3,9,12,15]`, FAXE KONDI and FANTA both `[3,6,9,12,15,…]`,
  COCA COLA and PEPSI all lags 1–15.

### ⚠ The one thing that must not be said carelessly

`step_3_derive_params.py:213` records the provenance string **"the lag-12 term
is retained"** beside a `lags` value of `(1,2,3,4,8,13)`. The justification and
the value contradict each other inside the same function.

**Do not present this as "our code documents the bug."** It is a stronger and
more specific claim than the thesis makes, it invites "what else disagrees with
its own comments?", and the honest reading is duller: the string was written when
the intent was lag 12 and was never revised. **If an examiner finds it, confirm
it plainly and do not elaborate.**

Equally: **do not claim the defect was noticed before submission.** Ch9 §9.4
states it, which is enough. Claiming foresight is the one move that converts an
owned limitation into a credibility problem.

### What else is in this class — prepared, not volunteered

| Gap | Status |
|---|---|
| **Non-seasonal ARIMA** — `SARIMAX(order=(1,1,1))`, no `seasonal_order`, on monthly seasonal data | Ch9 §9.4 concedes the substrate "lacks exponential smoothing and a seasonal ARIMA term" |
| **MASE denominator** is the one-step naive, where Hyndman & Koehler prescribe seasonal naive for seasonal data | **Weaker than it looks** — Ch5 §5.6.3 reports naive *and* seasonal-naive MASE side by side and surfaces their disagreement rather than resolving it |
| **`rolling_mean_13`** carries the same off-by-one as `lag_13` | Not separately stated in the thesis; it is the same root cause |

**Volunteer one defect, not four.** One well-evidenced flaw reads as
self-awareness; four reads as a thesis that needed another month. All are drilled
in `qa-drill.md`.

---

## Slide 06.2 — What transfers, and the closing claim

**Type:** Table + closing line · **Speaker:** B · **15:00–15:45** ·
**Layout:** table upper; closing sentence below, largest text on the slide

**On screen**

| Principle | Because we measured |
|---|---|
| **Delegation over generation** | tool arms identical every repeat; code arms differed almost every time |
| **Explicit refusal over silent fallback** | a fallback asserts something was found; an agent cannot tell |
| **Carry the track record, not only the interval** | interval spans 8–34× the forecast; the confidence index discriminates nothing |
| **Budget memory at selection time, report it at run time** | 4 GB excluded transformers up front; realised peak ~231 MB |
| **Report cost and latency beside accuracy** | 51× cost difference at comparable accuracy |

> A forecast becomes usable not when it is accompanied by an interval, but when it
> is accompanied by **evidence of how far the model producing it has been right
> before.**

**Notes — what to say**
> "Design science says an instantiation becomes a contribution only when the
> knowledge it embodies is stated separately from it. Each of these sits at the
> level of a problem class rather than our artefact, and each is falsifiable
> against the evidence column — we assert them because something in our evaluation
> would have come out differently had they not held.
>
> And the result we did not set out to find is the one we would keep. We set out to
> show that a dedicated forecasting layer was necessary. What we can actually
> defend is narrower and more useful: it earns its place on reproducibility, cost
> and auditability — **not on error alone**.
>
> A forecast becomes usable not when it is accompanied by an interval, but when it
> is accompanied by evidence of how far the model producing it has been right
> before."

**Grounded in:** Ch10 §10.2 (five principles, verbatim order and wording), §10.6
(the closing sentence — quoted almost exactly).

**Then stop.** Do not add a summary slide. 55% of the slot is dialogue, and
handing it over early is the strongest move available.

---

## Slide 07 — Let's discuss

**Type:** Title slide, no content · **Both** · **15:45–16:00**

Just the words. Everything after this is reserve — never presented, jumped to on
question.

---

# The reserve wall

**One question, one artefact.** Each slide titled as *the question it answers*,
so it is findable under pressure. Every file verified present 2026-09-19.
**No new figure is generated; nothing is copied into tier 06.**

| # | Slide title (= the question) | Artefact |
|---|---|---|
| R01 | The full seven-scenario comparison | `08_experimental_evaluation/tables/22_scenario_comparison.svg` |
| R02 | How runs failed, not just how badly | `.../23_outcome_taxonomy.svg` |
| R03 | What a single run actually looked like | `.../25_per_run_record_p1.svg` … `30_..._p6.svg` |
| R04 | Were the prompts really controlled? | `.../prompt_schema_composition.svg`, `31_run_configuration.svg` |
| R05 | The memory profile **(the F9 answer)** | `05_model_benchmark/tables/15_substrate_resource_profile.svg` |
| R06 | Sandbox-side resource measurement | `08_experimental_evaluation/tables/17_sandbox_resource_profile.svg` |
| R07 | Which baselines beat us, and where | `05_model_benchmark/tables/19_statistical_baselines.svg` |
| R08 | Why we won't name a winner | `.../20_seed_stability_p1.svg`, `21_..._p2.svg` |
| R09 | What retraining costs | `.../16_retraining_cost.svg` |
| R10 | Do the parameters drift? | `.../18_parameter_drift.svg` |
| R11 | What drives the model | `05_model_benchmark/figures/shap_importance.svg` |
| R12 | Does it track the actual series? | `.../fig3_forecast_overlay.svg` |
| R13 | How the serving model was chosen | `.../ch5_model_selection_v2.svg` |
| R14 | How the interval is communicated | `07_decision_synthesis/tables/24_interval_communication.svg` |
| R15 | The tool contract in full | `06_architecture/figures/ch6_tool_interface_v1.svg` |
| R16 | The data pipeline end to end | `04_data_assessment/figures/ch4_preprocessing_pipeline_v2.svg` |
| R17 | What is in the feature matrix | `.../08_feature_matrix_p1.svg` … `13_..._p6.svg` |
| R18 | Is there annual seasonality? **(lag-12 evidence)** | `04_data_assessment/figures/*/06_acf_pacf_plots.svg` |
| R19 | The research-question tree | `01_introduction/figures/ch1_research_questions_tree_v2.svg` |
| R20 | The model ladder | `05_model_benchmark/figures/fig1_model_ladder.svg` |

**Why the wall earns its place here specifically:** F6 item 4 notes the thesis
cites about two figures against 87 generated. Unanswered, that is a question an
examiner can ask. Built into a wall, it becomes the way questions get answered.

---

# Before the defence

- ⚠ **Inform supervisor *and* censor that GenAI was used in preparation.** CBS
  requirement, outside party, cannot be done from this repo. **No GenAI during
  the defence itself.**
- Print the deck for the examiners; check it survives greyscale.
- Bring `qa-drill.md` separately — exam aids are permitted in the room.
- Rehearse the two handovers (**02.2** and **05.3**) against a timer.
- Rehearse slide **01.2** hardest. It is the slide that turns a company feature
  request into a research contribution.
