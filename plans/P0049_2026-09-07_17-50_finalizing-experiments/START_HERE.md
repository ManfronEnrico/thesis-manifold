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

| # | Do | State |
|---|---|---|
| ~~1~~ | ~~Horizon fix~~ | ✅ **DONE** 2026-09-07 |
| **2** | **Retrain SRQ1** | **NEXT.** Models on disk are H=1-trained; Scenario C currently serves an H=1 model against H=3 features. **Read F24 first** — it decides what phase 2 *is*. |
| **3** | Re-verify the SRQ4 harness | Passing now, but re-run after retraining — the tool loads the persisted model. |
| **3b** | **Smoke test, n=1/scenario, ~$1** | Brian, 2026-09-07. `verify_setup.py` checks contracts, not an end-to-end run. A defect found here costs $1; in step 4 it costs $40. |
| **4** | P0042's ~111 funded runs (~$40) | Still last. |

**An open decision gates step 2** (F24): 13 live SRQ1 scripts hardcode `_h3`, so they now
read genuine H=3 features — but **none can produce H=1**. Either retrain at H=3 only
(faster, unblocks the funded runs) or parameterise the horizon across those 13 scripts
first. Do not find-and-replace to `h1`: that just swaps which horizon is unreachable.

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
| **P0040** prometheus-scenarios-d-e | focus | Scenarios D/E (real Prometheus engine). Tasks 1–3 done; nothing externally blocked. **Next: build the E2B template** — required, because the base image lacks statsmodels/prophet, so D would be silently handicapped. |
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
