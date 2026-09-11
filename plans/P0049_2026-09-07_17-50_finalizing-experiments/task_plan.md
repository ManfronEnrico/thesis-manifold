---
pid: P0049
created: 2026-09-07 17:50:00
updated: 2026-09-11 23:45:00
status: in_progress
focus_detail: "EXPERIMENT SIDE, 2026-09-11. **SEVEN scenarios, all measured, all green.** The ladder is A_llm_plain / B_llm_data / C_llm_model / D_prometheus_data / E_prometheus_model / F_llm_data_model / G_prometheus_data_model -- F and G are the COMBINED arm (history + code + the model payload together) added this session, and every arm was renamed to <letter>_<orchestrator>_<inputs> so the two ladders pair column-wise. Schema v5-seven-scenarios+d22fe7cdc30e; A-E strings are byte-identical to v4 so earlier paid runs stay poolable. Seven-arm smoke ran 2026-09-11 on CSD/HARBOE, billed $3.62, all 8 checks pass. THE HEADLINE: F and G both carry deviates_from_model=True -- neither returned the model number, and both cited its low confidence tier and wide interval as the reason, so DEC-COMBINED-INPUT measured integration rather than deference. sql_calls empty on D, E AND G. THE THREE OPEN QUESTIONS ARE ANSWERED (DEC-MVP-DESIGN): same 3 brands across all arms, CSD only, 39-month shared input -- all three resolve to existing harness behaviour. NEXT: the funded MVP, 3 CSD brands x 3 repeats x 7 arms = 63 runs, ~$19 raw and ~$34 at the observed under-estimate ratio. TWO THINGS FIRST: price web search (F57 -- it is detected but contributes $0 to every estimate, and cost_usd_est has under-reported on BOTH billed runs, 1.20x and 1.77x), and note the volume floor is now IN (F58, MIN_SCORED_UNITS=1000) because stratifying CSD returned VOELKEL at 9 units/month where one unit is 11% APE. Floored sample is HARBOE / 7-UP / ØRBÆK."
---

# P0049 — Finalizing experiments

> **Figures, tables and diagrams are owned by
> [P0050](../P0050_2026-09-07_18-40_figure-table-generation-and-provenance/START_HERE.md)**
> (also written for this account switch). Any artefact you need to cite, or find
> stale, belongs to that plan — 11 diagrams and 25 appendix tables regenerate
> from 5 scripts.


## Goal

Get the SRQ1 model numbers to a state that is **both reproducible and correctly
labelled**, then run the funded SRQ4 scenarios against them.

Reproducibility is done. Labelling is not.

## Why this plan exists

Seven plans were active at once, each holding part of the experimental picture, and the
account switch loses the conversation that held them together. This plan is the join:
one ordered sequence, with the blockers stated as they actually are rather than as the
older plans describe them.

Two of those older descriptions were **wrong when checked**:

- P0039 says it is blocked on `03_thesis_modelling/.env`. That path does not exist;
  `.env` is at the repo root and `verify_setup.py` passes 10/10.
- `LOCKED_STATE.md` said the funded runs were unblocked. The horizon defect is upstream
  of them.

Checking a stated blocker before acting on it is the main lesson of this plan.

## Keeping this plan current (Brian, 2026-09-10)

**This plan is updated every time an insight or an open question appears** — not
at the end of a session. Three machines (laptop, VPS, HPC) read these files as the
shared context, so an insight held in one conversation is an insight the other two
do not have.

| What | Goes to |
|---|---|
| A measured fact, or a corrected belief | `findings.md`, numbered |
| A question that is not yet answered | `findings.md`, under **OPEN QUESTIONS**, dated and attributed |
| A settled decision | the decisions table below, with its evidence |
| What happened in a session | `progress.md` |

An unanswered question left in a conversation is lost when that conversation ends.

## Phases

### Phase 1 — Horizon ✅ DONE (2026-09-07)

It was **three** defects in three layers, not one — see `findings.md` F23. Fixing only
`engineer_features()` would have left the experiment still scoring one month ahead.

1. ✅ `engineer_features()` takes a required `horizon`; every past-derived feature
   shifts by an extra `h − 1`. H=1 is byte-identical to the old definition.
2. ✅ `srq4_experiment.py` scores `test.iloc[HORIZON − 1]`, not `test.iloc[0]`.
   `HORIZON = 3` is one constant selecting both the matrix and the scored month.
3. ✅ Scenario C passes the scored month to the tool; the payload carries
   `months_ahead`. The leakage assert now checks the gap is **exactly** the horizon.
4. ✅ Steps 4–6 re-run, 4 categories × H=1,3. All 8 matrices published and verified:
   `lag_1` differs across horizons and `h3.lag_1 == h1.lag_3` exactly.
5. ✅ `verify_setup.py`: **10/10, no warnings.**

**Still to come: H3 accuracy should worsen after retraining.** Three months ahead is
harder than one. The models on disk are still H=1-trained — that is phase 2.

### Phase 2 — Re-run SRQ1 on both horizons (IN PROGRESS)

**DEC-HORIZON-BOTH (Brian, 2026-09-07): run H=1 and H=3 properly, both.**

The horizon is now a single value per run, `SRQ1_HORIZON` (default 3), read by
`srq1/_horizon.py` and used for **both** the input matrix and the output directory —
so the two can never describe different horizons.

| Horizon | Matrix | Results go to |
|---|---|---|
| **3** (primary) | `*_feature_matrix_h3.parquet` | `srq1_model_performance/{tables,figures,models}/` |
| **1** (secondary) | `*_feature_matrix_h1.parquet` | `srq1_model_performance/h1/{...}/` |

H=3 keeps the unsuffixed paths because `forecast_tool.py`, the SRQ4 harness, the
appendix exporter and the figure generators all read them. **An H=1 run therefore
cannot overwrite an H=3 result** — the property that makes this safe.

Run it: `python model_training/run_both_horizons.py` (`--dry-run`, `--horizon`,
`--only` available). 8 ordered stages × 2 horizons; the order is a dependency chain,
not a bag of scripts.

**Sanity check already passed** (untuned benchmark): H=3 is worse than H=1 in 3 of 4
categories — the plan's own test that the fix took effect. RTD moves the other way;
F26 records why that is real rather than survivorship, and what still needs confirming.

**Training moved to the HPC on 2026-09-08** after three OS memory kills on the laptop
(F27: the suite needs ~282 MB; the machine had ~1.2 GB free with Word, VS Code and two
Claude sessions resident). The run procedure is **P0053**, written to be read from the
HPC with no conversation history.

**The HPC must be on `ae4c290` or later.** Anything started before `3f8b0a9` is training
on 13 features instead of 18 (F31), and anything before `9745bf3` silently drops
Danskvand and Energidrikke on Linux.

Two defects found while doing this — see `findings.md`:
- **F24** — 13 scripts hardcoded `_h3`; none could produce H=1.
- **F25** — `train_and_persist.py` read its selection inputs from the tier root
  instead of `tables/`, so **model selection silently fell through to a hardcoded
  `"XGBoost"` default** and never consulted the CV study. The default was wrong for
  all four categories.

### Phase 3 — Re-verify the SRQ4 harness

`python 04_SRQ4_Scenario_Experiment/scenario_setup/verify_setup.py`

Required: **10/10 and no `!` warnings**. A warning here means the tool is serving
degraded payloads (see F21). Passing as of 2026-09-07, but **re-run after phase 2** —
the tool loads the persisted model, so retraining changes what it serves.

### Phase 3b — Smoke test ✅ BUILT (2026-09-09)

`04_SRQ4_Scenario_Experiment/scenario_setup/smoke_test.py` — one run per scenario,
**~$0.81**, into a `smoke/` subfolder under a `--budget` cap. Never the results
directory.

`verify_setup.py` never sends a request, so it cannot see what only appears when a
scenario runs. Nine checks, each traceable to a stated requirement rather than chosen
for coverage — see F34. Four come straight from ch2 §2.5's auditability taxonomy.

```bash
python 04_SRQ4_Scenario_Experiment/scenario_setup/smoke_test.py --dry-run   # free
python 04_SRQ4_Scenario_Experiment/scenario_setup/smoke_test.py            # ~$0.81
```

**Run it once the HPC results land**, before phase 4. A defect found here costs $1; the
same defect in phase 4 costs $40.

### Phase 4 — Funded runs

P0042's frozen sampling design: 111 runs, ~$40, allocated inversely to per-run cost
(A n=3, B/C n=10 stratified, C-only cross-category). DEC-VENDOR is settled (2026-09-10).

**The population change does NOT affect the allocation — checked 2026-09-10.** F32 took
scorable brands from 120 to 168, but `--brand-strategy stratified` picks
highest/median/lowest volume per category, which is population-relative by construction:
still 3 per category at either size. The larger population makes those picks more
representative, not the design different. No re-freeze needed.

### Phase 5 — Scenarios D and E ✅ BUILT (2026-09-10), not yet run

`SCENARIOS` holds all five; `--scenarios D,E` selects them like any other.

| | Mirrors | Gets | Verified |
|---|---|---|---|
| `D_prometheus` | B | the same series `_brand_history()` gives B | prompts render, degrades cleanly with no engine |
| `E_prometheus_model` | C | the same payload `_eval_forecast()` gives C | payload completeness checked as in C |

**Everything vendor-shaped is in `prometheus_bridge.py`**, which runs the engine
in its own interpreter. Importing it is allowed to fail: an assessor with A–C,
the shipped CSVs and an OpenAI key must still be able to run the harness.

Three things the build corrected, all in `findings.md`:

- **F45** — Prometheus is a **two-agent delegation**. The conversational agent's
  only data verb is `invoke_prometheus_coder`; the five data tools belong to a
  nested coder and are **hardcoded at module scope**, not passed through
  `ProjectDeps`. So DEC-D-SNAPSHOT cannot be enforced by configuration. It is
  **measured** instead: a run that queries the warehouse is detected and
  classified `warehouse_access`, and excluded. That is stronger evidence than a
  filtered tool list, because it is observed per run rather than trusted once.
- **F46** — the two venvs are **disjoint** (thesis 3.14 has xgboost, no
  langgraph; engine 3.13 the reverse). D/E therefore cross a process boundary,
  and **E works because the parent evaluates the model and injects the payload**
  — which also gives E's number the same origin as C's.
- **F44** — adding the D/E notes changed `schema_id()` to **v4-five-scenarios**.
  A/B/C strings are byte-identical to v3 (verified), but v3 and v4 rows are
  deliberately not pooled. **This is why D/E had to land before the funded set.**

**Next: smoke them.** `python smoke_test.py --scenarios D,E` (~$0.90 estimated).
That run replaces both placeholder cost estimates with measurements. A defect
found there costs $1; the same defect in the funded set costs $40.

## Decisions carried in

| ID | Decision | State |
|---|---|---|
| **DEC-VENDOR** | All SRQ4 scenarios run `gpt-5.5-2026-04-23` | **MADE 2026-09-10.** Decided on ecological validity: the Prometheus engine's own config sets `main_agent_model` and `coder_model` to `gpt-5.5`, so D/E run it regardless — a vendor split would put model family into the B→C vs D→E comparison. Argument: `writing-notes/dec-vendor-model-choice.md` |
| **DEC-HORIZON** | Implement both horizons, benchmark both, SRQ4 at 3 months | **MADE** (Brian, via P0048); implemented + verified 2026-09-07 |
| **DEC-HORIZON-BOTH** | H=1 and H=3 both run properly. H=3 primary, keeps the unsuffixed result paths; H=1 writes to `h1/` | **MADE** (Brian, 2026-09-07) |
| **DEC-DETERMINISM** | Accuracy at `n_jobs=1`; resource profiling at `-1` | **MADE**, implemented, verified |
| **DEC-GRAIN** | brand × month | Locked, earlier |
| **DEC-SHARE-CSV** | The filtered per-brand CSVs Scenario B receives DO ship to assessors, so A–C stay re-runnable with their own OpenAI key. Prometheus and `.env` do not | **MADE 2026-09-10** (Brian). Those CSVs are already filtered and aggregated — not live access, not the dataset — so they disclose no more than the thesis tables. Export must materialise them as files; the engineered matrices are not shipped. See F42 |
| **DEC-D-SNAPSHOT** | Scenarios D/E read the same local snapshot Scenario B gets — NOT the live `Nielsen_clean` warehouse | **MADE 2026-09-10** (Brian). Matching B's data path is what keeps D→E comparable to B→C. **Mechanism corrected 2026-09-10 (F45): it is MEASURED, not enforced** — the SQL tools are hardcoded into the vendor's nested coder agent and cannot be removed without forking it, so a run that queries the warehouse is detected and excluded instead. Disclosed in the limitations as written |

## What this plan does NOT cover

- **Prose insertion** — P0048, parallel session.
- **Word comment threads / claims verification** — Brian's, tracked in P0047.
- **Figure/table provenance Phase 5** — P0046.

## Related

- `START_HERE.md` — read first
- `../.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision/LOCKED_STATE.md` — the numbers
- `../.archive/P0046_2026-09-05_21-10_exogenous-enrichment-decision/findings.md` — F18–F22
- `../P0048_2026-09-07_13-51_remaining-prose-and-results-citations/START_HERE.md` — horizon origin

---

# STATUS 2026-09-11 - read this before touching the experiment

Appended by the session that ran the seven-arm smoke. Supersedes any earlier
statement in this file about scenario count, arm names, costs or open questions.

## The ladder is SEVEN arms, and they were all renamed

| key | orchestrator | inputs |
|---|---|---|
| `A_llm_plain` | hosted LLM | none (web search only) |
| `B_llm_data` | hosted LLM | history + code sandbox |
| `C_llm_model` | hosted LLM | typed `forecast_demand` tool |
| `D_prometheus_data` | Prometheus | history + code (B on production) |
| `E_prometheus_model` | Prometheus | model payload (C on production) |
| `F_llm_data_model` | hosted LLM | history + code + model payload |
| `G_prometheus_data_model` | Prometheus | F on production |

Every name is `<letter>_<orchestrator>_<inputs>`, so the two ladders pair
column-wise: B/D, C/E, F/G. **The old names are gone from code, CSVs and cached
response filenames** - migrated 2026-09-11, measured values untouched.

`A -> B` data access, `B -> C` the dedicated model, `C -> F` code on top of the
model, `D -> E -> G` the same three rungs on production.

## What the smoke measured (CSD/HARBOE, 2026-03, actual 6,365,900, billed $3.62)

| arm | forecast | APE | latency | est cost | code blocks |
|---|---|---|---|---|---|
| A_llm_plain | 4,900,000 | 23.0% | 119.5 s | $0.543 | - |
| B_llm_data | 6,700,000 | 5.2% | 91.3 s | $0.224 | 15 |
| C_llm_model | 4,969,050 | 21.9% | 6.7 s | $0.009 | - |
| D_prometheus_data | 6,379,795 | 0.2% | 113.6 s | $0.519 | 4 |
| E_prometheus_model | 4,969,050 | 21.9% | 41.7 s | $0.202 | 0 |
| F_llm_data_model | 6,200,000 | 2.6% | 75.3 s | $0.223 | 12 |
| G_prometheus_data_model | 5,604,800 | 12.0% | 80.9 s | $0.327 | 2 |

**The result that matters: `deviates_from_model=True` on BOTH F and G.** Neither
returned the model's 4,969,050, and both named its low confidence tier and wide
interval as the reason to weigh it rather than adopt it. That is the typed
payload carrying decision-relevant information - a result for SRQ2 independent
of accuracy. `sql_calls: []` on D, E and G; `usage_reported: true` on all three.

**Do NOT read the accuracy ordering as a finding.** A moved 38.7% -> 23.0% and B
1.0% -> 5.2% between two runs on identical prompts. Within-arm spread is
comparable to between-arm gaps at n=1.

## The three open questions are ANSWERED - see DEC-MVP-DESIGN in findings.md

| | question | answer |
|---|---|---|
| Q-A | brand pairing | **same 3 brands, all seven arms** |
| Q-B | dataset scope | **CSD only**, declared in design AND limitations |
| Q-C | shared input | **keep the 39-month aggregate** |

All three resolve to what the harness already does. No code change was needed.

## Next action: the funded MVP

3 CSD brands x 3 repeats x 7 arms = **63 runs**.

| basis | total |
|---|---|
| raw harness estimate | $19.32 |
| x1.2 (observed) | $23.19 |
| **x1.77 (observed)** | **$34.20** |

Fund ~$40. `--repeats` is one value for all arms, so a mixed allocation needs
two invocations; caching makes the second skip what the first completed.

### Two things before spending

1. **Price web search (F57).** It is detected and recorded but contributes $0.00
   to every estimate; the smoke's billing export shows a $0.20 line item.
   `cost_usd_est` has under-reported on **both** billed runs - 1.20x and 1.77x.
   Add `PRICE_WEB_SEARCH_PER_CALL` and count the items in `_usage()`.
2. **The volume floor is IN (F58).** `MIN_SCORED_UNITS = 1000`, applied by
   `_above_volume_floor()`. Stratifying CSD without it returned **VOELKEL at 9
   units/month**, where one unit of error is 11.1% APE. Floored pool is 45 of 76
   CSD brands; the sample is **HARBOE (6,365,900) / 7-UP (13,042) / ØRBÆK
   (2,850)** - still three orders of magnitude, worst-case rounding 0.035%.

## Where the reasoning lives

| topic | file |
|---|---|
| every finding F49-F58, DEC-MVP-DESIGN | `findings.md` (this folder) |
| the conclusion the evidence can carry | `writing-notes/ch8_experiment/the-defensible-conclusion-shape.md` |
| brand inclusion criteria + the floor | `writing-notes/ch8_experiment/brand-sampling-and-inclusion-criteria.md` |
| Ch6 anchored fixes | `writing-notes/ch6_architecture/` |
| final figure/table regeneration | P0050 (F36 = the relettering defect) |
| submission repo scope | P0054 (F-SUBMIT) |
