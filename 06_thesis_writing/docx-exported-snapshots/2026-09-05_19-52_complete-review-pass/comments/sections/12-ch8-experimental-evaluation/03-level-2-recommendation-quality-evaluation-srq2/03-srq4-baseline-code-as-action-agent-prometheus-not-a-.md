# Comments -- SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst

> Objections on **Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst**
>
> Prose: `chapters/sections/12-ch8-experimental-evaluation/03-level-2-recommendation-quality-evaluation-srq2/03-srq4-baseline-code-as-action-agent-prometheus-not-a-.md`
>
> 2 comment(s) in 2 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
2 comment(s) in 2 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [378](#c378) | SRQ4 baseline - code-as-action agent (Prometh | METACOMMENT, ACADEMIC |  | METACOMMENT, ACADEMIC: Seems like a meta comment... |
| [379](#c379) | SRQ4 baseline - code-as-action agent (Prometh | VERIFY |  | VERIFY... |

---

<a id="c378"></a>

## [378] Brian Rohde -- Experimental Evaluation  `METACOMMENT * ACADEMIC`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst
- **Date:** 2026-09-05T17:40:00
- **On:** “SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst”

METACOMMENT, ACADEMIC:


Seems like a meta comment

<a id="c379"></a>

## [379] Brian Rohde -- Experimental Evaluation  `VERIFY`

- **Section:** Experimental Evaluation > Level 2 - Recommendation quality evaluation (SRQ2) > SRQ4 baseline - code-as-action agent (Prometheus), not a human analyst
- **Date:** 2026-09-05T17:40:00
- **On:** “The SRQ4 baseline is not a human analyst (that comparison is out of scope - infeasible within the project timeline). It is the production code-as-action agent, Prometheus (the Manifold/Royal Unibrew Graph Engine): a LangGraph + PydanticAI agent whose coder writes and executes SQL/Python in an E2B sandbox in an investigate-and-verify loop to answer a data/forecasting brief. SRQ4 therefore compares the dedicated-model integration (this thesis: an LLM that delegates forecasting to pre-trained XGBoost models exposed as a structured tool) against the code-as-action baseline (Prometheus: an LLM that writes its own forecasting code), on correctness, consistency, replicability, cost and latency over a common prompt set. Both run on the same Nielsen categories (CSD, danskvand, energidrikke, RTD); execution is local + sandbox, with no human-in-the-loop baseline.”

VERIFY
