Activate the **Thesis Writing Agent** for the CBS Master Thesis project.

## Instructions

The user has invoked `/write-section` with the chapter ID: **$ARGUMENTS**

Follow the **Thesis Writing Agent** workflow exactly as defined in `.claude/agents/thesis-writer.md`.

If no chapter ID was provided ($ARGUMENTS is empty), list the available chapter IDs and ask the user which section to write:

```
Available chapter IDs:
  frontpage          — Front page (CBS required fields)
  abstract           — Abstract (max 1 page)
  ai-declaration     — AI use declaration
  ch1-introduction   — Chapter 1: Introduction
  ch2-literature-review — Chapter 2: Literature Review
  ch3-methodology    — Chapter 3: Methodology
  ch4-data-assessment — Chapter 4: Data Assessment
  ch5-framework-design — Chapter 5: Framework Design
  ch6-model-benchmark — Chapter 6: Model Benchmark (SRQ1)
  ch7-synthesis       — Chapter 7: Synthesis Module (SRQ2)
  ch8-evaluation      — Chapter 8: Evaluation (SRQ3/SRQ4)
  ch9-discussion      — Chapter 9: Discussion
  ch10-conclusion     — Chapter 10: Conclusion
```

## Reminder of the mandatory sequence

1. **READ** the bullet file → confirm status is `bullets_approved`
2. **GENERATE** prose draft → show in chat with char count estimate
3. **COMPLIANCE CHECK** → run all CBS checks, fix issues, re-check if needed
4. **HUMAN APPROVAL GATE** → present draft + compliance report, wait for explicit OK
5. **WRITE TO WORD** → only after approval → update section status in `.md` file

**NEVER skip the compliance check. NEVER write to Word without explicit human approval.**
