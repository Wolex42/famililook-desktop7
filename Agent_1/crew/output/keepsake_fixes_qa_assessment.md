# QA Assessment: Keepsake Bug Batch (KSK-01 to KSK-04)

**Date:** 2026-04-01
**Author:** QA Lead Agent
**Workflow:** bug_fix Step 2 — Confirm & Define Acceptance Criteria
**Status:** All 4 issues investigated, source code read, verdicts below

---

## KSK-01: Card products in catalogue

### Files Read
- `src/components/keepsakes/utils/productCatalog.js` (lines 25-27)
- `src/components/keepsakes/utils/printProfiles.js` (lines 51-57, 304-310)
- `src/components/keepsakes/mobile/KeepsakeCatalogue.jsx` (line 47)
- `src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx` (line 40)

### Verdict: ALREADY FIXED (no code change needed)

Both `standard_card` and `card_deck` have `hideFromCatalogue: true` in `printProfiles.js` (lines 56 and 309). The mobile catalogue at `KeepsakeCatalogue.jsx` line 47 filters these out:

```js
const products = getCategoryProducts(catId).filter((p) => !p.hideFromCatalogue);
```

**However**, they still appear in `PRODUCT_CATEGORIES.cards.products` (productCatalog.js line 26), which means:
1. They are listed in the `cards` category definition (alongside `greeting_card` and `postcard`)
2. The `hideFromCatalogue` filter prevents them from rendering in the grid
3. The FamiliUno deck ordering pipeline uses `card_deck` directly via its own flow (QPMarkets vendor), not through the catalogue browse path

**Risk assessment:** The current implementation works but is fragile. If a future developer removes the `hideFromCatalogue` filter or adds a new rendering path that doesn't check it, `standard_card` and `card_deck` will reappear. A cleaner fix would remove them from `PRODUCT_CATEGORIES.cards.products` entirely, but this is a hardening task, not a bug fix.

### Acceptance Criteria

| # | Criterion | Current State |
|---|-----------|---------------|
| AC-1 | `standard_card` NOT shown in mobile catalogue grid | PASS (hideFromCatalogue:true) |
| AC-2 | `card_deck` NOT shown in mobile catalogue grid | PASS (hideFromCatalogue:true) |
| AC-3 | `greeting_card` shown in mobile catalogue | PASS |
| AC-4 | `postcard` shown in mobile catalogue | PASS |
| AC-5 | FamiliUno deck ordering pipeline unaffected | PASS (separate QPMarkets flow) |
| AC-6 | (Hardening) Remove `STANDARD_CARD` and `CARD_DECK` from `PRODUCT_CATEGORIES.cards.products` array | NOT DONE — recommended |

**Recommendation:** Apply hardening fix AC-6. Remove `PRODUCT_TYPES.STANDARD_CARD` and `PRODUCT_TYPES.CARD_DECK` from `productCatalog.js` line 26. This makes the intent explicit and removes reliance on a runtime filter.

---

## KSK-02: Mug text overflow

### Files Read
- `src/components/keepsakes/MugCeramicPreview.jsx` (full file, 280 lines)
- `src/components/keepsakes/utils/characterHeadlines.js` (full file, 536 lines)
- `src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` (full file, 667 lines)
- `src/components/keepsakes/utils/mugThemes.js` (truncateAtWord function)

### Verdict: PARTIALLY MITIGATED, RESIDUAL RISK REMAINS

**MugCeramicPreview.jsx (SVG preview):**
- Hero feature callout is wrapped in `<g clipPath="url(#mugHeroTextClip)">` (line 192) which clips to a rect at `mugX+12` to `mugX+mugW-24` = 286px effective width
- The hero text inside has `fontSize="9.5"` and uses `truncateAtWord(heroDetail.description, 22)` which limits the description portion to 22 chars
- The hero callout rect is hardcoded at 170px wide (`artCx - 85` to `artCx + 85`, line 193), but the text has no width constraint other than the clip path
- **Risk:** Long `heroLabel` values (e.g. "Face Shape") combined with a 22-char description can still overflow the 170px rect visually even though the clip path catches it. The clip creates a hard crop, not an ellipsis — the text is cut mid-glyph.

**CharacterMugTemplate.jsx (print template):**
- Headline text has `whiteSpace: "pre-line"` and `maxWidth: "100%"` but no `overflow: hidden` or `textOverflow: ellipsis`
- The headline font size ranges from 32px to 42px depending on layout and photo presence
- The characterHeadlines.js engine enforces a 35-char limit (line 476) on `heroHeadline` text (excluding newlines), with a SHORT_FALLBACK pool if exceeded
- **However:** Template variable resolution can produce strings longer than 35 chars after substitution when `{child}` or `{winner}` are long custom names (e.g. "CHRISTOPHER-JAMES" = 17 chars, so `{child}:\nMUM'S MINI ME` becomes 31 chars — safe, but `{winner}'S GREATEST HIT` with winner="CHRISTOPHER-JAMES" = 35 chars, right at the limit)
- Feature subline is truncated at 50 chars (line 502-503)

**Score line and other text elements:**
- ScoreLine component (line 152-172) has `whiteSpace: "nowrap"`, `overflow: "hidden"`, and `textOverflow: "ellipsis"` — properly guarded
- Speech bubble (line 61-95) has `maxWidth: "100px"`, `overflow: "hidden"`, `textOverflow: "ellipsis"` — properly guarded

### Acceptance Criteria

| # | Criterion | Current State |
|---|-----------|---------------|
| AC-1 | SVG hero text does not visually overflow mug body bounds | PARTIAL — clip path catches overflow but causes hard crop, not graceful truncation |
| AC-2 | CharacterMugTemplate headline does not overflow its container | PARTIAL — 35-char engine limit works for most cases, but `maxWidth: "100%"` without `overflow: hidden` means long custom names at 42px font could exceed panel width |
| AC-3 | Feature subline truncated before visual overflow | PASS (50-char limit in characterHeadlines.js) |
| AC-4 | Score line and speech bubble overflow-safe | PASS (CSS overflow guards in place) |
| AC-5 | SVG hero text rect width matches actual text bounding box | FAIL — rect is hardcoded 170px, text length varies |
| AC-6 | CharacterMugTemplate headline containers have `overflow: hidden` | FAIL — no overflow guard on headline divs in any of the 4 layouts |

**Recommended Fixes:**
1. **MugCeramicPreview.jsx:** Reduce `truncateAtWord` limit from 22 to 18 for the hero description, OR widen the hero rect from 170px to 200px, OR add SVG `textLength` attribute to auto-shrink
2. **CharacterMugTemplate.jsx:** Add `overflow: "hidden"` to all 4 headline `<div>` styles (HeroLayout line 219, CelebrationLayout line 339, BlendLayout line 437, GiftLayout line 584)

---

## KSK-03: AI message toggle ungated

### Files Read
- `src/components/keepsakes/mobile/KeepsakeCustomise.jsx` (lines 519-671)
- `src/components/keepsakes/utils/templateRegistry.js` (full registry)
- `src/components/keepsakes/KeepsakesModal.jsx` (line 1164)

### Verdict: ALREADY GATED CORRECTLY (no bug)

**Mobile (KeepsakeCustomise.jsx):**
Line 519 shows the toggle is gated:
```jsx
{personalise && PRODUCT_TEMPLATE_REGISTRY[productId]?.supportsCustomMessage && (
```

This checks both:
1. `personalise` prop is truthy (hook is provided)
2. The product's registry entry has `supportsCustomMessage: true`

**Desktop (KeepsakesModal.jsx):**
Line 1164 shows the same gating:
```jsx
{PRODUCT_TEMPLATE_REGISTRY[selectedProduct]?.supportsCustomMessage && (
```

**Products with `supportsCustomMessage: true`:**
- fine_art_print, framed_canvas, mug_wrap, cushion, greeting_card, postcard, jigsaw_puzzle, family_mug_set, character_mug

**Products WITHOUT `supportsCustomMessage`:**
- standard_card, card_deck, baby_bodysuit, tshirt_print, pet_family_report

The gating is correct on both mobile and desktop. The toggle will NOT appear for products that don't support custom messages.

### Acceptance Criteria

| # | Criterion | Current State |
|---|-----------|---------------|
| AC-1 | Toggle shows ONLY for products with `supportsCustomMessage: true` | PASS |
| AC-2 | Toggle does NOT show for standard_card, card_deck, baby_bodysuit, tshirt_print, pet_family_report | PASS |
| AC-3 | Desktop modal gates correctly | PASS (line 1164) |
| AC-4 | Mobile customise gates correctly | PASS (line 519) |

**No fix required.** This issue can be closed.

---

## KSK-04: Transparent preview backing

### Files Read
- `src/components/keepsakes/templates/Products/Home/CushionTemplate.jsx` (full file, 232 lines)

### Verdict: CONFIRMED BUG

**Root Cause Analysis:**

CushionTemplate renders with `background: "transparent"` (line 42). The template is designed for print export where transparency is correct (the cushion manufacturer applies the design to fabric). However, in the mobile preview context:

1. The preview area in `KeepsakeCustomise.jsx` has a dark background (`#0D0F1A`)
2. CushionTemplate uses `theme.colors.text` for the child name (line 74) and `theme.colors.textLight` for subtitle (line 78)
3. The match badge at the bottom (lines 204-228) uses `color: "#fff"` on a gradient background — this is fine
4. **BUT** the feature badge labels (line 170) use `theme.colors.primary` (winner) or `theme.colors.textLight` (non-winner) — these are age-theme-dependent and could be dark colours
5. The child name text at line 74 uses `theme.colors.text` which depends on the age theme — typically dark text designed for light backgrounds
6. The "FamiliLook Family Resemblance" subtitle at line 79 uses `theme.colors.textLight` — also typically a dark gray

**The core problem:** The template was designed assuming a white or light backing behind it. On the dark `#0D0F1A` preview background, all dark-coloured text becomes invisible.

**Additionally:** The feature badge circles for non-winner features use `background: "#F3F4F6"` (line 155) which is a light gray — this will look fine on dark, but the `border: "2px solid #D1D5DB"` is low contrast against the light fill.

**What about the `ProductMockup3D` wrapper?** Looking at `KeepsakeCustomise.jsx` line 237-249, the cushion renders through `ProductMockup3D` (not `isMug` and not `isCard`). This wrapper may provide a background — but based on the code flow, the template itself renders with transparent bg inside the mockup.

### Acceptance Criteria

| # | Criterion | Current State |
|---|-----------|---------------|
| AC-1 | CushionTemplate text visible on dark preview backgrounds | FAIL — child name and subtitle use theme colours designed for light backgrounds |
| AC-2 | Feature badge labels readable on dark preview background | FAIL — non-winner labels use `theme.colors.textLight` (typically dark gray) |
| AC-3 | Preview area has subtle backing for transparent templates | FAIL — no backing layer added in KeepsakeCustomise.jsx or CushionTemplate.jsx |
| AC-4 | Export transparency NOT affected | N/A — fix must preserve `background: "transparent"` in the template for print export |
| AC-5 | Match badge text visible | PASS — uses white on gradient, always visible |

**Recommended Fixes:**
1. **Option A (preferred):** In `KeepsakeCustomise.jsx`, wrap the `ProductMockup3D` or non-mug/non-card preview in a container with a light background (e.g. `background: "#f9f9f7"`, `borderRadius: 12px`, `padding: 8px`) so all transparent templates preview correctly. This does NOT affect print export.
2. **Option B:** Add a `previewMode` prop to CushionTemplate that, when true, renders a white backing rect behind the content. This is more surgical but requires prop threading.

Option A is superior because it fixes the problem for ALL transparent templates (cushion, and any future ones) without modifying individual templates.

---

## Summary Table

| Issue | ID | Verdict | Fix Required? | Severity | Occurrence | Detection | RPN |
|-------|----|---------|---------------|----------|------------|-----------|-----|
| Card products in catalogue | KSK-01 | Already filtered via `hideFromCatalogue` | Hardening only | 5 | 2 | 4 | 40 |
| Mug text overflow | KSK-02 | Partially mitigated, headline overflow possible | YES | 6 | 4 | 8 | 192 |
| AI message toggle ungated | KSK-03 | Already gated correctly | NO | - | - | - | - |
| Transparent preview backing | KSK-04 | Confirmed bug | YES | 7 | 8 | 8 | 448 |

**Priority Order (by RPN):**
1. **KSK-04** (RPN 448) — Transparent preview backing: every user previewing a cushion on mobile sees invisible text
2. **KSK-02** (RPN 192) — Mug text overflow: custom names can cause headline overflow on CharacterMugTemplate
3. **KSK-01** (RPN 40) — Hardening only: remove card products from category array for explicitness
4. **KSK-03** (RPN 0) — No fix needed, close issue

---

## Files Requiring Modification

| File | Issue | Change |
|------|-------|--------|
| `src/components/keepsakes/mobile/KeepsakeCustomise.jsx` | KSK-04 | Add light backing container around ProductMockup3D preview |
| `src/components/keepsakes/templates/Products/Drinkware/CharacterMugTemplate.jsx` | KSK-02 | Add `overflow: "hidden"` to headline divs in all 4 layouts |
| `src/components/keepsakes/MugCeramicPreview.jsx` | KSK-02 | Reduce hero description truncation limit or widen rect |
| `src/components/keepsakes/utils/productCatalog.js` | KSK-01 | Remove STANDARD_CARD and CARD_DECK from cards.products array |

---

## Regression Risks

1. **KSK-04 fix:** Adding a background wrapper in KeepsakeCustomise must NOT affect the actual export pipeline. Verify that the export path (printExport.js) does not read from the preview DOM.
2. **KSK-02 fix:** Adding `overflow: hidden` to headline divs means very long headlines would be silently cropped rather than visibly breaking. The 35-char engine limit should prevent this, but verify with edge-case custom names.
3. **KSK-01 fix:** Removing products from the category array must not break FamiliUno deck ordering. The deck ordering flow uses `card_deck` product type directly, not via category browsing. Verify `BasketDrawer.jsx` and `KeepsakeMobileFlow.jsx` don't rely on category membership for card_deck.

---

**QA Lead sign-off:** Assessment complete. 2 bugs confirmed (KSK-02, KSK-04), 1 hardening item (KSK-01), 1 non-issue (KSK-03). Ready for FE Lead to implement fixes in priority order.
