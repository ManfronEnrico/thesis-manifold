# Validation scheme

> Section of **Model Benchmark & Selection > Experimental setup > Validation scheme**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- OUTDATED. Detail: `comments/sections/10-ch6-model-benchmark/03-experimental-setup/04-validation-scheme.md`

---

Hyperparameters are selected by **4-fold expanding-window (rolling-origin) cross-validation**, splitting on distinct **periods** rather than rows - the rows are brand-months, so a row-wise split would place the same month in training and validation for different brands. The training window grows forward and validation is the block immediately following it, so no model ever sees a period later than the one it predicts. The test split is untouched throughout.
Rolling-origin evaluation successively advances the forecast origin instead of relying on a single split, which is vulnerable to “corruption by occurrences unique to that origin” (Tashman, 2000, p. 439). Because each fold refits from scratch, this is **recalibration** rather than mere updating - Tashman’s preferred procedure (p. 440).
