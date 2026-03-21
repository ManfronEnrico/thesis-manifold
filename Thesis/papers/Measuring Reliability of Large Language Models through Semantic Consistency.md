
authors: Raj, H., Rosati, D., & Majumdar, S.

year: 2022

venue: ML Safety Workshop, NeurIPS 2022

doi:

apa7: >

  Raj, H., Rosati, D., & Majumdar, S. (2022). Measuring reliability of large

  language models through semantic consistency. *ML Safety Workshop,

  36th Conference on Neural Information Processing Systems (NeurIPS 2022)*.

  https://arxiv.org/abs/2211.05853

read_date: 2026-03-17

read_depth: full

---

  

## In one sentence

  

A semantic consistency framework for LLMs — measuring whether semantically equivalent prompts produce semantically equivalent outputs using paraphrase detection and entailment as agreement functions — reveals that consistency and accuracy are orthogonal properties, greedy decoding is substantially more consistent than sampling, and larger models are more consistent but not more accurate.

  

## Method

  

Evaluated OPT models (125M–2.7B parameters) and GPT-3 (175B) on TruthfulQA with 3,962 paraphrased questions (8,956 total before filtering). Four semantic agreement functions: BERTScore (BERTs), paraphrase detection (PP), entailment, contradiction — compared against lexical baselines (ROUGE-1, NER overlap). Human annotation study on 100 questions (903 answer pairs); Fleiss' κ = 0.84.

  

## Key findings — cite these

  

- **Greedy decoding is substantially more consistent** than sampling-based decoding; sampling introduces randomness that degrades consistency independently of factuality

- **Consistency and accuracy are orthogonal** (not correlated) — measuring accuracy alone is insufficient to guarantee reliable LLM outputs

- Larger models are more consistent but not more accurate (inverse scaling on TruthfulQA for accuracy)

- Entailment-based and paraphrase-based semantic consistency metrics correlate most strongly with human judgements (Spearman ρ: Entail = 0.70, PP = 0.52 vs. lexical: R1-C = 0.32)

- BERTScore alone is insufficient — entailment captures directional semantic equivalence that BERTScore misses

  

## Direct quotes — copy verbatim, include page/section

  

> "Without this property [consistency], we cannot ensure the safety of PLMs since we won't be certain about the outputs of models under inputs that are semantically equivalent to seen examples." (Section 1)

  

> "The biggest contributor to inconsistency is the decoding method. Greedy approaches to decoding are much more consistent than a sampling-based approach." (Section 3 / findings)

  

> "Consistency and accuracy are not correlated and seem to reflect orthogonal properties." (Section 3 / findings)

  

## Where this goes in my thesis

  

- **Ch.5 (Framework Design)**: The greedy decoding finding directly and explicitly justifies `temperature=0` in the Synthesis Agent's Claude API call — cite this paper as the empirical basis for that design decision rather than stating it as intuition

- **Ch.6 (Validation Framework — Level 2)**: The orthogonality finding means the thesis cannot use MAPE alone to validate the Synthesis Agent's recommendation quality; a separate consistency evaluation (does the same input → same recommendation across multiple runs?) is needed; this paper provides the theoretical grounding and a usable metric framework for that evaluation

- **Ch.2, Section 2.1**: Background on LLM reliability limitations — extend the hallucination discussion to the consistency dimension; two independent reliability failure modes (hallucination + inconsistency) must both be addressed in the validation framework

  

## What this paper does NOT cover (gap it leaves)

  

The framework evaluates consistency on open-domain QA (TruthfulQA); it does not address consistency of structured analytical recommendations generated from numerical model outputs, where the input is a formatted context of forecasts and the output is a managerial decision narrative. Whether semantic consistency degrades in domain-specific, quantitatively-grounded generation tasks — where both the prompt and expected output are highly constrained — remains untested.

  

## My critical assessment  
This paper is cool because it shows that reliability in LLMs is not just about being correct, but about being consistently correct across equivalent inputs — fundamentally changing how we evaluate and trust model outputs

**