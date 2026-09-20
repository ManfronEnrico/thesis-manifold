---
name: 2026-09-20_deck-review-pass-01
description: REFERENCE - Slide-by-slide fact check of the defence deck against the thesis, with rewrites and speaker-note bullets.
category: reference
applies-to: [oral defence, slide deck]
triggers: [deck review, fact check slides, slide rewrites]
created: 2026_09_20-19_40
updated: 2026_09_20-19_40
snapshot_deck: 2026-09-20_19-24_review_pass
snapshot_thesis: 2026-09-20_14-09_defence-deck-citation-audit
---

# Deck review — pass 01

Deck snapshot `2026-09-20_19-24_review_pass` (40 slides, unchanged since
`19-14_layout_audit`). Thesis snapshot `2026-09-20_14-09_defence-deck-citation-audit`.
Results artefacts read directly from `05_thesis_results/`.

**Every number on slides 21 and 23 traces to source and is correct.** The defects
below are citations, counts, vocabulary and two internal contradictions — not the
evidence base.

---

# Read this first — the three that cost marks

| # | Slide | Defect | Fix |
|---|---|---|---|
| **A1** | **15** | `Saunders et al. (2021)` — the thesis uses **2023** (9th ed.) in all 8 in-text occurrences. There is no 2021 Saunders anywhere. Slide 8 already says 2023, so **the deck contradicts itself.** | `Saunders et al. (2023)` |
| **A2** | **8** | `~150 records screened by title, ~60 read closely` — the thesis says **~100** and **~40**. Overstating your own screening effort in front of an examiner holding the chapter is the worst possible place to be wrong. | `~100 screened by title, ~40 read closely` |
| **A3** | **20 vs 23** | Peak fit memory is **34 MB** on slide 20 and **35 MB** on slide 23. The measurement is **34.5 MB**. | Use **34.5 MB** in both |

---

# The fixes, by slide

## Slide 02 — Agenda

### The defect

Six items; the deck has **seven** sections and ends on `Let's discuss!` (slide 27).
The agenda omits the discussion slide — which is the deck's entire strategy for
handling questions with the reserve wall behind it.

### Action

ADD a seventh item: **DISCUSSION**.

### Note

Slides 39 and 40 are older agenda variants in `Backup` reading
`DISCUSSION & LIMITATIONS` / `CONCLUSION` — a different six-item split. They are
backup, so they do no harm, but if either is ever shown it contradicts slide 2.

---

## Slide 08 — Review approach

### 8a — The screening numbers (A2 above)

**On screen now:**
> Search terms derived per theme from the research questions → **~150 records screened by title, ~60 read closely**

**Replace with:**
> Search terms derived per theme from the research questions → **~100 records screened by title, ~40 read closely**; under-covered themes sent back for further rounds

**Grounding:** Ch2 preamble — *"an initial set of approximately one hundred records
was screened by title, of which around forty were retained and assessed more
closely by abstract, introduction, and conclusion."*

---

### 8b — "61 sources cited" — Enrico's comment, resolved

Enrico's comment *"not sure of the numbers"* anchors here. **He was right to ask,
and the number is slightly off.**

- **62** entries in the thesis reference list, verified by counting entries carrying
  a year. (61 match a plain `(YYYY)`; the 62nd is Klee & Xia, dated `(2025, July 30)`.)
- **42** is what Ch2 says *its own corpus* is: *"the resulting corpus of forty-two
  cited sources, of which 14 are flagged as preprints."*
- **61** is neither.

**Replace with:**
> **Peer-reviewed prioritised.** Preprints only where they are the closest available precedent, flagged throughout → **42 sources in this chapter, 62 across the thesis**

That answers the comment and pre-empts "which number is that?" — the two counts
measure different things, and saying both is stronger than picking one.

⚠ **Two sources cited in Ch2 §2.5 are missing from the reference list** —
`Atıl et al. (2025)` and `Schwartz et al. (2020)`. That is a thesis defect, not a
deck defect, and it is now unfixable. **Do not raise it.** If asked, it is an
oversight in compiling the list, and the sources are real.

---

### 8c — The speaker note's section mapping is wrong

**Current note:**
> "Five strands on the slide, eight sections in the chapter: 2.1 and 2.2 are one strand here… 2.7 is the gap itself, not a strand, and 2.8 is the methodological paradigm. So the slide is sections 2.1 through 2.6, with the first two merged."

Chapter 2 has **ten** numbered sections, and 2.8 is *Thesis Contributions*:

| | |
|---|---|
| 2.1 | Forecasting as Predictive Substrate in FMCG |
| 2.2 | Lightweight ML under Computational and Deployment Constraints |
| 2.3 | From Descriptive BI to Forecast-Informed Decision-Support |
| 2.4 | LLM Agents and Tool-Mediated Reasoning |
| 2.5 | Reliability, Traceability, Uncertainty, and Evaluation |
| 2.6 | Production-Oriented Agentic Systems and Integration Readiness |
| 2.7 | **Research Gap** |
| 2.8 | **Thesis Contributions** |
| 2.9 | **Design Science Research** ← the paradigm |
| 2.10 | Chapter Summary |

**Replace the note with:**
> "Five strands on the slide, ten sections in the chapter. Six of those sections are the literature itself — 2.1 through 2.6 — and the slide merges the first two, because forecasting and the constraint it runs under are one argument here. The rest are not strands: 2.7 is the gap, 2.8 our contributions, 2.9 the Design Science paradigm, 2.10 the transition."

⚠ **The thesis has the same slip:** §2.10 says *"Section 2.8 frames the response as
Design Science Research"* when it is 2.9. If an examiner catches it, it is a
cross-reference error, and the correct section is 2.9.

---

### 8d — A trap sitting directly under this slide

Ch3 §3.2 calls Chapter 2 a **"systematic literature review"**. Ch2 says it is
*"a narrative, integrative review **rather than** a systematic review."* **The
thesis contradicts itself, and this slide's headline claim is the one under
attack.**

**Prepared answer — do not volunteer:**
> "Chapter 2 states the method: a narrative, integrative review, chosen because the
> contribution sits at the intersection of several literatures rather than in one
> bounded effectiveness question. The word 'systematic' in Chapter 3 is loose usage
> for 'done systematically' — the protocol in Chapter 2 is the operative statement."

---

## Slide 09 — Five strands

### 9a — Typo

`Does not Adress` → **`Does not Address`** *(column header — highly visible)*

---

### 9b — Row 4, drop "at scale"

**Current:** `feasibility demonstrated at scale`

The closest published exemplar in §2.6 is a **single beverage plant, one process
site**. "At scale" says the opposite of what the source supports, and it weakens
your own gap claim — if production agentic systems were proven at scale, the gap
is smaller.

**Replace with:** `feasibility demonstrated in production`

---

### 9c — Row 5, the gap cell is unsourced

**Current:** `benchmark compute; nothing on serving the forecast`

§2.7 names **four** strands and retail demand forecasting is not among them.
Neither phrase appears in Ch2. The nearest support is §2.2, where computational
efficiency is treated as a *"secondary design consideration"* in forecasting
research.

**Replace with:** `treats compute as secondary; nothing on serving the forecast to a decision-maker`

The second half is defensible — M5 is a forecasting-accuracy competition and says
nothing about delivery. The first half now matches §2.2.

---

### 9d — Font inconsistency

16 runs on this slide are **`-apple-system`** against 197 `Inter` across the deck.
It is the only slide affected — a paste from a browser or Mac source. Select the
table, set **Inter**.

---

## Slide 10 — The research question

### The defect

The slide is in quotation marks and reads as verbatim. It is not.

| | |
|---|---|
| **Slide** | "How can agentic decision-support systems without forecasting be extended with lightweight models, under real deployment and cost constraints?" |
| **Canonical** | "How can **production-oriented** agentic decision-support systems without **native predictive capabilities** be extended with lightweight **forecasting** models **to support reliable, forecast-informed, and cost-justified decision-making** under **computational and deployment** constraints?" |

Five departures. Three matter:

1. **"production-oriented" is gone** — this is the framing that makes the thesis a
   thesis rather than a project. It is what rules out the greenfield architecture
   the literature assumes.
2. **"to support reliable, forecast-informed and cost-justified decision-making"**
   is gone — the entire purpose clause, and the one that makes SRQ4's cost finding
   a *fulfilment* of the question rather than a consolation.
3. **"lightweight models"** drops *forecasting*.

**An examiner with the thesis open will compare these.** A shortened RQ in quotes
is the easiest possible thing to challenge.

### Action — pick one

**Option A (recommended) — restore it in full.** It is one slide with one sentence
on it; there is room.

> „How can ***production-oriented agentic decision-support*** *systems without*
> ***native predictive capability*** *be extended with* ***lightweight forecasting
> models*** *to support* ***reliable, forecast-informed and cost-justified***
> *decision-making under* ***computational and deployment constraints****?"*

**Option B** — keep the short form but **drop the quotation marks** and title it
*The question, in short*. Then it is a summary, not a misquotation.

⚠ Ch1 §1.3's RQ did not export to markdown — it is a text box or image in the
`.docx`. **Check the wording in Word directly before finalising**, since Ch1 is
where an examiner will look first.

---

## Slide 15 — Central academic grounding

### 15a — Saunders year (A1 above)

`Saunders et al. (2021)` → **`Saunders et al. (2023)`**

### 15b — Title typo

`METHDOLOGY` → **`METHODOLOGY`** — also on **slide 16**. It is in the title bar of
both, at 32pt.

### 15c — "MdAPE" is not a term the thesis uses

The thesis writes **WMAPE** (capitalised), **median APE**, and **MASE**. `MdAPE`
appears nowhere, and `wMAPE` is not the thesis's casing either.

**Replace:** `wMAPE primary, MdAPE and MASE alongside`
**With:** `WMAPE primary, median APE and MASE alongside`

### 15d — The three cycles are Hevner (2007), not Hevner et al. (2004)

The bullet sits under a heading reading `Hevner et al. (2004) & Peffers et al.
(2007)`, and the cycles bullet follows a bullet explicitly labelled *Hevner et al.
(2004)*. Ch3 §3.2 attributes the three cycles to **Hevner (2007)** — a different,
single-author paper.

**Replace:** `**Three cycles:** relevance (Manifold AI), design (Chapters 5–8), rigor (Chapter 2)`
**With:** `**Three cycles** *(Hevner, 2007)*: relevance (Manifold AI), design (Chapters 5–8), rigor (Chapter 2)`

Everything else on this slide — Hyndman & Athanasopoulos (2021, 3rd ed.), the six
Peffers activities, the exponential-smoothing limitation, out-of-sample evaluation,
benchmarks-as-floor — is **confirmed verbatim against Ch3 and Ch5.**

### 15e — Density

This slide carries **16 bullets across three columns**, most of them full sentences
with bold *and* underline. It is the densest slide in the deck and it sits in a
1:45 section. Consider cutting to **two bullets per column** and moving the rest to
the notes — the detail is what the notes are for.

---

## Slide 20 — Combined overview

**`34 MB` → `34.5 MB`** in the speaker note (A3 above).

The rest of the note is the thesis's own figure caption and is accurate.

⚠ **Know the other memory number.** Ch9 §9.2.2 reports the **realised end-to-end
peak as ~231 MB, under 6% of budget**. 34.5 MB is *XGBoost's peak fit memory*;
231 MB is *the whole pipeline running*. These are different measurements and an
examiner may quote the one you are not holding.

---

## Slide 21 — Performance overview

**Every cell is confirmed** against
`08_experimental_evaluation/tables/22_scenario_comparison.csv`. Cost for A is
`$0.3798`, correctly shown as `$0.38`.

### 21a — Align the ratios with slide 23 and the thesis

**Current note:** `B → C: 51× cheaper · 21× faster · zero variance — and worse on the median.`

The arithmetic is right (51.3× and 20.6×), but:

- **The thesis never says 51 or 21.** It says *"roughly fifty"* and *"roughly
  twenty"* — in Ch8, Ch9, Ch10 and the abstract.
- **20.6 rounds to 20, not 21.**
- **Slide 23 already says `~50×` and `~20×`** — the deck disagrees with itself.
- The cost figures are **token estimates**, which Ch8 flags as upper bounds (the
  $25.20 estimate overshot the billed $18.46 by ~29%).

**Replace with:**
> B → C: **~50× cheaper · ~20× faster · zero variance** — and worse on the median.

### 21b — Formatting

The bold in this table is close to meaningless — **26 of 28 data cells are bold**,
including every value in the A column. Bold should mark the winner per row. As it
stands `Mean APE` and `Cost per answer` bold the *loser*.

**Bold only:** B's median APE (2.9%), C's mean APE (13.1%), C's variation (0.0%),
C's identical-on-repeat (100%), C's cost ($0.0091), C's latency (6.0 s), and both
B/C usable answers (9/9). Everything else plain.

### 21c — Add a note

This slide has one line of notes and is the **most important table in the deck**.
Bullets to add:

> - Read the first increment first: **A → B is data access alone**, and it moves the median from 502% to 2.9%. That is worth more than anything above it on the ladder.
> - **Our step does not go the way we expected.** Worse on the median, better on the mean — the code agent is better most of the time and occasionally much worse.
> - What C buys: **~50× cost, ~20× speed, and an identical answer every time.** Zero variance, not low variance — the model is fitted once and loaded, so a repeat is a repeated read of the same parameters.
> - ⚠ **If they read the appendix:** scenario D (code, production orchestrator) is the most accurate rung at **0.9% median** — better than B. That is an orchestrator effect on the *code* path, not a point for our artefact. Say so plainly.

---

## Slide 23 — Findings

**All four rows confirmed**, several near-verbatim from Ch10. Two adjustments:

### 23a — `35 MB` → `34.5 MB` (A3)

### 23b — "across the whole evaluation" is exposed

**Current:** *"Reliability holds by construction — every reported figure matched the tool payload, across the whole evaluation"*

Ch10 says exactly this, so the slide is faithful. But `interval_communication.md`
shows **"Range matches the tool output" = 0 of 9** for scenarios A, B, D, F and G,
and 9 of 9 only for C and E. That row measures the *interval*, and scenarios
without tool access cannot satisfy it by construction — but an examiner reading
"the whole evaluation" beside five zeros will ask.

**Tighten to:** *"every reported figure matched the tool payload **in every run where the tool was called**"*

Ch7 states exactly that scope: *"in every run where the interface returned a
forecast, the figure the agent reported matched it exactly."*

### 23c — Expect "Prophet isn't parameter-free"

The SRQ1 qualification says two categories are *"beaten outright by parameter-free
benchmarks."* Ch10 uses that phrasing, so the slide is faithful to the thesis — but
**Prophet has parameters.** The genuinely parameter-free methods are naive,
seasonal naive, drift and mean.

**Prepared answer:**
> "Seasonal naive on RTD is parameter-free; Prophet on water is not, and the
> phrasing compresses two different cases. Prophet wins there because danskvand is
> the smallest panel — twenty-nine series, 174 test rows — where a method that
> imposes a trend and an annual cycle has least to get wrong and a high-capacity
> model has least to learn from. Chapter 5 reports it that way."

### 23d — This slide has no notes

It is the **centrepiece of Section 05**. Suggested bullets:

> - Four rows, one per SRQ, and every row has a qualification we put there ourselves.
> - **SRQ1:** the substrate works, and we still will not name a winner — a five-seed sweep changes the selected model in **all four** categories.
> - **SRQ2:** reliability holds by construction. The interval does not — 8 to 34 times the forecast. It is an honest account of uncertainty rather than a useful one, and we say which of the two carries the reliability claim: the measured track record.
> - **SRQ3:** assessed, not deployed. Three of seven scenarios ran inside the production platform, so readiness is derived from what an integration actually required — not from what we guessed it would need.
> - **SRQ4:** no scenario leads on every axis. **The contribution is qualified, and the qualification is the point.**

---

## Slide 25 — Limitations

### 25a — Title casing

`limitations` → **`LIMITATIONS & FUTURE WORK`** — every other content slide uses
`KEYWORD | Title`; this one is lowercase and bare. `Future work` mid-slide is also
lowercase where its counterpart is not.

### 25b — Ten bold bullets, no notes

Ten items, all bold, all long noun phrases, at ~1:45 for the whole section. You
cannot speak to ten. **Pick three limitations and three future-work items** for the
slide and keep the rest as reserve.

Recommended three limitations — the ones an examiner will find anyway:

- **Sample size and variation within scenarios** (9 runs, 3 repeats)
- **Forecasting practice inside the substrate** — no exponential smoothing, no
  seasonal ARIMA term
- **Interval width** — truthful, not usable

⚠ **This is the highest-value defensive slide in the deck and it has no notes.**
See below.

---

# The structural finding

## Speaker notes are figure captions, not speech

**15 of 40 slides have notes. 13 of those 15 are the thesis's own figure caption
pasted in, beginning "Original Figure Description:".** Only slides **8** and **21**
carry notes in a speaking voice — and 21's is one line.

The distribution is upside down:

| | Notes |
|---|---|
| Slides 9, 15, 23, 25 — **the four densest presented slides** | **none** |
| Appendix slides 29, 30, 32 — **shown only if asked** | 81, 86, 89 words |

Alt text already records each figure's provenance and source path, so the caption in
the notes field is **duplicated** — and it has cost you the notes field on every
figure slide.

**Recommendation:** keep captions in alt text where they already are. Use the notes
field for what you will say. The four slides above are where an unscripted sentence
is most expensive, and slide 15 (16 bullets) is where it is most likely.

## Three appendix slides have empty captions

Slides **33, 34, 35** carry `Original Description of Figure: - None`. If those
figures are shown under questioning, there is nothing to say from them. They are the
resource profile, the model ladder and the forecast overlay — **three of the most
likely things to be asked about.**

## The reserve wall is thinner than planned

The plan specified **20 reserve slides, each titled as the question it answers** so
it is findable under pressure. The deck has **8**, titled by artefact name
(`Model Selection`, `Resource Profile`).

All 20 planned artefacts **exist on disk** — verified. The gaps that matter most:

| Missing | Why it matters |
|---|---|
| `19_statistical_baselines.svg` | "which baselines beat you?" — slide 23 *invites* this question |
| `20_seed_stability_p1.svg` | "why won't you name a winner?" — same |
| `06_acf_pacf_plots.svg` | the **lag-12 evidence** |
| `22_scenario_comparison.svg` | the full seven-scenario ladder, incl. scenario D at 0.9% |
| `24_interval_communication.svg` | the 8–34× interval |

Retitling the existing 8 as questions costs nothing and makes them findable.

## Slide 06.x was not built

The planned *"What we applied, and where the chain broke"* slide (Variant T) is
absent. **That is a legitimate choice** — Ch9 §9.4 already states the lag-13
defect, so this is not concealment, and the plan built both variants deliberately.
Confirm it is a decision rather than an omission.

⚠ If it stays out, the lag-12/13 answer must be **fluent from `qa-drill.md`**. And
per the plan: **do not present this as "our code documents the bug"**, and **do not
claim it was noticed before submission.**

---

# Everything else that is wrong, cheaply

| Slide | Issue | Fix |
|---|---|---|
| 9 | `Does not Adress` | `Does not Address` |
| 11 | alt text `The Reasearch Gap` | `Research` |
| 15, 16 | `METHDOLOGY` in the title bar | `METHODOLOGY` |
| 37 | `UNIFCATED RESOURCES CONSTRANIS` | `UNDER RESOURCE CONSTRAINTS` — backup title slide; fix or delete |
| 1 | CBS logo has no alt text | add, or accept as chrome |
| 37 | `Table 15` has no alt text | backup slide |
| 29, 30, 31, 32 | title reads `MODELLING \|Data Pipeline` | missing space after the pipe |
| 18, 19, 20, 29, 30 | notes contain run-together words (`Countsshown`, `ismeasured`, `withtheir`, `drawson`) | line-break artefacts from copying the captions; invisible on screen, fix if the notes are reused |
| 4 | `Combining traditional ML Forecasting with  LLMs` | double space |
| 5 | alt text on Group 1 contains `enahnces` and `promotheus` | typos in provenance text, not on screen |

---

# What is right, and worth knowing is right

So this pass is not read as a list of problems:

- **Every number on slide 21** — all 21 cells — matches the source CSV exactly.
- **Every finding on slide 23** traces to Ch9 or Ch10, several verbatim.
- **8–34× interval width**, **three of seven scenarios**, **502% → 2.9%**,
  **4 GB ceiling**, **zero variance**: all confirmed.
- **Slide 15's methodology grounding** is accurate apart from the Saunders year and
  the Hevner attribution — the Peffers activities, the three cycles' content, the
  metric hierarchy and the exponential-smoothing limitation are all correct.
- **Slide 9's retail strand** is well-grounded in M5 (LightGBM top-50,
  cross-learning).
- **Alt text is 39 of 41**, and it names source paths. That is better provenance
  than most decks carry and it is what made this review possible.

---

# One thing to prepare that is not on any slide

Ch9 §9.3 says the code-writing scenarios **"did not improvise: every one of them
fitted exponential smoothing and a seasonal ARIMA, most added a decomposition, and
twelve of fourteen combined their candidate models explicitly"** — and that these
are *"precisely two techniques the thesis pipeline lacks."*

**So a material part of the code arm's median win is plausibly attributable to
established practice your substrate does not implement, rather than to code
execution as such.** The thesis states this. It is the sharpest available question
about SRQ4, and the honest answer is already written:

> "That is a limitation of this comparison and a concrete, cheap direction for the
> next cycle."

Better to say it before it is asked — it converts the finding from a weakness into a
stated boundary with work behind it.
