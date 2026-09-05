# Comments -- Analytical Approach

> Objections on **Methodology > Analytical Approach**
>
> Prose: `chapters/sections/07-ch3-methodology/05-analytical-approach.md`
>
> 9 comment(s) in 9 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
9 comment(s) in 9 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [109](#c109) | Analytical Approach |  |  | REFERENCE: Here a good reference to the ethical implications and transparency co... |
| [110](#c110) | Analytical Approach | CONTEXT |  | REFERENCE & CONTEXT: We cant just state it with no justification or citation... |
| [111](#c111) | Analytical Approach | SOURCE |  | We also track new metrics of evaluation, amongst others the Median APE. We need ... |
| [112](#c112) | Analytical Approach | WATERMARK, ACADEMIC |  | WATERMARK: I feel like brackets is also not really academic. I was trying to rep... |
| [113](#c113) | Analytical Approach | WATERMARK |  | WATERMARK: Parenthesis issue as before... |
| [114](#c114) | Analytical Approach | OUTDATED |  | OUTDATED: This is no longer true. We have one prompt per category that we keep c... |
| [115](#c115) | Analytical Approach | CONTEXT |  | CONTEXT: We are literally using E2B, also because that is what Manifold uses. Sh... |
| [116](#c116) | Analytical Approach |  |  | That is kind of untrue. E2B is not run locally either way, but if this sentence ... |
| [117](#c117) | Analytical Approach | OUTDATED, CONTEXT |  | OUTDATED: LLM as a Judge not up to date. CONTEXT: Also I feel like we must menti... |

---

<a id="c109"></a>

## [109] Brian Rohde -- Methodology

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:11:00
- **On:** “ARIMA” and “Ridge Regression” provide interpretable statistical and linear baselines with well-understood memory footprints”

REFERENCE: Here a good reference to the ethical implications and transparency considerations when delaing with ML models (super important and prevelant topic in AI & ML literature) would be crucial.


REFERENCE: Also for each model and the claims we made about it, would also benefit from a source

<a id="c110"></a>

## [110] Brian Rohde -- Methodology  `CONTEXT`

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:12:00
- **On:** “Hyperparameters for the gradient-boosted models are tuned with “Optuna”

REFERENCE & CONTEXT: We cant just state it with no justification or citation

<a id="c111"></a>

## [111] Brian Rohde -- Methodology  `SOURCE`

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:13:00
- **On:** “All models are evaluated on a common held-out test set using mean absolute percentage error (MAPE) and root mean squared error (RMSE) as accuracy metrics, peak RAM consumption and runtime as efficiency metrics, and coefficient of variation across repeated runs as a stability metric, following the methodology proposed by Klee and Xia (2025).”

We also track new metrics of evaluation, amongst others the Median APE. We need a source

<a id="c112"></a>

## [112] Brian Rohde -- Methodology  `WATERMARK * ACADEMIC`

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:20:00
- **On:** “(the Prometheus production system, whose Graph Engine is the concrete integration target examined under SRQ3)”

WATERMARK: I feel like brackets is also not really academic. I was trying to rephrase this sentence and remove the brackets, but was kind of struggling, while retaining the information.

<a id="c113"></a>

## [113] Brian Rohde -- Methodology  `WATERMARK`

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:21:00
- **On:** “(Prometheus, whose Graph Engine is the concrete integration interface)”

WATERMARK: Parenthesis issue as before

<a id="c114"></a>

## [114] Brian Rohde -- Methodology  `OUTDATED`

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:22:00
- **On:** “The two pipelines are run on a common set of approximately fifty decision-support prompts”

OUTDATED: This is no longer true. We have one prompt per category that we keep consistent and have varying number of trials of, not 50 different prompts with different trials.

<a id="c115"></a>

## [115] Brian Rohde -- Methodology  `CONTEXT`

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:23:00
- **On:** “sandboxed environment (for example E2B),”

CONTEXT: We are literally using E2B, also because that is what Manifold uses. Should be correctly mentioned.

<a id="c116"></a>

## [116] Brian Rohde -- Methodology

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:24:00
- **On:** “is runnable locally and does not require access to the production system”

That is kind of untrue. E2B is not run locally either way, but if this sentence is supposed to hint at Scenario B here the sandbox is instantiated via the OpenAI API and a passed along parameter, again not hosted locally but by OpenAI in this case.

<a id="c117"></a>

## [117] Brian Rohde -- Methodology  `OUTDATED * CONTEXT`

- **Section:** Methodology > Analytical Approach
- **Date:** 2026-09-03T12:26:00
- **On:** “Scoring uses an LLM-as-judge protocol with a separate judge model, explicit bias awareness, and a human-rated subset for validation. This evaluation is conducted at pilot scale in the first instance rather than as a full study; a full evaluation across the complete prompt set, and an optional comparison against the non-predictive production reference system, are identified as further work”

OUTDATED: LLM as a Judge not up to date.


CONTEXT: Also I feel like we must mention either here, or later on that we did not hold the number of trials per scenario equal (different cost, with Scenario B, C and D, E having significanlty more trials than A)
