# Thesis Structure

> Section of **Introduction > Thesis Structure**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

---

The remainder of this thesis is organised into nine chapters, each corresponding to a distinct phase of the Design Science Research process (Peffers et al., 2007).
**Chapter 2** reviews the literature across eight thematic sections: forecasting as a predictive substrate for FMCG demand; lightweight machine learning under computational and deployment constraints; the transition from descriptive business intelligence to forecast-informed decision-support; LLM agents and tool-mediated reasoning; the reliability, traceability, uncertainty, and evaluation of agentic outputs; production-oriented agentic systems and integration readiness; the research gap; and Design Science Research. This review establishes the theoretical foundations and the gap that the thesis addresses.
**Chapter 3** details the research methodology, grounding the thesis in Design Science Research and specifying the data sources, preprocessing, the forecasting-model benchmark, the structured forecast-tool interface, the integration-readiness assessment, and the evaluation design that compares dedicated-model agentic decision-support against a code-as-action LLM baseline.
**Chapter 4** presents the data assessment, characterising the quality, structure, and forecasting suitability of the Nielsen scanner data across the four beverage categories, and documenting the preprocessing decisions that inform the modelling.
**Chapter 5** describes the predictive-extension architecture: the forecasting substrate, the structured forecast-tool interface, and the bounded tool-using agentic decision-support layer, together with the integration-readiness capabilities, justified against the 8GB RAM budget. The evaluated prototype uses a lightweight Python coordinator; a LangGraph deployment is identified as the production target.
**Chapter 6** addresses SRQ1 through an empirical model benchmark, comparing lightweight forecasting models across the four categories on accuracy, memory efficiency, and stability, and testing category specialisation against pooling.
**Chapter 7** addresses SRQ2, and informs SRQ3, through the agentic extension prototype: the tool-using agent that consumes forecasts and their uncertainty through the structured interface and produces decision-support recommendations.
**Chapter 8** addresses SRQ4 through a pilot evaluation comparing dedicated-model agentic decision-support against a general-purpose code-as-action LLM baseline, on correctness, consistency, and replicability (primary) and cost and latency (secondary).
**Chapter 9** discusses the contributions, the integration-readiness findings, and the limitations of the thesis, including pilot-scale evaluation and designed-but-unevaluated calibration, and identifies directions for future research.
**Chapter 10** concludes by synthesising answers to the four subsidiary research questions and the main research question and reflecting on the broader implications for extending production-oriented agentic decision-support systems with forecasting capabilities under resource constraints.
