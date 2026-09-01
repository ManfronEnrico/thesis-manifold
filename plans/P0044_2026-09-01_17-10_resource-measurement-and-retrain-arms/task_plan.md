---
pid: P0044
created: 2026-09-01 17:10:00
updated: 2026-09-01 17:10:00
status: in_progress
focus_detail: "Phase 1 DONE: tracemalloc understated XGBoost 266x (0.1 -> 26.6 MB RSS); profiler now measures RSS per model in isolated subprocesses. Next: phase 2 writing-surface hygiene, then Ch1 reframing on the corrected numbers."
---

# P0044 — Resource measurement + retrain-in-sandbox arms

## Why this plan exists

Brian's Word comments [18] [19] [20] [22] [25] challenge the thesis's central
RAM premise. Investigation found the code half-supports him and half-refutes him:

- [25] "memory efficiency is not tracked" is WRONG -- `srq1_profiling.py` and
  `train_and_persist.py` both measure it, and `04_thesis_results/srq1/profiling.md`
  publishes a table.
- But the instrument is broken, which is what Brian actually suspected. It uses
  `tracemalloc`, which sees **only Python-level allocations**. LightGBM and
  XGBoost allocate their trees in C++. XGBoost reports **0.1 MB peak** -- less
  than Ridge, which is impossible for `n_estimators=1040, max_depth=10`.

So the published memory table understates tree models by an unknown factor, and
the whole ≤8 GB claim rests on it. **Fix the instrument before rewriting the
framing** -- otherwise the new promise sits on the same sand as the old one.

## Decisions

- **DEC-RSS** — measure process RSS, not `tracemalloc`. Native (C++) allocations
  are the dominant term for tree models and are exactly what `tracemalloc`
  cannot see.
- **DEC-SUBPROCESS** — profile each model in a **fresh subprocess**. In-process
  RSS never returns to baseline (allocators retain freed pages), so sequential
  models contaminate each other. One process per model is the only way to get a
  clean per-model number.
- **DEC-REFIT-NOT-RETUNE** — the retrain-per-query architecture refits on the
  **stored** hyperparameters in `cv_params.json`; it does not re-run Optuna.
  Tuning is hundreds of TPE trials; fitting on known params is 0.075-2.0 s.
  Tuned params are stable month-to-month, coefficients are what go stale.
  This is what makes the arms affordable and the argument defensible.
- **DEC-ARMS-LOW-N** — the two retrain arms run at n=3, matching the A-floor
  logic: enough for a directional signal, not enough to dilute the B/C and D/E
  contrasts that carry the contribution. Consistent with the frozen
  unequal-allocation design (P0042).
- **DEC-ARCHIVE-NOT-DELETE-PROSE** — `sections-drafts/*.md` becomes bullets-only;
  the current prose is moved to `.archive/`, not deleted. Two live prose copies
  with no authority rule is the drift P0043 exists to prevent.

## Tasks

### Phase 1 — fix the instrument (blocks the Ch1 rewrite)

- [x] **1. Replace `_profile()` with subprocess RSS measurement.**
      `srq1_profiling.py:82` currently does `tracemalloc.start()` / `get_traced_memory()`.
      Replace with: spawn one subprocess per model; sample RSS via `psutil`
      (installed, v7.2.2) in a poller thread at ~5 ms; report
      `peak_rss - baseline_rss`. Keep `tracemalloc` as a SECOND column so the
      old and new numbers sit side by side and the gap is visible and explicable.
      NOTE: `resource.getrusage` is NOT available -- Windows. psutil only.

- [x] **2. Capture the allocations tracemalloc misses, explicitly.**
      Per model record: peak RSS delta, tracemalloc peak (for contrast),
      serialised model size on disk, `n_estimators`/`max_depth` actually used,
      and thread count. XGBoost runs `n_jobs=-1` (line 119), so per-thread
      native buffers scale with core count -- the machine's core count must be
      recorded or the number is not reproducible.

- [x] **3. Fix the mislabelled title.** Line 140 reads
      "CSD brand×chain" but line 92 loads `get_category_engineered_bymonth_dir`.
      Stale label left by the P0035 grain removal. The published table is
      currently mislabelled with a grain that no longer exists.

- [x] **4. Re-run and compare.** Free (no API calls). Expect tree models to jump
      from ~0.1-8 MB into the hundreds of MB. If they do NOT, that is itself a
      finding and must be explained rather than assumed away.

- [ ] **5. Measure refit latency + RAM on the stored params** (feeds DEC-REFIT-NOT-RETUNE
      and the Ch9 argument). Separately record what a full Optuna re-tune costs,
      to show the gap that justifies refit-not-retune.

### Phase 2 — writing surface hygiene

- [x] **6. Delete `05_thesis_writing/sections-final/`.** All 6 files frozen
      2026-07-11; 4 of 10 chapters never exported. Superseded by the OneDrive
      document. Verified stale, not merely suspected.

- [x] **7. Strip prose from `sections-drafts/*.md`, archive the prose.**
      Ch1 draft (3,615 w) and snapshot (3,395 w) are the same text -- they agree
      only because nobody has edited either since the export. That luck expires
      the moment comment [17] gets acted on.

- [x] **8. Write the surface-authority rule** into `.claude/rules/`:
      OneDrive .docx = authoritative prose; `docx-exported-snapshots/` =
      read-only mirror; `sections-drafts/` = bullets only; `sections-final/` = gone.

### Phase 3 — Ch1 reframing (blocked by phase 1)

- [ ] **9. Rewrite the RAM premise as a result, not a promise.** Post-fix
      numbers only. RAM stops being "a hard constraint we operate under" and
      becomes "the serve-a-trained-model design fits commodity memory, which is
      what makes it deployable."

- [ ] **10. Promote the serving-approach contribution.** Comment [22]:
      the multi-indicator ML serving benefit on prediction quality, cost and
      latency is what SRQ4 actually measures and is currently under-elaborated.

- [ ] **11. Remove the exogenous-enrichment premise** (comments [15] [16] [17]).
      VERIFIED unsupported: live features in `engineer_features.py` are lags,
      rolling mean/std, month, quarter, peak_month, promo_intensity,
      zero_run_*, log_sales_units -- all endogenous or calendar-derived. Every
      holiday-calendar hit was in `.archive/`.

- [ ] **12. Fix comment [20]'s factual error.** Manifold does not host an LLM;
      the 8 GB is sandbox budget for code execution and conversation. The
      GPU-instance cost comparison does not apply to their architecture.

- [ ] **13. Verify or cut Ng (2017)'s "four terabytes"** (comment [21]).
      Cheapest resolution is to cut it.

### Phase 4 — retrain-in-sandbox arms (blocked by the E2B template)

- [ ] **14. Add scenario F (pre-trained served) vs G (ad-hoc refit in sandbox), n=3.**
      Answers "pre-trained, or guideline-instructed ad-hoc retraining in the
      cloud environment?" -- and is the only design in which the 8 GB budget is
      genuinely exercised.
      BLOCKED ON: the E2B template carrying statsmodels/xgboost, which
      D_prometheus already needs. Sequence AFTER blocks 1-3, which have no
      template dependency.

- [ ] **21. DECIDE: repoint training at cv_params.json, or document why not (F27).**
      `train_and_persist.py:208` reads `tuned_params.json` (30 trials, single
      split, 2026-08-19). `cv_params.json` (100 trials, 4-fold expanding CV,
      2026-08-24) is consumed by NOTHING. The served models use the weaker
      tuning the project itself called under-powered. **Settle this BEFORE
      spending API budget on blocks 1-3** -- afterwards, switching invalidates
      the runs.

- [ ] **15. Log RSS inside the sandbox per run**, so the arms produce a real
      occupancy number against the 8 GB budget rather than an assertion.

### Phase 5 — validate the claims the arms rest on (free; no API cost)

- [x] **16. Test refit-not-retune rather than asserting it (F9).** Walk forward:
      refit on stored params through month t, compare against a full Optuna
      re-tune at t, across several months. If accuracy tracks, the cheap
      architecture is validated; if it drifts, on-demand retraining needs
      re-tuning and the cost story changes. Either result is a Ch6 finding.
      Brian's doubt is well founded -- cv_params.json shows num_leaves moving
      120 -> 21 between two metrics on the same data.

- [x] **17. Measure the cost of a full Optuna re-tune** (time + RSS, same
      instrument). Optuna is fully automatic (F14), so this needs no human. It
      may rule per-query re-tuning out with a number, which is what makes
      refit-not-retune defensible instead of merely convenient.

- [x] **18. Time the full preprocessing chain, not just the fit (F13).** The 3 s
      fit is the cheap tail of load -> aggregate -> calendar-fill -> engineer ->
      split. On-demand refit pays the whole chain. This is the real feasibility
      question, more than RAM.

- [x] **19. Cost the two on-demand designs against each other**: preprocessing
      shipped as a pinned callable artefact vs. code-in-context for the agent to
      re-derive. The second risks a silently different feature matrix -- a
      correctness risk, not just a cost one.

- [x] **20. Confirm the E2B template exists before planning on it (F15).**
      `prometheus.yaml` was NOT found in the engine tree this session. Locate it,
      or list templates registered to the E2B account. Free. Do this before any
      arm that needs the scientific stack in-sandbox.

## Related

- P0042 — frozen sampling design; blocks 1-3 are independent of this plan
- P0043 — snapshot/comment workflow; phase 2 here settles its surface-authority question
- `04_thesis_results/srq1/profiling.md` — the table this plan invalidates and replaces
