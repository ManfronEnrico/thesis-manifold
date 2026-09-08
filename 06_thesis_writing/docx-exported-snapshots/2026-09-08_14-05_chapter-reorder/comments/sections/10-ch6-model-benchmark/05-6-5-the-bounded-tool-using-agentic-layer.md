# Comments -- 6.5 The Bounded Tool-Using Agentic Layer

> Objections on **Chapter 6 | Predictive-Extension Architecture > 6.5 The Bounded Tool-Using Agentic Layer**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/05-6-5-the-bounded-tool-using-agentic-layer.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-08 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [319](#c319) | 6.5 The Bounded Tool-Using Agentic Layer | CONTEXT |  | CONTEXT: Its also relevant to raise that the sandbox is being instatiated on dem... |
| [320](#c320) | 6.5 The Bounded Tool-Using Agentic Layer | VERIFY |  | VERIFY: No human in loop atp i think... |
| [321](#c321) | 6.5 The Bounded Tool-Using Agentic Layer | CONTEXT |  | CONTEXT: Besides in Scenarios A, B, and D... |
| [322](#c322) | 6.5 The Bounded Tool-Using Agentic Layer | VERIFY |  | VALIDATE: I think the model we ahve pinned does not even accept temperature as a... |

---

<a id="c319"></a>

## [319] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `CONTEXT`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.5 The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:39:00
- **On:** “The agentic layer is an LLM orchestrator accessed through a remote API rather than loaded locally, a decision that keeps the language model out of the RAM budget entirely (a locally hosted model would add several gigabytes; Semerikov et al., 2025)”

CONTEXT: Its also relevant to raise that the sandbox is being instatiated on demand, meaning only if queries are are actually send by end users, will the company be charged, cutting down the server costs significantly.

<a id="c320"></a>

## [320] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `VERIFY`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.5 The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:40:00
- **On:** “subject to human-in-the-loop checkpoints.”

VERIFY: No human in loop atp i think

<a id="c321"></a>

## [321] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `CONTEXT`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.5 The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:40:00
- **On:** “: the LLM does not itself predict demand or compute the forecast”

CONTEXT: Besides in Scenarios A, B, and D

<a id="c322"></a>

## [322] Brian Rohde -- Chapter 6 | Predictive-Extension Architecture  `VERIFY`

- **Section:** Chapter 6 | Predictive-Extension Architecture > 6.5 The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:41:00
- **On:** “Decoding is configured for reproducibility (temperature zero)”

VALIDATE: I think the model we ahve pinned does not even accept temperature as a argument.
