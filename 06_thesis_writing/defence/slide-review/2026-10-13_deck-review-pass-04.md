---
name: 2026-10-13_deck-review-pass-04
description: REFERENCE - What is still open after the 2026-10-13 evening edit round. Grouped by slide, verbatim Currently / Edit / Should be, answers the 3 remaining PowerPoint comments.
category: reference
applies-to: [oral defence, slide deck]
triggers: [deck review, re-snap, what is left]
created: 2026_10_13-21_30
updated: 2026_10_13-21_30
snapshot_deck: 2026-10-13_21-18_content_pass_02
snapshot_thesis: 2026-10-10_16-42_deck-finalisation
supersedes: pass-03 in full (everything still open is carried here)
---

# Deck review, pass 04: what is left

Verified against deck snapshot `2026-10-13_21-18_content_pass_02` (40 slides, 3
comments). The thesis snapshot is unchanged. The repo is at `418e1e6`, and the fetch is clean.

**Slide numbers moved.** Slide 20 became four build slides (20–23), so everything after
it is **+3** from pass 03: Findings is 25, Contributions 26, Limitations 28, Future Work
29, Let's discuss 31. Three appendix slides were added (38–40).

Pass 03 is now closed. Everything still open from it is carried below, so you only
need this file.

---

## What landed from pass 03

| Pass 03 | Slide now | State |
|---|---|---|
| 8.1 source count, 8.2 Saunders line, 8.3 body | 8 | ✅ landed |
| 9.1 retail gap cell, 9.2 row order | 9 | ✅ landed. One stray-quote typo is new, see 9.1 below |
| 10.1 verbatim RQ | 10 | ❌ **not applied**, carried as 10.1 |
| 11.1 four bullets | 11 | ✅ landed, one typo (11.1) |
| 12.1 SRQ bullets | 12 | ✅ landed. You dropped the chapter tags; that's fine |
| 14.1–14.3 three columns + Hevner (2007) | 14 | ✅ landed |
| 15.1 METHODOLOGY | 15 | ✅ landed |
| 20.1 full A–G table | 20–23 | ✅ landed. One number is wrong and one label is misleading, see below |
| 22.1–22.2 findings table | 25 | ✅ landed, rewritten in your own words. Three fixes below |
| 23.1 231 MB, 23.2 "never identical" | 26 | ✅ both landed |
| 25.1 subtitle, 25.2 context | 28 | ✅ landed. Three fixes below |
| 26.1 subtitle, 26.2 context | 29 | ✅ landed. One capital letter |
| 28 `Let‘s` | 31 | ❌ still `Let‘s`, carried |

The optional summary sentences for slides 28 and 29 (pass 03 25.3, 26.3) were not added.
They're still optional; the text is repeated at the bottom of this file.

---

## Slide 8 — REVIEW APPROACH

### Your question in chat: "search terms from the research questions": is that okay?

**Yes, it's fine, and it is what the thesis says.** Ch2's preamble: *"Starting from the
research questions, key concepts and search terms were defined for each thematic
area"*. The slide paraphrases that sentence.

Your instinct is also right, and the two don't conflict. Saunders et al. describe the
literature review as **cyclical, not linear**:

- **Before** the research questions are fixed, a preliminary search of the literature
  helps generate and refine the research idea.
- **Once** questions and objectives exist, they set the parameters of the review and
  supply the keywords and search terms.
- The review then iterates: what you read sharpens the questions, and sharper questions
  send you back to search.

*(That summary of Saunders is from general knowledge of the book. Its chapter on
critically reviewing the literature is not in the repo, so I couldn't quote a page.
The thesis only cites Saunders for "narrative, integrative review" and "the iterative
manner characteristic of a literature review".)*

The thesis already tells this two-way story: the RQs moved from a multi-agent framing
to the present one, and *"the scope of the reviewed literature was refined in step"*.
If you want the slide to show both directions, one word does it:

| | |
|---|---|
| **Currently** | `Search terms per theme, from the research questions` |
| **Edit** | REWORD (optional) |
| **Should be** | `Search terms per theme, from the research questions, refined as they moved` |

**If asked:** "Early reading shaped the questions; once they were set, they drove the
search; and when they moved, we searched again. That's the iterative review Saunders
describes."

Nothing else is open on slide 8. The arrows between "~100 screened" and "~40 read" are
Wingdings glyphs. They render in PowerPoint and only disappear in the text export.

---

## Slide 9 — FIVE STRANDS

### Your comments

**9.a USER "re-format… fills the screen":** yours to do.

**9.b AGENT "We could use some text underneath the table (summary)":** see 9.2. It's
built from the sentence the thesis uses to close the gap (Ch2 Fig. 2 caption, and the
notes on slide 11), so it also sets up the next two slides.

### 9.1 Stray quotation marks in the Forecast-to-decision gap cell

| | |
|---|---|
| **Currently** | `couples prediction and decision tightly"; "does not concern large language model agents` |
| **Edit** | REPLACE (remove the two quotation marks left over from pass 03's evidence column) |
| **Should be** | `couples prediction and decision tightly; does not concern LLM agents` |

While you're in the table: `Demonstrate feasibility` is the only cell that starts with a
capital. Use `demonstrate feasibility` to match the others.

### 9.2 Summary line under the table

| | |
|---|---|
| **Currently** | nothing below the table |
| **Edit** | INSERT a single line below the table, bold on the last clause |
| **Should be** | `Each strand is well populated, and each stops short of the same point:` **`extending a live agentic system with forecasting, under the constraints a smaller firm actually faces.`** |

Source: slide 11's notes / Ch2 Fig. 2 caption, *"Each strand is individually well
populated, and each stops short of the same point: none addresses the extension of an
agentic decision-support system with forecasting models under the deployment
constraints a smaller firm actually faces."*

---

## Slide 10 — RESEARCH QUESTION (carried, not yet applied)

### Your comment

**10.a "What is the verbatim research question? Can you confirm."** Confirmed again. It's
unchanged in `00_thesis_context/research-questions/` and Ch10 §10.1:

> How can production-oriented agentic decision-support systems without native
> predictive capabilities be extended with lightweight forecasting models to support
> reliable, forecast-informed, and cost-justified decision-making under computational
> and deployment constraints?

### 10.1 Replace the short version

| | |
|---|---|
| **Currently** | `„How can agentic decision-support systems without forecasting be extended with lightweight models, under real deployment and cost constraints?“` |
| **Edit** | REPLACE |
| **Should be** | `„How can production-oriented agentic decision-support systems without native predictive capabilities be extended with lightweight forecasting models to support reliable, forecast-informed, and cost-justified decision-making under computational and deployment constraints?“` |

Bold: *production-oriented* · *extended with lightweight forecasting models* ·
*reliable* · *cost-justified*.

**The one thing not to do** is keep the short version in quotation marks. Quotation
marks say "verbatim". If the long one doesn't fit, drop the marks and keep the short one
as a paraphrase.

---

## Slide 11 — THE GAP

### 11.1 Grammar

| | |
|---|---|
| **Currently** | `the agents asks, the model answers` |
| **Edit** | REPLACE |
| **Should be** | `the agent asks, the model answers` |

(The figure's alt text says `Reasearch Gap`. It isn't shown on screen; fix it if you're
in there anyway.)

---

## Slides 20–23 — EXPERIMENT | Performance Overview (the build)

Your colour rule, checked on slide 23 (the final build): green = best, orange = middle,
red = worst. Every cell follows it, and the tiering reads sensibly. Moving F next to C
works: the left four are one orchestrator, the right three the other.

### 20.1 ⚠ D's latency is wrong, on all four slides

| | |
|---|---|
| **Currently** | `113.3 s` (column D, Latency row) |
| **Edit** | REPLACE on slides 20, 21, 22 and 23 |
| **Should be** | `111.3 s` |

Source: `22_scenario_comparison.md`, Response time, D = 111.3. Every other number in
the table matches the source.

### 20.2 ⚠ "Runs in: GPT 5.5 / Prometheus" implies two different language models

All seven scenarios use the **same** model. Ch3: *"All scenarios call the same dated
model snapshot, gpt-5.5-2026-04-23"*. What differs is the orchestrator: our local
harness versus Manifold's production platform. As it stands, the row says D, E and G
did *not* run on GPT-5.5, and an examiner who knows Ch3 can catch that.

| | |
|---|---|
| **Currently** | row label `Runs in`; cells `GPT 5.5` ×4, `Prometheus` ×3 |
| **Edit** | REPLACE the row label and the seven cells |
| **Should be** | row label `Orchestrator`; cells `Local` ×4 (A, B, C, F), `Prometheus` ×3 (D, E, G); and one small line under the table: `All seven scenarios use the same language model (GPT-5.5).` |

### 20.3 Slide 22 drops four reds that slides 21 and 23 have

A build should only ever add. Slide 22 removes four red cells that slide 21 introduced
and slide 23 brings back, so they flicker off and on while you're presenting:

| Cell | Slide 21 | Slide 22 | Slide 23 |
|---|---|---|---|
| A · Cost per answer `$ 0.38` | red | **black** | red |
| B · Cost per answer `$ 0.47` | red | **black** | red |
| D · Mean APE `25.0 %` | red | **black** | red |
| D · Variation `8.1 %` | red | **black** | red |

Edit: on slide 22, make those four cells red (bold + underlined), the same as slide 21.

### 20.4 Bold/underline isn't on every coloured cell

You said you bolded and underlined the coloured cells. On slide 23 these are coloured
but **plain**:

- **Median APE:** B `2.9 %` (green), F `7.3 %` (orange, and italic), G `1.8 %` (green)
- **Mean APE:** B `27.9 %` (red), D `25.0 %` (red), G `15.6 %` (green)
- **Variation:** B `4.1 %` (orange), D `8.1 %` (red), G `3.3 %` (orange)
- **Cost per answer:** A `$ 0.38`, B `$ 0.47`, F `$ 0.43`, G `$ 0.55` (all red)
- **Latency:** A `69.5 s` (orange), F `103.9 s`, D `113.3 s`, G `84.4 s` (all red)

Either apply bold + underline to all of them, or (my suggestion) **bold only the green
cells** and let colour carry orange and red. Bolding everything coloured is most of the
table, so the bold stops meaning anything.

Also: F's header cell `GPT 5.5` and its `7.3 %` are in *italics*. Nothing else in the
table is, so it reads as if F were special. Remove the italics.

### 20.5 Tier boundaries, only if asked

Latency: A `69.5 s` is orange and G `84.4 s` is red. Cost: E `$0.20` is orange and A
`$0.38` is red. Both are defensible, but be ready to say what the cut is (for example,
"green = best, red = clearly worst, orange in between, judged per row"). If the
colours look like they came from a rule, an examiner may ask what the rule is.

---

## Slide 25 — FINDINGS (was 22)

### 25.1 Spelling

| | |
|---|---|
| **Currently** | `truthful, not useable` |
| **Edit** | REPLACE |
| **Should be** | `truthful, not usable` |

### 25.2 "Parameter-free benchmarks": Prophet isn't parameter-free

| | |
|---|---|
| **Currently** | `2 categories lose to parameter-free benchmarks` |
| **Edit** | REWORD |
| **Should be** | `2 categories lose to simple benchmarks: seasonal naive on RTD, Prophet on water` |

Ch5 is precise: *"both lose to seasonal naive on RTD and to Prophet on danskvand"*.
Seasonal naive has no parameters; Prophet has many. Ch10 says "parameter-free" for both,
which is loose. Don't repeat it on screen, where an examiner can point at it.

### 25.3 The combined-runs caveat isn't in the thesis

| | |
|---|---|
| **Currently** | `Performance of combining all three (Data, Code, Model) heavily relies on relative model performance` |
| **Edit** | REPLACE |
| **Should be** | `Combined runs (F, G) each invented their own weight for our forecast: the tool gives them none` |

Source: Ch9, *"Every combined run departed from the model's forecast… the payload
supplies no quantity from which a brand-specific weight could be derived, so each run
invented its own."* It also links straight to slide 29's "Per-Series Error" row.

Everything else on the slide checks out:

- gradient boosters beat Ridge and ARIMA in every category (Ch5)
- the seed flips the winner in all four categories (Ch5)
- fitting peaks at 35 MB
- every reported figure matched the tool payload (Ch9)
- 3 of 7 scenarios ran in production
- data access takes the median error from 502% to 2.9%

---

## Slide 28 — LIMITATIONS (was 25)

### 28.1 The run count doesn't add up on screen

| | |
|---|---|
| **Currently** | `3 brands, 1 category, 3 repeats: = 63 runs` |
| **Edit** | REPLACE |
| **Should be** | `7 scenarios × 3 brands × 3 repeats = 63 runs, in 1 category` |

3 × 3 is 9. Without the 7 scenarios the 63 looks like an arithmetic error.

### 28.2 "One brand" changes the claim

| | |
|---|---|
| **Currently** | `Intervals too wide to act on for one brand` |
| **Edit** | REWORD |
| **Should be** | `Intervals too wide to act on for any individual brand` |

Ch9 §9.4: *"too wide to act on for an individual brand"*, meaning *per brand, in
general*. "For one brand" reads as "only one brand was affected", which understates it.
An examiner who has read §9.4 would notice.

### 28.3 Spelling

| | |
|---|---|
| **Currently** | `the two effects can not be seperated` |
| **Edit** | REPLACE |
| **Should be** | `the two effects cannot be separated` |

---

## Slide 29 — FUTURE WORK (was 26)

### 29.1 Capital letter

| | |
|---|---|
| **Currently** | `the two techniques the code agents applied` |
| **Edit** | REPLACE |
| **Should be** | `The two techniques the code agents applied` |

The reconciliation row's *"One estimator needs no residual history, so it works for
agent forecasts too"* is checked against §9.5 (*"one of which requires no residual
history and would therefore extend to the scenario forecasts"*). ✅

---

## Slide 31 — Let's discuss! (carried)

| | |
|---|---|
| **Currently** | `Let‘s discuss!` (opening quotation mark ‘) |
| **Edit** | REPLACE |
| **Should be** | `Let's discuss!` (apostrophe ’) |

---

## Appendix slides 38–40 (new)

### 39.1 ⚠ "Model Performance" contradicts slide 25

Slide 39 shows `fig1_model_ladder.svg`. This figure is **not in the thesis** (it isn't
in the table of figures). It plots the **untuned** models, and its embedded title reads:

> `SRQ1 model ladder (brand×month, untuned) — every model beats SeasonalNaive`

Slide 25, Ch5 and Ch10 all say that two categories lose to simple benchmarks once the
models are tuned. An examiner who opens the appendix sees "every model beats
SeasonalNaive", and the internal "SRQ1 / untuned" label on top of it.

| | |
|---|---|
| **Currently** | slide 39, figure `fig1_model_ladder.svg` |
| **Edit** | REPLACE the figure, or DELETE the slide |
| **Should be** | a figure the thesis uses: **Figure 8, "Model Metadata – XGBoost & LightGBM – Tuned per Category"**, or Ch5's `ch5_model_selection_v2.svg` |

Slides 38 (Resource Profile, thesis Fig. 7) and 40 (Forecast Overlay, thesis Fig. 6) are
both thesis figures and are fine. Their notes say `- None`, which will be covered in the
notes pass.

---

## Still optional, carried from pass 03

| # | Slide | Item |
|---|---|---|
| O.1 | 28 | Summary sentence: *"Every claim in this thesis is sized to one category, three brands and sixty-three runs."* |
| O.2 | 29 | Summary sentence (verbatim §9.5): *"Five directions follow from what this evaluation could not settle."* |
| O.3 | 28 | Optional lag-13 bullet. Your call under don't-volunteer |
| O.4 | 3, 16, 31 | Divider titles to caps; alt text missing on slide 1 (CBS logo) and slide 35 (Graphic 2); slides 34–36 still share the title "Raw Nielsen Dataset Schema" |

---

## Then: speaker notes

Not part of this pass, as you asked. Once the content is frozen, the notes pass uses
your slide 26 four-block layout (Final Speaker Notes / What can be said / Content in
Plain English / Practice Notes) on every content slide. Known problems already in the
notes field:

- slide 8's "eight sections / 2.8 paradigm" is wrong
- slide 19 says 34 MB
- slides 28 and 29 hold copies of slide 26's notes
- slides 11, 12, 15, 19, 37–40 still carry "Original Figure Description"
- slide 25 says "Some Notes (Not final)"
