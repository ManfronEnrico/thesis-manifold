---
name: srq1-locked-state
description: STATE - The locked SRQ1 model numbers as of 2026-09-07, the determinism contract that produced them, and what remains. Read this FIRST in any new session touching SRQ1 results.
pid: P0047
created: 2026_09_07-16_00
updated: 2026_09_07-18_10
status: deterministic_but_horizon_mislabelled
---

# SRQ1 — LOCKED STATE (2026-09-07)

**Read this before touching any SRQ1 number.** One page; the detail is in `findings.md`.

> ## ⚠ READ THIS FIRST — these numbers are H1, not H3
>
> Every number below is **deterministic and reproducible**. Re-running today reproduces
> them exactly. That part is solved (F18/F19).
>
> But `engineer_features()` **never receives the horizon**: lags are `shift(lag)` at both
> H1 and H3, so the h1 and h3 matrices are the *same one-month-ahead task* (verified —
> `lag_1`, `lag_3`, `lag_13` all identical). Published results come from the `_h3` file,
> so the thesis reports **one-month accuracy while describing a three-month horizon**
> (F22, and P0048 F1 which found it).
>
> **So: correct and reproducible for H1; mislabelled as H3.** They are locked against
> *drift*, not against *the horizon fix*. A dual-horizon re-run will change them.
>
> This is a validity problem, not a reproducibility one — and it is the more serious of
> the two. See plan **P0049** for the consolidated state.

---

## 1. The determinism contract — the thing that makes these numbers real

**Every accuracy number in SRQ1 is produced with `XGB_N_JOBS = 1`.**

XGBoost with `n_jobs=-1` is **not reproducible**: its parallel gradient reduction is
order-dependent, so thread count changes the result. Measured, seed and data held
constant (danskvand):

| n_jobs | WMAPE |
|---|---|
| 1 | 34.65 (repeatable) |
| 2 | 34.95 |
| 4 | 35.40 |
| 8 / −1 | 37.30 |

**2.65 pp from thread count alone** — larger than most feature effects in this study.
`random_state` does not fix it.

### The rule, stated once

| Purpose | `n_jobs` | Why |
|---|---|---|
| **Accuracy** (8 scripts) | **1** | A number that changes with core count is not a result |
| **Resource profiling** (`srq1_profiling.py`) | **−1** | All-cores IS the measured quantity; core count is reported with it |

**Do not "fix" `srq1_profiling.py`.** Its `n_jobs=-1` is deliberate and documented.

**If you add an XGBoost call site:** import `XGB_N_JOBS`, never write a literal.

---

## 2. Locked numbers

### Tuned benchmark — the thesis headline track

| Category | Model | val WMAPE | test WMAPE | test medMAPE |
|---|---|---|---|---|
| CSD | LightGBM | 15.48 | 15.80 | 38.63 |
| CSD | XGBoost | 14.55 | **14.99** | 36.25 |
| danskvand | LightGBM | 27.20 | 23.65 | 47.38 |
| danskvand | XGBoost | 24.76 | **20.88** | 50.77 |
| energidrikke | LightGBM | 7.96 | 14.56 | 47.64 |
| energidrikke | XGBoost | 8.67 | **13.12** | 45.11 |
| RTD | LightGBM | 21.89 | **35.10** | 43.40 |
| RTD | XGBoost | 23.81 | 36.02 | 35.04 |

### Untuned benchmark — best per category

| Category | Model | WMAPE |
|---|---|---|
| CSD | XGBoost | 17.51 |
| danskvand | Ridge | 19.21 |
| energidrikke | XGBoost | 15.91 |
| RTD | LightGBM | 32.21 |

⚠ **RTD's winner is XGBoost → LightGBM versus the pre-fix run.** The old margin was
0.43 pp, smaller than the thread artefact. That conclusion was never real.

### Stability (5 seeds) — verdict SURVIVED the fix

Winner still **FLIPS in 4 of 4** categories. LightGBM and XGBoost remain statistically
indistinguishable.

**One qualification (F19):** "between-seed spread exceeds between-model difference" is
true for CSD (0.11 vs 0.65), danskvand (0.74 vs 1.22) and energidrikke (0.42 vs 1.38) —
but **NOT RTD**, where the model gap (3.16) now exceeds the seed spread (1.94). RTD's
winner still flips, so the conclusion holds on different grounds there.

### Holiday enrichment ablation

**7 of 12 helped, mean −1.42 pp.** Never quote the mean alone — the model-family split
is the finding: Ridge 3/4 (−2.49), LightGBM 3/4 (−2.45), **XGBoost 1/4 (+0.68)**.

> Prose for this is being handled in a **separate session**. Numbers here are canonical.

---

## 3. Artefact status

**All accuracy artefacts regenerated post-fix.** Verified: two consecutive full
benchmark runs are byte-identical.

| Still pre-fix | Why it is fine |
|---|---|
| `profiling.csv`, `sandbox_profiling.csv` | Resource measurement — the `n_jobs=-1` exception. Timing/memory columns only, no accuracy metric. |
| `param_drift.csv`, `refit_vs_retune.csv`, `retune_single_cutoff.csv` | **Efficiency measurement**, not accuracy: refit-vs-retune wall-clock and hyperparameter drift. Consumed by `04_SRQ4_Scenario_Experiment/scenario_setup/export_appendix.py` (`table_param_drift()`, and the Efficiency metric rows). LightGBM-only (`num_leaves`), and LightGBM is verified deterministic. |

**All five pre-fix files measure time or memory, not accuracy.** F18 does not reach any
of them, so none needs regeneration.

⚠ **Their producing script is not in the repo.** Nothing under `01_SRQ1_...` generates
them and they are absent from `.archive/`; only the SRQ4 appendix *reads* them. If these
numbers ever need refreshing, the generator must be reconstructed first — budget for
that rather than assuming a re-run exists.

## 4. What remains

| # | Task | Owner |
|---|---|---|
| 8 | Close five Word threads (ch1 15/18/20, ch2 66/69, ch3 127, ch4 177, ch5 207) | Brian, after prose lands |
| 22 | NotebookLM claims verification CV-01…CV-05 | Brian |
| — | P0042 ~111 funded runs (~$40) | ⚠ **NOT simply unblocked** — the horizon fix is upstream (F22) |

**Prose insertion (task 12) moved to a separate session.** Its note is
`06_thesis_writing/writing-notes/srq1-holiday-enrichment-result-and-limitations.md`,
anchored to snapshot `2026-09-07_14-29_holiday-enrichment`.

---

## 5. Known defects in existing thesis text

Flagged, **not** fixed — each needs a decision, not a guess:

1. **Ch4 §4.3 "22 columns"** — the matrix has **54**. Establish what it was counting.
2. **Ch4 §4.3 "14 modelling features"** includes `weighted_distribution`;
   `srq1_benchmark.py::FEATURES` has **13** and excludes it. One of the two is wrong.
3. **Ch6 §6.6 cites "(§6.5.7)"** for the seed sweep, which is **§6.5.9**.
4. **Ch6 §6.5.9 / §6.6 "every input held identical"** — false until the protocol note
   recording single-threaded XGBoost is added. Both must ship together.

---

## 6. Unverified claims — never cite these without checking

Register: `06_thesis_writing/writing-notes/unverified-claims-to-check.md`
Briefs: `06_thesis_writing/notebookLM/04-Claims_Verification/`

| ID | Claim | Note |
|---|---|---|
| CV-01 | VIF 5 / 10 | Attribution to Hair et al. was **invented from memory**, removed |
| CV-02 | Spearman ≥ 0.95 | Never had a source; a chosen parameter |
| CV-03 | Lukkeloven 2012 | Substance confirmed; statute name/year unverified |
| CV-04 | XGBoost thread mechanism | **Effect measured**; explanation unsourced |
| CV-05 | Store Bededag abolition | Effect in data; bill number unverified |

**Rule: if a source is not in the Zotero library, it is not a source.**

---

## 4. ⚠ These numbers measure a one-month horizon, not three (added 2026-09-07, P0048)

**The numbers above remain the locked, correct output of the current pipeline — but the
pipeline does not implement the horizon the thesis describes.**

`engineer_features()` has no `horizon` parameter. Lags are `shift(lag)` at both H1 and
H3, so the target is never moved away from the features. Merging the two CSD matrices on
brand × year × month, every lag column is **identical** across all 4,370 shared rows;
only `min_periods` differs (15 vs 17).

Every SRQ1 script hardcodes `_feature_matrix_h3.parquet`, and the row counts confirm the
locked numbers come from that file (1805/665/95 = h3 after dropna). **So the "H3" numbers
above are one-month-ahead accuracy.**

**Consequence for anyone reading this page:** the determinism contract in §1 is still
binding and still correct. But once the horizon is fixed (P0048 tasks 3–5), §2's numbers
are superseded and **H3 accuracy is expected to get worse** — a genuine three-month
forecast is harder. Do not treat §2 as final while P0048 task 5 is open.

See `plans/P0048_.../findings.md` F1 and F2, and `START_HERE.md` for the one-command
reproduction.
