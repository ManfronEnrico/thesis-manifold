# SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst

> Section of **Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- METACOMMENT, ACADEMIC, VERIFY. Detail: `comments/sections/12-ch8-experimental-evaluation/03-level-2-recommendation-quality-evaluation-srq2/03-srq4-baseline-code-as-action-agent-prometheus-not-a-.md`

---

The SRQ4 baseline is not a human analyst (that comparison is out of scope - infeasible within the project timeline). It is the production code-as-action agent, Prometheus (the Manifold/Royal Unibrew Graph Engine): a LangGraph + PydanticAI agent whose coder writes and executes SQL/Python in an E2B sandbox in an investigate-and-verify loop to answer a data/forecasting brief. SRQ4 therefore compares the dedicated-model integration (this thesis: an LLM that *delegates* forecasting to pre-trained XGBoost models exposed as a structured tool) against the code-as-action baseline (Prometheus: an LLM that *writes its own* forecasting code), on correctness, consistency, replicability, cost and latency over a common prompt set. Both run on the same Nielsen categories (CSD, danskvand, energidrikke, RTD); execution is local + sandbox, with no human-in-the-loop baseline.
