---
pid: P0046
created: 2026-09-05 20:40:00
updated: 2026-09-06 16:00:00
---

# P0046 — Progress Log

## Session 1 — 2026-09-05 20:40

**Branch:** `thesis/draft-bullet-reconstruction` (inherited from the P0045
session; this plan did not create a branch of its own. Worth splitting if
Phase 3+ execution starts, since P0045's working tree is already dirty.)

**Goal for session:** trace and classify every figure/table Brian listed; do not
move or delete anything yet.

### Done

- Created plan folder `P0046_2026-09-05_20-40_figure-table-provenance-centralisation`.
- Phase 1 complete. Findings F1–F10 written.
- Classified the listed artefacts. Headline counts:
  - **LIVE / healthy:** the four-category EDA layer (~240 files) and the
    12-table appendix. Both fully regenerable, both current.
  - **REGENERABLE-STALE:** `fig1_model_ladder`, `fig3_forecast_overlay` (both
    2026-07-11, while their sibling tables are 2026-08-24), plus
    `system_architecture_v1`, `data_flow_v1`, `ram_budget_v1`.
  - **ZOMBIE:** `fig2_granularity.png` — producing code deliberately removed by
    P0035; depicts a comparison the project decided to stop making.
  - **ORPHAN-CONCEPTUAL:** `ch2_gap_diagram`, `ch5_architecture_v1`.
  - **ORPHAN-DERIVED (cannot ship):** `05_thesis_writing/analysis/figures/` (11)
    and `analysis/figures_agentic/` (7) — traced to Enrico's archived notebooks.
  - **ORPHAN + stale content:** `ch1_research_questions_tree`.

### Key realisations

1. Brian's guess that some artefacts are "AI-generated with no source" was
   close but not quite right for the `analysis/` sets — they *had* a real
   producer (Enrico's notebooks), it was just archived and machine-pinned. The
   practical consequence is the same (unrunnable), but the framing matters for
   how they get cited or retired.
2. Three of the four "needs information update" figures are regenerable, meaning
   their fix is editing graphviz node labels, not redrawing. Much cheaper than
   the triage folders implied.
3. The most dangerous artefact found (`fig2_granularity.png`) was in the *right*
   folder with the *right* name. This is the argument for a provenance manifest
   over a tidier folder tree — see findings F10.
4. `ram_budget_v1` must NOT be fixed by simply re-running `generate_figures.py`:
   the script still contains the fabricated numbers P0040 F5 flagged. Real
   measurements now exist in the appendix and it needs rewiring to them.

### Not done / deliberately deferred

- No files moved, deleted or regenerated. Phase 2 is blocked on Brian's answers
  to the four open questions in findings.md.
- In-text thesis tables not yet diffed against generated artefacts (Phase 5).
- Danskvand and RTD have 7 EDA plots vs CSD/Energidrikke's 8 — noted, not yet
  explained.

### Errors

| Error | Attempt | Resolution |
|-------|---------|------------|
| `grep -rIl` over the repo root exceeded the 120s Bash timeout | 1 | Z: is a slow network drive for full-tree walks. Switched to the Grep tool (ripgrep-backed, honours ignore files) — returned in ~2s. Recorded for `/errors-log`. |

### Session 1b — Brian's decisions (same evening)

Brian reviewed the findings and settled three of the four open questions. Written
up as F11, F12, F13; Phase 2 closed; Phases 3-7 rewritten to match.

**What changed in the plan as a result:**

1. **F11 — the appendix folder is not exempt.** I had held up
   `04_thesis_results/appendix/` as the model to copy (F7) without noticing that
   under Brian's own contract it is a *production* site, not a publication one.
   Its name made it look like a destination. Brian caught this: "the scripts
   writing the current appendix folder should also follow the same logic." The
   sharpened invariant is that **no generator writes into tier 05** — only the
   curation script does. That single-writer rule is what makes the manifest
   trustworthy, so it is worth more than the folder layout it implies.

2. **F12 — the ORPHAN-DERIVED verdict was too blunt.** I wrote that those 18
   files "cannot ship", which is true of the files but slid into implying the
   notebooks were unusable. Brian pushed back correctly: they are archived, not
   broken, and the blockers (a macOS `FIGURE_DIR`, a pre-four-category scope) are
   edits. So the class now has two exits, RESTORE and RETIRE, decided per file —
   with the pairing rule that RETIRE archives the image too, since a stale image
   left in a live folder is precisely the `fig2_granularity` trap.

3. **F13 — PATHS centralisation accepted**, and reading the file end to end
   turned up an extra defect: the tier-map docstring at `PATHS.py:28` still lists
   `sections-final/`, archived 2026-09-01. The file that exists to be the
   authority on repo layout is advertising a directory that no longer exists.

**Phase ordering consequence:** Phase 5 grew a citation sweep and now feeds
Phase 2's leftover — the restore-or-retire table cannot be filled in without
knowing what the chapters cite. A new Phase 6 holds the curation script and
manifest; the style pass moved to Phase 7.

## Session 2 — 2026-09-06

**Goal:** settle the three open questions so Phase 3 can execute. All three
settled; the answer to Q3 reversed the plan's architecture, so Phase 2's design
is partly superseded before any of it was built. Nothing on disk changed.

### What was decided

1. **Q1 → generator** (F18). Straightforward; Brian agreed with the
   recommendation.

2. **Q2 → delete** (F17). Brian rejected archiving and asked me to help decide
   rather than just assert. Checking changed my answer: the file is committed at
   git `4c7a98b`, and a repo-wide search for the filename returns 9 files, all
   plan docs and generator copies — no chapter. My archive argument had been
   "an examiner might ask", which the clean-repo constraint kills outright: a
   tier-05 archive is never shared, so it protects against a reader who cannot
   see it.

3. **Q3 → tier 04 is the single home** (F14/F15). This is the significant one.

### The Q3 reversal, recorded honestly

Three destinations were proposed for the diagram generators inside a few hours:

| Proposal | By | Reasoning | Fate |
|---|---|---|---|
| `04_thesis_results/diagrams/` | me, F11 | one production site per writer | superseded, then re-adopted |
| `00_thesis_context/diagrams/` | me, revised | tier 04 is "results"; diagrams are context, and the production tree is what assessors read | **wrong** — tier 00 is not shipped either |
| `04_thesis_results/diagrams/` | Brian, F15 | tiers 00-04 all ship; artefacts must be findable in one place | adopted |

The middle step is the instructive error. I optimised for semantic fit inside
"the shipped tree" while getting the shipped tree's boundary wrong — the whole
revision rested on a premise Brian corrected in one line. The lesson recorded in
F15: **semantic fit is carried by the producer's location and the subfolder name,
not by which tier the output lands in.**

Brian's larger move was better than either of my proposals: drop the curation
layer entirely, so tier 05 holds no artefacts. He justified it by the sharing
boundary; the stronger justification (F14) is that it eliminates the second copy,
which is what the F11 manifest existed to police. Removing the thing the defence
was defending beats building the defence.

### Consequences for the plan

- Phase 3's destinations changed; three `THESIS_WRITING_*` constants dropped
  before being written — they would have institutionalised what F14 removes.
- **Phase 3b is new** (F16). Tier 04 is now the browse-and-pick tree, and it is
  not fit for that: `srq1/` has 36 loose top-level files, three of them
  differently-named metrics CSVs. Centralising the destination without a shape
  inside it relocates disorder rather than fixing it.
- Phase 6 shrank from "curation script + manifest" to "manifest as index". Its
  invariant flipped usefully: instead of *every tier-05 file has a manifest row*,
  it is now **every tier-04 artefact has a live producer** — which would catch
  both the F4 zombie and the F16 leftover automatically.

### Found while inspecting tier 04

- `04_thesis_results/phase3_region_grain_test/phase3_result.json` — P0035
  archived the region-grain script but left its output behind. Same class as the
  zombie: an artefact whose producer is gone.
- `04_thesis_results/__pycache__/` — clutter in what is about to be the
  deliverable tree.

### Errors

| Error | Attempt | Resolution |
|-------|---------|------------|
| `grep -rl` over the repo timed out at 120s **again** | 2 | Same Z:-drive cause logged in Session 1, and I reached for `grep` anyway despite having written the fix down. Used the Grep tool; it returned in seconds. The background job later completed and agreed exactly with the tool's results. Worth a `/errors-log` entry: the fix is known, the failure is that it was not applied. |

## Session 3 — 2026-09-06

**Context:** Brian restructured the repo to SRQ-aligned tiers between sessions
and asked for `PATHS.py` to be updated to match.

### The thing that mattered most was not the thing that was asked

The request was "update PATHS.py accordingly". Probing first turned up that
**32 of 34 directory constants were resolving to non-existent paths** — every
data tier, every results path, all of modelling. Every pipeline script in the
repo was broken, and `import PATHS` still succeeded, because `Path()` never
validates. Nothing would have failed until someone ran a pipeline and it wrote
to, or failed to find, the wrong place.

Checking before editing was what surfaced it; the request as phrased sounded
like routine bookkeeping.

### Done

- **`PATHS.py` rewritten** for the new layout. 43 constants, verified: 3 misses
  remain and all three are pre-existing SPSS placeholders documented as empty
  since before this session.
- **Removed rather than repointed**: `THESIS_MODELLING_SERVING_*` (x4) and
  `THESIS_DATA_ASSESSMENT_DIR` — those directories are genuinely gone, their
  scripts archived. Repointing them at plausible-looking paths would have
  recreated exactly the silent-breakage pattern being fixed.
- **New constants** for the SRQ tiers, the slugged results folders, the
  diagrams/EDA/appendix destinations, and the writing-tier subfolders.
- **New helpers**: `get_srq_results_dir()`, `get_category_eda_{plots,tables,results}_dir()`.
- **On disk**: results folders slugged; `diagrams/`, `eda/`,
  `srq3_integration_readiness/` created; SRQ4's 3 run folders + `raw_responses`
  moved to `04_SRQ4_Scenario_Experiment/runs/`, leaving exactly the 5
  aggregation files in the results tier.
- Smoke-tested `srq1_figures.py` and `export_appendix.py` compile.

### Where Brian's judgement beat mine, twice

1. **EDA split** (F21). I proposed keeping all ~240 files at the pipeline and
   promoting hand-picked candidates. Brian split by *file type*: `.csv` stays
   (downstream steps consume it), `.md` and `.png` promote (they are generated to
   be read). Better because it is mechanical — mine required a human decision per
   file before the citation sweep, which is the wrong order. It is also less
   volume than I feared: ~150, not ~240, since the CSVs are the bulk.

2. **SRQ4 runs** (F20). I offered fold-under-`raw/` or keep-as-is. Brian's answer
   was that runs do not belong in the results tier at all — they live with the
   experiment. This also retro-answers the question I could not answer in Session
   2 ("what would `raw/` hold for SRQ1?"): nothing, because `raw/` was the wrong
   idea.

And one correction: I had written the clean-repo boundary as "tiers 00-04 ship".
Tier 00 is excluded too (F22). The corrected line — the four SRQ tiers plus
results ship; context and writing do not — is cleaner than mine: the shipped set
is the work, the excluded set is the apparatus for writing about it.

### What F19 says about the plan's own thesis

DEC-P0046-PATHS was argued on tidiness grounds. This session gave it a sharper
justification: because the paths were centralised, **one file needed repair
instead of forty**, and a single probe enumerated the entire blast radius. The
counterfactual — 40 scripts each holding their own relative strings — would have
been discovered one crash at a time over weeks.

Proposed for Phase 6 as a result: a `PATHS.py` self-check asserting every `*_DIR`
exists apart from declared placeholders. That converts this class of breakage
from silent to loud, and it is the same shape as the manifest's "every artefact
has a live producer" invariant.

### Session 3b — SPSS removal + PATHS validation (same day)

**Done**

- Archived the Indeks Danmark/SPSS dataset to
  `.archive/spss_indeksdanmark_2026-09/` with a README recording what went and
  what it leaves open. Removed all four SPSS constants from `PATHS.py`.
- **`PATHS.py` now fully clean: 39/39 constants resolve, zero missing.**
  `print_all_paths()` runs. No live script imports a removed constant.

**Two findings worth more than the cleanup**

1. **The abstract still claims Indeks Danmark as an empirical source** (F23) —
   in the draft *and* in the authoritative `.docx`. Since the dataset was never
   used, that is a method claim that does not hold, sitting in the section
   examiners read first. Not actioned: prose edits are Brian's, in the `.docx`.

2. **Answering "what is left to validate in PATHS?" found more than expected**
   (F24). PATHS itself is done. But grepping for literal old-tier strings — a
   different search from "what imports PATHS" — turned up **five** live scripts
   with hardcoded dead paths, not the three already known. The two new ones are
   `zotero_client.py:270` and `thesis_snapshot.py:73-74`. The latter generates
   the `docx-exported-snapshots/` mirror the comment-audit workflow reads.

   Same lesson as F19 one level down: the scripts that broke silently are
   precisely those that do not route through `PATHS.py`. Worth stating
   DEC-P0046-PATHS as a greppable check — *no live script contains a literal
   tier-folder name* — rather than as an aspiration.

### Session 3c — Phase 3 completed: every script routes through PATHS

**Scope:** Brian asked for a sequential pass over every script, replacing
hardcoded paths with PATHS imports, plus the `CLAUDE.md` -> `.env.example`
anchor swap.

**Result: audit went 43 flagged scripts -> 10; all 77 live scripts compile;
39/39 PATHS constants resolve.** The 10 survivors are all legitimate and
individually justified in F25's table (PATHS.py's own literals, an explanatory
docstring, the OneDrive `.docx` default, sibling-relative `parents[1]` uses, and
3 scripts that were already dead for unrelated reasons).

**Two defects found while doing the anchor swap, neither being the anchor:**

1. `.gitignore`'s `.env.*` rule excluded `.env.example`. An uncommitted anchor
   cannot anchor a fresh clone — precisely the clean-repo case. Without catching
   this, the swap would have been *worse* than `CLAUDE.md`, which was at least
   committed. Added `!.env.example`.

2. Every inline finder walked up from `Path.cwd()` rather than `__file__`, so
   the root depended on where python was invoked. Fixed and verified from an
   unrelated cwd.

**`parents[N]` hops replaced in 17 scripts.** These encode folder *depth*, which
the restructure changed — the same silent-breakage class as F19, one level down.

**`ml_retraining/` archived, not repointed.** All 11 steps read `results/phase1/`,
`data/raw/` and `Thesis/indeksdanmark` — none of which exist. Repointing would
have created PATHS constants for folders nobody maintains, the exact failure this
plan removes.

**`generate_systemB_diagram.py`: Brian's suspicion confirmed** (F26). It renders
the abandoned multi-agent *writing* system — Thesis Coordinator, Writing Agent,
Critic Agent — not the SRQ2/SRQ4 artefact the thesis presents. Zero chapters cite
its output. Followed Brian's sequencing: relocated out of tier 06, repointed,
staleness warning added to the docstring, shadow copy archived. Keep/adapt/delete
is now a Phase 3b decision with a recommendation of delete.

**Writing note created** at
`06_thesis_writing/writing-notes/indeks-danmark-claim-must-be-corrected.md`, as
asked. Scope verified while writing it: the claim appears **only in the
abstract** (2 occurrences) — Ch3 and Ch4 are clean, so the correction is two
sentences, not a cross-chapter edit.

**One self-inflicted error worth noting:** my first `zotero_client.py` patch
inserted a module-level block inside a function body, and a second edit put a
closing paren after a comment. Both caught by the compile sweep immediately. The
lesson is that the sweep is the thing that made a fast mechanical pass safe —
worth keeping as a gate for any future bulk edit.

### Next session starts here

**Finish Phase 3** — now five scripts, not three (F24 added `zotero_client.py`
and `thesis_snapshot.py`); still small and mechanical,
then **Phase 3b**, which is the substantive work: the staleness triage of
`srq1_model_performance/` and `srq2_structured_tool_interface/`. Brian believes
`appendix/` and `srq4_scenario_experiments/` are current and the other two are
not — srq2 still carries LLM-as-Judge output from a dropped design.

Phase 4 must wait for 3b: regenerating into a layout that is about to change, or
regenerating artefacts that should be dropped, wastes the run.
