Activate the **Literature Researcher Agent** for the CBS Master Thesis project.

The user has invoked `/find-papers` with the following search topic: **$ARGUMENTS**

Follow the **Literature Researcher Agent** workflow exactly as defined in `.claude/agents/literature-researcher.md`.

---

## If no topic was provided ($ARGUMENTS is empty)

Ask the user:
1. What specific claim, section, or SRQ needs a paper?
2. Is this a gap identified during writing, or a proactive literature expansion?
3. Is there a `[CITATION NEEDED]` marker in a specific section file?

---

## Quick reference — workflow

```
1. Check existing corpus (docs/literature/papers/ + thesis_state.json)
2. Search NotebookLM:
     notebooklm use 48697de0-f0a5-4e66-918e-531abea82c20
     notebooklm ask "<targeted query>"
3. Supplement with web search if needed
4. Present proposals table (max 5 papers) — WAIT for approval
5. Add to corpus only after explicit human OK
```

**NotebookLM notebook ID**: `48697de0-f0a5-4e66-918e-531abea82c20`

**NEVER add papers to corpus without human approval.**
**NEVER fabricate paper metadata — if DOI is unknown, mark as pending.**
