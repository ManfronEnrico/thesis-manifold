---
pid: P0037
created: 2026-08-12 15:28:00
updated: 2026-08-19 01:50:00
status: in_progress
focus_detail: "Tasks 3, 4 and 7 DELIVERED 2026-08-19 -- build_service() runs end to end (230 forecasts, 4 categories), every response carries a trace block, and conformal calibration moved off test residuals (intervals were 4.4x too narrow). The SRQ4 experiment itself moved to P0039, which is now the focus. Remaining here is cleanup: tasks 2, 6, 8, 9."
---

# P0037 — Refining the Model Serving Approach

Align `03_thesis_modelling/model_serving/` with SRQ2's stated artefact (a typed tool
interface preserving **reliability, uncertainty, traceability**) and with the worked
example already written in `05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md` §6.

Full evidence: [findings.md](findings.md). Session log: [progress.md](progress.md).

## Framing — what this plan is and is not

The thesis's *design* is already right, and mostly already written. The ChatGPT
analysis independently arrives at the same architecture the rationale note §6 describes,
which is a useful external confirmation but not new information. **The gap is
implementation and contract, not concept** — with one genuine open design question
(the horizon, DEC-HORIZON below).

Scope discipline: this plan does **not** retrain models, does not touch SRQ1 results,
and does not change the feature set. It changes where serving code lives, what the tool
contract carries, and what the thesis claims about horizon.

---

## Decision required before tasks 4-6 — DEC-HORIZON

**The blocking question.** The trained model is one-step-ahead. The thesis's own worked
example asks for a 4-month horizon and Brian's question asks for 6. These cannot both
be satisfied by the current model without a strategy choice (findings F8).

| Option | What the tool does | Cost | Interval validity |
|---|---|---|---|
| **A — Restrict to h=1** | Keep `horizon` out of the schema; document the limit; rewrite §6's example to h=1 | None — code already does this | ✅ Valid as calibrated |
| **B — Recursive multi-step** | Feed each prediction back as the next `lag_1`, iterate to h | Moderate code; needs per-h conformal recalibration or a widening rule | ⚠️ h=1 interval is **invalid** at h>1 unless recalibrated |
| **C — Direct multi-horizon** | Train one model per horizon | Retraining; shorter effective panel per h; touches SRQ1 scope | ✅ Valid per h |
| **D — B, capped + declared** | Recursive to a stated max (e.g. h≤3), interval widened and labelled degraded-confidence | Moderate | ⚠️ Honest if the widening is empirically calibrated, not assumed |

**Recommendation: D, falling back to A if time is short.** D keeps the natural-language
demo ("what about six months out?") answerable while staying defensible, and it turns
the limitation into an SRQ2 result — *uncertainty that grows with horizon is exactly the
uncertainty-propagation property SRQ2 claims to preserve*. C is out of scope: it
reopens SRQ1.

Under A, the rationale note §6 example must change from 4 months to 1 — do not leave a
worked example in the thesis that the artefact cannot execute.

---

## Phases

### Phase 1 — Structural correction (unblocked, no design risk)

| # | Task | Why |
|---|---|---|
| 1 | Fix the broken `forecast_service.py` import in `srq4_experiment.py` | F2 — SRQ4 harness currently cannot be imported at all. Highest-severity defect |
| 2 | Move the serving-side code into `model_serving/` | F1 — the SRQ2 artefact is not in the serving folder. Per repo-tier-structure's train-vs-serve test |
| 3 | Build `forecasts.csv` and smoke-test `forecast_demand()` | F4 — the deployment-mode path has never been executed |

### Phase 2 — Contract (needs DEC-HORIZON)

| # | Task | Why |
|---|---|---|
| 4 | Add traceability + cutoff fields to the tool return | F7 — traceability is an SRQ2-named property with zero implementation |
| 5 | Resolve horizon: implement per DEC-HORIZON, or restrict and document | F6, F8 |
| 6 | Unify the duplicated FEATURES/category maps behind one `fit_scope` parameter | F3 — preserves the deployment-vs-evaluation distinction without copy-paste |

### Phase 3 — Correctness + write-up

| # | Task | Why |
|---|---|---|
| 7 | Fix `build_service` conformal calibration to use val, not test, residuals | F5 — test-split calibration undercuts the thesis's leakage-discipline claim |
| 8 | Write the serving-time feature taxonomy into the rationale note | F8 — with the promo correction: promo is derived-from-past here, **not** future-known |
| 9 | Reconcile rationale note §6 with the shipped contract | F6 — worked example must match what the tool accepts |

---

## Out of scope

- Retraining or model reselection (SRQ1 is settled — Ch6 §6.5.6)
- Feature-set changes, incl. `n_skus_active` (that is P0036 task 11)
- System B conversational serving — `generate_systemB_diagram.py` is a figure
  generator; no System B service exists and building one is not this plan's job
- Prometheus/Graph Engine integration (SRQ3 is an assessment, pending NDA)

## Related

- `01_thesis_research/research-questions/srq2-tool-interface.md` — the artefact spec
- `05_thesis_writing/notes/sample-size-and-tool-interface-rationale.md` §6, §9
- `.claude/rules/repo-tier-structure.md` — train-vs-serve placement test
- `plans/P0036_2026-08-11_16-08_csd-fixes-before-mirror/` — active sibling plan

---

## Status refresh 2026-08-19 — unblocked, and now the critical path

**DEC-HORIZON is resolved** (2026-08-18): H=3 is primary, and all 13 downstream call
sites were repointed to the `_h3` matrices. Tasks 4-6, blocked on that decision, can
start.

### Re-verified against the code today

| Task | Claim when written | State now |
|------|--------------------|-----------|
| 1 | `srq4_experiment.py` cannot import `forecast_service` at all | **`forecast_service` imports cleanly.** `srq4_experiment` still fails, but on `FileNotFoundError: 03_thesis_modelling/.env` — credentials, not code |
| 5 | Resolve horizon | **Decided**: H=3 (DEC-HORIZON), modelling layer repointed |
| 6 | Unify duplicated FEATURES/category maps | **Partly done**: `available_features()` added to all 9 scripts (F74); the category maps remain duplicated |

### The actual blocker

`srq4_experiment.py` reads `ROOT/.env` for **`ANTHROPIC_API_KEY`** and
**`E2B_API_KEY`**. The file is gitignored and absent from this machine. Nothing in
the harness can run until it exists.

This is the single highest-value unblock in the repo: SRQ4 *is* the thesis premise
— System A (a dedicated model exposed as a `forecast_demand` tool) versus System B
(code-as-action in an E2B sandbox), same model, same prompts, measuring whether model
availability improves the answer.

### Priority against the deadline

With under a month left and 120 pages outstanding, these tasks outrank every
remaining EDA refinement. Task 7 (conformal calibration using test rather than val
residuals) is the one that carries a correctness cost — it undercuts the leakage
discipline the rest of the pipeline now demonstrates, so it should not ship into a
results chapter uncorrected.

---

## 2026-08-19 — tasks 3, 4, 7 delivered; the experiment moved to P0039

| Task | Outcome |
|------|---------|
| 3 | **Done.** `build_service()` runs end to end: 230 forecasts across 4 categories |
| 4 | **Done.** Every `forecast_demand()` response carries a `trace` block (F12) |
| 7 | **Done.** Conformal calibration fits on train, calibrates on val (F10) |

Task 7 was worse than recorded: the model fitted on train+val+test and then measured
residuals on **test** rows it had already seen. Intervals were **4.4x too narrow**.

Found while running it (F13): serving built its prediction frame from the hardcoded
module-level `FEATURES` while the model was fitted via `available_features()`, so
XGBoost rejected the frame wherever a category lacked a capability. Fixed.

**The SRQ4 experiment moved to its own plan, P0039** — it is the thesis premise and
deserves a plan rather than a task row. This plan retains the serving-interface
cleanup:

| Task | Still open |
|------|-----------|
| 2 | move serving-side code into `model_serving/` |
| 6 | unify duplicated FEATURES/category maps behind one `fit_scope` (partly done — `available_features()` landed) |
| 8 | write the serving-time feature taxonomy into the rationale note |
| 9 | reconcile the rationale note §6 with the shipped contract |

None blocks P0039. Under the deadline, they are documentation-quality work that should
yield to the experiment and the write-up.
