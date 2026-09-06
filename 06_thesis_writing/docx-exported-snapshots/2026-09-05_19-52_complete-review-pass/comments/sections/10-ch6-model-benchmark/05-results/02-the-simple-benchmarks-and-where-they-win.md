# Comments -- The simple benchmarks, and where they win

> Objections on **Model Benchmark & Selection > Results > The simple benchmarks, and where they win**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/05-results/02-the-simple-benchmarks-and-where-they-win.md`
>
> 4 comment(s) in 4 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
4 comment(s) in 4 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [285](#c285) | The simple benchmarks, and where they win | METACOMMENT, PROSE |  | METACOMMENT, PROSE... |
| [287](#c287) | The simple benchmarks, and where they win | VERIFY, NAMING |  | NAMING & VERIFY: Also wth is „Best tuned ML“?! Which one does it refer to? It do... |
| [288](#c288) | The simple benchmarks, and where they win | VERIFY, PROSE |  | VERIFY, PROSE... |
| [289](#c289) | The simple benchmarks, and where they win | VERIFY, SOURCE, PROSE |  | VERIFY, SOURCE, PROSE... |

---

<a id="c285"></a>

## [285] Brian Rohde -- Model Benchmark & Selection  `METACOMMENT * PROSE`

- **Section:** Model Benchmark & Selection > Results > The simple benchmarks, and where they win
- **Date:** 2026-09-05T16:02:00
- **On:** “The four benchmarks of §6.2.0 were run on the same test rows. stat_baselines.csv.”

METACOMMENT, PROSE

<a id="c287"></a>

## [287] Brian Rohde -- Model Benchmark & Selection  `VERIFY * NAMING`

- **Section:** Model Benchmark & Selection > Results > The simple benchmarks, and where they win
- **Date:** 2026-09-05T16:07:00
- **On:** “Table 13 - Four Categories x 5 Model Performance”

NAMING & VERIFY:


Also wth is „Best tuned ML“?! Which one does it refer to? It doesnt seem like its jsut a focus column from the named approaches / models.

<a id="c288"></a>

## [288] Brian Rohde -- Model Benchmark & Selection  `VERIFY * PROSE`

- **Section:** Model Benchmark & Selection > Results > The simple benchmarks, and where they win
- **Date:** 2026-09-05T16:09:00
- **On:** “Two categories are not won by the tuned models, and this is the most important result in the section.On RTD, seasonal naive beats every tuned configuration - 27.3% against 31.8–36.1%. The most irregular category is the one where a method with no parameters wins.On danskvand, a plain Ridge regression reaches 10.9%, roughly half the tuned gradient-boosted error. danskvand is also the smallest panel (29 series, 174 test rows), where a high-capacity model has least to learn from.This is precisely the outcome the benchmark rung exists to detect. Hyndman and Athanasopoulos (2021, §5.2) recommend the simple methods as a standard against which any new method must justify itself; here they are not a formality but a live constraint, and reporting a headline ML number without them would have concealed that the thesis’s approach is beaten outright on half the categories.”

VERIFY, PROSE

<a id="c289"></a>

## [289] Brian Rohde -- Model Benchmark & Selection  `VERIFY * SOURCE * PROSE`

- **Section:** Model Benchmark & Selection > Results > The simple benchmarks, and where they win
- **Date:** 2026-09-05T16:09:00
- **On:** “Prophet is applied outside its design regime and its numbers should not be read as a defect of the method. Taylor and Letham (2018) target daily business series with multiple seasonalities and holiday effects; at month grain, weekly seasonality does not exist, no holiday calendar is supplied, and yearly seasonality reduces to about twelve observations. Fitting a linear trend on log-transformed short series lets the trend extrapolate to extreme values on back-transformation, producing the 105.7% and 972.4% figures. This is a limitation of the application, not of Prophet, and is reported as such.Ridge requires clipping to be reportable. Unclipped, its energidrikke WMAPE is 2.8×10¹³ and its RTD WMAPE 2459%, because back-transformed linear extrapolation diverges. The clipped variant is what appears above; the raw values are retained in stat_baselines.csv because the instability is itself informative about linear models on this panel.”

VERIFY, SOURCE, PROSE
