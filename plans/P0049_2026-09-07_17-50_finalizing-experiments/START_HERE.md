---
name: p0049-start-here
description: STATE - Entry point for P0049. Written for a session with NO prior conversation history (account switch). Consolidates every open thread across P0039/P0040/P0042/P0044/P0047 into one ordered picture.
pid: P0049
created: 2026_09_07-17_50
updated: 2026_09_07-18_15
status: in_progress
---

# P0049 — Finalizing experiments: START HERE

**You have no conversation history. This file is the whole picture.** Read it before
running anything.

Its scope is the **experiments and the model numbers**. Prose insertion lives in
**P0048** (a parallel session) — don't do prose work from here.

---

## 1. The two things that matter most

### (a) SRQ1 numbers are deterministic — that problem is solved

XGBoost was configured `n_jobs=-1`, which is **not reproducible**: its parallel gradient
reduction is order-dependent, so thread count changed the result. Measured, with seed
and data fixed: **34.65 / 34.95 / 35.40 / 37.30** WMAPE at 1 / 2 / 4 / 8 threads —
**2.65 pp from thread count alone**, larger than most feature effects in the study.

Fixed: `XGB_N_JOBS = 1` at every **accuracy** call site (8 scripts). Deliberately **not**
in `srq1_profiling.py`, where all-cores is the quantity being measured. Verified: two
consecutive full runs are byte-identical.

It corrected two conclusions that were never real: **RTD's best model** (XGBoost →
LightGBM, old margin 0.43 pp) and **3 of 12 holiday-ablation signs**.

> Numbers: `../.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision/LOCKED_STATE.md`
> Detail: same folder, `findings.md` F18–F20.

### (b) The H1-mislabelled-as-H3 defect — FIXED 2026-09-07

It was **three** defects in three layers, not the one P0048 reported. See
`findings.md` F23 for the full record.

| Layer | Was | Now |
|---|---|---|
| Features | `engineer_features()` ignored the horizon; h1 and h3 matrices byte-identical in every lag | required `horizon` arg; every past-derived feature shifts by an extra `h − 1` |
| Scoring | `srq4_experiment.py` scored `test.iloc[0]` = cutoff+1, whatever matrix it read | `HORIZON = 3`, scores `test.iloc[HORIZON − 1]` |
| Serving | `forecast_tool` called with no month → defaulted to the first test month | scored month passed explicitly; payload carries `months_ahead` |

**Layer 2 was the dangerous one.** Fixing only the features would have produced
correct-looking matrices, a passing pipeline, and the same wrong number.

Verified: all 8 matrices rebuilt; `h3.lag_1 == h1.lag_3` exactly (the offset is precise,
not merely different); **H=1 byte-identical to the old definition**, so nothing published
at H=1 changes; the leakage assert now requires the gap to *equal* the horizon and fires
on a forged 1-month gap; `verify_setup.py` **10/10, no warnings**.

**Still expected: H3 accuracy should worsen once models are retrained.** The models on
disk are still H=1-trained.

---

## 2. Do these in this order

**Updated 2026-09-10.** The experiment side is now code-complete: all five
scenarios exist and the pre-flight is green. What is left is spending money, and
two questions that should be answered before it is spent.

| # | Do | State |
|---|---|---|
| ~~1~~ | ~~Horizon fix~~ | ✅ **DONE** 2026-09-07 |
| ~~2~~ | ~~Parameterise the horizon~~ | ✅ **DONE.** F24 is resolved — `SRQ1_HORIZON` drives both the matrix read and the results path, so an H=1 run cannot overwrite an H=3 result |
| **2b** | **Retrain SRQ1** | **RUNNING ON THE HPC** (P0053). Models on disk are still H=1-trained, so Scenario C serves an H=1 model against H=3 features until it lands. **This gates step 4, not step 3.** |
| ~~3~~ | ~~Scenarios D and E~~ | ✅ **BUILT 2026-09-10** (`a941927`). Written, wired, verified free. **Never run.** |
| **3b** | **Smoke D and E — ~$0.90** | **NEXT, and it spends money.** Replaces both placeholder cost estimates with measurements. A defect here costs $1; in step 4 it costs $40 |
| **3c** | **Answer Q-A / Q-B / Q-C** | `findings.md`, under OPEN QUESTIONS. Q-A is now *partly* answered: the full five-scenario ladder at 3 stratified brands per category dry-runs to **60 runs / ~$17** |
| **4** | The funded set | Gated on 2b, 3b and 3c |

### What changed on 2026-09-10, in one line each

- **Scenarios D and E exist.** `SCENARIOS` holds all five; `--scenarios D,E`
  selects them. `verify_setup.py` is **13/13** with the engine and **11 + 2
  skipped** without it, so an assessor running A–C is never blocked.
- **DEC-D-SNAPSHOT is measured, not enforced** (F45). Prometheus is a two-agent
  delegation and its data tools are hardcoded in the nested coder, so they cannot
  be filtered out by configuration. A run that queries the warehouse is
  **detected and excluded** instead. Say this in the limitations as written.
- **The prompt schema is now `v4-five-scenarios`** (F44). A/B/C strings are
  byte-identical to v3, verified — but v3 and v4 rows are deliberately not
  pooled. This is why D/E had to land *before* the funded set.
- **Nothing has been spent.** The scenario-input CSVs and the D/E code were both
  built and verified without a paid call.

### Before running anything tomorrow

```bash
git fetch origin && git log origin/main --oneline -5   # the HPC and VPS push here too
python 04_SRQ4_Scenario_Experiment/scenario_setup/verify_setup.py
```

The pre-flight is the honest check that the engine is still reachable and that
the guard is armed. It sends no request and costs nothing.

---

## 3. A defect fixed today that would have wasted the funded runs

`02_SRQ2_Tool_Interface/forecast_tool.py` read its track-record CSVs
(`cv_metrics.csv`, `tuned_metrics.csv`, `stat_baselines.csv`) from the results **root**.
They live in `tables/`. Both reads sit inside `try/except`, so the tool **degraded
instead of failing** — returning a valid payload with the `historical_*` accuracy fields
simply **absent**.

Those fields are the thesis contribution. SRQ2's interface exists to carry "forecast
**plus** its measured reliability", and SRQ4's B→C comparison tests whether that evidence
changes an LLM's answer. **Scenario C would have run without the very thing that makes it
C, and the logs would have looked normal.**

Fixed to `get_srq_tables_dir(1)`. Verified after: `historical_wmape: 16.6`,
`historical_median_mape: 33.7` — present where they were absent. (F21)

**The lesson, because it will recur:** `verify_setup.py` printed **`READY — all 10 checks
passed`** *and* two `!` warnings on the same run. **Read the warnings.** A soft-failing
read is worse than a hard-failing one.

---

## 4. Every active plan, and what is actually open

| Plan | Status | What is genuinely open |
|---|---|---|
| **P0039** srq4-system-a-vs-b | focus | **Its stated blocker is STALE.** It says "blocked on `03_thesis_modelling/.env`" — that path no longer exists; `.env` is at repo root with 11 keys, and `verify_setup.py` now passes 10/10. Open decision **DEC-VENDOR** (~$7 Claude vs ~$4 GPT for 50 runs — decide on ecological validity, not cost). |
| **P0040** prometheus-scenarios-d-e | focus | Scenarios D/E. **Largely discharged 2026-09-10**: `run_scenario_d` / `run_scenario_e` are written and wired (`a941927`), and the E2B template was already built (2026-08-21, P0040 F42 — the 'unbuilt' claim was stale). What remains is running them. |
| **P0042** funded-testing-sequencing | focus | The ordering plan. Sampling design frozen at **111 runs / ~$40**. A/B/C ladder already delivered (2026-08-19, $4.92). Gate 1 open for D/E. **Now also gated on the horizon fix (F22).** |
| **P0044** resource-measurement | in_progress | Ch1 rewrite on the measured 4 GB bound, then scenarios F/G. Measured: refit 2.93 s vs re-tune 417 s (**142×**); 7-month param drift inconclusive. |
| **P0045** draft-bullet-reconstruction | in_progress | 6 of 11 tasks open. Writing-surface work. |
| **P0046** figure-table-provenance | in_progress | Phase 5: publish the inventory, then choose citations. 25 appendix tables, 5 producers, all regenerating. |
| **P0047** exogenous-enrichment (folder says P0046_…21-10) | numbers locked | Holiday enrichment shipped: **7/12 helped, mean −1.42 pp**. Open: Word threads (task 8), claims verification (task 22) — both Brian's. |
| **P0048** remaining-prose-and-citations | in_progress | **Parallel session.** Prose from ch4 onward. Found the horizon defect. Don't do prose from P0049. |

---

## 5. Traps

1. **`LOCKED_STATE.md` says "locked".** It means *locked against drift*, not *final*.
   The horizon fix will change every number in it.
2. **`srq1_profiling.py` still has `n_jobs=-1`. That is correct.** It measures resource
   cost under realistic multi-core execution and records the core count. Don't "fix" it.
3. **P-ID collisions have happened twice.** Two `P0046_*` folders exist (this plan set is
   *P0047*, in the folder named `P0046_…21-10`), and P0048 was claimed by the parallel
   session while this one was being written — hence P0049. **Check `plans/` before
   claiming an ID.**
4. **Five SRQ1 tables predate the determinism fix and that is fine** — all measure time
   or memory, not accuracy (F20). But **no script in the repo generates three of them**
   (`param_drift`, `refit_vs_retune`, `retune_single_cutoff`); only the SRQ4 appendix
   reads them. Refreshing means reconstructing the generator.
5. **Adding an XGBoost call site?** Import `XGB_N_JOBS`. Never write a literal.

---

## 6. Unverified claims — never cite these

Register: `06_thesis_writing/writing-notes/unverified-claims-to-check.md`
Briefs: `06_thesis_writing/notebookLM/04-Claims_Verification/`

CV-01 VIF 5/10 · CV-02 Spearman ≥0.95 · CV-03 Lukkeloven 2012 · CV-04 XGBoost thread
mechanism · CV-05 Store Bededag abolition.

CV-01's attribution to *Hair et al. (2019)* was **invented from memory** and removed.
That is why this register exists.

**Rule: if a source is not in the Zotero library, it is not a source.**
