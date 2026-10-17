---
name: 2026-10-17_scenario-heatmap-notes
description: REFERENCE - Speaker notes for the seven-slide scenario heatmap build (row reveal), paste-ready in the four-block layout.
category: reference
applies-to: [oral defence, slide deck, speaker notes]
triggers: [speaker notes, scenario heatmap, experiment slides]
created: 2026_10_17-18_30
updated: 2026_10_17-18_30
---

# Speaker notes: scenario heatmap build (7 slides)

These replace the notes for the old four-slide table build (slides 20–23). The new build
is seven slides, so every slide after it moves down by three.

| Slide in build | Image | What lights up |
|---|---|---|
| 1 | `defence_scenario_heatmap_1.svg` | nothing: plain table |
| 2 | `defence_scenario_heatmap_2.svg` | Usable answers |
| 3 | `defence_scenario_heatmap_3.svg` | Median + Mean APE |
| 4 | `defence_scenario_heatmap_4.svg` | Variation + Identical on repeat |
| 5 | `defence_scenario_heatmap_5.svg` | Cost per answer |
| 6 | `defence_scenario_heatmap_6.svg` | Latency |
| 7 | `defence_scenario_heatmap_7.svg` | Everything, with the cells to look at outlined |

The images are in `05_thesis_results/08_experimental_evaluation/figures/`. Every number below
comes from `22_scenario_comparison.csv`. Ratios are rounded: 0.4667 / 0.0091 ≈ 51×,
123.8 / 6.0 ≈ 21×, 0.7664 / 0.0091 ≈ 84×, 111.3 / 6.0 ≈ 19×.

---

## Build slide 1: plain table

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Seven scenarios, one ladder: each column adds one thing to the one before.

A gets nothing: the language model on its own. B gets the sales data and writes its own analysis code. C gets our forecasting model as a tool. F gets all three.

Right of the line: the same three set-ups inside Manifold's production platform, Prometheus. They're drawn lighter because they confirm the left side; the left side is what anyone can rerun.

Three brands, three repeats each: 63 runs in total.

We'll go through it one row at a time.

---

Content in Plain English

The same forecasting question, asked seven different ways. We check how often each way answers, how right it is, whether it says the same thing twice, what it costs and how long it takes.

---

Practice Notes:

Point at the Receives row: the colours pair B with D, C with E, and F with G.

No numbers yet. About 20 seconds.

ONLY IF ASKED about "Runs in": all seven use the same model, GPT-5.5. Prometheus is GPT-5.5 inside Manifold's harness.
```

---

## Build slide 2: usable answers

```text
Final Speaker Notes:



---

What can be said (Suggestions):

First question: does it answer at all?

Without data, A gave a usable forecast in only 6 of 9 runs.

Every scenario with access to data answered all 9.

---

Content in Plain English

With nothing to go on, the AI sometimes can't give a usable answer. As soon as it has data, it always can.

---

Practice Notes:

One sentence, then click. About 10 seconds.

Point at A's red cell only.
```

---

## Build slide 3: accuracy (median and mean)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Accuracy: the axis everyone usually reports.

Without data the model invents numbers: 502% median error.

Data access is the biggest step on the whole ladder: from 502% to 2.9% for the code agent.

After that it's a split decision. The code agents win the typical question: B at 2.9%, D at 0.9% median error.

But on average our model wins: 13.1% mean error, against 27.9% for B and 25.0% for D.

So the code agent is usually very close, but when it misses, it misses badly. Our model is steadier.

---

Content in Plain English

Giving the AI data makes it far more accurate. After that, the AI writing its own code is closer on a typical question, but our model makes fewer big mistakes.

---

Practice Notes:

Point at A first (502%), then B's median, then C's mean.

Say the median result yourself, before an examiner points it out. Owning it reads as a finding; being caught reads as a weakness.

"Typical question" = median; "on average" = mean. Use the plain words, not the abbreviations.
```

---

## Build slide 4: replicability (variation and identical on repeat)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Replicability: ask the same question twice, do you get the same answer?

With our model, yes, every time: 100% identical, 0% variation, on both platforms.

The code agents: never. 0% identical, in both orchestrators.

Combining everything (F, G) lands in between: identical a third of the time, because the agents depart from our forecast and invent their own weighting. (Ch8; Ch9)

---

Content in Plain English

Ask our system twice and it gives the same answer. Ask the AI that writes its own code twice and it gives two different answers.

---

Practice Notes:

This is the first click where the contrast is clear. Slow down here.

Point at C's green column against B's red.

The line people remember: "never the same answer twice".
```

---

## Build slide 5: cost

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Cost per answer.

Our model: under one cent ($0.009). The code agent: $0.47. About fifty times more.

Only the scenarios with our model are cheaper than asking the language model with no data at all.

Combining everything doesn't save money: F and G cost about as much as the code agent.

---

Content in Plain English

Our approach costs a fraction of a cent per answer. Letting the AI write its own code costs about fifty times more.

---

Practice Notes:

Point at C's green cell, then B.

If asked about E ($0.20) being dearer than C: the production platform sends far more context per request (about 30,000 tokens per answer against about 1,200 for C), but it's still the cheapest option on that side.

ONLY IF ASKED about D: $0.77, about 84 times the cost of C.
```

---

## Build slide 6: latency

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Latency: how long until the answer arrives.

Our model: 6 seconds. The code agent: just over two minutes (123.8 s). About twenty times slower.

Again, only the scenarios with our model are faster than the language model on its own.

---

Content in Plain English

Our system answers in seconds. The AI writing its own code takes about two minutes.

---

Practice Notes:

Short. Point at C, then B.

ONLY IF ASKED about D: 111.3 s, about 19 times slower than C.
```

---

## Build slide 7: conclusion (outlined cells)

```text
Final Speaker Notes:



---

What can be said (Suggestions):

Now step back and look at the whole table.

Our model, outlined in C and E: best on five of seven rows. Lowest mean error, identical every time, about fifty times cheaper, about twenty times faster.

The code agents, outlined on the median: best on the typical question.

And the pattern is the same on both sides of the line: in our orchestrator and on Manifold's production platform.

No column wins every row. The code agent wins on the axis usually reported, and loses on the three that usually aren't. (Ch9 §9.2.3)

---

Content in Plain English

Our model isn't always the closest on a single question, but it's cheap, fast and gives the same answer every time. For a business that has to rely on the number, that's what matters.

---

Practice Notes:

Gesture at the whole table first, then the outlined C column, then the two outlined median cells.

End on the Ch9 line, then pause.

ONLY IF ASKED about D's 0.9% median: it costs about 84 times more than C, is about 19 times slower, and was never identical across repeats.

ONLY IF ASKED why the right side is paler: it's the same set-up on a proprietary platform. It confirms the pattern; the left side is what other researchers can replicate.

Hand-over on the next divider: "That's what we measured. Enrico, what does it mean?"
```
