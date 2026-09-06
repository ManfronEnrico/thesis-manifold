# RAM profiling

> Section of **Experimental Evaluation > Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2) > RAM profiling**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE, OUTDATED. Detail: `comments/sections/12-ch8-experimental-evaluation/04-level-3-agent-behaviour-evaluation-srq1-srq2/01-ram-profiling.md`

---

Tool: tracemalloc (Python standard library)
Protocol: profile each agent component separately, then full pipeline end-to-end
Measurement: peak RAM per component, peak total pipeline RAM
Target: total peak ≤4GB (hard constraint)
Report: memory profile table per component (Forecasting Agent × 5 models, Synthesis Agent, Coordinator)
