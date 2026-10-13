---
name: 2026-10-13_deck-review-pass-03
description: REFERENCE - Slide-content pass on the defence deck, grouped by slide. Every edit has a verbatim Currently / Edit / Should be. Answers all 18 PowerPoint comments. Speaker notes deliberately deferred.
category: reference
applies-to: [oral defence, slide deck]
triggers: [finalise the deck, slide content, deck comments]
created: 2026_10_13-18_30
updated: 2026_10_13-18_30
snapshot_deck: 2026-10-13_17-42_content_pass
snapshot_thesis: 2026-10-10_16-42_deck-finalisation
supersedes: 2026-10-10_deck-review-pass-02.md (§1, §2, §3, §5); its §4 speaker notes wait for the notes pass
---

# Deck review — pass 03 (slide content)

## How to use this file

- **One section per slide, in deck order.** Work top to bottom with PowerPoint open
  beside it; you never jump back.
- Every edit is a small table: **Currently** (the exact text on the slide, so you can
  Ctrl+F it), **Edit** (what to do), **Should be** (paste-ready).
- Your PowerPoint comments are answered **inside the slide they sit on**, above the edits.
- Slides with nothing to change are listed in one line at the end, so you know they
  were checked.
- **Speaker notes are not in this pass.** As you asked: content first, notes after.
  The template for that pass is at the bottom.

Checked against: deck snapshot `2026-10-13_17-42_content_pass` (37 slides, 18 comments);
thesis snapshot `2026-10-10_16-42_deck-finalisation` (unchanged since submission);
`05_thesis_results/08_experimental_evaluation/tables/22_scenario_comparison.md`.

## What already landed from pass 02

| Pass 02 item | Status |
|---|---|
| 1.1 Saunders 2021 → 2023 | ✅ |
| 1.2 ~150/~60 → ~100/~40 | ✅ |
| 1.4 61 sources → 42 / 62 | ✅ (wording follow-up in slide 8 below) |
| 1.6 slide 9 "Adress", "at scale" | ✅ rewritten |
| 1.8 MdAPE → median APE | ✅ — Hevner (2007) for the three cycles still missing (slide 14 below) |
| 1.9 METHDOLOGY | ½ — fixed on 14, **still on 15** |
| 1.10 51× / 21× | ✅ (the multipliers are no longer on slide 20) |
| 1.11 "in every run where the tool was called" | ✅ |
| 1.12 agenda missing DISCUSSION | ✅ |
| 2.1 delete "approach" slide | ✅ |
| 3.4 design-principles slide | ✅ built as slide 23 (one fact error, below) |
| 1.7 slide 10 RQ not verbatim | ☐ below |
| 2.3 split limitations item 5 | ☐ below (now optional) |

---

## Slide 8 — REVIEW APPROACH

### Your comments

**8.a "Is there a Saunders et al. term for this procedure?"** No, and don't add one.
The thesis cites Saunders for two things only: that this is a *"narrative, integrative
review rather than a systematic review"*, and that refining the scope as the questions
moved is *"the iterative manner characteristic of a literature review"* (Ch2 preamble).
The search steps themselves (~100 screened, ~40 read) have no Saunders label in the
thesis. If you named one on the slide, the examiner could find it nowhere in the thesis.

**8.b "Sounds like we had 42 / 62 peer-reviewed papers. Is that true?"** No. Ch2 says
*"forty-two cited sources, of which 14 are flagged as preprints or non-peer-reviewed"*,
so **28 of the 42 are peer-reviewed**. The 62 is every source cited anywhere in the
thesis, and nobody counted how many of those are peer-reviewed. Because the line sits
under "Peer-reviewed prioritized", it does read as 42 peer-reviewed papers. Fix below.

**8.c "Could use improved formatting."** See 8.3: three blocks, each with a bold label
and two short sub-bullets.

### 8.1 The source count

| | |
|---|---|
| **Currently** | `flagged throughout → 42 in this chapter, 62 sources across thesis` |
| **Edit** | REPLACE |
| **Should be** | `flagged throughout → 42 sources in this chapter: 28 peer-reviewed, 14 preprints` |

Drop the 62. It's a thesis-wide count on a slide about the literature chapter, and it
invites exactly the misreading in 8.b.

### 8.2 Saunders citation sits on the wrong line

| | |
|---|---|
| **Currently** | `thematic synthesis, not a protocol-driven search (Saunders et al., 2023)` |
| **Edit** | MOVE the citation up one line |
| **Should be** | `Not a systematic review (Saunders et al., 2023)` as the heading; `thematic synthesis, not a protocol-driven search` with no citation |

The thesis attaches Saunders to "narrative, integrative review rather than a systematic
review", not to "thematic synthesis".

### 8.3 Formatting: whole slide

| | |
|---|---|
| **Currently** | 3 underlined headings, one long un-nested bullet (`Search terms derived per theme…`), mixed sub-bullet lengths |
| **Edit** | REPLACE the body |
| **Should be** | see below |

> **Narrative, integrative review** — not systematic *(Saunders et al., 2023)*
> - several literatures **intersect**; no single bounded question
> - **thematic synthesis**, not a protocol-driven search
>
> **Iterative search**
> - search terms per theme, **from the research questions**
> - **~100 screened** by title → **~40 read closely**; thin themes re-searched
>
> **Peer review prioritised**
> - **42 sources**: 28 peer-reviewed, 14 preprints, each flagged
> - throughout: what the literature **establishes** vs what we **design**

Remove the underlines; bold carries the labels.

---

## Slide 9 — FIVE STRANDS

### Your comments

**9.a "Double check accuracy of information."** Four of the five rows check out against
Ch2 §2.7, most of them near-verbatim. The **Retail demand forecasting** row has an
unsourced gap cell. Fix in 9.1.

| Row | Supplies | Gap | Source |
|---|---|---|---|
| Forecast-to-decision | ✅ "create value predominantly through their connection to downstream decisions" | ✅ "couples prediction and decision *tightly*"; "does not concern large language model agents" | §2.7 ¶1 |
| LLM agents & tool use | ✅ "tool delegation can substitute for raw model scale" | ✅ "does not address forecasting, reliability, or production constraints" | §2.7 ¶2 |
| Reliability & evaluation | ✅ "agentic outputs carry measurable risks" | ✅ "supply requirements but not the integration" | §2.7 ¶3, ¶5 |
| Production agentic systems | ✅ "demonstrate feasibility" | ✅ "real-time supervision of a live process on dedicated infrastructure" | §2.7 ¶4 |
| Retail demand forecasting | ✅ gradient boosting wins M5; cross-learning (§2.1) | ⚠ "benchmark compute; nothing on serving the forecast": **no thesis sentence says this** | — |

One thing to be ready for: §2.7 names **four** literatures in its gap, and slide 11's
figure shows four. Retail forecasting is the fifth strand on this slide because it is
the method source (§2.1), not one of the four the gap is built from. If asked "five or
four?", that's the answer.

**9.b "Re-format so it follows the general style and fills the screen."** Make it look
like slides 20 and 23. In 9.2: the same bold header row, underlined row labels, full
content width, 14–16 pt body. Also re-order the rows to follow the chapter.

### 9.1 Retail row, gap cell

| | |
|---|---|
| **Currently** | `benchmark compute; nothing on serving the forecast` |
| **Edit** | REPLACE |
| **Should be** | `accuracy-first: compute treated as secondary` |

Source: Ch2 §2.2, *"computational constraints that are often treated as secondary design
considerations in forecasting research"*.

### 9.2 Row order and layout

| | |
|---|---|
| **Currently** | Forecast-to-decision · LLM agents · Reliability · Production · **Retail forecasting last** |
| **Edit** | MOVE the Retail row to the top, then re-size the table to the full content width |
| **Should be** | Retail demand forecasting (§2.1) · Forecast-to-decision (§2.3) · LLM agents & tool use (§2.4) · Reliability & evaluation (§2.5) · Production agentic systems (§2.6) |

That puts the slide in chapter order, so the talk runs from "how to forecast" to "where
the forecast has to go".

---

## Slide 10 — RESEARCH QUESTION

### Your comment

**10.a "What is the verbatim research question? Can you confirm."** Confirmed from
`00_thesis_context/research-questions/` and Ch10 §10.1, which restates it:

> **How can production-oriented agentic decision-support systems without native
> predictive capabilities be extended with lightweight forecasting models to support
> reliable, forecast-informed, and cost-justified decision-making under computational
> and deployment constraints?**

(Ch1 §1.3's own copy of the RQ doesn't appear in the Word export: the line after
*"The overarching research question guiding this thesis is:"* comes out empty, which
probably means it sits in a text box. Worth a 10-second check in Word that it shows up
on the page.)

### 10.1 Restore the verbatim RQ

| | |
|---|---|
| **Currently** | `„How can agentic decision-support systems without forecasting be extended with lightweight models, under real deployment and cost constraints?“` |
| **Edit** | REPLACE (keep the quotation marks, since it's now verbatim) |
| **Should be** | `„How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed, and cost-justified decision-making under computational and deployment constraints?“` |

**Bold these four phrases:** *production-oriented* · *extended with lightweight
forecasting models* · *reliable* · *cost-justified*. They are the four words the rest of
the deck answers.

It's long. If it won't fit at your font size, drop the quotation marks and keep the
short version. **Don't keep both**: short text in quotation marks reads as a misquote.

---

## Slide 11 — THE GAP

### Your comment

**11.a "Bullet points could use re-wording."** They are §2.7's gap sentence cut into
four, so each bullet is a sentence fragment. 11.1 gives each bullet its own claim, with
a bold lead.

### 11.1 Re-word the four bullets

| | |
|---|---|
| **Currently** | `How a production agentic system without native predictive capability` / `can be extended with lightweight forecasting` / `through a loose, agent-mediated, reliable and traceable tool interface` / `whether dedicated-model integration improves on a code-as-action LLM baseline that writes its own forecasting code.` |
| **Edit** | REPLACE all four |
| **Should be** | see below |

> - **Agents that explain, not forecast**: a production system with no predictive capability
> - **Extend, don't rebuild**: add lightweight forecasting models inside the existing system
> - **Loosely coupled through a tool**: the agent asks, the model answers, every figure traceable
> - **Tested against the obvious alternative**: is a dedicated model better than an LLM writing its own forecasting code?

Source: Ch2 §2.7, closing paragraph. Every bullet is a paraphrase of one of its clauses.

---

## Slide 12 — THE RESEARCH QUESTIONS

### Your comment

**12.a "Copy-pasted from the previous slide. Needs its own bullets that fit the
figure."** The figure is the RQ tree, so the bullets should name the four
sub-questions: one per layer, each with the chapter that answers it.

### 12.1 Replace the bullets

| | |
|---|---|
| **Currently** | the same four bullets as slide 11 (`How a production agentic system…`) |
| **Edit** | REPLACE all four |
| **Should be** | see below |

> - **SRQ1 Substrate:** which lightweight models trade accuracy against memory best *(Ch5)*
> - **SRQ2 Interface:** how a forecast reaches the agent, reliable, uncertain and traceable *(Ch6–7)*
> - **SRQ3 Host system:** what a production agent must already do before forecasting can attach *(Ch7, Ch9)*
> - **SRQ4 Evidence:** does a dedicated model beat an agent writing its own code, at justified cost? *(Ch8)*

Chapter mapping: Ch1 §1.3. SRQ2 is "Section 6.4 and Chapter 7"; SRQ3 is "assessed in
Chapter 7 and Chapter 9".

The subtitle line `Thesis as an outcome from the overlap between our interest and
Manifold Business Case` is fine as it is.

---

## Slide 14 — METHODOLOGY | Central Academic Grounding

### Your comment

**14.a "Condense each bullet and/or use keyword highlighting."** Every bullet below is
cut to one line, the bold label stays, and one keyword is set in *italics*. The underlines
come off. This also fixes the overflow: column 3 currently runs past the bottom edge of
the slide.

### 14.1 Column 1, RESEARCH

| | |
|---|---|
| **Currently** | 4 bullets, e.g. `Modest realism: demand exists independently; the panel reaches it through an instrument that carries its own assumptions` |
| **Edit** | REPLACE the four bullets |
| **Should be** | see below |

> - **Pragmatism:** claims judged by what they *enable*
> - **Modest realism:** demand is real; the panel *measures* it imperfectly
> - **Strategy:** quantitative experiment in a *single embedded case*
> - **Secondary data:** commercial panel access is a *strength*, not a shortcut

### 14.2 Column 2, FORECASTING

| | |
|---|---|
| **Currently** | 4 bullets, e.g. `Metric discipline: wMAPE primary, median APE and MASE alongside; percentage errors break on near-zero demand` |
| **Edit** | REPLACE the four bullets |
| **Should be** | see below |

> - **Out-of-sample:** expanding-window CV; test split *never seen* in selection
> - **Metrics:** *wMAPE* primary; median APE and MASE alongside
> - **Benchmarks:** naive and seasonal-naive are the *floor*
> - **Classical families:** ARIMA; no exponential smoothing → *a limitation*

"Percentage errors break on near-zero demand" moves to the speaker notes.

### 14.3 Column 3, DESIGN SCIENCE: condense and add the missing citation

| | |
|---|---|
| **Currently** | header `Hevner et al. (2004) & Peffers et al. (2007)`; bullet `Three cycles: relevance (Manifold AI), design (Chapters 5–8), rigor (Chapter 2)` has no source |
| **Edit** | REPLACE the header and the four bullets |
| **Should be** | header `Hevner et al. (2004) · Hevner (2007) · Peffers et al. (2007)`, then: |

> - **Artefact + design knowledge**, *both* assessed
> - **Three cycles:** relevance (Manifold), design (Ch 5–8), rigour (Ch 2)
> - **Six activities:** problem → objectives → design → demonstration → evaluation → communication
> - **Judged against** *stated objectives*, not novelty

The three cycles come from Hevner (2007), *"A three cycle view of design science
research"*. Ch3 cites it for exactly this, and it is in the reference list.

---

## Slide 15 — METHODOLOGY | Summarized Approach

### 15.1 Title typo

| | |
|---|---|
| **Currently** | `METHDOLOGY` |
| **Edit** | REPLACE |
| **Should be** | `METHODOLOGY` |

---

## Slide 20 — EXPERIMENT | Performance Overview

### Your comment

**20.a "We are missing scenario D, F, G."** **E** is missing too: the slide shows
A, B and C only. Here is the full table, transcribed from the thesis's scenario table
(`22_scenario_comparison.md`). The rows and number formats match the slide.

⚠ **Know this before you add D.** D (code agent inside the production platform) has the
**best median error of all seven, 0.9%**, so the slide will then show a scenario beating
ours on the headline accuracy number. That's already in the thesis (Ch8 §8.3), and the
answer is the thesis's own line: *"it wins on the axis usually reported and loses on
three that usually are not"* (Ch9 §9.2.3). In the table, D also costs ~84× more per
answer than C, is ~19× slower, and is never identical on repeat. So it's safe to show,
as long as you've rehearsed that answer.

### 20.1 Replace the table

| | |
|---|---|
| **Currently** | 4 columns: `Measure · A_LLM_plain · B_data_code · C_model` |
| **Edit** | REPLACE with 8 columns |
| **Should be** | see below |

| Measure | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| *Runs in* | *general* | *general* | *general* | *production* | *production* | *general* | *production* |
| *Gets* | *nothing* | *data + code* | *our model* | *data + code* | *our model* | *both* | *both* |
| Usable answers | 6/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 |
| Median APE | 502.2% | 2.9% | 14.6% | **0.9%** | 14.6% | 7.3% | 1.8% |
| Mean APE | 662.1% | 27.9% | **13.1%** | 25.0% | **13.1%** | 18.3% | 15.6% |
| Variation across repeats | 26.7% | 4.1% | **0.0%** | 8.1% | **0.0%** | 1.7% | 3.3% |
| Identical on repeat | 0% | 0% | **100%** | 0% | **100%** | 33% | 33% |
| Cost per answer | $0.38 | $0.47 | **$0.009** | $0.77 | $0.20 | $0.43 | $0.55 |
| Latency | 69.5 s | 123.8 s | **6.0 s** | 111.3 s | 31.7 s | 103.9 s | 84.4 s |

**Bold only the best value in each row**, as above. The current slide bolds almost
every cell.

Cost is rounded to cents, apart from C, where two decimals would show $0.01 and hide
the gap. If you'd rather keep four decimals, use `$0.3798 · $0.4667 · $0.0091 · $0.7664
· $0.1994 · $0.4253 · $0.5536` throughout. The current slide mixes `$0.38` with
`$0.4667`.

### 20.2 Scenario names

| | |
|---|---|
| **Currently** | `A_LLM_plain`, `B_data_code`, `C_model` (code-style names) |
| **Edit** | REPLACE with single letters plus the two italic rows above |
| **Should be** | `A … G` |

The underscored names are internal identifiers. The two italic rows tell the examiner
what each letter is without a legend. The labels follow Ch8's per-brand table: *"A, no
firm data · B, data and code · C / E, dedicated model · F, both · D, data and code,
production · G, both, production"*.

---

## Slide 22 — FINDINGS | What each layer answered, and what it cost us

### Your comments

**22.a "What does this slide even say? Why Finding vs. Reported?"** It's Ch10 §10.1 in
table form: one row per sub-question. The left column is **the answer**. The right
column is **the qualification we report against ourselves**: what the answer doesn't
give you, or what it cost. The slide's message is that every answer comes with a
qualification, which is the thesis's closing argument: *"The contribution is qualified,
and the qualification is the point"* (abstract).

"Reported" is the wrong word for that column, which is why it's unclear. Rename both
headers (22.1).

**22.b "Too much text. Break cells into bullets, bold keywords."** Done in 22.2. Each
cell becomes two short bullets with one bold phrase each. The words are cut, the facts
are not.

### 22.1 Column headers

| | |
|---|---|
| **Currently** | `Finding` · `Reported` |
| **Edit** | REPLACE |
| **Should be** | `What we found` · `The catch` |

(If "The catch" is too informal for you, use `What it does not give us`.)

### 22.2 The four rows as bullets

| | |
|---|---|
| **Currently** | 8 cells of 1–2 full sentences each (e.g. `Both gradient boosters beat Ridge and ARIMA in all four categories; fitting peaks at 35 MB against a 4 GB ceiling`) |
| **Edit** | REPLACE every body cell |
| **Should be** | see below |

| | What we found | The catch |
|---|---|---|
| **SRQ1** substrate | • **Gradient boosters win** over Ridge and ARIMA, all 4 categories<br>• Fitting peaks at **35 MB** of 4 GB | • **XGBoost vs LightGBM undecidable**: the seed flips the winner in all 4<br>• 2 categories lose to **parameter-free benchmarks** |
| **SRQ2** interface | • **Every reported figure matched** the tool payload<br>• in every run where the tool was called | • Interval is **8–34× the forecast** at 90%: truthful, not usable<br>• The **track record** carries reliability, not the interval |
| **SRQ3** host system | • **3 of 7 scenarios ran in production**<br>• readiness taken from what integration actually needed | • **Assessed, not deployed**<br>• remaining gap is **operational**: credentials and a merge |
| **SRQ4** evidence | • **Data access alone**: median error 502% → 2.9%<br>• No scenario leads on every axis | • Our model **doesn't win on accuracy**<br>• it wins on **~50× cost, ~20× speed, zero variance** |

Every fact is the slide's existing claim, verified against Ch10 §10.1 in pass 02 §2.2.
Nothing is added.

**Optional third bullet for SRQ1, left column:** `• Pooling helps the **two smallest**
categories`. SRQ1 asks about *category specialisation* and the slide never answers it.
Source: Ch10 §10.1, *"pooling across categories wins on the two smallest by four to six
percentage points and is indecisive on the larger two"*. It's already in your notes; add
it to the slide only if it fits.

---

## Slide 23 — CONTRIBUTIONS | Five Design Principles

### 23.1 ⚠ The memory figure is mislabelled

| | |
|---|---|
| **Currently** | `Model Fitting realised peak ~231 MB` |
| **Edit** | REPLACE |
| **Should be** | `Realised end-to-end peak ~231 MB, under 6%` |

231 MB is the **end-to-end** peak: data, models and tool together. Ch9 DP4: *"the
realised end-to-end peak is approximately 231 MB, under six per cent"*. **Model fitting**
peaks at 35 MB, which is what slide 22 says. With the current label, slides 22 and 23
give two different numbers for the same thing.

### 23.2 "Almost every time" understates the result

| | |
|---|---|
| **Currently** | `Code-written answers differed almost every time` |
| **Edit** | REWORD |
| **Should be** | `Code-written answers were never identical across repeats` |

B and D are **0%** identical on repeat (scenario table). "Almost every time" is weaker
than what you measured.

Everything else on the slide checks out against Ch10 §10.2 and Ch9 §9.2.2, including the
closing sentence, which matches §10.6.

---

## Slide 25 — LIMITATIONS

### Your comments

**25.a "Need a subtitle."** It currently reads `Five Design Principles`, copied from
slide 23 (25.1).
**25.b "Need context bullets."** 25.2 gives two per row, all from Ch9 §9.4.
**25.c "Optional summary sentence."** 25.3. It goes in the `TEXT` placeholder.

### 25.1 Subtitle

| | |
|---|---|
| **Currently** | `LIMITATIONS \| Five Design Principles` |
| **Edit** | REPLACE the subtitle |
| **Should be** | `LIMITATIONS \| What bounds our claims` |

### 25.2 Context column

| | |
|---|---|
| **Currently** | every Context cell is empty |
| **Edit** | INSERT |
| **Should be** | see below |

| Limitation | Context |
|---|---|
| Sample Size and Variation within Scenarios | • **3 brands, 1 category, 3 repeats**: 63 runs<br>• detects **large differences only** |
| Forecasting Practice and Asymmetry inside the Substrate | • our baseline lacks **exponential smoothing and a seasonal term**; the code agents used both on every run<br>• *(optional, see note)* the annual cycle found in the EDA only **partly reaches** the model's features |
| Per-Series Adaptation and Code Execution | • code agents fit **per brand**, our model **per category**<br>• where they win, the two effects **can't be separated** |
| Interval Coverage, Width, and Bounding of Point Forecasts | • intervals **too wide to act on** for one brand; 3 alternative calibrations didn't fix it<br>• implausible forecasts **clipped after** back-transformation, not prevented by it |
| Planner Decisions and the Mixed Hierarchical and Grouped Structure | • **no test** of whether a planner decides better (needs human participants)<br>• brand forecasts **not reconciled** with category totals |

**Note on the optional bullet in row 2.** That bullet is the lag-13 item. The row title
("Asymmetry inside the Substrate") already names it, which is enough to count as stated.
Leave the bullet out if you want it less visible (don't volunteer). Put it in if you'd
rather the slide say it plainly in your own words before an examiner asks. Both are
consistent with "never deny". **Your call.**

The interval bullet deliberately doesn't claim coverage is met. Ch9 says it is, but
Ch5's table shows two categories short of 90% (drill Q16).

### 25.3 Summary sentence (optional)

| | |
|---|---|
| **Currently** | `TEXT` |
| **Edit** | REPLACE, or delete the placeholder |
| **Should be** | `Every claim in this thesis is sized to one category, three brands and sixty-three runs.` |

Grounded in Ch9 §9.4 ¶1. It turns the biggest limitation into a statement of scope,
which is how the thesis treats it.

### 25.4 Split row 5 (optional, carried from pass 02 §2.3)

| | |
|---|---|
| **Currently** | `Planner Decisions and the Mixed Hierarchical and Grouped Structure` |
| **Edit** | SPLIT into two rows |
| **Should be** | `Planner Decisions Untested` · `Hierarchical Structure Unexploited` |

The thesis treats these as two unrelated paragraphs (§9.4 ¶6 and ¶7). Splitting makes
six rows, so only do it if the table still fits. With 25.2's two bullets per cell, it
also works unsplit.

---

## Slide 26 — FUTURE WORK

### Your comments

**26.a "Need subtitle."** 26.1. **26.b "Need context bullets."** 26.2, from Ch9 §9.5.
**26.c "Optional summary sentence."** 26.3, the thesis's own opening line for §9.5.

### 26.1 Subtitle

| | |
|---|---|
| **Currently** | `FUTURE WORK \| Five Design Principles` |
| **Edit** | REPLACE the subtitle |
| **Should be** | `FUTURE WORK \| What the next design cycle closes` |

### 26.2 Context column

| | |
|---|---|
| **Currently** | every Context cell is empty |
| **Edit** | INSERT |
| **Should be** | see below |

| Future Work | Context |
|---|---|
| Exponential Smoothing and a Seasonal Term in the Classical Baseline | • the two techniques the code agents applied **unprompted, every run**<br>• cheap, established; **comparison not settled** until we have them |
| Per-Series Error Rather Than a Per-Category One | • the tool sends **one error per category**<br>• combined runs each **invented their own** brand-level weight |
| Reconciling Brand-Level Forecasts Against Category and Market Aggregates | • make brand forecasts **add up** to category and market totals<br>• one estimator needs no residual history, so it works for **agent forecasts too** |
| Widening the Evaluation Across Categories and Repeats | • more categories, more repeats<br>• needed **before any accuracy claim** at all |
| Whether a Communicated Forecast Improves a Planner's Decision | • an experiment **with human participants** *(Goodwin, Önkal & Thomson, 2010)*<br>• a **different study**, not an extension |

### 26.3 Summary sentence (optional)

| | |
|---|---|
| **Currently** | `TEXT` |
| **Edit** | REPLACE |
| **Should be** | `Five directions follow from what this evaluation could not settle.` |

Verbatim, Ch9 §9.5.

### 26.4 Order the rows to match slide 25 (optional)

Each future-work item answers a limitation. Ordered like this, row *n* on slide 26
continues row *n* on slide 25, and you can say "every limitation has a next step"
without having to show it:

| Slide 25 row | → Slide 26 row, in this order |
|---|---|
| 1 Sample size | Widening the Evaluation |
| 2 Forecasting practice | Exponential Smoothing and a Seasonal Term |
| 3 Per-series adaptation | *(no future-work item: a per-brand model needs a longer panel, §9.4)* |
| 4 Interval | Per-Series Error |
| 5 Planner + hierarchy | Planner's Decision · Reconciling |

Result: **Widening · Exponential Smoothing · Per-Series Error · Planner's Decision ·
Reconciling.**

---

## Slide 28 — Let's discuss!

| | |
|---|---|
| **Currently** | `Let‘s discuss!` (opening quotation mark) |
| **Edit** | REPLACE the character |
| **Should be** | `Let's discuss!` |

---

## Optional design polish (not content)

| Slide | Currently | Should be |
|---|---|---|
| 3 | `BACKGROUND & Motivation` | `BACKGROUND & MOTIVATION` |
| 16 | `Modelling, ARCHITECTURE & EXPERIMENT` | `MODELLING, ARCHITECTURE & EXPERIMENT` |
| 29 | `appendix` | `APPENDIX` |
| 22, 23, 25, 26 | table alt text `Table: Scenario Experiment Results` (copied from slide 20) | name each table for what it is; screen readers only, invisible when projected |
| 32, 33 | figures have no alt text | add a one-line description |
| 31–33 | three slides titled `Raw Nielsen Dataset Schema` with identical notes | add `(1/3)`, `(2/3)`, `(3/3)` or name each category |

---

## Checked, nothing to change

Slides **1, 2, 4, 5, 6, 7, 13, 16, 17, 18, 19, 21, 24, 27, 29–37**. Dividers, figures
whose captions were already checked in pass 02, the reference list (all seven slide-4/5
sources are there), and the appendix. Slides 4 and 5 sources and Royal Unibrew: you
settled those earlier (fine as they are).

---

# Deferred to the speaker-notes pass

Not for now. Recorded here so nothing is lost once the content is final.

## The template (from your slide 23)

Every content slide gets the same four blocks. Dividers get none.

| Block | Holds |
|---|---|
| **Final Speaker Notes** | empty. You and Enrico write it in your own words |
| **What can be said (suggestions)** | 2–4 bullets, each ending with its thesis section |
| **Content in plain English** | one line per element on the slide, for the non-technical examiner |
| **Practice notes** | how to deliver it: what to pick, what to skip, what to close on |

## Known errors already in the notes field

| Slide | Problem |
|---|---|
| 8 | says *"eight sections in the chapter… 2.8 is the methodological paradigm"*. Ch2 has ten sections; 2.8 is Contributions, 2.9 is DSR |
| 19 | the pasted figure caption says *"requires 34 MB to fit"*; the thesis says 34.5 MB (pass 02 §3.1) |
| 25, 26 | the notes are a copy of slide 23's design-principles notes |
| 11, 12, 15, 17, 18, 19, 30–37 | still hold the pasted *"Original Figure Description"* |

Pass 02 §4 holds drafted bullets for slides 4–26. They become the "What can be said"
block once the content is frozen, re-checked against the final slides.
