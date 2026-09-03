<!-- PROSE STRIPPED 2026-09-01 (P0044).
     Authoritative prose lives in the OneDrive .docx; the read-only mirror is
     docx-exported-snapshots/2026-09-01_18-50/chapters.
     This file is a PLANNING surface: bullets, structure, status and provenance.
     Do not paste prose back in -- two live copies is the drift this removes.
     Full pre-strip prose: .archive/2026-09-01_superseded-prose/sections-drafts-prose/ -->

# Chapter 3 — Methodology
> Status: PROSE DRAFT — written 2026-04-12; realigned 2026-06-16 to the rescoped framing (5 categories; RSS profiling); realigned 2026-06-17 to RQs v4 (SRQ4 baseline = code-as-action LLM; Main RQ cost-justified; metrics correctness/consistency/replicability + cost/latency)
> Author: Claude Code — requires human review before finalisation
> Word count target: ~12 standard CBS pages (~27,300 chars excl. spaces)
> Compliance note: ⚠️ DSR acceptance by CBS supervisor not yet confirmed (open item OI-03). Saunders "research onion" framework parked for application at writing time (see thesis-context/methodology/).

---

## 3.1 Philosophy of Science

---

## 3.2 Research Design: Design Science Research

---

## 3.3 Research Strategy

---

## 3.4 Data Sources

---

## 3.5 Analytical Approach

---

## 3.6 Validity and Reliability

---

## 3.7 Limitations

---

## References cited in this chapter

- Ahrens, A., Hansen, C. B., Schaffer, M. E., & Wiemann, T. (2024). Model averaging and double machine learning. *Journal of Applied Econometrics*. https://doi.org/10.48550/arXiv.2401.01645
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, *28*(1), 75–105.
- Klee, S., & Xia, Y. (2025). Measuring time series forecast stability for demand planning. *KDD '25 Workshop on AI for Supply Chain*.
- Kuleshov, V., Fenner, N., & Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. In *Proceedings of ICML 2018* (PMLR, Vol. 80).
- Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). M5 accuracy competition: Results, findings, and conclusions. *International Journal of Forecasting*, *38*(4), 1346–1364.
- Mehta, S. (2025). Beyond accuracy: A multi-dimensional framework for evaluating enterprise agentic AI systems. *arXiv preprint arXiv:2511.14136*. [PREPRINT, not peer-reviewed]
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems*, *24*(3), 45–77.


---

## OPEN AUDIT NOTES (P0044, 2026-09-03)

> Source: cross-check of Ch2/Ch3 promises against `srq4_experiment.py`,
> `srq1_profiling.py` and `04_thesis_results/`, plus the NotebookLM claim audits
> under `05_thesis_writing/notebookLM/`. Bullets only -- prose goes in the .docx.

### N1. Sec 3.4/3.5 -- four categories, not five

- `metrics.csv` carries **CSD, danskvand, energidrikke, RTD**. `totalbeer` was dropped.
- Sec 3.4 still describes five categories incl. beer; Sec 3.5 and 3.6 say "five Nielsen categories".
- **Action:** narrow every "five categories" to four. Scope description, no new work.
- The model count (five: ARIMA, Prophet, LightGBM, XGBoost, Ridge) is CORRECT and must
  not be changed while fixing the category count -- easy to conflate the two fives.

### N2. Prophet IS implemented -- an earlier claim that it was missing was wrong

- `srq1_baselines_stat.py:236 run_prophet()`; results in `stat_baselines.csv`, all four categories.
- WMAPE: CSD 105.7%, danskvand 19.5%, energidrikke 972.4%, RTD 66.8%.
- Prophet's failure is a **result**, not a gap. NLM audit Section J governs the wording:
  - **PRO-04 Contradicted:** Taylor & Letham do NOT exclude monthly data. Do not claim they do.
  - **PRO-05 Not Found:** they do not "prove" flat monthly forecasts. Do not attribute.
  - **PRO-06 Supported w/ qualification:** safe framing is that monthly frequency strips
    Prophet of weekly seasonality + holiday windows, leaving trend + yearly seasonality
    on a short history.
- **Action:** report Prophet in Ch6 with the PRO-06 wording. Cite Taylor & Letham (2018),
  *The American Statistician*, 72(1), 37-45 -- **currently missing from the Ch2 reference list**.

### N3. RAM: 8 GB -> 4 GB (measured)

- 17 occurrences across abstract, Ch1, Ch2 Sec 2.2, Ch3 (x3), Ch5 (x6), Ch10.
- 4096 MB is the **measured** allocation of Manifold's production E2B template
  (`templateID=fxe7gzkqjupdhbx4uvpr`, alias `prometheus`). 8 GB was unsourced --
  Ng (2017) sits beside it but states no SME budget.
- All results hold *a fortiori*: worst single model 38.1 MB = **0.93%** of 4096 MB.
- **Sec 3.7 is load-bearing:** "the eight-gigabyte RAM budget *requires* models to be
  executed sequentially." At 4 GB that argument is *stronger*, but it currently rests on
  a retired number. Rewrite the reasoning, do not just find-replace the figure.
- Appendix Table A.3 carries the measured figures.

### N4. Sec 3.5 SRQ2 understates the traceability that is actually implemented

- Ch3 promises "recording the mapping from tool call and forecast value to the resulting
  recommendation." The code records **more**:
  - `args_match_request` -- whether the LLM's tool arguments named the series it was asked
    about. A mismatch silently corrupts the accuracy figure and is invisible in answer text.
  - full raw response per run (generated code, reasoning summaries, web queries).
- Ch2 Sec 2.5 frames traceability (Dong et al., 2024; Kartik et al., 2025) as a *design
  objective*. It is an **implemented** capability -- currently an unclaimed contribution.
- **Action:** promote in Sec 3.5 and in the Sec 2.7 contribution list. Appendix Table A.10.

### N5. LLM-as-judge -- decided AGAINST (budget). The claims must follow.

- Ch2 Sec 2.5 builds the Gu et al. (2025) / Ye et al. (2024) bias-aware judge argument at length.
- Ch3 Sec 3.5 **and** Sec 3.6 both commit to "an LLM-as-judge protocol with a separate judge
  model ... and a human-rated subset for validation."
- Nothing live implements it; only a raised `NotImplementedError` in
  `.archive/superseded_scripts_2026-08/srq4_tier2.py`.
- **Decision (Brian, 2026-09-03): no judge.** See N5b for why this is defensible.
- **Action:** remove the judge commitment from Sec 3.5 and Sec 3.6; keep the Gu/Ye material in
  Ch2 as *reviewed context* explaining why the thesis scores deterministically instead.
  Record in Sec 3.7 as a scoping limitation.

### N5b. Why no judge is the right call, not merely the cheap one

- Correctness here is **numeric**: |forecast - actual|/actual against a held-out month.
  A judge scoring that would be strictly worse than arithmetic.
- Consistency and replicability are **measured over repeats** (CV, TAR@N) -- again arithmetic.
- The failure taxonomy is **rule-based** and reproducible.
- A judge could only add *qualitative* dimensions -- is the recommendation well-reasoned,
  does the prose faithfully represent the interval. That is real, but:
  - it needs a validated rubric + human-rated subset to be defensible (Gu et al., 2025);
  - Ye et al. (2024) show position and self-enhancement bias need explicit controls;
  - and it would evaluate **prose quality**, which is not what any SRQ asks.
- Honest framing: the thesis scores what can be scored deterministically, and declines a
  judge whose own reliability would first have to be established.
- **A strength when stated deliberately; a hole when discovered by an examiner.**

### N6. Sandbox RSS unmeasured -- the budget claim is about the laptop, not the artefact

- Ch5's <=4 GB claim rests on `profiling.csv`, measured **locally**.
- Scenario B runs in an E2B sandbox; the constraint is asserted there, never measured.
- **Action:** log peak RSS inside the sandbox per run. Free, and it is the one measurement
  that makes the constraint claim about the *deployed* artefact rather than the dev machine.
- Feeds Appendix A.3 as a second column ("in-sandbox peak").

### N7. Saunders alignment -- three Contradicted verdicts still live in Ch3

From `notebookLM/02-Methodology_Review/NLM Review/Methodology_Review-Section_A-saunders_alignment_report.md`.
Re-verified 2026-09-03 against the current .docx snapshot -- all three still present:

| ID | Where | Verdict | Action |
|----|-------|---------|--------|
| MR-01 | Sec 3.2 "research design type ... is explanatory" | **Contradicted** | Purpose is explanatory **and evaluative** under Saunders. Reframe. |
| MR-02 | Sec 3.3 "single-case embedded study" (4 occurrences) | **Contradicted** | One unit of analysis = **holistic**, not embedded. Relabel, or define the four categories as embedded sub-units. Also label the combination a **multi-method quantitative design**. |
| MR-09 | Sec 3.1 "The epistemological stance is empirical" | **Contradicted** | "Empirical" is a property of data/method, not an epistemology in Saunders' taxonomy. Reframe as pragmatist. |

- **MR-02 is the cheap fix with the better outcome:** the thesis already evaluates four
  categories separately, so declaring them embedded sub-units makes the existing design
  *correct as written* rather than forcing a relabel to holistic.
- Also unaddressed (Not Addressed verdicts on mandatory Research Onion layers):
  - **MR-07** time horizon -- add: cross-sectional evaluation over longitudinal secondary data.
  - **MR-08** approach to theory development -- add: abductive, with deductive testing in SRQ1.
  - **MR-10** ethics -- Saunders Ch6 expects more than a confidentiality mention.
  - **MR-19** "locked, pre-registered" split is attributed to Saunders, who does not discuss
    pre-registration. Reattribute to ML methodology (Cawley & Talbot, 2010).
- **MR-03 Qualified:** Sec 3.1's "modest realism" paragraph reads verbatim as *critical*
  realism, contradicting the pragmatist lead. Reframe ontology in pragmatist terms.

### N8. Appendix -- every tracked metric now exports as a thesis-ready table

- New: `03_thesis_modelling/scenario_setup/export_appendix.py` -> `04_thesis_results/appendix/`.
- Free to run, no API calls, safe to re-run; reads only what is already on disk.
- Each table emitted as **.md** (paste/screenshot) and **.csv** (trace a number to source).
- Generated from the same `runs.csv` as `summary.md`, so the two cannot disagree.
- **Table A.1 is the metric dictionary** -- unit, definition, direction of improvement and
  source field for every quantity. Every later table is unreadable without it.

| Table | Content |
|-------|---------|
| A.1 | Metric dictionary (14 metrics) |
| A.2 | Per-model resource profile -- RSS vs tracemalloc |
| A.3 | RAM budget against measured 4096 MB |
| A.4 | Statistical baselines incl. Prophet, all 4 categories |
| A.5 | Seed stability (Klee & Xia, 2025) |
| A.6 | Refit vs re-tune economics |
| A.7 | SRQ4 scenario comparison, all 5 dimensions |
| A.8 | Outcome taxonomy |
| A.9 | Per-run record |
| A.10 | SRQ2 traceability (pending scenario-C runs) |
| A.11 | Run configuration |


---

## APPENDIX + MEASUREMENT NOTES (P0044, 2026-09-03, session 2)

> Follows the OPEN AUDIT NOTES above. Bullets only.

### N13. Appendix tables are deliberately UNNUMBERED

- `export_appendix.py` emits a title + caption per table but **no "A.4" style number**.
- Reason: numbering is Word's job. Hard-coded numbers go stale the moment a table is
  dropped from the appendix; Word's caption/cross-reference fields renumber themselves.
- **When inserting:** use Word References > Insert Caption, then cross-reference by field.
  Never type a table number into the .docx by hand.
- The filename slug carries the ordering.

### N14. Submission-ready vs meta comments -- hard separation

- Everything in a table `.md` is publishable **as-is**: title, caption, table, `*Note.*`
- Everything for us is in **`04_thesis_results/appendix/_review_notes.md`**, a separate
  file that no table screenshot can capture.
- Verified 2026-09-03: zero review language leaked into any table `.md`.
- **`_review_notes.md` must never be pasted into the .docx.** It carries instrument
  corrections, claims-not-to-make, and pending-work flags.

### N15. Percentage convention

- Percentages are stored as **numbers** with the unit in the **column heading**
  ("Weighted MAPE (%)" with a bare `19.4`), not `19.4%` repeated per cell.
- This is the M4/M5 competition convention. It is not malpractice -- repeating the unit
  in every cell adds width without information and breaks numeric column alignment.
- Documented in the metric-dictionary note so a reader cannot misread `19.4` as a ratio.

### N16. "TAR@N" renamed

- Was undefined jargon in the tables. Now **"top-answer agreement rate"**, defined inline
  in the scenario caption AND in the metric dictionary.
- Definition: share of repeated runs returning the most common answer within 1% tolerance;
  1.00 = complete agreement, 0.20 = five repeats gave five different answers.
- Cite Atil et al. (2025). Keep the plain-English name in the thesis body.

### N17. Metric dictionary now defines central tendency

- Added **Median**, **Mean** and **Coefficient of variation** as first-class entries.
- Median is the headline for error; the note explains *why* (insensitive to outliers,
  where a mean is shifted without limit by one divergent series).
- Mean is reported beside it so the gap is visible: mean >> median signals right-skew
  driven by a few large failures. That gap is itself a finding worth commenting on.

### N18. Training/retraining metrics now separated into three tables

- The single "fit time" figure conflated three different operations. Now:

| Table | Operation | Answers |
|-------|-----------|---------|
| Resource profile | one fit, given hyperparameters | what does the model cost to build |
| Cost of retraining on request | refit vs re-tune, time + memory + budget share | can we retrain per query |
| Effect of holding hyperparameters fixed | frozen vs re-tuned across 5 origins | does freezing them cost accuracy |

- **Refit 2.93 s / 35.0 MB vs re-tune (100 trials x 4 folds) 417.3 s / 65.3 MB = 142x.**
- Memory is NOT the constraint -- re-tuning peaks at 2.11% of budget. The case against
  per-query re-tuning is **elapsed time alone**. Say so explicitly.
- Parameter-drift table carries an honest "absence of evidence at this horizon" note.

### N19. In-sandbox memory MEASURED -- N6 closed

Ran `measure_sandbox_rss.py` against template `prometheus`, 2026-09-03:

| | value |
|---|---|
| Container limit **read from cgroup** | **4,122 MB** |
| Processor cores | **1** |
| Baseline RSS (interpreter + libs) | 156.4 MB (3.79%) |
| Peak fit -- Ridge / LightGBM / XGBoost | 1.4 / 28.2 / 6.5 MB |
| Largest share of limit | **0.68%** (LightGBM) |

- **The container corroborates the 4 GB figure independently.** This is now measured in
  two ways: the template's provisioned allocation, and the container's own reported limit.
- **cpus=1** explains why in-sandbox RSS is *lower* than local (38.1 MB local LightGBM vs
  28.2 MB in-sandbox): fewer cores, fewer parallel histogram buffers. Not a contradiction --
  state the reason, or a reader will read it as an inconsistency.
- **Baseline (156.4 MB) exceeds every model fit.** That is the real shape of the finding:
  the constraint binds the *model class* chosen, not the chosen models' footprint.
- Cite **alongside** local profiling, not instead of it. Together they show the footprint
  is not an artefact of the dev machine.

### N20. A note on which sandbox is which -- do not conflate

- **Scenario B** runs in **OpenAI's hosted Code Interpreter** container, not E2B. It is a
  black box that cannot self-report RSS.
- **E2B / `prometheus`** is the **Prometheus production** environment, and is what the 4 GB
  budget describes.
- Ch3 sec 3.5 currently says the baseline "executes LLM-generated code in a sandboxed
  environment (for example E2B)". **That is misleading** -- E2B is the deployment target,
  the baseline uses OpenAI's container. Fix the parenthetical.

### N21. Per-run table is a PILOT, not the final size

- Currently 6 rows: scenario A only, CSD only, 2 brands x 3 repeats.
- **Intended full size: 225 rows** = 15 brands x 5 repeats x 3 scenarios.
- Blocked on API credit (P0042 blocks 1-3, ~$40). The table auto-states its coverage
  ("Reflects N of an intended 225 runs") so a draft screenshot cannot mislead.
- Do not present current scenario figures as results.


---

## APPENDIX CONVENTIONS + PRE-SPEND CHECKLIST (P0044, 2026-09-03, session 3)

### N25. Table numbering: filename yes, content no

- Files are `01_metric_dictionary.md` .. `12_run_configuration.md` -- numbered prefix so
  the directory sorts in generation order for our review.
- **No table number appears inside any `.md`.** Word's caption/cross-reference fields are
  authoritative, so dropping a table renumbers the rest automatically.
- **When inserting:** References > Insert Caption, then cross-reference by field. Never
  type a table number by hand.

### N26. Review notes are INLINE, below a horizontal rule

- Reverted the separate sidecar. Each table `.md` now ends with:
  `---` then `<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->` then the notes.
- Rationale (Brian): the notes belong beside the table they describe. A screenshot
  cropped to the table + its `*Note.*` cannot capture what sits below the rule.
- **Everything above the rule is submission-ready. Nothing below it goes in the .docx.**

### N27. Percentage convention -- now consistent everywhere

- **Bare number in the cell, unit in the column header.** `19.4` under "WMAPE (%)".
- The sandbox table had drifted to decimals; fixed. Verified across all 12 tables.
- Stated in the metric-dictionary note, so `19.4` cannot be misread as a ratio.
- This is the M4/M5 competition convention -- not malpractice. Repeating `%` per cell
  adds width without information and breaks numeric alignment.

### N28. Winners bolded in every cross-model comparison

- Applies to: resource profile, sandbox profile, statistical baselines, seed stability,
  parameter drift, retraining cost.
- Bolding is **per row** (same measure across models), never per column -- a column
  contains unlike quantities and bolding down it would assert a comparison that does
  not exist.
- **Two deliberate exclusions:**
  - `Ridge(unclipped)` never wins a baselines row -- it is a diagnostic variant, not a
    candidate model.
  - The **Python-heap row is never bolded**. Bolding it would award "best" to XGBoost,
    whose native allocation that instrument fails to observe -- inverting the point the
    row exists to make.

### N29. Three resource tables merged into one

- Was: per-model profile + budget share + retraining cost. Now one table.
- Justification: same unit system (seconds, MB, one budget) and same subject. A reader
  comparing fit / refit / re-tune had to hold three tables in view.
- **Parameter drift stays separate.** Its unit is percentage points of forecast error
  across origins, not time or memory; merging would invite comparison down a column
  where none exists.
- Net: 13 tables -> 12, with the key comparison now in one screenshot.

### N30. Every figure is COMPUTED, never inferred

- Confirmed across all tables: each number is read from a CSV or computed by an
  arithmetic expression in `export_appendix.py`. No LLM is asked to judge or estimate
  anything at table-generation time.
- Interval-communication percentages = regex extraction + numeric comparison against the
  tool payload (5% tolerance), then count / n.
- Re-running on identical inputs returns identical numbers. This is a **reproducibility
  claim we can make in Ch3 sec 3.6**, and should be stated there.

### N31. Sample size now visible wherever a percentage appears

- Interval-communication columns carry `n=` in the header, and cells read `3 of 3 (100)`.
- Baselines carry `(n=95)` per category; stability carries seed count in the caption.
- Scenario/per-run tables auto-state coverage against the intended 225 runs.

### N32. Ch3 sec 3.5 -- E2B is the wrong reference for the baseline

- Current text: the baseline "executes LLM-generated code in a sandboxed environment
  (for example E2B)".
- **Wrong.** Scenario B runs in **OpenAI's hosted Code Interpreter**. E2B is the
  **Prometheus production** environment and is what the 4 GB budget describes.
- **Action:** fix the parenthetical, and do not let the two sandboxes blur in Ch5 either.

---

## PRE-SPEND CHECKLIST -- what is open before P0042 blocks 1-3

Ordered by whether it forces a re-run if decided afterwards.

### Blocking (decide BEFORE spending -- deciding later invalidates the runs)

| # | Item | Why it blocks |
|---|------|---------------|
| B1 | **Does the prompt ask for a recommendation?** | See N33. Changing the question after the runs makes them unpoolable. |
| B2 | **Brand selection: `volume` or `stratified`** | `--brand-strategy` changes which 15 brands are run. Cannot be changed retrospectively. |
| B3 | **Repeat count (currently 5)** | Consistency and top-answer agreement are computed over repeats; fewer repeats weakens both, more costs linearly. |
| B4 | **Judge: confirmed NO** | Already decided (N5). Just ensure Ch3 sec 3.5/3.6 text is fixed BEFORE the runs, so the write-up matches what was run. |

### Non-blocking (safe to do after; scored retrospectively)

- Interval-communication scoring -- runs off logged answers, no re-run needed.
- Traceability table -- populates automatically from scenario-C raw responses.
- All Ch1/Ch2/Ch3/Ch5 text fixes (4 GB, four categories, Saunders, E2B parenthetical).
- Appendix regeneration -- free, idempotent.

### Verify immediately before spending (free)

```
python 03_thesis_modelling/scenario_setup/verify_setup.py
python 03_thesis_modelling/scenario_setup/srq4_experiment.py --dry-run --full
```

- The dry run prints the plan and its estimated cost and sends nothing. **Run it.**
- Confirm `train_and_persist.py` has been re-run since the selection fix, so scenario C
  serves the unbiased models (RTD = LightGBM, not XGBoost).

### N33. The recommendation criterion -- a prompt finding, not a scorer bug

- The first pilot scored "gives a recommendation" at **33%**. I checked `prompts.py`:
  the shared question asks for *"the number, a range, and how confident you are"* and
  **never asks for a recommendation**.
- So that criterion measured compliance with an instruction never given. The 33% figure
  is a finding about **our prompt**, not about the scenario. **It has been removed from
  the scorer and must not be cited.**
- **The open decision (B1):** Ch2 sec 2.3's Goodwin argument is that the interpretive step from
  interval to decision is where the value lies. If we want to evidence *that* step, the
  prompt must ask for a recommendation.
- **Trade-off:** the identical-question design is the core of the single-variable claim
  (see the `prompts.py` docstring -- an earlier version had per-scenario wording and that
  confounded prompt with mechanism). Adding "and what should the planner do?" to the
  shared question preserves the single-variable property, because all three scenarios
  get the identical addition.
- **My recommendation:** add it. It costs nothing extra per run, it is asked identically
  of all three scenarios, and it converts Goodwin from motivation into a measured
  dimension. But it MUST be decided before the runs.
- If we decline, scope Goodwin to motivation in Ch2 and say plainly that the decision
  step was not evaluated.


---

## PROMPT REDESIGN + RUN MECHANICS (P0044, 2026-09-03, session 4)

### N36. The shared question now asks for a recommendation -- DECIDED

- **Decision (Brian, 2026-09-03): Goodwin option 1.** Rationale given: spend the extra
  budget to make the experiment methodologically sound and reduce the assessor attack
  surface.
- New shared question (identical in all three scenarios):

  > How many units of {brand} will be sold in the {category} category in Danish retail
  > in {target}? Answer in units sold, not currency. Give the number, a range, how
  > confident you are, **and what you would recommend the category planner do about it**.

- The addition is applied **identically to A, B and C**, so the single-variable design
  survives -- no factor varies between scenarios.
- **This converts Goodwin from a motivating citation into a measured dimension.** Ch2
  sec 2.3 argues the interpretive step from interval to decision is where the value lies;
  the experiment now asks for that step and scores whether it was supplied.
- The `gives_recommendation` criterion is restored to the scorer.

### N37. One-shot output exemplar added -- and it needs a methodology paragraph

- All three prompts now carry **one** worked output example fixing the answer shape
  (Forecast / Range / Confidence / Recommendation / sentinel).
- **Why this is necessary, not cosmetic:** outputs are scored by *programmatic
  extraction*. `_parse_sentinel` reads the forecast; the interval scorer reads the bounds
  and confidence back out of the prose to check them against the tool payload. Extraction
  can only test what the model was asked to produce. Without a shown format, an answer
  saying "roughly 3.4 to 3.9 million" scores the same as one omitting the interval --
  measuring our parser's luck rather than the system.
- **Why exactly one example:**
  - Brown et al. (2020) show most of the in-context-learning gain arrives with the first
    example, with sharply diminishing returns after. **This citation must be added to Ch2
    or Ch3; it is not currently in the reference list.**
  - Every extra example is tokens paid on every run in all three scenarios.
  - One is the smallest intervention that fixes the format, which matters because the
    exemplar is prompt content and therefore a potential confound.
- **Confound control:** the exemplar uses a different brand and category from any scored
  cell, with rounded obviously-illustrative figures. It shows the *shape* of an answer,
  never a plausible answer to the question asked. And being identical across scenarios,
  it cannot advantage one over another.
- **Ch3 sec 3.5 must state this**: the prompting approach is one-shot, why, and how the
  exemplar is controlled.

### N38. runs.csv now APPENDS -- this was a money bug

- **Found while checking the incremental-trials requirement.** `--rep-offset` renumbered
  repeats, but the writer did `df.to_csv(runs.csv)` over the whole file. A second block
  would have **silently destroyed the first block's paid rows**.
- Fixed: `_merge_runs()` merges with what is on disk.
  - Run identity = (category, brand, system, rep).
  - A re-run of the same cell **replaces** that row (fixing a failed cell corrects it
    rather than duplicating it).
  - Every other row on disk survives untouched.
  - The summary now describes the **whole file**, not the latest slice.
- **Verified by test**, 2026-09-03: 2 rows -> +3 different-scenario -> 5 -> +2 via
  rep-offset -> 7 -> re-run of an existing cell -> still 7 with the value replaced.
- **This is what makes scaling up safe**: run the frozen blocks, read the real per-run
  cost, then add repeats with `--rep-offset` without losing anything.
- **Precondition:** only pool runs whose PROMPT is unchanged. The prompt just changed
  (N36/N37), so the 6 existing scenario-A rows cannot be pooled with anything run from
  now on.

### N39. Corrections to my own pre-spend checklist -- B2 and B3 were already settled

I listed brand strategy and repeat count as open. **They were not.** Both are frozen in
`plans/P0042_.../2026-09-01_DOC-srq4-sampling-design.md`:

- **DEC-STRATIFIED**: `--brand-strategy stratified`, not volume. Picks highest / median /
  lowest volume among brands with a fully non-zero test window (CSD ranks 1, 41, 76 of 76).
- **Repeats vary per scenario, allocated inversely to per-run cost** -- exactly the
  approach Brian described:

| Scenario | n | Why |
|---|---|---|
| A_plain | 3 | A->B gap measured +17.8pp, too large to doubt at any plausible n. Deliberately under-sampled -- A costs ~63x C |
| B_data | 10 | The contested increment. B->C measured +3.5pp; sized for 80% power |
| C_model | 10 | as above |
| C_model breadth | 5 x 9 brands | Generalisation across all 4 categories at ~$0.03/run |

- Three blocks, 111 runs, ~$40 realistic. **Do not re-open these; they are frozen and the
  reporting wording is fixed.**

### N40. The appendix picks up new scenarios automatically -- verified

- Tables derive scenario columns from `runs.csv` itself, so B and C appear the moment
  they are run. No code change needed after the paid blocks.
- **Verified 2026-09-03** by simulating a 27-run three-scenario file: all three columns
  rendered, the coverage sentence self-adjusted, and the real 6-row file was restored
  intact afterwards.
- The coverage sentence drops away entirely once the run count reaches the intended 225.

### N41. Winner emphasis is bold *italic*, not underline

- Markdown has **no underline primitive**. `<u>` is raw HTML and does not survive the
  paste into Word.
- So winners are `***value***` (bold + italic), the two emphases Markdown does define.
- If true underline is wanted, it must be applied **in Word after pasting** -- do not
  expect the exporter to produce it.


---

## RESULT CACHE + PROMPT SCHEMA VERSIONING (P0044, 2026-09-03, session 5)

### N45. Prompt schema is now versioned AND content-hashed

- "The prompt is unchanged" must be machine-checkable, not a recollection.
- `prompts.py` now exposes `SCHEMA_VERSION` (readable name) and `schema_id()`
  (SHA-256 over **every string that reaches the model**: question, all three capability
  notes, exemplar, sentinel instruction, tool schema).
- Current: **`v3-recommendation-oneshot+ff9b62a101f0`**
- **Editing any prompt string changes the id automatically.** There is no way to alter a
  prompt and forget to bump a version, which is the failure mode a manual version number
  would have.
- Per-run substitutions (brand, category, month, CSV) are excluded — they vary by design
  and are logged per run.

**Version history, now recorded in the code:**

| Version | Date | Change |
|---------|------|--------|
| v1-dkk-confound | 2026-08-19 | "what will X sell", no unit named. All Scenario A answers in DKK, ~4500% error. **Never pool.** |
| v2-units-no-recommendation | 2026-08-19 | units named explicitly. The 6-run A pilot. |
| v3-recommendation-oneshot | 2026-09-03 | + recommendation request (Goodwin) + one-shot exemplar. |

- **All historical runs.csv files were backfilled** with the schema that actually produced
  them (v1 for the dkk-confound run, v2 for the pilots) — not left blank and not
  optimistically treated as current.

### N46. Result cache — three modes, spend-avoiding by default

A completed run is a **cache entry** keyed by
`(schema, category, brand, scenario, repeat)`.

| Mode | Flag | Behaviour |
|------|------|-----------|
| **resume** | *(default)* | Execute only cells absent from the cache. Re-running an identical command **sends nothing and costs nothing**. |
| **append** | `--append` | Add repeats *alongside* cached ones, numbered past the highest stored. Use to deliberately grow n. |
| **refresh** | `--refresh` | Re-run cached cells and replace them. **Spends again** on paid work; only when a run is suspect. |

**The scenario Brian described, now the default behaviour:**
- Run #1 @ 10 trials → all cached
- Run #2 @ same 10 → **0 sent**, cache unchanged
- Run #3 @ 20 → **only the 10 new ones sent**

**Two safety properties, both tested:**
- **Schema-scoped:** only rows at the *current* schema count as hits. Change the prompt
  and old rows stop matching automatically — different questions are never pooled.
- **Failures are not hits:** a run classed anything other than `ok` is retried, not
  counted as done.

**Verified 2026-09-03**, all seven cases: empty cache → 6 to run; identical re-request →
0 to run / 6 skipped; 3→10 reps → 14 to run / 6 skipped; `--refresh` → 6 to run;
`--append` → 6 to run at base rep 3; different schema → 6 to run (no reuse); failed run →
retried.

### N47. `--dry-run` now costs what will ACTUALLY be sent

- Previously it costed the full requested grid, so the cache saving was invisible and a
  dry run would have over-stated the spend.
- It now costs the planned todo list and reports how many cached runs were skipped.
- **Always dry-run before a block.** It is free and it now tells the truth.

### N48. The appendix reports one schema only

- Scenario tables filter to the **current** prompt schema. Superseded rows stay on disk
  for the record but are never aggregated into a reported figure.
- If no rows exist at the current schema, the exporter prints a **warning** naming what it
  is reporting instead, rather than silently presenting stale runs as results.
- Currently warns: the 6 v2 rows predate the v3 question. They will be superseded by
  block 1, which re-runs the same two brands.

### N49. This belongs in Ch3 sec 3.6 (reliability)

Three claims that are now literally true of the code and worth stating:

- **Prompt provenance.** Every result row carries a content-derived id of the exact
  prompt set that produced it, so a reported figure can be tied to the instrument.
- **No accidental pooling.** Runs asked different questions cannot be aggregated; the
  filter is by identity, not by date or by folder.
- **Idempotent extension.** Adding observations never re-runs, overwrites, or duplicates
  existing ones, so an experiment grown across sessions is the same object as one run in
  a single pass.
