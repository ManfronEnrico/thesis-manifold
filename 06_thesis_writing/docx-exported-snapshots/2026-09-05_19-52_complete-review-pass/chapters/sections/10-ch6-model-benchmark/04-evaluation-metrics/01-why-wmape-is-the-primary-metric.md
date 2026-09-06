# Why WMAPE is the primary metric

> Section of **Model Benchmark & Selection > Evaluation metrics > Why WMAPE is the primary metric**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/04-evaluation-metrics/01-why-wmape-is-the-primary-metric.md`

---

The choice is not conventional but theoretical. A scoring function determines *which functional of the predictive distribution* an optimal forecast reports (Gneiting, 2011):
absolute-error loss is minimised by the **median** (p. 746);
pointwise absolute *percentage* error is minimised by the **(−1)-median**  - a density reweighted by y⁻¹ - which biases forecasts systematically downward (pp. 746, 752);
WMAPE aggregates absolute errors *before* dividing by total volume, so minimising it over a fixed evaluation sample is equivalent to minimising MAE, and is therefore consistent for the **standard median**.
**This predicts, rather than merely describes, the WMAPE/median-APE divergence reported throughout this chapter.** The two metrics estimate different functionals, so agreement was never to be expected. It also explains why tuning against median APE costs 8–13 pp of WMAPE while buying only 2–3 pp of median APE: that objective targets the (−1)-median and underforecasts, which WMAPE penalises directly.
