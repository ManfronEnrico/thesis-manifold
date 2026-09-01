# Word comments

Extracted 2026-09-01 from `MSc. Data Science - 175888 and 176171 - Master Thesis.docx`.
14 comment(s). Resolved status available.

> Read-only extract. Reply in Word, not here.

## [15] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.1 Background and Motivation
- **Date:** 2026-09-01T14:32:00
- **On:** “enriched with exogenous contextual features substantially outperform statistical baselines for high-volume stable SKUs.”

We didnt really add any enrichment (e.g. Holiday Calendar).

## [16] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.1 Background and Motivation
- **Date:** 2026-09-01T14:33:00
- **On:** “including promotional calendars and environmental signals, materially improved forecasting accuracy”

Again we did not enrich

## [17] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.1 Background and Motivation
- **Date:** 2026-09-01T14:34:00
- **On:** “This thesis takes up that direction by incorporating exogenous predictors into its forecasting substrate”

This premise is not supported. Seems to be an artifact from previous RQ iterations. If we want to maintain that, we must enrich (Holiday Calendar, or other exogenous variables

## [18] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.1 Background and Motivation
- **Date:** 2026-09-01T14:37:00
- **On:** “computational resource limitations.”

This is a bit difficutl/useless. In the beginning we wanted to go that angle, however, we train the models outside of the cloud deployment, which is the most compute heavy part of the process. Deploying and accessing the models only takes MBs instead of GBs. The 6-8 GB budget per sandbox deployment is more than sufficient. 

So we must revisit why we even talk about resource limits, or what I lean towards, remove that part from our promise and only focus on imrpoving the models.

## [19] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.1 Background and Motivation
- **Date:** 2026-09-01T14:38:00
- **On:** “Enterprise cloud deployments capable of running large deep learning models at scale are economically inaccessible to small and medium-sized AI providers”

Again this might not be really accurate. Training the models in the cloud yes. Deploying them in a trained status consumes barely anyhting.

## [20] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.1 Background and Motivation
- **Date:** 2026-09-01T14:40:00
- **On:** “locally hosted large language models require GPU instances with tens to hundreds of gigabytes of accelerator memory, which on major cloud platforms cost on the order of one to seven US dollars per hour of continuous operation [CITATION TO ADD: cloud-instance pricing source], whereas a general-purpose instance with eight gigabytes of RAM costs a small fraction of that”

That is true, if we taling about hosting an LLM locally or on a server. But Manifold is not doing that. They are dedicating 8 GBs of RAM per session, but in the background they are simply calling the OpenAI API for the intelligence, which is maitained and hosted by OpenAI on servers. 

Manifold is not running anything. The 8 GB RAM cloud sandbox budget is for the cloud code executions and the conversation, not runnign the model.

## [21] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.1 Background and Motivation
- **Date:** 2026-09-01T14:40:00
- **On:** “working with four terabytes of Nielsen weekly scanner data”

This is not verified, or must be confirmed.

## [22] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.1 Background and Motivation
- **Date:** 2026-09-01T15:05:00
- **On:** “however, addresses the specific combination this thesis targets: a lightweight forecasting substrate, exposed to a bounded tool-using agentic layer through a structured interface that preserves reliability and uncertainty, and deployed under a fixed RAM budget”

The overall premise of our thesis soudns promising, but the RAM contstraint is not properly elaborated, as I said in the comments above. We must make sure we actually have proper usage of the RAM budget. 

Perhaps we must make some changes to our experiment structure, where we actually test in the sandbox environment, whether we can supply the code-action enabled OpenAI API LLM, an instruction harness which allows it to train/re-train the ML models each query in the cloud. 

This would actually consume significant RAM resources, or at least significantly more that the deployment (GBs vs MBs), as we use light weight models anyways. 

Because currently the whole RAM discussion has no impact, as we train outside of the sandbox environment and only deploy trained models, which dont consume anything at all. 

Also our premise of the thesis is also to investigate which benefits a multi-indicator ML model serving approach will ahve on the prediciton quality, cost, and latency of AI agents. Something which is not really elaborated or highlighted properly so far. The main focus is only the limited RAM environemnt, which as said before is currently underutilized in the actual code base or experiments

## [25] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.3 Research Questions
- **Date:** 2026-09-01T15:09:00
- **On:** “SRQ1: Which lightweight forecasting models provide the best trade-off between accuracy, memory efficiency, and category specialization for FMCG demand forecasting under computational constraints?”

We currently have the accuracy, and category specialitation somewhat answered. But the memory efficiency is not actually tracked or logged as far as I know. 

We must implement that, especially if we slightly pivot the experiment and align them with one of our main premisises (8 GB RAM), then we must logg and record the training time, memory usage etc.

## [26] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.3 Research Questions
- **Date:** 2026-09-01T15:10:00
- **On:** “, observability and traceability of tool calls,”

This oversvability and traceability I am unsure of whether it was implemented well at this point

## [27] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.3 Research Questions
- **Date:** 2026-09-01T15:21:00
- **On:** “SRQ4: To what extent does giving an agentic decision-support system access to dedicated lightweight forecasting models improve the correctness, consistency, and replicability of forecast-informed decision-support outputs, at justified cost and latency, relative to the same system with only data access and code execution (a code-as-action baseline), and does that improvement hold in a production ag”

Not sure if it is alright to have such a long sub research question to be honest. But the content is quite good

## [28] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.3 Research Questions
- **Date:** 2026-09-01T16:11:00
- **On:** “thesis repository”

Unsure whether we will actually provide the whole thesis repository via Git. We must be careful to not showcase any CLAUDE artifacts, or showcase that we used AI to write the code. Further we cant share any propriatory infromation from Manifold (e.g. the nielsen dataset, database credentials etc.)

That said, we might be able to create a new „clean“ repository which has neither of them, or just placeholders instead. A repo that we can provide the reviewers with, while at the same time dodging AI or confidentiality scandals.

## [30] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.4 Delimitation
- **Date:** 2026-09-01T16:14:00
- **On:** “which allows the benchmark to test whether the modelling findings generalise across heterogeneous category structures.”

A good claim, we must verify and showcase that in our code however. Currently we are planning to include this in the experiment design. But this is up for verification.

## [31] Brian Rohde — Chapter 1 - Introduction

- **Section:** Chapter 1 - Introduction > 1.4 Delimitation
- **Date:** 2026-09-01T16:15:00
- **On:** “The categories differ in capability as well as in size: promotional measures are reported for CSD and energidrikke but not for danskvand or RTD, a structural property of the Danish market as Nielsen measures it rather than a limitation of the data extract.”

This is decent, but we are kind of already teasing at infromation that should be part of dedicated sections. 

In this instance, it hints at the EDA process results. Which is fine, but should be discusssed in mroe detail in the EDA sections. 

In general I feel like it is good to raise some hints in the introduction, but we should also raise the fact that these things will be discussed in more depth, and in which chapter -> pointing towards it
