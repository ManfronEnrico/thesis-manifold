---
name: ch7-book-citation-for-the-interval-criterion
description: NOTE - Section 5.5 gives Ch7 a source for WHY the interval-communication criterion exists, replacing a first-principles argument.
category: reference
applies-to: [ch7 decision synthesis]
triggers: [ch7 prose pass, defending the interval-communication criterion]
created: 2026_09_13-21_15
updated: 2026_09_13-21_15
source: P0055 book scan. Routed to BRANCH A deliberately - see plans/P0055_*/findings.md F15
---

# Ch7 - one free citation for the interval-communication criterion

**This finding belongs to BRANCH A, not to the Branch B re-engineering work.**
It was found during the P0055 book scan and routed here immediately.

## What the book says

Section 5.5, the opening claim:

> "**point forecasts can be of almost no value without the accompanying
> prediction intervals**"

## Why Ch7 wants it

Ch7 scored an **interval-communication criterion** on 2026-09-13. That criterion
is currently argued from first principles - i.e. the thesis asserts that
communicating uncertainty matters.

**5.5 says it outright, in the standard reference.** The criterion stops being
the thesis's own preference and becomes an operationalisation of a stated
requirement in the field.

## Also in 5.5, if the chapter needs the arithmetic

| | |
|---|---|
| Table 5.1 multipliers | 80% -> **1.28**, 95% -> **1.96** |
| Table 5.2, seasonal naive sd | `sigma * sqrt(k+1)` where `k = floor((h-1)/m)` |

⚠ The Table 5.2 formula is **parameterised by m**, which is a fourth independent
confirmation that m=12 for this panel. That half belongs to Branch B's lag
repair, not to Ch7.
