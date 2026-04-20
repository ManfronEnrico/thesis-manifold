Activate the **Citation Verification** routine for the CBS Master Thesis project.

The user has invoked `/verify-citations` for section: **$ARGUMENTS**

This routine is part of the **Thesis Writing Agent** workflow and uses NotebookLM to verify that every citation in a prose section is accurate — i.e. the cited paper actually makes the claimed argument.

---

## MANDATORY WORKFLOW

### STEP 1 — READ THE SECTION
If a chapter ID was provided in $ARGUMENTS, read the file:
`thesis/writing/sections/{chapter_id}.md`

If no chapter ID was given, ask the user to specify which section to verify, or paste the prose directly.

### STEP 2 — EXTRACT ALL CITATIONS
Parse the text and extract every in-text citation into a list:

Format:
```
[N] (Author, Year) — "claim being made in the prose that cites this paper"
```

Example output:
```
[1] (Makridakis et al., 2020) — "combining models consistently outperforms single best model selection"
[2] (Ma et al., 2025) — "no single model dominates across all demand patterns in beverage FMCG"
[3] (Ng, 2017) — "memory constraints are the primary binding design variable in retail scanner data"
```

Show the full list to the user before proceeding.

### STEP 3 — VERIFY EACH CITATION VIA NOTEBOOKLM

For each citation, run:
```
notebooklm use 48697de0-f0a5-4e66-918e-531abea82c20
notebooklm ask "Does [Author Year] argue that [claim]? Quote the relevant passage if yes."
```

Adapt the query to be specific and falsifiable. Examples:
- "Does Makridakis et al. 2020 show that combining forecasting models outperforms single model selection in the M4 Competition?"
- "Does Ma et al. 2025 find that no single ML model dominates across all demand patterns for beverage data?"
- "Does Ng 2017 state that memory constraints are the primary bottleneck in retail scanner data analysis?"

### STEP 4 — CLASSIFY EACH CITATION

For each citation, assign one of three statuses:

| Status | Meaning |
|---|---|
| ✅ **VERIFIED** | NotebookLM confirms the paper makes the claimed argument (with supporting quote) |
| ⚠️ **IMPRECISE** | Paper is real and related, but the specific claim is overstated, paraphrased incorrectly, or missing nuance |
| ❌ **NOT FOUND** | NotebookLM cannot locate the paper or the specific claim in its sources |

### STEP 5 — REPORT

Produce a verification report:

```
## Citation Verification Report — {chapter_id}
Date: {date}

### Summary
- Total citations: N
- Verified ✅: X
- Imprecise ⚠️: Y  
- Not found ❌: Z

### Detail

[1] (Makridakis et al., 2020) ✅ VERIFIED
    Claim: "combining models consistently outperforms single best model selection"
    Evidence: "NotebookLM response / direct quote from paper"

[2] (Author, Year) ⚠️ IMPRECISE
    Claim: "..."
    Issue: The paper argues X but does not say Y — suggested correction: "..."

[3] (Author, Year) ❌ NOT FOUND
    Claim: "..."
    Action required: [CITATION UNVERIFIED] — replace or remove before submission
```

### STEP 6 — FIX IMPRECISE / NOT FOUND CITATIONS

For each ⚠️ or ❌ citation:
- **IMPRECISE**: suggest a corrected paraphrase that accurately reflects what the paper says
- **NOT FOUND**: mark as `[CITATION UNVERIFIED]` in the prose AND trigger `/find-papers` to locate a valid replacement

### STEP 7 — HUMAN APPROVAL

Show the full report + proposed corrections.
State: "Awaiting your approval before updating the section file."
Only update `thesis/writing/sections/{chapter_id}.md` after explicit user OK.

---

## IMPORTANT RULES

- **NEVER mark a citation as verified based on your own knowledge** — verification must come from NotebookLM querying the actual papers in the notebook
- If NotebookLM says "I don't have this paper", add it as a source first: `notebooklm source add <url_or_path>`, then re-query
- `[CITATION NEEDED]` markers from the Writing Agent are automatically ❌ — trigger `/find-papers` for each one
- A citation is only ✅ if NotebookLM provides a supporting quote or passage, not just confirms the paper exists

---

## NotebookLM notebook ID

`48697de0-f0a5-4e66-918e-531abea82c20`

Always run `notebooklm use 48697de0-f0a5-4e66-918e-531abea82c20` before any query in a new terminal session.
