# Scope and Filtering

> Section of **Data Assessment > CSD - Worked Category (EDA and Parameters) > Scope and Filtering**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/08-ch4-data-assessment/02-csd-worked-category-eda-and-parameters/01-scope-and-filtering.md`

---

**Market scope**: DVH EXCL. HD (single Nielsen market level; see header). 187,907 facts rows fall in scope.
**Span**: 42 monthly periods (Oct 2022–Mar 2026) on Nielsen’s 4-4-5 week calendar. (Period identifiers are not calendar-monotonic, so the span is taken from the documented window, not raw min/max.)
**Brands**: 136 total; the adopted filter MIN_PERIODS ≥ 30 (≥30 non-zero monthly observations) retains **77 brands** and **3,077** brand-month rows (of 3,789 total). A ≥40 filter would retain only 57 and is infeasible for the other three categories (37–39 periods → zero brands), so ≥30 is applied globally (Table 4.1). These figures are recomputed locally under DVH EXCL. HD and **supersede** Brian’s all-markets values (143 → 62 brands; 4,040 rows), inflated by the market double-count.
**Aggregation grain**: brand × month, positive sales only; weighted distribution averaged rather than summed (correct for an ACV metric).
