# Feature engineering

> Section of **Model Benchmark & Selection > Experimental setup > Feature engineering**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/03-experimental-setup/02-feature-engineering.md`

---

**Lags**: t−1, t−2, t−3, t−4, t−8, t−13 months
**Rolling statistics**: 4-month and 13-month mean; 4-month standard deviation
**Calendar**: month, quarter, and a binary peak_month flag derived from the category’s own seasonal profile (months whose mean units exceed the category mean by more than 10%). **No holiday calendar is used**  - the flag is measured from the sales distribution, not from calendar dates
**Promotional**: “promo_intensity” (promotional share of units, clipped to [0,1], lagged one period). **Available for CSD and energidrikke only**  - Nielsen reports no promotional measure for danskvand or RTD, so the feature is omitted rather than zero-filled, since a constant zero would assert that no promotion ran
Missing lag values for short histories are left as NaN (handled natively by the tree models); Ridge receives a zero-fill at fit time
