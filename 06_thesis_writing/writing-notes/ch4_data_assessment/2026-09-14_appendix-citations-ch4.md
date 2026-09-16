---
name: 2026-09-14_appendix-citations-ch4
description: NOTE - Which generated artefacts Chapter 4 can cite. Seven tables, three figures and 30 EDA plots sit unreferenced; the holiday tables and the per-brand ADF evidence are the strongest candidates. Defers to S1-S4 in deferred-structural-decisions.md.
category: workflow
applies-to: [ch4_data_assessment]
triggers: [ch4 prose pass, appendix placement, EDA plots, holiday tables, figure placement]
created: 2026_09_14-11_45
updated: 2026_09_14-11_45
snapshot: 2026-09-13_21-30_book-citations-pass
status: recommendations - no prose written
---

# Chapter 4 — what it can cite

Master analysis: `00_appendices/2026-09-14_appendix-inventory-and-provenance-audit.md`.

**This note is the other direction from S1-S4.** `deferred-structural-decisions.md`
decides whether Chapter 4's **existing body tables** stay, move or are deleted.
This note asks which **generated artefacts not yet in the document** should come
in. They do not overlap, and where a table is already under discussion there,
this note defers.

Chapter 4 is the richest chapter in the results tree and the one with the largest
gap between what exists and what the document reaches.

---

# What this chapter owns

| Artefact | Type | Last regenerated | In document? |
|---|---|---|---|
| `02_pipeline_execution.md` | table | 2026-09-11 | indexed, uncited |
| `03_pipeline_data_reduction.md` | table | 2026-09-11 | indexed, uncited |
| `04_feature_matrix.md` | table | 2026-09-13 | indexed, uncited |
| `90_holiday_source_provenance.md` | table | 2026-09-10 | **unindexed**, uncited |
| `91_holiday_annual_counts.md` | table | 2026-09-10 | **unindexed**, uncited |
| `92_holiday_monthly_matrix.md` | table | 2026-09-10 | **unindexed**, uncited |
| `93_holiday_feature_definitions.md` | table | 2026-09-10 | **unindexed**, uncited |
| `ch4_raw_schema_v1.svg` | figure | 2026-09-10 | uncited |
| `ch4_data_pipeline_v1.svg` | figure | 2026-09-10 | uncited |
| `ch4_preprocessing_pipeline_v2.svg` | figure | 2026-09-10 | uncited |
| `ch4_eda_pipeline_csd_v1.svg` | figure | 2026-09-10 | uncited |
| 30 EDA plots, 4 categories | figures | 2026-09-10 | uncited |
| ~119 EDA tables, 4 categories | tables | 2026-09-10 | uncited |

All current. None regenerated since the funded run, and none needs to be —
nothing downstream of the EDA changed.

---

# R1 — The star schema figure answers a promise the chapter already makes

**The existing hook.** §4.1 already says:

> "A visualization of the star schema can be found in Appendix A."

**The artefact.** `ch4_raw_schema_v1.svg` is a generated star-schema diagram
reading live row counts — 9,824,601 fact rows, 2,103 products, 86 and 44
dimension rows.

**Recommendation: this figure becomes Appendix A.**

**Why this is the highest-value item in the chapter.** Appendix A currently
contains a hand-drawn diagram. A generated one carrying live counts is strictly
better: it cannot go stale, and the counts are the evidence for the scoping
argument §4.1 makes. S4 in `deferred-structural-decisions.md` already flags that
Appendix A's title promises more than it contains — this is what completes it.

**Check before applying:** confirm whether the existing Appendix A diagram and
this generated one show the same schema. If they differ, the generated one is
authoritative.

---

# R2 — The four holiday tables are a coherent appendix block

**The artefacts.** Source provenance, annual counts, the month-by-year matrix,
and the feature definitions. Together they document the holiday enrichment end to
end: where the calendar came from, what it contains, and what was derived from it.

**Recommendation: appendix, as one block, cited once from §4.3 Feature
Engineering.**

**Why.** §4.3 currently says three of the eighteen model inputs come from the
Danish public-holiday calendar, and stops there. An assessor asking "where did
that calendar come from and is it trustworthy" has no answer in the document. The
provenance table answers it directly — it names the source, the API and the
retrieval date.

This is also the enrichment added in the cluster re-run, so it is the newest
substantive feature work and currently the least visible.

**One sentence in §4.3 covers all four.** Something of the shape *"The calendar
source, its annual and monthly composition, and the three derived features are
documented in Appendix [N]."*

---

# R3 — The per-brand ADF tables are the strongest evidence in the EDA set

**The artefacts.** `eda/{category}/tables/step_2_05_adf_per_brand.md`, one per
category.

**Recommendation: appendix, cited from §4.2.2, and read the warning below.**

**Why.** §4.2.2 defends the uniform log transform on the grounds that per-series
tests have low power at 46 observations. That defence is good and the tables
support it — each one carries a header stating exactly that limitation.

**The warning.** These tables also contain a fact the chapter does not currently
state: **27 of 79 tested brands recommend `raw`, meaning they test as stationary
in level.** Verified 2026-09-14 across all four categories (CSD 4/20,
Danskvand 7/20, Energidrikke 8/20, RTD 8/19).

That is the evidentiary spine of P0051, and it bears on §4.2.2's neighbouring
claim that non-stationarity "is handled by differencing for the statistical
baselines." For a quarter of tested brands, differencing is applied to a series
that did not need it.

**So this is a decision, not a paste.** Citing the table exposes the finding. My
view is that exposing it is correct and cheap to defend — the chapter already
argues that per-series selection would be worse than uniform treatment, and that
argument survives the finding intact. But it needs a sentence, and the sentence
is Brian and Enrico's to approve.

**Do not cite these tables without adding that sentence.** An assessor who reads
the appendix and finds 27 stationary brands behind a claim that the panel is
difference-stationary will ask about it.

---

# R4 — The pipeline figures: pick one, not three

Three figures depict overlapping views of the same pipeline:

| Figure | Shows | Live counts |
|---|---|---|
| `ch4_data_pipeline_v1` | raw → panel → contract → matrices → training arms | 9,645/9,993 rows, 230/366 brands |
| `ch4_preprocessing_pipeline_v2` | the same flow, more compact | 4,370 rows, 95 brands, 54 columns |
| `ch4_eda_pipeline_csd_v1` | the EDA step worked through for one category | table and plot counts |

**Recommendation: `ch4_data_pipeline_v1` in text; the other two in the appendix or
dropped.**

**Why that one.** It is the only one showing both training arms, which is what
Chapter 5's pooled-versus-specialised comparison needs a reader to have seen. It
also carries the caption explaining why the matrices hold more rows than the
panel — a question a careful reader will otherwise ask.

**Why not all three.** Three diagrams of one pipeline reads as indecision. The
EDA-pipeline figure is the best appendix candidate of the two remaining, since it
documents the exploratory process that §4.2 summarises.

**Provenance note.** `ch4_preprocessing_pipeline_v2` types `"54 columns"` beside a
computed row count. True for CSD, wrong for three of four categories, and it will
not follow the data. If this one is used, fix the literal first.

---

# R5 — The 30 EDA plots: cite selectively, or not at all

Eight plot types across four categories: distribution histograms, ECDFs, monthly
sales distribution, seasonal decomposition, top-brand time series, ACF/PACF,
promo intensity, correlation heatmap. Danskvand and RTD have seven, correctly
lacking the promo plot.

**Recommendation: appendix, one category only, cited once from §4.2.**

**Why one category.** §4.2 is explicitly the CSD exploratory analysis, with the
other three taken through "the identical pipeline". Reproducing 30 plots makes
the appendix longer without making the argument stronger. The CSD set shows the
method; the per-category tables carry the results.

**Which plots earn their place**, in order:

1. **`04_seasonal_decomposition.svg`** — §4.2 claims category-appropriate
   seasonality and this is the direct evidence.
2. **`06_acf_pacf_plots.svg`** — §4.2.4 discusses lag structure at length with
   specific autocorrelation values; this is what they came from.
3. **`01_distribution_histograms.svg`** — supports the skewness argument for the
   log transform, alongside the numbers already in §4.2.2.

The correlation heatmap, ECDF and top-brands plots are diagnostic rather than
evidential. My view is they stay in the repository and go uncited.

**Alternative worth considering:** cite the whole EDA directory once, as a
reference to the repository rather than as appendix content. That preserves the
repository-driven claim without a forty-page appendix.

---

# R6 — The feature-matrix table and S4

`04_feature_matrix.md` lists every column of the CSD matrix with the role it
plays. S4 in `deferred-structural-decisions.md` is already open on *"where the
full per-category feature list goes"*.

**This table is the answer to S4.** It is generated, current as of 2026-09-13, and
computes its own caption — "4,370 brand-months across 95 brands in 54 columns, of
which 34 are model inputs" is interpolated, not typed.

**Recommendation: appendix, and resolve S4 by pointing at it.** Recorded here;
the decision belongs in S4.

---

# Summary of what I would apply

| # | Artefact | Placement | Confidence |
|---|---|---|---|
| R1 | star schema figure | **Appendix A** | high |
| R2 | four holiday tables | appendix, one block | high |
| R3 | per-brand ADF | appendix + a sentence | **needs a decision** |
| R4 | `ch4_data_pipeline_v1` | in text | medium |
| R5 | 3 CSD EDA plots | appendix | medium |
| R6 | feature matrix | appendix, resolves S4 | high |
