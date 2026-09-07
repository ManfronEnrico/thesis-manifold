# Comments — Chapter 5 | Predictive-Extension Architecture

Extracted 2026-09-07 from `MSc. Data Science - 175888 and 176171 - Master Thesis.docx`.
17 comment(s) in 17 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [204](#c204) | Chapter 5 | Predictive-Extension Architecture | FORMATTING |  | FORMATTING: Could use a subtitle for the chapter... |
| [206](#c206) | 5.1 Design Objectives and Constraints | METACOMMENT |  | METACOMMENT... |
| [207](#c207) | 5.1 Design Objectives and Constraints | METACOMMENT |  | METACOMMENT... |
| [209](#c209) | 5.2 Architectural Overview | VERIFY, INCORRECT |  | INCORRECT / VERIFY: Not really implemented as far as I know. There is no gate wh... |
| [210](#c210) | 5.2 Architectural Overview | VERIFY |  | VERIFY: See previous comment... |
| [215](#c215) | 5.3 The Forecasting Substrate (SRQ1) | MISSING |  | MISSING: the holiday api enrichment... |
| [216](#c216) | 5.3 The Forecasting Substrate (SRQ1) | UPDATE |  | UPDATE: Not really relevant due to the low ram usage on deploy (50mb). As i said... |
| [217](#c217) | 5.3 The Forecasting Substrate (SRQ1) | VERIFY |  | VERIFY... |
| [219](#c219) | 5.4 The Structured Forecast-Tool Interface (S | VERIFY |  | VERIFY... |
| [221](#c221) | 5.5 The Bounded Tool-Using Agentic Layer | CONTEXT |  | CONTEXT: Its also relevant to raise that the sandbox is being instatiated on dem... |
| [222](#c222) | 5.5 The Bounded Tool-Using Agentic Layer | VERIFY |  | VERIFY: No human in loop atp i think... |
| [223](#c223) | 5.5 The Bounded Tool-Using Agentic Layer | CONTEXT |  | CONTEXT: Besides in Scenarios A, B, and D... |
| [224](#c224) | 5.5 The Bounded Tool-Using Agentic Layer | VERIFY |  | VALIDATE: I think the model we ahve pinned does not even accept temperature as a... |
| [229](#c229) | 5.7 The Code-as-Action Baseline (SRQ4) | CONTEXT |  | CONTEXT: I think it would help tremendously to name each scenario and map it to ... |
| [230](#c230) | 5.7 The Code-as-Action Baseline (SRQ4) | CONTEXT |  | CONTEXT: „locally“ is a bit deceiving, because the API needs internet access and... |
| [236](#c236) | 5.9 Technology Choices and Justification | METACOMMENT |  | METACOMMMENT... |
| [238](#c238) | 5.9 Technology Choices and Justification | TABLE-REFERENCE, PROSE |  | PROSE & TABLE REFERENCE... |

---

<a id="c204"></a>

## [204] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `FORMATTING`

- **Section:** Chapter 5 | Predictive-Extension Architecture
- **Date:** 2026-09-05T18:53:00
- **On:** “COULD USE A SUBTITLE”

FORMATTING: Could use a subtitle for the chapter

<a id="c206"></a>

## [206] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `METACOMMENT`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.1 Design Objectives and Constraints
- **Date:** 2026-09-03T17:38:00
- **On:** “A note on status: this is a design specification, but its lower layers are implemented and measured”

METACOMMENT

<a id="c207"></a>

## [207] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `METACOMMENT`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.1 Design Objectives and Constraints
- **Date:** 2026-09-03T17:39:00
- **On:** “Where a figure depends on a layer still being hardened, this is stated explicitly rather than presented as a settled result”

METACOMMENT

<a id="c209"></a>

## [209] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `VERIFY * INCORRECT`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.2 Architectural Overview
- **Date:** 2026-09-03T17:42:00
- **On:** “with human-in-the-loop checkpoints”

INCORRECT / VERIFY: Not really implemented as far as I know. There is no gate where a human must validate or greenlight any information or outcomes before the Agent makes its recommendation

<a id="c210"></a>

## [210] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `VERIFY`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.2 Architectural Overview
- **Date:** 2026-09-03T17:42:00
- **On:** “human oversight”

VERIFY: See previous comment

<a id="c215"></a>

## [215] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `MISSING`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.3 The Forecasting Substrate (SRQ1)
- **Date:** 2026-09-03T17:53:00
- **On:** “). The gradient-boosted models use the exogenous predictors described in Chapter 4”

MISSING: the holiday api enrichment

<a id="c216"></a>

## [216] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `UPDATE`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.3 The Forecasting Substrate (SRQ1)
- **Date:** 2026-09-03T17:53:00
- **On:** “First, models are executed sequentially (load, run, unload) so that only one model occupies memory at a time, rather than concurrently”

UPDATE: Not really relevant due to the low ram usage on deploy (50mb). As i said before, so sequential is not necessary

<a id="c217"></a>

## [217] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `VERIFY`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.3 The Forecasting Substrate (SRQ1)
- **Date:** 2026-09-03T17:54:00
- **On:** “RSS terms: XGBoost adds about 15 MB, LightGBM about 7 MB, and Ridge under 1 MB over the runtime baseline (sequential, one model resident at a time)”

VERIFY

<a id="c219"></a>

## [219] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `VERIFY`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.4 The Structured Forecast-Tool Interface (SRQ2)
- **Date:** 2026-09-03T18:31:00
- **On:** “Reliability, by validating the agent’s stated numbers against the source forecast values before delivery, so that the agent reports the model’s numbers rather than its own.Uncertainty, by attaching interval information to every forecast; interval calibration follows the post-hoc approach of Kuleshov et al. (2018) and is treated as a design target, not an empirically validated property of the current prototype.Traceability, by recording the mapping from tool call and forecast value to the resulting recommendation, so that each recommendation can be audited back to its source forecast.”

VERIFY

<a id="c221"></a>

## [221] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `CONTEXT`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.5 The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:39:00
- **On:** “The agentic layer is an LLM orchestrator accessed through a remote API rather than loaded locally, a decision that keeps the language model out of the RAM budget entirely (a locally hosted model would add several gigabytes; Semerikov et al., 2025)”

CONTEXT: Its also relevant to raise that the sandbox is being instatiated on demand, meaning only if queries are are actually send by end users, will the company be charged, cutting down the server costs significantly.

<a id="c222"></a>

## [222] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `VERIFY`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.5 The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:40:00
- **On:** “subject to human-in-the-loop checkpoints.”

VERIFY: No human in loop atp i think

<a id="c223"></a>

## [223] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `CONTEXT`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.5 The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:40:00
- **On:** “: the LLM does not itself predict demand or compute the forecast”

CONTEXT: Besides in Scenarios A, B, and D

<a id="c224"></a>

## [224] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `VERIFY`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.5 The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:41:00
- **On:** “Decoding is configured for reproducibility (temperature zero)”

VALIDATE: I think the model we ahve pinned does not even accept temperature as a argument.

<a id="c229"></a>

## [229] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `CONTEXT`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.7 The Code-as-Action Baseline (SRQ4)
- **Date:** 2026-09-03T18:43:00
- **On:** “To evaluate whether dedicated-model integration is warranted at all, the architecture includes a code-as-action baseline: a general-purpose LLM that, given the same data access and the same prompts, writes, executes, and self-corrects its own forecasting and analysis code in a sandboxed environment (for example, E2B as it is used in our testing scenarios), without a dedicated pre-built model (Wang et al., 2024). The baseline uses the same base LLM as the agentic layer, so that the comparison isolates the effect of dedicated-model integration rather than differences in model quality.”

CONTEXT: I think it would help tremendously to name each scenario and map it to the respective set-up

<a id="c230"></a>

## [230] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `CONTEXT`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.7 The Code-as-Action Baseline (SRQ4)
- **Date:** 2026-09-03T18:44:00
- **On:** “baseline is runnable locally and does not require access to the production system”

CONTEXT: „locally“ is a bit deceiving, because the  API needs internet access and nothing is hosted on our end, excep the python code orchestrating the data flow and supplying the API with prompts

<a id="c236"></a>

## [236] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `METACOMMENT`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.9 Technology Choices and Justification
- **Date:** 2026-09-03T18:26:00
- **On:** “(evaluated)”

METACOMMMENT

<a id="c238"></a>

## [238] Brian Rohde -- Chapter 5 | Predictive-Extension Architecture  `TABLE-REFERENCE * PROSE`

- **Section:** Chapter 5 | Predictive-Extension Architecture > 5.9 Technology Choices and Justification
- **Date:** 2026-09-05T15:31:00
- **On:** “Each choice is argued against the four-gigabyte constraint, in keeping with the design criterion of Chapter 1.”

PROSE & TABLE REFERENCE
