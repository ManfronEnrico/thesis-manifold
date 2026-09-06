# Comments -- The Bounded Tool-Using Agentic Layer

> Objections on **Predictive-Extension Architecture > The Bounded Tool-Using Agentic Layer**
>
> Prose: `chapters/sections/09-ch5-framework-design/05-the-bounded-tool-using-agentic-layer.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [213](#c213) | The Bounded Tool-Using Agentic Layer | CONTEXT |  | CONTEXT: Its also relevant to raise that the sandbox is being instatiated on dem... |
| [214](#c214) | The Bounded Tool-Using Agentic Layer | VERIFY |  | VERIFY: No human in loop atp i think... |
| [215](#c215) | The Bounded Tool-Using Agentic Layer | CONTEXT |  | CONTEXT: Besides in Scenarios A, B, and D... |
| [216](#c216) | The Bounded Tool-Using Agentic Layer | VERIFY |  | VALIDATE: I think the model we ahve pinned does not even accept temperature as a... |

---

<a id="c213"></a>

## [213] Brian Rohde -- Predictive-Extension Architecture  `CONTEXT`

- **Section:** Predictive-Extension Architecture > The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:39:00
- **On:** “The agentic layer is an LLM orchestrator accessed through a remote API rather than loaded locally, a decision that keeps the language model out of the RAM budget entirely (a locally hosted model would add several gigabytes; Semerikov et al., 2025)”

CONTEXT: Its also relevant to raise that the sandbox is being instatiated on demand, meaning only if queries are are actually send by end users, will the company be charged, cutting down the server costs significantly.

<a id="c214"></a>

## [214] Brian Rohde -- Predictive-Extension Architecture  `VERIFY`

- **Section:** Predictive-Extension Architecture > The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:40:00
- **On:** “subject to human-in-the-loop checkpoints.”

VERIFY: No human in loop atp i think

<a id="c215"></a>

## [215] Brian Rohde -- Predictive-Extension Architecture  `CONTEXT`

- **Section:** Predictive-Extension Architecture > The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:40:00
- **On:** “: the LLM does not itself predict demand or compute the forecast”

CONTEXT: Besides in Scenarios A, B, and D

<a id="c216"></a>

## [216] Brian Rohde -- Predictive-Extension Architecture  `VERIFY`

- **Section:** Predictive-Extension Architecture > The Bounded Tool-Using Agentic Layer
- **Date:** 2026-09-03T18:41:00
- **On:** “Decoding is configured for reproducibility (temperature zero)”

VALIDATE: I think the model we ahve pinned does not even accept temperature as a argument.
