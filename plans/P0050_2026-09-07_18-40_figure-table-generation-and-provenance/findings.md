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
