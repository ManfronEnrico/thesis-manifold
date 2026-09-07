# Synthesis pipeline

> Section of **Context-Aware Decision Synthesis > Architecture of the Synthesis Agent > Synthesis pipeline**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**2 comment(s) on this section** -- VERIFY, SOURCE, PROSE, FORMATTING, MATH, INCORRECT. Detail: `comments/sections/11-ch7-decision-synthesis/02-architecture-of-the-synthesis-agent/02-synthesis-pipeline.md`

---

**Step 1** **-** **Model consensus scoring** - Compute inter-model agreement: std(point_forecasts) / mean(point_forecasts) = relative disagreement metric - High agreement (low spread) → higher base confidence - Assign inverse-MAPE weights to each model’s forecast: w_i = (1/MAPE_i) / Σ(1/MAPE_j) - Weighted ensemble point forecast = Σ(w_i × forecast_i)
**Step 2** **-** **Interval calibration** - Apply Kuleshov et al. (2018) post-hoc calibration to ensemble prediction intervals - Calibration set: validation period actuals vs. stated intervals - Output: calibrated 90% prediction interval with empirically validated coverage
**Step 4** **-** **Confidence score computation** - Composite confidence score (0–100): - 40% weight: calibrated interval width (narrower = higher confidence) - 30% weight: inter-model agreement (lower spread = higher confidence) - Map to 3-tier natural language: High (≥70), Moderate (40–69), Low (<40) - Cite: Kuleshov et al. 2018, Do Forecasts as Prediction Intervals Improve Planning (2010)
**Step 5** **-** **LLM recommendation generation** - LLM (claude-sonnet-4-6 via API) receives structured synthesis context: - Ensemble forecast + calibrated interval - Confidence score + tier - Historical actuals for comparison - LLM generates: 2–3 sentence natural language recommendation + stock action suggestion - Temperature: 0 (deterministic for reproducibility) - Prompt template: stored in agent code, versioned
