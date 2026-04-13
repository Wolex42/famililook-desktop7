# Keepsake System Fix Specification
## Version 1.0 — Pre-Code. No changes until approved.
## Date: 25 March 2026

---

## Purpose

This document describes every known issue in the keepsakes system that would prevent a customer from completing a purchase, and the exact fix for each. No code will be written until this spec is reviewed and approved.

---

## ISSUE 1: Invisible text on 5 templates (CRITICAL)

### What the customer sees
When selecting Mother's Day, Easter, Family Mug Set, or any template with a transparent background, the non-winner parent's features appear as invisible or near-invisible text. The card/mug/print looks half-empty — only the winning parent's features show.

### Root cause
Templates use `rgba(255,255,255,0.35)` (white at 35% opacity) for secondary text elements. This was designed for dark backgrounds. When backgrounds became transparent (for vendor compliance), white text on white/transparent = invisible.

The `mockupMode` ternary was meant to fix this, but:
- `mockupMode` is not passed to all templates from KeepsakesModal
- Even when passed, the default is `false`, so white text is used
- The fix should not depend on `mockupMode` at all — text should always be dark

### Affected files and exact lines

**FamilyMugTemplate.jsx** — ParentAnchor + ChildColumn sub-components:
- Line ~228: Placeholder circle initial letter `color: "#fff"` — white on transparent
- Line ~316: Child placeholder letter `color: "#fff"` — white on transparent
- Line ~363: Non-highlight feature chip bg `"rgba(255,255,255,0.03)"` — invisible
- Line ~369: Non-highlight feature label `"rgba(255,255,255,0.35)"` — invisible
- Line ~381: Non-highlight feature parent initial `"rgba(255,255,255,0.25)"` — invisible

**MothersDayTemplate.jsx**:
- Line ~155: Hero feature description `"rgba(255,255,255,0.4)"` — invisible
- Line ~189: Dad feature chip background `"rgba(255,255,255,0.04)"` — invisible
- Line ~195: Dad feature label `"rgba(255,255,255,0.35)"` — invisible
- Line ~220: Brand footer `"rgba(255,255,255,0.15)"` — invisible

**EasterCardTemplate.jsx** (InsideRight panel):
- Same pattern as MothersDayTemplate — non-winner features use the `mockupMode` ternary

**CushionTemplate.jsx**:
- Line ~118: Child placeholder initial letter `color: "#fff"` — white on transparent

**PetFamilyReport.jsx** (playful variant):
- Line ~16: When `mockupMode=true`, text is `"#FFFFFF"` on transparent — invisible

### The fix

**Principle**: Every `rgba(255,255,255,...)` in these templates becomes `rgba(0,0,0,...)` with equivalent opacity. Every `"#fff"` for text becomes `"#1a1a1a"` or theme-appropriate dark colour. No `mockupMode` conditionals for colour — colours are always dark/accent because backgrounds are always transparent or light.

**Specific changes per file:**

**FamilyMugTemplate.jsx:**
| Line | Old | New |
|------|-----|-----|
| ~228 | `color: "#fff"` | `color: "#fff"` (KEEP — this is inside a coloured gradient circle, white is correct here) |
| ~316 | `color: "#fff"` | `color: "#fff"` (KEEP — same, inside gradient circle) |
| ~363 | `mockupMode ? "rgba(0,0,0,0.03)" : "rgba(255,255,255,0.03)"` | `"rgba(0,0,0,0.04)"` |
| ~369 | `mockupMode ? "rgba(0,0,0,0.4)" : "rgba(255,255,255,0.35)"` | `"rgba(0,0,0,0.35)"` |
| ~381 | `mockupMode ? "rgba(0,0,0,0.3)" : "rgba(255,255,255,0.25)"` | `"rgba(0,0,0,0.25)"` |
| ~170 | `mockupMode ? "rgba(0,0,0,0.2)" : "rgba(255,255,255,0.15)"` | `"rgba(0,0,0,0.2)"` |

**MothersDayTemplate.jsx:**
| Line | Old | New |
|------|-----|-----|
| ~155 | `mockupMode ? "rgba(0,0,0,0.4)" : "rgba(255,255,255,0.4)"` | `"rgba(0,0,0,0.4)"` |
| ~189 | `mockupMode ? "rgba(0,0,0,0.04)" : "rgba(255,255,255,0.04)"` | `"rgba(0,0,0,0.04)"` |
| ~195 | `mockupMode ? "rgba(0,0,0,0.4)" : "rgba(255,255,255,0.35)"` | `"rgba(0,0,0,0.35)"` |
| ~220 | `mockupMode ? "rgba(0,0,0,0.2)" : "rgba(255,255,255,0.15)"` | `"rgba(0,0,0,0.2)"` |

**CushionTemplate.jsx:**
- Line ~118: `color: "#fff"` — KEEP (inside gradient circle placeholder, white is correct)

**PetFamilyReport.jsx:**
- Line ~16-18: When `mockupMode=true`, bg becomes transparent but text stays `"#FFFFFF"`. Fix: remove the mockupMode conditional entirely. The playful variant keeps its dark background for flat preview AND print (it's a paper product, not a surface product). Only the portrait variant needs to work on light backgrounds (which it already does with `"#2C2C2C"`).

**EasterCardTemplate.jsx:**
- The provided EasterCardTemplate.jsx already uses correct dark colours throughout (green palette on cream/white). No fix needed — it was written correctly from the start.

---

## ISSUE 2: Navigation blockages (MODERATE)

### What the customer sees
1. Pressing Back from the Style picker in a single-product category (e.g. Pets) jumps all the way back to the Category grid instead of going to the previous logical step
2. Pressing Back from Classic Cards mode goes to the Category grid instead of the Cards product list
3. The mockup/flat/video toggle state persists when navigating between products, causing stale views

### Root cause
`handleBack` uses current state to guess where to go back to, but when forward navigation **skips steps** (single product → skip PRODUCT, single style → skip STYLE), the back logic doesn't know what was skipped. It also doesn't reset view state (`showMockup`) when navigating away.

### The fix

**Approach**: Add a `navigationHistory` array that records each step visited during forward navigation. `handleBack` pops the last entry instead of guessing.

**Changes to KeepsakesModal.jsx:**

1. Add state: `const [navHistory, setNavHistory] = useState([]);`

2. Every forward navigation pushes the CURRENT step before changing:
```js
// In handleSelectCategory:
setNavHistory(prev => [...prev, STEPS.CATEGORY]);
// Then setStep(STEPS.PRODUCT) or setStep(STEPS.STYLE) etc.

// In handleSelectProduct:
setNavHistory(prev => [...prev, step]);
// Then setStep(STEPS.STYLE) or setStep(STEPS.PREVIEW)

// In handleSelectStyle:
setNavHistory(prev => [...prev, STEPS.STYLE]);
setStep(STEPS.PREVIEW);
```

3. `handleBack` pops the history:
```js
const handleBack = useCallback(() => {
  if (classicMode) {
    setClassicMode(false);
    // Go back to Cards product list, not Category
    setStep(STEPS.PRODUCT);
    setNavHistory(prev => prev.slice(0, -1));
    return;
  }
  if (navHistory.length > 0) {
    const previousStep = navHistory[navHistory.length - 1];
    setNavHistory(prev => prev.slice(0, -1));
    setStep(previousStep);
  } else {
    setStep(STEPS.CATEGORY);
  }
  // Reset view state when navigating away from preview
  setShowMockup(false);
}, [classicMode, navHistory]);
```

4. Reset history when modal opens/closes:
```js
// In the isOpen effect or reset logic:
setNavHistory([]);
setShowMockup(false);
```

### Specific navigation paths after fix

| Path | Before | After |
|------|--------|-------|
| Pets → Style → Back | Jumps to Category | Goes to Category (correct — only 1 product, no product list to show) |
| Cards → Standard Card → Back (classicMode) | Category grid | Cards product list |
| Cards → Card Deck → Back (classicMode) | Category grid | Cards product list |
| Preview (with mockup) → Back → new product | Stale mockup state | Reset to flat view |
| Drinkware → Mug (single style) → Preview → Back | Goes to PRODUCT list | Goes to PRODUCT list (correct) |

---

## ISSUE 3: Export background colours inconsistent (MODERATE)

### What the customer sees
Downloads a PNG and the background is wrong — black for paper products that should be white, or white for fabric products that should be transparent.

### Current state
`printExport.js` uses:
```js
const paperProducts = ["standard_card", "card_deck", "greeting_card", "postcard", "fine_art_print", "pet_family_report"];
const bgColor = paperProducts.includes(productType) ? "#FFFFFF" : "transparent";
```

### Issues
- `framed_canvas` is NOT in the paper list → exports as transparent (correct for canvas)
- `mug_wrap` is NOT in the paper list → exports as transparent (correct)
- `tshirt_print` and `baby_bodysuit` → transparent (correct)
- `cushion` → transparent (correct)
- `family_mug_set` → transparent (correct)

**This is actually correct now.** No change needed. But I need to verify it matches what each vendor expects:

| Product | Current export bg | Vendor expects | Match? |
|---------|-------------------|---------------|--------|
| standard_card | #FFFFFF | White (paper card) | YES |
| card_deck | #FFFFFF | White (paper card) | YES |
| greeting_card | #FFFFFF | White (paper card) | YES |
| postcard | #FFFFFF | White (paper card) | YES |
| fine_art_print | #FFFFFF | White (paper) | YES |
| pet_family_report | #FFFFFF | White (paper) | YES |
| mug_wrap | transparent | Transparent (ceramic surface) | YES |
| family_mug_set | transparent | Transparent (ceramic surface) | YES |
| tshirt_print | transparent | Transparent (fabric DTG) | YES |
| baby_bodysuit | transparent | Transparent (fabric DTG) | YES |
| cushion | transparent | Transparent (fabric) | YES |
| framed_canvas | transparent | Transparent (canvas) | YES |
| jigsaw_puzzle | transparent | Transparent (chipboard) | VERIFY — puzzle may need white |

**Action**: Verify with Prodigi whether jigsaw puzzle expects white or transparent. For now, leave as transparent.

---

## ISSUE 4: BodysuitTemplate fragile `dominantFeature` field (LOW)

### What the customer sees
Baby bodysuit or t-shirt always shows "Eyes" as the featured trait, even if a different feature is the strongest match.

### Root cause
`BodysuitTemplate` reads `data.dominantFeature` (line 13), which is set by `useKeepsakeData`. The field IS populated — it's the first winner feature. But if the hook returns data without it (edge case), the template defaults to "eyes".

### The fix
No code change. This is working correctly. `useKeepsakeData` always sets `dominantFeature` from the first winner feature key. The fallback to "eyes" is a safe default. Document this in the component JSDoc comment.

---

## ISSUE 5: PostcardBackTemplate not registered (LOW)

### What the customer sees
Nothing — postcards only show the front, which is correct for the customer preview. The back template exists but isn't used in the keepsakes flow.

### The fix
No code change for now. The back template could be wired into a "Print Layout" view (like Easter's 4-panel) in future, but it's not a customer-facing issue today.

---

## ISSUE 6: `previewStyleProp` not yet in KeepsakesModal (MODERATE)

### What the customer sees
Easter greeting card preview may show the wrong panel — the full 4-panel print layout instead of just the inside panel.

### Root cause
The provided KeepsakesModal.jsx has `getPreviewStyleVariant()` and `previewStyleProp` which maps `easter` → `easter_inside` for preview. I added the import and memo but the createElement calls in the preview area may not all use `previewStyleProp` yet.

### The fix
Verify that EVERY `React.createElement(resolvedComponent, ...)` in the preview-visible areas uses `style: previewStyleProp` (not `selectedStyle`), while every `React.createElement` in the hidden `cardRef` area uses `style: selectedStyle` (for export).

Specifically:
- Style picker preview (Step 3): use `previewStyleProp`
- Flat Design view (visible): use `previewStyleProp`
- Product Preview / Mockup view (visible): use `previewStyleProp`
- 3D Video view (visible part is video, not template)
- Hidden `cardRef` off-screen (all views): use `selectedStyle`

---

## Execution Order

1. **Fix Issue 1** (invisible text) — biggest customer impact, same pattern across all files
2. **Fix Issue 2** (navigation) — second biggest frustration
3. **Fix Issue 6** (previewStyleProp) — Easter card rendering
4. **Verify Issue 3** (export backgrounds) — confirm no changes needed
5. **Skip Issues 4 & 5** — not customer-facing

## What I will NOT change

- Template dimensions (already corrected to vendor specs)
- MugWrapTemplate (already rebuilt to spec)
- MugCeramicPreview (working correctly)
- EasterCardTemplate (written correctly from the start)
- printProfiles.js (already corrected)
- Legacy card templates (working correctly)
- CertificateTemplate, GreetingCardTemplate, PostcardTemplate (working correctly)

---

*No code until this spec is approved.*
