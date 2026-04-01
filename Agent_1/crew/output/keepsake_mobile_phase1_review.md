# QA Review: Keepsake Mobile Phase 1 Components

**Author:** QA Lead Agent
**Date:** 2026-04-01
**Scope:** All 7 new Phase 1 mobile keepsake files
**Spec References:**
- `Agent_1/crew/output/keepsake_mobile_shopping_ux_spec.md` (Visual Direction)
- `Agent_1/crew/output/keepsake_mobile_technical_plan.md` (Technical Plan)

---

## Files Reviewed

| # | File | LOC |
|---|------|-----|
| 1 | `src/utils/deviceDetection.js` | 73 |
| 2 | `src/components/keepsakes/mobile/MobileHeader.jsx` | 127 |
| 3 | `src/components/keepsakes/mobile/MobileActionBar.jsx` | 275 |
| 4 | `src/components/keepsakes/mobile/KeepsakeCatalogue.jsx` | 330 |
| 5 | `src/components/keepsakes/mobile/KeepsakeCustomise.jsx` | 417 |
| 6 | `src/components/keepsakes/mobile/KeepsakePreview.jsx` | 387 |
| 7 | `src/components/keepsakes/mobile/KeepsakeMobileFlow.jsx` | 486 |

---

## 1. deviceDetection.js

### A. Spec Alignment
| Item | Verdict | Notes |
|------|---------|-------|
| Breakpoint value | **PASS** | 768px matches standard mobile breakpoint |
| SSR safety | **PASS** | `typeof window !== "undefined"` guards present (lines 19, 31-35) |
| Debounce strategy | **PASS** | Uses `requestAnimationFrame` (line 46), avoids layout thrashing |

### B. Import Verification
| Import | Target | Verdict |
|--------|--------|---------|
| `useState, useEffect` from `react` | React core | **PASS** |

### C. Mobile UX Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Orientation change listener | **PASS** | Line 60 listens for `orientationchange` |
| State deduplication | **PASS** | Lines 50-54 prevent unnecessary re-renders |
| Cleanup | **PASS** | Removes listeners and cancels RAF on unmount (lines 65-69) |

### F. Potential Bugs
| Item | Verdict | Notes |
|------|---------|-------|
| Hooks called unconditionally | **PASS** | No conditional hook calls |
| RAF leak | **PASS** | `cancelAnimationFrame(rafId)` in cleanup (line 66) |

**Overall: PASS -- clean utility, no issues.**

---

## 2. MobileHeader.jsx

### A. Spec Alignment
| Item | Verdict | Notes |
|------|---------|-------|
| Header height | **PASS** | 56px (line 29) -- spec says 44px top bar but 56px includes safe-area + padding, acceptable |
| Back arrow touch target | **PASS** | 44x44px (lines 39-40) |
| Close (X) touch target | **PASS** | 44x44px (lines 91-92) |
| Background colour | **PASS** | `#0D0F1A` (line 23) matches spec |
| Progress bar height | **PASS** | 3px (line 109) matches spec |
| Progress bar colours | **PASS** | Filled: `#7C3AED` (line 116), Empty: `#2a2a4e` (line 110) |
| Safe-area padding | **PASS** | `env(safe-area-inset-top)` (line 22) |
| Title font | **PASS** | 16px weight 600 (lines 59-60) matches H3 spec |
| Subtitle font | **PASS** | 12px weight 400, #9090B0 (lines 70-74) matches Caption spec |
| Back arrow colour | **PASS** | `rgba(255,255,255,0.8)` = white at 80% (line 47) matches spec |

### B. Import Verification
| Import | Target | Verdict |
|--------|--------|---------|
| `ChevronLeft, X` from `lucide-react` | npm package | **PASS** |

### C. Mobile UX Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Spacer when no back arrow | **PASS** | 44x44px spacer div (line 51) keeps title centred |
| Truncation on long titles | **PASS** | `truncate` class on title and subtitle |
| Progress bar clamping | **PASS** | `Math.min(Math.max(progress, 0), 1)` (line 115) |

### F. Potential Bugs
| Item | Verdict | Notes |
|------|---------|-------|
| Missing `aria-label` on progress bar | **WARNING** | Progress bar is `aria-hidden="true"` (line 105) which is acceptable since it's decorative, but no `role="progressbar"` for screen readers. Acceptable for Phase 1. |

**Overall: PASS -- well-structured, spec-compliant.**

---

## 3. MobileActionBar.jsx

### A. Spec Alignment
| Item | Verdict | Notes |
|------|---------|-------|
| Fixed position bottom | **PASS** | `position: fixed, bottom: 0` (lines 182-183) |
| Safe-area padding | **PASS** | `env(safe-area-inset-bottom)` (line 189) |
| Primary CTA height | **WARNING** | 52px (line 203) -- spec says 48px (line 550 of UX spec). Difference is 4px, minor. |
| Primary CTA gradient | **PASS** | `linear-gradient(135deg, #7C3AED, #6D28D9)` (line 207) matches spec |
| Primary CTA border-radius | **PASS** | 12px (line 204) matches spec |
| Primary CTA font | **PASS** | 16px weight 600 (lines 209-210) matches CTA spec |
| Overflow button size | **WARNING** | 52x52px (lines 244-245) -- spec says 44x44px (line 565). Overflow is 52px, 8px larger than spec. |
| Overflow button border | **PASS** | `1px solid #2a2a4e` (line 248) matches spec |
| Overflow button radius | **PASS** | 12px (line 247) matches spec |
| Bottom sheet radius | **PASS** | `16px 16px 0 0` (line 89) matches spec |
| Bottom sheet background | **PASS** | `#1a1a2e` (line 87) matches spec |
| Drag handle | **PASS** | 36x4px pill, `#4a4a6e` (lines 101-105) -- spec says 40x4px `#2a2a4e`. Minor size/colour diff. |
| Sheet action row min-height | **PASS** | 48px (line 157) -- spec says 52px row / 44px touch target. 48px meets 44px touch target minimum. |
| Disabled state | **PASS** | `#3a3a5e` bg, `#6a6a8e` text (lines 205-208) |
| Loading spinner | **PASS** | CSS spinner animation (lines 223-232) |

### B. Import Verification
| Import | Target | Verdict |
|--------|--------|---------|
| `MoreHorizontal, X` from `lucide-react` | npm package | **PASS** |

### C. Mobile UX Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Outside-tap dismiss | **PASS** | `pointerdown` listener on document (lines 29-37) |
| Escape key dismiss | **PASS** | `keydown` listener (lines 41-48) |
| Backdrop overlay | **PASS** | Fixed inset, 60% black opacity (lines 64-74) |

### F. Potential Bugs
| Item | Verdict | Notes |
|------|---------|-------|
| `key={idx}` on secondaryActions map | **WARNING** | Line 148 uses array index as key. If actions are reordered this could cause React reconciliation issues. Low risk since the array is static per render, but `action.label` would be a better key. |
| Missing `type="button"` on overflow toggle | **WARNING** | Line 241 -- the overflow toggle button lacks `type="button"`. Inside a form this could cause unintended submit. Low risk since it's not in a form context. |
| Sheet close button lacks `type="button"` | **WARNING** | Line 126 -- same issue. |
| `slideUpSheet` CSS animation defined inline | **PASS** | Works but creates a `<style>` element each render. Minor perf concern, acceptable for Phase 1. |

### E. Missing Functionality
| Item | Verdict | Notes |
|------|---------|-------|
| Free tier CTA swap | **FAIL** | Spec (tech plan line 470-471): "If `!canOrderMerchandise()` the primary button changes to 'Download PNG'". The MobileActionBar receives `primaryLabel` as a prop and does not gate on plan tier. The **parent** (KeepsakeMobileFlow) must pass the correct label, but it currently always passes `"Add to Basket -- price"`. **The free-tier CTA label is never swapped.** |
| Backdrop-blur on action bar | **WARNING** | Spec says `95% opacity + backdrop-blur 20px` on the action bar background. Implementation uses solid `#0D0F1A` with no blur (line 184). Cosmetic, not functional. |

**Overall: WARNING -- functional but has spec deviations and missing free-tier gate logic in parent.**

---

## 4. KeepsakeCatalogue.jsx

### A. Spec Alignment
| Item | Verdict | Notes |
|------|---------|-------|
| 2-column grid | **PASS** | `gridTemplateColumns: "1fr 1fr"` (line 211) |
| Background colour | **PASS** | `#0D0F1A` (line 121) |
| Card background | **PASS** | `#1a1a2e` (line 223) |
| Card border | **PASS** | `1.5px solid #2a2a4e` (line 224) -- spec says `1px`, minor diff |
| Card border-radius | **WARNING** | 16px (line 225) -- spec says 12px. Visual deviation. |
| Card min-height | **WARNING** | 180px (line 228) -- spec says 220px total card height. Cards are 40px shorter than spec. |
| Product name font | **PASS** | 14px weight 600 (lines 283-284) -- spec says H3 16px. Minor deviation (14 vs 16). |
| Price font | **PASS** | 14px weight 700, `#9090B0` (lines 299-303) -- spec says 16px weight 700. Minor deviation. |
| Badge position | **PASS** | Absolute, top 8px right 8px (lines 247-248) matches spec |
| Badge border-radius | **PASS** | 6px (line 253) matches spec |
| Badge font | **PASS** | 10px weight 700, uppercase, 0.05em spacing (lines 249-252) matches spec |
| Progress bar value | **PASS** | `progress={0.33}` (line 128) matches spec (33%) |
| Category chip height | **PASS** | 40px (line 154) -- spec says 32px chip + 8px padding. Close enough. |
| Category chip radius | **WARNING** | 20px (line 156) -- spec says 16px (pill shape). Minor. |
| Category chip gap | **PASS** | `gap-2` = 8px matches spec |
| Category chip font | **PASS** | 14px (line 164) matches spec |
| Selected chip styling | **PASS** | `rgba(124, 58, 237, 0.2)` bg + `#7C3AED` border (lines 158-161) matches spec |
| Touch target highlight | **PASS** | `WebkitTapHighlightColor: transparent` (line 168) |
| Grid gap | **WARNING** | `gap-3` = 12px (line 209). Spec says 12px horizontal + 12px vertical. **PASS** for values but the spec layout diagram shows 12px which matches. |

### B. Import Verification
| Import | Target | Verdict |
|--------|--------|---------|
| `PRODUCT_CATEGORIES, CATEGORY_ORDER, getCategoryProducts` from `productCatalog.js` | Verified exports | **PASS** |
| `PRODUCT_SPECS` from `printProfiles.js` | Verified export | **PASS** |
| `useCurrency` from `CurrencyContext.jsx` | Verified export | **PASS** |
| `MobileHeader` from `./MobileHeader.jsx` | Local file exists | **PASS** |

### C. Mobile UX Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Horizontal scroll on chips | **PASS** | `overflowX: auto`, `-webkit-overflow-scrolling: touch`, `scrollbarWidth: none` (lines 135-138) |
| No horizontal scroll on grid | **PASS** | Grid uses `1fr 1fr`, no horizontal overflow |
| Empty state | **PASS** | Shows "No products in this category yet" (lines 316-325) |
| Safe-area bottom padding | **PASS** | `paddingBottom: "env(safe-area-inset-bottom, 32px)"` (line 186) |
| Product tap highlight | **PASS** | Border colour changes on `pointerDown/Up/Leave` (lines 232-240) |

### E. Missing Functionality
| Item | Verdict | Notes |
|------|---------|-------|
| Lifestyle product photos | **WARNING** | Spec explicitly calls for lifestyle mockup photographs. Implementation uses `product.icon` (emoji, line 277) as placeholder. Acceptable for Phase 1 (spec acknowledges photos need to be produced), but should be tracked. |
| Image area | **WARNING** | Spec shows a 150px image area with `object-fit: cover`. Implementation has a 64x64px emoji icon area (lines 268-276). This is a significant visual difference from the spec mockup. Phase 1 acceptable as placeholder. |
| Card shadow | **WARNING** | Spec calls for `0 2px 8px rgba(0,0,0,0.3)` card shadow. Not present in implementation. Cosmetic. |
| Single-product category auto-advance | **WARNING** | Tech plan (section 1, para 3): "If a category has only one product, tapping the category auto-selects the product and advances to Customise." Not implemented -- all categories show their product grid. Low priority. |
| Catalogue title | **WARNING** | Spec shows "KEEPSAKES" as H1 in top bar. Implementation uses MobileHeader with `title="Keepsakes"` at H2/16px (not H1/22px). Minor typography mismatch. |

### F. Potential Bugs
| Item | Verdict | Notes |
|------|---------|-------|
| `PRODUCT_SPECS` imported but unused | **WARNING** | Line 8 imports `PRODUCT_SPECS` but the component uses `product.price` and `product.label` from `getCategoryProducts()`. If `getCategoryProducts` returns objects without `price`/`label` the cards will show `undefined`. Need to verify `getCategoryProducts` return shape matches `PRODUCT_SPECS` entry shape. |
| No loading state | **WARNING** | If `FILTER_CHIPS` or products are empty on initial render (e.g. productCatalog.js fails to load), no spinner/skeleton is shown. Edge case. |

**Overall: WARNING -- functionally sound, multiple cosmetic spec deviations, missing lifestyle photos (expected in Phase 1).**

---

## 5. KeepsakeCustomise.jsx

### A. Spec Alignment
| Item | Verdict | Notes |
|------|---------|-------|
| Background colour | **PASS** | `#0D0F1A` (line 79) |
| Back button touch target | **PASS** | 44x44px (lines 99-100) |
| Close button touch target | **PASS** | 44x44px (lines 139-140) |
| Progress bar (66%) | **PASS** | 3-segment bar: 2 filled + 1 empty (lines 162-166) |
| Progress bar colour | **PASS** | `#7C3AED` filled, `#2a2a4e` empty (lines 164-166) |
| Preview area height | **PASS** | `minHeight: "50vh"` (line 185) -- spec says ~200px, 50vh is approximately correct |
| Mug preview width | **WARNING** | 300px (line 207) -- spec says 280px. 20px wider than spec. Minor. |
| Card template render | **PASS** | Cards render template directly (lines 212-224) |
| Non-mug/non-card uses ProductMockup3D | **PASS** | Lines 226-239 |
| Style chip min-height | **PASS** | 44px (line 279) meets touch target minimum |
| Style chip min-width | **WARNING** | 100px (line 278) -- spec says 72px wide, 88px tall with swatch. Implementation is wider, no swatch. Different approach from spec (text chips vs swatch chips). |
| Age chip flex layout | **PASS** | `flex: 1` fills row evenly (line 344) |
| Age chip min-height | **WARNING** | 40px (line 346) -- meets 40px spec minimum but not 44px iOS HIG minimum. |
| CTA button height | **PASS** | 52px (line 396) matches spec |
| CTA gradient | **PASS** | `linear-gradient(135deg, #7C3AED, #6D28D9)` (line 399) |
| CTA border-radius | **PASS** | 12px (line 397) |
| Section label styling | **PASS** | 12px uppercase `#9090B0` (lines 249-254) -- spec uses H3 16px for section labels. Different approach but functional. |

### B. Import Verification
| Import | Target | Verdict |
|--------|--------|---------|
| `getProductStyles, getTemplateComponent, getPreviewStyleVariant` from `templateRegistry.js` | Verified exports | **PASS** |
| `AGE_BRACKETS, getAgeTheme` from `ageThemes.js` | Verified exports | **PASS** (note: `AGE_BRACKETS` imported but unused) |
| `PRODUCT_SPECS` from `printProfiles.js` | Verified export | **PASS** |
| `MugCeramicPreview` from `../MugCeramicPreview.jsx` | File exists | **PASS** |
| `ProductMockup3D` lazy import from `../ProductMockup3D.jsx` | File exists | **PASS** |

### C. Mobile UX Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Scrollable content area | **PASS** | `overflowY: auto` with `-webkit-overflow-scrolling: touch` (lines 170-174) |
| Bottom padding for fixed CTA | **PASS** | `paddingBottom: 80` (line 175) prevents content hiding behind fixed bar |
| Fixed bottom CTA with safe-area | **PASS** | `position: fixed`, `env(safe-area-inset-bottom)` (lines 380-389) |
| Style chips horizontal scroll | **PASS** | `overflowX: auto`, hidden scrollbar (lines 260-267) |
| Lazy-loaded ProductMockup3D | **PASS** | `Suspense` with loading fallback (lines 188-200) |

### D. Data Flow Verification
| Item | Verdict | Notes |
|------|---------|-------|
| `handleContinue` passes selections up | **PASS** | Passes `{ style, ageTheme }` to `onContinue` (line 67) |
| Default style selection | **PASS** | Uses first available style or "default" (lines 46-48) |
| Default age selection | **PASS** | Defaults to "child" (line 49) |

### E. Missing Functionality
| Item | Verdict | Notes |
|------|---------|-------|
| Recipient selector | **FAIL** | Desktop KeepsakesModal has recipient selection (self/for_winner/for_loser/grandparent) for character_mug. Mobile KeepsakeCustomise does not implement this. Spec (UX spec lines 421-423) shows "Recipient input" for character_mug and greeting_card. **Missing from Phase 1.** |
| Variant toggle | **FAIL** | Spec shows variant toggle (Mum/Dad for family_mug_set, Front/Inside for greeting_card, Front/Back for postcard). Not implemented. |
| Personalised message toggle | **FAIL** | Desktop KeepsakesModal has `usePersonalizedMessage` toggle with LLM-generated text. Mobile KeepsakeCustomise does not expose any UI for enabling/toggling personalised messages. The hook IS used in KeepsakeMobileFlow but no UI controls exist to toggle it or show the generated message. |
| `AGE_BRACKETS` unused import | **WARNING** | Line 8 imports `AGE_BRACKETS` but uses hardcoded `AGE_CHIPS` array instead (lines 22-26). Not a bug but wasteful import. |

### F. Potential Bugs
| Item | Verdict | Notes |
|------|---------|-------|
| Hooks called unconditionally | **PASS** | All hooks at top level |
| Key props in map() | **PASS** | `key={style.id}` (line 274), `key={chip.id}` (line 339) |
| No `MobileHeader` used | **WARNING** | KeepsakeCustomise builds its own header (lines 86-167) instead of using the shared `MobileHeader` component. This creates visual inconsistency risk. The Catalogue uses `MobileHeader` but Customise and Preview do not. |
| Progress bar implementation differs | **WARNING** | Catalogue uses `MobileHeader` progress prop (continuous bar). Customise uses 3-segment bar (lines 157-167). Preview also uses 3-segment. The visual behaviour differs between screens. Not a bug but inconsistency. |

**Overall: FAIL -- missing recipient selector, variant toggle, and personalised message UI that exist in desktop flow and are called out in spec.**

---

## 6. KeepsakePreview.jsx

### A. Spec Alignment
| Item | Verdict | Notes |
|------|---------|-------|
| Background colour | **PASS** | `#0D0F1A` (line 121) |
| Back button touch target | **PASS** | 44x44px (lines 140-141) |
| Close button touch target | **PASS** | 44x44px (lines 181-182) |
| Progress bar (100%) | **PASS** | All 3 segments filled with `#7C3AED` (lines 205-208) |
| Mockup preview width | **PASS** | 340px for mugs and fallback (lines 248, 270) matches spec |
| Preview area height | **PASS** | `minHeight: "60vh"` (line 226) matches spec (~60% viewport) |
| Product name font | **PASS** | 16px weight 600 (lines 288-290) |
| Style subtitle font | **PASS** | 13px `#9090B0` (lines 294-296) |
| MobileActionBar integration | **PASS** | `primaryLabel` includes price (line 380) |
| Hidden export div | **PASS** | `position: absolute, left: -9999px`, `ref={cardRef}` (lines 364-366) matches spec |
| View flat design toggle | **PASS** | Toggle button with min-height 44px (line 319) matches spec |
| Flat design panel | **PASS** | Renders in `#1a1a2e` card with border (lines 329-359) |

### B. Import Verification
| Import | Target | Verdict |
|--------|--------|---------|
| `Download, Share2, ShoppingCart` from `lucide-react` | npm package | **PASS** |
| `getTemplateComponent, getPreviewStyleVariant` from `templateRegistry.js` | Verified exports | **PASS** |
| `PRODUCT_SPECS` from `printProfiles.js` | Verified export | **PASS** |
| `getAgeTheme` from `ageThemes.js` | Verified export | **PASS** |
| `exportCardAsPng, exportAndDownloadCard, generateKeepsakeFilename` from `cardExport.js` | Verified exports | **PASS** |
| `MugCeramicPreview` from `../MugCeramicPreview.jsx` | File exists | **PASS** |
| `MobileActionBar` from `./MobileActionBar.jsx` | File exists | **PASS** |
| `ProductMockup3D` lazy import | File exists | **PASS** |

### C. Mobile UX Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Large centred mockup | **PASS** | 340px width, centred in 60vh container |
| Mug uses MugCeramicPreview | **PASS** | Not flat template (line 245-250) |
| Card uses direct template | **PASS** | Lines 254-265 |
| Hidden export template | **PASS** | Off-screen at `-9999px` (line 366) |
| Padding for fixed bottom bar | **PASS** | `paddingBottom: 88` (line 217) |

### D. Data Flow Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Secondary actions built from props | **PASS** | onExport, onShare, onBuyNow mapped to overflow menu (lines 89-113) |
| Hidden template renders full resolution | **PASS** | TemplateComponent in off-screen div (lines 369-375) |

### E. Missing Functionality
| Item | Verdict | Notes |
|------|---------|-------|
| 3D Video toggle for mugs | **WARNING** | Tech plan (section 4, "3D Video Mockup") says mug_wrap should have a "3D Preview" toggle to play the MP4 mockup video. Not implemented. Lower priority for Phase 1. |
| Product name + price below mockup | **PASS** | Lines 286-303 |

### F. Potential Bugs
| Item | Verdict | Notes |
|------|---------|-------|
| `require()` in useMemo | **WARNING** | Lines 74-76 use `require("../utils/templateRegistry.js")` inside a `useMemo`. In a Vite ESM environment, `require` may not be available. This will throw at runtime. Should use the already-imported functions or a separate import. **This is a potential runtime error.** |
| `exportCardAsPng` and `exportAndDownloadCard` imported but unused | **WARNING** | Lines 11 imported but all export/share/basket logic is in `KeepsakeMobileFlow.jsx`, not in KeepsakePreview. These imports are dead code. Not a bug but adds bundle weight. |
| `generateKeepsakeFilename` imported but unused | **WARNING** | Same as above (line 11). Dead code. |
| No `MobileHeader` used | **WARNING** | Same issue as KeepsakeCustomise -- builds its own header instead of reusing MobileHeader. |

**Overall: WARNING -- mostly solid, but `require()` in useMemo (line 74) is a potential runtime error in Vite.**

---

## 7. KeepsakeMobileFlow.jsx

### A. Spec Alignment
| Item | Verdict | Notes |
|------|---------|-------|
| Full-screen fixed positioning | **PASS** | `position: fixed, inset: 0, zIndex: 400` (lines 423-427) |
| Background colour | **PASS** | `#0D0F1A` (line 426) |
| AnimatePresence mode | **PASS** | `mode="wait"` (line 431) prevents simultaneous old+new renders |
| Slide variants match spec | **PASS** | Forward: enter from right (`100%`), exit to left (`-100%`). Back: enter from left (`-100%`), exit to right (`100%`). Lines 401-413. Matches spec exactly. |
| Transition duration | **PASS** | 0.25s tween easeInOut (lines 415-419) matches spec (250ms) |
| Feature flag gate | **PASS** | `fl:disable-mobile-keepsakes` localStorage check (line 73) |

### B. Import Verification
| Import | Target | Verdict |
|--------|--------|---------|
| `AnimatePresence, motion` from `framer-motion` | npm package | **PASS** |
| `useKeepsakeData` from `hooks/useKeepsakeData.js` | File exists, export verified | **PASS** |
| `useGroupPairwiseKeepsakeData` from `hooks/useGroupPairwiseKeepsakeData.js` | File exists | **PASS** |
| `usePetKeepsakeData` from `hooks/usePetKeepsakeData.js` | File exists | **PASS** |
| `useFamilyKeepsakeData` from `hooks/useFamilyKeepsakeData.js` | File exists | **PASS** |
| `usePersonalizedMessage` from `hooks/usePersonalizedMessage.js` | File exists, export verified | **PASS** |
| `exportCardAsPng, exportAndDownloadCard, generateKeepsakeFilename` from `cardExport.js` | Verified exports | **PASS** |
| `PRODUCT_SPECS` from `printProfiles.js` | Verified export | **PASS** |
| `PRODUCT_TEMPLATE_REGISTRY, getTemplateComponent, getPreviewStyleVariant, buildTemplateKey` from `templateRegistry.js` | Verified exports | **PASS** |
| `getAgeTheme` from `ageThemes.js` | Verified export | **PASS** |
| `usePlanFeatures` from `hooks/usePlanFeatures.js` | File exists, `canOrderMerchandise` in return value | **PASS** |
| `useBasket` from `state/BasketContext.jsx` | Verified export | **PASS** |
| `useToast` from `components/ui/Toast.jsx` | Verified export | **PASS** |
| `useBodyModalFlag` from `hooks/useBodyModalFlag.js` | Verified export | **PASS** |
| `logger` from `utils/logger.js` | File exists | **PASS** |
| `analytics` from `utils/analytics.js` | File exists | **PASS** |
| `KeepsakeCatalogue` from `./KeepsakeCatalogue.jsx` | File exists | **PASS** |
| `KeepsakeCustomise` from `./KeepsakeCustomise.jsx` | File exists | **PASS** |
| `KeepsakePreview` from `./KeepsakePreview.jsx` | File exists | **PASS** |

**All 19 imports verified. No broken imports.**

### C. Mobile UX Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Browser back button (popstate) | **PASS** | `history.pushState` + `popstate` listener (lines 163-183) |
| Back from catalogue closes flow | **PASS** | Line 169 |
| Back from customise goes to catalogue | **PASS** | Line 172 |
| Back from preview goes to customise | **PASS** | Line 176 |
| Re-pushes history on back | **PASS** | Lines 174, 178 prevent back-button breaking after navigation |
| Direction tracking | **PASS** | `direction` state drives slide animation direction (lines 135-136) |
| `will-change: transform` | **PASS** | Line 443 -- GPU acceleration hint for animation |

### D. Data Flow Verification
| Item | Verdict | Notes |
|------|---------|-------|
| Mode detection (pairwise/pet/individual) | **PASS** | Lines 106-107 |
| Data source resolution | **PASS** | Lines 113-121 correctly select data based on mode |
| Family product data switching | **PASS** | Lines 152-153 -- switches to `familyData` for family products |
| Null data guard | **PASS** | Lines 369-390 -- shows fallback message |
| Export handler adapted from desktop | **PASS** | Lines 210-243 -- same pipeline: `exportAndDownloadCard` with correct params |
| Share handler with native share fallback chain | **PASS** | Lines 246-294 -- native share with file -> native share text-only -> clipboard fallback |
| AbortError handling in share | **PASS** | Line 289 -- ignores user cancellation |
| Add to basket payload | **PASS** | Lines 320-338 -- matches desktop `basket.addItem` structure with `productType`, `cardTypeId`, `pngDataUrl`, `unitPricePence`, `quantity`, `personalizedMessage`, etc. |
| Buy Now delegates to addToBasket | **PASS** | Lines 353-366 -- Phase 1 approach (add to basket + toast), OrderModal deferred to Phase 2 |
| `onCardGenerated` callback | **PASS** | Lines 223-229 -- fires with correct payload after export |
| Analytics events | **PASS** | `keepsake_exported`, `keepsake_shared`, `keepsake_added_to_basket` all tracked with `source: "mobile_flow"` |

### E. Missing Functionality
| Item | Verdict | Notes |
|------|---------|-------|
| `canOrderMerchandise` imported but not used in UI | **FAIL** | `usePlanFeatures()` is called (line 127) and `canOrderMerchandise` destructured, but **never used to gate the UI**. Free-tier users see "Add to Basket" with pricing, can trigger basket add, and will presumably hit a paywall later -- but the spec says the primary CTA should change to "Download PNG" for free tier. |
| Personalised message UI controls | **FAIL** | `usePersonalizedMessage()` is called (line 124) and `personalise.message` is passed into basket payload (line 334), but there is **no UI anywhere in the mobile flow** for the user to toggle personalisation on/off or see the generated message. The desktop modal has a toggle button + message display. |
| Recipient selection | **FAIL** | Desktop has `selectedRecipient` state with 4 options. Mobile flow has no equivalent. |
| Multiple children support (child selector) | **WARNING** | The mobile flow receives `childIndex` as a prop and uses it. The parent component is responsible for child selection before opening the flow. This matches the desktop pattern (desktop also receives childIndex). However, the desktop modal may allow switching children within the modal -- the mobile flow does not. Acceptable for Phase 1. |
| OrderModal integration | **WARNING** | "Buy Now" currently just adds to basket (lines 353-366). Desktop has full `OrderModal` integration. Tech plan explicitly says "Phase 2" for this. Acceptable. |
| `getTemplateComponent` and `getPreviewStyleVariant` imported but unused | **WARNING** | Lines 20 -- these are used in KeepsakeCustomise and KeepsakePreview directly, not in the flow orchestrator. Dead imports. |

### F. Potential Bugs
| Item | Verdict | Notes |
|------|---------|-------|
| React Rules of Hooks -- conditional returns before hooks | **CRITICAL FAIL** | Lines 73-74: `if (localStorage.getItem(...)) return null;` and lines 77: `if (!isOpen) return null;` -- these are **conditional returns before any hooks are called** in the outer `KeepsakeMobileFlow` component. However, this is actually SAFE because the outer component calls NO hooks. All hooks are in `KeepsakeMobileFlowInner` (line 96+). The outer component is a pure gate. **PASS after analysis.** |
| `handleAddToBasket` called inside `handleBuyNow` | **WARNING** | Line 358 calls `await handleAddToBasket()`. But `handleAddToBasket` calls `setIsAdding(true)` on line 299, then checks `if (isAdding) return` on line 298. Meanwhile `handleBuyNow` checks `isOrdering` (line 354). If `handleBuyNow` is called while `isAdding` is true from a previous basket add, the inner call will bail. Race condition is possible but unlikely with UI-driven clicks. |
| `cardRef` in KeepsakeMobileFlow | **WARNING** | `cardRef` is declared (line 148) but **no hidden export div is rendered in KeepsakeMobileFlow**. The hidden export div with `ref={cardRef}` is in KeepsakePreview.jsx (line 364), but KeepsakePreview uses its OWN `cardRef` (line 54). The flow's `cardRef` is **never attached to any DOM element**. The export/share/basket handlers in KeepsakeMobileFlow reference `cardRef.current` (lines 211, 247, 298) which will always be `null`. **This means export, share, and add-to-basket will silently fail.** |

**^^ THIS IS A P0 BUG: The `cardRef` in KeepsakeMobileFlow is never attached to a DOM element. All export/share/basket operations will fail because `cardRef.current` is always `null`.**

| Item | Verdict | Notes |
|------|---------|-------|
| KeepsakePreview has its own cardRef | **RELATED** | KeepsakePreview.jsx line 54 creates its own `const cardRef = useRef(null)` and attaches it to the hidden export div (line 364). But the export handlers live in KeepsakeMobileFlow, not in KeepsakePreview. There is a **complete disconnect** between where the ref is attached and where it is used. |
| `useEffect` popstate cleanup concern | **WARNING** | Lines 163-183: The popstate listener closes over `screen`, `onClose`, and `goTo`. The dependency array includes these (line 183). On each screen change, the old listener is removed and a new one added, which is correct. However, `pushState` is called once on mount (line 165) but also inside the handler (lines 174, 178). Multiple `pushState` calls could stack history entries. Minor UX concern -- pressing back multiple times quickly could behave unexpectedly. |

**Overall: FAIL -- P0 bug with disconnected `cardRef`. Export, share, and basket operations will all fail at runtime.**

---

## Summary Matrix

| File | Spec | Imports | Mobile UX | Data Flow | Missing | Bugs | Overall |
|------|------|---------|-----------|-----------|---------|------|---------|
| deviceDetection.js | PASS | PASS | PASS | N/A | N/A | PASS | **PASS** |
| MobileHeader.jsx | PASS | PASS | PASS | N/A | N/A | PASS | **PASS** |
| MobileActionBar.jsx | WARNING | PASS | PASS | N/A | WARNING | WARNING | **WARNING** |
| KeepsakeCatalogue.jsx | WARNING | PASS | PASS | N/A | WARNING | WARNING | **WARNING** |
| KeepsakeCustomise.jsx | WARNING | PASS | PASS | PASS | FAIL | WARNING | **FAIL** |
| KeepsakePreview.jsx | PASS | PASS | PASS | PASS | WARNING | WARNING | **WARNING** |
| KeepsakeMobileFlow.jsx | PASS | PASS | PASS | **FAIL** | FAIL | **FAIL** | **FAIL** |

---

## Critical Issues (Must Fix Before Merge)

### P0: `cardRef` Disconnected -- All Export/Share/Basket Operations Will Fail

**File:** `KeepsakeMobileFlow.jsx` line 148 + lines 211, 247, 298
**File:** `KeepsakePreview.jsx` line 54 + line 364

**Problem:** The orchestrator (`KeepsakeMobileFlow`) declares `const cardRef = useRef(null)` and uses it in `handleExport`, `handleShare`, and `handleAddToBasket`. But this ref is never attached to any DOM element. Meanwhile, `KeepsakePreview` declares its own separate `cardRef` and attaches it to the hidden export div. The two refs are completely independent.

**Effect:** Every call to export, share, or add-to-basket will hit `if (!cardRef.current) return` and silently do nothing. The user taps "Add to Basket" and nothing happens. No error shown.

**Fix:** Either:
1. Pass `cardRef` from `KeepsakeMobileFlow` down to `KeepsakePreview` as a prop and remove KeepsakePreview's local ref, OR
2. Move the export/share/basket handlers into `KeepsakePreview` and use its local ref, OR
3. Render the hidden export div in `KeepsakeMobileFlow` (outside the AnimatePresence) so it persists across screen transitions, and remove the one in KeepsakePreview.

**Recommendation:** Option 3 is best. The hidden export template should live in the orchestrator so it persists when the user navigates back/forward. Moving it out of `KeepsakePreview` also means the export source survives AnimatePresence unmounting.

### P0: `require()` Will Throw in Vite ESM

**File:** `KeepsakePreview.jsx` lines 74-76

**Problem:** `const { getProductStyles } = require("../utils/templateRegistry.js")` inside a `useMemo`. Vite uses ESM by default and `require` is not available unless explicitly configured. This will throw `ReferenceError: require is not defined` at runtime when the user navigates to the Preview screen.

**Fix:** Import `getProductStyles` at the top of the file (it's already exported from `templateRegistry.js`) and use it directly. The "circular deps" comment (line 73) is incorrect -- `getProductStyles` is already imported in `KeepsakeCustomise.jsx` from the same file without issues.

---

## High Priority Issues (Should Fix Before Deploy)

### H1: Free-Tier CTA Not Gated

**Files:** `KeepsakeMobileFlow.jsx` line 127, `MobileActionBar.jsx`

**Problem:** `canOrderMerchandise` is destructured from `usePlanFeatures()` but never used. Free-tier users see "Add to Basket -- price" and can attempt to add items. The spec and tech plan both state the primary CTA should change to "Download PNG" for free tier.

### H2: Missing Personalised Message UI

**Files:** `KeepsakeCustomise.jsx`, `KeepsakeMobileFlow.jsx` line 124

**Problem:** `usePersonalizedMessage()` hook is called but no toggle/display UI exists. Users cannot enable or view personalised messages in the mobile flow, even though the desktop flow supports this.

### H3: Missing Recipient Selector for Character Mug

**File:** `KeepsakeCustomise.jsx`

**Problem:** Desktop flow has a 4-option recipient selector (Self / For Winner Parent / For Loser Parent / Grandparent) that affects template rendering for `character_mug`. Mobile flow omits this entirely. Character mug orders will default to "self" with no ability to change.

### H4: Missing Variant Toggle

**File:** `KeepsakeCustomise.jsx`

**Problem:** Desktop flow has variant toggles (Mum/Dad for `family_mug_set`, Front/Inside for `greeting_card`). Mobile flow omits these. Users cannot view/select product variants.

---

## Medium Priority Issues (Fix in Phase 2)

| ID | File | Issue |
|----|------|-------|
| M1 | KeepsakeCustomise.jsx | Does not use shared `MobileHeader` component -- builds its own header, creating visual inconsistency |
| M2 | KeepsakePreview.jsx | Does not use shared `MobileHeader` component -- same issue |
| M3 | KeepsakePreview.jsx | Dead imports: `exportCardAsPng`, `exportAndDownloadCard`, `generateKeepsakeFilename` (all logic is in Flow) |
| M4 | KeepsakeMobileFlow.jsx | Dead imports: `getTemplateComponent`, `getPreviewStyleVariant` |
| M5 | KeepsakeCatalogue.jsx | Dead import: `PRODUCT_SPECS` (uses `product.price` from getCategoryProducts) |
| M6 | KeepsakeCustomise.jsx | Dead import: `AGE_BRACKETS` (uses hardcoded AGE_CHIPS) |
| M7 | KeepsakeCatalogue.jsx | Card border-radius 16px vs spec 12px |
| M8 | KeepsakeCatalogue.jsx | Card min-height 180px vs spec 220px |
| M9 | MobileActionBar.jsx | Overflow button 52px vs spec 44px |
| M10 | MobileActionBar.jsx | Missing `backdrop-blur` on action bar |
| M11 | KeepsakeCatalogue.jsx | Missing card shadow per spec |
| M12 | KeepsakePreview.jsx | Missing 3D video toggle for mugs |
| M13 | KeepsakeMobileFlow.jsx | OrderModal not integrated (Buy Now just adds to basket) |

---

## Positive Observations

1. **Clean component architecture** -- separation of concerns between orchestrator, catalogue, customise, and preview is well-executed.
2. **Correct AnimatePresence direction** -- forward slides left, back slides right, matching the spec exactly.
3. **Browser back button** -- `popstate` integration is thorough and handles all three screens correctly.
4. **Safe-area handling** -- consistent use of `env(safe-area-inset-*)` across all fixed-position elements.
5. **Touch targets** -- all back/close buttons meet the 44px minimum. Primary CTAs meet 52px.
6. **Data flow** -- mode detection (individual/pairwise/pet/family) is correctly implemented.
7. **Feature flag** -- `fl:disable-mobile-keepsakes` localStorage toggle allows easy rollback.
8. **Hooks architecture** -- the outer/inner component pattern in KeepsakeMobileFlow correctly avoids conditional hook calls.
9. **All 19 imports verified** -- every imported file and export exists. No missing dependencies.
10. **No new npm dependencies** -- uses only existing packages as required by the tech plan.

---

## Verdict

**CONDITIONAL FAIL** -- Two P0 bugs must be fixed before this code can be merged:

1. **`cardRef` disconnection** -- export/share/basket will all silently fail
2. **`require()` in Vite** -- Preview screen will throw at runtime

After P0 fixes, the code is functionally viable for Phase 1 deployment with the understanding that personalised messages, recipient selection, variant toggles, and free-tier gating are deferred. These should be tracked as Phase 2 tasks.

---

*QA Lead Agent -- 2026-04-01*
