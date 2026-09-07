---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-07 03:00:00
---

# P0046 — Findings

> Condensed 2026-09-06 from 946 lines. Superseded findings are dropped, not
> archived — the decisions they led to are in `task_plan.md`. Full history in git.

---

## The artefact map — where everything is now

| Group | Was (pre-09-06) | Now | Count | Regenerable |
|---|---|---|---|---|
| Appendix tables | `04_thesis_results/appendix/` | `05_thesis_results/appendix/` | 25 | **YES, tested** |
| SRQ1 results | `04_thesis_results/srq1/` (36 loose) | `…/srq1_model_performance/{figures,tables,models}/` | 49 | **YES, tested** |
| SRQ1 figures | `…/srq1/figures/` (4) | `…/srq1_model_performance/figures/` | 3 | **YES, tested** |
| SRQ2 results | `04_thesis_results/srq2/` | `…/srq2_structured_tool_interface/` | 5 | **NO — cited but unreproducible (F8)** |
| SRQ4 aggregation | `04_thesis_results/srq4/` | `…/srq4_scenario_experiments/` | 5 | yes (paid re-run) |
| SRQ4 runs + raw | `…/srq4/{run_*,raw_responses}` | `04_SRQ4_Scenario_Experiment/runs/` | 4 dirs | n/a — raw evidence |
| Conceptual diagrams | `05_thesis_writing/figures/` | `05_thesis_results/diagrams/` | 5 live + 1 quarantined | **YES, tested** |
| EDA `.md` + `.png` | pipeline outputs | **promoted** to `…/eda/{cat}/{tables,plots}/` | 119 + 30 | **YES, tested** |
| EDA `.csv` | pipeline outputs | **stays** (DEC-EDA-SPLIT) | 119 | yes (pipeline) |
| Enrico notebook figures | `05_thesis_writing/analysis/` | `06_thesis_writing/analysis/` | 18 | **NO — archived notebooks** |
| Triage figures | `05_thesis_writing/figures/{unsure,update_*}` | `06_thesis_writing/figures/…` | 12 | 6 pairs from the diagram generator |

**Nothing was lost.** Every artefact is accounted for.

### Archived this session (never deleted — DEC-ARCHIVE-NOT-DELETE)

| Item | To | Why |
|------|----|-----|
| `fig2_granularity.png` | `srq1_model_performance/.archive/zombie_…_2026-09/` | F1 |
| `phase3_result.json` | `05_thesis_results/.archive/phase3_region_grain_2026-09/` | producer archived by P0035 |
| `generate_systemB_diagram.py` | `05_thesis_results/.archive/systemb_…_2026-09/` | F4 |
| shadow copy of same | `.archive/shadow_scripts_2026-09/` | byte-identical duplicate |
| `ml_retraining/` (11 scripts) | `.archive/ml_retraining_2026-09/` | F5 |
| SPSS / Indeks Danmark | `.archive/spss_indeksdanmark_2026-09/` | F6 |
| `ram_budget_v1.{svg,png}` | `diagrams/.archive/fabricated_ram_budget_2026-09/` | F13 — fabricated values |

Each carries a README: what it is, why it moved, how to recover it.

---

## F1 — The zombie: `fig2_granularity.png`

The most dangerous artefact found, because it looked correct — right folder,
right name, same 2026-07-11 date as its legitimate siblings. It depicts a
brand-vs-chain grain comparison DEC-GRAIN (2026-07-12) decided to stop making.
P0035 deleted the producing code; `srq1_generate_performance_figures.py` still
carries the note *"fig2_granularity.png is no longer produced."* The image
outlived its producer by two months.

Verified before archiving: committed at git `4c7a98b`; **cited by zero
chapters**; re-running the producer yields 3 figures and does not recreate it.

**The general lesson**: a tidier folder tree would not have caught this. Only a
producer→artefact mapping does. That is why Phase 6's invariant is *every
artefact has a live producer*, not *every folder is neat*.

## F2 — 32 of 34 PATHS constants were silently dead

The 2026-09-06 SRQ restructure broke every tier constant. `import PATHS`
still succeeded because `Path()` never validates — nothing fails until a script
reads or writes.

**This vindicated DEC-PATHS more sharply than tidiness ever could**: one file
needed repair instead of forty, and a single probe enumerated the blast radius.
Constants for genuinely-removed directories (`THESIS_MODELLING_SERVING_*`,
`THESIS_DATA_ASSESSMENT_DIR`, the four SPSS ones) were **removed, not
repointed** — a constant aimed at a missing path is how this went unnoticed.

Now: 39/39 resolve, `print_all_paths()` clean.

## F3 — Hardcoded paths: 43 scripts → 10

Audited every live `.py` for five defect classes. All 77 compile. The `CLAUDE.md`
→ `.env.example` anchor swap (Brian: the repo ships to assessors and shouldn't
name the assistant) exposed two defects that were *not* the anchor:

1. **`.gitignore`'s `.env.*` excluded `.env.example`.** An uncommitted anchor
   cannot anchor a fresh clone — the swap would have been *worse* than
   `CLAUDE.md`, which was at least committed. Fixed with `!.env.example`.
2. **Every inline finder walked from `Path.cwd()`, not `__file__`** — so the root
   depended on where python was invoked, and runs from outside the repo failed.

`parents[N]` hops replaced in 17 scripts: they encode folder *depth*, which the
restructure changed — same silent-breakage class as F2, one level down.

**The 10 survivors are all legitimate**: `PATHS.py`'s own literals (it is the
authority), a docstring about the old anchor, `thesis_snapshot.py`'s OneDrive
default (outside the repo by nature), two sibling-relative `parents[1]` uses, and
3 scripts already dead from importing a long-removed module.

The rule is now a check, not an intention: *no live script contains a literal
tier name, a `CLAUDE.md` anchor, or a `parents[N]` repo-root hop.*

## F4 — `generate_systemB_diagram.py` drew the abandoned writing system

Brian's suspicion about "System A/B" scripts was right and sharper than expected.
It renders a multi-agent **thesis writing** system — Thesis Coordinator, Writing
Agent ("Bullet points only (never prose)"), Critic Agent, APA Citation Agent —
the abandoned promise, not the SRQ2/SRQ4 artefact the thesis presents.

Searching its output name `system_b_overview` returned three files: the script,
its shadow copy, and this plan. **Zero chapters.** Archived with a README.

`generate_architecture_diagrams.py`'s six diagrams are different — they depict
real architecture and are worth *updating*, not dropping.

## F5 — `ml_retraining/` archived rather than repointed

11 scripts reading `results/phase1/`, `data/raw/`, and `Thesis/indeksdanmark` —
none of which exist (`Thesis/` went in P0028). Repointing would have manufactured
PATHS constants for folders nobody maintains: the exact failure this plan
removes, and the same reasoning that deleted the serving constants in F2.

## F6 — SPSS dropped; the abstract still claims it

Indeks Danmark was never used. Data archived, four constants removed (three
already resolved to nothing).

**Open item**: the abstract still names it as part of the empirical base — twice,
in the authoritative `.docx`. That is a claim about *what data the study rests
on*, in the section examiners read first. Verified scope: **abstract only** (Ch3
and Ch4 are clean), so it is a two-sentence correction. Tracked at
`06_thesis_writing/writing-notes/indeks-danmark-claim-must-be-corrected.md`.

## F7 — Regenerability tested, not assumed → a reproducibility defect

Every free generator was **run**, not inspected.

| Generator | Result |
|-----------|--------|
| `export_appendix.py` | PASS — 12 tables, byte-identical bar the timestamp |
| `srq1_generate_performance_figures.py` | PASS — 3 figures |
| `srq1_generate_shap_figures.py` | PASS after installing `shap` |
| `training_report.py` | PASS |
| `generate_architecture_diagrams.py` | PASS after installing system graphviz (F13) |

`requirements.txt` omitted `graphviz` entirely (undeclared *and* uninstalled),
plus `matplotlib` and `statsmodels` (undeclared, coincidentally present). **An
assessor cloning the repo and running `pip install -r requirements.txt` could
reproduce no figure at all** — a defect in the deliverable, not a convenience
issue, and invisible to code reading. Now declared, with a comment warning that
the Python binding alone is insufficient: graphviz needs a system `dot`.

Also fixed: `export_appendix.py`'s generated README hardcoded a producer path
dead since the restructure — the index told readers to run a script that no
longer exists. Now derived from `Path(__file__).relative_to(ROOT_DIR)`.

## F8 — SRQ2: orphaned producers, but the results ARE cited (corrected)

**Correction, 2026-09-06.** My earlier reading — that the LLM-as-Judge files were
artefacts of a "dropped design" — was wrong, and it mattered. Reading the
chapters shows the opposite: **LLM-as-Judge is live in the thesis.**

`judge_scores.csv` is the source of **Table 21** in Ch8 §8.3
("LLM Judge Scoring Likert Scale Results"). The chapter states the exact numbers
the file holds — LLM synthesis mean 3.81 vs rule-based baseline 3.15, and the
per-dimension row `2.96 / 3.74 / 4.00 / 4.00 / 4.34`. The CSV has 100 rows =
50 stratified cases x 2 systems, matching the stated N=50 design.
`synthesis.csv`/`synthesis_summary.md` likewise back Ch7 §7.2's deterministic
synthesis results, which the summary file names explicitly.

So the SRQ2 problem is **not** "stale artefacts of an abandoned design". It is:

| | Status |
|---|---|
| Are these cited? | **Yes — Table 21 in Ch8, plus Ch7 §7.2 results** |
| Can they be reproduced? | **No — every producer is archived** |

That combination is worse than staleness. A cited table whose producer is
archived cannot be checked, corrected, or defended if an examiner asks how it
was computed. Zero live scripts reference `THESIS_RESULTS_SRQ2_DIR`; the
producers (`srq2_synthesis.py`, `srq2_agent.py`) sit in
`01_SRQ1_Model_Training/02_thesis_modelling/.archive/superseded_scripts_2026-08/`.

**Where my error came from**: I inferred "dropped" from Brian's remark plus the
2026-07 dates and the archived producers, and never checked whether a chapter
cited them. Provenance direction matters — *producer → artefact* says whether a
thing can be rebuilt; only *artefact → chapter* says whether it must be.

**Independently**, Brian has already flagged this exact section in review:
comments 381/383/384 on Ch8 §8.3 Results carry `VERIFY`, `OUTDATED` and
`INCORRECT` ("LLM as judge, trial number not up to date"). So the content is
under suspicion on its own terms, separate from the reproducibility gap.

**Recommendation (RESTORE, not retire)**: restore `srq2_synthesis.py` and
`srq2_agent.py` from `.archive/` to a live SRQ2 location, repoint them at
`THESIS_RESULTS_SRQ2_DIR`, and re-run. `srq2_synthesis.py` is deterministic and
free; only `srq2_agent.py` needs API calls. That closes the review comments and
the reproducibility gap in one pass. Retiring is not available: the table is in
the thesis.

## F9 — SRQ1 reshaped into figures/ tables/ models/ (done)

36 loose top-level files -> `figures/ 3`, `tables/ 33`, `models/ 13`, zero loose.

**Every one of the 36 has a live producer** — verified two ways: name-in-source
across all candidate scripts, then explicit write-call detection (35/36; only
`param_drift.csv` builds its name dynamically). That is a materially healthier
result than SRQ2 (F8) and worth stating: SRQ1 is fully reproducible.

**Moving files alone does not hold.** Re-running `training_report.py` after the
move immediately rewrote `training_report.md` to the flat path, undoing it. The
shape only persists if the producers write into it. Rather than edit ~40 call
sites across 15 scripts, `OUT`/`RES` is now a small `_SRQ1Out` resolver that
routes `OUT / "name.csv"` by role (models allow-list, then figure extensions,
else tables) and resolves reads the same way, so sibling scripts reading each
other's output keep working. One changed line per script.

Split by **role, not extension**: a `.csv` and its rendered `.md` twin are one
artefact in two formats, so an extension split would separate `calibration.md`
from the `calibration.csv` it came from.

Testing caught a bug the design invited: the figure scripts do `RES / "figures"`,
which the resolver filed as a *table*, producing `tables/figures/`. Fixed with a
passthrough for bare subfolder names. Found only by running the generators.

New `PATHS.py` helpers: `get_srq_figures_dir(n)`, `get_srq_tables_dir(n)`,
`get_srq_models_dir(n)`.

## F10 — Generator names now state what they emit

`generate_figures.py` said nothing about *which* figures, and sat beside
`srq1_figures.py`, which produced entirely different ones.

| Was | Now |
|-----|-----|
| `generate_figures.py` | `generate_architecture_diagrams.py` |
| `srq1_figures.py` | `srq1_generate_performance_figures.py` |
| `srq1_shap.py` | `srq1_generate_shap_figures.py` |

`export_appendix.py` and `training_report.py` already said what they do.
References updated in `README.md`, `CHEATSHEET.md`, `repository_map.md`,
`requirements.txt`.

## F11 — Enrico's 18 notebook figures (unresolved)

`06_thesis_writing/analysis/figures/` (11) and `figures_agentic/` (7) trace to
archived notebooks that hardcode `/Users/enricomanfron/Desktop/…`. They are
**archived, not broken** — the blockers are edits, not rewrites. Per-file
RESTORE or RETIRE after the citation sweep, with the pairing rule that RETIRE
archives the *image* too: a stale image left beside a retired producer is exactly
the F1 trap.

## F12 — `ram_budget_v1` must not be naively re-run

The diagram generator still holds P0040-F5's fabricated numbers. Real
measurements now exist in `05_thesis_results/appendix/`
(`02_substrate_resource_profile`, `04_sandbox_resource_profile`). Rewire before
regenerating, or the fabrication is reproduced.

---

## F13 — All six diagrams regenerate; one had to be quarantined

Graphviz installed 2026-09-06 (`winget install Graphviz.Graphviz`), clearing the
last blocker. **Every generator in the repo now runs.**

But the first successful run in months immediately re-emitted the fabrication:
`fig4_ram_budget()` hardcodes seven invented MB values (P0040 F5), and one of
them is **"Indeks raw load, 970 MB"** — the dataset dropped the same day as never
used. The figure charts memory consumed by data the thesis does not touch.

Handled:
- `ram_budget_v1.{svg,png}` -> `05_thesis_results/diagrams/.archive/fabricated_ram_budget_2026-09/`
- the `fig4_ram_budget()` **call is commented out** with an explanation, so the
  generator cannot silently reproduce it on the next run
- README records the real measurements to rewire to
  (`appendix/02_substrate_resource_profile`, `04_sandbox_resource_profile`,
  `srq1_model_performance/tables/sandbox_profiling.csv`)

Live: 5 diagrams x 2 formats = 10 files.

**Worth noting the near-miss**: installing a missing dependency to "unblock the
figures" would, unguarded, have shipped a fabricated figure into the results
tier. The plan had recorded the risk (F12); the guard is what made the recording
useful.

## F14 — EDA promoted, and the pipeline now keeps it in sync

149 artefacts copied to `05_thesis_results/eda/{category}/{tables,plots}/`:

| Category | .md tables | .png plots |
|----------|-----------:|-----------:|
| CSD | 31 | 8 |
| Danskvand | 28 | 7 |
| Energidrikke | 31 | 8 |
| RTD | 29 | 7 |

`.csv` stays at the pipeline per DEC-EDA-SPLIT — later steps consume it.

**Copy, not move**: the pipeline rewrites these on every run, so a move would be
undone next run and would strip the step-adjacent context that makes a plot
diagnosable.

A one-off copy would drift the moment the pipeline reran, so the promotion is now
`promote_eda_artifacts(category)` in `_shared_modules/pipeline_config.py`,
callable at the end of a run. Tested: `CSD -> (31, 8)`.

## F15 — Diagrams now read measured data; five stale claims removed

Every number and model name in the diagrams was a hardcoded literal. They are now
loaded from artefacts at render time (`profiling.csv`, `metrics.csv`,
`models/{cat}/metadata.json`), so a re-run cannot drift from the results.

| Was (invented) | Now (measured) |
|---|---|
| Ridge 15 / ARIMA 20 / Prophet 200 / LightGBM 300 / XGBoost 400 MB | Ridge 5 / LightGBM 38 / XGBoost 29 MB, from `profiling.csv` peak fit RSS |
| 5-model ladder incl. ARIMA + Prophet | 3-model ladder from `metrics.csv` — **Prophet is a statistical baseline, not in the ladder** |
| "≤ 512 MB / model" | "≤ 38 MB peak fit RSS", derived |
| "5 × ModelForecast" | count derived from the ladder |
| MAPE / RMSE | WMAPE / MASE (what SRQ1 actually reports) |

The old RAM figures overstated reality by **4–40×**. Brian's instruction — numbers
must be grounded in recorded pipeline output — is what surfaced it.

### Removed, not relabelled

- **Indeks Danmark** nodes in fig1/fig3/fig6, plus every edge into them, plus the
  orphaned "Consumer Signals (PCA → k-means)" node that derived from the survey.
  An empty placeholder box is worse than no box.
- **LLM-as-Judge** from both Validation Agent blocks and the ValidationReport →
  now "interval calibration" / "split-conformal interval coverage".
- **System B** — roughly half of `project_overview_v1` was the abandoned
  multi-agent *writing* system, labelled "scaffolding — not in thesis" while
  sitting in a thesis figure. Figure is now System A only.
- **`fig4_ram_budget()`** deleted from the generator per Brian; source preserved
  at `diagrams/.archive/fabricated_ram_budget_2026-09/fig4_ram_budget_source.py`.

### Confidence-score figure contradicted the implementation

`confidence_score_v1` showed the third component as "Consumer Signal Alignment
(Indeks Danmark demand index)". `synthesis_summary.md` says the composite is
**30% agreement + 40% interval tightness + 30% model accuracy**. Same weights,
different third term — and the diagram's version cited the dropped dataset.
Corrected to "Model Accuracy / lower historical WMAPE".

### An inconsistency found, not silently resolved

`export_appendix.py` computes budget shares against `RAM_BUDGET_MB = 4096`; the
thesis prose says "8 GB" in eight places. The diagrams now source the exporter's
constant (so diagram and appendix cannot disagree) and the discrepancy is flagged
in-code. **Which is correct is Brian's call** — it changes a claim in Ch6.

### Two bugs the edits exposed

1. `agent_workflow_v1`'s edge chain was hardcoded `ridge→arima→prophet→lgbm→xgb`.
   With arima/prophet gone, graphviz **silently created empty unlabelled nodes**
   for the dangling ids rather than erroring. Chain is now derived from the same
   ladder as the nodes.
2. `index.json` still carried pre-reorganisation `model_file` names. Synced.

## F16 — `fig1_model_ladder` was empty, and its title was false

Brian reported "no line in the chart". It is a bar chart, so no line is expected —
but the bars were **absent**: the filter read `dataset == "brand"` while
`metrics.csv` writes `"bymonth"`. P0035's grain repoint used the wrong tag, so
every bar height was NaN. It failed silently because a NaN bar is a valid
matplotlib call, not an error. Added a guard that refuses to write an empty figure.

Fixing it exposed a second defect: the hardcoded title claimed *"every model beats
SeasonalNaive"*, which the data contradicts — **Ridge loses on RTD, 57.3 vs 54.8
WMAPE**. The title is now derived: *"beats SeasonalNaive except Ridge (RTD)"*.

The claim had been unfalsifiable while the chart was empty. A caption that argues
with its own chart is worse than no caption.

## F17 — Models reorganised per category

`models/{CSD,danskvand,energidrikke,RTD}/{model,metadata}.json`, matching
`05_thesis_results/eda/`. Shared `index.json` and `*_params.json` stay at the root.

Repointing `train_and_persist.py` was not enough: **`forecast_tool.py` — the live
SRQ2 serving tool — read the old flat `{cat}_metadata.json`**. Fixed, with a
legacy fallback so an older persisted tree still loads rather than failing at
serve time. All four categories verified loading.

Served models are XGBoost(tuned) ×3 and LightGBM(tuned) for RTD — not the
"5 models" the diagrams claimed.

## F18 — The diagrams described a system that was never built

Brian: *"we never use a langgraph coordinator for the model training"* and
*"make doubly sure we can prove by the data and code each category and number."*
Checking the live tree against the diagrams:

| Depicted | Verified reality |
|---|---|
| LangGraph / StateGraph orchestration | **not in `requirements.txt`, imported by no live module.** Sole mention is an aspirational docstring line |
| Coordinator, Agent Layer, 4 named Agents | no such objects in any live script |
| Phase 1→2→3→4 approval gates | no approval mechanism exists |
| "Consumer Signals: PCA → k-means" | **no PCA or KMeans call in the repo** |
| ARIMA + Prophet in the ladder | statistical *baselines*, never ladder members |
| Per-model RAM 15/20/200/300/400 MB | invented; measured 5.4 / 29.2 / 38.1 |
| Indeks Danmark source | never used |
| LLM-as-Judge | decided against |
| System B writing agents | abandoned |

**The frame was the error, not the labels.** I patched labels twice before
concluding this, and each pass produced a more accurate description of a system
nobody built. Brian's "AI slop" reaction was diagnosing exactly that: decorative
boxes asserting structure that no code implements.

### What the repo actually does — three sequential stages, no orchestrator

1. **Preprocessing** — `run_preprocessing.py`, steps 0-6, one horizon at a time.
   Verified: CSD panel is 4,370 rows x 54 cols across 95 brands.
2. **Model selection** — each model fitted independently by its own script; the
   lowest test WMAPE per category is persisted. Verified: XGBoost(tuned) for
   CSD/danskvand/energidrikke, LightGBM(tuned) for RTD.
3. **SRQ4 comparison** — three scenarios in `srq4_experiment.py`:
   `A_plain`, `B_data`, `C_model`. Only C loads a trained model. Matches Brian's
   description exactly.

Rebuilt as `pipeline_v2`, `model_selection_v2`, `scenarios_v2`,
`resource_profile_v2`. Every value read from an artefact at render time; the
generator **exits rather than drawing** if a source table is missing. Style is
deliberately plain — one accent colour, no gradients or rounded cards, legible in
greyscale at column width. Old set + generator archived with a README listing
every disproved claim.

### A live break found while verifying

`srq4_experiment.py` loaded Scenario C's tool from
`ROOT/"model_serving_interface"/"scenario_c_forecast"/forecast_tool.py` — removed
in the SRQ restructure. **Scenario C would have raised FileNotFoundError at
import.** Now `SRQ2_DIR / "forecast_tool.py"`, verified resolving.

## F19 — Method correction: build the inventory first, cite second

Brian: *"your whole approach of 'what is already cited in the thesis' is
completely botched up and in reverse."*

He is right, and it invalidates how I framed several decisions. I had been using
"does a chapter cite this?" as the test for whether an artefact deserved to
exist. But the thesis draft is itself provisional — sections are being removed
(the LLM-as-Judge one), and the citation set is an *output* of this work, not an
input to it.

**The correct order:**

1. Make the EDA and modelling pipelines log properly and consume their own logs.
2. Make every table/figure/diagram data-driven and regenerable on demand.
3. *Then* choose what to cite, in-text or as appendix, with the full inventory
   visible.
4. Only then audit the snapshot comments against that inventory.

Where my inverted test led me wrong: I recommended **restoring** the SRQ2 judge
producers *because Table 21 cited them* — when the design had been dropped and
Brian's own review comments flagged that table for removal. Citation is evidence
of the *current draft's* state, not of what the thesis should contain.

This does not change the artefact decisions already made (the zombie, the
fabricated RAM figure, System B) — those rested on code and data, not citations.
It changes the remaining ones: the 18 `analysis/figures*` are decided on whether
they can be regenerated from current data, not on whether a chapter mentions them.

## F20 — Pipeline logging audit (Brian's correct ordering, step 1)

Per F19: make the pipelines log properly and consume their own logs *before*
deciding what to cite. First pass over the EDA/preprocessing pipeline.

### What is healthy

- Console capture is thorough: 11-12 `*_console.log` per category, plus a
  run-level `run_preprocessing_console.log`.
- `{slug}_eda_findings_h{N}.json` is a real machine-readable contract, written
  per horizon and **consumed** by later steps — the one place the pipeline
  genuinely reads its own output.
- Coverage is even across all four categories (2 logs / ~12 consoles / 2
  findings each), so nothing is category-specific.

### Gap 1 — structured step logs stop after step 1

Only `step_0` and `step_1` call `log_step_timing()` and emit
`step_N_log.json`. Steps 2-6 write console text only. So five of seven steps have
no machine-readable record of how long they took or whether they succeeded —
recoverable only by a human reading prose.

### Gap 2 — the orchestrator measured timings and then discarded them

`run_preprocessing.py` already times every step and records status in
`StepResult`/`RunResult` (`time.perf_counter()` around each call, failures
captured with a reason). It then **only printed them**. Its own docstring says
the console log is "the run-level view … which no individual step log contains"
— true, and precisely the problem: the record existed as prose, not data.

Nothing could answer *"when did RTD last run, did every step pass, how long did
step 4 take?"* without opening a log file and reading it.

**Fixed**: added `write_run_manifest()`, called after `print_summary()`. It
persists `run_manifest.json` — per category and horizon, per step number, name,
status, seconds and failure detail, plus an `ok` roll-up and total runtime.
Verified by constructing real `StepResult` objects and round-tripping the JSON,
rather than by inspection: the first draft used `st.reason` and `st.step` as a
string, and both were wrong (`detail`, and `Step` is a dataclass).

This closes the run-level gap without patching five step modules, and it is the
artefact a "pipeline execution" appendix table can be built from — which is the
point of doing this before choosing citations.

### Still open

- Steps 2-6 emit no per-step structured log. The run manifest covers timing and
  status; it does not cover per-step *content* metrics (rows in, rows out,
  columns dropped). Worth adding to `log_step_timing()` calls in each step if an
  appendix wants that granularity.
- No consumer yet reads `run_manifest.json`. It should feed an appendix table
  (`export_appendix.py`) so the pipeline's execution record becomes a thesis
  artefact rather than a debugging aid.

## F21 — `ch5_architecture_v1` rebuilt as `layered_architecture_v2`

The hand-drawn Ch5 SVG had the same defect class as the generated set. Its
three-layer framing was sound and is preserved; six specific claims were not:

| Claimed | Verified |
|---|---|
| 5-model substrate incl. ARIMA + Prophet | both are statistical **baselines**; the ladder is SeasonalNaive/Ridge/LightGBM/XGBoost |
| "human-in-the-loop checkpoints" | no approval mechanism in any live module |
| "Prometheus Graph Engine · LangGraph deployment" | neither is a dependency; imported nowhere |
| "sandbox (e.g. E2B)" | Scenario B uses Anthropic's **hosted Code Interpreter**; E2B appears only in `measure_e2b_cost.py` |
| "≤ 8 GB RAM" | 4096 MB (Brian confirmed) |
| "Lightweight Python coordinator" | no coordinator exists — separate scripts run in sequence |

`layered_architecture_v2` keeps substrate → tool interface → scenarios, and reads
the ladder, the served model per category, measured RAM and the scenario set from
artefacts. The SRQ2 layer now names what `forecast_log.jsonl` actually records
(model, training cutoff, calibration rows, interval method) — real traceability,
verified in the log file, rather than the previous decorative "reliability /
uncertainty / traceability" pills.

## Open questions

1. **SRQ2 restore** (F8) — no longer a restore-*or*-archive question: Table 21
   is in the thesis, so the producers must come back from `.archive/`.
   `srq2_synthesis.py` is free to re-run; `srq2_agent.py` needs API calls.
   Brian's review comments 381/383/384 flag the same section as OUTDATED.
2. **The 18 `analysis/figures*`** (F11) — still needs the Phase 5 citation sweep.
3. **Abstract correction** (F6) — Brian's prose call, in the `.docx`.
4. **`ram_budget_v1` rewire** (F13) — quarantined and guarded; needs the figure
   rebuilt from the real appendix measurements.

---

## F22 — The manifest consumer exposed two bugs in the manifest producer

Writing the reader is what proved the writer wrong. Both bugs were invisible in
the single-category, single-horizon case that had been exercised by hand.

**Bug 1 — every category filed under the first category's folder.** The output
path was `get_paths(results[0].category)`, but `results` spans categories:
`--all-categories` is an advertised flag. A four-category run would have written
RTD's, danskvand's and energidrikke's records into `CSD/pipeline_step_outputs/`,
each overwriting the last. Fixed by grouping runs by category, one manifest each.

**Bug 2 — horizons erased each other.** Horizons are run as separate invocations
(`--horizon 1`, then `--horizon 3`). A plain write meant the second run destroyed
the first run's record, and the appendix would have reported a single horizon as
though it were the whole pipeline. Fixed by merging: horizons not in the current
run are carried forward, horizons in it are replaced. An unreadable prior
manifest is replaced with a notice rather than raised on — losing an old record
is a smaller harm than failing an otherwise-successful pipeline run.

**Both were caught by round-tripping real `RunResult`/`StepResult` objects**, not
by reading the code. This is the second session running where that method caught
something inspection had missed (F20 caught `st.reason` vs `st.detail`).

### The consumer

`table_pipeline_execution()` in `export_appendix.py`. One design choice worth
keeping: **step names are read from the manifest, never held as a list in the
exporter.** A renamed or reordered step therefore cannot leave the appendix
describing a pipeline that no longer exists — the failure mode this whole plan
exists to eliminate.

Framed as a *reproducibility* table, not a performance claim: wall-clock seconds
on one laptop are not a benchmark, they are evidence that the stated pipeline is
the pipeline that ran and that no step was quietly skipped.

Verified end-to-end with a real CSD H=3 run (steps 3-6, 15.7s, all passed).

---

## F23 — The SRQ1 reshape silently halved the appendix

Last session moved SRQ1's loose output into `figures/ tables/ models/` and
repointed the **producers**. It did not repoint the **consumers**.
`export_appendix.py` still read `THESIS_RESULTS_SRQ1_DIR / "profiling.csv"` at
the flat root, where nothing lives any more.

The exporter is deliberately tolerant of missing inputs — "skipped with a notice
rather than crashing, so this is runnable before the paid blocks execute". That
tolerance turned a structural break into six polite notices and **exit code 0**:

    (skip resource profile: profiling.csv absent)
    (skip parameter drift: refit_vs_retune.csv absent)
    (skip baselines: stat_baselines.csv absent)
    ...

25 tables had become 6, and nothing failed. The plan still recorded the generator
as PASS, because it *had* passed — it just produced half an appendix.

**Fixed**: six reads repointed into `tables/`; output went 6 → 12 tables.

**Two lessons, both general.**

1. A move is not complete when the producers are repointed. Grep for *readers* of
   every path that moved. Producers are easy to find because they are what you
   just edited; consumers are somewhere else entirely.
2. **Skip-on-missing hides structural breaks.** It is the right behaviour for a
   half-run experiment and the wrong behaviour for a moved directory, and the
   code cannot tell the two apart. Phase 6's "every tier-05 artefact has a live
   producer" check should be inverted as well: *every producer's declared inputs
   should exist, or the run should say so loudly at the end* — a summary line
   like "12 written, 6 skipped" would have made this obvious immediately.

The full appendix is **22 tables** across three producers (12 + 4 + 6), all
verified regenerating on 2026-09-07, zero orphaned files in the output directory.

---

## F24 — The appendix numbered by generation order but never cleaned up

Surfaced immediately by F23's fix. `_emit()` names files `NN_slug` where `NN` is
a running counter, so **the prefix is generation order, not identity**: if one
table's input is missing, every later table shifts up one.

Nothing deleted the previous run's files. Across three runs in one session
(6 tables, then 12, then 13) the directory accumulated **29 files for 13 tables**,
with three different tables all named `02_`:

    02_pipeline_execution.md
    02_scenario_comparison.md
    02_substrate_resource_profile.md

An examiner tracing a number to `02_` would find three answers. Worse, the stale
copies are *plausible* — they are real tables from a real run, just superseded,
so nothing about their content reveals that they are debris.

**Fixed** by clearing this exporter's own output at the start of `main()`.

The scoping is the interesting part. Three different producers write into
`05_thesis_results/appendix/`:

| Producer | Block |
|----------|-------|
| `export_appendix.py` | 01-13 |
| `export_holiday_appendix.py` | 90-93 |
| `srq1_export_enrichment_appendix.py` | 94-99 |

So "clear the directory" would have silently destroyed the other two producers'
output. `_clear_previous(prefix_max=89)` removes only files in its own block —
the 90-99 block is verified surviving after the change.

**The general lesson**: a generated directory needs exactly one owner per file,
and a regenerating writer must clean what it previously wrote, or "regenerable"
degrades into "accumulates". This is worth adding to Phase 6's invariant checks:
*no two files in a generated directory share an identity prefix.*

Final state: **23 tables**, every one a matched `.md`/`.csv` pair, no orphans,
no duplicate prefixes, all three producers verified regenerating.

---

## F25 — Content metrics, extracted from what the steps already return

The manifest recorded that a step ran and how long it took. That evidences
execution but not *content*: a step that keeps 38 brands and one that silently
collapses to 4 produce identical timing logs, and a collapsed row count is the
failure most likely to invalidate a downstream result.

**Every step already returned the answer.** Step 1 returns the aggregated panel,
step 3 the measured contract (including its `retention` block), step 4 the
feature matrix, step 6 a manifest carrying `shape` with rows/columns/brands/
n_features. The orchestrator was discarding all of it except step 2's failure
list.

So `_step_metrics()` extracts centrally rather than instrumenting seven step
modules. This is the important design point: **there is no second code path to
keep in sync.** Instrumentation added inside each step could drift from what the
step actually computes; reading the returned object cannot. Unknown shapes yield
`{}` and any exception is swallowed into `metrics_error` — a summary must never
fail a pipeline run.

Metrics land in three places: the `StepResult`, the manifest JSON, and one
compact console line per step, so a collapse is visible without opening a file.

**Appendix**: a SECOND table, `table_pipeline_data_reduction`, deliberately not
extra columns on the execution table. That table's unit is seconds; this one's is
rows and brands. One row carrying both invites comparison down a column of unlike
quantities — the same reasoning that keeps `parameter_drift` separate from the
merged resource table (F-earlier).

Verified across all seven branches with real-shaped objects before running.

---

## F26 — The modelling layer has almost no run provenance

Audit of `01_SRQ1_Model_Training/02_thesis_modelling/model_training/` (21 live
scripts), asking the same question the preprocessing audit asked: does a script
record *how it was run*, or only what it produced?

**2 of 21 scripts write any provenance at all** (`generated_utc`, `generated_by`,
a timestamp, or a git ref). The result CSVs carry data columns only:

    metrics.csv    dataset,category,model,mape_mean,mape_median,wmape,n_train,n_test,n_series
    profiling.csv  model,fit_s,predict_ms,peak_fit_RSS_MB,...,n_train,n_features

Nothing in either says when it was produced, by which script, or against which
input. An examiner asking "is this metrics table current with the feature matrix
that shipped?" cannot answer it from the artefact.

**The good pattern already exists**, in exactly one place. `train_and_persist.py`
writes a per-category `metadata.json` recording model, hyperparameters, seed,
feature list, training window, calibration window and rows, interval method, test
window, train seconds, peak RAM, and `trained_at_utc`. That is a complete
provenance record — it answers every question the preprocessing manifest was
built to answer, and it was already there.

**Recommendation (not yet done, scoped for the next session).** Do NOT
instrument 19 scripts. The cheap, high-value version is a single shared helper
that stamps three fields — `generated_utc`, `generated_by`, and the input file's
mtime/hash — onto every results CSV as it is written, plus one `models/index.json`
roll-up. Most of these scripts write through a small number of save paths, so the
change is likely to be a handful of call sites rather than 19 edits. Confirm that
before starting.

**Priority judgement**: this is real, but it is provenance for *our own* audit
trail, not a blocker on any figure or table currently destined for the thesis.
Every artefact in `05_thesis_results/` has a verified live producer, which is the
property P0046 set out to establish. With 8 days to submission this ranks below
Phases 4-6.

---

## F27 — Phase 4 + the five requested chapter figures

Brian's instruction (2026-09-07): **generate everything programmatically**; he
may still redraw individual figures by hand afterwards. That settles the
outstanding `ch2_gap_diagram` question — rebuild, do not adopt.

Six new figures in `generate_architecture_diagrams.py`, plus one table generator:

| Figure | Chapter | Where its facts come from |
|--------|---------|---------------------------|
| `ch1_research_questions_tree_v2` | 1 | current RQ set (the hand-drawn one showed a superseded set) |
| `ch2_gap_diagram_v2` | 2 | §2.7's four literatures; envelope from `RAM_BUDGET_MB` |
| `ch4_data_pipeline_v1` | 4 opening | every count from each category's `step_4_log_h3.json` |
| `ch4_eda_pipeline_csd_v1` | 4 middle | section names read from the tables the EDA wrote |
| `ch6_modelling_pipeline_v1` | 6 | ladder from `metrics.csv`, RAM from `profiling.csv`, winners from each `metadata.json`, arms from `pooled_metrics.csv` |
| `ch5_tool_interface_v1` | 5 | field names from a persisted model's metadata |

### Three claims corrected against the code

1. **`ch2_gap_diagram` said 8 GB.** It is 4096 MB. Now read from the same
   constant every other diagram uses.
2. **Ch5's figure caption claimed "five lightweight models", "human-in-the-loop
   checkpoints" and a bounded agentic layer.** The ladder is four; the other two
   do not exist in any live module. Caption rewritten, correction noted inline.
3. **"18 EDA section groups"** — written from a directory listing. Counting them
   gives **16**; the numbered prefixes have gaps. Now counted, not asserted.

### Pooled vs per-category is genuinely split — say so

`pooled_metrics.csv` shows per-category training winning in **2 of 4** categories
(CSD, RTD) and pooled winning in the other two. The first draft of the label said
"per-category training wins in 2 of 4", which is true but reads as a direction.
It now states the split and names which categories fall each way. A figure should
not imply a result the numbers do not support.

**A scale trap worth remembering**: `metrics.csv` and `pooled_metrics.csv` store
WMAPE **as a percentage** (17.5 = 17.5%), while `retune_single_cutoff.csv` stores
it **as a fraction** (0.1257). Multiplying the first by 100 produces a plausible
1750%. The exporter's existing `*100` is correct for the file it reads. Check the
scale per file; do not assume it across the tier.

### Layout

Three figures were re-laid-out after looking at them, not after generating them:
the data pipeline ran ~1800px wide (unreadable at 6.5in), the modelling diagram's
orthogonal router drove dashed edges through the ladder cluster and left
SeasonalNaive apparently unconnected, and the tool interface put the caller
*below* the response it receives. Fixed with rankdir, `splines=polyline`,
cluster-level edges (`lhead`/`ltail` + `compound`), and `constraint=false` on the
return edge.

---

## F28 — The literature table is the one artefact with two provenances

`generate_literature_table.py` (new). Ch2 has no machine-readable
literature-to-design mapping — the links live in the prose. So the table has two
halves, and the script marks the boundary rather than blurring it:

* **Parsed** from `ch2-literature-review.md`: section titles, the `*Maps to ...*`
  SRQ mapping, and the `**Claims**` bullets. These cannot drift.
* **Curated** in the script: what each strand changed in the build. The test
  applied when writing each one — *if it cannot name something openable in the
  repository, it does not belong in the table.*

The review note says which column is which, and the script **warns** when a
parsed section has no design consequence recorded. That warning fired
immediately for §2.0 and §2.9 — correctly, since they are the chapter's
introduction and transition rather than literature strands, and are now excluded.

Parsing bug worth noting: claim bullets wrap across lines, so reading line-by-line
cut claims mid-sentence AND left a stray `**` where a bold span opened on one
line and closed on the next. Continuation lines are now joined before markup is
stripped.

---

## F29 — Block collision: one producer was deleting another's output

F24's `_clear_previous()` cleared prefixes `<= 89`. The new literature table
writes `89_`. So running `generate_literature_table.py` *before*
`export_appendix.py` silently deleted it — and the deleting run reports success.

It survived this session only because of the order I happened to run them in.

Fixed by lowering the bound to 88 and, more importantly, **writing the block
allocation into the docstring** so the next producer added to this directory has
somewhere to look:

    01-49   export_appendix.py            <- cleared by that script
    89      generate_literature_table.py
    90-93   export_holiday_appendix.py
    94-99   srq1_export_enrichment_appendix.py

Verified by running in the dangerous order and confirming survival.

**The general point, and it is the same one as F24**: a shared output directory
needs one owner per file *and a written record of who owns what*. A cleanup step
scoped by a magic number is correct exactly until someone adds a producer, and
nothing will tell them.
