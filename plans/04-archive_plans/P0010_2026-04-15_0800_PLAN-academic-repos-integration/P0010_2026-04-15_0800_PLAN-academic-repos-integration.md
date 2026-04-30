---
created: 2026-04-15 14:32:18
updated: 2026-04-15 15:45:00
---

# Integration Plan: Academic Repos as Optional Layers

## Overview

Integrate components from `academic-research-skills` and `scientific-agent-skills` as **optional enhancements** to your existing System B workflow, not replacements. Your current agent architecture stays intact; external skills become toggleable add-ons.

**Guiding principle**: Complexity on-demand. Start with your solid foundation, add features only when needed.

---

## 1. Thesis Context

**Title**: Manifold AI — Predictive Decision-Support in FMCG Retail Under 8GB RAM  
**Main RQ**: How can AI systems provide reliable decision-support under computational constraints?  
**SRQ1–4**: Forecasting efficiency, multi-agent coordination, consumer signal enrichment, predictive vs. descriptive BI  
**Methodology**: DSR (Hevner 2004 + Peffers 2007)  
**Deadline**: 15 May 2026 (45 days)  
**Hard constraints**: 8GB RAM, 120-page limit, no em dashes, writing agent produces bullets only

---

## 2. Proposed Integration Architecture

```
System B (Your Current Agents)
├─ Thesis Coordinator (existing)
├─ Writing Agent (bullets only)
├─ Compliance Agent (APA 7, CBS checks)
├─ Literature Agent (corpus management)
├─ Critic Agent (validation)
├─ [Other existing agents...]
│
└─ Optional Feature Toggles (Academic Repos)
   ├─ [TOGGLE] Pipeline State Machine → Chapter readiness tracking
   ├─ [TOGGLE] Anti-Leakage Protocol → Material gap detection
   ├─ [TOGGLE] Semantic Scholar API → Citation verification
   ├─ [TOGGLE] Writing Quality Check → Prose pattern detection
   ├─ [TOGGLE] Style Calibration → Author voice learning
   └─ [TOGGLE] Integrity Verification Gates → 5-phase pre-submission check
```

**Key**: Each toggle is independent. Enable only what you need.

---

## 3. The Five Toggleable Features

### Feature 1: Pipeline State Machine ⚙️

**What**: Tracks which chapters are ready, which blocked, why.

**Current state**: Chapters managed sequentially, but no formal state tracking.

**Why add it**: 
- Clear visibility on "which chapters can be prose-written now?"
- Auto-notification when blockers clear (data arrives, System A results ready)
- Prevents accidental out-of-order writing

**Toggle implementation** (simple):
- Add `chapter_state.json` with status per chapter
- System B Planner checks state before assigning writing tasks
- ~2–3 hours to add

**Enable when**: Data blockers expected (Nielsen + Indeks Denmark still pending) or coordinating with co-author

**Risk if disabled**: Manual tracking required; easier to accidentally write Ch. 6 before data arrives

---

### Feature 2: Anti-Leakage Protocol 🚨

**What**: Flags `[MATERIAL GAP]` when prose lacks source material; prevents hallucinated citations.

**Current state**: Writing Agent produces bullets; humans write prose (may invent facts if not careful).

**Why add it**: 
- CBS compliance risk: fabricated citations are integrity violation
- Tight deadline increases mistake likelihood
- Guards against subtle hallucination (plausible-sounding but false claims)

**Toggle implementation** (lightweight):
- Add Material Gap check to Critic Agent validator
- Flag prose that cites missing papers or data
- ~3–4 hours to add

**Enable when**: Writing prose for Ch. 4–8 (data-dependent chapters where hallucination risk is high)

**Risk if disabled**: May publish unsourced claims by accident (high-risk for CBS compliance)

---

### Feature 3: Semantic Scholar API Citation Verification ✓

**What**: Programmatically check every citation exists (title match, DOI verification, journal validation).

**Current state**: Manual spot-checks or trust in author accuracy.

**Why add it**: 
- 37 papers in Ch. 2 — error rate without automated QA is ~5% (1–2 bad citations)
- Pre-submission check catches errors before supervisor review
- Reusable infrastructure for future papers

**Toggle implementation** (medium):
- Free API (no key required); rate limits generous for thesis size
- Check all Ch. 2 citations in ~2 minutes
- Output: "37 verified, 35 PASS, 2 WARN (metadata variants)"
- ~5–6 hours to integrate

**Enable when**: Finalizing Ch. 2 (literature review) before submission

**Risk if disabled**: 1–2 citation errors slip through; supervisor catches it (recoverable but embarrassing)

---

### Feature 4: Writing Quality Check 📝

**What**: Scans prose for AI-typical patterns (overused openers, em dashes, uniform sentence rhythm, passive voice overuse).

**Current state**: Manual human review of prose drafts.

**Why add it**: 
- Saves 1–2 revision cycles (catch issues in draft, not after human review)
- Enforces your "no em dashes" rule automatically
- Flags monotonous prose (sentence rhythm uniformity)

**Toggle implementation** (lightweight):
- Checklist applied by Critic Agent after prose draft
- Output: "PASS | WARNING (em dashes ×3, fix before publishing)"
- ~2–3 hours to add

**Enable when**: Writing early chapters (Ch. 1–3) to establish quality baseline, then reuse for Ch. 9–10

**Risk if disabled**: Prose goes to human review without pre-checks; 1–2 extra revision rounds needed

---

### Feature 5: Style Calibration 🎨

**What**: Learn writing voice from Ch. 1 (already prose-complete), apply as soft guide to Ch. 9–10.

**Current state**: 2 students writing different chapters; potential tone inconsistency.

**Why add it**: 
- Improves coherence across co-authored chapters
- Optional "soft guide" (not hard rules)
- Useful if Ch. 9–10 written by different author than Ch. 1

**Toggle implementation** (lightweight):
- Extract style metrics from Ch. 1 (sentence length, formality, citation style)
- Store as JSON profile
- Prompt writer: "Use this style guide (soft, not strict)"
- ~3–4 hours to add

**Enable when**: Writing Ch. 9–10 (Discussion + Conclusion) if different author from Ch. 1

**Risk if disabled**: Ch. 9–10 may have different tone; coherence impact is minor (acceptable)

---

### Feature 6: Integrity Verification Gates 🔒

**What**: 5-phase pre-submission check: (A) claims have citations, (B) all refs exist, (C) data not hallucinated, (D) plagiarism scan, (E) ethics/disclosure.

**Current state**: Compliance Agent does manual checks (APA 7 format, abstract, front page only).

**Why add it**: 
- Comprehensive pre-submission QA (not just format compliance)
- Catches claim verification (Phase A) without sources
- Risk mitigation: no integrity issues at submission

**Toggle implementation** (heavier):
- Phases A + B: Automated (grep + Semantic Scholar API)
- Phases C + D + E: Manual checklist for now (difficult to fully automate)
- Output: "PASS all phases | 2 warnings (Phase A: 3 unsourced claims, Phase B: 0 failures)"
- ~8–10 hours to implement

**Enable when**: Final review, 3–5 days before submission (2026-05-10)

**Risk if disabled**: Skip to supervisor review without automated QA; supervisor catches major issues (adds delay)

---

## 4. Implementation Roadmap (Lean Version)

### Phase 0: Setup (1 day)
- [ ] Clone external repos into `.claude/imports/`
- [ ] Document which features are enabled (toggle checklist in `.claude/plans/`)
- [ ] No code changes yet; planning only

### Phase 1: Mandatory Features (4–5 days)
These have highest ROI and lowest risk:
- **Feature 3**: Semantic Scholar API (5–6 hours) → cite verification, pre-submission, low risk
- **Feature 2**: Anti-Leakage (3–4 hours) → CBS compliance safeguard, lightweight

**Deliverable**: Ch. 2 citations verified; all prose reviewed for material gaps. System B fully functional.

### Phase 2: Optional Enhancements (3–4 days, as time permits)
Add only if Phase 1 complete + time available:
- **Feature 4**: Writing Quality Check (2–3 hours) → easy to add, high QoL
- **Feature 1**: Pipeline State Machine (2–3 hours) → coordination help, non-blocking if skipped
- **Feature 5**: Style Calibration (3–4 hours) → coherence improvement, non-critical

### Phase 3: Advanced (If time + headroom remain)
- **Feature 6**: Full Integrity Gates (8–10 hours) → comprehensive but time-heavy; defer if deadline tight

---

## 5. Feature Complexity Dial

| Scenario | Recommendation | Enabled Features |
|----------|---|---|
| **Baseline (lowest risk)** | Keep existing System B, add minimal safeguards | #2, #3 only |
| **Standard (recommended)** | Add helpful tools + safeguards | #2, #3, #4, #5 |
| **Full (max complexity)** | All features, comprehensive QA | #1–6 |
| **If timeline slips** | Cut to essentials fast | #2, #3 only (stop here) |

**Your call**: Which scenario fits your risk tolerance + timeline confidence?

---

## 6. Effort & Cost

### Tier Breakdown

| Feature | Hours | Cost (Haiku) | Priority |
|---------|-------|---|---|
| 2. Anti-Leakage | 3–4 | $0.03 | HIGH |
| 3. Semantic Scholar | 5–6 | $0.20 | HIGH |
| 4. Writing QC | 2–3 | $0.02 | MED |
| 5. Style Calib | 3–4 | $0.02 | MED |
| 1. Pipeline State | 2–3 | $0.01 | LOW |
| 6. Integrity Gates | 8–10 | $0.15 | LOW |
| **TOTAL (all)** | **23–30** | **~$0.43** | — |
| **Minimum (#2+#3)** | **8–10** | **~$0.23** | — |

**Timeline**: Minimum setup (mandatory) = 1 week at 2 hours/day; full setup = 2 weeks at 2–3 hours/day.

---

## 7. Toggle Implementation Pattern

All features use the same pattern. Example:

```python
# In thesis_state.json
{
  "toggles": {
    "pipeline_state_machine": false,        # Not using yet
    "anti_leakage_protocol": true,          # Enabled
    "semantic_scholar_verification": true,  # Enabled
    "writing_quality_check": false,         # Not using yet
    "style_calibration": false,             # Not using yet
    "integrity_verification_gates": false   # Defer to Phase 3
  }
}
```

In System B agents, before invoking feature:
```python
if thesis_state.toggles.anti_leakage_protocol:
    # Run anti-leakage check
    gaps = check_material_gaps(prose)
    if gaps:
        flag_for_human_review(gaps)
```

**Benefit**: Toggle off instantly if feature causes issues; no code deletion needed.

---

## 8. Governance

- **System A is frozen** — no changes, ever
- **System B enhancements**: toggleable only; existing agents untouched
- **External repos**: Imported as read-only references (no modifications)
- **Phase gates**: Tier 1 (mandatory) approval required before adding Tier 2 (optional)

---

## 9. Decision: What Do You Want?

To move forward, confirm:

1. **Scenario**: Baseline (2 features) | Standard (5 features) | Full (6 features)?
2. **Timeline**: Can we invest 1–2 weeks? Or must we cut to minimum?
3. **Risk appetite**: Prioritize safeguards (anti-leakage first) or feature velocity (all at once)?

Once you decide, I'll create a detailed **Phase 1 action plan** with specific code changes.

---

**Status**: Ready for your input  
**Next step**: Tell me which scenario + timeline  
