# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Navigation hub. It carries **no results, no measurements and no status** — each of those has a
> home kept current by something other than a person remembering to edit this page. Keep it thin.

---

## What this thesis is

A production conversational assistant, deployed with Danish retailers and consumer-goods
manufacturers, explains what has already happened but cannot forecast. This thesis extends it with
forecasting light enough for a small-business cloud memory budget, and asks whether that beats
letting a language model write its own forecasting code.

**The framing that does most of the work:** this is a capability gap in a live product, not a
prototype. The deployed system is the empirical anchor and is **extended, not replaced** — which
rules out the greenfield architecture most of the literature assumes.

Full framing and reasoning: `00_thesis_context/thesis-topic/`. Canonical research-question text:
`00_thesis_context/research-questions/`. Both are deliberately not restated here.

### Four sub-questions, one per layer of the extension

| | Layer | Asks |
|---|---|---|
| **SRQ1** | the substrate | which lightweight models trade accuracy against memory and category specialisation best |
| **SRQ2** | the interface | how a forecast reaches the agent with reliability, uncertainty and traceability preserved |
| **SRQ3** | the host system | what a production agentic system must already do before forecasting can attach |
| **SRQ4** | the evidence | whether dedicated models beat an agent writing its own forecasting code, at justified cost |

Methodology is Design Science Research: the thesis produces an **instantiation** and a
**method-level contribution**, and both are assessed. That is why SRQ2 and SRQ3 are framed as
principles and criteria rather than as descriptions of what was built.

---

## Repo structure — the root is organised by research question

The folder a script lives in tells you which question it answers. Authoritative reference:
`.claude/rules/repo-tier-structure.md`.

| Folder | Holds |
|---|---|
| `00_thesis_context/` | Topic, research questions, methodology, CBS requirements |
| `01_SRQ1_Model_Training/` | Data pipeline (`_00_raw` → `_03_engineered`) and model training |
| `02_SRQ2_Tool_Interface/` | `forecast_tool.py` — the typed tool the agent calls |
| `03_SRQ3_Integration_Readiness/` | Empty **by design** — SRQ3 produces criteria, argued from the integration the other layers make possible, not code |
| `04_SRQ4_Scenario_Experiment/` | The scenario comparison harness and its runs |
| `05_thesis_results/` | Every generated figure and table, one folder per chapter |
| `06_thesis_writing/` | Writing notes, citations, drafts, read-only prose snapshots |

`PATHS.py`, `plans/`, `user-docs/`, `utility_scripts/` and `.claude/` are supporting infrastructure
and sit outside the numbered scheme by design.

**Artefact rule:** tier 06 holds no figures, tables or diagrams. Producers live with their SRQ and
write into `05_thesis_results/`. There is no second copy of any artefact anywhere.

### Results are keyed by CHAPTER, not by SRQ

`05_thesis_results/` subfolders are `{NN}_{chapter-slug}/`. The SRQ-to-chapter mapping lives only
in `PATHS.py`: SRQ1 → `05_model_benchmark/`, SRQ2 → `07_decision_synthesis/`,
SRQ4 → `08_experimental_evaluation/`. SRQ3 has no results directory of its own.

Chapter numbers move — Ch5 and Ch6 were swapped on 2026-09-08. Never hardcode one. Derive it from
`PATHS.CHAPTER_ORDER`, or call `get_chapter_results_dir(slug)` / `get_srq_results_dir(n)`.

---

## Commands

Run from the repo root with the project venv (`.venv`).

### Data pipeline (SRQ1)

```bash
# One shared orchestrator for every category — never a per-category copy
python 01_SRQ1_Model_Training/01_thesis_data/_02_preprocessing/nielsen/_shared_modules/run_preprocessing.py --category CSD --horizon 3
python .../run_preprocessing.py --all-categories --horizon 3 --skip-shared
python .../run_preprocessing.py --category CSD --from-step 4          # resume mid-pipeline
```

Steps 0 to 2 (validate cache, build the panel, describe it) are horizon-independent; steps 3 to 6
apply a per-horizon contract. That split is what `--skip-shared` exists for.

### Model training and benchmark (SRQ1)

```bash
python 01_SRQ1_Model_Training/02_thesis_modelling/model_training/run_both_horizons.py   # full suite, hours
python .../run_both_horizons.py --horizon 3
python .../run_both_horizons.py --dry-run                                               # print the plan, run nothing
python .../run_both_horizons.py --only benchmark,benchmark_cv
python .../model_training/train_and_persist.py [--category CSD]                         # fit once, persist to disk
```

**Order matters.** The suite is a dependency chain, not a bag of scripts. Running it out of order
does not crash — several stages guard their reads with `is_file()` and **degrade silently**, which
is how model selection once fell through to a hardcoded default. Use the wrapper.

### Scenario experiment (SRQ4) — spends real money

```bash
python 04_SRQ4_Scenario_Experiment/scenario_setup/verify_setup.py   # free contract checks
python .../scenario_setup/smoke_test.py                             # one run per scenario, cheap
python .../scenario_setup/srq4_experiment.py --demo --scenarios A,B
python .../scenario_setup/srq4_experiment.py --full --repeats 5     # the funded set
python .../scenario_setup/inspect_runs.py                           # read back logged runs
```

`verify_setup.py` checks contracts without sending a request, so it cannot see anything that only
appears when a scenario actually runs. Always run it **and** `smoke_test.py` before a full run.
Current per-run cost estimates live in the harness, not here.

### Thesis writing

```bash
python utility_scripts/scripts/thesis_snapshot.py --label "<slug>"   # mirror the OneDrive .docx
python utility_scripts/scripts/zotero_client.py                      # re-pull the Zotero library
python 05_thesis_results/generate_architecture_diagrams.py           # figures, SVG only
```

`/re-snap` runs the git fetch, snapshot, diff and Zotero pull together. Run it **before** writing
any prose pass or follow-up note — all four currency checks answer the same question, which is
whether what you are about to verify against still exists.

### Tests

```bash
python -m pytest utility_scripts/ -v
```

Two pytest suites exist under `utility_scripts/tests/`, covering Zotero sync and NotebookLM
scanning. **pytest is not currently installed in `.venv`.** There is no test suite over the
modelling or data code; those are verified through `verify_setup.py`, `smoke_test.py` and the
`--dry-run` paths.

---

## Architecture — the load-bearing decisions

### Feature construction stays server-side

The language model never handles a feature vector. It calls a tool and receives a forecast, an
interval, a confidence signal and the provenance needed to trace it. **That single decision is most
of SRQ2's contribution** — it is what makes the forecast auditable rather than merely available.

### Train once, serve many — the boundary is real

`train_and_persist.py` is the single training entry point. `forecast_tool.py` **loads** models and
never fits. Before this boundary existed, three copies of the training logic had drifted apart, and
a conformal-calibration fix landed in one while the other two kept the bug. Two models are fitted
per category: one on TRAIN only, whose validation residuals give the conformal quantile, and one on
TRAIN plus validation, which serves. **Only the calibration must be out-of-sample. Test is never
touched by either.**

### Horizon selection is an environment variable, not a flag

`SRQ1_HORIZON` drives **both** which feature matrix a script reads and where its results go, from
one value, via `model_training/srq1/_horizon.py`. The primary horizon keeps the unsuffixed paths;
the secondary writes to a parallel subtree, so **a secondary-horizon run can never overwrite a
primary result**. `run_both_horizons.py` sets the variable per child process.

An environment variable rather than a flag because the SRQ1 scripts have heterogeneous argparse
setups, several with none at all, and a run must not depend on whether a given script remembered to
define `--horizon`.

### SRQ4 is an information ladder, not a two-way comparison

Three scenarios, each adding one thing to the one below, so the increments attribute separately:
`A_plain` (no firm data), `B_data` (the history in a code sandbox, the model writes its own
analysis), `C_model` (the same data behind a typed tool). A to B measures what data access buys;
B to C measures what model integration adds, which is the thesis contribution. A two-scenario
design conflates these.

Outcomes are **classified**, never averaged — a failure rate says more about production readiness
than a small accuracy gap. Do not reintroduce the older "arm" vocabulary or the earlier lettering,
which ran the other way.

### Prose has exactly one authoritative home

The thesis text is a **OneDrive `.docx`**, shared between the two authors. That is the only
editable copy. `06_thesis_writing/docx-exported-snapshots/` is a read-only, gitignored mirror that
exists so prose can be grepped and diffed — **never edit one or convert it back**.
`sections-drafts/*.md` is a claims ledger: bullets, status, provenance, open questions, and never
prose. Staged prose with placement contracts goes in `writing-notes/`.

---

## Rules you must follow

Full text in `.claude/rules/`; conflicts resolve by tier per `rule-priority-hierarchy.md`.

**Trust tier (never yield)**
- **Never commit directly to `main`.** One branch or worktree per session.
- **Never stage with `git add -A` or `.`** — explicit paths only, or you sweep in another session's
  files.
- **No documentation at root.** Only the foundational files already there; everything else routes
  to `user-docs/` or a plan folder.

**Correctness tier**
- **Every path resolves through `PATHS.py`.** No directory-name string literals, no
  `Path(__file__).parents[N]` above the script's own directory, no lowercase category key used as a
  folder name. If a path is missing, add it to `PATHS.py`. The repo has been reorganised four times
  and every hardcoded string broke silently — the script ran, the file was not found, and a stage
  degraded instead of failing.
- **Generated numbers are computed, never typed.** Every figure in a table, caption or report is
  read from an input consumed on that run, including inside internal-review blocks. A hardcoded
  result is true when written and wrong after the next re-run.

**Quality tier**
- **Bullets before prose.** Thesis content starts as bullets; prose only after explicit human
  approval.
- **One-off execution by default.** A workflow command with no interval runs once. Never schedule a
  recurring loop unless the user says "every".
- **If it is not in the Zotero library, it is not a source.** A plausible-looking reference written
  from memory once read as verified.

Load before the relevant work: `prose-insertion-discipline.md` (any writing pass),
`figure-generation-standards.md` (any figure — landscape, SVG, no PNG twin),
`repo-tier-structure.md` (folder questions).

---

## Environment

- Windows 11, PowerShell primary; Bash tool also available. Python 3.11+, venv at `.venv`.
- Graphviz must be installed as a **system package**, not only the Python binding — without it the
  import succeeds and rendering fails.
- API keys come from `.env`, never from a file in the repo. `requirements.txt` is annotated:
  several pins carry a comment explaining the version, and a few record a dependency retained
  deliberately. Read the comment before changing a pin.
- **Never commit the raw panel.** It is commercial data under a licence and a non-disclosure
  agreement, must not leave the local environment, and `.gitignore` enforces this.
- Known Windows, OneDrive, CRLF and encoding traps live in `.claude/logs/tooling-issues.jsonl`
  (source of truth), rebuilt into `user-docs/integration/tooling-issues.md`.

---

## Key references

| Topic | Location |
|---|---|
| Every path constant, and the tier map | `PATHS.py` |
| What this thesis is about | `00_thesis_context/thesis-topic/` |
| Research questions, canonical | `00_thesis_context/research-questions/` |
| Any number, table or figure | `05_thesis_results/`, by chapter |
| Repo tier structure, authoritative | `.claude/rules/repo-tier-structure.md` |
| Architecture | `user-docs/architecture/architecture.md` |
| File-to-purpose map | `user-docs/contributing/repository_map.md` |
| CBS formal requirements | `00_thesis_context/formal-requirements/` |
| What is decided, open or blocked | `plans/PLANS_INDEX.md` and the registers in `06_thesis_writing/writing-notes/` |

`AGENTS.md` mirrors this file for non-Claude-Code agents — **update both together.**
