---
name: submission-export
description: SKILL - Build the clean, assessor-facing copy of this repository. Drops collaboration and tooling infrastructure, strips internal decision codes and plan references from code comments, and starts a fresh git history. Triggers - /submission-export, submission repo, clean repo for assessors.
category: workflow
applies-to: [the whole repository, every shipped .py file]
triggers: [/submission-export, preparing the assessor-facing repo, thesis code freeze]
created: 2026_09_10-15_35
updated: 2026_09_10-15_35
---

# /submission-export — build the assessor-facing repository

The working repository is a research artefact **and** a Claude-assisted
production harness. The assessors get only the first half. This skill performs
that separation into a new folder, leaving the working repo untouched.

**Read the plan before running:**
`plans/P0054_2026-09-10_15-35_submission-ready-repo/task_plan.md` holds the
file manifest and open decisions;
`plans/P0054_.../comment_rewrite_rules.md` holds the comment rules with worked
before/after examples. This skill is the procedure; those are the specs.

---

## Step 0 — Gate

**Do not proceed unless all four hold.** Ask the user to confirm each; do not
infer any of them.

| # | Precondition |
|---|---|
| 0.1 | Model training is final — no rerun in flight, no open gate in `writing-notes/post-hpc-validation.md` |
| 0.2 | Every chapter's writing-notes folder holds only `.archive/` |
| 0.3 | The OneDrive `.docx` is frozen |
| 0.4 | Every generated artefact has been regenerated since the last code change |

Also confirm the **Q1 data decision** (ship nothing / synthetic sample / real
matrices with written consent). It changes both the file set and the README, so
it cannot be deferred past this step.

If any gate fails, say which and stop. A premature export ships stale numbers
under a clean-looking surface, which is worse than not exporting.

---

## Step 1 — Create the export tree

Never edit in place. Never `git mv`. The working repo must be unchanged when
this finishes.

```bash
cd "Z:/_dev-ssd"
git -C thesis-manifold status --short          # must be clean
cp -r thesis-manifold thesis-manifold-submission
cd thesis-manifold-submission
rm -rf .git
```

Copying rather than cloning keeps gitignored-but-wanted files (the engineered
matrices, if Q1 says they ship) without a second decision about what git
tracked. The cost is that gitignored junk comes too, which Step 2 removes
anyway.

---

## Step 2 — Apply the manifest

Delete in this order — infrastructure first, so the later greps run over a
smaller tree.

```bash
# Claude / agent infrastructure
rm -rf .claude .agents .codex
rm -f CLAUDE.md AGENTS.md .claudeignore skills-lock.json

# Collaboration and writing record
rm -rf plans user-docs 06_thesis_writing 00_thesis_context
rm -rf utility_scripts            # see Step 3 before running this

# Archives, working state, editor config
rm -rf .archive worktrees .venv
find . -name "__pycache__" -type d -prune -exec rm -rf {} +
find . -name ".archive" -type d -prune -exec rm -rf {} +
rm -f thesis-manifold.code-workspace uv.lock

# Runtime logs and machine state
find . -name "*.jsonl" -delete
rm -f .run_both_horizons.stamp
```

Then, per the Q1 decision:

- **Ship nothing:** `rm -rf 01_SRQ1_Model_Training/01_thesis_data/_03_engineered`
  and the raw/converted data folders' contents, keeping their scripts
- **Synthetic sample:** keep the folder structure, replace contents, add the
  generator script
- **Real matrices:** keep as-is

`03_SRQ3_Integration_Readiness/` is empty — drop it unless Q5 says otherwise.

---

## Step 3 — Verify nothing shipped depends on something dropped

The manifest is a hypothesis. Test it before rewriting comments, because a
missing dependency changes the file set.

```bash
# Imports reaching a dropped tree
grep -rnE "^\s*(from|import)\s+(utility_scripts|plans)" --include="*.py" .

# Path constants pointing at folders that no longer exist
grep -nE "(THESIS_WRITING|NOTEBOOKLM|PLANS|SNAPSHOT|CITATIONS|CONTEXT)" PATHS.py
```

`PATHS.py` is the main risk. It defines constants for `06_thesis_writing/`,
`notebookLM/`, `sections-drafts/` and `plans/`. **Remove those constants** —
do not leave them resolving to absent directories, which is the silent-failure
mode `path-handling.md` exists to prevent.

`utility_scripts/scripts/dynamically_find_root_directory.py` is the one file in
that tree a shipped script might import. Check before deleting the folder; if
something imports it, inline the function rather than shipping the folder.

Then a smoke run in a fresh venv from `requirements.lock`, on the lightest real
entry point available given the Q1 decision. If nothing can run without Nielsen
credentials, that is a README statement, not a blocker.

---

## Step 4 — The comment pass

**This is the bulk of the work.** Follow
`plans/P0054_.../comment_rewrite_rules.md` for the rules, and these two
completed passes as the quality bar — both were produced by reading the whole
file, and both found defects a grep could not:

| Worked pass | Shows |
|---|---|
| `plans/P0054_.../worked_pass_step1_load_and_aggregate.md` | an ordinary pipeline module: 4 KEEP, 5 DELABEL, 4 DELETE, **2 FIX** (a corrupted section heading, a docstring asserting the wrong horizon) |
| `plans/P0054_.../worked_pass_export_appendix.md` | a generator, where the emitted output matters more than the source: 14 internal-note blocks reaching 26 published files, plus a stale output path |

### 4a — Read every file in full. Grep is a checklist, never the method.

**Read the complete file, top to bottom, before proposing a single edit.**
Not the marker hits with context lines. Not the docstring plus a grep. The
whole file, in one read.

This is not a preference — grepping produced four documented misdiagnoses on
the very first file it was tried on (`train_and_persist.py`, 2026-09-10). Each
was invisible to a keyword search:

| What grep cannot see | The instance |
|---|---|
| A docstring documenting **bugs that were fixed** | three paragraphs describing retraining defects in `forecast_service`, `srq4_experiment` and `srq2_synthesis` that no longer exist. An assessor reads them as current defects. |
| Paths that are simply **wrong now** | the docstring's output paths name `04_thesis_results/srq1/` and `05_thesis_results/model_benchmark/`; neither exists. The `Usage:` block names `03_thesis_modelling/`, a pre-September path, so the command an assessor would copy does not run. |
| A comment **orphaned from its subject** | a `weighted_dist is deliberately absent` note sits above `FEATURES = list(_FEATURES)`, but the list it describes lives in `_features.py`. It is a fragment left behind when the literal moved, and belongs in the other file. |
| Two unrelated comments **fused into one block** | the same block continues into a five-line refactor history. Only reading reveals they are two comments, one worth keeping and one not. |

Grep also cannot see the inverse error: a long comment that **must stay**
because the code is genuinely non-obvious. Both directions require the file.

So per file, in order:

1. **Read the whole file.** Understand what it does before judging any comment.
2. **Check every path, filename and command** a comment or docstring names —
   against `PATHS.py` and against the tree. Stale paths are common and are
   worse than meta-comments, because they are actively wrong.
3. **Check every claim about other files** (`x.py retrains on import`,
   `eleven copies of this existed`). If it describes a fixed bug or a past
   refactor, it goes.
4. **Judge each comment against the audience test** (below).
5. **Read the rewritten file top to bottom again**, as an assessor would.

Build the marker inventory too, but only as a completeness check after the
read — to confirm nothing was missed, never to find the work:

```bash
grep -nE "(DEC-[A-Z]|P00[0-9][0-9]|\bF[0-9]{1,3}\b|2026-[0-9]{2}-[0-9]{2})" <file>
```

As of 2026-09-10, 54 of 69 pipeline files carry at least one such marker;
`PATHS.py` is heaviest at 49. **Files with zero markers still need the read** —
`train_and_persist.py`'s wrong paths carry no marker at all.

### 4b — The audience test, applied per comment

> Would this sentence make sense to a reader who has never seen a previous
> version of this repository, does not know what a plan or a finding is, and
> is judging whether this code is competent?

Four verdicts, and the last is the one grep-driven work misses:

| Verdict | Applies when | Action |
|---|---|---|
| **KEEP** | explains why the code is as it is; a reader would ask otherwise | leave it |
| **DELABEL** | good reasoning wearing an internal label or date | strip the label, keep the sentence |
| **DELETE** | describes repo history, a fixed bug, a past refactor, a collaborator instruction | remove entirely |
| **FIX** | factually wrong now — a stale path, a renamed file, a superseded number | **correct it**, do not just strip it |

**FIX matters most.** A stale path is a defect an assessor can trip over, not a
tone problem. The pass is the last time anyone reads these files closely, so it
is where such things get caught.

**Never batch-edit with sed or a regex.** Every judgement is per-comment and
needs the file's context. A mechanical strip leaves dangling fragments —
exactly how the orphaned `weighted_dist` comment came about.

### 4c — Generated output must be submission-ready too

The appendix and report generators write **files that go into the thesis**, so
their output is under the same rule as their source. This is a second, separate
pass over each generator:

| Generator | Writes |
|---|---|
| `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` | SRQ4 appendix tables |
| `01_SRQ1_Model_Training/02_thesis_modelling/model_training/srq1/srq1_export_enrichment_appendix.py` | feature-enrichment appendix |
| `01_SRQ1_Model_Training/01_thesis_data/_00_raw/holidays/export_holiday_appendix.py` | holiday enrichment tables |
| `01_SRQ1_Model_Training/02_thesis_modelling/model_training/training_report.py` | the training report |
| `05_thesis_results/generate_architecture_diagrams.py`, `generate_literature_table.py` | figures and the literature table |
| every `step_*.py` writing a `.md` or `.log` under `pipeline_step_outputs/` | EDA and pipeline diagnostics |

In each, audit **the emitted strings**, not only the code comments: table
captions, `note=` and `review=` arguments, column headers, section titles,
printed banners, and any `INTERNAL REVIEW` separator.

Three specific things to remove from generated output:

- **The internal/submission split itself.** `REVIEW_SEP` and every
  `<!-- INTERNAL REVIEW -->` block exist because the working repo mixes
  submission text with notes to ourselves. In the submission repo there is no
  internal half — drop the separator and the blocks below it rather than
  shipping a document that visibly withholds a section.
- **Plan, finding and decision references inside captions and notes.**
- **Provenance sentences aimed at us** ("regenerate after the next run",
  "supersedes the all-markets values", "flagged in §4.6").

Then **regenerate every artefact and read the output**, not just the code. A
caption is only verified by looking at the file it produced.

### 4d — Non-Python files

Same pass: `.gitignore` (strip the exemption essays explaining our tracking
decisions) and every shipped `README.md` (strip the Claude-rule YAML
frontmatter — `applies-to`, `triggers`, `category` — and any stale folder
names).

---

## Step 5 — Write the new README

The existing `README.md` cannot be edited into shape. It documents the
pre-2026-09 tier names and explicitly describes System B, which is the thing
being removed. Replace it.

What the assessor's README needs, and nothing else:

1. **What this is** — thesis title, institution, authors, the research question
   and four sub-questions
2. **What the code does**, per top-level folder, one line each
3. **How to run it** — venv, `requirements.lock`, the three entry points
   (preprocessing orchestrator, `run_both_horizons.py`, `srq4_experiment.py`)
4. **Data availability** — the Q1 answer, stated plainly: what the data is,
   who provided it, why it is not included, what that means for reproduction
5. **Where the results live** — that `05_thesis_results/` holds every figure
   and table the thesis cites, and that each was generated by a named script

No System A / System B framing. No tier-history notes. No links into folders
that no longer exist. Verify every internal link resolves in the export tree.

---

## Step 6 — Final verification

```bash
# Internal markers
grep -rE "(DEC-[A-Z]|P00[0-9]{2}|\bF[0-9]{1,3}\b)" --include="*.py" .
# Names
grep -rniE "brian|enrico" --include="*.py" --include="*.md" .
# Claude and agent references
grep -rniE "claude|anthropic|\.agents|SKILL\.md" --include="*.py" --include="*.md" .
# Paths into dropped trees
grep -rE "plans/P0|writing-notes|notebookLM|user-docs|\.claude/" .
# Leftover working state
find . -name "__pycache__" -o -name "*.jsonl" -o -name ".archive"
```

Every one should return nothing, with two legitimate exceptions to check by eye:

- `anthropic` / `claude` appearing as a **named LLM vendor** in the SRQ4
  methodology is correct and must stay
- author names in the README byline are correct and must stay

**Then two checks no grep can do:**

1. Brian opens three files at random and reads them as an assessor would. The
   greps find labels; only reading finds tone.
2. Repeat the Step 3 smoke run in the final tree.

---

## Step 7 — Initialise history and hand over

```bash
cd "Z:/_dev-ssd/thesis-manifold-submission"
git init
git add .
git commit -m "Initial commit — CBS master's thesis code"
```

One commit. The working repo's 500+ commits narrate a Claude-assisted workflow
("docs: close chapter 4", "fix: zotero export dropped computerProgram") and are
themselves meta.

Hand over as a fresh **private** repo or a zip, per Brian's choice. Do not push
to the existing remote.

Finally, update `plans/P0054_.../task_plan.md` in the **working** repo:
`status: complete`, a `completed:` timestamp, and an `outcome_summary:` naming
what shipped and what the Q1 decision was.

---

## What this skill must never do

| Never | Why |
|---|---|
| Edit the working repo's code comments | the internal markers are how this project avoids re-litigating settled decisions |
| Run before Step 0's gates pass | ships stale numbers under a clean surface |
| Batch-strip markers with sed or a regex | leaves dangling clauses and destroys good comments |
| Push to the existing remote | the submission repo is a separate, private artefact |
| Ship Nielsen data without a confirmed decision | it is under a confidentiality agreement with Manifold AI |

---

## Related

- `plans/P0054_2026-09-10_15-35_submission-ready-repo/task_plan.md` — manifest and open decisions
- `plans/P0054_.../comment_rewrite_rules.md` — the comment rules with worked examples
- `.claude/rules/path-handling.md` — why removing a `PATHS.py` constant beats leaving it dangling
- `.claude/rules/prose-insertion-discipline.md` — the "no metacomment" rule this extends from prose to code
