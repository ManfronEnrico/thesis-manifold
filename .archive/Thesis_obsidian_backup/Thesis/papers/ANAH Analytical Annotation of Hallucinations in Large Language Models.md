
authors: Ji, Z., Gu, Y., Zhang, W., Lyu, C., Lin, D., & Chen, K.

year: 2024

venue: arXiv preprint / Shanghai AI Laboratory

doi:

apa7: >

  Ji, Z., Gu, Y., Zhang, W., Lyu, C., Lin, D., & Chen, K. (2024). ANAH:

  Analytical annotation of hallucinations in large language models.

  *arXiv preprint arXiv:2405.20315*.

  https://arxiv.org/abs/2405.20315

read_date: 2026-03-17

read_depth: full

---

  

## In one sentence

  

ANAH is a bilingual sentence-level hallucination annotation dataset (~12k annotations, ~4.3k LLM responses, 700+ topics) that reveals hallucinations progressively accumulate within a response and that a fine-tuned generative annotator trained on ANAH can match GPT-4-level hallucination detection at lower cost — establishing a taxonomy of hallucination types with direct applicability to LLM-based recommendation systems.

  

## Method

  

Human-in-the-loop annotation pipeline: for each answer sentence, annotators (1) retrieve a reference fragment, (2) classify hallucination type (No Hallucination / Contradictory / Unverifiable / No Fact), (3) provide correction. Dataset: ~12k sentence-level annotations across ~4.3k responses to ~2.2k questions spanning diverse Chinese and English topics. Trained and compared generative vs. discriminative hallucination annotators; evaluated against GPT-3.5, GPT-4, and open-source LLMs.

  

## Key findings — cite these

  

- **Hallucinations progressively accumulate** within a response — later sentences are more likely to contain hallucinations than earlier ones

- Fine-grained generative annotator trained on ANAH achieves **81.01% accuracy**, surpassing all open-source LLMs and GPT-3.5, approaching GPT-4 (86.97%)

- Only GPT-4 performs well on fine-grained hallucination annotation zero-shot — current open-source LLMs fail at this task

- Hallucination types: Contradictory (response contradicts verifiable reference), Unverifiable (claim cannot be grounded in any reference), No Fact (sentence makes no factual claim)

- Breadth of topics matters more than depth of questions for annotator generalisation

  

## Direct quotes — copy verbatim, include page/section

  

> "LLMs still face a worrisome problem that significantly hinders their real-world applications, hallucination, in which they produce plausible-sounding but unfaithful or nonsensical information." (Section 1)

  

> "The hallucinations of LLMs progressively accumulate in the answer." (Abstract)

  

> "The detection of their hallucinations becomes increasingly difficult given the fluency and convincing nature of the responses produced by LLMs." (Section 1)

  

## Where this goes in my thesis

  

- **Ch.2, Section 2.1**: Background reference for LLM reliability limitations — the hallucination accumulation finding directly supports the thesis's design choice to use `temperature=0` and structured prompts in the Synthesis Agent, and to validate outputs via a Validation Agent rather than accepting LLM output at face value

- **Ch.5 (Framework Design)**: ANAH's hallucination taxonomy (Contradictory / Unverifiable / No Fact) provides a conceptual vocabulary for the Validation Agent's Level 2 reliability checks — what does it mean for a retail recommendation to "hallucinate"? (e.g., claiming a promo effect size not present in the data = Contradictory)

- **Ch.9 (Limitations)**: Cite as evidence that hallucination in LLMs is a fundamental unsolved problem, even at GPT-4 level — frames the thesis's inability to fully eliminate this risk as a known limitation of the field, not a framework design failure

  

## What this paper does NOT cover (gap it leaves)

  

ANAH addresses hallucination in knowledge-based generative QA; it does not address hallucination in structured analytical outputs where the LLM is given a formatted context of ML model predictions and must synthesise a recommendation. The risk of a Synthesis Agent hallucinating a causal relationship between consumer signals and sales — given a specific numerical input — is a domain-specific reliability problem unaddressed by any existing benchmark.

  

## My critical assessment

This paper provides a strong conceptual foundation for understanding hallucinations as systematic and classifiable phenomena rather than random errors. Its taxonomy (e.g., Contradictory, Unverifiable) and the finding that hallucinations progressively accumulate within responses directly inform the thesis design choices, justifying the use of a Validation Agent, structured prompting, and deterministic generation settings to mitigate reliability risks.

However, the paper does not address how hallucinations manifest in structured analytical pipelines based on numerical inputs, nor how to operationalise detection and mitigation in domain-specific systems such as retail forecasting. Therefore, while it demonstrates that hallucinations are systematic and manageable, it does not provide guidance on how to handle them in the specific context of the thesis.

  
**