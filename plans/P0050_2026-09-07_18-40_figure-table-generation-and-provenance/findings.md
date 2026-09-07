---
pid: P0050
created: 2026-09-07 18:40:00
updated: 2026-09-07 18:40:00
---

# P0050 — Findings

Consolidated from the figure/table work in P0046 (2026-09-05 → 09-07). These are
the things that were **wrong** and how they were caught, kept because most of
them are traps that recur rather than one-off slips.

---

## F1 — The diagrams described a system that was never built

The original generator drew LangGraph state machines, a "Coordinator", four
named agents, phase-approval gates, and PCA + k-means consumer signals. Verified
against the live tree: **none of it exists.** LangGraph is not a dependency and
is imported nowhere; there is no coordinator, no approval mechanism, no PCA or
KMeans call. Per-model RAM figures (15/20/200/300/400 MB) were invented — the
measured values are 4-40× smaller.

**The process failure matters more than the content.** I patched labels on that
frame *twice* before recognising the frame itself was the error. When several
independent facts in one artefact are wrong, that is a signal to question the
structure, not to correct the text.

Rebuilt from what the repository actually contains: three sequential,
independently-run stages.

## F2 — Inventory first, citations second

Corrected by Brian, and it inverted the whole approach:

> "I am trying to fix and centralize all re-generatable figures, tables, graphs
> and diagrams, so we can then DECIDE if and how we are going to reference them.
> ... So your whole approach of 'what is already cited in the thesis' is
> completely bothed up and in reverse."

The draft is provisional — sections are being removed. **The citation set is an
output of this work, not an input to it.** "Is it already cited?" is not a test
of whether an artefact should be regenerable.

## F3 — Dead path constants fail silently

32 of 34 `PATHS.py` constants were dead after the tier restructure. `Path()`
never validates, so a dead constant fails at read/write time, not at import —
often much later, and in a different script. Rebuilt to 39/39 resolving.

The root anchor was moved from `CLAUDE.md` to `.env.example` because *"claude
will tell the assessor that we used claude"*. That swap exposed two latent bugs:
`.env.example` was uncommittable (a `.env.*` gitignore rule), and the walk
started from the working directory rather than `__file__`.

## F4 — `requirements.txt` was missing every plotting dependency

`graphviz`, `matplotlib` and `statsmodels` were absent. A fresh clone could
reproduce **no figure at all**. This is the kind of gap that is invisible on the
machine that has the packages.

## F5 — Skip-on-missing hides structural breaks

The SRQ1 reshape moved output into `tables/` and repointed the **producers**. It
did not repoint the **consumers**: `export_appendix.py` still read the flat root.

The exporter is deliberately tolerant of missing inputs, so a structural break
became six polite notices and **exit code 0**:

```
(skip resource profile: profiling.csv absent)
(skip parameter drift: refit_vs_retune.csv absent)
...
```

25 tables had become 6 and nothing failed. The plan still recorded the generator
as PASS — because it *had* passed; it just produced half an appendix.

**Two lessons.** A move is not complete when the producers are repointed: grep
for *readers* of every path that moved. And skip-on-missing is right for a
half-run experiment and wrong for a moved directory — the code cannot tell them
apart, so a run should report "N written, M skipped" loudly.

## F6 — Two collisions in one shared output directory

**First**: the `NN_` prefix is *generation order*, not identity. A dropped table
shifts every later number, and nothing cleaned up. Three runs left **29 files for
13 tables**, with three different tables all named `02_`. The stale copies are
plausible — real tables from a real run, just superseded.

**Second**: adding `generate_literature_table.py` at prefix `89` collided with
`export_appendix.py`'s cleanup bound of `<= 89`. Running them in that order
**silently deleted** the literature table, and the deleting run reported success.
It survived only by the order I happened to use.

Fixed by lowering the bound to 88 and **writing the block allocation into the
docstring**, since a cleanup scoped by a magic number is correct exactly until
someone adds a producer and nothing will tell them:

```
01-49   export_appendix.py
89      generate_literature_table.py
90-93   export_holiday_appendix.py
94-99   srq1_export_enrichment_appendix.py
```

Verified by running in the dangerous order.

## F7 — Extract metrics from what the code already returns

The orchestrator measured per-step timing and then only *printed* it. Adding
`run_manifest.json` closed that, and writing its **consumer** immediately exposed
two bugs in the **producer** — both invisible in the single-category case that
had been run by hand:

- `--all-categories` would have filed every category's record under the first
  category's folder
- running `--horizon 1` would have erased the H=3 record

Both found by round-tripping real `RunResult` objects. Verifying dataclass fields
by *reading* had already produced a wrong guess the day before (`st.reason` for
`st.detail`). **Execute the objects.**

For content metrics, every step already returned something meaningful — a
DataFrame, a contract, a manifest — and the orchestrator was discarding all of
it. Extracting centrally rather than instrumenting seven step modules means
**there is no second code path to drift**.

The metrics paid for themselves immediately: they showed step 4 producing *more*
rows than step 1 (4,209 → 4,876). Checked rather than assumed — it is the
calendar fill completing each brand's month grid. My draft caption had claimed
the opposite.

## F8 — The modelling layer has almost no run provenance

**2 of 21 scripts** in `model_training/` record anything (`generated_utc`,
`generated_by`, a timestamp, a git ref). The result CSVs carry data columns only:
no timestamp, no producing script, no input identity. An examiner asking "is this
metrics table current with the feature matrix that shipped?" cannot answer it.

The good pattern already exists in exactly one place:
`train_and_persist.py` writes a per-model `metadata.json` recording model,
hyperparameters, seed, features, training and calibration windows, interval
method, train seconds, peak RAM and `trained_at_utc`.

**Recommendation, scoped but deliberately not executed**: one shared stamp helper
at the small number of save paths, not 19 edits. Ranked below Phases 5-7 — it is
our audit trail, not a blocker on any thesis artefact.

## F9 — The literature table is the one artefact with two provenances

Ch2 has no machine-readable literature-to-design mapping; the links live in the
prose. So the generator splits and **marks** the halves:

- **Parsed** from the chapter: section titles, `*Maps to ...*` mappings, claims.
  These cannot drift.
- **Curated** in the script: what each strand changed in the build. The test
  applied to each entry — *if it cannot name something openable in the
  repository, it does not belong in the table.*

The script **warns** when a parsed section has no design consequence recorded.
That fired immediately for §2.0 and §2.9, correctly — they are the chapter's
introduction and transition, not literature strands.

Parsing note: claim bullets wrap across lines, so reading line-by-line cut claims
mid-sentence *and* left a stray `**` where a bold span opened on one line and
closed on the next.

## F10 — Three claims in figures contradicted the code

1. `ch2_gap_diagram` stated the deployment envelope as **8 GB**. It is 4096 MB.
2. **Ch5's figure caption** claimed a five-model substrate, human-in-the-loop
   checkpoints and a bounded agentic layer. The ladder is **four** (ARIMA and
   Prophet are statistical *baselines*); the other two exist in no live module.
3. **"18 EDA section groups"** was written from a directory listing. Counted, it
   is **16** — the numbered prefixes have gaps.

All three are the same failure: a number or a name written from memory or from a
glance, in a place where it reads as measured.

## F11 — A scale trap across sibling files

`metrics.csv` and `pooled_metrics.csv` store WMAPE **as a percentage**
(17.5 = 17.5%). `retune_single_cutoff.csv` stores it **as a fraction** (0.1257).
A blanket `*100` produces a plausible **1750%**.

The exporter's existing `*100` is correct for the file it reads. **Check the
scale per file; do not assume it across the tier.**

## F12 — Say what the numbers say, not what reads well

Pooled vs category-specific training is **split 2/2**: category-specific wins CSD
and RTD, pooled wins the other two. My first label said "per-category training
wins in 2 of 4", which is true but reads as a direction. It now states the split
and names the categories.

A figure should not imply a result the numbers do not support.

## F13 — Layout is only verifiable by looking

Generating without error is not the same as rendering legibly. Each of these was
caught **only** by opening the file:

- a flow running ~1800px wide, unreadable at page width
- an orthogonal router driving edges *through* a cluster, leaving a node
  apparently unconnected
- a request/response figure placing the caller *below* the response it receives

Also learned: `rank="same"` to force rows **fights** the layout — it produced a
column (ratio 0.8) and a staircase. And a wide caption sets a *floor* on figure
width, so a long single-line caption silently stretches the drawing above it.

## F14 — Style is a contract, not a preference

Brian's review named the pattern: horizontal layouts (the appendix prints
landscape), bold header rows in each box, no step numbers, greyscale contrast
tiers with nested boxes *lighter* than their container, transparent backgrounds,
and captions that never mention a script — *"not every assessor will look at the
repo"*.

Written to `.claude/rules/figure-generation-standards.md` and applied to all
eleven figures. Compliance is checkable mechanically: a regex over the rendered
SVGs for filenames, step numbers and plan IDs returns **zero** hits.

---

# Live state carried forward from P0046

P0046 is archived. F15-F18 below are the parts of it that describe **things still
on disk**, as opposed to lessons already generalised in F1-F14.

## F15 — Three quarantined archives, and why each is quarantined

`05_thesis_results/diagrams/.archive/` holds three directories, each with a
README. **None of their contents may be pasted into the thesis**, and the reason
differs in each case:

| Archive | Holds | Why it is not usable |
|---------|-------|----------------------|
| `fabricated_ram_budget_2026-09/` | `ram_budget_v1.{svg,png}` + its source function | Seven **invented** MB values (P0040 F5). One is "Indeks raw load, 970 MB" — a dataset dropped the same day as never used. The figure charts memory consumed by data the thesis does not touch |
| `fictional_architecture_2026-09/` | 5 diagrams + the old generator | Depicted LangGraph orchestration, a coordinator and named agents — see F1 |
| `ch5_architecture_v1_2026-09/` | the hand-drawn Ch5 figure | Claimed a five-model substrate, approval checkpoints and an 8 GB envelope |

**The RAM one is the near-miss worth remembering.** Installing graphviz to
"unblock the figures" would, unguarded, have shipped a fabricated figure straight
into the results tier on the first successful run in months. The plan had
recorded the risk in advance; that recording is what made the guard happen.

The guard itself is now moot in the best way: the 2026-09-06 generator rebuild
replaced the whole file, so `fig4_ram_budget()` **no longer exists** rather than
sitting commented out. Real measurements are in
`appendix/02_substrate_resource_profile`, `04_sandbox_resource_profile` and
`srq1_model_performance/tables/sandbox_profiling.csv` — the resource figure now
reads those.

## F16 — SRQ2 holds two files with no live producer

`05_thesis_results/srq2_structured_tool_interface/` contains exactly
`synthesis.csv` and `synthesis_summary.md`. **No live script writes them**; the
producers (`srq2_synthesis.py`, `srq2_agent.py`) sit in
`02_thesis_modelling/.archive/superseded_scripts_2026-08/`.

The judge artefacts that used to sit beside them are retired: Brian's decision,
stated directly — *"we decided against a judge; just because it is in the current
thesis doc doesn't mean it will be removed"* — and independently corroborated by
his own review comments 381/383/384 on Ch8 §8.3 (`VERIFY`, `OUTDATED`,
`INCORRECT`).

**A correction worth keeping**, because the reasoning error is repeatable: I had
first recommended RESTORING the judge producers, on the grounds that Table 21
cites them. That inferred a requirement from the *draft* rather than from the
design decision — the same inversion as F2. A chapter citing something is
evidence it was once intended, not evidence it must survive.

**Open**: the two surviving files are cited by Ch7 §7.2. Either restore
`srq2_synthesis.py` (deterministic, free to re-run) to a live SRQ2 location, or
withdraw the §7.2 numbers. Not decided.

## F17 — Enrico's 18 notebook figures, still unresolved

`06_thesis_writing/analysis/figures/` (11) and `figures_agentic/` (7). They trace
to archived notebooks that hardcode `/Users/enricomanfron/Desktop/…`, so they are
**archived, not broken** — the blockers are path edits, not rewrites.

Decide per file on **regenerability**, not on whether something currently cites
them (F2). And apply the pairing rule: **RETIRE archives the image too.** A stale
image left beside a retired producer is exactly the trap that produced the very
first finding of this whole effort — a figure still sitting in the results tier
whose generating code had been deleted a month earlier.

## F18 — Two more environment traps

Neither is a code defect; both cost time.

**Graphviz is not on PATH.** `winget install Graphviz.Graphviz` put `dot.exe` at
`C:\Program Files\Graphviz\bin` without adding it, so the generator raises
`ExecutableNotFound` in a fresh shell. Prepend it.

**A shell heredoc turned `\b` into a backspace inside a plan file.** Writing a
Windows path into a Python string inside a heredoc; Python warned
(`SyntaxWarning: invalid escape sequence`) and the control character landed in
the `.md`, where the Edit tool then could not match the line. The warning is the
tell — avoid backslash paths in generated strings.

---

## Inherited blocker — not this plan's to fix

**The forecast horizon is never applied to feature construction.**
`engineer_features()` takes no horizon argument (`engineer_features.py:444`,
verified directly). The `h1` and `h3` matrices encode the **same one-month task**
and differ only in their split dates.

Found by P0048 (F1), carried by P0049 (F22), fix lives in P0049.

**Consequence here**: the data-reduction table's "Horizon (months)" column labels
a horizon the pipeline never applied. The row counts are real. A DO-NOT-PUBLISH
warning sits in that table's review notes; re-run and remove it once the fix
lands.

---

## F19 — Tier 05 runs three organising schemes at once; `appendix/` is a routing decision baked into a path

Brian's observation, 2026-09-07: `05_thesis_results/appendix/` holds 25 correct
tables under an outdated name. The wider finding is that the tier mixes **three
different keys** simultaneously:

| Folder | Keyed by |
|--------|----------|
| `eda/` | pipeline stage |
| `srq1…srq4/` | research question |
| `diagrams/`, `appendix/` | artefact type |

`appendix/` is the worst of the three, because "appendix" is not a property of an
artefact — it is a **decision about where it lands in the document**, and that
decision is exactly what Phase 5 exists to make. Encoding it in a path pre-commits
every table to an answer nobody has given yet. (`diagrams/` has the same shape,
but Brian chose to keep it flat and solve it with filename prefixes instead.)

**DEC-CHAPTER-FOLDERS** (Brian, 2026-09-07): tier 05 will be keyed by **thesis
chapter**, matching the final document, with `figures/ tables/` beneath each.

### The routing is not clean — two conflicts, both real

Brian's stated instinct was "files go where they originate". That splits cleanly
by producer, but **producer location and chapter genuinely disagree twice**:

1. **`export_appendix.py` is not a scenario script.** It lives in
   `04_SRQ4_Scenario_Experiment/scenario_setup/` and writes 14 tables, but only
   ~8 concern the scenario experiment. The metric dictionary, pipeline execution,
   data reduction, substrate profile, retraining cost and statistical baselines
   are about the pipeline and the models. Routing by producer would file the
   pipeline-execution table under "scenario experiments" — worse than today.

2. **The holiday tables split across two chapters.** 90–93 describe the calendar
   *source* (Ch4, enrichment) and are written by `_00_raw/holidays/`. 94–96 are
   *ablation results* — with-feature vs without — written by `model_training/srq1/`.
   Same subject, different chapters, and the producers already differ.

**Resolution**: chapter wins. Producer location is an implementation detail that
has already drifted once — the SRQ1 reshape silently halved the appendix when
producers moved and consumers did not (F5).

### Blocked on the Word export, deliberately

Brian is reworking the `.docx` export so headings carry their numbers
("Chapter 2 | Literature Review", "2.8 Design Science Research") instead of bare
titles. **The folder names should come from that export, not from a guess at the
chapter numbering.** Ch2's numbering is what makes the literature map's home
obvious; guessing now would mean renaming later.

Proposed shape, to confirm against the export once it lands:

```
05_thesis_results/
  ch2_literature/        89
  ch4_data_and_eda/      CSD/ … + 90-93 + pipeline execution, data reduction
  ch5_tool_interface/    SRQ2's two files (see F16 — producer undecided)
  ch6_modelling/         srq1 figures/tables/models + 94-99 + baselines, metric dict
  ch7_scenarios/         srq4 + scenario comparison, taxonomy, per-run, config
  ch8_resources/         substrate + sandbox profile, retraining cost
  diagrams/              flat, chapter-prefixed (done — F20)
```

**Every mover must repoint consumers, not just producers** — that is F5's lesson,
and this move touches all five producers plus `PATHS.py`.

---

## F20 — The chapter prefix is now enforced, not remembered

Five diagrams had drifted unprefixed (`pipeline_v2`, `model_selection_v2`,
`scenarios_v2`, `resource_profile_v2`, `layered_architecture_v2`). Renamed by
**what each figure shows**, verified by reading its body rather than trusting its
name:

| Old | New | Why that chapter |
|-----|-----|------------------|
| `pipeline_v2` | `ch4_preprocessing_pipeline_v2` | raw extract → modelling matrix |
| `model_selection_v2` | `ch6_model_selection_v2` | benchmark, then deploy per category |
| `scenarios_v2` | `ch7_scenarios_v2` | the three-scenario information ladder |
| `resource_profile_v2` | `ch6_resource_profile_v2` | fit cost per model vs the envelope |
| `layered_architecture_v2` | `ch5_layered_architecture_v2` | its own docstring says Ch5 |

`_check_stem()` raises on a stem without `ch<N>_`. It raises rather than warns: a
figure with no chapter is a figure nobody can place, and a warning in a 11-figure
run is a line of output nobody reads.

**The trap it caught**: `fig_resource_profile` is the one figure that saves
through matplotlib rather than `_save()`, so a guard placed only in `_save()`
would have missed exactly the figure whose predecessor carried fabricated numbers
(F15). It now calls `_check_stem` explicitly.

**A second stale label surfaced while renaming**: that function's `print()` still
announced `resource_profile_v2` after the file had been renamed, because the
rename regex required a quote or slash before the stem and the print did not have
one. Cosmetic, but it is the same class of miss — a mechanical rename reaches
what it matches, not what it means.

Live consumers repointed: `ch5-framework-design.md` (two references — the image
path *and* a stale bullet still naming the archived `ch5_architecture_v1`) and
three diagram READMEs. Archived plan folders left as historical record.

---

## F21 — Graphviz ordering: three failed methods, and why each failed

Brian asked for the scenarios in alphabetical order with the Prometheus pair
below the LLM group. Simple to state, and it took four attempts because
graphviz's ordering controls are all *rank* controls in disguise.

| Attempt | Result | Why |
|---|---|---|
| Invisible `A→B→C→D→E` edges under `rankdir=LR` | `B E D C A` | an edge forces a new **rank**; under LR each scenario was pushed into its own column instead of ordered within one |
| `rank="same"` subgraph listing all five | order still wrong, **both cluster boxes vanished** | a `rank="same"` subgraph *re-parents* its nodes, pulling them out of `cluster_s`/`cluster_p` |
| `ordering="out"` on the `q` node | `B A C D E` | `ordering` is a **graph** attribute; set on a node it is silently ignored |
| `rankdir=TB` + `rank="same"` **per cluster** + invisible edges inside each | `A B C D E`, clusters intact | inside an already-same-rank cluster an invisible edge no longer re-ranks — it only constrains order, which is what was wanted |

**The lesson worth keeping**: two of the three failures were silent. The vanished
clusters in particular produced a valid SVG that simply no longer showed the
grouping — nothing errored. This is the concrete case for the standing rule that
a figure is verified by *measuring the rendered file*, not by the generator
exiting 0. Every diagnosis above came from parsing coordinates out of the SVG.

A trap in that measurement: **SVG y-coordinates are negative-upward**, so sorting
descending prints the stack bottom-to-top. One "still wrong" reading was my own
sort direction, not the layout.

---

## F22 — Aspect ratios measured against A4; one figure exceeds the page

Brian's target: figures scalable into either a portrait text block (in-text) or a
landscape appendix page. Measured against A4 with 2.5 cm margins — portrait text
block 160×247 mm (ratio 0.65), landscape 247×160 mm (**1.54**):

| Ratio | Diagrams |
|-------|----------|
| ≤ 1.54 — fits either orientation | `ch7_scenarios_v2` (1.10), `ch4_eda_pipeline_csd_v1` (1.35), `ch6_model_selection_v2` (1.54) |
| 1.54–3.6 — landscape, or in-text at reduced size | `ch5_tool_interface_v1` (2.26), `ch6_resource_profile_v2` (2.12), `ch5_layered_architecture_v2` (2.40), `ch6_modelling_pipeline_v1` (2.60), `ch1_research_questions_tree_v2` (3.19), `ch4_data_pipeline_v1` (3.25), `ch2_gap_diagram_v2` (3.41) |
| > 3.6 — **too wide to place** | `ch4_preprocessing_pipeline_v2` (4.45) |

`ch4_data_pipeline_v1` was 4.4 and is now **3.25**, by pinning the first stage of
each construction phase into a shared column so the flow folds into two rows —
Brian's own suggestion, and it worked without touching the content.

`ch4_preprocessing_pipeline_v2` at 4.45 is the one that still cannot be placed at
readable size. It is also **superseded in substance** by `ch4_data_pipeline_v1`,
which covers the same ground with counts read from the execution logs — so the
question is whether to fix it or retire it, and that is a Phase 5 citation
decision, not a layout fix.

### On generating two versions per figure

Brian asked whether each figure should ship a portrait-optimised and a
landscape-optimised variant. **Recommendation: no — not as a general rule.**

An SVG is vector: one file scales to either page without loss, so a second file
buys nothing unless the *layout itself* differs (a two-row fold for portrait
versus one row for landscape). That is a real difference, but it applies to at
most the three widest figures, and each variant is then a second artefact that
must be kept in step with the first — the exact duplication this plan exists to
remove (DEC-SINGLE-HOME).

Better: hold every figure at **ratio ≤ 3.6**, which is placeable in landscape and
still legible reduced into a portrait column. Only if a specific figure proves
unreadable in-text should it get a second variant, decided per figure with the
citation decision in Phase 5.

---

## F23 — A graphviz cluster cannot be ordered; stop trying and stop using one

**Supersedes the ordering advice in F21.** F21 concluded that `rank="same"` on a
cluster plus invisible edges inside it was the working recipe. It held for one
layout and broke the moment the figure changed direction. Four *further* methods
failed after it, each producing a different wrong order:

| # | Method | Result |
|---|--------|--------|
| 1 | invisible `A→…→E` chain | each node forced into its own column |
| 2 | `rank="same"` naming all five | nodes re-parented; **both cluster boxes vanished silently** |
| 3 | `ordering="out"` on a node | ignored (graph attribute) |
| 4 | `rank="same"` per cluster + chains | worked once, then gave `B A C` |
| 5 | edge `weight` to bias position | `D E B A C` |
| 6 | `constraint="false"` on fan edges | cluster order fixed, member order still `B A C`, cluster widths desynced |
| 7 | `newrank="true"` | clusters side by side again, order `C D E B A` |

**Every one of those is a hint to a heuristic.** Graphviz reorders a rank to
shorten edges, and a figure where several nodes share edges to a common source
and sink gives it every reason to. The nodes with fewer such edges (D, E) stayed
put; the ones with more (A, B, C) were shuffled. That is the tell.

### The fix: make the order text, not a layout decision

`_stack(title, rows)` renders a group as **one node** whose label is a table of
rows. The order is then the order of a Python list — it cannot be renegotiated.

```python
g.node("llm", _stack("evaluation scenarios — LLM", [
    ("A — Plain LLM", "no access to firm data"),
    ("B — LLM + data & code", "the firm's history, analysed in a sandbox"),
    ("C — LLM + dedicated model", "the forecast tool"),
]), shape="box", style="filled", fillcolor=CLUSTER, color=LINE)
```

**Cost**: members are no longer individually addressable as edge endpoints; the
group is. Worth paying whenever the sequence *is* the content — a lettered
ladder, a numbered pipeline — and not worth it when members genuinely need
their own edges.

**Use a cluster when** membership is the point and order is not. **Use a stack
when** order is the point.

### It also fixed a bug I had introduced

`rank="same"` across two clusters re-parents its members, and graphviz says so:

```
Warning: agg was already in a rankset, deleted from cluster data_pipeline
Warning: contract was already in a rankset, deleted from cluster data_pipeline
```

That warning was the "data contract box escaping its outer box" Brian spotted in
`ch4_data_pipeline_v1` — I had caused it one exchange earlier while folding that
figure into two rows, and the warning had been scrolling past unread. **Read
graphviz's warnings**; they name the node and the cluster.

### Measured outcome

| Figure | Before | After |
|--------|--------|-------|
| `ch7_scenarios_v2` | order wrong in 7 ways; ratio 1.10–4.16 | **A B C D E**, inputs left, outcomes right, ratio 2.05 |
| `ch4_data_pipeline_v1` | contract box outside its phase; ratio 3.25 | phases stacked and edge-aligned (both x 148..371), ratio **1.16** |

Nine of eleven figures now fit a portrait column or a landscape page.
`ch4_preprocessing_pipeline_v2` (4.45) remains the sole outlier and is still the
retire-or-fix decision from F22.

---

## F24 — Ch5's comparison names the capability, not the scenario

Brian, 2026-09-07. The architecture figure's comparison box had carried the old
descriptive scenario names; relettering them A/B/C fixed the vocabulary mismatch
but introduced a worse problem — **it implied the Prometheus pair was missing.**

Adding D and E would have been the obvious repair and the wrong one. It would
duplicate, in the architecture chapter, a mapping the scenarios figure already
owns, and every future change to the ladder would then need editing in two
places.

**The resolution generalises instead of enumerating:**

| Was | Is |
|-----|-----|
| A — Plain LLM | **Plain agent** — no access to firm data |
| B — LLM + data & code | **Agent + data & code** — the firm's history, analysed |
| C — LLM + dedicated model | **Agent + models** — the forecast tool |

Brian's reasoning, which is right: both the local orchestrator and the production
engine are *agents*; both can be given data and code; both can be given the
trained models; and both are measured against the plain agent as baseline. Three
conditions therefore cover all five lettered scenarios, and the architecture
chapter states the **capability ladder** while Chapter 7 states the **experiment**.

**Each figure owns one level of abstraction.** The letters are the experiment's
vocabulary and belong where the experiment is described. Repeating them in the
design chapter is not consistency, it is duplication — and it was duplication
that would have gone stale, since D and E are the part most likely to change.

Converted from a cluster to a `_stack` in passing: the cluster had rendered
C, B, A (F23 again), and the single edge that pointed at a member now addresses
the group. The caption was rewritten too — it had said "only the third
evaluation scenario", a phrase that only parses if the letters are present.

---

## F25 — Tier 05 is now chapter-keyed; the SRQ folders are gone

DEC-CHAPTER-FOLDERS executed 2026-09-07. `05_thesis_results/` now holds one
folder per thesis chapter, each with `figures/ tables/ models/`:

```
introduction/            1  ch1_research_questions_tree
literature_review/       2  ch2_gap_diagram + the literature-design map
data_assessment/       164  3 figures, 6 tables, and all 149 EDA artefacts
architecture/            2  ch5_layered_architecture, ch5_tool_interface
model_benchmark/        92  3 figures, 25 tables, the trained models
decision_synthesis/      9  ch7_scenarios + interval communication
experimental_evaluation/15  the scenario comparison
discussion/              0  (SRQ3 is argued, not measured)
```

`srq1_model_performance/`, `srq2_structured_tool_interface/`,
`srq3_integration_readiness/`, `srq4_scenario_experiments/`, `appendix/` and
`diagrams/` no longer exist. Quarantined material moved to `.archive/`.

### What made this cheap: three helpers, not thirty scripts

~30 producers write into the results tier, and 38 sites referenced the SRQ1
directory alone. Almost none needed editing, because they already went through
`get_srq_{figures,tables,models}_dir()`. **Repointing those three helpers moved
the output of ~25 scripts without touching them.**

The lesson generalises: a script should ask for *somewhere to put an SRQ's
tables*, not name a directory. Where that is belongs to `PATHS.py`. The scripts
that did need editing were exactly the ones that had built paths inline --
including two inside the diagram generator that reconstructed
`THESIS_RESULTS_DIR / "eda" / "CSD"` by hand instead of calling
`get_category_eda_results_dir()`, and broke the moment the EDA folder moved.

### Numbered folders, derived numbers

Brian is considering a reorder (swapping the benchmark and architecture
chapters; possibly moving feature diagnostics into the data chapter). Folders
named `ch04_`, `ch06_` would go stale the moment that happens, and renaming ten
folders plus every reference is the churn this avoids.

Folders are `{NN}_{slug}` so the tree sorts in reading order (`01_introduction`
… `10_conclusion`), but **the number is derived from position in
`CHAPTER_SLUGS`, never typed.** One private helper, `_chapter_folder()`, builds
the name, and both `get_chapter_results_dir()` and the five direct `*_DIR`
constants call it -- so the prefix exists in exactly one place.

**To reorder the thesis, reorder `CHAPTER_SLUGS`; nothing else changes.**
Verified by simulating the proposed benchmark/architecture swap: the folders
renumbered to `05_model_benchmark` / `06_architecture` with no other edit.

The first attempt hardcoded `"06_model_benchmark"` into those five constants,
which reintroduced exactly the duplication the slug scheme exists to avoid -- a
reorder would have left them pointing at the wrong chapter while still
resolving. Caught by the "does every `*_DIR` exist?" check.

### Two routing decisions worth keeping

**`export_appendix.py` routes per table, not per script.** It lives with the
SRQ4 harness but only 5 of its 15 tables concern the scenario experiment; the
rest describe the pipeline (Ch4), the models and their cost (Ch6), and the tool
interface (Ch7). `_TABLE_CHAPTER` names the chapter for each, and an unmapped
slug **raises** -- a default would file a new table wherever was convenient and
let it sit unnoticed.

**The holiday tables split deliberately.** 90-93 (calendar source) go to Ch4;
94-96 (ablation results) to Ch6. Same subject, two chapters, two producers.

### The prefix-block scheme is retired

`_clear_previous()` used to delete `NN_` files below a bound, because four
producers shared one flat directory and a whole-directory wipe would destroy
output this script cannot regenerate. That was fragile in both directions: the
bound was once set to 89 and silently deleted the literature table (F6), and a
new producer picking a free number relied on remembering to look.

It now deletes exactly `NN_<slug>.{md,csv}` for slugs it is about to rewrite. It
cannot reach another producer's output even in a shared directory, and no block
allocation needs maintaining.

### Verification

All five producers run clean; 11 figures and 38 tables land in chapter folders;
every file in the old flat `appendix/` and `diagrams/` was confirmed reproduced
**before** either was deleted; both draft image references were repointed and
checked to resolve; and no `*_DIR` constant resolves to a missing directory.

`THESIS_RESULTS_APPENDIX_DIR` and `THESIS_RESULTS_DIAGRAMS_DIR` were **removed**
rather than repointed -- their contents now span several chapters, so there is
no single directory left for either to name.
