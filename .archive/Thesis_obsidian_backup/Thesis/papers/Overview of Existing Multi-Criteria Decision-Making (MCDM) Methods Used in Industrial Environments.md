
authors: Avramova, T., Peneva, T., & Ivanov, A.

year: 2025

venue: Technologies (MDPI), Vol. 13, No. 10, Article 444

doi: 10.3390/technologies13100444

apa7: >

  Avramova, T., Peneva, T., & Ivanov, A. (2025). Overview of existing

  multi-criteria decision-making (MCDM) methods used in industrial environments.

  *Technologies*, *13*(10), 444. https://doi.org/10.3390/technologies13100444

read_date: 2026-03-17

read_depth: full

---

  

## In one sentence

  

A structured review of the main MCDM methods used in manufacturing (AHP, ANP, FUCOM, TOPSIS, VIKOR, BWM, SAW) covering their strengths, limitations, and situational applicability, concluding that no single method fits all contexts and that hybrid MCDM approaches — particularly integrating AI and IoT — represent the frontier for real-time industrial decision support.

  

## Method

  

Structured literature and patent review of over 200 sources from Scopus, Web of Science, and Google Scholar. Focuses on manufacturing and process engineering applications. Three-step analysis: (1) existing situation overview, (2) comparative method analysis, (3) challenges and future directions. Special attention to FUCOM applicability.

  

## Key findings — cite these

  

- **TOPSIS**: best for rapid ranking of many alternatives on quantitative metrics (e.g., supplier evaluation, energy options) — "high speed and intuitive interpretation of results"

- **AHP**: best for hierarchical problems with expert input and multiple sub-objectives; strongest transparency and consistency control

- **FUCOM**: reliable criteria weights with minimal expert comparisons; suitable for automated systems and strategic planning under time constraints

- **ANP**: recommended when significant correlations exist between criteria

- "There is not a single approach that works for all situations" — method selection must be context-driven

- Hybrid MCDM (combining multiple methods) is the emerging standard for overcoming individual method limitations

- AI and IoT integration identified as the key future direction for real-time MCDM systems

  

## Direct quotes — copy verbatim, include page/section

  

> "MCDM methods evaluate, rank and assign importance to set criteria; in this way they provide a reliable and structured approach to solving a specific problem or task." (Section 1)

  

> "Choosing the right MCDM method and implementing them properly in a particular situation or case is of major importance since it can result in an apparent boost in efficiency, optimization of resources used, cost reduction and improvement in general process efficiency." (Section 5)

  

> "There is not a single approach that works for all situations, and that variety can be both a strength and a challenge." (Section 5)

  

## Where this goes in my thesis

  

- **Ch.2, Section 2.4**: Background reference establishing the MCDM landscape — use to introduce the AHP/TOPSIS/VIKOR vocabulary before explaining why the thesis adopts a simplified weighted scoring approach in the Synthesis Agent rather than a full MCDM implementation; cite the "no single method fits all" conclusion as justification for the pragmatic composite confidence score design

- **Ch.5 (Framework Design)**: The TOPSIS characterisation ("high speed, quantitative metrics, intuitive interpretation") supports the Synthesis Agent's design rationale — for automated, real-time retail recommendation generation, computation speed and interpretability outweigh the precision of full AHP hierarchy construction

- **Ch.9 (Limitations)**: The paper's conclusion that "expert judgment is needed for criteria selection" is a known limitation in MCDM — the thesis's fixed weights (0.40/0.30/0.30) are a pragmatic heuristic, not an empirically calibrated AHP matrix; acknowledge this gap

  

## What this paper does NOT cover (gap it leaves)

  

The review covers MCDM in tangible manufacturing decisions (machine selection, process optimisation) with deterministic criteria; it does not address MCDM integration with probabilistic forecasting outputs, LLM-generated synthesis, or the challenge of weighting heterogeneous data signals (ML accuracy, inter-model agreement, consumer survey data) in a single confidence score for retail business recommendations.

  

## My critical assessment

  

Provides a comprehensive and well-structured overview of major MCDM methods, clarifying their strengths, limitations, and situational applicability  
  

Reinforces the key insight that no single decision-making method is universally optimal, supporting the thesis’s choice of a pragmatic, context-driven aggregation approach  
  

Highlights the importance of interpretability and computational efficiency, which aligns with the thesis’s design priorities for real-time recommendation systems  
  

Supports the relevance of hybrid decision-making approaches, conceptually aligning with the thesis’s combination of ML outputs and weighted scoring  
  

However, as a review paper, it does not provide empirical validation or concrete implementation guidance for integrating MCDM into automated systems  
  

Focuses on deterministic, industrial decision contexts and does not address probabilistic forecasting outputs or heterogeneous data fusion  
  

Does not consider LLM-based systems, multi-agent orchestration, or the generation of natural language recommendations  
  

Therefore, useful for conceptual grounding and justification of decision-making design choices, but limited in direct applicability to the technical implementation of the thesis framework

  
**