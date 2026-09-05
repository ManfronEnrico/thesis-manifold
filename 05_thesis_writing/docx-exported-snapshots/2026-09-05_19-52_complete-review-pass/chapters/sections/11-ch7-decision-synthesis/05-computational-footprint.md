# Computational footprint

> Section of **Context-Aware Decision Synthesis > Computational footprint**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

**1 comment(s) on this section** -- VERIFY, PROSE. Detail: `comments/sections/11-ch7-decision-synthesis/05-computational-footprint.md`

---

LLM API call: ~1–3 seconds per synthesis request; ~500–1000 input tokens; ~100–200 output tokens
No local LLM loaded - API call only; ~0MB additional RAM (vs. ~3–6GB for local Llama/Mistral)
Total synthesis step RAM: <50MB (structured data manipulation + API call)
This is the key architectural decision: using claude-sonnet-4-6 API keeps total RAM under 4GB ceiling
