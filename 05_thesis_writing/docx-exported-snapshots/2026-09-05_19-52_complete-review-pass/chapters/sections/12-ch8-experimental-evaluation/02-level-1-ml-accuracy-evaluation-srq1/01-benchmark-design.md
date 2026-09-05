# Benchmark design

> Section of **Experimental Evaluation > Level 1 - ML accuracy evaluation (SRQ1) > Benchmark design**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/12-ch8-experimental-evaluation/02-level-1-ml-accuracy-evaluation-srq1/01-benchmark-design.md`

---

Dataset: Nielsen CSD panel data, [N] SKUs × 28 retailers × [T] weeks
Stratification: evaluate separately by product category (regular CSD, diet, energy) and retailer tier (major chain, discount, convenience)
Test period: hold-out test set, [T_test] weeks (minimum 13 weeks - one quarter)
