# Comments -- 6.7 The Code-as-Action Baseline (SRQ4)

> Objections on **Chapter 6 | Predictive-Extension Architecture > 6.7 The Code-as-Action Baseline (SRQ4)**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/07-6-7-the-code-as-action-baseline-srq4.md`
>
> 2 comment(s) in 2 thread(s).

Extracted 2026-09-08 from `thesis_full.docx`.
2 comment(s) in 2 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [327](#c327) | 6.7 The Code-as-Action Baseline (SRQ4) | CONTEXT |  | CONTEXT: I think it would help tremendously to name each scenario and map it to ... |
| [328](#c328) | 6.7 The Code-as-Action Baseline (SRQ4) | CONTEXT |  | CONTEXT: „locally“ is a bit deceiving, because the API needs internet access and... |

---

<a id="c327"></a>

## [327] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `CONTEXT`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.7 The Code-as-Action Baseline (SRQ4)
- **Date:** 2026-09-03T18:43:00
- **On:** “To evaluate whether dedicated-model integration is warranted at all, the architecture includes a code-as-action baseline: a general-purpose LLM that, given the same data access and the same prompts, writes, executes, and self-corrects its own forecasting and analysis code in a sandboxed environment (for example, E2B as it is used in our testing scenarios), without a dedicated pre-built model (Wang et al., 2024). The baseline uses the same base LLM as the agentic layer, so that the comparison isolates the effect of dedicated-model integration rather than differences in model quality.”

CONTEXT: I think it would help tremendously to name each scenario and map it to the respective set-up

<a id="c328"></a>

## [328] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `CONTEXT`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.7 The Code-as-Action Baseline (SRQ4)
- **Date:** 2026-09-03T18:44:00
- **On:** “baseline is runnable locally and does not require access to the production system”

CONTEXT: „locally“ is a bit deceiving, because the  API needs internet access and nothing is hosted on our end, excep the python code orchestrating the data flow and supplying the API with prompts
