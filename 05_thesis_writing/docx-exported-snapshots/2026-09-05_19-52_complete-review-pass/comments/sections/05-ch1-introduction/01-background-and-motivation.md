# Comments -- Background and Motivation

> Objections on **Introduction > Background and Motivation**
>
> Prose: `chapters/sections/05-ch1-introduction/01-background-and-motivation.md`
>
> 19 comment(s) in 8 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
19 comment(s) in 8 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [15](#c15) | Background and Motivation |  | 2 | We didnt really add any enrichment (e.g. Holiday Calendar).... |
| [18](#c18) | Background and Motivation |  | 1 | Again we did not enrich... |
| [20](#c20) | Background and Motivation |  | 1 | This premise is not supported. Seems to be an artifact from previous RQ iteratio... |
| [22](#c22) | Background and Motivation |  | 2 | This is a bit difficutl/useless. In the beginning we wanted to go that angle, ho... |
| [25](#c25) | Background and Motivation |  | 1 | Again this might not be really accurate. Training the models in the cloud yes. D... |
| [27](#c27) | Background and Motivation |  | 1 | That is true, if we taling about hosting an LLM locally or on a server. But Mani... |
| [29](#c29) | Background and Motivation |  | 1 | This is not verified, or must be confirmed.... |
| [31](#c31) | Background and Motivation |  | 2 | The overall premise of our thesis soudns promising, but the RAM contstraint is n... |

---

<a id="c15"></a>

## [15] Brian Rohde -- Introduction  `thread of 3`

- **Section:** Introduction > Background and Motivation
- **Date:** 2026-09-01T14:32:00
- **On:** “enriched with exogenous contextual features substantially outperform statistical baselines for high-volume stable SKUs.”

We didnt really add any enrichment (e.g. Holiday Calendar).

<a id="c16"></a>

### [16] Guest User -- reply

- **Date:** 2026-09-02T10:21:00

yes, we do not have any exogenous variable in our model... however this is a statement coming from Ma et al...  so the claim is just reporting ma et al findings rather than saying what we have done/ we will do... we have used them also to say that is better having multiple models rather than one that fits all.What we are actually carrying is the lagged "promo" variable which is kinda exogenous...so the honest position here is that we have no exogenous variable and we can handle in 2 ways in my opinion: a) keeping it saying that it is important and valuable but we do not have it as a limitationb) trim the exogenous clause from Ch1 and keep only "no single model dominates", which is the half our results actually engage with(I´d go with a)

<a id="c17"></a>

### [17] Brian Rohde -- reply

- **Date:** 2026-09-03T14:15:00

„What we are actually carrying is the lagged "promo" variable which is kinda exogenous…” >> not really exogenoues by definition is an outside variable, not any derived ones from the dataset. 


Actually I would go with option c), simply include one exogenous variable (the holiday API). I used it already in a different previous project. So its hella easy and free to integrate. 


Easy adaptation that makes our thesis even more grounded in academic literature. Also especially because the M5 competition paper also highlighted exogenous variables as crucial.

<a id="c18"></a>

## [18] Brian Rohde -- Introduction  `thread of 2`

- **Section:** Introduction > Background and Motivation
- **Date:** 2026-09-01T14:33:00
- **On:** “including promotional calendars and environmental signals, materially improved forecasting accuracy”

Again we did not enrich

<a id="c19"></a>

### [19] Guest User -- reply

- **Date:** 2026-09-02T10:21:00

see answer 1

<a id="c20"></a>

## [20] Brian Rohde -- Introduction  `thread of 2`

- **Section:** Introduction > Background and Motivation
- **Date:** 2026-09-01T14:34:00
- **On:** “This thesis takes up that direction by incorporating exogenous predictors into its forecasting substrate”

This premise is not supported. Seems to be an artifact from previous RQ iterations. If we want to maintain that, we must enrich (Holiday Calendar, or other exogenous variables

<a id="c21"></a>

### [21] Guest User -- reply

- **Date:** 2026-09-02T10:21:00

see answer 1

<a id="c22"></a>

## [22] Brian Rohde -- Introduction  `thread of 3`

- **Section:** Introduction > Background and Motivation
- **Date:** 2026-09-01T14:37:00
- **On:** “computational resource limitations.”

This is a bit difficutl/useless. In the beginning we wanted to go that angle, however, we train the models outside of the cloud deployment, which is the most compute heavy part of the process. Deploying and accessing the models only takes MBs instead of GBs. The 6-8 GB budget per sandbox deployment is more than sufficient. 


So we must revisit why we even talk about resource limits, or what I lean towards, remove that part from our promise and only focus on imrpoving the models.

<a id="c23"></a>

### [23] Guest User -- reply

- **Date:** 2026-09-02T11:40:00

yes I do agree, as u mentioned in the audio the computational constraint is more relevant only when companies have a property model hosting it locally,I don´t really know how the computational angle could be faced trough our current setup... so I would say that if u have some valuable angles on this we can consider them and eventually include them in the thesis, otherwise we can rmove it and maybe insert it in future work/limitatins

<a id="c24"></a>

### [24] Brian Rohde -- reply

- **Date:** 2026-09-03T14:21:00

Fair points. I think in this case it is just important to transparently report the performance metrics.


I was also doing some tests / logging regarding the time necessary to run a re-train on demand (to potentially utilize the 4 GB Ram), but this fails primarily on the wallclock time (~ 400 seconds for a 100 CV training), which disqualifies this angle on the basis of no user wanting to wait for a good 6 minutes at minimum.


Which a highly optimistic baseline, granted that the LLM/Prometheus would need to either have access to / gets send all the additional prompt guidelines as additional prompt context, which would explode the cost. And also it would probably differ every single time to varying degrees in the results / approach -> which is a transparency and reproducibility nightmare. 


So i think that should be enough.

<a id="c25"></a>

## [25] Brian Rohde -- Introduction  `thread of 2`

- **Section:** Introduction > Background and Motivation
- **Date:** 2026-09-01T14:38:00
- **On:** “Enterprise cloud deployments capable of running large deep learning models at scale are economically inaccessible to small and medium-sized AI providers”

Again this might not be really accurate. Training the models in the cloud yes. Deploying them in a trained status consumes barely anyhting.

<a id="c26"></a>

### [26] Guest User -- reply

- **Date:** 2026-09-02T13:45:00

yes i do agree (see answer 2)

<a id="c27"></a>

## [27] Brian Rohde -- Introduction  `thread of 2`

- **Section:** Introduction > Background and Motivation
- **Date:** 2026-09-01T14:40:00
- **On:** “locally hosted large language models require GPU instances with tens to hundreds of gigabytes of accelerator memory, which on major cloud platforms cost on the order of one to seven US dollars per hour of continuous operation [CITATION TO ADD: cloud-instance pricing source], whereas a general-purpose instance with eight gigabytes of RAM costs a small fraction of that”

That is true, if we taling about hosting an LLM locally or on a server. But Manifold is not doing that. They are dedicating 8 GBs of RAM per session, but in the background they are simply calling the OpenAI API for the intelligence, which is maitained and hosted by OpenAI on servers. 


Manifold is not running anything. The 8 GB RAM cloud sandbox budget is for the cloud code executions and the conversation, not runnign the model.

<a id="c28"></a>

### [28] Guest User -- reply

- **Date:** 2026-09-02T13:46:00

yes i do agree (see answer 2)

<a id="c29"></a>

## [29] Brian Rohde -- Introduction  `thread of 2`

- **Section:** Introduction > Background and Motivation
- **Date:** 2026-09-01T14:40:00
- **On:** “working with four terabytes of Nielsen weekly scanner data”

This is not verified, or must be confirmed.

<a id="c30"></a>

### [30] Guest User -- reply

- **Date:** 2026-09-02T13:47:00

ok

<a id="c31"></a>

## [31] Brian Rohde -- Introduction  `thread of 3`

- **Section:** Introduction > Background and Motivation
- **Date:** 2026-09-01T15:05:00
- **On:** “however, addresses the specific combination this thesis targets: a lightweight forecasting substrate, exposed to a bounded tool-using agentic layer through a structured interface that preserves reliability and uncertainty, and deployed under a fixed RAM budget”

The overall premise of our thesis soudns promising, but the RAM contstraint is not properly elaborated, as I said in the comments above. We must make sure we actually have proper usage of the RAM budget. 


Perhaps we must make some changes to our experiment structure, where we actually test in the sandbox environment, whether we can supply the code-action enabled OpenAI API LLM, an instruction harness which allows it to train/re-train the ML models each query in the cloud. 


This would actually consume significant RAM resources, or at least significantly more that the deployment (GBs vs MBs), as we use light weight models anyways. 


Because currently the whole RAM discussion has no impact, as we train outside of the sandbox environment and only deploy trained models, which dont consume anything at all. 


Also our premise of the thesis is also to investigate which benefits a multi-indicator ML model serving approach will ahve on the prediciton quality, cost, and latency of AI agents. Something which is not really elaborated or highlighted properly so far. The main focus is only the limited RAM environemnt, which as said before is currently underutilized in the actual code base or experiments

<a id="c32"></a>

### [32] Guest User -- reply

- **Date:** 2026-09-02T13:49:00

let´s align together on this! so let´s have a call asap so we decide which RAM angle to take (if not none)

<a id="c33"></a>

### [33] Brian Rohde -- reply

- **Date:** 2026-09-03T14:23:00

I actually tested this already and ruled it out (previous answers to your answers above)
