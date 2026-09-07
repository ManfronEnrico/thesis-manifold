---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-07 04:00:00
---

# P0046 — Progress Log

> Condensed 2026-09-06. Full session-by-session narrative is in git history;
> this keeps what a future session needs.

**Branch:** `thesis/draft-bullet-reconstruction` (inherited from P0045).
**Uncommitted:** ~170 changed paths. **Worth committing before further work** —
this session moved, archived and rewrote a lot.

---

## Where things stand

Read `task_plan.md`'s STATUS QUO table first. Summary: architecture settled,
paths fixed and verified, every generator regenerates (tested by running), and
the diagrams have been rebuilt from the code rather than patched. No blockers.

Tomorrow starts at **Phase 3c** — make `export_appendix.py` consume
`run_manifest.json`.

---

## What actually happened, in order

**Session 1 (09-05)** — Traced ~70 artefacts. Found only 7-8 live producers, so
the sprawl was one script writing where it was told, not 70 independent origins.
Found the dangerous one: `fig2_granularity.png`, right folder, right name, same
date as its siblings, depicting a comparison DEC-GRAIN decided to stop making
and whose producing code P0035 deleted.

**Session 1b (09-05)** — Brian's three decisions. Two corrected me:
- I called the 18 `analysis/figures*` files unfixable. They are archived, not
  broken — a hardcoded macOS `FIGURE_DIR` and a stale scope are *edits*. Became
  per-file RESTORE-or-RETIRE.
- I held up `04_thesis_results/appendix/` as the model to copy without noticing
  it is a *production* site under the same contract. Sharpened the rule to **no
  generator writes into the writing tier**.

**Session 2 (09-06)** — Brian dropped the curation layer entirely: tier 06 holds
no artefacts at all. His reason was the sharing boundary; the stronger reason is
that it **removes the second copy**, which the manifest existed to police. I had
been building a defence against a problem I was creating.

Also reversed my own Q3 answer twice. I proposed `00_thesis_context/diagrams/`
on the grounds that "the production tree is what assessors read" — while getting
that tree's boundary wrong, since tier 00 is not shipped either. Lesson recorded:
**semantic fit is carried by the producer's location and subfolder name, not by
which tier the output lands in.**

**Session 3 (09-06)** — Brian restructured to SRQ-aligned tiers. Asked me to
update PATHS "accordingly"; probing first found **32 of 34 constants resolving to
non-existent paths**. Every pipeline script was broken, invisibly, because
`Path()` never validates and `import PATHS` still succeeded.

This is the plan's own thesis proving itself: because paths were centralised,
**one file needed repair instead of forty**, and one probe enumerated the whole
blast radius.

Brian's judgement beat mine twice more:
- *EDA split*: I proposed promoting hand-picked candidates. He split by file
  type — `.csv` stays (downstream steps consume it), `.md`/`.png` promote. Mine
  required a human decision per file before the citation sweep, i.e. backwards.
- *SRQ4 runs*: I offered fold-under-`raw/` or keep-as-is. He said runs don't
  belong in results at all. That retro-answered what I couldn't answer earlier
  ("what would `raw/` hold for SRQ1?") — nothing; `raw/` was the wrong idea.

And a correction: I wrote the ship boundary as "tiers 00-04". Tier 00 is
excluded too.

**Session 3b-3d (09-06)** — Full script sweep, then testing.

Audit went **43 flagged scripts → 10**, all 77 live scripts compile. The
`CLAUDE.md` → `.env.example` swap exposed two defects that were *not* the anchor:
`.gitignore` excluded `.env.example` (an uncommitted anchor cannot anchor a fresh
clone — the swap would have been worse than what it replaced), and every inline
finder walked from `cwd` rather than `__file__`, so any run from outside the repo
failed.

Then the shift that mattered most: **I ran the generators instead of reasoning
about them.** Three passed. Two failed on missing dependencies — and
`requirements.txt` turned out to omit `graphviz`, `matplotlib` and `statsmodels`
entirely. An assessor cloning the repo could reproduce **no** figure. Not
findable by reading the scripts.

Correction to my own first report: I initially said `shap` and `xgboost` were
undeclared. They are declared — my grep only read the first 25 lines. The real
gap was `graphviz` (undeclared *and* uninstalled), plus `matplotlib`/
`statsmodels` (undeclared, coincidentally installed).

Two confirmations from running things:
- `srq1_generate_performance_figures.py` produced 3 figures and did **not**
  recreate the zombie — P0035's removal is genuinely in the code, so archiving
  it is safe.
- `export_appendix.py`'s generated README hardcoded a producer path dead since
  the restructure: the index told readers to run a script that no longer exists.
  Now derived from `__file__`, so it cannot go stale again.

**SRQ2 is worse than Brian flagged, usefully so.** He suspected the LLM-as-Judge
files. A producer search found **zero** live producers — all five files are
orphaned, including the two 2026-08-19 synthesis outputs, because those scripts
were archived in August. The question is not "are the judge files stale" but
"can anything here be reproduced at all".

---

## Session 3e — Phase 3b execution (09-06)

Graphviz installed by Brian; all generators now run.

**Done**: SRQ1 reshaped (36 loose -> 3/33/13, zero loose, 15 producers
repointed); EDA promoted (149 files + a sync function); `ram_budget_v1`
quarantined.

**Two things testing caught that reading would not have:**

1. Moving SRQ1's files did not hold — re-running `training_report.py` rewrote to
   the flat path immediately. The shape only persists if producers write into it.
2. The `_SRQ1Out` resolver filed `RES / "figures"` as a *table*, creating
   `tables/figures/`. Fixed with a passthrough for bare subfolder names.

**A near-miss worth recording**: installing graphviz to "unblock the figures"
regenerated `ram_budget_v1` with its seven fabricated MB values — including an
"Indeks raw load" bar for the dataset dropped the same day. Quarantined, and the
generator call is now commented out so it cannot reappear. The plan had recorded
the risk; the guard is what made the recording useful.

**I had SRQ2 backwards, and it changed the recommendation.** I reported the
LLM-as-Judge files as artefacts of a "dropped design". Reading the chapters shows
they are **cited**: `judge_scores.csv` is Table 21 in Ch8 §8.3, its numbers
(3.81 vs 3.15, 100 rows = 50x2) matching the thesis exactly; the synthesis files
back Ch7 §7.2.

So SRQ2 is not stale-and-droppable, it is **cited-but-unreproducible** — worse,
because a cited table whose producer is archived cannot be checked or defended.
The answer is RESTORE, not retire; retiring is not available.

My error: I inferred "dropped" from Brian's remark plus 2026-07 dates plus
archived producers, without checking citations. *Producer → artefact* says
whether a thing can be rebuilt; only *artefact → chapter* says whether it must
be. Brian had independently flagged the same section OUTDATED/INCORRECT in review
comments 381/383/384.

## Session 3f — Diagrams rebuilt; logging audit opened (09-06/07)

### The diagrams were fiction, and patching them was the wrong move

Brian pushed back twice — "AI slop looking", then "we never use a langgraph
coordinator". Verifying against the live tree:

| Depicted | Reality |
|---|---|
| LangGraph / StateGraph | **not a dependency, imported nowhere.** One aspirational docstring line |
| Coordinator, Agent Layer, 4 Agents | no such objects in live code |
| Phase 1→2→3→4 approval gates | no approval mechanism exists |
| "Consumer Signals: PCA → k-means" | **no PCA or KMeans call in the repo** |
| ARIMA + Prophet in the ladder | statistical *baselines*, never ladder members |
| Per-model RAM 15/20/200/300/400 MB | invented; measured 5.4 / 29.2 / 38.1 |

I had patched labels **twice** before concluding the frame itself was the error.
Each pass produced a more accurate description of a system nobody built. The
lesson: when a diagram is wrong in several independent places at once, check
whether the *structure* is wrong before correcting the text.

Rebuilt as four stage diagrams plus `layered_architecture_v2`, all reading
artefacts at render time, exiting rather than drawing if a table is missing.
Style deliberately plain — one accent colour, no gradients or rounded cards,
greyscale-legible at column width.

### A live break found while verifying

`srq4_experiment.py` loaded Scenario C's tool from
`model_serving_interface/scenario_c_forecast/` — removed in the restructure.
**Scenario C would have raised FileNotFoundError at import.** Now `SRQ2_DIR /
"forecast_tool.py"`, verified.

### Brian corrected the method, and it invalidated one of my recommendations

*"Your whole approach of 'what is already cited in the thesis' is completely
botched up and in reverse."* Correct. I had used "does a chapter cite this?" as
the test for whether an artefact deserves to exist — but the draft is
provisional, and the citation set is an **output** of this work.

Where it led me wrong: I recommended **restoring** the SRQ2 judge producers
*because Table 21 cited them*, when the design had been dropped and Brian's own
review comments flagged that table for removal. Recorded as F19 and now the
plan's stated method.

### Pipeline logging audit (Phase 3c opened)

Healthy: console capture is thorough and even across all four categories, and
`{slug}_eda_findings_h{N}.json` is a real contract that later steps consume.

Two gaps:
1. Only steps 0-1 emit `step_N_log.json`; steps 2-6 write console text only.
2. **The orchestrator timed every step, then only printed it.** Its docstring
   even says the console log is "the run-level view no individual step log
   contains" — true, and exactly the problem: prose, not data.

Fixed the second with `write_run_manifest()`. Verified by constructing real
`StepResult` objects and round-tripping the JSON — worth doing, because the first
draft used `st.reason` and treated `st.step` as a string, and both were wrong.

## Recurring errors

| Error | Note |
|-------|------|
| `grep -rn` over the repo times out at 120s | Third session running. Fix (use the Grep tool) was logged by me twice and I reached for `grep` anyway. Genuine `/errors-log` material |
| Bulk-edit scripts broke syntax twice | Block inserted inside a function; closing paren after a comment. The compile sweep caught both instantly — keep it as a gate |
| Plugin hook flags `focus_detail` frontmatter | False positive: that field is required by `workflow-planning-with-files.md`. Not stripped |

---

## Session 4 — 2026-09-07 — Phase 3c: the logging loop closed

Picked up the recorded entry point: make `export_appendix.py` consume
`run_manifest.json`.

**Writing the consumer broke the producer** (F22). Two bugs, both invisible in
the one case that had been run by hand:

* `--all-categories` would have filed every category's record under CSD's folder
* running `--horizon 1` would have erased the H=3 record

Both found by round-tripping real `RunResult` objects — the same method that
caught the `st.reason`/`st.detail` slip last session. Fixed: per-category
manifests, merged by horizon.

**Then found a regression from last session's own reshape** (F23). Moving SRQ1
output into `tables/` repointed the producers but not `export_appendix.py`, which
still read the flat root. Because the exporter skips missing inputs by design, it
had been emitting **6 tables instead of 12** and exiting 0. The plan recorded it
as PASS, and it was — it just silently produced half an appendix.

**Delivered**
* `write_run_manifest()` rewritten: per-category, merge-not-overwrite, documented
* `table_pipeline_execution()` added — step names read from the manifest, so a
  renamed step cannot leave the table describing a pipeline that no longer exists
* Six exporter reads repointed into `tables/` (6 → 12 tables)
* Real CSD H=3 run (steps 3-6, 15.7s, all passed) → manifest → appendix table
* Full appendix verified: **22 tables** across 3 producers, zero orphans

**Verification**: 194 live scripts, 0 compile failures; `PATHS OK`.

**Process note.** A bulk-edit script broke the same file three times (`
` in a
heredoc collapsing to a real newline, twice; then a repair heuristic mangling 7
good lines). Recovered with `git checkout --` and the Edit tool. The 3-strike
rule should have fired on attempt two — the signal was that the *method* kept
failing, not the individual edit. Also reached for `grep -rln` a fifth session
running; the Grep tool answered instantly. Root cause is now known: any `-r`
sweep walks `.venv` (~40k files) and must exclude it.

---

## Session 5 — 2026-09-07 — Phase 3c closed + clean-slate re-run

Two tasks, both done.

### 1. Clean slate (Brian's request)

Full pipeline, **all 4 categories x H=1 and H=3, steps 0-6**. Ran the EDA too,
not just steps 3-6 — the earlier `--from-step 3` note would have skipped exactly
the EDA steps that were asked for.

**8 runs, all OK.** 149 EDA artefacts promoted to tier 05. Every category now has
a manifest; the merge logic held (CSD's earlier standalone H=3 run was replaced,
not duplicated).

### 2. Content metrics (F25)

`_step_metrics()` extracts from the value each step **already returns** — the
orchestrator was discarding all of it except step 2's failure list. No step
module was touched, so there is no second code path to drift from what the
pipeline computes. Tested all 7 branches with real-shaped objects first.

The metrics immediately paid for themselves: they showed **step 4 has MORE rows
than step 1** (CSD 4,209 -> 4,876). Checked rather than assumed — it is the
calendar fill completing each brand's month grid so a lag refers to the previous
month, not the previous observed row. My draft appendix note had claimed the
opposite; corrected before it shipped.

Following that up found step 4 **already writes a richer log** than my metrics
(`rows_in -> rows_calendar -> rows_filtered -> rows_out` with brands at each
stage). So the reduction table now reads `step_4_log_h{N}.json` directly, and a
docstring claiming "only steps 0 and 1 write logs" was corrected — it is 0, 1, 4
and 5.

### 3. Modelling-layer audit (F26)

**2 of 21 scripts record any provenance.** Result CSVs carry data columns only —
no timestamp, no producing script, no input identity. `train_and_persist.py`'s
per-model `metadata.json` is a complete record and is the pattern to copy.
Recommendation scoped but deliberately NOT executed: one shared stamp helper
rather than 19 edits, and it ranks below Phases 4-6 with 8 days to submission.

**Delivered**
* Content metrics in manifest + console (one line per step)
* `table_pipeline_data_reduction` — separate from the timing table (units differ)
* Appendix: **24 tables**, 3 producers, all regenerating, no duplicate prefixes
* All 5 diagrams regenerate; `pipeline_v2` independently agrees with the
  reduction table (CSD H=3: 4,370 rows / 95 brands from two different sources)

**Verification**: 194 live scripts, 0 compile failures; `PATHS OK`.

---

## Session 6 — 2026-09-07 — Phase 4 + the five requested chapter figures

**DEC-GENERATE-ALL** (Brian): generate every figure programmatically; redrawing
one by hand afterwards is his option, not a reason to leave it ungenerated. That
settled the open `ch2_gap_diagram` question — rebuild, not adopt.

### Built (F27, F28)

Six figures added to the diagram generator and one new table generator:

| Artefact | Ch | Facts from |
|---|---|---|
| `ch1_research_questions_tree_v2` | 1 | current RQ set |
| `ch2_gap_diagram_v2` | 2 | S2.7 + `RAM_BUDGET_MB` |
| `ch4_data_pipeline_v1` | 4 | each category's `step_4_log_h3.json` |
| `ch4_eda_pipeline_csd_v1` | 4 | section names read off the EDA's own tables |
| `ch6_modelling_pipeline_v1` | 6 | metrics/profiling/metadata/pooled CSVs |
| `ch5_tool_interface_v1` | 5 | a persisted model's metadata |
| `89_literature_design_map` | 2 | parsed from Ch2 + a curated design column |

### Wrong claims caught and corrected

1. `ch2_gap_diagram` stated the envelope as **8 GB**. It is 4096 MB.
2. **Ch5's figure caption** claimed a five-model substrate, human-in-the-loop
   checkpoints and a bounded agentic layer. The ladder is four; the other two
   exist nowhere in the code. Rewritten with the correction noted inline.
3. **"18 EDA section groups"** — asserted from a directory listing. Counted, it
   is **16**. Now derived.
4. **Pooled vs per-category is split 2/2**, not a direction. The label states the
   split and names the categories rather than implying a winner.

**Scale trap**: `metrics.csv` stores WMAPE as a percentage (17.5), while
`retune_single_cutoff.csv` stores a fraction (0.1257). A blanket `*100` produces
a plausible 1750%. Check per file.

### F29 — one producer was deleting another's output

The new literature table writes prefix `89`; `export_appendix.py` cleared
`<= 89`. Run in that order it was silently deleted, and the deleting run
reported success. It survived this session only by luck of ordering. Bound
lowered to 88 and **the block allocation written into the docstring**, since a
cleanup scoped by a magic number is correct only until someone adds a producer.
Verified by running in the dangerous order.

### Layout

Three figures were re-laid-out after *looking* at them: the data pipeline ran
~1800px wide (unreadable at page width), the modelling diagram's orthogonal
router drove edges through the ladder cluster leaving SeasonalNaive apparently
unconnected, and the tool interface put the caller below the response it
receives. Generating a figure is not the same as checking it renders legibly.

**Verification**: 195 live scripts, 0 compile failures; `PATHS OK`; 5 producers
run clean in any order; 11 diagrams + 25 appendix tables.

---

## Next session starts here

**Phase 5 — inventory, THEN citations** (F19: never the reverse):

1. Publish the complete regenerable inventory — 11 diagrams, 25 appendix tables,
   4 SRQ1 figures, 149 EDA artefacts, each with its producer.
2. Decide per artefact: in-text, appendix, or neither.
3. Then audit the snapshot comments against that inventory.
4. Decide the 18 `analysis/figures*` on regenerability, not on citation.

**Then Phase 6** (MANIFEST.md + invariant checks) and **Phase 7** (style pass).

**Open for Brian:**
- The five new chapter figures are drawn from code and ready to look at. If any
  should be redrawn by hand, the generated one is the reference for the facts.
- "8 GB" -> 4 GB in Ch6 prose (8 occurrences) and Ch2 (N11 note) — still open.
- Abstract's Indeks Danmark claim (2 occurrences) — still open.
- Ch8 S8.3 / Table 21 comes out with the retired judge.
- P-ID collision with the second `P0046_..._exogenous-enrichment-decision/`.

**Environment:** the diagram generator needs Graphviz's bin directory on PATH.

**Deferred:** modelling-layer provenance (F26) — real, but our audit trail, not
a blocker on any thesis artefact.

**Still uncommitted** — four sessions of work now. Worth committing.
