# Task Briefing: Character Mug Crash — React #426
**Agent:** FE Lead (Crash Fix)
**Track:** Sequential — activates AFTER Platform Architect assessment + CEO gate
**Date:** 2026-04-07
**Risk Tier:** P1 — protected files involved
**Parent bug:** CEO report 2026-04-07

---

## STOP — Prerequisites

Before reading anything else:
1. Platform Architect assessment must be complete
2. CEO must have approved scope (Option A, B, or C)
3. Your working set is defined by that approval — do not assume it

This briefing describes the full fix. Your actual working set is whatever CEO approved.

---

## Context

React error #426 ("Objects are not valid as a React child") fires when the user presses the character mug preview. The investigation confirmed:

- `CharacterPicker` correctly collects character + emotion selection
- `KeepsakeMobileFlow` stores it as `characterOverride` state
- `CharacterMugTemplate.jsx` calls `composeCharacterMug()` without passing `characterType` or `characterEmotion`
- `compositionEngine.js` builds a plan using defaults, a layout function returns a plain JS object `{}` somewhere in that plan
- React tries to render `{plan.something}` where something is an object → crash #426

The analysis results (winner, features, percentages) that should feed the character auto-selection are also disconnected — but that is a UX task handled separately. This task fixes the crash only.

---

## What You Must Read First

Read every file in your approved working set in full before writing any code. In particular:

1. `KeepsakeMobileFlow.jsx` — find exactly where `characterOverride` is in state and exactly where it is (or isn't) passed to `CharacterMugTemplate`
2. `CharacterMugTemplate.jsx` — find the `composeCharacterMug()` call. Read its full prop signature.
3. `compositionEngine.js` (if in approved scope) — read `composeCharacterMug()`. Find what it returns when `characterType` is undefined. Find the layout function that returns a plain object.

**Do not write any code until you have traced the full prop chain and know exactly where to insert each change.**

---

## The Fix (adjust to match CEO-approved scope)

### Part 1 — Thread the prop (always required)

In `KeepsakeMobileFlow.jsx`, find where `CharacterMugTemplate` (or the component that renders it) is called. Add `characterOverride` to the props passed:

```jsx
// BEFORE — characterOverride dropped
<CharacterMugTemplate
  data={data}
  occasion={occasion}
  recipient={selectedRecipient}
  variant={selectedVariantOverride}
/>

// AFTER — characterOverride threaded through
<CharacterMugTemplate
  data={data}
  occasion={occasion}
  recipient={selectedRecipient}
  variant={selectedVariantOverride}
  characterType={characterOverride?.character}
  characterEmotion={characterOverride?.emotion}
/>
```

In `CharacterMugTemplate.jsx`, find the `composeCharacterMug()` call. Add the missing props:

```javascript
// BEFORE
const plan = composeCharacterMug({
  data,
  occasion,
  recipient,
  variant,
});

// AFTER
const plan = composeCharacterMug({
  data,
  occasion,
  recipient,
  variant,
  characterType,   // from props
  characterEmotion, // from props
});
```

Ensure `CharacterMugTemplate` receives and destructures these props at the top of the component.

### Part 2 — Engine null guard (if CEO approved Option B)

In `compositionEngine.js`, find `composeCharacterMug()`. Add defensive defaults so missing `characterType` or `characterEmotion` never produces a plain object in the returned plan:

```javascript
// Pattern — defensive default on entry
function composeCharacterMug({ data, occasion, recipient, variant, characterType, characterEmotion }) {
  const safeCharacterType = characterType ?? 'default';
  const safeCharacterEmotion = characterEmotion ?? 'neutral';
  // use safeCharacterType and safeCharacterEmotion throughout
  // ...
}
```

Also find the specific layout function that returns a plain object instead of a string/element. Add a guard:

```javascript
// Pattern — wherever a plain object {} may be returned as a renderable value
const value = someLayoutFunction(plan.section);
// If value is an object, it cannot be a React child — render nothing or a fallback
const safeValue = typeof value === 'string' || typeof value === 'number' ? value : '';
```

**Do not change any layout logic — only add null/type guards. If you find yourself rewriting layout logic, STOP and escalate.**

---

## Pre-Edit Checklist (NON-NEGOTIABLE)

Before touching any file:
- [ ] Platform Architect assessment received: YES
- [ ] CEO scope approval received: Option A | B | C
- [ ] Working set confirmed — matches CEO approval exactly
- [ ] `python .claude/validate_scope.py "<file>" --mode edit` run for each file — exit 0
- [ ] Patch count verified for each file — none at 3+ patches

Before each edit:
- [ ] Show exact old_string and new_string diff preview
- [ ] Wait for CEO explicit approval
- [ ] Apply edit only after approval

After all edits:
- [ ] Hook import verification on every modified file
- [ ] `npm run test:run` — must PASS
- [ ] `npm run build` — must PASS
- [ ] Verify the specific error path: render `CharacterMugTemplate` with a characterOverride value and confirm no #426 error

---

## Tests to Write

In the CharacterMugTemplate test file:

1. **With characterOverride**: render with `characterType="gran"` and `characterEmotion="loving"` → no crash, renders without error
2. **Without characterOverride (defaults)**: render with no characterType/characterEmotion → no crash, renders with defaults
3. **composeCharacterMug returns renderable values**: every field in the returned plan is a string, number, null, or React element — never a plain object

---

## Definition of Done

- [ ] `characterType` and `characterEmotion` props threaded from KeepsakeMobileFlow → CharacterMugTemplate → composeCharacterMug
- [ ] Engine null guard added (if Option B approved)
- [ ] Plain object return caught (if Option B approved)
- [ ] No layout logic changed — only prop threading and type guards
- [ ] Tests pass for both with-override and without-override cases
- [ ] `npm run test:run` PASS
- [ ] `npm run build` PASS
- [ ] Diff preview shown and CEO approved before each edit
- [ ] Change log entry added
- [ ] Marked: **CRASH FIX APPLIED. Mobile device verification required — CEO must confirm preview no longer crashes.**

---

## Constraints

- Do NOT change any visual layout, colours, or copy — UX improvements are a separate task
- Do NOT change winner/percentage logic
- Do NOT add new npm dependencies
- Do NOT modify backend files
- Do NOT touch `KeepsakesModal.jsx` — that file has its own patch history and is out of scope
- If compositionEngine.js is NOT in approved scope, add zero changes to it — even if you spot other issues. Log them for Platform Architect instead.
