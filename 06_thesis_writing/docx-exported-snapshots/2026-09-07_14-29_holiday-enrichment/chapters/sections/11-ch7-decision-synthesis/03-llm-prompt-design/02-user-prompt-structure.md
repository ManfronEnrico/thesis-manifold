# User prompt structure

> Section of **Context-Aware Decision Synthesis > LLM prompt design > User prompt structure**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- PROSE, FORMATTING, OUTDATED, INCORRECT, APPENDIX. Detail: `comments/sections/11-ch7-decision-synthesis/03-llm-prompt-design/02-user-prompt-structure.md`

---

PRODUCT: {product_name} | RETAILER: {retailer_name} | WEEK: {target_week}



ENSEMBLE FORECAST: {point_forecast} units (90% interval: {lower} – {upper})

CONFIDENCE: {score}/100 ({tier}) - based on {inter_model_spread} model agreement, {calibration_quality} calibration

HISTORICAL: Last 4 weeks actuals: {actuals_list}



Generate a recommendation.
