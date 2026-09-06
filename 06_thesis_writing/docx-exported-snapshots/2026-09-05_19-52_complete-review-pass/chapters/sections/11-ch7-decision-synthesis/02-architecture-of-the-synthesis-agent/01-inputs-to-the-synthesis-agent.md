# Inputs to the Synthesis Agent

> Section of **Context-Aware Decision Synthesis > Architecture of the Synthesis Agent > Inputs to the Synthesis Agent**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- TABLE-REFERENCE, PROSE, VERIFY, NAMING. Detail: `comments/sections/11-ch7-decision-synthesis/02-architecture-of-the-synthesis-agent/01-inputs-to-the-synthesis-agent.md`

---

| Input | Source | Format |
|---|---|---|
| Model forecasts (5×) | Forecasting Agent | {model_name: {point_forecast, lower_90, upper_90, MAPE_validation}} |
| Historical context | Nielsen data | last_N_periods actuals, seasonality flags |
| Market context | Coordinator prompt | product category, retailer, planning horizon |
**Table** **18** - Inputs to the Synthesis Agent
