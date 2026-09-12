---
name: fallback-commit-record
description: STATE - Phase 0.4. The commit that IS the Branch A fallback, plus a correction to two things the commit message got wrong.
pid: P0055
created: 2026_09_13
updated: 2026_09_13
status: current
---

# PHASE 0 COMPLETE — the fallback is a commit (2026-09-13)

```
58243f3fb937cd8fe5c8911e14b850b90b12cb27
feat: v6 experiment redesign, 63-run funded set, and the P0055 book scan
94 files changed, 13648 insertions(+), 254 deletions(-)
```

**On `main`.** Brian directed everything to `main` including the Nielsen data,
waiving both the branch rule and the confidentiality hold: the repo is being made
private, and a cleaned copy will be built for submission.

> ## ⚠ NOT YET PUSHED
> `git push origin main` was **blocked by the permission classifier, twice**.
> The commit exists **only in this working tree**. Until someone pushes it, the
> fallback is one disk failure from gone.
>
> ```bash
> git push origin main
> git rev-list --left-right --count origin/main...HEAD   # expect 0  0
> ```

## To return to Branch A

```bash
git checkout 58243f3
```

Everything needed to reproduce the 63-run result is in that commit: the payload
generator, the v6 prompts, the harness, `runs.csv`, `summary.md`, all 65 raw
responses and the agent input CSVs.

---

## CORRECTION — two things I got wrong about the `RB_K` files

The commit message says `raw_responses/` holds "two pre-`_TRANSLIT` leftovers
named RB_K (A_llm_plain and G_prometheus_data_model, rep0)". **That is wrong on
the count**, and a follow-up worry about duplicated rows was wrong entirely.
Corrected here rather than by rewriting history.

### What is actually true

**There are SEVEN `RB_K` files, one per scenario, all `rep0`:**

```
A_llm_plain__CSD__RB_K__rep0.json      E_prometheus_model__CSD__RB_K__rep0.json
B_llm_data__CSD__RB_K__rep0.json       F_llm_data_model__CSD__RB_K__rep0.json
C_llm_model__CSD__RB_K__rep0.json      G_prometheus_data_model__CSD__RB_K__rep0.json
D_prometheus_data__CSD__RB_K__rep0.json
```

They are orphaned artefacts of a rep0 sweep written before the `_TRANSLIT` fix,
when ØRBÆK slugged to `RB_K` — NFKD left Ø and Æ whole, so combining-mark
stripping deleted them.

`OERBAEK__rep0.json` exists for **A and G only**; those two were re-run after the
fix and kept both filenames. B, C, D, E and F have `rep0` only under the old slug.

**65 files = 63 runs + 2 extra**, because A and G each carry their own rep0 twice.

### `runs.csv` is CLEAN — the duplication scare was my own filter bug

I briefly reported that `runs.csv` had two rows per (system, brand, rep) for
ØRBÆK. **It does not.** Verified:

| Check | Result |
|---|---|
| v6 rows | **63** |
| Rows per (system, brand, rep) | **1, for all 63 groups** |
| Rows per brand | HARBOE 21, 7-UP 21, ØRBÆK 21 |
| Brand strings | `HARBOE`, `7-UP`, `ØRBÆK` — correctly transliterated |

The false alarm came from filtering `brand.str.contains('RB')`, which matches
**HARBOE** as well as **ØRBÆK**. I was counting two brands and reading it as
duplication.

**No result in `summary.md` or `BRANCH_A_STATE.md` is affected.**

### What to do about the seven files

Nothing urgent — every aggregate is driven by `runs.csv`, not by filenames.
Before the clean submission repo is built, delete them: they are the only files
in `raw_responses/` with no corresponding CSV row, and a reader counting 65 JSONs
against 63 runs will ask why.
