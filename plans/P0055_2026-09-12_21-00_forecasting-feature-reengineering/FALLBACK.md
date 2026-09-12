---
name: p0055-fallback
description: STATE - The exact commit, schema id and artefact set the thesis ships if the re-engineering is abandoned. Written BEFORE any branch work begins.
pid: P0055
created: 2026_09_12-21_00
updated: 2026_09_12-21_00
status: reference
---

# The fallback

**If P0055 is abandoned, the thesis ships this. Nothing here needs redoing.**

## The commit

| | |
|---|---|
| Branch | `main` |
| Fallback commit | `8d30265` *(plus the v6 working-tree commit — see below)* |
| Remote | `origin/main`, 0 ahead / 0 behind at 2026-09-12 20:44 |
| Prompt schema | `v6-shared-composition+af04a42a478b` |

### ⚠ The v6 work was UNCOMMITTED when this plan was written

At 2026-09-12 21:00 the following were **modified or untracked on `main`** and
represent the entire v6 redesign plus the funded run:

```
 M 04_SRQ4_Scenario_Experiment/scenario_setup/prompts.py
 M 04_SRQ4_Scenario_Experiment/scenario_setup/srq4_experiment.py
 M 04_SRQ4_Scenario_Experiment/scenario_setup/verify_setup.py
 M 05_thesis_results/08_experimental_evaluation/runs.csv
 M 05_thesis_results/08_experimental_evaluation/summary.md
 M PATHS.py
 M plans/P0049_.../START_HERE.md, task_plan.md
 ?? 04_SRQ4_Scenario_Experiment/agent_inputs/
 ?? 04_SRQ4_Scenario_Experiment/scenario_setup/build_agent_inputs.py
 ?? 05_thesis_results/08_experimental_evaluation/raw_responses/
 ?? plans/P0049_.../STATE_2026-09-12_v6-redesign.md
 ?? 7 writing notes under 06_thesis_writing/writing-notes/
```

**COMMIT THIS TO `main` BEFORE BRANCHING.** It is the fallback. A branch taken
before committing leaves the fallback living only in a working tree.

Stage by explicit path — never `git add -A` (CLAUDE.md, Trust tier). The
`raw_responses/` directory is ~9 MB and embeds the Nielsen history in every
cached prompt; decide deliberately whether it is committed or stays local, the
same decision taken for the smoke on 2026-09-11.

## What the fallback contains

| Artefact | State |
|---|---|
| SRQ4 experiment | **63 runs, complete**, 3 brands × 3 repeats × 7 arms |
| Results | `05_thesis_results/08_experimental_evaluation/runs.csv` + `summary.md` |
| Models | 18-feature set, trained 2026-09-09 21:10, all four categories |
| Chapters 4, 5, 6, 7 | prose written and verified against these artefacts |
| Appendix tables | regenerated 2026-09-10 on the 18-feature set |

## Headline numbers the fallback supports

Median APE, nine runs per arm, three CSD brands:

| Arm | Median APE | Mean APE | USD/run | Latency |
|---|---|---|---|---|
| D_prometheus_data | 0.9% | 25.0% | 0.7664 | 111s |
| G_prometheus_data_model | 1.8% | 15.6% | 0.5536 | 84s |
| B_llm_data | 2.9% | 27.9% | 0.4667 | 124s |
| F_llm_data_model | 7.3% | 18.3% | 0.4253 | 104s |
| C_llm_model | 14.6% | 13.1% | 0.0091 | 6s |
| E_prometheus_model | 14.6% | 13.1% | 0.1994 | 32s |
| A_llm_plain | 502% | 662% | 0.3798 | 69s |

Within-arm spread across three repeats: **0.0% for C and E** (identical every
run), 0.9–22.6% for the data arms. That contrast is the reproducibility finding
and it does not depend on this plan.

## How to abandon

```bash
git checkout main          # the fallback, untouched
```

Then delete or leave the branch. **Nothing on `main` depends on the branch.**
Set this plan's frontmatter to `status: cancelled` with a
`cancellation_reason`, and add one line to `progress.md` saying what was
learned — a measured "we tried and ran out of time" is a limitations sentence,
not a loss.

## The honest limitation if abandoned

Chapter 5 already states the ETS omission and the fixed non-seasonal ARIMA. If
this plan is abandoned, those stay as written, and the discussion carries the
note at
`06_thesis_writing/writing-notes/ch9_discussion/the-result-hinges-on-forecasting-practice.md`,
which frames the comparison as *this pipeline* against *this agent practice*
rather than as a general claim. **That framing is already defensible.** The
re-engineering strengthens it; it is not required to make it honest.
