# Task Briefing: KS-01 — Character Mug Crash Fix
**Agent:** FE Lead Alpha
**Track:** Parallel A
**Date:** 2026-04-07
**Risk Tier:** P1 — Significant (production crash, user-facing)
**Audit Reference:** KS-01 (CRITICAL)

---

## Mission

Fix a confirmed production crash in the character mug keepsake flow. When a user selects the `gran_loving_african` character variant, `getCharacterImage()` returns `null` because the emotion images for that character are not imported in the character index. This null propagates to an `<img>` src, which crashes the render tree and triggers the ErrorBoundary.

---

## Working Set (ONLY these files may be edited)

```
famililook-desktop2/src/assets/characters/index.js
famililook-desktop2/src/components/keepsakes/mobile/CharacterPicker.jsx
```

No other files. If you discover the fix requires touching any other file, STOP and escalate to the orchestrator.

---

## What You Must Read First (before writing any code)

1. `src/assets/characters/index.js` — read the ENTIRE file. Map every character that IS imported and identify the pattern used (naming convention, file paths, emotion variants).
2. `src/components/keepsakes/mobile/CharacterPicker.jsx` — read fully. Understand how `getCharacterImage()` is called and what it expects.
3. `src/assets/characters/` — list the directory. Verify which image files physically exist on disk vs what is imported in index.js.

**Do not assume. Read first. The gap between what exists on disk and what is imported is the bug.**

---

## Root Cause (from audit)

`assets/characters/index.js` lines 58-66: `gran_loving_african` emotion images are missing from the import map. `getCharacterImage()` returns `null` for this character. `CharacterPicker.jsx:54` renders `<img src={null}>` which crashes React rendering.

---

## What the Fix Must Do

1. **Identify all missing character/emotion combinations** — do not just fix `gran_loving_african`. Read the full index.js and compare against files on disk. Fix ALL gaps in one pass.
2. **Add the missing imports** to `assets/characters/index.js` following the exact existing pattern.
3. **Add a null guard** in `CharacterPicker.jsx` — if `getCharacterImage()` returns null for any reason, render a fallback placeholder rather than crashing. This is a defensive fix; the import fix is the primary fix.

The null guard pattern:
```jsx
// BEFORE (crashes on null)
<img src={getCharacterImage(character, emotion)} />

// AFTER (defensive)
const imgSrc = getCharacterImage(character, emotion);
{imgSrc ? (
  <img src={imgSrc} alt={`${character} ${emotion}`} />
) : (
  <div className="w-full h-full bg-violet-100 rounded-full flex items-center justify-center">
    <span className="text-2xl">👤</span>
  </div>
)}
```

---

## Pre-Edit Checklist (NON-NEGOTIABLE)

Before touching any file:
- [ ] Run: `python .claude/validate_scope.py "src/assets/characters/index.js" --mode edit`
- [ ] Run: `python .claude/validate_scope.py "src/components/keepsakes/mobile/CharacterPicker.jsx" --mode edit`
- [ ] Both return exit 0

Before each edit:
- [ ] Show exact old_string and new_string diff preview
- [ ] Wait for CEO explicit approval
- [ ] Apply edit only after approval

After all edits:
- [ ] Hook import verification: `grep -E "use[A-Z][a-zA-Z]+" src/components/keepsakes/mobile/CharacterPicker.jsx | grep -v "^import"`
- [ ] No display:none used for responsive hiding
- [ ] `npm run test:run` — must PASS
- [ ] `npm run build` — must PASS

---

## Tests to Write

Add or update a test in the character mug test suite that:
1. Renders `CharacterPicker` with `character="gran_loving_african"` and every emotion variant
2. Asserts no crash (component renders without throwing)
3. Asserts the image src is not null

If no existing test file covers CharacterPicker, create one at:
`src/components/keepsakes/mobile/__tests__/CharacterPicker.test.jsx`

---

## Definition of Done

- [ ] All missing character/emotion imports added to index.js
- [ ] Null guard added to CharacterPicker.jsx
- [ ] Directory scan confirms no other characters have missing imports
- [ ] Test written and passing
- [ ] `npm run test:run` PASS
- [ ] `npm run build` PASS
- [ ] Diff preview shown and CEO approved before each edit
- [ ] Change log entry added to `.claude/change_log.md`
- [ ] Mark as: **FIXED — verified by build + tests. Mobile device verification pending CEO.**

---

## Handoff to QA Lead (after done)

```
HANDOFF: FE Lead Alpha → QA Lead
Task: KS-01 Character Mug Crash
Files changed:
  - src/assets/characters/index.js (imports added)
  - src/components/keepsakes/mobile/CharacterPicker.jsx (null guard added)
Test evidence: <paste npm run test:run output>
Build: PASS
Open items: Mobile device verification — CEO must confirm on physical device
```

---

## Constraints

- Do NOT edit any file outside the working set
- Do NOT add new npm dependencies
- Do NOT modify backend files
- Do NOT use display:none for any responsive logic
- If CharacterPicker.jsx has been patched 2+ times before (check change_log) — STOP and issue Two-Attempt Halt before proceeding
