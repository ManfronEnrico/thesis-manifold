# Latency profiling

> Section of **Experimental Evaluation > Level 3 - Agent behaviour evaluation (SRQ1 + SRQ2) > Latency profiling**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE, OUTDATED. Detail: `comments/sections/12-ch8-experimental-evaluation/04-level-3-agent-behaviour-evaluation-srq1-srq2/02-latency-profiling.md`

---

Wall-clock time for full pipeline: data load → feature engineering → model training → prediction → synthesis → recommendation
Target: end-to-end ≤5 minutes for single SKU×retailer×week forecast (reasonable for a category manager’s tool)
Separate training latency from inference latency (training once, inference per request)
