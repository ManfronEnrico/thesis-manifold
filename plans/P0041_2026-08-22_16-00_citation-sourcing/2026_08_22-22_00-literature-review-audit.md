---
name: literature-review-audit
description: Audit of Chapter 2's literature claims against what the modelling has since found, plus the citation-validation areas beyond the modelling that need NotebookLM attention.
created: 2026_08_22-22_00
updated: 2026_08_24-10_00
---

# Literature review audit — what else needs source validation

> **SUPERSEDED 2026-08-24 for NotebookLM use.** This file's claim list was written from
> an audit rather than from a line-by-line read of the chapters. That read has now been
> done, and it found 10 bibliographic errors, 4 sources cited in Ch2 but absent here, a
> Ch1-vs-Ch2 contradiction about M5, and a fabricated citation. The corrected,
> upload-ready pack is:
>
> **`05_thesis_writing/notebookLM/01-Literature Review/Literature_Review-00-MASTER-verification-brief.md`**
>
> Use that for verification. This file is retained for its reasoning and for the
> decisions it records (D1 ensemble, D3 stability), which the brief does not duplicate.


Brian, 2026-08-22, having started the NotebookLM workflow with 22 sources:
*"Are there any other source validation areas we should look into apart from the
modelling? I believe that we must for sure think about our academic justification of
our thesis as well, a.k.a. the literature review."*

**Yes — and there is a category of problem here the modelling register does not
cover.**

## First, credit where due: Ch2 is in far better shape than the other chapters

Unlike Ch6 and Ch8, `ch2-literature-review.md` is genuinely written: 39 cited sources,
zero unresolved citation flags, arguments constructed rather than asserted, preprints
explicitly flagged (15 of 39), and a stated search method. It reports its own
limitations honestly. **It does not need a rewrite.**

What it needs is a different kind of check.

---

## The problem the modelling register does NOT cover

P0041's register asks: *"does a source exist for this claim?"*

Chapter 2 raises the opposite question: **"the source exists and is cited — but does
our own evidence now contradict what we said it implies?"**

A literature review states what the literature establishes, and then says what that
motivates in the thesis design. When the modelling later produces a result that cuts
against the motivation, the review does not become factually wrong, but it becomes
**disconnected from the thesis it introduces**. That disconnection is exactly what an
examiner reading Ch2 and Ch6 in sequence would notice.

**Four such disconnections exist as of 2026-08-22.** None require dropping a citation;
all require the prose to acknowledge what was found.

---

## D1 — "Combining models outperforms any single model" vs. no ensemble was built

**Ch2 §2.1 (lines 29, 33)** cites M4 (Makridakis et al., 2020) for *"combining models
tends to outperform any single best model"*, and Ahrens et al. (2024) for stacked
averaging and inverse-variance weighting, concluding this *"supports combining
multiple forecasts rather than relying on a single model."*

**The thesis currently serves a single model.** `forecast_demand` returns one
prediction from one per-category model.

**CORRECTION (Brian, 2026-08-22): this IS planned.** `F_ensemble` — serving pooled and
specialised predictions together — was designed and approved as a separate scenario
(P0040 F55, DEC-ENSEMBLE-SCENARIO). The earlier wording here implied the ensemble had
simply been dropped, which is wrong.

**Severity: MEDIUM, conditional.** The disconnection is real *today* but has a plan
attached. Two outcomes:

1. **`F_ensemble` runs** → resolved, and better than resolved: the review motivates it,
   the thesis builds it, and `C → F` measures whether it helped. That is the literature
   doing its job.
2. **The pilot kills it on cost** (the ~$2 pilot decides — see
   `plans/P0040_.../context_experiment_design.md`) → **then** Ch2 or Ch6 needs the
   sentence: combination was evaluated and deferred, with the reason.

**Do not write the deferral sentence before the pilot has run.** Writing it now would
pre-empt a decision that has not been made.

**Not a citation problem.** The sources are real and correctly described. The problem
is the unfulfilled "therefore".

---

## D2 — "Fifteen percent MAPE as the acceptable benchmark" vs. our measured results

**Ch2 §2.1** cites Ceran et al. (2024) using *"a MAPE of fifteen percent or below as a
practical benchmark for acceptable demand forecasting."* This became the thesis's
≤15% target.

Measured (`cv_metrics.csv`, WMAPE, CV-tuned):

| Category | best WMAPE | best **medMAPE** |
|----------|-----------:|-----------------:|
| CSD | 14.5% | 31.8% |
| energidrikke | 13.0% | 32.3% |
| danskvand | 20.5% | 35.8% |
| RTD | **31.8%** | 32.8% |

**Two distinct problems.**

**The metric may not match.** Ceran et al. say *MAPE*; the thesis reports *WMAPE*
(volume-weighted). These are different quantities, and this project has repeatedly
found they disagree by 15-20pp. **If Ceran's 15% refers to plain or median MAPE, the
thesis does not meet the benchmark on any category.** On WMAPE it meets it on two.

**→ NOTEBOOKLM PRIORITY: establish which metric Ceran et al. (2024) actually use.**
This single fact determines whether a headline target is met or missed.

**RTD misses on any reading**, at roughly twice the benchmark. That needs stating as a
limitation rather than being absorbed into an average.

---

## D3 — "Tree ensembles are more stable than statistical models" vs. stability was never measured

**Ch2 §2.1** cites Klee & Xia (2025) [PREPRINT] on forecast stability, defined as the
coefficient of variation under nominally identical inputs, concluding that the SRQ1
benchmark evaluates *"accuracy, computational efficiency, and stability."*

**Stability was not measured.** No results file reports a coefficient of variation
across repeated runs. SRQ1's own scope file lists "Forecast stability" as item 4, and
`cv_metrics.csv` has no such column.

**Severity: HIGH — this is a promised deliverable that does not exist.** Three options:

1. **Measure it.** Cheap: refit with N seeds, report CV of predictions. No API spend.
   Would also settle the F51 seed-stability question at the same time.
2. Drop the stability claim from Ch2 and from SRQ1's scope.
3. Reframe: run-to-run variance *is* measured for the SRQ4 scenarios (consistency), so
   the concept survives at the agent layer even if not at the model layer.

**Option 1 is recommended** — it is a few hours of compute and closes a stated gap.

---

## D4 — "No single model dominates across demand patterns" — and here the evidence AGREES

**Ch2 §2.1** cites Ma et al. (2025): *"no single model dominating across demand
patterns, a finding that motivates evaluating category-specialised models."*

**This one is corroborated**, and more strongly than Ch2 currently claims:

- The pooled-vs-per-category crossover at ~750-1000 training rows, replicated across
  both algorithms
- Seasonal-naive beating every tuned model on RTD
- LightGBM winning some categories, XGBoost others

**Recommendation: strengthen this in the write-up.** Ch2 presents it as motivation for
the design; Ch6 can return to it as a confirmed finding with a *sample-size threshold*
attached, which is more than Ma et al. offer. This is a place where the thesis extends
the literature rather than merely applying it.

---

## Beyond Ch2: the other source-validation areas

### A. Preprint concentration — 15 of 39 sources

Ch2 flags this honestly, which is right. But the flag alone does not tell a reader
**which arguments load-bear on non-peer-reviewed work.**

**Worth doing:** identify every claim whose *only* support is a preprint, and check
whether a peer-reviewed equivalent now exists. Klee & Xia (2025) is one such case, and
it carries D3's stability claim.

**A cheap NotebookLM task:** for each flagged preprint, has it since been published?
Preprints from 2024-2025 frequently have by now, and a published version is a free
upgrade in citation quality.

### B. The "closest paper" claim needs verification

The project overview names **Bürger & Pauli (2024, EAAI)** as the closest precedent —
an LLM-enabled agent for industrial batch processes, positioned as the architectural
blueprint this thesis transposes to retail FMCG.

**This is the single most load-bearing citation in the thesis.** The novelty claim
rests on "nobody has done this in retail FMCG, and the closest thing is this dairy CIP
paper."

**NotebookLM should verify:** (a) that the paper says what is attributed to it, and
(b) **that nothing closer has appeared since.** A newer paper doing something similar
in retail would materially weaken the gap claim, and it is far better to find it now.

### C. The five research gaps (G1-G5) are assertions of absence

Gaps are claims that *no* literature addresses X. These are the hardest claims to
support and the easiest to refute — one counterexample defeats each.

| Gap | Claim of absence | Refutation risk |
|-----|-----------------|-----------------|
| G1 | No framework for extending a production agentic system with forecasting under ≤8 GB | Medium |
| G2 | No head-to-head benchmark of these models under an explicit RAM budget in retail FMCG | **HIGH** — benchmark papers are common |
| G3 | No structured tool interface for exposing ML forecasts with uncertainty to LLM agents | **HIGH** — a fast-moving area |
| G4 | Integration-readiness criteria not empirically derived | Medium |
| G5 | No replicable RAM profiling methodology for ML + LLM pipelines | Medium |

**G2 and G3 are the exposed ones.** G3 especially: LLM tool-use is moving quickly, and
a 2025-2026 paper on exposing predictive models to agents with uncertainty would
directly challenge it.

**NotebookLM task: actively try to REFUTE G2 and G3.** Finding a counterexample now
means narrowing the gap claim; finding one at the defence means losing the novelty
argument. Instruct it to search *for* the thing we claim does not exist.

### D. Conformal prediction has no source at all — and it is now in the artefact

Already register entry C3, but worth restating with its Ch2 consequence: **Ch2 does not
review conformal prediction anywhere**, yet every served forecast carries a
split-conformal interval, and SRQ2's uncertainty claim depends on it.

**This is a literature gap, not just a citation gap.** §2.5 covers uncertainty and
reliability, but the specific method the thesis uses is not situated in any literature.
A section or subsection is needed, not just a reference.

### E. Metric choice is now a finding and needs a literature home

Three separate analyses found WMAPE and median MAPE disagreeing, by up to 20pp. The
thesis therefore has a genuine methodological finding about metric choice on
zero-inflated retail panels.

**Ch2 does not review forecast-accuracy metrics at all.** Hyndman & Koehler (2006) is
the obvious anchor (register A6). Without it the metric discussion in Ch6 has no
grounding, and it deserves grounding because it recurs throughout the results.

---

## Priority for the next NotebookLM batch

| # | Task | Why |
|---|------|-----|
| 1 | **Which metric do Ceran et al. (2024) use for the 15% benchmark?** | Determines whether a headline target is met or missed (D2) |
| 2 | **Try to refute G2 and G3** | The novelty claim's most exposed points |
| 3 | **Verify Bürger & Pauli (2024) and search for anything closer** | The single most load-bearing citation |
| 4 | **Conformal prediction literature** | Used in the artefact, absent from the review (C3/D) |
| 5 | **Forecast-accuracy metrics** — WMAPE, MAPE failure modes | A recurring finding with no literature home (E) |
| 6 | **Global vs local forecasting models** | Contextualises the best SRQ1 result (register C4) |
| 7 | **Have the 15 flagged preprints been published since?** | Free citation-quality upgrade (A) |

---

## What needs deciding, not researching

| Item | Decision |
|------|----------|
| **D1 — ensemble** | Build `F_ensemble`, or state in Ch2/Ch6 that combination was evaluated and deferred, with the reason |
| **D3 — stability** | Measure it (recommended, cheap), or drop the claim from Ch2 and SRQ1 |
| **D2 — RTD misses the target** | State as a limitation; do not average it away |

## Related

- `2026_08_22-18_00-citation-register.md` — the modelling-side register
- `05_thesis_writing/notes/2026_08_22-21_00-chapter-staleness-audit.md` — the numbers audit
- `01_thesis_research/literature/gap_analysis_v4.md` — the full gap analysis (not yet audited)
