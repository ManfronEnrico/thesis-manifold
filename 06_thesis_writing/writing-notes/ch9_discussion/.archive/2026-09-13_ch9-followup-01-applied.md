---
name: 2026-09-13_20-30_BRANCH_A_ch9-followup-01
description: FOLLOW-UP - Two fixes from the Chapter 9 rewrite did not land. The old SRQ1 paragraph still sits above its replacement, so the chapter states a claim and its correction together; and 9.1.3 keeps two sentences that 9.1.2 now contradicts. Everything else in the rewrite is applied.
category: workflow
applies-to: [ch9_discussion]
triggers: [chapter 9 follow-up, what did not land, branch a]
created: 2026_09_13-20_30
updated: 2026_09_13-20_30
snapshot: 2026-09-13_20-20_ch9-post-rewrite
supersedes: parts of 2026-09-13_18-40_BRANCH_A_ch9-branch-a-rewrite.md
status: prose ready to paste, awaiting human review
---

# Chapter 9 — follow-up 01

Regenerated against `2026-09-13_20-20_ch9-post-rewrite` (45,677 words, up 2,093
from the pass). Repository at `ad9ca62`, fetch clean, 0 ahead / 0 behind. Zotero
re-pulled the same session: **89 items**.

**Do not re-read the main pass.** This note is read on its own, top to bottom.

---

# What you applied

Comment threads on Chapter 9 fell from **17 to 3**. Ten of the twelve fixes
landed, most of them verbatim.

| In the main pass | State |
|---|---|
| Fix 1, replace the SRQ1 paragraph | ⚠ **half applied** — see F1 below |
| Fix 2, 9.1.2 synthesis quality | ✅ applied |
| Fix 3, 9.1.3 opening reword | ⚠ **half applied** — see F2 below |
| Fix 4, 9.1.4 rewritten on the ladder | ✅ applied |
| Fix 5, new 9.1.5 deployment guidance | ✅ applied |
| Fix 6, 9.2.1 DSR framing | ✅ applied |
| Fix 7, Table 23 rebuilt | ✅ applied, with the caption reworded |
| Fix 8, 9.2.3 literature contribution | ✅ applied, both old subsections merged |
| Fix 9, 9.3 practical implications | ✅ applied |
| Fix 10, 9.4 limitations | ✅ applied |
| Fix 11, the four "Connect to:" lines and Outstanding decisions | ✅ all five deleted |
| Fix 12, 9.5 future research | ✅ applied |

**Everything above marked ✅ stands and needs nothing further.** Two fixes
remain, and both leave the chapter contradicting itself as it currently reads.

### One thing you did that no note proposed

You kept **"### 9.1.2 SRQ2: Synthesis quality"** as the heading over the replaced
text. The section no longer discusses synthesis; it delivers the three-property
verdict on the interface. ⚠ **Retitle it "SRQ2: What the interface preserves"**,
or a reader scanning the contents meets a heading that names a component the
thesis removed.

---

# F1 — The old SRQ1 paragraph is still there, above its replacement

**This is the most damaging item in the chapter right now**, because 9.1.1 states
a claim and its refutation in consecutive paragraphs without acknowledging
either.

The four replacement paragraphs landed correctly. The paragraph they were meant
to replace was not deleted, so the section now opens by asserting that tuned
XGBoost is best in every category, and then explains four paragraphs later that
the choice between families is not supported by the data.

**Every substantive claim in the surviving paragraph is false**, which is why the
pass proposed replacing rather than editing it:

| Claim | Measured |
|---|---|
| "Tuned XGBoost was the best model in every category" | Two of four serve **LightGBM** (Energidrikke, RTD) |
| "16.5% (CSD), 22.0% (danskvand), 11.4% (energidrikke), 31.0% (RTD)" | **18.4 / 23.4 / 17.4 / 30.8** — no artefact holds the quoted four |
| "disaggregating to a retail-chain dimension" | The chain grain was **deleted from the repository** (P0035, DEC-GRAIN) |
| "the ≤8 GB constraint" | The thesis constraint is **four** gigabytes |
| "(Ch6 §6.5.6)" | No such section exists |
| "SHAP attributes forecasts chiefly to ... weighted_distribution" | `weighted_distribution` was **tested and excluded** (Ch4 §4.3) |

### Anchor

**Section 9.1.1 SRQ1: Forecasting accuracy under constraints**, the **first**
paragraph of the section — the one immediately under the heading, directly above
the paragraph beginning *"The benchmark's headline result is that the choice
between the two gradient-boosted families is not supported by this data."*

⚠ **The model names are italicised in Word.** Search on a fragment without them:

> *"was the best model in every category, ahead of"*

It is the only occurrence in the document. The paragraph ends:

> *"...which is consistent with retail demand dynamics and lends face validity to
> the models."*

### Action

**DELETE the entire paragraph.** Nothing replaces it — its replacement is already
in the document, immediately below.

### Note — the comment thread on this paragraph

The `VERIFY, INTERNAL REFERENCE` thread anchored to this paragraph is one of the
three still open on Chapter 9, so the thread disappears with the text. That
closes it as **ADDRESSED** rather than leaving it hanging on deleted prose.

### Note — one claim worth rescuing, and it is verified

The surviving paragraph is the only place in the thesis that mentions **SHAP**.
The attribution to `lag_1` is real; only the second half, naming
`weighted_distribution`, is wrong. If you want to keep it, this is the sentence,
and it belongs at the end of the **fourth** replacement paragraph, the one ending
*"...slack as a runtime one."*:

> "Feature attribution supports the models' face validity: in every category the
> largest single contribution to a forecast is the previous month's sales, by a
> margin of roughly four to six times over the next feature, which is what a
> practitioner would expect of monthly demand at this grain."

✅ **Checked, so you need not.** `tables/shap_importance.csv` is dated 2026-09-10
19:04, after the 2026-09-09 18:48 retraining, so it satisfies the
artefact-recency rule. `lag_1` is top in all four categories, at mean absolute
SHAP 2.96 (CSD), 2.26 (Danskvand), 2.71 (Energidrikke) and 2.22 (RTD), against a
runner-up between 0.39 and 0.76.

✅ **`weighted_distribution` does not appear in the artefact at all**, which is
consistent with Chapter 4 recording it as tested and excluded. That is why the
old paragraph's second attribution had to go rather than be corrected.

---

# F2 — 9.1.3 still ends on two sentences that 9.1.2 contradicts

The reword landed: the section now opens correctly on the three production
scenarios. But the two sentences that followed the old opening were not removed,
and one of them asserts exactly what the section above it spends a paragraph
disproving.

The chapter currently says, three paragraphs apart:

> **9.1.2:** "The confidence index intended to summarise this discriminates
> nothing at all... every forecast in every category is assigned the lowest of
> three bands."

> **9.1.3:** "...emits point forecasts plus calibrated intervals and **a
> confidence tier suitable for an agent tool-call**."

Both cannot stand. The second also calls the intervals "calibrated" without
qualification, which 9.1.2 and Chapter 7 both spend paragraphs bounding.

### Anchor

**Section 9.1.3 SRQ3: Integration readiness**, the final two sentences of the
section. The text to replace starts mid-paragraph, immediately after
*"...rather than from the capabilities an integration was expected to need."*

Searchable opening of the span:

> *"The forecasting substrate is nonetheless integration-ready in the senses"*

Searchable end of the span:

> *"...a dev-merge into the Graph Engine), not architectural."*

### Action

REPLACE that two-sentence span. The rest of the section, which you already
applied, is untouched.

#### Replace with

> The substrate meets the readiness criteria in the senses Chapter 3 and Chapter
> 6 specify: it is exposed through a structured, reproducible interface, it is
> reached by a schema-constrained call whose arguments are recorded and checked
> against the request, and it returns provenance sufficient to reconstruct any
> forecast after the fact. What it emits alongside the point forecast is an
> empirical prediction interval and the served model's measured out-of-sample
> error, the latter being what carries the reliability claim for the reasons
> given above. The remaining gap to an active deployment is operational rather
> than architectural, consisting of credentials and a merge into the production
> graph engine.

### Note — what changed and why

- **"a confidence tier suitable for an agent tool-call" is gone.** It is the
  claim 9.1.2 disproves.
- **"calibrated intervals" became "an empirical prediction interval"**, which is
  true without implying the intervals are usable.
- **The track record is named**, so 9.1.3 points at the same load-bearing field
  as 9.1.2, 9.2.2's DP3 and Chapter 7.
- **"Ch3/Ch5" became "Chapter 3 and Chapter 6."** The integration-readiness
  specification is in Chapter 6 since the swap; Chapter 5 is the benchmark.

### Note — this closes the second open thread

The `VERIFY, OUTDATED` thread on 9.1.3 is anchored precisely to this two-sentence
span. Replacing it closes the thread as **ADDRESSED**.

---

# F3 — The subtitle, the last open thread

The third surviving thread is the `FORMATTING` one on the chapter title, asking
for a subtitle. Every other chapter now has one.

### Anchor

**The chapter heading**, where the placeholder text *"COULD USE A SUBTITLE"*
currently sits directly under **Chapter 9 | Discussion**.

### Action

REPLACE the placeholder.

#### Replace with

> What the ladder measured, and what follows for deployment

⚠ **The placeholder text is live in the document**, not a comment. It renders in
the thesis as written, so it must be replaced rather than merely resolved.

---

# Notes archived since the pass

Two of the four Chapter 9 notes are now fully consumed and have been moved to
`ch9_discussion/.archive/`:

| Note | Why |
|---|---|
| `when-to-use-which-scenario-group.md` | Every figure came from the 21-run smoke. Section 9.1.5 is this note rewritten on the funded set. Its F/G finding did not survive: F at 7.3 per cent sits **between** B at 2.9 and C at 14.6, rather than below both |
| `srq4-interpreting-the-accuracy-gap.md` | Its restatement is in 9.1.4 and its multipliers were two-run pilot figures. Its four-explanations table is **carried into `anticipated-assessor-questions.md` as Q4.5** rather than lost |

**Two notes remain live in the folder, deliberately:**

- **`the-result-hinges-on-forecasting-practice.md`** — the ETS and seasonal-ARIMA
  finding is now in 9.1.4, 9.4 and 9.5, but its **grain-asymmetry argument is
  not**. The chapter currently says per-series adaptation and code execution
  "cannot be separated"; this note shows they can, by fitting the pipeline per
  brand on the same three brands, which is one training run. That is the sharpest
  future-work item the thesis has and it is not yet written anywhere.
- **`ad-hoc-data-science-vs-a-trained-pipeline.md`** — its reproducibility axis
  landed, but the framing that opens it has not: the comparison is between an
  artefact produced once and a process re-enacted per request. See F4.

---

# F4 — Optional: the framing sentence the chapter is missing

Not a defect, and not required. Recorded because it is the one idea from your own
notes that makes the SRQ4 result cohere, and it is currently nowhere in the
thesis.

Chapter 9 reports that the dedicated model wins on cost, speed and
reproducibility. It does not say **why those three travel together**, which is
that they are properties of an artefact produced once rather than of a process
re-enacted on every request.

### Anchor

**Section 9.1.4**, at the end of the paragraph beginning *"The second increment
is the thesis contribution, and it is not an accuracy gain."* That paragraph
ends:

> *"...while a generated analysis is re-derived each time."*

### Action

INSERT AFTER — one short paragraph, between that paragraph and the one beginning
*"That reproducibility result deserves to be stated as a property."*

#### Replace with

> Those three advantages are not independent. They follow from a single
> structural difference: a trained pipeline is the product of work done once, and
> an agent handed the same data repeats that work in every session. Exploratory
> analysis, cleaning, feature construction, model selection and calibration are
> paid for once in the first case and per request in the second, which is why the
> dedicated model is simultaneously cheaper, faster and identical between runs.
> The comparison is therefore not between two forecasts but between an artefact
> produced once and a process re-enacted on demand.

### Note

If you take this, **`ad-hoc-data-science-vs-a-trained-pipeline.md` can be
archived** and the Chapter 9 folder reduces to one live note. If you do not, keep
the note live — the idea should not be lost.

---

# Verification

Every anchor in this note was checked verbatim against
`2026-09-13_20-20_ch9-post-rewrite`. All figures come from artefacts consumed
this session: `runs.csv` filtered to `schema.str.startswith('v6')` (63 rows),
`cv_metrics.csv`, `tuned_metrics.csv`, `calibration.csv`, `profiling.csv`, and
the 65 cached responses under
`05_thesis_results/08_experimental_evaluation/raw_responses/`.

⚠ **One correction to my own earlier reporting.** I told you the funded traces
showed no ETS or seasonal ARIMA. That was a false negative: I searched
`runs.csv`, whose `answer` column holds only the final formatted reply and whose
`trace` column holds metadata. Searching the cached responses, where the written
code actually lives, gives **36 of 37 data-scenario runs fitting exponential
smoothing and 32 of 37 a seasonal ARIMA**. The sentence you have already pasted
into 9.1.4 is correct as written.

⚠ **One thing I could not reconcile, flagged rather than resolved.** The cached
response folder holds **65 files** including a brand named `RB_K` and ten files
for two scenarios, while `runs.csv` holds 63 rows across three brands. The file
count is not a run count — the same filename-versus-record mismatch that
`score_interval_communication.py` was fixed for on 2026-09-13. **No figure in
this note or in Chapter 9 is derived from the file count**, but the extra files
are worth explaining before anyone else counts them.
