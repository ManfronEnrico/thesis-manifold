---
aliases:
learning_text_title: "Design Science in Information Systems Research"
learning_text_venue: MIS Quarterly
learning_text_doi: 10.2307/25148625
learning_text_apa7: "Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly*, *28*(1), 75–105. https://doi.org/10.2307/25148625"
learning_list_authors:
  - Hevner, A. R.
  - March, S. T.
  - Park, J.
  - Ram, S.
learning_list_topic:
  - Design Science Research
  - IS Research Methodology
  - IT Artifacts
  - Behavioral Science vs Design Science
learning_list_srq:
learning_list_chapter:
  - Ch.3
learning_number_release_year: 2004
note_list_type: Regular_Note
note_list_status: complete
note_list_relevance: High
note_list_read_depth: full
tags:
learning_date_read_date: 2026-03-22
cssclasses:
---

# AI Assessment
---
## In one sentence

Hevner et al. establish Design Science as a legitimate and necessary IS research paradigm — complementary to behavioural science — by defining IT artifacts (constructs, models, methods, instantiations) as valid research outputs and providing seven guidelines for conducting, evaluating, and presenting DS research that is simultaneously rigorous and relevant.

## Core Ideas
- IS research requires two complementary paradigms: behavioural science (explaining what is true) and design science (creating what is effective) — neither is sufficient alone
- IT artifacts are classified into four types: constructs (vocabulary), models (abstractions), methods (algorithms/practices), and instantiations (implemented systems) — all are valid DS research outputs
- Seven guidelines for DS research: (1) design as artifact, (2) problem relevance, (3) design evaluation, (4) research contributions, (5) research rigor, (6) design as search process, (7) communication of research
- Knowledge and understanding of a problem domain are achieved through the building and application of the designed artifact itself — not only through prior theory

## Methods
- Conceptual framework development from IS, engineering, and computer science literature
- Demonstration via three exemplar papers from the IS literature evaluated against the seven guidelines
- Analytical argument structure grounded in March and Smith (1995) and Simon (1996)

## Key findings — cite these
- Design science creates artifacts for specific information problems; behavioural science validates and anticipates their impact — both cycles are necessary for complete IS research
- An IT artifact that is not evaluated for utility in an organisational context does not constitute design-science research — evaluation is mandatory, not optional
- "Design-science research is perishable" — rapid technology advances can invalidate results before implementation, a direct challenge for AI system research

## Direct quotes — copy verbatim, include page/section
> "The behavioral-science paradigm seeks to develop and verify theories that explain or predict human or organizational behavior. The design-science paradigm seeks to extend the boundaries of human and organizational capabilities by creating new and innovative artifacts." (Abstract, p. 75)

> "In the design-science paradigm, knowledge and understanding of a problem domain and its solution are achieved in the building and application of the designed artifact." (Abstract, p. 75)

> "The design-science paradigm seeks to create innovations that define the ideas, practices, technical capabilities, and products through which the analysis, design, implementation, management, and use of information systems can be effectively and efficiently accomplished." (p. 76)

> "The dangers of a design-science research paradigm are an overemphasis on the technological artifacts and a failure to maintain an adequate theory base, potentially resulting in well-designed artifacts that are useless in real organizational settings." (Discussion, p. 98)

## SRQ Mapping
- **SRQ1** (forecasting accuracy vs. computational efficiency): N/A
- **SRQ2** (multi-agent coordination and recommendations): N/A
- **SRQ3** (contextual information improving AI capabilities): N/A
- **SRQ4** (predictive AI vs. descriptive BI): N/A — but DSR justifies building and evaluating the entire thesis artifact against a real organisational problem (Manifold AI descriptive→predictive transition)

## Where this goes in our thesis
- **Ch.3, Section 3.1 (Research Paradigm)**: Primary citation establishing DSR as the thesis methodology — the seven guidelines map directly onto our research phases and must be addressed explicitly in the methodology chapter
- **Ch.3**: The four artifact types (constructs, models, methods, instantiations) provide a vocabulary for describing our research outputs — our multi-agent framework is an instantiation; our confidence scoring approach is a method
- **Ch.1 (Problem Statement)**: The behavioural science vs. design science distinction justifies why a system-building thesis is academically valid at CBS — not consulting, but rigorous artifact creation

## What this paper does NOT cover (gap it leaves)

Hevner et al. define DSR at the level of general IS artifacts — they provide no guidance on evaluating AI/ML systems where correctness is probabilistic rather than binary, nor on how to handle computational resource constraints as a formal design criterion, both of which are central to our evaluation framework.

## Strength
- Published in MIS Quarterly — the highest-ranked IS journal (AIS Senior Scholar Basket of Eight), giving this citation maximum methodological authority at CBS
- The seven guidelines are operationalisable and can be directly mapped to each chapter of the thesis, providing a clear review checklist for examiners

## Weaknesses
- Written in 2004 — pre-dates LLM and multi-agent AI systems; the artifact types and evaluation criteria require adaptation for AI pipeline artifacts
- The guidelines assume a relatively stable problem domain; our thesis operates in a rapidly evolving AI landscape where "design-science research is perishable" (their own warning)

## My critical assessment


# Manual Assessment
---
- **Strengths:** Establishes Design Science Research (DSR) as a rigorous and legitimate IS paradigm, with clearly defined artifact types and seven widely adopted evaluation guidelines; provides strong theoretical grounding and academic legitimacy for artifact-centric research like your thesis.
- **Weaknesses:** Conceptual and high-level, offering limited operational guidance for implementing or evaluating complex AI systems; assumes relatively stable evaluation criteria, which is less applicable in fast-evolving, probabilistic AI contexts.
- **Relevance to thesis:** Directly justifies your system-building approach as valid academic research, framing your multi-agent forecasting system as an instantiation artifact and supporting your structured evaluation (accuracy, efficiency, decision quality) as aligned with DSR principles.
- **Gap addressed by your work:** Does not address **evaluation of probabilistic ML outputs, LLM-based reasoning systems, or computational constraints (≤8 GB RAM)**; your thesis extends DSR into a **modern AI setting**, operationalising its guidelines for hybrid ML–LLM decision-support systems in retail analytics.

---

# Additional References
## Parent Note Reference
- [[2026 - Project Note - CMT - CBS Master Thesis - MSc. Data Science]]
## Note References
- [[Peffers et al. (2007) - A Design Science Research Methodology for Information Systems Research]]
## Link References
-
## Physical References
+
## Other References
-
