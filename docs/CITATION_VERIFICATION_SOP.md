# Citation Verification SOP (Standard Operating Procedure)

**For**: Thesis team (Brian + Enrico)  
**Date**: 2026-04-18  
**Policy**: Academic Integrity First

---

## Overview

When you cite a paper in the thesis, especially using NotebookLM-extracted sources, you **must verify** that the quote is accurate and appears in the original PDF. This SOP ensures 100% citation accuracy before submission.

---

## Citation Trust Levels

Every citation falls into one of these categories:

| Level | Source | Verification | Use Case |
|-------|--------|------|----------|
| **Level 1: Direct PDF** | You read the PDF yourself | PDF page number logged | Primary — always acceptable |
| **Level 2: NotebookLM Verified** | NotebookLM returned quote + page | You checked the PDF | Secondary — acceptable with verification |
| **Level 3: NotebookLM Unverified** | NotebookLM returned quote, not checked | N/A | ❌ **NOT ALLOWED** — must move to Level 2 first |
| **Level 4: Secondary Source** | Another paper cited a source | Not primary source | ❌ **NOT ALLOWED** for thesis — use primary only |

**Rule**: No Level 3 or Level 4 citations in the final thesis.

---

## Workflow: Adding a Citation

### **Path A: Direct PDF (Most Reliable)**

```
Step 1: You're writing Chapter 2
        "The literature shows that agents require reasoning..."

Step 2: Open PDF from Drive: AgentReasoningSmith2024.pdf

Step 3: Find the exact passage
        Page 12: "Agents equipped with reasoning capabilities improve..."

Step 4: Record in thesis draft:
        [Smith et al., 2024, p. 12]
        Citation level: Direct PDF

Step 5: Add to verification log (see section below)
```

**Time**: ~2 minutes per citation  
**Risk**: Very low — you've seen the source  
**Result**: Level 1 citation ✅

---

### **Path B: NotebookLM with Verification (Acceptable)**

```
Step 1: You're writing Chapter 2
        "The literature shows that agents require reasoning..."

Step 2: Unsure if you read this or where to find it
        Ask: /notebooklm-ask ch2-literature "Do the papers discuss agent reasoning?"

Step 3: NotebookLM returns:
        "Yes, according to [1]: 'Agents equipped with reasoning...' (p. 12)"
        Source: Smith et al., 2024

Step 4: Open PDF from Drive: AgentReasoningSmith2024.pdf

Step 5: Verify:
        ✓ Find passage on page 12
        ✓ Quote matches exactly (or paraphrased legitimately)
        ✓ Context is accurate (not cherry-picked)
        ✓ Page number matches NotebookLM

Step 6: Record in thesis draft:
        [Smith et al., 2024, p. 12 — verified via NotebookLM]

Step 7: Add to verification log
```

**Time**: ~5 minutes per citation  
**Risk**: Low — you verified against PDF  
**Result**: Level 2 citation ✅

---

### **Path C: NotebookLM WITHOUT Verification (FORBIDDEN)**

```
Step 1: NotebookLM says: "According to [1]: 'Quote here'"

Step 2: You think: "That sounds right, I'll use it"

Step 3: You cite it in the thesis WITHOUT checking the PDF

🚫 STOP. This is a Level 3 citation. NOT ALLOWED.
    Before submitting, you MUST:
    - Open the PDF
    - Find and verify the quote
    - Move it to Level 2
```

---

## Verification Checklist

**Before you finalize ANY citation from NotebookLM:**

- [ ] I have the PDF open
- [ ] I found the exact passage (or nearest paraphrase)
- [ ] The page number matches NotebookLM's citation
- [ ] The quote is accurate (word-for-word or legitimately paraphrased)
- [ ] The context is preserved (not cherry-picked)
- [ ] I recorded the verification in the log (section below)

**If ANY checkbox fails**: Do not use the citation. Ask NotebookLM for a different source or re-read the paper yourself.

---

## Verification Log

Maintain this file: `docs/literature/verified_citations.md`

**Format**:
```markdown
# Verified Citations Log

## Chapter 2 — Literature Review

### Citation 1: Smith et al. (2024)
- **Claim**: "Agents equipped with reasoning improve performance"
- **Quote**: "Agents equipped with reasoning capabilities improve task completion by X%"
- **Page**: 12
- **Source**: AgentReasoningSmith2024.pdf
- **Verification Method**: Level 2 (NotebookLM + PDF check)
- **Verified By**: Brian
- **Date**: 2026-04-18
- **Status**: ✅ APPROVED

### Citation 2: ...
```

**Add one entry per citation.** This log is your audit trail.

---

## Pre-Submission Audit (Mandatory)

**Before you submit the thesis to CBS, run this audit:**

```bash
# 1. Export all citations from your thesis draft
#    (Your writing tools can generate a citation list)

# 2. Cross-reference against verified_citations.md
#    For each citation in the draft:
#    - Does it appear in verified_citations.md?
#    - Does the page number match?
#    - Is Status = APPROVED?

# 3. Fail cases:
#    - Citation not in log → ERROR (find and verify it)
#    - Status = PENDING → ERROR (finish verification)
#    - Status = REJECTED → ERROR (remove from draft)

# 4. Report:
#    Total citations: X
#    Verified: Y (should = X)
#    Unverified: Z (should = 0)
#    Result: PASS or FAIL
```

**You cannot submit if Z > 0.**

---

## NotebookLM Confidence Scoring

When NotebookLM returns a citation, assess its confidence:

| Score | Signal | Action |
|-------|--------|--------|
| **HIGH** | Exact page number provided + clear passage | Verify quickly (Level 2) |
| **MEDIUM** | Page number provided but quote is paraphrased | Verify carefully (cross-check PDF) |
| **LOW** | No page number OR vague passage | Verify thoroughly (re-read paper) |
| **NONE** | NotebookLM says "not found in sources" | Do not use; ask different question |

**Example**:
```
NotebookLM (HIGH confidence):
  "According to Smith et al (2024, p. 12): 'Agents equipped with reasoning...'"
  → Page number is specific ✅ → Verify quickly

NotebookLM (MEDIUM confidence):
  "The literature discusses how reasoning improves performance [Smith et al, 2024]"
  → No page number ⚠️ → Verify carefully

NotebookLM (LOW confidence):
  "Agents are better when trained well [multiple sources]"
  → Vague attribution ❌ → Do not use this
```

---

## Quick Decision Tree

```
START: You need to cite something

  ├─ "I read the paper myself"
  │  └─ → Level 1: Direct PDF ✅
  │     └─ Action: Record page number, add to log
  │
  ├─ "I'm using NotebookLM"
  │  │
  │  ├─ "I verified it against the PDF" 
  │  │  └─ → Level 2: Verified ✅
  │  │     └─ Action: Add to log with "verified" flag
  │  │
  │  └─ "I did NOT check the PDF yet"
  │     └─ → Level 3: Unverified ❌
  │        └─ Action: STOP. Go verify it. Then move to Level 2.
  │
  └─ "I'm using another paper's citation"
     └─ → Level 4: Secondary ❌
        └─ Action: STOP. Find and read the primary source.
```

---

## Before-and-After Examples

### **Example 1: ✅ CORRECT**

```markdown
**In thesis draft:**
"Research shows agents with reasoning improve performance [Smith et al., 2024, p. 12]."

**In verification log:**
Claim: Agents with reasoning improve performance
Source: Smith et al., 2024
Page: 12
Verified: ✅ PDF check passed
Status: APPROVED
```

### **Example 2: ❌ INCORRECT (Before Verification)**

```markdown
**In thesis draft:**
"Research shows agents with reasoning improve performance [Smith et al., 2024]."

**In verification log:**
Status: PENDING
(No entry yet — you haven't verified it)

ACTION NEEDED: Before submission, verify this citation.
```

### **Example 3: ❌ NEVER DO THIS**

```markdown
**In thesis draft:**
"Research shows agents with reasoning improve performance [Smith et al., 2024, p. 12]."

**Your process:**
1. Asked NotebookLM
2. Got the quote
3. Used it without checking PDF

VIOLATION: Level 3 citation. You must verify before submission.
```

---

## Handling Discrepancies

**Scenario**: You ask NotebookLM for a quote, but the PDF doesn't have it.

```
Step 1: Open PDF, search for the passage
        Result: Not found on page 12

Step 2: Try searching the whole PDF
        Result: Found on page 5 (slightly different context)

Step 3: Decision:
        - If context is the same: Update NotebookLM's page number, use it
        - If context is different: REJECT the citation, ask NotebookLM again
        - If not found anywhere: REJECT, find alternative source

Step 4: Record in log:
        Status: APPROVED / REJECTED
        Notes: "Quote found on page 5, not page 12. Context: [brief note]"
```

---

## Post-Submission (After May 15)

**Archive the verification log:**
```
Copy verified_citations.md → thesis_final/verified_citations_SUBMITTED_2026-05-15.md
This is your audit trail for the examiners if they ask.
```

---

## Common Questions

**Q: Do I need to verify every citation?**  
A: Yes, especially if from NotebookLM. Direct PDF reads are lower risk but should still be logged.

**Q: What if a quote is paraphrased?**  
A: Paraphrasing is fine, but you must note it: `[paraphrased, verified p. 12]`

**Q: What if the PDF doesn't have the quote?**  
A: Don't use it. Either find it elsewhere or ask NotebookLM for a different source.

**Q: Can I cite NotebookLM study guides or summaries?**  
A: No. Those are AI-generated summaries, not primary sources. Cite the original papers only.

**Q: What if I can't access a PDF?**  
A: Don't cite it. Find an alternative source or ask Brian to help locate it.

---

## Summary

| Phase | Rule |
|-------|------|
| **During writing** | Use NotebookLM for orientation, log citations as PENDING |
| **Before draft freeze** | Verify all PENDING citations; move to APPROVED or REJECTED |
| **Pre-submission audit** | 100% of citations must be APPROVED |
| **Submission** | Archive the verification log as proof of academic integrity |

**Academic Integrity Rule**: A citation without verification is a liability. Always verify.

---

**Questions?** Ask Brian or refer to NotebookLM integration guide.
