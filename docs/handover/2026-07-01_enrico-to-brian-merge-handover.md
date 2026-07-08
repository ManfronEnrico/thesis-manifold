---
name: enrico-to-brian-merge-handover
description: HANDOVER - everything merged to main on 2026-07-01, decisions Brian must know, and how to proceed with Ch4 + remaining EDAs
category: handover
applies-to: [ch4-writing, eda-replication, preprocessing, srq4-code-as-action]
triggers: [what-changed-on-main, how-to-start-ch4, eda-decisions, srq4-status]
created: 2026-07-01
updated: 2026-07-01
---

# Handover: Enrico → Brian — the 2026-07-01 merge to main

**Status**: main now contains the UNION of your data-engineering track and Enrico's modeling/agentic/thesis track. Nothing of yours was dropped; a few files were superseded (listed below, with reasons).

---

## In 30 seconds

- ✅ **SRQ1 (forecasting) DONE**: tuned XGBoost wins every category; per-category granularity locked; all results in `thesis/data/_05_results_srq1/`
- ✅ **SRQ2 (synthesis) DONE**: deterministic ensemble + Claude synthesis + GPT-4o judge; results in `_06_results_srq2/`
- ✅ **SRQ4 (dedicated tool vs code-as-action) BUILT**: working harness, demo ran; full run paused at the pay-wall until prompt review with Enrico
- ✅ **Your 13-fix CSD EDA adopted** — plus we repaired 2 bugs in Cell 12 (it had never run end-to-end; now it does, 100%)
- ✅ **Thesis chapters Ch1–Ch10 drafted** from real results (pending human review); references now carry peer-reviewed anchors for all 4 SRQ4 KPIs (supervisor request — done)
- 🟡 **Your region grain is intact but NOT adopted as default** — waiting on your WMAPE test (see §5)
- ❌ **9.8M raw data is NOT in git** (gitignored) — we need the parquets from you (§8)

**Next for you**: remaining EDAs (danskvand / energidrikke / RTD) + finish Ch4 (§6), and glance at the code-as-action material (§7).

---

## 1. What happened (branch topology)

Since the common ancestor (`4a62cbb`, the SRQ1-3 integration), the two tracks never touched the same layers:

| | Your `main` added | Enrico's branch added |
|---|---|---|
| Layer | Data engineering | Modeling + agentic + thesis |
| Content | 9.8M CSD refetch, DVH filter, 13-fix EDA, region grain, folder/docs cleanup | SRQ1 tuned results, SRQ2, SRQ4 harness, forecast service, Oracle skeleton, Ch1–Ch10 drafts, references |

The merge (`f85a7a6`) unions both. Resolution policy, so you can trust the tree:

| Kept from **main (yours)** | Kept from **Enrico's branch** |
|---|---|
| `.claude/` rules & skills org, `docs/` restructure, `plans/` | `pre_csd_1.5_eda.py` (= your 13 fixes + our Cell 12 repair) |
| `scripts/ml_retraining/`, `datasets/`, `_00_raw/`, `_01_converted/` | all `scripts/srq1_* srq2_* srq4_*`, `forecast_service.py` |
| **`_02_preprocessing/` incl. your region-grain pipeline, untouched** | `_03_engineered_dvhexclhd/`, `_04_engineered_bychain/`, `_05.._07` results |
| | `thesis/thesis-writing/` (all chapters + references), `thesis/thesis-context/` |
| | `thesis/thesis_agents/system_a_oracle/`, `CLAUDE.md`, `README.md` |

`.gitignore` = line union of both.

---

## 2. Decisions we made that you must know (EDA / preprocessing)

These are LOCKED decisions (approved by Enrico, written into chapters). Please don't silently re-decide them — if you disagree, raise it, there's usually a documented reason.

1. **Market scope = `DVH EXCL. HD` via `market_id` dedup + single-id filter** (`thesis/data/preprocessing/nielsen_dvh/build_feature_matrix.py`). Dedup the SCD market dim on `market_id` BEFORE merging, then filter to the single scope id → cross-market double-count is impossible by construction. (The old all-markets sum inflated CSD 6.16x, other categories 14–17x.)
2. **MIN_PERIODS = 30 global** (40 is infeasible for danskvand/energidrikke/RTD — only 37–39 periods exist).
3. **Granularity is per-category, decided by tuned test WMAPE** (Ch6 §6.5.6): CSD / energidrikke / RTD = brand×month (`_03`); danskvand = brand×chain (`_04`). We tested the finer grain — it only helps danskvand. This is why "more rows" alone never decides grain (see §5 for your region idea).
4. **Scope = 4 categories for the forecasting study** (CSD, danskvand, energidrikke, RTD). Totalbeer is OUT (facts absent at source). CSD-only is fine ONLY for the live agentic PoC — as agreed on WhatsApp 01/07.
5. **Metrics: WMAPE + median per-series MAPE + interval coverage.** Mean-MAPE is degenerate on low-volume series — never report it alone.
6. **Locked SRQ1 numbers** (tuned XGBoost, test WMAPE): CSD **16.5%**, danskvand **22.0%**, energidrikke **11.4%**, RTD **31.0%**. Beats ARIMA in 3/4. SHAP: `lag_1` + `weighted_distribution` dominate.
7. **Warmup = 13 periods per brand** (max lag/window). Your leakage point: good news — the training pipeline was never leaking (features use `shift()` / `shift(1)`), your fix correctly documents the warmup in the EDA. No results were contaminated, nothing was re-run.

---

## 3. Your EDA: adopted, repaired, and what it now outputs

We adopted your 13-fix `pre_csd_1.5_eda.py` wholesale — the fixes are genuinely good (per-brand ADF, Chow break, Spearman, decomposition auto-select, zero-sales, heterogeneity, warmup split validation). Two bugs we fixed in **Cell 12** (commit `1d55145`):

1. `series[max(0,i-w):i].mean()` at `i=0` is an empty-slice → `NaN` → `np.std(feature) > 0` was never True → **no window ever qualified → KeyError crash**. Cell 12 had never completed for anyone.
2. Same NaN made the collinearity `corrcoef` NaN → `NaN > 0.95` always False → **pruning silently never pruned**.

Both fixed with NaN-masking; the cell now fails loudly if no window qualifies. Full EDA runs 100% end-to-end. On our **partial** raw (2.5M rows, 86 brands) it derives: `LAGS=(1,2,3,4,8,12,13)`, `ROLLING_WINDOWS=(2,13)`, `HOLIDAY_MONTHS={9,12,6}`. ⚠️ **Re-derive all of these on the full 9.8M data** — treat our values as placeholders.

---

## 4. Supervisor request: KPI grounding — DONE

The supervisor asked for academic articles grounding the 4 SRQ4 KPIs. Status (all in `references.md`, wired in-text in Ch2 §2.5 + Ch3 SRQ4):

| KPI | Peer-reviewed anchor |
|---|---|
| Correctness | Hu et al. 2024 (ICML, InfiAgent-DABench) |
| Consistency | **Ouyang et al. 2025 (ACM TOSEM)** + Atıl et al. 2025 (Eval4NLP@ACL, TAR@N) |
| Replicability | Zeng et al. 2025 (EMNLP Findings, AIRepr) |
| Cost / latency | **Chen et al. 2024 (TMLR, FrugalGPT)** + Schwartz et al. 2020 (CACM, Green AI) |

Mehta/CLEAR and Bhattacharyya stay as corroborating preprints. If you add citations, use `/cite` (never edit `references.md` by hand).

---

## 5. Your region grain: intact, pending YOUR test

`pre_csd_1_load_and_aggregate.py` (brand×region×period, 25.1k rows) is untouched on main. It is **not** the default because it was chosen on sparsity alone, with no forecast validation — and our chain experiment shows finer grain can *hurt* (it did, for CSD). The agreed decision procedure (WhatsApp 01/07):

> Run tuned WMAPE on the region grain, **re-aggregated back to brand-national**, vs our 16.5% brand×month. Region wins → we switch. Otherwise → month stays, region becomes a limitation note.

Until then: **don't overwrite `_03_engineered_dvhexclhd/` or `_04_engineered_bychain/`** — the SRQ4 harness and all SRQ1 results read from them.

---

## 6. Chapter 4 — how to proceed

**Current state**: `thesis/thesis-writing/sections-drafts/ch4-data-assessment.md`, ~78% done, real numbers, Saunders 3-stage backbone, §4.3.6 has the per-category EDA summary. Read it BEFORE writing — much is already there.

**What's missing (your part):**
1. **Dedicated EDAs for danskvand / energidrikke / RTD** — replicate the (fixed) `pre_csd_1.5_eda.py` template per category. Light findings already exist in `thesis/data/_03_engineered_dvhexclhd/eda_findings_dvhexclhd.md` (ADF, promo, seasonality, top brands per category) — extend, don't duplicate.
2. **Refresh CSD numbers on the 9.8M refetch** where Ch4 cites extract-level figures.
3. **§4.3 prose from the EDA outputs** — keep the corrected inflation narrative (6.16x, market-scope) exactly as is.

**Workflow rules (project law):**
- Bullets first → **Enrico approves** → prose. Never prose without approval.
- After any approved edit: regenerate docx via `pandoc thesis/thesis-writing/sections-drafts/ch4-data-assessment.md -o thesis/thesis-writing/sections-final/ch4-data-assessment.docx`
- APA 7 via `/cite`; verify with `/verify-citations`.

---

## 7. Code-as-action (your review welcome)

Where the code-as-action LLM material lives:
- **`scripts/srq4_experiment.py`** — System B mirrors Prometheus: brand history preloaded as `df` (≈ your `run_sql`), Claude writes+runs its own forecasting code in an E2B sandbox, ≤8 tool turns, sentinel answer. Same LLM (Sonnet 4.6, temp 0) as System A for fairness. **Check the Prometheus fidelity** — you know the production system best.
- **Ch2 §2.4** (literature: Wang et al. code-as-action), **Ch5** (architecture: why B is the baseline), **Ch8** (evaluation skeleton, fills after the full run).
- Harness state: upgraded (fair inputs to B: sales + promo + distribution; TAR@N consistency metric; cost in USD; 5 repeats) and **paused before any paid run** — Enrico reviews the 25 Tier-2 prompts first. Demo single-point result (HARBOE): B beat A on APE but at 3x latency / 5x tokens — do not read anything into n=1.
- Known open issue: for danskvand the harness's `_brand_history` mixes chains (brand×chain matrix) — handling TBD at the prompt-review checkpoint.

---

## 8. What we need FROM you

1. **The 9.8M CSD parquets** (git ignores `*.parquet/*.jsonl`) — drive/transfer link, or confirm the warehouse credential path (RU_CLIENT_SECRET was broken; Nika was to re-send).
2. **The region-vs-month WMAPE test** (§5) — you said "will do it asap".
3. Ch4 per §6.

---

## 9. Verify the merge in 2 minutes

```bash
git log --oneline -5                       # f85a7a6 merge on top
python3 scripts/srq4_tier2.py --selftest   # $0, no API — should end with SELFTEST PASS
python3 -m py_compile scripts/srq4_experiment.py scripts/forecast_service.py
ls thesis/data/ | grep "^_0"               # _00.._07 all present
grep -c "Ouyang" thesis/thesis-writing/references.md   # 2 → KPI anchors in
```

## 10. Reading order

1. This document
2. `docs/handover/2026-06-30-session-handover.md` — full session state (SRQ1-4, Prometheus, blockers)
3. `thesis/thesis-writing/sections-drafts/ch4-data-assessment.md` — before writing anything
4. `thesis/data/EXECUTION_PROGRESS.md` — status board
5. `thesis/data/PROMETHEUS_ARCHITECTURE_REPORT.md` — if you touch SRQ4/System B
