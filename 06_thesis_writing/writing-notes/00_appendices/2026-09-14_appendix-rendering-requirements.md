---
progress_note: |
  IMPLEMENTATION STATUS as of 2026-09-14 evening. The contract below is
  unchanged; this records what has been built against it.

  DONE
    - Cambria 9pt, white ground, left alignment throughout
    - Per-side borders: header bottom-rule, first column right-rule, last row
      underline, grey top/bottom rules for row groups. Verified rendering.
    - The `***` bug fixed at source: _bold_best no longer writes Markdown
      emphasis into the shared frame; each renderer applies its own.
    - Table SVGs write to tables/, not figures/. Writers redirected.
    - get_chapter_plots_dir() and get_chapter_source_md_dir() added to PATHS.
    - Ch1 tree folded 2x2: 3.53 -> 1.56. Main question condensed.
    - Ch3 DSR title shortened; its SRQ parser rewritten against the new
      subsection headings (the chapter changed shape, not the parser).
    - h1/ archived. Model-metadata table added. Abbreviated raw-response JSON
      written to ch8_experiment/figures/.
    - Abbreviations: wMAPE/mMAPE, mWMAPE/sdWMAPE/medCV, scenario letters on
      the per-run record and outcome taxonomy -- each with its key in the note.
    - Per-run record split into two parts.
    - _clear_previous now clears .svg, which was the cause of four rounds of
      orphaned files as sequence numbers shifted.

  NOT DONE -- next session. Ordered: the border fix first, because it
  propagates through every table and every other change is cosmetic beside it.
    1. G5 border fix. An empty SIDES is the graphviz DEFAULT (all four sides),
       not "none" -- probed and confirmed 2026-09-14. No code path may emit
       SIDES="". Then G6 (legend/note rectangle) falls out of the same fix.
    2. Colour semantics: Green=Good / Yellow=Runner-up / Red=Bad, with a
       DIRECTION per measure. Training Rows and Features are more=better and
       are currently inverted. "_ALL_LOWER" is wrong for any table with counts.
    3. Remove colour from 09_parameter_drift; rank 10_statistical_baselines
       within category and sort by it; add colour to 13 and to every row of 14.
    4. R12: why F and G score 0 of 9 on interval_faithful. A and B are the
       intended finding; F and G are tool-backed and are not explained.
    5. R1: the EDA figure count globs *.png in an SVG-only tree.
    6. G7: captions under-fill the width on wide figures.
    7. R5 metric dictionary two-page split; R17 brand grouping; R18 the new
       scenario-input table; R14 archive the .html.
    8. R4/R8: the Danskvand 12-measure and ARIMA/Prophet 24-row anomalies --
       both are data questions surfaced BY correct rendering.
    - Still open from before: EDA table SVGs and .source_md per chapter;
      Ch2 gap diagram and Ch5 fig1_model_ladder verification; Ch9/Ch10.
    - Several tables still exceed 482pt in height; the cause is note and
      caption chrome, not row count, and cutting notes is what moves it.

  KNOWN DECISION, recorded rather than fixed
    - ch4_preprocessing_pipeline_v2 stays at ratio 4.17. Four attempts to
      bring it under the cap are documented in the source: a left-to-right
      chain is as wide as its node count, deleting a node made the ratio
      WORSE, and same-rank folds do not move nodes to a lower rank. A wide
      short flow diagram is the honest shape for a linear pipeline.

name: 2026-09-14_appendix-rendering-requirements
description: NOTE - Consolidated requirements for every generated appendix artefact. Page geometry, table styling contract, folder layout, and the full per-artefact defect list from Brian's 2026-09-14 review. Diffed against on each pass; updated as comments arrive.
category: reference
applies-to: [05_thesis_results, styled_tables.py, export_appendix.py, generate_architecture_diagrams.py, all appendix producers]
triggers: [rendering an appendix table, styling a figure, checking whether an artefact fits the page, adding a producer]
created: 2026_09_14-17_30
updated: 2026_09_15-00_30
status: contract current as of Brian's 2026-09-14 evening review; border fix (G5/F37) is the next implementation step
---

# Appendix rendering requirements

Consolidated from Brian's review of 2026-09-14. **This file is the contract.**
Each pass diffs against it; new comments are folded in rather than appended
loosely, so the list stays sorted by subject rather than by when it was said.

---

# 1. Page geometry — the hard constraint

The appendix is **A4 landscape** with custom margins.

| | |
|---|---|
| Page | 29.7 x 21.0 cm |
| Margins | top 2, bottom 2, left 1, right 1 cm |
| **Usable text block** | **27.7 x 17.0 cm** |
| In points | **785 x 482 pt** |
| **Target aspect ratio** | **1.63** |

**This supersedes the 3.6 cap used until now**, which came from the portrait
figure rule and was never right for appendix tables.

**The rule is a ceiling, not a target.** Nothing may exceed 1.63, because
anything wider must be scaled down and becomes unreadable. A narrow table stays
narrow: stretching a four-column lookup to fill the width adds whitespace, not
information.

A table taller than 482 pt does not fit and must be split across pages.

---

# 2. Table styling contract

## Typography

| Property | Value |
|---|---|
| Font | **Cambria** |
| Size | **9 pt** |
| Alignment | **left**, in every cell and every header |

**Why Cambria and not Times New Roman.** The Times files are present in Windows,
but Graphviz ships its own text stack and never sees them: it falls back to a
sans face for *metrics* while the SVG still carries `font-family="Times New
Roman"`, so the text would display in Times while every column width and line
break was computed in the wrong font. Cambria loads cleanly, is a Microsoft
serif designed for body text, and at 9 pt measures slightly narrower than Times
(189 vs 219 on the same string), which helps the wide tables.

**Semi-bold does not exist in this toolchain.** Tested: "Cambria Semibold"
renders identically to "Cambria Bold", and a deliberately invented font name
renders the same way — the font matcher maps anything unrecognised to a bold
default. So there are two weights, regular and bold, and contrast between the
header and the first column comes from the **borders**, not a third weight.

## Colour

Background is **white** throughout. No grey header band, no row shading for
decoration. Shading is reserved for meaning (see grouping, below).

## Borders — selective, forming an "H" shape

| Element | Border | Colour |
|---|---|---|
| Header row | **bottom only** | `#000000` |
| First column | **right only** | `#000000` |
| Last column, if a total or summary | **left only** | `#000000` |
| Last column, if ordinary | none | — |
| Last row, if ordinary | **bottom only** | `#000000` |
| Last row, if a total or summary | **top and bottom** | `#000000` |
| Row-group separators | **top and bottom** | `#d0d0d0` |

No cell has a border on any side not listed.

### The border bug — diagnosed 2026-09-14, not yet fixed

Brian: *"the cell borders of the content are messed up again"*, on
`05_model_metadata`, `12_scenario_comparison` and `15_per_run_record_p1`, with
the hypothesis that **the order of border application is wrong** — that content
is formatted, then the header row, then the first and last column, and a later
step overwrites an earlier one.

**The order is not the mechanism.** Probed directly:

```
CELLBORDER="1" + SIDES=""              -> a full box     (the bug)
CELLBORDER="1" + SIDES="none" / " "    -> a full box
CELLBORDER="0" on the table            -> nothing draws, SIDES ignored entirely
CELLBORDER="1" + BORDER="0" on a cell  -> nothing draws  <-- the fix
```

An **empty `SIDES` falls back to the graphviz default of all four sides.** It
does not mean "no border". So every interior body cell — one that is not in a
group boundary, not the first column, not the last row — asked for nothing and
was drawn as a full box, which is exactly the grid this styling exists to
remove. Header cells always carry `bottom`, so they emit a single-sided
`<polyline>` and look correct; that contrast is the visible symptom, and it is
what made an ordering bug the natural hypothesis.

The earlier claim in this file that "an explicitly empty side suppresses the
default" was **wrong**, and is the reason the defect shipped.

### How to measure this, because the obvious way is wrong

A graphviz SVG emits a `<polygon>` for the **graph background** and another for
**every cell carrying a `BGCOLOR`** — all of them `stroke="none"`. A drawn
border is a `<polyline>`. Counting raw `<polygon>` elements therefore measures
cell fills, not borders, and produced two wrong readings before this was caught
(see F37):

```python
stroked = [x for x in re.findall(r'<polygon[^>]*>', svg)
           if 'stroke="none"' not in x]        # genuine boxes
rules   = re.findall(r'<polyline[^>]*>', svg)  # single-sided rules
```

**The fix, as implemented**: "no border" is a property of the **cell** —
`BORDER="0"` — not of an empty `SIDES`. The table keeps `CELLBORDER="1"` so
that cells which *do* carry a rule still draw it, and the two compose: a
sibling cell in the same row renders its own `SIDES="B"` normally. One helper,
`styled_tables._border_attrs`, is the only place allowed to turn a sides string
into markup, so **no code path can emit `SIDES=""`** by construction.

`CELLBORDER="0"` on the table was the other candidate and was rejected: it
makes `SIDES` inert everywhere, so every rule would have to be drawn as its own
single-sided cell.

**Verified after the fix**: all 17 tables regenerated with **0 stroked polygons
and their rules intact**. `17_run_configuration` (8 rows x 2 columns) emits 11
polylines = 2 header bottoms + 8 first-column rights + 1 last-row bottom —
exactly the "H". G5 and G6 are closed.

### Ordering, which is a separate and real requirement

Brian, on the section rules: *"The section wise cell borders would need to be
the last step."* So once the per-side emission is fixed, precedence is:

1. body cell defaults (no border)
2. header row
3. first column, and last column where it is a total
4. last row
5. **row-group rules last**, so a group boundary is never overwritten

## Weight

- Header row: **bold**
- First column: **bold**
- Last column and last row: **bold only when they are totals or summaries**
- Everything else: regular

## Semantic highlighting — only where it means something

| Meaning | Encoding |
|---|---|
| Best across all scenarios | green fill, green text, bold + underline |
| Second best | amber fill, amber text, bold |
| Criterion not met | red fill, red text |

Applied **case by case**. A lookup table has no winner, and colouring one would
assert a comparison the table does not make. The overarching design stays
identical across every table regardless; only the highlighting is conditional.

### The colour means quality, not magnitude

Brian, 2026-09-14: *"Green = Good, Yellow = Runner Up (good), Red = Bad. That
meaning changes depending on the variable."*

The defect: `05_model_metadata` coloured **Training Rows** so that *fewer* rows
read as green. Fewer training rows is worse, not better. Likewise **Features**
— more is better there.

So a ranked column carries a **direction**, and the direction is a property of
the measure:

| Direction | Measures |
|---|---|
| lower is better | error (WMAPE, MAPE, APE), time, memory, cost, drift, variability |
| **higher is better** | **training rows, feature count**, coverage, counts of runs that succeeded, agreement, replicability |

`_RANKED`'s `"_ALL_LOWER"` sentinel is therefore **wrong for any table holding a
count**, because it asserts one direction over every row. `05_model_metadata`
needs per-row directions, not the sentinel.

### Where colour is added, and where it is removed

| Table | Change |
|---|---|
| `09_parameter_drift` | **remove colour entirely.** Drift across a refit is not a contest between models |
| `10_statistical_baselines` | rank **row-to-row within a category**, not across the whole table; and **sort by category** so wMAPE and mMAPE group together |
| `13_outcome_taxonomy` | **add** colour coding |
| `14_interval_communication` | **add** colour to every criterion row, not only the mean row it has now |

### One metric vocabulary across the benchmark tables

Brian: *"why do parameter drift and statistical baselines use only
WMAPE/mMAPE while seed stability uses medCV/sdWMAPE/mWMAPE — I believe the seed
stability is the actual correct way."*

Open, and a real inconsistency: three tables about the same models report
different measures, so a reader cannot compare across them. Seed stability's
set is the richer one because it reports a centre **and** a spread. Resolve by
deciding one vocabulary and applying it, rather than per-table choices.

## Row grouping

Where rows fall into meaningful bands, separate them with the light-grey
top/bottom rules. Two worked examples Brian gave:

- **Scenario comparison, by capability:** A (reference) | B, C, F | D, E, G
- **Scenario comparison, by measure type:** Runs and usable answers (runs) |
  median and mean APE (performance) | consistency, replicability, top-answer
  agreement (consistency) | tokens, reasoning tokens, cost (cost) |
  response time (latency)

---

# 3. Folder layout

Every results chapter folder carries only these subfolders:

```
05_thesis_results/{NN}_{chapter}/
  tables/       .md, .csv and the .svg render of each table
  plots/        charts and graphs (matplotlib output)
  figures/      diagrams only — flowcharts, conceptual figures
  .source_md/   source values behind each rendered artefact
  .archive/     superseded
```

**A table rendered as SVG belongs in `tables/`, not `figures/`.** Figures are
flowcharts and conceptualisations. This was wrong across the whole tree and is
being corrected.

**The writers must point at the new locations**, not just the files moved, or
the next regeneration puts them back.

`.source_md/` and `.archive/` are **excluded from the submission export**. The
source files exist so an AI agent has machine-readable numbers behind each
artefact, since image analysis is unreliable.

---

# 4. Per-artefact defects and requests

## Global

| # | Item |
|---|---|
| G1 | ~~Bold and italic render as literal `***`~~ — **fixed**. `_bold_best()` no longer writes Markdown emphasis into the shared frame |
| G2 | Note text boxes are mostly under-filled, making them needlessly tall. `10_seed_stability` is the one that looks right |
| G3 | Notes and descriptions run too long on several tables |
| G4 | Prefer wide format throughout — the appendix is landscape |
| **G5** | **Interior cell borders draw a full grid.** Root cause and fix in §2 — an empty `SIDES` is the graphviz default, not "none". Propagates through every table |
| **G6** | **The legend block and the note block draw a rectangle border along their top**, where the contract asks for a single separating line. Both sit inside the outer `CELLBORDER="1"` table and inherit its default the same way G5 does |
| **G7** | **Figure captions do not fill the available width** — several read as "too vertical", a narrow column of text under a wide drawing. The `_caption` wrap is 68 characters and `_CAPTION_WRAP` is 78; both are tuned to stop a long caption stretching a *small* figure, and they now under-fill a wide one. The wrap should follow the drawing's width rather than a constant. Named by Brian on `ch4_eda_pipeline_csd_v1` and `ch4_raw_schema_v1`, and visible on others |

## Terminology — what the thesis distinguishes

Brian: *"in the thesis written document we do not differentiate between figures
and plots. Only between tables, figures, and appendix."*

`plots/` and `figures/` is a **repository** distinction, kept because a chart
and a flowchart are regenerated by different code. In the document there are
tables and figures, and a plot is a figure. Any count printed **inside** an
artefact must therefore say "figures" and include the plots.

## Chapter 1 — Introduction

| # | Item |
|---|---|
| 1.1 | `ch1_research_questions_tree_v2`: **chapter mapping is stale.** Verified against the current snapshot: prose says SRQ1 is benchmarked in Chapter 5; the figure says Chapter 6. SRQ2 and SRQ3 also disagree |
| 1.2 | Main research question text is too long. Condense while keeping the content |

## Chapter 2 — Literature review

| # | Item |
|---|---|
| 2.1 | `ch2_gap_diagram_v2`: verify the content against the prose |
| 2.2 | `89_literature_design_map`: needs an SVG render and verification |

## Chapter 3 — Methodology

| # | Item |
|---|---|
| 3.1 | `ch3_methodology_design_v1`: verify the content |
| 3.2 | The DSR box title is too long, which forces its inner boxes excessively wide. Shorten to "The DSR Process (Peffers et al., 2007)". The rest of the figure is good |

## Chapter 4 — Data assessment

| # | Item |
|---|---|
| 4.1 | All tables need SVG renders |
| 4.2 | `04_feature_matrix`, `02_pipeline_execution`, `03_pipeline_data_reduction` are in `figures/` and belong in `tables/` |
| 4.3 | Every EDA category's `tables/` subfolder needs SVG renders |
| 4.4 | Every EDA `plots/` folder needs a `.source_md/` sibling holding the numbers behind each chart. Highest value for the distribution histograms, the ACF/PACF plots, and especially the correlation heatmap |

## Chapter 5 — Model benchmark

| # | Item |
|---|---|
| 5.1 | **No rendered tables at all** in `05_model_benchmark/tables` |
| 5.2 | Six table SVGs sit in `figures/` and belong in `tables/` |
| 5.3 | `ch5_resource_profile_v2`, `fig1_model_ladder`, `fig3_forecast_overlay`, `shap_importance` belong in `plots/` |
| 5.4 | `h1/` is a stale artefact from the abolished h1 horizon. Two files dated 2026-09-07. Investigate and archive |
| 5.5 | `01_metric_dictionary`: definitions are too dense against a narrow column while the metric column is too wide with no breaks. Rebalance |
| 5.6 | `05_substrate_resource_profile`: failed bolding (`***` around Ridge); note under-fills its box |
| 5.7 | `06_retraining_cost`: note under-fills its box |
| 5.8 | `08_parameter_drift`: note box, failed highlighting |
| 5.9 | `09_statistical_baselines`: abbreviate to `wMAPE (%)` and `mMAPE (%)` |
| 5.10 | `10_seed_stability`: measure names too long and repetitive. Abbreviate in the table, map them in the note — e.g. `mWMAPE (%)` with "mWMAPE (%) = Mean WMAPE across seeds in %". Failed highlighting. **Note box is correct here** — use as the reference |
| 5.11 | `fig1_model_ladder`: shows Test WMAPE but not mean or median WMAPE — include both. Also missing models: should be five plus SeasonalNaive. Verify |
| 5.12 | `models/{category}/metadata.json`: add an SVG table recording model metadata, one per category |

## Chapter 7 — Decision synthesis

| # | Item |
|---|---|
| 7.1 | `13_interval_communication` belongs in `tables/`; note box under-fills |
| 7.2 | `synthesis_summary.md` needs an SVG render and belongs in `tables/` |

## Chapter 8 — Experimental evaluation

| # | Item |
|---|---|
| 8.1 | Five table SVGs belong in `tables/` |
| 8.2 | `ch8_scenario_comparison.html` — archive, it is an HTML artefact |
| 8.3 | All `tables/` need SVG renders |
| 8.4 | `interval_communication.csv/.md` and `runs.csv` need renders |
| 8.5 | `11_scenario_comparison`: note box |
| 8.6 | `12_outcome_taxonomy`: note box, and colour highlighting would help |
| 8.7 | `14_per_run_record`: too many rows. **Split into two SVGs**, each with an extra header row above the existing one reading "Title — Page 1/2", so both halves sit side by side on one appendix page |
| 8.8 | Take one raw response (`B_llm_data__CSD_HARBOE__rep0.json`) and produce an abbreviated JSON into the Ch8 writing-notes figures folder. Abbreviate repeated elements (show one code block, then "[...] (Abbreviated: 10 other code_blocks)"), and abbreviate long strings to first and last ten words with a count of what was omitted. State the abbreviation methodology clearly at the top or bottom |

## Chapters 9 and 10

| # | Item |
|---|---|
| 9.1 | `09_discussion` could benefit from a rendered figure or table, derived from prose and codebase |
| 10.1 | `10_conclusion` likewise |

---

# 4b. The 2026-09-14 evening review — per artefact

Sequence numbers shifted this session as tables were added, so these are the
**current** filenames.

## Chapter 4

| # | Item |
|---|---|
| R1 | `ch4_eda_pipeline_csd_v1`: **"0 figures" is a live bug, diagnosed.** `generate_architecture_diagrams.py:941` counts `pdir.glob("*.png")`, but DEC-SVG-ONLY made the whole tree SVG — so the glob can never match, and the eight CSD plots are invisible to it. Not a mis-pointed path: a stale extension. Count `*.svg`, and call them figures (see Terminology) |
| R2 | `ch4_eda_pipeline_csd_v1`: caption does not use the full width (G7) |
| R3 | `ch4_raw_schema_v1`: description too narrow (G7) |
| R4 | `ch4_raw_schema_v1`: **why does Danskvand show 12 measures against 29, 29 and 28?** Read from the raw extract itself by `_read_raw_schema()`, so the figure is reporting the source truthfully and the anomaly is in the *data*, not the drawing. Establish whether the Danskvand view genuinely carries fewer measures or the extract is partial — then say which in the figure, because an unexplained 12 beside three 29s reads as a rendering fault |

## Chapter 5

| # | Item |
|---|---|
| R5 | `01_metric_dictionary`: **split across two pages.** Too tall for the 482pt block. Also rebalance the 382-character Definition column |
| R6 | `05_model_metadata`: cell borders (G5); legend and note rectangle (G6) |
| R7 | `05_model_metadata`: **colour direction is inverted on Training Rows** — fewer rows is shown as green. Also Features: more is better. See "The colour means quality, not magnitude" |
| R8 | `05_model_metadata`: **why do ARIMA and Prophet show 24 training rows?** Confirm whether that is the real per-series length or a column reporting something else |
| R9 | `09_parameter_drift`: **remove the colour coding** |
| R10 | `10_statistical_baselines`: rank row-to-row **within** a category; **sort by category** so wMAPE and mMAPE group |
| R11 | Metric vocabulary differs across `09`, `10` and `11` — seed stability's is the right shape. See §2 |

## Chapter 7

| # | Item |
|---|---|
| R12 | `14_interval_communication`: **"Range matches the tool output" is 0 of 9 for A, B, D, F and G. Investigated — it is NOT a wording-match failure.** Every one of the 63 runs has `states_interval = True`, so a range *is* always stated. Criterion 2 additionally requires the payload the tool returned, and `_payload_for_record()` returns empty unless `trace.payload_complete` is set — so a run with no payload fails by construction. For **A and B** that is the intended finding: no tool, nothing to check against. **D, F and G are the open question** — F and G are tool-backed arms by name and still score 0 of 9. Determine whether the payload was never logged complete, or the recompute guard rejected it. That decides whether the Ch7 note is about the artefact or about the harness |
| R13 | `14_interval_communication`: add colour to every criterion row (§2) |

## Chapter 8

| # | Item |
|---|---|
| R14 | `ch8_scenario_comparison.html` **still exists and must go** — the format is SVG. `render_scenario_comparison_formats.py` is the producer; retire or archive both |
| R15 | `12_scenario_comparison`: cell borders (G5). Section rules applied **last** (§2) |
| R16 | `13_outcome_taxonomy`: add colour coding |
| R17 | `15_per_run_record_p1`: **the split works well.** Cell borders (G5); **brand grouping is not visible** — add the row-group rules |
| R18 | New table from `scenario_inputs/CSD__HARBOE.csv`: **transposed**, three sample rows, possibly split in two |

---

# 5. Standing principles

- Every artefact regenerates from real outputs. No typed values, ever.
- The SVG and the Markdown carry the same note; neither may silently drop a
  caveat the other states.
- Numbering is Word's job. Filename prefixes order the directory only.
- A producer that cannot draw must say so, never degrade silently.
