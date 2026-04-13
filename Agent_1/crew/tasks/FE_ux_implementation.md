# Task Briefing: Character Mug UX Implementation
**Agent:** FE Lead (UX Implementation)
**Track:** Sequential — activates AFTER Visual Director spec + Copywriter bank are both complete and CEO has reviewed them
**Date:** 2026-04-07
**Risk Tier:** P2 — Standard
**Dependency:** Crash fix (FE_crash_fix_character_mug.md) must be merged first

---

## Prerequisites

Before writing any code:
- [ ] Crash fix is merged (React #426 is resolved)
- [ ] Visual Director spec exists: `crew/output/VISUAL_DIRECTION_character_mug_ux.md`
- [ ] Copywriter copy bank exists: `crew/output/COPY_BANK_character_mug_ux.md`
- [ ] CEO has reviewed both specs
- [ ] You have read both documents completely

If either spec is missing or unclear, STOP. Do not improvise design values. Return to Visual Director or Copywriter.

---

## Working Set

To be confirmed after reading specs — expected files:

```
famililook-desktop2/src/components/keepsakes/mobile/KeepsakeCustomise.jsx
famililook-desktop2/src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx  (if bridge moment needs state)
famililook-desktop2/src/components/keepsakes/mobile/KeepsakePreview.jsx     (if CTA position changes here)
```

Run scope validation on each before editing. If any file has been patched 2+ times — issue Two-Attempt Halt before proceeding.

---

## What You Are Building

Three UI elements, all specced by Visual Director, all copy from Copywriter:

**Element 1 — Product Explanation Moment**
A dismissable UI element (card/banner/modal — per VD spec) shown when the user is in the character mug flow, explaining what the product is. Shown once per session or permanently dismissed after first view (per VD spec).

**Element 2 — Results-to-Character Bridge**
A contextual chip/card shown when analysis results exist, connecting the winner/percentage to the character selection. Hidden when no results are available (user came directly, not from results).

**Element 3 — Preview CTA Position Fix**
Reposition the preview/add-to-basket CTA per Visual Director's recommendation (sticky bar or moved higher — implement exactly what VD specced).

---

## Implementation Rules (NON-NEGOTIABLE)

**Rule 1 — Implement to spec exactly**
Every colour, dimension, font, spacing value comes from the Visual Director spec. If the spec says `#7C3AED` at `16pt Inter Bold`, that is what you implement. Do not substitute, approximate, or improve.

**Rule 2 — Copy from copy bank exactly**
Every string comes from the Copywriter's copy bank. Use the exact characters, including capitalisation and punctuation. Template variables use `{variable}` notation — replace at render time with the actual data. Do not rephrase.

**Rule 3 — Tailwind only (these are UI elements, not print templates)**
All three elements are UI components, not print/export templates. Use Tailwind classes. No inline styles.

**Rule 4 — Results bridge requires real data**
The bridge element reads from context (`analysisResults`, `winner`, `winnerPct`, `childName`). Do not fabricate or hardcode values. If the data isn't available (no analysis run), render nothing — graceful omission, not a blank box.

**Rule 5 — Dismissal state**
The product explanation moment must be dismissable. Persist dismissal in `sessionStorage` (one session) or `localStorage` (permanent — per VD spec). Use `safeSessionSet`/`safeSessionGet` pattern if ErrorBoundary fix is already merged (it provides safe wrappers).

**Rule 6 — Touch targets**
All interactive elements (dismiss button, CTA) must meet 44pt minimum touch target. This is iOS HIG compliance — non-negotiable.

**Rule 7 — Safe area insets on sticky bar**
If VD specced a sticky bottom bar: add `paddingBottom: calc(16px + env(safe-area-inset-bottom))` and add `paddingBottom: 88px` (or the bar height) to the scroll container so content isn't hidden behind the bar.

---

## Pre-Edit Checklist (NON-NEGOTIABLE)

Before touching any file:
- [ ] Visual Director spec read completely
- [ ] Copywriter copy bank read completely
- [ ] `python .claude/validate_scope.py "<file>" --mode edit` — exit 0 for each file
- [ ] Patch count check — no file at 2+ patches without explicit approval
- [ ] No design decisions left to make (if any value is unspecified, return to VD)

Before each edit:
- [ ] Show exact old_string and new_string diff preview
- [ ] Wait for CEO explicit approval
- [ ] Apply edit only after approval

After all edits:
- [ ] Hook import verification on every modified file
- [ ] No display:none for responsive hiding — conditional rendering only
- [ ] `npm run test:run` — must PASS
- [ ] `npm run build` — must PASS
- [ ] Mobile items: mark as **UNVERIFIED on device** — CEO must confirm

---

## Tests to Write

1. **Product explanation moment**: renders when `product === 'character_mug'`, does not render for other products
2. **Dismissal**: after dismiss clicked, element not rendered; state persisted correctly
3. **Results bridge**: renders when `winner` and `winnerPct` exist in context; does NOT render when no results
4. **Bridge copy**: template strings interpolated correctly with real data values
5. **CTA position**: CTA element present in DOM; for sticky bar — has correct class/style for fixed positioning

---

## Definition of Done

- [ ] All three elements implemented exactly to Visual Director spec
- [ ] All copy from Copywriter copy bank (exact strings, no rewrites)
- [ ] Results bridge reads from real context data (no hardcoded values)
- [ ] Dismissal persisted correctly
- [ ] Sticky bar (if applicable) has safe area insets and content padding
- [ ] Touch targets ≥ 44pt on all interactive elements
- [ ] All tests passing
- [ ] `npm run test:run` PASS
- [ ] `npm run build` PASS
- [ ] Change log entry added
- [ ] Marked: **UX ELEMENTS APPLIED. UNVERIFIED on device — CEO must confirm on physical phone.**

---

## What to Flag if You Find It

While implementing, if you notice:
- Any other copy that contradicts or clashes with the new bridge text → flag to Copywriter, do not fix inline
- Any other layout issue in KeepsakeCustomise beyond the three specced elements → log it, do not fix inline
- Plan gate silent close (KS-07) — if a free user reaches the CTA, what happens? Flag to orchestrator if the behaviour is still broken → separate task

Do NOT fix things you weren't asked to fix. Log them and stay in scope.
