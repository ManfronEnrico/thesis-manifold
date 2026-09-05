# Simple benchmarks

> Section of **Model Benchmark & Selection > Model descriptions > Simple benchmarks**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/02-model-descriptions/01-simple-benchmarks.md`

---

Four parameter-free methods, defined as in Hyndman & Athanasopoulos (2021, §5.2):
| Method | Forecast for horizon *h* |
|---|---|
| Mean | ŷ(T+h) = ȳ |
| Naive | ŷ(T+h) = y(T) |
| Seasonal naive | ŷ(T+h) = y(T+h−m(k+1)), with *m* the seasonal period and *k* = ⌊(h−1)/m⌋ |
| Drift | ŷ(T+h) = y(T) + h · (y(T) − y(1)) / (T−1) |
**Table** **8** - Simple Benchmark Evaluation Parameters
**Seasonal naive is the decisive one for this panel.** Monthly beverage demand has strong annual seasonality, which seasonal naive exploits with zero parameters. It is the direct test of whether a tuned model has learned seasonality or merely fitted it
