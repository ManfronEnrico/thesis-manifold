# SRQ2 LLM layer — Synthesis Agent + LLM-as-Judge

N=50 stratified (seed=42). Synthesis: claude-sonnet-4-6 (temp 0). Judge: GPT-4o (temp 0). Likert 1-5 per dimension. Baseline = rule-based template.

| System | accuracy | calibration | actionability | relevance | clarity | mean |
|---|---|---|---|---|---|---|
| LLM | 2.96 | 3.74 | 4.00 | 4.00 | 4.34 | 3.81 |
| baseline | 3.42 | 3.46 | 2.14 | 3.28 | 3.46 | 3.15 |
