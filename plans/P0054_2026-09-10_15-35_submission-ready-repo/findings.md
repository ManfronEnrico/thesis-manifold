---
pid: P0054
created: 2026-09-10 15:35:00
updated: 2026-09-10 15:35:00
---

# P0054 findings — survey of the working repo, 2026-09-10

All counts measured on `main` at commit `71fe47b`, over the five shipping trees
(`01_SRQ1_Model_Training`, `02_SRQ2_Tool_Interface`,
`04_SRQ4_Scenario_Experiment`, `05_thesis_results`, `PATHS.py`), excluding
`__pycache__` and every `.archive/`.

## F1 — The meta-comment problem is narrower than expected, but nearly universal

69 pipeline `.py` files. **54 carry at least one internal marker.**

| Marker class | Sites |
|---|---|
| Plan IDs (`P00NN`, `P0038 task 3`) | 211 |
| ISO dates in comments | 185 |
| Finding IDs (`F63`, `F28/F38`) | 134 |
| Decision codes (`DEC-<NAME>`) | 101 |
| Change-history phrasing ("previously", "superseded", "no longer") | 27 |
| Names / collaboration | 12 |
| `TODO` / `FIXME` / `HACK` | **0** |

Heaviest files: `PATHS.py` (49), `srq4_experiment.py` (26),
`export_appendix.py` (21), `step_1_load_and_aggregate.py` (21).

**The comment *quality* is good.** This was the surprise. The comments explain
why a design was chosen over its obvious alternative, cite measured evidence,
and warn about correctness traps. Very little needs rewriting for substance —
the work is stripping labels and compressing over-long docstrings. Zero `TODO`
markers is itself evidence of a disciplined codebase.

**Implication for the plan:** a mechanical strip would destroy more value than
it removes. The pass is per-file and judgement-driven, which is why the skill
forbids sed.

## F2 — Length and banner headers are the strongest machine-written tell

Several file docstrings run 25–100 lines with section headers inside them
(`WHY THIS EXISTS AS A GENERATOR`, `ROUTING`, `CONVENTIONS`, `GRAIN HISTORY`).
No student writes a docstring with internal `----` headings.

This is a bigger tell than any individual marker, and grep cannot find it. It
is why Step 4 of the skill ends with "read the file top to bottom".

## F3 — `DEC-P0046-SHIP-SCOPE` already exists and agrees with the manifest

CLAUDE.md (rewritten during this session) records that tiers 01–05 ship to
assessors and tiers 00 and 06 do not. The manifest here was derived
independently from a file survey and reached the same split.

Where this plan goes further: it also drops `plans/` (427 tracked files),
`user-docs/` (94), `.claude/` (511), `.agents/` (419), `.codex/`, `.archive/`
(249) and all of `utility_scripts/` (27) — none of which that decision covers.

## F4 — The data question is a hard constraint, not a preference

CLAUDE.md states: *"Never commit Nielsen data. It is under a confidentiality
agreement and must not leave the local environment."*

But `.gitignore` carries a 2026-09-08 exemption tracking the engineered
matrices deliberately, with the reasoning written out: the VPS needed them to
train, and the decision was taken "with the repo's public visibility stated".

These two are in tension in the *working* repo, which is Brian's call and
outside this plan's scope. For the *submission* repo it resolves cleanly — the
assessors have no licence to the data, so shipping it serves nobody. Recorded
as Q1 in the task plan with three options and a recommendation.

## F5 — `utility_scripts/` is entirely droppable, with one check

Every file in it supports *writing the thesis*, not the pipeline being
assessed: Zotero sync and client, NotebookLM ingestion, Google Drive
integration, the docx snapshot exporter, draft hollow-section checks, citation
key setting, and two pytest suites for the first two.

One dependency to verify before deleting: `dynamically_find_root_directory.py`.
Six shipped scripts implement their own root-finder inline rather than
importing it, so the import probably does not exist — but Step 3 checks rather
than assumes.

## F6 — 17 code sites name a path that will not exist in the export

Comments and error messages referencing `plans/P0035/...`,
`writing-notes/unverified-claims-to-check.md`, `.claude/rules/...`,
`user-docs/reference/...`, `notebookLM/`.

Six of them are the same near-identical root-finder comment explaining why
`CLAUDE.md` is *not* the anchor. That is the one place a Claude reference is
functional rather than decorative — and in the export `CLAUDE.md` does not
exist, so the whole clause goes.

`PATHS.py` additionally defines constants for `06_thesis_writing/`,
`notebookLM/`, `sections-drafts/` and `plans/`. These must be **removed**, not
left pointing at absent directories — `path-handling.md` documents that a path
resolving to nothing degrades silently rather than failing.

## F7 — `README.md` is stale independently of this work

It documents the pre-2026-09-06 tier names (`01_thesis_research/`,
`02_thesis_data/`, `03_thesis_modelling/`, `04_thesis_results/`,
`05_thesis_writing/`) which no longer exist, and its "What This Repository
Contains" section is built around the System A / System B distinction — the
exact framing the export removes.

It also quotes SRQ1 baselines (XGBoost 45.5% median MAPE) that predate the
2026-08-18 leakage fixes and the move to H=3 as primary.

Not editable into shape. Step 5 replaces it. **The working repo's README is
also wrong today** and worth fixing separately, outside this plan.

## F8 — Git history is itself meta

500+ commits with messages like "docs: close chapter 4 -- all notes applied and
archived" and "fix: zotero export dropped computerProgram; add /re-snap skill".
The history narrates a Claude-assisted writing workflow.

The export starts fresh with one commit. This also sidesteps the confidential
matrices being recoverable from history after deletion, which a `git clone`
plus `rm` would not.

---

## Three requirements the SRQ4 work of 2026-09-10 places on the export

Written by the P0049 session, so this plan does not have to rediscover them.
All three are about files whose *absence* fails silently — the assessor gets a
repo that imports fine and cannot run.

### 1. `scenario_inputs/` — what it is actually for

`05_thesis_results/08_experimental_evaluation/scenario_inputs/` holds 12
per-brand CSVs, `index.csv` and a README, added 2026-09-10 (`127bbdf`). They are
already covered by the `05_thesis_results/**` SHIP row; nothing needs adding.

**One correction to how they were first described.** They are *not* what makes
scenarios A–C runnable. The harness builds every series at run time from
`_03_engineered/bymonth/**/*.parquet` via `_brand_history()` -- verified: three
`read_parquet()` calls, and no code path reads `scenario_inputs/`. Since this
plan already ships those 32 tracked matrix files, **A–C are runnable from the
parquet, and would be with or without the CSVs.**

What the CSVs are for is *inspection without execution*: an assessor can see
exactly what Scenario B was given, byte-for-byte, without running anything or
opening a parquet. `index.csv` additionally carries the held-out actual, which
is what lets a scored run be checked. Ship them as evidence, not as a
dependency.

**The check that does matter:** if a later decision reverses course and drops
the engineered matrices, A–C stop working, and `scenario_inputs/` would not save
them — a fallback loader would have to be written first. Worth stating in the
manifest so the dependency is explicit rather than assumed.

### 2. `prometheus_bridge.py` ships; Prometheus itself never does

`04_SRQ4_Scenario_Experiment/scenario_setup/prometheus_bridge.py` is new
(`a941927`) and is covered by the existing `scenario_setup/**` row. Keep it.

It contains **no credentials** (verified) and no vendor code. It holds one
absolute path to the engine, overridable by `PROMETHEUS_ENGINE_DIR`, and it is
written so that **importing it is allowed to fail**: an assessor with no
Prometheus gets scenarios D and E reporting `engine_unavailable` while A–C run
normally. That degradation is a shipped feature, so do not "tidy" the try/except
around its import in `srq4_experiment.py`.

`Z:\_dev-ssd\prometheus\**` is proprietary and outside this repo. It is not in
the SHIP list and must never be added.

### 3. Two `.env` questions the README must answer

The export ships `.env.example`, and an assessor reading it needs to know:

- **`OPENAI_API_KEY` alone runs scenarios A, B and C.** That is the reproducible
  tier, and it is the claim the README should make.
- **D and E additionally need Prometheus**, which is not distributable. Say so
  plainly rather than leaving an assessor to debug a missing engine.

Related open question for the README rewrite (Phase 3): the harness reads keys
under their OpenAI *dashboard* labels first, falling back to the standard names.
`.env.example` should show the standard name, since that is what an assessor
will set.

---

## F-SUBMIT — what ships, what is stripped, and the reproducibility claim to make

**Brian, 2026-09-11**, answering: *"We have to submit a repository with our thesis,
Prometheus will stay confidential, and sharing the aggregated brand snippets is also
technically confidential. Do you think it is okay to submit a cleaned up repo that is
not re-runnable?"*

### The answer: YES, and it is the normal outcome for licensed commercial data

A repository that cannot be re-run is defensible. One whose limitation is **discovered
by the assessor rather than declared by the authors** is not. The whole risk sits in
that distinction, so the README carries the declaration prominently rather than in a
footnote.

### Three things are tangled in the question and have DIFFERENT answers

| | What it is | Ships? |
|---|---|---|
| **Prometheus** | proprietary orchestrator, `Z:\_dev-ssd\prometheus\**` | **NEVER.** Was never vendorable. D, E and G are not reproducible by anyone outside Manifold, full stop. |
| **Nielsen brand-level data** | licensed retail panel under an NDA | **NO.** Note this includes the monthly CSV **embedded in cached prompt text** — see below, this is the live exposure. |
| **Aggregated results** | forecasts, APEs, latencies, token counts, costs, outcome classes | **YES.** Derived statistics, not the licensed data, and exactly what an assessor needs. |

### The recommendation

**Ship:** the code, the prompts (`prompts.py` in full — it is the experiment's method),
the results tables, and the run metadata.

**Strip:** the prompt and answer TEXT from cached responses in `raw_responses/`.

**Keep inside those cached files** the trace fields that carry the audit evidence:

- tool-call spans and `args_match_request`
- code-block presence and count (`code_calls`, `wrote_code`)
- `prompt_schema_id`
- `deviates_from_model`, `model_forecast`, `payload_complete`
- `sql_calls`, `usage_reported`, outcome class, token counts, latency

**This preserves the auditability claim the thesis rests on without shipping the data.**
The claim is that every forecast is traceable to a verified tool call — that is a property
of the trace, not of the prompt text. An assessor can confirm Scenario C called the tool
with the right arguments, that E made no warehouse query, and that F overrode the model,
without reading one row of Nielsen data.

### Scale of the exposure

The 2026-09-11 seven-arm smoke directory alone is **9 MB**, and every raw response embeds
the brand's monthly sales CSV because it is pasted into the prompt. **The results tables
are not the disclosure risk; the cached prompts are.** A strip pass must therefore be
keyed on the prompt/answer fields specifically, not on file size or directory.

Earlier run directories under `04_SRQ4_Scenario_Experiment/runs/` very likely carry the
same embedded CSVs. **Not audited** — Brian judged it unnecessary (below).

### The reproducibility statement for the README

State three tiers plainly rather than letting an assessor debug their way to them:

1. **Fully reproducible with an OpenAI key:** nothing, strictly — A, B, C and F need the
   Nielsen history, which is not shipped. The CODE PATH is inspectable and the prompts are
   complete. Say this precisely; the earlier draft claim that "`OPENAI_API_KEY` alone runs
   scenarios A, B and C" is **true only if the data is present**, and it will not be.
2. **Not reproducible, data withheld:** A, B, C, F — licensed Nielsen panel.
3. **Not reproducible, engine withheld:** D, E, G — proprietary Prometheus orchestrator.

Then: *the artefacts are provided for inspection; the experiment is not re-runnable
because it depends on licensed retail data and a proprietary orchestrator; the derived
results are complete.*

> **Correction to this plan's existing `.env` section.** It currently says
> "`OPENAI_API_KEY` alone runs scenarios A, B and C. That is the reproducible tier, and it
> is the claim the README should make." **That claim is wrong** and must not reach the
> README — those scenarios also need the brand history, which is withheld. It also predates
> scenarios F and G. Fix both when Phase 3 rewrites the README.

### Git history — CLOSED, no action

Flagged that the repo is public and history permanent, so anything already committed is
already disclosed regardless of later cleanup. **Brian, 2026-09-11:**

> "no its okay, we will turn the repo private anyways, and create a new repo that we will
> share."

That resolves it: the submission repo is a **fresh repository with no shared history**,
not a cleaned branch of this one. Two consequences for this plan:

- **No history rewrite is needed** (no `filter-repo`, no force-push). Simpler and safer.
- **The export must be a clean copy**, not a clone. A clone brings `.git` and therefore
  every past commit of the embedded CSVs.

### Seven arms, not five

This plan's SHIP/NO-SHIP reasoning predates scenarios F and G (added 2026-09-11) and the
arm rename (same day). The current keys are `A_llm_plain`, `B_llm_data`, `C_llm_model`,
`D_prometheus_data`, `E_prometheus_model`, `F_llm_data_model`, `G_prometheus_data_model`.
**G joins D and E in the "needs Prometheus" tier.**
