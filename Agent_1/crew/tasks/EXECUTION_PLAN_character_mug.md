# Character Mug Fix — Execution Plan
**Date:** 2026-04-07
**Two tracks:** Crash fix (immediate) + UX clarity (follows)

---

## The Problem Summary

| # | CEO report | Root cause | Track |
|---|-----------|-----------|-------|
| 1 | Not clear how characters render on mugs | No product explanation in the flow | UX Track |
| 2 | How results merge with characters | characterOverride never reaches compositionEngine + no bridge UI | Crash + UX Track |
| 3 | Preview CTA too far down | Layout position issue | UX Track |
| 4 | Crash on preview (React #426) | characterType/characterEmotion not passed to composeCharacterMug() | Crash Track |

---

## Execution Map

```
TRACK 1 — CRASH FIX (start immediately)
─────────────────────────────────────────────────────────────
Step 1: Platform Architect
  → ARCH_triage_character_mug_crash.md
  → Reads: KeepsakeMobileFlow, CharacterMugTemplate, compositionEngine
  → Output: scope assessment + patch count check

Step 2: CEO Gate
  → Approve Option A (prop thread only)
     OR Option B (prop thread + engine guard)
     OR Option C (prop thread + route engine to /crew redesign)

Step 3: FE Lead (Crash Fix)
  → FE_crash_fix_character_mug.md
  → Working set: per CEO approval
  → Output: crash fixed, tests written

Step 4: QA Lead
  → Validate crash fix
  → Verify no regression on other mug products (MugWrapTemplate, FamilyMugTemplate)
  → Device verification: PENDING CEO

Step 5: Change Manager
  → Log CR for crash fix
  → Update architecture migration candidates if compositionEngine flagged


TRACK 2 — UX CLARITY (start immediately, parallel to Track 1 Steps 1-3)
─────────────────────────────────────────────────────────────
Step 1: Visual Director + Copywriter (PARALLEL)
  → VD_character_mug_ux.md
  → CW_character_mug_ux.md
  → VD reads flow screens, specs 3 UI elements
  → Copywriter reads VD spec, writes copy for all 3
  → Outputs: VISUAL_DIRECTION_character_mug_ux.md + COPY_BANK_character_mug_ux.md

Step 2: CEO Reviews Specs
  → Read both documents
  → Approve, or return with notes

Step 3: FE Lead (UX Implementation)
  → FE_ux_implementation.md
  → ONLY after crash fix is merged (Track 1 complete)
  → Implements exactly to VD spec + CW copy bank
  → No design decisions

Step 4: QA Lead
  → Validate UX implementation
  → Check all 3 elements render correctly
  → Check bridge element with and without analysis results
  → Device verification: PENDING CEO

Step 5: Change Manager
  → Log CR for UX implementation
  → Combined release package with crash fix if timing allows
```

---

## File Boundary Summary

| Agent | Files they touch |
|-------|----------------|
| Platform Architect | READ ONLY: KeepsakeMobileFlow, CharacterMugTemplate, compositionEngine |
| FE Lead (Crash) | KeepsakeMobileFlow, CharacterMugTemplate, compositionEngine (if approved) |
| Visual Director | READ ONLY: all screens |
| Copywriter | READ ONLY: screens + VD spec |
| FE Lead (UX) | KeepsakeCustomise, KeepsakeMobileFlow (if bridge needs state), KeepsakePreview (if CTA moves) |

Zero overlap between crash fix files and UX files — both tracks can run simultaneously up to their respective FE steps.

---

## CEO Checkpoints

| Checkpoint | When | What you decide |
|-----------|------|----------------|
| Per-edit approvals | During each agent session | Approve each diff preview |
| Track 1 scope gate | After Platform Architect assessment | Option A / B / C |
| Track 2 spec review | After VD + CW output | Approve specs or return with notes |
| QA sign-off | After each track completes QA | Review verdict |
| Device verification | After both tracks merge | Test on physical phone: character mug full flow |
| Release approval | After device verification | Merge to production |

---

## Device Verification Checklist (CEO — physical phone)

After both tracks complete:

1. Open character mug flow
2. Run analysis first — get results showing a winner
3. Navigate to character mug from results
4. **Verify**: Bridge moment shows winner + percentage
5. **Verify**: Product explanation appears and is dismissable
6. **Verify**: CharacterPicker shows characters
7. Select a character (including gran_loving_african if available)
8. Press the preview CTA
9. **Verify**: No crash — preview renders
10. **Verify**: CTA is reachable without excessive scrolling
11. Add to basket
12. **Verify**: Basket receives the item correctly

All 12 points PASS → approve release.
