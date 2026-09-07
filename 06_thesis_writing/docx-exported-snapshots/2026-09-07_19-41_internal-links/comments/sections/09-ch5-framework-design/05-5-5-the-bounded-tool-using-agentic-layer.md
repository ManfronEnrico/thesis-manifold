# Comments -- 5.5 The Bounded Tool-Using Agentic Layer

> Objections on **Chapter 5 | Predictive-Extension Architecture > 5.5 The Bounded Tool-Using Agentic Layer**
>
> Prose: `chapters/sections/09-ch5-framework-design/05-5-5-the-bounded-tool-using-agentic-layer.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-07 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [221](#c221) | 5.5 The Bounded Tool-Using Agentic Layer | CONTEXT |  | CONTEXT: Its also relevant to raise that the sandbox is being instatiated on dem... |
| [222](#c222) | 5.5 The Bounded Tool-Using Agentic Layer | VERIFY |  | VERIFY: No human in loop atp i think... |
| [223](#c223) | 5.5 The Bounded Tool-Using Agentic Layer | CONTEXT |  | CONTEXT: Besides in Scenarios A, B, and D... |
| [224](#c224) | 5.5 The Bounded Tool-Using Agentic Layer | VERIFY |  | VALIDATE: I think the model we ahve pinned does not even accept temperature as a... |

---

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
