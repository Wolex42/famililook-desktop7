# CHANGE REQUEST -- CR-0012

**Feature:** Family Identity Profiles (Structured Role/Name Capture + Character Picker)
**Date:** 2026-04-05 | **Author:** Change Manager (Agent)
**Status:** PENDING CEO APPROVAL
**Risk Tier:** T2 (Medium) -- multiple FE files touched, composition engine logic change, but no backend/contract impact and full backward compatibility via fallback paths.

---

## Contract Impact

| Contract | Affected | Reasoning |
|---|---|---|
| `kinship_analyze.v1` | NO | All new data (role, ageGroup, ethnicity) is FE-only for keepsake rendering. Backend API unchanged. |
| `compare_faces.v1` | NO | FamiliMatch is a separate product. Zero overlap with this feature. |

## Backend Changes Required

**NO.** Phase 1 is entirely frontend. Structured profile data stays in FamililookContext + localStorage. compositionEngine reads it client-side.

---

## Files to Modify (exact paths)

| # | File | Change |
|---|---|---|
| 1 | `famililook-desktop2/src/state/FamililookContext.jsx` | Add `familyProfiles` state, 6 update helpers (role/ageGroup/ethnicity for parent+child) |
| 2 | `famililook-desktop2/src/state/stateNormalization.js` | Add defaults for `ageGroup`, `ethnicity` in normalize functions |
| 3 | `famililook-desktop2/src/utils/constants.js` | Add 4 roles to RELATIONSHIP_OPTIONS (Stepmum, Stepdad, Godparent, Grandchild) |
| 4 | `famililook-desktop2/src/utils/compositionEngine.js` | Read `winnerRole`/`winnerAgeGroup`/`winnerEthnicity`; fallback to label guessing |
| 5 | `famililook-desktop2/src/utils/characterHeadlines.js` | Support structured role input alongside label-based normalisation |
| 6 | `famililook-desktop2/src/assets/characters/index.js` | Export `getAvailableCharacters()` enumeration from IMAGES lookup |
| 7 | `famililook-desktop2/src/components/keepsakes/KeepsakeCustomise.jsx` | Replace Classic/Heritage toggle with CharacterPicker; insert after Recipient selector |
| 8 | `famililook-desktop2/src/components/detection/GroupSnapshotSection.jsx` | Extract `getSmartSuggestions` to shared utility |

## New Files to Create

| # | File | Purpose | ~Lines |
|---|---|---|---|
| 1 | `famililook-desktop2/src/components/creation/IdentitySheet.jsx` | Bottom sheet for role/name/age/variant per slot | ~120 |
| 2 | `famililook-desktop2/src/components/keepsakes/CharacterPicker.jsx` | Featured card + emotion strip + role chips | ~80 |
| 3 | `famililook-desktop2/src/utils/familyProfiles.js` | loadProfiles, saveProfile, matchProfile + localStorage | ~40 |
| 4 | `famililook-desktop2/src/utils/roleSuggestions.js` | Extracted getSmartSuggestions from GroupSnapshotSection | ~30 |
| 5 | `famililook-desktop2/tests/profiles/familyProfiles.test.js` | Unit tests for profile persistence | ~60 |
| 6 | `famililook-desktop2/tests/profiles/identitySheet.test.jsx` | Integration tests for IdentitySheet | ~80 |
| 7 | `famililook-desktop2/tests/profiles/characterPicker.test.jsx` | Integration tests for CharacterPicker | ~60 |

---

## Feature Flag

**Name:** `VITE_FAMILY_PROFILES`
**Location:** `famililook-desktop2/.env` + AppRouter or FamililookContext
**Behaviour:** Flag OFF = zero change to existing flows. Identity Sheet hidden, compositionEngine ignores profile fields, CharacterPicker not rendered.

---

## Implementation Order

1. **`constants.js`** -- add 4 roles (zero dependency, zero risk)
2. **`roleSuggestions.js`** (new) + **`GroupSnapshotSection.jsx`** -- extract utility
3. **`stateNormalization.js`** + **`FamililookContext.jsx`** -- schema + helpers
4. **`familyProfiles.js`** (new) -- localStorage persistence
5. **`IdentitySheet.jsx`** (new) -- UI for structured capture (depends on 1-4)
6. **`compositionEngine.js`** + **`characterHeadlines.js`** -- structured input path
7. **`characters/index.js`** -- export enumeration
8. **`CharacterPicker.jsx`** (new) + **`KeepsakeCustomise.jsx`** -- picker UI (depends on 6-7)
9. **Tests** -- all test files (depends on 1-8)

---

## Rollback Strategy

1. Set `VITE_FAMILY_PROFILES=false` -- instantly disables all new UI and logic paths.
2. All modified files have backward-compatible fallbacks (structured role absent = label guessing). No data migration needed.
3. localStorage key `fl:family-profiles` is inert when flag is off. Can be cleared manually if needed.
4. If composition engine regression detected: revert commits touching `compositionEngine.js` and `characterHeadlines.js` only. Label-based path is untouched.

---

## Blast Radius Summary

- **Affected area:** Upload flow, FamililookContext, composition engine, KeepsakeCustomise
- **Unaffected:** Backend, API contracts, FamiliUno, FamiliMatch, FamiliPoker, group photo mode, analytics, consent, navigation, payment flow
- **Estimated effort:** ~500 lines across ~10 modified + ~7 new files, ~10 hours
