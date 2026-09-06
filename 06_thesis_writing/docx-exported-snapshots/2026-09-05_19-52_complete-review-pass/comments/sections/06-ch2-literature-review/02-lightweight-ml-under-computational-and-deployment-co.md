# Comments -- Lightweight ML under Computational and Deployment Constraints

> Objections on **Literature Review > Lightweight ML under Computational and Deployment Constraints**
>
> Prose: `chapters/sections/06-ch2-literature-review/02-lightweight-ml-under-computational-and-deployment-co.md`
>
> 3 comment(s) in 3 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
3 comment(s) in 3 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [71](#c71) | Lightweight ML under Computational and Deploy |  |  | This is true, but again, Manifold is not hosting its own LLM instance, they just... |
| [72](#c72) | Lightweight ML under Computational and Deploy |  |  | Again a good point, but referring to hosting LLMs. Something Manifold doesnt do.... |
| [73](#c73) | Lightweight ML under Computational and Deploy |  |  | So this part kind of makes all the previous hosting claims a bit less bad, becau... |

---

<a id="c71"></a>

## [71] Brian Rohde -- Literature Review

- **Section:** Literature Review > Lightweight ML under Computational and Deployment Constraints
- **Date:** 2026-09-01T20:21:00
- **On:** “The cost asymmetry is substantial: transformer-based forecasters and locally hosted large language models often require substantially more accelerator memory than lightweight tabular models, available only on GPU instances that are markedly more expensive to run continuously than a general-purpose instance with a few gigabytes of RAM; for a provider serving inference across many client queries, this difference can materially affect operating costs. Computational efficiency is therefore a binding consideration rather than an afterthought.”

This is true, but again, Manifold is not hosting its own LLM instance, they just allocated 4 GB of Ram per conversation and to allow for code execution of the LLM, which they access via OpenAIs API.

<a id="c72"></a>

## [72] Brian Rohde -- Literature Review

- **Section:** Literature Review > Lightweight ML under Computational and Deployment Constraints
- **Date:** 2026-09-01T20:33:00
- **On:** “Semerikov et al. (2025) survey resource-constrained LLM deployment, documenting that quantisation and knowledge distillation are the dominant practical strategies but that even aggressively compressed LLMs typically require on the order of one to four gigabytes.”

Again a good point, but referring to hosting LLMs. Something Manifold doesnt do.

<a id="c73"></a>

## [73] Brian Rohde -- Literature Review

- **Section:** Literature Review > Lightweight ML under Computational and Deployment Constraints
- **Date:** 2026-09-01T20:35:00
- **On:** “The implication for a multi-component pipeline that must simultaneously load data, run forecasting models, and host a reasoning layer is that local LLM inference is difficult to accommodate within a small fixed memory budget; accessing the language model through an external API, rather than loading it locally, is the more viable pattern under such constraints.”

So this part kind of makes all the previous hosting claims a bit less bad, because it leads to why manifold accesses the LLM via API and can therefore resort to only 4 GBs of cloud code execution sandboxes. But might need a  bit more elaboration and contextualization, to not let the viewer think we are trying to solve hosting a LLM in compute constraint environments, which we are not doing.
