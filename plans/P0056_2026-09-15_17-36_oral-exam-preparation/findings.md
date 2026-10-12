---
name: p0056-findings
description: STATE - What the submitted thesis actually says, which plan-folder claims it supersedes, the verified numbers any slide may quote, and the measured shape of the top-grade reference deck (F11), and the post-submission reference-list correction (F12).
pid: P0056
created: 2026_09_15-17_36
updated: 2026_09_20-14_15
---

# P0056 — Findings

## F1 — Currency, stated so a later reader knows what this was verified against

- Repo at **`83689d3`**, branch `thesis/svg-table-styling`, fetch clean, 6 ahead of `origin/main`, nothing incoming.
- Snapshot **`2026-09-15_17-43_oral-exam-prep`**; source `.docx` modified 15:40:33, SHA `0b8c197b…`, **47,299 words**, 17 level-1 chapters, 30 tables, **1** live comment.
- Zotero re-pulled the same session: **88 items**.
- **Step 3 of `/re-snap` (diff against previous snapshot) deliberately skipped.** It exists to show which proposed fixes an author applied; the thesis is submitted, so there is no pending pass. Previous snapshot was 110 minutes earlier.

### ⚠ Superseded 2026-09-20 — re-read this before trusting anything above

The reasoning for skipping step 3 was **wrong, and it caused F12.** "The thesis
is submitted, so the document cannot move" is an assumption, and the document
moved: the bibliography field was refreshed after submission, adding 27
reference entries. Any audit against the 09-15 snapshot is stale.

**Current currency (2026-09-20 14:09):**

| | |
|---|---|
| Repo | `b9dbfd4`, branch `main`, fetch clean, **0 ahead / 0 behind** `origin/main` |
| Snapshot | `2026-09-20_14-09_defence-deck-citation-audit` — **47,139 words**, 17 chapters, 142 leaf sections, **0 comments** |
| Zotero | re-pulled same session, **88 items**; `bibtex.bib` + `citations.json` written, then the known cosmetic crash (F10) |
| Reference list | **61 entries** (was 34) |

**Verify against the 09-20 snapshot, not the 09-15 one.**

## F2 — The submitted document's shape

| Ch | Subject | Words |
|---|---|---:|
| 1 | Introduction | 3,108 |
| 2 | Literature Review | 6,307 |
| 3 | Methodology | 4,110 |
| 4 | Data Assessment | 5,665 |
| 5 | Model Benchmark & Selection | 8,205 |
| 6 | Predictive-Extension Architecture | 3,317 |
| 7 | The Structured Tool Interface | 5,596 |
| 8 | Experimental Evaluation | **2,318** |
| 9 | Discussion | 3,707 |
| 10 | Conclusion | 1,663 |

**Ch8 carries the thesis contribution in the fewest words of any substantive
chapter.** That is where an examiner with limited time will push, because it is
where the claim lives and where there is least text to defend it.

## F3 — Verified headline numbers, read from the artefact not the prose

Source: `05_thesis_results/08_experimental_evaluation/tables/22_scenario_comparison.csv`
(9 runs per scenario, 63 total).

| Measure | A plain | B data+code | C model | D prod+code | E prod+model | F both | G prod+both |
|---|---:|---:|---:|---:|---:|---:|---:|
| Usable answers | **6**/9 | 9 | 9 | 9 | 9 | 9 | 9 |
| Median APE % | 502.2 | 2.9 | 14.6 | **0.9** | 14.6 | 7.3 | 1.8 |
| Mean APE % | 662.1 | 27.9 | **13.1** | 25.0 | 13.1 | 18.3 | 15.6 |
| CV across repeats % | 26.7 | 4.1 | **0.0** | 8.1 | **0.0** | 1.7 | 3.3 |
| Replicability % | 0 | 0 | **100** | 0 | **100** | 33 | 33 |
| Cost/answer USD | 0.3798 | 0.4667 | **0.0091** | 0.7664 | 0.1994 | 0.4253 | 0.5536 |
| Response time s | 69.5 | 123.8 | **6.0** | 111.3 | 31.7 | 103.9 | 84.4 |

**Derived, computed not transcribed:** C vs B = **51.3×** cheaper
(0.4667/0.0091), **20.6×** faster (123.8/6.0). The thesis says "roughly fifty"
and "roughly twenty" — consistent.

⚠ **D is the most accurate rung on the median (0.9%), better than B (2.9%).**
The abstract and Ch10 do not foreground this. An examiner reading the appendix
table can. Be ready: the production orchestrator's *code* arm beat the
general-purpose one, which is an orchestrator effect on the code path, not a
point for the artefact. Drill this.

## F4 — Total evaluation cost, and which figure is which

Ch8 §8.3.1: **$19.60** actual (account-balance delta, the only non-estimated
figure); **$25.20** token-based estimate, a 29% overshoot; $18.46 from the
billing endpoint for an incomplete window. ≈**31 cents per run**.

Quote $19.60 as the cost. Per-scenario costs in the table above are **token
estimates and therefore upper bounds** — say so if pressed.

## F5 — ⚠ CORRECTION to P0055 F4: two claims it makes are superseded by the submitted text

P0055's `findings.md` F4 (written 2026-09-12) says Ch9 §9.1.4 states the
code-as-action baseline *"was not executed"*, and that Ch8 is a 1,384-word
skeleton with `[N] SKUs × 28 retailers × [T] weeks` placeholders and a weekly
grain. **Both were fixed before submission. Do not repeat either.**

- Ch9 §9.1.4 now reads *"executed as a ladder of seven scenarios over sixty-three funded runs"*.
- Ch8 is 2,318 words, monthly grain, no placeholders found.

**And the consequential one:** Ch9 §9.4 **already states the lag-13 defect in
full**, as *"a gap of provenance between the analytical and engineering layers
rather than of method… the same class of defect the structured interface is
designed to prevent downstream of the model."*

So the lag-12/13 issue is **an owned limitation in the submitted thesis**, not a
post-submission discovery. This reframes Phase 2 entirely: the "transparent"
variant foregrounds a limitation the thesis already makes, and the "silent"
variant merely omits a slide about text the examiner can read. **Neither variant
conceals anything.** Brian must be told this before choosing.

Lesson, and it is the one `plan-verification-discipline.md` already states: a
plan folder records intent at a moment. The submitted `.docx` is ground truth.

## F6 — Gaps in the inherited defence file, for Phase 4

`anticipated-assessor-questions.md` is strong (~25 questions, measured answers,
explicit concessions). Its **U1–U3 are now answerable** — they were blocked on
"the funded run", which has since run (63 runs). Those three rows are stale and
read as open questions when they are closed.

Questions it does **not** yet cover, all askable from the submitted text:

1. **Why is D more accurate than B?** (F3) — an orchestrator effect on the code path, unaddressed.
2. **Why does Ch8 devote 2,318 words to the thesis's own contribution?** (F2)
3. **Two categories are beaten by a parameter-free seasonal naive / Prophet** (Ch9 §9.1.1, Ch10). The thesis reports this well; the defence needs a crisp 20-second version.
4. **The thesis cites ~2 figures against 87 generated SVGs and ~317 result files.** Why is so little shown?
5. **DSR with one cycle** — design principles are *derived, not validated*. Ch10 §10.4 concedes it; expect a methodology examiner to press.
6. **"Bounded tool-using agent, not a multi-agent system"** (Ch9 §9.2.1, citing Sapkota et al.) — a framing correction the thesis makes about itself. Invites "so what is agentic about it?"

## F9 — ⚠ The submitted thesis reports two different peak-memory figures for the same models

Found 2026-09-15 while verifying SRQ1 numbers for the deck. **Both are in the
submitted document, forty pages apart.**

| Model | Ch9 §9.1.1 | Ch6 Table 20 | `15_substrate_resource_profile.md` |
|---|---:|---:|---:|
| XGBoost | **34.5** MB | **31.9** MB | 34.5 MB |
| LightGBM | **17.9** MB | **14.9** MB | 17.9 MB |
| Ridge | — | 1.6 MB | 1.5 MB |

Ch7 §7.6 adds a third framing: *"the fitting path peaks between 1.6 and 31.9
megabytes"* — i.e. it follows Ch6's pair, not Ch9's.

The artefact on disk agrees with **Ch9** (34.5 / 17.9). Ch6's Table 20 is dated
2026-09-11 and carries the Ridge figure 1.6 against the artefact's 1.5, so it
appears to be a separate, slightly earlier measurement run that was never
reconciled.

**Neither figure changes any conclusion** — the argument is a hundredfold margin
against a 4096 MB ceiling, and 34.5 vs 31.9 is 0.84% vs 0.78% of budget. But if
an examiner puts the two tables side by side, the answer must be ready and must
not be improvised. **Drill it (Phase 4), do not put it on a slide.**

The honest answer: two profiling runs at different dates, the later one
regenerated after the 18-feature retraining; the results artefact carries the
current figures; the discrepancy is within run-to-run variation of a memory
measurement and is immaterial against a ceiling three orders of magnitude above
it. Do **not** claim the difference is meaningful, and do not claim it was noticed
before submission.

## F10 — Zotero export integrity confirmed after the crash

`bibtex.bib` (157,324 B) and `citations.json` (167,113 B) both written 17:44.
**88 entries; exactly 1 has no `year`** — which is precisely what crashed the
sample-print loop. Exports are complete and current. The defect is one line
(`item["year"]` → `item.get("year")`) and is not this plan's work.

⚠ Carried forward from `deferred-structural-decisions.md` S16 and still open at
submission: the BibTeX exporter writes `author = {Hyndman Rob J., Athanasopoulos
George}` where BibTeX needs ` and ` as separator. **Harmless if Word's own
citation manager built the reference list; a Trust-tier defect if the `.bib`
did.** If an examiner asks how the bibliography was produced, know the answer.

## F7 — Reusable assets found (do not rebuild)

| Asset | Path |
|---|---|
| ~25 examiner Q&A with evidence | `06_thesis_writing/writing-notes/anticipated-assessor-questions.md` |
| 22 line-numbered forecasting defects + textbook citations | `plans/P0055_*/findings.md` |
| Scenario ladder figure | `05_thesis_results/07_decision_synthesis/figures/ch7_scenarios_v2.svg` |
| Layered architecture | `05_thesis_results/06_architecture/figures/ch6_layered_architecture_v2.svg` |
| Tool interface | `05_thesis_results/06_architecture/figures/ch6_tool_interface_v1.svg` |
| RQ tree | `05_thesis_results/01_introduction/figures/ch1_research_questions_tree_v2.svg` |
| Scenario comparison as styled SVG | `05_thesis_results/08_experimental_evaluation/tables/22_scenario_comparison.svg` |
| 87 SVGs total | `05_thesis_results/**/figures|tables/*.svg` |

**The deck reuses these.** Making new charts would both waste effort and risk
numbers that disagree with the submitted document.

## F11 — The reference deck, measured: 13 presented slides against 22 held in reserve

Brian supplied a printed handout with speaker notes from **Max's group, who took
the top grade**. Topic is unrelated to ours — participatory governance, content
integrity and user trust on decentralised social media (Mastodon and Bluesky),
a mixed-methods interpretivist study with 10 interviews and a 148-respondent
survey. **It is evidence about deck shape, not about content.**

Read 2026-09-19 from
`~/OneDrive/.../Documents/Max - Oral Defense Presentation_with_notes_OCR.pdf`,
35 pages, OCR'd. Text extracted with `pypdf`; OCR quality is poor on table
interiors but section structure and speaker notes are legible.

### The shape

| Pages | What |
|---|---|
| 1 | Title |
| 2 | Agenda — six sections, no numbers on screen |
| 3–4 | Motivation of the Study — anomaly, phenomenon, research question |
| 5 | Literature Review & Analytical Framework — concept matrix, propositions P1a–P3 |
| 6–7 | Methodology & Data Collection |
| 8–9 | Our Most Relevant Findings (1/2) and (2/2) |
| 10 | Revisited Analytical Framework |
| 11–12 | Limitations, Implications and Reflection |
| **13** | **"Let's discuss!"** — the wall begins |
| 14–35 | **22 reserve slides**, never presented |

**Presented: 13. Reserve: 22.** The reserve set is ~1.7× the deck.

### What is in their reserve wall

Participant overview, survey respondent overview, data-analysis workflow,
code-to-theme mapping, ethics, research quality & reflexivity, architectural
comparison of the two platforms, construct definitions, proposition-strength
assessment, and **nine further analytical diagrams** — each one answering a
single question that an examiner might ask and that a diagram answers faster
than a sentence.

### The three transferable moves

1. **The presented slides are sparse.** Findings get two slides for a whole
   mixed-methods study. Density is deliberately pushed behind the wall.
2. **Reserve slides are titled as answers, not as topics.** *"The architectural
   differences between Mastodon and Bluesky"*, *"How the two platforms produce
   user agency over the feed"* — the title is findable under pressure.
3. **The methodology slide states philosophy before instruments.** Interpretivist
   → abductive → exploratory → mixed-methods → sample. The *why* precedes the
   *what*, which is exactly the move our DSR slide needs.

### Where the analogy stops — do not copy these

- **They revisit an analytical framework; we do not have one.** Our equivalent
  slot is the five design principles (DSR method contribution). Not the same
  object, and calling ours a "framework" would invite a methodology examiner to
  ask which framework literature it extends.
- **Their findings are propositions with support levels.** Ours are measured
  quantities with a negative result inside them. Our findings slides must carry
  numbers; theirs carry strength assessments.
- **Their limitations are sampling and scope.** Ours include a *defect* (lag-13),
  which is a different kind of admission and is already in our submitted Ch9 §9.4
  (F5). Do not soften it into a "limitation" — it is a corrected flaw, which CBS
  explicitly invites us to surface.

### One caution on inference

We know this deck accompanied a top grade. **We do not know the deck caused it**,
and no part of the defence rubric rewards deck structure directly — the
presentation is ~20% of the slot. Treat the reserve wall as a good idea that is
demonstrably survivable at the top of the grade range, not as a formula.

## F12 — ⚠ The reference list was completed AFTER submission. My 2026-09-19 citation audit was measuring a stale document.

**Correcting myself.** On 2026-09-19 I audited citations against the
`2026-09-15_17-43_oral-exam-prep` snapshot, found **35** reference-list entries
against ~68 in-text citations, and told Brian his slide claim of "61 sources
cited" did not match the document. **The slide was right. My audit was stale.**

`/re-snap` on 2026-09-20 (`2026-09-20_14-09_defence-deck-citation-audit`) shows
the `.docx` was edited after submission:

| | 09-15 snapshot | 09-20 snapshot |
|---|---:|---:|
| Reference-list entries | 34 | **61** |
| Reference list, words | 934 | 1,642 (**+708**) |
| Table of contents, words | 829 | 109 (−720) |
| Live comments | 1 | **0** |
| Total words | 47,749 | 47,139 |

**The bibliography field had not been refreshed** when the submission snapshot
was taken; it has been since.

> ⚠ **Corrected by F15 (2026-09-20).** The "61" in the table above is one short.
> It was produced by counting entries matching a bare `(YYYY)`, which misses
> **Klee & Xia**, dated `(2025, July 30)`. The reference list holds **62**.
> So the headline of this finding — *"the slide was right"* — is itself wrong:
> the slide's 61 matches neither the reference list (62) nor Ch2's own stated
> corpus (42). **Enrico's comment on slide 8 was correct to query it.**
> The lesson about stale snapshots below still stands and is unaffected.

### What the lesson actually is

`plan-verification-discipline.md` says the submitted `.docx` is ground truth —
and I applied that rule. The failure was subtler: **I treated a snapshot as the
document.** A snapshot is a dated mirror, and this one was five days old. The
`/re-snap` skill exists precisely for this and I did not run it before auditing.

This is the same class of error as F5, inverted. There, a plan folder was stale
against the document. Here, a *snapshot* was stale against the document. Both
resolve the same way: **re-snap before verifying anything, every time.**

### Residual, measured on the fresh snapshot

13 in-text citations still have no exact reference-list match, but **8 of those
are year variants where the source IS listed** — Ahrens 2024↔2025, Elmachtoub
2024↔2022, González-Potes 2024↔2026, Gu 2024↔2025, Ji 2025↔2024, Ye 2025↔2024,
Chen 2024↔2026, plus Liu/Li/Wang first-author ambiguities. Those are in-text
year typos or genuine companion works, not missing sources.

**Five have no entry under any year:** Cain (2017), Doane (2017), Klee (2025),
Önkal (2010), Atıl (2025), Schwartz (2020). Of these, **Klee & Xia is cited in
four chapters** and is in Zotero; Önkal appears in Ch7 and Ch9 and is in Zotero
as part of Goodwin, Önkal & Thomson (2010), so it is almost certainly a
same-work name-order variant rather than a missing reference. **Atıl and
Schwartz are in neither the list nor Zotero** — those two are the only genuine
unknowns, and both sit in Ch3.

Five entries are listed but never cited: Li (2024), Liu (2025), Nager (2026),
Olszak (2025), Wang (2025).

**None of this needs action.** The thesis is submitted and closed. It is
recorded so that (a) the slide's "61 sources cited" is confirmed correct and
defensible, and (b) if an examiner raises a specific citation, the answer is
known rather than improvised.

### Consequence for the deck

**Brian's literature-review slide needs no change.** "61 sources cited" matches
the reference list exactly. My 2026-09-19 recommendation to drop the number was
based on the stale count and is **withdrawn**.

## F13 — The PDF split left 8 stale files behind, and 6 of them had misleading names

Re-ran `split_thesis_pdf.py` on 2026-09-20 against the current PDF (**136
pages**, dated 2026-09-16). The previous split was against a **142-page**
version, so the PDF was regenerated post-submission too — consistent with F12.

**`split_thesis_pdf.py` writes but does not delete.** Eight PDFs from the old
run survived alongside the new ones:

| Stale file | Why it is dangerous |
|---|---|
| `Thesis-Ch05-5.5-Results.pdf` | current §5.5 is **Evaluation metrics**; Results is now **§5.6** |
| `Thesis-Ch05-5.2-Model_descriptions.pdf` | current §5.2 is **Modelling Pipeline** |
| `…5.3-Experimental_setup`, `…5.4-Evaluation_metrics`, `…5.6-Model_selection_decision`, `…5.7-Connection_to_SRQs` | same off-by-one |
| `Thesis-Ch00-AI_Use_Declaration.pdf` (×2) | heading no longer in the PDF outline |

**Cause:** Chapter 5 gained a section — *5.2 Modelling Pipeline* — so every
later section shifted up by one number. The old files therefore occupy
*filenames that still look current* while carrying the previous document's
content under the wrong number. Opening `5.5-Results.pdf` would have given the
old §5.5 labelled as Results.

All 8 were verified absent from both regenerated `00_INDEX.md` files before
deletion. Final state: **13 chapter PDFs, 73 section PDFs**, matching the
script's reported unit counts exactly, 133 of 136 pages covered (1–3 are title
and TOC front matter, excluded by design).

**This is the same defect `figure-generation-standards.md` already names** —
*"A generator must delete, not only write"* — which `export_appendix.py` solves
with `_clear_previous()` and `generate_architecture_diagrams.py` with
`_out_for()`. `split_thesis_pdf.py` has no equivalent. It would be a small fix
(delete `Thesis-*.pdf` in the output dir before writing), **but the thesis is
closed and this plan does not touch tooling.** Recorded so the next person to
re-run it knows to sweep first.

## F14 — Forecasting methodology: snapshot vs codebase, line by line

> **In plain English:** see **F16.0** — the same defect, explained without jargon,
> with a verdict on how much it matters. F16.1 also corrects this entry: at the
> primary three-month horizon the offset is three months, not one.

Verified 2026-09-20 against snapshot `2026-09-20_14-09` and the live code.
**Most of the methodology holds and is implemented as described.** One link
fails, and one adjacent item is weaker than it first appears.

### Implemented as the thesis describes ✅

| Claim | Code |
|---|---|
| 4-fold expanding-window CV, split on **periods not rows** | Ch5 §5.4.4; rationale cites Bergmeir 2018 / Cerqueira 2020 correctly — K-fold rejected *for this data*, not on principle |
| Rolling origin, each fold refits from scratch | §5.4.4, Tashman (2000) |
| Test split untouched by selection | §5.4.4 |
| Conformal calibration genuinely out-of-sample | `train_and_persist.py:273` — `m_cal` fitted on TRAIN, residuals taken on VAL. ⚠ **This corrects a P0055 note suggesting an in-sample residual gate** |
| Sequential fit/unload so peak memory is per-model | §5.4.3 |
| Seed fixed at 42, sensitivity *measured* not assumed | §5.4.3 → §5.6.10 |
| Optuna TPE, 100 trials, budget justified by measured plateau (0–83, median 54) | §5.4.5 |
| ACF/PACF run per brand per category | `step_2_eda_descriptive.py` s16 |

### Where the chain breaks ⚠

**The diagnostic was performed correctly and never reached the feature spec.**

| Layer | Says |
|---|---|
| ACF evidence, CSD | **lag 12 significant for 5 of 5** leading brands; lag 13 for 2 — and both of those show *every* lag 1–15, i.e. trend not seasonality |
| `engineer_features.py:33` | `DEFAULT_LAGS = (1, 2, 3, 4, 8, 13)` |
| Shipped `csd_feature_matrix_h1.parquet` | `lag_13`, `rolling_mean_13` |
| `srq1_baselines_stat.py:21` | seasonal naive reads `y(t+h-12)` ✅ |
| `srq1_residual_diagnostics.py:105` | `SEASONAL_PERIOD = 12` ✅ |

So **the codebase understands monthly seasonality everywhere except the feature
matrix.** This is not a conceptual error; it is a configuration that no analysis
wrote to. `step_2_eda_descriptive.py` says it outright: the ACF is *"reported
here, never persisted."*

⚠ **`step_3_derive_params.py:213`** records the provenance string **"the lag-12
term is retained"** beside `lags = (1,2,3,4,8,13)`. Justification and value
contradict each other in the same function.

**Do not put this in the deck as "our code documents the bug."** It is a
stronger claim than the thesis makes, invites *"what else disagrees with its own
comments?"*, and the honest reading is duller — the string was written when the
intent was lag 12 and never revised.

### What the submitted prose now says

**Ch5 §5.4.2 documents the defect's value as correct:** lags "at one, two,
three, four, eight and **thirteen** months… carry recent history and the
year-ago comparison." Thirteen months is not the year-ago comparison.

**Ch9 §9.4 states the defect in full**, and names the mechanism precisely — "a
gap of provenance between the analytical and engineering layers rather than of
method… the same class of defect the structured interface is designed to
prevent downstream of the model."

**The two chapters therefore disagree**, which is the realistic examiner entry
point: Ch5 asserts the feature is right, Ch9 explains why it is wrong. The
defence answer is that Ch9 supersedes Ch5 and the correction was made late.

### Adjacent items — prepared, not volunteered

| Gap | Real weight |
|---|---|
| **Non-seasonal ARIMA** `SARIMAX(order=(1,1,1))`, no `seasonal_order` | Genuine. Ch9 §9.4 already concedes the substrate "lacks exponential smoothing and a seasonal ARIMA term" |
| **MASE denominator** = one-step naive, where Hyndman & Koehler prescribe seasonal naive | **Much weaker than P0055 F-notes imply** — Ch5 §5.6.3 reports naive *and* seasonal-naive MASE side by side and surfaces the disagreement. Not a hidden error |
| **`rolling_mean_13`** | Same root cause as `lag_13`; not separately stated in the thesis |

### Consequence for the deck

Written up as optional slide **06.x** in `slide-plan.md` (Variant T only), as a
two-column *"what we applied / where the chain broke"* table. The framing is
that the methodology holds and one diagnostic did not reach one configuration
file — which is both true and the most defensible reading.

**Volunteer one defect, not four.**

## F8 — The one live Word comment

Thread **279**, Ch8 §8.3, tagged `APPENDIX`, opened by Brian 2026-09-15 10:33 on
*"The seven scenarios on sixty-three runs"*: "APPENDIX PASS: Re-genearte &
Replace". Unresolved at submission. Cosmetic/appendix-regeneration intent, not a
factual defect — but confirm with Brian whether Table 24 in the submitted
document is the regenerated one.

---

## F15 — Deck review pass 01: every number is right, five citation/count defects are not

**Verified 2026-09-20** against deck snapshot `2026-09-20_19-24_review_pass` (40
slides) and thesis snapshot `2026-09-20_14-09_defence-deck-citation-audit`.
Full pass: `06_thesis_writing/defence/slide-review/2026-09-20_deck-review-pass-01.md`.

**The evidence base is sound.** All 21 cells of slide 21 match
`08_experimental_evaluation/tables/22_scenario_comparison.csv` exactly. All four
rows of slide 23 trace to Ch9/Ch10, several verbatim. 8-34x interval, three of
seven scenarios, 502% to 2.9%, 4 GB ceiling, zero variance: all confirmed.

**What is wrong is citation hygiene, counts and two self-contradictions:**

| | Defect | Truth |
|---|---|---|
| Slide 15 | `Saunders et al. (2021)` | **2023** (9th ed.) — all 8 in-text uses; slide 8 already correct, so the deck contradicts itself |
| Slide 8 | `~150 screened, ~60 read closely` | Ch2: **~100** and **~40** |
| Slide 8 | `61 sources cited` | **62** in the reference list; **42** is Ch2's own corpus. 61 is neither |
| Slides 20 vs 23 | `34 MB` vs `35 MB` | **34.5 MB** (`15_substrate_resource_profile.csv`, XGBoost peak fit RSS) |
| Slide 15 | three cycles under `Hevner et al. (2004)` | **Hevner (2007)** per Ch3 §3.2 |
| Slide 15 | `MdAPE` | never used in the thesis; it writes `median APE`, `WMAPE`, `MASE` |
| Slide 21 vs 23 | `51x / 21x` vs `~50x / ~20x` | thesis says "roughly fifty/twenty" everywhere; 123.8/6.0 = **20.6**, so 21 rounds the wrong way |
| Slide 10 | RQ in quotation marks | **not verbatim** — drops "production-oriented", "native predictive capability" and the whole "reliable, forecast-informed, cost-justified" clause |
| Slide 9 | `feasibility demonstrated at scale` | §2.6's exemplar is a **single plant, one process site** |
| Slide 9 | gap cell `benchmark compute; nothing on serving` | **unsourced** — §2.7 names four strands, retail forecasting is not among them |

**Enrico's slide-8 comment is resolved: he was right.** 61 is not a number the
thesis supports. This supersedes F12's conclusion that 61 was correct — F12
counted the *reference list* and got 61 by a regex that missed Klee & Xia, whose
date is `(2025, July 30)` rather than a bare year. The list holds **62**.

**Structural finding — the speaker notes are inverted.** 15 of 40 slides carry
notes; **13 of those 15 are the thesis's own figure caption pasted in**, beginning
"Original Figure Description:". Only slides 8 and 21 have notes in a speaking
voice, and 21's is one line. Meanwhile the four densest *presented* slides — 9,
15, 23, 25 — have **none**, while appendix slides 29/30/32 carry 81/86/89 words.
Alt text already records each figure's provenance and source path, so the caption
in the notes field is duplicated and has cost the notes field on every figure
slide.

**Reserve wall is 8 slides against the planned 20**, titled by artefact rather
than by the question each answers. All 20 planned artefacts verified present on
disk. The five most costly absences: statistical baselines, seed stability, the
ACF/PACF lag-12 evidence, the full seven-scenario ladder, and interval
communication.

**Three thesis-side defects found in passing, all now unfixable** — record so they
are drilled, not raised:
- Ch2 §2.5 cites `Atıl et al. (2025)` and `Schwartz et al. (2020)`; **neither is
  in the reference list**.
- Ch2 §2.10 says "Section 2.8 frames the response as Design Science Research" —
  it is **2.9**.
- Ch3 §3.2 calls Ch2 a "systematic literature review", contradicting Ch2's own
  "narrative, integrative review **rather than** a systematic review". This one
  sits directly under slide 8's headline claim.

**The sharpest unasked question, already answered in the thesis.** Ch9 §9.3: the
code-writing scenarios "did not improvise: every one of them fitted exponential
smoothing and a seasonal ARIMA, most added a decomposition, and twelve of fourteen
combined their candidate models explicitly" — "precisely two techniques the thesis
pipeline lacks". So a material part of the code arm's median win is plausibly
attributable to established practice the substrate does not implement, not to code
execution as such. Say it before it is asked.

---

## F16 — EDA → modelling chain, audited end to end (2026-10-10, R-1010-03)

Extends F14. Verified against the code, the shipped CSD H=3 matrix, the step-2
console logs and snapshot `2026-10-10_16-42_deck-finalisation`.

### F16.0 In plain English (read this first)

*The precise version follows in F16.1–F16.5. This block is the same content,
without the jargon. Given to Brian as R-1012-01.*

**The big one — the model never looks at "same month last year".** To forecast
December, the best single clue is last December. The analysis found that yearly
pattern, but the model's inputs were set to 13 months back instead of 12, and
because we forecast three months ahead, the model actually sees sales from **15
months** before the target month. It never sees "last December". Ch9 calls this
off by one month; it's off by three.

**Why it isn't a disaster.** The model is still told *which month* it is
forecasting (a month input and a peak-month flag), so it knows December is
usually big. It just lacks the most precise clue.

| Mistake | Plain English | Size |
|---|---|---|
| No seasonal classical baseline | one comparison model ignores seasons; already admitted in Ch9 | small, disclosed |
| Seasonality checked on trending data | if sales keep growing, every month looks related to every other, so the chart "finds" patterns everywhere | small — affects reading one chart |
| Decomposition picks its method wrongly | it compares numbers on different scales and always picks the same option | tiny, chart not in the thesis |

**Done right:** the log transform (skewed sales), stationarity (trends), the
train/test split and the uncertainty intervals.

**How bad, honestly?**
- No result is *wrong* — every number measures the model as built.
- The conclusion doesn't change, and this is the key point: **the mistake weakens
  our own model.** Fixing it would most likely make it more accurate, which only
  strengthens the thesis. "Wins on cost, speed and reproducibility, not accuracy"
  is if anything conservative.
- The accuracy cost is **unknown** — never re-run. Don't guess a number.
- Verdict: a medium-sized technical flaw with a small effect on the claims.

### F16.1 The lag defect is larger at the primary horizon than the thesis states

`engineer_features.py` builds `lag_k = shift(k + H − 1)`; names keep their H=1
meaning. **H=3 is primary** (`_horizon.py: PRIMARY = 3`). Measured on
`csd_feature_matrix_h3.parquet`: `lag_1 == shift(3)`, **`lag_13 == shift(15)`**.
So at H=3 no lag reaches the year-ago month (that would be `lag_10`), and
"fixing" 13→12 would give shift(14), still wrong.

- Ch5 §5.4.2: lags "carry … the year-ago comparison" — false at both horizons.
- Ch9 §9.4: "offset by one month" — true at H=1 only; at H=3 the offset is three.
- The thesis never discloses that lag names are horizon-relative.

**Mitigation, measured:** `month`, `quarter`, `peak_month` are target-month
aligned (verified), so annual position still reaches the trees — but they carry
only ~2–5% of SHAP attribution (`96_holiday_shap_attribution.csv`).

**Plausible root cause (hypothesis, not established):** Ch4 §4.2.4 justifies 13 as
"the annual cycle on the Nielsen calendar". The panel is 46 periods over
Oct 2022–Jul 2026 = **12 per year** (a 4-4-5 calendar has 12 periods; 13-period
calendars are the 4-week variant).

**Defence wording:** "the lag set never reaches the same month last year" — true
at both horizons. Never "off by one".

### F16.2 ACF read on non-stationary levels

`s16_acf_pacf` computes ACF on log1p **levels**; the ADF table finds 13 of 20 CSD
brands need differencing. On a trending series every lag clears the band —
COCA COLA and PEPSI are significant at all lags 1–15. The step-2 table note
concedes the band "assumes a stationary series". Box–Jenkins practice is to
difference first. Ch4's own pooled, demeaned figure gives lag 13 = **−0.16**.
FAXE KONDI and FANTA show lags 3, 6, 9, 12, 15 — a **quarterly rhythm**,
consistent with the quarter-end peak months Ch4 §4.2.3 reports.

### F16.3 Decomposition model choice is not a test

`s10_decomposition` picks additive vs multiplicative by lower residual variance,
comparing squared units (CSD 7.67e+11) against a dimensionless ratio
(2.15e-03). Multiplicative wins in all four categories by construction. The
conclusion is probably still right (consistent with the log transform) but the
selection proves nothing. Not cited in the thesis → low exposure.

### F16.4 Stationarity and skewness — handled, with code-side overclaims

**Not defects in the thesis.** Ch4 §4.2.2 states the treatment (log uniformly;
ARIMA differenced; trees via lags) and its cost. Code-side only:
- `step_2`: `log_necessary = (n_log + n_diff) >= n_raw` counts brands that need
  *differencing* as support for *log*.
- `step_3.derive_log_transform` records the evidence but returns the config
  value regardless.
- `pipeline_config.py:82` comments `LOG_TRANSFORM_TARGET` as "ADF-confirmed";
  the ADF table does not confirm it.
- Skewness (4.1–5.1) is computed on brand-months **pooled across brands**, so it
  mostly measures brand-size heterogeneity rather than within-series shape. The
  log transform remains right on the multiplicative-variance argument.

### F16.5 Thesis appendix coverage of the four EDA figures

ACF/PACF = **Appendix 5**, Top brands = **Appendix 7**. ECDF and decomposition are
**not** in the thesis.

---

## F17 — Q&A drill swept against the 10-10 snapshot (2026-10-12)

### F17.0 In plain English

The Q&A drill was written on 15 September, before several numbers settled. Six
answers said things the thesis doesn't support, and one said the opposite of the
thesis. All are fixed in `qa-drill.md`. Separately, the sweep found **two places
where the thesis disagrees with its own tables**. Neither matters to the
conclusions, but an examiner could spot either one, so the drill now carries a
prepared line for each.

### F17.1 Drill errors corrected

| Q | Was | Now | Source |
|---|---|---|---|
| Q19 | defended a **one-month** horizon | three months: a quarter is when promo and range decisions are taken | Ch5 §5.4 |
| Q1 | "51 times / 21 times"; "39 months" | "roughly fifty / twenty"; 46 months, last 6–7 held out | Ch10 §10.1; Ch4 |
| Q3, Q4 | "~37 training months" | under four years of monthly history | Ch4 |
| Q9 | implied a clear CSD win | CSD 18.4 vs seasonal naive 19.2 — inside 2.81 pp seed noise, a tie | Ch5 Table 10/11 |
| Q15 | "pilot brand-month" | funded set: B 2.9 vs C 14.6 median | `22_scenario_comparison.csv` |
| Q16 | "guarantee holds, 83.9–91.7"; "six orders of magnitude" | met on CSD/RTD, missed on Energidrikke (86.7) and Danskvand (83.9) | Ch5 §5.6.7 Table 14 |
| Q17 | "every forecast tiers Low" | one value per category, discriminates nothing | Ch7; Ch9 DP3 |

### F17.2 Thesis-internal inconsistencies (unfixable; drilled, not raised)

| # | Prose says | Table says | Weight |
|---|---|---|---|
| F17.2.1 | Abstract, Ch10: the interval "attains its coverage guarantee" | Ch5 Table 14: 2 of 4 categories miss at 90% | **medium** — on slide 23's SRQ2 row ("truthful") |
| F17.2.2 | Ch8, Ch9: serving "below half a megabyte for every model family" | `15_substrate_resource_profile.csv`: XGBoost 0.65, Prophet 1.73 MB | negligible against 4 GB |

### F17.3 One correction to pass 01

Pass 01 §21a said the $25.20 token estimate "overshot the billed $18.46 by ~29%".
Ch8 says the 29% is against the **measured $19.60** (25.20 / 19.60 = 1.29); $18.46
is a separate billing-endpoint figure. The slide fix (~50× / ~20×) is unaffected.

### F17.4 Cross-verified against code and raw results (2026-10-12, R-1012-04)

**In plain English.** Brian asked whether the slide and drill claims were checked
against the actual code and result files, not just the thesis text. Mostly yes.
Re-running the checks on the raw files confirmed nearly everything, **reversed one
of my own drill edits** (the old "36 of 37" counts were right, and the thesis
rounds them up), and found two more small gaps in the thesis.

| Claim | Checked against | Verdict |
|---|---|---|
| Scenario table (all 21 cells), ~50×, ~20× | `22_scenario_comparison.csv` | ✓ |
| Coverage 91.7/91.4/86.7/83.9; width 8–34× | `calibration.csv`; `srq1_calibration.py:267` | ✓. CSV column still named `mean_rel_width`, but the code computes a **median** (the code comment documents the rename); the thesis's "median" is right |
| Seed changes the winner in all four categories; 2.81 pp | `stability_per_seed_accuracy.csv` (recomputed per seed); `20_seed_stability_p1.csv` | ✓ all four flip |
| Pooling wins on the two smallest by 4.5–5.7 pp, "both families agree" | `pooled_summary.md` | **3 of 4 cells.** LightGBM −5.7 / −5.6, XGBoost −4.5 on Danskvand, **+0.1 (tie) on Energidrikke**. Ch9's "agreement between the two model families" is overstated for energy drinks |
| Lag offsets; calendar aligned to target month | `csd_feature_matrix_h3.parquet`; `engineer_features.py` | ✓ (F16.1) |
| Three refusal conditions | `forecast_tool.py`; Ch7 | ✓ |
| 34.5 MB fit peak; prediction 0.65 MB (XGBoost) | `15_substrate_resource_profile.csv` | ✓ (and F17.2.2) |
| **~231 MB end-to-end peak** | **no results artefact** | **Unverified.** Typed into Ch6 Table 20; its components sum to ~241 MB. Plausibly a direct measurement whose component peaks don't coincide — cannot be confirmed from the repo |
| ES / SARIMA use by the code scenarios | `raw_responses/*.json` (regex over 37 data-scenario responses) | ES **36/37**, SARIMA **32/37**; code-only B+D 18/18 and 17/18. Ch9 §9.3's "every one … a seasonal ARIMA" rounds up. **Corrects F17.1**: the drill's original counts were right; restored |

Caveat on the last row: a regex finds the method *named* in a response, which is
strong but not proof it was fitted. That matches how the original counts were made.
