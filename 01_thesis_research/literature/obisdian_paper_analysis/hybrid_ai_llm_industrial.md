---
title: "Hybrid AI and LLM-Enabled Agent-Based Real-Time Decision Support Architecture for Industrial Batch Processes"
authors: González-Potes, A., Mata-Rivera, M. F., Espinosa-Oviedo, J. A., Castellanos-Velasco, E., Alvarado-Nava, O., & Rodríguez-Reséndiz, J.
year: 2026
venue: AI (MDPI), 7(2), 51
tier: 1 — Core Essential
score: 10
angles: [Multi-Indicator + LLM/Agent, Prediction Quality]
srqs: [SRQ1, SRQ2, SRQ3, SRQ4]
note: CLOSEST PAPER TO THIS THESIS
status: CONTENT WITHDRAWN 2026-08-25 — see warning below
---

> [!DANGER] The previous contents of this note were fabricated. Do not cite from memory of it.
>
> Until 2026-08-25 this note attributed the paper above to **"Fabian Bürger, Josef Pauli
> (et al.), 2024, Engineering Applications of Artificial Intelligence"**, with a ScienceDirect
> URL. **No such paper exists.** The title belongs to González-Potes et al. (2026), published
> in *AI* (MDPI) — a real paper the thesis cites separately.
>
> The note also carried a **fabricated direct quotation**: *"The system reduces CIP process
> duration by 12–18% and chemical consumption by up to 20% relative to experienced human
> operators, while achieving 100% regulatory compliance."* Those figures appear nowhere in
> the real paper and contradict the figures Chapter 1 attributes to it. Its described method
> (a 3-layer symbolic/physics + LSTM architecture) was invented as well: the real system is a
> deterministic rule-based supervisor wrapped by a retrieval-augmented conversational layer
> running a locally hosted Qwen 2.5 7B model.
>
> Verified against the source PDF via NotebookLM. See
> `05_thesis_writing/notebookLM/01-Literature Review/Literature_Review-Section_D-reliability_and_evaluation.md`
> (claim LR-01b).

## What the real paper establishes

Use the source PDF, not this note. Verified findings, from the NotebookLM audit:

- **State specification consistency $\Gamma_s \geq 0.98$** — the rule-based severity label
  matched actual process conditions in >98% of cases. This is a property of the *labelling
  layer*; it is **not** a rate of compliant process operation, which averaged 58% on the
  degraded alkaline stages (CIP 3 was 0% compliant).
- **Median LLM numerical error below 3%** when summarising buffered time-series variables.
- **Architecture**: deterministic supervisory/HMI panel + RAG conversational layer (Qwen 2.5 7B,
  locally hosted).
- **Domain**: clean-in-place batch process at an operating beverage plant.
- **Not addressed** (thesis-author observation, *not* an authors' stated limitation): predictive
  forecasting over historical tabular data; SME resource or cost constraints. The authors' own
  stated limitations are the single-site process scope and the formal verification that
  regulated pharmaceutical manufacturing would require.
