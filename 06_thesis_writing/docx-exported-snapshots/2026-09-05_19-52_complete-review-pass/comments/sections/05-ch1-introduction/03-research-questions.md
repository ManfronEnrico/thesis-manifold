# Comments -- Research Questions

> Objections on **Introduction > Research Questions**
>
> Prose: `chapters/sections/05-ch1-introduction/03-research-questions.md`
>
> 11 comment(s) in 5 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
11 comment(s) in 5 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [36](#c36) | Research Questions |  | 2 | We currently have the accuracy, and category specialitation somewhat answered. B... |
| [39](#c39) | Research Questions |  | 2 | This oversvability and traceability I am unsure of whether it was implemented we... |
| [42](#c42) | Research Questions |  |  | Not sure if it is alright to have such a long sub research question to be honest... |
| [43](#c43) | Research Questions |  | 2 | Unsure whether we will actually provide the whole thesis repository via Git. We ... |
| [47](#c47) | Research Questions | OUTDATED |  | INTERNAL REFERENCE, OUTDATED: Must be referred to from in-text. As this is a fig... |

---

<a id="c36"></a>

## [36] Brian Rohde -- Introduction  `thread of 3`

- **Section:** Introduction > Research Questions
- **Date:** 2026-09-01T15:09:00
- **On:** “SRQ1: Which lightweight forecasting models provide the best trade-off between accuracy, memory efficiency, and category specialization for FMCG demand forecasting under computational constraints?”

We currently have the accuracy, and category specialitation somewhat answered. But the memory efficiency is not actually tracked or logged as far as I know. 


We must implement that, especially if we slightly pivot the experiment and align them with one of our main premisises (8 GB RAM), then we must logg and record the training time, memory usage etc.

<a id="c37"></a>

### [37] Guest User -- reply

- **Date:** 2026-09-02T13:50:00

yes, again, let´s have a call to wrap our minds around that

<a id="c38"></a>

### [38] Brian Rohde -- reply

- **Date:** 2026-09-03T14:25:00

This is also resolved, I implemented extensive tracking and logging at every major step. 


Currently we are sitting at 12 auto-regenerated markdown tables that are submission ready for the appendix. Once you pull from main (as soon as I pushed), this is where you find them and can already tell from file name what they are about.04_thesis_results\appendix\01_metric_dictionary.md04_thesis_results\appendix\02_substrate_resource_profile.md04_thesis_results\appendix\03_retraining_cost.md04_thesis_results\appendix\04_sandbox_resource_profile.md04_thesis_results\appendix\05_parameter_drift.md04_thesis_results\appendix\06_statistical_baselines.md04_thesis_results\appendix\07_seed_stability.md04_thesis_results\appendix\08_scenario_comparison.md04_thesis_results\appendix\09_outcome_taxonomy.md04_thesis_results\appendix\10_interval_communication.md04_thesis_results\appendix\11_per_run_record.md04_thesis_results\appendix\12_run_configuration.md

<a id="c39"></a>

## [39] Brian Rohde -- Introduction  `thread of 3`

- **Section:** Introduction > Research Questions
- **Date:** 2026-09-01T15:10:00
- **On:** “, observability and traceability of tool calls,”

This oversvability and traceability I am unsure of whether it was implemented well at this point

<a id="c40"></a>

### [40] Guest User -- reply

- **Date:** 2026-09-02T13:52:00

I do not know actually, maybe is embedded in Manifold´s engine... but not sure.... however I think it is quite an important point the we need to include! Observability and traceability are fundamental for building trust in organisations and enabling AI within processes

<a id="c41"></a>

### [41] Brian Rohde -- reply

- **Date:** 2026-09-03T14:26:00

Answered & Solved in my previous reply

<a id="c42"></a>

## [42] Brian Rohde -- Introduction

- **Section:** Introduction > Research Questions
- **Date:** 2026-09-01T15:21:00
- **On:** “SRQ4: To what extent does giving an agentic decision-support system access to dedicated lightweight forecasting models improve the correctness, consistency, and replicability of forecast-informed decision-support outputs, at justified cost and latency, relative to the same system with only data access and code execution (a code-as-action baseline), and does that improvement hold in a production agentic system as well as in a general-purpose one?”

Not sure if it is alright to have such a long sub research question to be honest. But the content is quite good

<a id="c43"></a>

## [43] Brian Rohde -- Introduction  `thread of 3`

- **Section:** Introduction > Research Questions
- **Date:** 2026-09-01T16:11:00
- **On:** “thesis repository”

Unsure whether we will actually provide the whole thesis repository via Git. We must be careful to not showcase any CLAUDE artifacts, or showcase that we used AI to write the code. Further we cant share any propriatory infromation from Manifold (e.g. the nielsen dataset, database credentials etc.)


That said, we might be able to create a new „clean“ repository which has neither of them, or just placeholders instead. A repo that we can provide the reviewers with, while at the same time dodging AI or confidentiality scandals.

<a id="c44"></a>

### [44] Guest User -- reply

- **Date:** 2026-09-02T13:54:00

I have heard opposite stories regarding that... I think at this point we should act as they will read the code

<a id="c45"></a>

### [45] Brian Rohde -- reply

- **Date:** 2026-09-03T14:30:00

But what do you mean? They can and should read the code. Its jsut that we remove all of the unnecessary bits and pieces (e.g. claude artifacts, writing agents, notes, handover docs, archived files, tests, datasets, propriotary data) and just keep the important stuff (the actual EDA, Modelling, Reporting Code) and have placeholders only where necessary (e.g. Nielsen Dataconnector code can stay, but the connection is „dead“ | similarly with any prometheus related code which can stay, just we insert placeholders disable proprietory accessors)So not really sure what you mean? What did you hear exactly?

<a id="c47"></a>

## [47] Brian Rohde -- Introduction  `OUTDATED`

- **Section:** Introduction > Research Questions
- **Date:** 2026-09-05T18:40:00
- **On:** “Hierarchical Structure of Research Questions (SRQ1–SRQ4).”

INTERNAL REFERENCE, OUTDATED:


Must be referred to from in-text. As this is a figure (image) it incorrectly caputred the 8GB budget instead of the correct 4GB.We might need to re-generate all figures in general.
