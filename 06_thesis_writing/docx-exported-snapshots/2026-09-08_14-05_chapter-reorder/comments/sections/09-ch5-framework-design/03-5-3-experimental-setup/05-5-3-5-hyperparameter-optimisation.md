# Comments -- 5.3.5 Hyperparameter optimisation

> Objections on **Chapter 5 | Model Benchmark & Selection > 5.3 Experimental setup > 5.3.5 Hyperparameter optimisation**
>
> Prose: `chapters/sections/09-ch5-framework-design/03-5-3-experimental-setup/05-5-3-5-hyperparameter-optimisation.md`
>
> 1 comment(s) in 1 thread(s).

Extracted 2026-09-08 from `thesis_full.docx`.
1 comment(s) in 1 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [238](#c238) | 5.3.5 Hyperparameter optimisation | VERIFY, SOURCE |  | VERIFY, SOURCES... |

---

<a id="c238"></a>

## [238] Brian Rohde -- Chapter 5 | Model Benchmark & Selection  `VERIFY * SOURCE`

- **Section:** Chapter 5 | Model Benchmark & Selection > 5.3 Experimental setup > 5.3.5 Hyperparameter optimisation
- **Date:** 2026-09-05T15:26:00
- **On:** “Hyperparameter optimisationOptuna’s TPE sampler, 100 trials per model × category × objective. TPE models the configuration density conditional on performance, splitting observed trials into densities l(x) below and g(x) above a quantile threshold (Bergstra et al., 2011, p. 2549). Optuna supplies the define-by-run interface, sampling and pruning infrastructure (Akiba et al., 2019, p. 2623).The trial budget is justified empirically, not by convention. No trial-count convention exists in the HPO literature; the requirement scales with search-space dimensionality. The tuner therefore records the running best CV score per trial and reports the trial after which improvement becomes negligible. Measured plateaus range from 3 to 87 trials with a median near 16, so 100 trials comfortably contains the converged region for every configuration.”

VERIFY, SOURCES
