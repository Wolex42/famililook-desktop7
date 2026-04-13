# CR-0012 Sub-phase B: Identity Sheet UI — Implementation Summary

**Author:** FE Lead (Agent)  
**Date:** 2026-04-05  
**Status:** COMPLETE  
**Build:** PASS (3.77s)  
**Tests:** 1314/1314 PASS (0 regressions)

---

## Files Created

### `famililook-desktop2/src/components/upload/IdentitySheet.jsx` (~220 lines)
New bottom sheet component for capturing structured identity data per family member.

**Features implemented:**
- Dark overlay backdrop (rgba(0,0,0,0.5)), tap-to-dismiss
- Sheet slides up from bottom with 280ms cubic-bezier animation (iOS spring feel)
- Handle bar: 40px wide, 4px tall, centered
- Header row: 48px photo thumbnail + "Tell us about them" title + "Done" button
- Role chip row: horizontal scrollable, 10 roles (Mum, Dad, Grandma, Grandad, Son, Daughter, Brother, Sister, Aunt, Uncle)
- Name input: placeholder "Their name (optional)", 44px height
- Age bracket: 4 buttons (Child, Teen, Adult, Senior) with smart defaults (Adult for parent slots, Child for child slots)
- Variant selector: 2 circular 64px thumbnails showing character preview (Classic/Heritage) using `getCharacterImage()`
- Helper text: "A little detail goes a long way. Better match, better mug."
- All touch targets >= 44px
- All strings from Copy Bank
- All styling from Visual Direction (theme tokens, chip styles, section labels)

---

## Files Modified

### `famililook-desktop2/src/components/upload/PhotoSlot.jsx`
- Added `onEditIdentity` and `structuredRole` props
- `handleLabelClick` now prefers `onEditIdentity` over inline edit when available
- Label displays `{name} · {role}` format when `structuredRole` is set
- Pencil icon shows when either `onEditIdentity` or `onLabelChange` is available
- Title attribute updated: "Tap to edit profile" when identity sheet is wired

### `famililook-desktop2/src/layout/UploadSection.jsx`
- Imported `IdentitySheet` component
- Destructured 6 new context helpers: `updateParentRole`, `updateParentAgeGroup`, `updateParentEthnicity`, `updateChildRole`, `updateChildAgeGroup`, `updateChildEthnicity`
- Added `identityTarget` state (`{ type, index }` or null)
- Wired `onEditIdentity` and `structuredRole` props to all parent PhotoSlots (index 0 and 1)
- Wired `onEditIdentity` and `structuredRole` props to all child PhotoSlots (via map)
- `onEditIdentity` only enabled when photo exists (`.previewUrl` truthy)
- Rendered `IdentitySheet` at bottom of component tree, reading all values from context and routing changes through context helpers

### `famililook-desktop2/src/components/keepsakes/hooks/useKeepsakeData.js`
- Added `winnerRole` (from `winnerParent.structuredRole`) and `winnerEthnicity` (from `winnerParent.ethnicity`) to returned object
- Both default to `null` when not set, preserving backward compatibility

---

## Backward Compatibility

- Identity Sheet is purely additive — no existing behavior changed
- If user never taps the label/pencil, the old inline edit path still works (falls through when `onEditIdentity` is undefined)
- If `structuredRole` is null/undefined, label displays as before (no " . role" suffix)
- `useKeepsakeData` return shape is additive only — new fields are `null` when profiles not set

---

## Dependencies

- Sub-phase A context helpers (already merged): `updateParentRole`, `updateParentAgeGroup`, `updateParentEthnicity`, `updateChildRole`, `updateChildAgeGroup`, `updateChildEthnicity`
- Character illustration index: `getCharacterImage()` from `assets/characters/index.js`
- Theme tokens: `colors`, `radius`, `spacing`, `shadows` from `theme/colors.js`
