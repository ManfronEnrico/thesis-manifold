---
name: prometheus-scenarios-design-rationale
description: RULE - Report-writing notes on why the SRQ4 ladder extends to five scenarios with the real Prometheus Graph Engine, and how to defend the reproducibility asymmetry.
category: reference
applies-to: [srq4, methodology, ch7, ch8]
triggers: [writing the SRQ4 methodology, defending scenario design, RAM budget figure]
created: 2026_08_20-00_00
updated: 2026_08_20-00_00
---

# Prometheus scenarios D and E — design rationale

Companion to `srq4-experiment-design-rationale.md`, which covers scenarios A-C.
Written for the methodology and results chapters.

## The ladder, extended

| Scenario | Engine | Forecast access | Reproducible |
|----------|--------|-----------------|--------------|
| `A_plain` | GPT-5.5 | none | yes |
| `B_data` | GPT-5.5 | Code Interpreter | yes |
| `C_model` | GPT-5.5 | `forecast_demand` | yes |
| `D_prometheus` | Prometheus Graph Engine | none (code-as-action) | no |
| `E_prometheus_model` | Prometheus Graph Engine | `forecast_demand` | no |

## Why five and not four

The original design tested the contribution in a GPT-based stand-in because
Prometheus access was pending (NDA + dev merge). With access granted, the obvious
move was a single Prometheus scenario — but that would move **two variables at
once** (engine *and* tool) relative to `C_model`, so any difference would be
uninterpretable.

Splitting into a plain and a tooled Prometheus scenario preserves the
one-variable-at-a-time discipline that makes the whole ladder readable:

- **A -> B** — what data access buys
- **B -> C** — what the trained model buys, in a generic LLM
- **D -> E** — what the trained model buys, **in the production agent**

`D -> E` is the thesis contribution measured where it is actually claimed to apply.

## The replication argument — the strongest thing here

`B -> C` and `D -> E` are **the same intervention applied to two different
orchestrators**. If both move in the same direction, the finding is not an artifact
of one harness. Write this up as an intentional replication, because it is the
single strongest structural feature of the design.

## How B_data's role changes

`B_data` was constructed as a proxy for Prometheus while access was pending. Once
`D_prometheus` exists, B is no longer standing in for anything — it is "a generic
LLM with code execution."

**Say this explicitly in the methodology.** A reviewer who notices the reframing
unprompted will read it as a design drift; stated openly it reads as the honest
account of a plan that improved when a dependency unblocked.

## Defending the reproducibility asymmetry

D and E cannot be re-run by an examiner: the Graph Engine is Manifold AI
proprietary, NDA-covered, and never enters the repository.

Do not apologise for this. Present the ladder as **two tiers that corroborate each
other**:

- **A-C** — fully reproducible from the repository plus an API key. Anyone can
  verify the mechanism.
- **D-E** — ecological validation in a real production agent. Nobody outside the
  collaboration could produce it.

Neither tier is sufficient alone; together they cover both internal and external
validity. A purely reproducible study would not show the effect survives contact
with a production system; a purely proprietary one could not be checked at all.

## Data comparability

All five scenarios must see the same data snapshot and the same held-out target
month, or they are not answering the same question.

The Royal Unibrew warehouse that Prometheus can read is refreshed **monthly, not
daily**; a re-poll on 2026-08-19 returned data through **July 2026**, matching the
local Nielsen snapshot exactly. Within August the sources coincide.

Two caveats for the write-up:

1. The coincidence is a **timing property, not a guarantee** — it expires at the
   next refresh. If runs slip past August, re-verify before claiming equivalence.
2. Where the engine supports reading a local snapshot (`type: file`), prefer it:
   it converts identical-input from a coincidence into an enforced property.

Record the data source in each run's trace regardless.

## The RAM budget figure — replace fabrication with measurement

`04_thesis_results/generate_figures.py::fig4_ram_budget` is currently **entirely
hardcoded** and does not read any data. Among its literals is a 512 MB "active ML
model (worst case)". The **measured** footprint of the served model is **3-4 MB**.

That figure cannot be defended and must not ship as-is.

Prometheus makes the honest version *stronger* than the invented one. The
compute-constraint claim was never "ML models are heavy":

> The trained model is the cheap part. The agent runtime is where the budget goes.

| Component | Footprint |
|-----------|-----------|
| Trained model, served | 3-4 MB (measured, `srq1_profiling.py`) |
| Agent runtime / graph engine | hundreds of MB (to be measured) |

This reframes the deployment argument usefully: the marginal cost of *adding* a
dedicated forecasting model to an existing agent is negligible against the runtime
already being paid for. That is a genuine finding and directly supports the
thesis's practical claim.

## Scope note — SRQ3 is unchanged by default

`srq3-integration-readiness.md` frames SRQ3 as an **assessment** by design, not
merely because access was blocked. Obtaining Prometheus does not automatically
convert it into a completed integration. Reframing it is a deliberate scope
decision for Brian and Enrico, and should not be assumed.

## Related

- `srq4-experiment-design-rationale.md` — scenarios A-C, the information ladder
- `srq4-first-results-and-interpretation.md` — the 18-run A/B/C result
- `plans/P0040_2026-08-20_prometheus-scenarios-d-e/` — execution plan and findings

---

# Pooled vs per-category modelling (SRQ1)

Added 2026-08-20. SRQ1's headline question names a **three-way** trade-off —
accuracy, memory efficiency, and **category specialization** — and
`srq1-models-efficiency.md:32` glosses the third as *"does a per-category model
beat a single pooled model?"* The results currently report the first two only:
`tuned_metrics.csv` holds 4 categories x 2 models and no pooled row. **Treat this
as a gap an examiner will look for, not an optional extra.**

## The feature intersection is a finding, not a limitation

Pooling requires a common feature set. Measured across the four
`*_feature_matrix_h3.parquet` files:

| | Count |
|---|---|
| Columns present in all four categories | **33** |
| Union | 51 |
| Missing from at least one | 18 |

**Write this up as a substantive result, because that is what it is.** The 18
non-shared columns are one coherent family — `baseline_*`, `promo_*`, and the
`weighted_distribution_*` promo/feature/display variants — and they are absent for
a real reason: **danskvand and RTD carry no promotional signal at all** (the
promo-zero finding). The intersection is therefore a *consequence of the Danish
beverage market's structure as Nielsen measures it*, not an arbitrary modelling
restriction.

The framing that follows: a pooled model across these categories is necessarily
restricted to non-promotional features, because promotion is not measured
everywhere. That is a genuine constraint on cross-category modelling in FMCG and
worth stating as such.

## Why intersect rather than union-with-NaN

Both sides of the comparison must see the same features, or two things change at
once and the result is uninterpretable.

There is a second, subtler reason. Under union-with-NaN, every danskvand row has
`promo_intensity = NaN`, and a tree can split on *is-NaN* — a split that separates
danskvand from CSD/energidrikke perfectly. The pooled model would then carry a
hidden category indicator and could learn per-category behaviour internally,
**partly becoming four models wearing one coat.** A good score would no longer
distinguish "cross-category learning helped" from "the model rebuilt the
specialization we were testing against." That is a construct-validity failure, not
a prediction-quality one, and the intersection removes it.

## The cost of dropping promo is measurably small

From `04_thesis_results/srq1/shap_importance.csv` (mean absolute SHAP):

| Category | 1st | 2nd | `promo_intensity` |
|----------|-----|-----|-------------------|
| CSD | lag_1 (1.319) | weighted_distribution (1.146) | 0.100 — 7th |
| energidrikke | lag_1 (1.428) | weighted_distribution (1.150) | outside top 8 |
| danskvand | lag_1 (1.344) | weighted_distribution (0.607) | absent |
| RTD | lag_1 (1.464) | weighted_distribution (0.760) | absent |

Promo is a minor contributor even where measured, so the intersection does not
meaningfully handicap CSD or energidrikke.

Worth reporting on its own: **the importance structure is near-identical across all
four categories** — `lag_1` then `weighted_distribution` dominate everywhere. That
is a mild prior in favour of pooling working, and it is a defensible reason to have
expected the comparison to be close.

**Before citing any of these numbers, regenerate the artifact.** It still contains
`holiday_month`, the pre-rename name for `peak_month`, so it predates that rename
and probably the 2026-08-19 re-tuning.

## Brand identity across categories

Brand names are **not** mutually exclusive: 213 unique names against 230
category-brand pairs, so 17 recur. Most are genuine multi-category brands (HARBOE,
FEVER TREE, SAN PELLEGRINO — CSD and danskvand alone share 11).

`OTHER BRAND` is **not a brand** but a per-category residual bucket, and it appears
in three categories with different contents each time.

**The pooled series key must therefore be `(category, brand)`, never `brand`
alone.** Methodologically this belongs in the write-up as a data-preparation
decision, since pooling on name would silently merge unrelated series.

---

# Feature importance is not feature selection

Added 2026-08-20. A measured instance worth a short methodology paragraph, because
the thesis can demonstrate the principle rather than assert it.

## The observation

`weighted_dist` ranked **#2 by mean absolute SHAP** in the CSD model (1.146, behind
only `lag_1`). It was nonetheless **dropped from model inputs**, because removing it
*improved* held-out accuracy in **3 of 4 categories** (commit `f4779a7`).

State plainly that this was an **accuracy decision, not a leakage fix.** The feature
was explicitly tested for leakage and cleared: it is structural and nearly static,
corr(t, t-1) = 0.976. Conflating "dropped for leakage" with "dropped because it did
not help" would misrepresent the modelling process.

## Why it is not a contradiction

The obvious explanation -- redundancy with the lag features -- **does not hold**, and
saying so strengthens the point. Measured on CSD (n = 4,275):

| Quantity | Value |
|----------|-------|
| corr(`weighted_dist`, `log_sales_units`) | 0.673 |
| corr(`lag_1`, `log_sales_units`) | 0.445 |
| corr(`weighted_dist`, `lag_1`) | 0.437 |
| **partial** corr(`weighted_dist`, target \| `lag_1`) | **0.594** |

The partial correlation barely drops below the raw one, so `weighted_dist` carries
information the lags do not. It is genuinely informative *and* removing it helped.

The resolution is that the two quantities answer different questions:

- **SHAP** measures how much the fitted model **used** a feature, on data it was fit
  around. A strong correlate will be leaned on. High SHAP means "relied upon", not
  "generalises."
- **Held-out error** measures whether that reliance **paid off on unseen months**.

`weighted_dist` is nearly static, making it close to a brand-identity fingerprint. A
tree can use it to recognise *which brand it is looking at* and recall that brand's
typical level -- effective until distribution shifts in the test window, at which
point the memorised level is wrong.

Had the feature been merely redundant, dropping it would have been roughly neutral.
That dropping it **helped** indicates active harm: the signature of over-reliance.

## What to claim

Model selection in this thesis was driven by **held-out error, not importance
ranking**, and this feature is the concrete justification. The general point --
that attribution methods explain a fitted model rather than identify features worth
fitting on -- is well known, but the thesis has its own measured instance, which is
more persuasive than a citation alone.

The column remains in the feature matrix for EDA (which is why the correlation
figures above are computable); it is simply not a model input.
