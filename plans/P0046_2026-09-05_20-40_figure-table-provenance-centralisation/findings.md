---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-05 20:40:00
---

# P0046 — Findings

Evidence gathered 2026-09-05. Every claim below is traceable to a command run in
session; where a claim is inference rather than observation it says so.

---

## F1 — There are exactly seven live producers, not seventy

Searching `*.py` for `savefig|to_markdown` returns 53 files, but 41 of those are
under `.archive/`, `.claude/skills/` or `.agents/skills/` (vendored skill
templates, not thesis code). The live set is small:

| Script | Emits | Into |
|--------|-------|------|
| `02_thesis_data/.../\_shared_modules/step_2_eda_descriptive.py` + `capture_utils.py` | EDA plots + tables | `{category}/pipeline_step_outputs/{cat}_eda_{plots,tables}/` |
| `03_thesis_modelling/model_training/srq1/srq1_figures.py` | `fig1_model_ladder`, `fig3_forecast_overlay` | `04_thesis_results/srq1/figures/` |
| `03_thesis_modelling/model_training/srq1/srq1_shap.py` | `shap_importance.png` + `.csv` | `04_thesis_results/srq1/figures/` |
| `03_thesis_modelling/model_training/training_report.py` | `training_report.md` | `04_thesis_results/srq1/` |
| `03_thesis_modelling/scenario_setup/export_appendix.py` | the 12 appendix tables + `.csv` twins + `README.md` index | `04_thesis_results/appendix/` |
| `03_thesis_modelling/scenario_setup/score_interval_communication.py` | `interval_communication` | `04_thesis_results/srq4/` |
| `04_thesis_results/generate_figures.py` | 6 conceptual diagrams | `05_thesis_writing/figures/` |
| `05_thesis_writing/figures/generate_systemB_diagram.py` | `system_b_overview.{svg,png}` | `05_thesis_writing/figures/` |

This is the good news: **the coverage gap is much narrower than the folder
sprawl suggests.** Most of what looks like chaos is one script's output sitting
in the folder it was told to write to, plus two folders of genuinely dead
artefacts.

---

## F2 — `generate_figures.py` produces exactly six names, and that settles the triage subfolders

Emitted (`save_dot` / `save_mpl` call sites, lines 149/263/361/437/557/759):

```
system_architecture_v1   agent_workflow_v1   data_flow_v1
ram_budget_v1            confidence_score_v1  project_overview_v1
```

Cross-referencing against the triage subfolders a prior session created:

| File | In folder | Producer? | Label |
|------|-----------|-----------|-------|
| `system_architecture_v1` | `update_information/` | ✅ yes | REGENERABLE-STALE |
| `data_flow_v1` | `update_information/` | ✅ yes | REGENERABLE-STALE |
| `ram_budget_v1` | `update_information/` | ✅ yes | REGENERABLE-STALE (+ see F5) |
| `ch1_research_questions_tree` | `update_information/` | ❌ **none** | ORPHAN |
| `ch5_architecture_v1` | `update_formatting/` | ❌ **none** | ORPHAN-CONCEPTUAL |
| `ch2_gap_diagram` | `unsure/` | ❌ **none** | ORPHAN-CONCEPTUAL |

The three `_v1` files being regenerable is significant: their "stale information"
problem is **a code edit away from fixed**, not a redraw. The figure content is
literally written in `generate_figures.py` as graphviz node labels — update the
labels, re-run, done. That reframes those three from "manual redraw backlog" to
"edit six strings".

The three orphans are the real gap. `ch1_research_questions_tree` is the one to
watch: it depicts the RQ/SRQ hierarchy, which is *structured content that has
changed* (the SRQ set moved during P0039/P0040). It is an ORPHAN whose content is
known-stale and which has no producer — worst of both.

---

## F3 — `analysis/figures/` and `analysis/figures_agentic/` trace to an archived notebook

Both sets were produced by Enrico's Jupyter notebooks, now at:

- `user-docs/.archive/thesis/analysis/thesis_notebook_CSD.ipynb` → `figures/01..07`, `final_01..04`
- `user-docs/.archive/thesis/analysis/thesis_agentic_notebook.ipynb` → `figures_agentic/*`

The notebook cell outputs still contain the save confirmations, e.g.
`✅ docs/thesis/analysis/figures/04_shap_importance.png`, and the notebook
hard-codes `FIGURE_DIR : /Users/enricomanfron/Desktop/Thesis Maniflod/docs/thesis/analysis/figures`.

So these are **not** AI-generated with no source — they had a real producer.
But that producer is:
- archived (under `.archive/`, i.e. deliberately retired),
- pinned to a path on another machine,
- written against the pre-`docs/`→`user-docs/` layout,
- and predates both the four-category scope and the H=3 horizon.

**Label: ORPHAN-DERIVED.** These are charts *of data* with no runnable producer.
That is the category that cannot ship. Concretely, `04_shap_importance.png` in
this folder is superseded by `04_thesis_results/srq1/figures/shap_importance.png`,
which has a live producer (`srq1_shap.py`) and is 2026-08-20 rather than
Enrico-era.

Note the naming collision hazard: **two different `shap_importance` figures exist
in two folders**, one live and one dead, differing only by a numeric prefix. This
is exactly the failure mode centralisation prevents.

---

## F4 — `fig2_granularity.png` is a zombie: its code was deliberately deleted

`04_thesis_results/srq1/figures/` on disk:

```
2026-07-11  fig1_model_ladder.png
2026-07-11  fig2_granularity.png      <-- ZOMBIE
2026-07-11  fig3_forecast_overlay.png
2026-08-20  shap_importance.png
```

`srq1_figures.py`'s own docstring says:

> GRAIN NOTE (P0035, 2026-08-01): fig2_granularity.png is no longer produced. It
> compared brand×month against brand×chain, and DEC-GRAIN (2026-07-12) dropped
> the chain grain — there is no second grain left to compare against.

So the file depicts a comparison the project **formally decided to stop making**.
It is not merely stale; its subject no longer exists in the thesis. If it reached
a chapter it would contradict the documented grain decision.

**This is the single most dangerous artefact found.** It looks exactly as
legitimate as its two siblings — same folder, same date, same naming scheme — and
the only thing marking it as dead is a comment inside a script that does not
mention it in its output. Delete it.

`fig1` and `fig3` are REGENERABLE-STALE: both predate not only P0035 (2026-08-01)
but the 2026-08-18 leakage fixes and the 2026-08-24 metric regeneration. Their
siblings in the parent directory (`calibration.md` etc.) are all 2026-08-24 —
i.e. **the tables were regenerated and the figures were not.** The figures and
tables in `srq1/` currently disagree about what the results are.

---

## F5 — `ram_budget_v1` is the known-fabricated figure

P0040 finding F5 (per the plans index) records that `fig4_ram_budget` was
fabricated and is to be replaced with real measurement. `generate_figures.py`
still contains `fig4_ram_budget()` → `save_mpl(fig, "ram_budget_v1")`, and the
file sits in `update_information/`.

The measurement that should replace it now exists: `04_thesis_results/appendix/`
carries `02_substrate_resource_profile` and `04_sandbox_resource_profile`
(2026-09-03), generated by `export_appendix.py` from `sandbox_profiling.csv`.

So this is resolvable, not blocked — but it must be resolved by *rewiring the
figure to real data*, not by re-running the current code, which would simply
regenerate the fabricated numbers. **Re-running `generate_figures.py` naively is
therefore not safe** for this one figure.

---

## F6 — The EDA layer is the healthiest thing in the repo

All four categories have current, complete pipeline outputs:

| Category | Plots | Tables (incl. `.csv` twins) | Tables dir mtime |
|----------|-------|------|------------------|
| CSD | 8 | 62 | 2026-08-12 |
| Danskvand | 7 | 56 | 2026-08-12 |
| Energidrikke | 8 | 62 | 2026-08-12 |
| RTD | 7 | 58 | 2026-08-12 |

Every one is emitted by the shared `_shared_modules/` pipeline via
`capture_utils.save_table()` / `print_and_save_table()`, and `PATHS.py` already
has `get_category_pipeline_step_outputs_dir(category)`.

Brian's instinct in the prompt — "perhaps we should point them to the thesis
writing folder" — is the one recommendation in this session I'd push back on.
See F10.

(Danskvand and RTD have 7 plots vs 8; likely the ACF/PACF or promo plot is
skipped where a category lacks the input. Worth confirming in Phase 4, but it is
a completeness question, not a provenance one.)

---

## F7 — `04_thesis_results/appendix/` is already the model to copy

Twelve tables, all 2026-09-03, each emitted as **both `.md` and `.csv`**, with a
generated `README.md` index, from a single script. Reading
`export_appendix.py`'s header, it already encodes the conventions this plan was
going to have to invent:

- No hard-coded table numbers — "numbering is Word's job", because a dropped
  table silently staleness-rots hard-coded numbers while Word's field-based
  cross-references renumber themselves.
- Publishable content above a `<!-- REVIEW -->` marker, student-facing notes in a
  separate `_review_notes.md` sidecar, so "a screenshot of any table is clean by
  construction".
- Units in the header (`WMAPE (%)`) not per-cell, per M4/M5 competition practice.
- Generated from the same `runs.csv` as `summary.md`, "so they cannot disagree".

**Recommendation: do not design a new table convention. Generalise this one.**
It is the newest, most thought-through surface in the repo and it already solves
the Word-integration problem that the rest of the artefacts do not.

---

## F8 — Two generators hard-code a CWD-relative path; one has a byte-identical shadow copy

`04_thesis_results/generate_figures.py` and
`05_thesis_writing/figures/generate_systemB_diagram.py` both do:

```python
OUTPUT_DIR = "05_thesis_writing/figures"
```

This is a *relative* string. It resolves correctly only when the script is run
with the repo root as CWD, and silently creates a stray `05_thesis_writing/`
subtree anywhere else. Every other live producer resolves through `PATHS.py`.

Additionally, `utility_scripts/scripts/generate_systemB_diagram.py` is
**byte-identical** (md5 `cc6f393695…`) to the copy under `05_thesis_writing/figures/`.
This is the same shadow-copy problem P0035 F6 already diagnosed and archived for
other scripts, recurring here. `.claude/rules/repo-tier-structure.md` states
`utility_scripts/` is tooling-only and never thesis content — the copy under it
is the one to delete.

---

## F9 — `PATHS.py` has no figure or table constants at all

`grep -nE "FIGURE|APPENDIX|PLOT|TABLE" PATHS.py` returns only
`get_category_pipeline_step_outputs_dir`. There is no
`THESIS_FIGURES_DIR`, no appendix constant, nothing.

This is the structural cause of the sprawl. Output locations are currently
expressed three different ways — a PATHS helper (EDA), a PATHS-derived results
dir (srq1, appendix), and a bare relative string (the two diagram scripts) — so
there has never been a single place that says where figures go. Centralising the
*files* without centralising the *constant* would re-sprawl within a month.

---

## F10 — Recommendation on the centralisation question

Brian proposed centralising everything into `05_thesis_writing/`, including
repointing the EDA pipeline outputs there. **I agree with the destination and
disagree with the scope.**

**Agree:** `05_thesis_writing/figures/` + a new `tables/` sibling is the right
home for anything that goes *into the thesis*, and there should be exactly one
such place.

**Disagree on moving the EDA outputs.** Those files are pipeline *step outputs* —
their value is that they sit next to the step that produced them, so an examiner
tracing "what did step 2 do to CSD" finds the evidence in one directory. Moving
them to a writing folder breaks that adjacency and mixes ~240 diagnostic
artefacts with the ~20 that will actually be printed. The pipeline would also
have to reach across tiers to write, which inverts the dependency direction the
tier structure exists to enforce.

**Proposed shape — a curation layer, not a move:**

```
05_thesis_writing/
  figures/            # in-thesis figures only
  tables/             # in-thesis tables only
  MANIFEST.md         # generated: artefact -> producer -> source data -> chapter
```

with the distinction that `05_thesis_writing/` holds the **selected** set, and
each entry is *copied in by a generator* that records where it came from. The
pipeline keeps writing to its own step-output folders; a thin curation script
promotes the chosen few and writes the manifest.

Why a manifest rather than just a tidy folder: the failure this whole session is
about is not that files were in the wrong folder — it is that **nobody could tell
whether a given file was alive**. `fig2_granularity.png` sat in the right folder
with the right name and was still poison. A folder cannot express provenance; a
generated manifest can. Any artefact that cannot get a manifest row is, by
definition, one that should not be in the thesis.

This also gives a cheap CI-style check: regenerate, and if a file in `figures/`
has no manifest row or a changed hash, it is stale — which is precisely the
question that took a whole session of manual inspection to answer this time.

---

---

## F11 — DECIDED: the "produce where it lives, promote what ships" contract

Brian, 2026-09-05, in response to F10:

> "Save where produced in entirety, and only the final appendix selection in the
> thesis_writing folders. Best of both worlds. That does mean however that the
> scripts writing the current appendix folder should also follow the same logic."

**DEC-P0046-CURATION** is therefore settled, with one consequence Brian caught
that F10 had not stated:

`04_thesis_results/appendix/` is not exempt. F7 praised it as the model to
generalise, but under this contract it is *also* a production site, not a
publication site. Its twelve tables stay where `export_appendix.py` writes them
(next to the `runs.csv` they came from), and the subset that actually appears in
the thesis appendix gets promoted into `05_thesis_writing/tables/` by the same
curation step as everything else.

This is the right call and worth stating plainly: the appendix folder's *name*
made it look like a destination. It is not. It is `scenario_setup/`'s output
directory that happens to be called "appendix" because of what its contents are
*for*. Under the contract, **no generator writes into `05_thesis_writing/`** —
that tier is populated exclusively by the curation step, and that invariant is
what makes the manifest trustworthy. One writer, one manifest, no exceptions.

Practical consequence for Phase 3: `export_appendix.py` keeps its
`OUT = THESIS_RESULTS_DIR / "appendix"` behaviour unchanged (though the literal
`"appendix"` becomes a constant per F13). What changes is that
`04_thesis_results/generate_figures.py` and `generate_systemB_diagram.py` stop
writing to `05_thesis_writing/figures/` — they currently violate the contract by
writing straight into the publication tier. They need a production home of their
own (proposed: `04_thesis_results/diagrams/`, since they are generated artefacts
like everything else in tier 04).

Resulting shape:

```
02_thesis_data/.../pipeline_step_outputs/{cat}_eda_{plots,tables}/   produced
04_thesis_results/srq1/figures/                                      produced
04_thesis_results/appendix/                                          produced
04_thesis_results/diagrams/                     <-- NEW              produced
                        |
                        |  curation script (the ONLY writer into tier 05)
                        v
05_thesis_writing/figures/     only what a chapter cites
05_thesis_writing/tables/      only what a chapter cites
05_thesis_writing/MANIFEST.md  artefact -> producer -> source -> chapter -> hash
```

---

## F12 — DECIDED: ORPHAN-DERIVED is a per-file restore-or-retire call, not a bulk verdict

Brian, 2026-09-05:

> "Technically we could just restore from archive for those, adapt them to have
> the proper up to date data and formatting guidelines, and then re-generate,
> right? We would need to decide for each of them, whether we want to restore and
> regenerate, or simply keep in archive and archive their therefore
> not-to-regenerate image leftovers."

Correct, and this supersedes F3's framing. F3 said these files "cannot ship",
which is true of the *files*, but that slid into sounding like the notebooks were
unusable. They are not. The notebooks are archived, not broken — the blockers are
a hardcoded macOS `FIGURE_DIR` and a pre-four-category scope, both of which are
edits rather than rewrites.

So the taxonomy needs a correction: **ORPHAN-DERIVED describes the file on disk,
not its producer's fate.** A file in that class has two legitimate exits:

| Exit | What it means | When it is right |
|------|---------------|------------------|
| **RESTORE** | Lift the notebook cell out of `.archive/`, port it to a script resolving through `PATHS.py`, re-run against current data | The figure shows something no live script covers, and a chapter wants it |
| **RETIRE** | Leave the notebook archived, and archive the stale image beside it | A live script already covers it, or no chapter cites it |

The pairing matters: retiring means archiving *the image too*, not leaving it in
place. A stale image sitting in a live folder next to a retired producer is
exactly the `fig2_granularity` failure mode (F4) — the file looks alive because
of where it sits. Retire moves both halves together.

One RETIRE candidate is already clear: `analysis/figures/04_shap_importance.png`
is covered by `srq1_shap.py`'s `shap_importance.png` (2026-08-20, live producer).
Keeping both is how you end up with two same-named figures of different vintages
in different folders (F3's collision hazard).

The 18 files each need a row. **Phase 5 supplies the missing input** — which of
them a chapter actually cites — so this table gets filled in *after* the citation
sweep, not before. Deciding restore-vs-retire without knowing what the thesis
references would be guessing.

---

## F13 — DECIDED: all output paths centralise in `PATHS.py`

Brian, 2026-09-05:

> "Great catch, we must rectify that. All paths should be dynamic to the highest
> degree and centralized in PATHS.py"

**DEC-P0046-PATHS.** No output location may be expressed as a literal string in
a generator. Every one resolves through a `PATHS.py` constant or helper.

Reading `PATHS.py` in full (804 lines) confirms F9 and surfaces two additions:

**1. The tier-map docstring is itself stale.** Line 28 reads:

```
    05_thesis_writing/    sections-drafts/, sections-final/, figures/, analysis/
```

`sections-final/` was archived 2026-09-01 — `.claude/rules/writing-surface-authority.md`
lists it as "**Gone** (archived 2026-09-01)". So the file that exists to be the
authority on repo layout is advertising a directory that no longer exists. This
is the same class of defect P0035 fixed when it removed constants resolving to
deleted paths, recurring in prose rather than in code. Phase 3 updates this line
to the post-P0046 shape (and should add `tables/`).

**2. `PATHS.py` already has a good convention for recording removals.** Lines
185-197, 356-360 and 662-665 leave explanatory comments where constants used to
be, naming the plan and the decision that removed them. New constants in Phase 3
should follow it, and the two generators being repointed should leave a note
saying a hard-coded relative string lived there and why it moved.

Constants to add in Phase 3 (names provisional):

| Constant | Resolves to | Serves |
|----------|-------------|--------|
| `THESIS_RESULTS_DIAGRAMS_DIR` | `04_thesis_results/diagrams` | the two diagram generators (F11) |
| `THESIS_RESULTS_APPENDIX_DIR` | `04_thesis_results/appendix` | `export_appendix.py` (replaces its inline `OUT =`) |
| `THESIS_RESULTS_SRQ1_FIGURES_DIR` | `04_thesis_results/srq1/figures` | `srq1_figures.py`, `srq1_shap.py` |
| `THESIS_WRITING_FIGURES_DIR` | `05_thesis_writing/figures` | curation script only |
| `THESIS_WRITING_TABLES_DIR` | `05_thesis_writing/tables` | curation script only |
| `THESIS_WRITING_MANIFEST` | `05_thesis_writing/MANIFEST.md` | curation script only |
| `get_category_eda_plots_dir(cat)` | `.../{cat}_eda_plots` | EDA pipeline |
| `get_category_eda_tables_dir(cat)` | `.../{cat}_eda_tables` | EDA pipeline |

The two EDA helpers are worth adding even though the pipeline currently works.
The folder name embeds a lowercased category (`csd_eda_plots` under `CSD/`), so
every caller reconstructs that casing by hand — a naming convention living in
call sites rather than in `PATHS.py`, which is precisely the decentralisation
this decision ends. It also means a future category with an awkward name has one
place to be special-cased instead of several.

## Open questions for Brian

Q1 (curation vs. move) and the PATHS question are **settled** — see F11 and F13.
Q2 is **reframed** by F12: no longer one bulk verdict but 18 per-file
restore-or-retire calls, and it needs Phase 5's citation sweep as input before it
can be answered. Remaining:

1. **`ch1_research_questions_tree`** — no producer, and its content (the RQ/SRQ
   tree) has changed. Redraw by hand, or add it to the diagram generator as a
   seventh graphviz figure? The latter costs ~40 lines and makes it permanently
   self-updating; given the RQ set has already moved once, I lean that way.

2. **Zombie deletion** — confirm `fig2_granularity.png` is deleted outright
   rather than archived. My argument for delete: P0035 already preserved the
   chain-grain evidence at `plans/P0035_.../preserved_chain_grain_results/`, so
   archiving it again duplicates a preservation that already exists.

3. **`04_thesis_results/diagrams/` as the production home** for the two diagram
   generators (F11) — reasonable, or somewhere else? They are the only generated
   artefacts with no tier-04 home, precisely because they were writing straight
   into tier 05.

4. **Deferred to Phase 5** — the 18-row restore-or-retire table (F12), fillable
   once we know which figures the chapters actually cite.
