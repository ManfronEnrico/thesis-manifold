# Hyperparameter optimisation

> Section of **Model Benchmark & Selection > Experimental setup > Hyperparameter optimisation**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE. Detail: `comments/sections/10-ch6-model-benchmark/03-experimental-setup/05-hyperparameter-optimisation.md`

---

Optuna’s TPE sampler, **100 trials** per model × category × objective. TPE models the configuration density conditional on performance, splitting observed trials into densities *l(x)* below and *g(x)* above a quantile threshold (Bergstra et al., 2011, p. 2549). Optuna supplies the define-by-run interface, sampling and pruning infrastructure (Akiba et al., 2019, p. 2623).
**The trial budget is justified empirically, not by convention.** No trial-count convention exists in the HPO literature; the requirement scales with search-space dimensionality. The tuner therefore records the running best CV score per trial and reports the trial after which improvement becomes negligible. Measured plateaus range from 3 to 87 trials with a median near 16, so 100 trials comfortably contains the converged region for every configuration.
