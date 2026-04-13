# Task: FaceFusion Regression Fix

**Date**: 2026-03-28
**Priority**: P1 — Significant (production regression, user-facing breakage)
**Raised by**: CEO
**Reason**: Rapid, uncontrolled changes to FaceFusion caused cascading regressions. Navigation broken, React crashes, stacking context leaks.

---

## What happened

10 commits were pushed to desktop2 production in a single session without proper change control:

```
af6e3b8 fix: FaceFusion tutorial overlay was blocking header back button
8d6be27 fix: FaceFusion morph — 15s timeout, start on mount, visible loading
ebdf598 fix: move useState before ALL early returns in FusePhase
5acec75 fix: move useState above early return in FusePhase (React #310 crash)
062fe95 fix: FaceFusion — real names from familyContext, onboarding, no flicker
b48e5a0 fix: FaceFusion — fix generic names in inventory, remove flickering
88d559e feat: FaceFusion v2 — modern UI, fix broken selection, bump spins
c39b2bf tweak: slow tagline rotation to 9s interval
0a09bdd feat: rotating tagline on homepage — 3 CTAs with slow pulse crossfade
b0e7e31 fix: pass tier param to FamiliMatch via Trail links
```

Last known-good commit: `a423937` (docs: add Cookie Policy page)

The first 3 commits (b0e7e31, 0a09bdd, c39b2bf) are clean — Trail tier gating and homepage tagline. The regression is in the 7 FaceFusion commits (88d559e → af6e3b8).

---

## Known issues in production

### 1. Back button (chevron) in FamiliUno header — NOT WORKING
- **Symptom**: Tapping the `<` chevron at top-left does nothing when FaceFusion tab is active
- **Root cause**: FaceFusion tutorial overlay (`position: absolute, inset: 0, zIndex: 30`) escapes the container stacking context and covers the sticky header (`zIndex: 10`). A fix was attempted (`isolation: isolate`) but not verified working.
- **File**: `src/game/FaceFusion/FaceFusion.jsx` (lines ~197-205, 237-300)

### 2. BackToTrail floating button — NOT WORKING
- **Symptom**: The fixed "Trail" button at bottom-left is unresponsive
- **Root cause**: Likely same stacking context issue, or another overlay blocking it. BackToTrail is `position: fixed, zIndex: 90` which should be above everything — needs investigation.
- **File**: `src/components/trail/BackToTrail.jsx` (already at zIndex: 90, should work)

### 3. React error #310 — MAY STILL OCCUR
- **Symptom**: "Minified React error #310" (too many re-renders / hook order violation)
- **Root cause**: FusePhase.jsx had `useState` after conditional early returns. Two fixes were applied (5acec75, ebdf598) — hook order appears correct now but needs verification under all phase transitions (merging → reveal → saved).
- **File**: `src/game/FaceFusion/FusePhase.jsx`

### 4. Generic names ("Family 5", "Family 6")
- **Symptom**: Family members show as "Family 5" instead of real names (Mum, Dad, Sarah)
- **Root cause**: Group snapshot stores faces as "Person N". A cross-reference to `fl:familyContext` was added but matching is by index position — fragile if face order doesn't match context order.
- **File**: `src/game/FaceFusion/FaceFusion.jsx` (lines ~76-108)

### 5. Face morph not producing visible blend
- **Symptom**: The "fusion" card shows one person's unmodified photo, not a blend
- **Root cause**: Backend morph (`/face/morph` on desktop3) works but has high latency. Timeout was increased to 15s and morph now starts on mount. If the morph succeeds, it should show a Delaunay-blended face. If it fails, falls back to dominant person's photo silently.
- **File**: `src/game/FaceFusion/faceCompositor.js`, `src/game/FaceFusion/FusePhase.jsx`

---

## Files changed (7 files)

| File | Lines | What changed |
|------|-------|-------------|
| `src/game/FaceFusion/faceFusionConfig.js` | 350 | Spins 3→5 for teens/adults. Added FUSION_FEATURE_COLORS, FUSION_FEATURE_ICONS, RARITY_GLOW maps |
| `src/game/FaceFusion/FaceFusion.jsx` | 452 | Tutorial overlay, name cross-referencing from familyContext, isolation: isolate, pass familyMembers to PickPhase |
| `src/game/FaceFusion/PickPhase.jsx` | 401 | COMPLETE REWRITE — chip-based feature rows replacing broken 2x4 grid |
| `src/game/FaceFusion/SpinPhase.jsx` | 435 | Rarity glow, particle burst, "PULL!" button text, RARITY_GLOW import |
| `src/game/FaceFusion/FusePhase.jsx` | 647 | Glassmorphism removed, 180px face, share button, morph-on-mount, useState moved before returns |
| `src/game/FaceFusion/faceCompositor.js` | 155 | Timeout 4s→15s |
| `src/pages/HomePage.jsx` | +32 lines | Rotating tagline (CLEAN — not related to regression) |

---

## Agent assignments

### Change Manager
1. Run a full change audit on today's 10 commits
2. Classify each by risk tier
3. Determine which commits are safe to keep vs which need revert
4. Produce a Change Request Package for CEO approval

### QA Lead
1. Run full test suite: `npm run test:run` (desktop2)
2. Run build: `npm run build`
3. Manually verify: FamiliUno page loads, all game tabs work, back button works, BackToTrail button works
4. Specifically test FaceFusion flow: ageSelect → spin → pick → fuse → save — no crashes
5. Produce a Test Health Report with Ship/Fix/Block verdict

### FE Lead
1. Review all 7 FaceFusion files for correctness
2. Verify Rules of Hooks compliance in FusePhase.jsx (all hooks before all returns)
3. Verify stacking context isolation (tutorial overlay, fullscreen toggle cannot block header or BackToTrail)
4. Fix any issues found — with diff preview and CEO approval before each edit
5. Run tests after each fix

### Recommended approach
- QA Lead runs first — establish what's actually broken vs what works
- FE Lead fixes only what QA identifies — no speculative changes
- Change Manager tracks everything
- CEO approves each fix before it's applied
- One commit per fix, tested between each

---

## Rollback plan

If fixes cannot stabilize within a reasonable timeframe:
```bash
cd /c/Users/wole/Documents/FML/famililook-desktop2
# Revert FaceFusion changes only (keep tagline + tier gating)
git revert af6e3b8 8d6be27 ebdf598 5acec75 062fe95 b48e5a0 88d559e --no-commit
git commit -m "revert: roll back FaceFusion v2 changes (regression)"
git push origin main
git checkout production && git merge main && git push origin production && git checkout main
```

This preserves the homepage tagline rotation and FamiliMatch tier gating while reverting all FaceFusion changes to their pre-session state.
