# Comments -- Forecast stability across seeds

> Objections on **Model Benchmark & Selection > Results > Forecast stability across seeds**
>
> Prose: `chapters/sections/10-ch6-model-benchmark/05-results/09-forecast-stability-across-seeds.md`
>
> 5 comment(s) in 5 thread(s).

Extracted 2026-09-05 from `thesis_full.docx`.
5 comment(s) in 5 thread(s). Resolved status available.

> **Read-only extract.** Reply in Word, not here -- this file is regenerated on every snapshot and any edit is lost.

## Index

| # | section | tags | replies | opens with |
|---|---|---|---:|---|
| [312](#c312) | Forecast stability across seeds | VERIFY, METACOMMENT, PROSE |  | METACOMMENT, PROSE, VERIFY... |
| [313](#c313) | Forecast stability across seeds | METACOMMENT, WATERMARK, ACADEMIC |  | WATERMARK, METACOMMENT, ACADEMIC... |
| [314](#c314) | Forecast stability across seeds | VERIFY, TABLE-REFERENCE |  | VERIFY, TABLE REFERENCE... |
| [316](#c316) | Forecast stability across seeds | VERIFY, METACOMMENT, NAMING |  | METACOMMENT, VERIFY, NAMING... |
| [317](#c317) | Forecast stability across seeds | WATERMARK, ACADEMIC |  | ACADEMIC, WATERMARK... |

---

<a id="c312"></a>

## [312] Brian Rohde -- Model Benchmark & Selection  `VERIFY * METACOMMENT * PROSE`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:23:00
- **On:** “Chapter 2 motivates evaluating the modelling substrate on accuracy, computational efficiency and stability, and SRQ1’s scope names stability as its fourth axis. This section supplies that measurement, which had not previously been made.Stability is measured as the coefficient of variation of the forecast for each (brand, month) cell across five random seeds, with data, splits, features and protocol held identical. Only the seed varies, driving Optuna’s sampler and the models’ own stochastic elements.”

METACOMMENT, PROSE, VERIFY

<a id="c313"></a>

## [313] Brian Rohde -- Model Benchmark & Selection  `METACOMMENT * WATERMARK * ACADEMIC`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:24:00
- **On:** “Two findings, and both matter more than the accuracy tables suggest.”

WATERMARK, METACOMMENT, ACADEMIC

<a id="c314"></a>

## [314] Brian Rohde -- Model Benchmark & Selection  `VERIFY * TABLE-REFERENCE`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:26:00
- **On:** “First, aggregate stability flatters the system by roughly three times. Aggregate WMAPE moves by about 4.7% of its own level across seeds, while the typical individual forecast moves by about 13%, and the ninetieth-percentile cell by 30–73%. Per-cell movements partly cancel within a volume-weighted sum, so a planner reading one brand’s number experiences considerably more run-to-run variability than a headline metric implies. Both figures are therefore reported; quoting only the aggregate would understate instability threefold.”

VERIFY, TABLE REFERENCE

<a id="c316"></a>

## [316] Brian Rohde -- Model Benchmark & Selection  `VERIFY * METACOMMENT * NAMING`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:27:00
- **On:** “Table 16 - Seed Stabiltiy across Models and Categories”

METACOMMENT, VERIFY, NAMING

<a id="c317"></a>

## [317] Brian Rohde -- Model Benchmark & Selection  `WATERMARK * ACADEMIC`

- **Section:** Model Benchmark & Selection > Results > Forecast stability across seeds
- **Date:** 2026-09-05T16:26:00
- **On:** “Every input is identical; only the random seed differs. A per-category statement of which gradient-boosting model is best is therefore not a finding - it reports the outcome of one seed. §6.6 states the conclusion this supports instead.”

ACADEMIC, WATERMARK
