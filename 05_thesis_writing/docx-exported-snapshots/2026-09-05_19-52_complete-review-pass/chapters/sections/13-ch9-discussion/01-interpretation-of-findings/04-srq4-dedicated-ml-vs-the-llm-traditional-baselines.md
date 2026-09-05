# SRQ4: dedicated ML vs the LLM/traditional baselines

> Section of **Discussion > Interpretation of findings > SRQ4: dedicated ML vs the LLM/traditional baselines**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, PROSE, OUTDATED, METACOMMENT. Detail: `comments/sections/13-ch9-discussion/01-interpretation-of-findings/04-srq4-dedicated-ml-vs-the-llm-traditional-baselines.md`

---

Against the **traditional statistical baseline**, dedicated ML (XGBoost) beats ARIMA in three of four categories (by 7.7, 4.3 and 17.2 pp WMAPE for CSD, energidrikke, RTD), with only danskvand better served by an additive Prophet model - so dedicated lightweight ML is, on balance, justified over classical forecasting. The **code-as-action LLM baseline** central to the v4 SRQ4 - an LLM that writes and self-corrects its own forecasting code - was *not* executed: it requires a secure execution sandbox (E2B) that is not configured. This is the principal open piece of the empirical SRQ4 answer and is carried as future work; what the present results establish is the prior, weaker comparison (dedicated ML vs traditional, and LLM synthesis vs template), both favouring the dedicated/structured approach on the decision-relevant dimensions. *Connect to: Humans vs. LLMs (IJF 2024); code-as-action (Wang et al. 2024).*
