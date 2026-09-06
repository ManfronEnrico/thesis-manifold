# The Code-as-Action Baseline (SRQ4)

> Section of **Predictive-Extension Architecture > The Code-as-Action Baseline (SRQ4)**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- CONTEXT. Detail: `comments/sections/09-ch5-framework-design/07-the-code-as-action-baseline-srq4.md`

---

To evaluate whether dedicated-model integration is warranted at all, the architecture includes a **code-as-action baseline**: a general-purpose LLM that, given the same data access and the same prompts, writes, executes, and self-corrects its own forecasting and analysis code in a sandboxed environment (for example, E2B as it is used in our testing scenarios), without a dedicated pre-built model (Wang et al., 2024). The baseline uses the **same base LLM** as the agentic layer, so that the comparison isolates the effect of dedicated-model integration rather than differences in model quality.
The baseline is runnable locally and does not require access to the production system, which makes the SRQ4 comparison feasible independently of integration access. The comparison protocol and metrics (correctness, consistency, and replicability as primary dimensions; cost and latency as secondary; following the multidimensional frame of Mehta, 2025) are specified in Chapter 3 and applied in Chapter 8.
