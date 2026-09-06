# The simple benchmarks, and where they win

> Section of **Model Benchmark & Selection > Results > The simple benchmarks, and where they win**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**4 comment(s) on this section** -- METACOMMENT, PROSE, VERIFY, NAMING, SOURCE. Detail: `comments/sections/10-ch6-model-benchmark/05-results/02-the-simple-benchmarks-and-where-they-win.md`

---

The four benchmarks of §6.2.0 were run on the same test rows. stat_baselines.csv.
| Category | Naive | Seasonal naive | Drift | Ridge | ARIMA | Prophet | Best tuned ML |
|---|---|---|---|---|---|---|---|
| CSD | 42.9% | 19.2% | 47.7% | 19.4% | 21.8% | 105.7% | 14.5% |
| danskvand | 32.5% | 35.9% | 32.0% | 10.9% | 33.5% | 19.5% | 20.5% |
| energidrikke | 18.9% | 23.8% | 17.7% | 18.3% | 19.4% | 972.4% | 13.0% |
| RTD | 89.3% | 27.3% | 95.9% | 40.5% | 53.3% | 66.8% | 31.8% |
**Table** **13** - Four Categories x 5 Model Performance
**Two categories are not won by the tuned models, and this is the most important result in the section.**
**On RTD, seasonal naive beats every tuned configuration**  - 27.3% against 31.8–36.1%. The most irregular category is the one where a method with no parameters wins.
**On danskvand, a plain Ridge regression reaches 10.9%**, roughly half the tuned gradient-boosted error. danskvand is also the smallest panel (29 series, 174 test rows), where a high-capacity model has least to learn from.
This is precisely the outcome the benchmark rung exists to detect. Hyndman and Athanasopoulos (2021, §5.2) recommend the simple methods as a standard against which any new method must justify itself; here they are not a formality but a live constraint, and reporting a headline ML number without them would have concealed that the thesis’s approach is beaten outright on half the categories.
Prophet is applied outside its design regime and its numbers should not be read as a defect of the method. Taylor and Letham (2018) target daily business series with multiple seasonalities and holiday effects; at month grain, weekly seasonality does not exist, no holiday calendar is supplied, and yearly seasonality reduces to about twelve observations. Fitting a linear trend on log-transformed short series lets the trend extrapolate to extreme values on back-transformation, producing the 105.7% and 972.4% figures. This is a limitation of the application, not of Prophet, and is reported as such.
Ridge requires clipping to be reportable. Unclipped, its energidrikke WMAPE is 2.8×10¹³ and its RTD WMAPE 2459%, because back-transformed linear extrapolation diverges. The clipped variant is what appears above; the raw values are retained in stat_baselines.csv because the instability is itself informative about linear models on this panel.
