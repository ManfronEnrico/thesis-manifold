---
created: 2026-04-15 17:50:00
updated: 2026-04-15 17:50:00
---

# Integration Plan — Phase 1: State Extension

**Objective**: Extend `ThesisState` to support 6 toggleable features (Full scenario).

**Scope**: Add infrastructure; no feature implementations yet.

**Timeline**: 1–2 hours

**Dependencies**: Restructuring complete ✅

---

## Phase 1 Overview

### Current State

System B (`thesis_production_system/`) uses `ThesisState` (Pydantic BaseModel) to persist all thesis context:

```python
# thesis_production_system/state/thesis_state.py
class ThesisState(BaseModel):
    literature_state: LiteratureState
    thesis_outline: Dict[str, Any]
    sections: Dict[str, SectionState]
    figures: Dict[str, FigureState]
    compliance_checks: ComplianceState
    # ... more fields
```

### What We're Adding

1. **Toggles** — Feature activation flags
2. **Feature-specific fields** — Output/state for each feature
3. **Backward compatibility** — Old JSON still loads

### Files to Modify

| File | Change | Purpose |
|------|--------|---------|
| `thesis_production_system/state/thesis_state.py` | Add `toggles`, `material_gaps`, `integrity_report` | New feature fields |
| `thesis_production_system/state/compliance_state.py` | Add `citation_verification_report`, `integrity_report` | Compliance output storage |
| `docs/tasks/thesis_state.json` | Update to reflect new schema | Feature flag configuration |

### Files to Create (Optional Reference)

- `.claude/plans/feature_toggles_checklist.md` — Toggle status reference

---

## Step 1: Update ThesisState

**File**: `thesis_production_system/state/thesis_state.py`

**Add to ThesisState class** (after existing fields):

```python
from typing import Dict, List, Optional

class ThesisState(BaseModel):
    # [existing fields...]
    literature_state: LiteratureState = Field(default_factory=LiteratureState)
    thesis_outline: Dict[str, Any] = Field(default_factory=dict)
    sections: Dict[str, SectionState] = Field(default_factory=dict)
    figures: Dict[str, FigureState] = Field(default_factory=dict)
    compliance_checks: ComplianceState = Field(default_factory=ComplianceState)
    
    # NEW: Feature toggle configuration (Phase 1)
    toggles: Dict[str, bool] = Field(
        default_factory=lambda: {
            "pipeline_state_machine": False,
            "anti_leakage_protocol": False,
            "semantic_scholar_verification": False,
            "writing_quality_check": False,
            "style_calibration": False,
            "integrity_verification_gates": False,
        }
    )
    
    # NEW: Feature-specific state (Phase 1)
    material_gaps: List[str] = Field(default_factory=list)  # For anti-leakage protocol
    chapter_states: Dict[str, str] = Field(default_factory=dict)  # For pipeline state machine
    style_profile: Dict[str, Any] = Field(default_factory=dict)  # For style calibration
    
    # ... existing save/load methods unchanged
```

**Rationale**:
- All toggles default to `False` (opt-in only; safe default)
- Pydantic `Field(default_factory=...)` ensures backward compatibility
- Old JSON without these fields will auto-populate with defaults on load

---

## Step 2: Update ComplianceState

**File**: `thesis_production_system/state/compliance_state.py`

**Add to ComplianceState class** (after existing fields):

```python
class ComplianceState(BaseModel):
    # [existing fields like apa7_check, structure_check, etc...]
    apa7_check: bool = False
    abstract_check: bool = False
    frontpage_check: bool = False
    
    # NEW: Feature-specific compliance outputs (Phase 1)
    citation_verification_report: Dict[str, str] = Field(default_factory=dict)  # For Semantic Scholar API
    integrity_report: Dict[str, Any] = Field(default_factory=dict)  # For Integrity Verification Gates
```

**Rationale**:
- Consolidates compliance-related outputs in one place
- Keeps feature outputs separate from core compliance state

---

## Step 3: Test State Round-Trip

**What to do**:

1. **Load existing state.json**:
   ```python
   from thesis_production_system.state.thesis_state import ThesisState
   
   state = ThesisState.load("docs/tasks/thesis_state.json")
   print(f"Loaded state: {len(state.sections)} sections")
   assert state.toggles["anti_leakage_protocol"] == False  # Default
   ```

2. **Verify schema**:
   ```python
   # Check all toggles exist
   assert "anti_leakage_protocol" in state.toggles
   assert "semantic_scholar_verification" in state.toggles
   assert "integrity_verification_gates" in state.toggles
   ```

3. **Save and reload**:
   ```python
   # Save to temp file
   state.save("docs/tasks/thesis_state_test.json")
   
   # Reload
   state2 = ThesisState.load("docs/tasks/thesis_state_test.json")
   
   # Verify identical
   assert state.model_dump() == state2.model_dump()
   print("✓ State round-trip successful")
   ```

4. **Clean up**:
   ```bash
   rm docs/tasks/thesis_state_test.json
   ```

---

## Step 4: Verify Backward Compatibility

**Scenario**: Old JSON (without toggles/material_gaps) still loads correctly.

```python
# Create a minimal old-format JSON (simulating pre-Phase-1 state)
old_json = """
{
  "literature_state": {},
  "thesis_outline": {},
  "sections": {},
  "figures": {},
  "compliance_checks": {
    "apa7_check": true,
    "abstract_check": true,
    "frontpage_check": false
  }
}
"""

# Write to temp file
with open("docs/tasks/thesis_state_old_format.json", "w") as f:
    f.write(old_json)

# Load with new schema (should auto-populate missing fields)
state = ThesisState.load("docs/tasks/thesis_state_old_format.json")

# Verify defaults applied
assert state.toggles["anti_leakage_protocol"] == False
assert state.material_gaps == []
assert state.chapter_states == {}
assert state.style_profile == {}

print("✓ Backward compatibility verified")
```

---

## Step 5: Update Coordinator.load() (If Needed)

**Check**: Does `ThesisCoordinator` have any special state loading logic?

**Location**: `thesis_production_system/core/coordinator.py`

**Action**: 
- Search for `ThesisState.load()` calls
- If custom logic exists, verify it still works with new fields
- If not, no changes needed (Pydantic handles backward compatibility)

---

## Step 6: Document Feature Toggles

**Create**: `.claude/plans/feature_toggles_checklist.md`

```markdown
# Feature Toggles Checklist

All toggles default to `False` (disabled). Enable in `docs/tasks/thesis_state.json` as needed.

| Feature | Toggle | Status | Default | Phase |
|---------|--------|--------|---------|-------|
| Pipeline State Machine | `pipeline_state_machine` | Planned | OFF | 2 |
| Anti-Leakage Protocol | `anti_leakage_protocol` | Planned | OFF | 2 |
| Semantic Scholar API | `semantic_scholar_verification` | Planned | OFF | 2 |
| Writing Quality Check | `writing_quality_check` | Planned | OFF | 2 |
| Style Calibration | `style_calibration` | Planned | OFF | 2 |
| Integrity Verification Gates | `integrity_verification_gates` | Planned | OFF | 3 |

## To Enable a Feature

1. Edit `docs/tasks/thesis_state.json`:
   ```json
   {
     "toggles": {
       "anti_leakage_protocol": true,  ← Set to true
       "semantic_scholar_verification": false
     }
   }
   ```

2. Run thesis workflow — feature will be active

3. Check `thesis_state.json` for feature outputs (e.g., `material_gaps` list)

## To Disable a Feature

1. Set toggle to `false` in `thesis_state.json`
2. Run workflow again — feature inactive
3. Old behavior restored
```

---

## Execution Checklist

- [ ] **Read this plan** (you are here)
- [ ] **Modify `thesis_production_system/state/thesis_state.py`** — Add toggles + feature fields
- [ ] **Modify `thesis_production_system/state/compliance_state.py`** — Add compliance fields
- [ ] **Test state round-trip** — Load/save/reload with new schema
- [ ] **Verify backward compatibility** — Old JSON still loads
- [ ] **Check Coordinator.load()** — Ensure no custom logic breaks
- [ ] **Create feature toggles checklist** — Document toggle reference
- [ ] **Verify git status** — No unexpected changes
- [ ] **Create outcome file** — Document what was added

---

## Expected Outcome

After Phase 1:
- ✅ `ThesisState` has 6 toggles (all default OFF)
- ✅ Feature-specific fields in state (material_gaps, chapter_states, style_profile, etc.)
- ✅ Old JSON still loads correctly (backward compatible)
- ✅ Ready for Phase 2 (implement first feature: anti-leakage protocol)

---

## Next: Phase 2 Planning

Once Phase 1 is complete, we'll create detailed Phase 2 plans for each feature:

1. **Feature 2**: Anti-Leakage Protocol (3–4 hrs)
2. **Feature 3**: Semantic Scholar API (5–6 hrs)
3. **Feature 4**: Writing Quality Check (2–3 hrs)
4. **Feature 5**: Style Calibration (3–4 hrs)
5. **Feature 1**: Pipeline State Machine (2–3 hrs)
6. **Feature 6**: Integrity Verification Gates (8–10 hrs)

Each will follow the same pattern:
- Extend relevant agent(s)
- Add validator to CriticAgent
- Test in isolation (toggle ON/OFF)
- Verify no regression

---

## Outcome

_Completed: 2026-04-15_

### ✅ Completed
- Extended ThesisState with toggle infrastructure (6 boolean flags, all default OFF)
- Added feature-specific state fields (material_gaps, chapter_states, style_profile)
- Extended ComplianceState with feature output fields (citation_verification_report, integrity_report)
- Implemented comprehensive backward compatibility (old JSON loads with auto-populated defaults)
- Created and executed test suite (4 tests, 100% pass rate)
  - Fresh state creation with defaults
  - Save/reload round-trip preservation
  - Backward compatibility verification
  - ComplianceState feature field initialization
- Verified zero breaking changes
- Committed changes to main branch (5b54919)
- Created outcome documentation

### 🔄 Adjusted
- **What**: Used safe OneDrive file editing pattern (write to /tmp, copy via bash) instead of direct Edit tool
  **Why**: Direct Edit/Write on OneDrive .py files causes CRLF corruption and EEXIST errors
  **How**: Created patching scripts in /tmp, copied via bash cp command, verified with tests

- **What**: Integrated outcome documentation directly into plan workflow instead of separate document
  **Why**: Needed visibility into what was actually completed vs. what was planned
  **How**: Created separate outcome_files/ directory structure; linked from plan via outcome file

### ❌ Dropped
- None — all planned work completed as designed

### Notes
- OneDrive file safety became critical; documented safe pattern for future Python modifications
- Toggle defaults (all OFF) ensure zero risk of unintended feature activation
- Backward compatibility tested extensively; old state JSON loads without modification
- Phase 2 features are now ready to implement independently via toggle flags
- No unexpected issues encountered; execution matched plan timeline exactly
