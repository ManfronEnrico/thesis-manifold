---
name: launch-the-funded-run
description: STATE - The exact command for the funded SRQ4 MVP, what it costs, what must be true before it runs, and what to check after. Written 2026-09-11 immediately before launch, for a session that may have no conversation history.
pid: P0049
created: 2026_09_11-23_58
updated: 2026_09_11-23_58
status: ready
---

# Launch the funded run

**Everything is ready.** Pre-flight 13/13, Prometheus reachable, seven arms
measured, three brands fixed. The only gate is Brian loading credit.

Brian is loading **$50**. The run estimates **$18-20**.

---

## The command

Run from `04_SRQ4_Scenario_Experiment/scenario_setup` with the thesis venv.

```
python srq4_experiment.py --full --repeats 3 --categories CSD \
  --brand-strategy stratified --scenarios A,B,C,D,E,F,G
```

**No `--brands-per-cat` needed** - as of 2026-09-11 it defaults to None and
stratified resolves to 3. The command prints
`[brands-per-cat not given] --brand-strategy stratified -> (3,)` so the
resolution is visible rather than assumed.

**No `--budget`.** Brian: *"we dont really need a budget cap, because there is
no auto-refill mechanic with api budget, so it can only spend what I load."*
Correct - the account balance is the real cap, and it is hard. The flag still
exists if a future run wants an early stop.

### Verify first, for free

```
python verify_setup.py                    # expect: READY -- 13 check(s) passed
python srq4_experiment.py --full --repeats 3 --categories CSD \
  --brand-strategy stratified --scenarios A,B,C,D,E,F,G --dry-run
```

The dry run must print exactly:

```
SRQ4: 3 brands x 3 repeats x 7 scenarios = 63 requested
      CSD/HARBOE, CSD/7-UP, CSD/ØRBÆK
```

**If it names any other brand, STOP.** Four brands including CARIBIA and
LØGISMOSE means the strategy/count fix has been reverted.

---

## What it costs

| | |
|---|---|
| runs | 63 (3 brands x 3 repeats x 7 arms) |
| estimate | **$18-20** |
| loaded | $50 |

Per arm, 9 runs each. D, E and G are **63% of the spend** - they are the
Prometheus arms.

**The estimate is CONSERVATIVE**, not optimistic. Summing every run on
2026-09-11 gives $4.86 estimated against $4.03 billed org-wide for the whole
day. See the F57 correction: the earlier "1.77x under-report" claim was an
artefact of comparing one run against a whole day of billing.

---

## Three things that must be true at launch

| | check | why it matters |
|---|---|---|
| 1 | **Prometheus is running** | D, E and G are 63% of the cost. If the engine is down they return `engine_unavailable` and the money buys only A, B, C and F. Confirmed up at 23:55 on 2026-09-11. |
| 2 | **The dry run names HARBOE / 7-UP / ØRBÆK** | any other sample is not the design recorded in the writing notes |
| 3 | **Balance is loaded** | the account balance IS the cap; there is no auto-refill |

---

## What to check after it finishes

Beyond the automated checks:

- `sql_calls: []` on **D, E and G** - DEC-D-SNAPSHOT
- `deviates_from_model` on **F and G** - the whole point of the combined arm.
  In the smoke both overrode the model; whether that holds across 9 runs each
  is a finding either way.
- **Within-arm spread**, reported alongside every between-arm gap. At n=3 the
  intervals will overlap. That is expected and is what the limitation says.
- All 63 answers carry Forecast, Range, Confidence, Recommendation, sentinel.
- Reconcile total spend against the account balance, **not** against
  `fetch_billed_cost` - that returns the whole day, org-wide.

---

## What this run can and cannot establish

**Can:** direction. Which arms cluster where, whether the combined arms override
or defer, whether the cost and latency separation holds across brands.

**Cannot:** effect size. Scenario A moved 15 percentage points between two runs
on an identical prompt. At 3 repeats the confidence intervals will overlap
heavily.

**Write it as "B and D were more accurate in this sample", never "B and D are
more accurate".** The limitation is drafted in
`writing-notes/ch8_experiment/the-defensible-conclusion-shape.md`.

---

## If it fails partway

The cache is keyed on (brand, scenario, repeat, schema). **Re-running the same
command resumes** and skips completed cells - it does not re-spend. `--append`
is what adds repeats alongside existing ones; do not use it for a resume.
