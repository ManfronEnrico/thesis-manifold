---
name: 2026-09-13_01-05_BRANCH_A_ch6-branch-a-pass
description: NOTE - Chapter 6 top-to-bottom against BRANCH A, the 63-run funded set. Six fixes, two comment verdicts. The argument stands unchanged; the memory figures are eight weeks stale and the pilot language is superseded by a funded run.
category: workflow
applies-to: [chapter 6]
snapshot: 2026-09-12_22-28_ch7-post-merge
branch: A (fallback) — commit 58243f3, schema v6-shared-composition+af04a42a478b
created: 2026_09_13-01_05
updated: 2026_09_13-01_05
status: open
---

# Chapter 6 — BRANCH A pass

Written against **Branch A**, the funded 63-run set, as if it is final — because
today it is. Branch B may re-engineer the features and re-run; it has not
happened and may never.

**Snapshot `2026-09-12_22-28_ch7-post-merge`.** Repository at `58243f3`, pushed,
0 ahead / 0 behind. Zotero 89 items. Chapter 6 is 3,175 words and unchanged since
the Section 6.7 followup landed, so every anchor below is current. **All anchors
verified verbatim against the snapshot.**

**Notes swept:** `ch6-CONSOLIDATED-pass.md` and `ch6-followup-02-section-6-7.md`
— both **applied**. Their fixes are present in the snapshot: 6.7 is retitled
"The Scenario Ladder", Table 17 names all seven arms, the sandbox provider is
gone, the duplicated memory clause is single, and "with human oversight" is gone.
**Archive both.** Nothing in them is carried forward.

**Every figure below is computed from an artefact consumed this run:**

| Artefact | Written | Used for |
|---|---|---|
| `tables/profiling.csv` | 2026-09-11 18:37 | the memory figures in F1 |
| `08_experimental_evaluation/runs.csv` (v6 rows only) | 2026-09-12 21:06 | the funded-run facts in F3, F4 |
| `models/index.json` | 2026-09-09 21:10 | which model each category serves |

⚠ **`runs.csv` holds 69 rows, not 63.** Six are superseded `v2` rows. Every
figure here filters `schema.str.startswith('v6')`. Pooling them once produced an
$11.13 figure for an $8.05 block.

---

# The verdict: Chapter 6 is sound and needs six fixes

The chapter's **argument is unaffected by the funded run**, exactly as the
handover predicts. The three-layer structure, the delegation-over-generation
principle, the bounded-agent framing and the ladder design are all confirmed
rather than challenged by 63 runs.

What needs fixing is narrower: a table of memory figures measured on 27 June,
superseded twice since; and four places where the chapter speaks of a pilot that
has now been replaced by a funded experiment.

---

# The fixes

## Fix 1 — The memory table is eight weeks stale, and two figures roughly doubled

Table 18 is dated **2026-06-27**. The substrate was retrained on 9 September and
re-profiled on 11 September. Two of its four model figures moved substantially,
and in the direction that makes the table *understate* the footprint.

| | Table 18 says | Measured 2026-09-11 |
|---|---|---|
| XGBoost, active | ≈15 MB | **31.9 MB** |
| LightGBM, active | ≈7 MB | **14.9 MB** |
| Ridge, active | < 1 MB | 1.6 MB |
| Max serving footprint | not stated | **0.47 MB** |

⚠ **The conclusion is untouched.** Even at 31.9 MB the largest model is under one
per cent of the four-gigabyte ceiling, so "the budget binds the space of models
that could be selected rather than the footprint of what was selected" remains
exactly right. **Only the numbers move.**

### Anchor

**Section 6.8 Memory, Cost, and Latency Budget.** The table above the caption
**"Table 18 - Per-component budget, measured by RSS (psutil), 2026-06-27"** —
its "Active model" row reads *"Active model (one at a time; XGBoost ≈15, LightGBM
≈7, Ridge < 1 MB)"*.

### Action

EDIT-THEN-INSERT. Two edits: the row, then the caption date.

#### Replace the "Active model" row with

| Active model (one at a time; XGBoost 31.9, LightGBM 14.9, Ridge 1.6 MB) | ~32 MB | Fitting |

#### Replace the caption with

> ***Table 18*** *- Per-component budget, measured by resident set size, 2026-09-11*

### Note — the end-to-end peak moves too, and someone must recompute it

⚠ The chapter states an end-to-end peak of **approximately 231 MB**, which was
computed from the June components. With the active model at 32 MB rather than 15,
the same arithmetic gives roughly **248 MB**. **I have not recomputed the other
rows**, and the runtime and data figures may also have moved, so do not simply
swap 231 for 248 — the whole column needs one re-measurement.

**Until it is re-measured, the safe edit is the two model figures and the date.**
The 231 MB total is then internally inconsistent with its own rows by about 17 MB,
which is worse than nothing but far better than four stale model figures. If a
re-measurement is not going to happen before submission, say "under 250 MB" and
drop the false precision.

---

## Fix 2 — "Five lightweight model families" is true of the benchmark, not of what is served

Section 6.3 says the substrate **comprises** five families. Measured from
`models/index.json`: **two are served.** CSD and Danskvand serve XGBoost;
Energidrikke and RTD serve LightGBM. ARIMA, Prophet and Ridge were benchmarked
and are not deployed.

The sentence is defensible as written if "substrate" means the benchmarked set,
which is how Chapter 5 uses it. But an examiner reading Chapter 6 as the
architecture specification will ask which five are running.

### Anchor

**Section 6.3 The Forecasting Substrate (SRQ1)**, first sentence:

> "The substrate comprises five lightweight model families, selected to cover the
> inductive biases most relevant to monthly retail demand: ARIMA and Prophet as
> classical statistical methods, LightGBM and XGBoost as gradient-boosted
> ensembles, and Ridge regression as a regularised linear baseline."

**The next sentence begins:** *"They are evaluated across the four beverage
categories..."*

### Action

REWORD — add one clause. The list stays.

**After:**

> "The substrate comprises five lightweight model families, selected to cover the
> inductive biases most relevant to monthly retail demand: ARIMA and Prophet as
> classical statistical methods, LightGBM and XGBoost as gradient-boosted
> ensembles, and Ridge regression as a regularised linear baseline. Five are
> benchmarked; one is served per category, selected on cross-validated accuracy,
> so the deployed substrate holds a single model at a time."

### Note

This also pre-empts a second question. Selection is on the **cross-validation**
score rather than the test score, deliberately, because selecting on test is
selection on the evaluation set. That is stated in Chapter 5 and does not need
repeating here, but the clause above makes the one-per-category fact visible at
the point a reader first meets the substrate.

---

## Fix 3 — "In the pilot run" is superseded by 63 funded runs

Section 6.4 closes on a pilot. The funded experiment has since run and the same
check passed on a far larger set.

**Measured across the 63 v6 runs:** every answer carried the fixed-format closing
line, and the figure in it matched the logged forecast in **58 of 58 traces
checked**, with zero mismatches. (Five ØRBÆK first-repeat traces are stored under
a superseded filename from before a transliteration fix; their rows are in
`runs.csv` and unaffected.)

### Anchor

**Section 6.4 The Structured Forecast-Tool Interface (SRQ2)**, the final
paragraph, in full:

> "In the pilot run validation was exercised: the figure the agent reported and
> the figure the model produced agreed exactly, and the recorded tool-call span
> confirmed that the agent had queried the series it was asked about at the
> intended horizon."

### Action

REPLACE.

#### Replace with

> In the evaluation reported in Chapter 8 this validation was exercised across
> every run: the figure each agent reported and the figure the model produced
> agreed in every case, and the recorded tool-call span confirmed that the agent
> had queried the series it was asked about at the intended horizon.

### Note — why not give the number here

The count belongs in Chapter 8, where the experiment is described and the reader
can see what 63 runs means. Naming it here would force Chapter 6 to explain the
design before it has introduced it. **The claim is the mechanism; the count is the
evidence.**

---

## Fix 4 — The ladder paragraph is now true as a statement of what was run

Comment 293 (Brian, 2026-09-12) on the "deliberately narrow" paragraph says:
*"This might need an update if we decide to ramp up the experiment. Currently it
is true, and the run is estimated at $20, so we could ramp up to $30 and have a
larger trial sample."*

✓ **No edit needed, and the thread closes.** The funded run went ahead at exactly
the size the paragraph describes: three brands from one category, spanning three
orders of magnitude, every scenario answering for the same three brands. Actual
spend was **$19.60**.

**One optional strengthening**, because the paragraph currently describes the
design in the abstract and the run has now happened:

### Anchor

**Section 6.7 The Scenario Ladder (SRQ4)**, the final paragraph. Starts:

> "The comparison is deliberately narrow."

Ends:

> "...which is what the ladder is built to expose."

### Action

REWORD — one sentence added at the end. Optional.

#### Append to that paragraph

> Each scenario answers three times for each brand, so that the variation within
> a scenario can be measured alongside the differences between them.

### Note — this is the single most important methodological fact about the results

⚠ The repeats are what make the ladder readable. **Within-arm spread on the plain
scenario reaches 766 percentage points on one brand** — larger than most of the
gaps between scenarios. Without repeats the comparison would have produced a
ranking that looked clean and meant nothing. Chapter 8 reports this; Chapter 6
should say the design anticipated it.

---

## Fix 5 — The on-demand sandbox point is made, but not the cost consequence Brian raised

Comment 287 (Brian) on Section 6.5: *"Its also relevant to raise that the sandbox
is being instantiated on demand, meaning only if queries are actually sent by end
users, will the company be charged, cutting down the server costs significantly."*

The chapter **already makes half of this**, in Section 6.7: *"the sandbox is
created per request, so it is charged only when a query is actually made."*

⚠ **It is in the wrong section.** The comment is anchored on 6.5, which is where
the agentic layer's cost profile is established, and 6.7 is about the comparison
design. A reader meets the memory argument in 6.5 and the cost argument two
sections later.

### Anchor

**Section 6.5 The Bounded Tool-Using Agentic Layer**, first sentence:

> "The agentic layer is an LLM orchestrator accessed through a remote API rather
> than loaded locally, a decision that keeps the language model out of the memory
> budget entirely, since model weights large enough to be useful would exhaust a
> four-gigabyte ceiling on their own."

### Action

INSERT AFTER — one sentence, immediately following the anchor.

#### Insert

> The same arrangement governs cost rather than only memory: because both the
> language model and the execution sandbox are reached as hosted services created
> per request, the deployment is charged when a user asks a question and not for
> the capacity to answer one.

### Note

This is a genuine architectural point for a small provider, and it is the reason
the four-gigabyte ceiling is a *hardware* budget rather than a total cost of
ownership. **Verified against the funded run:** the seven arms cost between $0.08
and $6.90 in estimated tokens across nine runs each, and nothing was charged
between runs.

---

## Fix 6 — Table numbering still collides with Chapter 7

⚠ **Carried forward from the Chapter 7 pass, still unresolved.** Chapter 6 and
Chapter 7 both number their tables **17, 18 and 19**.

| Chapter | Table numbers |
|---|---|
| Ch5 | 5–16 |
| **Ch6** | **17, 18, 19** |
| **Ch7** | **17, 18, 19** ← collision |
| Ch8 | 20, 21, 22 |

Chapter 6's numbers are Word field references and renumber automatically.
**Chapter 7's are typed as plain text**, which is why they did not move. The fix
belongs in Chapter 7 and is recorded there; it is noted here only so that nobody
"fixes" Chapter 6's numbering instead.

### Action

**None in Chapter 6.** Do not renumber this chapter.

---

# Comment ledger

| Thread | Section | Verdict |
|---|---|---|
| Brian, on-demand sandbox (CONTEXT) | 6.5 | **ADDRESSED** by Fix 5. The point existed in 6.7; Fix 5 puts the cost consequence where the comment sits. |
| Brian, ramp-up (UPDATE) | 6.7 | **VERIFIED-OK.** The funded run matched the described design exactly, at $19.60. The paragraph is true as written. Fix 4 offers an optional strengthening. |

---

# What Branch B would change, and what it would not

Recorded so this note stays valid if Branch B lands.

| Would change | Would not change |
|---|---|
| the memory figures again, if the feature set changes | the three-layer architecture |
| the lag-depth figure quoted in Chapters 4 and 5 (thirteen → twelve) | the delegation-over-generation principle |
| nothing else in this chapter | the ladder design, the bounded-agent framing, the technology table |

⚠ **The thirteen-month lag figure is not in Chapter 6.** I checked: it appears in
Chapters 4 and 5 only. The handover's pointer was to a note, not to this chapter.

---

# Related

- `plans/P0049_.../BRANCH_A_STATE.md` — the measured experiment
- `plans/P0049_.../HANDOVER_CH6_CH7_CH8_BRANCH_A.md` — the brief this pass answers
- `.archive/` — both prior Ch6 notes, applied, archive on reading this
