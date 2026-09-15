---
name: 2026-09-15_BRANCH_A_appendix-placement-analysis
description: PASS - The ten open threads analysed against artefacts. One is not a placement question at all - the memory figures diverge across three chapters and the abstract is stale by 2.5 MB. Placement recommendations for the rest.
category: workflow
applies-to: [ch4_data_assessment, ch5_model_benchmark, abstract, ch10_conclusion, appendix]
triggers: [appendix placement, figure placement, comment threads]
created: 2026_09_15-13_58
updated: 2026_09_15-13_58
snapshot: 2026-09-15_13-55_appendix-placement-comments
status: prose ready to paste, awaiting human review
---

# The ten threads, analysed

Verified at `b2e366a`, fetch clean, nothing incoming. Snapshot
`2026-09-15_13-55_appendix-placement-comments` — 46,868 words, **10 comments in
10 threads**. Zotero: 93 items.

⚠ **Read F1 first. It is not a placement question, and it is the only thing here
an examiner reads on page one.**

---

# F1 — ⚠ The memory figures disagree across three chapters

**Nobody flagged this. It surfaced while checking thread 201.**

`profiling.csv` (ground truth, written by `srq1_profiling.py`) holds:

| Model | Peak fit RSS |
|---|---|
| **XGBoost** | **34.5 MB** |
| **LightGBM** | **17.9 MB** |
| Prophet (per-series) | 5.2 MB |
| ARIMA (per-series) | 2.1 MB |
| Ridge | 1.5 MB |

**What the thesis says:**

| Site | Says | Verdict |
|---|---|---|
| **Ch5 §5.6.6** | *"34.5 MB for XGBoost, 17.9 for LightGBM"* | ✅ **correct** |
| **Ch9 §9.1** | *"31.9 megabytes for XGBoost and 14.9 for LightGBM"* | ⚠ **stale** |
| **Abstract** | *"fitting peaking at thirty-two megabytes"* | ⚠ **stale** |
| **Ch10 §10.1** | *"fitting peaking at thirty-two megabytes"* | ⚠ **stale** |

**What happened:** a re-profile landed after the earlier profiling fix was
applied. Ch5 was updated with the new numbers; the three restatements were not.

⚠ **The abstract is the first page an examiner reads, and it is wrong by 2.5 MB
against a table twenty pages later.**

## F1a — Ch9 §9.1

**Anchor**, verbatim:
> "Peak resident memory during fitting is 31.9 megabytes for XGBoost and 14.9 for LightGBM, against a four-gigabyte ceiling, and serving a forecast peaks below half a megabyte."

**Action:** REWORD.

**After:**
> "Peak resident memory during fitting is 34.5 megabytes for XGBoost and 17.9 for
> LightGBM, against a four-gigabyte ceiling, and serving a forecast peaks below
> half a megabyte."

## F1b — the Abstract

**Anchor**, verbatim:
> "The memory constraint bound the selection of architectures rather than run time, fitting peaking at thirty-two megabytes against a four-gigabyte ceiling."

**Action:** REWORD — `thirty-two` → `thirty-five`.

✅ **Thirty-five rounds 34.5 honestly.** Do not write "thirty-four"; that rounds
the wrong way.

## F1c — Ch10 §10.1

**Anchor**, verbatim:
> "The memory constraint proved non-binding at this data scale, with fitting peaking at thirty-two megabytes and serving below half of one, against a four-gigabyte ceiling."

**Action:** REWORD — `thirty-two` → `thirty-five`.

### Note — one false alarm, do not "fix" it

⚠ **Ch5 line 324 and Ch9 both contain "thirty-four", and neither is a memory
figure.** Both describe *interval width* — *"intervals spanning some thirty-four
times the quantity being forecast"*. **Correct as written. Leave alone.**

---

# F2 — Thread 201, the resource-profile figure ⚠ three-way disagreement

**Your comment says the figure has three models and the prose says four. Both are
true, and the artefact says five.**

| Source | Models |
|---|---|
| **`ch5_resource_profile_v2.svg`** | **3** — XGBoost, LightGBM, Ridge |
| **Ch5 §5.6.6 prose** | **4** — XGBoost, LightGBM, ARIMA, Ridge |
| **`profiling.csv`** | **5** — the four above **plus Prophet (5.2 MB)** |

✅ **The artefact is right and both the figure and the prose are incomplete.**

**Action — regenerate, then extend the prose by four words:**

1. **Regenerate** `ch5_resource_profile_v2.svg` from `profiling.csv` via
   `05_thesis_results/generate_architecture_diagrams.py`, so all five appear.
2. **Then REWORD** §5.6.6's opening sentence:

**Before:**
> "Peak resident memory during fitting is in the tens of megabytes for every model: 34.5 MB for XGBoost, 17.9 for LightGBM, 2.0 for a per-series ARIMA and 1.5 for Ridge, as can be seen in **Figure 7**."

**After:**
> "Peak resident memory during fitting is in the tens of megabytes for every
> model: 34.5 MB for XGBoost, 17.9 for LightGBM, 5.2 for a per-series Prophet,
> 2.1 for a per-series ARIMA and 1.5 for Ridge, as can be seen in **Figure 7**."

⚠ **The prose also says "2.0" where the artefact says 2.1.** Corrected above.

---

# F3 — Thread 139, the modelling-pipeline figure

**Your comment says the figure shows four candidate models including seasonal
naive, against five plus benchmarks in the prose.**

⚠ **The figure on disk does not match that description.**
`ch5_modelling_pipeline_v1.svg` contains: **ARIMA, Drift, Naive, Prophet, Ridge,
SeasonalNaive, LightGBM, XGBoost** — the full set.

✅ **§5.1 is correct and consistent with the repository:** *"Five model families
... ARIMA and Prophet ... LightGBM and XGBoost ... Ridge"*, plus the
parameter-free benchmarks. §5.3 has six subsections matching.

→ **Most likely you read a stale render.** **Re-insert the current SVG and
re-check.** If the freshly inserted figure still shows four, regenerate it — but
the source file is already right, so no prose change is warranted.

**Do not change the prose to match a figure.** The prose agrees with the code.

---

# F4 — Thread 104, "0 figures"

**Found it.** The string lives in the figure, not the prose:

`05_thesis_results/04_data_assessment/figures/ch4_eda_pipeline_csd_v1.svg`
> "22 tables, **0 figures**"

⚠ **The committed version says `0 figures`; the live CSD folder holds 8 plots.**
The count is computed at render time, so the shipped SVG was generated when the
plot directory was empty.

**Action: REGENERATE** via `generate_architecture_diagrams.py`. It will read the
directory and write **"22 tables, 8 figures"**. **No prose change** — §4.2.5's
text does not state a count.

---

# F5 — Thread 94, the four unplaced CSD EDA plots

✅ **All four exist and are ~1 MB each:**

| File | Recommendation |
|---|---|
| `06_acf_pacf_plots.svg` | ⚠ **in-text, §4.2.5** — the section discusses autocorrelation and currently shows no ACF plot |
| `07_promo_intensity_analysis.svg` | **appendix** — §4.2.5 already gives the r = 0.94 / r = 0.99 figures in prose |
| `05_top_brands_timeseries.svg` | **appendix** — context, not argument |
| `08_correlation_heatmap.svg` | **appendix** — diagnostic |

**Why ACF goes in-text:** §4.2.5's whole argument is that the quarterly signal
exceeds the first-order one (+0.53 at lag 3 against +0.40 at lag 1). **That is a
claim a reader wants to see.** The other three support claims already stated
numerically.

⚠ **At ~1 MB each, four more SVGs add ~4 MB.** The `.docx` is already 3.67 MB,
up from 1.86 MB two hours ago. **Watch the file size.**

---

# F6 — Thread 187, the XGBoost forecast overlay

**The figure exists:** `05_thesis_results/05_model_benchmark/figures/fig3_forecast_overlay.svg`

**Anchor**, Ch5 §5.6.1, verbatim:
> "An preview of XGBoosts forecast overlay for HARBOE within the CSD category can be seen in **Figure** **6**."

⚠ **Two typos in one sentence** — *"An preview"* → *"A preview"*, and
*"XGBoosts"* → *"XGBoost's"*.

**Action:** REWORD, and add the contextualising sentence you asked for.

**After:**
> "A preview of XGBoost's forecast overlay for HARBOE in the CSD category is shown
> in **Figure 6**. The fitted series tracks the observed one through both the
> December and June peaks, and the visible divergences fall in the months where
> the brand's own history is thinnest — which is the behaviour the error figures
> above summarise, shown for a single series rather than averaged across the
> panel."

**Placement: keep it in-text at §5.6.1.** It is the only place a reader sees what
a forecast from this substrate actually looks like.

---

# F7 — Thread 138, §5.2 has no prose at all

**§5.2 Modelling Pipeline is, in its entirety:**

> "As can be seen below in Figure 5."
> **Figure 5** - Modelling Pipeline

⚠ **A section consisting of one sentence pointing at a figure will read as
unfinished.** A figure cannot carry a section on its own.

**Action:** INSERT BEFORE the existing sentence.

> The modelling pipeline is a fixed sequence applied identically to every
> category, so that a difference in results reflects the model rather than the
> treatment it received. Each category's panel is aggregated to brand-and-month
> grain, split proportionally into training, validation and test partitions, and
> passed through feature construction that derives lags, rolling summaries and
> calendar terms from the training portion alone. Every candidate model is then
> fitted on the same matrix, tuned against the validation partition, and scored
> once on the untouched test partition. The sequence is shown in Figure 5.

Then delete *"As can be seen below in Figure 5."* — the new final sentence
replaces it.

⚠ **Verify the split and tuning description against §5.4 before pasting** — I
wrote it from §5.4.1–5.4.5's structure, and §5.2 must not contradict it.

---

# F8 — the appendix numbering is inconsistent

**The Table of Appendices lists two entries. The appendix body lists seven.**

| ToC | Body |
|---|---|
| **Appendix 1** – Literature Review Design Map | **Appendix 1** - Literature Review Design Map ✅ |
| **Appendix 2** – Star Schema Diagram (CSD) | ⚠ **Appendix 2** - Methodology Design |
| — | **Appendix 3** - Monthly Sales Distribution (CSD) |
| — | **Appendix 4** – Star Schema Diagram (CSD Example) |
| — | **Appendix 5** - Feature Matrix |
| — | **Appendix 6** - Abbreviated Model Response Example |
| — | **Appendix 7** - Per Scenario and Run Records |

⚠ **The ToC's "Appendix 2" is the body's "Appendix 4".** Regenerate the Table of
Appendices from the body before submission — a reader following the ToC lands on
the wrong appendix.

## Thread 99 resolves once the numbering settles

**The last `Appendix [N]` placeholder**, Ch4 §4.2.3 — ⚠ **note the double space
before "rather"**:

> "The cost is accepted deliberately, and the per-brand results are reported in full in Appendix [N]  rather than summarised away."

**The ADF table (`step_2_05_adf_per_brand`) is not yet among the seven.** Add it,
then use its number. **On the current scheme it would be Appendix 8.**

---

# Threads 27, 270, 308 — unchanged

| Thread | Item |
|---|---|
| **27** | Ch1 Figure 1, SRQ hierarchy tree — regenerate |
| **270** | Ch8 Table 23, seven scenarios — regenerate and replace |
| **308** | dynamic Zotero reference list |

⚠ **308 is still blocked by 13 bad dates in Zotero** — 4 missing a year (three of
them duplicate *Elements of Statistical Learning* records) and 9 with a month
string in the year field (`Augu` for XGBoost, `Marc` for Saunders, `July` for
Optuna, `01.2` for Hevner). **Fix in Zotero, re-pull, then generate.**

---

# The order I would work in, with 14:00 approaching

| | Item | Why first |
|---|---|---|
| **1** | **F1a, F1b, F1c** — three memory rewords | ⚠ **the abstract is wrong on page one.** Three minutes |
| **2** | **F4** — regenerate the EDA pipeline figure | one command, removes "0 figures" |
| **3** | **F2** — regenerate the resource figure, then the prose | figure and prose both under-report |
| **4** | **F8** — regenerate the Table of Appendices | a reader following it lands wrong |
| **5** | **F6, F7** — the two Ch5 prose blocks | paste-ready above |
| **6** | **F5** — place the four EDA plots | watch the file size |
| **7** | **F3** — re-insert the pipeline figure and check | may be nothing |

**Items 1 to 4 are twenty minutes and fix everything a reader can catch
unaided.**
