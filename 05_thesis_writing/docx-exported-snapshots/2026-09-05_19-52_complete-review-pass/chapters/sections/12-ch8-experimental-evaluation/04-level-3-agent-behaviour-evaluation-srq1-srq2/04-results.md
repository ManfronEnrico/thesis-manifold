# Results

> Section of **Experimental Evaluation > Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2) > Results**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, METACOMMENT, OUTDATED. Detail: `comments/sections/12-ch8-experimental-evaluation/04-level-3-agent-behaviour-evaluation-srq1-srq2/04-results.md`

---

Peak RAM (tracemalloc) is in the **tens of MB** for every model - Ridge 1.5, LightGBM 18.7, XGBoost 0.2, ARIMA 0.5 MB - i.e. three orders of magnitude below the 8 GB ceiling; the constraint is non-binding at this data scale (a different result from the hypothesised 4–6 GB, because the corrected matrices are far smaller than the all-markets ones). Training latency is seconds, not minutes (XGBoost ~1.7 s, LightGBM ~7.7 s with its tuned n_estimators); inference is ~16 ms for XGBoost. The Synthesis Agent adds only structured arithmetic plus, optionally, one LLM API call (~1–3 s, no local RAM). The end-to-end pipeline therefore runs comfortably within the operational budget. Note: tracemalloc captures Python-level allocations; native LightGBM/XGBoost C++ buffers are additional but small at this scale.
*(Failure-mode analysis §8.4.3* *-* *API timeout / fallback* *-* *is part of the agentic harness evaluation and is run with the LLM-dependent layer.)*
