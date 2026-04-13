# CR-0012 Sub-phase A: Composition Engine Wiring — Implementation Summary

**Date:** 2026-04-05  
**Author:** FE Lead (Agent)  
**Status:** COMPLETE  
**Tests:** 1314 passed (0 failures) | Build: clean

---

## Changes Implemented

### 1. `famililook-desktop2/src/utils/constants.js`
Added 4 roles to `RELATIONSHIP_OPTIONS`: `"Stepmum"`, `"Stepdad"`, `"Godparent"`, `"Grandchild"`. Appended at end to avoid reordering existing entries. Total: 21 roles.

### 2. `famililook-desktop2/src/utils/stateNormalization.js`
Added defaults to both `normalizeParentEntry()` and `normalizeChildEntry()`:
- `ageGroup`: defaults to `"adult"` for parents, `"child"` for children
- `ethnicity`: defaults to `null` (unset, not "default" — composition engine distinguishes)
- `structuredRole`: defaults to `null` (user didn't choose vs. user chose a role)

Follows existing spread pattern (`...entry` at end preserves explicit values from entry).

### 3. `famililook-desktop2/src/state/FamililookContext.jsx`
Added 6 `useCallback` helpers:
- `updateParentRole(index, role)` / `updateChildRole(index, role)` — sets `structuredRole`
- `updateParentAgeGroup(index, ageGroup)` / `updateChildAgeGroup(index, ageGroup)`
- `updateParentEthnicity(index, ethnicity)` / `updateChildEthnicity(index, ethnicity)`

All 6 exposed in context value object alongside existing `updateParentLabel`, `updateChildLabel`.

### 4. `famililook-desktop2/src/components/keepsakes/utils/compositionEngine.js`
Two changes:

**`deriveContext()`**: Prefers `input.data.winnerRole` over `input.data.winnerLabel` for parent type resolution. Falls back to label guessing if `winnerRole` is absent — fully backward-compatible.

**`selectCharacter()`**: Added structured ethnicity layer in variant resolution:
1. `input.variant` (explicit user override from customise screen) — highest priority
2. `input.data.winnerEthnicity` (from profile) — new layer
3. `AFRICAN_OCCASIONS` (occasion-based) — existing logic
4. `"default"` — fallback

### 5. `famililook-desktop2/src/assets/characters/index.js`
Exported two new functions from the previously module-private `IMAGES` object:

- `getAvailableCharacters(variant)` — returns `[{ type, emotions[], thumbnailUrl }]` for building picker UI
- `getAvailableVariants()` — returns `["default", "african"]` (extensible)

`IMAGES` itself remains unexported (private). Only the enumeration API is public.

### 6. `famililook-desktop2/src/utils/roleSuggestions.js` (NEW) + `GroupSnapshotSection.jsx`
Extracted `getSmartSuggestions(age, gender)` from GroupSnapshotSection (was a local function at line 630) to a shared utility at `src/utils/roleSuggestions.js`. GroupSnapshotSection now imports from the utility. Identical logic — no behavioral change.

---

## Backward Compatibility

All changes are additive. No existing behavior is modified:
- `winnerRole` / `winnerEthnicity` absent in existing data = original label-guessing path used
- `structuredRole` / `ageGroup` / `ethnicity` default to `null` / sensible defaults
- `RELATIONSHIP_OPTIONS` array only gained entries at the end
- `getSmartSuggestions` is an exact extraction (same function body)
- No backend changes. No contract changes. No API changes.

## Next Steps (Sub-phase B)

Sub-phase B will wire the Identity Sheet UI (bottom sheet for structured capture per photo slot) and the CharacterPicker component in KeepsakeCustomise. These depend on all Sub-phase A foundations being in place.
