# PRD: Family Identity Profiles

**Status:** Draft  
**Author:** CPO (Agent)  
**Date:** 2026-04-05  
**Product:** FamiliLook (desktop2 FE)  
**Dependencies:** compositionEngine.js, characterHeadlines.js, PhotoSlot.jsx, constants.js

---

## Problem

In the individual upload flow (`/app`), users label photos with free text ("Parent A", "Child"). The composition engine resolves these via `normaliseParent()` string matching against ~80 aliases. This fails silently for given names ("Sarah" defaults to mama, "Alex" defaults to mama, "Kwame" defaults to custom). Users never explicitly choose which character illustration represents their family. Age and ethnicity are not captured in individual mode at all — both are only available in group photo mode via backend `/detect`.

**Result:** Character mugs default to generic mama/papa illustrations. Products feel impersonal. Users have no reason to return for a second product because the system doesn't remember their family.

## Goal

Maximise character illustration accuracy by capturing structured identity data per family member: **role**, **name**, **age bracket**, and **visual variant** (ethnicity). Store profiles in localStorage so returning users see "Welcome back — your family is ready."

---

## 1. User Flow

**When:** After photo upload, before "Analyse" tap. Each PhotoSlot gains an "Edit profile" affordance.

| Step | Trigger | What happens |
|------|---------|-------------|
| 1 | User uploads photo to a slot | Slot shows photo thumbnail + current label (free text, as today) |
| 2 | User taps the label area OR a new "pencil" icon | **Identity Sheet** slides up (bottom sheet, same pattern as FaceNamingSheet) |
| 3 | User fills in role, name, age bracket, variant | Sheet saves on dismiss or "Done" tap |
| 4 | Slot label updates to show name + role badge (e.g. "Sarah" with a "Mum" chip) |
| 5 | User taps "Analyse" | Structured profile data flows into context alongside photo |

**Key constraint:** The sheet is optional. If the user skips it, the existing free-text label + normaliseParent() path is unchanged. Zero friction added to the happy path.

## 2. Interaction Design — Identity Sheet

The Identity Sheet is a half-screen bottom sheet (consistent with FaceNamingSheet in group mode).

### Layout (top to bottom)

1. **Photo thumbnail** (48px circle, left-aligned) + slot label as editable text field (right of thumbnail)
2. **Role picker** — horizontal scrollable chip row. Pre-populated from `RELATIONSHIP_OPTIONS`. First chip = "Auto" (use normaliseParent on the name). Selected chip is filled violet.
3. **Name input** — single text field, placeholder "Name (optional)". Pre-filled from slot label if already set.
4. **Age bracket** — 4 segmented-control options: `Child` (0-12), `Teen` (13-17), `Adult` (18-59), `Senior` (60+). Default = Adult for parent slots, Child for child slots.
5. **Visual variant** — 2-3 large circular preview thumbnails showing the character illustration that WILL appear on their mug. Each shows the character type (derived from role) in the variant skin tone. Tap to select. Initially: "Default" and "African". Extensible for future sets.
6. **"Done" button** — dismisses the sheet. Also dismisses on swipe-down or background tap.

### Smart defaults

- If role = "Mum" and variant = "African", the preview shows `mama_african_proud.png`
- If the user types a name but skips role, `normaliseParent(name)` runs silently to pre-select the role chip (existing alias matching). If no match, "Auto" stays selected.
- Age bracket defaults based on slot type: parent slots default to Adult, child slots default to Child.

## 3. Data Model

### Per-member profile object

```
FamilyMemberProfile {
  slotId:       string       // "parent1" | "parent2" | "child0" | "child1" ...
  name:         string       // Free text, e.g. "Sarah"
  role:         string       // From RELATIONSHIP_OPTIONS or "auto"
  ageBracket:   string       // "child" | "teen" | "adult" | "senior"
  variant:      string       // "default" | "african" | future variants
  photoDataUrl: string       // Existing photo blob URL (unchanged)
}
```

### Storage

- **Session state:** Stored in `FamililookContext` alongside existing photo/label state. New field: `familyProfiles: Record<slotId, FamilyMemberProfile>`.
- **Persistent profiles:** Saved to localStorage key `fl:familyProfiles` as a JSON array. Keyed by name+role combination (not slot ID, since slots change per session). Max 20 profiles retained.
- **Migration:** Existing sessions with only free-text labels continue to work. `familyProfiles` is undefined/null = use legacy path.

### Flow to composition engine

The composition engine's `input` object gains an optional `profile` field:

```
input.profile = {
  role:       "mum",          // normalised from structured role
  ageBracket: "adult",
  variant:    "african"
}
```

If `input.profile` exists, `selectCharacter()` uses `profile.role` directly (bypassing `normaliseParent()` on the label). If `input.profile.variant` is set, it overrides the occasion-based variant logic.

## 4. Matching Algorithm — Character Selection Priority

When `input.profile` is present, the character illustration is selected by this priority chain:

| Priority | Source | Determines | Fallback |
|----------|--------|-----------|----------|
| 1 | `profile.role` | Character type via ROLE_TO_CHARACTER | normaliseParent(label) |
| 2 | `profile.ageBracket` | Validates character type (e.g. role=Son + age=Senior is contradictory — flag but allow) | Slot type default |
| 3 | `profile.variant` | Illustration variant (default, african) | Occasion-based (AFRICAN_OCCASIONS) |
| 4 | `input.occasion` | Emotion selection (proud, celebrating, etc.) | "generic" |
| 5 | `input.recipient` | Emotion override layer | "unknown" |

**Age bracket validation rules:**
- Child/Teen + parent role (Mum, Dad) = warn but allow (young parents exist)
- Senior + child role (Son, Daughter) = suggest role change to Grandma/Grandad
- These are soft suggestions, not blocks

**Variant selection truth table:**
| Profile variant | Occasion | Result |
|----------------|----------|--------|
| "african" | any | african |
| "default" | heritage_gold/carnival_spirit/ubuntu | african (occasion override) |
| "default" | any other | default |
| not set | AFRICAN_OCCASIONS | african |
| not set | any other | default |

Note: When a user explicitly picks "default" variant, the occasion should NOT override to african. Only when variant is unset does the occasion logic apply. This requires distinguishing "user chose default" from "no choice made" — use `null` for unset, `"default"` for explicit choice.

## 5. Repeat Use Incentive

### Returning user experience

1. On app load, check `fl:familyProfiles` in localStorage.
2. If profiles exist, show a soft banner above the upload slots: **"Welcome back! Your family is ready."** with profile avatars (character illustration thumbnails, not photos).
3. Upload slots pre-fill with saved names and role badges. User just needs to add/change photos.
4. After analysis + keepsake creation, update the profile's "last used" timestamp.

### Growth hooks

- "Add another family member" prompt after first product — each new member means a new mug/deck possibility.
- "Make one for [name]" — pre-fill a new session with a saved profile as the recipient.
- Saved profiles power future features: FamiliVault (family tree), FamiliTrail (heritage journey), birthday reminders.

### Data hygiene

- Profiles expire after 90 days of inactivity (no `lastUsed` update).
- User can delete profiles from a "My Family" section (future, Phase 2).
- No photos are persisted — only name, role, age bracket, variant. GDPR-safe.

## 6. Backward Compatibility

| Scenario | Behaviour |
|----------|----------|
| User skips Identity Sheet entirely | Free-text label flows through normaliseParent() as today. Zero regression. |
| User sets role but not name | Role used for character selection, label used for headlines. |
| User sets name but not role | normaliseParent(name) attempted. If no match, defaults to mama/papa by slot type. |
| Existing saved sessions (pre-feature) | `familyProfiles` is undefined. Legacy path used. No migration needed. |
| Group photo mode | Unchanged. FaceNamingSheet already captures role. Future: merge profile data from individual mode into group mode naming. |

## 7. Scope Boundaries

### Phase 1 — Minimum (ship first)

- Identity Sheet UI (bottom sheet with role chips, name input, age bracket selector, variant selector)
- Profile data flows into FamililookContext
- compositionEngine.js reads `input.profile` for character selection
- localStorage persistence of profiles (`fl:familyProfiles`)
- "Welcome back" banner for returning users
- Existing free-text path remains fully functional

**Not in Phase 1:** No backend changes. No new illustrations. No new API fields.

### Phase 2 — Delight (ship after validation)

- Character illustration preview in the Identity Sheet (live preview of the mug character as user picks role + variant)
- "My Family" management screen (edit/delete saved profiles)
- Profile sharing across products (FamiliUno deck personalisation, FamiliMatch)
- Additional variant sets beyond default/african (e.g. East Asian, South Asian)
- Age-specific character sub-variants (teen versions of cub/mini)
- Birthday field capture for occasion-aware prompts ("It's Sarah's birthday next week — make her a mug!")
- Profile data flows into group photo mode (pre-fill FaceNamingSheet with saved profiles)

---

## Success Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| % of sessions with structured profile data | 0% | 40% within 30 days |
| Character illustration accuracy (correct role match) | ~60% (alias matching) | 90%+ |
| Returning user rate (2nd session within 14 days) | unknown | 15% |
| Keepsake products per session | 1.0 | 1.3 (more family members = more products) |

---

## Open Questions

1. Should variant selection be per-family (all members share a variant) or per-member? Per-member is more flexible but adds complexity to mug composition when multiple characters appear.
2. Should we capture gender explicitly, or infer it from role? Current ROLE_TO_CHARACTER already maps roles to gendered characters. Explicit gender adds a field but handles edge cases (non-binary presentation).
3. How do we handle the "Parent A / Parent B" default labels when the user hasn't opened the Identity Sheet? Keep as-is (normaliseParent defaults to mama) or prompt more aggressively?
