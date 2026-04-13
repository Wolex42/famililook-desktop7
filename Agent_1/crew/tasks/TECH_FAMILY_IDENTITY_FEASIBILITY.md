# Technical Feasibility: Structured Role/Name Capture + Character Picker

**Author:** FE Lead  
**Date:** 2026-04-05  
**Status:** Assessment complete

---

## 1. What Can Be Reused from Group Photo Flow

| Component / Utility | Location | Reuse Strategy |
|---|---|---|
| `FaceNamingSheet` | `src/components/detection/FaceNamingSheet.jsx` | Pattern reusable. Name input + role dropdown + prev/next navigation. Extract the name+role fieldset into a shared `<IdentityFields>` component. The sheet's overlay/handle chrome is group-specific — don't reuse that. |
| `getSmartSuggestions(age, gender)` | `GroupSnapshotSection.jsx` (local function) | Extract to `src/utils/roleSuggestions.js`. Currently returns `{ suggested, remaining }` from `RELATIONSHIP_OPTIONS` sorted by detected age/gender. Works as-is for individual flow if age bracket is known. |
| `RELATIONSHIP_OPTIONS` | `src/utils/constants.js` | 17 roles — sufficient for MVP. Missing: "Stepmum", "Stepdad", "Godparent", "Grandchild". Add those 4 for completeness. No breaking change — consumers iterate the array. |
| `normaliseParent()` | `characterHeadlines.js` | Already maps label strings to canonical role keys (mum, dad, gran, etc.). If we store structured `role` field, this function becomes a fallback for legacy data only. |

## 2. Context Schema Changes

Current parent/child shape in `FamililookContext.jsx` (line 80-81):
```
{ id, file, name, label, role }
```

`role` is currently a free-text string (e.g. "parent", "child"). `name` and `label` are display strings set via `updateParentLabel()` / `updateChildLabel()`.

**Proposed additions:**

```js
{
  id, file, name, label,
  role: "Mum",              // structured — from RELATIONSHIP_OPTIONS picker
  ageGroup: "adult",        // "infant" | "child" | "teen" | "adult" | "senior"
  ethnicity: "default",     // "default" | "african" (maps to character variant)
}
```

**Impact on `stateNormalization.js`:**  
The spread operator on line 67 (`...entry`) already preserves unknown fields. New fields will pass through normalisation untouched. No breaking change. Add defaults in `normalizeParentEntry()` and `normalizeChildEntry()`:
```js
ageGroup: entry.ageGroup ?? "adult",
ethnicity: entry.ethnicity ?? "default",
```

**New context helpers needed:**
- `updateParentRole(index, role)` — sets structured role
- `updateParentAgeGroup(index, ageGroup)`
- `updateParentEthnicity(index, ethnicity)`
- Mirror set for children: `updateChildRole`, `updateChildAgeGroup`, `updateChildEthnicity`

Effort: ~30 lines in `FamililookContext.jsx`, ~6 lines in `stateNormalization.js`.

## 3. Composition Engine Changes

`composeCharacterMug(input)` in `compositionEngine.js` currently receives `input.data.winnerLabel` (a string like "Mum") and calls `normaliseParent(label)` to guess the role. This guessing is the core problem — "Sarah" normalises to "custom", picking the wrong character.

**With structured data:**
- `input.data.winnerRole` (e.g. "Mum") replaces label-based guessing
- `input.data.winnerAgeGroup` feeds age-appropriate character selection
- `input.data.winnerEthnicity` replaces the manual "Classic"/"Heritage" toggle
- `input.variant` override still works (user can override ethnicity on customise screen)

**Changes to `deriveContext()`:** Replace `normaliseParent(input.data.winnerLabel)` with:
```js
const parentType = input.data.winnerRole
  ? normaliseParent(input.data.winnerRole)
  : normaliseParent(input.data.winnerLabel);  // fallback
```

This is backward-compatible — old data without `winnerRole` still works via label guessing.

Effort: ~15 lines across `compositionEngine.js` + `characterHeadlines.js`.

## 4. Character Picker Component

**Data source:** `IMAGES` lookup in `src/assets/characters/index.js`. Structure: `IMAGES[variant][character][emotion]`. Characters: mama, papa, cub, mini, gran, gramps. Variants: default, african.

**What picker needs to render:**
- 6 character types x 2 variants = 12 thumbnail options (use `proud`/`happy` pose for thumbnails)
- Grid of circular thumbnails (3 per row), dark theme, matching `KeepsakeCustomise` chip style
- Selected state: violet border `#7C3AED`, unselected: `#2a2a4e` border

**Integration point:** `KeepsakeCustomise.jsx`, after the existing "Character Style" toggle (line 458-524). Replace the binary "Classic"/"Heritage" toggle with the full picker. The picker sets both character type AND variant simultaneously.

**Props:** `selectedCharacter`, `selectedVariant`, `onCharacterChange(type, variant)`.

**Enumerating characters from `IMAGES`:** Export `IMAGES` (currently module-private). Or export a `getAvailableCharacters()` that returns `[{ type, variant, thumbnailUrl }]`.

Effort: ~80-line new component `CharacterPicker.jsx` + ~10 lines modifying `characters/index.js` to export enumeration + ~15 lines in `KeepsakeCustomise.jsx` to swap toggle for picker.

## 5. localStorage Persistence — Family Profiles

**Key:** `fl:family-profiles`  
**Shape:**
```json
{
  "version": 1,
  "profiles": [
    { "name": "Sarah", "role": "Mum", "ageGroup": "adult", "ethnicity": "default" }
  ],
  "updatedAt": "2026-04-05T..."
}
```

**No photos stored** — only metadata. Well within localStorage 5MB limit.

**Behaviour:** On upload, if a name matches an existing profile, auto-fill role/ageGroup/ethnicity. On first use, save entered profiles for next session. Profiles persist across sessions; photos do not (they're transient File objects).

**New utility:** `src/utils/familyProfiles.js` (~40 lines) with `loadProfiles()`, `saveProfile(entry)`, `matchProfile(name)`.

Effort: ~40-line utility + ~10 lines in upload flow to auto-fill on name entry.

## 6. Risk Areas

| Risk | Severity | Mitigation |
|---|---|---|
| **Breaking normalisation** | LOW | Spread operator preserves new fields. Add explicit defaults for safety. |
| **Composition engine regression** | MEDIUM | Backward-compatible: structured role is preferred, label guessing is fallback. Existing test suite covers all label-based paths. |
| **Bundle size from character picker** | LOW | Thumbnails are already imported (same PNGs used by mug preview). Picker reuses existing imports. |
| **KeepsakeCustomise scroll overflow** | MEDIUM | Adding picker below existing chips increases scroll content. Test on 375px/667px viewport. The `paddingBottom: 80` for fixed button should still work. |
| **sessionStorage cache shape change** | LOW | Analysis cache stores results only, not upload metadata. New fields flow through context, not cache. |
| **COPPA/biometric consent gate** | NONE | Role/age/ethnicity are user-entered metadata, not biometric data. No consent gate needed. |
| **Backend contract** | NONE | Role/age/ethnicity are FE-only for keepsake rendering. Backend API contract (`kinship_analyze.v1`) unchanged. |

**Blast radius:** UploadSection, FamililookContext, stateNormalization, KeepsakeCustomise, compositionEngine, characters/index. All other components unaffected.

## 7. Estimated Effort

| Component | Files Changed | New Files | Lines | Effort |
|---|---|---|---|---|
| Context schema + helpers | 2 (Context, stateNorm) | 0 | ~40 | 1h |
| Upload role/age/ethnicity fields | 1 (UploadSection or new inline sheet) | 0 | ~60 | 2h |
| Extract `getSmartSuggestions` | 2 (GroupSnapshot, new util) | 1 | ~30 | 0.5h |
| Expand `RELATIONSHIP_OPTIONS` | 1 (constants.js) | 0 | ~4 | 0.1h |
| Composition engine structured input | 2 (compositionEngine, characterHeadlines) | 0 | ~15 | 1h |
| Character picker component | 1 (new) + 2 (characters/index, KeepsakeCustomise) | 1 | ~105 | 2h |
| Family profile persistence | 0 | 1 (familyProfiles.js) | ~40 | 1h |
| Tests (unit + integration) | 3-4 new test files | 3-4 | ~200 | 3h |
| **Total** | **~10 files** | **~3 new** | **~500** | **~10h** |

**Verdict:** Fully feasible. No backend changes. No contract breaks. All reusable patterns exist. The composition engine's backward-compatible fallback means we can ship incrementally — structured role first, character picker second, profiles third.
