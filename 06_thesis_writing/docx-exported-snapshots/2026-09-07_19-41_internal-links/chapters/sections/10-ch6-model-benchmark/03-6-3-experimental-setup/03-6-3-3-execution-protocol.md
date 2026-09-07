# 6.3.3 Execution protocol

> Section of **Chapter 6 | Model Benchmark & Selection > 6.3 Experimental setup > 6.3.3 Execution protocol**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, SOURCE, PROSE. Detail: `comments/sections/10-ch6-model-benchmark/03-6-3-experimental-setup/03-6-3-3-execution-protocol.md`

---

Sequential execution: load → fit → predict → unload → gc.collect()
Memory profiling via tracemalloc at each stage; peak RAM recorded per model
Fixed seed (42) throughout; seed sensitivity is measured separately (§6.5)
