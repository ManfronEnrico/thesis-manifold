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

## F14 — Tier 05 holds no artefacts at all (supersedes F11's second half)

**Decided by Brian, 2026-09-06.** The curation layer proposed in F11 is dropped.
`05_thesis_writing/` receives **no** figures, tables or diagrams. It holds only
writing apparatus: `citations/` (Zotero), `docx-exported-snapshots/`,
`notebookLM/`, `sections-drafts/`, `thesis_inspiration/`, `writing_notes/`.

Every artefact lives exactly once, at the site that produces it, inside
`04_thesis_results/`. Humans browse that tree and pick what to paste into the
`.docx`.

**Why this is better than the curation design it replaces** — and the reason is
stronger than the one that motivated it:

Brian's stated rationale was the clean-repo boundary (tier 05 is not shared, so
artefacts must not be trapped in it). True, but that is a *side effect*. The
structural gain is that **there is no second copy of any artefact**. F11's design
had a curation script copying selected files into tier 05, which meant every
promoted figure existed twice and something had to keep the two honest. A copy
whose link to its producer is not machine-checked is exactly the
`fig2_granularity` failure mode (F4) — a plausible file in a plausible folder
with nothing tying it to live code. F11 proposed a MANIFEST to defend against
that; F14 removes the need for the defence by removing the copy. The manifest
survives as a useful index, but it is no longer load-bearing.

Two further gains:

- **The clean-repo rule becomes one line**: tiers 00-04 ship, tier 05 does not.
  Under F11 it would have been "tier 05 minus some subfolders", which is a rule
  someone eventually gets wrong.
- **Tier 05 becomes semantically coherent for the first time.** Everything left
  in it is writing apparatus — Zotero state, review passes, working notes.
  Figures were the only occupant that was not.

## F15 — Routing rule: producer tier decides, tier 04 receives

**Decided by Brian, 2026-09-06.** Which folder a generator lives in is settled by
what it is *about*; where it writes is always tier 04.

| Producer lives in | Because it is about | Writes to |
|-------------------|---------------------|-----------|
| `02_thesis_data/` | data processing, EDA, feature engineering | `04_thesis_results/eda/{category}/` |
| `03_thesis_modelling/` | training, serving, orchestration | `04_thesis_results/srq{N}/` |
| `04_thesis_results/` (own scripts) | general/conceptual diagrams, cross-cutting tables | `04_thesis_results/diagrams/` |

This is the same train-vs-serve-vs-scenario test `.claude/rules/repo-tier-structure.md`
already applies to scripts, now extended to their outputs — one rule covering
both, rather than two rules that can drift apart.

It also resolves the Q3 thrash. Three homes were proposed for the two diagram
generators in as many hours: `04_thesis_results/diagrams/` (F11),
`00_thesis_context/diagrams/` (my revision, on the reasoning that the production
tree is what assessors read), and now back to `04_thesis_results/diagrams/`.
The revision was wrong for a specific reason worth recording: it optimised for
*semantic fit within the shipped tree* while forgetting that tier 00 is not in
the shipped tree either. Brian's constraint — assessors see tiers 00-04, and
artefacts must be findable in one place — makes tier 04 the only destination that
satisfies both. **Semantic fit is expressed by the producer's location and the
subfolder name, not by which tier the output lands in.**

### The one exception: EDA volume

The ~240 EDA plots/tables are pipeline outputs, so F15's rule would route them
wholesale into `04_thesis_results/eda/`. That would recreate, at 10x scale, the
browsing problem F16 identifies. They stay written where the pipeline writes
them (`02_thesis_data/.../pipeline_step_outputs/`), and only the EDA artefacts
that are genuine thesis candidates get written to tier 04. This is the single
place a promotion step still earns its keep — and unlike F11's version, it
promotes *into* the shipped tree, not out of it.

## F16 — `04_thesis_results/` is not currently browsable, which F14 requires

F14/F15 promote tier 04 to "the tree humans browse to pick artefacts". It is not
in a state to serve that role.

`04_thesis_results/srq1/` holds **36 loose files at its top level** — 20 `.csv`,
13 `.md`, 3 `.json` — while `srq1/figures/` holds only 4. Among them sit
`metrics.csv`, `tuned_metrics.csv` and `cv_metrics.csv` side by side. Nothing in
the naming says which one a chapter should cite. Compare `04_thesis_results/appendix/`
(F7), which is uniform and readable.

**Consequence for the plan:** centralising the *destination* without imposing a
shape inside it centralises the location and keeps the disorder. Each results
folder needs a consistent internal layout — `figures/`, `tables/`, `models/`,
`raw/` — so that browsing is uniform regardless of which SRQ is open. Added as
Phase 3b.

Two leftovers found in the same sweep, both the same class as the F4 zombie —
an output whose producing code is gone:

- `04_thesis_results/phase3_region_grain_test/phase3_result.json` — P0035
  archived the region-grain *script* to `.archive/grain_artifacts_p0035_2026-08/`
  but left its *output* in place, in what is about to become the deliverable tree.
- `04_thesis_results/__pycache__/` — build clutter in the same tree.

## F17 — `fig2_granularity.png`: delete, on evidence

**Decided 2026-09-06.** Verified before deciding, and the check changed my
recommendation:

- **It is committed in git** — `4c7a98b` ("feat: SRQ1 publication figures") and
  again in the flatten `8329881`. `git show 4c7a98b:<path>` recovers it. An
  archive folder duplicates what version control already does.
- **No chapter cites the filename.** A repo-wide search for `fig2_granularity`
  returns 9 files: the P0046 and P0035 plan docs, `PLANS_INDEX.md`, and the two
  copies of `srq1_figures.py`. Zero chapters, zero snapshots. (The word
  "granularity" appears in many chapters, but as ordinary methodology
  vocabulary — not as a figure reference.)
- **The decision survives elsewhere** — the `srq1_figures.py` docstring note, the
  archived P0035 plan, and `.archive/grain_artifacts_p0035_2026-08/`. None of
  those is the image.

My earlier argument for archiving was "an examiner might ask about the dropped
grain". Brian's clean-repo constraint kills it: tier 05's archive is not shared,
so archiving there protects against a reader who by construction cannot see it.
A folder that costs nothing and does nothing.

## F18 — `ch1_research_questions_tree` → generator

**Decided by Brian, 2026-09-06.** Added to the diagram generator as a seventh
graphviz figure rather than redrawn by hand. The RQ set has already moved once;
a node list is a cheap edit next time it moves, whereas a hand-drawn tree goes
stale silently and nothing detects it.

## F19 — The SRQ-aligned restructure (2026-09-06) and what it broke

Brian restructured the repo between sessions: top-level folders now map
one-to-one onto research questions.

| Was | Now |
|-----|-----|
| `01_thesis_research/` | archived; `research-questions/` -> `00_thesis_context/` |
| `02_thesis_data/` | `01_SRQ1_Model_Training/01_thesis_data/` |
| `03_thesis_modelling/` | `01_SRQ1_Model_Training/02_thesis_modelling/` |
| `03_thesis_modelling/scenario_setup/` | `04_SRQ4_Scenario_Experiment/scenario_setup/` |
| `04_thesis_results/` | `05_thesis_results/` |
| `05_thesis_writing/` | `06_thesis_writing/` |
| — | `02_SRQ2_Tool_Interface/`, `03_SRQ3_Integration_Readiness/` (empty) |

**This silently broke every pipeline script.** A probe of `PATHS.py` on the new
tree found **32 of 34 directory constants resolving to non-existent paths** —
including `THESIS_DATA_DIR`, `THESIS_RESULTS_DIR` and every raw/converted/
engineered tier. 87 files import PATHS (about 40 live, the rest archived).

`import PATHS` still succeeded, which is exactly why this was invisible: the
constants are `Path` objects, and `Path` construction never validates. Nothing
fails until a script actually reads or writes. **This vindicates
DEC-P0046-PATHS more sharply than the original argument did**: the value of
centralisation here was not tidiness, it was that one file had to be repaired
instead of forty, and that a single probe could enumerate the whole blast radius.

Worth adding to the plan's own practice: a `PATHS.py` self-check that asserts
every `*_DIR` exists (excluding documented placeholders) turns this class of
breakage from silent into loud. Proposed for Phase 6 alongside the manifest.

### Three constants removed rather than repointed

`model_serving_interface/` and its `system_a_forecast/`,
`system_b_conversational/`, `srq2_synthesis/` subfolders no longer exist as live
code — `forecast_service.py`, `srq2_synthesis.py` and `srq2_agent.py` are all in
`.archive/superseded_scripts_2026-08/`. SRQ2's live surface is now
`02_SRQ2_Tool_Interface/forecast_tool.py`. The constants were **removed**, not
repointed, because there is no live directory to point at — and a constant
resolving to a missing path is precisely how this breakage went unnoticed.
`THESIS_DATA_ASSESSMENT_DIR` was removed for the same reason.

## F20 — `05_thesis_results/` slugs and the SRQ4 run split (executed)

Per Brian's instruction, results folders now carry descriptive slugs, and SRQ4's
per-run material moved to live beside the harness that produced it:

- `srq1/` -> `srq1_model_performance/`
- `srq2/` -> `srq2_structured_tool_interface/`
- `srq4/` -> `srq4_scenario_experiments/`
- new: `srq3_integration_readiness/`, `diagrams/`, `eda/`
- `srq4_scenario_experiments/{run_*,raw_responses}` ->
  `04_SRQ4_Scenario_Experiment/runs/`

This **settles the open question** from Session 2 (fold `srq4/` run folders under
`raw/`, or not). Brian's answer is better than either option I offered: the runs
do not belong in the results tier at all. `srq4_scenario_experiments/` now holds
exactly the 5 aggregation files (`summary.md`, `runs.csv`,
`interval_communication.{csv,md}`, `RESULTS_2026-08-19.md`), and the 4 run
folders sit with the harness.

The generalised rule (DEC-P0046-RUNS-WITH-EXPERIMENT): **raw per-run material
lives with the experiment; only the aggregation across runs reaches the results
tier.** This also answers what `raw/` would have contained for SRQ1/SRQ2, which I
could not answer in Session 2 — the answer is nothing, because `raw/` was the
wrong idea. The per-SRQ shape is `figures/`, `tables/`, `models/`; no `raw/`.

## F21 — EDA split: .csv stays, .md and .png promote

**Decided by Brian, 2026-09-06.** My Session 2 proposal (keep all ~240 EDA files
at the pipeline, promote a hand-picked few) was the wrong cut. Brian's cut is by
*file type*, and it follows from what consumes each:

- **`.csv` stays in `pipeline_step_outputs/`** — downstream EDA steps read them
  (structural breaks, ADF-per-brand feed data-handling decisions). They are
  pipeline plumbing.
- **`.md` tables and `.png` plots promote to `05_thesis_results/eda/{category}/`**
  — they are generated *to be read*, i.e. report material.

Volume: ~30 `.md` + 8 `.png` = 38 per category, ~150 across four categories. Not
the ~240 I feared, because the CSVs are the bulk of it.

Why this is better than my version: my "promote only thesis candidates" required
a human decision per file *before* the citation sweep, which is the wrong order.
A type-based rule is mechanical, needs no judgement, and still leaves the picking
to humans browsing the results tier — which is the whole point of F14.

## F22 — Clean-repo boundary corrected

I wrote in F14 that the rule reduces to "tiers 00-04 ship, tier 05 does not".
**Wrong.** Brian: tier 00 is the AI-guided writing harness and is excluded too.

The correct boundary, after the F19 renumbering:

- **Ships**: `01_SRQ1_...` through `05_thesis_results/` — the four SRQ tiers and
  the results.
- **Excluded**: `00_thesis_context/` (research questions, methodology notes,
  compliance working notes) and `06_thesis_writing/` (Zotero, snapshots,
  notebookLM, drafts).

The shipped set is exactly *the work*: the SRQs and what they produced. The
excluded set is exactly *the apparatus for writing about the work*. That is a
cleaner line than the one I drew, and it strengthens F14 rather than weakening
it — the artefact rule matters more, not less, when two tiers are excluded.

## F23 — SPSS/Indeks Danmark removed, and the claim it leaves behind

**Decided by Brian, 2026-09-06:** the Indeks Danmark consumer-survey dataset was
never used and will not be in the 9 days to submission. Executed:

- Data archived to `.archive/spss_indeksdanmark_2026-09/` with a README
  (real licensed source data, so archived rather than deleted).
- All four `PATHS.py` SPSS constants removed. Three of the four already resolved
  to non-existent directories before the archival — only `_00_raw` ever existed.
- No live script referenced any of them (verified by grep excluding `.archive/`).

### The part that is not just cleanup

**The thesis still claims this dataset as part of its empirical base.** Two lines
in the abstract:

> "deployed on Danish CSD retail data (Nielsen CSD panel + **Indeks Danmark
> consumer survey**)"

> "Single empirical context: Danish CSD retail, Manifold AI / Nielsen CSD panel,
> **Indeks Danmark consumer survey**"

Present in `06_thesis_writing/sections-drafts/abstract.md` (lines 40, 56) **and
in the 2026-09-05 `.docx` snapshot** — i.e. in the authoritative prose, not just
a draft note.

Since the data was never used, these describe a data source that informs no
result in the thesis. That is a factual claim about method that does not hold —
materially different from a stale figure, and it is in the abstract, which
examiners read first. Correcting it means editing the `.docx`
(`.claude/rules/writing-surface-authority.md`), not the draft `.md`.

Flagged here rather than acted on: prose edits need Brian, and the bullets-first
rule applies.

### Related, not actioned

`utility_scripts/scripts/ml_retraining/01_ingest_raw.py` ingests Indeks from
`PROJECT_ROOT / "Thesis" / "indeksdanmark"` — a path gone since P0028
(2026-07-11). The whole `ml_retraining/` folder is an April-era pipeline
superseded by `01_SRQ1_Model_Training/`. Left in place: it was broken for
reasons predating this change, and archiving it is a separate decision.

## F24 — `PATHS.py` is clean; three scripts bypass it and are still broken

**Verification state after the SPSS removal: 39 of 39 `*_DIR` constants resolve.
Zero missing.** `print_all_paths(verbose=True)` runs clean. No live script
imports a removed constant.

But constants resolving is not the same as scripts running. Three live scripts
hold **hardcoded old-tier strings** and so are unaffected by the PATHS repair:

| Script | Line | Holds | Effect |
|--------|------|-------|--------|
| `05_thesis_results/generate_figures.py` | 16 | `OUTPUT_DIR = "05_thesis_writing/figures"` | writes to a path that no longer exists |
| `06_thesis_writing/figures/generate_systemB_diagram.py` | 14 | same | same |
| `utility_scripts/scripts/generate_systemB_diagram.py` | 14 | same | same (the shadow copy, F8) |
| `utility_scripts/scripts/zotero_client.py` | 270 | `parents[2] / "05_thesis_writing" / "citations"` | **new find** — Zotero writes would land in a dead path |
| `utility_scripts/scripts/thesis_snapshot.py` | 73-74 | `REPO_ROOT / "05_thesis_writing" / ...` | **new find** — the snapshot tool is broken |

The last two were not in the Phase 3 list, because Phase 3 was scoped to figure
and table generators. They surfaced only from grepping for the literal old tier
names rather than for PATHS imports.

**This is the same lesson as F19, one level down.** The scripts that broke
silently are exactly the ones that did *not* route through `PATHS.py`. The three
figure generators were already known offenders (F8); `zotero_client.py` and
`thesis_snapshot.py` are two more of the same kind. Every one of them would have
failed at run time with no warning at import.

Note `thesis_snapshot.py` matters beyond itself: it generates the
`docx-exported-snapshots/` mirror that the whole comment-audit workflow reads.

**Consequence:** the Phase 3 remainder now covers five scripts, not three, and
the DEC-P0046-PATHS invariant should be stated as a check, not an aspiration:
*no live script contains a literal tier-folder name.* That is greppable, and it
belongs beside the F19 self-check in Phase 6.

## F25 — Full hardcoded-path sweep: 43 scripts -> 10, all survivors legitimate

A regex audit of every live `.py` (excluding `.venv/`, `.archive/`, `plans/`,
agent config) for five defect classes: literal tier names, `CLAUDE.md` anchors,
`parents[N]` root hops, absolute paths, and the dead `"Thesis"` segment.

**Before: 43 scripts. After: 10.** All 77 live scripts compile.

### The `CLAUDE.md` -> `.env.example` anchor swap

Brian's reason: the repo ships to assessors, and an anchor filename that names
the assistant is not something to hand over. Executed across 7 scripts plus the
shared finder.

Two defects were found while doing it, neither of which was the anchor itself:

1. **`.gitignore:15` (`.env.*`) excluded `.env.example`.** An anchor that is not
   committed cannot anchor a fresh clone — the exact clean-repo case this change
   exists to serve. Added `!.env.example` with a comment saying why. Without
   this, the swap would have been *worse* than `CLAUDE.md`, which at least was
   committed.

2. **Every inline finder walked up from `Path.cwd()`, not `__file__`.** So the
   root resolved from wherever python happened to be invoked, and any run from
   outside the repo failed. Now anchored on `__file__`; verified by resolving
   correctly from an unrelated working directory.

The shared `dynamically_find_root_directory.py` was rewritten as a documented
`find_project_root()` with an anchor tuple `(".env.example", ".env", "PATHS.py")`
— three fallbacks, so a missing `.env` on a teammate's clone is not fatal.

### `parents[N]` hops replaced in 17 scripts

`_REPO_ROOT = Path(__file__).resolve().parents[4]` encodes folder *depth*. The
2026-09-06 restructure changed depth for most of the tree, so these silently
pointed at the wrong directory — same failure class as F19, one level down.
Replaced with `_find_repo_root()`.

### What is left, and why each is fine

| Script | Finding | Verdict |
|--------|---------|---------|
| `PATHS.py` (7 tier literals) | literal tier names | **correct** — it is the authority; the names must be written down exactly once, here |
| `dynamically_find_root_directory.py` | `"CLAUDE.md"` | docstring explaining the swap, not an anchor |
| `thesis_snapshot.py` (2 abs paths) | `C:\Users\brian\OneDrive\...` | the OneDrive `.docx` default + a usage example. Outside the repo by nature; `--source` overrides it |
| `training_report.py`, `srq4_experiment.py` | `parents[1]` | resolving a *sibling* directory, not the repo root — correct relative use |
| `audit_datasets.py` | `parents[2] / ".csv"` | local output dir, unaffected by tier layout |
| 3 `nielsen_data_exploration`-family scripts | `parents[1]` | **dead already** — they import `thesis.ai_research_framework`, a module removed long ago. Pre-existing, unrelated to paths |

### `ml_retraining/` archived rather than repointed

11 scripts, `00_setup.py` .. `10_publication_figures.py`, all reading
`PROJECT_ROOT / "results" / "phase1" / ...`, `data/raw/`, and
`PROJECT_ROOT / "Thesis" / "indeksdanmark"`. **None of those directories exist**
— `Thesis/` went in P0028 (2026-07-11), `data/` and `results/` never existed in
this repo.

Repointing them would have manufactured `PATHS.py` constants for folders nobody
maintains — the failure mode this plan exists to remove, and the same reasoning
that deleted the `THESIS_MODELLING_SERVING_*` constants in F19. Archived to
`.archive/ml_retraining_2026-09/` with a README.

### The rule is now checkable

DEC-P0046-PATHS can be stated as a test rather than an intention: **no live
script contains a literal tier-folder name, a `CLAUDE.md` anchor, or a
`parents[N]` repo-root hop.** The audit script is the check. Belongs in Phase 6
beside the manifest and the `PATHS.py` self-check.

## F26 — `generate_systemB_diagram.py` diagrams the abandoned writing system

Brian's suspicion about "System A/B" scripts was right, and sharper than
expected. `generate_systemB_diagram.py` renders a multi-agent **thesis writing**
system: Thesis Coordinator, Planner Agent, Writing Agent ("Bullet points only
(never prose)"), Critic Agent, Outline Agent, APA Citation Agent, Thesis Writer
Agent.

That is the abandoned writing-agent promise, not the SRQ2 tool interface or the
SRQ4 scenario harness the thesis actually presents. A repo-wide search for its
output filename `system_b_overview` returns **three files: the script, its shadow
copy, and this plan. Zero chapters.**

Handled per Brian's sequencing (fix paths first, decide keep/adapt/delete after):

- Relocated `06_thesis_writing/figures/generate_systemB_diagram.py` ->
  `05_thesis_results/` (no generator may live in, or write to, the writing tier)
- Repointed to `THESIS_RESULTS_DIAGRAMS_DIR`
- Added a **staleness warning docstring** naming F26, so the next reader cannot
  mistake it for current
- Archived the byte-identical shadow copy (F8) to
  `.archive/shadow_scripts_2026-09/`

**Recommendation for Phase 3b: DELETE.** It depicts a system that was not built,
nothing cites it, and its existence in a shipped tier invites a defence question
about an artefact that does not exist. Kept for now only because Brian asked for
the keep/adapt/delete call to come after the paths were fixed.

`generate_figures.py`'s six diagrams are a different matter — those depict the
real architecture and are worth updating rather than dropping (F2, F5).

## Open questions for Brian

1. **Deferred to Phase 5** — the 18-row restore-or-retire table (F12), fillable
   once the citation sweep says which figures the chapters cite. Note these files
   are now at `06_thesis_writing/analysis/figures{,_agentic}/`.

2. **New, from F19** — `srq1_model_performance/` and
   `srq2_structured_tool_interface/` are, in Brian's assessment, stale to unknown
   degrees (srq2 still carries LLM-as-Judge output from a dropped design). The
   staleness triage is Phase 3b's real work; `appendix/` and
   `srq4_scenario_experiments/` are believed current.
