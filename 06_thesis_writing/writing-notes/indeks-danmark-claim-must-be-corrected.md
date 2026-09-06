# The abstract claims a dataset we never used

**Status:** OPEN — needs a prose edit in the `.docx`
**Raised:** 2026-09-06 (P0046 F23)
**Severity:** factual claim about method, in the abstract

---

## The problem

Two lines describe Indeks Danmark as part of the empirical base:

> "...deployed on Danish CSD retail data (Nielsen CSD panel + **Indeks Danmark
> consumer survey**)"

> "Single empirical context: Danish CSD retail, Manifold AI / Nielsen CSD panel,
> **Indeks Danmark consumer survey**"

Locations:

- `06_thesis_writing/sections-drafts/abstract.md` — lines 40 and 56
- `docx-exported-snapshots/2026-09-05_19-52_complete-review-pass/` — i.e. the
  claim is **in the authoritative `.docx`**, not just in a draft note

The dataset was never used. It informs no feature, no model, no result. The data
was archived on 2026-09-06 to `.archive/spss_indeksdanmark_2026-09/`, and its
four `PATHS.py` constants were removed — three of them had already been
resolving to directories that did not exist.

## Why this is worth fixing before submission

It is not a stale figure or an outdated number. It is a claim about **what data
the study rests on**, and it is in the section examiners read first and quote
from. A reader who takes it at face value will expect survey-derived features
somewhere in Chapter 4 or 6 and will not find them. If asked at the defence
which variables came from Indeks Danmark, there is no answer that is both honest
and consistent with the abstract as written.

The fix is small, which is the argument for doing it now rather than in the last
48 hours.

## What to change

Reduce the empirical base to what was actually used — the Nielsen CSD panel,
four categories, brand × month. Two options:

1. **Cut the mention.** "...deployed on Danish CSD retail data (Nielsen CSD
   panel)". Cleanest; nothing is lost, because nothing was gained from the
   survey.

2. **Cut it, and reuse it as scope.** Mention in the limitations/future-work
   section that consumer-survey enrichment (Indeks Danmark) was scoped and
   deliberately not pursued. This turns a false claim into an honest boundary
   statement, and it pairs with the exogenous-enrichment discussion in
   [`exogenous-enrichment-and-the-holiday-question.md`](exogenous-enrichment-and-the-holiday-question.md).

Option 2 is better if the limitations section has room: examiners tend to
reward a named, justified exclusion over silence.

## Where the edit goes

**The `.docx`, not the `.md`.** Per
`.claude/rules/writing-surface-authority.md`, prose lives in the OneDrive
document; `sections-drafts/` carries bullets and status only. After editing,
re-run `utility_scripts/scripts/thesis_snapshot.py` so the snapshot mirror
reflects the correction.

**Scope confirmed 2026-09-06:** a sweep of the 2026-09-05 snapshot's chapter
tree found the claim **only in the abstract** (2 occurrences, both listed above).
Chapters 3 and 4 do not mention Indeks Danmark. So the correction is two
sentences in one section, not a cross-chapter edit.

## Related

- `.archive/spss_indeksdanmark_2026-09/README.md` — what was archived and why
- P0046 `findings.md` F23 — the provenance trail
