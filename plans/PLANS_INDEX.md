# Plans Index

> **Scheme updated 2026-06-22**: Flat folder layout replaces status-bucket folders.
> New plans: `plans/P{NNNN}_YYYY-MM-DD_HH-mm_<slug>/`
> Archived plans: `plans/.archive/`
> Status tracked in plan frontmatter only — no outcome files, no folder movement on status change.
> Next available P-ID: **P0052**
>
> **P-ID note (resolved 2026-09-07):** two folders were named `P0046_*`. The
> exogenous-enrichment one renumbered itself to **P0047** in its frontmatter
> (folder name unchanged) because `P0046_..._figure-table-provenance-centralisation`
> owns the `DEC-P0046-*` decision IDs referenced elsewhere. **Both are now in
> `.archive/`**, so the collision no longer affects any active plan — but P0047
> is taken despite no `P0047_*` folder existing, and the two archived folder
> names still both begin `P0046_`.

---

## Active Plans

### Focus / In Progress

| P-ID | Folder | Status | Detail |
|------|--------|--------|--------|
| **P0048** | `P0048_2026-09-07_13-51_remaining-prose-and-results-citations/` | in_progress | **Remaining prose + working results into the text as citations.** Chapter-by-chapter prose pass from ch4 onward, verifying facts against `05_thesis_results/` first. **Written as a handoff across an account switch — read `START_HERE.md` first; the originating session is unrecoverable.** Headline finding (F1): the H1/H3 forecast horizon **never reaches feature construction** — `engineer_features()` has no `horizon` parameter, lags are `shift(lag)` at both horizons, and merging the two CSD matrices shows every lag column identical across all 4,370 shared rows. So both matrices are one-month-ahead tasks and **the thesis reports one-month accuracy while describing a three-month horizon**; the published numbers come from the h3 file (row counts 1805/665/95 match `summary.md`), and no H1 results exist at all — zero `_h1` references in SRQ1 code. Also: the split is proportional 70/15/remainder and recomputed, **not** locked (F4, confirming Brian's own threads 183/185/187/191); the feature count is **13, not 14** — `weighted_distribution` is not a model input, confirmed against the trained artefacts (F3); MIN_PERIODS is now *derived* as `warmup+horizon+1`, which **retracts** a stated limitation (F6). Two prose blocks are paste-ready and close **8 Word threads**; the horizon blocks are declared blocked on a code fix + full re-run. Cross-cutting: the thesis cites **2 figures** against ~317 result files. |
| **P0049** | `P0049_2026-09-07_17-50_finalizing-experiments/` | in_progress | **Finalizing experiments — the consolidation plan for the account switch.** Absorbs P0039/P0040/P0042/P0044, which are now archived; their live content is in `INHERITED_CONTEXT.md` (five-scenario ladder, DEC-VENDOR still open, DEC-RSS/DEC-SUBPROCESS/DEC-REFIT-NOT-RETUNE, the delivered A/B/C results, the frozen 111-run design). **Read `START_HERE.md` first.** Two headline facts: SRQ1 numbers are now deterministic (`XGB_N_JOBS=1`, F18) and the model-equivalence verdict survived (F19) — but `engineer_features()` never receives the horizon, so h1/h3 are the same one-month task and published results are **H1 mislabelled as H3** (F22, independently reproduced). The horizon fix is upstream of the ~111 funded runs. Also fixed: `forecast_tool.py` read its track record from the wrong directory inside a try/except, silently serving forecasts with **no** `historical_*` fields — that would have invalidated the B→C comparison the funded runs exist to measure (F21). |
| **P0050** | `P0050_2026-09-07_18-40_figure-table-generation-and-provenance/` | in_progress | **Figure, table and diagram generation — the consolidation plan for the account switch.** Supersedes the figure/table half of P0046. **Read `START_HERE.md` first.** 11 diagrams and 25 appendix tables regenerate from 5 producer scripts **in any order**, every value read from an artefact at render time, no duplicate filenames, and zero leaked filenames/step numbers/plan IDs (checked mechanically over the rendered SVGs). A house style is now a written contract at `.claude/rules/figure-generation-standards.md` — horizontal layouts (the appendix prints landscape), bold box headers, greyscale contrast tiers, transparent grounds, submission-ready captions. Three claims that read as measured were corrected against the code: the **8 GB** envelope (it is 4 GB), Ch5's **five-model** substrate and agentic layer (the ladder is four; the layer exists nowhere), and **18** EDA sections (counted: 16). Also caught a collision it had itself introduced — the new literature table at prefix `89` was being silently deleted by the appendix exporter's `<= 89` cleanup, surviving only by run order. **Inherited blocker:** the reduction table's horizon column carries a DO-NOT-PUBLISH warning until P0049's horizon fix lands. **Next: Phase 5 — publish the inventory, THEN choose citations, never the reverse.** |
| **P0051** | `P0051_2026-09-08_00-00_eda-diagnostics-provenance/` | pending | **EDA diagnostics computed but never consumed.** Per-brand ADF `recommendation` and per-feature skewness are reported and read by nothing; a global `log1p` is applied from a hardcoded constant and ARIMA uses a fixed `d=1`. Mainly a Ch4 prose-honesty task, not a modelling fix. Split out of P0050 on 2026-09-08. |
| **P0052** | `P0052_2026-09-08_14-45_snapshot-dynamic-chapter-naming/` | in_progress | **The Word export names chapters by number, so the Ch5/Ch6 swap silently inverted every filename.** `chapters/ch5-framework-design.md` now holds *Model Benchmark* and vice versa. Already producing false data: the drift table reports **+1,815 / -1,838** word deltas that are pure mispairing (benchmark chapter diffed against architecture draft), which the code's own comment calls *"worse than reporting none"*. Root cause: `CHAPTER_MAP` encodes identity twice, by number AND by title, and `startswith` anchoring means only the number key can ever match a prefixed heading. **`PATHS.py` already solves this correctly** (slug names the subject, number derives from position) -- this is a port, not a design exercise. Also fixes a pre-existing defect: ch7/ch8 have **never** appeared in a drift table because their draft filenames never matched. Investigation complete, no code changed. **Decide the Open question in `task_plan.md` before writing anything.** |
| **P0053** | `P0053_2026-09-08_15-40_vps-hpc-model-training/` | in_progress | **SRQ1 training moved laptop -> VPS -> CBS UCloud HPC.** The H=3 suite ran there on the 18-feature codebase (`0e95850`) and covers all four categories -- verified against `summary.md`. F1: a category-name casing bug silently dropped Danskvand/Energidrikke on Linux, patched across 9 scripts. **F6 (2026-09-10): a tenth script, `training_report.py`, still carries it** -- its report claims two categories have no feature matrix, and it is an appendix candidate, so it contradicts Ch4 as written. Two capital letters plus one re-run; NOT a retrain. **F7: the redundancy appendix tables (97, 98) predate the 18-feature set** -- their cluster file is dated 2026-09-06, three days before `3f8b0a9`, and Ch4 §4.3 cites its 26.4/28.8 figures today. `srq1_feature_diagnostics.py` already imports the shared list, so re-running needs no code change. |
| **P0054** | `P0054_2026-09-10_15-35_submission-ready-repo/` | in_progress | **The assessor-facing repo copy: procedure + `/submission-export` skill, built now, executed at code freeze.** Survey found **54 of 69** pipeline `.py` files carry an internal marker (211 plan IDs, 185 dates, 134 finding IDs, 101 `DEC-` codes) but **zero** `TODO`/`FIXME` -- the comment *quality* is good, so a mechanical strip would destroy more than it removes; the pass is per-file and judgement-driven. Biggest tell is not any marker but **docstring length plus banner headers** (`WHY THIS EXISTS`, `ROUTING`), which grep cannot find. Agrees independently with the existing `DEC-P0046-SHIP-SCOPE`, and goes further: drops `plans/`, `user-docs/`, `.claude/`, `.agents/`, `.archive/` and all of `utility_scripts/`. **Q1 is the open decision that changes the deliverable** -- CLAUDE.md forbids committing Nielsen data while `.gitignore` tracks the engineered matrices deliberately; recommendation is ship no data, with a synthetic sample if time allows. Fresh git history, one commit: the 500+ existing messages are themselves meta. |
| **P0046** | `.archive/P0046_2026-09-05_20-40_figure-table-provenance-centralisation/` | archived | **Archived 2026-09-07, superseded by P0050**, which carries all 28 findings forward (verified before archiving). Kept as the working record — three of its findings document reasoning errors worth re-reading in full: recommending a restore because a draft cited it (F8), patching diagram labels twice before questioning the frame (F18), and Brian's method correction in his own words (F19). Do not resume here; see `SUPERSEDED.md` in that folder. |

### Blocked / Paused / Backlog

None. **Verified 2026-08-20:** the rows previously listed here (P0001-P0005, P0019,
P0020) reference folders that exist neither in `plans/` nor in `plans/.archive/`.
They were removed from disk without the index being updated, so the index was
advertising plans that could not be opened. If any of that work is still wanted it
needs a fresh P-ID, not a resurrected row.

---

### Archived 2026-09-07 — absorbed into P0048

| P-ID | Was | Absorbed into |
|------|-----|---------------|
| **P0045** | `draft-bullet-reconstruction` | **P0048 tasks 11–16.** 6 of 11 tasks were open (ch3/ch6 MERGE, ch4/ch7/ch8, short files, verify). Delivered the Claims/Warrant/Evidence/Open contract, phase 2 (hollow 22→14), the corrected hollow detector, and F5 — ch6 passes `check_chapter_facts.py` while every headline number is stale. |
| **P0047** | `exogenous-enrichment-decision` (folder `P0046_…21-10`) | **P0048 tasks 9–10.** Experiments finished, numbers locked: holiday enrichment shipped (7/12 helped, mean −1.42 pp, reported as a per-model split, never the mean). 19 of 22 tasks complete; the 3 remaining were Brian's writing-side items. Its determinism contract (`XGB_N_JOBS=1`) lives on in `LOCKED_STATE.md` and P0049 depends on it. |

Live state from both is in
`P0048_…/INHERITED_CONTEXT.md` — read that rather than the archived folders.

### Archived 2026-09-07 (second sweep) — index corrected

These seven were moved to `.archive/` by a parallel session without the index being
updated, so the index was again advertising plans that could not be opened — the exact
failure the note below records from 2026-08-20. Rows removed 2026-09-07.

**P0043, P0042, P0041, P0040, P0039, P0037, P0034** — see `.archive/` for each. Their live experimental content was
consolidated into **P0049** (`INHERITED_CONTEXT.md`); their writing-side content into
**P0048**.

## Archived Plans

See `plans/.archive/README.md` for the full list. Archived: P0006-P0018, P0022-P0033, P0035, P0036, P0038.

**Every archived plan carries a terminal status** (`complete`, `cancelled`, or deliberately
`paused`) — verified 2026-08-20. Only P0025 and P0027 are archived while non-terminal
(`in_progress` / `paused`); both were superseded rather than finished.

---

## How to Create a New Plan

1. Next P-ID: **P0052**
2. Create folder: `plans/P0023_YYYY-MM-DD_HH-mm_<slug>/`
3. Create files: `task_plan.md`, `findings.md`, `progress.md` (use `/planning-with-files` skill)
4. Add to this index
5. Set frontmatter: `pid`, `created`, `updated`, `status`, `focus_detail` (if applicable)

## How to Archive a Plan

Move entire folder to `plans/.archive/` and update this index.

---

**Last updated**: 2026-09-08 (P0052 created — the snapshot exporter keys chapter identity off the chapter NUMBER, so the Ch5/Ch6 swap inverted every snapshot filename and the drift table is reporting mispairing as data; P0048 F14 records the swap plus 37 verified prose cross-reference repairs, and archived snapshots were untracked from git, 1,306 files). Previously 2026-09-08 (P0051 created — EDA diagnostics computed-but-unconsumed, split out of P0050; P0048 phase 8 chapter swap verified and given an execution recipe). Previously 2026-09-07 (P0046 archived into `.archive/` after folding its live state into P0050 — the three quarantined diagram archives and why each is unusable, SRQ2's two producerless files, Enrico's 18 unresolved figures, and two environment traps. Active plans are now three, one per concern: P0048 prose, P0049 experiments, P0050 figures.) 2026-09-07 (P0050 added — figure/table generation consolidated for the account switch; supersedes P0046. House style written as a rule; 11 diagrams + 25 tables regenerating in any order; three code-contradicting claims corrected.) 2026-09-07 (P0046: diagrams rebuilt from code after verifying they described a system that was never built; pipeline logging audit opened; method corrected to inventory-before-citations.) 2026-09-06 (P0046 architecture reversed: tier 05 holds no artefacts; `04_thesis_results/` becomes the single home for every figure and table, routed by producer tier. Also found a second orphaned output, `phase3_region_grain_test/phase3_result.json`, that P0035 left behind when it archived the producing script.) 2026-09-05 (P0046 added -- figure/table provenance + centralisation; Phase 1 trace and Phase 2 decisions landed same day. Found one zombie artefact whose producing code P0035 deleted, and a figures-vs-tables date split inside `04_thesis_results/srq1/`.) 2026-09-01 (P0043 added -- Word/Excel comment audit workflow for revision rounds; blocked on locating the reviewed .docx, since no repo copy carries comments.) 2026-09-01 (P0042 gate 1 frozen for A/B/C; see its findings F1-F6). 2026-08-22 (P0041 added -- citation sourcing register, maintained alongside P0040 rather than replacing it: every methodological claim needing an academic source, tracked as VERIFIED / PROSPECTIVE / UNSOURCED / UNSOURCEABLE for export to NotebookLM. Prompted by an unsourceable "50-200 HPO trials" claim caught before it reached the prose.) (2026-08-20: P0040 added — Prometheus scenarios D/E, now the focus. P0039's A/B/C ladder delivered its first paid results and drops to secondary. Index tables rewritten: they had listed P0022-P0038 as active while those folders were already archived on disk.)


---

## Archived 2026-09-07 — absorbed into P0049

P0039, P0040, P0042 and P0044 were consolidated into **P0049** and moved to
`.archive/`. Each keeps `superseded_by: P0049` and a reason in its frontmatter.

**Read `P0049/INHERITED_CONTEXT.md`, not the archive.** The archive is provenance; the
consolidation is the working copy, and it corrects three stale claims those plans
carried (P0039's `.env` blocker, P0042's "unblocked" funded runs, and two moved results
paths).
