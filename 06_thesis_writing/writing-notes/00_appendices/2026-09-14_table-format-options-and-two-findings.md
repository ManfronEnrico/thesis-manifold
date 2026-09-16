---
name: 2026-09-14_table-format-options-and-two-findings
description: NOTE - Answers three questions from the 2026-09-14 figure review. Why the interval table shows zeros, why the substrate figure listed four models when the thesis names five, and what the options are for richer table formatting than Markdown allows.
category: reference
applies-to: [appendix, ch5_model_benchmark, ch6_architecture, ch7_synthesis]
triggers: [table formatting, SVG tables, interval communication zeros, substrate model count, advanced highlighting]
created: 2026_09_14-12_30
updated: 2026_09_14-12_30
snapshot: 2026-09-14_11-55_ch9-followup-defence-and-anchoring
status: two findings + one prototype, awaiting a decision on scope
---

# Three answers from the figure review

---

# 1. The interval table's zeros do not mean "no range was stated"

**The question.** In `13_interval_communication.md`, five of seven scenarios
score 0 on *"Range matches the tool output"*. Did they communicate no range?

**No. Every scenario stated a range in all nine runs.** Measured across the 63
funded responses:

| Scenario | States a range | Range matches the tool |
|---|---|---|
| A_llm_plain | 9 | 0 |
| B_llm_data | 9 | 0 |
| C_llm_model | 9 | **9** |
| D_prometheus_data | 9 | 0 |
| E_prometheus_model | 9 | **9** |
| F_llm_data_model | 9 | 0 |
| G_prometheus_data_model | 9 | 0 |

The first criterion is 100% everywhere. The second asks something stricter:
**do the stated bounds match the numbers the forecasting tool actually
returned**, within a five per cent tolerance.

**Why that distinction is the whole point of the criterion.** It is the ANAH
principle from §2.5 applied to the interval: a generated statement is assessable
only against an explicitly retrieved source. A scenario with no tool access can
state a perfectly reasonable-looking range, and nothing in the answer ties it to
anything. The criterion catches an agent reporting a plausible but invented
range — which is exactly what A, B and D do.

**F and G are the interesting rows.** Both *had* the forecast tool, and both
still scored 0. They were given the tool's output and stated a different range
anyway. That is a finding about the combined scenarios, not a scoring artefact:
handed both a sandbox and a model, the agent did not carry the model's interval
through.

**Recommendation.** The label is accurate but invites the misreading Brian just
made, and an examiner will make it too. Two options:

1. **Rename the criterion** to something like *"Range traceable to the tool
   output"*, which says that the failure is a broken link rather than a missing
   range.
2. **Keep the label, add one sentence to the note** stating that all scenarios
   stated a range and the criterion tests correspondence.

My view: **do both.** The rename is one string in
`score_interval_communication.py:188`, and the F/G result deserves a sentence in
Chapter 7 §7.4 regardless.

---

# 2. The substrate figure was listing the wrong four models — FIXED

**The question.** Figure 2's forecasting substrate showed four models, one of
them SeasonalNaive. Were there not more?

**Yes. The thesis names five, and the figure showed four — the wrong four.**

| | |
|---|---|
| Ch6 §6.3 says | *"The substrate comprises five lightweight model families… ARIMA and Prophet as classical statistical methods, LightGBM and XGBoost as gradient-boosted ensembles, and Ridge regression as a regularised linear baseline. Five are benchmarked"* |
| Ch5 §5.2 has subsections for | simple benchmarks, ARIMA, Prophet, LightGBM, XGBoost, Ridge |
| The figure drew | SeasonalNaive, Ridge, LightGBM, XGBoost |

So it **omitted ARIMA and Prophet** — the two classical methods — and **included
SeasonalNaive**, which §5.2.1 defines as one of four parameter-free benchmarks a
learned model must beat, not a substrate candidate. The figure asserted the
thesis deploys a naive forecaster as a candidate model.

**Cause.** The figure called `ladder()`, which reads `metrics.csv`. That file
holds only the tabular arm. The statistical arm — ARIMA, Prophet and the
parameter-free floors — lands in `stat_baselines.csv`, which the figure never
read. Neither file alone holds the five.

**Fix.** A new `substrate()` helper reads **both** tables, subtracts the four
parameter-free benchmarks and the `Ridge(unclipped)` diagnostic variant, and
returns the five in the order Ch5 §5.2 presents them. Re-rendered and verified:
ARIMA, Prophet, LightGBM, XGBoost, Ridge.

**One honest gap left visible.** `profiling.csv` has no row for Prophet, so its
box carries no memory figure while the other four do. That is correct behaviour —
the alternative is inventing a number — but it is worth knowing that **Prophet
was never memory-profiled**. If the memory argument in §6.8 is meant to cover
all five, it currently covers four.

---

# 3. Richer table formatting: yes, and OCR is not needed

**The question.** Markdown gives bold and italic only. Could tables be rendered
as SVG so colour, weight, slant and underline can encode best-in-class, second
best, and scenario groupings?

## The measured answer

Graphviz HTML-like labels rendered to SVG produce **real `<text>` elements**:

```
<text ... font-weight="bold" text-decoration="underline"
      font-family="Helvetica">17.4%</text>
```

Verified in this repository on 2026-09-14. All of the following survive the
render, independently per cell:

| Channel | Works | How |
|---|---|---|
| Cell background | yes | `BGCOLOR="#d9ead3"` |
| Text colour | yes | `<FONT COLOR="#1a7f37">` |
| Bold | yes | `<B>` → `font-weight="bold"` |
| Italic | yes | `<I>` → `font-style="italic"` |
| Underline | yes | `<U>` → `text-decoration="underline"` |
| Combinations | yes | nest them |

**The text stays selectable and searchable in the PDF, so no OCR step is
required.** That was the open question and the answer is no — the concern was
about raster images, and SVG is not one.

## What it costs

An SVG pastes into Word **as a picture, not as a table**. Three consequences:

- its cells cannot be edited in the document;
- Word's caption and cross-reference fields treat it as a **figure**, so a
  converted table changes which numbered sequence it belongs to;
- the copy-paste-into-Word-as-a-table benefit that motivated Markdown is lost
  for that table.

So this is a **trade, not an upgrade**. It is worth it where the encoding
carries an argument the reader would otherwise assemble from raw numbers, and
not worth it where the table is a plain lookup.

## The prototype

`05_thesis_results/styled_tables.py` — written, not yet wired to any table.

It renders any DataFrame with a `style_fn(row, column, value) -> style` callback,
so **the encoding is computed from the data on every run** and cannot be typed
in. It keeps the Correctness-tier provenance rule intact: change the inputs and
the highlighting moves with them.

Two design choices worth flagging:

- **The legend is generated from the same constants that style the cells**, so a
  table cannot acquire a colour its key does not explain.
- **Row grouping by background shade** is supported via a `row_group` callback,
  which is what would let A sit alone and B/D, C/E, F/G read as matched pairs
  down the table.

## Recommended encoding, if this goes ahead

| Meaning | Encoding |
|---|---|
| Best across all scenarios | green fill, green text, **bold + underline** |
| Second best | amber fill, amber text, **bold** |
| Criterion not met | red fill, red text |
| Capability-matched pair | shared light-grey row shade |

Four semantic states is about the ceiling before a table needs studying rather
than reading. I would not add a fifth.

## What I suggest

**Pick one table and try it.** `11_scenario_comparison` is the best candidate:
eleven measures across seven scenarios, where best-in-class per row is exactly
the comparison a reader wants and currently has to do by eye.

Keep it as `.md` as well. If the SVG earns its place, convert; if it does not,
nothing was lost. **Do not convert the whole appendix** — most of those tables
are lookups, and a picture of a lookup is worse than the lookup.

---

# Files changed for findings 1 and 2

| File | Change |
|---|---|
| `05_thesis_results/generate_architecture_diagrams.py` | added `substrate()` and `_BENCHMARKS`; Figure 2 now reads it; profiling keyed by cleaned model name |
| `05_thesis_results/styled_tables.py` | **new** — the SVG table renderer, not yet wired |

Finding 1 needs a decision before anything changes.
